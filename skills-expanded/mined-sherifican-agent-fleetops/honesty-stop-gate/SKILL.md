---
name: honesty-stop-gate
description: Adapt the honesty stop gate (guard/honesty_stop_gate.py) to THIS user's stack — a Stop hook that blocks a turn asserting live state it never measured. Invoke when a user says "add the honesty gate", "wire up the stop hook", "adapt the honesty stop gate", or after copying guard/ into their project. The procedure forces the adopting AI to VERIFY every command it wires actually exists on the user's system (via --check-config), ASK about anything it cannot determine, keep private files and environments untouched, and prove the gate can fail end-to-end on the user's own box before calling it done.
license: MIT
---

# Honesty Stop Gate — adaptation skill

You are wiring `guard/honesty_stop_gate.py` into the user's agent so it blocks the agent from ending a turn on a live-state claim it never measured. Adapt the shipped configuration and verify its behavior on the adopting harness. The danger is **building a stair to nowhere**: a check that reads as coverage and verifies nothing, because it points at a command the user's system does not have, or one that cannot fail. Read [`specs/honesty-stop-gate.md`](../../specs/honesty-stop-gate.md) first — including *"What it enforces, precisely"* (the gate checks a recorded probe naming the subject and restricts flagged error-result credit; it does not adjudicate claim truth). Do not reimplement the mechanism.

## The contract you operate under

1. **Verify everything you can.** Anything checkable about the user's system, you check — before you write it into config, not after. A command goes in `verification_commands` only after `--check-config` confirms its binary resolves on this box.
2. **Ask about anything you cannot.** When you cannot determine how the user names their jobs, which command observes a service's state, or whether the user's agent harness even fires Stop hooks, ASK — one concrete question with your best guess offered. Do not invent an answer.
3. **Keep private things private.** Do not read secrets, credential files, `.env` files, tokens, or private data to infer configuration. **This includes the user's conversation transcripts, logs, and history** — they are a tempting source for "how does this agent phrase claims" and they routinely contain private data. You need command names and subject vocabulary, not file *contents*; get those by asking the user for representative phrasings, or from non-secret places (process lists, service names, public scripts). If configuring correctly seems to require reading a private file or a past transcript, that is a signal to ASK, not to read.
4. **No stair to nowhere.** Every `verification_commands` entry must be a real, existing command that can fail. An unconditional `echo`, a bare `&`, a file-existence read (`ls`, `stat`) or a log read (`cat`/`tail` a `.log`) does not observe liveness and verifies nothing. `--check-config` enforces the existence half; you enforce the observes-liveness half by only listing process/service probes for running-claims.

## Procedure

### 1. Read the mechanism, then map the three parameters
Open `guard/honesty_gate.config.example.json`. You are producing a `honesty_gate.config.json` (same directory, or pointed to by `$HONESTY_GATE_CONFIG`) that overrides `claim_patterns`, `verification_commands`, `subjects`, and optionally `non_subjects` / `verify_hint` and the file-scan keys below. Leave `completion_pattern` alone unless the user's language for "finished" genuinely differs — and keep its linking-verb + clause-final requirement, or a bare "Done," will fire. The `write_*` / `heredoc_sinks` / `arg_sinks` keys govern the scan of file bodies (a claim written into a report outlives the turn); the defaults fit a Claude-Code-shaped harness (`Write`/`Edit`, `file_path`) and you change them only if the user's tools are named differently. Add to `write_skip_paths` only files that legitimately *quote* claim phrases, by exact name or a narrow glob — a pattern with no literal name (`*.md`, `**/*`) is refused at load, and `--check-config` prints what survived.

### 2. Discover the user's SUBJECTS (what live things do they claim state about?)
Ask, or infer from what is safely visible: what does this agent launch and then report on? Background jobs, CI runs, deploys, services, containers, other agents/legs, long builds. These become `subjects`. Prefer distinct single tokens (a service name) over generic compounds — "build" and "job" as separate subjects make "build job" demand both be verified. If the user has a naming convention (e.g. logs named `<subject>_run.log`), note it: the gate resolves a subject from a `*.log`/`*.json`/`*.txt` filename.

