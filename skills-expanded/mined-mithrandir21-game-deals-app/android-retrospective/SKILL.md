---
name: android-retrospective
description: At the end of an Android or Kotlin Multiplatform development session, feature, or change, extract the few things Claude actually learned and persist them as condensed, reviewable lessons that future sessions can apply without having to re-derive them. The lessons are stored in `.claude/lessons.md` in a structured format (ID, status, confidence, date, scope, tags) so they can be audited, superseded, or deprecated as understanding evolves. Trigger this skill whenever the user says "retro", "retrospective", "wrap up", "session summary", "post-mortem", "what did we learn", "save the lessons", "capture lessons learned", or signals they're done with a feature, PR, or branch and wants to lock in learnings. Do NOT trigger for plain changelogs or daily status summaries.
---

# Android Retrospective

Distill what was learned in an Android or KMP development session into a small number of **condensed, structured, reviewable lessons** that future Claude sessions can apply.

The output is not a retro document. It is a short append to `.claude/lessons.md`. Goal: next session, Claude reads the file and already knows the things you had to teach it this session.

## Design principles

Every stored lesson must be:

- **Condensed** — hard caps: headline ≤ 70 chars, TL;DR ≤ 140 chars, body ≤ ~100 words (≤ 3 short paragraphs), Source ≤ 1 sentence. If it won't fit, it's probably two lessons or a design doc.
- **Structured** — carries an ID, date, status, confidence, scope, and tags. This is what makes it reviewable.
- **Scannable** — every lesson opens with a TL;DR line directly under the headline. That single line is what humans skim and what the auto-generated index uses.
- **Superseded, not silently corrected** — when a later session finds a lesson wrong or outdated, the old lesson gets marked `superseded` or `deprecated` and a new one is added. **Never edit an existing lesson's content.**

Lessons get outdated. Libraries change, practices change, earlier learnings turn out to be wrong. The format is built for that — not to pretend it won't happen.

## When to use this skill

Natural endpoints of work:

- A feature or user-facing change is done
- A refactor or modularization pass is complete
- A long debugging or investigation session wrapping up
- A branch is about to merge

Test: *"Would I, six months from now, want Claude to already know this instead of deriving it again?"* If yes, run the skill.

## Core workflow

### Phase 1 — Agree on scope

Confirm what "this session" means:

- **This conversation**
- **This branch vs `main`** — `git log main..HEAD`
- **Since the last lesson** — check the newest `Added` date in `.claude/lessons.md`; cover work since then
- **A specific commit range or time window**

If scope is obvious from context, state it in one line and move on.

### Phase 2 — Gather evidence

Just enough to ground extraction. **Do not run tests or builds** — this is reflection, not verification.

- `git log --oneline <range>` — commits
- `git diff --stat <range>` — changed files
- `git status` — uncommitted work (often where the freshest lessons live)
- `git log -p <range> -- <path>` for anything suspicious

For Android / KMP, pay extra attention to:

- `*/build.gradle.kts`, `settings.gradle.kts`, version catalogs — dependency quirks, KSP/KAPT/Gradle gotchas
- `commonMain` / `androidMain` / `iosMain` — `expect`/`actual` boundaries, Swift interop (SKIE, sealed result types, XCFramework)
- Compose — recomposition, state hoisting, navigation
- DI (Koin, Hilt) — scoping, multiplatform modules
- Networking (Ktor) — routing, serialization, WebSocket patterns
- Persistence (SQLDelight, Room) — migrations, queries
- Tests (Turbine, MockK, Kotest) — hard-won test patterns

The conversation itself is evidence. Dead ends and corrections from the user are where most real lessons live.

### Phase 3 — Synthesize in chat

Before proposing lessons, briefly summarize in chat what happened this session — goal, what shipped, what was hard. A few short paragraphs, not a document. **No file is written in this phase.** This is just shared ground before extraction.

### Phase 4 — Propose candidate lessons

For each candidate, use the full lesson format below (see *Lesson format*). The user's senior judgment is the filter: if a candidate feels obvious or not clearly durable, flag it as "probably not worth saving" rather than quietly including it.

Before presenting candidates, **self-check each one against the caps** (headline ≤ 70 chars, TL;DR ≤ 140 chars, body ≤ ~100 words, Source ≤ 1 sentence). If a candidate exceeds a cap, either trim it or split it into two lessons — do not present overlong candidates and ask the user to absorb the violation.

Bias toward fewer lessons. Three is already a lot from a single session. One well-chosen lesson is often the right output.

### Phase 5 — Reconcile with existing lessons

