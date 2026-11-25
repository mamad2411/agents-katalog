---
name: prd-review
description: Review a brief, PRD, or spec draft before anyone else sees it. Checks the argument, the evidence, and the user's own quality bar, then returns prioritized findings. Use when the user says "review this" about a product document.
---

# PRD review

Be the demanding colleague who reads the draft before the real audience does. Findings, not a rewrite.

## Steps

1. **Load the bar.** Read `context/preferences.md` (writing preferences and corrections log), `context/users.md` (who this is ultimately for), and the project's `brief.md` if the document belongs to a project.
2. **Read the document end to end** before flagging anything.
3. **Review against four lenses, in order of importance:**
   - **The problem.** Is it stated with evidence, or assumed? Would someone who disagrees be convinced there's a problem at all?
   - **The decision.** What is this document asking the reader to decide or accept? If you can't find it, that's the first finding.
   - **The evidence.** Every claim needs a source, a number, or a named observation. Flag each claim that has none.
   - **The edges.** What's out of scope, what could go wrong, what's the cost of being wrong? Silent edges get flagged.
4. **Check it against the user's own rules.** Anything in the corrections log that this draft violates gets flagged with the rule quoted.

## Output

Prioritized findings: must-fix first, then should-fix, then nits. Each finding quotes the passage, says what's wrong in one line, and proposes the concrete fix. Cap at ten findings; if there are more, the top ten are the review. End with the one-line verdict you'd give the user across a desk: ready to share, or not yet, and why.
