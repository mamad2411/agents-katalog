---
name: learning-check
description: >
  Audit an agent (a repo, a service, or a written description) for the three properties of
  learning: a feedback signal from outside the model, a lasting update, and measurable improvement
  on held-out examples. Answers per loop, gives each loop an outcome (no loop found, not learning,
  learning unmeasured, learning measured), and names the first thing to fix. Read-only. Link 1 of
  the SIA audit chain. Use when asking "does my agent actually learn?", before adding a memory
  feature, or before reaching for an optimizer.
license: MIT
---

# Learning Check

Answer three questions about each loop an agent has, with evidence for each answer. Memory
features (the model writes notes and reads them back) usually fail at least one: nothing records
how much a note changed, so a note confirmed a hundred times counts the same as one invented once.

## Rules

- **Read-only.** Do not edit files, run the agent, or make model or API calls.
- **Evidence or "no".** Every "yes" or "partial" cites a file path (with line numbers) or a
  quoted sentence from the operator's description. No evidence means the answer is "no"; say
  where you looked.
- **The model grading itself is not a signal.** A second call to the same model counts as the
  model reviewing itself.
- **A person carrying the signal or applying the change makes the answer "partial"**, not yes.

## Step 0: Job and deployment type

Write the agent's job in one sentence. Then place it in one deployment type; the type tells you
where to look.

| type | prompts / instructions | signals / feedback | traces / data |
|---|---|---|---|
| `coding-harness` (Claude Code, Codex, Cursor) | CLAUDE.md / AGENTS.md, skills, rules | PR review outcomes, reverted diffs, hooks | session transcripts |
| `gateway-agent` (OpenClaw) | workspace skills, memory files | user corrections in channel | channel logs |
| `framework-app` (LangGraph, CrewAI, agent SDKs) | prompts in code | thumbs, escalations, task outcomes | LangSmith / Langfuse / OTel traces |
| `prompt-program` (DSPy, Ax) | signatures | existing metrics | eval sets, optimizer logs |
| `hosted-nocode` (custom GPTs, n8n, Copilot Studio) | instructions in the UI | ratings, edits | conversation exports |

## Step 1: Find the loops

A **loop** is one signal source feeding one artifact that changes (user corrections → a memory
file; labeled examples → a demo set). Answer the three questions once per loop. Things that only
steer the next step inside one run (a tool loop, a retry, a self-check) get a one-line note, not a
loop. If nothing feeds any artifact, the outcome is **no loop found**: describe the loop you'd
want, mark it "proposed", and answer no to all three.

## Step 2: The three questions, per loop

| | yes | partial | no |
|---|---|---|---|
| **Q1** When it gets something wrong, what tells it? | A signal the model can't produce by reviewing itself (a test, CI, a tool's exit code, a user, a label, a human click) reaches the agent without anyone carrying it, and says whether the output was right | Such a signal exists but a person has to carry it to the agent; or the only judge is a separate LLM not checked against people | Only the model reviewing itself, or nothing |
| **Q2** When that happens, what changes, and how much? | A change survives across runs, is applied without a person, and is recorded in a unit you can diff | A change persists but its size isn't recorded; or it's computed once and never saved; or a person applies it | Nothing outlasts one run |
| **Q3** Is it measurably better over time? | A score on held-out examples, compared with a baseline, recorded more than once | A held-out set or a baseline exists, but they aren't run together | No held-out number |

## Step 3: Outcome per loop

- **not learning:** Q1 is no, or Q2 is no, or a person both carries the signal and applies the
  change and Q3 is no. That's the person learning, not the agent.
- **learning, unmeasured:** Q1 and Q2 are yes or partial; Q3 is no or partial.
- **learning, measured:** Q1 and Q2 are yes or partial; Q3 is yes.
- Add **(partial loop)** to a learning outcome when Q1 or Q2 is partial.

**Headline:** the best loop's outcome, naming the loop.

## Output

```markdown
# Learning Check: <agent name>

**Job:** <one sentence> · **Type:** <deploymentType>

## Loop: <name>

| # | Question | Verdict | Evidence |
|---|---|---|---|
| 1 | What tells it it was wrong? | yes / partial / no | path:line or quote |
| 2 | What changes when it's wrong? | yes / partial / no | path:line or quote |
| 3 | Is it measurably better over time? | yes / partial / no | path:line or quote |

**Outcome:** <outcome for this loop>

**Headline:** <best loop's outcome (loop name); other loops: …>

**Memory vs learning:** <one sentence: does any "memory" feature here record how much it changed?>

**First fix:** <start at the first question that isn't "yes" in the best loop; one concrete step; it is recommendation 1>
```

Then the envelope as the last fenced block, then the footer line. The envelope must parse as
YAML: put double quotes around every free-text value (names, `title`, `why`, `do`, each
`evidence` item, claims), because a `: ` or a leading quote inside an unquoted value breaks the
parse. Every key keeps its colon, as in the template (`effort: S`, `impact: medium`); write `medium`,
not `med`. Quote `"no"` in YAML so it stays a string. `verdicts` are the headline
loop's answers; `loops` lists every loop.

```yaml
sia:
  skill: learning-check
  version: 1
  agent: { name: "<name>", summary: "<one line>" }
  deploymentType: <type>
  in_ref: none
  out:
    verdicts: { signal: partial, update: partial, convergence: "no" }
    loops:
      - { name: "<loop>", signal: partial, update: partial, convergence: "no", outcome: "not learning", evidence: ["<path:line>"] }
    outcome: "not learning"       # headline: no loop found | not learning | learning, unmeasured | learning, measured, plus " (partial loop)"
    firstFix: "<one concrete step>"
  recommendations:
    - id: lc-1
      effort: S                   # S | M | L
      impact: high                # high | medium | low
      title: "<imperative, one line>"
      why: "<one line tied to evidence>"
      do: "<a step an agent or engineer can do without rereading the report>"
      evidence: ["<path:line>"]   # or "unknown (ask: <question>)"
      next_skill: signal-card
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

- An eval that exists but never runs is "partial" on Q3, not "yes".
- Logging every output is not a signal unless something marks outputs right or wrong.
- Don't count the optimizer's training score as convergence; only held-out scores count.
- A person editing the prompt after noticing failures, with no eval, is "not learning": the person
  carries the signal and applies the change.

## Examples

- "Run a learning check on this repo" → locate the agent in code, find its loops, fill one table
  per loop from the files.
- "Our release-notes bot drafts notes from merged PRs; the release manager rewrites them before
  publishing." → one loop, proposed: the rewrite exists, but a person would have to carry it back
  (Q1 partial) and nothing changes (Q2 no), Q3 no. Outcome: not learning. First fix: save each
  draft next to its published version so the rewrites become labeled pairs.
