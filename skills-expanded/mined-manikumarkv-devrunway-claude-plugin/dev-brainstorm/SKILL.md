---
name: dev-brainstorm
description: Technical exploration for a GitHub issue. Identifies challenges, compares approaches with a decision matrix, records all Q&A, and recommends an approach. Outputs docs/dev-brainstorm/<ticket>.md. Usage — /dev-brainstorm <issue-number>
argument-hint: "<issue-number>"
arguments:
  - name: issue
    description: "GitHub issue number"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash(find *)
  - Bash(ls *)
  - Bash(git *)
  - Bash(grep *)
  - Bash(gh *)
---

# Dev Brainstorm

Parse `$ARGUMENTS[0]` as the GitHub issue number.

---

## Step 1 — Load full context

```bash
# Fetch the issue
gh issue view <issue-number> --json title,body,milestone,labels,comments

# Load refinement doc if it exists
find docs/product-tasks/ -name "<issue-number>-refined.md" | head -1

# Load product plan for broader context
find docs/product-plans/ -name "*.md" | xargs grep -l "#<issue-number>\|Story.*<issue-number>" 2>/dev/null | head -1

# Understand current codebase structure
find src/ -type d | head -30
ls src/ 2>/dev/null
```

Read all available docs. Summarise the requirement back to the developer:

> **#<issue-number>: <title>**
>
> **Goal:** <one-line summary>
> **Key AC:** <2–3 most important criteria>
>
> Starting technical exploration. I'll work through challenges, approaches, and give a recommendation. You can question any part of my thinking at any time.

---

## Step 2 — Identify technical challenges

Analyse the requirement against the existing codebase and identify:
- New infrastructure or data model changes needed
- Integration points with existing systems (auth, DB, APIs)
- Performance or scalability concerns
- Security considerations (auth, ownership, input validation)
- Frontend state complexity
- External dependencies or unknowns

Present these clearly:

> **Technical Challenges:**
> 1. …
> 2. …
>
> Any challenges I've missed that you're already aware of?

Wait for the developer's input before generating approaches.

---

## Step 3 — Generate approaches

Propose 2–3 distinct implementation approaches. For each:
- Name it clearly
- Describe how it works in 2–4 sentences
- List pros and cons
- Note the effort level (Low / Medium / High)

> **Approach A: <Name>**
> Description: …
> Pros: …
> Cons: …
> Effort: Medium
>
> **Approach B: <Name>**
> …

---

## Step 4 — Decision matrix

Score each approach against weighted criteria relevant to this problem:

| Criteria | Weight | Approach A | Approach B | Approach C |
|---|---|---|---|---|
| Complexity | 3 | 3/5 | 4/5 | 2/5 |
| Maintainability | 3 | 4/5 | 3/5 | 5/5 |
| Performance | 2 | 3/5 | 5/5 | 3/5 |
| Dev speed | 2 | 4/5 | 2/5 | 3/5 |
| Test coverage ease | 1 | 4/5 | 3/5 | 4/5 |
| **Total** | — | **32** | **30** | **29** |

Adapt criteria to what actually matters for this specific problem.

---

## Step 5 — Open discussion

Before recommending, explicitly invite challenge:

> Based on the matrix, I lean toward **Approach A**.
>
> Before I make a formal recommendation — do you see any angle I haven't considered? Any constraint (team familiarity, existing code, timeline) that should change the weighting?

Record any questions and answers in the Q&A log.

Wait for the developer's input.

---

## Step 6 — Recommendation

State the recommended approach and the reasoning:

> **Recommended: Approach A — <Name>**
>
> Because: <2–3 concrete reasons based on the matrix and discussion>
>
> Key risk to watch: <one honest risk>
>
> Confirm this direction before I write the brainstorm doc?

---

## Step 7 — Write the output document

Write to `docs/dev-brainstorm/<issue-number>.md`:

```markdown
# Dev Brainstorm: #<number> <title>
_Date: <today>_
_Source: docs/product-tasks/<issue-number>-refined.md (if exists)_

## Requirements Summary
<concise summary of what needs to be built>

## Technical Challenges
1. …
2. …

## Approaches Considered

### Approach A: <Name>
**Description:** …
**Pros:** …
**Cons:** …
**Effort:** Medium

### Approach B: <Name>
…

## Decision Matrix

| Criteria | Weight | A | B | C |
|---|---|---|---|---|
| Complexity | 3 | 3 | 4 | — |
| Maintainability | 3 | 4 | 3 | — |
| Performance | 2 | 3 | 5 | — |
| Dev speed | 2 | 4 | 2 | — |
| Test ease | 1 | 4 | 3 | — |
| **Weighted total** | — | **32** | **30** | — |

## Q&A Log

**Q:** <question>
**A:** <answer>

## Recommended Approach
**Approach A — <Name>**

Reasoning: …

Key risk: …

## Next Step
→ Run `/dev-design <issue-number>` to create the detailed implementation plan.
```

---

## Step 8 — Hand off

> Brainstorm saved to `docs/dev-brainstorm/<issue-number>.md`.
>
> Ready to create the implementation plan?
> ```
> /dev-design <issue-number>
> ```
