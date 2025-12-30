# Phase 1 Quick-Start Bill of Materials

> Minimum-cost parts list to get started with the sensor array and baseline measurements

---

## Overview

This BOM covers the essentials for Phase 1: setting up the sensor array, data acquisition, and establishing environmental baseline measurements. This allows you to verify your sensor setup and characterize your workspace before committing to the full project cost.

**Total Estimated Cost: £75-150**

---

## Essential Components

### 1. Magnetometers

| Item | Qty | Est. Cost | Source | Notes |
|------|-----|-----------|--------|-------|
| HMC5883L or QMC5883L Breakout | 3 | £12 | AliExpress, Amazon | £4 each; check which chip you receive |

**Budget Option:** Start with just 2 sensors (£8) - one near the eventual plate position, one for reference.

### 2. Accelerometer

| Item | Qty | Est. Cost | Source | Notes |
|------|-----|-----------|--------|-------|
| ADXL345 Breakout | 1 | £5 | AliExpress, Amazon | For detecting vibrations |

**Alternative:** MPU6050 (£3) if already available

### 3. Microcontroller

| Item | Qty | Est. Cost | Source | Notes |
|------|-----|-----------|--------|-------|
| Arduino Due | 1 | £35 | Arduino Store, AliExpress | 12-bit ADC, 84 MHz |

**Budget Alternative:** Arduino Mega (£15) - works but lower ADC resolution

### 4. I²C Multiplexer

| Item | Qty | Est. Cost | Source | Notes |
|------|-----|-----------|--------|-------|
| TCA9548A Breakout | 1 | £3 | AliExpress, Amazon | Allows multiple same-address sensors |

### 5. Data Storage

| Item | Qty | Est. Cost | Source | Notes |
|------|-----|-----------|--------|-------|
| SD Card Module | 1 | £3 | AliExpress | SPI interface |
| SD Card 16GB+ | 1 | £5 | Amazon | Class 10 recommended |

### 6. Wiring & Connectors

| Item | Qty | Est. Cost | Source | Notes |
|------|-----|-----------|--------|-------|
| Dupont Jumper Wires | 1 pack | £4 | AliExpress | M-F and M-M |
| Breadboard | 1 | £3 | AliExpress | For prototyping |
| Header Pins | 1 pack | £2 | AliExpress | For sensor breakouts |

### 7. Passive Components

| Item | Qty | Est. Cost | Source | Notes |
|------|-----|-----------|--------|-------|
| 4.7kΩ Resistors | 4 | £1 | Any | I²C pull-ups |
| USB Cable | 1 | £3 | Any | For Arduino programming |

---

## Cost Summary

| Category | Minimum | Recommended | Notes |
|----------|---------|-------------|-------|
| Magnetometers | £8 (2×) | £12 (3×) | 3 sensors recommended |
| Accelerometer | £5 | £5 | |
| Microcontroller | £15 (Mega) | £35 (Due) | Due recommended |
| I²C Multiplexer | £3 | £3 | |
| Storage | £8 | £8 | |
| Wiring/Misc | £10 | £15 | |
| **Total** | **£49** | **£78** | |

Add ~£20 for shipping if ordering from AliExpress.

---

## Recommended Sourcing Strategy

### If Time is Not Critical (2-4 weeks delivery)

Order from AliExpress for lowest cost:
- 3× HMC5883L/QMC5883L breakouts: £12
- 1× ADXL345: £5
- 1× TCA9548A: £3
- 1× SD card module: £3
- 1× Arduino Due clone: £20
- Jumper wires, headers, resistors: £10

**Total: ~£53** (plus ~£15 shipping)

### If Starting This Weekend

Order from Amazon Prime or local supplier:
- Arduino Due: £35-45
- Sensor pack (often bundled): £20-30
- SD module + card: £10-15
- Wiring kit: £10

**Total: ~£75-100** (next-day delivery)

---

## What You Can Do With Phase 1

Once assembled, you can:

1. **Characterize your workspace**
   - Measure 50/60 Hz interference level
   - Identify magnetic noise sources
   - Establish baseline noise floor

2. **Verify sensor operation**
   - Confirm all sensors respond
   - Check I²C communication
   - Test data logging

3. **Develop analysis skills**
   - Practice with Python scripts
   - Learn FFT analysis
   - Understand sensor calibration

4. **Identify problems early**
   - Find grounding issues
   - Detect EMI sources
   - Optimize sensor placement

---

## Optional but Recommended

These items aren't essential for Phase 1 but will make life easier:

| Item | Cost | Reason |
|------|------|--------|
| USB isolator | £15 | Protects PC from ground loops |
| Ferrite cores | £5 | Reduces cable noise |
| Shielded cable (1m) | £8 | For sensor connections |
| BME280 environmental sensor | £5 | Log temperature/humidity |

---

## What's NOT Needed Yet

Save these for later phases:

- High voltage supply (Phase 3)
- Piezoelectric actuator (Phase 2)
- Copper plate (Phase 2)
- Faraday cage materials (Phase 2+)
- Function generator (Phase 2)
- Fluxgate magnetometer (Phase 3+, optional upgrade)

---

## Supplier Quick Links

| Supplier | Type | Delivery |
|----------|------|----------|
| [AliExpress](https://aliexpress.com) | Budget | 2-4 weeks |
| [Amazon UK](https://amazon.co.uk) | Quick | 1-2 days |
| [The Pi Hut](https://thepihut.com) | Maker-friendly | 2-3 days |
| [Pimoroni](https://pimoroni.com) | Quality | 2-3 days |
| [RS Components](https://rs-online.com) | Professional | Next day |

---

## Checklist

Before starting assembly, verify you have:

- [ ] 2-3× Magnetometer breakouts (HMC5883L or QMC5883L)
- [ ] 1× Accelerometer breakout (ADXL345)
- [ ] 1× I²C Multiplexer (TCA9548A)
- [ ] 1× Arduino Due (or Mega)
- [ ] 1× SD card module + SD card
- [ ] Jumper wires (at least 20)
- [ ] Breadboard or proto board
- [ ] 4× 4.7kΩ resistors
- [ ] USB cable for Arduino
- [ ] Computer with Arduino IDE installed

---

## Next Steps

1. Order components from your preferred supplier
2. While waiting, install Arduino IDE and required libraries
3. Read through Phase 1 documentation
4. Set up a clean workspace for assembly
5. When parts arrive, begin with sensor testing

---

*See [Phase 1: Sensor Array](../docs/02-phase1-sensors.md) for detailed assembly and testing instructions.*
