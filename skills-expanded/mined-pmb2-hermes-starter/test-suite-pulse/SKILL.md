---
name: test-suite-pulse
description: >-
  Run periodic targeted test suite sweeps with fix-suite regression tracking,
  divergence monitoring, and working tree audits. Designed for cron-based QA
  roles that validate codebase health at regular intervals by running a focused
  subset of critical test suites rather than the full collection.
version: 1.3.0
author: Sentry
metadata:
  hermes:
    tags: [cron, qa, testing, pulse, targeted-sweep, regression-prevention, divergence]
    triggers: [test-suite-pulse, targeted-sweep, fix-verification, regression-check, suite-health]
    related_skills: [discord-report-format, qa-pulse]
---

# Test Suite Pulse

Run periodic targeted test suite sweeps to validate fix categories, detect regressions early, and track divergence from upstream. Designed for cron-based QA agents (like Sentry) that need to verify codebase health quickly at regular intervals without running the full 40K+ test collection.

## Overview

A test-suite pulse is a bounded investigation cycle (typically every 4h or daily) that:

1. **Gates on quiet hours** — skips all work during 00-06 ET
2. **Reads pulse history** — learns what was tested, what failed pre-existing, and what fix categories matter
3. **Discovers test paths dynamically** — files move during rebases
4. **Runs targeted suites** — specific fix categories, not full collection
5. **Verifies fix categories** — checks that each known Windows compat fix still holds
6. **Tracks divergence** — monitors behind/ahead counts, rate of growth, and file overlap risk
7. **Audits working tree** — checks for uncommitted changes, stale stashes, artifacts
8. **Appends pulse log** — structured entry to PULSE.md
9. **Delivers compact report** — Discord-formatted output

## Phase 1: Quiet Hours Gate

```bash
TZ='EST5EDT,M3.2.0/2,M11.1.0/2' date +%H
```

- **00-06 ET**: output `[SILENT]` — no work, no report
- **07+ ET**: proceed with full pulse

⚠️ **Use the POSIX `EST5EDT,...` form, not `TZ='America/New_York'`.** git-bash/MSYS lacks the IANA zoneinfo database — an IANA zone name is silently ignored and `date` falls back to GMT, so the gate trips on the wrong hour (e.g. 6 AM ET = 10 AM GMT → proceeds during quiet hours; 11 PM ET = 3 AM GMT → wrongly silent). Validate with `%Z` in the format string if unsure.

## Phase 2: Read Pulse History

Read the last 2-3 entries from the pulse log (`$PROFILE_DIR/PULSE.md`). Extract:

- **Fix categories** — the set of fix suites that need re-verification
- **Pre-existing failures** — don't re-flag these as new regressions
- **Divergence trend** — growing/shrinking and rate
- **Last cycle's Next Action** — was it acted on?
- **Flake evolution** — check if previously noted pre-existing failures are still the same (they can change between cycles as upstream fixes or shifts test isolation)

## Phase 3: Dynamic Test Path Discovery

**Never hardcode test paths.** Upstream rebases frequently relocate test files. Always discover paths first:

```bash
find tests -name "*.py" -path "*tirith*"
find tests -name "test_context_references.py"
find tests -name "test_approval*.py"
find tests -name "test_file_safety_sandbox_mirror.py"
find tests -path "*hindsight*"
```

**Class names in pulse-log history ≠ file names.** When re-running a suite referenced in PULSE.md/digest entries, the entry names the class or commit subject, not the path (`TestReapCgroup` lives in `tests/gateway/test_cgroup_cleanup.py`, not `test_reap_cgroup.py`). Run `find tests -name "*<keyword>*"` (e.g. `*cgroup*`, `*godmode*`, `*busy*`) before running — a guessed path fails collection with `ERROR: file or directory not found: ...` and wastes a cycle.

Common relocation history:
- Context refs: `tests/tools/` → `tests/agent/`
- Hindsight: `tests/tools/` → `tests/plugins/memory/`
- Docker/MemPalace tests: often stripped entirely by upstream rebase
- **Major reorganization ~Jul 2026**: `agent/tests/` flattened into `tests/{agent,tools,acp,cron,cli,tui_gateway}/`. File-safety tests moved from `agent/tests/test_file_write_safety.py` to `tests/agent/test_file_safety*.py` and `tests/tools/test_write_*.py`. Approval tests split across `tests/acp/test_approval_isolation.py`, `tests/tools/test_write_approval.py`, `tests/tools/test_write_deny.py`. Per-directory test counts dropped significantly (ACP went from 311→84 in `tests/acp/` alone; approval/write gates add 61 more in `tests/tools/`).

