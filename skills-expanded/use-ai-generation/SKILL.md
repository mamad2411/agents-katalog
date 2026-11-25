---
name: use-ai-generation
description: >
  WHEN this project calls a model, and what our law says louder than the AI SDK's own skill. Load it
  before writing anything that generates, extracts, classifies, summarises or decides with a model;
  before adding a tool the model may call; before touching one of the twelve files that still call
  `v1/chat/completions` by hand; and the moment the `ai-sdk` skill offers the AI Gateway, a model
  identifier, or a provider install. The foreign skill owns HOW the SDK works; this one owns WHEN it
  is used here, where the key comes from, and which of its suggestions are forbidden in this project.
  Four collisions, each resolved in our favour with the reason, so the foreign skill can be followed
  everywhere else with a clear head.
---

# use-ai-generation

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

The `ai-sdk` skill (vendored, `.claude/skills/ai-sdk/`, provenance in its `SOURCE.md`) is short and
correct. Use it. It has one blind spot, and it is not its fault: it knows the SDK, it does not know
that in this project **the key, the model and the data all belong to somebody already.**

## 1. Its first rule is the one to keep, and it is about you

> *Never write AI SDK code from memory. Whatever you remember about the AI SDK is likely outdated.*

🔒 **AND THE DOCUMENTATION IS NOT ON A WEBSITE — IT SHIPS INSIDE THE PACKAGE**, at
`node_modules/ai/docs/`, eleven sections including `03-agents/`, and it **matches the version this
project actually runs**. The site describes the newest release; the package describes ours. Measured
2026-09-01: it updated together with the package when the SDK went to v7.

✗ **Paid for in one hour, twice.** An agent quoted `stopWhen: stepCountIs(20)` from those very docs
while the project sat on v6 — correct for our code, obsolete for the ecosystem, because in v7
`stepCountIs` became `isStepCount`. Reading the docs is right; assuming they are the ecosystem's
latest is not.

## 2. 🛑 Four collisions, and on all four we win

### 2.1 The AI Gateway is forbidden here

The foreign skill offers `AI_GATEWAY_API_KEY` as the fastest start. **Do not.**

This project has **one OpenAI key and three consumers** — the project itself, the data layer, the
knowledge graph — and a plaque on the bot's screen that turns amber and NAMES whoever is missing it.
A gateway would be a second path for the key, and second paths in this project diverge silently:
the panel paid a full day of debugging for exactly one such indicator, because the second consumer
fails **without saying anything** (ingestion answers `200` and embeds nothing).

**Where the key comes from:** `openAiKey()` in `lib/openai-key.ts`. Never `process.env` directly.

### 2.2 The model identifier is a SETTING, not a literal

The foreign skill is right that model ids must not come from memory. Here they must not come from
code either: the model arrives from `OPENAI_TEXT_MODEL`, and that value is set by a human on
`/{lang}/architect/telegram`. Its rule applies to **what you offer in that setting**, not to a string
you type into a call.

🛑 **Twelve files currently hard-code `?? "gpt-4o-mini"` as a fallback.** That is the same default
repeated twelve times from memory — a debt, not a pattern.

### 2.3 The provider package is ours to install, and its major line must match

`ai@7` needs `@ai-sdk/openai@4`. The foreign skill says «install `ai` first, providers later» and
does not know that a mismatched provider line fails in ways that read like nonsense inside somebody
else's file.

🔒 **Two instruments, both required, and one of them is invisible to the other:**
```
npm ls ai                    → one line and `deduped`   (catches DUPLICATES)
npm view ai version          → compare with installed   (catches STALENESS)
```
✗ Paid 2026-09-01: the first was green while the project sat a **major version** behind. It cannot
catch that, and its success is what stopped anybody from looking.

### 2.4 Skill uploads are not our mechanism for the fact registry

v7 brings `uploadSkill()`. It loads a bundle of files into a **sandboxed container on the provider's
side**, used together with a code-execution tool. 🛑 **That container cannot see our data layer, our
tables, our graph, our map** — and resolving a fact is precisely reaching into them.

**The right primitive for «let the model pick the registry element itself» is `tool()`**: declared in
our code, chosen by the model from its description, executed on our server where the database and
the keys are.

🔒 **Their honest niche, for the day it comes:** self-contained computation that needs none of our
data and is loaded **at runtime without a rebuild** — the exact constraint that forced a fact's
function to be a *description* rather than code (81-8).

## 3. What to reach for, instead of building it

| You are about to write | It already exists |
|---|---|
| a loop «ask → parse → decide whether to ask again» | `ToolLoopAgent`, default `stopWhen: isStepCount(20)` |
| JSON parsing and validation after every call | `Output.object({ schema })` on zod |
| «the model chose a source» expressed in prose | `tool({ description, inputSchema, execute })` |
| a journal of what the model decided and why | **`steps` — every call and result, for free** |
| «use the expensive model for the hard part» | `prepareStep({ stepNumber, steps })` |
| a spending cap | a custom `StopCondition` over `steps.reduce(usage)` |

🔒 **Check every name above against `node_modules/ai/docs/` before typing it.** This table is a map of
what exists, not a quotation of the current API — and by the law of §1 it is exactly the kind of list
that goes stale.

## 4. The twelve hand-rolled files are history, not a pattern

`lib/facts/run-fn` · `lib/products/telegram-desk/{answer,route-intent}` · its six `branches/*` ·
`app/api/i18n/translate` · `_tools/fact-draft/server/draft` · `_tools/socials-ai/server/resolve`.

They call `https://api.openai.com/v1/chat/completions` with `fetch`. **New code does not.**

🔒 **Converting one is a STEP with its own proofs, never a drive-by edit while passing through.** They
carry live behaviour — the bot's whole understanding of a message runs through `route-intent` and the
branches — and «I was in there anyway» is how a working product breaks quietly.

✗ **And the debt has already bitten in an unexpected direction:** the v6 → v7 migration cost nothing
precisely BECAUSE nothing used the SDK at runtime. That was luck wearing the costume of a decision.

## 5. Two laws of this project that survive every SDK

🔒 **A model PROPOSES, a person APPLIES.** Taken verbatim from `socials-ai` and re-proven by
`fact-draft`: closed lists are verified by us, never promised by the model — it will return a value
outside the list and it will look plausible. **A draft that fails verification is dropped whole**,
because half-parsed gets saved.

🛑 **`eval` and `new Function` are forbidden forever.** Whatever the model writes reaches our
executor, and the only defence that holds is **not being able to execute**. `lib/facts/run-fn.ts`
knows a finite set of operations and refuses everything else by construction — copy that shape.
