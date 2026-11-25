---
name: modes-of-thinking
description: Use for difficult decisions or when the user invokes think, deepthink, council, sweep, reframe, decide, forecast, redteam, experiment, or debrief. Routes problems through fitting lenses, evidence hygiene, experiments, and bounded independent-agent councils.
---

# Modes of Thinking

Improve the reasoning process, not the amount of prose. Classify the problem, select only the lenses that can change the answer, distinguish evidence from interpretation, and finish with a decision, test, or update.

Do not reveal private chain-of-thought. Present conclusions, supporting evidence, material assumptions, uncertainty, and concise decision rationale.

## Parse the request

Accept this portable form:

```text
$modes-of-thinking <mode> [agents=N] <problem>
```

Also accept a platform command adapter such as `/council` or `/decide`. If the user names no mode, use `think`. Preserve the user's original objective and any authorization boundaries; a reasoning mode does not grant permission to edit files, contact people, publish, purchase, or perform other external actions.

## Route before analyzing

1. State the decision or question in one sentence.
2. Identify the problem class:
   - truth or diagnosis
   - structure or representation
   - choice or allocation
   - prediction or risk
   - strategy or incentives
   - invention or design
   - failure or abuse
   - communication or human behavior
   - ethics or legitimacy
   - execution or learning
3. Select the smallest useful lens stack:
   - **Primary lens:** best fits the problem class.
   - **Challenge lens:** searches for a competing explanation, failure, or value conflict.
   - **Action lens:** converts analysis into an observable next step.
4. Add human and time-horizon lenses only when people will adapt, consequences compound, or the choice is hard to reverse.
5. Use tools and current sources when facts can be checked. Never replace missing evidence with confident role-play.

Read [references/model-atlas.md](references/model-atlas.md) when lens selection is unclear, the user invokes `deepthink`, `sweep`, or `reframe`, or the task crosses several domains.

## Protect the reasoning budget

Save context on transport and repetition, not on reasoning quality. Spend the available budget on framing, competing explanations, decision-relevant evidence, uncertainty, synthesis, and verification.

- Search or inspect an index before reading large sources in full. Start with metadata, filenames, headings, targeted queries, or bounded ranges; expand only when the narrower evidence is insufficient.
- Load only the references and tool definitions needed for the current phase. Use deferred tool discovery when the runtime supports it.
- Batch or parallelize independent read-only calls when safe. Use direct calls for adaptive investigation, approvals, mutations, and evidence that must remain visible for citation or review.
- Request compact structured results and only the fields, rows, files, lines, or date ranges needed. Preserve source IDs, URLs, and file paths so evidence can be reopened without fetching it again.
- Reuse verified evidence. Do not reread unchanged sources or send the same large context to several agents when a compact shared evidence packet will do.
- After a research phase, carry forward the objective, decisive facts, assumptions, disagreements, uncertainty, provenance, and open questions. Drop duplicated excerpts, tool boilerplate, and narration of completed steps.
- Stop gathering when another call is unlikely to change the conclusion, confidence, or next test. Do not stop before required evidence, material disagreements, or requested verification are resolved.

Do not save tokens by hiding uncertainty, omitting contrary evidence, skipping validation, or compressing away user constraints. Read [references/efficiency-protocol.md](references/efficiency-protocol.md) for multi-source research, large files or datasets, repeated tool use, or any council.

## Maintain reasoning hygiene

Separate these explicitly whenever they could be confused:

- **Observed:** directly verified facts or supplied evidence.
- **Inferred:** conclusions drawn from those facts.
- **Assumed:** claims currently accepted without verification.
- **Valued:** preferences, priorities, or ethical commitments.
- **Unknown:** missing information that could change the result.

Use calibrated ranges instead of decorative precision. Name the strongest evidence that would reverse the recommendation. Reduce confidence as projections move farther into the future.

Do not use every available model. More lenses can create repetition, false balance, and analysis paralysis. Stop when another lens is unlikely to change the decision or experiment.

