---
name: systematic-troubleshooting
description: >
  Break out of circular debugging by recognizing when contradictory evidence means
  the approach is wrong, not the data. Replace fragile workarounds with clean,
  direct solutions.
---

# Systematic Troubleshooting (Break the Loop)

## When to Use

- You've been going in circles with contradictory evidence
- A workaround keeps failing in new and interesting ways
- You're getting results that "can't both be true" (two sources disagree about the same thing)
- The user suggests a simpler approach you dismissed
- You've made 3+ attempts at the same class of fix without success

## The Pattern

### 1. Recognize the Loop

**Signals you're in a loop:**
- You keep re-running the same commands hoping for different results
- You're explaining away contradictions instead of resolving them
- You're adding more complexity to a workaround that was supposed to be "simple"
- The user calls you out on it

**When you detect a loop, STOP. Do not make another attempt.**

### 2. State the Contradiction Clearly

Write down exactly what contradicts, as evidence rather than interpretation:

```
Source A reports:  X
Source B reports:  not X
Both are querying the same underlying thing, so they cannot both be true
unless [unlikely explanation you have not yet proven].
```

Naming the contradiction in plain language is often enough to make the wrong
assumption obvious. If you cannot write the contradiction down crisply, you do
not yet understand the system well enough to fix it.

### 3. Ask: "Is the Approach Wrong, Not the Data?"

When evidence contradicts, the most likely explanation is **your mental model is
wrong**, not the tools. Common patterns:

| Symptom | Likely Root Cause |
|---------|-------------------|
| Two views of "the same" data disagree | They read from different layers (cache vs source, replica vs primary, in-memory vs persisted) |
| An operation fails only after a prior "fix" | The fix created hidden state that corrupts the next step |
| A workaround works once then breaks | It depends on transient state that no longer holds |
| It "works on my machine" but not elsewhere | An unstated environmental assumption differs |

### 4. Listen to the User's Suggestion

When the user proposes a simpler approach — **try it immediately**. Do not explain
why it won't work. Do not list reasons to keep debugging the broken approach. The
user has context you don't.

**Rule:** If the user suggests a simpler approach, try it before making another
attempt at the current approach.

### 5. Replace, Don't Patch

When a workaround is fundamentally broken:
- **Don't** add more error handling, retries, or edge cases
- **Don't** try to "fix" the workaround
- **Do** replace the entire approach with something clean

```
❌ Bad: "Let me add more error handling around the broken operation"
❌ Bad: "Let me work around the workaround with a smaller workaround"
✅ Good: "Let me drop the corrupted state and rebuild it from a known-good source"
```

### 6. Verify All Sources Are Consistent

After applying the fix, verify that every place the problem could resurface agrees.
Enumerate the relevant sources first (e.g. each replica/cache/instance, plus the
read path the user actually sees), then check each one:

```bash
# Example shape — adapt to your system:
for instance in <each-replica-or-layer>; do
  <query-the-same-thing-against "$instance">
done
<query-through-the-read-path-the-user-sees>
```

If any source disagrees, the fix is incomplete.

### 7. Run the Full Test Suite

A single passing test is not enough. Run the full end-to-end suite to catch
regressions introduced by the replacement approach.

### 8. Validate Through Gated-Testbed

After the fix is verified and tests pass, **load and run the `gated-testbed` skill**
(`/workspace/.pi/skills/gated-testbed/SKILL.md`) to validate the fix against all
four gates:

- **Gate 1 (Spec)** — always run. If troubleshooting changed ports, replaced
  containers, added/removed services, or modified any infrastructure, the spec
  must be updated first. Gate 1 catches spec drift.
- **Gate 2 (Implementation)** — confirms the fix aligns with the spec
- **Gate 3 (Security/Policy)** — catches any security regressions introduced
- **Gate 4 (Runtime/Integration)** — verifies the fix works in the live stack

This is especially important when the troubleshooting involved infrastructure
changes, config modifications, or service rebuilds. The gated-testbed provides
an independent validation layer that catches what ad-hoc testing might miss.

## Pitfalls

- **Explaining away contradictions** — "Maybe there's a cache" without evidence is denial. Prove it or drop it.
- **Adding complexity to a broken approach** — If a workaround needs more workarounds, the original approach is wrong.
- **Ignoring the user's suggestion** — The user has context you don't. Try their suggestion first.
- **Only checking one data source** — If you only check the path that "works," you miss where the problem actually lives. Check ALL relevant sources.
- **Forgetting to reset/restart after a state change** — Dropping or rebuilding state often requires the component to reload before it takes effect.

## Verification

- [ ] All relevant data sources agree (every replica, cache, and the user-facing read path)
- [ ] The full end-to-end test suite passes
- [ ] The fix is simpler than the workaround it replaced
- [ ] You can explain why the old approach was wrong
- [ ] Gated-testbed validation passed (Gates 1, 2, 3, 4)