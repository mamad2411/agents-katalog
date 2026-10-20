---
name: interaction-type-selection-rule-of-thumb
description: Evidence-based rule for selecting the optimal AI coding interaction type (in-code suggestions vs. chat) based on task characteristics. Use when designing AI coding assistant workflows, creating developer guidance for AI tool use, or evaluating interaction type effectiveness. NOT for non-coding AI interactions or when only one interaction type is available.
---

# Interaction Type Selection Rule of Thumb

## Overview
Mixed-methods evidence shows that using a single AI coding interaction type per task (either in-code suggestions OR chat) improves efficiency and reduces workload, while combining both types provides no additional benefits and may increase cognitive overhead. The rule of thumb: use in-code suggestions for coding-heavy, low-context tasks (boilerplate, docs, tests), and use chat for non-coding or context-rich, explanation-heavy tasks (debugging, brainstorming, summaries, information retrieval).

## When to Use
- Designing AI coding assistant interaction workflows
- Creating developer guidance for when to use in-code vs. chat
- Evaluating interaction type effectiveness in AI-assisted development
- Building task-aware AI assistant interfaces
- Reviewing or auditing developer-AI interaction patterns for friction
- NOT for non-coding AI interactions (e.g., writing prose, data analysis outside an IDE)
- NOT when only one interaction type is available in the tool

## Core Process / Workflow

### 1. Classify the Task
Determine task type across these dimensions:
- **Coding vs. non-coding**: Is the task primarily writing, completing, or modifying code?
- **Context requirement**: Does the task need broad codebase context (multi-file, project-level) or only local context around the cursor?
- **Explanation need**: Does the developer need to understand why/how the AI output works, or just accept the result?
- **Complexity**: Is the task simple/small-scale (boilerplate, single function) or complex/broad (debugging across modules, architectural reasoning)?
- **Verification need**: Does the output need explanation to be trusted/verified, or can it be inspected directly in the editor?

### 2. Select Interaction Type Using the Rule of Thumb

**Use In-Code Suggestions when:**
- Task is coding-related (writing, completing, modifying code inline)
- Little codebase context is needed (local code surrounding the cursor is sufficient)
- No explanations beyond inline comments are required
- The developer can verify the output by reading the code directly
- Task types: boilerplate coding, documentation generation, unit test scaffolding, small modifications, standard patterns/idioms

**Use Chat when:**
- Task is non-coding or requires higher-level reasoning
- Broader codebase context is needed (multiple files, project-level understanding)
- Explanations or reasoning are desired to build developer understanding or trust
- The task benefits from iterative Q&A or exploration
- Task types: debugging, brainstorming approaches, summaries, information retrieval, code comprehension, architectural exploration

### 3. Avoid Interaction Type Switching
- Do NOT combine in-code suggestions and chat within a single task
- Switching between modes mid-task introduces cognitive overhead that, per the study, yields durations and perceived workload comparable to not using AI at all
- The combination provides NO additional benefit over single-mode use — the overhead of context-switching negates any gains
- If the initial interaction type turns out to be suboptimal: prefer to complete the task with the chosen mode, OR switch cleanly to the other mode and commit to it — avoid bouncing back and forth

### 4. Monitor Interaction Intensity
- Moderate interaction improves efficiency; excessive interactions introduce overhead that diminishes or reverses benefits
- **In-code suggestions**: efficient up to approximately 13 interactions per task — beyond this, review overhead may dominate
- **Chat**: efficient up to approximately 6 interactions per task — frequent chat prompts add latency and context-management cost
- If approaching these thresholds, reassess: the task may be better suited to the other interaction type, or may need to be decomposed into smaller subtasks

### 5. Watch for Cognitive Load Signals
- During development-heavy tasks with AI assistance, perceived cognitive load can increase (small-to-moderate effect, d=0.34) while perceived productivity does not significantly change — this is normal during active coding with AI
- Cognitive load only stays elevated-and-unrewarded when the AI output is NOT perceived as helpful
- When AI output is perceived as helpful, cognitive load stays flat while productivity significantly increases (large effect, d=0.83)
- **Actionable signal**: if a developer reports high load AND low productivity with AI, the issue is likely output quality/helpfulness, not the interaction mode itself — focus on improving prompts, context provided, or task-IAI fit rather than forcing more AI usage

## Key Findings Behind the Rule
1. **In-code suggestions dominate day-to-day use**: 14 of 20 participants used in-code suggestions >50% of the time; rated higher for satisfaction and productivity than chat
2. **Single mode is best**: Using EITHER in-code OR chat alone improves efficiency and reduces perceived workload vs. no Copilot. COMBINING both during a task yields NO additional benefits and durations/workload comparable to no Copilot
3. **Chat improves accuracy**: Only chat-based interaction significantly increased task completion likelihood vs. no Copilot (relevant for hard-to-complete tasks)
4. **Intensity has a sweet spot**: Moderate use improves efficiency; excessive interactions (especially frequent chat prompts or combined modes) introduce overhead that diminishes or reverses benefits
5. **Helpfulness is the productivity lever**: When AI output is helpful, productivity rises sharply (d=0.83); when not, load rises without a productivity payoff
6. **73% of developers planned to change their interaction patterns** after learning these findings — there is strong latent demand for guidance on interaction type selection

## Limitations & Caveats
- Findings come from a single mixed-methods field study of 22 professional SAP developers using GitHub Copilot over 4 days; generalization beyond that population and tool should be validated
- The study focused on GitHub Copilot specifically; other tools (e.g., Cursor, Continue, Tabnine) may differ in their in-code vs. chat quality and thus shift the optimal split
- The interaction-intensity thresholds (~13 in-code, ~6 chat) are observed medians from one study, not universal constants — treat as heuristics, not hard limits
- The study measured perceived workload (NASA-TLX) and productivity (SPACE), not long-term code quality or defect rates
- Team dynamics findings (developers turn to GenAI faster than colleagues, but rate colleague feedback as more helpful for complex problems) are descriptive, not prescriptive

## References
- See [references/brandebusemeyer-2026-interaction-type-study.md](references/brandebusemeyer-2026-interaction-type-study.md) for full study details, methodology, statistics, and limitations.