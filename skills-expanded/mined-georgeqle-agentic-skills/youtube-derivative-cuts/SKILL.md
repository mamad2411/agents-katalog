---
name: youtube-derivative-cuts
description: Plan a prioritized derivative content slate from one long YouTube source video using metadata, transcript, chapters, audits, portfolio evidence, and available metrics
type: research
version: v0.0
argument-hint: "<video URL | video ID | source audit path> [--audit <path>] [--portfolio <path>] [--metrics <path>] [--transcript <path>] [--chapters <path>] [--max-shorts N]"
context_intake: artifact_only
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# YouTube Derivative Cuts

Invoke as `$youtube-derivative-cuts`.

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

- Required: one YouTube video URL, raw video ID, or existing source audit path such as `research/youtube/video-audit-<video-id>-YYYY-MM-DD.md` or `research/youtube/prelaunch-audit-<video-id>-YYYY-MM-DD.md`.
- Optional `--audit <path>`: source video audit, prelaunch audit, video research artifact, or channel audit that contains useful evidence.
- Optional `--portfolio <path>`: channel portfolio, content-programming, series, or product-media map evidence.
- Optional `--metrics <path>`: owner-provided analytics, creator metrics review, public performance export, or manually captured metrics artifact.
- Optional `--transcript <path>`: transcript JSON, text, SRT/VTT, or transcript summary.
- Optional `--chapters <path>`: chapter metadata, outline, timestamps, or chaptered source artifact.
- Optional `--max-shorts N`: maximum Shorts to recommend. Default 5. Keep the default release plan at 3-5 Shorts unless evidence supports fewer.

## Process

### 1. Resolve Source And Evidence

1. Extract the video ID from a normal watch URL, Shorts URL, youtu.be URL, embed URL, raw 11-character ID, or source audit filename/content.
2. Inspect existing local evidence before fetching or asking for more:
   - `research/youtube/video-audit-<video-id>-*.md`
   - `research/youtube/prelaunch-audit-<video-id>-*.md`
   - `research/youtube/vid-research-*.md`
   - `research/youtube/data/<video-id>/metadata-*.json`
   - `research/youtube/data/<video-id>/transcript/`
   - portfolio, programming, metrics, and creator evidence supplied by path.
3. Use `yt-dlp` or transcript tooling only when existing artifacts are insufficient and the source is publicly accessible or user-authorized. Do not bypass login walls, bot protections, access controls, or YouTube Studio UI restrictions.
4. Record every missing audit, transcript, chapter, analytics, portfolio, or metric source as an evidence gap. Do not invent unsupported quotes, timestamps, performance metrics, audience response, or retention claims.

### 2. Build The Cut Candidate Set

Separate two derivative types:

- **Companion clips**: horizontal or long-ish excerpts that can stand alone as a focused companion to the source video. Use when the idea needs context, technical nuance, or more than Shorts duration.
- **Shorts**: vertical short-form candidates with one crisp premise, fast payoff, and enough context to avoid misleading the viewer.

Prefer candidates that satisfy all of these:

- Clean thought boundaries with a clear beginning, middle, and payoff.
- Defensible context, so the cut does not distort the source argument.
- Trim-only feasibility, where the segment can work without a new shoot, heavy re-edit, or invented connective tissue.
- Clear source-video linkage, so every derivative can point viewers back to the full video.
- Audience job clarity: acquisition, trust-building, education, proof, launch support, community, or cleanup/repositioning.
- Human-reviewable risk: quote sensitivity, missing setup, outdated claim, product promise risk, sponsor/disclosure issue, or visual/audio concern.

Each candidate must include:

| Handle | Required detail |
| --- | --- |
| Cut type | Companion clip or Short |
| Timestamp start/end | Exact timestamp when available; otherwise estimated timestamp with gap note |
| Estimated duration | Duration in seconds or minutes |
| Quote/topic boundary | The opening and closing idea boundary, not a fabricated quote |
| Rationale | Why this segment earns a separate derivative asset |
| Expected audience job | What viewer job it serves |
| Packaging angle | Standalone title/hook direction |
| Risk | Context, accuracy, rights, production, or audience risk |
| Required human check | What the creator/editor must inspect before publishing |

