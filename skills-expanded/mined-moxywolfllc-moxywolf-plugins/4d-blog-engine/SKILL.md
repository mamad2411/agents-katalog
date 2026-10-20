---
name: 4d-blog-engine
description: >
  Orchestrates the 4D Blog Engine. Use it when the user wants a blog post derived from a base
  document: a whitepaper, a report, a transcript, meeting notes. It routes to the four phase
  commands (blog-delegate, blog-describe, blog-discern, blog-diligence), to blog-social for
  multi-platform derivatives, and to the lifecycle commands, and it is where the active Cowork
  project and the per-piece working directory get resolved. Trigger it for anything touching the
  4D framework, the Release Owner Gate, or deriving a blog from a base document. Do not use it to
  write a post from scratch with no base document, to edit an already-published post, or to
  rewrite a document with no derivation target.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion]
---

# 4D Blog Engine — orchestrator

## When this skill applies

This skill should be used when the user asks to "write a blog post from this document", "derive a blog from this whitepaper / report / transcript / meeting notes", "run the 4D pipeline on this", "write a LinkedIn article + teaser from this", "make a Twitter thread from this blog", "write a Facebook post from my blog", "run the release-owner gate on my draft", or any request to turn a base document into a publication-ready blog post (and optional multi-platform social derivatives) under the 4D AI Fluency Framework. This skill is the orchestrator — it routes to the four phase commands (blog-delegate, blog-describe, blog-discern, blog-diligence), the social derivative command (blog-social), and the lifecycle commands. It is also the central place that detects the active Cowork project and computes the per-piece working directory. Trigger aggressively for anything touching deriving a blog from a base doc, the 4D framework, the Release Owner Gate, or producing multi-platform social derivatives. Do NOT use this skill for: writing a blog post from scratch with no base document; editing an existing published post; rewriting an arbitrary document with no derivation target.


> **Read this when:** any `/4d-blog-engine:*` command runs. This file is the spine; it routes work to the phase commands and computes the working directory. Read `references/4d-discipline.md` immediately after this file — every phase needs the framework loaded.

## What this skill does

This skill turns a base document plus a chosen angle/question into a publication-ready blog post, plus optional multi-platform social derivatives (LinkedIn article + teaser, Twitter thread, Facebook post) — under the 4D AI Fluency Framework from MoxyWolf's *Beyond the Prompt* whitepaper.

It is composed of twelve commands, all prefixed `blog-` for consistency: four map directly to the four D's (delegate / describe / discern / diligence), four lifecycle commands (init / voice / start / publish), `blog-pillar` (manage hub-and-spoke pillars + linking maps), the end-to-end pipeline shortcut, the social derivative, and the status report. Every new post chooses a publishing **target** (`targets/*.md`) and a **pillar** before drafting — see STEP 1.5.

| Command | Purpose | Specialist skill invoked |
|---|---|---|
| `/4d-blog-engine:blog-init` | One-time setup — declare the blog project dir + GitHub repo + author + hero scene palette | `blog-init` |
| `/4d-blog-engine:blog-voice` | One-time voice capture — 8-question interview, writes `<author-slug>-voice.md` | `blog-voice` |
| `/4d-blog-engine:blog-start` | Open or resume a session — mount the two directories, surface in-progress/unpublished pieces | `blog-start` |
| `/4d-blog-engine:blog-pillar` | Create or edit a pillar (hub) + its linking map — the hub of the hub-and-spoke model | inline (this skill) + `references/linking-map-template.md` |
| `/4d-blog-engine:blog-delegate` | Delegation — triage, angle pick, earned-secret stall | inline (this skill) |
| `/4d-blog-engine:blog-describe` | Description — voice interview, outline, At-a-Glance | reuses `research-pipeline/content-writer`'s 8-question interview |
| `/4d-blog-engine:blog-discern` | Discernment — 30-day sweep, draft, slop pass | `discourse-sweep`, `research-pipeline/*`, `council:deliberate`, `bibtex-builder` |
| `/4d-blog-engine:blog-diligence` | Diligence — Release Owner Gate | `release-owner-gate` |
| `/4d-blog-engine:blog-social` | Multi-platform social derivatives (LinkedIn article+teaser, Twitter thread, Facebook post) — opt-in, writer picks platforms. Writes to `<piece>/04-diligence/social/`. Re-run `/blog-publish` after to ship the files to the repo. | `blog-social` |
| `/4d-blog-engine:blog-pipeline` | End-to-end pipeline (all four phases sequentially; social derivation is NOT auto-invoked — run `blog-social` after) | all of the above |
| `/4d-blog-engine:blog-publish` | Ship a signed piece to the live site via the configured GitHub repo. Auto-includes any social derivatives that exist for the piece in the same commit. | `blog-publish` |
| `/4d-blog-engine:blog-status` | Print current piece state | inline (this skill) |

