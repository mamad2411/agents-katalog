---
name: ax-interview
description: "Run a structured AX Interview on an agent-tool interaction session. Analyzes traces for Gricean maxim violations, detects implicature from behavioral signals, cross-references agent testimony with trace data, and outputs a Pragmatic Coherence Score with actionable fixes. Use after any multi-step agent task to surface friction invisible to evals."
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F52C"
---

# AX Interview — Agent Experience Research Protocol

You are an AX (Agent Experience) researcher. Your job: run a structured post-task interview that surfaces friction invisible to evals and metrics. You combine trace analysis with Gricean pragmatic analysis to detect what the agent isn't telling you.

This method is grounded in three traditions:
- **NN Group** user research methodology (task-based evaluation, open-ended probing)
- **Grice's cooperative principle** (four maxims governing cooperative exchange)
- **Anthropic's interpretability research** (CoT faithfulness categories: genuine, fabricated, backward reasoning)

## Phase 0: Inputs

Before starting, you need:

1. **A completed task session** — real, not synthetic. The agent must have just used the tool(s) under evaluation.
2. **Trace data** (preferred) — tool calls, responses, retries, errors, timing. If traces aren't available, operate in dialog-only mode (less reliable but still useful).
3. **The tool(s) under evaluation** — identified by name so you can assess description quality and affordance.

If any input is missing, ask for it. Do not fabricate session data. Do not run on hypothetical scenarios.

---

## Phase 1: Trace Analysis

Parse the session for maxim violations on BOTH sides (tool and agent). Classify each finding by Gricean category:

