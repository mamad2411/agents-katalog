---
name: prompt-triwizard
description: >
  Use when writing, refactoring, or evaluating LLM prompts (system prompts,
  user prompts, few-shot examples, or tool-call schemas) for agent pipeline
  nodes or stages. Triggers on: "write a system prompt for this agent",
  "improve this LLM instruction", "evaluate this prompt", "add few-shot
  examples to this node". Does NOT trigger for general coding, debugging,
  tests, or non-LLM tasks.
---

# Prompt Triwizard

Writes, refines, and evaluates LLM prompts (system prompts, user prompts, few-shot examples, and tool-call schemas) for agent pipeline nodes — producing high-quality, style-correct output every time.

---

## Reuse Within a Session

Once this skill has been loaded, its guidance (structural hierarchy, principles, anti-patterns) stays in the conversation context. When the same prompt needs another modification within the same session (e.g. a re-fix request after testing), continue applying this guidance without re-invoking the skill.

---

## Step 1 — Read the Context, Deliver in Kind (Common Step)

Prompts usually live as string literals inside code files (most often `.py`, but it varies — `.ts`, Jinja templates, etc.). Locate the prompt first; grep for the prompt text if you're unsure which file holds it.

Read only:
- The target prompt file
- Sibling files holding *related prompts* (other nodes of the same pipeline)
- Schemas, Pydantic models, or tool definitions the prompt feeds into

Don't read a file just because it shares the directory. Skip `.md`/`.json`/`.yaml`/config unless it's the schema or tool definition the prompt feeds.

Goal: understand the project's existing depth, tag conventions, and schema bindings — this shapes how specialized the new prompt should be.

Deliver in kind: match the file/format the original prompt lived in (most often `.py`, but it varies — `.ts`, Jinja templates, etc.); if there's no existing file to match (Mode 1), default to `.py` — use `.ts` or Jinja instead only if the project already shows that convention elsewhere. When the prompt takes variables, wrap it as a function call (Python/TS) or a render() call (Jinja) rather than a bare string. Name the system and user pieces — whether a constant or a function — so the literal tokens `system_prompt` and `user_prompt` appear in the name (e.g. `SYSTEM_PROMPT`, `build_system_prompt`, `USER_PROMPT`, `build_user_prompt`).

---

## Step 2 — Receive the Style and Language

Style is the primary axis of this skill — it determines the structural format of the prompt you produce, and everything downstream (Step 3's use-case content, Mode 1/2/3's output) is written in the style chosen here. The output language determines what language the prompt is written in.

### Style

**Priority order:**
1. User explicitly names a style → use it
2. Code read in Step 1 shows a model string (`claude-*`, `gemini-*`, `gpt-*`) → offer it as a suggestion, then confirm
3. Ask: *"Which format should I use? Anthropic / Google / OpenAI. I'll default to Anthropic if you skip."*
4. No response → use **Anthropic** as the default

If sibling prompts already exist in the project, ask: *"Should I also convert the existing prompts to the chosen style?"*

### Language

**Priority order:**
1. User explicitly names a language → use it
2. No explicit language → detect the language the user is writing in, then ask: *"Should I write this in [detected language] or English?"*
3. No response → use the detected language as the default

---

## Step 3 — Identify the Use Case

Use case is a secondary axis, layered on top of the style chosen in Step 2: style controls *how* the prompt is formatted (tags, headers); use case controls *what additional* instructional content the prompt needs (persistence rules, null-case handling, grounding policy, etc.) beyond the style's own baseline. Determine the use case from what the node actually does:

| Use case | Signal |
|----------|--------|
| **Conversational** | Multi-turn dialogue, persona/tone, no fixed completion point |
| **Single-shot transform** | Classification, extraction, summarization — one input, one output, done |
| **Agentic tool-use** | Calls tools in a loop, reasons between calls, has a stop condition |
| **RAG grounding** | Context/documents already injected; answers in one shot from what's provided |
| **Deep research** | Calls search tools iteratively across multiple angles before answering |

