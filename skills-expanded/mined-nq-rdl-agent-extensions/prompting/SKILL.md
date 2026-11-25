---
license: Apache-2.0
description: Internal guidance for composing Codex and GPT-5.6 prompts for coding, review, diagnosis, and research tasks inside the Codex Claude Code plugin
user-invocable: false
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

<!--
SPDX-License-Identifier: Apache-2.0
Derived from openai/codex-plugin-cc v1.0.6 (db52e28), Apache-2.0. Modified for rdl-agent-extensions.
Rewritten from the GPT-5.4 guide against OpenAI's GPT-5.6 prompting guidance.
-->

Source: OpenAI, [Prompting guidance for GPT-5.6 Sol](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6), verified 2026-09-29. That guide targets the API; this skill keeps only what a `codex:rescue` prompt can use. Re-check it when OpenAI ships a new model family. If it and this skill disagree, follow the guide for prompt wording and this skill for companion flags.

# GPT-5.6 Prompting

Use this skill when `codex:rescue` needs to ask Codex or another GPT-5.6-based workflow for help.

GPT-5.6 rewards leaner prompts than 5.4/5.5. Prompt Codex like an operator: state the task once, give the output contract, set follow-through defaults, and stop. Do not pad with repeated instructions or long natural-language explanations.

Core rules (5.6-specific):
- **State instructions once.** 5.6 follows a single clear instruction; repeating it degrades quality. Pruning redundant tools, examples, and restated rules improves both quality and token cost.
- **One autonomy / approval-boundary policy.** 5.6 is proactive. Repeated "ask first" instructions cause over-asking. Give one consolidated policy block that says when to proceed and when to stop for high-risk missing context.
- **Do not add generic length prose.** 5.6 is more concise than 5.5 by default, so "be brief" / "be thorough" lines over-correct. The companion exposes no verbosity parameter (the guide's `text.verbosity` is an API setting); put task-specific length in the output contract.
- Prefer one clear task per Codex run. Split unrelated asks into separate runs.
- Tell Codex what done looks like. Do not assume it will infer the desired end state.
- Add explicit grounding and verification rules only where unsupported guesses would hurt quality.
- Prefer better prompt contracts over raising reasoning effort or adding explanations.
- Use XML tags consistently so the prompt has stable internal structure.

Default prompt recipe:
- `<task>`: the concrete job and the relevant repository or failure context.
- `<structured_output_contract>` or `<compact_output_contract>`: exact shape, ordering, and brevity requirements.
- `<autonomy_policy>`: one block — what Codex does by default vs. when it stops for high-risk missing context. (Replaces scattered "ask first" lines.)
- `<verification_loop>` or `<completeness_contract>`: required for debugging, implementation, or risky fixes.
- `<grounding_rules>` or `<citation_rules>`: required for review, research, or anything that could drift into unsupported claims.

When to add blocks:
- Coding or debugging: add `completeness_contract`, `verification_loop`, and `missing_context_gating`.
- Review or adversarial review: add `grounding_rules`, `structured_output_contract`, and `dig_deeper_nudge`.
- Research or recommendation tasks: add `research_mode` and `citation_rules`.
- Write-capable tasks: add `action_safety` so Codex stays narrow and avoids unrelated refactors.

How to choose prompt shape:
- Use built-in `review` or `adversarial-review` commands when the job is reviewing local git changes. Those prompts already carry the review contract.
- Use `task` for diagnosis, planning, research, or implementation when you need to control the prompt directly.
- Use `task --resume-last` for follow-ups on the same Codex thread. Send only the delta instruction unless the direction changed materially.

Migration from 5.4/5.5:
- Keep the current effort as the baseline, then test the same setting and one level lower. See `codex:model-guide` for the ladder and per-model defaults.
- Remove obsolete step-by-step scaffolding; add targeted fixes only where a task fails.

Prompt assembly checklist:
1. Define the exact task and scope in `<task>`.
2. Choose the smallest output contract that still makes the answer easy to use.
3. Write one `<autonomy_policy>`: proceed by default, stop only for high-risk missing context.
4. Add verification, grounding, and safety tags only where the task needs them.
5. Remove redundant instructions before sending — leaner is better on 5.6.

Reusable blocks live in [references/prompt-blocks.rst](references/prompt-blocks.rst).
Concrete end-to-end templates live in [references/codex-prompt-recipes.rst](references/codex-prompt-recipes.rst).
Common failure modes to avoid live in [references/codex-prompt-antipatterns.rst](references/codex-prompt-antipatterns.rst).
