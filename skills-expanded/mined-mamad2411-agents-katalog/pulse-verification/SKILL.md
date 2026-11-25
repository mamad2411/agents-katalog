---
name: pulse-verification
description: Verify claims in pulse/recurring scans before reporting — check every lookup path, verify mechanisms end-to-end, audit config-toggling scripts. Prevents false-negative verdicts that poison follow-up actions.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pulse, verification, audit, false-negative, feature-check, config-toggle, recurring-scan]
    triggers: [verify feature, is it missing, script missing, feature broken, audit script, config toggle, pulse finding, verify before reporting, verdict correction]
    related_skills: [discord-report-format, recurring-status-checks, windows-cross-platform-debugging]
---

# pulse-verification

Verify findings in pulse/recurring scans BEFORE reporting them. A wrong "missing / broken / non-functional" verdict in one pulse poisons the Next-Action chain for every later pulse — they inherit the bad recommendation and act on it.

## Core Rule

**Never report a negative ("missing", "broken", "no commits", "non-functional") until you have checked every place the thing could be.** A negative from a partial check is not a finding — it's a guess. This is the same principle as the dynamic-git-scan rule ("don't trust a commit-only scan that returns empty") extended to feature/file claims. **Zero counts from inventory/gap-analysis scripts ("0 active cron jobs", "no gaps", "no issues") are negatives too — verify against the live system (scheduler, filesystem, live config) before reporting them.**

## Baseline Count Shifts Are Claims, Not Regressions

A recurring pulse that tracks test-pass totals will eventually see the number change (399→158, 158→138...). **Do NOT report a regression until you verify collection scope** — a count drop with everything passing is usually a collection change, not broken code.

**Worked example (2026-08-05 Sentry pulse):** combined baseline read 138 passed vs 158 the prior cycle — looked like 20 tests silently vanished. Per-suite breakdown (`pytest <dir> -q` for each member) showed approval 94 + hermes_state 42 matching baseline exactly; the drop was entirely `tests/scripts/` — the pulse had run the single file `test_build_skills_index_health.py` (2 tests) instead of the whole `tests/scripts/` directory (22 tests). Path error, zero regressions. The count shift was my own artifact.

**Verification pattern before reporting any count change:**
1. Run `pytest <suite-dir> --collect-only -q 2>&1 | tail -2` per suite member and compare each member's collection count against the prior baseline composition (the PULSE.md entry usually lists it).
2. Run each suite dir, sum, and compare to the baseline total.
3. If a single member changed, check the dir-vs-file distinction first, then upstream prunes / param changes / env-dependent skips.

Common causes of count shifts, in order of likelihood: collection path error (file vs dir), upstream test-prune wave, new tests added elsewhere, parametrization changes. All are findings worth one line — none are regressions until a test actually fails.

## Repo Divergence in Repo-Health Pulses

When a pulse scans a repo where local fixes are committed but **unpushed** (common after reset-recovery work), check divergence explicitly each cycle:

```bash
git rev-parse HEAD origin/main          # differ? → diverged
git log HEAD..origin/main --oneline | head -20   # upstream commits not merged
git log origin/main..HEAD --oneline | head -20   # local commits not pushed
```

If local `main` is ahead with a committed fix group AND the repo has a reset-damage history (`git reset --hard origin/main` wiping local work), **create a local backup branch immediately** — it costs nothing and turns a future reset from a reflog-recovery scramble into a one-command restore:

```bash
git branch qa-lead/fix-baseline-<date> HEAD
```

Check for an existing backup branch first (`git branch --list`) — if the same commit is already captured elsewhere, the new branch is redundant. Note in the pulse entry that the fixes are unpushed and exposed, so the next agent treats merge/push as priority.

## Pitfall: Cron prompt commands carry MSYS paths that native Python can't resolve

Pulse cron prompts often bake in digest/append commands verbatim, e.g. `python ${MY_REPOS}/.../append-digest.py`. Native Windows Python reads `/e/...` literally → `can't open file 'C:\e\...'`. Rewrite the path to `E:/...` (or `E:\...`) before running. The full diagnosis lives in `windows-cron-msys-path-fix` (user-owned — may need `hermes curator adopt`).

