---
name: ap-session-hub
description: Routes standard ArduPilot development questions to the correct project skill. Use at session start or when users mention boot, hwdef, HAL, drivers, scheduler, params, EKF, control, vehicle modes, MAVLink, mission, waf, SITL, testing, ChibiOS, or porting ArduPilot to a new MCU, board, or RTOS.
---

# ArduPilot Session Hub

## Workflow

1. Classify the user request by layer: boot, board, HAL, driver, runtime, algorithm, vehicle, communication, build, test, porting, or ecosystem.
2. Read the matching skill's `SKILL.md` first.
3. If the request crosses layers, read the canonical call flow in `_shared/call-flows/`.
4. Use ChibiOS/waf/SITL as the default reference path.
5. If a topic is not in v1, experimental, or platform-specific, check `_shared/scope-boundaries.md` before answering.

## Routing

| User topic | Read first |
|---|---|
| reset, crt0, `board.c`, `main`, `hal.run`, HardFault before setup | `../ap-boot-chain/SKILL.md` |
| bootloader, APJ, board id, signed firmware, app address | `../ap-bootloader-firmware/SKILL.md` |
| hwdef, pins, DMA, linker, ROMFS, ChibiOS board support | `../ap-hwdef-board/SKILL.md` |
| new HAL, scheduler semantics, UART/SPI/I2C/Storage/RC contracts | `../ap-hal-abstract/SKILL.md` |
| ChibiOS HAL implementation, threads, DMA/cache, watchdog, SD, USB | `../ap-hal-chibios/SKILL.md` |
| new MCU, new board, new RTOS porting order | `../ap-porting-playbook/SKILL.md` |
| sensor driver backend, probe, detect, dev_id, health | `../ap-driver-library/SKILL.md` |
| AP_Vehicle, scheduler, params, prearm, failsafe, watchdog | `../ap-runtime-core/SKILL.md` |
| waf, boards.py, wscript, build options, conditional compile | `../ap-build-waf/SKILL.md` |
| SITL, examples, gtest, autotest, CI | `../ap-test-sitl-autotest/SKILL.md` |
| EKF, AHRS, GPS/Baro/Compass fusion | `../ap-ekf-navigation/SKILL.md` |
| PID, motors, TECS, L1, SRV output | `../ap-control-actuation/SKILL.md` |
| Copter, Plane, QuadPlane, Rover, Sub modes | `../ap-vehicle-modes/SKILL.md` |
| MAVLink, GCS, parameter protocol, serial routing | `../ap-gcs-mavlink/SKILL.md` |
| Mission, Fence, Rally, Terrain | `../ap-mission-geo/SKILL.md` |
| uncertain failure or root cause investigation | `../ap-debug-root-cause/SKILL.md` |

## Shared References

- Topic coverage: `../_shared/topic-map.md`
- Scope and risk boundaries: `../_shared/scope-boundaries.md`
- Terms and units: `../_shared/glossary.md`
- Canonical call flows: `../_shared/call-flows/`

## Defaults

- Canonical board/HAL path: `libraries/AP_HAL_ChibiOS/`
- Canonical board description path: `libraries/AP_HAL_ChibiOS/hwdef/`
- Canonical vehicle entry pattern: `AP_HAL_MAIN_CALLBACKS(&vehicle)`
- Canonical build path: `./waf configure --board <board>` then `./waf <vehicle>`
- Canonical simulation path: `Tools/autotest/sim_vehicle.py`
