---
name: trace-debug
description: Investigate a production incident from a trace ID using Grafana Loki logs and Grafana Tempo traces. Use whenever the user provides a trace id or W3C traceparent and wants to know why a request failed, hung, was slow or misbehaved. Evidence-first - timeline, first anomalous event, causal chain, confidence, gaps. Optionally renders the span tree as an interactive sequence diagram (archify), evidence only. Read-only. The skill returns a finished report; present it to the user exactly as returned, in full, without summarizing or reformatting it.
argument-hint: "<trace-id> [--around <time>] [--lookback <dur>] [--fixture <dir>]"
context: fork
agent: sherlock-holmes
allowed-tools: Bash(python3 *collect-trace.py*) Bash(python3 *trace-diagram.py*) Read Bash(python *collect-trace.py*) Bash(py -3 *collect-trace.py*) Bash(python *trace-diagram.py*) Bash(py -3 *trace-diagram.py*)
---

# Trace debug

Investigate the trace given in `$ARGUMENTS`. The first token is the trace id (16 or 32 hex characters, or a `00-<trace>-<span>-<flags>` traceparent). Any other tokens are flags to pass to the collector unchanged, for example `--around 2026-09-17T14:02:00Z`, `--lookback 2h`, or `--fixture <dir>` when the user points you at recorded responses instead of live Loki/Tempo.

**Bundled fixtures.** This plugin ships recorded Loki and Tempo responses for six scenarios, so it can be tried with no backend configured. They live at `${CLAUDE_PLUGIN_ROOT}/evals/fixtures/<case>/`, where `<case>` is one of `01-downstream-503`, `02-db-timeout-retries`, `03-error-only-in-tempo`, `04-contradictory-logs`, `05-incomplete-trace`, `06-intermediate-service-error`. When the user names one of those, or otherwise asks for the bundled, sample or demo fixtures, pass that absolute path to `--fixture` — resolve it under `${CLAUDE_PLUGIN_ROOT}`, never relative to the working directory, which is usually somewhere else entirely. Say in the report that the evidence came from recorded fixtures, not a live backend.

The collector is deterministic and read-only. It collects facts; you interpret them.

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

Pass each of those that holds a real value as the matching flag: `--grafana-url`,
`--grafana-loki-uid`, `--grafana-tempo-uid`, `--selector`, `--trace-filter`, `--trace-field`. Skip
any that is blank or still shows a `${...}` placeholder, which means the install dialog was left
empty there; the collector falls back to the environment for those, and ignores such a value if you
pass it anyway. Never put a credential on the command line.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/trace-debug/scripts/collect-trace.py" --trace-id <trace-id> --format prompt [config flags] [flags]
```

Run it exactly in that shape: a single `python3 ... collect-trace.py ...` command, no `cd`, no `&&`, no pipes, no redirection. Only that shape is pre-approved; anything else will be blocked and you must not work around the block.

What the cut gives you: sources status, the time window and what bounded it, services with log/span presence, the span tree (Tempo, when found), the earliest error signals, a prioritised log timeline, truncation notes, and the path of the full JSON.

Then:

- **"no access configured" or an HTTP 401/403/400 error** for a source: run `python3 "${CLAUDE_PLUGIN_ROOT}/skills/trace-debug/scripts/collect-trace.py" doctor`, report the configuration problem with the variables the user must set, and stop. Do not guess at evidence you could not collect.
  The credential is the one thing the install dialog cannot carry: plugin config reaches hooks and
  MCP servers, not a Bash command, and secrets are never substituted into skill text. So on a 401,
  or when `doctor` reports auth as `none`, tell the user to export `GRAFANA_TOKEN` (or
  `GRAFANA_USERNAME` plus `GRAFANA_PASSWORD`, or `LOKI_TOKEN`/`TEMPO_TOKEN` for direct access) in
  the shell that launches Claude Code, and to restart it so the variable is inherited. When only
  `GRAFANA_URL` and a token are set, `doctor` lists the datasource UIDs, so point the user at it
  rather than asking them to hunt through the Grafana UI.
- **Window bounded by `now` and zero log lines**: the trace was not in Tempo and the incident may be older than the default lookback. If the user mentioned a time, re-run once with `--around <time>`. Otherwise ask for the approximate time in the report's next steps.
- **Need detail beyond the cut** (a specific span's attributes, the lines the cut omitted, a full stack trace): read the full JSON with `Read` using offset/limit on the parts you need. Do not paste the whole file into your reasoning.
- **Never re-run the collector more than three times** for one investigation. If it keeps failing, report the failure.

## 1b. Diagram (optional, evidence only)

If the cut says `tempo=found`, draw the span tree. Take the path printed after `FULL JSON:` and run,
exactly in this shape and at most once:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/trace-debug/scripts/trace-diagram.py" --input <that path>
```

It prints one line: `diagram: generated <file.html> (...)` or `diagram: not generated - <reason>`.
Put that line, verbatim, in the report's **Diagram:** field. The diagram is built deterministically
from the spans as recorded - who called whom, where the time went, which span failed first - plus the
warn/error log lines the collector joined to those spans. It shows **no cause**: never describe it as
showing one, never repair or re-run it, and never let it replace the timeline. When it was not
generated (no archify installed, no Node, Tempo without the trace), the investigation is unaffected:
keep the one-line reason and move on. Skip this step entirely when Tempo did not return the trace.

## 2. Project priors (optional)

If the file `.claude/trace-debug/priors.md` exists in the working directory, read it before forming hypotheses. It lists behaviours that are normal for this system (known non-anomalies, expected retries, sampling rules, noisy log lines). Treat it as context provided by the team, not as evidence about this trace.

