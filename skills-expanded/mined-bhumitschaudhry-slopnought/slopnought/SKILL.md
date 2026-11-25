---
name: slopnought
---

# Slopnought

## Why this skill exists

LLM-generated code often works today but becomes a liability tomorrow — nobody (human or agent) can tell what it does, why, or what's safe to change. This skill makes maintainability a first-class requirement, on par with "does it work."

Two modes:

1. **Code generation mode** — active whenever the agent produces code that outlives the session.
2. **Refactoring mode** — invoked via `/slopnought-audit`, for scanning and improving existing code.

Read the relevant reference file for the mode you're in: `references/code-generation-mode.md` for new code, `references/refactoring-mode.md` for audits. Keep `references/anti-patterns.md` in mind throughout.

## The core question

Before writing or changing a single line, and again before calling the work done, ask:

> **If a competent developer who has never seen this project opened this file with no other context, would they understand what it does, why it exists, how it connects to the rest of the system, how to verify it works, and what they'd risk by changing it?**

If the honest answer is no, the work isn't finished — regardless of whether the immediate task "works."

## How to use this skill

**For new code or features** → read `references/code-generation-mode.md`. It covers architectural boundaries, naming, error handling, security, documentation of intent, testing, and the specific discipline needed to avoid the failure modes in `references/anti-patterns.md`.

**For auditing or improving an existing codebase** → the user (or agent) invokes `/slopnought-audit`. Read `references/refactoring-mode.md` for the full workflow: how to scan, score, prioritize, report, and (with consent) remediate.

**For writing an Architecture Decision Record** (either mode may call for one) → use `references/architecture-records.md` and the template at `assets/adr-template.md`.

Don't try to hold all the reference material in your head at once — load the relevant file for the mode you're in, and re-check `anti-patterns.md` whenever something starts to feel like a shortcut.

## Non-negotiable principles (apply in both modes)

These five hold regardless of which mode you're in or how small the task seems:

1. **Maintainability is a requirement, not a nice-to-have.** A fast, working solution that nobody can safely modify later has not actually solved the problem — it has deferred it, with interest. Weigh maintainability alongside correctness and delivery speed when making tradeoffs, not after them.

2. **Optimize for the next reader, not for fewest keystrokes now.** The next reader might be a human teammate, a future agent session with zero memory of this one, or you in a different context window. Write as if you will have none of the context you have right now — because structurally, you won't.

3. **Every non-obvious decision needs a visible reason.** If a reviewer would reasonably ask "why is this done this way?", the answer should already be written down — in a comment, a docstring, a commit message, or an ADR — not locked in the head of whoever wrote it.

4. **Consistency beats local optimality.** A slightly-worse pattern applied consistently across a codebase is more maintainable than five locally-optimal patterns that all do the same thing differently. Match what's already there before introducing something new; if the existing pattern is genuinely bad, fix it deliberately and broadly, not by quietly adding a sixth variant.

5. **If you wouldn't want to debug it at 2am with no memory of writing it, don't ship it.** This is the gut-check version of everything above. Trust it when something feels like a shortcut.

## Scope discipline

This skill is about maintainability, not about gold-plating. It does not mean:
- Adding abstraction layers for hypothetical future requirements that don't exist yet (speculative generality is itself a maintainability problem — it adds indirection that has to be understood for no current benefit).
- Rewriting working, well-understood code because a newer pattern exists.
- Writing exhaustive documentation for trivial, self-evident code.

The judgment call is always: *does this serve the next reader, or does it serve an abstract ideal of "good code"?* When genuinely unsure whether something is over-engineering or right-sized, say so and explain the tradeoff rather than silently picking one.