After the reorganization, known test locations:
- File-safety suites: `tests/agent/test_file_safety*.py`
- Approval/deny gates: `tests/tools/test_write_approval.py`, `tests/tools/test_write_deny.py`
- ACP server/auth: `tests/acp/` (84+ tests)
- ACP adapter: `tests/acp_adapter/`
- Cron: `tests/cron/` (172+ tests, 1 pre-existing tilde-expand failure)
- Windows compat: `tests/tools/test_windows_compat.py`
- Windows native: `tests/tools/test_windows_native_support.py`

## Phase 4: Run Targeted Suites

**Locate the codebase first.** The Hermes Agent repo lives at `~/AppData/Local/hermes/hermes-agent` — NOT in the `${MY_REPOS}/Documents/github/` root (that root holds user projects like `_project`). Check both if unsure: `ls -d ~/AppData/Local/hermes/hermes-agent ${MY_REPOS}/Documents/github/_project`.

**Invoke pytest via the repo venv explicitly:** `venv/Scripts/python.exe -m pytest ...`. Bare `python` on PATH is the system interpreter (e.g. `${USER_HOME}\AppData\Local\Programs\Python\Python311\python.exe`), which may lack pytest or resolve foreign site-packages (see the Jul 30-31 PYTHONPATH contamination history in PULSE.md — bare `python -m pytest` failed with `No module named pytest`). The repo `venv/` has pytest + correct deps; verify once per session with `venv/Scripts/python.exe -m pytest --version` if a run behaves oddly.

Run each fix-category suite individually (not a single `pytest` call for everything — suite-level granularity aids debugging):

```bash
# Targeted runs, one per suite category
# Always discover current paths first — see Phase 3
pytest tests/agent/ -k "file_safety" --tb=short -q
pytest tests/acp/ --tb=short -q
pytest tests/tools/test_write_approval.py tests/tools/test_write_deny.py --tb=short -q
pytest tests/tools/test_windows_compat.py --tb=short -q
pytest tests/cron/ --tb=short -q
```

**Standing combined-regression baseline (Sentry cycle default):** the fast health check each cycle is one `venv/Scripts/python.exe -m pytest` call over the three-path combo `tests/tools/test_approval.py tests/scripts/ tests/hermes_state/`. **Baseline as of Aug 4 2026: 158 passed (~35s)** — composition approval 94 + scripts 22 + hermes_state 42. The historical 399 baseline (312+17+70) no longer applies: upstream test-prune wave `39975613b` (Jul 29, 28,106→19,757 test fns) shrank `test_approval.py` to 93 tests, and the pre-reset 312-test copy was local-only, lost in the Jul 2026 `origin/main` reset and not carried by the restored commits. Pulse-log shorthand **"approval" = `tests/tools/test_approval.py`** — NOT `tests/test_approval.py`; the guessed root path fails collection with `ERROR: file or directory not found` (wasted a cycle Aug 2026). Re-`find` if collection errors; counts drift as upstream adds tests.

Record per suite:
- **Pass/fail count** (e.g., 95/95, 13/14)
- **Timing** (e.g., 2.31s)
- **Test-count drift** — upstream may add or remove tests in a fix-category suite between cycles. Note any change (e.g., "ContextRefs 19/19, grew from 17→19, no regression"). Always re-discover expected counts from actual run results, not from the pulse log.
- **Pre-existing failures** — confirm they're the same ones from last cycle. If a previously-known flake disappears and a new one appears in a different test, update the record. This is normal flake evolution.
- **New regressions** — 🔴 attention items to investigate first

### Identifying Suite-Level Flakes

A test that passes in isolation but fails when run as part of the full suite collection is a **suite-level isolation flake**, not a regression. Verify by running the failing test alone:

```bash
pytest <test_file>::<TestClass>::<test_name> -x -q
```

If it passes in isolation but fails in the full sweep, flag it as a suite-level flake and note the variant (it may replace a prior flake that upstream fixed).

## Phase 5: Fix Category Verification

Each cycle, verify that previously-applied fixes are still holding. A fix category that silently regresses (even without a test failure) should be caught here.

Track fix categories in a table:

| Category | Tests | Fix Nature | Pre-existing | Cycles Verified |
|----------|-------|-----------|-------------|-----------------|
| Tirith autouse fixture | ~95 | Platform mocking | 0 | N |
| Approval pipeline | ~94 (post-prune Aug 2026) | Path-separator skip; `shlex.split(posix=)`; `rm ~/` pattern | 1 interrupt-timing (Windows) | N |
| USERPROFILE monkeypatch | ~19 | `setenv` in conftest | 0 | N |
| ACP CRLF normalization | ~312 | CRLF `\\r\\n→\\n` in decode | 1 suite-level flake | N |

Use `~` for test counts since upstream can add/remove tests between cycles without changing the fix category.

**Zero regressions** is the target state. Any new failure not in the pre-existing set is a 🔴 regression requiring immediate investigation.

## Phase 6: Divergence Tracking

