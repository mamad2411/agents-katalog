---
name: agentic-debug-mode
description: Use when a bug, regression, race condition, or unexpected behavior has no proven root cause and you must confirm the cause with runtime evidence instead of guessing from source code.
---

# Debugging with Runtime Evidence

## Core rule

Source code creates hypotheses. Runtime evidence confirms or rejects them.

**Do not implement a bug fix before collecting runtime evidence** that identifies the cause. Reading
code tells you what *could* happen; only observations from a real run tell you what *did* happen.

`debug-mode` is a small CLI that collects and queries that evidence for you. It manages its own
background service; you never manage processes, ports, or state files. Every command prints
readable text by default — read that text, do not scrape it.

## Do the work yourself

Do not ask the user to perform an action you can execute with available tools.
Run available CLI commands, tests, and HTTP requests yourself, including installation, session
setup, resetting evidence, reproduction, and evidence collection.

Ask the user only for inaccessible interactions: a physical device or on-screen tap you cannot
drive, an external system or account you have no credentials for, or subjective confirmation that
the observed behavior now looks correct. Before asking, complete every accessible prerequisite —
insert observations, reset the session, rebuild — and request only the smallest remaining step.

## Vocabulary

Terms used throughout, defined once:

- **Session** — one debugging investigation, identified by a random UUID. It owns one evidence
  record. Every session-scoped command needs `--session <id>`.
- **Hypothesis label** — your own name for one falsifiable guess, such as `H1`. You invent and
  track these; the CLI never registers, declares, or validates them. It only groups and filters the
  labels it sees in evidence.
- **Helper template** — a block of code, inserted **once** per runtime, that owns transport,
  serialization, size limits, secret redaction, and failure suppression. Treat it as opaque.
- **Call template** — a small block copied **once per observation**. You replace only its
  placeholders.
- **Observation** — one `agent log` region emitting one event that tests one hypothesis.
- **Ingest URL** — the loopback address an HTTP helper posts to. The session is in the URL path;
  it is not a secret and needs no header.
- **Append path** — the file a file helper appends newline-terminated JSON records to.
- **Reset cycle** — everything between one `reset` and the next. Resetting restarts sequence
  numbering at `1` and invalidates old log/query cursors.
- **Runtime evidence** — the validated events the CLI returns from `logs`, `query`, and `status`.

## Resolve the CLI

Run `debug-mode --version`. If it is missing, install it with the first channel the host's package
policy allows, then verify again:

1. npm: `npm install --global agentic-debug-mode@latest`
2. Bun: `bun install --global agentic-debug-mode@latest`
3. Homebrew only when the project documents its official tap coordinate.
4. Zero-install fallback: prefix every command with `npx --yes agentic-debug-mode@latest`.

Never use an unverified `curl | sh`, never request elevated privileges, and never edit shell
startup files. If no supported channel works, stop and report the exact error.

## Workflow

For one investigation, repeat this loop with **one** session:

1. Create a session.
2. Get a language template and insert folded observation regions.
3. Reset the session, then reproduce.
4. Read evidence with `logs`, `query`, and `status`.
5. Classify each hypothesis in your own reasoning.
6. Change code or observations.
7. Reset and reproduce again.
8. Compare evidence until it proves the fix.
9. Remove observations, then stop.

### 1. Create a session

```bash
debug-mode create
```

The output returns a **Session ID**, an **Ingest URL**, and an **Append Path**. Keep the Session ID
and pass `--session <id>` to every later command. Reuse this one session for the whole
investigation — do not create a fresh session per attempt.

Never guess a session. If you lose the ID, recover it (newest first):

```bash
debug-mode sessions
```

`sessions` lists sessions; it never selects one for you. `sessions --all` includes older sessions.

### 2. Get a template and instrument

State expected behavior, actual behavior, and the shortest reproduction. Form three to five
precise, falsifiable hypotheses and label them `H1`, `H2`, and so on. Then request the template for
the runtime you are instrumenting.

```bash
debug-mode template --language typescript --ingest http
debug-mode template --language python --ingest file
```

Transport follows runtime reachability. Use **HTTP** for JavaScript and TypeScript (one shape
across browser and server) with the Ingest URL. Use **file** append for local CLIs and services
with the Append Path. Advertised combinations, each verified end-to-end:

| Language   | Ingest | Language    | Ingest |
| ---------- | ------ | ----------- | ------ |
| JavaScript | http   | Ruby        | file   |
| TypeScript | http   | PHP         | file   |
| Python     | file   | PowerShell  | file   |
| Go         | file   | C#          | file   |
| Swift      | file   |             |        |

The output has four sections: **HELPER TEMPLATE**, **CALL TEMPLATE**, **PLACEHOLDERS**, and
**EVENT SCHEMA**.

Insert the helper template once per runtime boundary. Copy the call template once per observation.
Replace only the listed placeholders — for HTTP replace the ingest placeholder with the Ingest URL;
for file replace the append placeholder with the Append Path; then fill hypothesis, location,
message, and data.

Keep every observation inside its own region, and keep the exact markers so the block stays foldable
and mechanically removable:

```ts
// #region agent log
__agentDebugEmit({
  hypothesisId: "H1",
  location: "src/cart.ts:84",
  message: "Before discount calculation",
  data: { itemCount: items.length, subtotal },
});
// #endregion
```

Python and other file runtimes use `# region agent log` / `# endregion`. Never put production
behavior inside a region, never `await` an observation, and never instrument a generated file whose
syntax cannot hold the markers.

### Event schema

Every observation carries exactly five fields:

