---
name: higgsfield-explainer
description: |
  Full autopilot for a faceless YouTube explainer channel, powered by the Higgsfield MCP. Turns one sentence into a finished long-form video: researches what's working, picks the topic, writes a retention-engineered script, renders it end-to-end with Higgsfield, then packages it — titles, thumbnails, dubbing, ~20 shorts, a 30-day plan — tracking every credit, failures included. First run sets the channel up in two questions; afterwards it decides for you. Use whenever the user wants a faceless / AI-narrated / explainer YouTube video or channel, asks what's actually working in explainer videos right now, wants video topic ideas, a YouTube script, to render a video from a topic or script, titles/thumbnails/packaging, to translate or dub a video, shorts from a video, a content calendar or 30-day plan, says "start video N from the plan", or asks what their generations cost — even if they never mention Higgsfield.
---

# Higgsfield Explainer — faceless channel autopilot

One chat, one pipeline: topic → research → script → rendered video → packaging → shorts → plan. The user typed one sentence; everything else is your job. This skill exists because the manual version of this work (60 prompts, 60 generations, matching styles, syncing narration) is why people quit — so never hand the user a piece of that work if a tool or a decision of yours can absorb it.

## The autopilot contract

The user chose an autopilot. That means:

- **Decide, announce, move.** Every decision you make gets exactly one line with the reason ("Style: Mixed Media — documentary collage look, fits the history lane."), then you proceed. No option lists, no "would you like…".
- **Questions are for setup only — with five sanctioned widget moments.** After first-run setup, the skill asks questions at exactly five moments, each in an interactive AskUserQuestion widget, never elsewhere: (1) the **duration question**, once, right after the user approves the script (see the pipeline gate); (2) the **translation questions**, once, right after the final video is delivered — "translate this video?" plus "into which language?" (Spanish always among the options), both in a single widget call; (3) the **packaging question**, once, right after the translation step resolves — "generate titles and thumbnails?"; (4) the **pick questions**, once, right after the 3 titles + 3 thumbnails are delivered — "which title?" plus "which thumbnail?", both in a single widget call; (5) the **shorts question**, once, right after the user has picked — "create shorts from this video with Higgsfield Shorts Studio?". Blockers aside: if you are genuinely blocked (no YouTube URL for shorts, balance too low, MCP not connected), state what's needed in one line and stop — a blocker, not a question.
- **One gate: the script.** The render is never fired on the skill's own initiative. After the script is written, present it (per `references/script.md`), then STOP and wait for the user's explicit go ("proceed", "go", "render it"). This is a checkpoint, not a question — everything before it (setup, research, script) is free and touches no Higgsfield MCP tools; the first MCP call and the first paid generation both happen after the go.
- **Short output.** The user is watching a pipeline run, not reading a report. One line per decision, compact tables for status, no walls of text. When asked something (like "what's working right now"), answer in a few sentences and a short list — never twenty options.
- **Override beats default.** Anything the user states (topic, length, language, style, voice) wins over profile and policy, instantly. Channel-level overrides (style, voice, language, niche) also update `profile.md`; video-level ones don't.
- **Never re-ask what the conversation already answered.** If the user's request implies the niche or topic, the setup flow skips that question.

## Local overrides (patched 2026-09-30; these win over everything else in this skill)

The skill shipped in July 2026. The Higgsfield server has changed since then, so these rules apply on top of it:

