# Troubleshooting Guide

> Common issues and solutions for the Pais Effect Demonstrator

---

## Sensor Issues

### Magnetometer Not Detected

**Symptoms:**
- "FAIL on channel X" message during initialization
- I2C scanner shows no devices

**Possible Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Wrong I2C address | HMC5883L uses 0x1E, QMC5883L uses 0x0D. Check which chip you have |
| Wiring error | Verify SDA/SCL connections; check for crossed wires |
| Missing pull-ups | Add 4.7kΩ pull-up resistors on SDA and SCL lines |
| Multiplexer not responding | Check TCA9548A address pins (A0-A2) are grounded for 0x70 |
| 3.3V vs 5V issue | HMC5883L is 3.3V only; use level shifter with 5V Arduino |
| Dead sensor | Try a known-good replacement |

**Diagnostic Steps:**
```cpp
// I2C Scanner - upload to Arduino to find connected devices
#include <Wire.h>

void setup() {
    Wire.begin();
    Serial.begin(115200);
    while (!Serial);
    Serial.println("I2C Scanner");
}

void loop() {
    for (byte addr = 1; addr < 127; addr++) {
        Wire.beginTransmission(addr);
        if (Wire.endTransmission() == 0) {
            Serial.print("Device at 0x");
            Serial.println(addr, HEX);
        }
    }
    Serial.println("Scan complete");
    delay(5000);
}
```

### QMC5883L Instead of HMC5883L

Many "HMC5883L" boards sold today are actually QMC5883L clones. They are NOT drop-in compatible.

**How to identify:**
- Check chip markings under magnification
- HMC5883L ID registers return "H43"
- QMC5883L uses address 0x0D (not 0x1E)

