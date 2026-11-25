---
name: codex-deep-research
description: Run web-first deep research in the current Codex session for comparisons, evaluations, market scans, recommendations, and other citation-heavy questions that need current information. Escalate to multi-agent work only when task complexity justifies it.
metadata:
  short-description: Codex-native deep research workflow
---

# Codex Deep Research

Use this skill when the user is asking for research rather than a normal answer. Typical triggers include:

- comparisons, evaluations, and recommendations
- market scans, competitive analysis, and landscape research
- questions where current information materially affects the answer
- requests that need citations, trade-offs, risks, or explicit source quality

Do not force the full workflow onto simple factual questions. First decide whether the task truly needs deep research.

## Quick start

1. Rewrite the request into a compact internal research brief.
2. Browse early and prefer current, verifiable sources.
3. Stay single-agent unless there is a real quality benefit to parallel work.
4. If complexity is high, delegate distinct sub-questions to a small number of sub-agents using the sub-agent template.
5. Deliver a complete research report in the current conversation unless the user explicitly asks for a shorter format.
6. Only save files when the user asks or the result is clearly worth preserving after the in-session report is complete.

## Workflow

### 1. Detect research mode

Enter deep-research mode when one or more of these are true:

- the answer depends on up-to-date information
- the user is making a decision with meaningful downside risk
- the task needs multiple sources or source comparison
- the user wants a recommendation, ranking, comparison, or market view
- the expected output should include citations, trade-offs, or explicit uncertainty

If the request is too vague to research responsibly, ask one minimal clarifying question instead of starting a large search.

### 2. Build an internal brief

Use [assets/brief-template.md](assets/brief-template.md) as the default structure. Keep the brief internal unless sharing it would help the user.

Capture at least:

- the exact research question
- the user's likely decision or goal
- what is in scope and out of scope
- time sensitivity
- the evaluation dimensions that matter most
- the expected deliverable style

### 3. Browse by default

For research tasks, browse first instead of relying on memory. Prefer official and primary sources, then high-quality reporting. Use [references/source-quality.md](references/source-quality.md) and [references/citation-rules.md](references/citation-rules.md) when judging evidence.

For time-sensitive topics, use absolute dates in the final answer.

### 4. Decide whether to use multi-agent work

Start single-agent by default. Upgrade to multi-agent only when it clearly improves coverage or speed.

Only escalate when one or more of these are true:

- the task contains distinct sub-questions that can be researched independently
- the source space is broad enough that parallel coverage will materially improve quality
- the report would benefit from role separation such as official-source review, market scan, and risk review
- the user is making a decision where missing counter-evidence would be costly

Avoid escalation when the task is small, narrow, or already well-covered by a single search path.

When delegating, default to [assets/subagent-task-template.md](assets/subagent-task-template.md). Unless the task is extremely simple, give each sub-agent:

- one narrow question
- an explicit scope and out-of-scope boundary
- a source-priority instruction
- a concise return format

The main agent owns final judgment and synthesis.

### 5. Synthesize carefully

Never concatenate search results or sub-agent outputs. Merge them into one coherent report. Always:

- deduplicate overlapping evidence
- surface source conflicts
- explain uncertainty where evidence is thin
- keep facts separate from inferences
- keep recommendations tied to the user's goals

For the full staged process, see [references/workflow.md](references/workflow.md).

## Output contract

Default to a real research report in the conversation, not a short generic answer and not a summary that points the real content to a file. Use [assets/report-template.md](assets/report-template.md) unless the user explicitly asks for a different format.

The final answer should usually include:

- conclusion summary
- research question and scope
- method and source strategy
- key findings
- evidence and citations
- risks and unknowns
- recommendation
- next steps

Keep these categories explicit:

- facts: directly supported by sources
- inferences: reasoned conclusions drawn from those facts
- recommendations: suggested actions based on the user's goals

If the user explicitly asks for a short report, compress the answer but keep citations and evidence boundaries intact.

Do not treat a saved file as the primary deliverable unless the user explicitly asked for file output.

## Persistence

Do not save files by default. Complete the in-session research delivery first. Persist only when:

- the user asks to save the output
- the result is clearly reusable
- the task benefits from an auditable artifact trail

Do not save files merely because auditability could be helpful. When saving is appropriate, follow repository conventions instead of inventing new ones.

## Completion check

Before finalizing, quickly verify:

- the conversation already contains the full research deliverable, not just a summary
- facts, inferences, and recommendations are kept distinct
- multi-agent work was used only if it materially improved coverage
- no files were written by default

## Reference map

- [references/workflow.md](references/workflow.md): staged research flow, escalation, synthesis
- [references/source-quality.md](references/source-quality.md): source hierarchy and evidence handling
- [references/citation-rules.md](references/citation-rules.md): citation visibility and date rules
- [assets/brief-template.md](assets/brief-template.md): internal research brief scaffold
- [assets/report-template.md](assets/report-template.md): default report scaffold
- [assets/subagent-task-template.md](assets/subagent-task-template.md): delegation scaffold