### 3. Prioritize The Slate

Prioritize candidates by:

1. Source-video strategic role and likely long-form linkage.
2. Strength of standalone idea.
3. Fit for companion clip vs Short format.
4. Evidence from transcript, chapters, audits, comments, retention, portfolio gaps, or metrics.
5. Production feasibility using trim-only or light assembly.
6. Risk and required human review.

Default release plan:

1. Publish one companion clip first when a self-contained companion segment exists.
2. Publish 3-5 Shorts from the strongest clean boundaries.
3. Pause for checkpoint review before programming more cuts from the same source.

If evidence supports no companion clip or fewer than 3 Shorts, say so and explain the evidence gap or quality constraint.

### 4. Package Within Scope

For each selected cut, draft:

- 2-3 standalone title options.
- First-line hook or on-screen opening copy.
- Short description or caption.
- Source-video link line and linkage rationale.
- Playlist or series fit when visible from portfolio/programming evidence.

This skill does not design thumbnails, create vertical edits, edit captions, upload, schedule, or finalize upload-ready descriptions. Hand off thumbnail design and Test and Compare packaging to `youtube-title-thumbnail-audit`; hand off upload-ready description optimization, link stacks, tags, and final metadata polish to `youtube-description-optimizer`.

### 5. Measurement Scope

Plan measurement for the slate, not only individual cuts. Track:

- Views by derivative asset.
- Subscribers gained and lost.
- Comments and comment themes.
- Returning viewers where available.
- Audience retention or average view duration where available.
- Long-form spillover back to the source video.
- Source-video traffic from derivative assets.
- Series-level learning: what idea, packaging angle, or audience job should repeat or stop.

Explicitly state that Shorts views alone are insufficient success evidence. A strong derivative plan needs linkage, retention, audience quality, and long-form spillover signals where available.

## Output

Create `research/youtube/` if it does not exist.

Save the approved canonical artifact to:

```text
research/youtube/derivative-cuts-<video-id>-YYYY-MM-DD.md
```

Use this structure:

```markdown
# YouTube Derivative Cuts - [Source Title]

> Source video: [URL or path]
> Video ID: [id]
> Source artifact: [path or not provided]
> Date captured: YYYY-MM-DD
> Transcript/chapters: [paths or evidence gaps]
> Metrics/portfolio evidence: [paths or evidence gaps]

## Source Intake

[Source identity, strategic role, target audience/job, and source-video linkage assumptions.]

## Evidence Coverage

| Evidence | Status | Path or gap | Use in cut planning |
|---|---|---|---|
| Metadata | Available / Missing | ... | ... |
| Transcript | Available / Missing | ... | ... |
| Chapters | Available / Missing | ... | ... |
| Source audit | Available / Missing | ... | ... |
| Portfolio/programming evidence | Available / Missing | ... | ... |
| Metrics/analytics | Available / Missing | ... | ... |

## Cut Candidates

| ID | Type | Start | End | Est. duration | Quote/topic boundary | Rationale | Audience job | Risk | Required human check |
|---|---|---:|---:|---:|---|---|---|---|---|
| C1 | Companion clip / Short | ... | ... | ... | ... | ... | ... | ... | ... |

## Priority Order

1. [Candidate ID and title] - [why first]
2. [Candidate ID and title] - [why next]

## Packaging Notes

### [Candidate ID]

- **Title options**:
  1. ...
  2. ...
  3. ...
- **First-line hook**: ...
- **Short description/caption**: ...
- **Source-video link**: ...
- **Thumbnail handoff**: ...
- **Description optimization handoff**: ...

## Publish Sequence

| Sequence | Asset | Timing | Why now | Dependency | Human check |
|---|---|---|---|---|---|
| 1 | Companion clip | First | ... | ... | ... |
| 2 | Short 1 | After companion | ... | ... | ... |

## Checkpoint Review

[What to review after the companion clip and first 3-5 Shorts before making more cuts.]

## Measurement Plan

| Signal | Where to check | Why it matters | Decision it informs |
|---|---|---|---|
| Views | ... | Reach only; insufficient alone | ... |
| Subscribers gained/lost | ... | Audience quality | ... |
| Comments | ... | Viewer job and objections | ... |
| Returning viewers | ... | Fit with existing audience | ... |
| Retention/AVD | ... | Hook and payoff quality | ... |
| Long-form spillover | ... | Source-video linkage | ... |
| Source-video traffic | ... | Derivative-to-source conversion | ... |
| Series learning | ... | Repeat/stop decision | ... |

## Handoffs

- Thumbnail and packaging visual review: `youtube-title-thumbnail-audit`.
- Upload-ready description, link stack, tags, and final metadata polish: `youtube-description-optimizer`.
- Editing, captions, upload, and scheduling: human/editor workflow outside this skill.
```