## Verification Methodology (any feature/completeness claim)

1. **Enumerate every lookup path in the code's own fallback chain.** Read the handler/loader source; list all candidate paths; check them ALL. Concluding "missing" from one location is the classic false negative — the deployed copy often lives in `HERMES_HOME/scripts/` or another path, not the repo-relative one.
2. **Verify the mechanism end-to-end, not just file existence.** A script existing ≠ the config keys it writes are read at runtime. Grep the runtime (`gateway/`, `agent/`, `hermes_cli/`) for the keys the script writes.
3. **Check live state.** Grep the live config for the toggled keys — the feature may be enabled RIGHT NOW; that is a finding in itself.
4. **Correct the record explicitly.** When evidence contradicts a prior pulse entry, say so in the new entry with the corrected verdict and why — later pulses must not compound the error.
5. **Watchdog/monitor output is a claim, not data.** A monitor reporting N failures is the first word, never the verdict. Triage before reporting: (a) streak age — grep the log for the first occurrence; a streak predating today is a pre-existing false positive, not a new incident; (b) reproduce the exact failing check manually — exit 0 + real output means the monitor's own wrapper is broken (e.g. JSON parse choking on compose warning lines), not the service; (c) verify actual state independently (`docker compose ps`, `docker ps -a`) — healthy containers beat a monitor's "missing service" claim; (d) check the ALERT-DELIVERY channel itself — a watchdog whose notification path is dead (SMTP "Authentication required") sends nothing on real failures. The dead alert channel is usually the true actionable incident hiding under the false positive. Worked example: `references/watchdog-alert-triage.md`.

## Lookup-Path False Negatives (grep)

- **Case-sensitive grep on capitalized headers.** Digest/pulse headers are capitalized (`## [16:15 EST] Weaver Pulse`) — `grep -E "dev-lead|qa-lead|integration-lead"` silently returns ZERO matches even when entries exist. Use `grep -iE`. When any grep that should match returns empty, read the file tail directly before concluding "no findings" — an empty result is a hypothesis, not a verdict.

## Commit-Window False Negatives (`git log --since` local-time resolution)

`git log --since="YYYY-MM-DD HH:MM"` resolves the bare timestamp in **local time, not UTC**. Pulse logs (PULSE.md, digests) timestamp in UTC; on a DST-observing machine (EDT in summer), the filter silently returns ZERO commits for work committed inside your window — the UTC times land "before" the local-time cutoff.

**Worked example (2026-08-10 Scribe pulse):** last pulse logged at `19:15 UTC`; `git log --since="2026-08-10 19:15"` returned nothing while `git log --oneline -5` clearly showed 4 commits above the last pulse's commit (feeb3ee @ 19:17 UTC, 969751d @ 19:20, 90cee4c @ 19:54, 2633923 @ 20:36). The EDT host read the cutoff as 19:15 local (= 23:15 UTC), so all four UTC times fell "before" it. The commits were only caught because graph order was cross-checked against the known last commit.

**Fix:** append an explicit offset — `--since="2026-08-10 19:15 UTC"` or `--since="2026-08-10 19:15:00 +0000"` — or compute the cutoff with `date -u`. Never trust a "zero new commits" result: cross-check against `git log --oneline -5` ordering vs the last known commit (graph order is authoritative regardless of clock/timezone interpretation). Applies to every scan that uses `git log --since="<last report date>"`.

## Worked Example (2026-08-01 godmode false negative)

A pulse reported `/godmode` "non-functional — `scripts/godmode_toggle.py` is MISSING" after checking only the repo `scripts/` dir (one of three lookup paths). The script actually lived at `HERMES_HOME/scripts/godmode_toggle.py` — the FIRST of the handler's fallback paths — and the feature was LIVE (config.yaml already carried the GODMODE system_prompt and `prefill_messages_file`; the next session started with the prefill injected verbatim). Corrected verdict: "functional, 3 defects" instead of "incomplete, don't commit." Full detail + audit transcript: `references/pulse-verification-false-negatives.md`.

