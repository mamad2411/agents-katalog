# VistA Evolved Platform — Copilot Instructions

## Root law

Read `/AGENTS.md` before any task. It is the canonical cross-tool governance file.

> **Multi-root workspace:** `/AGENTS.md` means this repo's AGENTS.md, not a sibling repo's.
> The archive repo's AGENTS.md is reference material only — it does not govern this repo.

## RULE ZERO — Docker-first verification (MANDATORY)

**Before writing ANY code:** run `docker ps` and verify `local-vista-utf8` and `ve-platform-db` are healthy.
If not running, start them. If Docker Desktop is not running, start it and wait.
Code that was never tested against live Docker is NOT done. No exceptions.
See `.cursor/rules/01-docker-first-mandatory.mdc` for the full startup and verification protocol.

## Key rules

1. **Docker-first.** Verify live runtime before ANY code changes. See Rule Zero above.
2. **Terminal-first.** VistA Evolved starts from VistA truth, not broad GUI surfaces.
3. **Contract-first.** HTTP APIs in OpenAPI (`packages/contracts/openapi/`), events in AsyncAPI, config in JSON Schema. Use generated SDKs.
4. **No documentation sprawl.** Only: tutorials, how-to, reference, explanation, adrs, runbooks under `/docs`. Evidence in `/artifacts`.
5. **No silent mocks.** Return explicit `integration-pending` when infrastructure is unavailable.
6. **One slice at a time.** Verify each slice before starting the next.
7. **Proof required.** Every task must report: files changed, commands run, outputs, pass/fail.
8. **ADRs are enterprise-namespaced.** `VE-PLAT-ADR-NNNN` for this repo. Register in `docs/reference/decision-index.yaml`.

## Key references

| What | Where |
|------|-------|
| Source of truth index | `docs/reference/source-of-truth-index.md` |
| Doc governance | `docs/reference/doc-governance.md` |
| Contract system | `docs/reference/contract-system.md` |
| Decision index | `docs/reference/decision-index.yaml` |
| Boundary policy | `docs/reference/boundary-policy.md` |
| Persistence policy | `docs/reference/persistence-policy.md` |

## Task response format

Every task must end with: Objective, Files inspected, Files changed, Commands run, Results, Verified truth, Unverified areas, Risks, Next step.
