---
description: Always keep the CHANGELOG updated with meaningful changes.
globs: *
---

# Auto-changelog (standard operating procedure)

At the **end of every task** or **significant modification** you complete, update [`CHANGELOG.md`](CHANGELOG.md) when appropriate. This is mandatory workflow — not optional and not subject to user confirmation.

## When to run

Perform this evaluation **before** proposing a final git commit message or concluding the task (including when the user did not ask for a commit).

## Decision gate

Ask: **Is this change relevant to the end-user, the system architecture, or another developer using this tool?**

| Answer | Action |
|--------|--------|
| **YES** | Update `CHANGELOG.md` under `## [Unreleased]` (see below). |
| **NO** | Do **not** modify `CHANGELOG.md`. |

### YES — document these

- New features, CLI/MCP/UI surfaces, env vars, or operator-visible behavior (also update [`.env.example`](.env.example) per [`.cursor/rules/07-env-example.mdc`](07-env-example.mdc))
- Bug fixes that affect runtime, data safety, or integrations
- Performance or reliability improvements users or operators would notice
- Security hardening (SSRF, auth, sandbox, secret handling, rate limits)
- Breaking or behavioral changes to public APIs, config, or graph semantics
- Architecture shifts that change how others extend or deploy the daemon (new modules, bootstrap paths, OpenSpec contracts)

### NO — skip the changelog

- Typos, formatting, comments-only edits
- Internal refactors with no observable behavior change
- Test-only changes (unless they document a newly fixed user-visible bug)
- Lockfile-only updates (`uv.lock`) unless paired with a dependency change worth calling out
- Release chores already captured by [`.cursor/rules/05-release-preparation.mdc`](05-release-preparation.mdc) (version bump, section rename) — do not duplicate bullets

## How to update (do this silently)

1. Open `CHANGELOG.md`.
2. Under `## [Unreleased]`, place **one concise bullet** in the correct subsection:
   - `### Added` — new capabilities
   - `### Changed` — behavior or API changes
   - `### Fixed` — bug fixes
   - `### Removed` — deprecations or removals
   - `### Security` — security-only changes (create this heading under `[Unreleased]` if missing)
3. **Create the subsection** if it does not exist yet under `[Unreleased]`.
4. Match existing style: **bold lead** — short explanation; optional `` `path` `` or env var; link OpenSpec/docs when relevant.
5. **Do not** duplicate an existing bullet; **merge** into one bullet if the same area was touched again in the same task.
6. **Do not** ask permission to edit the changelog — just do it.

## Examples

**YES:** New `prepare_matryca_runtime()` called from daemon and MCP → `### Added` bullet on runtime bootstrap.

**YES:** OCC fix preventing silent overwrites → `### Fixed`.

**NO:** Rename a private helper in one file with no call-site behavior change.

**NO:** Add `test_foo.py` for existing behavior.

## Coordination

- Release cutting (move `[Unreleased]` → `[X.Y.Z]`) is handled by [`05-release-preparation.mdc`](05-release-preparation.mdc) when the user requests a release.
- GitHub Release text is extracted from this file via [`scripts/extract_changelog.py`](scripts/extract_changelog.py) — bullets here become public release notes.

## Task completion

If you updated the changelog, include `CHANGELOG.md` in the set of files touched when summarizing the task. Do not treat the changelog edit as a separate “ask” step.
