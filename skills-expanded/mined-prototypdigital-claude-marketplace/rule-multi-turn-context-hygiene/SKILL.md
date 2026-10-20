---
name: multi-turn-context-hygiene
description: Don't keep talking to a derailed conversation — consolidate the requirements and restart fresh. Multi-turn degradation is large and doesn't self-correct.
---

# Multi-turn context hygiene

Models perform measurably worse when a task is spread across many conversational turns than when the same task is stated once. Across six task types and multiple model families, average performance dropped by roughly **39%** in sharded multi-turn conversations versus a single fully-specified turn. The cause is **unreliability, not lower ceiling**: the model commits to an interpretation early, often on incomplete information, and then fails to recover even after the missing details arrive — it gets "lost" and keeps building on the wrong assumption.

## Rules

- When a multi-turn conversation has gone off the rails, **don't try to steer it back turn by turn.** Consolidate everything you've learned into one clear, fully-specified instruction and start a **fresh conversation** from it.
- Prefer stating the complete requirement up front over dribbling it out across turns. If you must reveal it incrementally, restate the full accumulated requirement when you add new constraints, rather than assuming earlier turns are still anchoring the model.
- Watch for early lock-in: if the model made an assumption before it had enough information, correcting it in-place is unreliable. Re-specify from a clean slate.
- This pairs with [multi-turn-state-management](multi-turn-state-management.md) (track decisions) and [context-pollution-prevention](context-pollution-prevention.md) (drop stale turns) — together they keep a long interaction from accumulating contradictions the model silently carries forward.

## Examples

```text
// BAD — trying to steer a derailed conversation turn by turn
Turn 1: "Build a checkout flow."
Turn 5: "No, I meant with Stripe, not PayPal."
Turn 8: "Also it needs to handle subscriptions."
Turn 12: "Wait, go back — the cart shouldn't use local state."
→ Model keeps building on early wrong assumptions

// GOOD — consolidate and start fresh once requirements are clear
New conversation:
"Build a Stripe checkout flow with subscription support.
 Cart state must live in the server session, not local state.
 Redirect to /success on completion."
→ One fully-specified turn; no early lock-in to resolve
```

## Source

Laban et al., "LLMs Get Lost in Multi-Turn Conversation," 2025 — <https://arxiv.org/abs/2505.06120>. The ~39% average degradation and the "early assumption, fails to recover" unreliability mechanism are from the paper's six-task evaluation.
