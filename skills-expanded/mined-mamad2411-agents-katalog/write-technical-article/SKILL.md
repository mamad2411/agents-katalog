---
name: write-technical-article
description: "Plan, draft, revise, or review an original technical article, engineering blog post, architecture case study, migration story, public incident lesson, tutorial, or opinion grounded in the user's real experience and verifiable sources. Produces the artifact appropriate to the requested mode without inventing incidents, metrics, quotations, or authority. Use this skill whenever the user asks to write a technical post, turn project experience into an article, explain an engineering decision publicly, draft a case study or tutorial, improve a technical draft, find the argument in rough notes, or says \"write about this migration\", \"turn this into a blog post\", or \"make this publishable\". Do not use it for internal postmortems or RCAs, private learning notes, product marketing, API/reference documentation, academic papers, or fabricating experience the user did not provide."
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch
---

# Write a Technical Article

A good technical article gives a specific reader a useful change in judgment: what to do,
what to avoid, or how to reason differently, supported by evidence they can inspect.

Generated technical prose fails in two directions. It becomes a tidy summary of general
knowledge with no lived detail, or it turns sparse experience into invented numbers and
false certainty. Keep the author's real observations separate from sourced facts and from
explicit opinion throughout the workflow.

## Scope

Use for: engineering essays, migration and architecture case studies, public transferable
lessons derived from an existing incident record, tutorials, technical explainers,
experience-backed opinion, and review of such drafts.

Do not use for: internal incident postmortems or RCAs, private knowledge-base notes,
product marketing, reference documentation, academic publication, confidential incident
disclosure, or ghostwriting invented history. Use `postmortem` for the internal record.

## Evidence rule

Never invent a metric, date, incident detail, organisation policy, quotation, benchmark,
or claimed outcome. Mark missing author evidence as `[TK: question]`. Source external
claims from primary material where practical, and distinguish what the source states from
what the article infers.

Before publishing, remove or resolve every `[TK:]`; do not silently turn one into a vague
claim.

## Workflow

### 1. Select the requested mode

Match the deliverable to the request before doing article work:

- **Plan** — return the brief, evidence map, and outline; do not draft prose.
- **Draft** — return the plan plus a full draft and publication package.
- **Revise** — preserve the author's argument and voice; make only requested or necessary
  edits and report material changes.
- **Review** — return ranked findings with evidence and recommended fixes; do not rewrite
  unless the user asks for it.

### 2. Name the reader and the change

Complete these sentences before outlining:

- This is for **[specific reader in a specific situation]**.
- They currently believe or do **[current model]**.
- After reading, they should **[new judgment or action]**.
- The article earns that change by showing **[mechanism and evidence]**.

“Engineers” is not a reader. “Platform leads planning their first stateful cluster
migration” is.

### 3. Choose the article shape

| Material available | Shape |
| --- | --- |
| Real project with before/after evidence | Case study |
| Repeatable procedure with verified steps | Tutorial |
| Decision with meaningful rejected options | Architecture argument |
| Incident with a transferable mechanism | Incident lesson |
| Several sources supporting one model | Synthesis/explainer |
| Strong experience-backed disagreement | Technical opinion |

If the material does not support the requested shape, change the shape rather than fill
the gaps with generic prose.

### 4. Build the evidence map

Separate evidence into three columns:

| Claim | Evidence type | Status |
| --- | --- | --- |
| What happened in the author's work | Author-provided artifact or recollection | confirmed / TK |
| How a tool or system behaves | Primary documentation, code, standard, or measurement | sourced / verify |
| What the reader should conclude | Author's inference or recommendation | label and argue |

Read `references/evidence-and-structure.md` before researching or outlining. It contains
source order, claim testing, case-study structures, and confidentiality transforms.

### 5. Find the thesis under the topic

A topic names the shelf; a thesis gives the article a reason to exist.

Weak: “Migrating from Jenkins to GitHub Actions.”

Stronger: “A CI migration is an ownership migration before it is a YAML migration.”

Test the thesis:

- A reasonable experienced reader could disagree with it.
- The body can prove it with mechanisms and evidence.
- It excludes material that is interesting but does not advance the claim.
- It does not promise a universal rule from one local experience.

### 6. Outline by reader questions

Use the minimum structure that carries the argument:

1. The concrete situation and stakes.
2. The misleading first model or failed approach.
3. The mechanism that actually governed the outcome.
4. The decision or procedure, including rejected alternatives.
5. Evidence and results, with limitations.
6. What transfers to the reader and what does not.

Each section heading should make a claim or answer a reader question. “Background” and
“Implementation” are containers, not arguments.

### 7. Draft with concrete operating detail

Prefer one real decision, failure signal, command, constraint, or diagram over a paragraph
of adjectives. Explain why the detail matters and where it stops applying.

Use code only when the reader needs to execute or inspect it. Keep examples minimal,
safe, and runnable; test them when the article presents them as working instructions.

Use diagrams for topology, ownership, state flow, or sequence—not decoration. Every
diagram needs a sentence stating what relationship the reader should notice.

### 8. Protect confidentiality without deleting the lesson

Remove credentials, personal data, customer-identifying details, private hostnames, and
security-sensitive topology. Generalise names and scale only where the exact value is not
load-bearing. Say “scale withheld” instead of replacing it with a plausible number.

Preserve the mechanism: sequence, constraint, trade-off, failure mode, and decision. Read
the confidentiality section in `references/evidence-and-structure.md` before publishing a
workplace case.

### 9. Edit in four passes

1. **Truth:** verify claims, sources, calculations, code, and author-provided facts.
2. **Argument:** remove sections that do not advance the thesis; expose counterarguments.
3. **Usefulness:** ensure the reader gets a decision rule, procedure, or diagnostic model.
4. **Voice:** remove inflated transitions, generic scene-setting, repetition, and language
   the author would not say aloud.

Use `references/publication-checklist.md` for the final review and metadata handoff.

## Output format

Return only the sections required by the selected mode. A review returns ranked findings
instead of a replacement draft unless rewriting was explicitly requested.

```markdown
## Article brief
- Reader:
- Situation:
- Thesis:
- Reader change:
- Shape:

## Evidence map
| Claim | Evidence/source | Status |

## Outline
[Claim-led section headings with one-line purpose.]

## Draft
[Publication-ready article.]

## Verification and open items
[Sources checked, code run, every unresolved TK, confidentiality review.]

## Publication package
[Title options, description, slug, canonical/source notes, diagram and image needs.]
```

## Anti-patterns

**Topic without thesis.** The draft becomes a tour of everything known about the subject
and gives the reader no changed judgment.

**Invented authority.** A plausible metric, unnamed “industry benchmark”, or fabricated
incident makes every true part less trustworthy.

**Chronological project diary.** The order work happened is rarely the order a reader
needs to understand the mechanism.

**Tool-first lesson.** “How we configured X” ages quickly. Explain the constraint and
decision that made the configuration correct.

**Universal claim from one case.** State boundary conditions and what would change the
recommendation.

**Polished voice that is not the author's.** If the author cannot defend or naturally say
the sentence, rewrite it before publication.

## Reference files

- `references/evidence-and-structure.md` — read before research and outlining: evidence hierarchy, claim map, article structures, counterarguments, and confidentiality transforms.
- `references/publication-checklist.md` — read during the final edit: accuracy, code and diagram checks, readability, metadata, accessibility, SEO hygiene, and publication handoff.
