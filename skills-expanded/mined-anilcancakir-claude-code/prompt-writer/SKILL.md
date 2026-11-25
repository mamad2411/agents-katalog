---
name: prompt-writer
description: "Write or audit a prompt another Claude will run: system prompts, subagent briefs, skill, command and agent bodies, CLAUDE.md and rules. Also prompts for Gemini models."
when_to_use: "Use when authoring instruction text a model will follow, even if nobody says prompt, and before writing the prompt for the generate_image tool."
disable-model-invocation: false
---

# Prompt Writer

You are about to write or edit a prompt another Claude will execute. The Claude models covered are Opus 5.5, Sonnet 5.5 and Haiku 5.5 (the `opus`, `sonnet` and `haiku` aliases on the Anthropic API). Pick the reference below, read the card of the target model, fill in the template, validate against the checklist.

## References

| File | Load when... |
|---|---|
| `${CLAUDE_SKILL_DIR}/references/claude-models.md` | Any Claude prompt, first: the model matrix, rules all three 5.5 models share (effort, thinking, sampling, prefill, append-only history), what Claude Code adds, a porting table, the checklist. |
| `${CLAUDE_SKILL_DIR}/references/opus-5-5-tuning.md` | Target `claude-opus-5-5`: effort from `medium`, the unattended four-stop paragraph, progress updates, time signals, pasted-content tags, and the length, scope and subagent rules carried from Opus 5. |
| `${CLAUDE_SKILL_DIR}/references/sonnet-5-5-tuning.md` | Target `claude-sonnet-5-5`: check-ins at `low` and `medium`, unrequested additions, self-started review at `xhigh`, `between_tools`, JSON answers, search, tolerant tool calls. |
| `${CLAUDE_SKILL_DIR}/references/haiku-5-5-tuning.md` | Target `claude-haiku-5-5`: early stopping in long agent prompts, the verify paragraph, search with the date, JSON with your own tools, chatbot rules. |
| `${CLAUDE_SKILL_DIR}/references/claude-code-builtin-prompts.md` | Anything that runs inside Claude Code: verbatim built-in prompt text per shape and model, CLAUDE.md wrapper, subagent defaults, Agent tool text, patterns worth copying. |
| `${CLAUDE_SKILL_DIR}/references/claude-code-conventions.md` | Prompts for the Claude Code harness: agents, slash commands, hooks, harness rules. |
| `${CLAUDE_SKILL_DIR}/references/subagent-prompts.md` | Briefing a fresh subagent, designing a `subagent_type`, lookup vs investigation, length caps. |
| `${CLAUDE_SKILL_DIR}/references/architecture.md` | Message structure, XML tag names, long-context layout, example design. |
| `${CLAUDE_SKILL_DIR}/references/snippets.md` | A copy-paste building block (verbosity, parallel tools, hallucination control, output format, scope). |
| `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` | Auditing or debugging a prompt that produces wrong output. |
| `${CLAUDE_SKILL_DIR}/references/worked-examples.md` | A complete prompt as a starting template (extraction, code review, custom agent, long-document RAG, slash command, meta-prompt). |
| `${CLAUDE_SKILL_DIR}/references/gemini-tuning.md` | A Gemini model or `generate_image`: delimiters, placement, thinking and sampling deltas, how Gemini CLI and Antigravity prompts are built, image prompt rules. |
| `${CLAUDE_SKILL_DIR}/references/gemini-model-cards.md` | A specific Gemini model: the per-model matrix and cards for 3.8 Flash, Hydrogen, Carbon, Argon, older Flash and 3.1 Pro, plus a porting table. |
| `${CLAUDE_SKILL_DIR}/references/gemini-4-neon-tuning.md` | `gemini-4-neon`, any Gemini 4 model, or Antigravity rules, skills and Orchestrator: thinking levels, pre-tool text, turn state, reported failure modes. |

Source material is Anthropic's documentation; append `.md` to a URL for raw markdown. API and model docs: `https://platform.claude.com/docs/en/<path>.md`; Claude Code docs: `https://code.claude.com/docs/en/<path>.md` (the former `docs.claude.com` host redirects to the first and does not serve the Claude Code pages). When the docs conflict with observed CLI behavior, trust the live binary.

## Ground before you write

Do not author a prompt from built-in knowledge alone: it is frozen at the training cutoff and the world the prompt runs in is not. Two grounding passes come before the first line, every time.

- **Read the actual target.** When the prompt names an existing file, agent, skill, command, or symbol, open it first with Read, Grep, Glob, or `ac:explore`. Editing an existing prompt means reading its current body and the references it points at, not recalling what it likely says.
- **Verify against fresh sources.** Model behavior, effort and thinking parameter shapes, API surfaces, SDK signatures, and library or framework features shift between versions. Confirm anything version-sensitive against current docs through `ac:librarian` or the `ac` MCP web tools (`web-search`, `web-fetch`, `search-docs`) before you state it as fact, and cite what you found.

