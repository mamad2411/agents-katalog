---
name: identity-analytics-anomalous
description: "Identity Analytics Anomalous."
domain: cybersecurity
---

|
| **Impossible Travel** | Authentication anomaly where a user logs in from two geographically distant locations within a timeframe that makes physical travel impossible |
| **Password Spraying** | Credential attack that tries a small number of commonly used passwords against many accounts to avoid lockout thresholds |
| **Credential Stuffing** | Automated attack using stolen username/password pairs from data breaches to gain unauthorized access to accounts |
| **UEBA** | User and Entity Behavior Analytics technology that builds behavioral baselines and detects deviations using machine learning and statistical analysis |
| **Behavioral Baseline** | Statistical profile of a user's normal authentication patterns including typical hours, locations, devices, and applications |
| **Isolation Forest** | Unsupervised machine learning algorithm that detects anomalies by isolating observations that differ from the majority of data points |
| **Risk Score** | Composite numerical value aggregating multiple anomaly signals with weighted scoring to prioritize authentication threats |

## Tools & Systems

- **Microsoft Sentinel UEBA**: Cloud-native SIEM with built-in entity behavior analytics for Azure AD and multi-cloud authentication anomaly detection
- **Exabeam Advanced Analytics**: UEBA platform using machine learning for user session analysis and automated threat timeline construction
- **Splunk UBA**: Behavioral analytics add-on for Splunk providing pre-built authentication anomaly models and risk scoring
- **Elastic SIEM ML Jobs**: Machine learning anomaly detection jobs for authentication log analysis in the Elastic Stack

## Common Scenarios

### Scenario: Detecting Compromised Executive Account After Password Spray

**Context**: SOC observes a spike in failed authentication attempts from a cloud VPS IP address targeting 200+ accounts. Two hours later, an executive account shows successful authentication from the same IP range followed by mailbox rule creation and data exfiltration.

**Approach**:
1. Run password spray detection across the timeframe to identify all targeted accounts
2. Cross-reference targeted accounts with subsequent successful logins from related IP ranges
3. Build behavioral baseline for the executive account and flag all deviations
4. Check for impossible travel between the executive's last legitimate login and the attacker's session
5. Identify post-compromise activity: mailbox rules, file downloads, delegated access changes
6. Calculate composite risk score combining password spray, new IP, off-hours login, and new device signals
7. Trigger automated response: force session termination, disable account, notify manager

**Pitfalls**:
- Relying on single-signal detection (failed logins only) misses successful spray results
- Not correlating across identity providers when users have accounts in multiple IdPs
- Static thresholds that do not account for legitimate VPN IP changes or travel
- Ignoring successful authentications after the spray window closes (attackers may wait before using credentials)

## Output Format

```
AUTHENTICATION ANOMALY DETECTION REPORT
=========================================
Analysis Period:   2026-02-01 to 2026-02-24
Total Auth Events: 2,847,392
Users Monitored:   3,847
Alert Sources:     Azure AD, Okta, Windows AD

THREAT DETECTION SUMMARY
Password Spray Attacks:    3
Brute Force Attacks:       12
Impossible Travel:         8
Credential Stuffing:       1
Behavioral Anomalies:      47

HIGH-RISK ACCOUNTS
[CRITICAL] j.smith@corp.com     Score: 92
  - Impossible travel: Chicago -> Moscow (7,876 km in 0.5h)
  - Password spray target followed by successful login
  - New device and browser fingerprint
  - Off-hours access to SharePoint and email
  Action: Account suspended, SOC investigation initiated

[HIGH] m.johnson@corp.com       Score: 67
  - Login from new country (Brazil)
  - New source IP not matching VPN ranges
  - Access to HR application outside normal pattern
  Action: MFA re-enrollment required, manager notified

[MEDIUM] a.williams@corp.com    Score: 38
  - Weekend login at 03:00 UTC
  - New device (Linux, typically Windows user)
  Action: Step-up authentication applied

ATTACK CAMPAIGN DETAILS
Password Spray Campaign #1:
  Source:            185.220.101.x/24 (Tor exit node)
  Targeted Users:    247
  Success Rate:      0.8% (2 accounts compromised)
  Compromised:       j.smith@corp.com, r.davis@corp.com
  Duration:          45 minutes
  Pattern:           2 attempts per user, 3-second interval
```
