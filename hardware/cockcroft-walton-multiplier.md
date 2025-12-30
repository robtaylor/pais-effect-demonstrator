# Cockcroft-Walton Voltage Multiplier

> High-voltage power supply for the Pais Effect Demonstrator charging system

---

## Overview

The Cockcroft-Walton (CW) voltage multiplier is a classic circuit for generating high DC voltage from a low-voltage AC source. It's ideal for this project because:

- Simple construction from common components
- Inherently current-limited (safer than transformer-based supplies)
- Scalable to required voltage
- No custom transformer needed

---

## Theory of Operation

The CW multiplier works by charging capacitors in parallel during one half-cycle, then stacking them in series during the other half-cycle.

### Single Stage (Voltage Doubler)

```
        AC Input              DC Output
         (Vac)                 (2×Vac)
           │                      │
           │    ┌────────────┐    │
           ├────┤     C1     ├────┤
           │    └────────────┘    │
           │          │           │
           │        ──┴──         │
           │        ╲  ╱ D1       │
           │         ╲╱           │
           │          │           │
           │        ──┴──         │
           │        ╲  ╱ D2       │
           │         ╲╱           │
           │          │           │
           │    ┌─────┴─────┐     │
           │    │     C2    │     │
           │    └─────┬─────┘     │
           │          │           │
          ─┴─        ─┴─         ─┴─
          GND        GND         GND
```

**Operation:**
1. Negative half-cycle: D1 conducts, C1 charges to Vac
2. Positive half-cycle: D2 conducts, C2 charges to 2×Vac

### Multi-Stage Multiplier (Recommended)

For higher voltages, cascade multiple stages:

```
                 4-Stage Cockcroft-Walton Multiplier
                         Output: ~8 × Vpeak

    AC ○────┬────┤├────┬────┤├────┬────┤├────┬────┤├────┬──○ HV+
    IN      │    C1    │    C3    │    C5    │    C7    │
            │         ─┴─        ─┴─        ─┴─        ─┴─
            │         ╲╱ D1      ╲╱ D3      ╲╱ D5      ╲╱ D7
            │          │          │          │          │
            │    ┌─────┴──────────┴──────────┴──────────┴─────┐
            │    │                                            │
            │    │    C2         C4         C6         C8     │
            │    ├────┤├────┬────┤├────┬────┤├────┬────┤├────┤
            │   ─┴─        ─┴─        ─┴─        ─┴─          │
            │   ╲╱ D2      ╲╱ D4      ╲╱ D6      ╲╱ D8         │
            │    │          │          │          │           │
    GND ○───┴────┴──────────┴──────────┴──────────┴───────────┘


    Simplified View:

         Stage 1      Stage 2      Stage 3      Stage 4
        ┌───────┐    ┌───────┐    ┌───────┐    ┌───────┐
    AC ─┤ ×2    ├────┤ ×2    ├────┤ ×2    ├────┤ ×2    ├─── 8×Vpeak
        └───────┘    └───────┘    └───────┘    └───────┘
```

### Voltage Output Equation

Ideal output voltage (no load):
```
Vout = 2 × N × Vpeak

Where:
  N = number of stages
  Vpeak = peak AC input voltage
```

Example: 4 stages × 2 × 325V peak (from 230V mains) = 2600V

**Note:** Actual voltage is lower under load due to capacitor discharge.

---

## Design for This Project

### Target Specifications

| Parameter | Value | Notes |
|-----------|-------|-------|
| Output voltage | 10-30 kV | Adjustable |
| Output current | <1 mA | Current limited for safety |
| Ripple | <10% | Acceptable for charging |
| Input | Variac + 230V | Adjustable AC input |

### Recommended Configuration

**6-Stage Design:**
- Input: Variac (0-270V AC)
- Peak input voltage: ~380V max
- Theoretical output: 2 × 6 × 380V = 4.56 kV per 100V AC input
- At 270V AC: ~12 kV output

For higher voltages (20-30 kV), use 10-12 stages.

---

## Bill of Materials

### For 6-Stage, 15kV Design

