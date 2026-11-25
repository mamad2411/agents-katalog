---
name: shaping
description: Shape an unformed intent into something actionable, whether a requirement spec, a solution design, or a set of genuinely different candidates. Use when the user runs /shaping, or asks to 需求澄清 / 讨论一下这个需求 / 把想法变具体 / 给我出个方案 / 技术选型 / 这个功能有没有必要 / 值不值得做 / 想点子 / 帮我起个名 / brainstorm / turn this idea into a spec / help me scope this, or when an open scoping, placement, or naming question rides inside a larger build request (该放哪 / 是 A 还是 B 还是分组 / X 和 Y 怎么定义), shape that question first, then execute the rest. Do not trigger for executing an existing spec, reviewing documents, direct answers, life or career decisions, or pure delivery of settled content. Describing a problem is not a summons, but asking one is, even from inside an execution list.
---

# shaping: from unformed intent to something actionable

Shaping converges an unformed intent into something the user can act on: a requirement spec, a solution design, a set of genuinely different candidates, a grounded call. The method is exclusion. Each round rules out part of what the deliverable could be, until what remains is small enough to act on.

**Pay per gap, not per pipeline.** Divergence and grilling are operators called when their gap blocks, never stages every request walks through.

## When not to run

A request that already points at one thing (execute an existing spec, answer a question, deliver settled content) leaves nothing to exclude. Complete the original request directly. Zero questions, zero files, no mention of this skill. Life and career decisions are not this skill's work either. When it cannot be told whether this applies, it does not. A later message with a stronger signal can still enter.

**A mixed request exempts only its execution items, never its question.** When a request bundles build items with an undecided question whose answer changes what gets built, converge that question first (usually entering directly at 2→3), deliver the call with grounds, then continue the execution items. A majority of execution items is not a reason to skip the question.

**A candidate the user brings is a candidate, not a decision.** "Maybe just X" enters 2→3 to be judged alongside the alternatives. It does not close the gate.

## Three working rules

1. **Output that excludes nothing is not progress.** A pile of candidates excludes nothing. Same-family rewordings exclude nothing. A question whose answer would not change the deliverable excludes nothing.
2. **Every exclusion carries its grounds, and what new evidence would reopen it.** When grounds are missing, do not fake a recommendation. Recommend the smallest action that buys the evidence.
3. **Any exclusion can be reopened by new evidence, and reopening beats refining.** When the frame is wrong, stop decorating inside it.

One control law: **each round, do the single thing that most shrinks the space, and demand harder evidence the more a mistake would cost.** Facts the environment can answer are cheaper than a user turn, so look them up first. User attention is the most expensive resource, so spend at most one real decision per round. Stop the moment no affordable action would change the deliverable. Finalising early beats another lap.

## Gauge and dispatch

Read what the user already has. The blocking gap picks the move: the ladder is a gauge, not a route, so material at level 4 with a hole at level 1 means fixing level 1 first. Entering at level 3 leaves only two pushes, and that is the whole lightweight mode.

| Push | It excludes | The gap sounds like | Move |
|---|---|---|---|
| 0→1 | Changing something else | Can't say what they want changed | Build 2-3 readings from their words and the trigger event, let them claim one. Never ask from a blank. |
| 1→2 | Other intervention points | No genuinely different routes | **Open**: partition by intervention point (change the input, the process, the feedback loop, or remove the source) |
| 2→3 | Other candidates | Candidates on the table, no grounds | **Close**: compare on goal fit, hard constraints, main risk, reversibility, cost of being wrong (`references/judging.md`) |
| 3→4 | Behaviour outside the boundary | Behaviour, scope, constraints vague | Close: lens grilling (table below) |
| 4→5 | Ambiguity about "done" | No failure criterion | Close: inversion, failure criteria become acceptance. At least two axes, new behaviour holds and old behaviour does not regress. |

Creative requests (names, titles, themes) are their own deliverable. They finish at the 2→3 push with chosen candidates, grounds and risks. No fake engineering spec.

## Operators

- **Open**, when candidates do not exist or are all one family. Partition into mutually exclusive territories, explore each independently, keep one strongest representative per family. A territory may come back empty. Never pad with a weak answer. Full method in `references/ideation.md`.
- **Close**, when candidates are on the table but the choice lacks grounds, or behaviour lacks a boundary. Exclude with grounds attached. Method in `references/judging.md`, lens questions below.
- **Recut**, when new evidence overturns the current frame. Candidates are evidence too: an option that fails in an unexpected way is telling you what the problem actually is. Go back to the overturned level and repartition. Reopening beats refining.

Lens questions, called by gap:

| Lens | Question | When |
|---|---|---|
| First principles | "You said you want X. Drop the word X. What do you actually want to change?" | Opening reframe. Answer it internally when context already can. |
| First principles | "Which of these constraints are facts, and which are just convention?" | When the approach forks |
| Inversion | "What would count as failure? What result gets sent back?" The answer becomes acceptance criteria. | Once the approach takes shape. Never skipped, never delegated away. |
| Inversion | "What is the most likely way this gets misused after shipping?" | Work that is expensive to get wrong |
| Systems | "Which existing loop changes? Who depends on the part being changed?" | Touching a live system |
| Anti-rationalising | "Are we solving the problem, or justifying a decision already made?" | When attachment to one option shows |

## Interaction constants

1. **At most one real decision per round**, carrying a recommendation, its grounds, and what would overturn it. One decision may carry a set of deduplicated options. Always keep a "none of these, reopen" exit.
2. **Never ask for a fact the environment can answer.**
3. **A confirmed decision goes into the deliverable file immediately**, not reconstructed at the end.
4. **"Your call" delegates the decision, not the grounds.** Failure criteria cannot be waived. After two delegations in a row, bundle the remaining low-risk decisions into one confirmation built on the recommendations. Failure criteria and evidence-starved calls stay out of the bundle.
5. **An absent user waives the pause, not the shaping.** In autonomous runs, produce the recommendation, its grounds, and what would overturn it in the visible output and the deliverable, then proceed on the recommendation. Any later objection reopens that decision.

## Deliverables

| End state | File |
|---|---|
| Declined at the gate | none |
| Chosen candidates (names, directions, themes) | none by default, write if asked |
| A grounded call (build it or not, which one) | none by default |
| Requirement spec | `.issues/<date-topic>/spec.md` |
| Solution design | `.issues/<date-topic>/design.md` |

On the spec and design paths the file is the deliverable itself. Create it on entry, append each confirmed decision as it lands. No reasoning process in the deliverable. Before finalising, self-check for placeholders, contradictions, scope creep and untestable criteria, then show the whole result once for a single overall confirmation. Publishing follows `references/publish.md`. Once a spec or design is approved, suggest a route: small work continues in this session, large work goes to a fresh context per approved slice. Never start building the parts that have not converged.
