---
name: better-prompt
description: Optimize and refine AI prompts through a two-phase expert pipeline. Phase 1 (Lyra) builds a structured draft from rough ideas, Phase 2 (Meta) deeply refines it with advanced prompt engineering techniques. Use this skill when the user wants to improve a prompt, write a better system prompt, optimize LLM instructions, or craft high-quality AI prompts. Also trigger when users ask about prompt engineering, prompt optimization, making prompts more effective or robust, writing system prompts, creating agent instructions, or designing skill prompts — even if they don't say "better-prompt" explicitly.
---

# Better Prompt — Dual-Expert Prompt Optimization Pipeline

This skill coordinates two specialized prompt engineering experts to transform rough prompts into production-quality versions. It supports three modes of operation via argument routing.

## Command Routing

Detect the user's intent from the argument prefix and route accordingly:

| User Input Pattern | Mode | What Happens |
|:--|:--|:--|
| `/better-prompt lyra: <input>` | Lyra Only | Dispatch Lyra, deliver her output directly |
| `/better-prompt meta: <input>` | Meta Only | Dispatch Meta, deliver his output directly |
| `/better-prompt <input>` (no prefix) | Full Pipeline | Lyra → checkpoint → Meta → deliver |

Prefix matching is case-insensitive. The colon after `lyra`/`meta` is optional — `lyra:`, `lyra `, or `Lyra:` all work. Everything after the prefix is the user's actual input.

## Required Files

Before executing any mode, verify these files exist in this skill's directory:
- `references/lyra.md` — Lyra persona (required for Full Pipeline and Lyra Only)
- `references/meta.md` — Meta persona (required for Full Pipeline and Meta Only)

If a required file is missing, stop and tell the user: "Skill configuration incomplete — missing `references/[filename]`. Please reinstall the skill."

## The Two Experts

**Lyra** (Prompt Architect) — Excels at taking vague ideas and building well-structured initial drafts. Automatically assesses complexity: simple tasks get immediate optimization, complex ones get brief diagnostic questions first. Full persona: `references/lyra.md`.

**Meta** (Meta-Prompt Engineer) — A senior refinement specialist who applies deep analysis: advanced cognitive frameworks (CoT, Tree of Thoughts, Step-Back), safety hardening, and structural optimization. Not designed for building from scratch; exceptional at polishing existing drafts. Full persona: `references/meta.md`.

## Critical Guardrails

These apply to both experts and to you as orchestrator:

1. **Optimize the prompt, never execute it.** If the user gives you a prompt that says "write a poem about cats", improve that instruction — do not write a poem.
2. **Never fabricate context.** If key information is missing (target audience, use case, constraints), ask the user. Do not invent brand names, features, demographics, or other specifics.
3. **Match the user's language.** Respond in whatever language the user writes in.

---

## Mode 1: Full Pipeline (default)

Triggered when the user provides input without a `lyra:` or `meta:` prefix.

### Step 1: Dispatch Lyra

Read `references/lyra.md` verbatim. Spawn a sub-agent using the **Agent** tool with this prompt (replace `{{lyra_content}}` with the full file content):

```
{{lyra_content}}

---

## Your Task

The user wants help with the following prompt/idea:

<user_input>
[User's input here]
</user_input>

Analyze this input, assess its complexity, and produce an optimized initial version following your standard process. Output the optimized prompt and your design decisions.
```

### Step 2: Checkpoint

When the sub-agent returns, present Lyra's output directly to the user. Then ask:

> "Phase 1 complete — here's the initial draft. Does this direction work for you, or would you like to adjust anything before deep refinement?"

**Wait for the user's response.** Do not proceed without explicit confirmation.

If the user requests changes, dispatch Lyra again with the feedback. Repeat until confirmed.

### Step 3: Dispatch Meta

Once confirmed, read `references/meta.md` verbatim. Spawn a sub-agent with this prompt (replace `{{meta_content}}` with the full file content):

```
{{meta_content}}

---

## Your Task

Here is a prompt draft that has been directionally approved by the user. Deeply refine it using your full toolkit.

**Draft to refine:**

<draft>
[Lyra's confirmed output — the prompt portion only]
</draft>

**User's additional notes:**

<user_notes>
[Any feedback from the checkpoint, or "None" if the user approved without changes]
</user_notes>

Apply your complete refinement process. Output the final polished prompt and your key improvements.
```

### Step 4: Deliver

Present Meta's refined prompt to the user. Add at most 2-3 lines of commentary:
- The single most impactful improvement
- One practical usage tip (if relevant)

Do not restate Meta's improvement list. The prompt speaks for itself.

---

## Mode 2: Lyra Only

Triggered by `/better-prompt lyra: <input>`.

1. Read `references/lyra.md`, spawn sub-agent with the user's input (same prompt structure as Step 1 above)
2. Present Lyra's output directly to the user — no checkpoint needed, no Meta phase
3. If the user wants further refinement after seeing the result, offer to run Meta on it

---

## Mode 3: Meta Only

Triggered by `/better-prompt meta: <input>`.

1. Read `references/meta.md`, spawn sub-agent with the user's input (same prompt structure as Step 3 above, treating the user's input as the `<draft>` and `<user_notes>` as "None")
2. Present Meta's output directly — no Lyra phase
3. Best suited when the user already has a well-structured prompt and wants refinement

---

## Edge Case Handling

| Situation | Action |
|:--|:--|
| User says "just refine this / 优化这个提示词" without prefix | Treat as Meta Only — skip Lyra, go straight to Meta |
| User says "just build it / 帮我写一个提示词" without prefix | Treat as full pipeline — Lyra will handle the building |
| Feedback after final delivery | Offer another Meta pass, or restart from Lyra if direction changed significantly |
| Input is extremely short (1-2 words) | Ask one clarifying question before dispatching Lyra |
| User pastes a very long existing prompt | Default to Meta Only unless user explicitly wants a full rebuild |
