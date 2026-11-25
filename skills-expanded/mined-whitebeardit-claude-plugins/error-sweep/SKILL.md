---
name: error-sweep
description: List the errors of a time window - without a trace id - as a fixed, numbered table of facts from Grafana Tempo (spans with error status) and Grafana Loki (error lines grouped by a masked message signature), then let the user choose what to see - the sequence diagram of an example trace, or a full investigation with trace-debug. Use when the user asks whether there were errors in a period ("any errors in the last 2 hours?", "what failed in payment-service yesterday afternoon?", "sweep the logs for errors"). Deterministic - no model judges severity or cause. Read-only. The table is the answer - show it to the user exactly as printed, in full, without summarizing, reordering or commenting on it.
argument-hint: "[--last 2h | --start <t> --end <t>] [--service <name>] [--fixture <dir>]"
allowed-tools: Bash(python3 *sweep-errors.py*) Bash(python3 *collect-trace.py*) Bash(python3 *trace-diagram.py*) Bash(python3 *window-map.py*) Read Bash(python *sweep-errors.py*) Bash(py -3 *sweep-errors.py*) Bash(python *collect-trace.py*) Bash(py -3 *collect-trace.py*) Bash(python *trace-diagram.py*) Bash(py -3 *trace-diagram.py*) Bash(python *window-map.py*) Bash(py -3 *window-map.py*)
---

# Error sweep

Answer "were there errors in this period, where, how many, since when" with facts. A script builds
the answer; you only run it, show it, and act on what the user picks from it.

`$ARGUMENTS` may hold a window (`--last 2h`, or `--start <time> --end <time>`, ISO-8601 or epoch), a
service (`--service <name>`) and `--fixture <dir>`. No window given: use `--last 2h` and say so.
A window in words ("yesterday between 14h and 16h") becomes `--start`/`--end` in UTC; say which
absolute times you used.

**Bundled fixtures.** Three recorded scenarios live at `${CLAUDE_PLUGIN_ROOT}/skills/error-sweep/fixtures/<case>/`
(`cascade`, `timeouts`, `silence`), each with its own window. When the user asks for the demo,
sample or bundled fixtures, pass that absolute path to `--fixture`, resolved under
`${CLAUDE_PLUGIN_ROOT}`, never the working directory.

**Python command.** The commands below start with `python3`. If the shell answers "command not
found", or `python3` opens the Microsoft Store (Windows, where the python.org installer provides
`python` and `py` instead), run the same command with `python` in place of `python3` - or `py -3` -
and change nothing else; keep using that one for the rest of the session. If none of the three
exists, stop and tell the user: install Python 3.8+ (on Windows from python.org, ticking "Add
python.exe to PATH"), then fully close and reopen the editor or terminal that runs Claude Code, since
it reads PATH only when it starts.

## 1. Sweep

This installation was configured with:

- Grafana URL: `${user_config.grafana_url}`
- Loki datasource UID: `${user_config.grafana_loki_uid}`
- Tempo datasource UID: `${user_config.grafana_tempo_uid}`
- Loki selector: `${user_config.loki_selector}`

Pass each real value as `--grafana-url`, `--grafana-loki-uid`, `--grafana-tempo-uid`, `--selector`.
Skip blanks and unreplaced `${...}` placeholders. Never put a credential on the command line.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/trace-debug/scripts/sweep-errors.py" --format table [window] [--service <name>] [config flags] [--fixture <dir>]
```

One command, exactly that shape: no `cd`, `&&`, pipes or redirection. At most two runs per request
(a second only if the user changes the window or the service). On "no access configured" or an
HTTP 401/403 for every source, run
`python3 "${CLAUDE_PLUGIN_ROOT}/skills/trace-debug/scripts/collect-trace.py" doctor` and report the
configuration problem, or point the user at `/sherlock-holmes:setup`.

## 2. Show the table

Put the script's output in a code block, **exactly as printed, in full**: every row, the
"Not covered" footer and the "Next" line. Then one sentence in the user's language offering the
choice below. Nothing else.

Never:

- summarize, reorder, merge, translate or drop rows - the order is a documented rule, not a ranking;
- say which row is "the cause", "the most serious" or "probably related" - rows that share counts and
  times may belong to one failure, and finding out is what an investigation is for;
- call a row harmless because it is marked `known` - the mark comes from the team's priors file, and
  the row is shown on purpose;
- treat "no errors recorded" as "everything is fine" - the footer says what the data cannot see.

## 3. Act on the user's choice

The user answers with a row number and what they want.

- **"diagram N"** - take the first trace id listed under row N and draw it (cheap, no model):

  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT}/skills/trace-debug/scripts/collect-trace.py" --trace-id <trace id> --source tempo --format prompt [config flags]
  ```

  then, with the path printed after `FULL JSON:`,

  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT}/skills/trace-debug/scripts/trace-diagram.py" --input <that path>
  ```

  and give the user its one `diagram:` line verbatim. If Tempo does not have that trace, say so and
  offer the row's next example. Offline: the `cascade` fixture's most recent trace,
  `2aa803b2e40c97a2490d754a465fe9de`, is recorded in
  `${CLAUDE_PLUGIN_ROOT}/evals/fixtures/01-downstream-503` - pass that as `--fixture` to the collector.
  The other fixture traces have no recording; say so instead of guessing.

- **"map"** - draw every call recorded in the window's error traces as one sequence diagram (no model):

  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT}/skills/trace-debug/scripts/window-map.py" --start <start> --end <end> [--service <name>] [config flags] [--fixture <dir>]
  ```

  with `<start>`/`<end>` copied from the table's header (the absolute window, so the map describes
  exactly the swept window), the same `--service` and the same `--fixture` as the sweep. Give the user
  the script's output verbatim - the `map:` line and every line under it (the arrows, what is not in
  the map, the reading note) - in a code block, and nothing else. Do not open, read or search the
  HTML: everything there is to say about the map is in those lines. Each arrow is one kind of call,
  counted once; a sweep row counts one side of a call, so rows outnumber arrows by design. It shows
  what happened, not why: never read a cause into it.

- **"investigate N"** - invoke `/sherlock-holmes:trace-debug <first trace id of row N>` (add the
  `--fixture` above for the cascade demo). That is the only step here that runs an agent, and it runs
  because the user asked for it.

- Anything else about a row (which services, when it started, how many) - answer only from the table.
