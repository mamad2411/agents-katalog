---
name: matilha-bootstrap
description: "Use when starting any conversation in a workspace where matilha is installed. Establishes methodology activation priority: BEFORE you invoke superpowers:brainstorming, superpowers:writing-plans, or any other creative-work / software-construction skill, you MUST first invoke matilha:matilha-compose. Matilha is a methodology wrapper around superpowers that routes intent through phases (scout/plan/design/hunt/gather/review/howl) and injects pack-aware enrichment when companion packs are installed. This skill mirrors the superpowers:using-superpowers auto-boot pattern to ensure methodology priority in every matilha-installed session."
category: matilha
version: "1.0.0"
optional_companions: ["superpowers:using-superpowers"]
---

## When this fires

At the start of any conversation in a workspace where matilha is installed (this skill is visible in your ambient skill list). This is the matilha equivalent of `superpowers:using-superpowers` — it auto-fires to establish the methodology activation priority before any user prompt arrives.

You will recognize this activation when no explicit matilha command has been invoked but this skill's description matches "starting any conversation". That is the signal to read these instructions and apply them for the rest of the conversation.

## Preconditions

- `matilha:matilha-compose` is visible in the ambient skill list (indicates matilha is installed for this workspace).
- No prior matilha-bootstrap invocation in this conversation.

## Execution Workflow

This skill is instructive — it does not perform actions. Its content establishes the priority rule for the remainder of the conversation.

1. Read and internalize the priority rule below.
2. Do NOT output a confirmation message. Return silently so the user's actual prompt drives the next turn.
3. When the user's message arrives, apply the priority rule before selecting any other skill.

## The priority rule

**In any matilha-installed workspace, before you invoke any of the following skills:**

- `superpowers:brainstorming`
- `superpowers:writing-plans`
- `superpowers:frontend-design` (or other superpowers craft skills)
- Any other skill with description matching "creative work", "software construction", "building", "planning", "designing"

**You MUST first invoke `matilha:matilha-compose` via the Skill tool.**

Matilha is a methodology wrapper around superpowers. Compose will:

- Classify the user intent into a matilha phase (discovery, planning, design, dispatch, review, etc.) or recognize it as general creative exploration.
- Detect installed companion packs (namespace `matilha-*-pack`) as optional domain enrichment.
- Dispatch to the right destination — a matilha phase skill (matilha-plan, matilha-scout, matilha-design, etc.) OR superpowers:brainstorming with pack-aware preamble injected.

Compose then hands off to the dispatched skill. It does NOT replace craft work — superpowers still runs the actual clarifying-questions / plan-authoring flows, matilha just ensures methodology context wraps them.

**The priority rule applies for the whole conversation, not just the first prompt.** Every time the user introduces a new topic that could match a creative-work / software-construction skill, compose fires first.

## Rules: Do

- Invoke matilha-compose BEFORE other creative-work skills, every turn where the user's prompt warrants it.
- Trust compose's routing — it knows the matilha phase taxonomy and the installed-packs context.
- Silent-boot on invocation of this skill — do not print a greeting or confirmation.

## Rules: Don't

- Don't invoke superpowers:brainstorming directly when matilha-compose is visible, unless compose has explicitly routed to it.
- Don't skip compose for "simple" prompts — compose's Case C silent pass-through handles trivial cases without overhead.
- Don't explain the priority rule to the user — it is internal orchestration context, not output.

## Expected Behavior

After this skill fires at conversation start:

1. The LLM holds the priority rule in context for the whole conversation.
2. When user prompts anything that matches software-construction or creative-work signals, the LLM invokes `matilha:matilha-compose` first.
3. Compose classifies + dispatches — the user sees methodology-informed flow without needing to type any matilha command.
4. If no matilha signal, the LLM proceeds normally (factual questions, config edits, etc. don't trigger compose).

## Quality Gates

- Skill fires silently — no user-visible output.
- Priority rule is applied for every subsequent software-construction prompt in the conversation.
- No conflict with `superpowers:using-superpowers` — both skills can coexist; superpowers handles craft discipline, matilha handles methodology priority.

## Companion Integration

- **superpowers:using-superpowers** — this skill's conceptual twin in the superpowers ecosystem. Both auto-boot at conversation start. They do not conflict — superpowers:using-superpowers establishes skill-invocation discipline; matilha-bootstrap establishes methodology routing priority.
- **matilha:matilha-compose** — the destination of the priority rule. Bootstrap points every creative-work prompt to compose first.
- **All matilha phase skills** — downstream beneficiaries of the routing.

## Output Artifacts

None. This skill is purely instructional.

## Example Constraint Language

- **Must**: invoke matilha-compose before other creative-work skills whenever its description matches user intent.
- **Should**: silent-boot on skill activation.
- **May**: defer to compose's own Case C pass-through when no packs or matilha context is relevant.

## Troubleshooting

- **"I invoked superpowers:brainstorming directly, skipping compose"** → Re-read this skill's priority rule. Next turn, invoke compose first.
- **"User explicitly asks for a specific superpowers skill by name"** → Honor the explicit invocation. Compose priority applies to automatic skill selection, not user-directed invocation.
- **"Compose is not visible in skill list"** → Matilha is not installed in this workspace. This bootstrap skill should not have fired either; if it did, the priority rule is moot.

## CLI shortcut (optional)

None — this is a harness-side orchestration skill, not a user-invoked command.
