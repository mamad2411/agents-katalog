---
name: nature-workflow
description: Use when the user explicitly asks for Nature Skills, nature-skills, Nature style, Nature-style, Nature Communications, Nature-family, CNS, high-impact journal, or Springer Nature workflows, including Nature figure work, polishing, writing, reviewer critique, high-impact journal major revision response, Nature/CNS citations, Nature data-sharing workflows, paper readers, reviewer response, paper-to-PPT, submission checklist, or Nature-specific academic-search workflows.
---

# Nature Workflow Bridge

This skill is a bridge to the upstream `nature-skills` bundle, not a simplified
clone of it. Its job is to route the user's request to the right original
`nature-*` skill when that skill is installed or otherwise available, and to
fall back to ScholarAIO's existing skills only when the original upstream skill
cannot be used in the current host.

## Direct-Use Policy

Use the original upstream nature-* skill directly whenever it is available. Do
not emulate, summarize, or partially rewrite upstream behavior from this bridge.
Do not copy only SKILL.md from upstream; direct use requires the whole skill
directory, including `manifest.yaml`, `static/`, `references/`, scripts, assets,
and `skills/_shared` when the upstream skill references it.

If the upstream skill is unavailable, say so, then use the ScholarAIO fallback
route from `references/upstream-skill-map.md`. Mark the output as a ScholarAIO
fallback, not as an upstream-equivalent Nature Skills result.

## Reference Loading

Load only what the current request needs:

- `references/upstream-skill-map.md`: load for routing decisions or when the
  request could match more than one upstream skill.
- `references/bridge-policy.md`: load when installation, direct-use behavior,
  upstream fidelity, or fallback limitations matter.
- `references/upstream-install.md`: load when the user needs the original
  upstream `nature-*` skills installed or asks whether this bridge is a
  simplified local copy.
- `references/quickstart.md`: load when the user asks how to use the bridge or
  wants example prompts.

## First Pass

Classify the request before doing work:

1. **Upstream target**: one or more of `nature-figure`, `nature-polishing`,
   `nature-writing`, `nature-reviewer`, `nature-citation`, `nature-data`,
   `nature-reader`, `nature-response`, `nature-paper2ppt`, or
   `nature-academic-search`.
2. **Availability**: original upstream skill available, installed through a
   plugin/local skill path, or unavailable.
3. **ScholarAIO fallback**: only if upstream cannot be used.
4. **Evidence state**: manuscript/text/PDF/figures/comments/data/references
   supplied, workspace available, or missing inputs.

State the upstream target and whether direct upstream use is available before
doing substantial work.

## Route Table

| User intent | Primary route |
|-------------|---------------|
| Nature/high-impact scientific figure, publication plot, manuscript figure, figures4papers-style output | `nature-figure` |
| Nature-style polishing, manuscript prose polish, Chinese-to-English academic polish | `nature-polishing` |
| Draft/rebuild abstract, introduction, methods, experiments, discussion, conclusion, title, or manuscript argument | `nature-writing` |
| Pre-submission reviewer critique, mock peer review, Nature-style reviewer report | `nature-reviewer` |
| Nature/CNS citation support, claim-to-reference mapping, reference-manager export | `nature-citation` |
| Data Availability, repository plan, FAIR metadata, accession/DOI/source-data/code availability | `nature-data` |
| Full-paper bilingual reader, source-grounded Markdown reader, paper translation/reading | `nature-reader` |
| Reviewer comments, rebuttal, point-by-point response letter, major/minor revision response | `nature-response` |
| Paper-to-PPT, Chinese journal-club PPTX, group meeting deck from a paper | `nature-paper2ppt` |
| Multi-source literature search, citation verification, MeSH/search strategy, citation-file management | `nature-academic-search` |

Submission package is only one scenario. Do not require a full submission
package when the user asks only for polishing, figures, reading, PPT, citation
support, reviewer critique, Data Availability, response, or search.

## ScholarAIO Fallbacks

When the original upstream skill is not available:

- figure work -> `/draw`
- prose polish -> `/writing-polish`
- manuscript writing -> `/paper-writing`
- reviewer response -> `/review-response`
- citation/search/export -> `/search` + `/citation-check` + `/export`
- paper reading/translation -> `/show` + `/translate`
- paper-to-PPT or document packaging -> `/document`
- literature search -> `/search`, plus host-native web search when current or external coverage is required

Use fallbacks conservatively. Preserve upstream-style guardrails such as
non-invention, source grounding, explicit missing inputs, and final-output
verification, but do not claim to have executed the original upstream workflow
unless the original skill was actually used.

## Output Shape

For routing tasks, return:

1. `Upstream target:` selected `nature-*` skill or skill sequence.
2. `Mode:` direct upstream use or ScholarAIO fallback.
3. `Route:` exact skill sequence.
4. `Immediate next action:` file to inspect, command to run, or question to ask.
5. `Guardrails:` only the relevant non-invention, source-grounding, or
   verification constraints for this request.