```bash
# Ahead/behind counts
git rev-list --left-right --count HEAD...origin/main

# Recent commits
git log --oneline -5

# File overlap risk (must be 0 for low-risk rebase)
git diff --stat HEAD...origin/main -- <fix-paths> 2>/dev/null

# Merge conflict prediction
git merge-tree HEAD origin/main 2>/dev/null | grep -c "^+<<<<<<<"
```

Severity scale (from 52+ cycles of observation):
- **0-50 behind**: 🟢 low risk, rebase when convenient
- **50-200**: 🟡 moderate, schedule within 3 cycles
- **200-500**: 🟡 attention, plan rebase
- **500+**: 🔴 critical rebase gap — but file overlap with fix paths may still be 0

### Divergence Rate Tracking

Beyond absolute count, track the **rate of divergence growth** between cycles. A jump from +139 per cycle to +443 in 2 days signals an upstream burst. Note the delta in the report:

```
Divergence: X ahead, Y behind (+delta since last cycle)
```

Rate acceleration is actionable even when file overlap is 0 — it affects rebase complexity and eventually forces a window for resolution.

## Phase 7: Working Tree Audit

```bash
git status --short
git stash list
```

Document:
- Modified tracked files (should be 0 for clean)
- Untracked artifacts (`.coverage`, `.playwright-mcp/`, temp files — harmless unless they accumulate)
- Stale stash entries (drop when flagged for 10+ cycles)
- **Gateway liveness:** `tasklist | grep -i pythonw` — a running `pythonw.exe` with a ~500MB working set means the Hermes gateway is up. Record up/down in the pulse entry; the fleet lane owns MCP-unlock decisions from this signal (restart scheduling), so a down gateway is worth flagging even when tests are green.

## Phase 8: Pulse Log Append

Append structured entry to `PULSE.md`:

```markdown
## Pulse @ YYYY-MM-DD HH:MM UTC (Nth Cycle — Brief Title)

- **Status**: 🟢 Nominal / 🟡 Attention / 🔴 Issue
- **Focus**: [what you investigated]
- **Findings**:
  - ✅ Suite: count/expected (timing)
  - ✅ Suite: count/expected — [note test-count drift if any]
  - 🟡 New pre-existing flake variant: test fails in suite, passes in isolation
  - 🟡/🔴 New regressions (if any)
  - 🟢 Divergence: X ahead, Y behind (+delta since last pulse)
  - 🟢/🔴 Working tree: CLEAN / N modified / N stash
- **Next Action**: [one concrete thing]
```

Append with `cat >>` or targeting the last line. Never use `write_file` on a file read partially.

## Phase 9: Report Delivery

Format using `discord-report-format` conventions:

```text
**🔵 SENTRY PULSE** | Mon Jul 24 · 8:57 AM ET

━━━━━━━━━━━━━━━━━━━━━━━━━━

**📊 RECAP** — all fix suites clean
- ✅ Tirith 95/95 (2.31s) — 52 cycles verified
- ✅ ContextRefs 17/17 — USERPROFILE holding
- ✅ Sandbox mirror 13/13 — as_posix() fix holding
- ✅ Approval 312/312 — symlink fix confirmed, no regression

**⏳ PENDING**
- 1 pre-existing Windows interrupt timing flake (test_approved_command_clean_slate)
- Divergence: 10 ahead, 1164 behind origin/main (+139 since last)

**🎯 RECOMMENDED ACTIONS**
- Push access or upstream PR merge to break 52-cycle fix-loss pattern
- Schedule Hermes restart to unlock locked MCP servers

━━━━━━━━━━━━━━━━━━━━━━━━━━

**🔍 Checked:** Jul 24 · 12:57 PM UTC
```

## Pitfalls

