---
name: lawstu-legal-writing
version: 1.0.0
description: Coach your legal writing — memos and briefs — on CREAC structure, rule synthesis, and citation, critiquing your draft without rewriting it.
author: matrixx0070
tags: [law-student, legal-writing, creac, memo, brief]
capabilities: []
---

## When to use

Reach for this when you have drafted a legal memo, brief, or writing assignment and want a rigorous critique — structure, rule synthesis, application depth, and citation form. The skill reads *your* draft and tells you where an editor or professor would mark it up.

**Not for:** writing the assignment for you. On graded 1L legal-writing and journal work this is the bright line: the skill critiques and asks questions, it never drafts, rewrites, or supplies sentences you paste in as your own. That would be plagiarism and defeats the purpose. Not for exam IRAC (see `lawstu-irac-practice`) or oral prep (see `lawstu-cold-call-prep`).

## Method

1. **State the assignment type and audience.** A predictive memo (objective) reads differently from a brief (persuasive). Decision point: if audience is a court, tone shifts to advocacy — flag any hedging.
2. **Check the macro-structure.** Question presented → brief answer → facts → discussion (CREAC per issue) → conclusion. The skill flags missing or out-of-order pieces.
3. **Audit rule synthesis.** Are rules stated from multiple authorities and reconciled, or just quoted? It points to thin synthesis; you fix it.
4. **Test the application.** Every rule proposition must connect to a client fact, with counterargument addressed. It marks conclusory sentences for you to rework.
5. **Citation pass.** Flags obviously non-conforming cites (missing pincite, wrong signal) against Bluebook conventions — you correct them.
6. **Line-level flags.** Passive voice, legalese, and buried holdings get marked, not rewritten.

## Example

Your discussion opens "The court will likely rule for our client because the facts are strong." The skill flags: no rule stated, conclusory, no authority. Coaching prompt: "Lead the paragraph with the synthesized rule from *Case A* and *Case B*, then apply the specific facts — which two facts carry the most weight?" You do the rewriting.

## Pitfalls

- Rule-then-nothing paragraphs with no fact application.
- Persuasive tone in an objective memo (or vice versa).
- String-citing without synthesizing the rule the cases share.
- Treating critique as a rewrite request — do the revision yourself.

## Output format

```
Assignment type | audience | issue(s)
Macro-structure check: [present / missing pieces]
Per issue (CREAC):
  Conclusion | Rule (synthesis quality) | Explanation | Application (gaps) | Conclusion
Citation flags: [non-conforming cites]
Line flags: passive | legalese | conclusory
Revision to-do (yours to execute):
```

## Reference

- **CREAC:** Conclusion → Rule → Explanation (rule proof from authority) → Application → Conclusion; the standard memo/brief structure.
- **IRAC** is the exam cousin; CREAC front-loads the conclusion for readers who scan (`lawstu-irac-practice`).
- **Citation:** Bluebook conventions — pincites, signals, short forms.
