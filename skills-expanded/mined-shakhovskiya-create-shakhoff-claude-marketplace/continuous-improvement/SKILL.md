---
name: continuous-improvement
description: Generate concrete, actionable improvement recommendations after every phase, every implementation, and every review. Use this skill at the END of every Claude Code task. Triggers when a phase completes, after implementation is done, after a code review, or when the user asks "what could be better". The user explicitly values critical analysis over validation. Outputs structured recommendations the user can act on or ignore.
---

# Continuous Improvement Skill

## Why This Skill Exists

The user does not want pep talks. The user wants critical, specific, actionable feedback at every milestone. This skill is what produces the "Recommendations" section that should appear at the end of every meaningful task.

## When to Trigger

ALWAYS trigger at:
- End of Discovery phase (after brief written)
- End of Requirements phase (after PRD written)
- End of Architecture phase (after design + ADRs)
- End of each Implementation step (after tests pass)
- End of Verification phase (after review)
- After a debugging session (what to prevent next time)
- When user asks "anything else?", "what could be better?", "review this"

## Workflow

### Step 1: Determine the context

What was just done? Read the relevant artifacts. Available:
- `docs/specs/<feature>/brief.md` (if Discovery just done)
- `docs/specs/<feature>/prd.md`
- `docs/architecture/<feature>/`
- recent diff (`git diff` or list of changed files)
- test output

### Step 2: Apply the right lens for the context

Different phases need different recommendation lenses:

#### After Discovery
- Are there personas missing?
- Are there integrations the user might have forgotten?
- Are acceptance criteria observable, or are they aspirational?
- Is the scope realistic for v1?
- What edge cases were not discussed?

#### After Requirements
- Are NFR targets defensible? Where did the numbers come from?
- Are there FR that depend on FR not yet listed?
- Are there hidden NFRs (e.g., audit trail, data residency, accessibility)?
- Is the priority distribution sensible (P0 should be <50%)?

#### After Architecture
- What is the single biggest technical risk and how cheaply can we de-risk it?
- Where are we likely over-engineering for v1?
- Where are we likely under-engineering (will hurt by month 6)?
- Are there boring choices we should make to free attention for hard parts?
- What boring infrastructure problems are hidden in the design (logging, monitoring, secrets, deploys)?

#### After Implementation
- Tests that look fragile to refactor
- Code that has unclear ownership of state
- Duplication that should be extracted
- Functions/classes that grew too large (>50 lines, >5 deps)
- Lack of error context (errors that say "failed" without which call, which input)
- Missing observability hooks
- Performance hotspots not yet measured

#### After Verification
- What kinds of bugs slipped past the tests? Why?
- Could a property test or fuzzer have caught it?
- Should a runtime assertion have been added?
- What's the next likely regression?

#### After Debugging
- Root cause vs symptom: what was the actual bug?
- What signal would have made this obvious 5x faster?
- What test would have caught this?
- What's the kindest pre-mortem next time?

### Step 3: Output the Recommendations block

Structure:

```markdown
## Recommendations

### High-impact, low-cost (do these soon)
1. **<Title>:** <one-paragraph specific suggestion with concrete first step>
2. ...

### Medium-impact, moderate-cost (consider in next iteration)
1. **<Title>:** ...

### Watch list (likely to matter later)
1. **<Title>:** <what to monitor, what threshold should trigger action>

### Risks acknowledged but not mitigated
1. **<Title>:** <what risk, why we accepted it, when to revisit>
```

### Step 4: Be specific

**Bad recommendation:**
> "Consider improving error handling."

**Good recommendation:**
> "**Wrap DB errors in custom types:** The repository layer currently returns raw `sql.ErrNoRows` and `pq.Error` to callers. This couples the application layer to the driver. Wrap in `ErrNotFound`, `ErrConflict`, etc. - then handlers can do `errors.Is(err, ErrNotFound)` cleanly. First step: add `domain/errors.go` with the 3-4 sentinel errors actually used."

### Step 5: Quantify when possible

Bad: "Tests are slow."
Good: "Test suite takes 47s; the top 3 slowest tests are integration tests using a real DB. Moving them to a parallel test container would cut this to ~12s based on measurements."

Bad: "Code coverage could be better."
Good: "Coverage on `pkg/pricing` is 62%; the uncovered branches are the discount eligibility checks (lines 87-104, 132-148). These are exactly the rules most likely to break under requirements changes - prioritize these tests."

### Step 6: Distinguish "do" from "consider" from "monitor"

- **Do:** there's a clear action and it should happen. Suggest first step.
- **Consider:** there's a tradeoff. Lay out both sides.
- **Monitor:** something that doesn't need action now but should be watched.

### Step 7: Limit the list

5-10 recommendations max per phase. More than that overwhelms and gets ignored. Pick the highest-leverage ones.

## Style Rules

- No corporate-AI language. No "It's important to note that..." or "It's worth considering...".
- Direct sentences. Short paragraphs.
- Numbers > vibes.
- Reference specific files/lines/functions.
- Suggest the first step, not the entire roadmap.

## Anti-recommendations (don't do these)

- Don't recommend rewriting in a different language unless the existing one is fundamentally wrong.
- Don't recommend adopting a new framework unless there's a specific pain it solves.
- Don't recommend "more tests" without saying which ones.
- Don't recommend "better documentation" without saying what's missing.
- Don't recommend "follow best practices" - name the specific practice.

## Calibrate to the user

The user has 20+ years of IT experience. Don't explain basics. Skip preambles. Point to gnarly issues, not surface-level concerns. They've seen "you should write tests" 1000 times - skip that level.

What lands well: "Your aggregate is leaking through the repository - your handler is doing `repo.GetOrderRows(...)` then assembling the Order in the application layer. That's an anemic model. Move assembly into the repository, return an Order aggregate."

What doesn't land: "Consider applying SOLID principles."
