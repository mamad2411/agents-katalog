---
name: chevelle-restoration
description: "Use when restoring or troubleshooting a 1970-1972 Chevelle or El Camino — interior trim and wiring, Hi-Tech Classics dash kits, Dakota Digital HDX gauges, or recommissioning a car after storage."
---

# 1972 Chevelle SS Interior Restoration Knowledge Base

This skill contains accumulated knowledge for Corey's 1972 Chevelle SS 396/454 interior build and recommissioning project. The car has been sitting for 3 years and uses the **Hi-Tech Classics SS Dash Kit with Dakota Digital HDX-70C-CVL gauges**.

## Project Context

- **Car**: 1972 Chevrolet Chevelle SS, 396/454 trim level
- **State**: Partially assembled, sat for 3 years
- **Dash Kit**: Hi-Tech Classics SS Dash Kit Complete with Dakota Digital HDX Gauges
- **Gauge System**: Dakota Digital HDX-70C-CVL (6 analog sweeps + 2 TFT message center displays)
- **Kit Contents**: Black SS dash face, HDX gauge cluster, HDX Control Box, senders/sensors, backing plate, 10 bulbs with sockets, SS dash harness with integrated fuse box, SS dash pad
- **Console**: Included with the Hi-Tech kit
- **Official Manual**: Dakota Digital Manual #650572B (HDX-70C-CVL.pdf at dakotadigital.com). For current firmware/manual versions, call tech support at (605) 332-6513.

## Dakota Digital HDX-70C-CVL System

### Key Features
- 6 analog gauge sweeps (tach, speedo, oil, water temp, fuel, volts)
- 2 TFT message center displays (configurable readouts)
- Capacitive touch buttons for menu/configuration
- 30+ backlight color options (configurable via buttons or Bluetooth app)
- Bluetooth connectivity for smartphone calibration/configuration
- Fully programmable via HDX Control Box

### HDX Control Box Wiring
The Control Box is the brain of the system. Mount it behind the dash in a protected, accessible location.

| Wire | Connection | Notes |
|------|-----------|-------|
| Red (constant 12V) | Battery-hot fuse (5-20A) | 18 AWG minimum, always-hot circuit |
| Pink (switched 12V) | Ignition-hot fuse | Powers gauges with key ON |
| Black (ground) | Chassis ground bolt | Clean bare metal, star washer |
| Dimmer (orange) | Headlight switch rheostat | Dash light dimming |

### HDX Sensor Connections
| Sensor | Type | Thread | Wiring | Notes |
|--------|------|--------|--------|-------|
| Oil pressure | 3-wire (SEN-01-5) | 1/8" NPT | White=SIG, Red=5V PWR, Black=GND | Use Teflon tape on threads |
| Water temp | 2-wire | 1/8" NPT | Signal + ground through block | May need bushing adapter for GM blocks |
| Speed | 3-wire pulse | Cable-drive adapter or trans | Signal, power, ground | Replaces mechanical cable |
| Fuel level | Existing tank sender | N/A | Signal wire to Control Box | Calibrate via HDX menu (empty/full points) |
| Tachometer | Coil signal | N/A | Coil (-) terminal or HEI TACH terminal | Set cylinder count in HDX menu |

### HDX Calibration
After installation, calibrate through the touch buttons or Bluetooth app:
1. Set cylinder count (8 for 396/454)
2. Calibrate speedometer (tire size, gear ratio, or GPS calibration)
3. Set fuel sender range (mark empty and full points)
4. Select backlight color
5. Configure message center displays (choose which readings to show)

### HDX Troubleshooting
- **Gauges don't power on**: Check constant 12V (red wire), ground, and 5-20A fuse
- **Gauges power but no readings**: Check switched 12V (pink wire) and sensor connections
- **Oil pressure reads zero**: Verify 3-wire SEN-01-5 sender wiring (white/red/black)
- **Speedo inaccurate**: Recalibrate via GPS method or enter exact tire size/gear ratio
- **Fuel gauge wrong**: Recalibrate empty/full points through HDX menu
- **Backlight flickers**: Check dimmer wire connection and headlight switch rheostat

## Installation Order (Critical)

Follow this sequence — skipping ahead causes rework:

1. Sound deadening / Dynamat (floor, firewall, doors, trunk)
2. Wiring harness routing (dash harness, engine harness, rear harness)
3. Dash metal support structure + dash assembly
4. Steering column and wheel
5. Headliner
6. Carpet and floor padding
7. Door panels
8. Console
9. Seats and seat belts
10. Rear panels, package tray, trim
11. Stereo and accessories
12. Final inspection and recommissioning

## Dash Metal Support Structure

