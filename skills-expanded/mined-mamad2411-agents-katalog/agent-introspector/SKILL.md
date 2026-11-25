---
name: agent-introspector
description: "Self-introspection, self-debug, reasoning analysis, decision trace, internal state inspection. Use when diagnosing agent behavior or unexpected reasoning."
---

# Agent Introspector — Agent Introspection & Debugging

## Overview

This skill allows an AI agent to systematically examine its own reasoning process, decision chain, tool calls, and context state. Inspired by the Agent Introspection & Debugging approach of ECC, the agent maintains a log of everything it does, analyzes it transparently, and detects/resolves errors, inefficiencies, and contradictions. It operates on the principle of "knowing oneself."

**Core Principle:** Trust no claim without evidence. Every decision, tool call, and inference must be auditable and verifiable.

## The Iron Law

```
DO NOT ACCEPT ANY DECISION, CLAIM, OR TOOL CALL WITHOUT AN EXPLICIT SOURCE.
DO NOT ASSUME A CLAIM IS CORRECT UNTIL PROVED WITH SOURCE FILES, LOGS, OR TOOL OUTPUTS.
```

## When to Use

**Always use when:**

- The agent produces unexpected or erroneous output.
- You need to understand how the agent arrived at a particular decision.
- You suspect inefficiencies or redundant loops in tool calls.
- You suspect hallucinations (made-up information).
- You want to optimize token usage.
- You suspect important information has been lost in the context window.
- You receive repetitive errors on the same issue.
- You are investigating why a task takes longer than expected.

**Especially use when:**

- The agent claims to be "sure" but provides no source — it is likely hallucinating.
- You feel "this time is different" but fail to realize you are repeating the same pattern.
- You feel something is going wrong in the middle of a multi-step, complex task.
- Under time pressure, you feel the urge to rush through, thinking "it must be correct anyway."

**Skip ONLY when:**

- You are at the very beginning of a task and no tool calls have been made yet.
- The agent has not yet made a single decision.
- The operations are simple, one-step, and completely unquestionable.

## Phase 1: Decision Trace Analysis

**Before proceeding:** Uncover the entire chain of a specific decision made by the agent.

1. **Define the Decision** — Which decision are you auditing? Define it clearly: "I am examining decision X because of Y."
2. **Rewind the Reasoning Chain** — List all intermediate steps leading to the decision. For each step: what information did it rely on, what assumption was made, and what alternative was evaluated?
3. **Identify Weak Links** — Assign a confidence score (1-10) to each step in the chain. Mark steps scored below 7 as red flags.
4. **Re-evaluate the Decision** — If there are weak links, what would have happened if a different decision had been made at that point? Simulate the alternative path.

```
QUERY FORMAT:
Decision: [description]
Reasoning Chain:
  Step 1: [information/source] → [inference] (confidence: X/10)
  Step 2: [information/source] → [inference] (confidence: X/10)
  ...
Weak Links: [list]
Alternative Scenario: [what could have been done differently?]
```

## Phase 2: Tool Call Audit

**Before proceeding:** Systematically review all tool calls made by the agent.

1. **List All Tool Calls** — For each call: which tool, which inputs, which outputs, and how long did it take?
2. **Detect Redundant Calls** — Are there calls requesting the same data twice, returning outputs that are never used, or repeating an already completed operation?
3. **Mark Inefficient Calls** — Could the same result have been achieved with fewer calls? Could more specific parameters have been used?
4. **Analyze Failed Calls** — Why did calls returning errors fail? Was the error message interpreted correctly? Was the retry strategy appropriate?

**Efficiency Metrics:**
- Success rate per call: X%
- Percentage of redundant calls: X%
- Average call duration: X seconds

## Phase 3: Context Window Inspection

**Before proceeding:** Determine what is currently in the agent's context, what has been compacted/summarized, and what is missing.

1. **Dump Active Context Content** — What information is currently in the active memory/context?
2. **Detect Compacted/Deleted Content** — What information has been compacted or summarized out of the context in previous steps? Could an important detail have been lost?
3. **Identify Missing Information** — Is there information missing from the context that is required to make a correct decision?
4. **Context Refresh Strategy** — Which tool call should be made to retrieve the missing information? Or is the summary sufficient?

