---
name: release-ops
description: Handle release promotion requests that inspect commits on `uat`, find changes missing from `release` or `master`, cherry-pick them in source order, create SemVer tags, and push. Use for prompts about “哪些提交没上 release/master”, “上生产”, “发版”, “推上去”, “发到release”, “cherry-pick 到 release”, feature-based backporting, or release-tag publishing, including inspect-only prompts.
---

# Release Ops

Use this skill for git release promotion tasks that follow a repeatable backport workflow.

## Defaults

- Default source branch: `uat`
- If default `uat` does not exist, stop and ask the user to specify the source branch.
- Target production branch: prefer `release`, otherwise `master`
- Timezone for relative dates: `Asia/Shanghai`
- Default author name: current repo `git config user.name`; fall back to `assets/defaults.json`
- Author matching: git `author name`
- Author scope: only process the current author by default; include another author only when the user explicitly names that author or asks to process that other author's commits.
- Missing-on-target rule: patch-equivalent, not raw commit hash
- Preflight checks: `git fetch --all --prune --tags` and clean `git status`
- Tag style: annotated, message `chore: release vX.Y.Z`
- Release commit: when the target branch has a root `package.json` with a `version` field, set it (and the root version in `package-lock.json`) to the new tag without the `v`, commit as `chore: release vX.Y.Z`, and tag that commit. The tag version is authoritative; do not keep a separate hand-maintained `package.json` version. Backend `pom.xml`/`build.gradle` and uni-app `manifest.json` versions are not touched. Repositories without such a `package.json` get only the annotated tag on the last cherry-picked commit. The release commit stays on the target branch and is not pushed back to the source branch.
- Release batching invariant: one user release request plus one repository produces at most one new tag. Collect every confirmed commit for that repository first, cherry-pick them in source order, then tag and push once.

## Script

Use `scripts/release_ops.py` for deterministic execution.
Resolve script paths relative to this skill directory. The installed path is:

```bash
~/.agents/skills/release-ops/scripts/release_ops.py
```

Do not use the legacy `~/.codex/skills/release-ops/...` path; this skill is installed under `~/.agents/skills`.

Typical flow:

