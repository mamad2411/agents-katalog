---
name: simplified-technical-english
description: Write clear, unambiguous English for technical documentation using Simplified Technical English principles (adapted from ASD-STE100 Issue 9). Use this skill whenever you write or review PR descriptions, commit bodies, READMEs, API documentation, ADRs, changelogs, runbooks, error messages, migration guides, code comments, or release notes — and any time the audience includes non-native English readers or machine translation. Also use it when the user asks for "STE", "ASD-STE100", "simplified English", "plain technical English", or asks to make documentation clearer, shorter, or easier to translate.
---

# Simplified Technical English for software documentation

## What this is

Simplified Technical English (STE) is a controlled natural language: a restricted
vocabulary plus a set of writing rules. The authors built it so that a
maintenance technician in Jakarta and one in Toulouse read the same sentence
and reach the same conclusion. It removes ambiguity rather than making prose pretty.

This skill adapts those principles to software documentation. It is an
independent adaptation, not the specification. Rule numbers such as `[3.6]`
point back to ASD-STE100 Issue 9 (© ASD) for traceability. ASD holds the
copyright on the official dictionary and on the rule text, so this skill does
not reproduce them. See
`references/rule-index.md` for the full tag list.

## When to apply it, and when not to

Apply it to: PR descriptions, commit bodies, ADRs, READMEs, API reference,
runbooks, incident postmortems, migration guides, error and log messages,
changelogs, code comments, onboarding docs.

Do not apply it to: marketing copy, blog posts, conference talks, anything where
voice and rhythm matter more than a single interpretation. STE deliberately
sounds flat. The flatness is the point. STE is the wrong tool for
persuasion.

Half-application is worse than none. If a document is in scope, apply the rules
throughout it, not to selected paragraphs.

## How to use this skill

Choose the workflow that matches the request.

**The user writes something new.** Apply the core rules below as you draft. Do
not draft first and clean up after. Check the result against
`references/review-protocol.md`, section "Self-check".

**The user asks you to review or rewrite an existing text.** Follow
`references/review-protocol.md`. Report concrete edits, not general advice.

**The text is a specific artifact** (commit, PR, ADR, runbook, error message,
changelog, code comment). Read `references/artifacts.md` for the rules that are
specific to that artifact.

**You need a word.** Read `references/word-substitutions.md`. The table gives
one short word for each meaning. It also lists the words that cause the most
trouble in software writing.

**You want a mechanical check.** Run the linter:

```bash
python3 scripts/ste_lint.py --mode auto docs/**/*.md
```

The linter finds what a machine can find. It checks sentence length,
semicolons, Latin abbreviations, contractions, passive constructions,
nominalizations, phrasal verbs, long noun groups, and terminology drift. The
linter cannot judge whether a sentence carries one idea. Run it as a first
pass, then read the text yourself. See
`references/linter.md` for the rule codes, the configuration file, and the
suppression comments.

## The two modes

Every technical text is either **procedural** (it tells the reader to do
something) or **descriptive** (it tells the reader how something is). The rules
differ. Decide which mode a block is in before you write it.

| | Procedural | Descriptive |
|---|---|---|
| Verb form | Imperative `[5.3]` | Indicative. No imperative `[6.x]` |
| Max sentence length | 20 words `[5.1]` | 25 words `[6.3]` |
| Typical artifacts | Runbooks, setup steps, CONTRIBUTING | ADRs, architecture docs, API concepts |

A README usually contains both. Switch mode per section, not per sentence.

## Core rules

### One idea per sentence, one topic per paragraph

Write short sentences with a clear structure `[4.1]`. In procedures, write one
instruction per sentence, unless two actions must happen simultaneously `[5.2]`.
In descriptive text, give each sentence a single subject and build up
information gradually `[6.1]`. Each paragraph covers one topic `[6.5]` and holds
no more than six sentences `[6.6]`.