| Item | Specification | Qty | Est. Cost |
|------|---------------|-----|-----------|
| HV diodes | 10kV 5mA (e.g., 2CL77 or similar) | 12 | £8 |
| HV capacitors | 10nF 3kV ceramic | 12 | £12 |
| Variac | 0-270V 2A | 1 | £40 |
| HV wire | Silicone 20kV rated | 5m | £10 |
| Enclosure | Plastic project box | 1 | £8 |
| HV connector | Banana socket, insulated | 2 | £4 |
| Bleeder resistors | 10MΩ 2W | 6 | £3 |

**Total: ~£85**

### Component Selection Notes

**Diodes:**
- Must be rated for peak inverse voltage (PIV) > 2 × Vpeak per stage
- For 15kV output: use 3kV diodes minimum (10kV preferred for margin)
- Fast recovery not required - standard rectifiers fine
- Examples: BY8406, 2CL77, UF5408 (stacked)

**Capacitors:**
- Voltage rating > 2 × Vpeak per stage
- Higher capacitance = lower ripple, better regulation
- Ceramic disc capacitors are ideal for HV
- 10nF minimum, 100nF preferred if available

---

## Construction

### PCB Layout Considerations

```
    ┌────────────────────────────────────────────────────────┐
    │                                                        │
    │   ○ AC IN                                   HV OUT ○   │
    │                                                        │
    │   ┌──┐    ┌──┐    ┌──┐    ┌──┐    ┌──┐    ┌──┐        │
    │   │C1│    │C3│    │C5│    │C7│    │C9│    │C11│       │
    │   └┬─┘    └┬─┘    └┬─┘    └┬─┘    └┬─┘    └─┬─┘       │
    │    │  ┌──┐ │  ┌──┐ │  ┌──┐ │  ┌──┐ │  ┌──┐  │         │
    │    ├──┤D1├─┴──┤D3├─┴──┤D5├─┴──┤D7├─┴──┤D9├──┤         │
    │    │  └──┘    └──┘    └──┘    └──┘    └──┘  │         │
    │    │  ┌──┐    ┌──┐    ┌──┐    ┌──┐    ┌──┐  │         │
    │    ├──┤D2├─┬──┤D4├─┬──┤D6├─┬──┤D8├─┬──┤D10├─┤         │
    │    │  └──┘ │  └──┘ │  └──┘ │  └──┘ │  └──┘  │         │
    │   ┌┴─┐    ┌┴─┐    ┌┴─┐    ┌┴─┐    ┌┴─┐     │         │
    │   │C2│    │C4│    │C6│    │C8│    │C10│    │         │
    │   └──┘    └──┘    └──┘    └──┘    └──┘     │         │
    │                                             │         │
    │   ○ GND ────────────────────────────────────┘         │
    │                                                        │
    └────────────────────────────────────────────────────────┘

    CRITICAL: Maintain >10mm clearance between all HV traces
              Use rounded corners on all conductors
              No sharp points or edges
```

### Assembly Steps

1. **Test components individually**
   - Check all diodes with multimeter
   - Verify capacitor values

2. **Mount on insulating substrate**
   - Use fibreglass PCB or acrylic sheet
   - Avoid standard FR4 at voltages >5kV (may track)

3. **Wire point-to-point for HV section**
   - Use silicone-insulated wire
   - Keep leads as short as possible
   - Dress wires away from grounded surfaces

4. **Add bleeder resistors**
   - 10MΩ resistor across each capacitor
   - Ensures safe discharge when powered off
   - Also reduces stored energy

5. **Enclosure**
   - Mount in plastic enclosure
   - Add ventilation holes (corona produces ozone)
   - Label clearly with voltage warning

### Bleeder Resistor Network

```
    HV+ ────┬─────┬─────┬─────┬─────┬─────┐
            │     │     │     │     │     │
           ┌┴┐   ┌┴┐   ┌┴┐   ┌┴┐   ┌┴┐   ┌┴┐
           │ │   │ │   │ │   │ │   │ │   │ │  10MΩ each
           │R│   │R│   │R│   │R│   │R│   │R│  (2W minimum)
           │ │   │ │   │ │   │ │   │ │   │ │
           └┬┘   └┬┘   └┬┘   └┬┘   └┬┘   └┬┘
            │     │     │     │     │     │
    GND ────┴─────┴─────┴─────┴─────┴─────┘

    Discharge time constant: τ = R × C
    For 10MΩ, 10nF: τ = 0.1 seconds
    5τ for 99% discharge: 0.5 seconds
```

