---
name: enterprise-discover
description: Use when starting enterprise work in a new repo, new worktree, unfamiliar package, or new computer, or whenever commands, paths, conventions, portability, or project traps are not yet known
---

# Enterprise Discover
## Global Precheck

Before reading further, writing artifacts, delegating, or changing files, run:

```bash
enterprise-precheck --skill enterprise-discover
```

If it exits non-zero, stop and report stderr verbatim. Do not hand-craft packet files or evidence markers to bypass it.


Profile the repository before the rest of the enterprise workflow starts guessing, then generate the repo-local overlay skills that travel with the repo.

## Required Approach

1. Start with an indexed repo lookup if available.
   - if `cortex-engine` or an equivalent repo index exists, use it first
   - if not available, state that and fall back to direct filesystem search
2. Build committed `.codex/enterprise-state/repo-profile.json`.
3. Build committed `.codex/enterprise-state/repo-traps.json`.
4. Build committed `.codex/enterprise-state/repo-best-practices.json` if current primary-source guidance is needed and available.
5. Build gitignored `.codex/enterprise-state/local-machine.json` for this computer only.
6. Ensure gitignored `.codex/enterprise-state/agent-sessions/` is the only home for in-flight agent workflow state.
7. Start or refresh the current agent session with `python3 tools/enterprise-skills/enterprise/scripts/agent_session.py ensure ...`, then record discover in that session.
8. Generate or refresh `.codex/repo-skills/<repo-family>-enterprise*` using `scripts/generate_repo_overlay.py`.
9. Validate overlay freshness with `scripts/validate_overlay_manifest.py`; the manifest must include generator version, generated timestamp, source hashes, and generated skill hashes.
10. Stage and commit the portable setup artifacts with `scripts/commit_portable_state.py`.
11. State unknowns instead of guessing.

## Minimum Outputs

- repo slug and display name
- workspace layout and relative source roots
- test, build, and lint commands when verified
- migration locations if relevant
- auth, tenancy, and high-risk domain conventions
- dominant file conventions
- known structural traps
- source-of-truth docs for risky domains
- generated repo-local overlay family name
- overlay manifest hash proof: generator version, generated timestamp, repo-profile/trap/best-practice hashes, generic source hashes, and generated skill hashes
- commit sha for the portable setup commit

## Portability Rules

- committed profiles must use relative paths and portable command names only
- do not commit usernames, absolute paths, secrets, local interpreter wrappers, or machine-specific install locations
- keep machine-only facts in `local-machine.json`
- keep live agent workflow state in gitignored `agent-sessions/`
- setup is not complete until the portable repo artifacts are committed
- if a command cannot be verified, mark it unknown instead of inventing one

## Codex Rules

- Use `multi_tool_use.parallel` for independent reads.
- If web research is needed, prefer official documentation and current primary sources.
- Refresh the repo-local overlay whenever the committed profile materially changes.
- Treat a stale or missing overlay manifest hash as a fail-closed discover gap.
- Commit only the portable setup artifacts by default:
  - `.codex/enterprise-state/repo-profile.json`
  - `.codex/enterprise-state/repo-traps.json`
  - `.codex/enterprise-state/repo-best-practices.json` when present
  - `.codex/repo-skills/`
- If discover also updated another portable setup file such as `.gitignore`, include it explicitly with `scripts/commit_portable_state.py --extra-path .gitignore`.
- Never commit `.codex/enterprise-state/local-machine.json` or `.codex/enterprise-state/agent-sessions/`.

## References

- Use [profile-schema.md](references/profile-schema.md) for the committed repo profile shape.
- Use [machine-state-schema.md](references/machine-state-schema.md) for machine-only state.
- Use [repo-overlay-layout.md](references/repo-overlay-layout.md) for generated skill naming and paths.
- Use [agent-session-model.md](../enterprise/references/agent-session-model.md) for agent-bound workflow state.
- Use `scripts/validate_overlay_manifest.py` after generation and before relying on repo-local overlays.
