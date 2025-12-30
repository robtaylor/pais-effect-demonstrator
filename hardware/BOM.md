# Bill of Materials

> Complete parts list for the Pais Effect Demonstrator (Vibrating Charged Plate configuration)

---

## Cost Summary

| Category | Estimated Cost (£) | Notes |
|----------|-------------------|-------|
| Sensing System | £150-350 | Magnetometers are main cost driver |
| Mechanical System | £120-250 | Piezo stack is main cost |
| Electrical/HV System | £80-180 | DIY Cockcroft-Walton saves money |
| Data Acquisition | £40-80 | Arduino-based |
| Enclosure & Safety | £50-100 | Faraday cage + shielding |
| Consumables & Misc | £30-50 | Wire, fasteners, etc. |
| **Total** | **£470-1010** | |

---

## 1. Sensing System

### 1.1 Magnetometers

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| Fluxgate Magnetometer | 1 | ±100 μT range, <10 nT resolution, analog output | £100-250 | Stefan Mayer Instruments, eBay surplus | Primary sensor; FLC-100 or equivalent |
| HMC5883L Breakout | 3 | 3-axis, ±800 μT, I²C interface | £5 each | AliExpress, Amazon, eBay | Secondary sensors, spatial array |
| QMC5883L Breakout | 2 | 3-axis, ±800 μT, I²C (HMC5883L alternative) | £3 each | AliExpress | Backup/alternative |

**Alternatives:**
- MLX90393 (£8): Better resolution than HMC5883L
- IST8310 (£10): Industrial grade, SPI interface
- DIY Fluxgate: See `/hardware/schematics/diy-fluxgate/` for build instructions

### 1.2 Motion Sensing

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| ADXL345 Accelerometer | 1 | 3-axis, ±16g, 3200 Hz sample rate | £8 | Adafruit, SparkFun, AliExpress | Mounted on plate |
| MPU6050 IMU | 1 | 6-axis (accel + gyro), I²C | £4 | AliExpress, Amazon | Alternative/backup |
| Laser Displacement Sensor | 1 | 0.1 μm resolution (optional) | £150+ | Keyence, Panasonic surplus | For precise amplitude verification |

### 1.3 Environmental Sensing

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| BME280 | 1 | Temperature, humidity, pressure | £6 | Adafruit, AliExpress | Environmental monitoring |
| DS18B20 | 2 | Temperature probe, waterproof | £3 | Amazon | Piezo and plate temp monitoring |

---

## 2. Mechanical System

### 2.1 Vibration Actuator

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| Piezo Stack Actuator | 1 | 100+ μm displacement, 10+ kHz bandwidth | £80-180 | Thorlabs (PK2FMP2), PI Ceramic, eBay surplus | Main actuator |
| Piezo Disc Elements | 5 | 27mm diameter, brass-backed | £5 pack | AliExpress, electronics surplus | For DIY stack alternative |
| Piezo Amplifier | 1 | 0-150V output, audio input | £40-80 | eBay, DIY build | See schematics for DIY option |

**DIY Piezo Stack Alternative:**
Stack 5-10 piezo discs in series (electrically parallel) for ~50 μm displacement at 150V. Total cost ~£20 vs £100+ for commercial stack.

### 2.2 Charged Plate

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| Copper Sheet | 1 | 100×100×1 mm, polished | £10-20 | metals4U, eBay | Main test plate |
| Copper Sheet (spare) | 2 | 100×100×1 mm | £15 | As above | For modifications |
| Aluminium Sheet | 1 | 100×100×2 mm | £8 | metals4U | Alternative plate material |

### 2.3 Mounting & Isolation

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| Sorbothane Pads | 4 | 50×50×6 mm, 50 duro | £12 | RS Components, Amazon | Vibration isolation |
| PTFE Sheet | 1 | 150×150×10 mm | £8 | eBay, plastics suppliers | Electrical isolation base |
| Ceramic Standoffs | 4 | M4, 20mm height | £6 | RS Components, Farnell | HV isolation |
| Optical Breadboard | 1 | 300×300 mm, M6 tapped (optional) | £50-100 | Thorlabs surplus, eBay | Precision mounting |
| Aluminium Plate | 1 | 300×300×10 mm | £25 | metals4U | Base plate alternative |