```
Avoid: The migration script reads the legacy table, maps the columns to the new
       schema, and then writes to the target database, but if a row fails
       validation it is written to a dead-letter table instead.

Write: The migration script reads the legacy table. It maps each column to the
       new schema. Then it writes the mapped rows to the target database. If a
       row fails validation, the script writes that row to the dead-letter table.
```

### Active voice

Use the active voice `[3.6]`. Passive voice is allowed only in descriptive text,
and only when the agent is genuinely unknown. Two examples hide who acted:
"It was decided" and "the schema was changed". <!-- ste-disable-line STE002 -->
A reader of an ADR or a postmortem needs exactly that information.

```
Avoid: The connection pool was exhausted and the requests were rejected.
Write: The connection pool ran out of connections. The gateway then rejected
       the requests.
```

### The action is a verb, not a noun

Do not turn actions into nouns `[3.7]`. Nominalization is the single most common
failure in developer writing.

```
Avoid: Perform a validation of the payload before the invocation of the handler.
Write: Validate the payload before you call the handler.

Avoid: This change is a refactoring of the authentication module.
Write: This change refactors the authentication module.
```

### Simple verb forms only

Use the infinitive, the imperative, the simple present, the simple past, the
simple future, and the past participle as an adjective `[3.2]`. Do not stack
auxiliaries into complex constructions `[3.4]`. No continuous tenses, no perfect
tenses, no conditional chains.

```
Avoid: The worker will have been retrying the job for up to five minutes.
Write: The worker retries the job for a maximum of five minutes.

Avoid: This would have caused the cache to be invalidated.
Write: This invalidates the cache.
```

Use the `-ing` form only as a noun or as a modifier inside a noun `[3.5]`:
"logging level" is correct, "the service is starting" is not. <!-- ste-disable-line STE004 -->
Write "the service starts".

### Short noun groups

Write compound nouns of three words at most `[2.1]`. A longer chain forces the
reader to guess how the words attach to each other. If a term genuinely needs
more words, write it in full one time. Then define a short form, or hyphenate
the parts that belong together `[2.2]`.

```
Avoid: user session token refresh endpoint configuration
Write: the configuration of the token-refresh endpoint
```

### Say the words you left out

Do not drop words to shorten a sentence, and do not use contractions `[4.2]`.
Keep the conjunction "that". It marks where the main clause ends, and many
languages cannot omit it `[GR-1]`. Keep articles and demonstratives before nouns
`[4.5]`.

```
Avoid: Make sure the flag's enabled before deploy.
Write: Make sure that the flag is enabled before you deploy.
```

### Conditions come first

When the reader must know a condition before acting, put the condition at the
start of the sentence and separate it with a comma `[5.4]`. The reader reaches
a condition placed after the command too late.

```
Avoid: Delete the temporary volumes if the pipeline failed.
Write: If the pipeline failed, delete the temporary volumes.
```

### Vertical lists for anything complex

Turn dense text into a vertical list `[4.3]`. Lists are easier to scan, and they
make each item independently checkable. Keep list items parallel: same verb
form, same structure.

### No semicolons

The semicolon is not permitted `[8.1]`. It joins long sentences, and the rules
exist to prevent long sentences. Write two sentences.

Hyphens bind words that are directly related `[8.2]`, especially compound
modifiers before a noun: `read-only replica`, `zero-downtime migration`,
`token-refresh endpoint`.

### Pronouns must be unambiguous

If a pronoun could point at more than one noun, repeat the noun `[GR-3]`. Pay
special attention to "this" at the start of a sentence. It very often refers to
a whole preceding clause, which the reader has to reconstruct `[GR-4]`.

```
Avoid: The job writes to the queue and the consumer reads from it. This can fail.
Write: The job writes to the queue. The consumer reads from the queue. The write
       operation can fail.
```

### No Latin abbreviations