The dash assembly mounts to the firewall through a **stamped steel dash support bracket** (also called the dash carrier or dash frame). This is a critical structural piece.

### Components
- **Upper dash support bar**: Spans the full width of the firewall, bolts at each end to the A-pillar area and to the firewall center. Typically 4-6 bolts, 5/16"-18 x 3/4" hex head with lock washers.
- **Lower dash support brackets** (left and right): L-shaped brackets that anchor the bottom of the dash assembly. Bolts to firewall with 5/16"-18 hardware.
- **Center support brace**: Vertical brace behind the radio/heater area, connects upper bar to the lower cowl.
- **Steering column bracket**: Integral to the dash support, holds the column clamp. Two 3/8"-16 bolts with lock washers.

### Key Fasteners
- Dash support to firewall: 5/16"-18 x 3/4" Grade 5 hex bolts, lock washers, flat washers
- Column clamp bolts: 3/8"-16 x 1" Grade 5
- Dash pad to dash frame: 4 spring clips (2 long: 2-3/4" x 5/8", 2 short: 2-3/8" x 5/8")

### Inspection Before Assembly
Before mounting anything, inspect the dash support for:
- Rust at firewall bolt holes (repair or reinforce if needed)
- Bent or tweaked brackets (straighten before installation)
- Missing or broken weld tabs
- Cracked steering column bracket area

### Critical: Ground Return Through Dash Structure
**Wire brush all firewall bolt holes to bare metal before bolting the dash support in place.** Paint, powder coat, or seam sealer at the contact face prevents good ground return through the dash structure — which is the path the gauges, lights, and radio use back to chassis ground. Hidden ground problems here are extremely hard to diagnose later because everything physically connects but voltage drops under load.

## Reference Files

For detailed screw-by-screw hardware specs for every interior component, read:
`references/hardware-specs.md`

For connector identification, wire color codes, and harness routing:
`references/wiring-guide.md`

For Dakota Digital HDX-70C-CVL gauge system installation, calibration, and troubleshooting:
`references/hdx-gauges.md`

For the full checklist of fluid, brake, fuel, battery, and safety items for a car that sat 3 years:
`references/recommissioning.md`

## Key Suppliers

| Supplier | Specialty | URL |
|----------|-----------|-----|
| Hi-Tech Classics | SS dash conversion kits | hitechclassics.com |
| Dakota Digital | HDX gauge systems, senders, accessories | dakotadigital.com |
| SS396.com | Chevelle restoration parts | ss396.com |
| Ausley's Chevelle Parts | OEM reproduction hardware | chevelle.com |
| YEARONE | Interior/exterior parts | yearone.com |
| OPGI | Interior kits, weatherstripping | opgi.com |
| Muscle Car Central | Clips, fasteners, brackets | musclecarcentral.com |
| Classic Dash | Aftermarket dash kits | classicdash.com |
| American Autowire | Wiring harnesses | americanautowire.com |
| Painless Performance | Wiring harnesses | painlessperformance.com |
| Lectric Limited | OEM-style wiring | lectriclimited.com |
| Dynamat | Sound deadening | dynamat.com |

## Community Resources

- **Team Chevelle Forum**: chevelles.com — The go-to forum for Chevelle-specific questions. Search before posting.
- **72 Chevelle Wiring Connection Pictures**: chevelles.com/threads/72-chevelle-wiring-connection-pictures-and-diagrams.401618/ — Photographic guide to every connector
- **ChevelleStuff.net**: chevellestuff.net — Wiring diagrams, specs, and tech info

## Important Notes

### SS Dash Harness vs. Sweep Harness
The SS round-gauge dash harness is NOT interchangeable with the sweep-style gauge harness. The Hi-Tech kit includes the correct SS harness. Do not mix harnesses.

**Why this matters:** Mixing harnesses will short fuses and disable gauges — the connector positions look similar but feed different circuits. Verify your Hi-Tech kit part number against the SS variant before opening the harness bag. Once the harness is uncoiled and routed, it's hard to return.

### Year Differences (70 vs 71 vs 72)
While 1970-1972 Chevelles share the same A-body platform:
- 1970 and 1971 share most dash wiring, but differ from 1972
- 1972 moved to a different emissions/ignition setup affecting underhood wiring
- Bulkhead connectors vary by year and factory options
- Always verify part numbers against YOUR specific year

### Torque Specifications (Key Values)
- Steering wheel nut: 35 ft-lbs
- Steering gear mounting bolts: 70 ft-lbs
- Seat track to floor bolts: 25-35 ft-lbs (5/16"-18)
- Seat belt anchor bolts: 30 ft-lbs (Grade 8 required)
- Steering column clamp: 20 ft-lbs
- Wheel lug nuts: 85-100 ft-lbs (star pattern)
