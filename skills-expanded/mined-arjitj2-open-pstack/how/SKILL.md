---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
---

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

**Dispatch contract.** Resolve every configured role through [`provider-dispatch.md`](../poteto-mode/references/provider-dispatch.md). Each lane below names a role line in the current harness's pstack model sheet and a default descriptor: use the line's value, or the default when the sheet or the line is missing. `auto` and `inherit-parent` run on the parent model natively. Each lane runs its saved attempt chain: a terminal outcome the sheet's `# fallback` policy authorizes advances to the next saved attempt per provider-dispatch's fallback state machine (`usage-exhausted` only when no policy is saved); every other route failure is a dropout, not a substitution. These lanes are read-only, so an eligible fallback advances directly. On Codex, resolve remaining Claude tool names via [`codex-tools.md`](../poteto-mode/references/codex-tools.md).

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. Dispatch one read-only lane that explores and explains in one pass using the `how explainer` line's descriptor (default `claude:opus@max`), with `references/explainer-prompt.md` built without the explorer-findings section. Go to step 4.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Start all explorers in one fan-out phase through provider dispatch, each with `references/explorer-prompt.md` and its angle filled in. Use the `how explorer` line's descriptor (default `grok:grok-4.7@xhigh`) in `read-only` mode. A native lane uses the parent subagent primitive; an external lane uses the launcher directly.

## 3. Synthesize (complex only)

Wait for every explorer lane to reach a verified terminal result or a recorded dropout under provider dispatch. Retain native results and external task/session handles and receipts; startup, progress, or a worker's claim of completion is insufficient. Then dispatch one read-only lane using the `how explainer` line's descriptor (default `claude:opus@max`), with `references/explainer-prompt.md`, every explorer's full findings, and named dropouts. Verify the explainer's completion before presenting it.

## 4. Present

Present the explainer's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
