---
name: muxing-style-review
description: 21-rule prose review workflow for technical and academic Markdown/LaTeX excerpts. Use when the user asks for muxing-style-review, wants a complete agent-style check combining check-human.md with agent-style audit-only evidence, wants a compact-rule check, wants a DeepSeek/Codex manuscript draft checked for clarity, evidence, citation discipline, terminology, AI-tell prose, or wants an A/B draft comparison. Prefer a dedicated review subagent when available for non-trivial reviews. Use the sibling style-review skill for the upstream post-hoc audit/polish workflow.
---

# Muxing Style Review

Review technical or academic prose against the bundled `RULES.md` contract. This skill owns two review modes:

- **Complete check**: combine `agent-style review --audit-only FILE` with manual/model review using `references/check-human.md`.
- **Compact check**: load `references/check-compact.md` when the caller explicitly asks for a compact-rule check.

## Core Contract

For complete checks, always cover all 21 rules by combining:

- automatic evidence from `agent-style review --audit-only FILE`, whose implemented detector coverage is documented in `references/rule-detectors.md`; and
- manual/model judgment from `references/check-human.md`, which contains only the rules not covered by automatic detectors.

Treat `references/RULES.md` as the full source of truth for rule text, examples, severity, scope, enforcement tier, and escape hatches. Use it when a finding needs more context than `check-human.md` or `check-compact.md` provides.

Triage by upstream severity first (`critical`, `high`, `medium`, `low`), then by local manuscript impact. Critical/high reader-state, evidence, claim-calibration, and AI-tell issues should usually appear before medium/low polish findings.

Do not report "no style issues" just because `agent-style` is clean. A clean automatic pass only clears implemented detector coverage; `check-human.md` still governs the remaining manual rules.

## Workflow

1. Identify the requested mode:
   - Use complete check by default.
   - Use compact check only when the caller explicitly asks for "compact", "compact rules", "紧凑版", or equivalent.
2. Identify the artifact shape:
   - For Markdown or plain text, review the target directly.
   - For LaTeX, extract only the prose-bearing bounded excerpt. Preserve citations, labels, equations, and inline code as literal markers when they affect meaning.
   - For A/B comparison, align comparable sections before scoring.
3. For compact check, load `references/check-compact.md`, review against those compact directives, and report that the compact mode uses abbreviated rule text.
4. For complete check, run:

   ```powershell
   agent-style review --audit-only FILE
   ```

   Parse the automatic findings and skipped coverage. If `agent-style` is not installed or fails, report that the automatic detector half could not be completed, then still perform the manual/model check with `references/check-human.md`.
5. Load `references/check-human.md` for complete checks. It contains only manual rules, so do not duplicate automatic detector findings unless they interact with a manual rule.
6. For non-trivial complete reviews, delegate the focused manual style review to a subagent when the current Codex harness supports subagents and the user has not prohibited delegation. Give the subagent:
   - the target excerpt or two aligned excerpts;
   - the local reader, venue, and manuscript position if known;
   - any nearby definitions, notation, claims, citations, or reviewer comments needed to judge context;
   - `references/check-human.md`;
   - the output schema from `references/subagent-review-prompt.md`.
7. In the parent Codex thread, inspect the subagent output instead of accepting it blindly. Merge it with local manuscript context, remove false positives, and add any issues the subagent missed.
8. Report findings as a scorecard plus actionable issues. For each issue include rule id, severity, location, evidence, and concrete revision instruction.
9. When this skill is used inside `codex-deepseek-paper-protocol`, output a DeepSeek revision brief using `references/revision-brief-template.md` instead of rewriting the manuscript directly.

## Severity

- **BLOCKER**: upstream `critical`, or any issue that undermines correctness, trust, reader comprehension, citation discipline, or manuscript integration.
- **MAJOR**: upstream `high`, or any issue that makes the argument vague, overclaimed, hard to follow, inconsistent, or visibly AI-written.
- **MINOR**: upstream `medium` or `low` localized polish issues that do not change trust or substance.

Default to fewer, higher-quality findings. Do not list every tiny surface issue when trust or argument-level issues remain.

## Output Shape

For single-file review, return:

1. **Verdict**: ready, usable with minor edits, needs revision, or not usable.
2. **Scorecard**: rule groups with counts by severity.
3. **Findings**: ordered BLOCKER, MAJOR, MINOR. Each finding has rule id, location, evidence, impact, and revision instruction.
4. **Revision Brief**: only when the user asks for revision guidance or when called from the DeepSeek protocol.
5. **Automatic Evidence**: `agent-style` CLI result for complete checks, including any failure to run it.

For compact checks, return a shorter findings list and state that the review used `references/check-compact.md`.

For A/B comparison, report which draft is better by upstream severity group, then list regressions and improvements. Do not treat lower mechanical violation count as decisive if the draft worsens evidence, terminology, or reader state.

## Boundaries

- For the upstream post-hoc audit/polish workflow, point users to the sibling
  `skill-examples/style-review/` package rather than to a private local skill.
- Do not silently downgrade complete checks when `agent-style` is unavailable; state that automatic detector evidence is missing.
- Do not write `FILE.reviewed.md` by default.
- Do not edit manuscript prose directly when the active workflow delegates writing to DeepSeek.
- Do not invent citations, metrics, definitions, or support for unsupported claims. Flag the gap and request source material.

## References

- `references/RULES.md`: vendored upstream `RULES.md`, used as the full bundled 21-rule review contract.
- `references/check-human.md`: complete-check manual rules only; use with `agent-style review --audit-only FILE`.
- `references/check-compact.md`: compact 21-rule directives for explicit compact-mode calls.
- `references/subagent-review-prompt.md`: prompt and output schema for the dedicated review subagent.
- `references/revision-brief-template.md`: template for passing findings back to DeepSeek or another writing agent.
- `references/rule-detectors.md`: automatic detector coverage notes for `agent-style`.
