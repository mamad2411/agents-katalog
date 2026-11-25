---
name: iot-radio-rf-policy
description: Policy-only guidance for wireless and RF security assessment — explains SDR-based signal analysis, spectrum monitoring, and RF protocol review boundaries, unlock gates, legal and spectrum-regulation constraints, safer alternatives, and explicit refusal of active transmission, jamming, or unauthorized spectrum use.
disable-model-invocation: true
risk: disabled-default
allowed-modes: [red-team, offensive, ctf]
authorization-required: yes
evidence-outputs: [policy-note, approval-record, scope-decision]
disabled-category: wireless
---

# IoT radio and RF security — policy and boundaries

This skill is policy-only and explains the wireless/RF assessment boundary for `pi-pentest-agent`. Wireless and RF security testing is disabled by default because active radio transmission can affect nearby devices, interfere with licensed spectrum users, violate telecommunications regulations, and impact unintended targets including emergency services, aviation, medical devices, and critical infrastructure.

## Required inputs

- Written scope naming each wireless device, frequency band, protocol, maximum transmission power, modulation type, time window, physical test area boundary, and prohibited interactions.
- Regulatory authorization: FCC experimental license, ISM compliance statement, or equivalent spectrum authorization for the jurisdiction.
- Lab certification: Faraday cage, anechoic chamber, or certified RF test lab confirmation.
- Valid authorization cache covering the lab/device target and spectrum authorization proof.
- Explicit per-engagement consent that names wireless/RF testing explicitly.
- Known frequency bands, protocols, and modulation types from firmware analysis or datasheet/FCC filing review.

## Required gates

1. Repo config unlock for `wireless` category via `pentest_agent_validate_policy`.
2. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
3. `pentest_agent_parse_scope` → `pentest_agent_validate_target` for every device and frequency band.
4. `pentest_agent_check_authorization` before any active transmission.
5. Aggressive risk approval through executor gates for any transmission beyond passive reception.
6. `pentest_agent_execute_tool` for all execution — never raw shell, never raw SDR transmission commands.
7. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Why wireless is disabled by default

- **Legal risk**: radio transmission requires regulatory authorization (FCC in the US, ETSI/Ofcom in Europe, ACMA in Australia, etc.). Unauthorized transmission at certain frequencies or power levels is illegal in most jurisdictions.
- **Unintended interference**: RF signals propagate beyond the intended test area. Bluetooth, Wi-Fi, Zigbee, LoRa, and SDR transmissions can interfere with nearby devices — including medical implants, industrial control systems, and emergency communications.
- **Spectrum licensing**: many frequency bands require a license. Even ISM bands (2.4 GHz, 5 GHz, 915 MHz, 868 MHz) have power and duty-cycle restrictions that vary by country.
- **Collateral impact**: jamming testing (even unintentional) can disable Wi-Fi networks, Bluetooth Low Energy medical sensors, garage-door openers, key fobs, tire-pressure monitors, and other safety-critical wireless systems.
- **No safe default**: unlike web application testing where scope boundaries are IP/domain-based, RF boundaries are physical and uncontrollable. There is no equivalent of a `Host` header or CIDR block for RF that reliably constrains transmissions.

## Boundary

This skill covers wireless and RF assessment policy only. It does not authorize, enable, or guide any active radio transmission, signal capture beyond passive monitoring in authorized bands, or protocol exploitation. All active RF work requires the gates below.

## Required unlock process

Before any wireless/RF active assessment can proceed:

1. **Repo config unlock**: the `wireless` category must be explicitly enabled in `.pi/pentest-agent/config.json` (`dangerousCategories.wireless: true`). This is a maintainer-level decision, not per-engagement.
2. **Per-engagement consent**: the engagement must include explicit, written consent for wireless/RF testing from the party that owns or controls the physical test environment.
3. **Scope definition**: the scope must define exact device models, frequency bands, maximum transmission power, modulation types, time window, physical test area, and prohibited interactions.
4. **Spectrum authorization**: the operator must provide the relevant regulatory authorization (FCC experimental license, ISM compliance statement, or equivalent for the jurisdiction) before transmission begins.
5. **Authorization cache**: valid authorization cache covering the lab/device target, proof of spectrum authorization, and explicit consent record.
6. **Aggressive risk approval**: any transmission beyond passive reception is classified as aggressive risk and requires explicit approval through executor gates.

## Safer alternatives

When the wireless category is not unlocked, prefer these safer alternatives:

1. **Firmware analysis**: extract and analyze the device firmware for radio-configuration parameters, supported protocols, encryption keys, and pairing logic. The `iot-firmware` skill covers this workflow.
2. **Datasheet and FCC/ETSI filing review**: read the device's FCC-ID or equivalent regulatory filing, which includes internal photos, block diagrams, operational frequencies, modulation types, and antenna specifications. This is public information for certified devices.
3. **Passive spectrum monitoring**: use an SDR in receive-only mode to observe the device's RF emissions without transmitting. Passive monitoring does not require a license in most jurisdictions but still requires authorization to monitor communications that are not your own.
4. **Protocol documentation review**: study the wireless protocol specification (BLE, Zigbee, LoRaWAN, Z-Wave, proprietary) for known vulnerabilities, weak encryption, replay-attack susceptibility, and pairing weaknesses.
5. **Lab notes and report-only planning**: document the device's wireless capabilities based on firmware and datasheet analysis. Produce a report of theoretical attack surfaces without active validation.
6. **Detection review**: if the organization is assessing its own wireless security posture, review existing wireless intrusion detection (WIDS) logs, rogue-AP detection, and Bluetooth device inventories.

## What this policy covers

