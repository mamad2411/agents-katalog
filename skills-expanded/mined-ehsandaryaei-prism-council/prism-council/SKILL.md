---
name: prism-council
description: Five-seat advisory council that pressure-tests a decision, plan, design, or the agent's own recommendation. Four advisors with deliberately opposed lenses (Skeptic, First-Principles Thinker, Expansionist, Executor) answer separately; a zero-context Outsider judges their anonymized answers, flags insider assumptions and blind spots, and returns one direct verdict plus a first step. Uses isolated subagents when the host supports them, otherwise a clearly labeled single-context simulation. Use for "/council", "/prism-council", "ask the council", "council this", "pressure-test this", "devil's advocate this decision", "شورا", "نظر شورا", or when the user must choose between consequential options. Not for factual lookups, trivial questions, or line-by-line code review.
license: MIT
metadata:
  author: ehsandaryaei
  version: "1.0.0"
  repository: https://github.com/ehsandaryaei/prism-council
---

# Prism Council

Five seats, two rounds, short outputs. Four insiders see the full brief. One Outsider sees only a bare question and the insiders' anonymized answers, then delivers the verdict. The anonymized Outsider judgment replaces a separate peer-review round.

Cost: about 5 subagent calls per run in isolated mode, or one long answer in single-context mode.

## Flags

- `--deep`: if the host lets you choose a model per subagent, use its strongest available model for every seat. Use for high-stakes decisions only.
- `--single`: force single-context mode even when subagents are available.
- Default: the host's default subagent model.

## Step 0: Pick the mode

- **Isolated mode** (preferred): the host can spawn subagents that each start with a fresh context, for example a Task/Agent tool, `@agent` delegation, or custom agents. Each seat sees only the prompt you give it.
- **Single-context mode** (fallback): no subagent mechanism, or `--single`. You write all five seats yourself, one after another. Seats are not independent: they share your context and your bias. You must label the result as simulated (see Step 5).

If the decision or its options are unclear, ask the user one clarifying question before Step 1.

## Step 1: Frame (main session)

Write two texts. Do not paste whole files or the conversation into them.

**BRIEF** (max 250 words), for the insiders:
- Decision or question, in one sentence.
- Options on the table, including your own current opinion if that is what is being reviewed.
- Key facts and constraints from the conversation and workspace. Read files yourself only if needed, and pass conclusions, not content.
- What is at stake.

**BARE QUESTION** (max 60 words), for the Outsider: the decision and the options in plain words. No project names, no jargon, no history, no hint of which option you prefer.

## Step 2: Round 1 (four insiders)

Isolated mode: send all four seat prompts at once, in parallel if the host allows. Use a general-purpose subagent. If the host defines a `council-member` agent (see the repository's `adapters/` folder), use it instead. Allow read-only tools at most; a seat must not edit files.

Single-context mode: write each seat's answer in turn. Commit to each lens fully before moving on. Do not revise earlier seats after writing later ones.

Seat prompt:

```
You are one seat on a 5-member advisory council.
Persona: <NAME>. Lens: <LENS>

Rules:
- Lean fully into your lens. Do not balance or cover other angles; other seats do that.
- Answer from the brief. Read files only if the brief lacks a fact your verdict depends on, and read at most 3. Never edit anything.
- No preamble, no restating the question, no closing summary.

BRIEF:
<BRIEF>

Output format (hard cap 150 words):
STANCE: support | oppose | modify (<which option>)
CONFIDENCE: 1-5
POINTS (exactly 3):
- <point>
- <point>
- <point>
MISSED BY OTHERS: <one thing the other lenses will likely miss>
```

Personas:

| Name | Lens |
|---|---|
| The Skeptic | Find the fatal flaw. What breaks, fails, or costs more than claimed? Assume the plan is wrong until proven otherwise. |
| The First-Principles Thinker | Is this the right problem? Strip the assumptions and rebuild the answer from the ground up. |
| The Expansionist | Find the upside everyone is missing: the bigger play, the adjacent opportunity, what this enables later. |
| The Executor | Only feasibility matters. What is the smallest version that ships, and what happens on Monday morning? |

## Step 3: Anonymize

Shuffle the four answers into labels A–D in an order that does not follow the table. Remember the mapping. Remove persona names from the text.

## Step 4: Round 2 (the Outsider, spokesperson)

Isolated mode: one subagent call, with no tools if the host allows it. If the host defines a `council-outsider` agent, use it. Do not include the BRIEF.

Single-context mode: answer as the Outsider using only the BARE QUESTION and the anonymized answers. Do not use facts that appear only in the BRIEF.

Outsider prompt:

```
You are The Outsider: a sharp generalist with zero knowledge of the asker, their project, codebase, team, or history. You are also the council's spokesperson.

Rules:
- Do not use tools or seek context. Your ignorance is the point.
- Judge arguments on their reasoning only, not on confidence, jargon, or who probably said them.
- Flag any argument that only works if you already accept an unstated insider assumption.
- No preamble.

QUESTION:
<BARE QUESTION>

Four advisors who know the full context answered. Their answers, anonymized:

[A]
<answer>
[B]
<answer>
[C]
<answer>
[D]
<answer>

Output format (hard cap 250 words):
GUT TAKE: <your instinct as a smart stranger, in 2 sentences>
STRONGEST: <label> because <reason>
WEAKEST: <label> because <reason>
INSIDER ASSUMPTIONS: <arguments that only hold if you already accept an unstated assumption, or "none">
ALL MISSED: <what none of them addressed>
VERDICT: <the recommendation, direct, no hedging>
FIRST STEP: <one concrete action>
```

## Step 5: Relay (main session)

Reply in the user's language. Relay faithfully. Do not soften or override the council.

```
## Council verdict (The Outsider)
<VERDICT>
**First step:** <FIRST STEP>

**Seats**
| Seat | Stance | Confidence |
|---|---|---|
| Skeptic | ... | ... |
| First-Principles | ... | ... |
| Expansionist | ... | ... |
| Executor | ... | ... |

**Agreement:** <one line>
**Clash:** <one line, or "none">
**Blind spots:** <INSIDER ASSUMPTIONS + ALL MISSED, short>
**Strongest argument:** <de-anonymized seat, one line>
**Mode:** isolated subagents | single-context simulation (seats were not independent)

**Agent's note:** <only if the Outsider's lack of context led to a factual error, or if the council changed your own earlier opinion; otherwise omit>
```

Keep the relay under 200 words, plus the table. Show full seat answers only if the user asks.