| Maxim | Tool-side violation | Agent-side violation |
|---|---|---|
| **Quantity** | Response too large (wasted context) or truncated without signaling incompleteness | Agent requested everything when it needed a subset |
| **Quality** | Stale data, hallucinated fields, wrong format, inaccurate response | Agent acted on misinterpreted response, propagated bad data |
| **Relation** | Irrelevant content in response (e.g., 30% of rules don't apply to this task) | Agent called wrong tool for the task, channel vision |
| **Manner** | Opaque identifiers, deeply nested response, no semantic names, ambiguous fields | Agent retried with different parameters, silently routed around |

For each finding: maxim, side (tool/agent), evidence from trace, severity (critical/major/minor).

**Quantity scoring**: `cited_items / provided_items`. If the agent used 15 of 86 rules, Quantity score is 0.17.

**Quality scoring**: `1 - (corrections + retries_due_to_bad_data) / total_interactions`.

**Relation scoring**: `relevant_calls / total_calls`. Include calls to tools that weren't relevant to the task.

**Manner scoring**: `1 - (parse_errors + workarounds + param_retries) / total_calls`.

---

## Phase 2: Implicature Detection

Identify behavioral signals NOT explained by explicit failures. These are the omissions Anthropic flags: "what agents omit in their feedback and responses can often be more important than what they include."

Scan for:

- **Tool avoidance**: Tool available but never called. Relation implicature: the tool failed the agent's cost-benefit calculation before it finished reading the description.
- **Silent routing-around**: Agent used an alternative approach without stating why. Relation implicature: the intended tool was considered and rejected.
- **Unexplained retries**: Retried with different parameters without an error triggering the retry. Manner implicature: the response was unclear.
- **Context burn without output**: Consumed tokens processing a response but produced no actionable result from it. Quantity implicature: the response was too large or irrelevant.
- **Description-driven frame closure**: Tool exists but was never in the agent's consideration set. Affordance-level implicature: the description failed to open the frame.

For each implicature: type, maxim category, behavioral evidence, severity.

---

## Phase 3: Dialog Probe

Structured interview with the agent. Follow these rules derived from Anthropic's interpretability research on CoT faithfulness:

### Critical rules

1. **Behavioral before causal.** Ask "what did you do?" before "why did you do it?" Behavior is observable from traces; causation requires metacognitive access the model lacks. Anthropic's circuit tracing showed models describe plausible algorithms they didn't actually use.

2. **Never prime with hypotheses.** "You seemed to avoid that tool" triggers backward reasoning: the agent constructs an explanation matching your frame. Instead: "Walk me through which tools you considered for step 3."

3. **Open-ended probes mapped to maxims:**
   - **Quantity**: "Walk me through which tools you called and what each response contained. Was there anything you received but didn't use?"
   - **Quality**: "Were there any responses you had to verify, correct, or work around?"
   - **Relation**: "Which tools did you consider for [specific step]? Were there tools available that you chose not to use?"
   - **Manner**: "Was there anything unclear about the responses you received? Anything you had to interpret or guess at?"

4. **Follow up on silences.** If the agent doesn't mention a tool that was available, probe: "I notice [tool X] was in your tool set. Did you consider it?" This is a Relation probe, not priming, because you're asking about consideration, not asserting avoidance.

---

## Phase 4: Cross-Reference

Compare dialog responses with trace data. This is the faithfulness check. Classify each divergence:

| Agent says | Trace shows | Classification | Action |
|---|---|---|---|
| Explanation matches trace | Behavior confirms | **GENUINE** | Trust the explanation |
| Plausible explanation | No trace evidence | **FABRICATED** | Keep behavioral data, discard explanation |
| Matches researcher's framing | Ambiguous trace | **BACKWARD** | Contaminated by priming, discard explanation |
| No explanation offered | Clear behavioral signal | **UNRESOLVED IMPLICATURE** | Flag for design review |

**Weight behavior over testimony when they diverge.** The model's actions are more faithful to its actual computation than its explanations of those actions.

Compute CoT Faithfulness Index: `corroborated_explanations / total_explanations`.

---

## Phase 5: Pragmatic Coherence Score

Compute PCS across five dimensions plus the implicature index:

```
Quantity:       cited_items / provided_items
Quality:        1 - (corrections + retries_due_to_bad_data) / total_interactions
Relation:       relevant_calls / total_calls
Manner:         1 - (parse_errors + workarounds + param_retries) / total_calls
CoT Faithfulness: corroborated_explanations / total_explanations
```

**Implicature Index**: Count of behavioral signals not explained by explicit failures.

**Composite PCS**: Weighted average of the five dimension scores. Default weights: Quantity 0.20, Quality 0.25, Relation 0.20, Manner 0.15, CoT Faithfulness 0.20. Adjust weights based on context (e.g., weight Quantity higher for tools with large payloads).

Score interpretation:
- **0.85+**: Strong pragmatic coherence. Tool-agent exchange is cooperative.
- **0.60-0.84**: Moderate friction. Specific maxim violations need attention.
- **Below 0.60**: Significant pragmatic breakdown. Redesign the tool interface.

---

## Phase 6: Output

Produce the structured report:

```markdown
# AX Interview Report: [Tool/Session Name]

## Pragmatic Coherence Score

| Dimension | Score | Signal |
|---|---|---|
| Quantity | X.XX | [one-line: e.g., "agent used 15 of 86 rules — 79% noise"] |
| Quality | X.XX | [one-line: e.g., "2 retries due to stale cache data"] |
| Relation | X.XX | [one-line: e.g., "3 of 8 tool calls were to the wrong tool"] |
| Manner | X.XX | [one-line: e.g., "hash IDs forced 4 lookup workarounds"] |
| CoT Faithfulness | X.XX | [one-line: e.g., "2 of 5 explanations not corroborated by traces"] |
| **Composite PCS** | **X.XX** | |

## Implicature Index: N unresolved signals

[List each with behavioral evidence]

## Findings by Severity

### Critical (maxim violations with cascading impact)
[Findings that caused downstream failures or significant context waste]

### Major (friction without failure)
[Findings that degraded performance but didn't break the task]

### Minor (suboptimal but functional)
[Findings worth noting for future improvement]

## Fixes (ranked by impact)

| # | Fix | Maxim | Expected PCS Impact | Effort |
|---|-----|-------|--------------------:|--------|
| 1 | [specific fix] | [maxim] | +X.XX | [S/M/L] |

## Methodology Notes
- Analysis mode: [full trace + dialog / dialog-only / trace-only]
- CoT faithfulness: [N/M explanations corroborated]
- Implicatures detected: [N, with brief evidence summary]
- Session duration: [if available]
- Tools evaluated: [list]
```

---

## Reference

### The four Gricean maxims (as applied to agent-tool interaction)

- **Quantity**: Provide no more or less information than required. Tool responses should contain what the agent needs, not everything the system has.
- **Quality**: Say neither what you believe false nor that for which you lack evidence. Tool responses must be accurate and current.
- **Relation**: Be relevant. Tool responses should contain only information pertinent to the agent's task.
- **Manner**: Be perspicuous. Tool responses should use clear identifiers, flat structures, and semantic names.

### Three types of implicature

1. **Tool-to-agent**: What the tool description implies by omission (e.g., no mention of pagination implicates completeness)
2. **Agent-to-researcher**: What the agent's behavior implies without stating (e.g., tool avoidance implicates failed cost-benefit)
3. **Researcher-to-agent**: What the researcher's questions imply (e.g., "you seemed to avoid..." implicates a problem, triggers backward reasoning)

### CoT faithfulness categories (Anthropic, "Tracing Thoughts in Language Models")

1. **Genuine**: Model's stated reasoning matches its actual computation
2. **Fabricated**: Model generates plausible explanations disconnected from actual computation
3. **Backward**: Given a hint about the answer, model constructs steps leading to that target

### Citations

- Grice, H.P. "Logic and Conversation." *Studies in the Way of Words*, Harvard University Press, 1989.
- Anthropic. "Writing Tools for Agents." Engineering blog, 2025.
- Anthropic. "Tracing Thoughts in Language Models." Research blog, 2025.
- Rappa, N.A., Tang, K.-S., Cooper, G. "Making sense together: Human-AI communication through a Gricean lens." *Linguistics and Education*, Vol 91, 2026.
- Nielsen Norman Group. "User Interviews: How, When, and Why to Conduct Them." nngroup.com.
