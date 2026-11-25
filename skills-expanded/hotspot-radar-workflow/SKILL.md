---
name: hotspot-radar-workflow
description: Use when the user gives a content theme or niche and wants Douyin benchmark accounts, benchmark content, evidence-backed topic candidates, and an owner checklist for do/observe/do-not decisions.
license: MIT
metadata:
  version: "0.1.1"
  author: "Dalin AI Works"
x-alice-class: assist
---# Hotspot Radar Workflow

## Role

Act as the internal "热点雷达" workflow controller.

Given a content direction, run or guide the radar workflow:

`theme -> keyword expansion -> Douyin candidate fetch -> normalization -> metrics and comment evidence -> opportunity scoring -> 10-topic owner checklist -> owner do/observe/do-not review -> rule calibration`

The goal is not to collect every hotspot or generate finished scripts. The goal is to find high-interaction, account-fit, evidence-backed benchmark content that can become a short list of topic opportunities for the owner to judge.

## Use When

Use this Skill when the user asks to:

- find domestic short-video hotspot/topic candidates for a theme;
- validate a content niche such as AI, Codex, Skill, AI automation, real projects, or content workflow;
- use existing TikHub access to search Douyin candidates;
- score candidate content with likes, comments, favorites, shares, fit, transferability, and risk;
- output a simple 10-topic owner checklist for "要做 / 可观察 / 不要做";
- continue Gate 1 hotspot-radar workflow validation.

## Do Not Use When

Do not use this Skill for:

- Web MVP, Next.js UI, desktop app, authorization, SaaS, or commercial packaging;
- automatic publishing, editing, video rendering, or talking-head production;
- claims that a topic is guaranteed viral;
- direct synonym-level rewriting or "洗稿";
- downloading videos, bypassing login, ASR/OCR, or scraping beyond the authorized API path;
- showing or exporting internal reports, API keys, raw crawl data, candidate tables, scoring JSON, or source creators' media as public video material;
- treating script quality, conversion, filming, or publishing performance as the radar's first-stage acceptance gate.

## Required Inputs

If missing, infer conservatively only when safe. Ask only when the missing item would change the workflow materially.

- `theme`: content direction, for example `AI 自动化真实项目`.
- `target_audience`: audience served by the account.
- `content_goal`: trust, followers, series validation, education, leads, etc.
- `primary_platform`: Gate 1 defaults to Douyin.
- `owned_cases`: the owner's projects, views, skills, or real cases that can support original content.
- `forbidden_directions`: exaggerated income, copying, internal data, unverified tools, sensitive claims.

Optional:

- `seed_keywords`
- `max_requests`, default 25
- `content_formats`, default oral short video first
- `must_include_view`
- `exclude_keywords`

## Default Assumptions

When the user does not specify otherwise:

- Platform: Douyin.
- Theme family: AI / Codex / Skill / AI workflow / real projects.
- Owner audience: people using AI to make content, projects, workflows, and real useful things.
- Request budget: 25 TikHub requests per run.
- Public output: no internal reports, raw data, keys, screenshots, creator media, or comment identities.
- Owner-facing default output: topic checklist, not full script.

## Prerequisite Check

Before every real fetch, run the first-run check or token preflight.

For a shared Skill package, prefer:

`node scripts/first-run-check.mjs`

The first-run check verifies Node.js, TikHub API base URL, local Token availability, and required scripts.

Run:

`node scripts/run-gate1-topic-validation.mjs --check-token`

If `ok: false`, stop and ask the owner to provide a TikHub API Token. Do not continue to mock or stale data unless the owner explicitly asks for a no-fetch dry run.

First-time setup:

1. Open TikHub dashboard: `https://user.tikhub.io/dashboard/api`
2. Copy the API Token.
3. Run `node scripts/setup-tikhub-token.mjs`.
4. Paste the Token into the prompt and press Enter. Interactive input should be hidden by the terminal.
5. Re-run `node scripts/first-run-check.mjs`.

The default API base URL is `https://api.tikhub.io`. Only use another base URL when the owner explicitly approves that exact domain.

Token storage rules:

- Prefer macOS Keychain service `hotspot_radar_tikhub_api_token` with the current local account.
- Keep backward compatibility with legacy service `ai_anget_tikhub_api_token` and account `dalin`.
- `TIKHUB_API_KEY` may be used for a temporary shell session, but it disappears when that session ends.
- Never write API Keys into project files, reports, logs, Git, screenshots, or public Skill packages.
- If the terminal still echoes Token input in a specific environment, stop and use a safer local terminal path before sharing the screen or logs.

## Workflow

### 0. User-Facing Usage

The simplest usage is one theme in, one owner checklist out:

`node scripts/run-topic-checklist.mjs "AI 自动化真实项目"`

The user only needs to provide one broad content direction, such as:

- `AI 自动化真实项目`
- `Codex Skill 工作流`
- `母婴睡眠`
- `本地生活探店`

The Skill then:

