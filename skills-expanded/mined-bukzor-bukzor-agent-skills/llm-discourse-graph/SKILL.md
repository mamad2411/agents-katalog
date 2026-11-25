---
name: llm-discourse-graph
description: "Epistemic knowledge graph for collaborative human-LLM inquiry -- questions, claims, deductions, sources, and definitions as linked .kb/ collections. Agent MUST load when adding to or restructuring a discourse graph, when deciding which collection a new node belongs in, or when an inquiry needs recording as a graph of questions and evidence rather than a flat list."
---

# llm-discourse-graph

Epistemic knowledge graph for collaborative human-LLM knowledge management.
Built on the `llm.kb` pattern. Models what we believe, why, how confidently,
and where it comes from.

## The five collections

| Collection | What it holds |
|---|---|
| `questions.kb/` | Open inquiries that structure investigation |
| `claims.kb/` | Propositional assertions — observed or hypothesized |
| `deductions.kb/` | Structured inference — premises that entail or contradict a conclusion |
| `sources.kb/` | Provenance references (papers, reports, testimony, discussion participants) |
| `definitions.kb/` | What terms mean — scope, boundaries, usage |

### When to use each

- **Question**: someone asks something that needs investigation
- **Claim**: someone asserts something that may or may not be true
- **Deduction**: premises entail or contradict a conclusion (claim or deduction) — the body text explains *why*
- **Source**: citing where claims originate
- **Definition**: establishing what a term means, independent of claims about it

## Scoping and hierarchy

Elaboration uses the standard `llm.kb` nesting convention: `$ITEM.kb/`
as a sibling of `$ITEM.md`. A sub-scope may contain any of this skill's
collection types (only those needed — none are mandatory, and a scope
may have zero of a given type) plus project-specific auxiliary
collections (e.g. `background.kb/`, `technical-policy.kb/` from
`Skill(llm-design-kb)`). The project root is itself an implicit scope.
Every collection carries its own `$CATEGORY.jsonschema.yaml` beside it --
schemas do not inherit from an ancestor scope, so one left at the graph
root leaves each sub-scope's collections silently unvalidated.

### When to elaborate

- Multiple claims supporting/countering the same parent
- Sub-questions arising from a question or claim
- A deduction complex enough to need its own sub-claims

Most nodes should NOT have elaboration. A few sentences of body text with
frontmatter references to other nodes is the normal case.

### Roll-up

The parent node IS the summary. When a sub-scope resolves (e.g. a question
is answered), update the parent node's status and body accordingly -- this
is the discourse-graph instance of `Skill(llm-kb)`'s general "Decision
Points" pattern (`$ITEM.md` + `$ITEM.kb/`); see that skill for the full
keep-as-background vs. clean-up-entirely lifecycle once resolved.

## Path resolution

Cross-references are plain file-relative paths, resolved exactly like any
relative filesystem path from the referencing file's own directory (e.g.
`../claims.kb/conways-law.md`). There is no collection-relative or
ancestor-walking resolution — moving a file requires updating every path
that points to it and every path it itself contains (see ADR
`2026-07-03-000-file-relative-paths.md`, which supersedes the original
lexical-scoping decision).

- Content lives at the narrowest scope containing all its uses —
  a placement judgment made once, not a mechanism to lean on
- Prefer placing a node at the scope it's used from over reaching up
  with a long `../../..` chain

## Schemas

Five `$COLLECTION.jsonschema.yaml` files, placed alongside the collections
they govern. See `jsonschema/` in this skill directory.

## Relations and metadata

Cross-references are file-relative paths in YAML frontmatter
(`../claims.kb/x.md`). Epistemic
metadata (status, likelihood, kind) tracks the standing of
each node. Questions derive their state from field presence: `resolved` means
answered, `candidate-resolutions` means under investigation, neither means
new/open. See the schemas for the complete field definitions.

Two axes, not one. `status` is whether we believe a node (`asserted`,
`contested`, `retracted`); `live` is whether it still bears on anything.
Retiring is not retracting: a claim that was true and then got acted on is
`status: asserted, live: false`, and saying it stopped mattering must never
require calling it wrong. Where a successor exists, name it in
`superseded-by:` -- any collection, not just `claims.kb/` -- instead of
burying the replacement in prose.

### The core wiring pattern

Questions are answered by claims. Claims are supported by deductions.
Deductions draw on other claims as premises.

```
question
  candidate-resolutions: [claim]
                           ↑ conclusion
                         deduction
                           premises: [claim, claim, ...]
```

- `candidate-resolutions` points to **claims**, not deductions
- `conclusion` points to a **claim or deduction**, not a question
- `depends` expresses "needs context from" without implying support or refutation

## Creating a discourse graph

1. Create a scope directory with CLAUDE.md declaring this skill
2. Link or copy `$COLLECTION.jsonschema.yaml` schemas from `jsonschema/`
3. Create collections as needed — start with `sources.kb/` and `questions.kb/`
4. Populate nodes as markdown files with YAML frontmatter
5. Wire questions to claims via `candidate-resolutions`, claims to
   deductions via `conclusion`/`premises`
6. Elaborate nodes into sub-scopes when they outgrow a single file

### Decomposition workflow

When extracting a discourse graph from a source document:

1. **Source** — create the provenance node first
2. **Questions** — identify the inquiries the source addresses
3. **Claims + Deductions** — interleaved, not separate passes. Each claim
   is either justified by a deduction or fundamental.
4. **Wire** — link questions to their candidate-resolutions, add `depends`
5. **Scope** — identify strictly inner questions and nest them

## Reading a discourse graph

```bash
ls */                                        # What collections exist
grep -rL "resolved:" questions.kb/*.md        # Open questions
cat claims.kb/some-claim.md                  # Read a claim
ls claims.kb/some-claim.kb/                  # Has elaboration?
grep -l "status: contested" claims.kb/*.md   # Find contested knowledge
grep -l "live: false" claims.kb/*.md         # Retired, not retracted
```

## Design rationale

See `docs/dev/adr/` for decision records covering collection types, path
resolution, elaboration conventions, terminology, similarity groups, and the
open world assumption.

## See also

- `Skill(llm-design-kb)` — the **normative** companion (values, design rules,
  requirements, goals). When content isn't truth-apt — *held/desired* rather
  than *true/false* — it belongs in a design tower, not here. Cross-link the two.