When your built-in knowledge disagrees with the file or a fresh source, the file and the source win.

## Decision flow

Route by what you are about to produce. Each branch points at a reference for the depth.

```
Writing a prompt for a Gemini model, or the prompt for the generate_image tool?
├── YES → read `${CLAUDE_SKILL_DIR}/references/gemini-tuning.md` and read nothing
│         else in this body: the text skeleton, the image rules, worked image prompts
│         and the checklist live in that file, and the rest of this body targets Claude.
│         For a text or agent prompt, also read the target model's card in
│         `${CLAUDE_SKILL_DIR}/references/gemini-model-cards.md` (3.8 Flash, Hydrogen,
│         Carbon, Argon, older Flash, 3.1 Pro); for Neon, any Gemini 4 model and for
│         Antigravity work, also `${CLAUDE_SKILL_DIR}/references/gemini-4-neon-tuning.md`.
│         Both win where they differ from the generic file.
└── NO  → continue
        ↓
Writing a SKILL.md body or a slash workflow (/name [args])?
├── YES → use this skill for the prompt body, route the skill SHAPE
│         (frontmatter, scope, invocation, bundling, and for a typed workflow
│         arguments and shell injection) through `ac:skill-creator`.
└── NO  → continue
        ↓
Writing a custom subagent definition (.claude/agents/<name>.md)?
├── YES → use this skill for the system-prompt body, route the agent SHAPE
│         (tools, model, permissions, isolation) through `ac:agent-creator`.
│         Then read `${CLAUDE_SKILL_DIR}/references/subagent-prompts.md`.
└── NO  → continue
        ↓
Writing CLAUDE.md, CLAUDE.local.md, or .claude/rules/*.md?
├── YES → use this skill for content tone and structure, route the file SHAPE
│         (scope, paths:, @imports, loading order) through `ac:claude-md-rules-creator`.
└── NO  → continue
        ↓
Briefing a fresh Agent tool call (no custom subagent_type)?
├── YES → `${CLAUDE_SKILL_DIR}/references/subagent-prompts.md`
└── NO  → continue
        ↓
Auditing or improving an existing prompt?
├── YES → `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` FIRST,
│         then `${CLAUDE_SKILL_DIR}/references/architecture.md`.
└── NO  → use the Quick template below; validate against the checklist.
```

Every Claude branch also reads `claude-models.md` and the card of the model that will run the prompt.

## Core principles

The ten rules that change outcomes the most.

1. **Static in system, dynamic in user.** Persona, schema, examples, invariants go in the system prompt so prompt caching amortizes them; per-request data (the document, the question, the file under review) goes in user messages.
2. **Wrap every distinct block in XML tags.** Tag boundaries are the reliable way to separate instructions from data. Use descriptive, consistent names: `<role>`, `<context>`, `<examples>`, `<input>`, `<output_format>`. In a Claude Code body, markdown headings may mark the instruction sections instead; data still goes in tags.
3. **Tell the model what to do; to move it off a default, name the exact behavior.** "Provide concise responses" beats "do not be verbose." A named list works: Anthropic says Opus 5.5 responds to instructions that name the specific early stop to avoid ("a summary that announces the next step instead of taking it"); treat the same move for Sonnet and Haiku as this skill's extension.
4. **State scope explicitly, in both directions.** Where a rule must span, say so: "apply to every X, not just the first." Where the task must not widen, say that too: Sonnet 5.5 adds unrequested tests and docs, and Opus 5's page reports scope widening that the 5.5 page does not retract (Carried), so name the boundary ("change only these files; report adjacent problems instead of fixing them").
5. **Examples are the highest-leverage tool for gray areas.** 3 to 5 diverse, labeled examples beat any abstract instruction. Wrap each in `<example>` inside `<examples>`. Cover edge cases.
6. **Repeat the top constraint right before generation.** Recency wins. End the prompt with the one or two rules the model must not break.
7. **No "CRITICAL: you MUST" language.** Modern Claude overtriggers on aggressive wording. Plain instructions work; if a rule needs weight, explain the why.
8. **Structured Outputs over prefill.** Prefilling the last assistant message returns 400 on Claude 4.6 and later. Use Structured Outputs, tool calls with enums, or XML tags around the output shape in the user turn.
9. **Set scope before length.** A short prompt with the right scope outperforms a long one with hedges; the model fills hedged gaps with priors.
10. **The colleague test.** Show the prompt to someone with no context. If they would be confused, the model will be too.

## Standard architecture

Place components in this order. Skipping any is a choice, not a default.