## STEP 0 — Always load these references first

When this skill is invoked, **immediately Read these files in this order before doing any other work**:

1. `${CLAUDE_PLUGIN_ROOT}/references/4d-discipline.md` — the framework, the gate definitions, the load-bearing rules.
2. `${CLAUDE_PLUGIN_ROOT}/references/ai-anti-patterns.md` — the slop catalog (two-tier).
3. **The writer's voice profile** — resolved by globbing `<blog-project-dir>/*-voice.md` (after walking up from CWD to find `blog-project-instructions.md`). The multi-voice resolution:

   - **Zero voice files:** halt with *"No voice profile found in `<blog-project-dir>`. Run `/4d-blog-engine:blog-voice` to create one, then retry."* The plugin never falls back to any preset.
   - **One voice file:** use it. Report the author name (from frontmatter) and the file path in the STEP 0 voice-load report.
   - **Two or more voice files:** ask the writer via `AskUserQuestion` which voice to use for this post. Options are one-per-voice-file, labeled with the author name from each file's frontmatter. After they pick, proceed with that file.

   The voice profile is per-writer and per-blog; the plugin never falls back to any preset.

**Report back to the user** what was loaded (voice tone, sentence-length range, contraction rate target, fragment frequency, conjunction-starter frequency, top forbidden phrases). Silent loading causes voice drift in long sessions. This is the jamon8888/cc-suite STEP 0 LOAD DNA discipline — never skip the report-back.

## STEP 1 — Detect the active project and compute the working directory

The plugin saves everything into the active project's directory using a standardized structure. There are **two supported project markers**, in this priority order:

1. **MoxyWolf-internal marker:** `<project>/00 – Project Hub/cowork-project-instructions.md` (full MoxyWolf Cowork project)
2. **External blog marker:** `<project>/blog-project-instructions.md` (slim blog-only setup created by `/4d-blog-engine:blog-init`)

The discovery walk checks for both at every ancestor directory, MoxyWolf-internal first. Whichever it finds first determines the project mode:

- **MoxyWolf mode** → posts land at `<project>/12 – MARCOM/Posts/<slug>/` (the MoxyWolf MARCOM convention).
- **External-blog mode** → posts land at `<project>/Posts/<slug>/` (the slim convention, no numbered folders).

Implement with Bash. **Numbered MoxyWolf project folders may use either an en-dash (`–`, U+2013) or a plain hyphen (`-`, U+002D) as the separator** — folders 00-09 + 99 typically use en-dash; folders 11-12 (Project Knowledge + MARCOM) sometimes use hyphen depending on when they were created. Path resolution must tolerate both:

