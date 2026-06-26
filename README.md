# ─── Circuit Diagram ───

> AI-powered circuit diagram generator · Natural language → publication-quality schematics

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![SchemDraw](https://img.shields.io/badge/SchemDraw-0.23-green)](https://schemdraw.readthedocs.io/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue)](./LICENSE)


```

<!-- ────────────────────────────────────────────────── -->

## ✦ What It Does

**circuit-diagram** is an AI skill for Reasonix / Claude Code built on Python's [SchemDraw](https://schemdraw.readthedocs.io/) library. Generate properly laid-out circuit schematics from natural language or SPICE netlists — no drag-and-drop schematic editor needed.

| Input | Output |
|-------|-------|
| "Draw a common-emitter amplifier" | SVG / PNG schematic |
| SPICE netlist (`.cir`) | Auto-parsed → schematic |
| Boolean expression `(A and B) or C` | Logic gate diagram |
| Timing waveform description | Timing diagram |
| Flowchart description | Flowchart |

<!-- ────────────────────────────────────────────────── -->

## ✦ Quick Start

### 1. Install

```bash
pip install schemdraw matplotlib
```

> `matplotlib` is optional — only needed for PNG/PDF output. SVG works with `schemdraw` alone.

### 2. Enable in Your AI

**Option A: `npx skills add` (recommended)**

```bash
npx skills add bonanyan/circuit-diagram
```

**Option B: Git clone**

```bash
git clone git@github.com:bonanyan/circuit-diagram.git \
  ~/.reasonix/skills/circuit-diagram
```

**Option C: `install-capability`**

Install via `install-capability` from the GitHub URL.

### 3. Draw with SchemDraw Directly

```python
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='rc-filter.svg') as d:
    elm.Resistor().right().label('1kΩ')
    elm.Capacitor().down().label('10μF', loc='bottom')
    elm.Line().left()
    elm.Ground()
```

<!-- ────────────────────────────────────────────────── -->

## ✦ Examples

### Analog — RC Low-Pass Filter

```
Prompt: Draw an RC low-pass filter, R=1kΩ, C=10μF
```

```python
with schemdraw.Drawing(file='rc-lowpass.svg'):
    elm.SourceSin().up().label('$V_{in}$')
    elm.Line().right()
    elm.Resistor().right().label('$R_1=1k\Omega$')
    elm.Dot()
    elm.Capacitor().down().label('$C_1=10\mu F$', loc='bottom')
    elm.Ground()
    elm.Line().right()
    elm.Dot().label('$V_{out}$')
    elm.Line().down()
    elm.Ground()
```

### Digital — Boolean Expression

```python
from schemdraw.parsing import logicparse

logicparse('(A and B) or (not C)', outlabel='$Y$')
```

### SPICE Netlist → Schematic

```bash
# Parse the netlist topology first
python3 scripts/spice_parser.py amplifier.cir --summary

# Output:
#   R1  resistor  nodes=['VCC','BASE']  value=100k
#   Q1  bjt       nodes=['COL','BASE','EMIT']  value=2N2222
#   ...
```

Then the AI converts the parsed result into SchemDraw code and renders the image.

<!-- ────────────────────────────────────────────────── -->

## ✦ Supported Elements

| Category | Elements |
|----------|----------|
| **Passives** | Resistor (US/IEC/variable), capacitor (standard/polarized/variable), inductor, diode (rectifier/zener/schottky/LED) |
| **Sources** | DC/AC/sine/pulse/square voltage & current sources, battery, grounds |
| **Transistors** | BJT (NPN/PNP), JFET, MOSFET (analog/digital), IGBT |
| **Opamps** | Standard, integrator, differentiator, comparator |
| **Logic gates** | AND / NAND / OR / NOR / XOR / XNOR / NOT / Schmitt triggers |
| **More** | Switches, relays, transformers, optocouplers, Wheatstone bridge, rectifier bridge, connectors, 7-segment displays |
| **Annotations** | Voltage/current labels, loop currents, encircling boxes, annotation arrows |

Full catalog: [`references/element-catalog.md`](references/element-catalog.md).

<!-- ────────────────────────────────────────────────── -->

## ✦ Directory Structure

```
circuit-diagram/
├── SKILL.md                         ← Skill entry point (the AI reads this)
├── references/
│   └── element-catalog.md           ← Full element & anchor reference
├── scripts/
│   └── spice_parser.py              ← SPICE netlist → JSON parser
└── README.md
```

<!-- ────────────────────────────────────────────────── -->

## ✦ License

Apache-2.0 © bonanyan

---

<p align="center">
  ⚡ Draw circuits with words · One sentence is all it takes ⚡
</p>