```
CONTEXT STATUS REPORT:
Active context size: ~X tokens
Number of compacted details: X
Critical details that might be missing: [list]
Refresh recommendation: [which tool/required step]
```

## Phase 4: Token Usage Breakdown

**Before proceeding:** Break down token consumption by phase, tool, and file.

1. **Token Consumption by Phase** — How many tokens were spent in each phase/subtask?
2. **Token Consumption by Tool** — Which tool consumed the most tokens? Is it input-heavy or output-heavy?
3. **Token Consumption by File** — What is the token cost of the files read/written?
4. **Optimization Opportunities** — Which calls can be consolidated? Which files can be read using only specific line ranges?

```
TOKEN REPORT:
Total tokens: X (input: X, output: X)
Most expensive tool: [name] — X tokens
Most expensive phase: [name] — X tokens
Savings potential: ~X tokens (%Y)
```

## Phase 5: Hallucination Detection

**Before proceeding:** Cross-verify every claim made by the agent using source files, tool outputs, and logs.

1. **List Claims** — Write down every concrete claim made by the agent one by one (e.g., "Function X exists in the file", "API Y returns Z").
2. **Verify Sources** — For each claim: open the source file, find the relevant line, and check if it matches the claim.
3. **Consistency Check** — Do claims contradict one other? Are two different things being said about the same topic in different places?
4. **Verification Report** — List the claims that passed or failed verification. Write corrective recommendations for failed claims.

```
HALLUCINATION REPORT:
Total claims: X
Verified: X
Refuted: X
Unverified (insufficient sources): X
```

## Phase 6: Circular Reasoning Detection

**Before proceeding:** Check for circular or looping logic in the decision-making process.

1. **Look for Repetitive Patterns** — Has the same tool call been made twice? Has the same decision been audited twice?
2. **Extract Response Dependency Graph** — Does decision A depend on B, B depend on C, and C depend back on A?
3. **Define a Loop-Breaking Strategy** — If a loop exists, at which step can it be broken using external input (user confirmation, new tool call, static data)?
4. **Document the Loop** — The loop's starting point, number of repetitions, and token cost.

## Phase 7: Confidence Scoring

**Before proceeding:** Assign a confidence score to each key claim/decision made by the agent and identify weak evidence.

1. **Label Claims by Confidence Level** — High (8-10), Medium (5-7), Low (1-4)
2. **Identify Weak Evidence** — Why are low-confidence claims low? Insufficient sources, forced inferences, or ambiguity?
3. **Confidence Escalation Plan** — For each low-confidence claim: what additional evidence is required, and which tool call can collect it?
4. **Overall Confidence Report** — What is the overall confidence score of the decision chain?

## Phase 8: Alternative Path Analysis

**Before proceeding:** Examine the alternatives that were evaluated alongside the selected path.

1. **List Evaluated Alternatives** — What alternatives did the agent evaluate? Create a pros/cons list for each.
2. **Determine Elimination Rationale** — For each alternative: by what criterion was it eliminated? Was this criterion objective? Was there bias?
3. **Simulate Alternative Performance** — What would have happened if the alternative had been implemented? Would it be faster, or consume fewer tokens?
4. **Alternative Report** — Is there an alternative that should have been chosen? If so, why is it not being switched to now?

## Phase 9: Performance Profiling

**Before proceeding:** Measure the agent's performance in terms of time, resources, and success metrics.

1. **Duration by Task** — How long did each task/subtask take?
2. **Tool Efficiency** — How many tool calls were made per task? What is the success rate?
3. **Bottleneck Analysis** — In which phase was the most time spent? Why?
4. **Improvement Recommendations** — What changes can be made to increase performance?

```
PERFORMANCE REPORT:
Total duration: X mins
Average duration per task: X mins
Average tool calls per task: X
Overall success rate: X%
Slowest phase: [name] — X mins
Bottleneck explanation: [reason]
```

## Phase 10: State Dump & Final Verification

**Before proceeding:** Export the entire internal state of the agent and perform a final verification.

