---
name: youtube-competitive-research
description: Analyze why an external YouTube video performed well and extract evidence-backed competitive lessons, positioning gaps, and adaptation opportunities
type: research
version: v0.5
argument-hint: "<video URL or ID...> [--primary-channel <slug>] [--comments N] [--angle packaging|topic|retention|positioning]"
interview_depth: none
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` instead of the target skill. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# YouTube Competitive Research

Invoke as `$youtube-competitive-research`.

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
- Optional `--primary-channel <slug>`: compare the lessons against existing evidence for the user's channel under `research/youtube/data/<slug>/`.
- Optional `--comments N`: fetch up to N public top-level comments when public comment tooling/API access is available. Default 50, max 200.
- Optional `--angle packaging|topic|retention|positioning`: default is to cover all four.

## Process

1. Resolve every target into a video ID from watch URLs, Shorts URLs, youtu.be URLs, embed URLs, or raw 11-character IDs.
2. Require `yt-dlp` for public metadata:

   ```bash
   command -v yt-dlp
   ```

3. Select a transcript Python interpreter. Prefer a workspace-local `.venv`; create it if missing. Install `youtube-transcript-api` into `.venv` only when the import check fails and network access is available.
4. Persist raw evidence under `research/youtube/data/<video-id>/`:
   - `metadata-YYYY-MM-DD.json`: raw `yt-dlp --dump-json "VIDEO_URL"` output.
   - `transcript/<video-id>.json`: raw transcript JSON when available.
   - `transcript/transcript-summary.json`: transcript text or failure reason.
   - `api/comment-threads-YYYY-MM-DD.json`: optional public comments when an already-authorized API path is available.
5. Extract performance signals from public metadata when present: views, likes, comments, age, views/day, duration, views/minute, title, thumbnail URLs, description, tags, chapters, upload timing, and channel identity.
6. Analyze:
   - Performance hypothesis: why the video likely earned attention relative to public evidence.
   - Audience job: the problem, desire, identity, fear, or curiosity the video served.
   - Packaging: title, thumbnail, topic framing, specificity, novelty, and expectation match.
   - Content/retention drivers: hook, pacing, proof, examples, conflict, payoff, structure, and CTA.
   - Distribution context: timing, trend fit, search demand, collaboration, controversy, community, or platform format signals when evidence supports them.
   - Comment themes only when comments were captured; separate praise, objections, confusion, requests, and spam/noise.
   - Adaptation opportunities for the user's channel, product, or content strategy.
7. If a primary channel slug is supplied, compare against the user's existing raw channel evidence and state what the competitor proves that the primary channel does not yet prove.

## Output

Create the `research/youtube/` and `research/youtube/data/<video-id>/` directories if they do not exist.

Write:

```text
research/youtube/competitive-research-<video-id-or-slug>-YYYY-MM-DD.md
```

Use this structure:

```markdown
# YouTube Competitive Research - [Title or Video Set]

> Videos: [URLs]
> Primary channel: [slug or not provided]
> Date captured: YYYY-MM-DD
> Evidence: [raw paths used]
> Angle: packaging / topic / retention / positioning / all

## Evidence Coverage

| Video | Metadata | Transcript | Comments | Primary-channel comparison |
|---|---|---|---|---|
| [Title](URL) | Available / Missing | Available / Missing | Available / Missing / Not requested | Available / Not provided |

## Performance Snapshot

| Video | Published | Duration | Views | Likes | Comments | Views/day | Views/min |
|---|---|---:|---:|---:|---:|---:|---:|
| ... | ... | ... | ... | ... | ... | ... | ... |

## Why It Likely Worked

1. [Hypothesis] - [evidence]
2. [Hypothesis] - [evidence]
3. [Hypothesis] - [evidence]

## Audience Job And Positioning

[Audience need, competitor promise, category wedge, and emotional or practical trigger.]

## Packaging And Retention Lessons

- **Title / thumbnail promise**: ...
- **Topic timing / novelty**: ...
- **Hook and structure**: ...
- **Proof and payoff**: ...
- **Comments / audience signal**: ...

## Adaptation Opportunities

| Opportunity | Adapt, avoid, or counter-position | Evidence | Suggested next move |
|---|---|---|---|
| ... | ... | ... | ... |

## Risks Of Copying

[What would be derivative, off-brand, unsupported by evidence, or risky to imitate.]

## Open Questions And Evidence Gaps

[Missing transcript, unavailable comments, absent owner analytics, uncertain distribution cause, or claims needing independent verification.]
```

## Constraints

- Do not invent metrics, transcript quotes, comments, thumbnail details, or distribution causes.
- Separate observed public evidence from performance hypotheses.
- Do not recommend copying a competitor directly; translate evidence into differentiated positioning and execution.
- Do not treat public views as proof of profitability, subscriber conversion, retention, CTR, or revenue.
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

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/youtube-competitive-research-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
