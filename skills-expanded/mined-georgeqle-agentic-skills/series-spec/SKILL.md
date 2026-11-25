---
name: series-spec
description: Specify a repeatable YouTube series format with audience job, episode shape, evidence requirements, packaging rules, and success metrics
type: planning
version: v0.1
argument-hint: "<series idea or programming path>"
---

# Series Spec

Invoke as `$series-spec`.

Define a repeatable series format that can be produced consistently. Use this for founder updates, interviews, teardown series, recurring shows such as WeeklyG or WeeklySOTA, and product-led education series.

## Inputs

- Prefer `research/youtube/content-programming-<slug>.md` and `creator-positioning-<slug>.md`.
- Read relevant audit, portfolio, peer benchmark, and product-led media map artifacts.

## Output

Create the `specs/youtube/` directory if it does not exist.

Write `specs/youtube/series-<slug>.md` with:

- Series promise and target viewer.
- Viewer job and expected transformation.
- Episode format: opening, proof, body segments, CTA, and outro.
- Packaging rules: title patterns, thumbnail promise, description structure, chapter style.
- Evidence requirements: sources, demos, product artifacts, examples, or guest proof.
- Production constraints: length range, cadence, preparation burden, editing complexity.
- Metrics: leading indicators, lagging indicators, and stop/iterate thresholds.
- Example episode briefs, not full scripts.

## Approved Artifact Handoff

After an approved synthesized write, explicit write/update mode, or any direct artifact mutation:

- List every created or updated synthesized artifact path in the final response.
- State the verification performed, such as readback, schema/check command, or why no executable verification applies for a Markdown-only strategy artifact.
- Check and report the relevant git status for intended artifacts when the project is a git repository. If intended artifacts are modified or untracked, make the next action shipping, committing, or an explicit dirty-artifact handoff before recommending downstream strategy work.
- Do not imply the research workflow is complete while approved artifacts remain untracked or uncommitted unless the user explicitly asked not to ship.
- If stopping for approval before writing, the approval request remains the next action; do not include downstream routing.

## Intent-Aware Routing

Before applying the default `## Next-Skill Routing` sequence, classify the user's immediate intent and route to the missing action that best serves that intent:

- Strategy refresh: recommend the missing or stale positioning, programming, portfolio, metrics, or product-media artifact.
- Recording prep: recommend the missing series spec, script, build proof, walkthrough guide, or validation artifact needed before recording.
- Upload prep: recommend packaging, title/thumbnail, description, chapters, or final metadata work before broader strategy work.
- Performance review: recommend metrics, cadence, portfolio, peer benchmark, or owner-analytics export work before new content planning.
- Owner analytics or private/manual platform evidence: route to an explicit manual/guide handoff instead of inventing unavailable metrics.
- Dirty intended artifacts: route to shipping/commit/handoff first, not another creator strategy skill.

Use the default next-skill sequence only when no stronger user intent, missing artifact, manual blocker, or dirty-artifact handoff applies.

## Alignment Page

Follow the shared Alignment Page convention in CLAUDE.md. Output: `alignment/series-spec-{topic}.html`.

## Constraints

- Do not write scripts unless explicitly asked.
- Keep the series format reusable; one-off video ideas do not qualify.
- If the series depends on a product, tie claims to actual product evidence.
