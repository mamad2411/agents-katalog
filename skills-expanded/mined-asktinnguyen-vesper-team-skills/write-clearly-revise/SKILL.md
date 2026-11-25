---
name: write-clearly-revise
description: "Revision and multi-review validation for substantive human-facing narrative, marketing, editorial, rhetorical, or stakeholder prose already routed through the write-clearly family. Runs Abbott's words, word-order, and brevity passes, then clarity, brevity, evidence, and red-team review. Use only when the user explicitly requests rigorous validation or when an in-scope, high-stakes prose deliverable clearly warrants it. Do not invoke for agent or system prompts, operational instructions, runbooks, coding tasks, technical troubleshooting, status updates, ordinary chat replies, commit messages, short utility text, or merely because another skill produced a draft."
license: MIT
metadata:
  hermes:
    tags: [writing, revision, editing, validation, subagents, composition]
    related_skills: [write-clearly, write-clearly-words, write-clearly-word-order, write-clearly-brevity]
---

# Write Clearly — REVISE (self-critique + multi-subagent validation)

This is the workflow to run an in-scope human-facing prose draft through Abbott's rules to a verified result. It has
three stages: **(A) checklist revision**, **(B) self-critique against the source**, and
**(C) multi-subagent validation**. It works for prose, essays, emails, documentation,
articles, narrative marketing, speeches, editorial copy, and stakeholder communications.
It does not apply to agent or system prompts, operational instructions, runbooks, coding
tasks, technical troubleshooting, status updates, ordinary chat replies, commit messages,
or short utility text unless the user explicitly invokes `write-clearly-revise`.

## A. Checklist revision (three passes)

Load the relevant part skills and make three passes. Do NOT mix passes; each has a single
lens, so violations surface cleanly.

**Pass 1 — WORDS (load `write-clearly-words`).** For each sentence, check Rules 1–14b:
exact sense (1); no exaggeration (2); no circumlocution/"fine writing" (3); the small words
*not/and/any/only/that* unambiguous (4, 4a); pronouns have one clear antecedent (5);
reported speech clear (6–6b); participles explicit (7); who/which vs that right, no "and
which" (8, 9); relative equivalents not causing ambiguity, antecedent repeated (10, 10a');
particular terms where they add force (11, 12); verbal nouns avoidable (11a); metaphors
unmixed and apt (13–14b).

**Pass 2 — WORD ORDER (load `write-clearly-word-order`).** For each sentence, Rules 15–45:
emphatic words at start/end (15–15b); emphatic subject/object placed deliberately (16, 17);
one clear strongest emphasis (18); related words adjacent (19–25); no harmful parentheses
(26); conditionals and "that"-clauses and infinitives kept distinct (27–29); suspense held,
not over-held, if-clauses first, no trailing "not…/which…" (30–34); subjects, prepositions,
conjunctions, verbs repeated where omission muddies (35–38); climax not bathos (39–40);
no unexpected construction change (40a); antithesis/epigram in reach (41–42); one principal
subject per sentence (43); sentences visibly connected (44–45).

**Pass 3 — BREVITY (load `write-clearly-brevity`).** Rules 46–56: compress via metaphor,
word-for-phrase, participles, implication, apposition, condensation — but **clearness first**
(56). Delete tautology in both senses (same word, same meaning) (54).

For each violation produce: the original text, the rule number, and the rewrite. Rewrites
must fix the flagged defect without introducing a new one.

## B. Self-critique against the source

Before shipping, challenge your own rewrites:
1. **Faithfulness check:** for every rule/example you cited, verify the wording against
   `write-clearly/references/how-to-write-clearly.txt` (the verbatim book text). Flag any
   paraphrase that changed Abbott's meaning.
2. **Clarity-vs-brevity check:** for every Brevity edit, confirm you did not sacrifice clarity.
3. **Did-rewrite-introduce check:** read each rewrite as if you were a hostile reader — does
   the "fix" create a new ambiguity (e.g. a pronoun now dangling, an adverb now misplaced)?
4. **Emphasis check:** confirm each sentence still has one clear principal subject and a
   deliberate emphasis position.

## C. Multi-subagent validation orchestration

Spawn **independent** subagents in parallel via `delegate_task` (batch mode, up to 3 at
once — run two batches for 4 roles). Give each the full source text path, the original
draft, and your revised draft. Each returns claims + verdicts; you must verify their
outputs (subagent self-reports are not proof — check their cited rule numbers and page
quotes against the reference file yourself before trusting them).

**Role 1 — CLARITY reviewer:** Is the revised text unambiguous at word and sentence level?
Flag any pronoun, "only/not/that/and/or", dangling modifier, or misplaced adverb. Cite
rule numbers (1, 4, 5, 8, 20, 21, 25…).

**Role 2 — BREVITY reviewer:** Is the revision needlessly wordy anywhere? Flag tautology
(54) and any phrase compressible to a word (47a). But confirm none of its cuts harmed
clarity (56).

**Role 3 — EVIDENCE reviewer:** Verify every example and every rule-reference in the
deliverable matches the source text verbatim (check against the reference file). Report
exact mismatches; do not assume the writer was right.

**Role 4 — RED-TEAM challenger:** Attempt to MISREAD the revised text. Give the most
plausible wrong interpretation of each complex sentence. If a sentence can be read two
ways, it fails — cite the offending rule (5, 8, 21, 25, 30a, 43…).

### Adjudication
- If any role reports a clear violation you agree with, fix it, then re-run the relevant
  reviewers once (do not loop indefinitely).
- If a role's claim does not survive your own check of the cited rule against the source,
  record it as rejected with the reason.
- Emit a final **verdict table**: rule / original / revised / reviewer / accepted-or-rejected.
- Deliver the revised text only after roles 1–4 are clean or their findings adjudicated.

## Notes
- The full book text is available at `write-clearly/references/how-to-write-clearly.txt`
  for verbatim quoting and verification by every subagent.
- Keep subagent contexts self-contained: pass in the draft text and the reference path;
  they do not share your conversation.
- This workflow is itself recursive in spirit — if your final prose is long, run the same
  three passes on it. Abbott's Rule 56 is the guardrail: never let any process, brevity
  included, obscure the meaning.
