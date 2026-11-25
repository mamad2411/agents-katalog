---
name: handoff
description: >-
  use this when a session hits a phase boundary — choose
  continue/clear/compact/handoff/subagent, or write a review-grade handoff doc
license: MIT
metadata:
  portability: portable
---
# handoff

Portable context transfer and the **phase-boundary decision tree** (continue / clear / compact / handoff / subagent).

## Smart-zone budget
Dumb-zone onset is model-dependent; working figure ≈ **150,000 tokens** (a slope, not a cliff). Bail/compact/handoff as you approach it. **At ≥~150k mid-feature:** stop hard work; prefer compact+one-line focus to finish a thin slice, or handoff if crossing a boundary — **never "just continue."**

**Tiebreaker:** the tree outranks any single skill's default. If a skill suggests Continue but the tree's first question (still in smart zone?) is already NO, the tree wins — compact or handoff.

## Ordered decision tree (ask in order)
1. **Continue?** Still in smart zone *and* you still need the primary grilled/implementation context. **Typical mid-feature at ~90k: Continue** — handoff early throws away primary context. Grill→implement usually Continues.
2. Else if context is **irrelevant** to what's next → **Clear** (cheapest; most room).
3. Else if work must cross **agent / directory / person / side-quest** → **Handoff**.
4. Else if the next chunk can run **AFK** (no human), e.g. automated review → **Subagent**.
5. Else → **Compact** with a one-sentence focus (residual default). Implement→QA is a cast-iron compaction case.

**"Review" means walk the tree:** same-agent QA → **Compact**; AFK automated review → **Subagent**; other agent/person/dir → **Handoff**. Do not answer compact-vs-subagent without asking which of those three. If the user won't disambiguate, assume same-session QA → **Compact**, and say that's what you assumed.

Do not outsource mid-phase boundaries to auto-compaction.

## Handoff (when tree says handoff)
1. State a **reason** (shapes the summary).
2. Write an ephemeral handoff doc to the OS temp dir. **Never commit handoffs into the repo.**
3. Include: feature summary; files + `git status`/`diff`; binding decisions/bugs; **pre-existing issues out of scope**; verification done; conventions; **review angles**; suggested next skills.
4. Seed the next session with that file only after clear — not the old transcript.

Compaction stays inside one agent/directory; handoff crosses those boundaries.

## Related
compact · grill-execute-clear · to-spec
