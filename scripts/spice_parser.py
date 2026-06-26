#!/usr/bin/env python3
"""
SPICE Netlist Parser for circuit-diagram skill.

Parses standard SPICE netlists (.cir files) and extracts component
information into JSON for downstream SchemDraw code generation.

Supports:
  - Passive components: R, C, L
  - Active components: D, Q, M, J
  - Sources: V, I
  - Subcircuits: X
  - Models: .MODEL
  - Subcircuit definitions: .SUBCKT ... .ENDS
  - Comments: * (leading) and ; (inline, limited)
  - Continuation lines: + at start of line

Usage:
    python3 spice_parser.py netlist.cir --json output.json
    python3 spice_parser.py netlist.cir --summary
    cat netlist.cir | python3 spice_parser.py --stdin --json output.json
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

# ── component type dispatch ──────────────────────────────────────────────
COMPONENT_KEY_MAP = {
    "R": "resistor",
    "C": "capacitor",
    "L": "inductor",
    "D": "diode",
    "Q": "bjt",
    "M": "mosfet",
    "J": "jfet",
    "V": "vsource",
    "I": "isource",
    "X": "subcircuit",
    "K": "coupling",  # mutual inductance coupling
}

# ── data classes ──────────────────────────────────────────────────────────

@dataclass
class Component:
    """A single SPICE component instance."""
    type: str           # resistor, capacitor, inductor, diode, bjt, mosfet, etc.
    designation: str    # e.g. R1, C2, Q3
    nodes: list[str]    # list of node names
    value: str          # e.g. 1k, 10uF, 2N2222
    params: dict[str, str] = field(default_factory=dict)  # extra parameters
    line: int = 0       # original line number


@dataclass
class Model:
    """A .MODEL definition."""
    name: str
    type: str           # e.g. NPN, PNP, NMOS, PMOS, D
    params: dict[str, str] = field(default_factory=dict)
    line: int = 0


@dataclass
class SubcircuitDef:
    """A .SUBCKT ... .ENDS definition."""
    name: str
    external_nodes: list[str] = field(default_factory=list)
    components: list[Component] = field(default_factory=list)
    models: list[Model] = field(default_factory=list)
    lines: list[str] = field(default_factory=list)
    line_start: int = 0
    line_end: int = 0


@dataclass
class Netlist:
    """Top-level parsed netlist structure."""
    title: str = ""
    components: list[Component] = field(default_factory=list)
    models: list[Model] = field(default_factory=list)
    subcircuits: list[SubcircuitDef] = field(default_factory=list)
    global_nodes: list[str] = field(default_factory=list)  # .GLOBAL nodes
    options: dict[str, str] = field(default_factory=dict)
    analysis: list[str] = field(default_factory=list)  # .OP, .AC, .TRAN, .DC
    raw_lines: int = 0


# ── parser ────────────────────────────────────────────────────────────────

SPICE_COMMENT_RE = re.compile(r"^\s*\*")         # * comment
SEMICOLON_COMMENT_RE = re.compile(r";.*$")        # inline ; comment
CONTINUATION_RE = re.compile(r"^\s*\+")           # continuation line
MODEL_RE = re.compile(
    r"\.MODEL\s+(\w+)\s+(\w+)\s*\((.*)\)",
    re.IGNORECASE,
)
SUBCKT_START_RE = re.compile(
    r"\.SUBCKT\s+(\w+)\s+(.*)",
    re.IGNORECASE,
)
ENDS_RE = re.compile(r"\.ENDS", re.IGNORECASE)
GLOBAL_RE = re.compile(
    r"\.GLOBAL\s+(.*)",
    re.IGNORECASE,
)
OPTION_RE = re.compile(
    r"\.OPTIONS?\s+(.*)",
    re.IGNORECASE,
)
ANALYSIS_RE = re.compile(
    r"\.(OP|AC|DC|TRAN|TF|NOISE|SENS|FOURIER|DISTO|PZ)\b",
    re.IGNORECASE,
)
END_RE = re.compile(r"\.END", re.IGNORECASE)


def _clean_line(line: str) -> str:
    """Remove comments and strip whitespace."""
    line = SEMICOLON_COMMENT_RE.sub("", line)
    # Strip leading * from full-line comments (handled by caller)
    return line.strip()


def _merge_continuations(lines: list[str]) -> list[tuple[str, int]]:
    """Merge + continuation lines into the previous line. Returns (merged_line, original_line_number)."""
    merged: list[tuple[str, int]] = []
    for i, line in enumerate(lines):
        line_num = i + 1
        stripped = line.strip()
        if not stripped or SPICE_COMMENT_RE.match(line):
            continue
        if CONTINUATION_RE.match(stripped):
            if merged:
                prev_text, prev_num = merged.pop()
                merged.append((prev_text + " " + stripped[1:].strip(), prev_num))
        else:
            merged.append((stripped, line_num))
    return merged


def _parse_component_line(text: str, line_num: int) -> Optional[Component]:
    """Parse a single component line like 'R1 n1 n2 1k' or 'Q1 c b e 2N2222'."""
    parts = text.split()
    if len(parts) < 2:
        return None

    designation = parts[0]
    comp_type_key = designation[0].upper()

    if comp_type_key not in COMPONENT_KEY_MAP:
        return None

    comp_type = COMPONENT_KEY_MAP[comp_type_key]

    if comp_type in ("resistor", "capacitor", "inductor", "diode"):
        # Format: Rname n+ n- value [params...]
        if len(parts) < 4:
            return None
        nodes = [parts[1], parts[2]]
        value = parts[3]
        params = {}
        for p in parts[4:]:
            if "=" in p:
                k, v = p.split("=", 1)
                params[k] = v
        return Component(
            type=comp_type,
            designation=designation,
            nodes=nodes,
            value=value,
            params=params,
            line=line_num,
        )

    elif comp_type == "bjt":
        # Qname nc nb ne [ns] model [params...]
        if len(parts) < 5:
            return None
        nodes = [parts[1], parts[2], parts[3]]
        if len(parts) >= 6:
            nodes.append(parts[4])  # substrate node
            value = parts[5]
        else:
            value = parts[4]
        params = {}
        rem = parts[6:] if len(parts) >= 6 else parts[5:]
        for p in rem:
            if "=" in p:
                k, v = p.split("=", 1)
                params[k] = v
        return Component(
            type=comp_type,
            designation=designation,
            nodes=nodes,
            value=value,
            params=params,
            line=line_num,
        )

    elif comp_type in ("mosfet", "jfet"):
        # Mname nd ng ns nb model [params...]
        if len(parts) < 6:
            return None
        nodes = [parts[1], parts[2], parts[3], parts[4]]
        value = parts[5]
        params = {}
        for p in parts[6:]:
            if "=" in p:
                k, v = p.split("=", 1)
                params[k] = v
        return Component(
            type=comp_type,
            designation=designation,
            nodes=nodes,
            value=value,
            params=params,
            line=line_num,
        )

    elif comp_type in ("vsource", "isource"):
        # Vname n+ n- [DC/AC/SIN/PULSE...] value [params...]
        if len(parts) < 4:
            return None
        nodes = [parts[1], parts[2]]
        # Determine if there's a source type keyword
        offset = 3
        params = {}
        source_type = parts[3].upper()
        if source_type in ("DC", "AC", "SIN", "PULSE", "EXP", "SFFM", "AM", "TRNOISE"):
            offset = 4
            params["source_type"] = parts[3]
        value = parts[offset] if offset < len(parts) else ""
        for p in parts[offset + 1 :]:
            if "=" in p:
                k, v = p.split("=", 1)
                params[k] = v
            else:
                # positional parameters for source waveforms
                idx = len([x for x in params if x.startswith("param")])
                params[f"param{idx + 1}"] = p
        return Component(
            type=comp_type,
            designation=designation,
            nodes=nodes,
            value=value,
            params=params,
            line=line_num,
        )

    elif comp_type == "subcircuit":
        # Xname node1 node2 ... subckt_name [params...]
        if len(parts) < 3:
            return None
        # Last non-param token is the subcircuit name
        # Find the subcircuit name (last token without =)
        subckt_idx = len(parts) - 1
        for j in range(len(parts) - 1, 0, -1):
            if "=" not in parts[j]:
                subckt_idx = j
                break
        nodes = parts[1:subckt_idx]
        value = parts[subckt_idx]
        params = {}
        for p in parts[subckt_idx + 1 :]:
            if "=" in p:
                k, v = p.split("=", 1)
                params[k] = v
        return Component(
            type=comp_type,
            designation=designation,
            nodes=nodes,
            value=value,
            params=params,
            line=line_num,
        )

    elif comp_type == "coupling":
        # Kname L1 L2 [L3 ...] coeff
        if len(parts) < 4:
            return None
        nodes = parts[2:-1]
        value = parts[-1]
        return Component(
            type=comp_type,
            designation=designation,
            nodes=nodes,
            value=value,
            line=line_num,
        )

    return None


def parse_netlist(text: str) -> Netlist:
    """Parse a SPICE netlist from a string into a Netlist object."""
    lines = text.splitlines()
    # Capture title from first non-empty line
    title = ""
    raw_lines = text.splitlines()
    for raw_line in raw_lines:
        stripped = raw_line.strip()
        if stripped:
            title = stripped
            break
    netlist = Netlist(raw_lines=len(raw_lines), title=title)

    merged = _merge_continuations(lines)

    # Title already captured from raw lines above; skip in merged loop
    title_set = True
    in_subcircuit: Optional[SubcircuitDef] = None

    for text_line, line_num in merged:

        # Title — first line is always the title in SPICE
        if not title_set:
            netlist.title = text_line
            title_set = True
            continue

        upper = text_line.upper()

        # .END
        if END_RE.match(upper):
            break

        # Inside a .SUBCKT definition
        if in_subcircuit is not None:
            if ENDS_RE.match(upper):
                in_subcircuit.line_end = line_num
                in_subcircuit.lines.append(text_line)
                netlist.subcircuits.append(in_subcircuit)
                in_subcircuit = None
                continue
            in_subcircuit.lines.append(text_line)
            # Also parse components inside subcircuit
            comp = _parse_component_line(text_line, line_num)
            if comp:
                in_subcircuit.components.append(comp)
            continue

        # .SUBCKT start
        m = SUBCKT_START_RE.match(text_line)
        if m:
            name = m.group(1)
            nodes_str = m.group(2).strip()
            external_nodes = nodes_str.split() if nodes_str else []
            in_subcircuit = SubcircuitDef(
                name=name,
                external_nodes=external_nodes,
                line_start=line_num,
                lines=[text_line],
            )
            continue

        # .MODEL
        m = MODEL_RE.match(text_line)
        if m:
            model_name = m.group(1)
            model_type = m.group(2)
            params_str = m.group(3)
            params = {}
            for chunk in re.split(r"\s+", params_str):
                if "=" in chunk:
                    k, v = chunk.split("=", 1)
                    params[k.strip()] = v.strip()
            netlist.models.append(
                Model(name=model_name, type=model_type, params=params, line=line_num)
            )
            continue

        # .GLOBAL
        m = GLOBAL_RE.match(text_line)
        if m:
            netlist.global_nodes = m.group(1).split()
            continue

        # .OPTIONS / .OPTION
        m = OPTION_RE.match(text_line)
        if m:
            for opt in m.group(1).split():
                if "=" in opt:
                    k, v = opt.split("=", 1)
                    netlist.options[k] = v
            continue

        # Analysis commands
        if ANALYSIS_RE.match(upper):
            netlist.analysis.append(text_line)
            continue

        # Component line
        comp = _parse_component_line(text_line, line_num)
        if comp:
            netlist.components.append(comp)
            continue

    return netlist


def netlist_to_json(netlist: Netlist) -> str:
    """Serialize a Netlist to JSON string."""
    return json.dumps(
        {
            "title": netlist.title,
            "components": [asdict(c) for c in netlist.components],
            "models": [asdict(m) for m in netlist.models],
            "subcircuits": [
                {
                    "name": s.name,
                    "external_nodes": s.external_nodes,
                    "components": [asdict(c) for c in s.components],
                    "models": [asdict(m) for m in s.models],
                    "line_start": s.line_start,
                    "line_end": s.line_end,
                }
                for s in netlist.subcircuits
            ],
            "global_nodes": netlist.global_nodes,
            "options": netlist.options,
            "analysis": netlist.analysis,
        },
        indent=2,
    )


def print_summary(netlist: Netlist) -> None:
    """Print a human-readable summary of the parsed netlist."""
    print(f"Title: {netlist.title}")
    print(f"Components: {len(netlist.components)}")
    for c in netlist.components:
        print(f"  {c.designation:8s} {c.type:12s} nodes={c.nodes} value={c.value}")
    if netlist.models:
        print(f"Models: {len(netlist.models)}")
        for m in netlist.models:
            print(f"  .MODEL {m.name} ({m.type})")
    if netlist.subcircuits:
        print(f"Subcircuits: {len(netlist.subcircuits)}")
        for s in netlist.subcircuits:
            print(
                f"  .SUBCKT {s.name} nodes={s.external_nodes} "
                f"({len(s.components)} internal components)"
            )
    if netlist.global_nodes:
        print(f"Global nodes: {netlist.global_nodes}")
    if netlist.analysis:
        print(f"Analysis: {', '.join(netlist.analysis)}")


# ── CLI ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Parse a SPICE netlist into structured JSON for circuit-diagram generation."
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Path to SPICE netlist file (.cir). Omit if using --stdin.",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read netlist from stdin instead of a file.",
    )
    parser.add_argument(
        "--json",
        metavar="OUTPUT",
        help="Path to write JSON output. If omitted, writes to stdout.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a human-readable summary instead of JSON.",
    )

    args = parser.parse_args()

    if args.stdin:
        text = sys.stdin.read()
    elif args.input:
        with open(args.input, encoding="utf-8", errors="replace") as f:
            text = f.read()
    else:
        parser.print_help()
        sys.exit(1)

    netlist = parse_netlist(text)

    if args.summary:
        print_summary(netlist)
    else:
        json_str = netlist_to_json(netlist)
        if args.json:
            with open(args.json, "w", encoding="utf-8") as f:
                f.write(json_str)
            print(f"✅ Wrote {args.json}", file=sys.stderr)
        else:
            print(json_str)


if __name__ == "__main__":
    main()
