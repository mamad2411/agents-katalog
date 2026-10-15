---
name: gap-analysis-worksheet
description: Analyzes an initial business requirements document for gaps, ambiguities, and missing information. Generates gap-analysis-worksheet.md with structured requirement/question/answer blocks grouped by category — designed to be completed by a business analyst before formal requirements gathering begins.
---

# Gap Analysis Worksheet

Analyzes an initial requirements document for gaps, ambiguities, and missing information. Produces `gap-analysis-worksheet.md` — a structured worksheet for a business analyst to complete before proceeding to `/business-requirements-interview`.

## Purpose

Initial requirements from stakeholders typically contain:

- Vague or ambiguous statements
- Missing personas or user types
- Undefined scope boundaries
- Unstated assumptions
- Missing non-functional requirements
- Undefined success criteria

This skill surfaces those gaps as targeted questions, ensuring the formal requirements interview builds on validated, complete inputs.

## Prerequisites

- An initial requirements document in any format: plain text, Markdown, YAML, PDF summary, meeting notes, product brief, or similar

## Usage

```
/gap-analysis-worksheet path/to/requirements
```

## Process

### Step 1: Load & Read the Requirements

Read the input document in full. Identify all stated requirements, goals, personas, constraints, and assumptions.

### Step 2: Analyze for Gaps by Category

For each category below, scan the document and identify gaps. A gap is any of:

- **Missing** — Information that should be present but isn't stated at all
- **Ambiguous** — A statement that could be interpreted multiple ways
- **Incomplete** — A requirement that is only partially specified
- **Contradictory** — Statements that conflict with each other
- **Assumed** — Something implied but never explicitly stated

**Gap Categories (evaluate all ten):**

1. **Problem & Goals** — Is the core problem clearly defined? Are goals specific and measurable?
2. **Personas & Users** — Are all user types identified? Are their needs and pain points described?
3. **Scope** — What is explicitly in scope vs. out of scope? Where are the boundaries?
4. **Functional Requirements** — Are all features described with enough detail to build? Are edge cases addressed?
5. **Non-Functional Requirements** — Performance, security, scalability, accessibility, reliability expectations?
6. **Success Criteria** — How will success be measured? What does "done" look like?
7. **Assumptions** — What is being assumed but not stated? What dependencies are implied?
8. **Constraints** — Technical, timeline, budget, regulatory, or team constraints?
9. **Dependencies & Integrations** — External systems, APIs, third-party services, or team dependencies?
10. **Risks** — What could go wrong? Are any mitigation strategies needed?

Skip any category that has **no gaps** — do not include empty sections in the output.

### Step 3: Write gap-analysis-worksheet.md

Write `gap-analysis-worksheet.md` in the same directory as the input requirements document.

## Output Format

```markdown
# Gap Analysis Worksheet

**Document:** [path to requirements file]
**Generated:** [date]
**Status:** Awaiting Review
**Total Gaps:** [n]

---

## [Category Name]

### Gap [n]

**Requirement:** "[exact snippet or brief reference to the relevant requirement, or 'Not addressed' if entirely missing]"
**Question:** [A specific, answerable question that surfaces the gap]
**Answer:**

---

### Gap [n+1]

**Requirement:** "[...]"
**Question:** [...]
**Answer:**

---

## [Next Category]

...
```

Gaps within each category should be ordered by importance — critical questions first, minor clarifications last.

## Writing Good Gap Questions

**Be specific** — Reference the exact requirement or missing area.

> Good: `What is the maximum file size a user can upload?`
> Bad: `Are there any limits?`

**Be answerable** — The business analyst should be able to respond with a concrete answer.

> Good: `Should unauthenticated users be able to view public workflows, or is login required for all access?`
> Bad: `What about authentication?`

**One gap per question** — Do not combine multiple gaps into one question.

> Good: `What should happen when a workflow task fails — should the entire workflow stop, or continue with remaining tasks?`
> Bad: `What should happen with errors and timeouts and retries?`

**Prioritize critical gaps** — Questions about core functionality, personas, and scope come before nice-to-have clarifications.

## Requirement Snippet Guidelines

- Use a direct quote from the document when possible — keep it under 15 words
- If the gap is about something entirely missing, use: `"Not addressed in requirements"`
- If the gap applies to a whole section rather than a specific line, reference the section: `"[Goals section]"`

## Example Output

See [examples/gap-analysis-worksheet.md](./examples/gap-analysis-worksheet.md) for a complete sample based on [examples/sample-requirements.md](./examples/sample-requirements.md).

## Self-Review

After generating the worksheet, perform the following checks and output a brief summary inline.

### Checks

- [ ] All 10 categories were evaluated (skipped categories had no gaps worth capturing)
- [ ] Every question is specific and answerable by a business analyst
- [ ] No two questions address the same gap
- [ ] Critical gaps (scope, personas, core functionality) are listed first within their category
- [ ] Requirement snippets accurately reflect the source document
- [ ] No category with real gaps was omitted

### Inline Summary

```
## Worksheet Summary

**Input:** [requirements file]
**Output:** gap-analysis-worksheet.md
**Total Gaps Found:** [n]

By Category:
  Problem & Goals:              [n gaps or "✓ no gaps"]
  Personas & Users:             [n gaps or "✓ no gaps"]
  Scope:                        [n gaps or "✓ no gaps"]
  Functional Requirements:      [n gaps or "✓ no gaps"]
  Non-Functional Requirements:  [n gaps or "✓ no gaps"]
  Success Criteria:             [n gaps or "✓ no gaps"]
  Assumptions:                  [n gaps or "✓ no gaps"]
  Constraints:                  [n gaps or "✓ no gaps"]
  Dependencies & Integrations:  [n gaps or "✓ no gaps"]
  Risks:                        [n gaps or "✓ no gaps"]

Next step → Complete the worksheet, then run:
  /business-requirements-interview
```
