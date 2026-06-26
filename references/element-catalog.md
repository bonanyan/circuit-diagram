# SchemDraw Element Catalog

Complete reference of SchemDraw elements organized by category. All elements imported via `import schemdraw.elements as elm` unless otherwise noted.

---

## Basic Two-Terminal Elements

### Resistors

```python
elm.Resistor()        # US-style (zigzag), default
elm.ResistorIEC()     # IEC-style (rectangle)
elm.ResistorVar()     # Variable resistor (US)
elm.ResistorVarIEC()  # Variable resistor (IEC)
elm.RBox()            # US box-style resistor
elm.Potentiometer()   # Potentiometer (3-terminal)
elm.Thermistor()      # Thermistor
elm.Photoresistor()   # Light-dependent resistor
```

### Capacitors

```python
elm.Capacitor()       # Standard unpolarized
elm.CapacitorPolar()  # Polarized (electrolytic) — curved plate
elm.CapacitorVar()    # Variable capacitor
elm.CapacitorFeedthrough()  # Feedthrough capacitor
```

### Inductors

```python
elm.Inductor()        # Standard (loops)
elm.Inductor2()       # Alternative style (filled arcs)
elm.InductorVar()     # Variable inductor
elm.Transformer()     # Two-winding transformer
```

### Diodes

```python
elm.Diode()           # Standard rectifier diode
elm.Zener()           # Zener diode
elm.Schottky()        # Schottky diode
elm.LED()             # Light-emitting diode
elm.LED2()            # LED alternative style
elm.Tunnel()          # Tunnel diode
elm.Varactor()        # Varactor/varicap diode
elm.Thyristor()       # SCR thyristor
elm.Triac()           # TRIAC
elm.Diac()            # DIAC
elm.SiliconControlledRectifier()  # SCR alternative name
```

### Sources

```python
elm.SourceV()         # DC voltage source
elm.SourceI()         # DC current source
elm.SourceSin()       # Sinusoidal voltage source
elm.SourcePulse()     # Pulse voltage source
elm.SourceSquare()    # Square wave source
elm.SourceTriangle()  # Triangle wave source
elm.SourceRamp()      # Ramp source
elm.Battery()         # Battery (multi-cell)
elm.BatteryCell()     # Single battery cell
```

### Grounds & References

```python
elm.Ground()          # Standard earth ground
elm.GroundSignal()    # Signal ground
elm.GroundChassis()   # Chassis ground
elm.GroundReference() # Reference ground
elm.Vss()             # VSS / negative supply rail
elm.Vdd()             # VDD / positive supply rail
```

### Connecting Elements

```python
elm.Line()            # Straight wire segment
elm.Dot()             # Connection dot (filled by default)
elm.Dot(open=True)    # Open dot
elm.Gap()             # Open-circuit gap, useful for voltage labels
elm.Wire()            # Same as Line
elm.Jumper()          # Wire jumper (arch)
```

### Switches & Relays

```python
elm.Switch()          # SPST switch
elm.SwitchSpdt()      # SPDT switch
elm.SwitchSpdt2()     # SPDT switch alternative
elm.SwitchDpst()      # DPST switch
elm.SwitchDpdt()      # DPDT switch
elm.Button()          # Push button (normally open)
elm.ButtonNC()        # Push button (normally closed)
elm.Relay()           # Relay coil + contacts
```

### Protection & Misc

```python
elm.Fuse()            # Fuse
elm.Lamp()            # Incandescent lamp
elm.Neon()            # Neon lamp
elm.Motor()           # DC motor
elm.MotorAC()         # AC motor
elm.Generator()       # Generator
elm.Speaker()         # Speaker
elm.Mic()             # Microphone
elm.Antenna()         # Antenna
elm.Crystal()         # Crystal / resonator
```

### Meters

```python
elm.MeterV()          # Voltmeter
elm.MeterA()          # Ammeter
elm.MeterOhm()        # Ohmmeter
```

---

## Transistors

### BJT (Bipolar Junction Transistors)

```python
elm.BjtNpn()          # NPN BJT — anchors: base, collector, emitter
elm.BjtPnp()          # PNP BJT — anchors: base, collector, emitter
```

### JFET

