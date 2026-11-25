---
name: aws-iam-roles-anywhere
description: >
  AWS IAM Roles Anywhere for owned hybrid access: trust anchors (CAs), profiles,
  role trust policies, certificate session policies, CRL/revocation, and least-privilege
  on-prem workloads. Use when exchanging X.509 certs for temporary AWS credentials —
  not for forging certificates or accessing accounts without authorization.
---

# AWS IAM Roles Anywhere

## Scope And Authorization

- **In scope:** Roles Anywhere trust anchors, profiles, and roles in accounts you own; certificates from your PKI.
- **Out of scope:** Using stolen/forged certs against foreign AWS accounts; weakening CA controls.
- Certificate private keys are equivalent to long-lived cloud credentials — protect HSMs/filesystems.
- Prefer short session durations and tight profiles.
- Pair with `aws-iam-least-privilege` and org PKI practices; `code-quality-standards` for credential helpers.

## When To Use

- On-prem/hybrid servers needing AWS API access without static IAM keys.
- Mapping certificate attributes (OU/CN) to role session tags.
- Setting up trust anchors with ACM PCA or your own CA certificates.
- Rotating/revoking compromised host certificates via CRL.
- Migrating off embedded AKIA keys on servers.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| EKS pod AWS identity | `aws-eks-pod-identity` |
| Standard IAM least privilege | `aws-iam-least-privilege` |
| Human SSO access | IAM Identity Center skills |
| Secrets Manager for apps already in AWS | secrets skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Object | Role |
| --- | --- |
| Trust anchor | Establishes CA(s) AWS trusts for client certs |
| Profile | Links roles + optional session policies + duration |
| Role | IAM role assumed via Roles Anywhere |
| Credential helper | `aws_signing_helper` obtains temporary creds |
| CRL | Revocation list for compromised certs |

## Trust Flow

```text
Host X.509 cert (private key local)
  → CreateSession / credential helper
  → Roles Anywhere validates cert against trust anchor + CRL
  → STS temporary credentials for profile role
  → AWS API calls
```

## Workflow

### 1. Confirm scope and success criteria

1. Record accounts, CA type (ACM PCA / external), host inventory, required AWS APIs.
2. Success: hosts obtain temp creds; wrong CA/cert denied; revoked cert fails; no static keys remain.
3. Define cert lifetime and rotation automation.

### 2. Inventory

```bash
aws rolesanywhere list-trust-anchors
aws rolesanywhere list-profiles
aws rolesanywhere list-crls
aws iam list-roles --query "Roles[?contains(RoleName, 'Anywhere') || contains(AssumeRolePolicyDocument, 'rolesanywhere')]"
```

1. Find servers still using access keys (IAM credential report).
2. Confirm CA issuance policies (who can mint client certs).

### 3. Baseline

1. Export trust anchor and profile JSON.
2. Sample successful CreateSession (lab) and CloudTrail events.
3. Document mapping CN/OU → environment/app.

### 4. Configure securely

**Trust anchor:** import CA cert chain; enable CRL if provided.

**Role trust policy (sketch):**

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "rolesanywhere.amazonaws.com" },
    "Action": ["sts:AssumeRole", "sts:TagSession", "sts:SetSourceIdentity"],
    "Condition": {
      "ArnEquals": {
        "aws:SourceArn": "arn:aws:rolesanywhere:REGION:ACCT:trust-anchor/TA_ID"
      }
    }
  }]
}
```

**Profile:** attach role ARNs; set `durationSeconds` low enough; optional intermediate session policy restricting actions further.

**Attribute mapping:** map certificate OU to `aws:PrincipalTag` for ABAC policies on data resources.

**Host setup**

```bash
# Example credential helper usage (paths vary)
./aws_signing_helper credential-process \
  --certificate /etc/pki/host.crt \
  --private-key /etc/pki/host.key \
  --trust-anchor-arn "$TA_ARN" \
  --profile-arn "$PROFILE_ARN" \
  --role-arn "$ROLE_ARN"
```

Configure `~/.aws/config` `credential_process` for the system user.

**Hardening**

1. Private keys: root-only, preferably HSM/TPM.
2. Separate roles per app tier; do not share one role for all datacenter hosts.
3. Network: restrict which hosts receive client certs via CA profiles.
4. Delete AKIA keys after cutover verification.

### 5. Verify with evidence

```bash
aws sts get-caller-identity   # via credential_process profile
# Expect assumed-role via rolesanywhere
# Revoke cert, publish CRL, expect failure after cache expiry
```

1. Wrong trust anchor / expired cert → denied.
2. Role policy denies unauthorized S3; allows intended.
3. CloudTrail shows Roles Anywhere sessions with source identity/tags.

### 6. Observe and harden

1. Monitor failed CreateSession spikes (theft attempts or expiry).
2. Alert on trust anchor/profile modifications.
3. Rotate CA and host certs before expiry; test CRL path annually.

### 7. Hand off

1. PKI + Roles Anywhere RACI.
2. Host bootstrap script/docs.
3. Break-glass for CA outage (limited static? prefer secondary CA).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Keys | short-lived sessions from certs | static AKIA on disk |
| Roles | per-app least privilege | one mega role for all hosts |
| PKI | controlled CA + CRL | anyone can mint trusted client certs |
| Duration | short sessions | max duration always |
| Mapping | ABAC from cert attributes | ignore attributes; same perms |
| Audit | CloudTrail + tags | no source identity |

## Output Checklist

- [ ] CA/trust anchors/profiles/roles recorded
- [ ] Trust policies conditioned on trust anchor
- [ ] Session duration and session policies set
- [ ] Host credential_process working
- [ ] Revocation/CRL tested
- [ ] Static keys removed post-migration
- [ ] ABAC/attribute mapping reviewed
- [ ] Monitoring on config and failures
- [ ] `aws-iam-least-privilege` applied to roles

## Rules

- Owned PKI and accounts only.
- Protect private keys like production credentials.
- Prefer short sessions and narrow roles.
- Always test revocation before relying on it in IR.
- Focus on Roles Anywhere; human SSO and in-AWS workload identity elsewhere.
