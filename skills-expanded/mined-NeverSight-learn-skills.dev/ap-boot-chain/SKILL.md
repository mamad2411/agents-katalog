---
name: ap-boot-chain
description: Explains upstream ArduPilot ChibiOS boot from STM32 reset through crt0, board init, AP_HAL main, HAL run, AP_Vehicle setup, and scheduler loop. Use for startup, vector table, VTOR, linker entry, early HardFault, hal.run, AP_HAL_MAIN_CALLBACKS, or reset-to-main questions.
---

# AP Boot Chain

## When To Use

Use this skill for questions about:

- STM32 reset, vector table, `Reset_Handler`, ChibiOS crt0
- `__early_init`, `__late_init`, `boardInit`
- `AP_HAL_MAIN` or `AP_HAL_MAIN_CALLBACKS`
- `hal.run()`, `setup()`, `loop()`
- HardFault before vehicle setup
- bootloader-to-application transition at a flash offset

## First Files To Read

- `modules/ChibiOS/os/common/startup/ARMCMx/compilers/GCC/crt0_v7m.S`
- `libraries/AP_HAL_ChibiOS/hwdef/common/board.c`
- `libraries/AP_HAL/AP_HAL_Main.h`
- `libraries/AP_HAL_ChibiOS/HAL_ChibiOS_Class.cpp`
- `libraries/AP_Vehicle/AP_Vehicle.cpp`
- `_shared/call-flows/boot-to-main.md`

## Workflow

1. Identify whether the question is about bootloader or application boot.
2. If the fault occurs before `main()`, inspect vector table, linker origin, crt0, and `board.c`.
3. If the fault occurs after `main()`, inspect `AP_HAL_MAIN_CALLBACKS`, `HAL_ChibiOS::run()`, and `main_loop()`.
4. If `setup()` starts but `loop()` does not, move to `ap-runtime-core`.
5. If the app is reached from bootloader, also read `ap-bootloader-firmware`.

## Key Contract

ChibiOS application boot is:

```text
Reset_Handler
→ crt0_v7m.S
→ __early_init()
→ __late_init()
→ main()
→ hal.run()
→ AP_Vehicle::setup()
→ AP_Vehicle::loop()
→ AP_Scheduler::loop()
```

## Checkpoints

- [ ] The vector table is at the linked flash origin.
- [ ] Stack pointer points into RAM.
- [ ] Reset handler points into valid flash.
- [ ] `FLASH_RESERVE_START_KB` matches bootloader/app layout.
- [ ] `__early_init()` does not depend on initialized globals.
- [ ] `hal.run()` reaches `main_loop()`.
- [ ] `AP_Vehicle::setup()` is called exactly once.
- [ ] `AP_Vehicle::loop()` is called repeatedly.

## References

- Shared call flow: `../_shared/call-flows/boot-to-main.md`
- Bootloader details: `../ap-bootloader-firmware/SKILL.md`
- HAL semantics: `../ap-hal-abstract/SKILL.md`
- ChibiOS HAL details: `../ap-hal-chibios/SKILL.md`

## Boundaries

This skill is ChibiOS canonical. Other startup systems should be treated as platform-specific ports and checked against `ap-hal-abstract` and `ap-porting-playbook`.