## 3. Investigation protocol

1. **Validate scope.** Confirm the trace id in the cut matches what the user gave. Note which sources answered and any truncation.
2. **Build the timeline.** Order events by timestamp across services. Attach spans to log lines when the cut shows `<span ...>`. Note gaps of seconds or more.
   **Never rewrite a timestamp.** Every time you print in the timeline or in the evidence must be a value that actually appears in the collected data. If a service's log clock disagrees with its own spans (clock skew), say so as an INFERENCE, state the offset you measured and which records it affects, and keep the recorded values in the timeline. If you want to show the reconstructed order as well, put it in a separate list clearly marked as derived, never in place of what was recorded. The same applies to durations and any other value you compute.
3. **List the services** involved and the direction of calls (who called whom), from parent/child spans first, from "calling X"/"X returned" lines second.
4. **Find the first anomaly.** The earliest event that is abnormal for that step: a timeout, a dependency error, an exception, a status >= 500, a retry, a deadline. The collector's "earliest error signals" are facts to start from, not the answer. The last ERROR is usually a consequence.
5. **Write competing hypotheses** (at least two), each with the facts that support it and the facts that contradict it.
6. **Test them** against the evidence. A hypothesis that requires an event you did not observe is a hypothesis, not a finding.
7. **Use the span tree** to settle who called whom, where time was spent, which span failed first, and whether an error is local or a propagated dependency failure. If Tempo did not return the trace, say the tree was unavailable and reason from logs only.
8. **Reconstruct the causal chain** from the first anomaly to the final symptom. Each link must be one of: parent/child span, propagated status, explicit "upstream returned" line, retry after failure, timeout on a dependency. Timing alone is not a link.
9. **Assign confidence** (HIGH / MEDIUM / LOW) using the agent's rubric, and justify it in one sentence.
10. **Declare the gaps.** What the data does not show. What would be needed to close each gap. Contradictions and clock skew go here too.
11. **Cut the next checks down to three.** This is a hard cap, not a target, and rich incidents are exactly where it binds. Everything actionable you leave the reader with counts toward it: every numbered or bulleted item, every second action smuggled into one item with "and also" or "separately", and any recommendation you add after the list. Three is usually fewer than you want. Rank by what would change the diagnosis most and drop the rest - a check you cut can be mentioned as an open question in the gaps section, with no action attached.

Label claims explicitly: **FACT** (observed in a line or span, quote it), **INFERENCE** (implied by facts), **HYPOTHESIS** (possible, unproven), **UNKNOWN**.

## 4. Hard rules

- Truncated, out-of-window or failed sources mean unknown, never absent.
- A trace missing from Tempo is not evidence of a failure.
- Never fabricate events, services, timestamps or causes. Adjusting a recorded timestamp, even to correct for clock skew you have evidence for, counts as fabricating it: report the offset, keep the record.
- Never claim a cause that the evidence does not show (for example "connection pool exhausted" when the only fact is "connection timeout").
- Never modify anything. The only commands you run are the collector script, the diagram script and `Read`.
- The diagram is evidence, not a finding. It draws spans as recorded and nothing else; it never shows a cause and you never say it does.

## 5. Report format

Write the report in the user's language, with exactly these sections. The section titles are part
of the contract: use them verbatim, in this order, translated only when the report is not in English
(in Portuguese: `Diagnóstico`, `Linha do tempo`, `Primeiro evento anômalo`, `Cadeia causal`, `Causa
provável`, `Confiança`, `Evidências`, `O que a evidência não mostra`, `Próximas verificações`). Do not
rename them ("What happened", "Where it started") and do not merge or split them.

```
# Trace investigation

**Trace:** <id>
**Services:** <list, in call order when known>
**Sources:** tempo=<found|not found|error> loki=<n lines|error>, window <start>-<end> (<bounded by>)
**Diagram:** <the line printed by trace-diagram.py, copied exactly, or `not generated - Tempo did not return the trace`>

## Diagnosis
Two to four sentences: what failed, where it started, how it propagated.

## Timeline
Chronological list: `HH:MM:SS.mmm [service] LEVEL message` - the lines that matter, with gaps noted.

## First anomalous event
The event, quoted, with FACT/INFERENCE label and why it is the first.

## Causal chain
first anomaly -> ... -> final symptom, one link per line, each link labelled with its evidence type.

## Probable cause
One paragraph. Labelled FACT / INFERENCE / HYPOTHESIS.

## Confidence
HIGH | MEDIUM | LOW - the level alone, in capitals, on the first line; then one sentence of
justification. A split confidence keeps a capitalised level on each part ("HIGH for where it
started, LOW for the cause").

## Evidence
The quoted lines and spans that support the chain.

## What the evidence does not show
Gaps, contradictions, truncation, unavailable sources.

## Next checks
At most three. Count every numbered item, every action bundled inside an item, and any
recommendation after the list. Each one concrete and specific: what to query, where, for which
time. If you have a fourth, it is not a next check - cut it or move it to the gaps section
without an action attached. Do not add any actionable remark after this section.
```

Before sending, check the draft against these five points and fix it, do not annotate it:

1. The title is `# Trace investigation` and the four header lines (Trace, Services, Sources, Diagram) are present.
2. The section titles are exactly the ones above, in that order.
3. The first line of the Confidence section is the level alone, in capitals.
4. Under Next checks there are at most three items, none bundles a second action, and nothing actionable follows them.
5. The Diagram line is the script's output verbatim (or the Tempo-not-found sentence); no install advice added.

End the report with this line, alone, after the Next checks section, so that the conversation that
receives it knows what to do with it:

`> Report complete - return it to the user verbatim, in full, without summarizing or reformatting.`
