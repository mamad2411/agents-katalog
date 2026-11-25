---
name: salvage-project
description: Use when a project has gone down a bad path (wrong stack, over-engineered, incomplete requirements) and the developer wants to start over simpler without losing what they learned. Recovers the real requirements and emits a portable spec bundle to rebuild. Also runs on session start to detect and accept an existing salvage/ bundle. Triggers on "start over", "salvage this project", "rebuild simpler".
---

# Salvage Project

Start over, simpler — without losing what you learned.

This skill has two modes. Which one runs is decided by **mode detection**, below.
Run mode detection first, every session, before doing anything else.

## Mode detection (run first, every session)

Check the working directory for the file `salvage/manifest.yaml`.

- **Present** → a salvage bundle is already here. Run **Accept mode (Act 3)** —
  set up a fresh project from the bundle. See that section below.
- **Absent** → no bundle. Run **Salvage mode (Act 1)** — recover the real
  requirements from a broken project and emit a bundle. Salvage mode is
  triggered by the `/salvage` command or by natural language such as "start
  over", "salvage this project", or "rebuild simpler".

If `salvage/manifest.yaml` is present but the developer explicitly invoked
`/salvage` (a salvage intent), confirm which mode they want rather than silently
routing to accept mode.

Do not mix modes. Decide once, then follow that act to the end.

---

## Salvage mode (Act 1)

You are in a project that went down a bad path. Your job is to recover the
*real* requirements (now that the developer knows more) and write a portable
spec bundle that a fresh agent can rebuild from — on the simplest stack the
developer can actually maintain.

**Two rules of discipline for the whole act:**

1. **One question at a time.** Never batch questions. If a topic needs more
   exploration, break it into separate messages. Prefer multiple-choice when it
   makes a question easier to answer.
2. **Write NOTHING into the project until Stage 4.** Stages 1–3 only *read and
   ask*. No files, no edits. The bundle is written once, at the end.

The four stages run in order, pausing for the developer between each.

### Stage 1 — Intake (what went wrong)

Ask these one at a time. Listen for the real requirement hiding behind each
complaint.

1. What is this app *supposed* to do, in one sentence?
2. Which features fought you hardest? What broke, or wouldn't scale?
3. Where did the previous agent resist a change you wanted?
4. **Maintenance ceiling (HARD constraint).** What languages and tools are you
   comfortable owning long-term? Are you OK with a build step? With Docker? With
   async code? Be concrete.

The maintenance ceiling is not a preference — it is a **hard cap on Stage 3**.
No rung you choose later may exceed what the developer answered here, no matter
how tempting. Record the ceiling verbatim; you will weigh every architecture
decision against it.

### Stage 2 — Code archaeology (what it actually does)

Read the existing code to extract the *real* requirements. Your goal is to
separate two things that are tangled together in the old project:

- **Genuine behavior (KEEP)** — what the app actually needs to do for its users.
- **Incidental tech decisions (DROP)** — choices the last build made that aren't
  requirements at all (a framework, a database, a pattern).

Produce two drafts and show them to the developer:

1. A **feature inventory** — the "keep" list, in plain behavioral terms.
2. A list of **complexity smells** — places where the old build climbed higher
   than any requirement justified. For example: "websockets for a dashboard that
   refreshes every 30s", "Postgres for fewer than 1000 rows", "a SPA for three
   static pages".

The developer confirms or corrects the inventory before you continue. Do not
move to Stage 3 until the "keep" list is agreed.

### Stage 3 — Architecture interview

Now choose the stack, one fork at a time. Invoke the **simplicity-guide** skill;
it holds one reference file per fork (data store, frontend, realtime, auth, jobs,
deploy), each structured as a ladder of rungs.

A fork is **relevant** if the Stage-2 keep list implies that capability; skip
forks the app doesn't need (e.g. no realtime needs → skip `realtime.md`). This
reinforces YAGNI.

For **each fork that is relevant** to this project, run this loop:

1. Open the matching `simplicity-guide` reference.
2. Find the **lowest rung whose "Use when" the project satisfies.**
3. Climb a rung **only when a STATED requirement (from Stage 1 or the Stage 2
   keep list) matches that rung's "Climb when."** Never climb "to be safe" or
   "for scale we might need."
4. Weigh the rung's **Cost** against the Stage-1 **maintenance ceiling.** If a
   rung's cost exceeds the ceiling, you may not choose it — stay lower and tell
   the developer why.
5. Ask the developer the trade-off question, framed by their ceiling, and
   confirm the choice.
6. Record the decision by filling the rung's **Rationale template**, and cite
   the exact rung you used (for example `data-store.md#sqlite`).

Each fork ends with one recorded, rung-cited decision. These become
`tech-stack.md` in Stage 4.

### Stage 4 — Emit the bundle

Now — and only now — write the portable bundle. Create a `salvage/` directory at
the **root of the broken project** containing exactly these six files:

**`manifest.yaml`** — the detection file and greeting source. Schema:

```yaml
salvage_version: 1
created: <today's date, YYYY-MM-DD>
app_name: <one-line app name>
stack: <chosen stack, one line>
docs: [CLAUDE.md, requirements.md, tech-stack.md, design-notes.md, anti-patterns.md]
```

