---
name: circleci-contexts-security
description: >
  Harden CircleCI Contexts: secret storage, project restrictions, security groups,
  OIDC vs long-lived keys, and least-privilege env vars. Use for org-owned CircleCI
  when reviewing who can attach contexts, rotating context secrets, or migrating
  project-level env vars into restricted contexts — not for attacking other orgs’ CI.
---

# CircleCI Contexts Security

## Scope And Authorization

- **In scope:** CircleCI organizations/projects you own or are authorized to administer.
- **Out of scope:** accessing another org’s contexts, dumping secrets from jobs you do not own, or bypassing SSO without approval.
- Prefer dry-run config validation and non-prod contexts before production secret rotation.
- Redact context secret values, API tokens, and OIDC audience details from tickets.
- Pair pipeline YAML changes with `code-quality-standards` and `secrets-management-hygiene`.

## When To Use

- Designing or reviewing **Contexts** (named secret bags attached via `context:` in workflows).
- Restricting which projects/security groups may use a context.
- Replacing stored AWS/GCP keys with **OIDC** (`circleci` identity provider).
- Audit: who can edit context env vars; leaked secrets in build logs.
- Tokens: circleci, context, security groups, restricted context, OIDC, project env vars.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic secrets program / vault design | `secrets-management-hygiene` |
| GitHub Actions OIDC / environments | platform GHA skill |
| Container image signing in pipeline | `container-image-signing` |
| Code quality of application code | `code-quality-standards` |
| CMD injection in scripts run by CI | `cmdi-command-injection` / `command-injection-defenses` |

## Domain Concepts

| Concept | Security impact |
| --- | --- |
| Context | Shared env vars/secrets injectable into jobs that list the context name |
| Project restriction | Limit context to allowlisted projects |
| Security groups | VCS/org groups that may use or administer a context |
| Project env vars | Often broader blast radius; prefer context + restriction |
| OIDC tokens | Short-lived cloud auth; prefer over static keys in contexts |
| API tokens | Personal/org tokens can read/write contexts — treat as root |

## Workflow

### 1. Confirm scope and success criteria

1. Org name, projects in scope, who is Context Admin, SSO/security group model.
2. Success: only intended projects/jobs receive secrets; unauthorized attach fails; rotation works without downtime.
3. Break-glass: documented path for emergency secret inject with dual control.

### 2. Inventory contexts and attachment surface

```bash
# CircleCI CLI / API (examples — use org-approved auth)
circleci context list <vcs-type> <org>
circleci context show <vcs-type> <org> <context-name>
# Search config for context usage
rg -n "context:" .circleci/
```

1. List each context: secret **names** (not values), restricted projects, security groups.
2. Find jobs using `context: [prod-deploy]` vs unrestricted project env vars.
3. Inventory long-lived cloud keys still stored as context secrets.

### 3. Baseline and risk

1. Map secrets by sensitivity (prod DB, cloud deploy, package publish).
2. Note any context usable by **all** projects (high risk for supply-chain PR abuse).
3. Check whether forks/PRs from external contributors can run privileged contexts (should not).

### 4. Apply hardening

**Config pattern (restricted context attach):**

```yaml
version: 2.1
workflows:
  deploy:
    jobs:
      - deploy-prod:
          context:
            - prod-aws-oidc
          filters:
            branches:
              only: main
```

**Hardening steps:**

1. Create separate contexts: `dev-*`, `stage-*`, `prod-*`; never share prod secrets with feature branches.
2. Enable **project restrictions** on prod contexts; allowlist deploy projects only.
3. Bind context use to **security groups** aligned with deployers, not all org members.
4. Migrate AWS/GCP/Azure to **OIDC** role assumption; delete static keys after dual validation.
5. Remove secrets from project env vars once context migration is verified.
6. Turn on secret masking; forbid `echo $SECRET` / debug dumps in orbs and scripts.
7. Restrict who can create/edit contexts (org admin policy + SSO).

### 5. Verify with evidence

```bash
# Unauthorized project: job requesting prod context should fail to start or lack secrets
# Authorized pipeline on main: assume role / deploy succeeds
# Confirm secret names present, values never printed:
circleci context show github my-org prod-aws-oidc
# Cloud side: only OIDC trust from CircleCI org/project claims
```

1. Open a PR from a fork or untrusted branch — must **not** receive prod context.
2. Rotate one non-prod secret end-to-end; confirm old value fails.
3. Grep pipelines/orbs for plaintext secret references and unpinned orbs.

### 6. Observe and harden

1. Audit context membership and restrictions quarterly.
2. Alert on context edits and new API tokens with context scope.
3. Prefer short-lived OIDC; set calendar for remaining static secrets.

### 7. Hand off

1. Document context → project matrix and owners.
2. Runbook: rotate context secret, revoke leaked token, disable compromised context.
3. Link to `secrets-management-hygiene` for org vault SSOT if contexts are not the only store.

## Context Threat Model

| Threat | Control |
| --- | --- |
| Malicious PR runs deploy job | Branch filters + restricted contexts + no context on untrusted PR jobs |
| Developer copies prod secret | Least privilege groups; no local echo; prefer OIDC |
| Stolen personal API token | Token inventory, SSO, short expiry, audit log |
| Shared “kitchen sink” context | Split by env and purpose |
| Orb supply chain | Pin orb versions; review orb source for secret exfil |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Attachment | Prod context only on protected branch jobs | Context on all workflows |
| Credentials | OIDC + role trust conditions | Long-lived AKIA keys in context |
| Scope | One purpose per context | Single mega-context for entire org |
| Verification | Failed attach from wrong project shown | “We think it’s restricted” |
| Logging | Secrets masked | Printing env in “debug” job |

## Output Checklist

- [ ] Org/projects/admins in scope recorded
- [ ] Full context inventory (names, restrictions, groups)
- [ ] Config references to contexts mapped
- [ ] Project restrictions + security groups applied for sensitive contexts
- [ ] OIDC migration plan or completed for cloud deploy keys
- [ ] Untrusted PR path cannot obtain prod secrets (tested)
- [ ] Rotation/break-glass runbook updated
- [ ] Residual static secrets have owners and expiry
- [ ] `code-quality-standards` applied to pipeline YAML changes

## Rules

- Authorized CircleCI orgs only.
- Never dump live secret values into chat, tickets, or skill notes.
- Prefer reversible restriction changes; validate deploy path before removing fallback keys.
- Keep this skill focused on CircleCI **contexts** security; broader vault and app secret design go to companion skills.
