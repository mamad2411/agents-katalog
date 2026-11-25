---
name: cloud-zerotrust-deviceposture
description: "Cloud Zerotrust Deviceposture."
domain: cybersecurity
---

|
| Device Posture | Collection of endpoint security attributes (OS version, encryption, EDR status, patch level) evaluated before granting access |
| CrowdStrike ZTA Score | Numerical score (1-100) calculated by CrowdStrike Falcon assessing endpoint security posture based on OS signals and sensor configuration |
| Device Compliance Policy | MDM-defined rules specifying minimum security requirements (encryption, PIN, OS version) that devices must meet |
| Conditional Access | Policy engine (Entra ID, Okta) that evaluates user identity, device compliance, location, and risk before allowing access |
| Device Trust | Verification that an endpoint is managed, enrolled, and meets security baselines before treating it as trusted |
| Posture Drift | Degradation of device security posture over time (expired patches, disabled encryption) that should trigger access revocation |

## Tools & Systems

- **CrowdStrike Falcon ZTA**: Real-time endpoint posture scoring based on OS and sensor security signals
- **Microsoft Intune**: MDM platform enforcing device compliance policies and reporting to Entra ID Conditional Access
- **Jamf Pro**: Apple device management with compliance rules for macOS and iOS endpoints
- **Microsoft Entra ID Conditional Access**: Policy engine consuming Intune compliance and risk signals for access decisions
- **Okta Device Trust**: Device assurance policies integrating with CrowdStrike, Chrome Enterprise, and MDM platforms
- **Cloudflare Device Posture**: WARP client-based posture checks for disk encryption, OS version, and third-party EDR

## Common Scenarios

### Scenario: Enforcing Device Compliance for 2,000 Endpoints Across Windows and macOS

**Context**: A healthcare company with 2,000 endpoints (70% Windows, 30% macOS) must enforce HIPAA-compliant device posture before allowing access to patient data systems. Devices are managed by Intune (Windows) and Jamf (macOS) with CrowdStrike Falcon deployed on all endpoints.

**Approach**:
1. Define Windows compliance policy in Intune: BitLocker, Secure Boot, TPM, Defender enabled, OS >= 10.0.19045
2. Define macOS compliance policy in Jamf: FileVault, Gatekeeper, SIP, Firewall, OS >= 14.0
3. Configure CrowdStrike ZTA thresholds: >= 70 for general apps, >= 85 for patient data systems
4. Create Entra ID Conditional Access policies requiring compliant device + MFA for all cloud apps
5. Configure 24-hour grace period for newly non-compliant devices before blocking
6. Set up weekly compliance report for IT showing non-compliant devices and remediation actions
7. Implement automated remediation via Intune: push BitLocker enablement, deploy pending patches

**Pitfalls**: Grace periods must be long enough for IT to remediate but short enough to limit risk exposure. CrowdStrike ZTA scores can fluctuate with sensor updates; avoid setting thresholds too aggressively initially. BYOD devices may lack MDM enrollment; provide a separate Browser Access path with reduced functionality for unmanaged devices.

## Output Format

```
Device Posture Assessment Report
==================================================
Organization: HealthCorp
Report Date: 2026-02-23
Total Managed Devices: 2,000

COMPLIANCE BY PLATFORM:
  Windows (1,400 devices):
    Compliant:              1,302 (93.0%)
    Non-compliant:            98 (7.0%)
    Top Issue: Missing patches (45), BitLocker disabled (23)

  macOS (600 devices):
    Compliant:                567 (94.5%)
    Non-compliant:             33 (5.5%)
    Top Issue: OS outdated (18), FileVault disabled (8)

CROWDSTRIKE ZTA SCORES:
  Average Score:              78.4
  Devices >= 85 (Critical):  1,456 (72.8%)
  Devices >= 70 (Standard):  1,812 (90.6%)
  Devices < 50 (Blocked):       34 (1.7%)

CONDITIONAL ACCESS IMPACT (last 7 days):
  Total sign-in attempts:    45,678
  Blocked by posture:           312 (0.7%)
  Remediated within 24h:        289 (92.6%)
  Still non-compliant:           23

POSTURE DRIFT ALERTS:
  Encryption disabled:            5
  EDR sensor stopped:             3
  OS downgraded:                  1
```
