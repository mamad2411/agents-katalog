---
name: metric-signature
description: >
  Turn an agent's chosen learning signal into metric functions: the cheapest check that can tell a
  good output from a bad one, written as a DSPy-style Python signature, an Ax-style TypeScript
  signature and plain language, normalized to 0..1, with a named do-nothing baseline. Read-only.
  Link 3 of the SIA audit chain; reads the signal-card envelope. Use after signal-card, before
  building a gold set, or when an optimizer needs a metric and nobody has written one.
license: MIT
---

# Metric Signature

An optimizer only climbs what the metric measures. This skill writes the metric down before
anyone builds a dataset or runs a search: which output fields it scores, how cheaply, on what
scale, and what "doing nothing" scores.

## Rules

- **Read-only.** Don't edit files, run the agent, or make model or API calls.
- **Evidence or "unknown".** Every claim cites `path:line` or a quote from the operator.
- **Cheapest adequate tier.** Use code before partial credit, and partial credit before a judge.
  Use an LLM judge only when nothing cheaper can tell good from bad, and say why.
- **Scores run from 0 to 1.** Higher is better.
- **Never invent an upstream verdict.** If a field you read is missing, ask for it or reconstruct
  it from the code and list it under `out.reconstructed`.

## Step 0: Deployment type

Place the agent in one type; it tells you where outputs and labels live.

| type | outputs are defined in | labels / outcomes live in |
|---|---|---|
| `coding-harness` | skill files, CLAUDE.md / AGENTS.md | PR review outcomes, reverted diffs |
| `gateway-agent` | workspace skills | corrections in the channel |
| `framework-app` | structured-output schemas in code | thumbs, escalations, task outcomes, traces |
| `prompt-program` | DSPy / Ax signatures | eval sets, existing metric functions |
| `hosted-nocode` | instructions in the UI | ratings, edits, conversation exports |

## Step 1: Read the signal

From the `signal-card` envelope read `chosenSignal` and `slots.artifact`. Without an envelope, ask
for the one line "My agent gets better when ___ goes up", or reconstruct it from the code.

## Step 2: List the output fields the signal touches

Name each output field (with `path:line` where it is defined) whose value changes the signal. A
field the signal doesn't touch goes in `fieldsUnscored`, with no metric.

## Step 3: Pick a tier per field

| tier | use when | examples |
|---|---|---|
| `code` | the right answer can be checked exactly | exact match, verbatim span, schema valid, label equality |
| `partial` | closeness matters more than exactness | token overlap, set F1, numeric tolerance |
| `judge` | only a reader can tell | an LLM grades against a written rubric |

For every `judge` metric, write the rubric (criteria and pass conditions) and one line on judge
bias: position, length, and self-preference when the judge shares a model with the agent.

## Step 4: Write the signature three ways

- **Python (DSPy shape):** `def metric(example, pred, trace=None) -> float`. DSPy accepts a
  float, int or bool; return a float in 0..1.
- **TypeScript (Ax shape):** `({ prediction, example }) => number`, normalized to 0..1.
- **Plain language:** one sentence a reviewer can check by hand.

For GEPA, say whether the metric can also return feedback text
(`dspy.Prediction(score=..., feedback=...)`). Code-tier metrics usually can: say which check failed.

## Step 5: Baseline and labels

- **Baseline:** what a do-nothing version scores (always the majority label, an empty answer, or the
  current prompt unchanged). Without a baseline, no gain can be claimed.
- **Labels needed:** for each metric, the reference values it compares against (`labelsNeeded`).
  `gold-set` plans how to collect them.

## Output

```markdown
# Metric Signature: <agent name>

**Signal:** <chosenSignal, and where it came from>

| Metric | Output field | Tier | Labels needed | Feedback text |
|---|---|---|---|---|

<for each metric: the Python, TypeScript and plain-language signatures>

**Baseline:** <do-nothing version and its expected score, or "unknown (ask: …)">
**Unscored fields:** <fields the signal doesn't touch>
```

Then the envelope as the last fenced block, then the footer line. The envelope must parse as
YAML: put double quotes around every free-text value (names, `title`, `why`, `do`, each
`evidence` item, claims), because a `: ` or a leading quote inside an unquoted value breaks the
parse. Every key keeps its colon, as in the template (`effort: S`, `impact: medium`); write `medium`,
not `med`.

```yaml
sia:
  skill: metric-signature
  version: 1
  agent: { name: "<name>", summary: "<one line>" }
  deploymentType: <type>
  in_ref: signal-card#v1          # or "none"
  out:
    metrics:
      - name: vendor_exact
        outputField: vendor_id
        tier: code                # code | partial | judge
        range: "0..1"
        feedbackText: true
        labelsNeeded: [approved_vendor_id]
        signature:
          python: "def metric(example, pred, trace=None) -> float: return float(pred.vendor_id == example.approved_vendor_id)"
          typescript: "({ prediction, example }) => (prediction.vendor_id === example.approved_vendor_id ? 1 : 0)"
          plain: "1 when the extracted vendor equals the vendor the AP clerk approved, else 0"
    baseline: "always the most frequent vendor"
    fieldsUnscored: [notes, currency]
  recommendations:
    - id: ms-1
      effort: S                   # S | M | L
      impact: high                # high | medium | low
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

## Gotchas

- A metric on a field nothing reads optimizes nothing. Check `fieldsUnscored` against the consumers.
- Exact match on free text almost always reads as 0. Use partial credit or a verbatim span instead.
- A judge that shares a model with the agent tends to prefer its own outputs. Name that bias.
- A boolean metric is fine for DSPy demo bootstrapping, but averaging over examples needs floats.

## Examples

- Invoice extractor with a `vendor_id` field and the clerk's approved value → one `code` metric
  (vendor exact match), labels = approved vendor, baseline = most frequent vendor; every other
  output field the signal doesn't touch goes in `fieldsUnscored`.
- Meeting-summary bot whose users edit the summary before posting → a `partial` metric (token
  overlap of the draft with the posted version); "summary was useful" ratings noted as a slower
  signal, not the metric.