## Worked Example (2026-08-03 dream-cycle "0 cron jobs" false zero)

The Hermes Dream Cycle inventory script reported **"Cron Jobs: 0 active"** and **"No critical gaps detected"** — both verdicts wrong. Verification against the live scheduler (`hermes cron list`) and `~/AppData/Local/hermes/cron/jobs.json` showed **62 enabled jobs** (95 total, 30 disabled, 3 paused), **10 in error state** — including 5+ jobs silently blocked by the config-drift spend guard (see `cron-watchdog` / `hermes-operational-audit`) and one enabled job with no `next_run_at` (scheduled but never fires). The script's cron probe reads the wrong store; its gap analysis is invalid until fixed.

**Lesson:** An inventory/gap-analysis script's aggregate verdict is a claim, not data. When a count or "no issues" verdict feeds a report, verify the mechanism (scheduler state, jobs.json, live config) before propagating it — and flag the broken probe explicitly so later pulses don't inherit the false zero.

## Config-Toggle Script Audit Checklist

Apply when auditing any script that flips config keys (feature toggles, mode switches):
- **Destructive disable?** Does `enable()` OVERWRITE a user-facing key (docstring may claim "append" while code replaces) and does `disable()` pop it with no backup of the prior value? Fix pattern: save prior value to a state file on enable, restore on disable.
- **Status false-positive?** Is `enabled` derived from presence of ANY value in a shared key (any system_prompt + any prefill.json = "ENABLED") instead of a dedicated state record? Key status off the state file / content match.
- **Windows path construction?** `Path(os.environ.get("APPDATA")) / "Local" / ...` is wrong — APPDATA resolves to `Roaming`, so the path becomes `Roaming\Local\hermes` (nonexistent). Use `LOCALAPPDATA` or prefer `HERMES_HOME`.
- **Atomic config write?** Full-file `yaml.safe_dump` rewrite with no temp+rename and no lock races against the running process (which may also write config on model switch). Prefer atomic replace + a lock.

## Grep Scoping on Large Repos

Full-tree `grep -rin <term> .` from the repo root can time out (observed 60s on hermes-agent). Scope to key dirs:
```bash
grep -rin "term" gateway/ hermes_cli/ agent/ scripts/ 2>/dev/null | grep -v ".pyc" | head -20
```

**Zero results from a scoped search are still a hypothesis on a 3k-file repo — cross-check with targeted grep on the specific files under audit before concluding a symbol is absent.** Observed 2026-08-10 (hermes-agent): `search_files` (ripgrep) returned 0 hits for `api_request_error` while the string exists in `run_agent.py`; a broad `grep -rn ... tests/ gateway/ run_agent.py` timed out at 30s; targeted `grep -c "api_request_error" run_agent.py gateway/run.py` found 3 hits immediately. When auditing a commit, grep the exact files the diff touched first — it is fast, unambiguous, and immune to scoping/globbing quirks. Treat any single-tool zero as "not yet found", never "absent".

## "New Item" Claims Are Claims Too (intel dedup)

The intel-scan mirror of the false-negative rule: **never surface an article/finding as NEW before checking a prior pulse didn't already report it.** A re-reported item is a false positive that doubles downstream attention on stale news.

1. **Bound the window by source timestamps.** `blogwatcher-cli blogs` prints per-feed `Last scanned` — if that timestamp equals the previous pulse's run time, no scan happened since, so nothing genuinely new can exist; the unread list is a stale subset of what the last pulse already saw.
2. **Dedupe against session history.** Before calling an item new, `session_search` on its distinctive title terms (e.g. `Bugtraq OR leverage OR Zigbee`) and check the previous pulse's own output for the same window. The prior pulse usually lists counts per source (e.g. "16 HN, 2 Ars") that subsume the current unread items.
3. **Timestamp trap:** `blogwatcher-cli articles --since` accepts only bare `YYYY-MM-DD` — `--since "2026-08-05 04:05"` fails with `invalid date format ... expected YYYY-MM-DD`. Retry with the date only, then dedupe.

