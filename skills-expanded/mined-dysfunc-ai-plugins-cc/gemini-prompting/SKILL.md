---
name: gemini-prompting
description: Internal guidance for composing Gemini prompts for planning, research, diagnosis, and review tasks inside the Gemini Claude Code plugin
user-invocable: false
---

# Gemini Prompting

Use this skill when `gemini:gemini-rescue` needs to ask Gemini for help via the `task` runtime.

Prompt Gemini like an analyst, not a collaborator with tool access. The plugin runs Gemini headless via `gemini -p`, so it cannot read files, run commands, or browse the working tree on its own. Everything Gemini sees has to be in the prompt text.

Core rules:
- Prefer one clear task per Gemini run. Split unrelated asks into separate runs.
- Tell Gemini what done looks like. Do not assume it will infer the desired end state.
- Keep prompts compact and block-structured with XML tags so the contract has stable shape.
- Inline any relevant code, log output, or file excerpts directly in the prompt — Gemini cannot fetch them.
- Add explicit grounding rules for any task where unsupported guesses would hurt quality (review, diagnosis, postmortem analysis).
- For follow-up requests, the plugin prepends the prior per-job transcript automatically; you only need to send the delta instruction.

Default prompt recipe:
- `<task>`: the concrete job and the relevant repository or failure context (inlined).
- `<structured_output_contract>` or `<compact_output_contract>`: exact shape, ordering, and brevity requirements.
- `<default_follow_through_policy>`: what Gemini should do by default instead of asking routine questions.
- `<grounding_rules>`: required for review, research, or anything that could drift into unsupported claims.

When to add blocks:
- Diagnosis or planning: add `<completeness_contract>` and an `<observable_evidence>` block listing what you've inlined.
- Review or adversarial review: prefer the built-in `/gemini:review` and `/gemini:adversarial-review` commands — those carry the review contract and JSON schema. Only fall back to `task` when the review needs a non-standard target or shape.
- Research or recommendation tasks: add `<research_mode>` and `<citation_rules>` (cite the inlined evidence by line reference, not URL).

Working rules:
- Prefer explicit prompt contracts over vague nudges.
- Use stable XML tag names so the structure is recognizable across runs.
- Do not raise reasoning effort first. Tighten the prompt and grounding rules before escalating.
- Ask Gemini for brief, outcome-based progress updates only when the task is long-running.
- Keep claims anchored to inlined evidence. If something is a hypothesis, say so.
- For long-running follow-ups, lean on `--resume-last` so the prior transcript is reused; the plugin truncates oldest turns when the transcript exceeds the cap.

Prompt assembly checklist:
1. Define the exact task and scope in `<task>`.
2. Inline the evidence Gemini needs to answer — file excerpts, log slices, error messages, schemas.
3. Choose the smallest output contract that still makes the answer easy to use.
4. Decide whether Gemini should keep going by default or stop for missing high-risk details.
5. Add grounding and verification tags only where the task needs them.
6. Remove redundant instructions before sending the prompt.

Common antipatterns:
- Asking Gemini to "look at file X" — it cannot. Inline X (or a relevant slice) in the prompt instead.
- Asking Gemini to "run the tests and report" — it cannot. Run them yourself, inline the output, then ask Gemini to analyze.
- Restating the full prompt on every `--resume-last` turn — the prior transcript is already prepended.
- Mixing several unrelated questions in one prompt — split them into separate `task` runs.
