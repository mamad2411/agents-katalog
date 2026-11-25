---
name: read-logs
description: Read the running Flutter app's latest run logs as context for a task — an auth flow, a crash, a race, "why did X happen at runtime". Use when the user invokes `/read-logs`, asks why the app behaved a certain way during a run, or wants the most recent run's logs as evidence. Reads the log; first-run setup edits only local editor config and never commits.
argument-hint: "[what to look for in the run logs]"
---

# Read run logs

> **⚠️ Reading a run sends its contents to the model — that *is* the leak, and it's how
> this skill works.** Run logs routinely contain auth/refresh/push tokens, emails, and
> customer data; the moment you read one, that data is sent to the model. Invoking
> `/read-logs` means **consciously accepting** that this captured run gets sent. Don't run
> it against production or real-customer data unless you've accepted that risk. (Redaction is
> not built yet; see the plugin README for the full data-handling note.)

Load the running app's `flutter run` output as context for the task the user gave when
invoking this skill. Editor setup (making the app write the log file) is documented in this
plugin's `README.md` — that is canonical. The **First-run setup** section below intentionally
repeats those steps inline because this skill applies them at runtime, when the dev is in
their editor and not reading GitHub. Keep the two in sync.

Logs are captured per-project to `/tmp/flutter-<repo>.log` (`<repo>` derived from the shared
`.git` via `--git-common-dir`, so the main checkout and every git worktree resolve to the
*same* file), overwritten on every launch (always the latest debug session; with VS Code or
Cursor that includes a test run started from the editor), living in `/tmp` —
outside the repo, nothing to gitignore. Two capture formats exist depending on editor; the
skill auto-detects which:
- **Zed / terminal run task:** raw `script` TTY transcript (plain text, ANSI codes).
- **VS Code / Cursor (`dart.dapLogFile`):** Debug Adapter Protocol log (JSON-framed; the
  app's output is inside `event:"output"` messages).

**This skill loads logs as CONTEXT — it is not a standalone analyzer.** Don't summarize the
run, surface all errors, or volunteer a diagnosis on your own. Read the logs so you have
them, then carry out the task you were invoked with (e.g. "why did login flash", "does auth
reach the API"). If no task was given, confirm the logs are loaded and ask what they want —
don't analyze unprompted.

---

## Step 1 — Resolve the path and check it exists (Bash)

```bash
# Worktree-stable name: derive from the shared .git so the main checkout and all its
# worktrees resolve to ONE file. (--git-common-dir is relative from the main repo and
# absolute from a worktree, so cd into it and resolve before taking the repo dir name.)
CDIR=$(git rev-parse --git-common-dir 2>/dev/null)
if [ -n "$CDIR" ]; then REPO=$(basename "$(dirname "$(cd "$CDIR" && pwd -P)")"); else REPO=$(basename "$(pwd)"); fi
L="/tmp/flutter-$REPO.log"
echo "$L"
if [ ! -f "$L" ]; then
  echo "MISSING"
else
  echo "exists — $(wc -l < "$L") lines"
  # Freshness: how old is the run, and did code change since?
  MT=$(stat -f %m "$L" 2>/dev/null || stat -c %Y "$L" 2>/dev/null)
  if [ -n "$MT" ]; then
    AGE_MIN=$(( ($(date +%s) - MT) / 60 ))
    echo "captured $(stat -f '%Sm' "$L" 2>/dev/null || stat -c '%y' "$L" 2>/dev/null) (${AGE_MIN} min ago)"
    [ "$AGE_MIN" -gt 15 ] && echo "⚠️ this run is ${AGE_MIN} min old"
  fi
  if [ -d lib ] && [ -n "$(find lib -name '*.dart' -newer "$L" 2>/dev/null | head -1)" ]; then
    echo "⚠️ Dart files in lib/ changed AFTER this run — the log predates your current code"
  fi
fi
```

- **Exists** → go to Step 2 (note any freshness ⚠️ for Step 3).
- **MISSING** → do NOT just report missing. Go to the **First-run setup** section.

## Step 2 — Read the run (format-aware, task-led)

The file holds **only the most recent run** (it's overwritten on every launch), so there
are no older runs to scroll past and no need for a flat tail. With VS Code or Cursor, every
Dart-Code debug session overwrites it, tests included: if the log shows a test run instead of
the app, say so and ask the dev to relaunch the app. First normalize it to plain
text, then read it with the **task as your lens** — not a fixed filter.

**Normalize** (sniff the first lines for format) into a clean temp file you can page through:

```bash
CLEAN="${L%.log}.clean.log"
if head -50 "$L" | grep -qE '\[DAP\]|"event"[[:space:]]*:[[:space:]]*"output"'; then
  echo "[format: DAP — extracting app output]"
  # grep first: only the output-event lines reach the JSON parser, not the whole protocol —
  # so extraction cost tracks app output, not total DAP traffic. -E (not \|) for portable
  # alternation; [[:space:]]* tolerates non-compact JSON.
  grep -E '"event"[[:space:]]*:[[:space:]]*"output"' "$L" | python3 -c '
import json, sys
import re
OUT = re.compile(r"\"output\"\s*:\s*\"((?:[^\"\\]|\\.)*)")
for line in sys.stdin:
    i = line.find("{")
    if i < 0: continue
    try: m = json.loads(line[i:])
    except Exception:
        # Dart-Code cuts lines longer than dart.maxLogLineLength and appends "…", which
        # breaks the JSON. Keep the part of the output that survived and mark the cut.
        g = OUT.search(line.rstrip("\n"))
        if g:
            try: s = json.loads("\"" + g.group(1) + "\"")
            except Exception: s = g.group(1)
            sys.stdout.write(s + " [truncated: raise dart.maxLogLineLength]\n")
        continue
    if m.get("event") == "output":
        sys.stdout.write(m.get("body", {}).get("output", ""))
' > "$CLEAN" 2>/dev/null
  # jq fallback if python3 is unavailable:
  # grep -E '"event"[[:space:]]*:[[:space:]]*"output"' "$L" | sed -E 's/^[^{]*//' | jq -rj 'select(.event=="output") | .body.output' > "$CLEAN"
else
  echo "[format: plain transcript]"
  sed -E $'s/\x1b\\[[0-9;?]*[ -\\/]*[@-~]//g; s/\r$//' "$L" > "$CLEAN"
fi
wc -l "$CLEAN"
```

(If a DAP log can't be extracted because neither `python3` nor `jq` is present: `python3`
ships on most systems; otherwise install `jq` via the platform's package manager —
`brew install jq` on macOS, `apt install jq` / `dnf install jq` on Linux. Until then, fall
back to reading matching raw lines so the user isn't blocked.)

**Transparency:** before reading, surface one line to the dev — *"reading `<path>` — its
contents go to the model"* — so each read is a visible, conscious step (no blocking prompt).

**Then read `$CLEAN` with the task as the lens — go as deep as the task needs:**

- **Small run (roughly ≤ 600 lines):** read the **whole** file (`Read` it / `cat`). It's one
  run; the full thing is the cleanest context. No filtering.
- **Large run** (long session, many hot reloads): **don't dump it.** Investigate against the
  task — `grep` the cleaned text for what it's actually about, read those windows (`Read`
  with offset/limit, or `grep -B/-A`), and **iterate deeper** (widen context, follow the
  thread, read more) until you can answer. The lens comes from the task:
  - crash / "doesn't work" → error markers: `^E/flutter`, `[SEVERE]`, `Exception:`,
    `^#[0-9]+ ` (stack frames), `═══`, build failures (`FAILURE:`, `BUILD FAILED`,
    `Error (Xcode`, `lib/...: Error`).
  - race / ordering / timing → trace the relevant cubits/events/timestamps **in sequence**;
    error markers are irrelevant here.
  - a specific feature/screen → grep its names and read around them.

  Errors are just **one possible lens — never the only one.** Don't reduce every log read to
  error-hunting.

## Step 3 — Use as context

Carry out the task you were invoked with against the logs. No run summary or error report
unless the task asks for it.

If Step 1 flagged the run as stale — old, or (especially) Dart files changed after it was
captured — **and** the task is recency-sensitive ("does my fix work", "I just changed X"),
lead with that: tell the dev the log may not reflect their current code and suggest
re-running before you draw conclusions. It's a heads-up, not a refusal — if they clearly
want the existing run (e.g. investigating a past race), just proceed.

---

## First-run setup (log is MISSING)

Goal: leave the dev with their editor configured to capture logs, with no surprises. Never
guess silently and never commit anything. (The `README.md` is the canonical copy of these
steps; this inline version exists so setup works at runtime.)

**This is the conscious opt-in moment.** Before wiring anything up, make sure the dev
understands that enabling capture means Claude will read run logs into context — which
**sends them to the model** — and that runs can contain tokens and customer data. Get a
clear yes before applying the setup; if they prefer not to take that risk, don't wire it.

### 1. Determine which editor the dev runs the app in

Detection is a convenience to skip a question — never a hard dependency. In order:

```bash
echo "TERM_PROGRAM=$TERM_PROGRAM"   # vscode (also Cursor) | zed | iTerm.app | Apple_Terminal | tmux ...
test -d .zed && echo "has .zed"; test -d .vscode && echo "has .vscode"
```

- `$TERM_PROGRAM` clearly says **vscode** → VS Code/Cursor path. **zed** → Zed path.
- Inconclusive (plain terminal) → fall back to config dirs: only `.zed/` → Zed; only
  `.vscode/` → VS Code/Cursor.
- Still ambiguous (both dirs, or neither, and no host signal) → **ask** the dev which
  editor they launch the app in. Asking once here is fine — this is one-time setup.

Note: Cursor is a VS Code fork — it uses the same Dart-Code extension and reads
`.vscode/settings.json`, so it follows the VS Code path. A `.cursor/` dir is irrelevant to
logging.

### 2. Check whether logging is already wired (then decide)

The expected path is `L` from Step 1.

- **VS Code/Cursor** — Read `.vscode/settings.json`; logging is wired iff
  `"dart.dapLogFile"` equals `L`. (Legacy note: `dart.flutterRunLogFile` is **removed** in
  current Dart-Code — ignore it if present.)
- **Zed / terminal task** — Read `.zed/tasks.json` (or `.vscode/tasks.json` for a VS Code
  task runner); wired iff the `flutter run` tasks use `command: "script"` with `-q` `L`.

Then:
- **Already wired correctly** → setup is fine; the app just hasn't been launched since (or
  `/tmp` was cleared). Tell them to run the app, then re-run `/read-logs`.
- **Not wired** → explain what's missing and **offer to set it up** (next step). Don't edit
  until they agree.

### 3. Propose the fix (only after the dev agrees)

Pick by editor. For VS Code/Cursor, prefer `dapLogFile` (keeps the F5 / Run-and-Debug
workflow — it captures F5 **and** Ctrl+F5 debug sessions). Only use the `script` task
variant if they launch via a non-debug terminal task (then `dapLogFile` would stay empty).

**Before editing, check whether the target file is tracked — and warn if so:**

```bash
TARGET=.vscode/settings.json   # or .zed/tasks.json
git check-ignore -q "$TARGET" && echo "ignored (local-only — safe to edit)" || echo "TRACKED/committable — edit will show in git"
```

If TRACKED, tell the dev before applying: *"heads-up — `$TARGET` is tracked in this repo,
so this change will appear in `git status`. A `dapLogFile` line is a personal pref, and
wrapping committed run tasks in `script` changes the run command for the whole team —
commit it only if your team wants shared logging."* Then let them decide.

**VS Code / Cursor** — merge into `.vscode/settings.json` (never drop existing keys like
`dart.flutterSdkPath`); create the file with just these keys if absent:
```json
{
  "dart.dapLogFile": "<L>",
  "dart.maxLogLineLength": 1000000
}
```
(`maxLogLineLength` default is 2000 and truncates long lines — bump it so output/stack
traces aren't cut.) **Bake the resolved literal `<L>`** (the `--git-common-dir`-derived
path from Step 1) — do **not** use `dapLogFile`'s `${workspaceName}` variable: it expands to
the workspace folder, which differs per worktree and won't match the read derivation. Then:
reload the VS Code window, F5/Ctrl+F5 a run, re-run `/read-logs`.

  ⚠️ `dapLogFile` only captures **debug-adapter sessions** (F5 / Ctrl+F5), and app logs reach
  the editor only on **simulator / macOS / Android / the `chrome` device**. A `-d web-server`
  run sends app logs to the *browser's* console — the file will then hold build/launch
  output but no app logs. If a dev sees an empty/launch-only capture on web, that's why.

**Zed / terminal task** — wrap each `flutter run` task in `script`, **preserving its
existing flavor / target / dart-define args** (wrap what's there — don't invent args).
`script`'s syntax differs by OS, so detect it first: `uname -s`.
- **macOS (Darwin), BSD `script`:** set `command` to `"script"`, args become
  `["-q", "<L>", <existing command + its args>]` (logfile, then the command as trailing
  args). E.g. `["-q", "<L>", "flutter", "run", "-t", "lib/main.dart"]`.
- **Linux, GNU `script`:** the command goes through `-c` as a single string and the logfile
  is **last**: args become `["-q", "-c", "<existing command + args joined into one string>", "<L>"]`.
  E.g. `["-q", "-c", "flutter run -t lib/main.dart", "<L>"]`.
- **Windows:** there's no `script`; that dev should use the VS Code/Cursor `dapLogFile`
  path instead (it's cross-platform).

Then: launch the app once, re-run `/read-logs`.

If neither `.vscode/` nor `.zed/` exists and the dev's editor is unknown, ask which editor
they run the app in, then apply the matching setup above.