**Priority order:**
1. User explicitly names a use case → use it
2. Code read in Step 1 shows the shape (multi-turn loop, single function call, tool-call loop, injected context, iterative search) → infer it, then confirm
3. Ambiguous → ask before proceeding

A node can combine traits from more than one use case (e.g., a conversational agent that also calls tools). When it does, read every applicable `usecases/` reference and merge their instructional content — don't force a single label where the task genuinely spans two.

---

## Step 4 — Identify the Mode

| Mode | Triggered by | Output |
|------|-------------|--------|
| **Mode 1 — Create** | Request for a new prompt | Full system + user prompt from scratch |
| **Mode 2 — Refine** | Request to improve, fix, or rewrite an existing prompt | Before/after diff with diagnosis |
| **Mode 3 — Eval** | Request to test or measure a prompt | Eval report with scores and regression check |

---

## Step 5 — Apply References

Read the references below in the order indicated. They are located in the `references/` directory beside this file, split into `common/` (shared quality backbone), `styles/` (fixed set of 3 format styles — the primary axis, from Step 2), and `usecases/` (what additional instructional content the prompt needs, by agent/task purpose — the secondary axis, from Step 3).

| Reference | Read when |
|-----------|-----------|
| `common/core-principles.md` | **All modes, always** — quality backbone |
| `common/anti-patterns.md` | After drafting — self-check before delivery |
| `common/eval-rubric.md` | Mode 2 (diagnosis) and Mode 3 (eval loop) |
| `styles/anthropic-claude.md` | Style = Anthropic |
| `styles/google-gemini.md` | Style = Google |
| `styles/openai-gpt.md` | Style = OpenAI |
| `usecases/conversational.md` | Use case = Conversational |
| `usecases/single-shot-transform.md` | Use case = Single-shot transform |
| `usecases/agentic-tool-use.md` | Use case = Agentic tool-use |
| `usecases/rag-grounding.md` | Use case = RAG grounding |
| `usecases/deep-research.md` | Use case = Deep research |

Each `usecases/` file includes a per-item placement table showing which style container that content belongs in — read the style reference first, then cross-check the usecase file's placement table against it rather than treating the two as independent lookups.

---

## Mode 1 — Create a New Prompt

1. Clarify requirements: task, inputs, outputs, tool calls (if any), output schema
2. Read `core-principles.md` → choose the right technique (zero-shot, few-shot, CoT, ReAct)
3. Read the chosen style reference (from Step 2) → this is the format the prompt will be written in
4. Read the use-case reference(s) from Step 3 → determine what additional instructional content the prompt needs, and place each piece per its placement table for the chosen style
5. Self-check with `anti-patterns.md`
6. If the prompt feeds a Pydantic model or tool schema: verify field descriptions are in sync

**Deliverable:** Full system prompt + user prompt template, labeled clearly — delivered per the Step 1 rule.

---

## Mode 2 — Refine an Existing Prompt

Refine covers two distinct jobs. They share the same diagnosis, then split:

- **Path A — In-place** — the prompt is already in the target style; improve its content without restyling.
- **Path B — Re-style** — the prompt is in a different style (or styleless), and you carry it into the target style.

A re-style is **never a marker swap.** Each style encodes a different philosophy — Anthropic's motivation-over-negation and positive framing, Google's `RULE N` routing with `[REQ]/[OPT]` severity, OpenAI's outcome-oriented output contracts. Carrying a prompt across styles means re-expressing its intent in the target philosophy, which changes wording and structure by design. And the original may be rough: when it is, improve the content while you restyle — the two jobs merge.

### Common diagnosis (both paths)

