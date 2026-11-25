---
name: thoth
version: 1.6.0
description: Build and maintain a unique, consistent LinkedIn voice for one or more users. Runs a framework-driven persona interview (brand archetypes + tone spectrum + hot-take exercises), then generates ready-to-publish LinkedIn posts across a 30/25/20/15/10 content mix (Personal / Work / Thought-leadership / Educational / Promotional). Handles multi-user installs — teams, agencies, or families can share one install with a persona per person. Trigger on any `/thoth` command, on phrases like "write a LinkedIn post", "draft a post for [name]", "help me sound more like myself on LinkedIn", "onboard me on Thoth", "set up my LinkedIn voice", or when the user asks for help building a personal brand / thought leadership on LinkedIn. Also trigger when the user references their own posting cadence, content calendar, or wants to regenerate a post. Use this skill instead of writing a generic LinkedIn post whenever the user has a Thoth persona on file.
---

# Thoth — LinkedIn Voice Skill

Named after the Egyptian god of writing, wisdom, and the spoken word. Thoth weighed the hearts of the dead against the feather of Ma'at — truth. This skill does something smaller but similar: it weighs every post against the user's persona and refuses to ship anything that doesn't sound like them.

## What this skill does

1. **Onboards** a user through a 20–30 minute interview grounded in proven voice/personality frameworks.
2. **Stores** each user's persona, topic bank, posting history, and preferences in a portable folder inside the skill.
3. **Generates** LinkedIn posts in that user's voice, aligned to a 30/25/20/15/10 content mix, using the story-arc and post-type frameworks documented here.
4. **Regenerates** on demand with or without feedback.
5. **Schedules** a recurring daily prompt that asks the user what's on their mind and drafts today's post.
6. **Optionally** reads a local git repo for POV context only — never to promote the repo or code.

Output is always **copy-ready post text**. Thoth never publishes to LinkedIn on its own. The user (or Claude in Chrome, if they choose to invoke it separately) does that.

---

## Where persona data lives

Persona data — `personas/<name>/persona.md`, drafts, history, recent inputs — is **mutable user data** and lives **outside** the skill folder. The skill itself (this `SKILL.md`, `references/`, `scripts/`) is immutable code and stays at `~/.claude/skills/thoth/`. Separating them lets the user grant blanket read/write on the data root without exposing Claude's own config files.

### Resolving the data root

On every `/thoth ...` invocation, resolve the **data root** in this order:

1. If `./.thoth/personas/` exists relative to the current working directory → data root is `./.thoth/` (per-project mode — useful for teams checking personas into a project repo).
2. Else if `~/.thoth/personas/` exists → data root is `~/.thoth/` (global mode, default).
3. Else if a legacy install exists at `~/.claude/skills/thoth/personas/` and migration has been declined this session → data root is `~/.claude/skills/thoth/` (legacy mode — see migration below).
4. Else → create `~/.thoth/personas/` and use it. This is the default landing place for new installs.

Throughout this document, any path written as `personas/<name>/...` resolves to `<data-root>/personas/<name>/...`. The `personas/.active` file lives at `<data-root>/personas/.active`.

### One-time migration from the legacy location

Before v1.1, Thoth stored persona data inside `~/.claude/skills/thoth/personas/`. On the first `/thoth ...` invocation after upgrade, check for legacy data and offer to move it:

1. **Trigger condition.** All of these are true:
   - `~/.claude/skills/thoth/personas/` exists and contains at least one persona subfolder (not just `.active` or the template).
   - `~/.thoth/personas/` does **not** exist.
   - `./.thoth/personas/` does **not** exist relative to CWD.
2. **Prompt the user once per session:**
   > *"Found existing Thoth personas at the legacy location `~/.claude/skills/thoth/personas/`. Newer versions store persona data in `~/.thoth/` instead — outside Claude's config root, so you can grant blanket read/write without affecting Claude's own settings. Move now? (yes / not now)"*
3. **On `yes`:**
   - Create `~/.thoth/` if it doesn't exist.
   - `mv ~/.claude/skills/thoth/personas ~/.thoth/personas`.
   - Write a one-line breadcrumb at `~/.claude/skills/thoth/personas-MIGRATED.md` containing the date and the new location, so anyone inspecting the old path knows what happened.
   - Confirm: *"Moved. Data root is now `~/.thoth/`. The skill itself is still at `~/.claude/skills/thoth/`."*
4. **On `not now`:** Continue using `~/.claude/skills/thoth/personas/` as the data root for this session (legacy mode). Ask again on the next invocation.

The migration is idempotent — once moved, the trigger condition fails on future invocations and the prompt does not appear.

### Quick reference

| Concept | Path |
|---|---|
| Skill code (immutable) | `~/.claude/skills/thoth/` |
| Data root — global default | `~/.thoth/` |
| Data root — per-project | `./.thoth/` (when present in CWD) |
| Data root — legacy (pre-v1.1) | `~/.claude/skills/thoth/` |
| Active persona pointer | `<data-root>/personas/.active` |

---

## Commands

All commands are of the form `/thoth [subcommand] [args...]`. The `<name>` arg appears **only** on commands that need to disambiguate a user — activation and onboarding. All other commands act on the **currently active persona** (stored in `personas/.active`).