1. checks whether TikHub Token is available;
2. expands the theme into 6 to 8 enabled search keywords;
3. searches Douyin candidate content through TikHub;
4. normalizes likes, comments, favorites, shares, author, title, description, source keyword, and missing fields;
5. scores each candidate with content opportunity score;
6. excludes same-theme candidates already returned in previous runs;
7. outputs a 10-topic checklist for `要做 / 可观察 / 不要做`.

When the user gives only one keyword or theme, do not ask them to manually provide expanded keywords unless the first run is clearly off-track.

### 1. Establish TrackBrief

Create a concise TrackBrief:

- theme;
- target audience;
- content goal;
- platform;
- owned cases;
- forbidden directions;
- request budget;
- run id.

### 2. Expand Keywords

Generate 6 to 8 enabled keywords.

Expansion means the user does not need to know every search term. For example:

Input theme: `AI 自动化真实项目`

Possible enabled keywords:

- `AI 自动化真实项目`
- `AI 做项目`
- `一个人 AI 工作流`
- `AI 项目复盘`
- `AI 工作流 保姆级教程`
- `Codex 项目实战`
- `Codex 工作流`
- `Skill 工作流`

Each keyword should have a reason and status. Status can be `enabled`, `candidate`, or `paused`. Only `enabled` keywords are fetched in the current run.

Prefer:

- Codex project;
- Skill workflow;
- AI real project;
- AI content production line;
- one-person AI workflow;
- AI project review;
- tool-specific terms only when the owner has evidence or can avoid tool review claims.

Avoid or downweight:

- AI making money;
- AI side hustle;
- replacing jobs;
- violent income claims;
- generic AI news;
- film/visual effects if not tied to Codex/Skill/real projects.

### 3. Fetch Candidates

For a real run, use the lower-level project script when intermediate files need inspection:

`node scripts/run-gate1-topic-validation.mjs <run-id> '<theme>'`

For a shared Skill package, prefer the simpler end-to-end entry:

`node scripts/run-topic-checklist.mjs "<theme>"`

Important:

- Run from the repository root or installed skill root.
- Use the preflight token check first.
- Do not print or store secrets.
- Default endpoint is `https://api.tikhub.io`.
- Do not send the token to an alternative domain unless the user explicitly approves that exact domain.
- Do not download videos.
- Do not publish or call video production.

Expected outputs:

- `data/gate-1/runs/<run-id>/keywords/keyword-nodes.json`
- `data/gate-1/runs/<run-id>/raw/search/`
- `data/gate-1/runs/<run-id>/raw/comments/`
- `data/gate-1/runs/<run-id>/normalized/content-candidates.json`
- `data/gate-1/runs/<run-id>/scores/opportunity-scores.json`
- `data/gate-1/runs/<run-id>/analyses/structured-analyses.json`
- `data/gate-1/runs/<run-id>/logs/run-log.json`
- `data/gate-1/runs/<run-id>/logs/failure-summary.json`
- `reports/gate-1/<run-id>-candidate-selection-report.md`

### 4. Score Candidates

Use "content opportunity score", not viral score.

Suggested v0.1 weights:

- basic metrics: 25
- user demand: 15
- track relevance: 20
- account fit: 20
- transferability: 15
- structure clarity: 8
- freshness: 4
- evidence completeness: 3
- risk penalty: up to -30

Missing play count, completion rate, follower count, transcript, or OCR must be marked as missing. Do not fake them as valid zeros.

### 5. Filter With Judgment

Do not mechanically accept Top 1 to Top 5.

Downweight even high-data candidates when:

- topic is off-account, such as factory automation unrelated to AI/Codex/Skill content;
- income claim is exaggerated;
- content depends on source creator's personal story;
- content requires copying screenshots, music, visuals, comments, or unique expression;
- tool review would require unverified hands-on use.

Prefer candidates that:

- have strong metrics or strong comment demand;
- fit AI/Codex/Skill/real-project positioning;
- can be rebuilt with owner's own project or process;
- can become oral explanation, screen-recording demo, or abstract workflow content;
- have clear "cannot copy" boundaries.

Recording samples must pass a stricter evidence gate than A/B candidates:

- score is at least the A-tier threshold;
- has minimum interaction volume;
- has comment evidence and demand comments, or very strong interaction;
- confidence estimate is at least `0.55`;
- account fit is acceptable;
- does not rely on copying source creator materials.

Low-interaction, no-comment, low-confidence candidates may stay in the candidate pool or owner-view pool, but must not automatically enter recording packages.

When selecting Top 3 recording samples, keep angle diversity where possible:

- Skill/workflow;
- Codex usage or onboarding;
- content/video workflow;
- real project case.

### 6. Generate Owner Checklist

Default Gate 1A output is a 10-topic checklist.

Use the helper when a score file already exists:

`node scripts/build-gate1a-owner-review.mjs <source-run-id> reports/gate-1/<run-id>-owner-review-checklist.md`

The checklist must include:

- 10 candidate topics;
- recommendation level: `S`, `A`, `B`, `C`, or `Noise`;
- metrics: likes, comments, favorites, shares;
- short recommendation reason;
- missing data and risk;
- owner checkbox: `[ ] 要做  [ ] 可观察  [ ] 不要做`.

