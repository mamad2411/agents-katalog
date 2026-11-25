---
name: trace-diagram
description: Draw a trace as an interactive, self-contained sequence diagram (archify) from its Grafana Tempo spans, without investigating it. Use when the user wants to see, share or export the call sequence of a trace id - who called whom, where the time went, which span failed first - and does not ask why it failed. Evidence only. Read-only.
argument-hint: "<trace-id> [--around <time>] [--lookback <dur>] [--fixture <dir>]"
allowed-tools: Bash(python3 *collect-trace.py*) Bash(python3 *trace-diagram.py*) Read Bash(python *collect-trace.py*) Bash(py -3 *collect-trace.py*) Bash(python *trace-diagram.py*) Bash(py -3 *trace-diagram.py*)
---

# Trace diagram

Draw the trace given in `$ARGUMENTS` (first token: a 16- or 32-hex trace id or a W3C traceparent;
the rest are collector flags such as `--around`, `--lookback` or `--fixture <dir>`). This skill does
**not** diagnose. If the user wants to know *why* the request failed, point them at
`/sherlock-holmes:trace-debug <trace-id>`; the investigation draws the same diagram as part of its
report.

The bundled fixtures live at `${CLAUDE_PLUGIN_ROOT}/evals/fixtures/<case>/` (cases
`01-downstream-503`, `03-error-only-in-tempo`, `04-contradictory-logs`, `05-incomplete-trace`,
`06-intermediate-service-error`; `02-db-timeout-retries` has no trace in Tempo and therefore no
diagram). Resolve `--fixture` under `${CLAUDE_PLUGIN_ROOT}`, never relative to the working directory.

**Python command.** The commands below start with `python3`. If the shell answers "command not
found", or `python3` opens the Microsoft Store (Windows, where the python.org installer provides
`python` and `py` instead), run the same command with `python` in place of `python3` - or `py -3` -
and change nothing else; keep using that one for the rest of the session. If none of the three
exists, stop and tell the user: install Python 3.8+ (on Windows from python.org, ticking "Add
python.exe to PATH"), then fully close and reopen the editor or terminal that runs Claude Code, since
it reads PATH only when it starts.

## 1. Collect

This installation was configured with:

- Grafana URL: `${user_config.grafana_url}`
- Loki datasource UID: `${user_config.grafana_loki_uid}`
- Tempo datasource UID: `${user_config.grafana_tempo_uid}`
- Loki selector: `${user_config.loki_selector}`
- Trace-id filter mode: `${user_config.loki_trace_filter}`
- Trace-id field: `${user_config.loki_trace_field}`

Pass each value that is real as the matching flag (`--grafana-url`, `--grafana-loki-uid`,
`--grafana-tempo-uid`, `--selector`, `--trace-filter`, `--trace-field`); skip blanks and unreplaced
`${...}` placeholders. Never put a credential on the command line.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/trace-debug/scripts/collect-trace.py" --trace-id <trace-id> --format prompt [config flags] [flags]
```

One command in exactly that shape: no `cd`, `&&`, pipes or redirection. The diagram needs only the
spans, so if the cut reports a Loki problem but `tempo=found`, continue; the log lines are an extra
(warn/error lines joined to spans become notes on the diagram). If the cut says Tempo did not return
the trace, stop: there is nothing to draw, and say so. On an access error (401/403, "no access
configured"), run `python3 "${CLAUDE_PLUGIN_ROOT}/skills/trace-debug/scripts/collect-trace.py" doctor`
and report the configuration problem instead. Never run the collector more than twice.

## 2. Draw

Take the path printed after `FULL JSON:` and run, at most once:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/trace-debug/scripts/trace-diagram.py" --input <that path>
```

## 3. Answer

In the user's language, at most eight lines:

- the `diagram:` line exactly as printed (path, message count, "evidence only");
- the services in call order and the root span, from the cut;
- span count, spans with error status, trace duration and the first span to fail, from the cut - as
  facts, with recorded timestamps only;
- how to read it: open the HTML in a browser; `/` finds a participant, `R` traces a route between two
  participants, `P` plays the guided chapters, Export gives PNG/SVG.

If the diagram was not generated, give the one-line reason and, when it is archify or Node missing,
the install line `npx skills add tt-a1i/archify -g` (or `ARCHIFY_BIN=<path to archify.mjs>`). Do not
speculate about causes and do not propose fixes to the system under investigation.
