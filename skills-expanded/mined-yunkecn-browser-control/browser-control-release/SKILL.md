---
name: browser-control-release
description: Use when releasing this browser-control repository: review documentation/code alignment, update docs or code as needed, bump every version source, rebuild, run validation, commit, tag, push, and open a GitHub PR/MR. Trigger on requests like "release browser-control", "修改版本号并发布", "构建测试提交打 tag 推 PR", or "prepare a Browser Control release".
---

# Browser Control Release

Run the Browser Control release workflow end-to-end unless blocked. Be outcome-first and report exact validation evidence in Chinese.

## Inputs

- Target version: use the user-provided SemVer version, for example `1.2.1`. If absent, infer a SemVer bump from pending changes and state the inference before editing.
- Base branch: default to `main` unless the user provides another base.
- PR mode: default to ready-for-review; use draft only if the user asks for draft.

## Guardrails

- Do not push or tag if build, typecheck, lint, or tests fail.
- Do not overwrite an existing tag. If `v<version>` exists locally or remotely, stop and ask for direction.
- Do not commit `.omx/plans/**`, transient `.omx/state/**`, local logs, or unrelated files unless explicitly requested.
- If the current branch is `main`, create or ask for a release/feature branch before committing.
- Before account-affecting browser actions such as submitting a GitHub PR through the web UI, confirm unless the user already explicitly asked to create the PR/MR.
- Prefer repository commands from `AGENTS.md` and `package.json`.

## Workflow

### 1. Inspect repository state

Run and summarize:

```bash
git status --short --branch
git remote -v
git log --oneline --decorate -5
```

Identify current branch, upstream, base branch, pending changes, and any existing PR if cheaply checkable.

### 2. Review docs and code alignment

Review changed code and public/agent-facing docs for drift. Inspect relevant diffs and these files when affected:

- `README.md`, `README.zh-CN.md`
- `AGENTS.md`
- `skills/browser-control/SKILL.md`
- `skills/browser-control/references/api.md`
- `skills/browser-control/references/recipes.md`
- `skills/browser-control/references/troubleshooting.md`
- `docs/testing.md`, `docs/maintainer-architecture.md`
- `contracts.ts`
- `src/extension/**`
- `skills/browser-control/extension/**`
- `skills/browser-control/scripts/**`
- `tests/**`

Check that:

- command names, arguments, response fields, diagnostics, capabilities, and errors match code/tests;
- generated extension output is expected and not stale;
- agent-facing docs describe behavior and usage, not unnecessary implementation detail;
- maintainer docs contain deeper implementation/testing notes only when useful;
- tests cover newly documented behavior.

If docs and code disagree, update the smaller wrong surface. If behavior changed but docs are silent and the behavior affects agents/operators, add concise documentation.

### 3. Bump every version source

Update the target version consistently in:

- `package.json`
- `package-lock.json` root `version`
- `package-lock.json` `packages[""].version`
- `src/extension/manifest.json`
- `skills/browser-control/scripts/package.json`

Then rebuild generated extension metadata:

```bash
npm run build:extension
```

Verify all version-bearing files:

```bash
grep -n '"version"' package.json package-lock.json src/extension/manifest.json skills/browser-control/extension/manifest.json skills/browser-control/scripts/package.json
```

### 4. Validate

Run:

```bash
npm run build:extension
npm run typecheck
npm run lint
npm test
```

If browser-facing behavior changed and Chrome/extension are available, also run focused live smoke. First check readiness:

```bash
node skills/browser-control/scripts/browser-control.js doctor --json
```

If daemon or extension versions are stale, tell the user to restart/reload and only continue live smoke after confirmation. Do not block non-browser release work on unavailable live smoke unless the change requires it.

### 5. Commit

Before committing, show:

```bash
git diff --stat
git status --short
```

Stage only relevant files. Commit with a concise message, usually:

```bash
git commit -m "chore: release <version>"
```

If substantial feature/fix changes are still uncommitted, split commits logically before the release version commit.

### 6. Tag

Create an annotated tag after commit and validation:

```bash
git tag -a v<version> -m "v<version>"
```

Verify the tag points at the intended commit.

### 7. Push code and tag

Push branch and tag:

```bash
git push
git push origin v<version>
```

If no upstream exists, set upstream explicitly with the current branch name.

### 8. Open PR/MR

Create a PR against the base branch. Prefer, in order:

1. GitHub connector/tool, if available and authorized;
2. `gh pr create`, if installed and authenticated;
3. Browser Control with the real GitHub UI, after confirming intended PR creation.

Suggested PR title:

```text
Release v<version>
```

Suggested PR body:

```markdown
## Summary
- review documentation/code alignment and update release metadata
- bump Browser Control to `<version>`
- rebuild generated extension assets

## Validation
- `npm run build:extension`
- `npm run typecheck`
- `npm run lint`
- `npm test`
- live smoke: <include if run, otherwise explain why skipped>
```

### 9. Final report

Report in Chinese:

- version;
- commit SHA;
- tag;
- pushed branch;
- PR URL;
- validation commands and pass/fail evidence;
- warnings, skipped live smoke, or manual follow-up.
