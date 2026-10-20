# Result Synthesis

The orchestrator invokes this skill to merge minion outputs into a single platform-agnostic response.

## When to invoke
- After all minions in a DAG phase have been collected.
- When a simple single-minion result needs formatting for the channel.

## Input
- `results`: array of minion result objects from `delegate-management`.
- `original_request`: the user's original message (string).
- `platform`: the source channel — `slack`, `teams`, `cli`, or `dashboard`.
- `root_correlation_id`: the session root correlation ID (string).

## Rules
- Preserve correlation IDs for traceability.
- Surface both successes and failures clearly.
- Keep responses concise; use bullets for multiple findings.
- Do not invent results not present in minion outputs.
- Use the four-field error template from `docs/error-handling.md` for failures.
- Include `[View Details]` placeholder when a correlation ID is referenced.

## Output format
Return plain text or a structured response suitable for Slack Block Kit / Teams Adaptive Card rendering.

### Example (success)
```
✅ PR review complete for #342
- 2 minor style suggestions in `src/auth.ts`
- 1 potential null-reference in `src/login.ts:48`
- Overall: changes requested
Session: corr_a1b2c3 — [View Details]
```

### Example (degraded)
```
⚠️ Partially completed:
✅ Ticket INC00421 analyzed (auth timeout bug)
❌ Code location not found (explorer timed out)
❌ PR not created
Session: corr_a1b2c3 — [View Details] [Retry]
```

### Example (failure)
```
❌ Unable to review PR #342
Cause: GitHub API rate limit exceeded (50 req/min).
Impact: Review not posted. PR #342 remains unreviewed.
Action: Review will be retried automatically in 2 minutes.
Session: corr_a1b2c3 — [View Details] [Retry Now]
```
