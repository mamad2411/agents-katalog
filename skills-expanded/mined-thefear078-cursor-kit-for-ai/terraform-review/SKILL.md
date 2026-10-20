---
name: terraform-review
description: MUST USE for Terraform/OpenTofu PR review — plan analysis, state safety, IAM blast radius, module pins, drift, secrets in tfvars. Triggers on infra changes, state lock errors, or destructive plan surprises.
---

# Terraform Review

Infrastructure code merges are **production changes**. Review plans for destroy/replace, IAM expansion, and state coupling before apply — severity-first, with explicit rollback notes.

## When This Skill Applies

- `.tf` / `.tfvars` PRs
- `terraform plan` shows unexpected `-/+` or `destroy`
- State lock, backend migration, workspace split
- New module version or provider major bump
- Multi-account/network peering changes

## Severity Model

| Level | Signal | Gate |
|-------|--------|------|
| **T0** | `force_destroy` on data store; 0.0.0.0/0 admin; state with secrets in git; open S3 bucket | Block |
| **T1** | Replace on stateful resource; broad IAM `*`; no plan in CI | Fix pre-merge |
| **T2** | Missing tags, no lifecycle ignore where needed | Same train |
| **T3** | Style/docs | Optional |

Cross-ref: `cost-optimize` for instance SKUs; `k8s-review` for cluster modules; `secrets-audit` for keys in tfvars.

## Phase 0 — Plan Hygiene

```bash
terraform fmt -check -recursive
terraform validate
tflint
terraform plan -out=plan.bin
terraform show -json plan.bin | jq '.resource_changes[] | select(.change.actions[]?=="delete") | .address'
```

Capture: resources to **create**, **update**, **destroy**, **replace** (note `-/+`).

## Phase 1 — Destructive Change Audit

For each destroy/replace:

- [ ] Data loss risk? Backup snapshot exists (`backup-restore`)
- [ ] Downtime window acceptable?
- [ ] `create_before_destroy` where zero-downtime needed
- [ ] `prevent_destroy` lifecycle on critical buckets/DBs

Question every **resource address rename** — Terraform treats as delete+create.

## Phase 2 — IAM & Network

- [ ] Least privilege — no `Action: "*"` on `Resource: "*"` for workloads
- [ ] Trust policies scoped to OIDC role ARN / specific SA
- [ ] Security groups: minimal ingress; no admin SSH from 0.0.0.0/0
- [ ] Private subnets for databases; public only for LB

```bash
# Example: find wide policies in repo
rg -n '0\.0\.0\.0/0|"Action":\s*"\*"' --glob '*.tf'
```

## Phase 3 — State & Modules (2025–2026)

- [ ] Remote backend encrypted (S3+Dynamo lock, Terraform Cloud, GCS)
- [ ] State **not** in git; no secrets in state outputs logged in CI
- [ ] Module sources pinned: registry version or git ref SHA — not `main` float
- [ ] Provider versions locked in `.terraform.lock.hcl` committed
- [ ] Workspaces or directory split per env — no single state for dev+prod
- [ ] OpenTofu vs HashiCorp noted if org standardized

## Phase 4 — Operability

- [ ] Outputs documented for downstream systems
- [ ] Tags: env, service, owner, cost center
- [ ] Drift detection scheduled (Terraform Cloud, cron plan)
- [ ] Import/migration steps in PR description if moving existing infra

## Phase 5 — CI Integration

- Plan on PR; apply on merge to main with approval
- Policy as code: OPA/Sentinel/Checkov/tfsec in pipeline
- Cost estimate: Infracost comment on PR (`cost-optimize`)

Cross-ref: `ci-fix` when plan job fails.

## Output Template

```markdown
## Terraform Review: [stack/module]

**Plan summary:** +N ~M -K replace R | **Verdict:** ✅ / 🔶 / ❌

### Destructive / replace (must acknowledge)
| Address | Action | Risk | Mitigation |

### IAM / exposure
| Finding | Sev | Fix |

### Module/provider pins
| Module | Current | Recommendation |

### Apply checklist
- [ ] backup/snapshot
- [ ] maintenance window
- [ ] rollback: previous state version ID

### Follow-ups
- [ ] `cost-optimize` — SKU changes
```

## Anti-Patterns

- **Manual console edits** — drift until next apply surprise
- **Local apply only** — no PR plan artifact
- **One mega-module** — untestable blast radius
- **Sensitive in plain tfvars** in git — use env-specific secret store
- **Ignoring replace** on RDS instance class — downtime

## Cross-References

| Skill | Use when |
|-------|----------|
| `backup-restore` | Before DB replace |
| `docker-audit` | ECR lifecycle |
| `monitoring-check` | New alert modules |

## Cursor Kit Templates

- `vps-setup`, `kubernetes` — reference Terraform layouts

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

