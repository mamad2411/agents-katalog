---
name: esp32-power-integrity
description: Use when diagnosing ESP32 brownouts, radio transmit resets, battery sag, relay inrush, regulator heating or intermittent boot failures.
license: MIT
---

# Power Integrity

Power integrity is a hardware property that firmware logs reveal only after failure. Wi-Fi, BLE, LoRa, camera, motors and relays create dynamic loads; average-current arithmetic alone is insufficient.

## Power budget

Separate average current, peak current and transient response. A regulator that meets average load can still collapse during a radio burst. Include module, radio, sensors, display, relay coil, actuator and conversion losses. Check dropout, thermal derating, current limit and battery impedance at low temperature.

## Measurement

Measure 3V3 at the module supply pins during radio and actuator events using suitable probing technique. Capture minimum voltage, duration and ringing; a multimeter may miss short dips. Measure input rail simultaneously to distinguish source/cable sag from regulator behavior. Compare idle, Wi-Fi TX, BLE TX, LoRa TX and relay switching.

## Layout and mitigation

Follow the module reference design for decoupling and supply routing. Keep high-current return paths away from analog references and communication references. Select capacitors by effective capacitance under DC bias, ESR and transient requirements. Use separate supplies or controlled sequencing for motors/relays when necessary.

## Safe firmware response

Stagger radio and actuator startup where possible. Detect repeated brownout and preserve reset reason. Do not disable brownout detection as a production workaround. Define safe outputs during reset and ensure external pull resistors establish safe states before firmware runs.

## Verification

| Test | Evidence |
|---|---|
| Radio transmit burst | Rail waveform and reset counter |
| Relay/motor inrush | Rail sag and EMI observation |
| Low battery / cold | Startup margin |
| Peripheral disconnected | Fault isolation |
| Long-duration duty cycle | Thermal and battery trend |

## Agent rules

Never infer a power fix from a log alone; request rail measurements. Distinguish brownout from watchdog, panic and software reset. Include peak and average budgets. Keep protection and safe-state design independent of application firmware.


## Field capture

Record rail voltage at the module pins during the event, along with source voltage, current waveform, reset reason and load state.
