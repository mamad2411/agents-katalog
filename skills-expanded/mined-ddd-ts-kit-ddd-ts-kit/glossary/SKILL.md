---
name: glossary
description: >-
  Use when a business term is missing, ambiguous or has two meanings, when the generator or
  language/glossary-term refuses a name, when a CONTEXT.md is empty or stale, or for the
  glossary step of a new project. Ubiquitous language, one row per term.
argument-hint: "[context]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(npx ddd-ts-kit list *)
  - Bash(npx ddd-ts-kit docs)
  - Bash(npx ddd-ts-kit check *)
---

# Ubiquitous language

Context: `$ARGUMENTS` (every context of `docs/architecture/contexts.md` when empty)

The glossary is the source of every class, method, event, command and permission name. The
generator refuses a name whose words it does not define, and `language/glossary-term` fails
the check. A refusal class is named from it too (`SlotTaken`: `Slot`, `Take`), with the
qualifiers of a refusal besides: `invalid`, `unknown`, `already`, `too`, `no`, `missing`,
`required` (`BookingTooLate`, `InvalidAppointment`).

The boundary of a context itself is skill `ddd-ts-kit:bounded-contexts`.

## Where it is written

| Project state | File |
|---|---|
| before the bootstrap | `docs/architecture/glossary.md`, one section per context; the bootstrap turns each row into a `--term "<Term>=<meaning>\|<not to be confused with>"`, three cells kept, and deletes the file |
| after | `src/contexts/<context>/CONTEXT.md`, section `## Ubiquitous language`; there is no second copy |
| a value two contexts share | `<sharedKernelDir>/CONTEXT.md` (`src/shared-kernel/CONTEXT.md`), the glossary of the shared kernel: its first `generate value-object shared-kernel <Name> --term ...` creates it, and `language/glossary-term` names the value objects and refusals of the shared kernel after it. A word with another meaning in one context stays in that context's glossary |

## A context a preset writes

A context that `generate context <name> --preset <preset>` will write (today `identity`) takes
the preset's glossary as its draft, not an empty one: its terms are in
[identity-preset.md](identity-preset.md), next to this skill, the rows the preset writes into its
CONTEXT.md word for word (before the bootstrap the project has no CLI to read them from). Keep
the preset's word for each concept it names
(`Organisation` is the tenant, `Member` a membership), and add only the business terms beyond it,
one row each. The preset's terms win: the glossaries downstream refer to them.

## Collect the terms

From the discovery timeline (or from the owner), for one context at a time:

- each **noun** the business uses: candidates for aggregates, entities, value objects;
- each **verb**: candidates for commands and intention methods (`place`, `cancel`, `issue`);
- each **fact**, in the past tense: candidates for events (`placed`, `cancelled`);
- each **role** that acts.

For each, one sentence of meaning **in this context**, and for a word a neighbour also uses,
what it must not be confused with there. Refuse technical words (`record`, `data`, `item`,
`manager`, `info`, `status` alone) and ask for the business word. When the business does name a
concept with one, write the term as it says it (`Scoring model`, `Copy of data`): the generator
and `language/no-technical-name` then accept `ScoringModel` and `CopyOfData`, whose words say
the whole term. That is what their refusal points to; a row added only to pass it is a deviation. One word per concept: pick
`cancel` or `void`, not both. Ten precise terms beat fifty vague ones.

```markdown
## ordering
| Term | Meaning | Not to be confused with |
|---|---|---|
| Order | A customer's request to buy products, from placement to delivery | billing: Invoice, the debt it creates |
| Place | To submit an order for fulfilment; it cannot be edited afterwards | |
```

## After the bootstrap: `CONTEXT.md`

It is what an agent reads instead of the code of the context. Keep it true and short.

| Section | Written by | Content |
|---|---|---|
| `## Purpose` | you | two sentences in business terms; the first one feeds the context map |
| `## Classification` | `generate context --classification <c> --reason "..."` | the classification and one sentence of why |
| `## Ubiquitous language` | you | the table above |
| `## Aggregates`, `## Published events`, `## Permissions`, `## Scheduled jobs`, `## Background jobs`, `## State machines`, `## Process managers`, `## Relationships`, `## Reference` | `npx ddd-ts-kit docs`, between markers | never edit between the markers; add below a list one line per aggregate with the invariant it guards |

A new term enters with the code that needs it:
`npx ddd-ts-kit generate <kind> ... --term "<Term>=<meaning>"` adds the row in the same
command; `--term "<Term>=<meaning>|<not to be confused with>"` fills the third cell too, for
homonyms only (a cell never holds a `|`, so it cannot clash with a meaning). Finish with
`npx ddd-ts-kit check --rule tree/context-doc --rule language/glossary-term`.

## Done when

Put this to the owner: **would a domain expert sign each definition, and does every word of
the timeline have exactly one meaning per context?** On a yes, the next step is
`ddd-ts-kit:context-map`.