This policy applies to ALL wireless and RF assessment activities, including:

- **Software-defined radio (SDR)**: any use of HackRF, RTL-SDR, LimeSDR, USRP, BladeRF, or similar devices for transmission. Receive-only SDR for passive spectrum monitoring is not blocked by the wireless category but still requires scope authorization.
- **Wi-Fi (802.11)**: active probing, deauthentication, PMKID capture, WPA handshake capture, evil-twin AP deployment, KARMA attacks, and WPS PIN brute-forcing. Passive Wi-Fi monitoring (channel hopping in monitor mode without transmitting) is less restricted but still requires scope confirmation.
- **Bluetooth/BLE**: active scanning, connection attempts, GATT service enumeration, pairing attacks, and BTLEJack-style hijacking. Passive BLE advertisement sniffing is less restricted.
- **Zigbee/Z-Wave/LoRaWAN**: any active transmission, network joining, replay attacks, or device impersonation.
- **RFID/NFC**: active reading beyond publicly readable fields, card emulation, relay attacks, and cryptographic challenge-response testing.
- **Proprietary RF (sub-GHz)**: any transmission on 315 MHz, 433 MHz, 868 MHz, 915 MHz, or other ISM/sub-GHz bands.
- **Cellular (GSM/LTE/5G)**: any transmission on licensed cellular frequencies — requires carrier authorization and spectrum license.
- **GPS/GNSS**: GPS spoofing or jamming is illegal in most jurisdictions and is not permitted under any product configuration.
- **Radar and millimeter-wave**: any transmission above 6 GHz for radar or mmWave sensing.
- **Jamming**: intentional RF jamming of any frequency, protocol, or service — prohibited regardless of unlock status.

## When active RF testing may be appropriate

Active RF testing should only proceed when ALL of these conditions are met:

1. The test environment is a Faraday cage, anechoic chamber, or certified RF test lab.
2. The operator holds the appropriate spectrum license or authorization for the specific frequencies and power levels.
3. The device under test is owned by the operator or explicitly authorized by the owner.
4. No production, safety-critical, or third-party devices are in range.
5. All transmissions are at the minimum power necessary to test the target device.
6. A spectrum analyzer monitors for unintended emissions during testing.
7. The testing window is pre-approved with a defined stop time.

Even with all conditions met, active RF testing must be approved through the full executor gate chain: preflight → scope validation → authorization cache → mode check → wireless category consent → aggressive risk approval.

## Evidence for policy-only reporting

When reporting wireless/RF findings without active testing:

```text
Device: <model> | Wireless capabilities: <BLE | Wi-Fi | Zigbee | LoRa | proprietary>
Analysis method: <firmware review | datasheet | FCC filing | passive monitor>

Protocol and frequency:
  Protocol(s): <list>
  Frequency bands (from datasheet/FCC filing): <list>
  Modulation types: <list>
  Encryption: <AES-CCM | AES-128 | custom | none>

Theoretical findings (not validated):
  Weak pairing mechanism: <describe from firmware/datasheet evidence>
  Hardcoded keys in firmware: <yes — firmware analysis ref | no>
  Replay attack susceptibility: <likely — no nonce/timestamp | unlikely>
  Missing encryption: <yes — cleartext protocol | no>

Active validation status: BLOCKED — wireless category not unlocked.
Recommendation: <lab test with Faraday cage | firmware fix | protocol upgrade>
```

## Decision points

- **Escalate on wireless category unlock request**: operator must provide spectrum authorization, lab certification, and written consent → maintainer decision.
- **Escalate on passive SDR monitoring request**: less restricted but still requires scope authorization for the specific frequencies and communications being monitored.
- **Escalate on firmware/key extraction revealing wireless credentials**: critical — same key used across all devices; recommend vendor notification.
- **Deny any jamming, GPS spoofing, or cellular transmission request**: not permitted under any product configuration.

## Prohibited behavior

- Active RF transmission without the wireless category unlocked and all gates satisfied.
- Jamming, GPS spoofing, or interference with any spectrum user — prohibited regardless of config.
- Capturing or decrypting third-party communications (devices not owned or authorized by the operator).
- Deploying rogue base stations (IMSI catchers, fake cell towers, evil-twin APs) that would affect non-target devices.
- Any transmission on licensed cellular, aviation, maritime, emergency-services, or satellite frequencies.
- Using SDR transmission to bypass device authentication, clone key fobs, or impersonate authorized devices outside the lab.
- Providing step-by-step active RF attack instructions in skill bodies, reports, or evidence — policy-only language only.

## Stop conditions

- Wireless category not unlocked → stop, produce policy-only report with theoretical findings from firmware/datasheet.
- Spectrum authorization not provided → stop, request authorization before any active work.
- Physical test environment not confirmed as isolated → stop, require Faraday cage or certified lab.
- Non-target devices detected in range → stop, remove or power down non-target devices.
- Evidence would include captured third-party communications or RF samples with identifiable data → redact immediately.

## Report handoff

1. `pentest_agent_record_finding` for: hardcoded wireless keys in firmware, weak pairing mechanisms identified from code review, missing encryption on wireless protocols, and replay-attack susceptibility based on protocol analysis.
2. Reference the wireless/RF policy and note that active validation was not performed.
3. Recommend: use hardware secure elements for wireless key storage; implement anti-replay mechanisms (timestamps, nonces, sequence numbers); use industry-standard encryption (AES-CCM for BLE, WPA3 for Wi-Fi); require authenticated pairing with out-of-band verification; conduct RF security testing in a certified lab with proper spectrum authorization; and rotate per-device wireless keys — never use global keys.
