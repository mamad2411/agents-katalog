---
name: youtube-title-thumbnail-audit
description: Audit YouTube titles and thumbnails against channel performance and peer packaging patterns
type: research
version: v0.6
required_conventions: [alignment-page]
argument-hint: "<channel slug or handle> [--peer <channel>...] [--count N]"
context_intake: artifact_only
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# YouTube Title Thumbnail Audit

Invoke as `$youtube-title-thumbnail-audit`.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page so it renders the complete working-packet substance as structured HTML review UI: purpose-built sections, tables, matrices, gates, cards, and tier-appropriate charts or diagrams that preserve every packet section, finding, caveat, and decision detail without summary loss. Raw Markdown packet text may appear only as a supplemental source view after the rendered review UI; do not make a `Full Preliminary Packet` or `Full Working Packet` raw Markdown dump, giant `<pre><code>` block, link-only view, or source-only view the primary review surface. Include the evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Inputs

- `research/youtube/channel-audit-<slug>.md`
- `research/youtube/data/<slug>/videos-*.jsonl`
- Optional `research/youtube/peer-benchmark-<slug>.md`
- Optional peer raw metadata under `research/youtube/data/<peer-slug>/`

## Process

1. Require a channel slug, handle, or channel audit path.
2. Ensure current channel evidence exists. If not, run `$youtube-channel-audit <channel> [--count N]`.
3. When peers are provided, ensure comparable peer benchmark or raw peer metadata exists.
4. Pull thumbnail URLs or local thumbnail files from raw `yt-dlp` metadata when available. If thumbnails are missing, fetch them through the existing `$youtube-audit` evidence path rather than inventing visual details.
5. Score each title for length, keyword clarity, specificity, curiosity pattern, series fit, and avoidable redundancy.
6. Classify thumbnail patterns: text density, face presence, product screenshot presence, logo count, background style, contrast, focal clarity, and channel-template consistency.
7. Correlate packaging features with views, views/day, upload age, and content role.
8. Produce exactly 3 title+thumbnail combinations for YouTube's **Test and Compare** feature. Each combination is a paired title and thumbnail concept designed to run simultaneously — YouTube rotates all 3 across real viewers and measures watch-time-per-impression over up to 2 weeks to surface a winner. Do not frame these as "pick one and swap later"; all 3 upload at the same time. Each combo should test a distinct packaging hypothesis (e.g., search-led vs. curiosity-hook vs. feature-led) while staying within the channel's visual identity.
9. Write `research/youtube/title-thumbnail-audit-<slug>.md`.

Create the `research/youtube/` directory if it does not exist.

## Report Sections

- Evidence coverage: videos scored, thumbnail availability, peer coverage, and missing fields.
- Packaging performance table: title, views, views/day, title pattern, thumbnail pattern, and recommendation.
- Title diagnosis: recurring strengths, overlong patterns, keyword loading, unclear promises, and examples to keep.
- Thumbnail diagnosis: visual templates, consistency gaps, high-performing motifs, low-performing motifs, and peer contrasts.
- Channel identity impact: whether packaging creates a coherent channel signal.
- Existing-video fixes: prioritized title and thumbnail refresh candidates with expected rationale.
- Future templates: 3-5 repeatable title/thumbnail patterns mapped to content roles.
- Test and Compare combos: exactly 3 title+thumbnail combinations ready for YouTube's native A/B testing. Each combo includes a full title, thumbnail concept description, packaging hypothesis, and what signal a win for that variant would confirm about the channel's audience. Present these as simultaneous uploads, not sequential swaps.
- Strategic packaging recommendation: which combo to watch most closely and what to do after Test and Compare declares a winner.

## Constraints

- Cite source metadata paths and video IDs.
- Do not claim visual features unless thumbnail evidence was inspected or unavailable status is explicit.
- Do not recommend copying peer faces, branding, or trade dress; translate peer evidence into differentiated templates.
- Keep recommendations practical for the creator's apparent production capacity.
- Route follow-up cleanup decisions to `$youtube-portfolio` and future-topic decisions to `$youtube-search-positioning` or `$content-programming`.

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

## Next-Step Routing

After writing the artifact, recommend the next contextual creator-media skill in the final response as `Recommended next skill: <command>`.

Default recommendation: `$youtube-description-optimizer`.

If the default successor already exists and is current, recommend the first missing or stale downstream creator-media artifact in this order:

`$youtube-channel-audit` -> `$youtube-video-audit` -> `$youtube-vid-research` -> `$youtube-concept-research` -> `$youtube-competitive-research` -> `$youtube-title-thumbnail-audit` -> `$youtube-description-optimizer` -> `$youtube-portfolio` -> `$youtube-peer-benchmark` -> `$youtube-search-positioning` -> `$youtube-cadence-diagnosis` -> `$creator-positioning` -> `$content-programming` -> `$series-spec` -> `$product-led-media-map` -> `$creator-metrics-review`

If the sequence is ambiguous, multiple upstream artifacts are stale, or the recommendation depends on channel-level strategy vs programming-level changes, recommend `$creator-metrics-review` when metrics evidence exists, otherwise recommend the default successor and explain the missing artifact.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/youtube-title-thumbnail-audit-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
