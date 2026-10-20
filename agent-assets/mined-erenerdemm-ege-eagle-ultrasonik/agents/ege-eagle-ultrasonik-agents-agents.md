# EAGLEULTRASONİK — AGENT OS V2 DECLARATIVE SUBAGENTS REGISTRY

agents:
  - name: system-architect
    description: "System Architect — High-level architecture, multi-node state machines, and cross-subsystem protocol specifications. (No direct firmware code modification)."
    tools:
      - scope: "*.md"
      - scope: ".agent/reports/"

  - name: stm32-specialist
    description: "STM32 Specialist — Expert in STM32G474RE HAL firmware, TIM15 PWM generation, OPAMP3 PT100 ADC signal processing, interrupts, and MISRA C compliance."
    tools:
      - scope: "STM32/"

  - name: esp32-hmi-specialist
    description: "ESP32 & HMI Specialist — Expert in ESP32-S3 FreeRTOS tasks, queue management, NVS recipe storage, Nextion HMI UART interface, and C++ standards."
    tools:
      - scope: "esp32/"
      - scope: "EKRAN/"

  - name: hardware-engineer
    description: "Hardware Engineer — Guardian of hardware_wiring_FINAL_AUTHORITY.md. Verifies physical pinouts, OPAMP channels, jumpers, and protects hardware source of truth."
    tools:
      - scope: "hardware_wiring_*"

  - name: communication-specialist
    description: "Communication Specialist — Multi-drop RS485 ASCII UART bus framing, command packet matrix, ASCII parsing, and clamping rules."
    tools:
      - scope: "STM32/Ultrasonik_G4_Master/Core/Src/esp32_uart.c"
      - scope: "STM32/Ultrasonik_G4_Master/Core/Inc/esp32_uart.h"
      - scope: "esp32/ekran_kontrol/"

  - name: qa-test-engineer
    description: "QA & Test Engineer — Executes HIL pytest suites (test_hil_uart.py), mock HMI and RS485 tests. Ensures zero regression without modifying core firmware source."
    tools:
      - scope: "test_*.py"

  - name: code-reviewer
    description: "Code Reviewer — Read-only code quality auditor checking MISRA C compliance, FreeRTOS thread safety, boundary checks, and git diff safety before human gates."
    tools:
      - scope: "STM32/"
      - scope: "esp32/"
      - scope: "EKRAN/"
      - scope: "test_*.py"
