---
name: signal-card
description: >
  Name the signal an agent should learn from, in one line ("My agent gets better when ___ goes
  up"), then lay out the self-improvement loop around it: act, take a signal, search for a better
  version, apply it. Fills the three choosable slots (signal, search, artifact) with options found
  in the codebase or the operator's description. Read-only. Link 2 of the SIA audit chain; reads
  the learning-check envelope. Use after learning-check, when an agent has no signal, or when
  "I edit the prompt" is the only improvement path.
license: MIT
---

# Signal Card

Most agents improve only when a person reads output, judges it, and edits the prompt. That
works until it has to scale, run unattended, or survive an audit. This skill writes down the
signal that would let the agent run that loop itself, and the slots around it.

The loop vocabulary (act → signal → search → apply) follows Micheal Lanham's *Self-Improving
Agents* (Manning).

## Rules

- **Read-only.** No edits, no agent runs, no model or API calls.
- **The signal comes from outside the model.** It has one of four types, decided by what is
  recorded per output:
  - **score:** a number or pass/fail per output, whether a test computes it or a person's action
    implies it (a refund issued or not, an order returned, a link clicked, a file downloaded).
  - **preference:** which of two or more outputs for the same input won (A/B, a ranking).
  - **feedback:** words a person wrote about an output ("that date is wrong, use the invoice date").
  - **confidence:** the agent's own estimate, checked against something external.
  Type a signal by its raw form as recorded, not by the number you compute from it: notes a
  reviewer writes are feedback even when you count them. A person keeping or changing one output
  before using it is a score per output (kept unchanged = pass), even when the changed version is
  stored next to it. Preference needs two or more candidate outputs for the same input that a
  person chose between.
- **One signal first.** Propose up to three candidates, then recommend one and say why.
- **Cite what exists.** For each slot, prefer options already present in the code (path:line).
  Mark anything new as "to build".
- **Never invent an upstream verdict.** If a field you read is missing, ask for it or reconstruct
  it and list it under `out.reconstructed`.

## Step 0: Read upstream and place the agent

If a `learning-check` envelope is in context, read `deploymentType`, `verdicts.signal` and
`firstFix`, and reuse its evidence. Otherwise place the agent in one deployment type yourself:

| type | where signals usually are |
|---|---|
| `coding-harness` | PR review outcomes, reverted diffs, CI results |
| `gateway-agent` | corrections in the channel |
| `framework-app` | thumbs, escalations, task outcomes in the app |
| `prompt-program` | labeled examples and existing metric functions |
| `hosted-nocode` | ratings, edits people make before using an output |

## Step 1: Current loop

Describe how the agent improves today in four nodes: agent runs → who reads the output → who
judges it → what gets edited. If a person fills the middle two, say "you are the loop".

## Step 2: Candidate signals

List up to three candidates. For each: what is measured, where it would come from, how often it
arrives, what it costs, and its type: **score**, **preference**, **feedback**, or **confidence**.

## Step 3: The one line

Write: **"My agent gets better when ___ goes up."** The blank names one measurable quantity on a
defined set of examples.

## Step 4: The slots

| Slot | Options | Pick for now |
|---|---|---|
| Signal | score · preference · feedback · confidence | the recommended candidate's type |
| Search | hill-climbing · demo selection (bootstrap few-shot) · an evolutionary optimizer such as GEPA · person reviewing proposals | the cheapest that fits |
| Artifact | instructions · demos · skill file · memory · code | what the search will change |

## Output

```markdown
# Signal Card: <agent name>

**Today:** <four-node loop; "you are the loop" if applicable>

**My agent gets better when <quantity> goes up.**

| Candidate | Type | Source | Frequency | Cost |
|---|---|---|---|---|

**Slots:** Signal = … · Search = … · Artifact = …
```

Then the envelope as the last fenced block, then the footer line. The envelope must parse as
YAML: put double quotes around every free-text value (names, `title`, `why`, `do`, each
`evidence` item, claims), because a `: ` or a leading quote inside an unquoted value breaks the
parse. Every key keeps its colon, as in the template (`effort: S`, `impact: medium`); write `medium`,
not `med`.

```yaml
sia:
  skill: signal-card
  version: 1
  agent: { name: "<name>", summary: "<one line>" }
  deploymentType: <type>
  in_ref: learning-check#v1       # or "none"
  out:
    candidates:
      - { quantity: "<what is measured>", type: score, source: "<path:line or system>", frequency: "per release", cost: "free; already recorded" }
    chosenSignal: "<the recommended candidate's quantity>"
    oneLine: "My agent gets better when <quantity> goes up."
    slots: { signal: score, search: "person reviewing proposals", artifact: instructions }
  recommendations:
    - id: sc-1
      effort: S                   # S | M | L
      impact: high                # high | medium | low
      title: "<imperative, one line>"
      why: "<one line tied to evidence>"
      do: "<a step an agent or engineer can do without rereading the report>"
      evidence: ["<path:line>"]   # or "unknown (ask: <question>)"
      next_skill: metric-signature
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

- "User satisfaction" is not a signal until you say how it's recorded per output.
- A signal that arrives once a quarter can't drive search; pair it with a faster proxy and say so.
- If the honest answer is "when I edit the prompt", that is the finding. Don't dress it up.
- `slots.signal` is the chosen signal's type (score, preference, feedback, confidence), not the
  quantity.

## Examples

- Release-notes bot: "My agent gets better when the share of bullets the release manager
  publishes unedited goes up." Type: score. Search: person reviews proposed instruction changes.
  Artifact: instructions.
- Changelog summarizer: "…when the share of summary quotes found verbatim in the source goes up."
  Type: score. Search: demo selection (bootstrap few-shot). Artifact: demos.