Do not write `e.g.`, `i.e.`, `etc.`, `via`, `N.B.`, `vs.` `[GR-6]`. Write "for
example", "that is", "and other <things>", "through", "note", "compared with".

### One term per concept, always

Never use two different terms for the same thing `[1.11]`, and keep terminology
and style consistent across a document set `[9.4]`. In software this is the
highest-value rule: if the entity is a `tenant` in the code, it is a `tenant` in
the docs. It is not an "org", not a "workspace", not an "account".

Pick American spelling unless a house style says otherwise `[1.14]`.

### Gender-neutral language

Use neutral terms and constructions `[GR-7]`. Address the reader as "you". Use
"they" for an unspecified person, or restructure to avoid the pronoun.

### Word budget

Sentence limits are 20 words for procedures and 25 for descriptive text and for
notes. When you count `[8.4]`–`[8.7]`:

- A number, or a number with its unit, counts as one word: `500 ms`, `2 GB`
- An abbreviation counts as one word: `HTTP`, `JWT`
- An alphanumeric identifier counts as one word: `PR-4821`, `v2.1.0`
- Quoted text counts as one word
- Anything in parentheses counts as one word
- A hyphenated word counts as one word
- Headings, titles, and labels count as one word
- In a vertical list, the colon ends the sentence for counting purposes

## Vocabulary

STE's real enforcement mechanism is its dictionary: one approved word per
meaning, and one meaning per approved word. ASD holds the copyright on that
dictionary, so this skill does not reproduce it. Two things you can do without
it:

1. Apply the principle. Choose the shortest common word that carries the
   meaning, and use it with only one meaning throughout the document.
2. Use `references/word-substitutions.md` in this skill. The table covers
   software writing, and it lists the terms that cause the most trouble in
   developer documentation.

If the project needs formal conformance (aerospace, defense, regulated
industry), the licensed specification and a checker such as HyperSTE or
Congree are required. This skill does not produce certified STE.

## Warnings and cautions

For anything destructive or dangerous, use a signal word that matches the level
of risk `[7.1]`. Start with the command or the condition `[7.2]`. Then explain
the consequence `[7.3]`. In the source standard, a warning covers injury and a
caution covers damage to equipment. The software equivalent:

- **WARNING** — irreversible data loss, security exposure, production outage
- **CAUTION** — recoverable damage, degraded service, cost impact

```
WARNING: Before you run this migration, take a full database snapshot. This
         migration drops the legacy tables and you cannot undo it.
```

Never bury a destructive consequence in the middle of a paragraph.

## Review procedure

The short form is below. The full protocol, the report format, and the
severity model are in `references/review-protocol.md`.

1. Split every sentence that carries more than one idea.
2. Convert passive constructions to active, and name the agent.
3. Convert nominalizations back into verbs.
4. Reduce complex verb constructions to simple tenses.
5. Cut noun groups down to three words or fewer.
6. Move conditions to the front of their sentence.
7. Replace ambiguous pronouns with the noun.
8. Remove semicolons and Latin abbreviations.
9. Unify terminology. List every concept that appears under more than one name.
10. Check sentence length against the 20/25-word budget.
11. Restore omitted "that", articles, and demonstratives.

If a word-for-word substitution does not produce a correct sentence, rewrite the
whole sentence `[9.1]`. Do not force a bad sentence to survive.

## Files in this skill

| File | Use it when |
|---|---|
| `references/word-substitutions.md` | You need one approved word for a meaning |
| `references/rule-index.md` | You need the meaning of a `[x.y]` tag |
| `references/artifacts.md` | You write a commit, PR, ADR, runbook, or error message |
| `references/review-protocol.md` | You review or rewrite an existing text |
| `references/linter.md` | You run, configure, or extend `ste_lint.py` |
| `scripts/ste_lint.py` | You want a mechanical first pass |

## What this does not cover

STE says nothing about document structure, formatting, heading hierarchy, or
information architecture. It governs sentences. Pair it with a style guide for
everything above sentence level.
