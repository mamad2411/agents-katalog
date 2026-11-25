---
name: write-clearly
description: "Clear-writing framework derived from Edwin A. Abbott's 'How to Write Clearly' (1883), for substantive human-facing prose such as narrative marketing, articles, essays, speeches, editorial copy, and stakeholder communications. Use when the user explicitly requests this framework or when the primary deliverable is substantial audience-facing prose that needs clarity, force, or literary revision. Routes to write-clearly-words, write-clearly-word-order, write-clearly-brevity, and write-clearly-revise. Do not invoke for agent or system prompts, operational instructions, runbooks, coding tasks, technical troubleshooting, status updates, ordinary chat replies, commit messages, or short utility text unless the user explicitly names this skill. Do not infer activation merely because a task involves drafting, editing, or revision."
license: MIT
metadata:
  hermes:
    tags: [writing, clarity, composition, editing, rhetoric, prose]
    related_skills: [write-clearly-words, write-clearly-word-order, write-clearly-brevity, write-clearly-revise]
---

# Write Clearly (Abbott)

## Activation boundary

Use this family for substantive prose written for human readers, especially narrative,
marketing, editorial, rhetorical, or stakeholder communication. Do not use it for agent
prompts, system prompts, operational recovery instructions, runbooks, coding instructions,
technical troubleshooting, status messages, ordinary assistant replies, commit messages,
or other short utility text unless the user explicitly invokes `write-clearly`.

The presence of words such as *write*, *draft*, *edit*, *revise*, *clarify*, or *prompt*
does not activate this skill by itself. When the requested artifact primarily instructs a
machine or coordinates technical work, use the task's technical workflow instead.

This is the router and index for the **write-clearly** family. It encodes the complete
method of *How to Write Clearly: Rules and Exercises on English Composition* by
Edwin A. Abbott (1883) — 56 numbered rules for clear, forcible English prose.

Abbott's core claim: **clear writing is largely a mechanical matter of word placement —
adverbs, conjunctions, prepositions, and auxiliary verbs placed and repeated per definite
rules.** It is teachable and checkable, unlike force, which depends on thought and
imagination. Every rule below exists to remove *ambiguity* (clearness) or to add *force*.

## The framework: 56 rules in two divisions

Abbott's rule index groups the 56 rules under **two divisions**: *I. CLEARNESS AND FORCE*
(covering WORDS and ORDER OF WORDS) and *II. BREVITY*. The three skills below mirror the
three subsections of the index.

**WORDS** (Rules 1–14b) → see `write-clearly-words`
Choose words for exact sense, avoid exaggeration and circumlocution, watch tricky small
words (*not/and/any/only/that*), keep pronouns unambiguous, use relative pronouns
correctly (who/which vs that), prefer particular to general terms, and manage metaphor.

**ORDER OF WORDS IN A SENTENCE** (Rules 15–45) → see `write-clearly-word-order`
Put emphatic words in emphatic positions, keep related words close, use suspense to hold
the reader, repeat subjects/prepositions/conjunctions where omission causes ambiguity,
build climax (not bathos), and give each sentence one principal subject.

**BREVITY** (Rules 46–56) → see `write-clearly-brevity`
Prefer brief forms (metaphor, general terms, single words, participles, apposition), strip
tautology — but *let clearness be the first consideration* (Rule 56).

**Revision & validation** → see `write-clearly-revise`
Run any draft through Abbott's rules as a checklist, criticize it against the source text,
and validate it with a multi-subagent orchestration (clarity, brevity, and evidence
reviewers).

## Master index of rules

**WORDS**
- 1 Use words in their proper sense.
- 2 Avoid exaggerations.
- 3 Avoid useless circumlocution and "fine writing."
- 4 Be careful with "not…and," "any," "but," "only," "not…or," "that."
- 4a Be careful with ambiguous words, e.g. "certain."
- 5 Be careful with "he," "it," "they," "these," &c.
- 6 Report a speech in the First Person where necessary to avoid ambiguity.
- 6a Use the Third Person where the exact words are not intended.
- 6b Omission of "that" in a speech in the Third Person.
- 7 Show clearly what a Participle (implying when/while/though/that) implies.
- 8 Use "who"/"which" if the meaning is "and he/and it, for he/for it"; otherwise use "that" if euphony allows.
- 9 Do not use "and which" for "which."
- 10 Equivalents for the Relative (participle, infinitive, whereby, if, and this, what, omission).
- 10a' Repeat the Antecedent before the Relative where non-repetition causes ambiguity.
- 11 Use particular for general terms. Avoid abstract nouns.
- 11a Avoid Verbal Nouns where Verbs can be used.
- 12 Use particular persons instead of a class.
- 13 Use metaphor instead of literal statement.
- 14 Do not confuse metaphor.
- 14a Do not mix metaphor with literal statement.
- 14b Do not use poetic metaphor to illustrate a prosaic subject.

