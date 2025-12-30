# DIY Fluxgate Magnetometer

> Build a high-sensitivity magnetometer for the Pais Effect Demonstrator

---

## Overview

A fluxgate magnetometer offers significantly better sensitivity than the HMC5883L/QMC5883L sensors (~1 nT vs ~200 nT), making it ideal for detecting subtle magnetic field anomalies. While more complex to build, a DIY fluxgate is achievable with basic electronics skills.

### Why Build a Fluxgate?

| Sensor Type | Noise Floor | Cost | Complexity |
|-------------|-------------|------|------------|
| HMC5883L | ~200 nT | £5 | Very Low |
| DIY Fluxgate | ~1-10 nT | £30-50 | Medium |
| Commercial Fluxgate | ~0.1 nT | £500+ | Low (buy) |

For serious anomaly detection, the DIY fluxgate offers the best sensitivity-to-cost ratio.

---

## Theory of Operation

### Basic Principle

A fluxgate magnetometer works by:

1. **Driving a high-permeability core into saturation** using an AC excitation signal
2. **Measuring the asymmetry** in the saturation caused by external magnetic fields
3. **Extracting the external field** by detecting the second harmonic of the excitation frequency

```
                    External Field (B_ext)
                           ↓
    ┌──────────────────────────────────────────────┐
    │                                              │
    │   ╔══════════════════════════════════════╗   │
    │   ║  Excitation      Sense               ║   │
    │   ║  Coil            Coil                ║   │
    │   ║   ┌───┐         ┌───┐                ║   │
    │   ║   │|||│ CORE    │|||│                ║   │
    │   ║   │|||│ ═══════ │|||│                ║   │
    │   ║   │|||│         │|||│                ║   │
    │   ║   └───┘         └───┘                ║   │
    │   ╚══════════════════════════════════════╝   │
    │                                              │
    └──────────────────────────────────────────────┘
           │                   │
           │                   │
      AC Drive            Output Signal
      (f = 10kHz)         (2f component ∝ B_ext)
```

### Second Harmonic Detection

- The excitation coil drives the core at frequency **f** (typically 5-20 kHz)
- In zero external field, the core saturates symmetrically → no second harmonic
- An external field biases the core → asymmetric saturation → second harmonic (2f) appears
- The amplitude and phase of the 2f component indicate field magnitude and direction

---

## Design Options

### Option 1: Ring Core (Recommended)

Uses a toroidal ferrite or permalloy core with a single sense winding.

**Advantages:**
- Compact design
- Good sensitivity
- Single-axis measurement per core

**Typical specifications achievable:**
- Noise: 1-5 nT/√Hz
- Bandwidth: DC to ~1 kHz
- Range: ±100 μT

### Option 2: Dual Rod Core (Förster Type)

Uses two parallel rod cores wound in opposite directions.

**Advantages:**
- Can achieve very low noise
- Common in commercial designs
- Inherent common-mode rejection

**Disadvantages:**
- More complex winding
- Requires matched cores

---

## Bill of Materials

### Core Components

| Item | Specification | Qty | Est. Cost |
|------|---------------|-----|-----------|
| Ferrite toroid | Fair-Rite 5943000201 or similar | 1 | £3 |
| Permalloy tape | 0.1mm × 5mm (optional upgrade) | 1m | £15 |
| Enamelled copper wire | 0.2mm (32 AWG) | 50m | £5 |
| Enamelled copper wire | 0.1mm (38 AWG) for sense coil | 20m | £4 |

### Electronics

| Item | Specification | Qty | Est. Cost |
|------|---------------|-----|-----------|
| Function generator IC | XR2206 or AD9833 | 1 | £5 |
| Instrumentation amp | AD620 or INA128 | 1 | £5 |
| Op-amps | TL072 or OPA2134 | 2 | £3 |
| Phase-sensitive detector | AD630 or CD4066 + op-amp | 1 | £5 |
| Voltage regulator | 7805, 7905 (±5V supply) | 2 | £1 |
| Passives | Resistors, capacitors (various) | 1 set | £5 |

**Total: ~£45**

---

## Construction

### Step 1: Wind the Core

#### For Ring Core Design:

**Excitation Winding:**
1. Use 0.2mm wire
2. Wind 100 turns evenly around the toroid
3. Bring out centre tap (50 turns from each end)
4. Secure with varnish or tape

**Sense Winding:**
1. Use 0.1mm wire
2. Wind 500-1000 turns over the excitation winding
3. Keep windings even and tight
4. Secure and bring out leads

```
    Cross-section of wound core:

         Sense Winding (500-1000 turns)
              ↓
         ┌─────────────┐
    ─────│  ┌─────┐    │─────
         │  │█████│    │
         │  │█████│    │   ← Excitation (100 turns)
         │  │█████│    │
    ─────│  └─────┘    │─────
         └─────────────┘
              ↑
         Ferrite Core
```

### Step 2: Build the Excitation Circuit

```
                            +12V
                              │
                              R1
                              │
              ┌───────────────┼───────────────┐
              │               │               │
            ┌─┴─┐           ┌─┴─┐           ┌─┴─┐
            │ Q1│           │   │           │ Q2│
            │NPN│           │   │           │NPN│
            └─┬─┘           │   │           └─┬─┘
              │       ┌─────┴───┴─────┐       │
              ├───────┤   EXCITATION  ├───────┤
              │       │     COIL      │       │
              │       │  (CT at top)  │       │
              │       └───────────────┘       │
              │                               │
              └───────────────┬───────────────┘
                              │
                             GND

    Drive Q1, Q2 in anti-phase at 10 kHz
    from oscillator (XR2206 or similar)
```