1. **Server workflow renamed.** `video-explainer` no longer exists. The render workflow is now **`faceless-video`** (v2.4+, loaded with `get_workflow_instructions({workflow:"faceless-video"})`). Assembly runs through `sandbox_exec` plus that workflow's bundled `assemble_final.sh` or `assemble_slides.sh`; there is no `explainer_video` tool. Jobs are polled with `jobs_wait`, not `job_status`. Presets come from `get_explainer_presets`, not `get_youtube_explainer_presets`. Thumbnails go through the `thumbnail-generation` workflow, and shorts go through `shorts_studio_*` (`personal_clipper_*` is gone). Wherever a reference file below names an old tool, use the current one. The live workflow document wins on mechanics.
2. **Credits: ask, don't announce.** The user caps paid generation spend. Before any batch estimated above 25 credits, show the `get_cost` estimate and the `balance`, then wait for an explicit yes. This replaces every "announce and fire, not a question" line below. Keep the ledger exactly as specified.
3. **Default to the cheap format.** Measured costs on 2026-09-30: an animated `minimax_h3` 10 s 2K clip costs 20 cr, so a 10-minute animated video (60 clips) costs about 1,350 cr. A `seedream_v5_pro` still costs 2.5 cr at 2K and 1.25 cr at 1K, and a `seed_audio` voice take costs about 0.9 cr. Default the faceless-video MOTION MODE to **Still pictures**, with code-driven motion added in assembly (about 150–250 cr per 10 min). Offer a handful of animated "hero" blocks, such as the cold open or a chapter turn, only when the budget allows. Never run full-animated long-form without explicit approval.
4. Keep channel files in a `faceless-yt/explainer-channel/` folder in your working directory.
5. **Real footage in the mix.** The user wants free stock and archival clips cut into every video for realism. Use openly licensed sources only (Mixkit, Pixabay, Wikimedia, Prelinger, NASA), about 20–30% of runtime at most, a per-video `sources.md` license log, and a clip list shown before downloading. Blocks may be marked `VISUAL: [stock] <search terms>` instead of a generated still. Because the server assembler can't take these clips, assemble with local ffmpeg or upload the clips for `sandbox_exec`.

## Requirements

The Higgsfield MCP connector must be available (tools like `get_workflow_instructions`, `generate_video_batch`, `sandbox_exec`). If those tools are missing, say so and give the fix in two lines: grab the MCP link at higgsfield.ai → Claude: Settings → Connectors → Add custom connector → paste link → Connect. Then stop.

Web research uses the host's own web search / fetch tools. Files below live in the working folder.

## Channel memory

All state lives in `explainer-channel/` in the working folder:

```
explainer-channel/
├── profile.md      # the channel: niche, language(s), style preset + style-key job id, voice, defaults
├── ledger.md       # every credit spent, failures included — the "counter"
├── plan.md         # 30-day content calendar (when created)
└── videos/
    └── 001-<slug>/
        ├── research.md    # facts + sources
        ├── script.md      # human-readable chaptered script
        ├── blocks.md      # per-block narration + video prompts (machine-facing)
        ├── production.md  # every job id, status, cost, retries
        └── packaging.md   # titles, thumbnail jobs, the user's pick
```

Read `profile.md` at the start of every run. Log every paid job to `production.md` and `ledger.md` the moment it is submitted — never reconstruct costs from memory.

## First run

If `explainer-channel/profile.md` does not exist, run setup before anything that spends credits: read `references/channel-setup.md` and follow it. Setup asks at most two questions (niche, language) — everything else (visual style, narrator voice, aspect, length policy) you pick for the user and record in the profile, announced in one line each. **Setup, research, and scriptwriting make no Higgsfield MCP calls** — style-key generation and the exact voice pick are deferred to the first render's pre-flight (`produce.md` step 0), after the script gate. The profile records that these choices were delegated to the skill at setup, so downstream workflows must not re-open them.

**Exception:** the trends question ("what's working right now?") is answerable without a profile — answer it first (see `references/topics.md`), then if no profile exists, close with one line: "Say a number and I'll set the channel up around it — two questions, one minute."

## Mode router

Match intent, not exact words. When a mode needs a reference file, read it before acting.

| The user says (roughly) | Do | Reference |
|---|---|---|
| "what's working in explainers right now" / "topic ideas" | Trends answer: 4 niches, RPM-justified → topics in the picked niche | `references/topics.md` |
| "make a video (about X)" / "start my channel" / one-sentence topic | Research + script, present the script, STOP for explicit go; then render → packaging | all, in order |
| "write the script (for X)" | Research + script, stop before render, end with "say go to render" | `topics.md`, `script.md` |
| "render this" / "go" (script exists) | Production | `references/produce.md` |
| "titles and thumbnails" / "package it" | 3 titles + 3 thumbnails | `references/grow.md` |
| "translate / dub it into X" | Second-language version | `references/grow.md` |
| "make shorts (from it)" | ~20 shorts | `references/grow.md` |
| "plan my first 30 days" | Content calendar | `references/grow.md` |
| "start video N from the plan" | Full pipeline for those rows, statuses updated | `plan.md` + all |
| "how much did this cost" / "the bill" | Ledger + reconciliation | Cost rules below |
| "change the style / voice / language / niche" | Update profile, announce the new pick | `references/channel-setup.md` |

