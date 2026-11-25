---
name: helpmetest-context
description: "Use this skill to access or update the testing project's memory. Invoke it when the user asks about prior work — what tests exist, what bugs were found, which features have been covered, or what happened in a previous session. Also invoke it when the user needs to record new work into the project — linking a newly written test to a feature, adding a discovered bug, updating coverage or feature status. This skill answers \"what do we know?\" and performs \"please remember this.\" Two jobs: reading the testing record (catch me up, resume work, show coverage) and writing to it (link this test, record this bug, update this artifact). Skip it for: running tests, debugging test failures, exploring a new site's features, or writing test code."
allowed-tools: mcp__helpmetest-*
---

# HelpMeTest Context

Two responsibilities: **discover** what already exists before doing work, and **link** new work back into artifacts after doing it.

These are two sides of the same coin — context discovery prevents recreating work that already exists, and artifact linking ensures future sessions can discover what you just did.

## Part 1: Discovery (Before Starting Work)

Always call this before any task:

```
how_to({ type: "context_discovery" })
```

Then read the output to understand:

- **ProjectOverview** — what site is being tested, what features are known, what's missing
- **Personas** — which user types and auth states exist (use these, don't recreate them)
- **Features** — which capabilities have been discovered, their status (untested/working/broken/partial)
- **Tests** — what's already been written and run

### What to do with the results

| Found | Action |
|-------|--------|
| Existing ProjectOverview | Resume from it — don't recreate |
| Existing Persona with auth state | Use `As <StateName>` — don't re-authenticate |
| Feature with `status: untested` | These are candidates for test generation |
| Feature with `test_ids: []` on a scenario | This scenario has no test yet |
| Feature with `status: broken/partial` | Known bugs exist — check `feature.bugs[]` |
| No artifacts at all | Check for orphaned tests first (see below), then start with `/helpmetest-discover` |

### Recovering context from orphaned tests

Tests are a rich source of implicit context. A test tagged `feature:password-reset`, `project:evershop`, `priority:critical` is essentially a compressed Feature artifact — it names the feature, the project, and the importance level. When Feature artifacts are missing but tests exist, **reconstruct context from the tests rather than starting from scratch**.

1. Search for all tests: `helpmetest_status` or `helpmetest_search_artifacts`
2. Group tests by their `feature:X` tag — each unique feature tag represents a capability
3. For each feature group, create a minimal Feature artifact stub:
   - `goal`: infer from test names (e.g. tests named "User can reset password" → goal is password reset)
   - `status`: infer from recent pass/fail rates — all passing → "working", failing → "broken", mixed → "partial"
   - `test_ids`: populate from the existing tests immediately
   - `functional`: create a scenario stub for each test

```json
{
  "type": "Feature",
  "id": "feature-password-reset",
  "name": "Feature: Password Reset",
  "content": {
    "goal": "Users can recover account access via email reset",
    "status": "working",
    "functional": [
      {
        "name": "User can request password reset email",
        "given": "User is on login page",
        "when": "User submits reset request with valid email",
        "then": "Reset email is sent",
        "test_ids": ["test-password-reset-basic"]
      }
    ],
    "edge_cases": [],
    "bugs": []
  }
}
```

4. Create a ProjectOverview linking all reconstructed features
5. Tell the user what was reconstructed and what gaps remain (e.g., scenarios with no tests, features with no artifacts)

This gives the user an accurate picture of current state rather than "no artifacts found." The reconstructed artifacts also serve as the starting point for future sessions.

### If user says "continue" or "same as before"

Infer the URL and context from the existing ProjectOverview. Don't ask the user to repeat information that's already in artifacts.

## Part 2: Linking (After Doing Work)

Whenever you create something, update the artifact that owns it. This is how future sessions know what was done.

### Test created → link to Feature scenario

Find the Feature artifact the test belongs to (via `context_discovery` or `helpmetest_search_artifacts`), then add the test ID to the matching scenario's `test_ids`:

```json
{
  "name": "User can complete checkout",
  "given": "...",
  "when": "...",
  "then": "...",
  "test_ids": ["test-checkout-complete"]
}
```

**If the Feature artifact doesn't exist yet:** don't silently create one from scratch. First check if tests exist for that feature (they may have been written before the artifact). If tests exist, use the recovery path above to reconstruct the artifact from them. If truly nothing exists, create a minimal stub and tell the user the feature hadn't been formally discovered yet.

### Bug found → add to Feature.bugs

```json
{
  "bugs": [
    {
      "name": "Checkout fails when cart has >10 items",
      "given": "User has 11 items in cart",
      "when": "User clicks Checkout",
      "then": "Order confirmation page",
      "actual": "500 error from /api/checkout",
      "severity": "critical",
      "test_ids": ["test-checkout-large-cart"],
      "tags": ["priority:critical", "severity:critical", "feature:checkout"]
    }
  ]
}
```

**Valid tag categories:** `priority:X`, `severity:X`, `feature:X`, `scenario:X`, `workflow:X`, `role:X`, `project:X`. Do not invent new categories like `platform:mobile` or `type:bug` — these break filtering. To capture platform-specific context, put it in the bug's `name` or `actual` field instead.

### Feature status changed → update ProjectOverview

```json
// In ProjectOverview.features, update the status:
{ "feature_id": "feature-checkout", "name": "Checkout", "status": "broken" }
```

### Auth state created → save to Persona artifact

```json
{
  "auth_state": "CustomerState",  ← this is what other skills use with "As CustomerState"
  "username": "test@example.com",
  "password": "SecureTest123!"
}
```

## The Rule

> If you created it, link it. If you discovered it, use it.

A test without a `test_ids` link is invisible to the next session. A bug without a `feature.bugs` entry will be rediscovered. A persona without an `auth_state` will require re-authentication. Artifacts are the memory of the system — keep them current.

## Quick Checklist

Before starting:
- [ ] Called `how_to({ type: "context_discovery" })`
- [ ] Found and read existing ProjectOverview (if any)
- [ ] Identified which Persona auth states exist
- [ ] Identified which features still need tests

After finishing:
- [ ] New tests linked to scenario `test_ids`
- [ ] Bugs added to `feature.bugs[]`
- [ ] Feature status updated (untested → working/broken/partial)
- [ ] ProjectOverview updated if feature status changed
