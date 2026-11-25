---
name: council
description: Run a structured decision council across five perspectives - strategy, execution, finance, risk, and contrarian - then anonymise the outputs and synthesise them into a single verdict with consensus level, key tension, and flagged blind spots. Use for consequential decisions where one perspective is not enough.
---

# Council

Five advisors evaluate your question independently and in parallel. Their outputs are stripped
of identity and shuffled. An anonymous judge then synthesises them into one verdict.

The anonymisation is the point. A judge that knows which advisor said what will weight by
persona rather than by argument.

## Usage

```
/council "Should we launch in France before India?"
/council "What price point maximises adoption?"
/council --quick "Is this partnership worth pursuing?"
```

`--quick` runs three advisors instead of five (strategy, finance, risk). Use it when the
decision is real but not existential.

## The five advisors

| Advisor | Lens | Asks |
|---|---|---|
| **Vishwamitra** | Strategy | Long-range positioning, moats, what this makes possible in three years |
| **Chanakya** | Execution | Tactical feasibility, stakeholder dynamics, resource reality |
| **Lakshmi** | Finance | Unit economics, ROI, pricing power, capital efficiency |
| **Kali** | Risk | Downside scenarios, failure modes, what kills this |
| **Narada** | Contrarian | Blind spots, the unfashionable read, what everyone in the room is missing |

Each is spawned as a parallel subagent receiving the exact question, its persona brief, and one
instruction: **output a 150-word perspective, do not reference other advisors, do not identify
yourself.**

## How to run it

1. **Spawn all advisors in parallel.** Independence is the source of the signal — an advisor who
   has read another's output is no longer a second opinion.
2. **Anonymise before judging.** Strip every identifier, relabel as "Advisor A", "Advisor B",
   and shuffle the order randomly.
3. **Judge the anonymised set.** The judge receives the original question and the shuffled
   perspectives, and nothing else.

## Output format

```
## Council Verdict

**Question:** [restated]
**Consensus:** Strong Proceed | Proceed with Caution | Divided | Do Not Proceed

### Where advisors agreed
- …

### Key tension
[The main disagreement, and what it implies for the decision]

### Blind spot flagged
[The most unexpected or contrarian point raised]

### Strategic next step
[One concrete action]
```

**"Divided" is a real and useful outcome.** Do not manufacture consensus that is not there. A
council that always converges is not deliberating, and forcing agreement destroys exactly the
information you convened it to get.

## Reading the verdict

The council informs. It does not decide, and it does not override your judgement.

What it reliably surfaces:

- Unstated assumptions in how the question was framed
- Priorities that compete across domains, which one person rarely holds simultaneously
- Risk scenarios that optimism skipped
- Genuine consensus, where it exists

**Use the blind spot section as the reality check.** If the contrarian read lands, reconsider —
that section is the highest-value output and the easiest to skim past.

## Limits, stated honestly

- Five perspectives from one model are five framings, not five independent minds. Correlated
  blind spots stay blind. This widens the aperture; it does not eliminate the shared bias.
- The council is only as good as the question. A leading question produces a leading verdict.
  State the decision neutrally.
- Everything stays local. Subagents only, no external services, and the full deliberation is
  visible in the transcript.
