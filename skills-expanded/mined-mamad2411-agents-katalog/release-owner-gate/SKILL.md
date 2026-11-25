---
name: release-owner-gate
description: |
  This skill should be used when Phase 4 (Diligence) of the 4D Blog Engine runs. It orchestrates the nonce-bound 5-stage Release Owner Gate from MoxyWolf's "Beyond the Prompt" whitepaper — Layer-1 deterministic preflight script + Layer-2 BLOCKING reviewer subagent with restricted tools + a CSPRNG nonce echo requirement + a 100-point rubric + an iteration cap + the human Release Owner sign-off. Triggers: "/4d-blog-engine:blog-diligence", "run the release-owner gate", "score this draft", "is this ready to ship", "preflight my blog post". This is a specialist skill — invoked by the 4d-blog-engine orchestrator, not directly by the user in normal usage.
allowed-tools: [Read, Write, Edit, Bash, Glob]
user-invocable: false
---

# Release Owner Gate — Phase 4 orchestration

> **Read this when:** Phase 4 (Diligence) has been invoked. Phase 3's draft exists at `<piece>/03-discernment/draft.md`. Your job is to drive the 5-stage gate to either a clean `BLOCKING: false` (the Release Owner then signs by hand) or a documented escalation.

## STEP 0 — Load the rubric

Immediately Read `${CLAUDE_PLUGIN_ROOT}/references/release-owner-rubric.md` in full. This file defines:
- The 100-point scoring (5 categories: Content 30 / SEO+AEO 25 / E-E-A-T 15 / Voice match 15 / AI-citation 15)
- The exact reviewer output contract (NONCE line + scorecard table + Three highest-leverage claims + BLOCKING line)
- The nonce verification rule and iteration cap

Also Read `${CLAUDE_PLUGIN_ROOT}/references/ai-anti-patterns.md` since the Voice-match category scores against it.

## STEP 1 — Stage the draft into 04-diligence/

The draft from Phase 3 lives at `<piece>/03-discernment/draft.md`. Phase 4 operates on a **staged copy** at `<piece>/04-diligence/blog.md` — Phase 4 may revise this copy across iterations, but `03-discernment/draft.md` remains the canonical Phase-3 output. Copy:

```bash
mkdir -p <piece>/04-diligence
cp <piece>/03-discernment/draft.md <piece>/04-diligence/blog.md
```

If `<piece>/04-diligence/blog.md` already exists from a previous Phase-4 round, do NOT overwrite — that's the revision-in-progress.

## STEP 2 — Build the hero as a labeled Excalidraw story scene

Phase 4's Stage 3 requires `<piece>/04-diligence/og-hero.png` and `<piece>/04-diligence/og-hero-prompt.md` (the AI-transparency artifact). **The plugin builds heroes as labeled Excalidraw scenes only — never as abstract AI-generated cover art.** A hero must depict the actual story: title bar at top, panels for the main beats, concept icons with text labels, arrows showing flow, and an optional small chart or number callout. The reference register is a hand-drawn editorial infographic, not a stock illustration and not a generative-AI cover.

This is a deliberate rejection of the previous abstract-image flow. The writer ran the abstract path, got `"a polished surface with hairline fracture revealing rougher material beneath"`-style outputs, and pushed back with *"we need to change the graphic to be something that relates to the story."* The fix is to make every hero a literal, labeled scene composed from the post's own concrete artifacts by a deterministic three-stage pipeline (extract → outline → render). No image model is called at any step.

The pipeline is:

```
blog.md  ──(STEP 2.1 extract)──▶  scene-outline.json
                                         │
                                         ▼
                            (STEP 2.2 propose drafts)
                                         │
                                         ▼
              writer picks A/B/edit ──▶ approved outline
                                         │
                                         ▼
                       (STEP 2.3 invoke hero-scene-composer)
                                         │
                                         ▼
                <slug>.excalidraw.md  +  og-hero.png  +  og-hero-prompt.md
```

If the hero doesn't exist yet:

### 2.1 — Locate the brand style and extract the scene outline