1. Read the existing prompt in full → detect its current style. Check exclusive, structural markers, not just "has XML tags" (multiple styles use backtick-wrapped XML tags):
   - `**FOLLOW-UP RULES**` / `*RULE N: NAME*` bold+italic pattern anywhere → Google
   - A single XML tag wraps the entire system prompt, closing right before the user turn (which is itself then wrapped in a task-specific tag) → Google
   - Bare `#` (H1) headers structure the top level, with no enclosing wrapper; any XML tags present are supplementary and plain, never backtick-wrapped → OpenAI
   - Many independently-named XML tags scattered as top-level siblings, with any Markdown headers nested inside a specific tag's content (never floating between tags) → Anthropic
2. Read `eval-rubric.md` → score on 4 axes: Clarity / Specificity / Actionability / Scope
3. Read `core-principles.md` → identify which principles are violated
4. Read the chosen style reference (from Step 2) in full
5. Read the use-case reference(s) from Step 3 → check whether required instructional content (persistence, null-case handling, grounding policy, etc.) is present and correctly placed for the chosen style

### Choose the path

- Current style **==** target style → **Path A**
- Current style **!=** target style (or styleless) → **Path B**
- If it's unclear whether the user wants a restyle or only a content fix in the existing style, ask before proceeding.

### Path A — In-place refine

Present diagnosis and changes using the before/after format:

```
❌ Original:
[exact original text]

🤔 Diagnosis:
[which axis fails, and why]

✅ Improved:
[exact replacement text]
```

**Rule:** One change per block. Multiple changes in separate blocks.

### Path B — Re-style refine

The prompt is rewritten whole, so block-level diffs don't apply. Instead:

1. Re-express the prompt in the target style's **philosophy**, not just its markers (reasoning induction, priority markers, data placement, rule structure all convert).
2. Preserve the original's core intent and hard constraints — verify nothing load-bearing was dropped in translation.
3. If the original is underspecified or low-quality, improve the content as you convert (apply `core-principles.md`).
4. If the original's intent is ambiguous, do not guess — confirm with the user first.
5. Present as a single whole before/after, plus a short conversion note explaining which philosophy shifts you applied:

```
❌ Original ([source style]):
[full original prompt]

🤔 Diagnosis + conversion notes:
[axis scores, principles violated, and how the target philosophy was applied]

✅ Rewritten ([target style]):
[full rewritten prompt]
```

### Self-check (both paths)

6. Self-check with `anti-patterns.md`

---

## Mode 3 — Eval Loop

1. Define the baseline:
   - New prompt → baseline = no system prompt (raw model)
   - Refined prompt → baseline = the version before the change
2. Design the input set: minimum 3 scenarios — typical / edge / adversarial
3. Score each scenario on the 4-axis rubric from `eval-rubric.md`
4. Check for regressions: re-run all previously-passing scenarios
5. Report: trigger-fit accuracy + output quality scores + regression status

**Fresh session rule:** always evaluate in a session that has not seen the prompt in conversation history.

---

## Self-Check Before Delivery

After drafting, always run through `anti-patterns.md`. Key questions:

- Is every rule verifiable (binary or measurable)?
- Is any rule here to prevent a failure mode I've never observed?
- Are volatile values at the end of the system prompt or in the user turn?
- Do few-shot examples cover edge cases, not just the happy path?
- Am I using the correct structural markers for the chosen style — not just "has XML tags" (all three styles can contain XML tags; the real signals are a single system-prompt-wide wrapper + RULE N for Google, bare H1 headers with no wrapper and only supplementary plain XML for OpenAI, and many independent sibling tags with headers nested inside them for Anthropic)?
- Does the prompt contain the instructional content its use case requires (e.g. a stop condition for agentic/deep-research, a null-case rule for single-shot transform, an insufficient-context rule for RAG grounding), each placed in the container its style's placement table specifies?
- Are tool/schema descriptions synchronized with the prompt?
- If writing to a file, does the format match the project's existing convention — wrapped as a function/render call when parameterized?
- Do the system and user constants/functions literally contain `system_prompt` / `user_prompt`?
