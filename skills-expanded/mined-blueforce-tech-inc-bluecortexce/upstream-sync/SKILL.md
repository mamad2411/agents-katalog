---
name: upstream-sync
description: Compare BlueCortexCE with the experimental claude-mem-java port and its WebUI for inspiration and feature-gap analysis. Use from any Agent Skills-compatible runtime when the user asks to inspect upstream changes, study claude-mem improvements, update the WebUI submodule, or selectively adapt an idea; never treat the Java port as production-ready or as an automatic merge source.
---

# Upstream Sync Skill

Use this workflow to study and selectively adapt ideas from the projects that BlueCortexCE tracks. The phrase “sync upstream” means **inspiration, comparison, and controlled adaptation** here—not a blind merge, production certification, or claim that the source implementation is production-ready.

## Portability

This is a project-local, Agent Skills-compatible instruction set. It is intentionally usable by Claude Code, Codex, OpenClaw, and other runtimes that can load `SKILL.md` files. The workflow is not tied to any one agent, model, lifecycle hook, slash command, UI, or plugin API.

- The host runtime decides how this Skill is discovered, invoked, authorized, and reported; do not assume a Claude-specific or Codex-specific invocation mechanism.
- Use ordinary workspace-relative paths, shell commands, Git, and the project's available build/test tools. If the host cannot provide a required capability, report that limitation instead of inventing a result.
- Do not rely on agent-specific memory stores, hooks, subagents, or permission behavior. Preserve the private-path and WIP rules below even when the host provides no persistent memory.
- Keep the workflow's repository and documentation outputs portable: use Markdown, public repository URLs, commit IDs, and `<local-upstream-path>` rather than host-specific metadata.

## Upstream Positioning

The `claude-mem-java` repository is an **experimental Java port**. It has no required implementation-quality level and provides **no guarantee of production readiness, operational safety, security, compatibility, or correctness**. Treat its code, migrations, tests, and design choices as research material:

- inspect the idea and its intended behavior;
- compare it with BlueCortexCE's current implementation;
- independently review risks, contracts, and failure modes;
- adapt only what is justified for this codebase;
- compile and test the adapted behavior before calling it complete.

Do not describe an upstream feature as supported merely because it exists in `claude-mem-java`. Do not copy its migrations or implementation without checking whether BlueCortexCE already implements a different version of the behavior.

## Source Defaults

Use these public repository URLs unless the user explicitly names alternatives:

| Source | Default URL | Role |
|--------|-------------|------|
| claude-mem-java | `https://github.com/wubuku/claude-mem-fork.git` | Experimental backend reference |
| WebUI | `https://github.com/Blueforce-Tech-Inc/claude-mem.git` | `webui/` submodule source |

The required runtime input is the **local checkout path** of `claude-mem-java`. The user may provide it in the request or a previous message; do not ask them to repeat the default repository URL.

Local checkout paths are private machine information. Never write them to tracked files, `docs/drafts/upstream-sync-plan.md`, commits, pushed output, or other artifacts intended for Git. Use `<local-upstream-path>` in plans and reports. A local-only ignored memory file may contain the path when that improves continuity.

If the local checkout's `origin` URL differs from the default, report the mismatch and ask whether it is intentional. Do not silently replace the user's remote or clone another repository.

## Paired WebUI Invariant

The `webui/` git submodule is a compatibility artifact, not an independently
floating “latest WebUI” pointer. It must always point to the WebUI commit that
is known to match the backend behavior selected for the current BlueCortexCE
working tree.

- Record the backend reference commit and the paired WebUI commit together in
  the sync plan or implementation summary.
- Do not advance `webui/` to `origin/main` merely because it is newer.
- Before changing the gitlink, inspect the WebUI routes, response shapes, and
  SSE events that the backend implements; verify that the backend contract is
  compatible with the chosen WebUI commit.
- If no compatible WebUI commit can be identified, keep the existing gitlink
  and report the unresolved pairing instead of guessing.
- When the backend changes after a pairing decision, re-check the WebUI
  pointer before declaring the work complete. A checked-out submodule commit
  is not enough—the parent repository must record the intended gitlink.

## Quick Reference

```bash
# Inspect the local backend reference without changing its working tree
git -C <local-upstream-path> remote -v
git -C <local-upstream-path> fetch origin main --prune
git -C <local-upstream-path> log --oneline --decorate <base-commit>..origin/main

# Inspect WebUI alignment
git submodule status -- webui
git -C webui remote -v
git -C webui log -1 --oneline --decorate

# Inspect the local migration baseline
find backend/src/main/resources/db/migration -maxdepth 1 -type f -name 'V*.sql' -print | sort -V | tail -1

# Build and validate
cd backend && ./mvnw clean compile
```

Use `mvn clean compile` only when the Maven wrapper is unavailable. Fetching remote refs is read-only with respect to source files; checking out a new WebUI commit changes the submodule and requires an explicit alignment decision.

## Step 0: Scope and Safety

