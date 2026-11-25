---
name: asd-ste100
version: 1.0.0
description: "Two branches: Rewrite (turns dense, confusing writing into clear, simple sentences — one meaning per word, one idea per sentence) and Check (flags STE violations without changing the text). Triggers: rewrite this clearly, make this simpler, plain english this, too complicated, explain simply, use simple sentences, check this for STE compliance, is this compliant."
---

# ASD-STE100: Flat Parse

## What "Flat Parse" Means

A **flat parse** is a sentence with exactly one valid parse: one way to read who does what to whom. Every ASD-STE100 rule eliminates a specific kind of ambiguity that would make a sentence parse in more than one way:

| The rule…                               | …removes this ambiguity                                                                   |
| --------------------------------------- | ----------------------------------------------------------------------------------------- |
| One approved meaning per word           | Lexical: is "check" a verb or a noun? Is "follow" "come after" or "obey"?                 |
| One part of speech per word             | Part-of-speech: is "oil" here a noun or a verb?                                           |
| Active voice in procedures              | Structural: who does the action?                                                          |
| Simple tenses only                      | Temporal: is the action still in progress or done?                                        |
| One instruction per sentence            | Scope: does "and then" start a new action or continue the first?                          |
| No omitted subjects, verbs, or articles | Referent: "the bolt and the stop" can mean the bolt AND the stop, or the bolt as the stop |
| Conditions before commands              | Dependency: does this condition apply to one action or to many?                           |
| Noun clusters ≤ 3 words                 | Grouping: which words modify which?                                                       |

When this skill says **"parse flat"** or **"flat parse"**, it means: the sentence passes all eight ambiguity tests above. It has one parse tree and the reader cannot mistake it for a different one.

## Branches

This skill has two execution modes. Pick one before you start:

| Branch      | When to use                                                                                                                                                  |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Rewrite** | User says "simplify this", "too complicated", "make this easier to understand", "rewrite this", "flat parse this": transforms input text into flat-parse STE |
| **Check**   | User says "check this for STE compliance", "is this compliant": flags violations and suggests rewrites, does not change the text                             |

Both branches share the same four steps below.

## Step 1: Classify Text Type

Every sentence is either **procedural** (tells the reader what to do) or **descriptive** (explains how something works, what happened, why). Classify before you rewrite. The sentence-length limits and voice rules differ.

| Sentence                                         | Type        | Signal                        |
| ------------------------------------------------ | ----------- | ----------------------------- |
| "Install the bracket."                           | Procedure   | Imperative verb, tells action |
| "The bracket holds the panel in position."       | Description | States function, third person |
| "Remove the four screws (2) from the cover (3)." | Procedure   | Imperative verb, tells action |
| "The system operates at 12 V DC."                | Description | States a characteristic       |

If the input mixes both types, separate them before rewriting: put procedures together, descriptions together. Do not rewrite a mixed passage as a single unit.

**Completion criterion:** Every sentence in the input is classified as procedure or description. Mixed passages are separated into distinct sections.

## Step 2: Analyze

Load `references/rules.md` and `references/dictionary.md`. Read them before you start the analysis. Then run three tests on every sentence.

**Test A: Every word has one job**

Check each word against `references/dictionary.md`:

- Is the word approved in the dictionary with the correct part of speech and meaning?
- If not approved, can you put it in one of the 22 technical noun categories?
- If not a technical noun, can you put it in one of the 4 technical verb categories?
- If none of these apply, replace it with an approved alternative.

**Test B: The structure parses flat**

Check against these rule categories from `references/rules.md`:

- Approved verb form only (imperative, simple present, simple past, simple future, infinitive, past participle as adjective)
- Active voice in procedures; active preferred in descriptions (passive only when agent is genuinely unknown)
- Approved modals only: CAN (ability, possibility, permission) and MUST (requirement). Not approved: may, might, shall, should, would. Do not use COULD to show possibility (it is a form of CAN, restricted).
- No -ing form as a verb (permitted only as technical noun or modifier within a technical noun)
- No omitted subjects, verbs, or articles
- Noun cluster ≤ 3 words (longer clusters must be broken with prepositional phrases)
- Conditions before commands ("If X, do Y", not "Do Y if X")
- One instruction per sentence in procedures

