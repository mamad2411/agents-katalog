---
name: cleanup-stale
description: Walk the Graphory pending suggestion queue (merge candidates, link-review pairs, unresolved relationships) and recommend confirm or reject for each one - but never auto-confirm without explicit user approval. Trigger on phrasings like "clean up suggestions", "walk the review queue", "show me what needs review", "process pending suggestions", or as a follow-up when the queue is non-empty.
---

# cleanup-stale

This skill walks your pending suggestion queue in Graphory and proposes an action (confirm / reject / skip) for each item, with one-sentence reasoning. You make the final call - this skill never auto-confirms or auto-rejects.

The queue contains things the system flagged for review as ambiguous:
- Merge candidates (two contacts that might be the same person)
- Link-review pairs (multi-signal matches that scored below the auto-merge threshold)
- Uncertain relationships, incomplete contacts, and unconnected entities

The system is conservative by design - real-world judgment calls go in the queue. This skill is how you (with AI assistance) burn down the queue without the system making bad merges. It runs on your own AI, so there is zero inference cost to walking the queue.

## When to trigger

Run this skill when you say:

- "Clean up suggestions" / "walk the queue" / "process pending"
- "Show me what needs review" / "what's in my review queue"
- "Adjudicate the pending merges"

Or when the pending queue is non-trivial (5+ items) and you want to burn it down quickly.

## Required tools (Graphory MCP)

| Tool                                                              | Purpose                                        |
|-------------------------------------------------------------------|------------------------------------------------|
| `get_suggestions(status="pending", limit=20, category="")`        | Pull the queue                                 |
| `confirm_suggestion(suggestion_id, reason="")`                    | Accept the suggested action                    |
| `reject_suggestion(suggestion_id, reason="")`                     | Decline the suggested action                   |
| `batch_merge_suggestions(suggestion_ids=[...])`                   | Optional: confirm a batch (only if user asks)  |

Valid `category` values are `merge_candidate`, `link_review`, `uncertain_relationship`, `incomplete_contact`, `unconnected_entity`, and `unresolved_mention`. Default to `category=""` (all categories) on the first pull.

See https://docs.graphory.io/mcp for the full tool reference.

## The flow

1. Pull a batch of 20 pending suggestions.
2. For each suggestion, do a quick read of the payload and pick: `CONFIRM`, `REJECT`, or `SKIP` (skip = "I genuinely can't tell, leave it for the user").
3. Present the batch as a clean numbered list with your recommendation per item.
4. Wait for the user. They will say things like "do 1, 3, 5" or "all confirms" or "skip the dupes".
5. Execute the user's instructions via `confirm_suggestion` / `reject_suggestion`.
6. Summarize what you did.
7. Offer to pull the next batch.

See `examples/walk-queue.md` for a worked example of the loop.

## How to recommend

For each suggestion, look at:

- **Type / category** - merge candidate vs link review vs unresolved relationship. Different priors.
- **Names** - exact match? nickname variant? same first letter, totally different last name?
- **Emails** - exact match (high confidence same), same domain (probably same), different domains (probably different)?
- **Sources** - same-source duplicates are usually merges. Cross-source is usually two angles on the same real person.
- **Confidence the system already attached** - it's a hint, not a verdict.
- **Recent activity** - if both sides have recent activity, the merge will affect live data. Be more careful.

Pick:

| Recommendation | When                                                            |
|----------------|-----------------------------------------------------------------|
| `CONFIRM`      | High confidence the suggested action is right                   |
| `REJECT`       | High confidence the suggested action is wrong                   |
| `SKIP`         | Genuinely uncertain - the user should adjudicate this themselves |

**Default to SKIP when in doubt.** A wrong CONFIRM bakes a bad merge into your graph that's painful to undo. A SKIP just leaves the item in the queue for tomorrow.

## Output shape

Present the batch like this (numbered, scannable, concise):

```
Pulled 20 pending suggestions. My recommendations:

  1. [CONFIRM]  merge "Sarah Chen <sarah@acme.com>" + "Sarah Chen <sarah.chen@acme.com>"
                  Same name, same domain, different mailbox alias. Almost certainly the same person.
  2. [REJECT]   link "John Smith <john@acme.com>" + "John Smith <jsmith@helix.com>"
                  Same name but different companies. Probably two different Johns.
  3. [SKIP]     merge "M. Park" + "Marcus Park"
                  Could be the same Marcus, could be a different M. Park (Mei? Mike?). Worth a human eyeball.
  ...

Tell me which to apply: "do all CONFIRMs", "do 1 and 5", "skip everything", etc.
```

After the user responds, execute and summarize:

```
Done.
  Confirmed: 6 (5 merges, 1 link)
  Rejected:  3
  Skipped:   11 (left in the queue)

Want me to pull the next batch?
```

## Safety rails

- **NEVER auto-execute.** Always wait for the user to approve before calling `confirm_suggestion` or `reject_suggestion`. The whole point is human-in-the-loop.
- **NEVER use `batch_merge_suggestions` without explicit user instruction** - and even then, only on items the user named individually first. Batch is for confirming a *known* set, not a "trust me" mass merge.
- **Default to SKIP under uncertainty.** A bad merge is harder to undo than a missed merge.
- **Cap at 20 per session.** After 20, summarize and ask before pulling more. Long queue-walks become rubber-stamping, which is exactly what we're trying to avoid.
- **If you've recommended REJECT on 5+ in a row from the same category, stop and tell the user.** That signals the queue is surfacing too many false positives in that category - worth flagging instead of just powering through.
- **Don't expose internal IDs in your output.** `suggestion_id` and node IDs are for tool calls, not for the user's eyes. Show names and context.
