---
name: technical-handoff-writer
description: >
  Use when a PM or non-engineer has done exploratory technical work (SQL, Python, data
  analysis, algorithm validation) and needs to hand it off to engineering. Triggers:
  "write up my analysis for engineering", "create a handoff doc", "help me present this
  to the dev team", "I ran this analysis and need to share it with a developer".
---

# Technical Handoff Writer

The goal: an engineer reads the output and thinks "this person did their homework" rather than "why is this interrupting me." The handoff is structured so they can verify the core claim without trusting anything they didn't check themselves.

---

## Step 0: Gather Context First

Before asking the user anything, mine the conversation and project files:
- Read key scripts, outputs, READMEs in the project directory
- Check Obsidian project docs (`Work/Chalktalk/Projects/`) if they exist

Map what you found against these five inputs:

| # | Required Input | Where to Look |
|---|---|---|
| 1 | What was done | Conversation, project files |
| 2 | The single most important claim | Key numbers/conclusions in conversation |
| 3 | Reproducibility | Runnable scripts, queries, notebooks |
| 4 | Known assumptions/limitations | Caveats, workarounds mentioned |
| 5 | **The bounded ask** | Usually NOT in context — ask the user |

Only ask for what you genuinely can't infer. Present findings and gaps:
> "I found: claim = X, scripts = Y, assumptions = Z. I still need: what specifically do you want engineering to do?"

**If there's no reproducibility:** stop. Either offer to turn ad-hoc work into a runnable script (preferred), document manual steps precisely with expected outputs, or flag it as a Medium-risk limitation. Don't proceed until one of these is resolved.

---

## The Four-Part Structure

### Part 1 — The Claim
One paragraph. Specific numbers. Plain language. Pick the one finding that matters — don't list five.

> [Approach] achieves [metric = value] on [dataset], compared to [baseline = value]. This represents [plain-English interpretation].

### Part 2 — How to Reproduce
The most important trust-building section. Include exact commands, prerequisites (Docker, Python version, credentials), and — critically — the expected output so the engineer knows if something went wrong.

```
Prerequisites: [software/access]
Steps:
  1. [exact command]
  2. [exact command]
Expected output: [the number or table you're claiming]
Estimated time: [X min]
```

### Part 3 — Assumptions and Limitations
Engineers respect honesty. List everything imperfect. For each:
```
Assumption: [what was assumed]
Why: [why necessary]
Risk: Low / Medium / High — [consequence if wrong]
```
Common ones: data completeness, deduplication logic, algorithm approximations, population definition, known data quality issues (nulls, anonymized IDs).

### Part 4 — The Bounded Ask
One specific, time-estimable request with a clear success criterion.

**Good:** "Run `python3 elo_compare.py` and confirm the Pearson r values match the table above. ~5 min."
**Bad:** "Let me know if this looks right" / "Can you productionize this?"

Format:
```
What I need: [one sentence]
How: [2-3 steps]
Success looks like: [expected output]
Time: [estimate]
What happens next: [what you'll do with the result]
```

---

## Output

Three files, saved in the project directory and linked from Obsidian:

### File 1: Handoff Document
**File:** `handoff_[project_name]_[date].md`

**Length:** Under 500 words body. Appendix for full SQL, code, raw results.

```markdown
# [Project] — Engineering Handoff
*[Date] | Author: [Name] | Status: Awaiting verification*

## The Claim
## How to Reproduce
## Assumptions and Limitations
## What I Need From You
---
## Appendix
```

### File 2: Development Timeline
**File:** `journey-into-[project_name].md`

Generated via `/claude-mem:timeline-report`. This is a comprehensive narrative of the project's entire development history — every investigation, decision, breakthrough, and dead end. It gives the receiving engineer full context on how the work evolved, not just the final result.

**When to generate:** After writing the handoff document, invoke the `timeline-report` skill targeting the relevant project. This runs automatically as part of the handoff workflow — do not skip it.

### File 3: Agent Context Document
**File:** `agent-context_[project_name]_[date].md`

This is the file the engineer loads into their Claude session (via `cat` in the prompt, CLAUDE.md include, or pasting) so the receiving agent has full project knowledge without re-discovery. It bridges the gap between "here's what to do" (File 1) and "here's everything the agent needs to know to do it well."

**When to generate:** After Files 1 and 2 are written. Synthesize from all three sources: the handoff doc, the timeline, and the conversation context.

**Structure:**

```markdown
# Agent Context: [Project]
*Generated [Date] — load this into your Claude session before starting work*

## Project Telos
What this project exists to achieve and why it matters. One paragraph max.

## Current State
What has been built, validated, or proven so far. Reference specific files and
their purposes. Only include what EXISTS — verified file paths and function names.

## Key Decisions and Rationale
Decisions made during exploration, with WHY. Format:
- **Decision:** [what was chosen]
  **Why:** [the reason — constraint, data finding, or stakeholder input]
  **Alternative considered:** [what was rejected and why]

## Evidence vs. Assumptions
Separate clearly. The receiving agent must know what's proven vs. what's believed.

| # | Claim | Status | Evidence/Source |
|---|---|---|---|
| 1 | [claim] | Verified / Assumed / Partially verified | [file, query, or test that proves it] |

## Known Risks
Ranked by impact. Include what would go wrong and how to detect it.

| Risk | Impact | Likelihood | Detection |
|---|---|---|---|
| [risk] | High/Med/Low | High/Med/Low | [how the agent would notice] |

## Domain Knowledge
Non-obvious business rules, data quirks, or domain context the agent won't find
in the code. Things that took the PM time to learn and would take the agent time
to re-derive.

## File Map
Every file the agent needs to know about, with one-line purpose.
- `path/to/file.py` — [what it does]
- `path/to/query.sql` — [what it queries]

## Reproduction Quick-Start
Copy-paste block to verify the environment works before starting real work.
(Duplicated from handoff doc for self-containedness.)

## The Task
What the engineer's Claude session should accomplish, stated as a clear directive.
Include success criteria and out-of-scope boundaries.
```

**Quality rules for File 3:**
- Every file path must be verified to exist at generation time
- Every function/flag name must be grep-confirmed
- No narrative filler — this is a reference doc, not a story
- Domain knowledge section must contain at least 2 non-obvious items
- Evidence table must have at least 3 entries
- The task section must match the bounded ask from File 1

**Why three files:** The handoff doc says "here's what we found and what we need" (human-readable). The timeline says "here's how we got here" (narrative context). The agent context doc says "here's everything you need to start working" (machine-optimized). The engineer reads File 1, skims File 2 if curious, and loads File 3 into Claude.

## Quality Checklist

- [ ] Claim is one paragraph with specific numbers
- [ ] Reproduction steps are copy-paste with expected output stated
- [ ] At least 3 assumptions listed with risk assessment
- [ ] Bounded ask is single, specific, time-estimable
- [ ] Body is under 500 words
- [ ] Engineer does NOT need to trust any math to fulfill the ask
- [ ] Agent context doc has verified file paths (all exist)
- [ ] Agent context doc has at least 3 evidence-vs-assumption entries
- [ ] Agent context doc has at least 2 non-obvious domain knowledge items
- [ ] Agent context doc task matches the bounded ask

---

## Reference

Worked examples:
- Handoff doc: [`references/irt-elo-handoff-example.md`](references/irt-elo-handoff-example.md)
- Agent context doc: [`references/irt-elo-agent-context-example.md`](references/irt-elo-agent-context-example.md)
