---
name: verasic-github-governance
description: GitHub repo governance factory — soft hooks + CI bootstrap, plan-gated hard protection via OpenTofu. Use when creating GitHub repos, wiring branch governance, bootstrapping CI/hooks, applying branch protection, or preparing repo transfers for Verasic Labs / Milkywayrules.
disable-model-invocation: true
---

Security: see `references/scanner-notes.md` and upstream [SECURITY.md](https://github.com/Milkywayrules/verasic-skills/blob/main/SECURITY.md) for expected scanner signals and trust model.

# Verasic GitHub Governance — Factory + Soft Enforcement

## Workflows

**New repo factory path — bootstrap a repo once:**

1. Read `references/governance-protocol.md` (model, plan matrix, mutation routing) and `references/factory-protocol.md` (ordered checklist).
2. Create a **private** repo (default). Do not apply GitHub branch protection on Free private plans.
3. Prefer init orchestrator: `bash .cursor/skills/verasic-github-governance-init/scripts/factory.sh --yes`
4. Or manually: `bootstrap-repo.sh` → `wire-hooks.sh` → `lefthook install` → `doctor.sh`
5. Open first PR to prove CI merge + Actions. Required status check name: **`ci`**.
6. Verify: `bash .cursor/skills/verasic-github-governance/scripts/doctor.sh`

**Existing repo with CI:** bootstrap stops on foreign workflows (exit 2). Read `references/existing-repo-conflicts.md` and pass `--ci-strategy=skip|merge|replace`.

**Turborepo:** when `turbo.json` exists at repo root, bootstrap uses `ci-turborepo.yml` (bun + turbo + gate job **`ci`**).

**Hard protection path — when plan allows (Team/Pro/public Free):**

1. Confirm plan eligibility in `references/plan-matrix.md`.
2. Apply OpenTofu from a dogfood registry repo at `infra/github-governance/` ([public-free](https://github.com/Milkywayrules/verasic-github-governance-public-free) or [private-free](https://github.com/Milkywayrules/verasic-github-governance-private-free)) with `enable_hard_protection=true`.
3. Re-run `doctor.sh`; plan-gated items should report ready for hard apply.

**Mutation routing — any GitHub write (create repo, settings, protection, CI bootstrap, transfer prep):**

1. Load this skill and follow `references/governance-protocol.md` mutation routing.
2. Read-only `gh` (status, log, view) elsewhere is fine without this skill.

## Source of truth

| doc | role |
| --- | --- |
| `references/governance-protocol.md` | Governance model, plan matrix summary, mutation routing, enforcement layers |
| `references/factory-protocol.md` | Ordered new-repo bootstrap checklist |
| `references/existing-repo-conflicts.md` | CI conflict tiers and `--ci-strategy` |
| `references/plan-matrix.md` | Free private vs public vs Team — branch protection eligibility |
| `hooks/pre-push` | Block direct push to default branch (soft layer) |
| `hooks/pre-commit` | Lightweight reminder on default-branch commits |
| `scripts/bootstrap-repo.sh` | Copy CI/CONTRIBUTING/lefthook/AGENTS templates (idempotent) |
| `scripts/wire-hooks.sh` | Wire lefthook or `core.hooksPath` |
| `scripts/doctor.sh` | Soft-governance readiness (`0`) vs gaps (`2`) |
| Dogfood registry `infra/github-governance/` | OpenTofu scaffold for hard rules when plan allows — **not copied to product repos** |

The Cursor subagent (`.cursor/agents/verasic-github-governor.md`) is a thin pointer — never duplicate the spec elsewhere.

Registered in verasic-init manifest (wire-hooks + doctor). Install via `npx skills add Milkywayrules/verasic-skills` or bundle tag `@v0.2.4`.

## Hard rules

- Default: **private + Free** → no GitHub branch protection; enforce via hooks + CI culture + doctor.
- OpenTofu holds **intended** hard rules; apply branch protection only when `enable_hard_protection=true`.
- Required CI job name is **`ci`** — matches future required status checks.
- No signed commits in v1.
- Standard floor when hard protection is enabled: no direct push to default branch, PR + 1 review, required check `ci`, delete branch on merge.
- Never commit secrets or apply OpenTofu against production repos without explicit user approval.
