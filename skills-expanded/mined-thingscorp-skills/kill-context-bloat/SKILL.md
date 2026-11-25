---
name: kill-context-bloat
description: >-
  use this when agent sessions feel bloated — the measure→edit→quit→remeasure
  lab with /context; named harness settings as examples not law
license: MIT
metadata:
  portability: portable
---
# kill-context-bloat

Shrink always-on payload so more of the window stays in the **smart zone**. Motive is **quality of attention**, not min-maxing spend.

## Lab loop (do not skip remeasure)
1. Fresh session. Measure starting context (your harness's slash command — see `<harness>-habits`; or a request logger).
2. Trivial Hello; record baseline tokens (demos often start ~**68k** — shockingly high).
3. Edit harness settings. First **locate the settings file** for your harness and **back it up**. **Named flags below are examples for one harness/version — not universal law**:
   - disable unused connectors/integrations — demo drop ~68k→~47k
   - disable unused workflows — further toward ~39k
   - disable bundled skills you don't use — toward ~37k (also disables those skills entirely)
   - disable artifacts/media generation when unused
   - **deny unused tools** — denied tools drop **definitions** from the system prompt, not just runtime blocks

   "Unused" test: if nothing in your last ~20 sessions referenced it, it's unused. When unsure, disable one thing at a time and remeasure.
4. **[human step — the agent cannot do this]** Fully quit and relaunch — edits often change nothing until restart (**deny without relaunch** is a common false "fix").
5. Hello → measure → **remeasure**. Repeat until the floor is honest (demos often land near ~**20k** after cuts).

## Cut categories
Unused MCP/connectors, workflows, bundled skills, artifacts, always-on essay instructions (move behind pointers/skills), unused tools via deny lists.

## See the real cost
- **Turns vs provider requests** — a *turn* (your message → final reply) can hide many *provider requests* (tool rounds, retries). Point a request logger at your agent and look at the actual graph instead of guessing.
- **Prefix-cache nuance** — providers cache matching prompt prefixes (cached input often ~10× cheaper than base). The first hit may be a **cache write**; the later reads are the win. Subscriptions usually beat surprise API burn; **process > penny-pinching**.

## Before you start
Back up your settings file and skills directory before labs that reset harness config, so you can restore them.

## Success
Same task with less preamble and a visibly lower starting token floor — more room for smart-zone work.

## Anti-patterns
- Denying a tool and calling it fixed without quit/relaunch — edits often change nothing until restart.
- Cutting for spend instead of attention — the motive is quality of attention, not min-maxing spend.
- Guessing which requests are expensive; point a request logger at the graph instead.
- Editing harness config with no backup before the lab.

## Related
session-hygiene · steering-push-vs-point
