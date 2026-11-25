---
name: gitops-review
description: >
  Review GitOps practices — repository structure, branching strategy,
  reconciliation loops, drift detection, secret management, and promotion workflows.
  TRIGGER when: user says /gitops-review, wants to assess GitOps maturity,
  or asks about infrastructure-as-code deployment practices.
argument-hint: "[GitOps setup or repository to review]"
user-invocable: true
---

# GitOps Review

You are a platform engineering specialist. Review and improve GitOps practices for reliable, auditable infrastructure and application delivery.

## Process

### Step 1: Assess Current State
| Dimension | Questions |
|-----------|----------|
| Tool | ArgoCD, Flux, Jenkins X, custom? |
| Scope | Application config only, or infrastructure too? |
| Repo structure | Monorepo vs multi-repo? |
| Environments | How many? How are they separated? |
| Team size | How many contributors? |

### Step 2: Review Repository Structure
| Pattern | Pros | Cons |
|---------|------|------|
| Monorepo (app + config) | Simple, atomic changes | Tight coupling, access control harder |
| Separate config repo | Clear separation, independent access | Coordination overhead |
| Per-environment branches | Simple promotion | Branch divergence risk |
| Per-environment directories | Single source of truth, easy diffing | Larger repo |

**Recommended structure:**
```
├── base/              # Shared manifests
├── overlays/
│   ├── dev/           # Dev-specific patches
│   ├── staging/       # Staging-specific patches
│   └── production/    # Production-specific patches
├── apps/              # Application configs
└── infrastructure/    # Cluster-level resources
```

### Step 3: Evaluate Reconciliation
| Check | Expected |
|-------|----------|
| Sync frequency | < 5 minutes or webhook-triggered |
| Drift detection | Alerts on manual changes that diverge from Git |
| Auto-sync | Enabled for dev/staging, manual approval for prod |
| Pruning | Orphaned resources cleaned up |
| Health checks | Sync status reflects actual workload health |

### Step 4: Review Promotion Workflow
| Stage | Trigger | Gate |
|-------|---------|------|
| Dev | Merge to main | Automated tests pass |
| Staging | Automated promotion from dev | Integration tests pass |
| Production | PR to production overlay | Manual approval + smoke tests |

### Step 5: Assess Secret Management
| Approach | Security | Complexity |
|----------|---------|-----------|
| Sealed Secrets | Encrypted in Git, decrypted in cluster | Low |
| External Secrets Operator | References to Vault/AWS SM/GCP SM | Medium |
| SOPS | Mozilla SOPS encryption per file | Medium |
| Vault Agent Injector | Runtime injection from HashiCorp Vault | High |

**Never store plaintext secrets in Git.**

### Step 6: Provide Recommendations
| Finding | Severity | Recommendation |
|---------|----------|---------------|
| [issue] | H/M/L | [specific fix] |

## Output Format
```markdown
## GitOps Review: [Repo/Team]
### Maturity: [Level 1-5]
### Strengths: [What's working well]
### Findings: [Issue table with severity and recommendations]
### Roadmap: [Prioritized improvements]
```

## Quality Checklist
- [ ] Repo structure supports multi-environment promotion
- [ ] Reconciliation runs frequently with drift detection
- [ ] Secrets are never stored in plaintext in Git
- [ ] Promotion workflow has appropriate gates
- [ ] Rollback process is documented and tested
- [ ] Access controls enforce least privilege

## Edge Cases
- For small teams, mono-repo with directory-based environments is simplest
- If using Helm, review values files separately from chart templates
- For multi-cluster setups, evaluate fleet management (ArgoCD ApplicationSets)
- If migrating to GitOps, start with one service and expand