| # | Component | Location | Why this position |
|---|---|---|---|
| 1 | Persona, role, tone | system | Frames the lens; without it the model defaults to baseline. |
| 2 | Static rules, schemas, invariants | system | Cacheable. |
| 3 | Few-shot examples (3 to 5) | system | Format visible before dynamic input. |
| 4 | Dynamic content (documents, retrieved data, images) | user | Per-request; uncacheable. |
| 5 | Step-by-step instructions | user | Order for processing the dynamic content. |
| 6 | End-of-prompt reminders | user (last lines) | Top 1 to 3 constraints, for recency. |
| 7 | Output format lock | user (last) or Structured Outputs | Final shape of the response. |

For inputs above 20k tokens the order inside the user turn flips: long documents at the very top, instructions and the actual question at the bottom. Full detail in `architecture.md`.

## Quick template

Strip components you do not need with intent.

```xml
<!-- SYSTEM PROMPT -->
<role>
You are [persona, one sentence: who, domain, tone].
</role>

<context>
[Static facts the model cannot derive: schemas, business rules, shape of the input. Cacheable.]
</context>

<examples>
  <example>
    <input>[representative input]</input>
    <expected_output>[exactly what the model should produce]</expected_output>
  </example>
  <!-- 2 to 4 more, diverse, covering edge cases -->
</examples>

<output_format>
[Shape: XML tags, JSON schema reference, plain prose, etc.]
</output_format>

<!-- USER MESSAGE -->
<input>
[The actual per-request data]
</input>

<instructions>
1. First, [process the structured part of the input].
2. Then, [interpret the ambiguous part using the structured baseline].
3. Finally, [produce the output in the shape specified above].
</instructions>

<reminders>
- [Top constraint, e.g., "cite the specific input region for every claim"]
- [Scope constraint, e.g., "apply to every section, not just the first"]
</reminders>
```

## The three models at a glance

Detail, sources and the porting table are in `claude-models.md`; each card carries the model's own paragraphs.

| Knob | Opus 5.5 | Sonnet 5.5 | Haiku 5.5 |
|---|---|---|---|
| Default effort | `medium` | `high` on the API, `medium` in Claude Code | `medium` |
| Thinking | always on; `disabled`, manual and `between_tools` 400 | adaptive; `between_tools` at `high` or below; `disabled` and manual 400 | adaptive; `disabled` at `high` or below; manual and `between_tools` 400 |
| `tool_choice` `any` or `tool` | 400 | 400 | accepted, no text before the call |
| Watch for | unattended loops that end on a progress report | check-ins at `low` and `medium`, unrequested additions | early stops in long agent prompts at `low` |

**Effort is the depth and cost lever; labels do not port.** Set it explicitly and test levels on your own evals. Lower effort before writing "think less" prose, and drop "think carefully" lines. **Keep the prefix append-only:** editing `system` or `tools` mid-session invalidates earlier thinking blocks, so a late rule goes in a mid-conversation system message. **No reasoning in the reply:** "explain your reasoning, then answer" can draw a `reasoning_extraction` refusal; read `display: "summarized"` thinking instead.

## When the prompt runs inside Claude Code

What the host already says depends on the model's prompt shape; restate only what that shape lacks.

