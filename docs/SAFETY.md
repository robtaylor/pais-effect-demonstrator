# ⚠️ Safety Documentation

> **READ THIS ENTIRE DOCUMENT BEFORE STARTING THE PROJECT**

This project involves hazards that can cause **serious injury or death** if not properly managed. Do not proceed unless you understand and can implement all safety measures.

---

## Hazard Summary

| Hazard | Severity | Likelihood | Risk Level | Primary Control |
|--------|----------|------------|------------|-----------------|
| Electric shock (HV) | Fatal | Possible | **CRITICAL** | Current limiting, procedures |
| Electric shock (mains) | Fatal | Possible | **CRITICAL** | Proper wiring, RCD/GFCI |
| Corona discharge burns | Serious | Likely | **HIGH** | Distance, insulation |
| Ozone inhalation | Moderate | Likely | **MEDIUM** | Ventilation |
| UV exposure | Moderate | Possible | **MEDIUM** | Shielding, time limits |
| Hearing damage | Moderate | Possible | **MEDIUM** | Ear protection |
| Projectile (plate failure) | Serious | Unlikely | **LOW** | Shielding |
| Fire | Serious | Unlikely | **LOW** | No flammables, extinguisher |

---

## High Voltage Safety

### The One-Hand Rule

**ALWAYS keep one hand behind your back or in your pocket when working near energized HV equipment.** This prevents current from passing through your heart.

### Current Limiting is Essential

The HV supply MUST be current-limited to < 1 mA. At this current:
- Shock is painful but survivable
- Capacitors cannot store lethal charge
- Arc energy is limited

**Never use a supply capable of more than 1 mA at HV without additional current limiting.**

### Discharge Procedure

Before touching ANY part of the apparatus after HV operation:

```mermaid
flowchart TD
    A[Turn off HV supply] --> B[Wait 30 seconds]
    B --> C[Verify supply shows 0V]
    C --> D[Connect discharge stick to ground]
    D --> E[Touch discharge stick to plate]
    E --> F[Hold for 5 seconds]
    F --> G[Verify with electrostatic meter]
    G --> H{Reading < 100V?}
    H -->|No| E
    H -->|Yes| I[Safe to touch with grounding strap]
```

### Discharge Stick Construction

Build a discharge stick from:
- 1 meter insulating rod (fibreglass, PVC, or dry wood)
- 10 MΩ resistor chain (rated for HV)
- Grounding wire to mains earth

The resistor limits discharge current to prevent:
- Damage to the plate surface
- Loud/startling spark
- EMI to nearby electronics

### Emergency Procedures

**If someone receives an electric shock:**

1. **DO NOT TOUCH THEM** if they're still in contact with the source
2. Disconnect power at the source or circuit breaker
3. Call emergency services (999/112/911)
4. If safe, move them away from the source using non-conductive material
5. Check breathing and pulse
6. Begin CPR if needed and trained
7. Treat for shock (lay flat, elevate legs, keep warm)

**Post emergency contact numbers near the workspace.**

### Emergency Contact Template

Print and complete this form. Post it prominently in the workspace.