- **Don't hardcode test paths.** Upstream moves them without warning. Always `find` first.
- **Don't run the full test collection.** 40K+ tests wastes time. Targeted suites only.
- **Don't flag pre-existing failures as new regressions.** Track them across cycles and note "unchanged" each time.
- **Don't assume static test counts.** Upstream adds/removes tests in fix-category suites — note drift, don't hardcode expected counts.
- **Don't flag a suite-level isolation flake as a regression.** If it passes in isolation, it's a test-ordering issue, not a code defect.
- **Don't use `write_file` to append PULSE.md** after a partial read — truncates the file. Use targeting the last line or `cat >>`.
- **Don't run during quiet hours (00-06 ET).** Output `[SILENT]` immediately.
- **Don't omit divergence tracking.** It's essential context for whether failures are local or upstream-introduced.
- **Don't report "no activity" without checking the working tree.** Uncommitted changes are common and represent real activity.
- **Don't treat push-blocked as a new discovery each cycle.** After 10+ cycles, it's a standing condition noted in the status line, not a fresh finding.
- **Don't treat divergence rate acceleration as a new alarm each cycle.** When it accelerates sharply (+443 in 2 days), flag it once and then track it as a standing condition.
- **Don't call `append-digest.py` without verifying it exists.** The script lives at `_project/scripts/append-digest.py` and may be absent if that repo isn't cloned. Always check existence before calling: `test -f path/to/append-digest.py || echo "not found"`. If absent, skip the digest cross-post silently.
- **Call `append-digest.py` (or any native EXE) with a Windows-native path.** MSYS paths are NOT translated for native `python.exe`: `python ${MY_REPOS}/.../append-digest.py` fails with `can't open file 'E:\e\yourdata\...'` — the `/e/` prefix resolves against the shell's **current drive** (E: when the shell's cwd is on E:, C: when on C:), producing `<current-drive>:\e\...` with a doubled letter. The mangled drive letter varies, so a `C:\e\` signature from one session doesn't rule out `E:\e\` in another. Use `python "${MY_REPOS}/Documents/github/_project/scripts/append-digest.py"` — forward-slash native paths resolve fine.
- **Don't read `append-digest.py`'s `[SILENT]` output as your delivery order.** The script gates its own digest delivery on the **UTC** hour (00-06 UTC) and prints `[SILENT]` / "Quiet hours — saved to digest only" when tripped — but it STILL appends the digest (confirm with `[Digest] Appended to <file>.md` in its output). Your report delivery decision comes from your own Phase 1 EST gate, never the script's stdout. A 22:00 ET run (= 02:00 UTC next day) trips the script's gate while you're in full delivery hours — deliver the report anyway; the digest append is still fine.
- **Root-cause sharp pass-count drops before reporting them.** If the combined suite returns far fewer tests than the documented baseline (e.g. 158 vs 399), do NOT assume coverage loss or a regression. Decompose: `python -m pytest <each path> --collect-only -q | tail -2` per suite, and check the test file's history (`git log --oneline -- <test-file>`) for upstream test-prune waves (commit messages like "test: prune wave N — 28,106 → 19,757 test functions"). A reset-recovered HEAD can legitimately carry a smaller test set than pre-reset baselines — count delta ≠ coverage loss ≠ regression. Grep for the critical regression test names (e.g. `test_symlinked_temp_dir_only_exempts_canonical_target`) to confirm they survived, then lock the new baseline in PULSE.md so future cycles don't re-investigate it.
- **`git -C <msys-absolute-path>` (e.g. `/c/Users/...`, `${MY_REPOS}/...`) silently fails on git-bash** with `fatal: not a git repository` even when the repo exists — MSYS absolute paths aren't translated for `git -C`. In an `&&` chain the exit-128 failure silently skips every downstream command (a digest-script existence check was skipped this way, Aug 2026). Fix: `cd` into the repo first and use relative paths (`git log ...`). When a chain's output looks incomplete, verify each stage separately rather than trusting the tail.

## Pre-Existing Windows Failure Patterns (Cosmetic)

These are OS-level behavior differences, not code defects. Common examples:
- Windows process interrupt timing race — `test_approved_command_genuine_interrupt_after_start_still_kills` fails because the signal lands before the child process finishes setting up its handler. **This flake can spontaneously resolve** when test ordering shifts — it depends on CPU scheduler behavior, not code changes. Track disappearance as normal variance, not a fixed bug.
- Windows `IocpProactor` pipe handle behavior in asyncio — `test_bare_ping_request_produces_proper_response_and_no_stderr_noise` in `tests/acp/test_ping_suppression.py` consistently 1/9 fails with `OSError: [WinError 6]` on the IOCP proactor. Candidate for `pytest.mark.skipif(sys.platform == "win32")`.
- Bash cold-start timeout (shell spawning overhead on Windows CI)
- File permission mask (`mode==0o600`) assertion semantics differ on Windows
- Suite-level isolation flakes where tests that pass solo fail when run in collection order (ACP `ProactorEventLoop`, `test_result_passed_to_build_tool_complete`)

### Flake Evolution Tracking

A pre-existing flake that disappears and is replaced by a different flake in the same cycle is **flake evolution** — not a regression. This is normal on Windows where timing, scheduler, and test-ordering variance shift which test lands in the race window. Track the change in your pulse log:

```
🟡 Flake evolution: interrupt-kill flake (pre-existing) disappeared;
    ACP ping suppression now the sole remaining Windows flake (1/9 fails, IOCP proactor race)
```

Do NOT flag the disappearance as a "fix" or the new flake as a "new regression" unless the new failure is structurally different (e.g., assertion failure vs OSError). Same error class = same root cause, different test unlucky.

## Related Skills

- `discord-report-format` — Discord formatting rules for delivery
- `qa-pulse` — broader QA pulse checks (complementary: wider scope vs targeted fix verification)
- `recurring-status-checks` — stakeholder-focused status checks
