---
name: certipy-adcs-lab
description: >
  Certipy against owned Active Directory Certificate Services labs: enumerate templates,
  find ESC1–ESC8 style misconfigs, request/auth with certificates, and remediate. Use
  when Certipy find, AD CS ESC vulns, template enrollment rights, or lab PKI abuse
  paths — only authorized labs/engagements, never unauthorized CA attacks.
---

# Certipy Adcs Lab

## Scope And Authorization

- **In scope:** AD CS environments you own, lab forests, or written-scope assessments.
- **Out of scope:** Attacking third-party CAs; production abuse without RoE; ransomware.
- Certificate abuse can yield Domain Admin — treat with change control and logging.
- Pair with `bloodhound-ce-basics` for graph context; Windows auth hardening skills.

## When To Use

- Lab practice of AD CS attack paths (ESC1, ESC2, ESC3, ESC4, ESC8, etc.).
- Authorized enumeration with Certipy `find`.
- Validating remediations on templates, enrollment rights, and HTTP endpoints.
- Purple-team detection engineering for cert requests.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| BloodHound graph general | `bloodhound-ce-basics` |
| Generic Windows privesc | `windows-privilege-escalation` |
| TLS web certs (public ACME) | cert-manager skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Piece | Role |
| --- | --- |
| Certipy | Offensive/defensive AD CS toolkit |
| Templates | Define EKU, subject supply, enrollment who |
| CA | Issues certs; ACL sensitive |
| ESC patterns | Community taxonomy of AD CS misconfigs |
| PKINIT / Schannel | Auth with certs to AD |

## Workflow

### 1. Confirm authorization and success criteria

1. Forest/domain, CA servers, allowed techniques, data handling.
2. Success: enumerated findings mapped to ESC IDs; proof in lab; remediations verified; detections noted.
3. Prefer lab snapshots before requests that alter state.

### 2. Enumerate with Certipy

```bash
# Examples — credentials/lab only
certipy find -u 'user@lab.local' -p '***' -dc-ip 10.0.0.10 -stdout
certipy find -u 'user@lab.local' -hashes 'aad3...:...' -dc-ip 10.0.0.10 -vulnerable -stdout
# JSON/text output for reports
certipy find -u 'user@lab.local' -p '***' -dc-ip 10.0.0.10 -output lab_adcs
```

1. Record CA names, templates, enrollment groups, flags (e.g. client auth EKU, enrollee supplies subject).
2. Cross-link principals with BloodHound for who can enroll.

### 3. Map common misconfig classes (defensive summary)

| Pattern (community) | Core issue | Remediation direction |
| --- | --- | --- |
| ESC1 | Enrollee supplies SAN + client auth + enroll rights | Disable subject supply; restrict enroll; manager approval |
| ESC2 | Over-permissive EKU / Any Purpose style issues | Fix template EKUs |
| ESC3 | Enrollment agent dangerous paths | Restrict agent templates |
| ESC4 | Template ACL write → reconfig | Fix template ACLs |
| ESC6 | EDITF_ATTRIBUTESUBJECTALTNAME2 on CA | Disable dangerous flags |
| ESC7 | CA ACL manage rights | Harden CA admin groups |
| ESC8 | AD CS HTTP enrollment NTLM relay | Disable HTTP / require EPA / relay defenses |

Use current Certipy/docs for exact flags — taxonomy evolves.

### 4. Controlled validation in lab

```bash
# Request certificate only in authorized lab
certipy req -u 'lowpriv@lab.local' -p '***' -ca 'LAB-CA' -template 'VulnerableTemplate' -dc-ip 10.0.0.10
# Authenticate with cert (lab)
certipy auth -pfx './user.pfx' -dc-ip 10.0.0.10
```

1. Minimal proof: obtain cert + TGT/auth as unintended principal **in lab**.
2. Do not export production DA certs offsite.
3. Clean up issued certs per RoE (revoke).

### 5. Remediate and re-test

1. Template: remove `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` where not required; least enroll groups; require manager approval for sensitive templates.
2. CA flags: review `EDITF_ATTRIBUTESUBJECTALTNAME2` and enrollment agent rights.
3. ACL: only PKI admins edit templates; no Domain Users write.
4. ESC8: prefer disable IIS enrollment if unused; enforce EPA; SMB signing/channel binding defenses per org standards.
5. Monitoring: event logs for unusual template requests, CA config changes.

```bash
certipy find ... -vulnerable  # should no longer flag fixed paths
```

### 6. Detection engineering notes

| Signal | Why |
| --- | --- |
| Sudden cert requests by low-priv users | ESC1-style abuse |
| Certificates with unexpected SAN UPN | Account impersonation |
| CA config changes | ESC6/7 prep |
| HTTP enrollment auth spikes | ESC8 attempts |

Ship detections to SIEM; test in purple team.

### 7. Hand off

1. Findings table: ESC ID, template/CA, principal, evidence, fix owner.
2. BloodHound edges if modeled.
3. Dispose lab PFX files securely.
4. Do not publish weaponized one-click against production defaults without context.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Lab/RoE only | Internet-wide CA scanning |
| Proof | Minimal lab auth | Mass cert issue in prod |
| Fix | Template ACL + flags | “Disable AD CS entirely” only answer |
| Creds | Lab accounts | Prod DA in chat |
| Docs | Map to ESC + evidence | Tool dump without interpretation |
| Detect | SIEM use cases | Enumerate and leave |

## Output Checklist

- [ ] Authorization recorded
- [ ] Certipy find output archived (safe storage)
- [ ] Vulnerable templates/CA flags identified
- [ ] Lab proof performed if allowed
- [ ] Remediations applied and re-enumerated
- [ ] Detections proposed/tested
- [ ] PFX/secrets disposed
- [ ] Report with ESC mapping delivered
- [ ] Cross-links to BloodHound as needed

## Rules

- Authorized AD CS assessment and labs only.
- Prefer remediation and detection over offensive glory.
- Handle certificates as credentials — protect PFX.
- Taxonomy names evolve; verify with current tooling output.
- General AD paths → `bloodhound-ce-basics`.
