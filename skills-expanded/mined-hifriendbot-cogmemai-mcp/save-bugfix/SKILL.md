---
name: save-bugfix
description: After resolving any bug, save what broke, the root cause, and the fix as a CogmemAi memory so the same problem never has to be debugged twice. Use immediately after a bug is fixed, after diagnosing a flaky test, after recovering from a production incident, or after the user says "got it working", "that fixed it", "nailed it", "it works now". Builds a searchable team-wide fix database that eliminates duplicate debugging.
metadata:
  author: HiFriendbot
  version: 1.0.0
  mcp-server: cogmemai
  category: developer-tools
  tags: [bug, bugfix, debugging, memory, mcp, incident, postmortem, developer-tools]
---

# Save Every Bugfix with CogmemAi

Every team wastes hours re-debugging problems that someone already solved. The fix lives in someone's head, buried in Slack, or attached to an old Jira ticket nobody can find. CogmemAi solves this: every bugfix gets saved as a searchable memory, and every new bug starts with a search instead of from-scratch debugging.

This skill is the *save* half of that loop. Pair it with the `search-before-debugging` skill for the *recall* half.

## When to Use

Trigger immediately on any of these signals:

- A bug was just fixed and the test/build is now passing
- A flaky test was diagnosed and the root cause identified
- A production incident was resolved
- The user says: "got it", "that fixed it", "it works now", "nailed it", "found it", "the problem was X"
- A non-obvious workaround was applied
- An error message has been understood and resolved

Do not wait for the user to ask. Save proactively the moment the fix is verified.

## What to Save

Use `save_memory` with `memory_type: "bug"` and capture all four parts. Skipping any of them makes the memory useless for future recall.

### 1. Symptom (what broke)

The exact error message or observable behavior. Future-you will search for this. Include:

- Verbatim error text or stack trace summary
- Affected component, file, or service
- Conditions under which it appeared (browser, OS, request volume, time of day)

### 2. Root cause (why it broke)

The actual underlying reason, not the surface trigger. "Login failed because the JWT signing key was rotated last week but the auth service cached the old key in memory." Not "login failed."

### 3. Fix (what made it work)

The concrete change. Include the file path and the nature of the edit. "Added a 60-second TTL to the JWT key cache in `src/auth/keystore.ts`." Not "fixed the cache."

### 4. Why this fix works (mechanism)

One sentence on the mechanism so future readers can judge whether the same fix applies to a similar bug. "Forces re-fetch when keys rotate, at the cost of one extra round trip per minute under load."

## Example

```
save_memory({
  content: "BUG: Stripe webhook handler returned 500 on every event after the May 13 deploy. Symptom: 'Cannot read properties of undefined (reading id)' in the logs. ROOT CAUSE: Stripe SDK was upgraded from 14.x to 17.x; in 17.x, the event payload moved from event.data.object.id to event.data.object.metadata.checkout_session_id. FIX: Updated webhook-handler.ts:42 to use the new path and added a runtime guard. WHY IT WORKS: matches the new SDK shape and fails loudly if the path changes again.",
  memory_type: "bug",
  importance: 8,
  scope: "project",
  tags: ["stripe", "webhooks", "sdk-upgrade"]
})
```

## Importance Scoring for Bugs

| Score | Use For |
|-------|---------|
| 9-10 | Production-down incidents, security vulnerabilities, data-loss bugs |
| 7-8 | Bugs that took more than an hour to find, gotchas in widely-used code |
| 5-6 | Common gotchas, library quirks, environment-specific issues |
| 3-4 | Trivial typos, minor regressions caught immediately |

## Tagging for Recall

Tag generously so the memory surfaces from multiple search angles:

- The component or area: `["auth"]`, `["stripe"]`, `["webhooks"]`
- The technology: `["typescript"]`, `["postgres"]`, `["sdk-upgrade"]`
- The pattern: `["race-condition"]`, `["off-by-one"]`, `["null-pointer"]`

A future debugger searching any of those terms will find the fix.

## Linking Related Bugs

If this bug is related to a previously saved one (same component, same root cause family, same migration), link them with `link_memories`. Linked memories surface together, building a network of related fixes.

## Promote to Global if Universal

If the bug is library-level (a Stripe SDK gotcha, a Next.js footgun, a Postgres quirk) and would apply to *any* project using the same library, call `promote_memory` to move it from `project` to `global` scope. Future projects benefit automatically.

## What NOT to Save as a Bug Memory

- "I'm currently debugging X" — that's a task, not a fix. Use `save_task` instead.
- "Maybe the bug is X" — speculative. Wait until the fix is verified.
- The full code diff — save the *pattern*, not the entire patch. Git history holds the diff.
- Bugs that are obvious typos with no learning value — skip them.

## Related Skills

- `search-before-debugging` — the partner skill that searches for existing fixes before debugging from scratch
- `cogmemai-memory` — full reference for memory management
- `save-context` — broader context capture beyond bugfixes
- `remember-this` — for explicit user-stated preferences and decisions
