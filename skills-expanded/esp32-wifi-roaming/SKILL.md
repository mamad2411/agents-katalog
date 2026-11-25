---
name: esp32-wifi-roaming
description: Use when designing Wi-Fi roaming, multi-AP failover, reconnect policy, RSSI thresholds or field deployments across access points.
license: MIT
---

# Wifi Roaming

Wi-Fi roaming behavior depends on station firmware, AP configuration, security mode, RF environment and framework version. A fixed RSSI threshold is not a universal roaming solution.

## Deployment survey

Record AP model/firmware, band, channel plan, security mode, RSSI and noise floor at each handoff area. Check overlapping coverage and channel utilization. Validate antenna placement inside the final enclosure; bench RSSI does not predict installed performance.

## Roaming policy

Define when to scan, disconnect and avoid ping-pong between APs. Use hysteresis and minimum dwell time; a single weak sample should not trigger a roam. Prefer AP-assisted 802.11k/v/r only when both infrastructure and station support are confirmed. Do not assume seamless fast transition on every ESP32 target.

## Reconnect state machine

Separate association, authentication, DHCP and application-server availability. Use bounded exponential backoff with jitter and reset backoff after stable operation. Preserve local control during outage and avoid blocking event callbacks. Do not restart the entire device for every AP loss.

## Validation

| Scenario | Measure |
|---|---|
| Walk between AP cells | Handoff interruption and packet loss |
| Same SSID, different security | Association result |
| AP disappears | Recovery time and retry load |
| RSSI fluctuates near threshold | Ping-pong count |
| DHCP server delayed | State and timeout behavior |
| Busy 2.4 GHz channel | Latency and loss under load |

## Agent rules

Do not promise seamless roaming without target/AP evidence. Log BSSID, channel, RSSI, disconnect reason, DHCP state and outage duration. Keep application reconnect independent from Wi-Fi association.

## Field evidence to capture

- Record the exact ESP32 SoC, module, board revision and schematic revision.
- Record framework, compiler, driver version and relevant configuration flags.
- Preserve raw measurements and error codes before applying filters or retries.
- Separate a suspected cause from a reproduced root cause and a verified fix.
- Link the test result to a reproducible fixture or documented manual procedure.

## Version and safety boundary

Check the selected target's datasheet, errata and framework release notes before choosing APIs or pin capabilities. Electrical protection, isolation, overcurrent limits and safe outputs must be designed independently of firmware. A passing host test is not evidence of electrical compliance or field reliability.
