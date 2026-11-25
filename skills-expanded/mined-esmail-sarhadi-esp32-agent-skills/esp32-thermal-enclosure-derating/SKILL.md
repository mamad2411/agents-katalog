---
name: esp32-thermal-enclosure-derating
description: Use when deploying ESP32 electronics in sealed, hot, cold or outdoor enclosures; especially when Wi-Fi resets, sensor drift or component failures correlate with temperature and solar load.
license: MIT
---

# Thermal design and enclosure derating

A firmware temperature reading is not a substitute for measuring the hottest component on the assembled board.
Thermal behavior depends on enclosure, PCB copper, airflow, mounting, solar load and component self-heating.

## Build a thermal budget

- Record the ambient operating range, storage range, solar exposure, altitude and enclosure ingress requirement.
- Identify heat sources: regulator, charger, radio PA, Ethernet PHY, display backlight, relay coils and external loads.
- Read absolute maximum and recommended operating limits from each component datasheet.
- Apply derating and design margin; do not operate continuously at absolute maximum ratings.
- Include worst-case simultaneous loads such as Wi-Fi transmit, display refresh, charging and relay switching.
- Separate junction temperature limits from board or enclosure ambient temperature.

## Measure the real assembly

- Place thermocouples on the regulator, ESP32 module shield, flash, power MOSFET and other likely hotspots.
- Record ambient and internal air temperature at the same time.
- Test the final enclosure, cable glands, mounting orientation and PCB revision.
- Run sustained radio traffic and maximum peripheral load until temperatures stabilize.
- Repeat at minimum and maximum supply voltage and across the intended ambient range.
- Use IR cameras carefully; emissivity and reflective shields can produce misleading readings.

## Radio and power interaction

- High transmit duty cycle raises radio and regulator dissipation; use realistic traffic patterns.
- Regulator thermal limiting can appear as brownout or unexplained reboot under radio peaks.
- Check regulator input/output ripple and transient response while hot, not only at room temperature.
- Confirm antenna clearance and enclosure material effects separately from thermal performance.
- Avoid placing temperature sensors next to a heat source if they are intended to represent ambient air.

## Firmware response

- Use sensor validity, hysteresis and dwell time to prevent rapid thermal on/off cycling.
- Define degraded modes before a thermal limit is reached: reduce transmit duty, disable nonessential loads or stop charging.
- Keep protective actions deterministic and local; cloud telemetry must not be required.
- Do not infer component junction temperature from an unrelated on-chip temperature estimate.
- Log temperature, supply voltage, radio state, reset reason and workload together.

## Environmental and mechanical details

- Check condensation, humidity, corrosion, dust and pressure equalization in outdoor installations.
- Validate gasket compression and cable entry without trapping excessive heat.
- Consider thermal expansion, connector retention and strain relief over the full temperature range.
- Do not add conformal coating without checking RF, connector, sensor and thermal implications.
- Re-test after enclosure or PCB changes; a small mechanical change can alter airflow and heat spreading.

## Verification

1. Perform thermal soak at the highest specified ambient and worst-case workload.
2. Measure hotspot temperatures and regulator rails over time.
3. Repeat radio transmit bursts, Ethernet traffic and actuator switching at thermal equilibrium.
4. Test cold start and hot restart, including brownout recovery.
5. Verify sensor calibration and firmware thresholds against a traceable reference.
6. Document the exact board, enclosure, firmware, supply and instrumentation.

## Acceptance criteria

- Thermal report contains ambient, hotspot, stabilization time and measurement uncertainty.
- Each component remains within its recommended operating range with stated margin.
- Firmware degraded-mode transitions are covered by host tests.
- No environmental rating is claimed from a bench test outside the final enclosure.

## References

- Espressif hardware design guidelines: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/
- Espressif technical documents: https://www.espressif.com/en/support/documents/technical-documents
- IPC standards overview: https://www.ipc.org/
