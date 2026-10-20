# Claude Code Instructions — VistA Evolved Platform

> **This file is a thin shim.** The canonical rules live in `/AGENTS.md`.
> If anything here conflicts with AGENTS.md, AGENTS.md wins.
> **Multi-root workspace:** `/AGENTS.md` means this repo's AGENTS.md, not a sibling repo's.
> The archive repo's AGENTS.md is reference material only — it does not govern this repo.

Read and follow `/AGENTS.md` in full before any task.

## RULE ZERO — Docker-first (mandatory)

**Before writing ANY code:** verify Docker is running and all containers are healthy.
Run `docker ps` and confirm `local-vista-utf8` and `ve-platform-db` are up.
If they are not running, start them FIRST. No exceptions. No deferrals.
See `.cursor/rules/01-docker-first-mandatory.mdc` for the full protocol.

## Key rules

1. Docker-first. Verify live runtime before ANY code changes. See Rule Zero above.
2. Terminal-first. No broad GUI feature work unless explicitly instructed.
3. Contract-first. APIs defined in OpenAPI/AsyncAPI before implementation.
4. No documentation sprawl. Only approved categories in `/docs`.
5. No claiming done without proof. Evidence goes in `/artifacts`.
6. Stop after each slice. Report what was done and wait for instruction.
7. Task responses must use the format defined in AGENTS.md section 5.

## Key references

- Source of truth: `docs/reference/source-of-truth-index.md`
- Doc governance: `docs/reference/doc-governance.md`
- Contract system: `docs/reference/contract-system.md`
- Decision index: `docs/reference/decision-index.yaml`
- AI governance: `docs/explanation/ai-coding-governance-and-sdlc.md`
