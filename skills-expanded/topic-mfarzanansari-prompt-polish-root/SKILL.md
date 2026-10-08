---
name: prompt-polish
description: Rewrite a rough prompt into a polished, model-specific prompt grounded in the official Anthropic prompting guides. Use when the user invokes prompt-polish, types an invocation like "prompt-polish/FABLE 5/[prompt]" or "prompt-polish/OPUS 4.8/[prompt]", or asks to polish, improve, rewrite, optimize, or tune a prompt for a named model ("make this prompt better for Fable 5", "tune this for Opus"). Supports Claude Fable 5 and Claude Opus 4.8 (Opus 4.7 routes to 4.8 guidance). If no draft prompt is provided, ask for it rather than inventing one.
---

# Prompt Polish

Turn a rough prompt into the prompt an expert would have written for that exact model — using the model's official prompting guide, not generic prompt-engineering folklore.

**Core belief: polishing is mostly subtraction.** Frontier models rarely fail from missing instructions; they fail from missing intent, instruction noise, and habits carried over from older models. The polished prompt is the smallest set of words that makes the target model's defaults work in the user's favor.

## Invocation

Accept any of these shapes:

- `prompt-polish/[MODEL]/[PROMPT]`
- `prompt polish / fable / [PROMPT]`
- `OPUS 4.8: [PROMPT]`
- Natural language: "polish this for Fable 5", "make this prompt work on Opus"

Model aliases (case-insensitive):

| Input contains | Routes to |
|---|---|
| `fable`, `fable 5`, `fable5`, `claude fable 5`, `claude-fable-5`, `mythos` | `references/fable-5.md` |
| `opus`, `opus 4.8`, `opus48`, `4.8`, `claude opus 4.8`, `claude-opus-4-8` | `references/opus-4-8.md` |
| `opus 4.7`, `4.7` | `references/opus-4-8.md` — the closest published doctrine; say so in the Note line |

- Model missing → default to Fable 5 and say so in the Note line.
- Prompt missing → ask for it. Never polish an imagined prompt.
- Unsupported model (GPT, Gemini, Sonnet, Haiku, …) → say it isn't supported yet, name the supported models, and offer the nearest fit. Never fake model-specific guidance.

## Workflow

1. **Parse and route.** Extract the model and the raw prompt. Read ONLY the routed reference file — it is the single source of model doctrine; this file never duplicates it.

2. **Diagnose before touching anything.** Classify the raw prompt on four axes:
   - **Form** — a one-off task message, or a system/harness prompt that will run many times? Harness-only patterns (memory rules, send-to-user tools, context reassurance) are bugs in a one-off message.
   - **Class** — *ask* (question or one-shot generation) · *build* (coding or creation, one session) · *agent* (long-running, autonomous, tool-using) · *review* (find problems) · *design* (frontend or visual) · *pipeline* (runs unattended at scale). Build-vs-agent tiebreaker: *agent* only if the work should survive the user walking away for an hour; otherwise it's *build*.
   - **Gaps** — missing intent, undefined deliverable, no done-condition, unstated audience.
   - **Noise** — instructions the target model makes redundant. The reference's "free by default" section lists them; delete on sight.

3. **Pick the smallest tier that fits.**
   - **Tier 1 — light touch** (most *ask* prompts): intent, deliverable, audience, constraints — in one or two paragraphs. No headers, no scaffold.
   - **Tier 2 — structured** (*build*, *review*, *design*, *pipeline*): add scope, output contract, success criteria. A section must earn its place.
   - **Tier 3 — harness** (*agent*): autonomy boundaries, evidence-grounded progress, verification cadence, communication contract.

   If the polished prompt is much longer than the raw one, the added words must carry proportional odds of success. When in doubt, drop a tier.

4. **Rewrite** using the reference's decision table and snippet library. Adapt snippets to the task; never paste boilerplate the diagnosis didn't call for. Anything material that's missing and that only the user knows becomes a `[BRACKETED PLACEHOLDER]` — each one fillable by the user in under a minute. Example hints inside brackets (`[stack — e.g., React + Tailwind]`) are suggestions, not inventions. If the rewrite would need more than four placeholders, the task itself is underspecified — ask instead, per the output contract.

5. **Gate-check, then emit.** Walk the hard gate below. Fix violations before output, not after.

## Approved Praxis contracts

When the input is explicitly labeled as an approved [Praxis Workflow OS](https://github.com/mfarzanansari/praxis-workflow-os) contract, treat that contract as authoritative. Preserve its target model, task form, constraints, approval gates, and done-condition. Adapt wording through the routed model doctrine, but do not redesign the workflow, add deliverables, or relax its gates. Praxis is optional; inputs not labeled this way follow the normal workflow above.

## Hard gate

<HARD-GATE>
- The polished prompt asks for the same task as the raw prompt. Polishing reshapes how the task is asked — never what is asked.
- Precedence when they collide: user intent outranks model doctrine. If the raw prompt itself contains a doctrine anti-pattern (a vague aesthetic like "make it modern", an open-ended "clean up everything"), don't delete it — repackage it: bound it, make it concrete, or route it through a placeholder or propose-first step.
- Nothing is invented: no facts, file paths, tools, data sources, deadlines, audiences, or policies the raw prompt didn't contain. Missing and material → bracketed placeholder. Missing and immaterial → leave out.
- Every instruction in the output either changes the target model's behavior or gets deleted. "Be thorough", "think step by step", and restated defaults are noise on these models.
- Never instruct the target model to reveal, transcribe, or echo its chain-of-thought. If reasoning visibility matters, ask for a concise rationale, key assumptions, and evidence instead.
</HARD-GATE>

## Output contract

Emit, in order, and nothing else:

1. The polished prompt in a single fenced `text` code block — ready to copy.
2. `Fill in:` — one line listing the bracketed placeholders. Only if any exist.
3. `Note:` — one line, only if material: defaulted model choice, 4.7→4.8 routing, a refusal-risk domain (per the reference), instructions removed because the model no longer needs them, or an effort/API-setting recommendation that can't live inside a prompt.

No preamble, no "here's your polished prompt", no explanation of changes. If the user asks why, then explain — diff-style, briefly. If the raw prompt is unsafe, or so under-specified that any rewrite would be guessing at the task itself, ask the one or two questions that unblock it instead of guessing.

## Anti-patterns

The known failure modes of prompt-improvement tools. Each one is a bug here:

- **Inflation** — turning a two-line question into an agent operating manual.
- **Boilerplate transplant** — pasting every reference snippet whether or not the diagnosis called for it.
- **Drift** — "improving" the task into a different task: adding deliverables, audiences, or quality bars the user never asked for.
- **Museum instructions** — keeping prompt cargo-cult ("you are a world-class expert", "take a deep breath") that does nothing on current models.
- **Wrong-model habits** — micromanaging Fable 5 with steps it doesn't need, or leaving Opus 4.8 scope implicit when it follows instructions literally.

## Extending to a new model

1. Find the model's official prompting guide. Never write doctrine from memory.
2. Distill it into `references/<model-slug>.md` using the existing files' structure: model profile → free-by-default list → decision table → snippet library → skeletons → final check.
3. Add the alias row to the table above. Keep this file model-agnostic.
