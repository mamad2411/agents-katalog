---
name: prompt
description: >
  Format an informal request into a structured prompt, then execute it.
  Add "only:" prefix or say "hold"/"don't run" to output without executing.
  Add "refine:" prefix to audit and improve an existing prompt instead.
  Use when the user types /prompt or asks to turn a rough request into a
  structured prompt.
---

# /prompt — Format, Execute, or Refine

## Reference Files
Before formatting, read `${CLAUDE_SKILL_DIR}/references/formatting-core.md` —
it holds the shared formatting elements, depth calibration, and tool routing
rules used by all three modes below.

## Input
$ARGUMENTS

---

## Mode Detection

Detect mode from the input before doing anything else:

| Signal | Mode |
|--------|------|
| Input starts with `refine:` | **Refine** — audit an existing prompt |
| Input contains `only:`, `hold`, `don't run`, `just format` | **Format-only** — output, no execute |
| Otherwise | **Execute** — format then run |

Strip the mode prefix (`only:`, `refine:`) from the input before processing.

---

## Execute Mode (default)

The user has given an informal, conversational request. Format it and run it.

1. **Parse the intent**: Extract the core task, audience, and desired output.

2. **Calibrate depth** (see formatting-core.md):
   - **Light** (default): format only, no depth injection
   - **Standard**: format + assumptions/rationale block
   - **Deep**: format + research/compare/verify block
   - User can override with `depth:light`, `depth:standard`, `depth:deep`

3. **Format** using the elements in formatting-core.md. Match complexity to task — don't over-engineer simple requests.

4. **Inject depth directives** if Standard or Deep. Skip for Light.

5. **Show the formatted prompt** in a fenced code block.

6. **Tool-routing check**: If another tool serves better (see formatting-core.md), add a brief note before executing. Don't block — just flag.

7. **Execute the prompt immediately** — respond as if the user typed it directly.

8. Ask ONE clarifying question only if ambiguity would lead to a significantly different output.

---

## Format-only Mode

Same as Execute, but stop after showing the formatted prompt. Do not run it.

After the code block:
- Add `**Best run in:** [tool] — [reason]` if another tool fits better (omit if Claude Code is best)
- If the prompt looks **reusable** (template, workflow, recurring task):
  - Add a version header: `## Prompt v1.0 — [short name]`
  - Suggest 3–5 eval test cases: brief input → expected-output pairs
- If the prompt has **agent/workflow context** (system vs. user turn):
  - Separate into **System Prompt** and **User Prompt** sections within the code block

---

## Refine Mode

The user has given an existing prompt to audit and improve.

1. **Substance checklist** (new issues matter most):
   - [ ] Depth calibration — does it tell the model how deeply to engage?
   - [ ] Self-verification — check step present (assumptions, uncertainty)?
   - [ ] Best-practice grounding — research standards instructed where appropriate?
   - [ ] Specificity of "good" — strong output defined?
   - [ ] Metacognitive scaffolding — rationale, assumptions, confidence requested?

2. **Structure checklist**:
   - [ ] Task clarity — unambiguous core ask?
   - [ ] Context — enough for a cold reader?
   - [ ] Constraints — length, tone, format, exclusions?
   - [ ] Output format — structure defined?
   - [ ] Role/persona — included if it improves output?
   - [ ] Examples — provided if they reduce ambiguity?
   - [ ] Bookend pattern — key instruction restated at end (if long)?
   - [ ] System/user separation — clear if used in agent/API context?
   - [ ] Versioning — version header if reusable?

3. **Identify the primary finding.** Lead with the single most impactful improvement.

4. **Fix anti-patterns**:
   - Format-only prompts for substantive tasks → add depth directives
   - Vague thoroughness language ("be meticulous") → specific action verbs
   - Over-prompting ("CRITICAL", "YOU MUST") → calm, direct directives
   - Excessive caveats → make direct
   - Vague format instructions → specify structure
   - Missing constraints → add length/scope limits
   - Buried lede → move core task to top

5. **Show what changed and why** — bullet list with brief rationale. Lead with primary finding.

6. **Present the refined prompt** in a fenced code block.

7. **Tool-routing check**: note in changes list if another tool would serve better.

8. **For reusable prompts**: add/increment version header and suggest 3–5 eval test cases.

Do NOT execute the refined prompt. Do NOT rewrite from scratch if the original is mostly good.
Preserve the user's intent and voice. If the prompt is already strong, say so.

---

## Important (all modes)
- Default depth is Light — most requests pass through with formatting only.
- Match formatting complexity to task complexity.
- Use Claude Code tools (MCP, file access, search) when executing if the task requires them.
