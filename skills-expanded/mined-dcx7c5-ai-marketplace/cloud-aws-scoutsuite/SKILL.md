---
name: cloud-aws-scoutsuite
description: "-| | IAM | Root account MFA, password policy, unused credentials, overprivileged policies | | S3 | Public buckets, unencrypted buckets, versioning disabled, logging disabled | | EC2 | Security groups with 0."
domain: cybersecurity
---

-|
| IAM | Root account MFA, password policy, unused credentials, overprivileged policies |
| S3 | Public buckets, unencrypted buckets, versioning disabled, logging disabled |
| EC2 | Security groups with 0.0.0.0/0, unencrypted EBS volumes, public IPs |
| RDS | Public accessibility, unencrypted databases, backup retention |
| CloudTrail | Logging disabled, log file validation, multi-region disabled |
| Lambda | Public access, environment variable secrets, VPC configuration |

## Interpreting Findings

### Severity Levels

- **Danger (Red)**: Critical security issues requiring immediate remediation (e.g., S3 buckets with public write access)
- **Warning (Orange)**: Moderate risk findings that should be addressed (e.g., unused IAM access keys)
- **Good (Green)**: Security best practices that are properly configured

### Common High-Risk Findings

1. **IAM root account without MFA**: The AWS root account has no multi-factor authentication enabled
2. **S3 bucket policy allows public access**: Bucket policies with Principal set to "*"
3. **Security group allows unrestricted SSH**: Inbound rule allowing 0.0.0.0/0 on port 22
4. **CloudTrail not enabled in all regions**: Audit logging gaps allow unmonitored API activity
5. **RDS instance publicly accessible**: Database endpoints reachable from the internet

## Remediation Workflow

1. Run ScoutSuite scan to establish baseline
2. Export findings and prioritize by severity
3. Create remediation tickets for danger and warning findings
4. Implement fixes (update security groups, enable encryption, restrict access)
5. Re-run ScoutSuite to verify remediation
6. Schedule regular scans (weekly or after infrastructure changes)

## Integration with CI/CD

```bash
# Run ScoutSuite in CI/CD pipeline and fail on danger findings
scout aws --services s3 iam ec2 --no-browser --report-dir ./scout-report/

# Parse results programmatically
python -c "
import json
with open('./scout-report/scoutsuite-results/scoutsuite_results.json') as f:
    results = json.load(f)
    for service in results.get('services', {}):
        findings = results['services'][service].get('findings', {})
        for finding_id, finding in findings.items():
            if finding.get('flagged_items', 0) > 0 and finding.get('level') == 'danger':
                print(f'CRITICAL: {finding_id} - {finding.get(\"description\", \"\")}')
"
```

## Multi-Cloud Capability

ScoutSuite supports multiple cloud providers using the same framework:

```bash
# Azure
scout azure --cli

# GCP
scout gcp --user-account

# AWS with specific profile
scout aws --profile production
```

## References

- ScoutSuite GitHub Repository: https://github.com/nccgroup/ScoutSuite
- AWS Security Audit Checklist
- CIS AWS Foundations Benchmark
- AWS Well-Architected Security Pillar