Use this Skill when the user asks to:

- inspect or compare BlueCortexCE with `claude-mem-java`;
- study upstream improvements or feature gaps;
- update the `webui/` submodule to match its public source;
- selectively adapt an idea from the experimental Java port.

Before changing files:

1. Inspect `git status --short` in BlueCortexCE and the local reference checkout.
2. Preserve existing work in progress. Never reset, stash, discard, rebase, or overwrite another person's changes without explicit permission.
3. If an uncommitted change overlaps a file that must be modified, stop and ask how to handle that overlap.
4. Do not commit or push as part of this skill unless the user separately requests it.
5. Keep the experimental status visible in plans, summaries, and implementation notes.

## Step 1: Resolve Inputs

### 1.1 Local backend checkout

If the user has already supplied a local path, use it as `<local-upstream-path>` without asking again. Otherwise ask exactly:

> 请提供或确认本机上的 claude-mem-java 代码库路径。

Validate that the path is a Git worktree and that it contains the expected backend project. Then inspect its remotes:

```bash
git -C <local-upstream-path> rev-parse --show-toplevel
git -C <local-upstream-path> remote get-url origin
git -C <local-upstream-path> status --short
```

The expected `origin` is `https://github.com/wubuku/claude-mem-fork.git`, unless the user explicitly selected another source.

### 1.2 WebUI alignment

Inspect rather than asking the user to report a status that Git can establish:

```bash
git config -f .gitmodules --get submodule.webui.url
git submodule status -- webui
git -C webui remote get-url origin
git -C webui rev-parse HEAD
git -C webui rev-parse origin/main 2>/dev/null
```

The expected WebUI source is `https://github.com/Blueforce-Tech-Inc/claude-mem.git`. Report whether the submodule is:

- initialized or uninitialized;
- on the expected remote;
- at the same commit as `origin/main`, behind it, ahead of it, or unable to compare.

Ask for a decision only when the remote is unexpected, the submodule cannot be inspected, or updating it would change the parent repository. Do not check out `origin/main` silently.

### 1.3 Comparison baseline

The reference commit is optional, but `HEAD` is **not** a valid implicit comparison base. Resolve the baseline in this order:

1. Use an explicit commit supplied by the user.
2. Reuse a valid public commit marker from the existing `docs/drafts/upstream-sync-plan.md` or another project sync record.
3. If no trustworthy marker exists, ask for the upstream commit from which to compare.

Verify the chosen commit exists in the local reference checkout:

```bash
git -C <local-upstream-path> cat-file -e <base-commit>^{commit}
```

Compare the baseline to `origin/main`, not to the local reference `HEAD` by assumption:

```bash
git -C <local-upstream-path> log --reverse --oneline <base-commit>..origin/main
```

## Step 2: Analyze Upstream Changes

After the inputs are resolved:

1. Fetch `origin/main` in the local reference checkout.
2. List commits and inspect each relevant diff with `git show --stat` and `git show`.
3. Classify changes into migrations, entities, repositories, services, controllers, configuration, tests, API contracts, and WebUI dependencies.
4. Search BlueCortexCE before calling a feature missing. Existing local behavior takes precedence over old notes or templates.
5. Inspect the current highest local Flyway migration dynamically. At the time this skill was revised, BlueCortexCE contained V18; treat that as a checked observation, not a permanent assumption.
6. Read `.agents/skills/upstream-sync/references/feature-patterns.md` for implementation patterns only after the gap analysis. Verify every pattern against current source code.
7. Produce a feature gap analysis that distinguishes:
   - already implemented;
   - partially implemented or behaviorally divergent;
   - an idea worth adapting;
   - blocked by WebUI/API compatibility;
   - intentionally not applicable;
   - unsafe to port without additional design or tests.

Do not copy upstream commits blindly. Preserve BlueCortexCE-specific migrations, API compatibility, provider configuration, and client integrations.

## Step 3: Create or Update the Sync Plan

Use the existing `docs/drafts/upstream-sync-plan.md` when present; do not create a duplicate plan. The plan is a draft project document and must not contain local machine paths.

Use this structure:

```markdown
# BlueCortexCE Upstream Sync Plan

**Date**: YYYY-MM-DD
**Status**: Draft vN
**Positioning**: Experimental reference; inspiration and gap analysis only
**Backend source**: https://github.com/wubuku/claude-mem-fork.git
**WebUI source**: https://github.com/Blueforce-Tech-Inc/claude-mem.git
**Reference**: upstream commit <upstream-commit>

## Executive Summary

## Current State
| Component | BlueCortexCE | Reference |
|-----------|--------------|-----------|
| Latest migration | <local-latest-migration> | <reference-latest-migration> |

## Feature Gap Analysis

## Adaptation Plan

## Testing

## Rollback
```

Plan rules:

- Use `<local-upstream-path>` rather than any developer-specific absolute path.
- State clearly that the Java port is experimental and not a production authority.
- Use placeholders such as `<upstream-commit>` when a plan is intended for Git; do not embed private checkout paths in examples or history.
- Record the dynamically observed migration baseline; do not repeat already-applied V17/V18 work as new work.
- Keep the plan focused on the current study; move completed historical work to the implementation summary instead of duplicating it.
- Review the plan at least three times before presenting it or using it to drive implementation.

## Step 4: Implement Adapted Changes

Only implement items identified as worthwhile adaptations and approved by the user. A feature in the experimental port is not, by itself, approval or evidence of correctness.

### Order of operations

1. Add a new Flyway migration using the next number after the highest migration actually present in BlueCortexCE.
2. Update entities and JSON properties.
3. Update repositories and query parameters.
4. Update services, asynchronous processing, and event handling.
5. Update controllers and API responses.
6. Update or align the WebUI submodule only after backend contracts are compatible.
7. Update tests and documentation.

### Compatibility and quality checks

Before changing API response fields, search both `webui/` and `proxy/`. Preserve the established contracts for `hasMore`, `updateFiles`, `CLAUDE_MEM_*`, and the distinct singular `/api/mode` versus plural `/api/modes` families.

For new platform fields, use the existing snake_case JSON contract, such as `platform_source`, and verify all consumers before changing names. For new feedback or retrieval behavior, trace the complete path from controller to repository and event/async processing rather than changing only the DTO.

For every adapted idea, record the independent review required in the plan: schema safety, data migration behavior, concurrency, failure handling, security/privacy, API compatibility, and regression coverage as applicable.

### WebUI submodule changes

If alignment is requested and a compatible paired commit has been identified:

```bash
git -C webui fetch origin main
git -C webui checkout <paired-webui-commit>
git add webui
```

Explain that the parent repository records a new submodule pointer. Never
commit the submodule pointer automatically unless the user explicitly
requested a commit. If the checked-out commit differs from the parent gitlink,
report that as unfinished work rather than treating the worktree state as the
final pairing.

## Step 5: Verify

Run the narrowest relevant checks first, then broader checks when available:

```bash
cd backend && ./mvnw clean compile
cd .. && git diff --check
```

When the service is running, verify changed endpoints with representative requests. Run relevant scripts from `scripts/`, such as `regression-test.sh`, `thin-proxy-test.sh`, `mcp-e2e-test.sh`, or `webui-integration-test.sh`, only when their prerequisites are available.

Verify all of the following before declaring success:

- migrations are numbered after the actual local maximum;
- no duplicate V17/V18 migration is introduced;
- API response contracts remain compatible with WebUI and Proxy consumers;
- WebUI submodule status and the parent gitlink match the intended backend/WebUI pairing;
- private local paths are absent from tracked diffs and the sync plan;
- adapted code has independent tests or an explicit testing gap;
- build/test results are reported as passed, failed, skipped, or not run—never implied;
- no statement implies that the experimental Java port is production-ready.

## Step 6: Document the Result

Append an implementation summary to `docs/drafts/upstream-sync-plan.md` without private paths:

```markdown
## Implementation Summary (YYYY-MM-DD)

### Completed
| Adapted idea | Status | Files |
|--------------|--------|-------|
| ... | ✅ Done | ... |

### Independent Review
- Production-readiness assessment: <result>
- API and WebUI compatibility: <result>
- Migration and rollback safety: <result>
- Test coverage: <result>

### Build and Test Status
- Compile: <passed/failed/not run>
- Regression: <passed/failed/not run>
- Backend reference / paired WebUI commit: <public commit IDs>

### Pending
- [ ] ...
```

If the plan or any tracked document contains a local checkout path, replace it with `<local-upstream-path>` before review or commit.

## Questions and Stop Conditions

Ask the user only when the workflow cannot resolve the answer safely:

1. Missing or invalid local `claude-mem-java` checkout path.
2. Local reference remote differs from the default and the user has not explained why.
3. No valid comparison baseline can be found.
4. WebUI remote/status is inconsistent or updating the submodule would be a consequential choice.
5. Existing WIP overlaps a file that implementation would change.
6. The proposed adaptation has a production-readiness, migration, security, or compatibility risk that cannot be resolved from the repository.

Do not ask for the two default repository URLs unless the user wants to override them. Do not proceed past a required stop condition by guessing.

## Common Pitfalls

1. Calling the experimental Java port a production upstream or treating its tests as a production guarantee.
2. Comparing `<base>..HEAD` in the wrong repository; inspect `origin/main` explicitly.
3. Assuming V16 is current; determine the highest local migration dynamically.
4. Re-adding V17 or V18 when those migrations already exist locally.
5. Writing a developer's local checkout path into a tracked plan or commit.
6. Updating a detached WebUI submodule without checking its remote and parent pointer.
7. Changing API fields without searching both WebUI and Proxy consumers.
8. Treating a compile-only result as proof that integration or regression tests passed.
9. Assuming the host runtime supplies Claude-specific hooks, Codex-specific commands, or OpenClaw-specific APIs.
