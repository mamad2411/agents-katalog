---
name: test-feature
description: Run every automated check a project has, build it the way users get it, and on a connected iPhone install, launch and watch for crashes; then write a test report with the real output. Use after implementing a task and before review (the test step of the spec, plan, implement, test, review workflow), again after review fixes, or when asked to "test this" or "run the tests".
argument-hint: "[task-name]"
allowed-tools: Bash(git status *) Bash(git log *) Bash(ls *)
model: sonnet
effort: medium
---

# Test the feature

Invoked as `/dev-workflow:test-feature` when installed as a plugin, or `/test-feature` if the folder is copied into `~/.claude/skills/`.

Goal: prove, with real output, that the project's checks pass after this change. Never say "should work".

## Context
- Status: !`git status --short 2>/dev/null | head -30 || true`
- Recent commits: !`git log --oneline -5 2>/dev/null || true`
- Project files: !`{ setopt nonomatch 2>/dev/null; ls -d testing.md CLAUDE.md AGENTS.md package.json pyproject.toml setup.py requirements*.txt *.xcodeproj Package.swift app.json app.config.* tests test __tests__ docs/testing.md docs/implementation */testing.md */CLAUDE.md */AGENTS.md */package.json */pyproject.toml */setup.py */requirements*.txt */*.xcodeproj */Package.swift */app.json */app.config.* */tests */test */__tests__; } 2>/dev/null | sort | head -40 || true`

## Steps

0. **Find the project root.** The context lines above describe the folder Claude was started in, which may not be the project the task lives in (for example a fork or a parent folder). If the argument or the task's docs are in another folder, go there and re-check `git status`, `git log --oneline -5` and the project files before going on. Treat the context lines as hints only.
1. **Find the task.** Use the argument, else the newest folder in `docs/implementation/`, else ask. The report goes to `docs/implementation/<task>/test-report.md`. If the project has no `docs/implementation/`, ask where to put it. If the task has no code changes yet (spec and plan only), run the checks anyway and label the report "baseline, before any change".
2. **Find the checks.**
   - If `docs/testing.md` exists, it is the source of truth: run exactly what it lists, in its order, with its pass criteria.
   - Otherwise detect the stacks from the files above. Several can apply in one repo. Say what you detected, and offer at the end to write `docs/testing.md`.
   - Also read the commands `CLAUDE.md` or `AGENTS.md` name for testing.
3. **Load the recipe** for each stack: open and read the file now, before running anything, and follow it (don't work from memory):
   - Native iOS / Xcode project (optional, macOS with Xcode only): [ios-native.md](ios-native.md)
   - Expo / React Native: [expo.md](expo.md)
   - Node, Next.js, plain JS: [node-web.md](node-web.md)
   - Python: [python.md](python.md)
4. **Run in this order:** fast tests → type checks and lint → production-style builds → device. A failure doesn't stop the independent checks after it, but don't install a build that failed.
5. **Record each check:** the command, PASS / FAIL / NOT RUN, counts (tests, checks), and the decisive lines. For a failure, keep the full failing output, trimmed to the relevant part.
6. **Write the report** (format below), then reply with the same table and a one-line verdict.

## Rules
- Real output only. A check that was skipped, impossible or flaky says so, with the reason.
- **Never create or boot a simulator.** Use the connected device. If none is connected, or it's locked, mark the device checks NOT RUN with the reason. Don't fall back to a simulator. This is the default; a project's `docs/testing.md` may say otherwise (for example, "use the iOS Simulator"), and then that file wins.
- Don't edit source code to make a check pass. If a test is wrong, report it; fixing it is separate work.
- Don't commit or push.
- Never print or save secrets (API keys, tokens, `.env` values). Redact them in quoted output.
- Long-running output: filter it (`grep`, `tail`) to what decides pass or fail.
- Build into a scratch folder (your scratchpad when you have one), not the repo.
- **Clean up at the end** by the rules in [../token-wise/cleanup.md](../token-wise/cleanup.md): stop what this run started (dev servers, watchers), shut down any simulator it booted, and delete its scratch output except the last Release build when a rerun is likely (for example after a review).

## Report format

```markdown
# Test report: <task>
<date, time> · <git short sha> (<branch>) · uncommitted changes: yes/no

| # | Check | Command | Result | Detail |
|---|---|---|---|---|
| 1 | Swift core | `sh scripts/test_ios_core.sh` | PASS | 828 checks |

**Verdict:** all passed / N failed / device not checked (reason)

## Not run
- <check>: <reason>

## Failures
<check>: the command, then the relevant output in a code block
```