```bash
# tolerant of en-dash (U+2013) and hyphen (U+002D) in numbered folder names
find_active_project() {
  local d="$PWD"
  while [ "$d" != "/" ]; do
    # MoxyWolf-internal marker — checked first
    for sep in '–' '-'; do
      if [ -f "$d/00 ${sep} Project Hub/cowork-project-instructions.md" ]; then
        echo "moxywolf:$d"; return 0
      fi
    done
    # External-blog marker — checked second
    if [ -f "$d/blog-project-instructions.md" ]; then
      echo "blog:$d"; return 0
    fi
    d="$(dirname "$d")"
  done
  # Standard fallback locations for external blog mode
  for fallback in "$HOME/Documents/MyBlog" "$HOME/Blog"; do
    if [ -f "$fallback/blog-project-instructions.md" ]; then
      echo "blog:$fallback"; return 0
    fi
  done
  echo "fallback:$HOME/4d-blog-engine-work"
}

# Returns the per-piece base directory for the resolved project + mode.
# - MoxyWolf mode: <project>/12 – MARCOM/Posts (creates the MARCOM folder if absent, en-dash form)
# - External-blog mode: <project>/Posts
# - Fallback mode: <fallback>/Posts
resolve_posts_dir() {
  local raw="$1"          # "moxywolf:<path>" | "blog:<path>" | "fallback:<path>"
  local mode="${raw%%:*}"
  local proj="${raw#*:}"
  case "$mode" in
    moxywolf)
      for d in "$proj"/12\ *MARCOM "$proj"/12-MARCOM; do
        [ -d "$d" ] && { echo "$d/Posts"; return 0; }
      done
      local dest="$proj/12 – MARCOM"
      mkdir -p "$dest/Posts"
      echo "$dest/Posts"
      ;;
    blog|fallback)
      mkdir -p "$proj/Posts"
      echo "$proj/Posts"
      ;;
  esac
}

RAW=$(find_active_project)
PROJECT_MODE="${RAW%%:*}"          # moxywolf | blog | fallback
ACTIVE_PROJECT="${RAW#*:}"
POSTS_DIR=$(resolve_posts_dir "$RAW")
```

**Report the resolved project to the user** in one line, with the mode explicit:

- MoxyWolf mode: `Active project: <name> (MoxyWolf — <path>)`
- External-blog mode: `Active blog project: <name> (<path>)`
- Fallback: `No project found — falling back to $HOME/4d-blog-engine-work. Run /4d-blog-engine:blog-init to set up a real blog project.`

The per-piece working directory is `<POSTS_DIR>/<YYYY-MM-DD-slug>/`. The slug is computed from the chosen post title (kebab-cased, ASCII, ≤40 chars, leading articles dropped).

Create the per-piece directory tree at the start of the run:

```
<piece>/
├── state.md
├── 01-delegation.md         # Phase 1 writes
├── 02-description.md        # Phase 2 writes
├── 03-discernment/          # Phase 3 writes
└── 04-diligence/            # Phase 4 writes
```

The `state.md` template lives at the bottom of this file.

## STEP 1.5 — Choose the publishing target and the pillar

Runs at the start of any new-post flow (`blog-pipeline`, `blog-delegate`), after
STEP 1 and **before Phase 1**. Skip it for commands operating on an existing
piece (`blog-publish`, `blog-social`, `blog-status`) — they read `target` and
`pillar` from the piece's `state.md`.

This is the hub-and-spoke entry point. Every blog post is a **spoke** on exactly
one **pillar** — the engine makes that non-optional. The model is generalized
from `Taskade/Team Plugins/11 - Project Knowledge/methodology-hub-and-spoke-linking-map-2026-06-14.md`.

**1. Target.** Load the publishing-target registry by globbing
`${CLAUDE_PLUGIN_ROOT}/targets/*.md` (see `targets/README.md` for the schema).
Ask which target via `AskUserQuestion`, one option per descriptor (label =
`project`). Read the chosen `targets/<name>.md`. If its `status: register-only`,
say now that the post will be drafted, formatted, and added to the linking map,
but the descriptor's site-side checklist must close before it renders live —
surface that here, don't surprise the writer at publish.

**2. Folder.** Default to the descriptor's `content_dir`; let the writer override.
Record the resolved folder.

**3. New pillar or existing pillar — mandatory.** Ask via `AskUserQuestion`:
**new pillar** or **existing pillar**? There is no "no pillar" path.