**See:** [QMC5883L section in Phase 1 docs](02-phase1-sensors.md#qmc5883l-compatibility) for initialization code.

### Erratic Magnetometer Readings

**Symptoms:**
- Values jumping randomly
- Readings don't correlate between sensors
- Noise much higher than expected

**Possible Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| EMI from nearby electronics | Move sensors away from power supplies, motors |
| Ground loops | Connect cable shields at one end only |
| Ferrous materials nearby | Remove steel objects; use brass/aluminium hardware |
| Overheating sensor | Add cooling, reduce sample rate |
| Insufficient averaging | Enable 8-sample averaging in configuration |
| Bad solder joint | Reflow all connections |

### Accelerometer Issues

**Symptoms:**
- ADXL345 not detected
- Wrong readings (not ~1g when stationary)

**Solutions:**
- Check I2C address: 0x53 if SDO pin low, 0x1D if SDO high
- Verify sensor is connected to main I2C bus (not through multiplexer)
- Check for mechanical stress on the breakout board

---

## SD Card Issues

### Card Not Detected

**Symptoms:**
- "FAIL - continuing without logging" message

**Possible Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Wrong CS pin | Verify SD_CS_PIN matches your wiring (default: pin 4) |
| Card not formatted | Format as FAT32 (cards ≤32GB) or exFAT (>32GB) |
| Card not fully inserted | Push until it clicks |
| Worn contacts | Try a different card |
| Power issue | Some SD modules need 5V even with 3.3V logic |
| SPI conflict | Check no other devices sharing SPI pins incorrectly |

### Files Corrupted or Missing Data

**Symptoms:**
- CSV files truncated
- Missing lines in data
- File won't open on PC

**Solutions:**
- Always allow system to power down gracefully
- Increase SD write buffer size if losing data
- Use high-quality Class 10 or faster SD card
- Avoid removing card while logging

---

## High Voltage Issues

### No Charge Accumulating

**Symptoms:**
- Electrostatic meter shows no voltage on plate
- No corona discharge visible

**Possible Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| HV supply not outputting | Verify supply is on and set correctly |
| Poor connection to plate | Check all connections; use corona-dope on joints |
| Humidity too high | Environment must be <70% RH; use dehumidifier |
| Current limiting too aggressive | Verify supply can provide required current |
| Leakage path | Check insulation; look for conductive contamination |

### Excessive Corona Discharge

**Symptoms:**
- Visible purple glow
- Hissing/crackling sound
- Strong ozone smell

**Solutions:**
- Reduce voltage
- Round off sharp edges on plate and connections
- Increase clearance to grounded objects
- Polish plate edges smooth
- Use corona rings on HV connections

### Arcing

**Symptoms:**
- Visible sparks
- Audible snapping
- Equipment shutting down

**Immediate Actions:**
1. **POWER OFF IMMEDIATELY**
2. Wait 30 seconds
3. Discharge all components
4. Inspect for damage before re-energizing

**Prevention:**
- Increase clearances (rule of thumb: 25mm per 10kV)
- Remove sharp points
- Clean insulating surfaces
- Reduce operating voltage

---

## Mechanical Issues

### Piezo Not Vibrating

**Symptoms:**
- No audible tone
- Accelerometer shows no vibration signal

**Possible Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Amplifier not connected | Verify signal chain from function generator |
| Wrong frequency | Sweep frequency to find resonance |
| Amplitude too low | Increase drive level gradually |
| Piezo damaged | Inspect for cracks; test with multimeter (should show capacitance) |
| Wiring polarity | Check piezo polarity if applicable |

### Vibration at Wrong Frequency

**Symptoms:**
- Resonance peak not where expected
- Multiple resonance modes visible

**Solutions:**
- Mass loading changes resonance; recalculate with actual plate mass
- Check piezo mounting - should be rigid and centred
- Verify amplifier bandwidth is sufficient
- Use frequency sweep to map actual resonance

### Plate Detachment

**Symptoms:**
- Sudden change in resonance frequency
- Rattling sound
- Visible gap between plate and actuator

**Prevention:**
- Use appropriate adhesive (epoxy recommended)
- Clean and roughen surfaces before bonding
- Allow full cure time (24h for most epoxies)
- Don't overdrive the system

---

## Data Quality Issues

### 50/60 Hz Noise Dominant

**Symptoms:**
- Large peak at mains frequency in FFT
- Readings oscillate at mains frequency

**Solutions:**
- Improve Faraday cage shielding
- Move away from mains wiring
- Use twisted pair cables for sensors
- Add ferrite cores to sensor cables
- Consider battery-powered operation
- Apply notch filter in analysis

### Poor Sensor Correlation

**Symptoms:**
- Reference sensor doesn't track environmental changes
- Sensors show uncorrelated noise

**Possible Causes:**
- Sensors too far apart for environmental correlation
- Local interference affecting one sensor
- Different sensor types with different responses
- Timing skew between readings

### Data Dropouts

**Symptoms:**
- Gaps in timestamp sequence
- Sample rate lower than expected

**Solutions:**
- Reduce sample rate
- Increase I2C clock speed
- Optimize code to reduce loop time
- Use DMA or interrupts for more consistent timing

---

## Software Issues

### Arduino Won't Upload

**Common Solutions:**
- Select correct board (Arduino Due - Programming Port)
- Select correct COM port
- Press reset button twice quickly
- Try a different USB cable
- Install/update board support package

### Python Script Errors

**Common Issues:**

```python
# "No module named 'xxx'"
# Solution: Install missing package
pip install numpy pandas matplotlib scipy

# "File not found"
# Solution: Use absolute path or verify current directory
import os
print(os.getcwd())  # Check current directory

# "Permission denied" on serial port
# Solution (Linux): Add user to dialout group
# sudo usermod -a -G dialout $USER
# Then log out and back in
```

### Serial Port Issues

**Symptoms:**
- Can't connect to Arduino
- Data appears corrupted

**Solutions:**
- Close other programs using the port (Arduino IDE Serial Monitor, etc.)
- Check baud rate matches (default: 115200)
- Try different USB port
- Check cable supports data (not charge-only)

---

## Analysis Issues

### FFT Shows Unexpected Peaks

**Diagnostic Questions:**
1. Is peak at mains frequency (50/60 Hz)? → Shielding issue
2. Is peak at sample rate / N? → Aliasing
3. Is peak at vibration frequency? → Expected if running
4. Does peak disappear when system off? → System-generated

### Results Not Matching Expectations

Before concluding the experiment failed, verify:

- [ ] Baseline was properly established
- [ ] All sensors are calibrated
- [ ] Sample rate is sufficient (>2× highest frequency of interest)
- [ ] Environmental conditions are stable
- [ ] Equipment is functioning correctly
- [ ] Analysis code is correct

Remember: A properly conducted null result is still valuable scientific data.

---

## Getting Help

If you can't resolve an issue:

1. **Check the GitHub Issues** for similar problems
2. **Search the discussions** for community solutions
3. **Create a new issue** with:
   - Detailed description of the problem
   - Hardware configuration
   - Error messages (exact text)
   - Steps already tried
   - Relevant log files or screenshots

---

*Last updated: 2024-XX-XX*