**Test C: The sentence is within bounds**

- ≤ 20 words (procedures) / ≤ 25 words (descriptions)
- ≤ 6 sentences per paragraph (descriptions)
- One topic per paragraph
- American English spelling per Merriam-Webster (so "colour" becomes "color", "centre" becomes "center", etc.)

For the **check** branch: flag each violation with the rule number, the offending text, and a compliant rewrite suggestion. Then stop. Do not modify the input.

For the **rewrite** branch: continue to Step 3.

**Completion criterion:** Every sentence in the input has been tested against all applicable rules. Every violation is identified. No sentence is skipped.

## Step 3: Rewrite Each Violation

Fix violations in this order. The sequence prevents wasted work: you fix structure before words, so you only check each word once.

1. **Verb form.** Convert non-approved modals to approved ones - may/might/shall/should/would → CAN or MUST (or the imperative in procedures); do not use COULD for possibility. ("You can adjust" is already valid STE; do not "fix" it.) Convert complex tenses ("has been installed" → "was installed" or "is installed"), and -ing verbs ("when you are doing" → "when you do").
2. **Voice.** Convert passive to active. Use one of four methods from `references/rules.md` (Section 3):
   - Move the agent (the object of "by") to subject position
   - Change an infinitive verb to an active verb
   - Use the imperative in procedures
   - Use "you" or "we" when the agent is the reader or your organization
3. **Word choice.** Replace non-approved words with approved alternatives. If no approved alternative carries the exact meaning, change the sentence construction instead of forcing a wrong word.
4. **Structure.** Split combined instructions into one per sentence. Move conditions before commands. Break noun clusters longer than 3 words with prepositional phrases. Restore omitted subjects, verbs, or articles.
5. **Cut to length.** If still over the word limit, split into more sentences. Never drop a condition, a scope qualifier, a safety instruction, or a number just to shorten a sentence. If splitting would lose precision, keep the longer version and flag the trade-off.
6. **Terminology sweep.** Call the same thing by the same name everywhere. If it's "inspect" on page one, don't switch to "examine" on page three — pick one and stay with it.
7. **Spelling.** Use American English (Merriam-Webster). Convert British spellings like "colour", "centre", or "organise" to their American forms unless an official directive says otherwise.

If the text contains safety instructions (WARNING or CAUTION): apply STE rules within the safety structure, but flag the changes for human review - legal departments may control warning text. (NOTE is not a safety instruction; it is governed by Rule 5.5.)

**Completion criterion:** Every violation from Step 2 is addressed. Every rewritten sentence preserves the original meaning: all conditions, scope qualifiers, safety warnings, and numbers are intact. Every sentence parses flat.

## Step 4: Verify

Load `references/checklist.md`. Run every item. Each rule must either pass or be flagged with a remaining violation. Check everything.

**Completion criterion:** All checklist items checked. Every violation is either resolved (rewrite branch) or reported with a suggested rewrite (check branch).

## Output

**Rewrite branch:** A before/after table.

| Rule violated                             | Original                                       | STE                                             |
| ----------------------------------------- | ---------------------------------------------- | ----------------------------------------------- |
| passive voice (procedural text): Rule 3.6 | "The valve must be closed before maintenance." | "Close the valve before maintenance."           |
| noun cluster > 3 words: Rule 2.1          | "engine oil temperature sensor housing"        | "housing for the engine oil temperature sensor" |

If the input already complies, say so. Do not force changes onto compliant text.

**Check branch:** A violations table with the rule number, the offending text, and a suggested rewrite. End with a summary: all clear, violations found but fixable, or needs human review.

## Reference Files

| File                       | When to load                                                                                  |
| -------------------------- | --------------------------------------------------------------------------------------------- |
| `references/rules.md`      | Step 2 (analysis) and Step 3 (rewriting): the full 53 rules with examples                     |
| `references/dictionary.md` | Step 2 word checks: approved words, 22 technical noun categories, 4 technical verb categories |
| `references/checklist.md`  | Step 4 verification: every rule to check                                                      |

Load only the file you need for the current step.