## Summarize In Thread

After saving an approved artifact, report:

- Source video and evidence coverage.
- Recommended companion clip if any.
- Recommended Shorts count and top 3 Shorts.
- Default publish sequence.
- Highest-risk human check.
- Measurement plan headline, including why Shorts views alone are insufficient.
- Artifact and alignment page paths.

## Constraints

- This is a programming and planning artifact, not an editing plan, thumbnail design artifact, upload automation, scheduling action, or full metadata optimization pass.
- Do not fabricate timestamps, transcript quotes, retention data, comments, viewer intent, source-video traffic, or performance claims.
- Keep companion clips separate from Shorts in candidates, priority order, publish sequence, and measurement.
- Prefer fewer strong cuts over filling a quota with weak or context-poor clips.
- Missing analytics, transcripts, chapters, or audits are evidence gaps, not permission to invent unsupported claims.
- Keep recommendations practical for trim-only or light-assembly feasibility unless the user explicitly asks for deeper editing work.

## Approved Artifact Handoff

After an approved synthesized write, explicit write/update mode, or any direct artifact mutation:

- List every created or updated synthesized artifact path in the final response.
- State the verification performed, such as readback, schema/check command, or why no executable verification applies for a Markdown-only strategy artifact.
- Check and report the relevant git status for intended artifacts when the project is a git repository. If intended artifacts are modified or untracked, make the next action shipping, committing, or an explicit dirty-artifact handoff before recommending downstream strategy work.
- Do not imply the research workflow is complete while approved artifacts remain untracked or uncommitted unless the user explicitly asked not to ship.
- If stopping for approval before writing, the approval request remains the next action; do not include downstream routing.

## Intent-Aware Routing

Before applying the default `## Next-Step Routing` sequence, classify the user's immediate intent and route to the missing action that best serves that intent:

- Derivative slate planning: use this skill for clips, Shorts from this video, derivative cuts, repurposing a long video, and publish-sequence planning.
- Packaging: route thumbnail or Test and Compare questions to `$youtube-title-thumbnail-audit`.
- Upload prep: route upload-ready description, tags, links, and final metadata polish to `$youtube-description-optimizer`.
- Editing or production execution: route to human/editor workflow or `youtube-format-research` when the installed pack context supports format work.
- Performance review: route to `$youtube-video-audit` or `$creator-metrics-review` when the user asks how published derivatives performed.
- Dirty intended artifacts: route to shipping/commit/handoff first, not another creator strategy skill.

## Next-Step Routing

After writing the approved artifact and completing artifact handoff checks, recommend the most relevant next skill:

- Default: `Recommended next skill: $youtube-title-thumbnail-audit`
- If thumbnail/title packaging has already been handled and description polish is the next needed work: `Recommended next skill: $youtube-description-optimizer`
- If derivatives are already published and performance evidence exists: `Recommended next skill: $creator-metrics-review`

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/youtube-derivative-cuts-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