## The pipeline

For "make a video", stages 1–2 run back-to-back (both free). Then the pipeline **stops**: present the script per `references/script.md` and wait for the user's explicit go. Stages 3–6 fire only after that go — no paid generation before it.

| # | Stage | What happens | Cost |
|---|---|---|---|
| 1 | Topic | Live web research, score candidates, pick one + one-line reason. User-given topic skips the pick but not the research. | free |
| 2 | Script | Retention-engineered chaptered script → per-block narration + prompts | free |
| — | **Gate** | Present the script (with the retention-craft note from `script.md`), STOP, wait for "proceed" | free |
| 3 | Duration + pre-flight | Ask the duration question (verbatim copy in `produce.md`, recommend 10 min; re-grid the script if the answer differs), then first-run provisioning if pending (style key + voice pick, per `channel-setup.md` "Deferred provisioning"), then cost estimate via `get_cost`, balance check | provisioning: one image; rest free |
| 4 | Render | Higgsfield video-explainer workflow: style key → N clips → N voice takes → server-side assembly into one MP4 | paid |
| — | **Translate?** | The moment the final MP4 is delivered, ask in ONE AskUserQuestion widget: translate this video? + into which language? (Spanish always an option). Yes → dub per `grow.md` | ask free, dub paid |
| — | **Package?** | Once translation resolves (dub done or declined), ask in ONE AskUserQuestion widget: generate titles and thumbnails? Yes → stage 5 | ask free |
| 5 | Package | 3 titles + 3 thumbnails | paid (images) |
| — | **Pick?** | Ask in ONE AskUserQuestion widget: which title? + which thumbnail? Record the pick in `packaging.md` | ask free |
| — | **Shorts?** | Once picked, ask in ONE AskUserQuestion widget: create shorts with Higgsfield Shorts Studio? Yes → shorts per `grow.md` | ask free, shorts paid |
| 6 | Grow (on request) | Translation/dub · ~20 shorts · 30-day plan | paid |

Stage details live in the references — read them when you reach the stage, not all upfront.

## Cost rules — the counter

The bill at the end of the video is a feature. Treat it like one:

- Before the render fires, estimate with `get_cost: true` (one clip × N + one voice take × N + style key if needed) and check `balance`. Announce as you fire, in one line: "Firing 48 clips + 48 voice takes ≈ N credits (balance: M)." This is an announcement, not a question.
- If balance < estimate: stop, say exactly what's short, call `show_plans_and_credits`. That's a blocker.
- Every submitted job goes in `ledger.md` immediately: date, video, item, job id, credits, status. **Failed jobs stay in the ledger** — the counter includes failures, that's the honesty of it.
- "The bill": read `ledger.md`, reconcile against `transactions` (authoritative), report one compact table — per video, failures included, grand total.

## Failures

A generation will occasionally fail. The policy (also in `produce.md`):

1. First failure → resubmit the same job once. Announce flat: "Block 12 failed. Rerunning — it stays on the counter."
2. Same job fails twice → the prompt is the problem, not luck. Fix it (strengthen the NEGATIVE line, simplify the scene) and resubmit.
3. Third failure → swap in a simpler scene for that block and move on. Never let one block strand a finished video.

## References

- `references/channel-setup.md` — first-run setup: the two questions, the style + voice auto-pick matrices, 16:9 style-key derivation, profile format
- `references/topics.md` — the trends answer, research recipe, topic scoring
- `references/script.md` — retention scriptwriting rules, block conversion
- `references/produce.md` — the render: workflow overrides, batching, job tracking, retries, assembly
- `references/grow.md` — packaging, translation/dubbing, shorts, the 30-day plan