**If this agent launches nothing in the background** — it works synchronously, its output is always in the transcript — say so and do NOT ship a running-claim gate: there are no subjects to guard, and an empty `subjects` list is a degenerate config. Either scope the config to completion-type claims only, or tell the user the gate has nothing to watch on this stack. Do not manufacture subjects to have something to configure.

### 3. Discover and VERIFY the user's verification commands — the critical step
For each way the user's agent could observe live state, find the actual command. Then **prove it exists on this box with `--check-config`, not by eye.**

- Is there a process supervisor? `systemctl status` / `systemctl is-active` / `supervisorctl status` / `pm2 list`.
- Containers/orchestration? `docker ps` / `kubectl get`.
- Process table? `pgrep` / `ps`; validate the query via [Instrument self-defeat](../guard-target-correctness/SKILL.md#instance-3--instrument-self-defeat).
- A job runner, task queue, or the agent harness's own status command? The exact binary/subcommand, and it must *observe* state (be able to return "not running"), not always succeed.
- Health endpoints? `curl .../health` — only if the endpoint is real.

When you replace or harden a probe (for example, stop using `pgrep -f` because it matches its own
command line), update `verification_commands` in the same commit; follow the
[producer/consumer vocabulary rule](../../specs/the-silent-clear-problem.md#producer-and-consumer-vocabulary).
Do not add a generic reader such as `cat` or `python3`: it credits unrelated reads. A `/proc` reader
that names its subject is an option only after it passes the
[Instance 3 controls](../guard-target-correctness/SKILL.md#instance-3--instrument-self-defeat);
neither `guard/honesty_gate.config.example.json` nor `guard/honesty_gate.config.minimal.example.json`
includes one.

Write your candidate list into `honesty_gate.config.json`, then run:

```
HONESTY_GATE_CONFIG=guard/honesty_gate.config.json python3 guard/honesty_stop_gate.py --check-config
```

It refuses unresolved command binaries and malformed selected configuration. It also refuses invalid overrides of the three required regex lists, `completion_pattern`, `non_subjects`, `write_path_keys`, `heredoc_sinks`, and `arg_sinks`, including invalid regexes in the expressions the hook actually compiles. The required lists and three file-scan lists must be nonempty lists of nonblank strings; `completion_pattern` must be a nonblank string; `non_subjects` must be a list of strings and may be empty.

Omitted keys inherit defaults. A rejected field keeps **only that field's default** at runtime, preserving other valid choices, but `--check-config` still exits 1 and names the refusal. A malformed, nonobject or unreadable selected JSON document retains the full defaults and is refused; an explicitly selected missing/nonfile path is also refused. An absent ordinary default config is permitted. Fix every refusal before accepting the configuration: fallback protects the hook from these malformed inputs; it does not establish that the defaults suit the user's stack.

**Tell the user which overrides were refused and why** — silent omission reads as "covered everything." If, after dropping unresolved commands, `verification_commands` would be empty, STOP and tell the user: the gate cannot function without at least one real probe — surface the gap rather than shipping a gate that can never verify. Do not proceed past a red `--check-config`.

A successful check establishes these bounded shape, regex and executable-presence checks only. A valid regex can match nothing, a well-typed tool/path key can name the wrong harness field, and an existing command can observe nothing useful. The end-to-end controls in step 6 remain required; this check is not a blanket validator for every optional configuration field.

### 4. Write the CLAIMS' regexes conservatively
`claim_patterns` should cover how *this* agent phrases live-state claims (keep both running-type and completion-type families from the example). When unsure whether a phrase is a claim, leave it in — a false block is recoverable (run the check, delete, or label); a missed claim is the silent failure the gate exists to prevent. But do not add a pattern so broad it matches ordinary prose every turn — an always-firing gate gets disabled, which is the same as no gate.

### 5. Confirm the harness will actually run the hook
The hook's contract is Claude-Code-shaped: the harness must (a) invoke `Stop` hooks, (b) supply a JSON object with the turn's `transcript_path` on stdin, (c) honor a `{"decision":"block"}` response, and (d) set `stop_hook_active` on re-entry. A hook that is never invoked provides no check; an invoked hook with malformed input or an unavailable transcript now returns a CANNOT CHECK block. A harness that honors blocks but repeatedly sends an unparseable payload, or never sends `stop_hook_active` after a block, can block every turn or loop; verify both the first invocation and the continuation before adopting it. Confirm the user's harness supports all four requirements, or ASK. For Claude Code: add one `Stop` hook entry pointing at `guard/honesty_stop_gate.py`. **Show the exact settings diff and back up the settings file before writing**, and add only that one entry — do not modify settings you were not asked to.

Stop invocations attempt a best-effort stage log beside the module unless `HONESTY_GATE_STAGE_LOG` selects an absolute path or is empty to disable logging. A relative override has no fallback, diagnostic modes do not log, and a log failure is silent and does not change the hook decision. Use an approved output location and inspect valid stage records; absence of a record is not PASS.

In four completed headless `-p` runs of cursor-agent 2026.10.19 on 2026-10-31 that configured a stop hook (two in Cursor's own hook format, two as a Claude-format `Stop` entry), no stop event fired, so a Stop hook, this one included, would not have run in them; for that build in headless `-p` mode a wrapper must own the turn-end check. The v0.1.10 `guard/headless_turn_end.py` adapter scans result text only when the worker status is 0 and the declared `json` capture is one UTF-8 JSON object with `type: "result"`, `subtype: "success"`, boolean `is_error: false` and a string `result`; every other `json` input and all `stream-json` inputs yield CANNOT CHECK. Duplicate keys, parser recursion and trailing non-whitespace data are invalid, and configuration refusals or scan failures also yield CANNOT CHECK. A scanned result with no findings yields PASS/0; ordinary findings only yield BLOCK/1; a returned CANNOT CHECK finding, alone or mixed, yields SCAN_INCOMPLETE, CANNOT CHECK/2. These returned scans have result-text-only coverage and no tool evidence; callers accept only checker return code 0. This describes the adapter's input contract, not verified compatibility with an unsupplied capture. One of those runs also configured Claude-format `SessionStart` and `PreToolUse` hooks in the project, and both fired, so project Claude-format hook files were imported. A fifth run showed that user-level ones are imported too and that a `PreToolUse` hook with matcher `Bash` fired for Cursor's `Shell` tool. These runs do not establish Stop behavior in other Cursor builds or modes.

Run `python3 guard/headless_turn_end.py --format json --capture CAPTURE --worker-exit-code STATUS` only after the worker exits, passing its actual status and retaining its capture. Optional `--lane` and `--worker-outcome` supply receipt metadata; omitted values are null, and worker outcome accepts only `ok`, `partial`, `empty`, `usage` or `timeout`. Format and capture arguments must be nonempty; an empty capture argument is an invalid invocation with a null artifact path. The checker emits a JSON receipt on stdout with the original worker status, capture path, byte count and SHA-256, lane, UTC timestamp and worker outcome, plus `turn_end` verdict, reason code, coverage, findings, configuration refusals and checker status. Empty readable bytes have byte count 0 and the SHA-256 of empty bytes; unreadable captures have null byte count and hash. Outer worker outcome `ok` is not a PASS: callers accept only checker return code 0 and a consistent `turn_end.verdict` of `PASS`; BLOCK returns 1 and CANNOT CHECK returns 2. `--help` prints usage on stdout, emits no receipt and exits 2, reserving status 0 for a PASS receipt. The entire `result` string is scanned once, including earlier concatenated segments; an empty result string is valid text, while an empty capture is CANNOT CHECK. Tool-looking text supplies no tool evidence, and this check certifies neither tool history, file writes nor claim truth. Any configuration refusal stops the check with CANNOT CHECK and is listed in the receipt. The checker does not retract output already written or persist its own receipt; the caller owns the receipt destination and acceptance decision. A sanitized real capture with provenance is required before claiming compatibility with a particular build; stream-json and Cursor `tool_call` mapping remain a separate follow-up.

### 6. Prove it can fail END-TO-END, on this box, with the user's own config
Two acceptance checks, both required:

1. `--check-config` is green **under the user's config** (step 3), and `--self-test` prints
   `SELF-TEST PASS` (the mechanism itself is intact). These two check *different things* and you
   need both: `--check-config` validates the operator's vocabulary and probes, while `--self-test`
   runs built-in fixtures with their own hard-coded subjects (`deploy`, `build`, `pgrep -af
   deploy`) against the **built-in** config. Do not read a self-test result as evidence about the
   user's config — it is not, and earlier versions that ran the fixtures under a narrowed config
   printed `SELF-TEST FAIL` for a perfectly legal one while `--check-config` printed `OK`.
2. **A real trigger with a real subject.** The `--self-test` uses generic strings and only exercises `scan_turn` directly — it does *not* prove the harness fires the hook or that your subjects/commands work. So drive the hook the way the harness does: build a tiny transcript file naming one of the *user's* subjects with an unbacked claim, and feed it in —

   ```
   printf '{"type":"assistant","message":{"content":[{"type":"text","text":"The <their-subject> is still running."}]}}\n' > /tmp/ht.jsonl
   echo '{"transcript_path":"/tmp/ht.jsonl"}' | HONESTY_GATE_STAGE_LOG="" HONESTY_GATE_CONFIG=guard/honesty_gate.config.json python3 guard/honesty_stop_gate.py
   ```

   That must emit a `{"decision":"block", …}`. Then add a line running one of the user's *real* verification commands naming that subject (a `tool_use` + `tool_result` pair) before the claim, and confirm it goes silent. A gate you have not watched block a real unbacked claim and pass a real backed one on this machine is not yet trusted — this is the same law the rest of the guard ladder runs on ([rigor-spectrum](../../specs/rigor-spectrum.md)): no guard without a proof it can fail.

### 7. Report what you wired and what you skipped
Tell the user, in plain terms: the subjects you configured, the verification commands `--check-config` confirmed exist (and any you dropped and why), the harness-support facts you confirmed or the questions you still need answered, and the self-test / end-to-end teeth result. If you asked questions in steps 2–5 that are unanswered, the config is provisional — say so; do not present it as done.

## Acceptance
Acceptance requires: config written from verified facts (not guesses, not scraped from private history), `--check-config` green with every verification command's binary confirmed present, no private file or transcript read to produce it, the harness confirmed to fire Stop hooks with a JSON object containing `transcript_path`, honor `decision:block`, and set `stop_hook_active` on the continuation, the settings diff shown and backed up, `--self-test` green, and the gate observed to block a real unbacked claim, pass a real backed one, and skip the re-entry continuation **end-to-end** on the user's own machine. Anything you could not determine is surfaced as a question, not filled in silently. If the agent launches nothing in the background, the honest deliverable is saying so — not a degenerate config.

The Stop payload may supply `last_assistant_message` before the final prose appears in the
transcript. After successfully reading the transcript, I scan this field only if it is a string,
as the last assistant text under the same configuration and ordered evidence. It grants no
probe credit and emits at most one block decision even when duplicated in the transcript.
Absent or wrong-type final-message values retain transcript-only behavior after a successful transcript read. A missing, invalid, unreadable or malformed transcript blocks with CANNOT CHECK, even when final-message text is supplied; that text is not scanned independently. Re-entry alone intentionally skips inspection with empty stdout and status 0.

For a result flagged `is_error: true`, I credit only an exact first text line `Exit code 1` with no permission-denial, unknown-tool, sandbox or hook refusal phrase, and only when status is attributable to an unconditional terminal probe-plus-filter unit. String and text-block bodies are supported; unavailable text gets no error credit. This keeps direct `pgrep` no-match absence credit; the bracket form `grep '[d]eploy'` names no subject under the unchanged extraction rules and does not receive `deploy` credit. `false && pgrep -af deploy` does not establish that the probe ran. Missing/false flags retain legacy nominal-success handling, but a later statement, an OR or background chain (including trailing `&`), or a stage after the probe-plus-filter unit withholds credit; compound commands and indeterminate parses receive no credit. Unquoted `|&` is one pipeline operator in the status view. Use two tool calls, or one `&&` chain with a nominal-success result, to credit two subjects. Other flagged statuses (including `systemctl status` exit 3) fail closed until a typed outcome adapter is available.
