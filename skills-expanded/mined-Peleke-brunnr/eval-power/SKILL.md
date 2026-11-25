---
name: eval-power
description: >
  Decide whether an agent's eval can detect the change you care about, and how to report the
  result: measure the noise floor with repeated zero-change runs, set repetitions per condition,
  choose a bootstrap interval with its unit stated, and grade every existing improvement claim as
  supported, inconclusive or unsupported. Read-only. Link 5 of the SIA audit chain; reads the
  gold-set and metric-signature envelopes. Use before claiming a prompt or optimizer change
  helped, or when two runs gave different numbers.
license: MIT
---

# Eval Power

A score that moved from 0.71 to 0.74 may be noise. This skill works out how much the score moves
on its own, how many runs a comparison needs, and how to state the result so the claim never goes
further than the interval.

## Rules

- **Read-only.** Don't edit files, run the agent, or make model or API calls.
- **Evidence or "unknown".** Every claim cites `path:line` or a quote from the operator.
- **Inconclusive is a result.** An interval that includes zero means the eval can't tell; say so.
- **No claim beyond its interval.** Grade claims as stated by the team; don't restate them more
  strongly.
- **Never invent an upstream verdict.** If a field you read is missing, ask for it or reconstruct
  it and list it under `out.reconstructed`.

## Step 0: Deployment type

| type | where past results live |
|---|---|
| `coding-harness` | CI logs, PR descriptions, notes |
| `gateway-agent` | channel logs, memory file history |
| `framework-app` | trace dashboards, experiment tables (LangSmith, Langfuse) |
| `prompt-program` | optimizer logs, `Evaluate` output, saved result files |
| `hosted-nocode` | exported ratings, spreadsheets |

## Step 1: Read the split, metrics and results

From upstream envelopes read `split` (`gold-set`) and `metrics` (`metric-signature`). Collect any
existing results: scores per run, per fold or per example, with dates.

## Step 2: Noise floor

Recommend running the unchanged system at least twice on the same split (zero-change runs). The
spread between those runs is the smallest gain the eval can distinguish from noise. If the team
has only ever run it once, the noise floor is unknown.

## Step 3: Repetitions per condition

Recommend repetitions per condition from the noise floor: more when zero-change runs disagree,
and at least two whenever the model is sampled at temperature above zero.

## Step 4: Interval

Recommend a percentile bootstrap of the difference between conditions. Resample the same unit the
split groups by: folds if the team cross-validates, groups (customer, conversation, PR) if the
split is grouped, examples only if examples are independent. State the unit.

## Step 5: Interpretation

Write how to read the result:
- interval entirely above zero → supported at that interval
- interval spans zero → inconclusive; the eval can't tell
- interval entirely below zero → the change hurt

Recommend writing down the hypothesis, metric, N and model list before any real-model comparison
run (pre-registration).

## Step 6: Grade existing claims

For each improvement claim a person on the team made (in notes, PRs, commit messages, or the
operator's words): `supported`, `inconclusive` or `unsupported`, with one line why. The agent's own
messages ("Done", "I'll remember that") and claims you infer from an edit are not claims; leave
them out. A score on training data, a single run per
condition, or no baseline makes a claim `unsupported` as stated.

## Output

```markdown
# Eval Power: <agent name>

**Noise floor:** <measured spread, or "unknown: never run twice">
**Reps per condition:** <n, and why>
**Interval:** <method>, resampling <unit>

| Claim | Where | Verdict | Why |
|---|---|---|---|
```

Then the envelope as the last fenced block, then the footer line. The envelope must parse as
YAML: put double quotes around every free-text value (names, `title`, `why`, `do`, each
`evidence` item, claims), because a `: ` or a leading quote inside an unquoted value breaks the
parse. Every key keeps its colon, as in the template (`effort: S`, `impact: medium`); write `medium`,
not `med`.

```yaml
sia:
  skill: eval-power
  version: 1
  agent: { name: "<name>", summary: "<one line>" }
  deploymentType: <type>
  in_ref: gold-set#v1             # or "none"
  out:
    reps: { zeroChange: 2, perCondition: 3 }
    interval: { method: "percentile bootstrap of the difference", unit: vendor }
    interpretation:
      - "interval above zero: supported"
      - "interval spans zero: inconclusive"
    claimVerdicts:
      - { claim: "prompt v3 raised exact match from 0.71 to 0.74", verdict: unsupported, why: "one run per condition, no zero-change run" }
  recommendations:
    - id: ep-1
      effort: S
      impact: high
      title: "<imperative, one line>"
      why: "<one line tied to evidence>"
      do: "<a step an agent or engineer can do without rereading the report>"
      evidence: ["<path:line>"]   # or "unknown (ask: <question>)"
      next_skill: none
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

- Two runs that differ by three points with no zero-change run tell you nothing about the change.
- Bootstrapping over examples when the split is grouped makes the interval too narrow.
- A held-out set re-used to pick among many candidates stops being held out. Keep the test set for
  one final run.
- `claimVerdicts` may be empty when nobody has claimed anything yet. Say so; don't invent claims.

## Examples

- Extraction prompt scored 0.71 then 0.74 on the 25 examples its demos came from → claim
  `unsupported`; recommend a held-out split, two zero-change runs, and a bootstrap over sources.
- Invoice extractor with no results yet → empty `claimVerdicts`; plan zero-change runs on the
  validation split and a bootstrap over vendors.
