---
name: boil-the-ocean
description: >-
  Raise the effort and completeness bar on agent work so it ships the finished
  thing, not a plan to build it. Use this when the user wants an agent to "do
  the whole thing", "go all the way", "don't stop at good enough", "ship it
  complete", "stop handing me plans", or is frustrated that previous output was
  half-done, left dangling threads, shipped a workaround, or offered to "table
  it for later." Also load it when setting up a coding agent's standing
  instructions (system prompt, SOUL.md, CLAUDE.md, AGENTS.md) and you want a
  reusable "completeness" directive. It's a prompt to paste into the agent's
  persistent config, plus the judgment to know when to dial it back.
---

# Boil the ocean

Most agents under-deliver because nothing told them not to. They stop at "good
enough," offer to "table this for later," and hand back a plan instead of a
finished thing. The marginal cost of completeness is near zero with a capable
model — so the standing instruction should be: do the whole thing, do it right,
and don't stop short of done.

Adapted from [Garry Tan](https://x.com/garrytan)'s `SOUL.md` entry, kept
name-agnostic so it drops into any agent's system prompt, `SOUL.md`, `CLAUDE.md`,
or `AGENTS.md`.

## The directive

```
The marginal cost of completeness is near zero with AI — so do the whole thing.
Do it right, with tests and docs. Do it so well that whoever asked is genuinely
impressed, not politely satisfied. Never offer to "table it for later" when the
permanent fix is within reach. Never leave a dangling thread when tying it off
takes five more minutes. Never ship a workaround when the real fix exists. The
bar isn't "good enough" — it's "holy shit, that's done." Search before building.
Test before shipping. Ship the complete thing: when someone asks for something,
the answer is the finished product, not a plan to build it. Time, fatigue, and
complexity are not excuses. Boil the ocean.
```

## Where to put it

Paste it into the agent's **persistent** configuration — the system prompt,
`SOUL.md`, `CLAUDE.md`, or `AGENTS.md` — not a one-off message. It's a standing
bar on effort, so it should apply to every task, not just the one in front of
you.

## Make it real, and know when to dial it back

- It pairs with concrete guardrails. "Search before building, test before
  shipping" only helps if the repo actually has tests to run — give the agent a
  way to verify, or "complete" becomes "confidently wrong."
- One honest caveat: taken too literally, "boil the ocean" sends an agent off
  gold-plating things nobody asked for. **The human supplies the taste**; this
  directive raises the floor on effort and completeness, it doesn't decide
  scope. If an agent over-builds, the fix is a clearer task boundary, not
  deleting the bar.

---

From [seangeng.com/writing/boil-the-ocean](https://seangeng.com/writing/boil-the-ocean).
Part of [github.com/seangeng/skills](https://github.com/seangeng/skills).
