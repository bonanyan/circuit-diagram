# ─── Circuit Diagram ───

> AI 驱动的电路图生成器 · 自然语言 → 精美电路原理图

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![SchemDraw](https://img.shields.io/badge/SchemDraw-0.23-green)](https://schemdraw.readthedocs.io/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue)](./LICENSE)

╭──────────────────────────────────────────────────────────────╮
│  「给我画一个 RC 低通滤波器」                                    │
│                                                              │
│          ╔══════════╗                                        │
│    ──────╢ R1  1kΩ  ╟──────┬──────                           │
│          ╚══════════╝      │                                 │
│                           ═╪═ C1                             │
│                            │  10μF                           │
│                           ─┴─                                │
│                            ═══ GND                           │
│                                                              │
│  ✅ 3 秒出图 · SVG / PNG · 即改即得                             │
╰──────────────────────────────────────────────────────────────╯
```

<!-- ────────────────────────────────────────────────── -->

## ✦ 用途

**circuit-diagram** 是一个 Reasonix / Claude Code 的 AI Skill，基于 Python 的 [SchemDraw](https://schemdraw.readthedocs.io/) 库，让你用自然语言或 SPICE 网表直接生成排版良好的电路原理图。

| 输入 | 输出 |
|------|------|
| 「画一个共射极放大器」 | SVG / PNG 电路图 |
| SPICE 网表 (`.cir`) | 自动解析 → 生成原理图 |
| 布尔表达式 `(A and B) or C` | 逻辑门电路图 |
| 时序波形描述 | 时序图 |
| 流程图描述 | 流程图 |

<!-- ────────────────────────────────────────────────── -->

## ✦ 快速开始

### 1. 安装

```bash
pip install schemdraw matplotlib
```

> `matplotlib` 可选：仅 PNG/PDF 输出需要；纯 SVG 只需 `schemdraw`。

### 2. 在 AI 中启用

把这个仓库克隆到 Reasonix skills 目录，或通过 install-capability 安装：

```bash
git clone git@github.com:bonanyan/circuit-diagram.git \
  ~/.reasonix/skills/circuit-diagram
```

### 3. 直接使用 SchemDraw 画图

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

## ✦ 示例

### 模拟电路 — RC 低通滤波器

```
输入：画一个 RC 低通滤波器，R=1kΩ，C=10μF
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

### 逻辑电路 — 布尔表达式

```python
from schemdraw.parsing import logicparse

logicparse('(A and B) or (not C)', outlabel='$Y$')
```

### SPICE 网表 → 原理图

```bash
# 先用 parser 提取拓扑
python3 scripts/spice_parser.py amplifier.cir --summary

# 输出:
#   R1  resistor  nodes=['VCC','BASE']  value=100k
#   Q1  bjt       nodes=['COL','BASE','EMIT']  value=2N2222
#   ...
```

然后 AI 自动将解析结果转为 SchemDraw 代码并生成图片。

<!-- ────────────────────────────────────────────────── -->

## ✦ 支持的元素

| 类别 | 元素 |
|------|------|
| **无源元件** | 电阻 (US/IEC/可变)、电容 (普通/极性/可变)、电感、二极管 (整流/齐纳/肖特基/LED) |
| **电源** | 直流/交流/正弦/脉冲/方波 电压源 & 电流源、电池、接地 |
| **晶体管** | BJT (NPN/PNP)、JFET、MOSFET (模拟/数字)、IGBT |
| **运放** | 标准运放、积分器、微分器、比较器 |
| **逻辑门** | AND / NAND / OR / NOR / XOR / XNOR / NOT / 施密特触发器 |
| **其他** | 开关、继电器、变压器、光耦、惠斯通电桥、整流桥、连接器、7 段数码管 |
| **注释** | 电压/电流标签、环路电流、包围圈、标注箭头 |

完整列表见 [`references/element-catalog.md`](references/element-catalog.md)。

<!-- ────────────────────────────────────────────────── -->

## ✦ 目录结构

```
circuit-diagram/
├── SKILL.md                         ← Skill 主文件（AI 读这个）
├── references/
│   └── element-catalog.md           ← 全部元件 & 锚点速查
├── scripts/
│   └── spice_parser.py              ← SPICE 网表解析器
└── README.md
```

<!-- ────────────────────────────────────────────────── -->

## ✦ License

Apache-2.0 © bonanyan

---

<p align="center">
  ⚡ 用自然语言画电路 · 一句话搞定原理图 ⚡
</p>
