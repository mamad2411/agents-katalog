---
name: youtube-video-audit
description: Audit one YouTube video in depth using public metadata, transcript/content evidence, release timing, comments, and optional owner analytics
type: research
version: v0.5
argument-hint: "<video URL or ID> [--owner-analytics <path>] [--comments N] [--compare-channel <slug>]"
interview_depth: none
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` instead of the target skill. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# YouTube Video Audit

Invoke as `$youtube-video-audit`.

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

- Required: one YouTube video URL or video ID.
- Optional `--owner-analytics <path>`: user-provided CSV/JSON export or OAuth/API output from YouTube Studio or YouTube Analytics API.
- Optional `--comments N`: fetch up to N public top-level comments when public comment tooling/API access is available. Default 50, max 200.
- Optional `--compare-channel <slug>`: compare the video against existing raw channel evidence under `research/youtube/data/<slug>/`.

## Process

### 1. Resolve Target and Tools

1. Extract the video ID from a normal watch URL, Shorts URL, youtu.be URL, embed URL, or raw 11-character ID.
2. Require `yt-dlp` for public metadata:

   ```bash
   command -v yt-dlp
   ```

3. Select a transcript Python interpreter. Prefer a workspace-local `.venv`; create it if missing. Install `youtube-transcript-api` into `.venv` only when the import check fails and network access is available.
4. Do not require API keys. If `YOUTUBE_API_KEY` is already present, optionally use the YouTube Data API to enrich public metadata and public comments. If it is absent, continue with `yt-dlp` and transcript evidence.
5. Do not scrape logged-in YouTube Studio pages, bypass bot protections, or ask for private account credentials.

### 2. Persist Raw Evidence

Create:

```text
research/youtube/data/<video-id>/
```

Persist public evidence before analysis:

- `metadata-YYYY-MM-DD.json`: raw `yt-dlp --dump-json "VIDEO_URL"` output.
- `transcript/<video-id>.json`: raw transcript JSON when available.
- `transcript/transcript-summary.json`: transcript text or failure reason.
- `api/videos-list-YYYY-MM-DD.json`: optional YouTube Data API `videos.list` response when `YOUTUBE_API_KEY` is already available.
- `api/comment-threads-YYYY-MM-DD.json`: optional public `commentThreads.list` response when available.
- `owner-analytics/<source-file>`: copy or cite user-provided owner analytics exports when supplied.

Record evidence gaps explicitly. Missing transcript, comments, likes, retention, CTR, impressions, traffic sources, or daily history are not failures.

### 3. Public Metadata Fields

Extract when present:

| Field | Source and use |
| --- | --- |
| `id`, `webpage_url`, `title`, `description` | Identity, promise, and audit links |
| `channel`, `channel_id`, `uploader`, `uploader_id` | Channel identity |
| `upload_date`, `timestamp`, `release_timestamp`, `live_status` | Release timing and live/premiere context |
| `duration`, `availability`, `age_limit`, `is_live`, `was_live` | Format and access context |
| `view_count`, `like_count`, `comment_count` | Public performance snapshot |
| `tags`, `categories`, `chapters` | Topic, SEO, and structure signals |
| `thumbnail`, `thumbnails` | Packaging review evidence |
| `subtitles`, `automatic_captions` | Transcript availability signal |

If YouTube Data API enrichment is available, include `snippet`, `contentDetails`, `statistics`, `status`, `topicDetails`, and `liveStreamingDetails` from `videos.list`. Respect quota costs and do not run repeated unnecessary API calls.

### 4. Owner Analytics Lane

When `--owner-analytics <path>` is supplied, inspect the local file format and parse only available fields. Support CSV or JSON with any of these fields:

- views, watch time, average view duration, average view percentage.
- impressions, click-through rate, traffic source, playback location, device type, geography.
- audience retention, relative retention, intro retention, end-screen metrics.
- likes, dislikes if owner-exported, comments, shares, subscribers gained, subscribers lost.
- daily or hourly time series after publish.

Treat owner analytics as private or owner-provided evidence. Cite local paths, avoid copying sensitive rows unrelated to this video into the report, and do not claim owner-only metrics unless they are present in the supplied evidence.

### 5. Analyze the Video

Analyze performance and content together:

- Release timing: date, weekday, time, recency, premiere/live/Shorts context, and any owner-provided first-24h or first-7d curve.
- Public performance: views, likes, comments, like rate, comment rate, views/day, views/minute, and comparison to channel median when `--compare-channel` evidence exists.
- Packaging: title promise, specificity, search/topic clarity, thumbnail focal clarity, description support, chapters, tags, and promise-match with the opening.
- Hook and structure: first 30-60 seconds, problem statement, payoff setup, pacing, chapter structure, recurring dead zones, outro and CTA.
- Content quality: clarity, credibility, examples, evidence, novelty, production value, and whether the video serves acquisition, trust-building, proof, education, launch support, community, or cleanup/repositioning.
- Audience response: summarize public comments into themes only when comments were captured; separate praise, objections, confusion, requests, and spam/noise.
- Owner analytics diagnosis: when present, connect retention, traffic, CTR, watch time, and time-series signals to concrete packaging or content hypotheses.

Do not fabricate transcript quotes, comments, thumbnails, retention curves, or metric values. Every major conclusion must cite the raw path, video metadata field, transcript excerpt, comment evidence, or owner analytics field that supports it.

### 6. Write Report

Create the `research/youtube/` and `research/youtube/data/<video-id>/` directories if they do not exist.

Save to:

```text
research/youtube/video-audit-<video-id>-YYYY-MM-DD.md
```

Use this structure:

```markdown
# YouTube Video Audit - [Title]

