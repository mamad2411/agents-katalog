---
name: youtube-meta-research
description: Research the current public YouTube meta around a channel handle or URL, including peer and adjacent surfaces, breakout/outlier videos, search observations, topic/packaging/format patterns, and differentiated exploit/avoid/counter-position recommendations. Use for prompts like current YouTube meta, what is working now, find opportunities for @channel, breakout patterns, or what this channel should exploit or avoid.
type: research
version: v0.0
required_conventions: [alignment-page]
argument-hint: "<channel URL or @handle> [--count N] [--peer-limit N] [--query-limit N] [--window 30|90|180|365]"
context_intake: artifact_only
visual_tier: visual
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# YouTube Meta Research

Invoke as `$youtube-meta-research`.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, peer/search discovery limits, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, identify breakout patterns, rank opportunities, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, candidate surfaces, command availability, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language while waiting for scope or artifact approval. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, peer/search discovery limits, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the target channel, normalized slug, proposed public evidence sources, available repo evidence, planned peer and query discovery limits, transcript/comment/tool availability checks, owner-analytics boundary, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, identify meta patterns, rank opportunities, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-youtube-meta-research-research.md`; product-path mode uses `research/{slug}/_working/preliminary-youtube-meta-research-research.md`. Raw evidence, metadata captures, transcript files, and search logs may remain as supporting evidence, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page so it renders the complete working-packet substance as structured HTML review UI: purpose-built sections, tables, matrices, gates, cards, and tier-appropriate charts or diagrams that preserve every packet section, finding, caveat, and decision detail without summary loss. Raw Markdown packet text may appear only as a supplemental source view after the rendered review UI; do not make a raw Markdown dump, giant `<pre><code>` block, link-only view, or source-only view the primary review surface. Include the evidence matrix, search/query observation log, breakout/outlier table, assumptions/confidence register, private-data boundary, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifact to `research/youtube/meta-research-<slug>-YYYY-MM-DD.md`, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged after Stage 1 approval unless the user explicitly approves a path change.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Inputs

- Required: a YouTube channel URL, channel ID URL, custom URL, or `@handle`.
- Optional `--count N`: maximum recent videos per channel to inspect for baseline and peer samples. Default 30, max 100 unless the user approves more.
- Optional `--peer-limit N`: maximum peer/adjacent channels to include. Default 8, max 20 unless the user approves more.
- Optional `--query-limit N`: maximum YouTube search queries to observe. Default 12, max 30 unless the user approves more.
- Optional `--window 30|90|180|365`: recency window in days for breakout/outlier and current-meta analysis. Default 180.
- Optional user-supplied owner analytics paths: use only when explicitly provided by the user; never imply they are required.

## Process

1. Resolve the target channel handle or URL to a stable channel identity and normalized `<slug>` for filenames. If identity cannot be resolved without login or protected access, stop with the limitation and ask for a public URL or user-supplied artifact.
2. Inspect existing repo evidence before public collection: `research/youtube/channel-audit-<slug>.md`, `research/youtube/peer-benchmark-<slug>.md`, `research/youtube/search-positioning-<slug>.md`, `research/youtube/data/<slug>/`, and any user-provided artifacts named in the invocation.
3. Require `yt-dlp` for public channel/video metadata when public collection is approved:

   ```bash
   command -v yt-dlp
   ```

4. Select a transcript Python interpreter only when transcripts are needed for topic/format evidence. Prefer a workspace-local `.venv`; install `youtube-transcript-api` into `.venv` only when the import check fails and network access is available.
5. Persist raw public evidence where collection happens:
   - `research/youtube/data/<slug>/channel-metadata-YYYY-MM-DD.json`: target channel metadata when available.
   - `research/youtube/data/<slug>/videos-YYYY-MM-DD.jsonl`: target recent video metadata sample.
   - `research/youtube/data/<slug>/peers/<peer-slug>/videos-YYYY-MM-DD.jsonl`: peer or adjacent-channel samples.
   - `research/youtube/data/<slug>/search/search-observations-YYYY-MM-DD.md`: dated manual/tool-assisted query observations, including geography/account/personalization caveats.
   - `research/youtube/data/<slug>/transcripts/<video-id>.json`: transcript JSON only when available and needed.
6. Discover peer and adjacent surfaces from approved evidence: known peers, channels appearing in search results, channels linked by topic/category adjacency, repeated audience jobs, title/thumbnail promise overlap, and formats competing for the same viewer moment.
7. Detect breakout/outlier videos using public metadata only. Prefer relative signals over raw popularity: views/day versus channel baseline, view multiple versus recent median, unusually high comment/view or like/view when counts are public, recency-adjusted peer outliers, and repeated packaging/topic patterns across channels.
8. Build a query observation set from the target channel, recurring peer topics, breakout titles, audience jobs, and user seed terms. Date every search/ranking observation and state that results are personalized, geography-sensitive, account-sensitive, and unstable.
9. Extract current meta patterns:
   - Topics: repeated audience jobs, novelty frames, pain points, identities, trends, and recurring promises.
   - Packaging: title structures, thumbnail motifs, specificity, stakes, contrast, proof, curiosity, and expectation match.
   - Formats: length bands, pacing, structure, proof devices, collaboration, series design, Shorts/long-form relationship, and production complexity.
   - Cadence: upload frequency signals, series rhythm, event/timing hooks, and freshness expectations.
   - Discovery mode: search-led, browse-led, suggested-led, community-led, external-event-led, or mixed, with evidence strength.
10. Convert patterns into differentiated recommendations. Use `exploit` for credible opportunities the channel can own, `avoid` for saturated/derivative/low-fit moves, and `counter-position` for ways to win by opposing the visible meta.

## Output

Create the `research/youtube/` and supporting `research/youtube/data/<slug>/` directories if they do not exist.

Write the approved canonical artifact only in Stage 3:

```text
research/youtube/meta-research-<slug>-YYYY-MM-DD.md
```

Use this structure:

```markdown
# YouTube Meta Research - [Channel]