Before writing, read the current `.claude/lessons.md` (if it exists) and scan the `## Active` section. For each new candidate, check whether any existing lesson is:

- **Confirmed** by the new learning — note it, no file change needed (surviving another pass is the confirmation signal)
- **Refined or superseded** — the new lesson replaces the old with more precision or a different conclusion → mark old as `superseded by <new-ID>`
- **Contradicted** (old lesson is now wrong) — mark old as `deprecated (<one-line reason>)`

Surface any of these alongside the new candidates so the user approves everything in one pass.

### Phase 6 — Confirm

Present the final plan:

- New lessons to add (with proposed IDs)
- Existing lessons to mark superseded or deprecated (with one-line reason)

**Do not write anything until the user approves.** The user may reword, drop, or change status decisions.

### Phase 7 — Persist

Edit `.claude/lessons.md` (create it from the template below if missing). Three operations:

1. **Prepend approved new lessons** to the `## Active` section (most recent first).
2. **Move superseded/deprecated lessons** from `## Active` to `## Archive`, updating only their status chip. **Never change any other field on an archived lesson** — the audit trail depends on it.
3. **Regenerate `## Index — Active`** above the `## Active` section. The index is pure derivation: one row per active lesson, columns `ID | TL;DR | Tags`, in the same order as `## Active`. For older lessons that predate the TL;DR field, fall back to the headline (the text after the `· `). Comma-join tags. Never hand-edit the index — rewrite it in full each time.

## Lesson format

Every lesson — active or archived — follows this exact structure:

```markdown
### L-<YYYY-MM-DD>-<NN> · <concise headline>
**TL;DR:** <single-line summary, ≤ 140 chars — the rule in one sentence>
`<active|superseded by L-…|deprecated (reason)>` · `<confirmed|tentative>` · <YYYY-MM-DD> · `<tag1>` `<tag2>` `<tag3>`
**Applies to:** <where future-Claude would encounter this — 1 line>

<Body, ≤ ~100 words / ≤ 3 short paragraphs, imperative voice. Lead with the advice; then just enough context for a future session to know when it applies. Mention a specific library/version only if it's load-bearing.>

**Source:** <one sentence — feature, concept, or area this came from>
```

**Field rules:**

- **ID** — `L-` then ISO date then `-NN` (01, 02, …) for multiple lessons on the same day. **IDs never change**, even when a lesson is archived.
- **Headline** — ≤ 70 chars. State the rule, not an example. No backticked symbols — those belong in the body.
- **TL;DR** — mandatory. Single line, ≤ 140 chars, restating the rule in one sentence. This is what humans skim and what the generated index uses.
- **Status chip** — one of:
    - `active` — apply it
    - `superseded by L-YYYY-MM-DD-NN` — don't apply; see replacement
    - `deprecated (<short reason>)` — don't apply; no replacement
- **Confidence chip** — exactly `confirmed` or `tentative`. No qualifying suffixes; if a caveat matters (e.g. "only verified for KSP 2.3.8"), state it in the body, not the chip.
- **Tags** — short, kebab-case or single word: `ktor`, `websocket`, `kmp`, `compose`, `gradle`, `ci`, `testing`, `skie`, `koin`, `sqldelight`.
- **Body** — ≤ ~100 words / ≤ 3 short paragraphs. If it doesn't fit, it's two lessons or a design doc.
- **Source** — ≤ 1 sentence. Provenance, not a postmortem. Longer narratives belong in PR bodies.

### Example — active lesson

```markdown
### L-2026-04-20-01 · Ktor WebSocket incoming channel must be actively pulled
**TL;DR:** Launch a dedicated coroutine to collect from a Ktor client WebSocket's `incoming` channel — it doesn't pull on its own.
`active` · `confirmed` · 2026-04-20 · `ktor` `websocket` `kmp`
**Applies to:** Ktor client WebSocket sessions using request/response multiplexing

When using a Ktor client WebSocket, the `incoming` channel doesn't pull messages on its own. Launch a dedicated coroutine that collects from it in a loop, otherwise `CompletableDeferred`-based response pairing will hang. This is how Ktor's channel model works.

**Source:** `:shared` module's WebSocket request-multiplex layer.
```

### Example — superseded lesson

```markdown
### L-2025-11-02-01 · Use callbackFlow for WebSocket events
**TL;DR:** Wrap a Ktor WebSocket session's incoming channel in a `callbackFlow` to expose events.
`superseded by L-2026-04-20-01` · `tentative` · 2025-11-02 · `ktor` `websocket` `kmp`
**Applies to:** Ktor client WebSocket sessions

Wrap the WebSocket session's `incoming` channel in a `callbackFlow` to expose events to the app layer.

**Source:** Initial WebSocket spike.
```