### 2.4 Mechanical Fasteners

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| M3 Stainless Set | 1 | Bolts, nuts, washers assortment | £8 | Amazon | General assembly |
| M4 Nylon Set | 1 | Bolts, nuts, washers | £5 | RS Components | Electrically isolated connections |
| Epoxy Adhesive | 1 | 2-part, high strength (Araldite) | £8 | Hardware stores | Plate-to-actuator bond |
| Cyanoacrylate | 1 | Thin viscosity | £4 | Hardware stores | Sensor mounting |

---

## 3. Electrical System

### 3.1 High Voltage Supply

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| HV Module (Option A) | 1 | 10-30 kV, <1 mA, adjustable | £50-150 | eBay, AliExpress | Pre-built module |
| Cockcroft-Walton Kit (Option B) | 1 | DIY voltage multiplier | £20-40 | Components below | Recommended for learning |

**Cockcroft-Walton Components (if building):**

| Item | Qty | Specification | Est. Cost | Sources |
|------|-----|---------------|-----------|---------|
| High Voltage Diodes | 20 | 1N4007 or UF4007, 1kV | £3 | AliExpress, Farnell |
| High Voltage Capacitors | 20 | 10 nF, 1 kV ceramic | £8 | AliExpress, RS |
| Neon Transformer | 1 | 10 kV, 30 mA (current limited) | £30 | Sign supply shops |
| Variac | 1 | 0-240V, 2A | £30 | eBay | For voltage control |

### 3.2 Corona Charging

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| Tungsten Wire | 1m | 0.1 mm diameter | £5 | eBay, welding suppliers | Charging needle |
| Steel Sewing Needles | 10 | Sharp point | £2 | Haberdashery | Alternative needles |
| HV Wire | 5m | Silicone insulated, 30 kV rated | £15 | eBay | HV connections |
| Banana Plugs (HV) | 4 | Insulated, rated 5 kV | £8 | RS Components | Safe connections |

### 3.3 Signal Generation & Amplification

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| Function Generator | 1 | 1 Hz - 100 kHz, arbitrary waveform | £50-150 | eBay, Banggood, JDS6600 | Signal source |
| Audio Amplifier | 1 | 50W+, good linearity | £25 | eBay, parts bin | Drives piezo amplifier |
| Piezo Driver | 1 | 0-150V output, low distortion | £60 | DIY or commercial | See schematics |

### 3.4 Electrostatic Measurement

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| Electrostatic Fieldmeter | 1 | 0-30 kV, non-contact | £40-200 | eBay surplus, Simco-Ion | Verify charging |
| Electrometer Op-Amp | 2 | AD549, OPA128 | £15 | Farnell, Mouser | DIY fieldmeter |
| HV Probe | 1 | 1000:1 divider, scope compatible | £30 | eBay | Voltage verification |

---

## 4. Data Acquisition

### 4.1 Microcontroller

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| Arduino Due | 1 | ARM Cortex-M3, 84 MHz, 12-bit ADC | £35 | Arduino, eBay | High-speed ADC |
| Arduino Mega | 1 | ATmega2560 (backup/alternative) | £15 | Arduino, AliExpress | Lower cost option |
| Teensy 4.0 | 1 | 600 MHz, 2× ADC (premium option) | £25 | PJRC | Highest performance |

### 4.2 Data Storage & Interface

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| SD Card Module | 1 | SPI interface | £4 | AliExpress | Data logging |
| SD Card | 1 | 32 GB, Class 10 | £8 | Amazon | Storage |
| USB Isolator | 1 | 2.5 kV isolation | £15 | Amazon, eBay | Protects PC |
| Logic Level Shifter | 2 | 3.3V/5V bidirectional | £3 | AliExpress | Sensor interfacing |

### 4.3 Signal Conditioning

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| Instrumentation Amp | 2 | INA128, AD620 | £10 | Farnell, Mouser | Fluxgate signal conditioning |
| Op-Amp Assortment | 1 | TL072, LM358, OP07 | £8 | AliExpress | General purpose |
| Precision Resistors | 1 set | 0.1%, assorted values | £10 | Farnell | Bridge circuits |

---

## 5. Enclosure & Shielding

### 5.1 Faraday Cage

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| Copper Mesh | 2m² | 100 mesh (150 μm) | £30 | eBay, screening suppliers | EM shielding |
| Aluminium Sheet | 1 | 500×500×1 mm | £15 | metals4U | Cage base |
| Aluminium Angle | 4m | 25×25×3 mm | £12 | metals4U | Cage frame |
| BNC Feedthroughs | 4 | Panel mount, 50Ω | £12 | RS Components | Signal pass-through |
| Copper Tape | 1 roll | 50mm × 20m, conductive adhesive | £15 | Amazon, eBay | Seam sealing |

