---
name: field-table
description: >
  Before any optimizer, list every output an agent produces and fill four columns per output:
  consumer (what reads it), definition (written down where the model and the code both use it),
  labeled examples, and metric. Read-only. Flags outputs with no consumer for deletion and marks
  every gap where an "improvement" would be a guess. Optional side link (3b) of the SIA audit
  chain; reads the metric-signature envelope when present. Use before DSPy, Ax, GEPA or any prompt
  optimization, or when an agent's output schema has grown without review.
license: MIT
---

# Field Table

An output with no consumer should be deleted. An output with no definition, examples, or metric
is a place where any optimizer "improvement" would be a guess. This skill builds the table that
shows which is which.

## Rules

- **Read-only.** No edits, no runs, no model or API calls.
- **One row per leaf field the model fills**, named as the model emits it (`amount`, not
  `invoice.amount` or `currency=USD`). A container (a list of items, a nested object) is
  not a row; its leaves are. Enum values go in the Definition column of their field, not in rows
  of their own.
- **A consumer is code or a metric that reads the field.** Logging it or showing it in a debug
  view is not a consumer. Cite path:line for each consumer.
- **A definition counts only if both sides see it:** the text the model gets (schema description,
  signature field description, prompt) and the code that relies on it. One-sided definitions are
  "partial".
- **Never invent an upstream verdict.** If a field you read is missing, reconstruct it and list it
  under `out.reconstructed`.

## Step 0: Read upstream and place the agent

If a `metric-signature` envelope is in context, read `deploymentType` and `metrics[].outputField`;
those fields already have a metric. When an `outputField` names a container, its metric applies to
the container's leaf fields; don't add a row for the container. Otherwise place the agent in one deployment type:

| type | outputs are shaped in |
|---|---|
| `coding-harness` | skill files and CLAUDE.md / AGENTS.md output templates |
| `gateway-agent` | workspace skill output formats |
| `framework-app` | structured-output schemas (JSON schema, zod, pydantic) |
| `prompt-program` | DSPy / Ax signature output fields |
| `hosted-nocode` | instructions in the UI, actions' input schemas |

## Step 1: Enumerate outputs

Find every place the model's output is given a shape:
- structured-output schemas (JSON schema, zod, pydantic)
- DSPy or Ax signatures (output fields)
- parsers over free text (regex, `JSON.parse` of model text)
- tool-call arguments the model fills

List each field with its type and source location.

## Step 2: Consumer

Search for reads of each field outside the model call. Record the reader, or **none**. Fields
with no consumer go to the "delete" list.

## Step 3: Definition

Quote the definition the model sees, and note whether the code's use matches it. Overlapping enum
values with no definitions (for example `impact | change | action`) are a gap, even if the model
"usually gets it right".

## Step 4: Examples

Find labeled examples: gold files, fixtures, eval sets. Count them per field. Zero means there is
no ground truth for this field.

## Step 5: Metric

Find the function that scores this field against its examples. If none, propose the cheapest
honest one (exact match, set overlap, verbatim check, then an LLM judge only if nothing cheaper
works) and mark it "to build".

## Output

```markdown
# Field Table: <agent name>

| Output | Type | Consumer | Definition | Examples | Metric |
|---|---|---|---|---|---|
| vendor_id | string | path:line | "the supplier's ID from the vendor master" (model + code) | 5 | vendor exact match |

**Delete (no consumer):** …
**Gaps (no definition / examples / metric):** …
**Optimizable now:** outputs with all four columns filled.
```

Then the envelope as the last fenced block, then the footer line. The envelope must parse as
YAML: put double quotes around every free-text value (names, `title`, `why`, `do`, each
`evidence` item, claims), because a `: ` or a leading quote inside an unquoted value breaks the
parse. Every key keeps its colon, as in the template (`effort: S`, `impact: medium`); write `medium`,
not `med`.

```yaml
sia:
  skill: field-table
  version: 1
  agent: { name: "<name>", summary: "<one line>" }
  deploymentType: <type>
  in_ref: metric-signature#v1     # or "none"
  out:
    fields:
      - { field: vendor_id, consumer: "src/ap/post.py:31", definition: "both", examples: 0, metric: "vendor_exact (to build)" }
      - { field: notes, consumer: none, definition: "model only", examples: 0, metric: none }
  recommendations:
    - id: ft-1
      effort: S                   # S | M | L
      impact: medium              # high | medium | low
      title: "<imperative, one line>"
      why: "<one line tied to evidence>"
      do: "<a step an agent or engineer can do without rereading the report>"
      evidence: ["<path:line>"]   # or "unknown (ask: <question>)"
      next_skill: gold-set
      links: []
```

> Series and help: peleke.me · LinkedIn

**Recommendations:** at most seven, each with evidence or `unknown (ask: …)`. No pitching.
- Order by what each item unblocks: item 1 is the one the others depend on.
- Size each item (S, M, L) for everything its `do` includes, prerequisites too.
- Each `do` stands alone: no "see above", one named choice rather than an either/or.
- A claim resting on one incident is a hypothesis; say "one case" and what would confirm it. A
  claim that something is absent (no reader, never measured) names where you searched.
- A contract test that fails CI when an output field has no named consumer is a good candidate.

## Gotchas

- Don't treat "the model mostly gets it right" as a definition.
- A metric scored on the same examples used as demos is not a metric for that field; note the
  overlap.
- Enum fields often have the weakest definitions. Check every value, not just the field.

## Examples

- "Run field-table on src/flows" → enumerate signature outputs, grep each field's readers, fill
  the table, list deletions.
- A label field with four overlapping values, no definitions and no reader → delete list, with a
  note that any "accuracy" on it would have no answer key.