Same-theme dedupe is required:

- The helper records returned candidates in `data/gate-1/owner-review-history.json`.
- On the next run with the same normalized theme, previously returned `candidate_id` and near-duplicate topic fingerprints are excluded.
- If fewer than 10 new candidates remain, output fewer and say the same-theme candidate pool is exhausted; do not refill with old topics unless the owner explicitly asks.
- Use `--no-history` only for debugging or reproducing an old report.

The owner should only need to judge the checklist. Do not ask the owner to inspect raw JSON, sort metrics, or approve every scoring detail.

Gate 1A passes when one run has 3 to 5 `要做` items, and is stable when two comparable runs reach that bar.

### 7. Optional Downstream Creation

Only after the owner marks topics as `要做`, downstream content skills may generate briefs, scripts, recording plans, or conversion routes.

These outputs belong to content production, not radar acceptance.

### 7.1 Generate Creation Briefs

Before writing briefs, generate one structured analysis per selected recording candidate.

The structured analysis must include:

- user problem;
- retention reason;
- borrowable structure;
- do-not-copy boundaries;
- original angle;
- owner-owned case;
- three recreation routes;
- title options;
- cover copy options;
- evidence used;
- evidence limitations;
- confidence and confidence reason;
- risk notes.

Use OpenAI only when `HOTSPOT_AI_ANALYSIS=1` or `--ai-analysis` is explicitly set and `OPENAI_API_KEY` exists. If OpenAI is disabled, missing, or fails, use the heuristic fallback and record the provider reason. Do not let AI analysis failure break candidate selection.

For selected candidates, output three routes when useful:

1. Same pain point, different viewpoint.
2. Same structure, owner's own case.
3. Hotspot joined with a real project.

Each brief must include:

- source candidate and metrics;
- what can be borrowed;
- what cannot be copied;
- owner-owned case;
- original angle;
- target audience;
- title options;
- risk notes;
- evidence limitations.

### 7.2 Generate Recording Packages

Only for candidates confirmed as worth doing or for validation samples.

Recording package includes:

- recommended title;
- cover copy;
- teleprompter script;
- short shot plan;
- required shots;
- subtitle highlights;
- forbidden materials;
- pinned comment suggestion;
- owner review gate.

Mark:

- `publish_ready: false`
- `status: recording_material_ready_for_owner_review`

Do not call `talking-head-video-production` unless the user explicitly asks to enter actual filming/production.

### 7.5 Review Data Source Failures

Every real run must preserve a failure summary.

Classify failed or weak requests as:

- `network_error`: local/network/API host unreachable;
- `http_error`: HTTP 4xx or 5xx;
- `api_error`: API returned a non-success code;
- `parse_error`: response was not valid JSON;
- `field_shape_changed`: expected result arrays are missing;
- `empty_result`: request succeeded but produced zero usable candidates or comments.

Use this to decide whether a bad run was caused by the theme, the keyword set, API stability, quota/auth, or response field changes. Do not hide these failures behind a low candidate count.

### 8. Owner Review Gate

The owner should only need to judge:

- whether the theme direction is right;
- which Top candidates are `要做 / 可观察 / 不要做`.

Do not require the owner to manually:

- sort metrics;
- inspect raw JSON;
- write scoring reasons;
- approve every small step.
- judge script quality before radar acceptance.

### 9. Review And Calibrate

End every run with a concise workflow review:

- search success;
- comment success;
- candidate count;
- selected count;
- accepted candidates;
- rejected or risky candidates;
- scoring issues;
- keyword adjustments;
- next run recommendation.

## Current Known Project Facts

As of 2026-08-05:

- Gate 0 has validated Douyin search/detail/comment availability with limitations.
- Gate 1 round 2 produced 82 deduplicated candidates and 20 A/B candidates.
- Owner selected ranks 6, 11, and 4; all three were later judged worth recording.
- A new topic rerun for `AI 自动化真实项目` produced 117 deduplicated candidates and 20 A/B candidates.
- `sort_type` and `publish_time` must be strings for the current TikHub endpoint.
- Web MVP is not ready.
- This Skill may be drafted/used for workflow validation, but should not imply commercial product readiness.

## Output Style

Prefer:

- Chinese;
- concise but evidence-backed;
- direct decisions when the evidence is enough;
- clear "do / do not / wait" boundaries;
- file outputs for reusable reports and packages.

Avoid:

- saying the owner is right by default;
- calling candidates "viral" when play/completion/follower data are missing;
- burying risk caveats;
- producing long generic marketing copy without evidence;
- step-by-step confirmation for every small artifact.

## Completion Criteria

A successful run should produce:

- candidate report;
- structured scores;
- 10-topic owner checklist;
- owner review fields;
- workflow review and rule adjustments;
- no leakage of secrets or internal data;
- no claim of publishing, Web MVP, script readiness, recording readiness, or Skill installation unless actually done.
