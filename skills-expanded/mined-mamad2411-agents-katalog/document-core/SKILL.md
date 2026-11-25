---
name: document-core
description: Constitution of the professional document tree: the audience model that decides structure, the separation of skill language from output language, the evidence rule that forbids inventing facts, the shared style standard, and the eight-point quality gate every document passes before delivery. Load before writing any technical, user, report or administrative document.
license: MIT
metadata:
  category: documentation
  version: 1.0.0
  depends_on: []
  outputs: [audience-profile, document-plan, quality-gate-record]
---

# Document Core

Constitution of the `documents/` tree. Every skill in it is subordinate to
this file and refers to it rather than restating it.

A professional document is not prose with headings. It is an instrument built
for one reader to do one thing. The reader decides the structure, the
structure decides the content, and nothing in the document exists that the
reader does not need.

## 1. Scope

Applies to technical documentation, developer documentation, user
documentation, project documentation, guides, manuals, reports,
administrative and institutional documents, and anything the `documents/` tree
renders to PDF.

Does not apply to fiction, poetry or screenplay, which are governed by
`writing-constitution`. Does not apply to documentation that lives in a
codebase and is maintained with the code, which is governed by
`technical-documentation` in the engineering tree. Section 9 draws that
boundary precisely.

## 2. The three languages

Confusing these produces documents written in the wrong language for the wrong
reader, and configuration keys nobody outside one country can read.

| Layer | What it is | Value |
|---|---|---|
| Skill language | the language these instructions are written in | English, always |
| System language | identifiers, paths, keys, filenames, commits | English, always |
| Output language | the language the recipient reads | whatever the recipient reads |

Rules:

- The output language is the recipient's, never the author's, never the
  system's. A French administrative body receives a French document. A
  Spanish client receives Spanish.
- Resolve it in this order: an explicit instruction, the language of the
  request or source material, then `language.document_output` from the
  configuration.
- State the output language at the top of the document plan. It is a decision,
  not an accident.
- Technical identifiers stay in their original form inside a translated
  document. A field named `created_at` is `created_at` in every language, and
  is glossed on first use rather than translated.
- One document, one output language. A bilingual deliverable is two documents,
  or one document with a clearly separated second part.

## 3. Audience before structure

No document is written before its audience is named. The same subject produces
eight different documents.

| Audience | Wants | Opens with | Never wants |
|---|---|---|---|
| Developer | to integrate correctly and fast | a working example | narrative introductions |
| Technical administrator | to install, configure, operate | prerequisites and the exact procedure | rationale before the steps |
| Project manager | status, risk, dependencies, dates | the summary and the decisions needed | implementation detail |
| Client | what was delivered and how to use it | what it does for them | internal architecture |
| End user | to complete a task | the task, by name | the system's vocabulary |
| Executive | the decision and its cost | one page, conclusion first | anything on page two |
| Support team | to resolve a ticket | symptom to cause to resolution | design history |
| Operations team | to keep it running and fix it at 3am | alerts, thresholds, first commands | product context |

Build the profile before writing:

```
Who reads this, by role
What do they already know
What must they be able to do afterwards
Where do they read it: screen, print, mobile, terminal, under pressure
How much time will they give it
What happens if they misread it
Output language
```

The last question sets the register. A document whose misreading causes a
production incident or a rejected application is written differently from one
whose misreading causes mild confusion.

## 4. Structure follows purpose

| Purpose | Structure |
|---|---|
| Enable a task | prerequisites, numbered steps, verification, troubleshooting |
| Explain a system | context, model, components, interactions, boundaries |
| Reference a contract | one entry per item, identical shape, alphabetical or logical order |
| Support a decision | conclusion, options, criteria, recommendation, cost |
| Record what happened | facts, timeline, analysis, consequences, actions |
| Request or notify formally | reference, subject, statement, request, deadline, signature |

Rules that hold across all six:

- One document, one purpose. A guide that also argues for a decision does
  neither.
- The reader's most likely question is answered above the fold, not in
  section 4.
- Every heading is a claim or a task, never a category label. `Configuring the
  webhook endpoint` beats `Configuration`.
- A section that can be removed without loss is removed.
- Procedures are numbered, ordered, and each step is one action with an
  observable result.
- A statement of what something does is followed by what it looks like when it
  works, and what happens when it fails.

## 5. The evidence rule

**Nothing is asserted that was not verified.** This is the rule that
distinguishes a document from a plausible text.

Never invent:

```
a command, flag, path, endpoint, field name or default value
a version number or a compatibility claim
a legal reference, statute, article or regulation
a credential, registration number, licence or accreditation
an institutional name, address, office or procedure
a date, a deadline, a price or a figure
a person's title, role or authority
a citation, a source or a standard
```

Three permitted behaviours when a fact is missing, and only three:

| Situation | Behaviour |
|---|---|
| Verifiable now | verify it, then write it |
| Not verifiable, not essential | omit it |
| Not verifiable, essential | mark it explicitly as a gap and name who can fill it |

The marker is visible in the delivered draft, never a silent blank:

```
[TO CONFIRM: exact registration number, held by the finance office]
```