### 5.2 Safety Enclosure

| Item | Qty | Specification | Est. Cost | Sources | Notes |
|------|-----|---------------|-----------|---------|-------|
| Polycarbonate Sheet | 1 | 500×500×3 mm, clear | £20 | Plastic suppliers | Viewing/projectile shield |
| Acrylic Sheet | 1 | 500×500×5 mm (not for HV side) | £15 | Plastic suppliers | Secondary shielding |
| HV Warning Signs | 3 | Self-adhesive | £5 | eBay, safety suppliers | Workspace marking |
| Rubber Mat | 1 | 600×600×6 mm, insulating | £20 | RS Components | Floor protection |

---

## 6. Test Equipment (Assumed Available)

These items are typically available in a hackspace:

| Item | Specification | Notes |
|------|---------------|-------|
| Digital Multimeter | True RMS, basic | Continuity, voltage checks |
| Oscilloscope | 2+ channels, 50+ MHz | Signal verification |
| Bench Power Supply | 0-30V, 0-5A | Low voltage testing |
| Soldering Station | Temperature controlled | Assembly |
| Heat Gun | Adjustable temperature | Heat shrink, adhesive curing |

---

## 7. Consumables

| Item | Qty | Est. Cost | Notes |
|------|-----|-----------|-------|
| Hook-up Wire (assorted) | 1 pack | £10 | 22-26 AWG, stranded |
| Heat Shrink Tubing | 1 pack | £6 | Assorted sizes |
| Solder (leaded) | 100g | £8 | 60/40, 0.7mm |
| PCB Proto Board | 5 | £8 | For circuits |
| Cable Ties | 1 pack | £4 | Organisation |
| Isopropyl Alcohol | 1L | £8 | Cleaning |
| Silica Gel | 1 pack | £4 | Moisture control |

---

## Sourcing Guide

### UK Suppliers

| Supplier | Best For | Website |
|----------|----------|---------|
| RS Components | Professional components, fast delivery | rs-online.com |
| Farnell | Semiconductors, precision parts | uk.farnell.com |
| Mouser | Wide range, detailed specs | mouser.co.uk |
| Rapid Electronics | Educational, good prices | rapidonline.com |
| CPC | General electronics | cpc.farnell.com |
| metals4U | Metal stock | metals4u.co.uk |
| AliExpress | Budget components (longer delivery) | aliexpress.com |
| eBay | Surplus equipment, used test gear | ebay.co.uk |

### Surplus/Secondhand Sources

| Source | What to Look For |
|--------|------------------|
| eBay | Test equipment, piezo actuators, fluxgate sensors |
| Surplus Shed | Scientific surplus |
| University surplus sales | Lab equipment |
| Hamfests/Radio rallies | Test equipment |
| Hackspace members | Parts bin treasures |

---

## Substitution Notes

### Critical Components (No Substitution)

These must meet specifications:
- Fluxgate magnetometer (sensitivity critical)
- HV supply current limiting (safety critical)
- Piezo actuator displacement (determines amplitude range)

### Flexible Components

These can be freely substituted:
- Arduino variant (any with sufficient ADC speed)
- Secondary magnetometers (various I²C types work)
- Mechanical fasteners (metric/imperial equivalent)
- Enclosure materials (function over form)

---

## Phased Purchasing

### Phase 1: Sensor Array (£100-200)
```
- Fluxgate magnetometer
- HMC5883L breakouts (×3)
- ADXL345 accelerometer
- Arduino Due
- SD card module + card
- Basic components
```

### Phase 2: Mechanical (£100-150)
```
- Piezo stack actuator
- Copper plate
- Mounting hardware
- PTFE base
- Sorbothane isolation
```

### Phase 3: Electrical (£100-200)
```
- Function generator (if not available)
- HV supply or components
- Piezo amplifier
- Cables and connectors
- Safety equipment
```

### Phase 4: Enclosure (£50-100)
```
- Faraday cage materials
- Polycarbonate shielding
- BNC feedthroughs
- Warning signs
```

---

## Notes

- Prices are estimates based on 2024 UK market; expect ±30% variation
- Check hackspace inventory before purchasing; many items may be available
- Quality matters for sensors; budget elsewhere if needed
- Always have spares of cheap components (op-amps, connectors, etc.)
