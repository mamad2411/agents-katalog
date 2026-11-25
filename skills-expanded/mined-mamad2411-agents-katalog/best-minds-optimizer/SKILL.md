---
name: best-minds-optimizer
description: Prompt optimizer that rewrites the user's input through the lens of the world's top domain expert before executing. Activates when the user asks a substantive question, wants strategic advice, needs a deeper take, requests expert-level analysis, or is working through a complex decision. Triggers on phrases like "best minds", "optimize this prompt", "what would [expert] say", "give me a world-class take", or any non-trivial question where expert framing would produce a sharper result. Does NOT trigger on mechanical tasks like file edits, git commands, or simple code operations. When in doubt about whether to trigger, trigger — the skill will self-skip if the input is trivial.
---

# Best Minds — Prompt Optimizer

A pre-processing layer that optimizes prompts before execution. For any substantive question or task, it identifies the world's best domain expert and rewrites the user's prompt through that expert's frameworks — producing sharper, more precise prompts that get better results from the LLM.

The core insight: LLMs are simulators. A prompt framed through Charlie Munger's mental models produces a fundamentally different response than a vague question. This skill applies that insight automatically.

## Pipeline

### Step 1: Triage — Skip, Polish, Clarify, or Optimize

Before doing anything, classify the user's prompt into one of four lanes:

**Optimize** — The prompt is substantive and clear enough that expert framing will sharpen it:
- The question has a definite problem structure even if the user phrased it loosely
- Clarification would just delay an obviously useful rewrite
- The user explicitly says "just give me your take"
- Read `references/optimize.md` for the full pipeline (Logic Mapping → Expert Selection → Prompt Rewrite → Output → Answer Format).

**Polish** — The prompt is multi-sentence or contains user-authored text that would benefit from a quick wording pass:
- Any prompt where the user composed multiple sentences, specified requirements, or provided context — regardless of whether the task is mechanical, creative, or analytical
- The user explicitly asks to "polish", "clean up", "improve wording", or similar
- **Rule of thumb: if the user wrote more than one short sentence, it's worth a polish.** The user invested effort in composing the prompt — a quick wording pass respects that effort.
- Read `references/polish.md` for detailed instructions. Do NOT run the full optimization pipeline.

**Clarify** — The prompt is substantive but could go in meaningfully different directions:
- The user's situation, constraints, or goals are unclear
- The answer would change significantly depending on unstated context
- Read `references/clarify.md` for detailed instructions. After gathering context, proceed to Optimize.

**Skip** — The prompt is a short, simple instruction where polishing adds no value:
- Single-sentence commands with no user-authored detail ("read this file", "commit this", "rename X to Y")
- Follow-up messages in an ongoing conversation where the prompt is already refined (see Follow-up Handling below)
- **Only skip if the prompt is roughly one short sentence with no requirements, constraints, or context.** If the user wrote more than one sentence, route to **Polish** instead.
- Emit `status: "skipped"` (or skip JSON entirely) and proceed with the original prompt unchanged.

### Step 2: Confirmation — Review Gate

After triage completes and the optimization pipeline runs (Steps 1.5–3), you **must** pause and present the Review Gate before executing. This is mandatory — never skip it.

**Review Gate display format:**

```
### Review Gate

**Expert Persona**: [Name] — [one-line rationale]
**Reasoning Framework**: [Logic Structure type] — [framework applied, e.g., First Principles / Inversion]
**Key Metrics**: [2–3 North Star metrics]

**Rewritten Prompt**:
> [The full optimized prompt from Step 3]

---
⏳ **Awaiting your authorization.** Reply with:
- **"go"** or **"yes"** — execute as shown
- **"adjust [feedback]"** — re-optimize with your feedback (e.g., "adjust — use a different expert" or "adjust — focus more on pricing")
- **"skip"** — abandon optimization and answer the original prompt directly
```

**Rules:**
- **Never execute the optimized prompt until the user explicitly authorizes.** Silence is not consent — wait for a response.
- If the user says **"go"** / **"yes"** / **"proceed"** (or any clear affirmative), execute the optimized prompt per Steps 4–5 in `references/optimize.md`.
- If the user provides **adjustment feedback**, return to Step 2 (Expert Selection) or Step 3 (Rewrite) as appropriate, then present the Review Gate again with the revised output.
- If the user says **"skip"**, abandon the optimization and answer the original prompt directly without expert framing.
- The **Direction-shift pause** in `references/optimize.md` Step 4 is now subsumed by this gate — the Review Gate already surfaces the reframe for user review, so no separate pause is needed.

## Follow-up Handling

When the user follows up on an already-optimized answer (e.g., "tell me more about point 3", "what about the pricing angle?", "can you elaborate?"):
- **Do NOT re-optimize.** The expert and framework are already established.
- **Stay in the same expert's voice** and go deeper on the specific point requested.
- **Maintain plain-English delivery** — the Bilingual Execution rule still applies.
- Only re-optimize if the follow-up is a genuinely new question that shifts the problem domain (e.g., the original was about pricing and the follow-up is about hiring).

## Reference Files

| File | When to read | What it contains |
|------|-------------|-----------------|
| `references/optimize.md` | Triage → Optimize | Steps 1.5–5: Logic Mapping, Expert Selection, Prompt Rewrite, Output Format, Answer Format + examples + common mistakes |
| `references/methodology.md` | Step 3 of Optimize, Polish lane | 4-D prompt optimization methodology: Deconstruct → Diagnose → Develop → Deliver |
| `references/polish.md` | Triage → Polish | Polish instructions + example |
| `references/clarify.md` | Triage → Clarify | Clarify instructions + example, then routes to optimize.md |

## Common Mistakes (Quick Reference)

| Mistake | Why it matters |
|---------|---------------|
| Optimizing trivial tasks | Adds friction where there's no value — users notice and get annoyed |
| Skipping multi-sentence prompts | If the user wrote more than one short sentence, they invested effort in composing the prompt — always route to Polish at minimum, never Skip |
| Assuming intent on ambiguous prompts | Ask 2–3 targeted clarifying questions first — don't guess at context that changes the answer |
| Re-optimizing follow-ups | When the user asks "tell me more about point 3," go deeper in the same expert's framework — don't re-run the full pipeline |
| Executing before Review Gate authorization | Never execute the optimized prompt until the user explicitly says "go", "yes", or equivalent — silence is not consent |

See `references/optimize.md` for the full common mistakes table specific to the optimization pipeline.
