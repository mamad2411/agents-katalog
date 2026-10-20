---
name: bamboo-specs-security
description: >
  Atlassian Bamboo Specs (Java/YAML) security for owned build systems: least-privilege
  deployment projects, secret variables, repository-stored Specs review, injection in
  script tasks, and restricted admin permissions. Use when hardening Bamboo pipelines
  as code — not for attacking shared CI or exfiltrating plan credentials.
---

# Bamboo Specs Security

## Scope And Authorization

- **In scope:** Bamboo instances, projects, and Specs repos you administer.
- **Out of scope:** Modifying CI of orgs without authorization; dumping shared credentials.
- Specs can run as high-privilege build agents — treat plan-as-code like production code.
- Pair ADO environments with `azure-pipelines-environments` concepts; use `code-quality-standards`.

## When To Use

- Onboarding Bamboo Specs in Java or YAML stored in Bitbucket/Git.
- Reviewing script tasks for secret leakage or command injection from untrusted PR branches.
- Separating build vs deploy permissions and environments.
- Rotating shared credentials out of Specs source.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Azure DevOps Environments | `azure-pipelines-environments` |
| Generic secrets hygiene | `secrets-management-hygiene` |
| Bandit Python SAST | `bandit-python-scan` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Specs as code | Reviewed PRs; protected default branch |
| Secrets | Bamboo variables/secret variables — not hard-coded in Specs |
| Agents | Isolate prod deploy agents; no world-writable working dirs |
| Branches | Untrusted branches cannot publish prod plans without review |
| Permissions | Project admin ≠ every developer deploy prod |
| Tooling | Bamboo Specs scanner, REST, Bitbucket branch perms, Credential Manager |

## Workflow

### 1. Confirm scope and success criteria

1. Bamboo URL, projects, Specs repos, deploy environments, authorization.
2. Success: no secrets in git; prod deploy gated; Specs publish only from trusted path.
3. Break-glass admin accounts monitored.

### 2. Inventory Specs and credentials

```bash
# In Specs repo
rg -n "password|secret|token|api[_-]?key|BEGIN RSA" -i
rg -n "scriptTask|commandTask|inject|variable" -i
# Bamboo UI: Project variables, Deployment projects, Agents
```

1. List shared credentials linked to jobs.
2. Identify plans auto-updated from Specs on every commit vs gated.
3. Map who can administer Specs repositories.

### 3. Baseline risks

| Risk | Example |
| --- | --- |
| Secret in Specs | API token string in Java Specs |
| Untrusted PR | PR changes deploy job to exfil env |
| Overbroad agent | Same agent mounts prod kubeconfig |
| Injection | Script uses unquoted `${bamboo.inject.*}` from PR |

### 4. Harden Specs and Bamboo

1. **Secrets:** Move to Bamboo secret variables or external vault; reference by name only.
2. **Branch protection:** Only `main` publishes Specs to Bamboo; require PR reviews (CODEOWNERS security/platform).
3. **Split plans:** build plans vs deployment projects with environment permissions.
4. **Script hygiene:** quote variables; never `eval` user content; pin tool versions.
5. **Agents:** dedicated deploy agents with minimal network; no interactive login shared.
6. **Specs scanning:** enable Bamboo’s Specs security scanning / VCS repository checks where licensed.
7. **Java Specs:** avoid logging configuration objects that contain passwords.

**YAML Specs sketch (pattern):**

```yaml
# Do NOT put secrets here
variables:
  envName: prod
# Reference Bamboo-managed secret variables in tasks by name
```

### 5. Verify with evidence

1. `rg` clean of high-entropy secrets in Specs repo.
2. PR from feature branch cannot change prod deployment without review.
3. Build log redaction: secret variables masked.
4. Deploy to prod requires environment permission / approval gate.

### 6. Observe and harden

1. Audit Specs publish events and permission changes.
2. Rotate any secret that ever appeared in git history; consider history rewrite policy.
3. Periodic agent image rebuilds; patch bootstrap.

### 7. Hand off

1. Specs contribution guide (security section).
2. Credential ownership matrix.
3. Incident runbook for leaked plan variable.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Secrets | Secret variables / vault | Token in `bamboo-specs` commit |
| Review | Required reviewers on Specs | Direct push to Specs default branch |
| Deploy | Gated deployment project | Any plan can SSH to prod |
| Scripts | Fixed commands + allowlisted args | `sh -c "$USER_INPUT"` |
| Agents | Prod-isolated | Developer laptop agent for prod |

## Output Checklist

- [ ] Specs repos and publish path inventoried
- [ ] Secrets removed from VCS; stored as secret vars
- [ ] Branch protection + review enforced
- [ ] Build/deploy separation verified
- [ ] Script injection review done
- [ ] Agent isolation appropriate
- [ ] Logs mask secrets
- [ ] Audit of permission changes considered
- [ ] `code-quality-standards` applied to Specs code

## Rules

- Authorized Bamboo administration only.
- Treat Specs as production code.
- Never commit credentials.
- Untrusted branches are hostile input.
- Prefer least privilege on agents and deploy projects.
