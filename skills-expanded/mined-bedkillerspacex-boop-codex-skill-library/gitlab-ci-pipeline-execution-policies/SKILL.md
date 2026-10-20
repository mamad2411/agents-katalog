---
name: gitlab-ci-pipeline-execution-policies
description: >
  GitLab pipeline execution policies / compliance pipelines: enforce org-required
  CI jobs (SAST, license, approvals hooks) via policies so projects cannot opt out.
  Use for GitLab Ultimate/org policy features on owned instances — not to disrupt
  third-party GitLab.com namespaces without authority.
---

# GitLab CI Pipeline Execution Policies

## Scope And Authorization

- **In scope:** GitLab groups/instances you administer (often Ultimate features).
- **Out of scope:** Applying policies to groups outside your authority; using policies
  as a supply-chain attack to inject malicious jobs into others’ projects.
- Policies can break all pipelines if misconfigured — pilot on a subgroup first.
- Treat policy YAML as security-critical code under review.
- Pair with `gitlab-ci-security-basics` for project-level hardening.

## When To Use

- Mandating security scanners on every project pipeline.
- Enforcing required stages/jobs without relying on each team to copy YAML.
- Centralizing compliance evidence collection.
- Preventing projects from disabling secret detection / dependency scanning.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Project `.gitlab-ci.yml` hygiene | `gitlab-ci-security-basics` |
| OIDC cloud deploy | `gitlab-ci-oidc-cloud` |
| GitHub org required workflows | GitHub ruleset/required workflow features |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| Pipeline execution policy | Group-level policy injecting/enforcing CI configuration |
| Compliance framework | Labels projects; bind policies to frameworks |
| Scan execution policy | Related: schedule/force security scans (feature set varies) |
| Inject / override strategies | How policy merges with project CI |
| Enforcement | Projects cannot skip required jobs |

**Note:** Feature names and YAML schemas differ by GitLab version (self-managed vs GitLab.com).
Confirm against your version’s docs before apply. This skill captures the operational pattern.

## Workflow

### 1. Confirm edition and scope

1. Verify GitLab tier supports pipeline execution / security policies.
2. Record group path, pilot projects, policy owners, authorization.
3. Success: every pilot pipeline runs required job; attempt to remove it fails.

### 2. Inventory current CI

```bash
# List projects under group (API)
# curl --header "PRIVATE-TOKEN: $TOKEN" \
#   "https://gitlab.example/api/v4/groups/GROUP/projects?include_subgroups=true"
```

Sample existing `.gitlab-ci.yml` patterns; note custom stages that might conflict.

### 3. Design required controls

| Control | Job examples |
| --- | --- |
| Secret detection | `secret_detection` |
| SAST / dependency scanning | GitLab templates or third-party |
| License scanning | Policy-driven |
| Build provenance | Custom job |
| Block on critical | `allow_failure: false` |

Define fail vs warn (`allow_failure`) per severity with security leadership.

### 4. Author policy (illustrative)

```yaml
# Conceptual structure — replace with current GitLab policy schema
type: pipeline_execution_policy
name: org-required-scanners
description: Enforce secret detection and SAST
enabled: true
pipeline_config_strategy: inject_ci   # or override per docs
content:
  include:
    - template: Jobs/Secret-Detection.gitlab-ci.yml
    - template: Jobs/SAST.gitlab-ci.yml
```

Store policy in management project with CODEOWNERS-equivalent approvals.

### 5. Bind to group / compliance framework

1. Create compliance framework label (e.g. `production`).
2. Apply framework to projects that must comply.
3. Link execution policy to framework or entire group (prefer framework for gradual rollout).
4. Pilot 1–2 projects → expand.

### 6. Merge behavior and stages

- Ensure project stages include names required by templates or use `stage: .pre` / reserved stages per docs.
- Resolve job name collisions (`script` override conflicts).
- Document how teams add jobs without disabling policy jobs.

### 7. Verify

| Test | Expect |
| --- | --- |
| Pipeline on pilot | Required jobs present in graph |
| Project deletes local SAST | Policy still injects job |
| Critical finding | Pipeline fails if configured |
| Non-framework project | Unaffected during pilot |

```text
# In pipeline UI: confirm "jobs from policy" indicators if shown by version
```

### 8. Operate

- Version policies; changelog for breaking scanner upgrades.
- Monitor pipeline failure rates after enforce.
- Exception process: time-boxed framework removal with ticket.
- Audit who can edit security policies (break-glass).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | Subgroup pilot | Instant org-wide break |
| Exceptions | Ticket + expiry | Permanent silent skip |
| Jobs | `allow_failure` intentional | All scanners warn forever |
| Ownership | Security + platform co-own | Random project maintainer edits policy |
| Schema | Match GitLab version docs | Copy blog YAML for wrong major |

## Output Checklist

- [ ] Tier/feature availability confirmed
- [ ] Pilot group and success criteria set
- [ ] Required controls agreed with security
- [ ] Policy authored under review
- [ ] Framework binding applied to pilot
- [ ] Pipelines show enforced jobs
- [ ] Failure thresholds tuned
- [ ] Exception process documented
- [ ] Expansion plan for remaining projects
- [ ] `code-quality-standards` applied to custom policy jobs

## Rules

- Only on groups you administer.
- Pilot before broad enforce.
- Policies are code — review and restrict editors.
- Exceptions expire.
- Confirm schema against **your** GitLab version; do not invent unsupported fields in production without docs.