- **Existing pillar** → glob the target's `linking_map_dir` for `*.md`, read each
  frontmatter, present the list (pillar title — hub URL — spoke count). The writer
  picks one. Record `pillar: <slug>`.
- **New pillar** → run the `/blog-pillar new "<title>"` logic inline: derive the
  slug, set `hub_url` from the descriptor's `pillar_route_pattern`, ask the **hub
  term** (the phrase whose first mention auto-links to the hub), create the
  linking map from `references/linking-map-template.md` in the target's
  `linking_map_dir`, and **register the term** with `scripts/hub_term.py register`
  (BP-001), run from the device's macOS shell:
  `python3 "$CLAUDE_PLUGIN_ROOT/scripts/hub_term.py" register --hub-links <GitHub root>/hub-links --term "<term>" --owner <owner> --site-url <SITES url for owner> --path <path>`.
  It adds the site and the `{ pattern, owner: <hub_links_site_slug>, path }` entry,
  adds a test, builds and tests hub-links, and commits, pushes and pulls back as
  `moxywolf-agent`. Exit 1 halts the pipeline with the script's reason. Nobody is
  asked to rebuild, push or tag; `/blog-publish` pins the new head in the target.
  Record `pillar: <slug>`. This post is the pillar's first spoke.

**4. Record to state.** Write `target`, `target_status`, `content_folder`,
`pillar`, `pillar_why` (the linking map's `why:` belief statement — omit if the
map predates the field), and `hub_url` into the piece's `state.md` frontmatter
so every later phase and the publish step inherit them.

**Carried into later phases:**

- Phase 2/3 (drafting) ensure the pillar's `hub_term` appears in the body at least
  once. Every target's `auto_linker` (the `@moxywolf/hub-links` adapter) links the
  first mention at **build time**, so do **not** hand-insert the first-mention link
  — just mention the term, and vary anchor text where it recurs. (DR-079: link at
  render time, not authoring time.)
