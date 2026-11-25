---
name: delegation-templates
description: Fill-in-the-blank prompt templates for delegating work to subagents or tmux workers - SEARCH/LOCATE, IMPLEMENT, REFACTOR, RESEARCH, REVIEW/VERIFY. Invoke BEFORE writing any delegation prompt (Agent tool, agent-tmux worker, or fanout task) so the prompt ships with explicit GOAL, ACCEPTANCE, and REPORT sections instead of a vague ask. Not for deciding WHETHER to delegate or for driving workers after launch (see the tmux-delegate agent and the tmux-agent-tools skill for those).
---

# Delegation Prompt Templates

Fill every `{blank}`. Delete a line only if truly inapplicable — never skip the
ACCEPTANCE or REPORT sections. A delegation without objective acceptance
criteria is a guess you outsourced.

REFERENCES (optional, prefer when they exist): paths to code, tests, rubrics, or
HTML/specs that DEFINE done — a rich reference beats prose restating it. Add a
`REFERENCES:` line to any template below when the task has one.

Common footer — include in EVERY delegation:

> REPORT: return ONLY short conclusion bullets + `file:line` per claim +
> verification evidence if you changed anything. Hard cap 30 lines. Long
> artifacts → write to `{artifact_path}` and return the path. Do not paste file
> contents or logs.
> If you cannot meet an acceptance criterion, say which one and why — do not
> fake it.

## 1. SEARCH / LOCATE  (cheapest capable tier; read-only agent type if available)

```
GOAL: Find {what} in {repo/dir}. This will be used to {why}.
SCOPE: Look in {paths/globs}; also consider {alternative naming/conventions}.
ACCEPTANCE:
- Every match listed as file:line with a one-line role description.
- Explicitly state "no other occurrences" only after checking {N} naming variants: {variants}.
- Zero-result duty: before reporting zero matches, prove each search pattern works on a known positive (or synthetic sample); an unproven zero = UNCONFIRMED, not zero.
NON-GOALS: Do not review quality, do not propose fixes.
```

## 2. IMPLEMENT  (default worker tier)

```
GOAL: Implement {feature/change} in {files/module}. Motivation: {why}.
CONTEXT: {key constraints, existing helpers to reuse, style notes}. Read {files} first.
ACCEPTANCE:
- {objective condition, e.g. "`{test command}` exits 0"}.
- {behavioral condition, e.g. "endpoint returns 403 for expired tokens"}.
- No placeholder text; new non-trivial logic ships with one runnable check.
- Surgical diff: nothing outside {scope} touched.
VERIFY BEFORE REPORTING: run {command}; include exit code + key lines in the report.
```

## 3. REFACTOR  (default worker tier)

```
GOAL: Refactor {target} to {shape}, behavior UNCHANGED. Motivation: {why}.
BASELINE FIRST: run {test command} before touching anything; record the result.
ACCEPTANCE:
- Same test results after as before (attach both).
- Public API/signatures unchanged unless listed here: {allowed changes}.
- No new dependencies; dead code your change created is removed.
STOP CONDITION: if behavior must change to proceed, stop and report — do not decide alone.
```

## 4. RESEARCH  (default worker tier)

```
GOAL: Answer: {question}. The answer will drive {decision}.
SOURCES: prefer {official docs/repo/spec}; treat blogs/forums as secondary.
ACCEPTANCE:
- Every claim cited (URL or file:line). Uncited = label UNCONFIRMED.
- Distinguish "documented" vs "inferred" vs "not found".
- "Not found" duty: prove each search pattern/query works on a known positive before reporting absence; an unproven "not found" = UNCONFIRMED.
- If sources conflict, present both sides — do not silently pick one.
OUTPUT: findings to {artifact_path}; return path + a ≤10-bullet summary.
```

## 5. REVIEW / VERIFY  (fresh context; stronger tier when the change is risky; NEVER the author)

```
GOAL: Adversarially review {diff/files/claim}. Assume it is broken until proven otherwise.
CHECK:
- Claims vs reality: for each stated behavior, find the code or run the command that proves it.
- {task-specific checks: edge cases, error paths, security, contradictions between docs}.
- Files: read back in full; flag truncation, placeholders, broken paths/references.
ACCEPTANCE:
- Verdict per item: PASS / FAIL / UNCONFIRMED + one-line reason + file:line.
- Overall verdict on the last line, exactly one of: VERDICT: PASS | VERDICT: BLOCK.
Do not fix anything; report only.
```

## Dispatch shape A — in-process subagent (Agent tool)

```
Agent({
  subagent_type: "Explore" | "general-purpose" | ...,
  model: "haiku" | "sonnet" | "opus",   // cheapest tier that can pass ACCEPTANCE
  description: "{3-5 words}",
  prompt: "{filled template + common footer}"
})
```

Parallelize independent delegations in one message. Wait for results before
dispatching anything that depends on them.

## Dispatch shape B — tmux worker (agent-tmux <cli>)

```sh
agent-tmux claude start --exact --prompt-file {prompt-file} {safe-name} {repo-dir}
```

When the delegate is a tmux worker, ADD these lines to the filled template
(they replace nothing — the common footer still applies):

> Do not spawn additional tmux sessions or delegate further.
> When done, write the structured completion (result.json contract,
> schema_version 1) to the literal result path injected into this prompt —
> do not rely on `$TMUX_AGENT_RESULT` inside tool sandboxes. Put the REPORT
> bullets in its `summary` field.

Write the filled template to a prompt file and pass it via `--prompt-file`
(alias of `--from-file`; works on `start`, `send`, `send-wait`) — never
interpolate raw task text into the command line (the tmux-delegate agent's
rule, applied here to the prompt file).
Ownership boundaries: this skill owns the prompt body (templates + footers +
addendum). The dispatch shapes above are illustrative carriers showing where
the filled prompt lands — the authoritative rules for deciding WHETHER to
delegate, constructing invocations, and supervising workers after launch live
in the tmux-delegate agent and the tmux-agent-tools skill, and are not
restated here.
