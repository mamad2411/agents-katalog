---
name: gold-set
description: >
  Plan the reference set an agent's metrics run on: the example schema, where real inputs come
  from, which approved outputs already exist, the mix of real, hand-written and model-made
  examples, who drafts and who checks labels, and a train / validation / test split grouped to
  prevent leakage. Read-only. Link 4 of the SIA audit chain; reads the metric-signature envelope.
  Use before any optimizer run, or when an eval set was written in an afternoon and never split.
license: MIT
---

# Gold Set

A metric needs examples with known answers. This skill plans that set: what one example looks
like, where real ones come from, who labels them, and how they're split so the score on the test
set means something.

## Rules

- **Read-only.** Don't edit files, run the agent, or make model or API calls.
- **Evidence or "unknown".** Every claim cites `path:line` or a quote from the operator.
- **Real inputs first.** Hand-written and model-made examples fill gaps; they don't replace real
  usage.
- **Split before scoring.** The split is fixed before anyone looks at a score, and the test set is
  scored once, at the end.
- **Never invent an upstream verdict.** If a field you read is missing, ask for it or reconstruct
  it and list it under `out.reconstructed`.

## Step 0: Deployment type

| type | real inputs | approved outputs (drafts vs. finals) |
|---|---|---|
| `coding-harness` | PRs, issues, session transcripts | merged diffs, resolved review comments |
| `gateway-agent` | channel messages | the user's corrections, the version the user kept |
| `framework-app` | requests in traces (LangSmith, Langfuse, OTel) | outcomes in the app: final queue, resolved ticket |
| `prompt-program` | existing devset / trainset files | labels in those files |
| `hosted-nocode` | conversation exports | the version a person sent after editing |

## Step 1: Read what the metrics need

From the `metric-signature` envelope read `metrics[].outputField` and `metrics[].labelsNeeded`.
Each label needed becomes a label column in the example schema.

## Step 2: Find real inputs and existing approved outputs

Search the places in the Step 0 table. Look for pairs of draft and approved version: a draft
someone edited before sending, and a reviewer's change, are labels the team already made. Count
what exists per source.

## Step 3: Choose sources

For each source: `kind` (`real`, `hand`, `synthetic`), where it lives, and a target count. Use
`hand` for edge cases real usage hasn't produced yet, and `synthetic` only with a person checking
every item.

## Step 4: Plan labeling

A model may draft labels. A person checks every label that goes into validation or test. Write a
one-page labeling guide: each label's definition, two examples, and how to resolve a tie. A label
with no written definition is a gap.

## Step 5: Split and size

- Split into train / validation / test, plus dev if the team iterates on prompts by hand.
- **Group by source** (the same customer, conversation, PR or template) so near-duplicates stay on
  one side. Name the `groupBy` key.
- **Size in the tens to hundreds.** As a starting point, about 30 to 300 examples each for
  training and validation, with most of them in validation. Count groups, not items: thirty items
  from five sources are five groups.
- List leakage checks: no group on both sides, no demo drawn from validation or test, no example
  text in the prompt.

## Output

```markdown
# Gold Set: <agent name>

**One example:** inputs <…> → labels <…>

| Source | Kind | Where | Exists now | Target |
|---|---|---|---|---|

**Labeling:** drafter <…>, checker <…>, guide <where it will live>
**Split:** train / validation / test (dev?), grouped by <key>
**Leakage checks:** <list>
```

Then the envelope as the last fenced block, then the footer line. The envelope must parse as
YAML: put double quotes around every free-text value (names, `title`, `why`, `do`, each
`evidence` item, claims), because a `: ` or a leading quote inside an unquoted value breaks the
parse. Every key keeps its colon, as in the template (`effort: S`, `impact: medium`); write `medium`,
not `med`.

```yaml
sia:
  skill: gold-set
  version: 1
  agent: { name: "<name>", summary: "<one line>" }
  deploymentType: <type>
  in_ref: metric-signature#v1     # or "none"
  out:
    exampleSchema: { inputs: [invoice_text], labels: [approved_vendor_id] }
    sources:
      - { kind: real, location: "AP system export", targetCount: 160 }
    labelingPlan: { drafter: "model", checker: "AP lead", guide: "docs/labels.md (to write)" }
    split: { train: 30, validation: 100, test: 30, groupBy: vendor }
    leakageChecks: ["no vendor on both sides of a split", "demos drawn from train only"]
  recommendations:
    - id: gs-1
      effort: M
      impact: high
      title: "<imperative, one line>"
      why: "<one line tied to evidence>"
      do: "<a step an agent or engineer can do without rereading the report>"
      evidence: ["<path:line>"]   # or "unknown (ask: <question>)"
      next_skill: eval-power
      links: []
```

> Series and help: peleke.me · LinkedIn

**Recommendations:** at most seven, each with evidence or `unknown (ask: …)`. No pitching.
- Order by what each item unblocks: item 1 is the one the others depend on.
- Size each item (S, M, L) for everything its `do` includes, prerequisites too.
- Each `do` stands alone: no "see above", one named choice rather than an either/or.
- A claim resting on one incident is a hypothesis; say "one case" and what would confirm it. A
  claim that something is absent (no reader, never measured) names where you searched.

## Gotchas

- An eval set written by one person in one sitting is one source. It counts as one group.
- Scoring on the set the optimizer chose demos from doesn't measure held-out performance.
- Model-made examples tend to be easier than real ones. Report their share.
- "Approved" outputs that nobody reviewed are drafts. Check who signed off.

## Examples

- Invoice extractor whose AP system keeps the approved vendor per invoice → real source, labels
  already exist (the approved vendor), group by vendor, draft-by-model unnecessary.
- Ax extractor with 25 hand-written examples and no test set → add real documents, split by source
  before the next optimizer run, keep the 25 as one group.