---

## Current Limiting

The CW multiplier is inherently current-limited by its capacitive impedance, but additional limiting is recommended for safety.

### Capacitive Current Limit

```
I_max ≈ 2 × π × f × C × Vout / N

Where:
  f = AC frequency (50 Hz)
  C = stage capacitance
  Vout = output voltage
  N = number of stages

For 10nF, 50Hz, 15kV, 6 stages:
I_max ≈ 0.8 mA
```

### Additional Series Resistor (Recommended)

Add a 10MΩ resistor in series with output:

```
    CW Multiplier      10MΩ         Output
    Output ──────────/\/\/\/\──────── HV+
                       │
                       │ Limits current to:
                       │ I = V/R = 15kV / 10MΩ = 1.5mA max
```

This ensures arc current stays in the "painful but survivable" range.

---

## Testing Procedure

### Initial Power-Up

1. Connect variac set to minimum (0V)
2. Connect HV meter or resistive divider probe
3. Slowly increase variac voltage
4. Verify output increases linearly
5. Check for corona (hissing) or arcing

### Measuring HV Safely

Build a resistive voltage divider:

```
        HV Input              Multimeter
           │                      │
           │    ┌───────────┐     │
           ├────┤  100MΩ    ├─────┤
           │    │  (10×10MΩ)│     │
           │    └───────────┘     │
           │          │           │
           │    ┌─────┴─────┐     │
           │    │   100kΩ   │     │
           │    └─────┬─────┘     │
           │          │           │
          ─┴─        ─┴─         ─┴─
          GND        GND         GND

    Divider ratio: 1001:1
    At 10kV input: multimeter reads 10V
```

**Warning:** Ensure resistors are rated for HV. Use multiple 10MΩ resistors in series.

---

## Safety Features

### Essential Safety Additions

1. **Bleeder resistors** - Discharge caps when off
2. **Series limiting resistor** - Limits short-circuit current
3. **Indicator lamp** - Shows when HV present
4. **Interlock switch** - Cuts power if enclosure opened
5. **Earth/ground connection** - One terminal earthed

### Indicator Circuit

```
           HV+
            │
           ┌┴┐
           │ │ 100MΩ (multiple in series)
           └┬┘
            │
           ─┴─
           ╲ ╱  Neon indicator lamp (NE-2)
           ─┬─
            │
           ─┴─
           GND
```

---

## Integration with Experiment

### Connection to Charging Plate

```
    CW Multiplier ────┬──── HV+ ────○ Plate
                      │
                     ─┴─
                     ╲ ╱  Indicator
                     ─┬─
                      │
                      ├──── GND ────○ Faraday Cage
                      │
                    Earth
```

### Operating Procedure

1. Verify all connections before applying power
2. Start with variac at minimum
3. Slowly increase to desired voltage (monitor with HV meter)
4. Observe plate for corona (indicates voltage is high enough)
5. When finished: reduce variac to zero, wait 30 seconds, use discharge stick

---

## Troubleshooting

### No Output

- Check AC input with multimeter
- Verify all diode orientations (band toward HV+)
- Look for open capacitor (measure each one)

### Low Output

- Check for shorted diode
- Measure capacitor values
- Increase AC input voltage
- Check for leakage across PCB (clean with isopropanol)

### Excessive Ripple

- Increase capacitor values
- Reduce load current
- Add output filter capacitor

### Arcing/Corona

- Increase clearances
- Round off sharp edges/points
- Apply corona dope to connections
- Reduce voltage

---

## Alternative: Commercial HV Supply

For those preferring a ready-made solution:

| Option | Voltage | Current | Est. Cost |
|--------|---------|---------|-----------|
| Neon sign transformer | 10-15 kV | 30 mA | £30-50 |
| Flyback driver | 20-30 kV | <1 mA | £20-30 |
| Commercial HV module | 0-30 kV | 0-1 mA | £100-200 |

The CW multiplier offers better control and inherent current limiting, making it preferred for this application.

---

*Document version: 1.0*
