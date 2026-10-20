# EAGLEULTRASONİK — AGENT OS V2 CORE ENGINEERING RULES

## Entrypoint & Rule Hierarchy
Detailed engineering rules are modularized under `.agents/rules/`:
- `00-global-engineering.md`: C/C++ Memory Safety, Non-blocking Loops, MISRA C
- `01-source-of-truth.md`: Hardware Authority Protection & Pinout Conflict Guard
- `02-scope-control.md`: Subagent Directory Write Scope Enforcement
- `03-stm32.md`: STM32G474 HAL, TIM15 PWM, OPAMP3 PT100, Interrupt Safety
- `04-esp32.md`: ESP32-S3 FreeRTOS Tasks, Queues, NVS Storage, Nextion HMI
- `05-communication.md`: RS485 Multi-drop ASCII UART Bus Framing & Packet Matrix
- `06-testing.md`: Pytest HIL & Mock Verification Standards
- `07-agent-orchestration.md`: Task Complexity Classification & Minimum Agent Policy

## Core Project Guidelines
1. **STM32 Geliştirme Kuralları**
   - STM32 dizinindeki kodlarda her zaman **HAL kütüphanelerini** kullanın.
   - **MISRA C** standartlarına uygun, bellek sızıntısı yaratmayan güvenli C kodu yazın.

2. **ESP32 Geliştirme Kuralları**
   - ESP32 dizininde **FreeRTOS** standartlarına uygun C++ kodları üretin.

3. **HIL Test Kuralları**
   - HIL testleri için (`test_hil_uart.py`) **pytest** standartlarını kullanın.
