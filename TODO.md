# TODO

> Outstanding tasks, improvements, and wishlist items for the Pais Effect Demonstrator project.

---

## 🔴 High Priority

### Documentation
- [ ] Add `docs/TROUBLESHOOTING.md` with common issues and solutions
- [ ] Create `references/patent-summary.md` with key patent excerpts and analysis
- [ ] Add wiring photos/diagrams to Phase 1 sensor documentation
- [ ] Document QMC5883L differences (common HMC5883L clone)

### Safety
- [ ] Add emergency contact template to SAFETY.md
- [ ] Create printable safety checklist (PDF)
- [ ] Add first aid specific guidance for electrical burns
- [ ] Document lock-out/tag-out procedure for HV system

### Hardware
- [ ] Create KiCad schematic for piezo driver circuit
- [ ] Design simple PCB for sensor breakout/distribution
- [ ] Add Cockcroft-Walton multiplier schematic (KiCad or SVG)
- [ ] Document DIY fluxgate magnetometer option

---

## 🟡 Medium Priority

### Technical Diagrams (SVG)
- [ ] `diagrams/mechanical-assembly-exploded.svg` - Full assembly exploded view
- [ ] `diagrams/electrical-schematic.svg` - Complete system schematic
- [ ] `diagrams/sensor-placement.svg` - Sensor array positioning detail
- [ ] `diagrams/faraday-cage-construction.svg` - Cage build details
- [ ] `diagrams/wiring-diagram.svg` - Point-to-point wiring guide
- [ ] `diagrams/hv-clearances.svg` - Safety clearance zones

### Software
- [ ] Extract full analysis module from docs (separate .py files)
- [ ] Add real-time plotting script (matplotlib animation or pyqtgraph)
- [ ] Create sensor calibration wizard script
- [ ] Add data export to HDF5 format option
- [ ] Implement automatic artifact detection
- [ ] Add frequency sweep automation script

### Arduino Firmware
- [ ] Add configurable sample rate via serial command
- [ ] Implement trigger input for synchronised acquisition
- [ ] Add watchdog timer for reliability
- [ ] Create version for Teensy 4.0 (higher performance)
- [ ] Add support for ADS1115 external ADC (higher resolution)

### Protocols
- [ ] Create standalone protocol checklist PDFs
- [ ] Add data sheet templates (printable)
- [ ] Design experiment logbook template
- [ ] Create calibration record forms

---

## 🟢 Low Priority / Nice to Have

### Documentation
- [ ] Add glossary of terms
- [ ] Create quick-start guide (single page)
- [ ] Add FAQ section
- [ ] Translate to other languages (German, Spanish, Mandarin)
- [ ] Add video build guide links (when available)
- [ ] Create presentation slides for hackspace talks

### Analysis Enhancements
- [ ] Jupyter notebook versions of analysis
- [ ] Interactive dashboard (Streamlit or Dash)
- [ ] Automated report generation (LaTeX/PDF)
- [ ] Machine learning anomaly detection experiment
- [ ] Monte Carlo uncertainty propagation

### Hardware Variants
- [ ] Document spinning disc alternative (Track A from original discussion)
- [ ] Low-cost version using salvaged components
- [ ] High-performance version with SQUID magnetometer interface
- [ ] Portable/field version design
- [ ] Multi-plate array configuration

### Software Features
- [ ] Web interface for remote monitoring
- [ ] MQTT/InfluxDB integration for long-term logging
- [ ] Automated nightly analysis runs
- [ ] GitHub Actions CI for Python linting/tests
- [ ] Docker container for reproducible analysis environment

### Community
- [ ] Create results submission template
- [ ] Build comparison database of community results
- [ ] Set up GitHub Discussions categories
- [ ] Create Discord/Matrix channel for real-time discussion
- [ ] Organise virtual build-along sessions

---

## 🔬 Future Experiments

These are extensions beyond the core experiment:

- [ ] **Frequency extension:** Test above 10 kHz with ultrasonic transducer
- [ ] **Charge density increase:** Vacuum chamber for higher sustainable charge
- [ ] **Cryogenic test:** Does effect change at low temperature?
- [ ] **Multiple plates:** Phased array of vibrating plates
- [ ] **Rotating reference frame:** Mount sensors on spinning platform
- [ ] **Pulsed operation:** High-intensity short bursts
- [ ] **Alternative geometries:** Sphere, cone (closer to patent design)
- [ ] **Superconducting plate:** Test with YBCO tile

---

## 🐛 Known Issues

- [ ] `docs/00-project-overview.md` may be redundant with README.md - consolidate
- [ ] BOM prices are estimates from 2024 - need periodic updates
- [ ] Arduino sketch assumes HMC5883L - QMC5883L needs different init sequence
- [ ] Analysis scripts not yet tested with real experimental data

---

## ✅ Completed

- [x] Main README with project overview
- [x] Comprehensive safety documentation
- [x] Theory and background document
- [x] Phase 1-5 build documentation
- [x] Bill of materials
- [x] Arduino DAQ firmware
- [x] Python analysis framework
- [x] CONTRIBUTING guide
- [x] MIT License
- [x] .gitignore

---

## Contributing to TODOs

Found something missing? Please either:
1. Submit a PR adding to this TODO.md
2. Open an issue with the `enhancement` label
3. Just do the thing and submit a PR!

---

*Last updated: 2024-XX-XX*