### Step 3: Build the Sense Amplifier

```
                              +5V
                               │
        SENSE     ┌────────────┼────────────┐
        COIL      │            │            │
          ○───┬───┤─\      +   │            │
              │   │  \    ┌────┼────┐       │
              R2  │   >───┤ AD620   ├───────┼───○ OUTPUT
              │   │  /    │  G=100  │       │    TO DETECTOR
          ○───┴───┤─/      └────┬────┘       │
              │            │    │            │
              │           GND  -5V           │
              │                              │
              └────────────┬─────────────────┘
                           │
                          GND
```

### Step 4: Build the Phase-Sensitive Detector

The phase-sensitive detector (PSD) extracts the 2f component:

```
    Sense Amp      ┌─────────────────┐
    Output ────────┤                 │
                   │   AD630 or      ├────○ DC Output
    Reference ─────┤   Synchronous   │     (∝ B_ext)
    (2f from       │   Detector      │
    oscillator)    └────────┬────────┘
                            │
                         Low-pass
                          Filter
                            │
                            ▼
                       To Arduino
                         ADC
```

### Step 5: Complete System Block Diagram

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│              │     │              │     │              │
│  Oscillator  ├────→│  Excitation  ├────→│    Core      │
│   (10 kHz)   │     │   Driver     │     │  (in field)  │
│              │     │              │     │              │
└──────┬───────┘     └──────────────┘     └──────┬───────┘
       │                                         │
       │ (×2 freq)                              │ Sense
       │                                         │ Signal
       ▼                                         ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│              │     │              │     │              │
│   Phase      │←────┤    Lock-in   │←────┤    Sense     │
│  Reference   │     │   Detector   │     │  Amplifier   │
│              │     │              │     │              │
└──────────────┘     └──────┬───────┘     └──────────────┘
                            │
                            │ DC Output
                            ▼
                     ┌──────────────┐
                     │   Arduino    │
                     │     ADC      │
                     └──────────────┘
```

---

## Calibration

### Null Offset Adjustment

1. Place sensor in a magnetic shield (or distant from magnetic sources)
2. Adjust offset potentiometer for zero output
3. Verify stability over temperature

### Scale Factor Calibration

1. Generate a known field using a Helmholtz coil
2. Apply known DC field (e.g., 1 μT)
3. Record output voltage
4. Calculate: `Scale Factor = V_out / B_applied`

### Helmholtz Coil Construction

For calibration, build a simple Helmholtz coil:

```
    d = 2r (coil separation = coil radius)

    ┌───────────┐                   ┌───────────┐
    │   Coil 1  │                   │   Coil 2  │
    │     N     │←───── d = 2r ────→│     N     │
    │   turns   │                   │   turns   │
    └─────┬─────┘                   └─────┬─────┘
          │                               │
          └───────────────┬───────────────┘
                          │
                          I (current)

    Field at centre: B = (4/5)^(3/2) × μ₀ × N × I / r

    For r = 10 cm, N = 50 turns:
    B (μT) ≈ 281 × I (mA)
```

---

## Integration with DAQ

### Arduino Connection

Connect the fluxgate DC output to an Arduino analog input:

```cpp
// Fluxgate reading (assumes 0-5V output scaled to ±100 μT)
const int FLUXGATE_PIN = A0;
const float SCALE_FACTOR = 0.0391;  // μT per ADC count (calibrate!)
const float OFFSET = -100.0;         // Offset for bipolar measurement

float readFluxgate() {
    int raw = analogRead(FLUXGATE_PIN);
    float field_uT = (raw * SCALE_FACTOR) + OFFSET;
    return field_uT;
}
```

### Noise Reduction Tips

1. **Shield the sensor** - Use mu-metal or aluminium enclosure
2. **Use differential inputs** - Reduces common-mode noise
3. **Average multiple readings** - √N improvement in noise
4. **Synchronize sampling** - Avoid beating with mains frequency
5. **Keep excitation frequency away from harmonics of 50/60 Hz**

---

## Expected Performance

| Parameter | DIY Achievable | Good Commercial |
|-----------|----------------|-----------------|
| Noise floor | 1-10 nT/√Hz | 0.01-0.1 nT/√Hz |
| Bandwidth | DC - 1 kHz | DC - 10 kHz |
| Range | ±100 μT | ±100 μT |
| Linearity | 1-2% | 0.01% |
| Power consumption | 100-500 mW | 50-200 mW |

A well-built DIY fluxgate should achieve 10-100× better sensitivity than the HMC5883L, making subtle anomaly detection more feasible.

---

## Troubleshooting

### No Output Signal

- Check excitation oscillator is running (oscilloscope on drive signal)
- Verify core is not cracked or damaged
- Check all winding connections

### Excessive Noise

- Add shielding around sensor
- Check for ground loops
- Reduce excitation frequency if PSD aliasing occurs
- Add more output filtering

### Output Drifts

- Allow warm-up time (15-30 minutes)
- Add temperature compensation
- Improve power supply regulation

### Non-Linear Response

- Core may be saturating - reduce excitation amplitude
- Check for nearby ferromagnetic materials
- Calibrate over full measurement range

---

## References

- Ripka, P. (2001). *Magnetic Sensors and Magnetometers*. Artech House.
- Primdahl, F. (1979). "The fluxgate magnetometer". *J. Phys. E: Sci. Instrum.* 12, 241.
- Application notes from Bartington Instruments, Billingsley, Stefan Mayer Instruments

---

## Safety Notes

- The fluxgate operates at low voltage (<15V) and is inherently safe
- Keep away from strong permanent magnets (can magnetize the core)
- Handle the core carefully - ferrite is brittle

---

*Document version: 1.0*