Only the status chip changed. Everything else is preserved so the archive remains an honest record of what was once believed.

## File template

When creating `.claude/lessons.md` for the first time, use this skeleton:

```markdown
# Lessons Learned

Condensed, structured lessons from past development sessions. Claude reads this file at the start of each session (via a separate skill) so it can apply past learnings without re-deriving them.

Each lesson has an immutable ID. When a lesson is superseded or turns out to be wrong, it is moved to `## Archive` with an updated status chip — its content is never rewritten. This preserves the audit trail.

**Claude:** apply lessons from `## Active` only. Consult `## Archive` only if something appears contradictory and you need the history. Ignore `## Index — Active` — it's a generated human-readable TOC, not a source of lesson content.

## Index — Active
<!-- generated; do not hand-edit -->

| ID | TL;DR | Tags |
|---|---|---|

## Active

<newest first>

## Archive

<superseded / deprecated lessons, newest first>
```

## Output rules

- **Never** write files before the user has approved the plan in chat.
- **Never** edit the content of an existing lesson — only move it between sections and update its status chip.
- **TL;DR backfill is the sole sanctioned edit to an existing lesson.** A `**TL;DR:** …` line may be inserted directly under the headline of any lesson (active or archived) that lacks one. **No other field may be added, removed, modified, or reordered.** Once a TL;DR is present, the lesson reverts to fully immutable.
- **Never** truncate, reorder, or delete archived lessons. The archive is permanent.
- **Always** regenerate `## Index — Active` in full as the last step of any write — never hand-edit individual rows. The index is a derived view; the lessons themselves are the source of truth.
- If git is unavailable or the working tree is empty, rely on conversation alone and note this during scoping.
- Keep new lessons per retro small. Three is already a lot; one well-chosen lesson is often the right output. If the session taught Claude nothing durable, say so and stop — "no new lessons" is a valid outcome.

## Example — abridged end-to-end

**User:** "Wrap up this session — what did we learn?"

**Claude's flow:**

1. Scopes to `feature/ws-multiplex` vs `main` (6 commits).
2. Runs `git log`, `git diff --stat`; notes changes in `:shared/src/commonMain/.../ws/`.
3. Summarizes inline: *"We built WebSocket request/response multiplexing in `:shared`. Main friction was correlating responses to requests, and `incoming` not auto-pulling messages."*
4. Proposes two candidates:
    - `L-2026-04-20-01` · Ktor WebSocket incoming channel must be actively pulled (confirmed)
    - `L-2026-04-20-02` · Correlation IDs for single-socket request multiplexing (confirmed)
5. Reads existing `.claude/lessons.md`; finds `L-2025-11-02-01 · Use callbackFlow for WebSocket events`. The new lesson refines and replaces it. Flags the supersession.
6. User approves both new lessons and the supersession.
7. Prepends the two new lessons to `## Active`; moves `L-2025-11-02-01` to `## Archive` with its status chip set to `superseded by L-2026-04-20-01`; regenerates `## Index — Active` so the new rows appear at the top.

## Anti-patterns — avoid these

- **Over-saving.** If the session didn't teach Claude anything durable, "no new lessons" is the right answer. Say so and stop.
- **Vague lessons.** "Be careful with coroutines" is noise. "When collecting Ktor's `incoming` channel, launch a dedicated coroutine — it's passive" is signal.
- **Silently correcting old lessons.** If an earlier lesson turns out wrong, it gets superseded or deprecated via its status chip. Never rewrite the original content — reviewability depends on the record staying honest.
- **Running the skill for trivial changes.** A one-commit bugfix rarely produces durable lessons. If it does, fine; if not, skip the persist step.
- **Treating `tentative` as `confirmed`.** If you only saw it work once, mark it tentative. A future session can promote it to confirmed via supersession after the pattern holds up.
- **Reordering or pruning the archive.** The archive is an audit log. Its value comes from being complete.
- **Hand-editing the index.** The index is a generated view, not a source of truth. Edits won't survive the next retro — fix the underlying lesson instead.
- **Omitting the TL;DR.** A lesson without a TL;DR is unscannable and falls back to its headline in the index. The TL;DR is the one mandatory new field — write it.
- **Using the TL;DR backfill exception as a hook to "tidy up" old lessons.** The exception is TL;DR-line addition only. Reflowing the body, converting old `**Status:**` metadata to chip style, rewording the headline, etc. are still forbidden — even when the temptation to "fix it while we're here" is strong.