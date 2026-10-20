# Intent Classification

The orchestrator invokes this skill to classify a user message into a supported intent before dispatching minions.

## When to invoke
- At the start of every user request.
- When the orchestrator needs to re-classify after clarification.

## Input
- `user_message`: the raw text from the user (string).
- `platform`: the source channel — `slack`, `teams`, `cli`, or `dashboard` (string).
- `session_context`: optional prior-turn summary (string).

## Output
Return JSON matching `schemas/intent.json`:

```json
{
  "intent": "ticket_lookup|ticket_summary|code_explore|code_review|pr_create|security_audit|ticket_fix_pr",
  "complexity": "simple|complex",
  "platform": "slack|teams|cli|dashboard",
  "entities": {}
}
```

### Intent definitions
- `ticket_lookup` — "What's the status of INC00421?"
- `ticket_summary` — "Summarize AB#1234"
- `code_explore` — "Find where login timeout is handled"
- `code_review` — "Review PR #342"
- `pr_create` — "Create a PR for this fix"
- `security_audit` — "Audit this repo for secrets"
- `ticket_fix_pr` — "Fix work item #567 and create a PR"

### Complexity rules
- `simple` — single minion can handle it (`ticket_lookup`, `ticket_summary`, `code_explore`, `code_review`, `security_audit`).
- `complex` — requires a DAG of multiple minions (`ticket_fix_pr`, batch reviews, multi-ticket summaries).

## Example
Input: `"@minions review PR #342"`
Output:
```json
{
  "intent": "code_review",
  "complexity": "simple",
  "platform": "slack",
  "entities": { "pr_number": 342 }
}
```