```python
elm.JfetN()           # N-channel JFET — anchors: gate, drain, source
elm.JfetP()           # P-channel JFET
```

### MOSFET (Analog style — 3 pins)

```python
elm.AnalogNFet()      # N-channel MOSFET, analog — anchors: gate, drain, source
elm.AnalogPFet()      # P-channel MOSFET, analog
```

### MOSFET (Digital style — 4 pins with body diode)

```python
elm.NFet()            # N-channel MOSFET — anchors: gate, drain, source, body
elm.PFet()            # P-channel MOSFET
```

### Other Transistors

```python
elm.IgbN()            # IGBT N-channel — anchors: gate, collector, emitter
elm.IgbP()            # IGBT P-channel
elm.Ujt()             # Unijunction transistor
```

---

## Operational Amplifiers

```python
elm.Opamp()           # Standard opamp — anchors: in1, in2, out, vdd, vss
elm.OpampDual()       # Dual opamp package
elm.Integrator()      # Opamp integrator (amp + R + C)
elm.Differentiator()  # Opamp differentiator (amp + R + C)
elm.Comparator()      # Comparator
elm.SchmittTrigger()  # Schmitt trigger (opamp-based)
elm.Ota()             # Operational transconductance amplifier
```

---

## Vacuum Tubes

```python
elm.Triode()          # Triode vacuum tube
elm.Tetrode()         # Tetrode
elm.Pentode()         # Pentode
```

---

## Transformers & Couplers

```python
elm.Transformer()     # Simple two-winding transformer
elm.TransformerCore() # Transformer with magnetic core
elm.TransformerTap()  # Center-tapped transformer
elm.Optocoupler()     # Optocoupler / opto-isolator
```

---

## Integrated Circuits

### DIP Packages

```python
elm.Ic()              # Generic DIP IC — specify pins with `pins=` parameter
elm.Ic(pins=[elm.IcPin(name='VCC', side='left', pos=1),
             elm.IcPin(name='GND', side='right', pos=1)])
```

### Multiplexers

```python
elm.Mux()             # Multiplexer
elm.Demux()           # Demultiplexer
```

### Seven-Segment Display

```python
elm.SevenSegment()    # 7-segment LED display
```

---

## Connectors

```python
elm.Header()          # Pin header
elm.HeaderFemale()    # Female header
elm.DSub()            # D-sub connector
elm.DSub9()           # DE-9 connector
elm.Rca()             # RCA/phono jack
elm.Coax()            # Coaxial connector
elm.Barrel()          # Barrel/power jack
elm.Outlet()          # Wall outlet
```

### Data Busses

```python
elm.BusLine()         # Bus line (thicker, with slash marks)
elm.BusTie()          # Connection from wire to bus
```

---

## Labels & Annotations (as standalone elements)

These are elements you place on a drawing without a parent component:

```python
elm.Label()           # Invisible element that carries a label only
elm.Tag()              # Label with a pointer line
elm.Annotate()         # Curved annotation arrow with text
elm.Encircle([e1,e2])  # Ellipse around listed elements
elm.EncircleBox([e1,e2])  # Rounded rectangle around listed elements
```

---

## Current & Voltage Label Elements

```python
elm.CurrentLabel()         # Current arrow placed over an element
elm.CurrentLabelInline()   # Inline arrow on an element's lead
elm.VoltageLabelArc()      # Arc-shaped voltage label over an element
elm.LoopCurrent([e1,e2,e3,e4])  # Loop current arrow around a mesh
elm.LoopArrow()            # Free-form loop arrow
elm.ZLabel()               # Right-angle impedance arrow
```

---

## Compound Elements

Pre-built combinations of basic elements:

```python
elm.Rectifier()       # Full-wave bridge rectifier (4 diodes)
elm.Wheatstone()      # Wheatstone bridge (4 resistors in diamond)
elm.Relay()           # Relay with coil and contacts
```

---

## Two-Port / Signal Processing

```python
elm.Amp()             # Amplifier triangle
elm.Adder()           # Summing junction
elm.Mixer()           # Signal mixer
elm.Oscillator()      # Oscillator symbol
elm.Filter()          # Filter block
elm.VGA()             # Variable-gain amplifier
elm.ADC()             # Analog-to-digital converter
elm.DAC()             # Digital-to-analog converter
```

