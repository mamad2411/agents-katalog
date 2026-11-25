---
name: no-stub
description: "MANDATORY before declaring code \"done\", \"ready\", or ending a turn after writing a function/handler/module. Use whenever you write or edit code and are tempted to leave a placeholder — TODO/FIXME, NotImplementedError, an empty `...` body, \"your code here\", \"implementation goes here\", a stub return, or a half-built path. Forces you to finish the job: real, working implementation, or an explicit intentional-stub declaration. Triggers on \"I'll add this later\", \"placeholder for now\", \"scaffolding\", \"stub out\", \"TODO\", \"left as an exercise\", \"wire this up later\"."
---

# No Stub

**A function that says `# TODO: implement` is not a function. A scaffold is not a feature.**

You were asked to do the work. Leaving a marker where the logic should be moves the work back to the human — silently, where they'll find it at runtime instead of in your reply.

## The rule

> **Don't ship half-written code.** Every code path you touch is either fully implemented, or you say out loud that it isn't and why.

## What counts as a stub

- `TODO` / `FIXME` / `XXX` / `HACK` comments parked where logic belongs
- `NotImplementedError`, `raise NotImplementedError`, `throw new Error("not implemented")`, Rust `todo!()` / `unimplemented!()`
- Natural-language placeholders: `// your code here`, `# implementation goes here`, `// rest of the handler here`, `fill this in later`
- Empty bodies: a function whose only statement is `...`, `pass  # TODO`, or `// ...`
- Fake returns: `return null // TODO`, `return []  # placeholder`

## Step 1 — When you catch yourself reaching for a placeholder, stop

A placeholder is a signal you don't yet know how to do the thing, or you're trying to look finished. Both are fixable:

- **Don't know the value?** Read the surrounding code, the types, the caller. The answer is almost always already in the repo.
- **Genuinely blocked** (needs a secret, an external API you can't reach, a human decision)? That's not a stub — that's a surfaced blocker. Implement everything around it and state the one thing you need.
- **Scope is large?** Implement the slice you were asked for completely. A small thing that works beats a large thing that's all scaffolding.

## Step 2 — Finish the path

Replace each placeholder with code that actually runs. If a branch can't happen yet, make it fail loudly and correctly (validate + raise a real, typed error) rather than silently returning a fake value.

Then verify it (pair with **`verify-before-done`**) — a stub-free function that was never run is only half-trusted.

## Step 3 — Intentional stubs are allowed, but only out loud

Sometimes a stub is the correct deliverable: an interface method, an abstract base, a Protocol, a deliberately-deferred path the user agreed to. That's fine — but it must be a *decision*, not a leftover. Declare it:

```
NO-STUB: INTENTIONAL — abstract method; concrete impls live in subclasses
NO-STUB: INTENTIONAL — payments path deferred per user; raises until phase 2
```

The Stop hook scans code you edited this turn for stub markers and blocks the turn unless it's clean or you've recorded that line.

## Avoiding false alarms

The gate is built to ignore legitimate `...`: JS spreads (`{...obj}`, `[...arr]`, `fn(...args)`), type-hint ellipses (`Tuple[int, ...]`), and any `...` that isn't the sole statement of a body. If it still mis-fires on a real interface stub, use the sentinel above or the kill switch.

## Kill switch

False positive (data file with the word "todo", a real ellipsis it misread): `touch .no-stub-off` in the project root, or `export NO_STUB_GATE=off`.

## Pairs with

- **`verify-before-done`** — once the code is real, prove it runs.
- **`scope-guard`** — finish *the* job, not five other files while you're there.
