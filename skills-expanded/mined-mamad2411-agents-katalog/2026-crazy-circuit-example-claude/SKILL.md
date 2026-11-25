# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Firmware for a **line-following smart race car** (2026 Crazy Circuit / NXP Cup competition) built by TYUT JBD TEAM C. The car uses a 15-channel light sensor array, IMU (gyro), and quadrature encoders to autonomously navigate a track via cascaded PID control. It supports a **build mode** that records mileage intervals between track elements to Flash for analysis.

## Target Hardware

- **MCU**: Infineon TC264D (TC26xD B-Step), dual-core TriCore @ 200MHz
- **Toolchain**: TASKING compiler, AURIX Development Studio (ADS) v1.10.2 (Eclipse-based IDE)
- **Debugger**: DAP/IC5700 over JTAG

## Building

There is no Makefile or CLI build system. The project is built exclusively through the **AURIX Development Studio IDE**:
1. Open the project in ADS (`File → Import → Existing Projects`)
2. Select the active build configuration (Debug/Release)
3. Build with `Project → Build All` (Ctrl+B)
4. Flash via `Run → Debug` or `Run → External Tools → DAP programmer`

The linker script is [Lcf_Tasking_Tricore_Tc.lsl](Lcf_Tasking_Tricore_Tc.lsl).

## Architecture

### Dual-Core Split

| Core | RAM | Role |
|------|-----|------|
| CPU0 | 72KB DSPR | Real-time control: 3ms PIT ISR executes the full control loop (sensor read → PID → motor PWM) |
| CPU1 | 120KB DSPR | Non-real-time: UART serial tuning command processor (polling loop) |

CPU0 signals CPU1 to start via `cpu_wait_event_ready()` after initialization.

### Control Loop (3ms ISR on CPU0)

Every 3ms, `Car_Go()` in [code/Ctrl.c](code/Ctrl.c) runs:

```
Get_Speed() → Get_IMU() → Get_Light() → Light_Process()
→ Safety_Check() → Build_Mode_Get_Error() → Set_Speed() → Set_Out()
```

### Cascaded PID (3-tier, in [code/pid.c](code/pid.c))

1. **Position PID** (Angle_PID): 15-channel light sensor error → gyro rate target
2. **Gyro PID**: Gyro rate target vs actual Gyro_Z → differential wheel speed
3. **Wheel Speed PID** (Left_PID / Right_PID): Target speed vs encoder → motor PWM

PID supports 3 modes: positional, derivative-on-measurement, and incremental.

### Build Mode State Machine

The track is a pre-programmed action list (31 actions by default) in `Race_Action[31]`: straight segments, left turns, right turns. Mileage (encoder tick accumulation) and gyro integration detect segment boundaries and turn completion. Turns use a 2-phase approach: decelerate-and-advance then in-place rotate.

### Startup Sequence

1. Peripheral init (clock, ADC, encoders, motors, IMU)
2. Load PID parameters and speeds from Flash
3. 500-sample gyro Z zero-drift calibration (suction fan on)
4. Line scan auto-threshold calibration (200-1600 iterations)
5. UART init @ 921600 baud
6. Start 3ms PIT, signal CPU1, enter main loop

## Key Files

| File | Purpose |
|------|---------|
| [user/cpu0_main.c](user/cpu0_main.c) | CPU0 entry point: init sequence, calibration, main loop |
| [user/cpu1_main.c](user/cpu1_main.c) | CPU1 entry point: UART tuning loop |
| [user/isr.c](user/isr.c) | All ISRs; CCU60_CH0 triggers `Car_Go()` every 3ms |
| [user/isr_config.h](user/isr_config.h) | Interrupt priority and core assignment |
| [code/Ctrl.c](code/Ctrl.c) | Core control: state machine, PID cascade, build mode, Flash storage (~1475 lines) |
| [code/Fun.c](code/Fun.c) | Hardware abstraction: ADC, encoders, motor PWM, VOFA telemetry |
| [code/pid.c](code/pid.c) | PID controller with 3 modes |
| [code/Debug_Car.c](code/Debug_Car.c) | 4 debug sub-modes: wheel tuning, ground test, angle tuning, normal trace |
| [code/Uart_Adjust.c](code/Uart_Adjust.c) | Serial tuning protocol parser (@XXX=value# frame format) |
| [code/WS2812.c](code/WS2812.c) | 8-LED WS2812 strip driver with 7 light effects, dual-buffered for ISR safety |
| [code/headfiles.h](code/headfiles.h) | Central include hub; all project headers included here |
| [code/OLED/FlashFun.c](code/OLED/FlashFun.c) | Flash parameter persistence (PID gains, debug flags) |

## Serial Tuning Protocol

UART2 @ 921600 baud, frame format `@XXX=value#`. Commands in [code/Uart_Adjust.c](code/Uart_Adjust.c):

| Key | Parameter |
|-----|-----------|
| LKP, LKI | Left wheel speed PID |
| RKP, RKI | Right wheel speed PID |
| TKP, TKD | Angle (track position) PID |
| GKP, GKD | Gyro rate PID |
| YES | Save parameters to Flash (1 = save) |

VOFA telemetry frames (motor speeds, gyro, sensors, battery) are sent over the same UART. Protocol spec in [串口调参.md](串口调参.md).

## Parameter Persistence

PID gains, speeds, and debug flags are stored in **Data Flash sector 0, pages 0-3**. Turn mileage and segment edge records use pages 5-9. Loaded at startup via `Data_Load()`, saved via serial `@YES=1#` or keyboard menu.

## Library Stack

Three-layer driver architecture:
- **iLLD** (`libraries/infineon_libraries/iLLD/TC26B/`): Infineon low-level drivers
- **ZF Driver** (`libraries/zf_driver/`): SEEKFREE abstraction layer (adc, pwm, encoder, pit, uart, spi, etc.)
- **ZF Device** (`libraries/zf_device/`): Device drivers (IMU660RB, OLED, cameras)

ZF library version: v3.4.1.

## Git Branches

- `main` — primary development branch (current car)
- `test/new-car` — new car hardware testing (has `NEW_CAR_TEST_ENABLE` flag)
- `ldz/main` — collaborator branch
- `origin/refactor-decouple` — architecture refactoring effort

## Hardware Documentation

- [new_car_test_pin_config.md](new_car_test_pin_config.md) — Complete pin map for motors, IMU, ADC sensors, encoders, UART, OLED, WS2812
- [串口调参.md](串口调参.md) — Serial tuning protocol specification
- [推荐IO分配.txt](推荐IO分配.txt) — Recommended IO allocation for peripherals
- [尽量不要使用的引脚.txt](尽量不要使用的引脚.txt) — Pins to avoid (boot pins, input-only, TC264DA-incompatible)
- [artifacts/front_sensor_layout.svg](artifacts/front_sensor_layout.svg) — Light sensor board physical layout

## MCP Tools

Two MCP servers are configured in [.mcp.json](.mcp.json):
- `systematlas` — Architecture flow/sequence diagram authoring (`.systematlas/` directory)
- `flowscript` — Flow chart SVG rendering from JSON node/edge definitions