---

## Logic Gates (`from schemdraw import logic`)

### Standard Gates

```python
logic.And()           # AND gate — anchors: in1, in2, out
logic.Nand()          # NAND gate
logic.Or()            # OR gate
logic.Nor()           # NOR gate
logic.Xor()           # XOR gate
logic.Xnor()          # XNOR gate
logic.Not()           # Inverter (NOT)
logic.Buf()           # Buffer
logic.NotNot()        # Double inverter (buffer with two triangles)
logic.Tgate()         # Transmission gate
logic.Tristate()      # Tri-state buffer
```

### Schmitt Trigger Gates

```python
logic.Schmitt()       # Schmitt buffer
logic.SchmittNot()    # Schmitt inverter
logic.SchmittAnd()    # Schmitt AND
logic.SchmittNand()   # Schmitt NAND
```

### Multi-Input & Active-Low

```python
logic.Nand(inputs=5)                    # 5-input NAND gate
logic.And(inputs=3, inputnots=[1, 3])   # Inputs 1 and 3 are active-low
```

---

## Timing Diagrams (`from schemdraw import timing`)

```python
timing.Clock()              # Clock signal
timing.Signal()             # Arbitrary digital signal
timing.SignalBus()          # Bus signal
timing.State()              # State line
timing.Transition()         # Transition marker
```

---

## Flowcharts (`from schemdraw import flowchart as fc`)

```python
fc.Start()            # Start/terminator (rounded)
fc.Process()          # Process box (rectangle)
fc.Decision()         # Decision diamond
fc.Data()             # I/O parallelogram
fc.Predefined()       # Predefined process (double-sided)
fc.Document()         # Document symbol
fc.Connector()        # On-page connector (circle)
fc.Terminator()       # Same as Start
fc.Arrow()            # Flow arrow
fc.Line()             # Flow line (no arrow)
```

---

## Styling Reference

### Common Methods on All Elements

```python
elem.label('text', loc='top', ofst=0.5, rotate=False, fontsize=12)
elem.color('red')
elem.fill('lightblue')
elem.fill(True)       # fill with default/current color
elem.fill(False)      # disable fill
elem.linestyle('--')  # dashed, ':', '-.', (0, (5,2)) etc.
elem.linewidth(2)
elem.theta(45)        # rotate entire element
elem.flip()           # mirror horizontally
elem.reverse()        # swap start/end
elem.anchor('center') # get named anchor position
elem.at(pos)          # place at absolute coordinate or element's anchor
elem.right()          # draw next element to the right
elem.down()           # draw next element down
elem.left()           # draw next element to the left
elem.up()             # draw next element up
```

### Color Names

Standard CSS/SVG color names: `red`, `blue`, `green`, `black`, `orange`, `purple`, `cyan`, `magenta`, `gray`, `darkred`, `darkblue`, `darkgreen`, etc. Hex codes also work: `'#ff0000'`.

### Line Styles

| Style | Code |
|-------|------|
| Solid | `'-'` (default) |
| Dashed | `'--'` |
| Dotted | `':'` |
| Dash-dot | `'-.'` |
| Custom | `(0, (5, 2, 1, 2))` — (offset, (on, off, on, off...)) |

---

## Element Anchor Quick Reference

Every two-terminal element has at minimum:

| Anchor | Position |
|--------|----------|
| `start` | Left terminal (before direction) |
| `end` | Right terminal (after direction) |
| `center` | Geometric center |
| `N`, `S`, `E`, `W` | Cardinal compass points |
| `NE`, `NW`, `SE`, `SW` | Corners |
| `top`, `bottom` | Top/bottom edge center |
| `left`, `right` | Left/right edge center |

Special anchors by element type:

| Element | Special Anchors |
|---------|----------------|
| `BjtNpn`/`BjtPnp` | `base`, `collector`, `emitter` |
| `AnalogNFet`/`AnalogPFet` | `gate`, `drain`, `source` |
| `NFet`/`PFet` | `gate`, `drain`, `source`, `body` |
| `Opamp` | `in1`, `in2`, `out`, `vdd`, `vss` |
| `And`/`Nand`/etc. | `in1`, `in2`, ..., `inN`, `out` |