> Channel: [URL or handle]
> Date captured: YYYY-MM-DD
> Window: 30 / 90 / 180 / 365 days
> Peer limit: N
> Query limit: N
> Evidence: [raw paths used]

## Evidence Coverage And Capture Limits

| Source class | Captured | Path / note | Limits |
|---|---|---|---|
| Target channel metadata | Yes / No | ... | ... |
| Peer metadata | Yes / No | ... | ... |
| Search observations | Yes / No | ... | Personalized, dated observations |
| Transcripts | Yes / No / Partial | ... | Availability varies |
| Owner analytics | Provided / Not provided | ... | Never inferred from public evidence |

## Channel Baseline

[Public baseline: positioning, recent topics, formats, cadence, public performance distribution, and evidence caveats.]

## Peer And Adjacent Surface Map

| Surface | Why included | Evidence | Relationship to target |
|---|---|---|---|
| ... | ... | ... | peer / adjacent / search competitor / format competitor |

## Search / Query Observation Log

| Date | Query | Top observed results | Target presence | Caveats |
|---|---|---|---|---|
| ... | ... | ... | ... | geography/account/personalization |

## Breakout / Outlier Video Table

| Video | Channel | Published | Public signals | Outlier basis | Pattern evidence |
|---|---|---:|---|---|---|
| ... | ... | ... | views/day, comments, likes when public | vs baseline / peer / recency | ... |

## Current Meta Patterns

### Topics

[Observed topic patterns with evidence and confidence.]

### Packaging

[Observed title/thumbnail/framing patterns with evidence and confidence.]

### Formats

[Observed structure, length, pacing, and production patterns with evidence and confidence.]

### Cadence

[Observed cadence/timing patterns with evidence and confidence.]

### Discovery Mode

[Search/browse/suggested/community/external-event diagnosis with caveats.]

## Opportunity Map

| Recommendation | Type | Evidence | Why it fits or does not fit | Execution guardrail |
|---|---|---|---|---|
| ... | exploit / avoid / counter-position | ... | ... | ... |

## Recommended Next Content Moves

1. [Move] - [evidence, channel fit, and first execution step]
2. [Move] - [evidence, channel fit, and first execution step]
3. [Move] - [evidence, channel fit, and first execution step]

## Evidence Gaps And Private-Data Boundaries

[Missing public evidence, unavailable transcripts/comments, unstable search observations, and any private Studio metrics that would be needed to increase confidence.]
```

## Constraints

- Do not infer private YouTube Studio metrics, CTR, retention, revenue, subscriber conversion, profitability, traffic source mix, or audience demographics from public evidence.
- Do not bypass login walls, bot protections, access controls, private YouTube Studio data, paid tools, or any source that requires unauthorized access.
- Date every search/ranking observation and state personalization, geography, account state, language, device, and temporal caveats when known.
- Separate observed public evidence from performance hypotheses and strategic judgment.
- Do not invent metrics, transcript quotes, comments, thumbnail details, peer identities, or distribution causes.
- Do not recommend copying creators. Translate patterns into differentiated recommendations that fit the target channel's position, constraints, and audience.
- Archive existing canonical artifacts before replacing them under `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.

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
- Performance review: recommend metrics, cadence, portfolio, peer benchmark, owner-analytics export work, or meta refresh before new content planning.
- Owner analytics or private/manual platform evidence: route to an explicit manual/guide handoff instead of inventing unavailable metrics.
- Dirty intended artifacts: route to shipping/commit/handoff first, not another creator strategy skill.

Use the default next-skill sequence only when no stronger user intent, missing artifact, manual blocker, or dirty-artifact handoff applies.

## Next-Step Routing

After writing the artifact, recommend the next contextual creator-media skill in the final response as `Recommended next skill: <command>`.

Default recommendation: `$youtube-search-positioning` when the opportunity map depends on query capture, otherwise `$content-programming` when programming or series decisions are the next bottleneck.

If the default successor already exists and is current, recommend the first missing or stale downstream creator-media artifact in this order:

`$youtube-channel-audit` -> `$youtube-peer-benchmark` -> `$youtube-search-positioning` -> `$youtube-cadence-diagnosis` -> `$creator-positioning` -> `$content-programming` -> `$series-spec` -> `$product-led-media-map` -> `$creator-metrics-review`

If the sequence is ambiguous, multiple upstream artifacts are stale, or the recommendation depends on channel-level strategy vs programming-level changes, recommend `$creator-metrics-review` when metrics evidence exists, otherwise recommend `$content-programming` and explain the missing artifact.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/youtube-meta-research-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