```
╔═══════════════════════════════════════════════════════════════╗
║                    EMERGENCY CONTACTS                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  EMERGENCY SERVICES: _______________ (999 / 112 / 911)        ║
║                                                               ║
║  NEAREST HOSPITAL: ________________________________________   ║
║  Address: _________________________________________________   ║
║  Phone: __________________  Distance: _______ mins drive      ║
║                                                               ║
║  POISON CONTROL: ___________________________________________  ║
║                                                               ║
║  LOCAL FIRE DEPARTMENT: ____________________________________  ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║  PROJECT CONTACTS                                             ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Primary Experimenter: _____________________________________  ║
║  Phone: ____________________________________________________  ║
║                                                               ║
║  Safety Officer / Buddy: ___________________________________  ║
║  Phone: ____________________________________________________  ║
║                                                               ║
║  Facility Manager: _________________________________________  ║
║  Phone: ____________________________________________________  ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║  WORKSPACE LOCATION                                           ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Address: __________________________________________________  ║
║  ___________________________________________________________  ║
║                                                               ║
║  Specific Location: ________________________________________  ║
║  (building, room, floor)                                      ║
║                                                               ║
║  Access Instructions: ______________________________________  ║
║  ___________________________________________________________  ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║  This workspace contains HIGH VOLTAGE EQUIPMENT               ║
║  In case of electrical emergency, disconnect power at:        ║
║  ___________________________________________________________  ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Workspace Requirements

### Minimum Requirements

- [ ] Dry environment (< 70% relative humidity)
- [ ] Non-conductive flooring (rubber mat minimum)
- [ ] Clear of flammable materials within 2 meters
- [ ] Adequate ventilation (for ozone)
- [ ] Fire extinguisher (CO₂ or dry powder) within reach
- [ ] First aid kit present
- [ ] Emergency power cutoff accessible
- [ ] Another person present or on-call

### Recommended Additions

- [ ] RCD/GFCI protected mains supply
- [ ] Isolation transformer for mains equipment
- [ ] Grounded anti-static wrist strap
- [ ] HV warning signs posted
- [ ] Interlocked enclosure

---

## Personal Protective Equipment

### Required PPE

| Item | Specification | When Required |
|------|---------------|---------------|
| Safety glasses | Side shields, polycarbonate | Always |
| Closed-toe shoes | Insulating soles preferred | Always |
| Long trousers | Non-synthetic preferred | Always |
| No jewellery | Remove rings, watches, necklaces | During HV operation |

### Situational PPE

| Item | Specification | When Required |
|------|---------------|---------------|
| Hearing protection | NRR 25+ | Vibration > 1 kHz |
| HV gloves | Class 0 minimum (1kV rated) | HV system maintenance |
| Face shield | Full face, polycarbonate | Initial HV tests |
| Lab coat | Cotton, not synthetic | Extended HV operation |

---

## First Aid for Electrical Burns

Electrical burns may occur from arc flash or direct contact with energized conductors. They are often more serious than they initially appear because current can cause deep tissue damage.

### Types of Electrical Burns

| Type | Cause | Appearance |
|------|-------|------------|
| **Arc Flash** | Radiant heat from electrical arc | Surface burns, may affect large area |
| **Contact** | Current flowing through tissue | Entry and exit wounds, deep tissue damage |
| **Thermal** | Ignition of clothing or materials | Standard thermal burn presentation |

### Immediate First Aid

**For Minor Burns (small area, superficial):**

1. Ensure power is disconnected before touching victim
2. Cool the burn under running lukewarm water for 10-20 minutes
3. Do NOT use ice, ice water, or very cold water
4. Remove jewellery and loose clothing near the burn (before swelling)
5. Cover with sterile, non-adhesive dressing
6. Do NOT apply butter, oil, or ointments
7. Seek medical evaluation - electrical burns are often worse than they appear

**For Serious Burns (large area, deep, or any loss of consciousness):**

1. **CALL EMERGENCY SERVICES IMMEDIATELY**
2. Do NOT touch victim if still in contact with electrical source
3. Disconnect power at source if safe to do so
4. Check breathing and pulse - be prepared for CPR
5. Do NOT remove burned clothing stuck to skin
6. Cover burns loosely with clean, dry cloth
7. Treat for shock (lay flat, elevate legs if no spinal injury suspected)
8. Keep victim warm
9. Do NOT give food or water (surgery may be needed)

### Warning Signs Requiring Immediate Medical Attention

Seek emergency medical care if:
- [ ] Any loss of consciousness occurred
- [ ] Burns on hands, feet, face, genitals, or over joints
- [ ] Burns encircling a limb
- [ ] Entry/exit wounds visible
- [ ] Victim reports chest pain or difficulty breathing
- [ ] Cardiac rhythm abnormalities
- [ ] Deep tissue damage (charred or white appearance)
- [ ] Burns cover >5% body surface area

### Special Considerations for HV Burns

High voltage burns from this equipment may cause:

- **Cardiac arrhythmias:** Even if victim appears fine, ECG monitoring is recommended
- **Internal injuries:** Current path through body may damage organs
- **Delayed effects:** Symptoms may appear hours later
- **Compartment syndrome:** Swelling in limbs can cut off circulation

**All personnel receiving HV shock should be medically evaluated, even if asymptomatic.**

---

## Corona Discharge Hazards

### Ozone Production

Corona discharge produces ozone (O₃), which is:
- Toxic at concentrations > 0.1 ppm
- Detectable by smell at ~0.01 ppm ("fresh/electric" smell)
- Heavier than air, accumulates at floor level

**Mitigation:**
- Work in well-ventilated area
- Use extraction fan if running > 10 minutes
- Take breaks outside the area
- If strong ozone smell, stop and ventilate

### UV Radiation

Corona discharge produces UV radiation, primarily UV-C:
- Can cause eye damage (welder's flash)
- Can cause skin burns with prolonged exposure

**Mitigation:**
- Do not stare at corona discharge
- Polycarbonate shielding blocks UV
- Limit continuous operation time

### Nitrogen Oxides

Sustained corona produces NOₓ, which:
- Combines with moisture to form nitric acid
- Corrodes equipment
- Irritates respiratory system

**Mitigation:**
- Ventilation
- Clean equipment after extended runs
- Limit continuous operation

---

## Lock-Out/Tag-Out (LOTO) Procedure

Lock-out/Tag-out procedures ensure that hazardous energy sources are isolated before maintenance or adjustment of equipment. This is mandatory before working on the HV system.

### When LOTO is Required

- Any work on HV wiring or connections
- Replacing or adjusting the HV supply
- Maintenance of Faraday cage or enclosure
- Repair of piezo driver or amplifier
- Any work where accidental energization could cause injury

### LOTO Equipment Required

| Item | Purpose |
|------|---------|
| Padlock (personal) | Physically prevents reconnection |
| Lockout hasp | Allows multiple locks on same point |
| Danger tags | Visual warning; records who applied lock |
| Voltage tester | Verifies zero energy state |

### Step-by-Step LOTO Procedure

#### Step 1: Prepare

1. Notify all personnel that LOTO is being applied
2. Identify all energy sources:
   - [ ] HV power supply (mains input)
   - [ ] Function generator (mains input)
   - [ ] Amplifier (mains input)
   - [ ] Any batteries or capacitors
3. Gather LOTO equipment

#### Step 2: Shut Down

1. Power off equipment using normal controls
2. Follow discharge procedure (wait, verify, discharge stick)
3. Disconnect HV supply from mains
4. Disconnect function generator from mains
5. Disconnect amplifier from mains

#### Step 3: Isolate

1. Unplug all equipment from wall outlets
2. If hardwired: switch off and lock circuit breakers

#### Step 4: Lock Out

1. Apply personal padlock to each isolation point:
   - Main circuit breaker (if applicable)
   - Mains plugs (use lockout plug covers or place in locked box)
2. Each person working must apply their own lock

#### Step 5: Tag Out

Attach danger tag to each lock point:

```
╔═══════════════════════════════════════╗
║           ⚠ DANGER ⚠                 ║
║                                       ║
║      DO NOT OPERATE                   ║
║      DO NOT REMOVE THIS TAG           ║
║                                       ║
║  This equipment is locked out by:     ║
║                                       ║
║  Name: ____________________________   ║
║  Date: ____________________________   ║
║  Time: ____________________________   ║
║  Reason: __________________________   ║
║                                       ║
║  Contact before removal required      ║
╚═══════════════════════════════════════╝
```

#### Step 6: Verify

1. Attempt to start equipment (should not start)
2. Use voltage tester on HV circuit - must read zero
3. Test discharge stick on plate - should produce no spark
4. Verify with electrostatic meter - must read <100V

**Only after successful verification is it safe to work.**

#### Step 7: Perform Work

- Work on equipment as needed
- Keep locks and tags in place throughout
- Do not bypass or remove another person's lock

#### Step 8: Remove LOTO

1. Verify work is complete
2. Verify all tools and materials removed
3. Verify guards and covers replaced
4. Notify all personnel that power will be restored
5. Each person removes only their own lock and tag
6. Reconnect power sources in reverse order
7. Test equipment function

### Multiple Person LOTO

When multiple people are working:
- Use a lockout hasp that accepts multiple padlocks
- Each person applies their own lock
- Equipment cannot be energized until ALL locks are removed
- Never remove another person's lock

### LOTO Violations

If you find equipment with LOTO bypassed or removed:
1. Stop work immediately
2. Notify safety officer
3. Do not operate equipment
4. Investigate cause before resuming

---

## Mechanical Safety

### Piezo Actuator Hazards

Piezoelectric actuators can:
- Generate high voltages when mechanically shocked
- Shatter if overdriven (ceramic shrapnel)
- Overheat if driven at resonance for extended periods

**Mitigation:**
- Never exceed rated displacement
- Use polycarbonate shield around assembly
- Monitor temperature during operation
- Allow cooling periods

### Plate Failure Modes

Although unlikely, the copper plate could:
- Detach from actuator if adhesive fails
- Fracture if driven at resonance with flaws present

**Mitigation:**
- Inspect plate and bonds before each session
- Use polycarbonate enclosure
- Stay clear of plate plane during operation

---

## Electrical Safety (Mains)

### Grounding

All equipment chassis must be properly grounded:
- Function generator
- Amplifier
- HV supply
- Faraday cage
- Oscilloscope

Use a ground continuity tester before first operation.

### Mains Wiring

- All mains wiring must be done by a competent person
- Use appropriate cable ratings
- Include RCD/GFCI protection
- Fuse all circuits appropriately

### Isolation

Consider using an isolation transformer for:
- Increased safety margin
- Reduced ground loop noise
- Protection from mains transients

---

## Emergency Equipment Checklist

Before each session, verify presence of:

- [ ] Fire extinguisher (serviced within 12 months)
- [ ] First aid kit (stocked)
- [ ] HV discharge stick (tested)
- [ ] Insulating mat (dry, undamaged)
- [ ] Emergency power cutoff (functional)
- [ ] Mobile phone (charged, in reach)
- [ ] Emergency contact list (posted)
- [ ] Safety glasses (clean, undamaged)

---

## Operating Procedures

### Pre-Session Checklist

```
[ ] Review today's experimental plan
[ ] Verify another person is present or on-call
[ ] Check all safety equipment present
[ ] Inspect HV connections for damage
[ ] Verify ground connections
[ ] Clear workspace of unnecessary items
[ ] Remove jewellery
[ ] Don PPE
[ ] Test emergency power cutoff
[ ] Verify ventilation operating
```

### During Operation

```
[ ] One hand rule near HV
[ ] Monitor for unusual sounds/smells
[ ] Watch for excessive corona (visible discharge)
[ ] Check temperatures periodically
[ ] Take breaks every 30 minutes
[ ] Log any anomalies immediately
```

### Post-Session Checklist

```
[ ] Power down all equipment in sequence
[ ] Execute discharge procedure
[ ] Verify discharge with meter
[ ] Ground all HV components
[ ] Allow piezo to cool
[ ] Secure HV supply
[ ] Ventilate area for 10 minutes
[ ] Document session in log
[ ] Store equipment properly
```

---

## Training Requirements

Before operating this apparatus, you should have:

### Essential Knowledge
- [ ] Basic electrical safety principles
- [ ] Understanding of capacitor discharge hazards
- [ ] CPR/First Aid training (recommended)
- [ ] Familiarity with this safety document

### Essential Skills
- [ ] Ability to use a multimeter safely
- [ ] Experience with soldering and electronics assembly
- [ ] Ability to recognise electrical faults
- [ ] Calm response to unexpected events

### Recommended Background
- [ ] Previous experience with HV systems
- [ ] Understanding of experimental physics methodology
- [ ] Familiarity with hackspace/makerspace safety culture

---

## Incident Reporting

All incidents, near-misses, and safety concerns must be documented:

### What to Report
- Electric shocks (even minor)
- Equipment failures
- Near-miss events
- Unexpected behaviours
- Safety equipment failures

### Reporting Format

```markdown
## Incident Report

**Date/Time:** 
**Personnel Present:** 
**Activity:** 

### Description
[What happened]

### Immediate Actions Taken
[What you did]

### Root Cause Analysis
[Why it happened]

### Corrective Actions
[What will prevent recurrence]

### Follow-up Required
[Any outstanding actions]
```

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024-XX-XX | [Name] | Initial release |

**This document must be reviewed before each build session.**

---

## Signatures

I have read and understood this safety documentation:

| Name | Date | Signature |
|------|------|-----------|
| | | |
| | | |
| | | |

---

*Safety is not optional. If you're unsure about any aspect of this project, stop and seek advice.*
