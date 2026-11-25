---
name: engineer-doctor
description: Pre-flight health check for a CoDriDe setup — what's configured, what's missing, what needs attention
---

# Doctor

Run this before diving into the pipeline on a project you just adopted CoDriDe into, or periodically on one you've been using it on for a while. It doesn't fix anything by itself — it reports, so you can decide what to act on.

## Checks

Run all of these and collect the results before reporting — don't stop at the first failure.

### 1. `gh` CLI
- `gh --version` — installed?
- `gh auth status` — authenticated? Which account?
- `git remote get-url origin` — does a remote exist, and is it actually a `github.com` URL? (If it's GitLab/Bitbucket/none, most of this framework's product-track and issue-sync skills won't work — say so plainly rather than letting them fail deep in a skill later.)

### 2. Default branch
- `git remote show origin | sed -n '/HEAD branch/s/.*: //p'` (or `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`).
- Report it explicitly — this is what branch-level code review, documentation sync, test coverage, and master-docs checks compare branches against. If it isn't `main`, that's fine, just confirm it resolved correctly rather than silently assuming.

### 3. Test suite
- Look for the project's test configuration: a `test` script in `package.json`, `pytest.ini`/`pyproject.toml`'s `[tool.pytest]`, `jest.config.*`, `vitest.config.*`, or equivalent.
- If nothing is found, say so explicitly — `engineer-pr` assumes a test suite exists and can be run; if there isn't one, that assumption needs to be surfaced now, not discovered mid-PR.

### 4. Master docs status
- Does `docs/business-context/` exist? Does it have an `index.md`?
- Does `docs/technical-context/` exist? Which shape does it have — `project-briefing.md` (from `engineer-discover`), `index.md` (from `bootstrap-tech-docs`), neither, or (unusually) both?
- Does `docs/technical-context/adr/` (or `docs/adr/`, `adr/`) exist, and roughly how many ADRs are in it?

### 5. GitHub label taxonomy
- `gh label list` — check whether the labels this framework's skills reference by default exist: `status:backlog`, `status:todo`, `status:in-progress`, `status:in-review`, `priority:critical`, `priority:high`, `priority:medium`, `priority:low`, `bug`, `enhancement`, `improvement`, `research`. (`module:*` labels are created dynamically per module by the GitHub project sync skill, so there's nothing fixed to check there.)
- Missing labels aren't an error — every skill that uses them already says "adjust to what the repo uses" — but report which ones are missing so the human can decide whether to create them or keep redirecting skills to different names each time.

### 6. Monorepo shape
- Check for `workspaces` in `package.json`, `pnpm-workspace.yaml`, `nx.json`, `turbo.json`, `lerna.json`, `settings.gradle`(.kts) with multiple `include(...)` modules, or multiple independent manifests (`package.json`, `pyproject.toml`, `pubspec.yaml`, `build.gradle`(.kts), `Package.swift`, `go.mod`) under `apps/*/`/`packages/*/` — same broadened, non-JS-only signal list `/engineer:discover`'s own Phase 2.0 uses.
- If found, note it — `engineer-discover` handles monorepos by analyzing each workspace separately (whichever domains — backend, frontend, mobile — each one turns out to have); if `engineer-discover` was already run before the project became a monorepo (or vice versa), the briefing may be stale in a specific way worth flagging.

### 7. CoDriDe framework files
- `.agents/skills/` — does it exist? If `.claude/.generation-log.md` shipped with this copy (only present if it was copied from the CoDriDe repo directly rather than via a clean adopter checkout — adopters usually won't have it), compare the actual skill-directory count on disk against that log's most recent `codex` entry's manifest count, not a hardcoded number — precise and self-maintaining as the framework's own skill roster grows or shrinks, rather than drifting stale like a fixed count would. If the log isn't present, just confirm the directory exists and holds a non-trivial number of skills — don't guess an exact expected count with nothing to check it against. Any project-specific skills already added alongside the core ones?
- `.codex/work/` — any stale/abandoned work items sitting there from an interrupted session?

### 8. Project preferences
- Does `docs/PROJECT_PREFERENCES.md` exist (documentation language, extensible for more later)?
- Not blocking — report configured/not configured either way. `meta-preferences` sets this, so just point there if missing.

## Output

```markdown
# CoDriDe Doctor Report

## ✅ Working
- [Each check that passed, one line each]

## ⚠️ Missing (optional, but the pipeline is sharper with it)
- [Each gap that isn't blocking, with the one skill that fixes it]
- Project preferences (language): [configured / not configured — run `meta-preferences`]

## ❌ Blocking (these will break specific skills)
- [Each real problem, which skill(s) it breaks, and how to fix it]

## Summary
- Default branch: [detected]
- Test suite: [found / not found]
- Master docs: [business-context: yes/no, technical-context: shape or none]
- Monorepo: [yes, N services / no]
```

Don't fix anything automatically — this skill's only job is to tell the human what's true about their setup right now.
