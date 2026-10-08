---
name: repo-init-gate
description: "Use before repo-init-scan to cheaply decide whether a target repository already satisfies the current best-copilot init contract by reading only the root `best-copilot.md` sentinel."
---

# Repo Init Gate

Use this tiny skill before loading `repo-init-scan`. It is the repeat-request fast path.

## Immediate Execution Rule

When loaded, the next assistant action must be only this gate.

Preferred shell-capable path: run the bundled preflight helper from the target root when it is discoverable:

```bash
<best-copilot-skills-dir>/repo-init-gate/scripts/run-preflight.sh "$PWD" claude
```

For an installed Claude Code plugin, resolve the helper from `CLAUDE_SKILL_DIR` when present, or from the active plugin `skills/` directory. The helper reads only the target root `best-copilot.md` on the fast path. If the sentinel frontmatter version is not current, it immediately delegates to `repo-init-scan/scripts/bootstrap-after-gate-failure.sh`, which owns official init, manual fallback, artifact verification, and the final `## Init Summary`.

If the helper cannot be located or shell execution is unavailable, execute the inline gate exactly:

1. Read only the target root `best-copilot.md`, or determine that it is missing or unreadable.
2. Parse only its YAML frontmatter and compare `version` to the current contract version below.
3. Emit the `## Repo Init Gate` output block below.
4. If the frontmatter version is current, skip `repo-init-scan`; otherwise run `repo-init-scan` or its single-command bootstrap helper before any business-source read/search.

Forbidden before this block: search, grep, glob, source reads, project structure exploration, code intelligence, planning, dispatch, implementation summaries, scaffold writes, or reading `.github/instructions/**`, `memories/**`, `spec/**`, `AGENTS.md`, or `CLAUDE.md`.

## Contract

Canonical `best-copilot.md` content written by init:

```md
---
version: "0.8.0"
---
```

- Current YAML frontmatter `version: "0.8.0"`: `ready` + `skip_repo_init_scan`.
- Missing, unreadable, invalid frontmatter, missing version, or version mismatch: report the corresponding gate result and run `repo-init-scan`.
- Extra content after a current frontmatter block is not a reason to run scan on repeat requests. Writers should still keep the canonical three-line sentinel when creating or repairing the file.
- Explicit reinitialize/repair requests bypass this gate and run `repo-init-scan`.
- This gate is read-only; `repo-init-scan` owns sentinel creation/repair.
- If skill invocation fails, run the preflight helper when available. Otherwise do the same single-file read inline and report `HARNESS_DEGRADED skill_invocation_unavailable`.

## Output

```markdown
## Repo Init Gate
- gate_result: ready|needs_init|version_mismatch|invalid_sentinel
- next_action: skip_repo_init_scan|run_repo_init_scan
- evidence: target_root_best_copilot_md=present|missing|unreadable, observed_version=<version-or-none>
```
