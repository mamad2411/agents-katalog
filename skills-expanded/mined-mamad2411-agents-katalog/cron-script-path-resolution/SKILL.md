---
name: cron-script-path-resolution
description: >-
  Diagnose and fix "Script not found" failures in Hermes cron jobs. Covers how
  the jobs.json `script` field is resolved (bare-filename convention, the
  `scripts/scripts/` doubling bug), why last_status "ok" does not prove a script
  ran, and the fix-in-run workflow for recurring script failures.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cron, jobs.json, scripts, path-resolution, config, diagnostics]
    triggers:
      - script not found
      - scripts/scripts
      - cron script path
      - daily_brief.py not found
      - council_checkin.py not found
      - cron job script error
      - fix cron script
      - jobs.json script field
      - can't open file
      - MSYS path
      - append-digest.py
    related_skills:
      - cron-watchdog
      - recurring-status-checks
      - council-checkin-reconstruction
---

# Cron Script Path Resolution

Diagnose and fix Hermes cron jobs that fail with **"Script not found"**. The
canonical failure is a doubled path: `scripts\scripts\daily_brief.py`.

## How the `script` field resolves

The cron runner resolves each job's `script` value relative to the **scripts
base dir** (`~/AppData/Local/hermes/scripts/`), NOT the job's `workdir`.

- A value like `"script": "scripts/daily_brief.py"` is joined as-is →
  `scripts\scripts\daily_brief.py` → **"Script not found:
  C:\Users\<user>\AppData\Local\hermes\scripts\scripts\daily_brief.py"**.
- The convention across a healthy job store is a **bare filename**:
  `"script": "cron-guardian.py"`, `"script": "buzz_watchdog.py"`.
- The job's `workdir` (e.g. `E:\...\_project`) is NOT searched. A script
  that only exists in the workdir repo (e.g. `_project/scripts/foo.py`)
  must be **copied into `~/AppData/Local/hermes/scripts/`** for the runner to
  find it.

## Why it's silent

`last_status: "ok"` does NOT mean the script executed. Script-not-found is
non-fatal: the runner embeds the error in the cron prompt and the LLM still
produces output, so the job "succeeds" while the data script never runs. A
"Script Error" block at the top of the prompt is the tell — treat it as a
config bug to fix, not a data-collection outcome.

## Diagnosis

1. Read the job record in `~/AppData/Local/hermes/cron/jobs.json` (search by
   job name, e.g. `daily-command-brief`). Check the `script` value for a
   `scripts/` prefix.
2. Confirm whether the nested dir actually exists:
   `ls -d ~/AppData/Local/hermes/scripts/scripts` — if missing, the prefix is
   the bug, not a real nesting.
3. Locate the real script: `find ~/AppData/Local/hermes -maxdepth 3 -name "<name>.py"`
   and check the workdir repo (`<workdir>/scripts/<name>.py`).

## Fix (in-run, don't re-flag)

