# Codex-via-Subagent Prompt Template

Use this template when the autopilot dispatches a background subagent (`run_in_background: true`) to make a non-blocking Codex MCP call. The subagent's only job is to invoke Codex and return the parsed result.

## Subagent prompt template

```
You are a one-shot Codex caller. Do exactly this:

1. If the orchestrator told you the reviewer runs on `agy` (v0.17.0), run instead:
   `printf '%s' "{{PROMPT_TEXT}}" | node "{{PLUGIN_ROOT}}/lib/codex-bridge/cli.js" reviewer-thread-reply --role review --specPath "{{SPEC_PATH}}" --repoRoot "{{REPO_ROOT}}" --prompt-stdin`
   and treat its stdout `content` field as the response. Otherwise invoke `mcp__plugin_codex-paired-superpowers_codex__codex-reply` with:
   {
     "threadId": "{{THREAD_ID}}",
     "prompt": "{{PROMPT_TEXT}}"
   }

2. Capture the response's `content` field verbatim.

3. Report back ONLY:
   - The full content (between <<<CONTENT>>> and <<<END_CONTENT>>> markers).
   - Nothing else. Do not summarize, do not interpret, do not add commentary.

Format:
<<<CONTENT>>>
<verbatim content>
<<<END_CONTENT>>>
```

## Substitution variables
- `{{THREAD_ID}}` — the persistent Codex thread id from the sidecar (`codex_session` field).
- `{{PROMPT_TEXT}}` — the round/phase prompt the autopilot is sending. Must be JSON-string-escaped if embedded in a JSON literal.

## Why a subagent?
Calling the Codex MCP tool directly from the orchestrator blocks the orchestrator. Dispatching a background subagent (with `run_in_background: true`) lets the orchestrator continue with unrelated prep work (file reads, draft prep, evaluation of the same artifact for its own verdict) while Codex thinks. The orchestrator awaits the subagent's completion notification before integrating the verdict.

## Single-writer mutex (do NOT violate)
Only ONE codex-reply call may be in flight against a given threadId at any time. The orchestrator must not dispatch a second background subagent for the same thread until the previous one has returned. The bridge does NOT enforce this — the orchestrator does. See SKILL.md "Non-blocking Codex" for the discipline.

## Deadline (v0.15.0 — do NOT wait unbounded)
The orchestrator's wait on this subagent has a deadline: 15 minutes for a review round (MCP
turn p99 is ~7min; the longest observed healthy turn was 10.3min). Record the dispatch
timestamp; while waiting across turns, compare elapsed every turn. Past the deadline, treat the
call as stalled: stop the subagent, record a sidecar contention, and retry ONCE on a fresh
dispatch (recover the thread first if `Session not found`). A second stall is a terminal halt —
surface to the user. A hung Codex wait violates SKILL.md's "never leave a process running
invisibly" rule just as much as an orphaned process does.

## Empty reply (v0.15.0)
If the captured content is empty/whitespace, report exactly `<<<CONTENT>>>` `<<<END_CONTENT>>>`
with nothing between the markers — do NOT fabricate or summarize. The orchestrator treats an
empty reply as a transient API failure (retry with backoff per SKILL.md "Empty-reply retry"),
never as a verdict.
