---
name: codex-break-loop
description: "Post-bug-fix retrospective — classify root cause, identify prevention, write the lesson into specs. Use after fixing any non-trivial bug, when a task involving 'fix', 'bug', 'debug', or 'diagnose' is being finished, or when the user asks 'what went wrong', 'why did this break', 'root cause', or 'lessons learned'. Also use when the lifecycle hook reminds you to run break-loop."
---

# Break Loop

After fixing a bug, systematically analyze what went wrong and write the lesson into durable specs. The analysis is worthless if it stays in chat.

## Process

### 1. Classify Root Cause

Identify which category this bug falls into:

| Category | Description | Example |
|----------|-------------|---------|
| **Missing Spec** | No documented rule prevented this | "Nothing said the cache must invalidate on logout" |
| **Cross-Layer Contract** | Two layers disagreed on a contract | "View assumed sync, but ViewModel is async" |
| **Change Propagation** | A change in A broke B because the link was undocumented | "Renamed enum case, 3 switch statements missed" |
| **Test Gap** | The scenario was untested and could have been caught | "No test for empty-array edge case" |
| **Implicit Assumption** | Code assumed something that was never guaranteed | "Assumed array was sorted, but API doesn't guarantee order" |

### 2. Analyze Why Prior Approach Failed

If this bug persisted through multiple fix attempts:
- What did each attempt get wrong?
- What assumption did they share that was incorrect?
- What would have caught the real issue on the first try?

### 3. Identify Prevention Mechanism

What durable change prevents this CLASS of bug (not just this instance)?

- A spec rule? (Add to `.codex/spec/project/`)
- A code contract? (Add assertion/guard)
- A test pattern? (Add to test suite)
- An architectural boundary? (Document in spec)

### 4. Write to Specs

Find the most relevant existing spec file and add the lesson under `## Lessons`:

```bash
ls .codex/spec/project/
```

If no existing spec covers this area, create one following the spec-bootstrap format.

The entry format:
```markdown
### <Short title> (YYYY-MM-DD)

**Root cause**: <category> — <one sentence>
**Prevention**: <what rule/pattern prevents recurrence>
**Evidence**: <git commit hash or file:line reference>
```

### 5. Expand to Related Areas

Ask: "Where else in this codebase could the same category of bug exist?"

Scan for similar patterns. If found, either:
- Fix them now (if trivial)
- Record them as a task subtask (if non-trivial)
- Add a spec warning (if the pattern is inherent to the area)

### 6. Record to Journal

```bash
python3 scripts/codex_harness.py record-session --title "Break-loop: <bug title>" --summary "Root cause: <category>. Prevention written to <spec-file>."
```

If a task is active, also record to task memory:
```bash
python3 scripts/codex_harness.py task memory add --type lesson --text "<one-line summary of what was learned>"
```

## Rules

- Run this AFTER the fix is verified, not before.
- The spec update is the primary output — not the chat explanation.
- If the same root cause category appears 3+ times in specs, escalate: the architecture needs a structural fix, not more rules.
- Never skip the "expand to related areas" step — one bug usually indicates a pattern.
