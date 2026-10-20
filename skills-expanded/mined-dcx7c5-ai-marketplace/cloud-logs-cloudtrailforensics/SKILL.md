---
name: cloud-logs-cloudtrailforensics
description: "Cloud Logs Cloudtrailforensics."
domain: cybersecurity
---

|
| boto3 CloudTrail client | Programmatic CloudTrail event lookup |
| AWS Athena | SQL-based analysis of CloudTrail S3 logs |
| AWS CLI | Command-line CloudTrail queries |
| jq | JSON processing for CloudTrail event parsing |
| CloudTrail Lake | Advanced event data store with SQL query support |

## Output Format

```
Forensic Report: AWS-IR-[DATE]-[SEQ]
Account: [AWS Account ID]
Timeframe: [Start] to [End]
Compromised Credentials: [Access Key IDs]
Suspicious Events: [Count]
Source IPs: [List of attacker IPs]
Actions Taken: [API calls by attacker]
Data Accessed: [S3 objects, secrets, etc.]
Persistence Mechanisms: [New users, keys, roles]
```