1. Run `inspect` first.
2. Review blockers, warnings, pending commits, target branch, proposed tag, and `package_version_change`.
3. Run `execute` only when the user has authorized this release scope (including its branch/tag publication) and the script reports no blockers. Inspect-only requests remain read-only; reuse an already confirmed commit list only within the same release request (see [Execution Rules](#execution-rules)).
4. Apply [Batch Confirmation](#batch-confirmation) when the pending-count threshold is exceeded. Reuse explicit authorization from the same release request for the same exact commit list and target; pass `--confirm-all` with repeated `--commit <sha>` selectors instead of asking again.
5. Use `--sync-target` with execute mode when the local target branch may be behind `origin/<target>`; it only fast-forwards when there are no local-only target commits.
6. After execute mode finishes, the script restores the branch that was checked out before execution when possible.
7. When one repository contains multiple requested features or disconnected file clusters, inspect them separately if needed, then execute once with repeated `--commit` selectors. Never run `execute` repeatedly for the same repository in one user release request.

Examples:

```bash
uv run ~/.agents/skills/release-ops/scripts/release_ops.py inspect \
  --repo "$PWD" \
  --since 2026-04-14 \
  --until 2026-04-14T23:59:59+08:00
```

```bash
uv run ~/.agents/skills/release-ops/scripts/release_ops.py execute \
  --repo "$PWD" \
  --feature "结算统计页面" \
  --bump auto \
  --sync-target
```

Batch exact commits from one repository under one tag:

```bash
uv run ~/.agents/skills/release-ops/scripts/release_ops.py execute \
  --repo "$PWD" \
  --commit 17247b5b9540 \
  --commit 260d04e3b83b \
  --commit 43813af5e7e0 \
  --bump auto \
  --sync-target
```

Short natural-language prompts should usually omit the target branch and bump type:

- `帮我查找今天提交但还没有合并到生产分支的提交，cherry-pick过去并推送`
- `帮我查找 Anonym 提交到 uat 的合同筛选功能，但还没上生产分支的，cherry-pick 并推送`

Stable shorthand prompts:

- `今天没上生产的提交，推上去`
- `今天没上生产的提交，发版`
- `合同筛选功能没上生产的提交，发到release`
- `合同筛选功能没上生产的提交，上生产`

Do not rely on bare action words alone. For stability, shorthand execute prompts still need a selector such as:

- a time scope like `今天`, `昨天`, `一周内`
- a feature scope like `合同筛选功能`

## Mode Detection

Interpret the prompt as **execute mode** when it contains action intent such as:

- `cherry-pick`
- `合并到`
- `打 tag`
- `推送`
- `上生产`
- `发版`
- `推上去`
- `发到release`

Otherwise treat it as **inspect-only mode**.

## Commit Selection

Support these selectors:

- author + relative time
- author + absolute time range
- author + feature keyword
- author + feature keyword + time range
- author + one or more exact commits

If the prompt omits the author, use the current repo `git config user.name`; if unavailable, use the configured default author. Do not include commits by other authors unless the user explicitly names that author or explicitly asks to process that other author's commits.

If the prompt gives a feature keyword but no time range:

1. search the last 1 week,
2. then expand by 1 week at a time,
3. stop after 1 month,
4. report no match if still empty.

Feature matching details live in `references/matching-rules.md`.

## Execution Rules

- Treat the current user release request as the batch boundary. For each repository, finish selection before execution and create exactly one final tag, even when commits belong to multiple features or file clusters.
- A release request authorizes only the repositories or components the user named and the commits listed or selected when the user made it. A later bug report, fix, feature, or feedback round in the same conversation is a new release request even when the target and tag line are unchanged: run `inspect` again and wait for an explicit release request before `execute`. Never cite an earlier release ("沿用刚才的发布范围") as scope for new commits.
- Use repeated `--commit` selectors when a single feature selector cannot safely express the whole confirmed set. Explicit commits must be reachable from the source branch, match the selected author, and are reordered into source-branch order automatically.
- Do not split one repository into sequential tagged releases merely to satisfy feature-cluster matching. If the exact set is still uncertain, stop and ask instead of producing multiple tags.
- If pending commits after filtering are `0`, report no action needed.
- If pending commits are `1-5` in execute mode, execute directly.
- If pending commits are `>5`, apply [Batch Confirmation](#batch-confirmation); the count alone does not require repeating an existing exact-scope authorization.
- `inspect` always fetches first and analyzes against the latest remote target ref such as `origin/release`.
- In execute mode, use `--sync-target` to fast-forward the local target branch to the remote target before cherry-picking when it is safely behind.
- `--sync-target` must not resolve local-only commits or diverged target branches; stop and report those cases for manual handling.
- Cherry-pick multiple commits in original source-branch chronological order.
- Attempt conflict resolution before stopping.
- The script currently aborts failed cherry-picks and reports the conflict files; if needed, resolve manually after the script stops.
- After execution, switch back to the branch that was active before the run when restoration is possible.

## Batch Confirmation

The pending-count threshold protects unconfirmed release scope; it does not invalidate authorization already given in the current task. Before executing more than five pending commits:

- Inspect the exact pending commit list, repository, source, target, and proposed tag/production effects. Reuse an explicit approval, given within the same release request, of that same complete list and publication scope, including an earlier `全部执行` tied to the displayed list. Do not ask again solely because the count exceeds five.
- When that authorization exists and all other checks pass, use repeated `--commit <full-sha>` selectors for the confirmed list and `--confirm-all`. The flag records the existing approval; it does not grant permission or bypass other blockers.
- If the list or publication scope was not confirmed, prepare the concrete list and ask once. Allow confirming all, narrowing the scope, or cancelling; do not force an all-or-nothing choice. A generic `发版` or an inspect-only request is not batch approval.
- If inspection finds additional candidates, a different target, or newly uncovered side effects outside the approved scope, pause only that release operation for the changed scope. Never silently include new commits or use `--confirm-all` to bypass unresolved scope.

## Tag Rules

- If the user explicitly says `major`, `minor`, or `patch`, follow SemVer exactly.
- If the prompt implies execution but omits the bump type, infer it using `references/matching-rules.md`.
- For the bump decision, ask only when inference is not confident enough. Other release authorization and risk stops still apply.
- Use the latest SemVer tag reachable from the target branch only.
- If the latest reachable tag is not `vX.Y.Z`, stop and report the problem.
- Before creating the tag, clearly state: current reachable tag -> target tag, plus the `package.json` version change when the script reports one.

## Risk Stops

Stop and ask before continuing when any of these happen:

- the prompt has only an execute alias such as `上生产` or `发版` but no selector
- default source branch `uat` is absent
- `release` and `master` are both absent
- feature keyword is too vague, such as only `优化`, `修改`, or `调整`
- fuzzy feature matching finds multiple unrelated clusters and the current release request has not confirmed an exact commit set; an already confirmed SHA list follows [Batch Confirmation](#batch-confirmation)
- related commits from other authors are detected
- bump inference is low confidence
- conflict resolution is not reliable
- pending commits exceed the confirmation threshold and the exact batch/publication scope lacks confirmation in the current release request under [Batch Confirmation](#batch-confirmation)
- pending commits were created after the release request that would authorize this run, or the latest user message asks for a fix or feature rather than a release

## Output Shape

Inspect-only mode:

- list only `commit sha + subject`
- if other-author related commits exist, call that out separately
- include a coarse bump suggestion

Execute mode:

1. summarize the matched pending commits and quote the user message that authorizes this release
2. report the target branch
3. report the tag plan
4. cherry-pick
5. create the `chore: release vX.Y.Z` release commit when a `package.json` version exists, then the annotated tag
6. push branch and tag
7. verify remote refs

Use [Production Release Completion](../../../.codex/docs/workflows/harness-engineering.md#production-release-completion) as the completion boundary: stop after successful publication and remote-ref verification by default. Do not query or wait for production CI/build/deployment unless the user explicitly requests it; report those results as unchecked.

This boundary covers waiting for CI, not deployment steps that a tag push does not perform. When an installed project deploy skill says the request's wording (for example `上线` / `发布上线` / `上生产` for a service that only changes in production after a manual k8s apply) asks for that deployment, continue with that skill after remote-ref verification instead of ending the turn; that skill owns waiting for the tag pipeline and its own confirmation step.

## Resources

- Deterministic CLI: `scripts/release_ops.py`
- Matching and bump heuristics: `references/matching-rules.md`
- Default config template: `assets/defaults.json`