Walk up from `<piece>` to find the project marker (`blog-project-instructions.md` first, then `00 – Project Hub/cowork-project-instructions.md`). Parse the `## Hero image brand style` block if present. Fall back to the neutral default if missing: warm off-white ground (`#F8F1E5`), deep navy accent (`#2C3E50`), muted gold secondary (`#C9A66B`), `#1A1A1A` ink, `#6B7280` muted.

Read the staged blog at `<piece>/04-diligence/blog.md`. Apply the extraction recipe in `${CLAUDE_PLUGIN_ROOT}/references/story-to-scene-extraction.md` to produce a structured outline. Write the outline to `<piece>/04-diligence/scene-outline.json`. The extraction recipe is the single source of truth for the outline schema, the icon-name vocabulary it draws from, and the "no invented copy" rule.

### 2.2 — Propose two scene drafts to the writer

Read `scene-outline.json` and present two alternative scene framings via `AskUserQuestion`. The two drafts share the title, the source artifacts, and the icon vocabulary, but differ on (at least one of):

- **Panel split.** Which H2 anchors the left vs. right panel.
- **Icon roster.** Which 2–4 concrete nouns each panel features.
- **Bridge framing.** Which verb of motion bridges the two panels.
- **Chart presence/kind.** Whether the micro-chart appears, and if so which `kind` (bars3 / count_of / contrast_pair).

Present each draft as a short text outline — no images — so the writer can pick by reading. Include a third option: *"let me edit the outline"* — which surfaces the JSON for direct editing before composition.