- **All three 5.5 models get the LEAN shape.** It already carries markdown rendering, permission denials as signal, hook output as user feedback, mid-conversation system turns as harness, `<pasted_content>` handling, dedicated tools over shell, parallel independent calls, `file_path:line_number`, confirming hard-to-reverse actions, faithful outcome reports, acting without re-deriving settled facts. Do not restate these.
- **LEAN does not carry** the CLASSIC-only rules: the software-engineering frame, matching the surrounding code's style (sent by 2.1.314, absent from the 2.1.318 captures), no comments unless the why is non-obvious, no speculative abstraction, no compatibility shims, no handling for impossible cases, prefer editing a file, never guess a URL, flag injection (`claude-code-conventions.md` lists them). A body that needs one states it in one line.
- **Custom subagents get neither shape.** Their system prompt is the agent body plus environment notes, so every rule the agent follows lives in the body.
- **Delegation.** The Agent tool description is cautionary ("When in doubt, don't spawn"); a prompt that holds the Agent tool still says when not to spawn.
- **Match the host's register.** `claude-code-builtin-prompts.md` holds Claude Code's own prompt text verbatim, with a Patterns section: `#` headings over short plain sentences, the reason in the same sentence as the rule, named behaviors, no caps. Section markers can be headings or XML tags (follow the target's family); data always sits inside XML tags.

## Sibling skills (route the surrounding shape)

This skill owns the prompt text; the shape around it routes through a sibling skill, and both stay loaded:

- A SKILL.md body or a slash workflow body (`/name [args]`): `ac:skill-creator`.
- A subagent definition (`.claude/agents/<name>.md`): `ac:agent-creator`.
- `CLAUDE.md`, `CLAUDE.local.md` or `.claude/rules/<topic>.md`: `ac:claude-md-rules-creator`.
- `PROJECT.md`, `ARCHITECTURE.md` or `DESIGN.md`: `ac:project-md-writer`, `ac:architecture-md-writer`, `ac:design-md-writer`.
- A direct Agent tool call (no custom subagent type): no sibling; this skill covers the `prompt` field.

When the request implies one of these, invoke the matching creator for shape and keep this skill for the prompt body.

## Common shapes

**Subagent briefing** (Agent tool call). Brief like a smart colleague who just walked in: goal, what you already learned, surrounding context, length cap, response shape. A worked briefing and the full detail: `subagent-prompts.md`.

**Custom subagent definition** (`.claude/agents/<name>.md`): bounded description, explicit tools, decisional steps, a locked output contract, and every rule the agent needs restated in its body. For a reviewer or advisor, ask for coverage-first findings that each carry their evidence or say "unverified". Full template in `worked-examples.md` Example 3.

Copy-paste fragments (hallucination control, verification, verbosity, action defaults, output lock, code review) live in `snippets.md`. Inside Claude Code the lean prompt already carries parallel tool use and context compaction, so add those only to API prompts or subagent bodies.

## Anti-patterns

The full audit checklist with the why behind each fix is in `anti-patterns.md`.

| Anti-pattern | Fix |
|---|---|
| Negative-only instructions ("do not be verbose") | Positive scope: "Provide concise, focused responses." Naming the exact default to avoid is different and works (principle 3). |
| Aggressive "CRITICAL / MUST / ALWAYS" wording | Plain instructions; explain the why if a rule needs weight. |
| Prefilled last assistant message | Use Structured Outputs or wrap output in XML tags. |
| Unstated scope, or no upper bound | "Apply to every X, not just the first", and name the boundary. |
| Vague verbs: "format properly", "handle errors" | State the format and the error contract exactly. |
| Hidden context (prompt relies on chat history) | Restate load-bearing facts inside the prompt itself. |
| Static and dynamic mixed in user message | Move static to system; dynamic stays in user. |
| Long documents at the bottom of the user turn | Move documents to the top for inputs over 20k tokens. |
| "Based on your findings, fix the bug" (in subagent prompts) | Specify file paths, line numbers, exact change; do not delegate synthesis. |
| "Think less" or "answer directly" used as a depth control | Lower `effort`; the docs say prose does not reliably reduce thinking. |
| Effort labels copied across models; reasoning-in-reply scaffolds | Re-sweep effort; remove the lines. |
| `thinking` `enabled` + `budget_tokens`, `disabled` or forced `tool_choice` on a model that returns 400 | Omit `thinking` or send `adaptive`; use `auto` plus a prompt line, or Structured Outputs. |
| Editing `system` or `tools` mid-session | Append a mid-conversation system message instead. |
| A body that assumes Claude Code's classic code-style rules | State the rule in one line; the lean prompt does not carry it. |
| Top-level `output_format`, the `effort-2025-11-24` beta header, `client.beta.messages.create` | Use `output_config.format`; drop the header; use `client.messages.create`. |

## Pre-flight checklist

Before shipping a prompt:

- [ ] Persona, domain, tone stated in the system prompt.
- [ ] Static content (schema, examples, invariants) in system; dynamic in user.
- [ ] Every data block in named XML tags; instruction sections marked consistently (tags or headings).
- [ ] 3 to 5 diverse examples covering edge cases.
- [ ] Instructions ordered: process structured input first, ambiguous second; input above 20k tokens: documents at top, question at bottom.
- [ ] End-of-prompt reminders restate the top 1 to 3 constraints; no "CRITICAL / MUST / ALWAYS" language.
- [ ] Scope stated in both directions: the span ("every X, not just the first") and the boundary.
- [ ] The target model's `claude-models.md` checklist passes: effort chosen by measurement, thinking shape valid, no sampling parameters, no prefill, no forced `tool_choice` on Opus or Sonnet, `max_tokens` sized for thinking.
- [ ] Main-thread text (skill, command, CLAUDE.md) restates what the reader's shape lacks and nothing it carries. An agent body restates every rule it needs, except what the subagent Notes already give it (`claude-code-builtin-prompts.md`, section 5).
- [ ] Every fenced command in the body has been run, in the shell it will actually run in, and its output matches what the surrounding prose claims (`claude-code-conventions.md`).
- [ ] Length controlled by an explicit target, not by lowering effort.
- [ ] Output shape lock uses `output_config.format`, a tool call with an enum, or an XML wrap.
- [ ] Colleague test passes.
