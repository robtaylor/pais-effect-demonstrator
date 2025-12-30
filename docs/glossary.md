# Glossary of Terms

> Definitions of technical terms used throughout the Pais Effect Demonstrator documentation.

---

## A

**ADC (Analog-to-Digital Converter)**
An electronic circuit that converts continuous analog signals to discrete digital numbers. The Arduino Due has a 12-bit ADC.

**ADXL345**
A 3-axis digital accelerometer IC from Analog Devices. Used in this project to detect plate vibration.

**Amplitude**
The maximum displacement or strength of an oscillating signal. In this project, refers to the vibration amplitude of the piezoelectric actuator.

**Artifact**
An unwanted signal component not related to the phenomenon being measured. Common artifacts include mains hum (50/60 Hz), mechanical vibration coupling, and EMI.

---

## B

**Baseline**
The normal signal level measured when the experimental stimulus is not active. Used as a reference for detecting anomalies.

**Bandwidth**
The range of frequencies over which a system operates effectively. For magnetometers, wider bandwidth allows detecting faster-changing fields.

---

## C

**Calibration**
The process of adjusting sensor readings to account for systematic errors (offsets, scale factors) and convert raw values to physical units.

**Cockcroft-Walton Multiplier**
A voltage multiplier circuit using diodes and capacitors to generate high DC voltage from low AC voltage. Named after John Cockcroft and Ernest Walton.

**Corona Discharge**
Electrical discharge occurring when the electric field near a conductor exceeds the breakdown strength of air, causing ionization. Produces ozone and UV light.

---

## D

**DAQ (Data Acquisition)**
System for measuring and recording physical phenomena. In this project, the Arduino-based sensor interface.

**DC (Direct Current)**
Electric current flowing in one direction. The HV charging system produces DC voltage.

---

## E

**EMI (Electromagnetic Interference)**
Unwanted electromagnetic signals that can affect sensitive measurements. Common sources include power supplies, motors, and digital circuits.

**Excitation**
The driving signal applied to cause vibration. In this project, the sinusoidal signal from the function generator.

---

## F

**Faraday Cage**
An enclosure made of conductive material that blocks external electric fields. Used to shield the experiment from external EMI.

**FFT (Fast Fourier Transform)**
An algorithm that converts time-domain signals to frequency-domain representation. Used to identify frequency components in sensor data.

**Fluxgate Magnetometer**
A sensitive magnetometer that uses the nonlinear magnetic properties of a ferromagnetic core to detect magnetic fields. More sensitive than Hall-effect sensors.

**Function Generator**
An electronic instrument that produces various waveforms (sine, square, triangle) at adjustable frequencies and amplitudes.

---

## G

**Gauss**
A unit of magnetic flux density (field strength). 1 Gauss = 100 microtesla (μT). Earth's field is approximately 25-65 μT (0.25-0.65 Gauss).

**Ground Loop**
An unwanted current path created when multiple ground connections exist between pieces of equipment. Causes noise pickup.

---

## H

**Hard Iron Offset**
A constant magnetic field bias in magnetometer readings caused by permanently magnetized materials near the sensor. Corrected during calibration.

**HMC5883L**
A 3-axis digital magnetometer IC from Honeywell. Commonly used for compass applications. Has I²C interface.

**HV (High Voltage)**
In this project, voltages above 1 kV. The charging system operates at 10-30 kV.

---

## I

**I²C (Inter-Integrated Circuit)**
A serial communication protocol using two wires (SDA data, SCL clock). Used to connect multiple sensors to the Arduino.

**Impedance**
The total opposition to current flow in an AC circuit, combining resistance and reactance.

---

## L

**LOTO (Lock-Out/Tag-Out)**
Safety procedure ensuring that hazardous energy sources are isolated and cannot be activated during maintenance or adjustment.

**LSB (Least Significant Bit)**
The smallest unit in a digital measurement. Sensor data is often expressed in LSB before calibration converts it to physical units.

---

## M

**Magnetometer**
A sensor that measures magnetic field strength and/or direction. This project uses multiple magnetometers to detect field anomalies.