After approval, write the final approved outline back to `<piece>/04-diligence/scene-outline.json` (overwriting the extraction's draft).

### 2.3 — Compose the scene

Invoke the `hero-scene-composer` skill (`${CLAUDE_PLUGIN_ROOT}/skills/hero-scene-composer/SKILL.md`) with the approved `scene-outline.json` and the resolved brand palette. The composer:

1. Validates the outline against its schema.
2. Loads the canvas template at `${CLAUDE_PLUGIN_ROOT}/references/excalidraw-canvas-template.json`.
3. Drops icons from `${CLAUDE_PLUGIN_ROOT}/references/excalidraw-icon-vocab.md` into the panel slots.
4. Renders the optional chart and callouts.
5. Writes the wrapped `.excalidraw.md` source to `<BLOG_PROJECT_DIR>/drafts/blog-media/<slug>.excalidraw.md`.
6. Calls `${CLAUDE_PLUGIN_ROOT}/scripts/excalidraw-to-png.mjs` to export `<piece>/04-diligence/og-hero.png` at 1600×900.
7. Writes the AI-transparency artifact to `<piece>/04-diligence/og-hero-prompt.md`.

### 2.4 — Handle export failures

If `excalidraw-to-png.mjs` exits non-zero (typically because the writer hasn't installed Playwright yet), the composer writes a fallback file at `<piece>/04-diligence/og-hero-export-instructions.md` and surfaces the failure to this gate. In that case, the gate stops here and tells the writer:

> The Excalidraw scene was composed and saved to `<BLOG_PROJECT_DIR>/drafts/blog-media/<slug>.excalidraw.md`. Open it in Obsidian, switch to Excalidraw view, and export PNG to `<piece>/04-diligence/og-hero.png` at 1600×900. Then re-run `/4d-blog-engine:blog-diligence` to continue.
>
> To make this fully automatic next time, install once:
>
> ```bash
> npm install -g playwright
> npx playwright install chromium
> ```

The gate **does not** offer an image-generation fallback. That path is permanently retired.

### 2.5 — Existing hero re-check

If `<piece>/04-diligence/og-hero.png` already exists (re-run), do not regenerate. Verify the PNG is non-empty and continue. If the writer wants to regenerate, they delete the PNG (and optionally the `.excalidraw.md` source) and re-run `/blog-diligence`.

## STEP 3 — Rotate the nonce and dispatch the BLOCKING reviewer

For round 1, rotate the nonce (preflight.py auto-creates if absent; --rotate-nonce regenerates):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preflight.py \
  --piece <piece> --round 1 --rotate-nonce
```

Read the freshly-generated nonce from `<piece>/.review-nonce`. This is the 32-char hex string the reviewer subagent **must** echo verbatim in its scorecard.

Now dispatch the reviewer subagent. Use the Agent tool (or `Task` if available) with a **restricted-tools spec**: `Read, Write, Glob, Grep` only. **No Bash. No Edit.** The reviewer cannot execute or modify; only read and write its review.

The reviewer's prompt (substitute the placeholders):

```
You are the BLOCKING Release Owner reviewer for the 4D Blog Engine.

CONTEXT:
- Draft to review: <piece>/04-diligence/blog.md
- Rubric: ${CLAUDE_PLUGIN_ROOT}/references/release-owner-rubric.md
- Anti-pattern catalog: ${CLAUDE_PLUGIN_ROOT}/references/ai-anti-patterns.md
- AEO checklist: ${CLAUDE_PLUGIN_ROOT}/references/aeo-checklist.md
- Discourse sources: <piece>/03-discernment/sources-verification.md
- Phase 1 angle and earned secret: <piece>/01-delegation.md

YOUR TASK:
1. Read all four reference files in full.
2. Read the draft in full.
3. Read the sources-verification file to know which claims are [V]/[S]/[F].
4. Score the draft against the 100-point rubric. Be conservative — when uncertain, score lower. Conservatism applies to SCORES, not to the findings list: report every issue you find, including low-severity ones you are unsure about, each tagged with severity — the verdict threshold does the filtering, not you.
5. List the three highest-leverage claims or numbers in the draft, each with its source URL.
6. Write your scorecard in the EXACT FORMAT in references/release-owner-rubric.md §"Reviewer output contract". Any deviation from the format causes the gate to reject the review.
7. Echo this nonce verbatim on the NONCE: line: <NONCE_HEX>
8. End with BLOCKING: true|false (reason). The verdict rules are in the rubric — pay attention to them.

Write your output to: <piece>/04-diligence/review.md
Do not write anywhere else. Do not execute anything. Read-and-write only.
```

## STEP 4 — Run preflight against the review

After the reviewer finishes, run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preflight.py \
  --piece <piece> --round <N>
```

The script reads `<piece>/04-diligence/blog.md` and `<piece>/04-diligence/review.md`, verifies the nonce echo, validates the scorecard format, parses the BLOCKING verdict and the total score, and runs Stages 1-5 of the gate. It writes `preflight-report.json` and `preflight-report.md`.

**Exit codes drive your next action:**

- **0 (pass):** The gate passed. Go to STEP 5 (Release Owner sign-off).
- **1 (retry):** A pre-review stage failed (capability / format / visual / asset_integrity), OR Stage 4 failed but round < 3. Surface the findings to the user, revise the staged blog (you may Edit `<piece>/04-diligence/blog.md` to address the findings), then go back to STEP 3 with `--round <N+1>` and `--rotate-nonce`.
- **2 (escalate):** Round 3 still failing. Stop. Tell the user: *"Release Owner Gate failed after 3 rounds. The draft needs structural rework — likely a different angle, more research, or a manual rewrite. See `<piece>/04-diligence/preflight-report.md` for the findings trail."*
- **3 (gate-pre-review):** Stage 1, 2, 3, or 5 failed and we never got to the reviewer. Fix the structural issue (missing frontmatter, em-dash, [F] data, missing hero) and re-run without dispatching the reviewer again.

## STEP 5 — Release Owner sign-off

If preflight passes, **do not auto-sign.** The plugin never auto-signs. Surface the gate result to the user with the three whitepaper questions, in this exact format:

```
Release Owner Gate passed.

Score: <total>/100
Reviewer BLOCKING verdict: false
Three highest-leverage claims to verify by hand:
  1. <claim> — Source: <url>
  2. <claim> — Source: <url>
  3. <claim> — Source: <url>

Three questions before you sign:

  1. Is every claim grounded? (Trace each of the three claims above to its source.)
  2. Does it sound like us? (Read the first 200 words and the last 200 words aloud.
     If the middle 80% drifts in voice, the gate fails — say so.)
  3. Would you send this with your own name on it?

If all three answers hold, append this line to <piece>/changelog.md:

  Verified — <your initials>, <today YYYY-MM-DD>

Then say "signed" and I'll stage the draft for publish.
```

Wait for the user's explicit "signed" (or equivalent confirmation). Do not stage the draft before this. The signature is the whole point of the framework.

## STEP 6 — On signature: stage the draft

When the user confirms the signature:

1. Verify `<piece>/changelog.md` contains a `Verified — <initials>, <date>` line dated today.
2. **Stage the signed post as a clean draft** at `<blog-project-dir>/drafts/<slug>.md`. The `drafts/` folder is the writer-facing handoff between sign-off and publish — a clean copy of the signed post, easy to find without digging into `Posts/<slug>/04-diligence/`. The piece directory remains the forensic archive (delegation, description, discernment artifacts stay where they are).

    ```bash
    # Walk up from <piece> to find the blog project directory (where blog-project-instructions.md lives)
    BLOG_PROJECT_DIR=$(find_blog_project_dir "<piece>")
    mkdir -p "$BLOG_PROJECT_DIR/drafts"
    cp "<piece>/04-diligence/blog.md" "$BLOG_PROJECT_DIR/drafts/<slug>.md"
    ```

    The hero image is NOT copied to `drafts/` — it stays in `<piece>/04-diligence/og-hero.png` until publish. Drafts/ is markdown-only by convention (matches the writer's mental model of "where my finished drafts live as files I can read").

    If `<blog-project-dir>/drafts/<slug>.md` already exists (re-running Phase 4 on a piece that's been signed before), overwrite it without asking — the freshly-signed version is canonical.

3. Update `<piece>/state.md`: `gates_passed: [01, 02, 03, 04]`, append `<ISO> — Phase 04 passed, signed by <initials>. Staged to <blog-project-dir>/drafts/<slug>.md` to the process log.

4. **Tell the writer their next-step options** (do NOT auto-invoke anything):

    ```
    Phase 4 passed and signed. The post is staged for publish.

    Next steps (run when you're ready):

      • /4d-blog-engine:blog-publish     — push the post to your live site
      • /4d-blog-engine:blog-social      — derive social posts (LinkedIn pair, Twitter thread, Facebook post)
                                            You pick which platforms; nothing is auto-generated.

    Both commands are optional and can run in any order. The blog is the canonical artifact;
    social derivatives are downstream and the writer decides when (and whether) to make them.
    ```

   Critical: the release-owner-gate skill ends here. It does **not** invoke `blog-social` automatically. Social derivation is opt-in and writer-driven. This is a deliberate decoupling — the writer often wants to publish first, see how the post reads in the wild for a day, and *then* decide which social platforms to derive for.

## What the reviewer subagent IS allowed to do

- Read the draft, the rubric, the anti-pattern catalog, the AEO checklist, the sources file, the delegation file.
- Read any reference file in `${CLAUDE_PLUGIN_ROOT}/references/`.
- Glob/Grep within the piece directory.
- Write `<piece>/04-diligence/review.md`.

## What the reviewer subagent is NOT allowed to do

- Execute anything (no Bash).
- Edit the blog draft (no Edit).
- Write anywhere outside `<piece>/04-diligence/review.md`.
- Make network requests.
- Mark its own verdict approved without echoing the nonce verbatim.

The tool restriction is the security boundary — a reviewer that can edit can write its own pass condition. A reviewer that can shell can spoof preflight's parsed values. Hold the boundary.

## What this skill does NOT do

- It does NOT draft or rewrite content. The orchestrator's iteration loop revises the draft based on the reviewer's findings; the reviewer never does the revision.
- It does NOT decide when to publish. The Release Owner signs by hand; the plugin never auto-publishes.
- It does NOT touch the canonical Phase-3 artifact. `<piece>/03-discernment/draft.md` remains read-only after Phase 3.

## Degradation behaviors

- **Reviewer subagent unavailable** (Agent tool not loaded): fall back to having Claude itself act as reviewer with the same prompt, in the same session — but flag this in `preflight-report.md` as a degraded mode (less independent than a subagent context). Still required to echo the nonce.
- **Hero image generation fails or no image-gen MCP is connected:** surface the prompt as `<piece>/04-diligence/og-hero-prompt.md` and ask the user whether to (a) generate the image by hand and drop the PNG at `<piece>/04-diligence/og-hero.png`, or (b) skip the hero (preflight will fail Stage 3 until a PNG exists at that path). Never insert a placeholder image and call the stage passed.