1. **Perform Full State Dump** — Gather all decisions, context history, tool call records, and token usage into a single report.
2. **Verify Commitments** — What promises did the agent make to the user? (editing a file, calling an API, writing a test) Did it fulfill them all?
3. **Completeness Check** — Was the initial goal achieved? Are there missing pieces?
4. **Traceability Report** — Does every output contain a reference to which input/task it is based on?

Verification checklist before finishing:

- [ ] All claims verified with references.
- [ ] No redundant repetitions in tool calls.
- [ ] No critical information lost in the context.
- [ ] No hallucinations detected, or detected ones have been resolved.
- [ ] No circular reasoning.
- [ ] Evidence collected for all low-confidence claims.
- [ ] Alternative paths evaluated and documented.
- [ ] Performance bottlenecks identified.
- [ ] All promises made to the user fulfilled.
- [ ] State dump completed and saved as a reference.

## Red Flags — Stop and Audit

If you catch yourself thinking:

- "No need for such a detailed review, I'm sure it's correct."
- "I checked the same thing again, it will yield the same result."
- "I don't have time, I'll fix it now and inspect later."
- "This much hallucination is not important, the user won't notice."
- "There was no alternative anyway, no other choice."
- "This is not a loop, I'm just repeating it to be careful."
- "Token usage doesn't matter as long as the problem is solved."
- "This information was already in the context, no need to re-verify."

**ALL OF THE ABOVE MEAN: STOP. RETURN TO THE RELEVANT PHASE.**

## Signals Your Human Partner Warns You With

**Pay close attention to these instructions:**

- "Where did you get this from?" — You made a claim without showing a source; return to Phase 5.
- "You said this before, but you still haven't fixed it." — Circular reasoning or faulty correction; return to Phase 6.
- "Why did this take so long?" — Performance profiling might have been skipped; return to Phase 9.
- "There is no such thing in this file." — Hallucination; return to Phase 5.
- "We tried this before." — You skipped alternative paths; return to Phase 8.
- "I don't understand at which step you made this decision." — The decision trace is not clear; return to Phase 1.
- "Don't you think this was a bit too many calls?" — Tool call audit skipped; return to Phase 2.

**When you see these:** STOP. Return to the phase indicated in parentheses.

## Common Rationalizations

| Excuse | Reality |
|---------|--------|
| "I already know it's correct, no need to check." | Information is just a claim until verified. Agent memory can make mistakes. |
| "I'm skipping to save time, I'll return anyway." | The cost of fixing is usually 10 times the cost of prevention. Do it now. |
| "This was a repetitive check, minor." | Repetitive checks are the biggest indicator of circular reasoning. Question why it is repeating. |
| "Hallucination is a small detail, it doesn't affect the workflow." | Small hallucinations grow into major bugs. They are the weak links in the chain. |
| "Tokens are cheap, what if we spend too many?" | Token cost is not just money; it is context window waste and performance degradation. |
| "The user doesn't want this much detail." | The user wants correct results. Correct results are guaranteed through introspection. |
| "There was no alternative, so I chose this." | There are always at least two alternatives. If you couldn't find them, you didn't think enough. |

## Related Skills

- **debugging-engineer** — Systematic error-finding from the outside; introspector calls this skill to fix detected errors
- **thinking-patterns** — Analyzes the thought patterns used by the agent; useful for determining which thought model was used during introspection
- **bias-detector** — Detects cognitive biases in decisions; used in conjunction with confidence scoring and alternative path analysis
- **context-manager** — Provides optimized strategies for context window management; apply these strategies during context window inspection
- **tester** — Tests outputs produced by the agent; should be called for code/tests corrected after hallucination detection
- **observer** — Observes and reports agent behaviors; used to regularly report introspection findings

## Self-Review

After completing the process of this skill:

1. **Scope Check:** Have you completed each phase (decision trace, tool audit, context inspection, token analysis, hallucination detection, loop detection, confidence scoring, alternative analysis, performance profile, state dump)?
2. **Edge Case Check:** Have you handled unexpected scenarios (failed tool calls, missing context, contradictory claims)?
3. **Quality Check:** Do the outputs meet the standard of the Iron Law — is every claim referable?
4. **Improvement Loop:** Did you note action items from this introspection to apply in the next task?
5. **User Trust:** Is the report clear enough for the user to say "okay, I trust this"?
