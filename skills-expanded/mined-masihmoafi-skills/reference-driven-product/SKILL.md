---
name: reference-driven-product
description: Use when improving or rebuilding a product from a reference app, screenshots, user feedback, or open-source alternatives, when speed and a restart guide matter. Not for isolated bug fixes or purely visual imitation.
---

# Improve a product from a working reference

Deliver the user's important workflows, prove each claim, and leave a guide that reaches the same place without this conversation.

1. **Destination.** Read the real project state and the user's newest priorities before extending an old plan. Name the few jobs they want done and what they value in the reference; not every visible reference feature is a requirement. One acceptance contract, per the [spec](../spec/SKILL.md) skill.
2. **Compare like with like.** View every screenshot and use the reference. Compare the same task in the same state, and record differences in behavior, hierarchy, type, spacing and interaction. Match zoom, scale, window size and theme before measuring pixels. Check what reached the built executable, not only the source.
3. **Learn from open source.** Study a few relevant projects from primary sources: version, license, platform, gaps. Separate their claims from what you observe. Read the code behind an advantage and reuse it when the architecture and license fit, with attribution. Do not switch stacks because another product looks fast.
4. **Measure fairly.** Use the [experiment workflow](../experiment-workflow/SKILL.md): equal work, same host, run serially; keep startup, indexing, input-to-frame and save latency apart; check correctness (exact saved text, Unicode) with speed.
5. **Fix the most valuable gap.** A small change tied to the user's priority, with a check that fails today, made through the shared component or path, verified on the built artifact in the real flow. Show it early; fold feedback into the contract. Never call partial work finished or ship controls that do nothing.
6. **Guide for a restart.** One project guide, linked from the orientation file, answering: what we build and what waits; which references and observations matter; the simplest architecture and why; the build-and-verify order from a clean checkout; what failed and the decision that avoids it; what is verified, unknown and next. A route, not a diary; link the evidence.