**Worked example (2026-08-05 03:35 ET pulse):** blogwatcher showed 4 unread articles; 1 (Flowise shutdown) had already been reported by the 12:05 AM pulse; all `Last scanned` stamps were identical to the prior pulse's run; session_search on the other 3 titles showed no prior coverage but the scan window proved nothing newer existed. Verdict: nothing new in window → `[SILENT]`.

## Commit Claims Are Claims Too (positive-claim verification)

When a sibling agent's commit claims a fix (test hermeticity, restored feature, "now passes N/N"), verify before reporting it as landed — a wrong **positive** verdict is as poisonous as a false negative:

1. **Run the claimed test scope.** `pytest <file> -q` — confirm the pass count in the commit message (e.g. "55/55") rather than trusting it.
2. **Check the mock against the real interface.** A test fix that adds a mock must satisfy the real contract: the mocked method/attribute exists on the real class (`grep -n "def has_credentials" agent/...`), and every production call site consumes the mock the way it provides it (`grep -n "load_pool\|has_credentials" <module>`). A wrong-shaped mock can pass while exercising nothing.
3. **Confirm the mock forces the claimed path.** E.g. an empty-pool `load_pool` mock must return `has_credentials()=False` so the credential-pool short-circuit is skipped and the OAuth fallthrough block actually runs. If the mock only satisfies a truthiness check, the test passes without testing what the message claims.
4. **Signature-change commits: check what the tests assert before declaring the diff safe.** When a commit adds kwargs to a lifecycle hook / function call (e.g. `agent=self` to the `api_request_error` hook), find the tests referencing the symbol (`grep -rln "api_request_error" tests/`) and read their assertions: key-subset access (`hook_events[0]["error_type"]`) survives additive kwargs; exact dict/payload equality breaks. Worked example (2026-08-10): `d65359b43` added `agent=self` + rewrote provider-error strings — relay-metrics and run_agent tests assert specific keys only, so the additive kwarg was provably safe before the 195-test combined run confirmed it (2 expected skips).

**Worked example (2026-08-08 Forge pulse):** Sentry commit `a163743ad` claimed `test_qwen_oauth_auto_fallthrough_on_auth_failure` was now hermetic via an empty-pool `load_pool` mock. Verified end-to-end: 55/55 pass (3.93s); `CredentialPool.has_credentials()` exists (`agent/credential_pool.py:614`); call sites at `hermes_cli/runtime_provider.py:617-618` + `:1852-1855` both consume `has_credentials()` truthiness — empty pool → False → credential short-circuit skipped → OAuth fallthrough exercised. Reported as landed.

## Pitfall: Helper-script quiet-hours verdicts are claims, not the delivery gate

`append-digest.py` (and similar helper scripts) print a quiet-hours verdict (`[Digest] Quiet hours (00:00-06:59 EST) — saved to digest only. [SILENT]`) that can be **wrong**. Observed 2026-08-08 01:48 UTC: the script declared quiet hours while the job's own TZ check (`TZ='EST5EDT,M3.2.0/2,M11.1.0/2' date +%H` → 21) said 21:48 ET — waking hours — and the script still wrote the correct ET-dated digest file. The script's hour gate and its date resolution can disagree.

**Rule:** the cron job's own Eastern-Time check is authoritative for delivery — not the helper script's `[SILENT]` line. The script only tells you it saved-to-digest; it does not tell you whether to deliver. If your TZ check says waking hours, deliver the report even when the script prints `[SILENT]`.

## Related
- `discord-report-format` — pulse report formatting + PULSE.md append rules (the report this skill feeds)
- `recurring-status-checks` — stale-state reconstruction, escalation tracking for periodic reports
- `windows-cross-platform-debugging` — Windows path/env pitfalls (USERPROFILE, MSYS, APPDATA/LOCALAPPDATA)
