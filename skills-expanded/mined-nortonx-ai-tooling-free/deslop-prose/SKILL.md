---
name: deslop-prose
description: "Review a prose draft (report, doc, spec, ADR, PR description) before it is saved or sent: strip AI slop, catch pt-BR calques, gloss jargon, turn parallel structure into tables, enforce the length budget. For source code use `deslop`. Args: <file>"
argument-hint: "<file>"
---

# Deslop (prose)

Review gate for text, not code. `deslop` handles code; this handles anything a human will read as prose.

Run it on the **draft**, before writing to disk and before showing the user.

## Step 0: load the destination's own rules

If the target path is inside a tree that has a `CLAUDE.md` at its root (for example `docs/CLAUDE.md`), **read that file first**. It outranks everything below. Those files carry the project's own substitution tables, terminology bans, and glossary thresholds, and they are usually the only place a house rule is written down.

Skipping this step is the single most common way this gate fails. Do not skip it because the rules "look generic".

## Step 1: mechanical checks

Grep the draft. Any hit is a defect.

```bash
grep -nP '\x{2014}|\s-\s' <file>      # em dashes and spaced dashes
grep -niE 'robust|seamless|abrangente|poderoso|simplesmente|essencialmente|basicamente|obviamente|vale ressaltar|é importante notar|In this change'
```

Then run whatever verification greps the destination `CLAUDE.md` defines.

## Step 2: calques and jargon (pt-BR drafts only)

A literal translation that is grammatically valid can still be wrong. Check the destination's substitution table first, then these.

| English | Use | Avoid |
|---|---|---|
| harden / hardening (noun) | `hardening`, in italics | "endurecimento" |
| harden (verb) | "fazer o hardening de" | "endurecer" |
| finding (audit / security audit) | "achado", the established audit term | rewriting a documented audit glossary |
| finding (engineering investigation) | "o que foi encontrado" | "achado" as a generic heading |
| bypass | `bypass`, in italics | "contorno", "desvio" |
| pool / pooling | `pool`, in italics | "piscina", "agrupamento" |
| placeholder | `placeholder`, in italics | "marcador de posição" |

**Rule of thumb**: if the team says the English word out loud in a code review, keep the English word and italicize it. If nobody says it, translate the concept.

**Check the corpus before inventing a term.** Grep the destination tree for both candidates and follow what is already there, unless what is there is provably a repeated mistake.

## Step 3: gloss the jargon that is not an acronym

Glossary rules usually trigger on acronym count and therefore miss the terms that actually confuse people: library names, product names, and internal concept names.

Every **library**, **product** and **named concept** gets a one-line gloss at its first occurrence, or a row in the glossary table. Ask of each one: *would a competent dev outside this repo know what this is?*

Worked examples of failures this catches:

- "undici": a reader cannot tell it is the HTTP library built into Node that implements `fetch`.
- "agente interno": reads like an HTTP client. It is an `https.Agent`, a connection pool plus TLS options.

Glossing the term is not enough when the term is the crux of the document. If the whole point turns on *why* two things do not fit together, spend a short paragraph on the mechanism.

## Step 4: shape

- Parallel structure with 3 or more items becomes a **table**. Repeated `### file` headings with one paragraph each are parallel structure.
- No section the calling skill did not authorize. If a section feels necessary and is not on the list, ask instead of adding it.
- Respect the caller's line budget. Count the body, excluding frontmatter, and report the number.
- Every sentence carries a fact, a decision or a constraint. Delete the rest.

## Step 5: report

State what changed and the before/after line and word count. If the draft is over budget, say by how much and why, rather than cutting content the user explicitly asked for.

## Red Flags: STOP and fix

- Reviewing a doc bound for a tree with its own `CLAUDE.md` without having read it.
- Translating a technical term the team says in English.
- A library or product name appearing with no gloss.
- Three or more sibling sections with identical shape, left as headings.
- A section that the calling skill never listed.
- Claiming the review passed without running the greps.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "The tree's CLAUDE.md is probably generic" | It is where the house rules live. Read it. |
| "The corpus already uses this word 20 times" | Check whether those 20 came from the same generator. Frequency is not authority. |
| "Everyone knows what undici is" | The reader is a colleague in six months, not you today. Gloss it. |
| "The table would lose nuance" | Parallel content in headings loses more, and costs three times the lines. |
| "Two lines over budget is fine" | Say so out loud with the number. Silent overrun is how 45 becomes 80. |
| "It reads fine to me" | Read it aloud. If it would be awkward in a code review with senior peers, rewrite. |