- `hypothesisId` — your label for the one hypothesis this observation tests.
- `location` — stable source location, preferably `path:line`.
- `message` — a constant description of the observation; changing values go in `data`, never here.
- `data` — bounded JSON holding the values that change between runs.
- `timestamp` — observation time in Unix epoch milliseconds. The helper sets it for you.

Stored evidence adds `id`, `sequence` (order within the reset cycle), and `receivedAt` (receipt
time, also Unix epoch milliseconds). When timestamps tie, `sequence` breaks the tie.

Keep `message` constant and put changing values in `data`. Keep `data` small and bounded. Never
record passwords, cookies, authorization headers, private keys, full request bodies, or unrelated
personal data — the helper redacts obvious secrets, but you choose what to observe. A failed
observation must never change application control flow; the helper isolates transport failures, so
missing events mean an unexecuted path or a failed run, never a crash.

### 3. Reset and reproduce

Clear the previous evidence for this session, then reproduce:

```bash
debug-mode reset --session <id>
```

Reset preserves the session ID, the append path, and your inserted observations; it only clears
evidence and restarts sequence numbering. Reproduce yourself whenever the runtime is accessible
(run the test, script, or request). If reproduction needs the currently valid Ingest URL, take it
from the reset output before running.

### 4. Read evidence

**Use only `debug-mode logs`, `debug-mode query`, and `debug-mode status`** to read runtime
evidence. **Never use native file-reading tools**, shell commands, `tail`, `sed`, `awk`, a direct
`jq`/`jaq`, or ad hoc scripts against the evidence — those bypass validation and session isolation.

Start with a bounded read:

```bash
debug-mode logs --session <id> --limit 100
```

Filter or transform with an embedded jaq program:

```bash
debug-mode query --session <id> 'select(.message | test("timeout|deadline"; "i"))'
debug-mode query --session <id> 'select(.hypothesisId == "H1" and .data.durationMs >= 100)'
debug-mode query --session <id> '{seq: .sequence, loc: .location, ms: .data.durationMs}'
```

Streaming is the default and stays memory-bounded. Collection operations — `sort_by`, `group_by`,
whole-run aggregation — need explicit `--slurp`:

```bash
debug-mode query --session <id> --slurp \
  'group_by(.hypothesisId) | map({hypothesisId: .[0].hypothesisId, count: length})'
```

Every result is ordered: **warnings first**, then the session scope, then statistics, then the
records or results, then actionable hints. Read them in that order — check warnings, confirm the
session, weigh completeness, then follow the printed continuation commands to page. Those commands
carry the query scope; reuse them instead of inventing offsets.

If `logs` or `query` reports **malformed** records, inspect all of them:

```bash
debug-mode status --session <id>
```

`status` lists every malformed record and evidence-health summary. Fix the emitting observation each
diagnostic identifies, `reset` the session, and reproduce. Never edit stored evidence.

### 5. Classify each hypothesis

In your own reasoning, mark every hypothesis and cite event IDs or sequence numbers:

- `CONFIRMED` — events directly demonstrate the causal path.
- `REJECTED` — events contradict the hypothesis.
- `INCONCLUSIVE` — expected evidence is absent or ambiguous.

Missing events can mean an unexecuted path, a failed run, or stale code — not proof of absence. Add
a control observation before rejecting on silence. If nothing is confirmed, form new hypotheses in
other subsystems and repeat. Remove speculative edits for rejected hypotheses; implement only the
smallest fix the confirmed evidence supports.

### 6. Verify the fix

Keep every observation in place through verification. Record your baseline conclusions from the
first run in your own notes, apply the fix, then `reset` and reproduce again and re-run the same
queries. The post-fix evidence must show **both** that the wrong path or state no longer occurs
**and** that the expected path or invariant now does. Baseline and post-fix both live in this one
session across reset cycles; nothing persists two separate runs for you.

Remove the complete `agent log` regions only after post-fix evidence succeeds and the user confirms
the behavior looks correct.

### 7. Clean up

- `debug-mode reset --session <id>` reuses the same session — it clears evidence but keeps the
  session and your observations for the next attempt. This is the normal per-attempt command.
- `debug-mode clean --session <id>` permanently deletes the session and all its evidence. Use it
  only when the user explicitly asks to delete the investigation.
- `debug-mode stop` ends the background service without deleting any evidence. The next command
  restarts it transparently.

## Common mistakes

- Fixing before evidence confirms the cause. Collect first.
- Creating a new session per attempt. Reuse one; `reset` between attempts.
- Reading the evidence file directly. Use `logs`, `query`, `status` only.
- Rejecting a hypothesis on missing events without a control observation.
- Removing observations before post-fix evidence and user confirmation.
- Putting changing values in `message` instead of `data`.
- Asking the user to run something you can run yourself.

## Quick reference

| Step             | Command                                             |
| ---------------- | --------------------------------------------------- |
| Create session   | `debug-mode create`                                 |
| Get template     | `debug-mode template --language <l> --ingest <t>`   |
| Reset evidence   | `debug-mode reset --session <id>`                   |
| Read a page      | `debug-mode logs --session <id> --limit 100`        |
| Query evidence   | `debug-mode query --session <id> '<jaq>'`           |
| Diagnostics      | `debug-mode status --session <id>`                  |
| Recover an ID    | `debug-mode sessions`                               |
| Delete a session | `debug-mode clean --session <id>`                   |
| Stop the service | `debug-mode stop`                                   |

For the full command and jaq-query reference, see [REFERENCE.md](REFERENCE.md). For worked
end-to-end investigations, see [EXAMPLES.md](EXAMPLES.md).