- Phase 2 (outline) and Phase 3 (drafting) treat `pillar_why` as the piece's
  belief anchor when present: the opener flows inside-out (belief or its villain
  first, approach second, artifact last — Sinek's Golden Circle ordering), and no
  claim in the body may contradict the `why`. The post's thesis is a *specific
  argument for* the pillar's belief, not a restatement of it.
- Phase 4's Release Owner runs the **Celery Test** against `pillar_why` when
  present — see `references/release-owner-rubric.md`, hand-check 4.
- Phase 4 / `blog-publish` registers this spoke in the pillar's linking map and adds
  the "Part of *<Pillar>*" note + an explicit "Read the full *<Pillar>* →" CTA (not
  the auto-linked first mention), and — for `register-only` targets — prints the
  site-side gaps blocking a clean render.

## STEP 2 — Route the command

After STEP 0, STEP 1, and STEP 1.5, route to the requested phase. Each phase has its own skill or inline workflow described below. **Phases enforce ordering via the `_phase` and `_status` fields in their output frontmatter** — Phase N+1 refuses to run if Phase N didn't pass or if more than 24 hours have elapsed since Phase N passed. Don't try to defeat this — it's the engineered gate the whole plugin exists for.

### Phase 1 — Delegation (inline)

Triggered by `/4d-blog-engine:blog-delegate <base-doc>` or as the first step of `/4d-blog-engine:blog-pipeline`.

**Workflow:**

1. **Locate the base document.** `<base-doc>` can be: a file path (absolute or relative to CWD), a URL, or pasted text supplied in a prior message. If a URL, use WebFetch (after checking the provenance set) or Claude in Chrome. If a file, Read directly. If pasted, use as-is.
2. **Classify the doc type** (LLM judgment): blog post / whitepaper / meeting notes / transcript / report / email / braindump / code commit log / other. State the classification in one line.
3. **Capability triage** — apply a fast yes/no test from `references/4d-discipline.md` (Delegation section): does this topic warrant a post against the jagged frontier? If NO, surface the one-line reason and exit with a clean message ("Triage NO: topic falls outside the model's reliable frontier — recommend a manual brief instead").
4. **Angle elicitation.** If the user supplied an angle, restate it and confirm. If not, propose 3-5 candidate angles via `AskUserQuestion`. Each angle = one-sentence thesis + audience + a slot for the earned secret. Angles must be genuinely different (not three rephrasings).
5. **Earned-secret stall — enforce these deterministic checks before accepting any answer.** This stall is the most load-bearing gate in the framework. An LLM judging "is this concrete?" by feel has been observed to accept weak answers from non-Dorian writers because the model defaults to politeness. Run these checks explicitly:

   **Reject the answer if any of these are true:**

   - Length under 80 characters (real lived experience can't fit; the writer is brushing the question off)
   - Contains zero of: a number, a date, a named person, a named company/product, a specific event location, a specific dollar amount, a specific duration. (Concrete artifacts are required. *"It surprised me how often I see this"* has no artifact; *"In April 2025 our team ran a 30-person experiment"* has three.)
   - Pattern-matches one of these platitude shapes:
     - *"I want to help [audience]"* / *"My goal is to..."* — that's an intention, not experience.
     - *"I think it's important that..."* — that's an opinion, not experience.
     - *"In my experience, [generic claim with no specifics]"* — uses the words but has no artifact.
     - *"As [a role], I've seen [generic pattern]"* — credentials don't count as experience for this question.
     - Anything starting with *"It's interesting that..."* / *"It's worth noting that..."* — both AI-prose tells and evasions.

   **On reject (round 1):** paraphrase the question with a concrete prompt:

   > *That's the kind of thing you might have read. The question is asking for something specific you LIVED through. A moment, a number, a person who said something to you, a thing that broke. What did YOU do, see, or measure that the reader hasn't?*

   **On reject (round 2):** narrow further with a multiple-choice-style nudge:

   > *Try answering one of these instead of the open question: (a) a recent experiment you ran with a number attached, (b) a customer or colleague who said something specific that changed how you think about this, (c) a moment when you tried the advice you'd normally give and it didn't work, (d) a thing you noticed in your data that surprised you.*

   **On reject (round 3):** hard-block. Write to `state.md` frontmatter `_status: blocked, _block_reason: no earned secret after 3 rounds` and exit Phase 1 with:

   > *I can't find a concrete lived-experience anchor for this piece. The framework's design says the post will read as generic restatement without one. Two paths from here: (a) write a different post — one you have a specific story for, (b) go run the experiment or have the conversation that gives you the story, then come back. Both are legitimate. The plugin won't generate a post without an earned secret.*

   The 3-round hard cap is intentional. The writer can re-invoke `/4d-blog-engine:blog-delegate` later when they have a real answer.

   **On accept:** record the earned secret in `01-delegation.md` frontmatter as `earned_secret: <one line summary>` and proceed. Save the full answer in the body of `01-delegation.md` for downstream phases to anchor against.
6. **Modality decision.** Ask which modality (automation / augmentation / agency, default automation) — see `references/4d-discipline.md`. Most pieces are automation: the plugin drafts, the human signs.
7. **Write `01-delegation.md`** with frontmatter `_phase: 01, _status: passed, _timestamp: <ISO-8601>, earned_secret: <one line>, modality: <choice>`. Body: base doc location, doc type, angle, candidate angles considered + why rejected, audience persona (forced to specifics — name, role, recent context, frustration).

### Phase 2 — Description

Triggered by `/4d-blog-engine:blog-describe` or as Phase 2 of `:blog`. Refuses to run if `01-delegation.md`'s `_status` isn't `passed` or its timestamp is >24h old.

**Workflow:**

0. **Media-file caption capture (new in v0.5.7).** Before the voice load and interview steps, scan `<blog-project-dir>/drafts/blog-media/` for files. Read the base-doc's YAML (if any) for an existing `media:` array — those entries are already captioned, skip them. For each file in `drafts/blog-media/` that is NOT yet referenced in the YAML, ask the writer one question per file via separate messages (not a single bulk question):

   > *I see `<basename>` in your `drafts/blog-media/` folder. What's the caption for it? (Short description shown alongside the download link in the post.)*

   Record each (basename, caption) pair. Persist to `<piece>/state.md` frontmatter under:

   ```yaml
   media:
     - file: /blog-media/<basename>
       caption: <writer's caption>
   ```

   This `media:` block in state.md is the canonical list Phase 3's `content-writer` reads when generating the YAML in the signed `blog.md`. The outline step (step 4 below) can also use the media list to plan where in the post to introduce each file.

   If `drafts/blog-media/` has no files, this step is a no-op — proceed silently.

   If the writer wants to skip captioning a file (because they don't want it in this post), accept a `(skip)` answer and DON'T add it to state.md's media list. The file stays in `drafts/blog-media/` but won't be referenced or copied at publish time.


1. **Phase 1 → Phase 2 carry (v0.1.1+).** Before invoking the voice interview, read `<piece>/01-delegation.md`'s `earned_secret` field and the `angle` + `audience` blocks. Scan the earned-secret text for content matching each of the 8 voice-injection slots:

   - **Trigger** — a recent event that prompted the topic
   - **Evidence** — a specific number, fact, or anecdote that grounds the claim
   - **Contrarian Take** — the "but actually" the post pushes against
   - **Authority** — why this author specifically gets to say this
   - **Specific Reader** — the named persona the post is for (also drawn from the audience block)
   - **Business Connection** — how it connects to the author's product/service
   - **Call to Action** — the Monday move the reader should make
   - **Emotional Core** — the visceral phrase or image that sticks

   For each slot where a substantive match is detectable, pre-fill a draft answer. Present the pre-filled set to the user with one confirmation message: *"Based on your earned secret + angle, I have draft answers for: [Trigger, Evidence, Emotional Core, ...]. Use these, refine them, or re-ask?"* If the user accepts, skip the corresponding slots in step 2. If the user wants to refine, capture the refinement. If the user wants to re-ask, queue that slot for step 2.

   This step exists because the Phase 1 earned-secret answer frequently substantively answers Trigger, Evidence, and Emotional Core — re-asking those wastes the user's turns and risks thinner second-pass answers.

2. **Voice interview (carried slots skipped).** For any of the 8 voice-injection slots NOT pre-filled in step 1, ask the question from `research-pipeline/content-writer`'s set (Trigger / Evidence / Contrarian Take / Authority / Specific Reader / Business Connection / Call to Action / Emotional Core). **One question per message.** Push back on vague answers; the discipline of specifics is what makes the rest work.
3. **Pick the structure.** Default: Sorkin DOB (Desire / Obstacle / Battle). Alternatives: Hero's Journey, Story Circle, Inverted Pyramid. State the choice and explain why.
4. **Build the outline.** H2-by-H2, 60-70% of H2s phrased as natural questions per `references/aeo-checklist.md`. Per-section word budget. Per-section evidence-mapping ("what does the 30-day sweep need to find for this section?"). Per-section "what's the citation capsule's load-bearing claim?"
5. **Draft the "At a Glance" block.** 60-90 words. Self-contained. Takes a point of view. Use the template in `references/aeo-checklist.md`.
6. **Pre-load the anti-slop catalog.** Read `references/ai-anti-patterns.md` in full; state in one line which Tier-2-Major patterns you'll specifically guard against in this piece's prose.
7. **Write `02-description.md`** with frontmatter `_phase: 02, _status: passed, _timestamp: <ISO>`. Body: voice interview Q&A (including carried slots, marked as carried-from-Phase-1), structure choice + reason, outline (H2s with section budgets and evidence needs), At-a-Glance block, anti-slop watch list.
8. **Gate.** Show the outline + At-a-Glance to the user and ask "proceed / revise <specific>". Cap at 2 revision rounds before escalating.

### Phase 3 — Discernment

Triggered by `/4d-blog-engine:blog-discern` or as Phase 3 of `:blog`. Refuses to run on stale Phase 2.

**Workflow:** Hand off to the `discourse-sweep` skill (in this plugin) for steps 1-2, then call `research-pipeline/content-writer` for the draft, then `prose_lint.py` and the Tier-2 LLM sub-agent for the slop pass. Detailed orchestration is in `skills/discourse-sweep/SKILL.md` and the discern command file.

The orchestrator's responsibility in Phase 3: **chain the sub-skills in order**, persist each step's artifact in `<piece>/03-discernment/`, and surface the slop letter grade to the user at the end. If grade ≤ C, force a re-rewrite. If grade = D or F, abort the phase and require a structural rethink.

**Signature devices.** Before running `prose_lint.py`, read the writer's voice profile and collect the devices it names as signature constructions. Pass them through: `--signature-devices contrast-framing,three-beat-reveal`. On a piece over ~900 words those counts become advisories and rhetorical *density* is scored instead — see `references/ai-anti-patterns.md` §"Long-form allowance for signature devices". Omitting the flag re-applies the raw-count rule that made a writer's own published work ungradeable, which is the failure this allowance was built to fix.

**When a rewrite scores worse than the draft it replaced, stop.** A rising second-pass score means the findings are being satisfied literally — punctuation laundered, devices traded between columns — not structurally. Restart from outline instead of patching a third time.

### Phase 4 — Diligence

Triggered by `/4d-blog-engine:blog-diligence` or as Phase 4 of `:blog`. Refuses to run on stale Phase 3.

Hand off entirely to the `release-owner-gate` skill (in this plugin). Detailed orchestration is in `skills/release-owner-gate/SKILL.md`. Phase 4 is non-trivial — read that skill's instructions in full before invoking it.

### Derivative — Social posts (multi-platform)

Triggered by `/4d-blog-engine:blog-social` on an existing Diligence-passed blog. **Opt-in only** — social derivation is NOT auto-invoked by `:blog-pipeline` or by Phase 4 sign-off. The writer runs `blog-social` explicitly when they want derivatives, then picks which platforms (LinkedIn pair, Twitter thread, Facebook post) via `AskUserQuestion`. Hand off entirely to the `blog-social` skill.

## Status command

`/4d-blog-engine:blog-status [<piece-slug>]` — if no slug given, pick the most-recently-modified piece directory. Read its `state.md` and print: current phase, gates passed, next command to run, slop grade if Phase 3 ran, preflight verdict if Phase 4 ran. Useful when resuming a multi-day piece.

## state.md template

When STEP 1 creates the piece directory, write `state.md` with this structure:

```markdown
---
slug: <YYYY-MM-DD-kebab-title>
title: <title>
created: <ISO-8601>
active_project: <project name>
piece_dir: <absolute path>
current_phase: 01
gates_passed: []
target_words: 1500
modality: automation
earned_secret: <one line, filled by Phase 1>
---

# Piece state — <title>

## Progress

- [ ] 01 — Delegation
- [ ] 02 — Description
- [ ] 03 — Discernment
- [ ] 04 — Diligence
- [ ] LinkedIn pair derived

## Process log

(Each phase appends a one-line entry: `2026-05-25T16:13 — Phase 01 passed.`)
```

Every phase updates `current_phase` and appends to `gates_passed` when its gate passes. The status command reads from this file.

## Hard rules

- **Never publish an unsigned post.** After the Release Owner signs, `/blog-publish` commits, pushes, merges and verifies the live page itself (BP-001); the writer never pushes.
- **Never auto-publish to LinkedIn.** Phase 4 writes the article and teaser to disk; the user posts them by hand.
- **Never fabricate citations.** Tier 1-3 sources only; `[F]` data is forbidden in body; unverifiable claims get `[CITATION NEEDED]`.
- **Never skip the Release Owner Gate.** The gate is the whole point of the framework.
- **Never assume the active project.** Always run the discovery walk in STEP 1 and report the resolved project to the user.
- **Never load voice silently.** STEP 0 loads voice anchor + reports back what was loaded.