## Run the selected mode

### `think`

Use the three-lens stack. Return:

1. **Frame** — the real question and success condition.
2. **What matters** — observed facts, assumptions, and unknowns.
3. **Lens findings** — one compact section per selected lens.
4. **Verdict** — the best current answer and confidence.
5. **Next move** — one action or information-gathering step.

### `deepthink`

Use this only for consequential, ambiguous, or cross-domain questions. Work through:

1. objective and exclusions
2. evidence, inference, assumptions, and values
3. primitives, constraints, bottleneck, and useful representation
4. causal mechanism and plausible rival explanation
5. ranges, base rates, correlated risks, and ruin conditions
6. materially different options, including inaction
7. actor reactions, adaptation, and time horizons
8. failure, abuse, harm, reversibility, and legitimacy
9. smallest decision-changing experiment
10. prediction, confidence, thresholds, and review point

Compress empty or irrelevant stages rather than padding them.

### `council`

Read and follow [references/council-protocol.md](references/council-protocol.md).

If `agents=N` is absent, ask the user how many agents to spawn before spawning anything. Offer **2, 3, or 4** and wait for the answer. Do not select a default silently. Treat ordinary chat as interactive even when no structured question tool exists; ask in plain text when necessary. Treat a run as non-interactive only when the runtime explicitly identifies it as batch, headless, or unable to receive another user message. In that case, stop and request `agents=N`.

The main agent is the chair; the requested number counts only spawned council members. Reject counts outside 2–4. Do not permit nested delegation. Keep council members advisory and read-only. The chair alone synthesizes and performs any separately authorized execution.

If the runtime lacks enough simultaneous slots, use independent sequential waves without lowering the requested count. If it has no subagent capability, say so and offer a clearly labeled single-agent simulation. Never claim that subagents were spawned when perspectives were only simulated.

### `sweep`

Select four to six materially different disciplines from the atlas. Give each one decision-relevant question and one finding. Do not spawn agents. End with:

- what several lenses agree on
- the most important disagreement
- the overlooked risk or opportunity
- the next action

### `reframe`

Translate the problem into three to five different representations, such as a causal graph, state machine, queue, game, portfolio, feedback loop, timeline, or experiment. For each representation, state what becomes easier to see. Choose the representation that most simplifies the next decision.

### `decide`

List real options, including inaction where valid. Define decision criteria before scoring options. Consider opportunity cost, reversibility, downside boundaries, information value, and performance across plausible futures. Recommend one option, state confidence, and identify the condition that would switch the choice.

### `forecast`

Define the event and time horizon precisely. Use relevant base rates where available. Return a plausible range or scenario distribution, not a single unsupported number. State key drivers, correlated risks, confidence, and the observations that would trigger an update.

### `redteam`

Attack the proposal through at least three relevant failure sources, chosen from malicious actors, careless use, incentives, dependency failure, scale, bad data, environmental shocks, and institutional response. Rank failure paths by likelihood times consequence. Pair each serious path with detection, containment, recovery, or an explicit accepted risk.

### `experiment`

Identify the assumption carrying the most decision risk. Design the smallest safe test that can meaningfully update it. Specify:

- prediction and current confidence
- test population or environment
- observable metric
- success, stop, and scale thresholds
- cost and timebox
- review date or trigger
- what decision follows each possible result

### `debrief`

Require a prior expectation and an observed outcome. Compare them without hindsight rewriting. Identify which assumption, mechanism, or execution step failed; distinguish a bad process from ordinary variance; update confidence; and record one rule or next experiment.

## Finish cleanly

Match depth to stakes. A routine choice may need five lines; a major decision may need the full protocol. End every response with a concrete conclusion, the uncertainty that matters most, and the next move. Do not end with a menu of generic possibilities when the evidence supports a recommendation.

Read [references/runtime-adapters.md](references/runtime-adapters.md) only when platform invocation, agent capacity, or fallback behavior needs clarification.
