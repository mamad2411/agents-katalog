---
name: adversarial-review
description: Run an adversarial peer-review swarm on a paper draft, report, or manuscript by spawning parallel persona subagents (hostile theorist, experimentalist, statistician, journal editor, citation auditor, figure critic) and synthesizing their critiques into a ranked fix list with suggested defense experiments. Use when the user asks for a paper review, referee simulation, desk-reject check, pre-submission audit, citation audit, figure audit, novelty attack, or wants feedback on a draft report before submission or internal circulation.
---

# Adversarial Review

Use this skill to stress-test a draft before it reaches real reviewers. It spawns a small swarm of specialized persona subagents in parallel, each attacking the manuscript from one angle, then synthesizes the critiques into a prioritized fix list.

This is the opposite of a friendly read-through. The goal is to surface desk-reject-level problems, unsupported claims, weak statistics, and citation hallucinations *before* submission — not to reassure the author.

## When to use

- Pre-submission audit for a journal (PRX, JCAP, JOSS, etc.) or conference.
- Internal circulation of a research report or technical memo.
- Response drafting for a revise-and-resubmit where the author wants to predict reviewer pushback.
- Any draft the user wants "torn apart" or "reviewed hard."

If the user wants a friendly copy-edit pass, this is the wrong skill — suggest a plain editing request instead.

## Inputs to confirm

Ask only for what is missing:
- path to the draft (default: `report.md` in the current directory)
- journal or venue the draft targets (affects the Journal Editor persona)
- any sections the user wants emphasized or skipped
- whether figures live alongside the draft and where (`plots/`, `figures/`, etc.)
- whether a bibliography file or a references section should be audited
- whether Korean translation of the final summary is expected

If nothing is specified, default to:
- draft: `report.md` in CWD
- venue: "general physics/ML journal" (Journal Editor persona stays generic)
- figures: `plots/` if present, else skip Figure Critic
- Korean translation: no, unless the user previously asked

## Core workflow

### 1. Locate and stage inputs

Before spawning any agents:

- Read the draft once end-to-end to understand the claim structure.
- Enumerate figure paths and bibliography entries.
- Produce a compact **context packet** that every persona will receive: draft path, venue, figure list, bibliography location, and any sections to emphasize or skip.

Do not let each persona re-read and re-summarize the whole draft from scratch — give them the packet plus the draft path.

### 2. Spawn personas in parallel

Spawn the persona subagents using the Agent tool, **in a single message** so they run concurrently. Use `references/personas.md` for the exact persona briefs; each persona gets:

- the context packet
- its own persona brief (role, what to attack, what to ignore)
- an output contract (see below)
- an explicit length cap so critiques do not bloat

Default persona set (skip any the draft does not support):

1. **Hostile Theorist** — attacks novelty; uses `reference-search` to surface prior art the draft may have missed.
2. **Experimentalist** — attacks reproducibility, missing ablations, undisclosed controls, hyperparameter sensitivity.
3. **Statistician** — attacks error bars, significance claims, baseline fairness, multiple-comparison exposure.
4. **Journal Editor** — predicts desk-reject reasons for the target venue; checks scope fit, framing, required sections.
5. **Citation Auditor** — verifies every non-trivial citation resolves to a real paper via `reference-search`; flags hallucinations and mischaracterizations.
6. **Figure Critic** — checks figure paths resolve, captions match the data, axes are consistent, cutoffs are applied uniformly, and no figure is referenced but missing.

### 3. Output contract (per persona)

Every persona must return a markdown block with this exact structure so the meta-editor can merge them deterministically:

```markdown
# <Persona Name>

## Severity-classified findings
- **DESK-REJECT**: <finding> — <evidence pointer: section/figure/citation>
- **MAJOR**: <finding> — <evidence pointer>
- **MINOR**: <finding> — <evidence pointer>

## Suggested defense / fix
- <action the author should take>

## Confidence
<high | medium | low> — <one sentence why>
```

Personas that find nothing at a severity level simply omit that bullet. Never fabricate findings to fill the template.

### 4. Meta-editor synthesis

After all personas return, run the meta-editor pass described in `references/meta-editor.md`. It:

- deduplicates overlapping critiques
- ranks by severity (DESK-REJECT > MAJOR > MINOR)
- attaches a proposed defense experiment or textual fix to every DESK-REJECT and MAJOR
- drops low-confidence findings that no other persona corroborates

Meta-editor output is the canonical `summary.md` the user reads first.

### 5. Write outputs

Write all artifacts under `outputs/review/<YYYYMMDD_HHMM>/` relative to the draft's directory, with the stamp taken from `date +%Y%m%d_%H%M`. Alphabetical order then equals chronological order across repeated reviews. Keep individual persona files alongside the synthesis so the user can trace any claim in `summary.md` back to its source.

```text
outputs/review/20260418_1430/
  summary.md                 # meta-editor synthesis — read this first
  hostile_theorist.md
  experimentalist.md
  statistician.md
  journal_editor.md
  citation_auditor.md
  figure_critic.md
  context_packet.md          # the packet given to every persona (for reproducibility)
```

### 6. Report and stop

Show the user the path to `summary.md`, the count of findings by severity, and the three highest-severity items inline. **Do not** start fixing the draft. The user decides which findings to act on.

## Integration

See `references/integration.md` for how this skill wires into the rest of the collection:

- `reference-search` is the citation and prior-art backbone for Hostile Theorist and Citation Auditor.
- `research-report` produces the `report.md` and figure layout this skill consumes; reports that follow its conventions are easiest to review.
- Korean translation of `summary.md` follows the user's standing convention when requested: a Sonnet subagent produces `summary_ko.md` next to the English file.

## Guardrails

- Never modify the draft. This skill is read-only with respect to the manuscript.
- Never silently skip a persona. If a persona cannot run (e.g. no figures to critique), say so in `summary.md` under "skipped".
- Never accept a persona output that invents findings not grounded in the draft, figures, or bibliography. If a persona returns unsupported claims, rerun that persona once with an explicit "ground every finding in a section, figure, or citation pointer" instruction; if it fails again, mark its section as unreliable in `summary.md`.
- Never fabricate a citation when checking citations. If `reference-search` returns nothing for a cited title, flag it as "not found via OpenAlex — manual verification required" rather than guessing.
- Never push the review outputs. Writing under `outputs/review/...` is fine; git operations are out of scope.

## Resources

- `references/personas.md` — the six persona briefs with role, attack surface, ignored concerns, and output contract.
- `references/meta-editor.md` — dedup, severity ranking, and defense-experiment authoring rules.
- `references/integration.md` — wiring notes for `reference-search`, `research-report`, and Korean translation.
