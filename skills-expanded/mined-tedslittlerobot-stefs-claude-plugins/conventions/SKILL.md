---
name: conventions
description: How a project records its own conventions — the conventions/ directory, one file per topic, what belongs there versus in a reusable skill, in architecture documentation or in the glossary, precedence when a project rule contradicts a general one, and how to write a convention so the reasoning survives. Use when adding or editing a conventions file, when asked "what are the conventions for X", when a decision needs recording as a rule, or when project rules and general guidance appear to conflict.
---

# Project Conventions

A project's conventions are the rules that govern how its code and documents are written: naming,
layout, structure, formatting, what is required and what is forbidden. They exist so a decision is
made once and then followed, rather than re-argued in every review.

Conventions are recorded in a **`conventions/` directory at the repository root, one markdown file
per topic** — `conventions/golang.md`, `conventions/terraform.md`, `conventions/sql.md`, and so on.
That is the only place project rules live. A rule that exists solely in someone's memory, in a
review comment, or in a chat thread is not a convention.

## Two Layers

Conventions come in two layers, and keeping them apart is what makes any of this reusable:

| Layer | Lives in | Contains |
| --- | --- | --- |
| **Portable** | A skill (`api-design`, `documentation`, `frontend`, `infrastructure`, `lambdas-go`, `lambdas-node`, `mysql`, `glossary`, `product-requirements`) | The rule and its reasoning, stated without reference to any one project's services, paths or vocabulary |
| **Project** | `conventions/<topic>.md` in the repository | What this project's rules are *on top of* that: which paths the rules apply to, the project's chosen values, its registered exceptions, and its worked examples |

A project conventions file is therefore usually **short**. It opens by saying what it applies to and
which skill carries the general rules, then records only what is genuinely specific to this
repository. If a project file grows to restate rules the skill already states, the restatement is
the bug — delete it, because two copies of a rule drift and then contradict each other.

### What counts as project-specific

- **Scope** — the actual directories and files the rules govern in this repository
- **Chosen values** — a tag value, a prefix, a module version, a pinned language version, a
  directory name, an approved library list
- **Registered exceptions** — a place this project knowingly departs from the general rule, *with
  the reason*. An unexplained exception reads as an oversight and gets "fixed" by the next person
- **Registers** — an explicit allow-list the general rule depends on (e.g. which shared libraries
  may be imported). The general rule can describe the mechanism; only the project can hold the list
- **Worked examples** — a pointer to the real file in this repository that shows the pattern done
  properly. These are the most useful lines in a conventions file and should not be genericised away

### What does not belong in `conventions/`

| It is… | It belongs in… |
| --- | --- |
| A rule that would hold in any project using the same stack | the relevant skill |
| A description of what the system currently is, or how it works | `architecture/` |
| The meaning of a term the system relies on | `glossary/<term-slug>.md` |
| Steps a human performs at a keyboard | `instructions/<topic>.md` |
| A design not yet built | `proposals/<slug>/proposal.md` |
| A staged plan for building one | `proposals/<slug>/plan-of-action/<n>-<description>.md`, summarised in `plan-of-action/plan.md` |
| A decision a proposal has to make, or an assumption it tests | `proposals/<slug>/decisions/D<n>-<description>.md` or `proposals/<slug>/tests/T<n>-<description>.md`, summarised in `decisions.md` or `tests.md` |
| A user-level feature and its acceptance criteria | `requirements/` |

The commonest mistake is the second row: architecture record smuggled into a conventions file. "Our
Cognito pool is configured for email-only sign-in" is not a convention, it is a fact about what
exists. The convention is the rule that produced it. When a "convention" can be falsified by
looking at the deployed system, it is documentation in the wrong place.

## Precedence

**The project file wins.** A `conventions/<topic>.md` rule overrides the corresponding skill rule
for that repository — that is the entire point of having the layer. When the two conflict:

1. Follow the project file
2. Say out loud that it diverges from the general rule, so the divergence is visible rather than
   silently absorbed
3. If the project file's rule looks like an accident rather than a decision, ask — don't quietly
   apply the general rule instead

Where a project file is silent, the skill applies in full. Silence is not permission to improvise.

## Writing a Convention

- **Keep a table of contents** above the file's first heading, like every markdown document — see
  the `documentation` skill's "Table of Contents" rule. A conventions file is consulted for one
  rule at a time, which is exactly the read a contents list serves
- **State the rule as a rule.** Imperative, unambiguous, and testable against a diff: "every named
  resource is prefixed with `${var.project_prefix}-`", not "resources should generally be prefixed"
- **Record the reasoning immediately after it.** This is the part that cannot be recovered later. A
  bare rule gets deleted the first time it is inconvenient; a rule with its reason attached gets
  followed, or gets changed deliberately. Give the reason even when it feels obvious now
- **Prefer the failure that motivated the rule** over an abstract justification. "Custom error
  responses are a property of the distribution, not the cache behaviour, so a 403 → `/index.html`
  mapping also swallows genuine 403s from `/api/*`" teaches the rule in a way "be careful with
  custom error responses" never will
- **Say what is verified and how.** When a rule rests on a claim about a tool's behaviour, say that
  it was checked and against what — the provider docs, the module's own source, a built artefact.
  A conventions file full of unattributed assertions cannot be audited when a version changes
- **Cover the negative case.** What must *not* be done, and what will happen if it is — especially
  when the wrong thing fails silently rather than loudly
- **Write for the reader who disagrees.** The audience for a convention is the person about to do
  something else

### Corrections

When a convention turns out to be wrong, **edit it in place and say that it was corrected** — what
it used to say, and why the old version was wrong. Do not silently rewrite it. Someone will read
code written under the old rule and needs to know it was written in good faith, and the reason the
old rule failed is usually the reason the new one is shaped as it is.

Corrections are also how a conventions file earns trust. A file that has visibly been corrected
reads as maintained; one that has never changed reads as aspirational.

## Applying Conventions

- Before making a **structural** decision — where a file goes, what it is named, how a module is
  laid out — read the relevant conventions file and skill rather than pattern-matching the code you
  happen to have open. Existing code may predate a convention or be the exception that motivated it
- Conventions are binding on **new** work. Reworking existing code purely to conform is a separate,
  explicit task — not something to fold into an unrelated change
- When work reveals a rule that is missing, add the convention **in the same change** as the code
  that first follows it. A convention added later describes the past rather than governing the
  future

## Related

- `documentation` skill — the three kinds of document (`architecture/`, `instructions/`,
  `proposals/`) and how they differ by tense
- `glossary` skill — where the *meaning* of a term is recorded, as opposed to a rule about it
- The per-stack skills — `frontend`, `infrastructure`, `lambdas-go`, `lambdas-node`, `mysql`,
  `product-requirements` — and the stack-independent `api-design` carry the portable layer these
  project files sit on top of