> Video: [URL]
> Video ID: [id]
> Channel: [channel]
> Published: YYYY-MM-DD HH:MM TZ if known
> Date captured: YYYY-MM-DD
> Public metadata: research/youtube/data/<video-id>/metadata-YYYY-MM-DD.json
> Transcript: [path or unavailable reason]
> Owner analytics: [path or not provided]

## Evidence Coverage

| Evidence | Status | Path or gap |
|---|---|---|
| Public metadata | Available | ... |
| Transcript | Available / Missing | ... |
| Public comments | Available / Missing / Not requested | ... |
| Owner analytics | Provided / Not provided | ... |
| Channel comparison | Available / Not provided | ... |

## Performance Snapshot

- **Views**: N
- **Likes**: N / unavailable
- **Comments**: N / unavailable
- **Views/day**: N
- **Views/minute**: N
- **Like rate**: N% / unavailable
- **Comment rate**: N% / unavailable
- **Channel comparison**: [above/below median, if evidence exists]

## Release Timing

[Publish date/time, weekday, recency, Shorts/live/premiere context, early curve if owner analytics exists.]

## Packaging Diagnosis

- **Title promise**: ...
- **Thumbnail signal**: ...
- **Description/tags/chapters**: ...
- **Expectation match**: ...

## Content and Retention Diagnosis

- **Hook**: ...
- **Structure**: ...
- **Pacing**: ...
- **Credibility and evidence**: ...
- **CTA/outro**: ...

## Audience Response

[Comment themes or explicit evidence gap.]

## Owner Analytics Findings

[Only include when owner analytics were supplied; otherwise state the gap.]

## What Worked

1. [Finding] - [evidence]
2. [Finding] - [evidence]
3. [Finding] - [evidence]

## What Hurt Performance

1. [Finding] - [evidence]
2. [Finding] - [evidence]
3. [Finding] - [evidence]

## Recommended Fixes

| Priority | Change | Why | Evidence | Human check |
|---|---|---|---|---|
| High / Medium / Low | ... | ... | ... | ... |

## Reusable Lessons

[What to repeat or avoid in future videos, scoped to this video's evidence.]
```

### 7. Summarize In Thread

After saving the report, output the performance headline, top 3 strengths, top 3 weaknesses, highest-priority fix, evidence gaps, report path, and raw data paths.

## Constraints

- Public-first by default; owner analytics are optional and must come from user-provided files or already-authorized API output.
- Do not bypass login walls, bot protections, access controls, or YouTube Studio UI restrictions.
- Do not invent metrics, comments, transcript quotes, thumbnails, or retention data.
- Separate public evidence from private or owner-provided analytics in both raw paths and report language.
- Do not treat one video as a channel trend. Route channel-level pattern questions to `$youtube-channel-audit` or `$creator-metrics-review`.
- Do not perform external account actions or make automated channel changes.

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

Default recommendation: `$youtube-vid-research` when the user needs neutral context from an external reference video; `$youtube-format-research` from the `remotion` pack when the next step is to reuse the video's format, design, pacing, edit, or production grammar; `$youtube-competitive-research` when the user asks why the video worked or what to learn from a specific competitor; `$youtube-concept-research` when the audit should inform a new video concept; `$youtube-description-optimizer` when description support, CTA/link structure, chapters, hashtags, disclosures, or metadata/search alignment are the main next step; `$youtube-title-thumbnail-audit` when title/thumbnail packaging changes are the main next step; otherwise `$creator-metrics-review` when owner analytics or channel comparison evidence suggests broader performance review.

If the user asks whether the issue is unique to this one video, recommend `$youtube-channel-audit`. If the user asks what to make next, recommend `$content-programming` after the audit report exists.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/youtube-video-audit-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
