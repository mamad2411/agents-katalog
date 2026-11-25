---
name: disabled-wireless-policy
description: Policy-only boundary for wireless testing, RF attacks, and radio-spectrum requests. Explains refusal rationale, unlock prerequisites, and safer defensive alternatives.
disable-model-invocation: true
risk: disabled-default
allowed-modes: [red-team, offensive]
authorization-required: yes
evidence-outputs: [policy-note, approval-record, safer-alternatives]
disabled-category: wireless
---

# Wireless testing policy

Use this skill to explain why wireless attack workflows are disabled by default. This skill is policy-only. It must not provide capture steps, cracking workflow, deauthentication guidance, rogue access point setup, proximity tactics, key handling, or command sequences.

## Boundary

Wireless testing interacts with radio-frequency spectrum, which is regulated in most jurisdictions. Even authorized testing can affect devices outside the target scope — neighboring offices, apartments, medical facilities, or critical infrastructure — and can violate telecommunications laws if transmission power, frequency bands, or modulation types exceed license privileges.

Treat every wireless request as high abuse-risk. The only allowed discussion paths are:

- Wireless architecture review: assessing WPA3/WPA2-Enterprise configuration, RADIUS server posture, client-isolation settings, and guest-network segmentation.
- Configuration audit: reviewing access-point settings, firmware versions, and known-vulnerability exposure without active scanning.
- Detection engineering: designing rules that detect rogue access points, deauthentication floods, or unusual probe-request patterns.
- Spectrum policy planning: understanding regulatory requirements and defining authorized testing boundaries.

Do not help with: capturing handshakes, forcing client deauthentications, cracking WPA/WPA2/WPA3 PSKs, setting up rogue access points, conducting evil-twin attacks, jamming, replay attacks, Bluetooth/BLE/Zigbee exploitation, SDR-based attacks, or any transmission beyond normal client operation. Do not store keys, passphrases, raw packet captures, or device identifiers.

## Required unlock process

All gates must pass before any wireless-related workflow can be considered:

- Repo config explicitly unlocks `wireless` in `.pi/pentest-agent/config.json`.
- User provides explicit per-engagement consent that defines the physical location, frequency bands, transmission power limits, equipment, and testing window.
- Rules of engagement define the exact SSIDs, BSSIDs, channels, and time window for testing.
- Regulatory compliance is documented: the operator holds appropriate licenses, transmissions stay within authorized bands and power limits, and spectrum-regulator notification is complete when required.
- Physical-location authorization is documented: building owner, facilities management, and any co-located tenants are notified.
- Stop conditions are defined: any interference with non-target devices, medical equipment, or critical infrastructure triggers immediate halt.
- Authorization cache is valid for the engagement scope.
- Risk approval is recorded for disruption-prone behavior and regulatory exposure.
- Output is bounded, redacted, and stored only under `.pi/pentest-agent/`.

Use `pentest_agent_check_authorization`, `pentest_agent_validate_target`, `pentest_agent_validate_policy`, and `pentest_agent_request_unlock` to confirm gates. If any gate fails, refuse active help.

## Safer alternatives

Prefer these non-disruptive wireless security assessments:

- **Configuration baseline audit**: Review wireless controller or access-point configurations for encryption type, authentication method, PMF (Protected Management Frames) status, client isolation, and rogue-AP detection settings.
- **WPA Enterprise review**: Assess RADIUS server configuration, EAP method selection, certificate validation settings, and supplicant posture for 802.1X-secured networks.
- **Guest network segmentation audit**: Review whether guest traffic is isolated from internal networks, whether client isolation is enforced, and whether captive-portal bypasses are mitigated.
- **Firmware and patch review**: Check access-point and controller firmware versions against vendor security advisories. Identify known vulnerabilities without active exploitation.
- **Physical security walkthrough**: Inspect access-point placement, physical access to network ports in public areas, and rogue-device attachment risks.
- **Detection and alerting checklist**: Review whether the wireless infrastructure and SIEM can detect rogue APs, deauthentication floods, MAC spoofing, or probe-request anomalies.
- **Asset inventory and classification**: Map all authorized SSIDs, BSSIDs, and wireless devices. Identify unknown or abandoned networks without active scanning.
- **Report-only risk narrative**: Use `pentest_agent_render_report` to document wireless security gaps, regulatory considerations, and recommended configuration changes.

## Decision guidance

| Request | Response |
|---|---|
| "Crack our Wi-Fi password" | Refuse unless all unlock gates pass and regulatory compliance is documented. Offer configuration audit. |
| "Set up a rogue access point" | Refuse. Do not configure or deploy transmission equipment that impersonates authorized networks. |
| "Audit our WPA3 configuration" | Allow. Conduct read-only configuration review. |
| "We detected a rogue AP; help investigate" | Allow. Help analyze collected logs and plan containment steps. |
| "Capture handshakes from our office Wi-Fi" | Refuse unless unlock gates pass. Even authorized capture affects devices outside direct control. |

## Depth rules

- Keep this skill policy-only: explain refusal boundary, approval prerequisites, regulatory constraints, audit trail requirements, and safer alternatives.
- Do not provide active wireless procedures, capture techniques, cracking workflows, rogue-AP setup, deauthentication guidance, channel-hopping scripts, or SDR-based attack instructions.
- Route allowed discussion toward configuration auditing, architecture review, firmware-patch assessment, detection engineering, and report-only risk documentation.
- Require repo unlock, per-engagement consent, regulatory compliance documentation, physical-location authorization, defined stop conditions, fresh authorization cache, risk approval, and redacted local evidence before any active workflow.
- Refuse when user asks to bypass disabled-default policy, transmit outside authorized bands, or affect non-target devices.
- Cross-reference related skills: `iot-radio-rf-policy`, `iot-firmware`, `blue-detect`, `blue-ir`.

## Evidence

Record policy decision, requested activity, location and spectrum constraints if discussed, regulatory notes, approval status, safer alternative chosen, and redaction notes. Never store keys, passphrases, raw packet captures, BSSID/client MAC lists, device identifiers, or unredacted wireless logs.