**`requirements.md`** — the recovered "keep" feature inventory from Stage 2.
Behavioral requirements only; no tech decisions.

**`tech-stack.md`** — the chosen stack, with the filled rationale (from Stage 3)
for each decision, each citing its simplicity-guide rung.

**`design-notes.md`** — how the pieces fit together. Keep this deliberately
small; it is orientation, not a spec.

**`anti-patterns.md`** — the failed decisions from last time. For each one, state
**WHY** it failed and mark it clearly **"do NOT reintroduce."** This is the
single most valuable artifact in the bundle — it stops the fresh agent from
walking back into the same wreck.

**`CLAUDE.md`** — start from this plugin's bundled template at
`${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md` (not a file in the project being
salvaged) and fill its slots from the
interview: `{{skill_level}}` (from the Stage-1 maintenance ceiling), `{{stack}}`
(from Stage 3), and `{{requirements}}` (a one-line summary of the keep list). The
fixed principles half is copied verbatim — do not soften it.

Then tell the developer exactly what to do next:

1. Create a new, empty git repository for the rebuild.
2. Copy the `salvage/` directory into it.
3. Open a fresh Claude Code session in that repo — this skill will detect the
   bundle and set the project up automatically.

---

## Accept mode (Act 3)

A `salvage/manifest.yaml` is present, which means a bundle is waiting to be
rebuilt into a clean project. Your job is to set the project up from the bundle
and hand off to the build — **without re-brainstorming.** The salvage interview
already validated this design; treat the bundle as the finished spec.

### 1. Detect and confirm

Read `salvage/manifest.yaml`. Use its `app_name` and `stack` for the greeting,
verbatim shape:

> "Found a salvage spec to rebuild **[app_name]** on **[stack]**. Want me to set
> up the project?"

Wait for the developer to say yes before doing anything. The greeting's yes
authorizes the safety check, not the writes — if the fresh-target check finds
code, escalate to a second confirmation before writing anything.

Sequence, in order:

1. Greet and wait for yes.
2. On yes → run the safety check (fresh-target check + per-file no-clobber).
3. If the fresh-target check finds non-allowlisted code → **STOP** and require a
   SECOND explicit confirmation ("This repo already has code (X, Y, Z) — set up
   anyway?") before any write.
4. Only then write the docs, still honoring per-file no-clobber with `.bak`.

### 2. Safety check (BEFORE writing anything)

Two separate guards. Run both.

**Fresh-target check.** The repo is "empty enough" if — ignoring `.git/`, the
`salvage/` bundle itself, and this inert allowlist — nothing else remains:

- `README*`
- `LICENSE*`
- `.gitignore`
- `.editorconfig`

If anything outside that set exists (any real source file, config, or stray
doc), the repo is **not fresh.** List exactly what you found and require explicit
confirmation before any setup:

> "This repo already has code (X, Y, Z) — set up anyway?"

Do not proceed until the developer confirms.

**Per-file no-clobber (always, even in a fresh repo).** Before writing each
canonical doc, check whether a file of that name already exists. If it does,
**STOP and ask** — offer to back it up to `<name>.bak` first. Never overwrite
blindly. A stray `CLAUDE.md` is not on the inert allowlist, so this guard runs
even when the fresh-target check passed.

### 3. Detect superpowers

Glob the plugins directory for superpowers, e.g.:

```
~/.claude/plugins/**/superpowers/**/SKILL.md
```

(plus its config/manifest if present). Install paths vary, so this glob can
miss even when superpowers is installed — if it does, fall back to asking (the
degrade-to-question behavior below).

- **Found** → state it with confidence: "superpowers is available — I'll use its
  plan/execute workflow."
- **Not found** → do **NOT** assert that it is absent (install paths vary).
  Instead ask: "I don't see superpowers — if you have it installed, tell me;
  otherwise I'd recommend `/plugin install superpowers`, or I can continue
  standalone." Only the positive claim is made with confidence; the negative
  degrades to a question.

### 4. Write the canonical docs

Copy the five docs from the bundle into the **repo root** (respecting the
per-file no-clobber guard above for each):

- `CLAUDE.md`
- `requirements.md`
- `tech-stack.md`
- `design-notes.md`
- `anti-patterns.md`

These come straight from `salvage/`; you are not regenerating them. Only these
five docs are copied out to the repo root; the `manifest.yaml` stays in
`salvage/`.

### 5. Transition to the build

The bundle **is** the validated design. Do **not** re-brainstorm and do not
reinvent plan-writing or execution — drop straight into building.

- **superpowers present** → hand directly to `superpowers:writing-plans`, then
  `superpowers:executing-plans`. The bundle is the spec the plan is written
  from.
- **superpowers absent** → follow the "How to build" fallback in the freshly
  written `CLAUDE.md`: build feature-by-feature from `requirements.md`,
  simplest-first, confirming each feature works before starting the next.

salvage owns recovery and setup; the build is owned by superpowers (or a plain
agent). superpowers is an optional accelerator, never a hard dependency.