Every command in a document is run before it is documented. Every path is
checked to exist. Every example is executed. A document describing behaviour
that was never observed is a hypothesis in the shape of a manual, and it will
be trusted precisely because it looks like one.

## 6. Style standard

Binding on the `documents/` tree, and on this repository's own documentation.

Never:

```
emoji, pictograms, decorative symbols
em dashes
manufactured enthusiasm
filler, throat clearing, restated headings
the same information in three places
vague intensifiers: very, extremely, incredibly, seamlessly, robust, powerful
promises the system does not keep: simply, just, easily, obviously
```

Always:

```
short paragraphs, one idea each
tables where the content is comparative
lists where the content is enumerable
prose where the content is an argument
the specific noun rather than the general one
the active voice, unless the actor is genuinely irrelevant
present tense for what the system does
the reader's vocabulary, or the system's word glossed once
```

`easily` and `simply` are banned outright. They describe the author's
experience, not the reader's, and a reader for whom it is not easy concludes
the failure is theirs.

Formatting conventions are owned by `document-design`. Typography, spacing,
numbering, headers and covers are not decided per document.

## 7. Quality gate

No document is delivered before all eight pass. Failure at any point sends the
document back, not forward.

| # | Review | Passes when |
|---|---|---|
| 1 | Content | every claim is verified or marked as a gap; nothing invented |
| 2 | Structure | the reader finds their answer without reading linearly |
| 3 | Language | output language correct, register consistent, terms uniform |
| 4 | Formatting | conforms to `document-design`; consistent from first page to last |
| 5 | Audience | written for the named profile, not for the author |
| 6 | Consistency | terms, names, versions and figures identical throughout |
| 7 | Requirement | every requested element present, nothing unrequested added |
| 8 | Self critique | `self-critique` run with the documentation role panel |

For a paginated deliverable, three more, owned by `pdf-production`:

| # | Review | Passes when |
|---|---|---|
| 9 | Rendering | the file opens, renders, and contains no missing glyph |
| 10 | Pagination | no orphan heading, no broken table, no empty page, correct numbering |
| 11 | Visual | inspected as rendered, not as source |

Record the gate. A gate claimed without a record did not run.

```markdown
## Quality gate
Document: <name, version, output language>
Audience: <profile>
1 Content     pass | fail  <what was verified, or what remains marked>
2 Structure   pass | fail
3 Language    pass | fail
4 Formatting  pass | fail
5 Audience    pass | fail
6 Consistency pass | fail
7 Requirement pass | fail
8 Self critique  pass | fail  <roles used>
Gaps remaining: <marked items, and who fills them>
```

## 8. Maintenance

A document with no owner and no trigger is wrong within a year, and being
wrong is worse than being absent: absence prompts a question, wrongness
prompts an action.

Every document carries: owner, last verified date, and the event that
invalidates it. When the event happens, the document is updated in the same
change, not in a later cleanup that never comes.

Delete rather than deprecate. A document marked outdated is still read.

## 9. Boundaries

| Work | Owner |
|---|---|
| Documentation living in a codebase, maintained with the code | `technical-documentation`, engineering tree |
| Standalone technical or developer deliverable | `technical-writing` |
| End user guides and manuals | `user-documentation` |
| Reports, status, audit, executive summaries | `report-writing` |
| Formal letters, official correspondence, institutional documents | `administrative-writing` |
| Layout, typography, covers, tables of contents | `document-design` |
| Paginated output and its verification | `pdf-production` |
| Fiction, poetry, screenplay | `writing-constitution` |

The line between `technical-documentation` and `technical-writing` is where
the document lives and who maintains it. A readme, an API reference generated
from routes, a runbook in the repository: engineering tree, updated in the
same commit as the code. An integration guide handed to a partner, an
architecture document delivered to a client, a manual with a cover page:
`documents/` tree, versioned as a deliverable.

## 10. Protocol

1. Name the audience profile and the output language, with section 3.
2. Name the single purpose. Split the document if there are two.
3. Choose the structure from section 4.
4. Collect the material and separate verified facts from gaps, with section 5.
5. Ask for the essential gaps in one batch, through `project-brief`.
6. Write the plan: sections, what each answers, approximate length.
7. Write, applying section 6.
8. Apply `document-design`. Render with `pdf-production` where required.
9. Run the gate of section 7, all eight, plus 9 to 11 when paginated.
10. Fix what the gate found, then re-run the checks the fixes touched.
11. Deliver with the gate record and the list of remaining gaps.

## 11. Auto-critique

Score 0 to 5: audience named before writing, output language deliberate,
single purpose, structure matched to purpose, every claim verified, gaps
marked rather than filled with plausible text, style standard respected,
consistency across the whole document, gate run and recorded, nothing
unrequested added.

Threshold: no axis below 3, average at least 4. For a document leaving the
organisation, average at least 4.3.

Automatic failure, whatever the average: an invented fact, a command never
run, a legal or institutional reference not taken from a source, or a gate
claimed without a record.

## 12. Interfaces

- Upstream: `project-brief` for the request and the audience.
- Downstream: `technical-writing`, `user-documentation`, `report-writing`,
  `administrative-writing`, `document-design`, `pdf-production`.
- Related: `technical-documentation` owns documentation inside a codebase.
  `self-critique` runs gate 8.
