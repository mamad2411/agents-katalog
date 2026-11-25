---
name: profile-content
description: Campaign content profile standards for audience insight, single-minded message, voice, proof, and CTA measurement.
---

# Profile content

Serves: content — R2.4, R2.6, R2.7

## Core method

- Name a behavioral audience segment and the insight or tension the work resolves. Source: skills/creative-brief/SKILL.md
- Set one proposition with no more than three supporting reasons, each backed by proof. Source: skills/creative-brief/SKILL.md
- Define brand voice, run-language register, one primary CTA, its destination, and its measurement event. Source: skills/creative-brief/SKILL.md

## Definition of done

The content names a segment and insight, uses one proposition with up to three proven supports, specifies voice and run-language register, and has one measured primary CTA with destination.

## Rubric

- `audience` — pass when a named segment and insight are present; evidence: audience and insight lines with source.
- `message` — pass when one proposition has no more than three supports with proof; evidence: message and proof table.
- `voice` — pass when brand voice and the register for the run language are stated; evidence: voice guide and language note.
- `cta` — pass when one primary CTA has a destination and measurement method; evidence: CTA line and event definition.

## Default skills

Load `creative-brief` with the Skill tool when installed. If it is missing, resolve the facet through `codex-flow:skill-selection` (LOAD/VET/AUTHOR); never proceed without a verdict. Embed only distilled blocks into the executor prompt.

## Evidence

When evidenceMode is not `off`, every number follows evidence v2 as in codex-flow:profile-pilot: use anchors and a manifest, and have claims cite figures. Measured numbers come from their data source. Designed rates, targets, prices, and capacities live in a parameters file next to the deliverable, such as `params.csv`; figure/table commands READ that file. A command that echoes its own constant is forbidden. With evidence `off`, apply the `exec-deliverable` Verification block.

## Sampling

When evidence is not off, sample 3 figure-backed claims with `--sample 3 --seed <task number>` for the owner in one AskUserQuestion, as codex-flow:profile-pilot describes. A claim marked wrong is a finding.

## Failure modes

- Do not accept demographic targeting without a behavioral insight, or multiple competing propositions. Source: skills/creative-brief/SKILL.md
- Do not accept unsupported claims, vague voice, or a CTA without a destination and measure. Source: skills/creative-brief/SKILL.md

## Reviewer checklist

- Confirm the audience tension and proof are sourced, not invented. Source: skills/creative-brief/SKILL.md
- Check one proposition, voice/register, mandatories, and CTA measurement. Source: skills/creative-brief/SKILL.md
- Check each rubric item pass/fail with evidence in reviews.md. derived, unverified

## Provenance

- Brief, insight, proposition, voice, and CTA rules: Source: skills/creative-brief/SKILL.md
- Evidence and rubric integration: Source: skills/profile-pilot/SKILL.md
