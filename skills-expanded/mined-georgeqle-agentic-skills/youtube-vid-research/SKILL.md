---
name: youtube-vid-research
description: Research one or more external YouTube videos for context, claims, structure, examples, terminology, and transferable takeaways
type: research
version: v0.5
argument-hint: "<video URL or ID...> [--focus context|claims|summary|references] [--compare-channel <slug>]"
interview_depth: none
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` instead of the target skill. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# YouTube Video Research

Invoke as `$youtube-vid-research`.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page with the full preliminary packet, evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Inputs

- Required: one or more YouTube video URLs or video IDs.
- Optional `--focus context|claims|summary|references`: default `context`.
- Optional `--compare-channel <slug>`: reuse channel evidence under `research/youtube/data/<slug>/` when the user asks how the reference relates to a known channel.

## Process

1. Resolve every target into a video ID from watch URLs, Shorts URLs, youtu.be URLs, embed URLs, or raw 11-character IDs.
2. Require `yt-dlp` for public metadata:

   ```bash
   command -v yt-dlp
   ```

3. Select a transcript Python interpreter. Prefer a workspace-local `.venv`; create it if missing. Install `youtube-transcript-api` into `.venv` only when the import check fails and network access is available.
4. Persist raw evidence before analysis under `research/youtube/data/<video-id>/`:
   - `metadata-YYYY-MM-DD.json`: raw `yt-dlp --dump-json "VIDEO_URL"` output.
   - `transcript/<video-id>.json`: raw transcript JSON when available.
   - `transcript/transcript-summary.json`: transcript text or failure reason.
5. Extract public metadata fields when present: title, URL, channel, upload date, duration, description, chapters, tags, categories, thumbnails, view count, like count, and comment count.
6. Analyze the video for:
   - Main thesis, audience, context, and assumed prior knowledge.
   - Key claims, examples, frameworks, named entities, tools, sources, and references.
   - Narrative structure: hook, setup, sections, payoff, and CTA.
   - User-relevant takeaways: what matters for the current project, idea, spec, or decision.
   - Uncertainties and evidence gaps.
7. If multiple videos were supplied, synthesize common themes, contradictions, and how each video contributes distinct context.

## Output

Create the `research/youtube/` and `research/youtube/data/<video-id>/` directories if they do not exist.

Write:

```text
research/youtube/video-research-<video-id-or-slug>-YYYY-MM-DD.md
```

Use this structure:

```markdown
# YouTube Video Research - [Title or Video Set]

> Videos: [URLs]
> Date captured: YYYY-MM-DD
> Evidence: [raw paths used]
> Focus: context / claims / summary / references

## Evidence Coverage

| Video | Public metadata | Transcript | Notes |
|---|---|---|---|
| [Title](URL) | Available / Missing | Available / Missing | ... |

## Context Brief

[What this video is about, who it is for, and why it matters to the user's request.]

## Key Claims And Examples

| Claim / Idea | Evidence | Confidence | Relevance |
|---|---|---|---|
| ... | metadata/transcript/chapter reference | High / Medium / Low | ... |

## Structure Notes

- **Hook**: ...
- **Sections**: ...
- **Payoff**: ...
- **CTA / next action**: ...

## Terms, References, And Source Leads

[Named people, companies, tools, papers, links, topics, or source leads surfaced by the video.]

## Transferable Takeaways

[What the user or downstream agent should carry forward.]

## Open Questions And Evidence Gaps

[Missing transcript, unclear claims, unavailable references, or claims needing independent verification.]
```

## Constraints

- Do not invent transcript quotes, links, references, comments, metrics, or visual details.
- Mark missing transcript or metadata explicitly.
- Do not treat a single external video as proof of a market, trend, or channel pattern.
- When a claim affects factual, legal, medical, financial, or current-event accuracy, recommend independent source verification instead of relying only on the video.
- Do not bypass login walls, bot protections, access controls, or private YouTube Studio data.
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
- Performance review: recommend metrics, cadence, portfolio, peer benchmark, or owner-analytics export work before new content planning.
- Owner analytics or private/manual platform evidence: route to an explicit manual/guide handoff instead of inventing unavailable metrics.
- Dirty intended artifacts: route to shipping/commit/handoff first, not another creator strategy skill.

Use the default next-skill sequence only when no stronger user intent, missing artifact, manual blocker, or dirty-artifact handoff applies.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/youtube-vid-research-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