**ORDER OF WORDS**
- 15 Emphatic words in emphatic positions (start or end of sentence).
- 15a Keep unemphatic words from the end.
- 15b An interrogation sometimes gives emphasis.
- 16 An unusually emphatic Subject is often removed from the beginning.
- 17 The Object is sometimes placed before the Verb for emphasis.
- 18 Where several words are emphatic, make clear which is the most emphatic.
- 19 Words must be near the words they are grammatically connected with.
- 20 Adverbs placed next to the words they qualify.
- 21 "Only" should be placed before the word it affects.
- 22 After "not only…but also," each must be followed by the same part of speech.
- 23 "At least," "always," &c. sometimes produce ambiguity.
- 24 Nouns placed near the nouns they define.
- 25 Pronouns follow the Nouns they refer to, without another Noun intervening.
- 26 Connected clauses kept close; avoid parentheses (but see 55).
- 27 In conditionals, keep antecedent ("if") clauses distinct from consequent clauses.
- 28 Dependent "that" clauses kept distinct from independent ones.
- 29 Infinitives dependent on the same word kept distinct from others.
- 30 The principle of Suspense.
- 30a Don't end a long sentence with a short unemphatic clause in "not…" or "which…".
- 31 Suspense must not be excessive.
- 32 In "if/when/though" sentences, put the if-clause (protasis) first.
- 33 Suspense via a Participle/Adjective that qualifies the Subject, placed before it.
- 34 Suspensive Conjunctions (either, not only, on the one hand) add clearness.
- 35 Repeat the Subject where omission would cause ambiguity.
- 36 Repeat a Preposition after an intervening Conjunction.
- 37 Repeat Conjunctions, Auxiliary Verbs, Pronominal Adjectives.
- 37a Repeat Verbs after "than," "as," &c.
- 38 In long sentences repeat the Subject or a summary of what was said.
- 39 Clearness through a rising structure — "climax."
- 40 An unexpected descent — "bathos" — causes feebleness.
- 40a Do not introduce a new construction unexpectedly.
- 41 Antithesis adds force and often clearness.
- 42 Epigram.
- 43 Let each sentence have one, and only one, principal subject of thought.
- 44 Keep the connection between sentences with connecting words at the start.
- 45 A short intervening sentence may be needed between two long ones.

**BREVITY**
- 46 Metaphor is briefer than literal statement.
- 47 General terms are briefer, though less forcible, than particular terms.
- 47a A phrase may be expressed by a word.
- 48 Participles as brief equivalents of conjunction+verb phrases.
- 49 Participles/Adjectives as equivalents of relative phrases.
- 50 A statement may be briefly implied instead of expressed at length.
- 51 Conjunctions may be omitted.
- 51a The imperative may be used for "if."
- 52 Apposition may convert two sentences into one.
- 53 Condensation by not repeating a common Subject/Object.
- 54 Tautology — avoid unnecessary repetition (of word or of meaning).
- 55 Parenthesis may aid brevity.
- 56 Caution: let clearness be the first consideration.

## Quick routing

- **I'm writing something fresh** → load `write-clearly` (+ relevant part skills), draft with the rules in mind, then run `write-clearly-revise`.
- **I'm editing/revising a draft for clarity** → go straight to `write-clearly-revise`.
- **A draft has a word/choice problem** → `write-clearly-words`.
- **A draft reads muddled at sentence level** → `write-clearly-word-order`.
- **A draft is wordy** → `write-clearly-brevity`.

## Reference

- `references/how-to-write-clearly.txt` — the full extracted public-domain text of Abbott's book (all 56 rules with original examples and exercises). Quote the book verbatim from here when an example or rule wording is needed.
