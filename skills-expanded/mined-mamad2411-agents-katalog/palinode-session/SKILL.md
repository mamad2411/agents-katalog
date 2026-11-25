---
name: palinode-session
description: "Guide intentional persistent-memory capture during coding sessions via Palinode MCP. Recall at session start; save durable milestones, explicit wrap-ups, and user-requested memories. Do NOT write for recall-only/no-new-information sessions or after an explicit no-save request."
---

# Palinode Session Memory

This skill keeps your AI agent's memory fresh across coding sessions using Palinode MCP tools.

## On Session Start

Search for prior context before beginning work:

```
palinode_search(query="[current project or task description]", limit=5)
```

Review results and reference relevant decisions or blockers from previous sessions.

## During Work — Save Milestones

After each major milestone, save the outcome:

```
palinode_save(
  content="[what was accomplished and why]",
  type="Decision",          # or "Insight" for reusable lessons
  project="[project-slug]"
)
```

### When to save:
- Tests pass after a significant change
- Feature is complete and working
- Architectural or design decision made (include rationale)
- Bug fixed that took >15 minutes (save the root cause)
- Something surprising discovered (save as Insight)

### When NOT to save:
- Routine file edits, typo fixes
- Intermediate debug steps (save the resolution only)
- Things git already tracks (code changes, file history)

## Every ~30 Minutes

If actively working and new durable progress has accumulated, consider a brief
progress note after roughly 30 minutes. Do not turn this into a timer-based
write for a recall-only/no-new-information session, and honor an explicit
request not to save:

```
palinode_save(
  content="Progress: [what's been done so far, what's next]",
  type="ProjectSnapshot"
)
```

## On Session End

At a user-requested wrap-up, or when the session produced new durable
information, capture the session:

```
palinode_session_end(
  summary="[1-2 sentence summary of accomplishments]",
  decisions=["decision 1 with rationale", "decision 2"],
  blockers=["open question or next step"],
  project="[project-slug]"
)
```

Do not create a recap for a recall-only or no-new-information session, and
honor an explicit request not to save. `palinode_save` and
`palinode_session_end` are intentional, content-bearing MCP writes; they are
separate from opt-in client hooks and background auto-summary enrichment.
`palinode init --no-hook` leaves automatic hooks off, but this skill can still
guide an agent to make an intentional explicit tool call. When the user invokes
`/wrap`, preserve that explicit requested session-end write unless the user
separately says not to save.

## Tool Reference

| Tool | When |
|---|---|
| `palinode_search` | Start of session, or "what do we know about X" |
| `palinode_save` | Milestones, decisions, insights, progress |
| `palinode_session_end` | End of session — structured summary |
| `palinode_diff` | "What changed recently?" |
| `palinode_blame` | "When was this decided?" |
| `palinode_trigger` | Register auto-recall for recurring topics |