| Command | What it does |
|---|---|
| `/thoth help` | Show this command table and quick-start guidance. |
| `/thoth <name>` | **Activate** that persona. Subsequent commands run for this user until another is activated. First run also creates the persona folder. |
| `/thoth onboard` | Run the full persona interview for the active user. Required before generating posts. |
| `/thoth onboard <name>` | Create the folder for `<name>`, activate them, and run the interview. |
| `/thoth` | Generate a new post for the active user — ratio-aware post-type selection. |
| `/thoth <type>` | Force a specific post type. `<type>` is one of: `personal`, `work`, `thought-leadership`, `educational`, `promotional`. Overrides ratio-aware selection but still logs to history. |
| `/thoth daily` | One-shot daily flow: ask "anything interesting happen?", integrate the answer, draft today's post. |
| `/thoth regenerate` | Redraft the most recent post. |
| `/thoth regenerate <feedback>` | Redraft with steering, e.g. `/thoth regenerate shorter, less corporate`. |
| `/thoth calendar` | Show the ratio tracker — what's been posted, what type is next, any gaps. |
| `/thoth edit` | Open the active user's persona for editing. |
| `/thoth list` | List all personas on this install. |
| `/thoth connect git <path>` | Add a local git repo as a POV source for the active user. Read-only. Never promoted. See `references/git-safety.md`. |
| `/thoth disconnect git <path>` | Remove a git source. |
| `/thoth schedule [HH:MM]` | Set up a recurring daily run that writes a draft to `inbox/` and pings the user. Default 08:30 local time. |
| `/thoth unschedule` | Cancel the recurring schedule. |
| `/thoth inbox` | List drafts produced by scheduled runs that are awaiting review. `/thoth inbox <date>` opens a specific one; `/thoth inbox accept` / `reject` / `regenerate` handles a draft. |
| `/thoth image [<date>] [--variant <name>]` | Render the post as an animated GIF (portrait 1080×1350, inside LinkedIn's <5 MB / <400-frame envelope). Auto-picks the template from content; override with `--variant`. Pass a `.png` output for a static frame. Output to `<data-root>/exports/`. |
| `/thoth brand` | View / edit the active persona's visual identity (`brand.yaml`). First run auto-derives it from the persona's archetype + tone (no interview); `/thoth brand setup` runs the explicit colour interview. |
| `/thoth recover` | Scan past Claude session logs for persona content and restore it to the current data root. Use after an upgrade that wiped your persona data (e.g. `amskills update` from a v1.0.x install). |
| `/thoth update` | Check for a newer Thoth release and upgrade in place. Persona data is independent of the skill folder — never touched. |
| `/thoth version` | Print the installed Thoth version and where the skill + data live. |
| `/thoth frameworks` | Browse the framework catalog (20 frameworks across the 5 post types) and the hook-pattern library. Read-only. |

### Command dispatch

On receiving any `/thoth ...` invocation, follow these steps in order:

1. **Resolve the data root** using the algorithm in "Where persona data lives" above. If a legacy install at `~/.claude/skills/thoth/personas/` is detected and the user hasn't been prompted this session, run the one-time migration offer before continuing.
2. **Parse** the subcommand. Unknown subcommand → show `help`.
3. **Resolve the active persona** by reading `personas/.active` (single line with the username). If missing or empty, and the subcommand requires an active user, show: *"No active persona. Run `/thoth <name>` to activate one, or `/thoth list` to see who's on this install."*
4. **Check the persona is onboarded** — `personas/<name>/persona.md` exists and is marked `STATUS: ACTIVE`. If not, route to `onboard` first.
5. **Dispatch** to the relevant section below.

### `/thoth <name>` — activate

- Ensure `personas/<name>/` exists; create it if not, copying from `references/persona-template.md`.
- Write `<name>` to `personas/.active` (overwriting previous).
- If this is a fresh persona (`STATUS: DRAFT`), automatically offer: *"I don't have a persona on file for `<name>`. Want to run onboarding now? (yes / later)"* — yes → go to `/thoth onboard`.
- Confirm: *"`<name>` is now active."*

### `/thoth onboard` — run the interview

Read `references/onboarding-interview.md` in full. Follow it **end-to-end without skipping sections**. The interview produces `personas/<active>/persona.md` with the canonical persona document. When the interview completes, set `STATUS: ACTIVE` in the file header.

### `/thoth` (generate a post)

Selection runs in four ordered steps before drafting begins. The full algorithm with rotation windows and tie-breakers is in `references/content-mix.md` ("Selection algorithm"). Summary:

1. Read `personas/<active>/persona.md`, `history.yaml`, `topics.md`, and `recent.md`.
2. **Pick the type** using the ratio rules in `references/content-mix.md`.
3. **Pick the framework** — open `references/post-types.md` for the chosen type, filter the 4-framework catalog by last-4-used (rotation) and archetype/topic fit (from each framework's `Skip when` clauses), pick the strongest match. User can force one with `--framework <name>`.
4. **Pick the hook pattern** — read the chosen framework's `Compatible hooks` list, filter against `references/hook-patterns.md` for last-3-used and archetype fit, pick one. User can force one with `--hook <name>`.
5. **Pick the topic** — rotate pillar topics from `topics.md`, integrate any recent inputs in `recent.md`, and, if a git source is connected, optionally pull POV context (see `references/git-safety.md` — absolutely no repo/code promotion).
6. **Announce the picks** in one paragraph before drafting:
   > *"Today: Thought-leadership (10pp under target). Framework: `heretical-claim-receipts-stake` (5 posts since last used). Hook: `inverted-truism`. Topic: AI workflows vs prompt training. Drafting now."*
7. **Draft the post** using:
   - The voice in `persona.md` — including the `enneagram:` block's `voice_implications` if present (it grounds *why* the user writes; let it shape conviction and emotional register, not just surface tone).
   - The framework's `Shape` block from `post-types.md`.
   - The framework's default arc from `story-arcs.md`.
   - The hook pattern's `Shape` block from `hook-patterns.md`.
8. **Run the voice check** (see below) before emitting. One extra item in v1.2.0: *"Does the draft actually follow the chosen framework's shape, or did it slide into a generic Classic arc?"*
9. **Emit** the post text, with a final one-line meta footer:
   ```
   — type: <type> • framework: <framework> • hook: <hook> • topic: <short> • ~<wordcount> words
   ```
10. **Log** the new row to `history.yaml` with `date`, `type`, `framework`, `hook_pattern`, `topic`, `wordcount`, and save the draft to `personas/<active>/last-post.md` for regenerate.
11. **Attach a GIF infographic — automatic, no prompt required.** This is **not** an optional follow-up step and you must **never** stop to ask the user whether they want an image or wait for them to request one. Every `/thoth` post ships with a matching animated GIF in the **same turn** as the text — analyze the post, pick the template yourself, render it, and present text + GIF together. The only exceptions: the user passed `--no-image`, or no template fits cleanly (see the skip rule below). **The infographic must visualize the post's core POV — not decorate it.** Before choosing anything, name the post's central claim in one sentence (usually its hook/thesis); the card exists to make *that* land at a glance.
    1. **Ensure a brand.** If `personas/<active>/brand.yaml` is missing, auto-derive it (no interview) by running `derive-brand.js` against `persona.md` — see the `/thoth brand` default-behavior step. Explicit user colours, if any, override.
    2. **Pick the infographic type by the SHAPE OF THE POV** — match the form to how the argument is built, not to surface keywords:
       - one **magnitude / result** (a single number *is* the point) → `stat-card`
       - a **trend over time** (growth, a rising/falling curve) → `line-chart-card`
       - a **before/after or size gap** (a few values to weigh) → `bar-chart-card`
       - **2–3 options compared** across attributes (which to pick) → `comparison-card`
       - a **sequence of steps** (a how-to, "N things" in order) → `steps-card`
       - a **process with flow** (stages connected, cause→effect, branching) → `flowchart-card`
       - a **repeating loop** (a cycle that feeds itself) → `cycle-card`
       - a **chronology** (milestones, an evolution over time) → `timeline-card`
       - **depth / hierarchy** (nested levels, what's underneath) → `layers-card`
       - a **funnel or pyramid** (tiers that narrow) → `funnel-card`
       - **overlapping factors → an intersection** (the sweet spot) → `venn-card`
       - **two axes / four quadrants** (position on two dimensions) → `matrix-card`
       - a **position on a range** (this ↔ that, where things fall) → `spectrum-card`
       - a **collection of N ideas** (an unordered set / examples) → `grid-card`

       **Anti-default rule — do not reach for `grid-card`.** `grid-card` (the N×2 sticker grid) is the single most over-used template and the most common failure mode: almost any post *can* be flattened into "N ideas," so it becomes a lazy catch-all. It is a **last resort**, valid only when the items have genuinely **no order, no comparison, no trend, and no relationship** to one another. Before you may pick it, rule out — in this order — every richer shape:
       - Is there an **order or flow**? → `steps-card` / `timeline-card` / `flowchart-card` / `cycle-card`
       - Is anything being **compared or weighed**? → `comparison-card` / `bar-chart-card` / `matrix-card` / `spectrum-card` / `venn-card`
       - Is there a **number, magnitude, or trend**? → `stat-card` / `line-chart-card`
       - Is there **structure, depth, or narrowing**? → `layers-card` / `funnel-card`

       Only if all four are honestly "no" does `grid-card` win. A numbered list is `steps-card`, not `grid-card`. When two non-grid templates both fit, pick the one that dramatizes the *tension* in the POV. Across consecutive posts, actively vary the template — if the last post used a given card, prefer a different one when the fit is close. If nothing fits cleanly, skip the image rather than force a `grid-card` (or fall back to a static `headline-card`/`quote-card`).
    3. **Extract the POV into the template's fields** — the headline carries the post's central claim (often the hook), and the body elements are the *structure that proves it*, in the post's own words. Pull the punchiest 2–4 words as the pill/emphasis. The test: someone who reads **only the card** should walk away with the POV. Write the `content.json` to a temp file. (Per-template field rules are in `/thoth image`.)
    4. **Render the GIF** with the persona's `brand.yaml` via `render.js`, using a `.gif` output (portrait 1080×1350, inside LinkedIn's envelope):
       ```sh
       node ~/.claude/skills/thoth/scripts/render.js \
         --template <template> \
         --content /tmp/thoth-content-<rand>.json \
         --brand <data-root>/personas/<active>/brand.yaml \
         --out <data-root>/exports/<date>-image-<template>.gif
       ```
    5. **Present the post text PLUS the GIF path** as the attachment, and append the `exports:` row to `history.yaml` (same shape as `/thoth image`). Honor the image hard rules in `/thoth image`.

### `/thoth daily`

Two modes depending on how `/thoth daily` was invoked.

**Mode A — interactive (user-typed `/thoth daily`):**

1. Ask the user: *"Anything interesting happen today? A meeting, a win, a frustration, a thing you read, a conversation — doesn't have to be big. (or type 'skip')"*
2. Append the response to `personas/<active>/recent.md` with today's date.
3. Run the `/thoth` generate flow, weighting today's recent entry heavily in topic selection.
4. Log the post to `history.yaml` with `status: accepted` (interactive mode means the user is here — they implicitly accept by being part of the flow).

**Mode B — scheduled (invoked by `/thoth schedule`):**

Detect this mode by the presence of either:
- Environment variable `THOTH_SCHEDULED=1`, OR
- The trigger prompt containing the literal string `"[scheduled run]"`.

In Mode B, do not ask the user anything — there's no user attached. Behavior:

1. **Read context:** `persona.md`, `topics.md`, `history.yaml`, the last 7 days of `recent.md` entries.
2. **No interactive prompt.** Skip the "anything interesting happen today?" question.
3. **Topic seeding fallback chain:**
   - If `recent.md` has an entry from the last 24 hours → use it as the topic seed.
   - Else if `recent.md` has entries from the last 7 days → use the most recent one.
   - Else → fall back to **topic rotation** from `topics.md` + the active persona's `contrarian_beliefs` or `signature_grievances` if relevant to the rotated topic.
4. Run the normal **type → framework → hook → topic** selection (per `references/content-mix.md`), but with a soft preference for shorter post types (Personal, Promotional) on scheduled runs — the user is more likely to engage with a polished short draft than a 400-word thought-leadership wall they have to edit.
5. Generate the draft.
6. **Write to inbox**, not stdout:
   - Path: `<data-root>/inbox/YYYY-MM-DD.md` (use the scheduled day's date in the persona's configured timezone from `<data-root>/integrations/schedule.yaml`).
   - If a file at that path already exists today, append a `-2`, `-3` suffix — don't overwrite a draft the user might still be reviewing.
   - The file contains a YAML frontmatter block + the draft body:
     ```yaml
     ---
     status: pending-review
     date: 2026-05-25
     persona: nirvana
     type: thought-leadership
     framework: heretical-claim-receipts-stake
     hook: inverted-truism
     topic: AI workflows vs prompt training
     wordcount: 312
     generated_at: 2026-05-25T08:30:14+05:30
     ---

     <draft body>
     ```
7. **Append to `history.yaml`** with `status: pending-review`. This row is excluded from `/thoth calendar` ratio math until accepted (see `references/content-mix.md`).
8. **Fire a notification** using the rules in `integrations/schedule.yaml`:
   - `notification: macos` → run via Bash: `osascript -e 'display notification "Today's Thoth draft is ready. Run /thoth inbox to read it." with title "Thoth" sound name "Glass"'`
   - `notification: telegram` / `slack` / `discord` → use the `configure-notifications` skill's send action with channel and message.
   - `notification: none` → skip, but write `<data-root>/inbox/_unread` as a marker file so `/thoth inbox` can detect there's something new.
9. Update `integrations/schedule.yaml`'s `last_run` + `last_run_outcome` fields.

If anything in step 6–8 fails (write error, notification failure), still attempt the remaining steps — a draft that exists but didn't notify is recoverable; a missed notification with no draft is worse.

### `/thoth regenerate [feedback]`

1. Read `personas/<active>/last-post.md`.
2. Redraft the same topic and type, applying feedback if provided. If no feedback, vary the angle: if the previous draft opened with a question, try a scene opener; if it was a list, try prose; etc.
3. Overwrite `last-post.md`. Do **not** add a new row to `history.yaml` — the regenerate replaces, not appends.

### `/thoth calendar`

Read `history.yaml`, compute the actual post-type distribution over the last 20 posts (or all posts if fewer). Render a simple table:

```
Target    Actual   Type
30%       32%      Personal          ✓
25%       21%      Work              —
20%       25%      Thought-leadership ↑
15%       12%      Educational       —
10%        5%      Promotional       ↓
```

Then say which type is "next up" based on the ratio gap.

### `/thoth connect git <path>`

1. Confirm the path is a valid git repo (`git -C <path> rev-parse --is-inside-work-tree`).
2. Append the path to `personas/<active>/sources.yaml` under `git:`.
3. Restate the git safety rules to the user in one sentence: *"Thoth will read your git history to understand what you've been working on, but will never name the repo, quote code, or promote the work in posts."* Point to `references/git-safety.md` if they want the full rules.

### `/thoth schedule [HH:MM]`

Sets up a recurring daily run that produces an inbox draft and pings the user. Combines a cron trigger + notification configuration.

**Dispatch:**

1. **Time argument.** Default `08:30`. Accept any `HH:MM` 24-hour value. Reject ambiguous AM/PM strings.
2. **Timezone.** Read from the OS (`date +%Z`). If the user wants a different timezone (e.g. they travel), they can edit `integrations/schedule.yaml` after.
3. **Notification channel selection.** Check what's available, in this order:
   - Read `<data-root>/integrations/schedule.yaml` if it exists — honor any existing `notification:` setting.
   - Else check if `configure-notifications` skill has Telegram / Slack / Discord configured (look at its config or ask: *"Use your already-configured Telegram channel for daily notifications?"*).
   - Else default to `macos` on macOS, `linux-notify-send` on Linux, `none` elsewhere.
4. **Create or update `<data-root>/integrations/schedule.yaml`:**
   ```yaml
   enabled: true
   time: "08:30"
   timezone: "Asia/Kolkata"
   notification: macos
   inbox_path: ~/.thoth/inbox/
   schedule_id: <id from the cron tool used below>
   last_run: null
   last_run_outcome: null
   ```
5. **Create the cron job.** Try in this order:
   - If the OMC `schedule` skill is available, delegate to it: schedule a daily task with the prompt *"[scheduled run] Run /thoth daily for the currently active Thoth persona."* — the `[scheduled run]` marker triggers Mode B in `/thoth daily`. Store the returned schedule ID in `schedule.yaml`.
   - Else if `scheduled-tasks` MCP is available, use that.
   - Else write a native crontab entry that runs Claude Code in headless mode with the same prompt. Print the entry for the user to inspect.
6. **Create the inbox directory** if it doesn't exist: `mkdir -p <data-root>/inbox/`.
7. **Confirm to the user:**
   > *"Daily Thoth scheduled for 08:30 (Asia/Kolkata). Drafts will land in `~/.thoth/inbox/` and you'll get a macOS notification when one's ready. Run `/thoth inbox` to read it. Cancel anytime with `/thoth unschedule`."*
8. **Offer a dry run:** *"Want me to run one now as a test, so you can see what the daily output looks like?"* — on yes, run `/thoth daily` in Mode B once immediately (with today's date suffix `-test` so it doesn't collide with tomorrow's real run).

The skill resolves the active persona itself when the scheduled task fires — don't bake a data-root path into the prompt, since the data root is resolved at runtime per the rules in "Where persona data lives."

### `/thoth unschedule`

1. Read `<data-root>/integrations/schedule.yaml`. If missing or `enabled: false`, tell the user there's nothing to cancel.
2. Cancel the cron job by ID (whatever tool was used to create it — `schedule` skill, `scheduled-tasks`, or crontab).
3. Update `schedule.yaml` to `enabled: false` (don't delete the file — keep last_run history).
4. Confirm: *"Daily Thoth cancelled. Existing inbox drafts are unaffected. Run `/thoth schedule` again to reactivate."*

### `/thoth inbox` — review scheduled drafts

Read-by-default; act on the user's confirmation.

**No arguments — list mode:**

1. Resolve the data root.
2. List every file in `<data-root>/inbox/` sorted by date descending. For each, show: date, type, framework, hook, topic, wordcount, status.
3. Output as a compact table. Highlight the most recent `pending-review` row.
4. If the `_unread` marker file exists, surface a leading line: *"You have N new drafts to review."*

```
Thoth inbox — 3 drafts

  ● 2026-05-25   thought-leadership   heretical-claim   inverted-truism   312w   PENDING
    2026-05-24   personal             quiet-reveal       micro-confession   180w   ACCEPTED
    2026-05-23   work                 decision-log       constraint-reveal  248w   REJECTED

Run /thoth inbox 2026-05-25 to read the pending draft.
```

After listing, clear `<data-root>/inbox/_unread`.

**`/thoth inbox <date>` — open a draft:**

1. Read `<data-root>/inbox/<date>.md`.
2. Render the body (omit the YAML frontmatter from display, but keep it in the file).
3. After rendering, ask: *"Accept, regenerate, or reject? (a/r/x or 'edit' to open in $EDITOR)"*

**`/thoth inbox accept [<date>]`:**

1. If no date, default to the most recent `pending-review` draft.
2. Update the inbox file's frontmatter: `status: accepted`.
3. Copy the draft body to `personas/<active>/last-post.md` (so `/thoth regenerate` works on it).
4. Update the matching `history.yaml` row: `status: accepted`. Now it counts toward the `/thoth calendar` ratio math.
5. Confirm: *"Accepted. Draft is in `last-post.md`. Copy & post when ready."*

**`/thoth inbox reject [<date>]`:**

1. Update inbox file frontmatter: `status: rejected`.
2. Update `history.yaml` row: `status: rejected`.
3. Confirm. Don't delete the file — keep for record.

**`/thoth inbox regenerate [<date>] [<feedback>]`:**

1. Update inbox file frontmatter: `status: regenerating`.
2. Run the normal `/thoth regenerate` flow on that draft, with optional feedback.
3. Overwrite the inbox file body with the new draft (frontmatter status returns to `pending-review`).

**`/thoth inbox cleanup`:**

1. Archive all `accepted` or `rejected` drafts older than 30 days into `<data-root>/inbox/archive/YYYY-MM/`.
2. Don't touch `pending-review` drafts regardless of age — those are still waiting on the user.

### `/thoth image [<date>] [--variant <name>]` — render a single image

Renders an **animated GIF** from a post draft, at **portrait 1080×1350 (4:5)** — LinkedIn's max feed real estate. The GIF is held inside LinkedIn's animation envelope (**under 5 MB, under 400 frames**); `render.js` logs `LinkedIn envelope: frames/size OK` and exits non-zero if either limit is breached. Output mode is chosen by the `--out` extension: a `.gif` path renders the animation; a `.png` path still renders a single static frame instead. Uses `skill/scripts/render.js` (Puppeteer-core + system Chrome; GIF encoding via gifski if installed, else ffmpeg two-pass palette).

**Resolve the source draft:**

1. If `<date>` is provided → read `<data-root>/inbox/<date>.md` (frontmatter + body).
2. Else → read `<data-root>/personas/<active>/last-post.md`.
3. If neither exists, tell the user and stop.

**Pick the template** unless `--variant` was passed. The 14 animated templates and what each is best for:

| Source content signal | Template | Best for |
|---|---|---|
| A single striking number with a claim (e.g. "3×", "73%", "$1.4M") | `stat-card` | One big number that counts up |
| A trend / growth over time (a rising or falling curve) | `line-chart-card` | A line+area curve that draws in + a count-up result |
| A before/after or size gap (a few values to weigh) | `bar-chart-card` | Bars that grow + count-up |
| 2–3 options compared across attributes (which to pick) | `comparison-card` | A decision table with an accent "winner" column |
| A numbered list / "N things" / "N ways" in order | `steps-card` | Numbered sticker cards with a pill lockup |
| A process with flow (stages, cause→effect, branching) | `flowchart-card` | Node boxes joined by drawn-in arrows |
| A repeating loop / cycle that feeds itself | `cycle-card` | Stages around a ring with looping arrows |
| A chronology / milestones / an evolution | `timeline-card` | A vertical timeline of dated events |
| A layered or nested framework (depth, what's underneath) | `layers-card` | Concentric framework rings |
| A funnel or pyramid (tiers that narrow) | `funnel-card` | Stacked width-stepped tiers |
| Two overlapping factors → an intersection (the sweet spot) | `venn-card` | Overlapping circles with a center insight |
| Two axes / four quadrants (position on two dimensions) | `matrix-card` | A 2×2 with an accent "winner" quadrant |
| A position on a range (this ↔ that, where things fall) | `spectrum-card` | Markers placed along an axis |
| A collection of N ideas / examples (unordered) | `grid-card` | A grid of idea cards with a colour sweep |

**Anti-default rule — `grid-card` is a last resort.** The N×2 sticker grid is by far the most over-selected template: nearly any post can be flattened into "N ideas," so it becomes a lazy catch-all and the renders end up monotonously similar. Pick `grid-card` **only** when the items have genuinely no order, no comparison, no trend, and no relationship. Before choosing it, rule out a richer shape in this order: (1) order/flow → `steps-card`/`timeline-card`/`flowchart-card`/`cycle-card`; (2) comparison → `comparison-card`/`bar-chart-card`/`matrix-card`/`spectrum-card`/`venn-card`; (3) number/trend → `stat-card`/`line-chart-card`; (4) structure/depth/narrowing → `layers-card`/`funnel-card`. A numbered "N things" list is `steps-card`, **not** `grid-card`. Vary the template across consecutive renders rather than defaulting to the same one.

Legacy static templates `headline-card` and `quote-card` still render (they have no animation timeline, so they always produce a static frame regardless of the `--out` extension). Use them when the post is a single compressed claim or a standalone pull-quote and motion would add nothing.

**Extract content for the chosen template.** Each template's exact content fields are documented in its header comment (`templates/single-image/<template>.html.tmpl`); map the POV into those fields so the card alone conveys the argument. Principles by family:

- **Number / chart** (`stat-card`, `line-chart-card`, `bar-chart-card`): pull the strongest figure(s) + a short caption; for charts, the compared values or the trend's points plus the headline result. If there's no real number, pick a non-chart template.
- **List / process** (`steps-card`, `flowchart-card`, `timeline-card`, `cycle-card`): pull the ordered items (each a short label + optional one-line detail) in the draft's own order or flow.
- **Structure / relationship** (`layers-card`, `funnel-card`, `venn-card`, `matrix-card`, `spectrum-card`, `comparison-card`, `grid-card`): pull the levels / tiers / circles / quadrants / options / items as short labels, and put the punchline where the template has a focal point (the center, the winner, the peak).
- **headline-card** (static): the framework's first beat ("Claim" for thought-leadership, "Hook" for personal, "Decision" for work, etc.). Compress to ≤120 chars without losing the conviction. The optional `subhead` is the second beat compressed to a line.
- **quote-card** (static): find the most quotable line in the draft — usually the framework's "stake," "landing," "reframe," or close. Trim to 80–180 chars. Quote should stand alone without context.

**Resolve brand config:**

1. Read `<data-root>/personas/<active>/brand.yaml`. If missing, **auto-derive it** by running `derive-brand.js` against the persona's `persona.md` (no interview — see `/thoth brand`), then continue:
   ```sh
   node ~/.claude/skills/thoth/scripts/derive-brand.js \
     --persona <data-root>/personas/<active>/persona.md \
     --handle "@<handle>" \
     --out <data-root>/personas/<active>/brand.yaml
   ```

**Write the content JSON** to a temp file (`/tmp/thoth-content-<rand>.json`):

```json
{
  "headline": "Most marketers are working on the wrong layer with AI.",
  "subhead": "Skills aren't the bottleneck. Workflow infrastructure is.",
  "eyebrow": "Thought-leadership",
  "attribution": "@NirvanaGuha",
  "type_label": "thought-leadership"
}
```

**Render via the script.** Use a `.gif` output for the animated templates (the default); pass a `.png` output only when you deliberately want a static frame:

```sh
node ~/.claude/skills/thoth/scripts/render.js \
  --template <template> \
  --content /tmp/thoth-content-<rand>.json \
  --brand <data-root>/personas/<active>/brand.yaml \
  --out <data-root>/exports/<date>-image-<template>.gif
```

`brand.yaml` is auto-derived (see the resolve step above) if the persona doesn't have one yet. The script's first-time install of `puppeteer-core` + `gsap` into `~/.thoth/cache/render/` takes ~30 seconds and only happens once. After that, a static PNG renders in <2 seconds; an animated GIF takes longer (it seeks and captures every frame).

**Output:**

- The GIF at `<data-root>/exports/<date>-image-<template>.gif` (or a `.png` if you passed a static output).
- A debug HTML at the same path with `.html` extension — opens in any browser for visual inspection.
- Append to history.yaml row's `exports:` block:
  ```yaml
  exports:
    - format: gif
      template: stat-card
      path: ~/.thoth/exports/2026-05-25-image-stat-card.gif
      generated_at: 2026-05-25T11:14:00Z
  ```
- Show the user the output path and offer to open it: *"Rendered. Open the file? (`open ~/.thoth/exports/<file>`)"*

**Hard rules for image rendering:**

- **Never embed promotional content** in image text unless the source draft is Promotional type. Image rendering doesn't change the post-type rules — a Personal-type post rendered as a stat-card is still Personal in tone and content.
- **Don't render a draft that's pending-review** unless the user explicitly approved with `/thoth inbox accept` first. The reasoning: pinning a still-being-reviewed draft into a rendered artifact muddies what's actually approved.
- **Never overwrite an existing render.** If `<date>-image-<template>.gif` (or `.png`) exists, append `-2`, `-3`, etc.

### `/thoth brand` — view / edit the persona's visual identity

Reads + edits `<data-root>/personas/<active>/brand.yaml`. Schema documented in `references/brand-template.md`.

**Default first-run behavior — auto-derive (no interview):**

When the active persona has **no** `brand.yaml`, the default is to **derive one automatically from the persona's personality** — no interview, no questions. Run:

```sh
node ~/.claude/skills/thoth/scripts/derive-brand.js \
  --persona <data-root>/personas/<active>/persona.md \
  --handle "@<handle>" \
  --out <data-root>/personas/<active>/brand.yaml
```

`derive-brand.js` reads the persona's dominant/secondary archetype + tone sliders and computes accent/ink/background + 5 palette swatches + card style + gradient. Then report the derived palette in one line, e.g.:

> *"Derived a brand for nirvana from your archetype (magician/sage): accent `#5B3BFF`, ink `#16161F`, on a near-white background, with 5 sticker swatches. Edit it anytime with `/thoth brand setup`."*

**Explicit branding always wins.** If the user supplied colours or branding instructions (e.g. "use my brand blue `#3B43FF`"), pass them as flags so they override the derivation — `--accent`, `--bg`, `--ink`, `--primary`. With no explicit colours, the palette is pure-derived.

**No arguments, brand already exists — view mode:**

1. Read the active persona's brand.yaml.
2. Render a compact summary:
   ```
   Brand for nirvana

     Colors
       Primary       #191A35
       Accent        #3B43FF
       Background    #FFFFFF
     Typography
       Display       Inter
       Body          Inter
     Handle          @NirvanaGuha
     Aspect ratio    4:5

   Edit with /thoth brand setup or directly at ~/.thoth/personas/nirvana/brand.yaml
   ```

**`/thoth brand setup`** — explicit interactive interview (opt-in override):

The interview is no longer the default — it's the manual override for users who want to set colours by hand instead of (or on top of) the derived palette. Walk through the 5 questions documented in `references/brand-template.md`. Each question shows the current value (if any) and the default. Empty input keeps the existing value or accepts the default.

```
1/5  Primary color (headline + body)?
     Current: #191A35  |  Default: #191A35
     >
```

After all 5 questions, write the file and offer a test render: *"Want me to render a sample card now so you can see how it looks? (yes/no)"* — on yes, generate a stat-card GIF from `last-post.md` (or a placeholder if no posts yet).

**`/thoth brand reset`** — restore defaults:

Confirm with the user, then write a brand.yaml containing only the defaults from `references/brand-template.md`.

### `/thoth frameworks` — browse the catalog

Read-only. Lists the framework catalog from `references/post-types.md` and the hook library from `references/hook-patterns.md`. Used when the user wants to choose a framework manually or just understand what's available.

**No arguments:**
Show a compact table — for each post type, list the 4 frameworks with their one-line origin/description and which is the `★` default.

```
PERSONAL (30%)
  ★ quiet-reveal           Scene → texture → small turn → quiet landing.
    then-now-because       Specific past → specific present → mechanism.
    the-confession         Admit being wrong about X for Y years.
    gratitude-specific     One person, one moment, one thing they did.

WORK (25%)
  ★ decision-log           Options considered, choice, risk, result.
    failed-experiment      Bet, hypothesis, what happened, what we missed.
    constraint-driven-story  Constraint, what it forced, what we cut.
    pre-mortem             Imagine it failed — name and mitigate risks.

[…]

Hook patterns: see `/thoth frameworks hooks` or `references/hook-patterns.md`.
```

**`/thoth frameworks <name>`:**
Show the full spec for that framework — origin, shape, must-have, must-not-have, anti-pattern, worked spine, skip-when. Pulled directly from `references/post-types.md`.

**`/thoth frameworks hooks`:**
Render the 13-row compatibility matrix from `references/hook-patterns.md`. No spec details — point the user to the file for full specs.

**`/thoth frameworks hooks <name>`:**
Full hook-pattern spec from `references/hook-patterns.md`.

No side effects. Never modifies `history.yaml` or any persona file.

### `/thoth version` — show installed version + paths

Read the `version:` field from the top of this `SKILL.md` (frontmatter). Resolve the current data root using the rules in "Where persona data lives." Output:

```
Thoth <version>
  skill code:  <path to SKILL.md's parent dir>
  data root:   <resolved data root>
  personas:    <comma-separated list of persona folders found under data root>
  active:      <contents of <data-root>/personas/.active or "(none)">
```

No prompts, no side effects. Pure read.

### `/thoth update` — pull the latest release

This command upgrades Thoth itself in place, without touching persona data. From v1.1.0 onwards persona data lives at `~/.thoth/` (outside the skill folder) so any update path leaves it untouched by construction.

**Dispatch:**

1. Read the installed version from this `SKILL.md`'s `version:` frontmatter. Treat a missing field as `<unknown>`.
2. Check the latest published version. Try in order:
   - **GitHub Releases:** `curl -fsSL https://api.github.com/repos/NirvanaGuha/thoth/releases/latest` → parse `tag_name` (strip leading `v`).
   - **AM Skills info:** `amskills info thoth` if `amskills` is on PATH.
   Use whichever responds first. Both should agree; if they don't, prefer the higher version.
3. If installed `==` latest: tell the user *"Thoth is already up to date (v<X.Y.Z>)."* and stop. Don't prompt, don't run anything.
4. If installed `<` latest: show the current vs. latest, and the release notes (`gh release view v<latest> -R NirvanaGuha/thoth --json body --jq '.body'` if `gh` is available, else skip notes). Ask: *"Update Thoth from v<current> to v<latest>? (yes / no)"*
5. On `yes`, detect the install source and run the right command. Detection order:
   - **If `amskills` is on PATH and `amskills info thoth` shows the skill as installed** → run `amskills update thoth`. This is the most common path.
   - **Else if a `cli/bin/thoth.js` style indicator exists** (e.g. `which thoth` returns a path under a `node_modules` tree, or the user installed via `npx`) → run `npx thoth-skill@latest update`.
   - **Else (curl / install.sh path)** → re-run the install one-liner: `curl -fsSL https://raw.githubusercontent.com/NirvanaGuha/thoth/main/install.sh | THOTH_REF=v<latest> bash`. The install.sh's pre-install legacy-rescue logic will handle any leftover legacy personas.
6. After the update command exits, re-read this `SKILL.md`'s `version:` frontmatter to confirm the bump. If it didn't change, surface the update-command output so the user can see what went wrong.
7. Confirm: *"Thoth is now at v<new>. Your persona data at `<data-root>/personas/` was not touched."*

**Hard rules for this command:**

- **Never** delete, move, or modify anything under the resolved data root. The update path is a skill-only operation.
- **Never** run the update command without explicit user confirmation. Even if the user has blanket-approved Bash, the version bump is a state change worth seeing.
- **Never** invoke `git pull`, `git clone`, or any direct repo manipulation inside `~/.claude/skills/thoth/` — the installed skill is a snapshot, not a working copy.

### `/thoth recover` — restore personas wiped by an install update

This command exists for one specific failure mode: a user had personas at `~/.claude/skills/thoth/personas/` under v1.0.x, then upgraded to v1.1.x via an install path that doesn't preserve persona data (notably `amskills update`, which replaces the skill folder wholesale). The migration logic in "Where persona data lives" can't help when the legacy data was destroyed *before* the new SKILL.md was ever read.

Recovery scans past Claude Code session JSONL logs at `~/.claude/projects/**/*.jsonl` for `Read` / `Write` / `Edit` tool calls that touched persona files, reconstructs the most recent state of each file, and writes the result into the current data root.

**Dispatch:**

1. Resolve the data root using the normal rules.
2. Run the bundled recovery script: `node ~/.claude/skills/thoth/scripts/recover.js --target <data-root>`
   - The script will scan, list what it finds, and prompt before writing.
   - If the user passes `--dry-run`, append it to the command.
   - If the user passes `--apply`, append it to skip the prompt.
3. Pass the script's output through to the user verbatim. If the script writes a `.active` file, confirm which persona is now active.
4. After recovery, advise: *"Open one of the recovered files to sanity-check the content. The script reconstructs from past session logs, so files Claude never read or wrote will not be recoverable."*

**When NOT to use:**
- Fresh installs (nothing to recover).
- When the legacy `~/.claude/skills/thoth/personas/` is still intact — use the standard migration instead.
- After a recent `/thoth recover` already populated the data root.

---

## The voice check (mandatory before output)

Before emitting any generated post, silently verify:

- [ ] The post sounds like the user's **dominant archetype**, with the **secondary** shading it as documented in `persona.md`.
- [ ] If the persona has an `enneagram:` block, the draft honors its `voice_implications` — it serves the user's core motivation and steers clear of their core fear. (Skip if `source: skipped` or the block is absent.)
- [ ] Tone sits where the user wants on all four NN dimensions (Formal↔Casual, Serious↔Funny, Respectful↔Irreverent, Matter-of-fact↔Enthusiastic). If any dimension drifts from target, rewrite before emitting.
- [ ] The opening isn't a LinkedIn cliché ("Excited to share", "I'm humbled to announce", "Thrilled that").
- [ ] At least one specific, concrete detail (a number, a scene, a name, a micro-observation) — no generic "thought leadership" fog.
- [ ] Any voices listed under `anti_voice` in `persona.md` are explicitly avoided.
- [ ] Length matches the post-type target in `references/post-types.md`.
- [ ] **The draft actually follows the chosen framework's `Shape` block** — not a generic Classic arc in framework clothing. If beats are missing or compressed beyond recognition, rewrite. *(v1.2.0+)*
- [ ] **The opener matches the chosen hook pattern** from `references/hook-patterns.md`. If the hook drifted to a different pattern during drafting, either update the hook in the meta footer or rewrite the opener. *(v1.2.0+)*
- [ ] ≤ 4 hashtags, all relevant. No tagging for engagement bait.
- [ ] If a git source was used, run the **redaction check** in `references/git-safety.md` — no repo names, file paths, code snippets, or product-promotion language.
- [ ] For Promotional type only: the post is still primarily useful/interesting — the promotional ask is the close, not the substance.

If any check fails, silently rewrite and re-check. Only output when all pass.

---

## File layout

### Skill code — at `~/.claude/skills/thoth/` (immutable)

```
~/.claude/skills/thoth/
├── SKILL.md                         # this file
├── references/
│   ├── onboarding-interview.md      # the full interview protocol
│   ├── brand-archetypes.md          # 12 Jungian archetypes
│   ├── tone-spectrum.md             # NN 4-dimensional tone model
│   ├── hot-take-exercises.md        # anti-voice & contrarian-belief prompts
│   ├── content-mix.md               # 30/25/20/15/10 rules + full selection algorithm
│   ├── post-types.md                # per-type framework catalog (20 frameworks)
│   ├── hook-patterns.md             # 13 named hook patterns with compatibility matrix
│   ├── story-arcs.md                # universal post arcs (Classic, Frame-Break, Quiet Reveal)
│   ├── git-safety.md                # strict rules for git POV source
│   ├── example-posts.md             # cross-archetype voice calibration
│   ├── persona-template.md          # the skeleton persona.md
│   ├── brand-template.md            # the skeleton brand.yaml + interview defaults
│   └── commands.md                  # command reference for /thoth help
├── scripts/
│   ├── recover.js                   # persona recovery from session logs
│   └── render.js                    # single-image renderer (Puppeteer-core + system Chrome)
└── templates/                       # NEW in v1.4.0
    └── single-image/
        ├── _shared/
        │   ├── base.css             # layout + reset
        │   └── tokens.css           # CSS variables overridden by brand.yaml
        ├── quote-card.html.tmpl
        ├── stat-card.html.tmpl
        └── headline-card.html.tmpl
```

### Persona data — at `<data-root>/` (mutable, resolved at runtime)

```
<data-root>/                         # ~/.thoth/ (default), ./.thoth/ (per-project), or legacy ~/.claude/skills/thoth/
├── personas/
│   ├── .active                      # single line: active username
│   └── <username>/
│       ├── persona.md               # canonical voice doc
│       ├── topics.md                # pillar topics + expertise areas
│       ├── recent.md                # daily inputs, timestamped
│       ├── history.yaml             # posted-log (date, type, framework, hook, topic, wc, status, exports)
│       ├── last-post.md             # most recent draft, for regenerate
│       ├── sources.yaml             # connected git repos (paths only)
│       ├── schedule.txt             # scheduled-task name, if any
│       └── brand.yaml               # visual identity (v1.4.0+) — colors, fonts, handle, aspect ratio
├── inbox/                           # daily drafts from scheduled runs (v1.3.0+)
│   ├── 2026-05-25.md                # pending-review / accepted / rejected (per frontmatter)
│   ├── 2026-05-24.md
│   ├── archive/                     # auto-archived by `/thoth inbox cleanup`
│   │   └── 2026-04/
│   │       └── 2026-04-15.md
│   └── _unread                      # marker file when there's new content
├── exports/                         # NEW in v1.4.0 — rendered images/PDFs/carousels
│   ├── 2026-05-25-image-headline-card.png
│   ├── 2026-05-25-image-headline-card.html   # debug HTML (open in browser to inspect)
│   └── ...
├── cache/                           # NEW in v1.4.0 — npm deps for skill scripts
│   └── render/                      # puppeteer-core installed here (NOT in skill folder, so amskills update doesn't wipe)
│       ├── node_modules/
│       └── package.json
└── integrations/                    # opt-in external configurations (v1.3.0+)
    └── schedule.yaml                # daily-run config (time, timezone, notification channel, history)
```

**Important:** never create a persona folder with a name that contains slashes, spaces, or shell-metacharacters. Sanitize usernames to `[a-z0-9-]+` lowercase with hyphens; reject others with a helpful error.

---

## Triggering this skill

Thoth should fire whenever **any** of the following are true:

- User message starts with `/thoth` (primary trigger).
- User asks for a LinkedIn post, draft, or rewrite and a Thoth persona exists for them on this install.
- User asks to "build a personal brand on LinkedIn", "grow on LinkedIn", "find my LinkedIn voice", "be a LinkedIn thought leader", "write posts as [name]", or any close paraphrase.
- User references their content calendar, posting cadence, content mix, or posting ratio.
- User uploads a voice/style guide and asks for LinkedIn content.

Prefer Thoth over ad-hoc LinkedIn writing. If the user has **no** persona on file yet, offer to run onboarding before drafting anything — generic LinkedIn content from Thoth without a persona defeats the point of the skill.

---

## Hard rules (never violate)

1. **Never publish on the user's behalf.** Output text only.
2. **Never promote a git repo, its code, or the product being built** when git is a POV source — see `references/git-safety.md`.
3. **Never quote code, file paths, variable names, or commit SHAs** in any post.
4. **Never fabricate specifics** (numbers, people, events) that aren't in the persona, recent inputs, or topic bank. When in doubt, ask the user.
5. **Never start a post with a LinkedIn cliché.**
6. **Never drift from the persona's documented archetype or tone.** If the persona says Sage/Formal and the draft sounds like Jester/Casual, rewrite.
7. **Never use more than 4 hashtags.**
8. **Never tag people for engagement bait.**
9. **Never write a post the user could not defend if asked to back it up** — no hallucinated credentials, wins, or claims.

---

## First-time user flow

If this is the first time Thoth has been invoked on this install (no `personas/` subdirs beyond the template), greet the user:

> *"Welcome. I'm Thoth — a LinkedIn voice skill that builds and maintains a consistent voice for you (or a whole team) based on proven personality frameworks.*
>
> *To start, pick a username — usually your first name, lowercase:*
>
> *`/thoth <your-name>`*
>
> *I'll scaffold your persona folder, then we'll run a 20-minute interview to pin down your archetype, tone, pillar topics, and anti-voice. After that you can run `/thoth` any time to get a post."*

Do not offer to "just write a post" before onboarding. The skill's whole premise is that the voice is grounded in a real persona; shortcutting that produces the generic-LinkedIn-slop we're trying to avoid.
