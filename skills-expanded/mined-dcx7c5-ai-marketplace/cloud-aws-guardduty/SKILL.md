---
name: cloud-aws-guardduty
description: "| | Backdoor | 5.0 - 8.0 | Backdoor:EC2/C&CActivity | | CryptoCurrency | 5."
domain: cybersecurity
---

|
| Backdoor | 5.0 - 8.0 | Backdoor:EC2/C&CActivity |
| CryptoCurrency | 5.0 - 8.0 | CryptoCurrency:EC2/BitcoinTool |
| Trojan | 5.0 - 8.0 | Trojan:EC2/BlackholeTraffic |
| UnauthorizedAccess | 5.0 - 8.0 | UnauthorizedAccess:IAMUser/ConsoleLogin |
| Recon | 2.0 - 5.0 | Recon:EC2/PortProbeUnprotected |
| Persistence | 5.0 - 8.0 | Persistence:IAMUser/AnomalousBehavior |

## Multi-Account Setup

```bash
# Designate GuardDuty administrator
aws guardduty enable-organization-admin-account \
  --admin-account-id 111111111111

# Auto-enable for new accounts
aws guardduty update-organization-configuration \
  --detector-id DETECTOR_ID \
  --auto-enable
```

## References

- AWS GuardDuty Best Practices: https://aws.github.io/aws-security-services-best-practices/guides/guardduty/
- EventBridge Integration: https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings_eventbridge.html
- GuardDuty Finding Types Reference