1. Ensure the script exists in `~/AppData/Local/hermes/scripts/` (copy it from
   the workdir repo if that's where it lives).
2. Patch `~/AppData/Local/hermes/cron/jobs.json`:
   `"script": "scripts/<name>.py"` → `"script": "<name>.py"`.
   Use the `patch` tool — single-value edits are safe (JSON lint validates;
   `jobs.json.bak.*` backups exist). Both values must be unique matches.
3. Run the script manually with the correct path to verify it works and
   produces real output (not template stubs with `{{placeholders}}`).
4. If the job also needs the script's artifact (e.g. a dated report file),
   generate it during the same run and archive it.

## Verification

- The script executes and its artifact (output file) exists with real data.
- `jobs.json` still parses as valid JSON.
- Check sibling jobs for the same defect — the `scripts/` prefix bug hit two
  jobs at once (`daily-command-brief`, `weekly-council-checkin`); audit all
  `script` values in the store: `grep -o '"script": "[^"]*"' jobs.json`.

## Create-side constraint (cronjob tool rejects absolute paths)

When creating a job with `cronjob action=create ... script=<path>`, the tool
REJECTS absolute and home-relative paths outright:

```
Error: Script path must be relative to ~/.hermes/scripts/. Got absolute or
home-relative path: 'E:\\...\\ops\\billing\\billing_daily.py'. Place scripts
in ~/.hermes/scripts/ and use just the filename.
```

So the `script` field must ALWAYS be a bare filename that exists in
`~/AppData/Local/hermes/scripts/` — same resolution rule as jobs.json, but
enforced at creation time (no silent failure possible here; it errors).

**Wrapper pattern for repo-owned scripts:** don't copy the repo script into
the scripts dir (it computes paths from `__file__` and would break). Instead
drop a thin wrapper in `~/AppData/Local/hermes/scripts/` that
`subprocess.run([sys.executable, "<repo-abs-path>"], cwd="<repo>", ...)`
with a timeout, prints the child's stdout, and exits non-zero on child
failure. Give the child a repo-absolute Windows path (`E:/...` form — see the
MSYS pitfall below). Verify the wrapper manually once before creating the job:
`python ~/AppData/Local/hermes/scripts/<wrapper>.py` — silent (no stdout) for
watchdog jobs is the correct healthy state, not a failure.

## MSYS paths break native Windows Python invocations

A sibling path-resolution failure: passing an MSYS-style path to a **native Windows executable** from git-bash. `python ${MY_REPOS}/.../script.py` fails with `can't open file 'E:\e\yourdata\...'` — the mangled path keeps the `/e` segment but resolves it relative to a drive root (observed `C:\e\...` in one context, `E:\e\...` in another — the leading drive letter varies, so don't match on it). Bash builtins (`ls`, `cd`, `cat`) understand MSYS paths; native Windows exes (`python.exe`, `node.exe`) do not.

**Fix:** pass a Windows drive-letter path with forward slashes — Python accepts both `${MY_REPOS}/...` and `E:\\yourdata\\...`:

```bash
# ❌ fails — native python.exe sees a mangled drive-root path (e.g. E:\e\yourdata\...)
python ${MY_REPOS}/_project/scripts/append-digest.py "Pulse" "- finding"

# ✅ works — drive-letter form with forward slashes
python "${MY_REPOS}/Documents/github/_project/scripts/append-digest.py" "Pulse" "- finding"
```

The exit code is 0 even on this failure (the shell reports success) — always verify the script's own output (`[Digest] Appended to ...`) rather than trusting the exit code. This bites cron/pulse jobs where the job prompt hard-codes the MSYS form of a repo path.

## IANA TZ names silently return GMT on git-bash — use the POSIX DST-rule format

**When a cron/pulse prompt runs `TZ='America/New_York' date +%H` (any IANA zone name) on Windows git-bash, the zone is silently ignored** — the MSYS runtime lacks the IANA zoneinfo database, so `date` falls back to GMT/UTC with no error and exit code 0. This silently breaks quiet-hours gates (always reports the wrong hour). `%Z` shows `GMT`/`UTC` regardless of the zone specified.

**The verified fix — full POSIX TZ string with DST transition rules (works on git-bash, no tzdata, no PowerShell):**

```bash
# Eastern Time, DST-aware: EDT=UTC-4 from 2nd Sun Mar, EST=UTC-5 from 1st Sun Nov
TZ='EST5EDT,M3.2.0/2,M11.1.0/2' date +%H
# → returned 05 at 09:24 UTC (correct EDT) — verified Aug 7 2026, matches the dev-lead-pulse cron prompt
```

The `M3.2.0/2,M11.1.0/2` suffix encodes the US DST transitions (month.week.day/hour), so the offset tracks DST automatically — unlike the bare `TZ='UTC-4'` form, which is only correct half the year. This is the format to use in cron prompts for quiet-hours/time-gate checks on Windows.

**Validation:** always print `%Z` (`date +"%H %Z"`) to confirm the zone resolved (`EDT`/`EST`, never `GMT`). For zones outside the US or unusual DST rules, the PowerShell fallback is the safe answer:
```bash
powershell.exe -Command "[TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow, 'Eastern Standard Time').ToString('HH')"
```

## Which interpreter runs a no-agent cron script (ModuleNotFoundError diagnosis)

When a scheduled `no-agent` cron job fails with `ModuleNotFoundError: No
module named '<pkg>'`, the runner does NOT use the venv or system python —
it executes the script under the **bundled `.hermes-runtime` cpython**
interpreter bundled inside the Hermes install. That interpreter has its own
isolated `site-packages`, separate from both the hermes venv and `python311`.

**How the script-path-only job map works:** jobs.json records only
`"script": "<name>.py"` (plus `mode: no-agent`, `python: null`). Hermes
itself resolves the interpreter, so you CANNOT tell from the job record
which python runs it — you must discover the runtime path (see below).

**Discover the runtime interpreter (and check a dep):**
```bash
# This is the cpython bundled under hermes-agent — the cron runner's interpreter.
RT=$(ls -d ${HERMES_HOME}/hermes-agent/.hermes-runtime/python/generation-*/*/python.exe | head -1)
"$RT" -c "import sys; print(sys.executable)"
"$RT" -c "import pandas; print(pandas.__version__)"   # check the missing pkg HERE, not in the venv
```

**Verify by running the failing script directly with that interpreter:**
```bash
cd ${HERMES_HOME}/scripts && timeout 120 "$RT" -u <name>.py
```
A clean run (`EXIT=0`, real output) confirms the fix even before the next
scheduled run.

**Install a missing dep for a cron script — target the runtime python, not
the venv/system:**
```bash
"$RT" -m pip install pandas
# NOT  uv pip install --python <venv>  → wrong interpreter; and NOT system pip → won't be seen by the runner
```
GOTCHA: `uv pip install --python /path/to/venv/Scripts/python.exe` can fail
with `No virtual environment ... found for path` even when that venv
imports the package fine — `uv` doesn't always recognize the bundled
`.hermes-runtime` tree as a venv. Use the interpreter's own `-m pip`
instead.

**Check both before declaring RED:** `import` success in the hermes venv
does NOT imply the cron script imports — the runtime interpreter is a
different site-packages. Conversely, if deps are present in the runtime
interpreter but the job error is dated, it may already be fixed by a
recovery pass (re-verify the script live before reporting). See
`references/runtime-interpreter-deps.md` for the worked example.

## Escalation context

If the same broken path has been re-flagged across consecutive reports (Jul 27
→ Jul 31 → Aug 2 in the Aug 2026 case), each re-flag costs a cycle — apply the
fix during the run that detects it. Related escalation rules live in
`recurring-status-checks` (Phase 4) and `council-checkin-reconstruction`
(root-cause check); cron job health monitoring lives in `cron-watchdog` (all
three are sibling skills — the last two are agent-editable, `cron-watchdog` is
protected).