**Mains Frequency**
The frequency of AC power distribution: 50 Hz in most of the world, 60 Hz in North America. A common source of electrical noise.

**Multiplexer (Mux)**
A device that selects one of several inputs and forwards it to a single output. The TCA9548A is an I²C multiplexer allowing multiple sensors with the same address.

---

## N

**Noise Floor**
The minimum signal level that can be reliably detected above background noise. Determined by sensor sensitivity and environmental interference.

**Null Result**
An experimental outcome where no significant effect is detected. Still scientifically valuable as it constrains possible effect magnitudes.

---

## O

**Ozone (O₃)**
A molecule consisting of three oxygen atoms. Produced by corona discharge. Toxic at high concentrations but detectable by its distinctive "fresh" smell.

---

## P

**Pais Effect**
The hypothetical phenomenon described in US Navy patents by Salvatore Pais, suggesting that rapidly vibrating electrically charged matter could produce unusual electromagnetic effects.

**Piezoelectric**
Materials that produce voltage when mechanically stressed, and conversely deform when voltage is applied. Used for precise vibration generation.

**PSD (Power Spectral Density)**
A measure of how signal power is distributed across frequencies. Used to identify dominant frequency components and noise characteristics.

**Pull-up Resistor**
A resistor connected between a signal line and positive voltage to ensure a defined logic level when no device is driving the line. Required for I²C buses.

---

## Q

**QMC5883L**
A 3-axis magnetometer from QST Corporation, often sold as HMC5883L replacement. Uses different I²C address (0x0D vs 0x1E) and registers.

---

## R

**RCD/GFCI (Residual Current Device/Ground Fault Circuit Interrupter)**
Safety device that disconnects power when it detects current leaking to ground, protecting against electric shock.

**Resonance**
The tendency of a system to oscillate with greater amplitude at specific frequencies. Piezo-plate assemblies have mechanical resonances.

---

## S

**Sample Rate**
The number of measurements taken per second, measured in Hz. Higher sample rates allow detecting faster signal changes but generate more data.

**Sensitivity**
The smallest change in the measured quantity that produces a detectable change in output. Often expressed as LSB per physical unit.

**Shielded Cable**
Cable with a conductive outer layer (shield) that protects the inner conductors from electromagnetic interference.

**Sigma (σ)**
Statistical measure of detection significance. A 3σ detection means the signal is 3 standard deviations above the noise floor (0.3% probability of false positive).

**SNR (Signal-to-Noise Ratio)**
The ratio of desired signal power to background noise power. Higher SNR makes signal detection more reliable.

**Soft Iron Distortion**
Distortion of the magnetic field by nearby conductive (but not permanently magnetized) materials. Corrected by scale factors during calibration.

---

## T

**TCA9548A**
An 8-channel I²C multiplexer IC from Texas Instruments. Allows connecting multiple devices with the same I²C address.

**Tesla (T)**
SI unit of magnetic flux density. 1 Tesla = 10,000 Gauss. Typical laboratory fields are measured in microtesla (μT).

---

## U

**Upper Bound**
When no effect is detected, the maximum effect size that could exist while remaining undetected given the measurement noise.

**UV (Ultraviolet)**
Electromagnetic radiation with wavelength shorter than visible light. Produced by corona discharge; can cause eye and skin damage.

---

## V

**Variac**
Variable autotransformer allowing continuous adjustment of AC voltage. Used to control the input to the HV multiplier.

**Vibration Mode**
A specific pattern of oscillation in a mechanical system. Plates have multiple vibration modes at different frequencies.

---

## W

**Welch's Method**
An algorithm for estimating power spectral density by averaging multiple overlapping FFT segments. Reduces noise in frequency analysis.

---

## Symbols

**μT (Microtesla)**
Unit of magnetic field strength. 1 μT = 10⁻⁶ Tesla = 0.01 Gauss.

**Ω (Ohm)**
Unit of electrical resistance. 1 MΩ = 1,000,000 ohms.

**Hz (Hertz)**
Unit of frequency. 1 Hz = 1 cycle per second. kHz = 1000 Hz.

---

*See also: [Theory and Background](01-theory-background.md) for deeper explanations of the physics involved.*
