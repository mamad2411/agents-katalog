---
name: kick-mk-dump
version: 1.0.0
description: Challenges and resolves branches, unclear assumptions, and blind spots through interactive grilling, then writes an action-ready spec for /play-mk-dump. Works from a cleaned dump or a new idea described directly. Use when user runs /kick-mk-dump, wants to design or challenge ideas, or wants to explore something new before building it.
user-invocable: true
---

# kick-mk-dump

Challenges ideas interactively to resolve branches and blind spots. Role: adversarial thinking partner — find holes, not validate. Output: an action-ready spec that `/play-mk-dump` can execute from.

Works from two sources:
- **Cleaned dump** — grills the summary of a `/clean-mk-dump` session
- **New idea** — user describes an idea directly; kick grills it from scratch

## Flow

**Step 1: Determine source**

Check that `docs/monkey-brain/` directory exists. If not: tell user "Run `/init-mk-dump` first — it creates the directory structure and spec index." → stop.

Read `docs/monkey-brain/dump-index.md` → find sessions with status `cleaned`:
- Sessions exist → ask: "Kick a cleaned dump, or explore a new idea?"
  - Cleaned dump → show list if multiple, else use the single one → Step 2a
  - New idea → ask user to describe it in a few sentences → Step 2b
- No sessions → ask: "No cleaned dumps found. Describe your new idea, or run `/clean-mk-dump` first."
  - New idea described → Step 2b
  - User wants to clean first → stop

**Step 2a: Cleaned dump path**

Read the full dump file. Use `## Summary` as the primary structure — extract all [BRANCH], [UNCLEAR], and Open Questions from it. For any item that feels thin or has missing conditions, check the raw sections below `## Summary` for the original context before grilling. → Step 3

**Step 2b: New idea path**

Ask 1–2 scoping questions (what is it, what does success look like?). → Step 3

**Step 3: Create spec file + Grill**

Before the first grill question, determine `{NNN}` and the spec filename:
- **Dump source:** extract NNN from the session filename (e.g. `2026-05-23-001-dump-system-design.md` → NNN=`001`). Filename: `{yyyy-mm-dd}-dump-{NNN}-{topic}-kick.md`
- **Idea source:** count files matching `{yyyy-mm-dd}-idea-*` in `docs/monkey-brain/specs/{yyyy}/{mm}/` for today; add 1 and zero-pad to 3 digits. Filename: `{yyyy-mm-dd}-idea-{NNN}-{topic}-kick.md`

Create the spec file at `docs/monkey-brain/specs/{yyyy}/{mm}/{filename}` with the header from [REFERENCE.md](REFERENCE.md) (status, title, source, empty `## Decisions Made`).

Follow Grilling Rules. After each BRANCH or UNCLEAR item is resolved, immediately append the decision to `## Decisions Made` in the spec file — do not wait until the end. After covering all items, checkpoint:
"I've challenged X items. Want to go deeper on anything, or move to research?"
- Go deeper → continue grilling
- Ready → Step 4

**Step 4: Research (up to 3 rounds)**

Search the web for real-world solutions, tools, or approaches related to the refined idea. Each round:
1. Run 2–3 targeted searches on key themes from the grilling output
2. Present findings: top approaches found + pros/cons for each
3. Ask: "Want another research round, or shall I write the spec?" (track round number)

Stop when: user signals done, or 3 rounds completed — whichever comes first.
Research findings are included in the spec — use REFERENCE.md content already in context from Step 3 — do not re-read.

**Step 5: Write Issues section**

After grilling and research are complete, append `## Issues` to the spec file. Follow these rules exactly:

**Issue structure** (each issue must have all fields):
```
### Issue N: [title]
_Independent_ OR _Depends on: Issue X_
Done when: [1–2 sentence success criteria — specific enough to verify]
- [ ] [sub-step]
- [ ] [sub-step]
```

**Issue structure** (each issue must have all fields; `> Note:` is optional):
```
### Issue N: [title]
_Independent_ OR _Depends on: Issue X_
Done when: [1–2 sentence success criteria — specific enough to verify]
> **Note:** [decisions from grilling that constrain this issue — omit if none]
- [ ] [sub-step]
- [ ] [sub-step]
```

**Issue decomposition rules:**
- **Independent or declared dependency** — if an issue needs another to finish first, state it explicitly
- **Single concern** — one issue does one thing; if it touches two areas, split it
- **Session-sized** — 10–30 min of work; if "Done when:" needs more than 2 sentences, the issue is too big
- **2–6 sub-steps** — specific enough that play can execute each without asking clarifying questions. If a decision from grilling constrains a sub-step, embed the constraint inline (e.g. "Create X using Y pattern — per Decision: [topic]")
- **"Done when:" must be verifiable** — not "update the skill" but "skill file has X section with Y content"
- **Can't write "Done when:" without assumptions?** — unresolved decision remains; go back and grill it
- **Decision coverage check** — after writing all issues, re-read `## Decisions Made`. Every decision must appear in at least one sub-step or `> Note:` block. Any decision not reflected = coverage gap — go back and add it

**Step 6: Create spec-index.md row + update dump-index**

After writing the spec file, add a row to `docs/monkey-brain/spec-index.md`:
```
| docs/monkey-brain/specs/{yyyy}/{mm}/{filename} | remaining | — | — |
```
If `spec-index.md` does not exist, create it first:
```
# Spec Index

| File | Status | Date done | Note |
|------|--------|-----------|------|
```

**Dump source only:** update the originating session row in `docs/monkey-brain/dump-index.md` — change status `cleaned` → `kicked`. Then:
1. Create `docs/monkey-brain/dump-sessions/{yyyy}/{mm}/done/` if it doesn't exist
2. Move the dump session file to `docs/monkey-brain/dump-sessions/{yyyy}/{mm}/done/{filename}`
3. Update the file's path in `dump-index.md` Sessions table to include `done/` (e.g. `2026/05/done/{filename}`)

Tell user: "Spec written. Run `/play-mk-dump` next."

## Grilling Rules

- **One topic per message.** If an answer is unclear or contradictory, follow up on the same thread before moving on — don't drop it and don't stack new topics.
- **Follow the thread.** If an answer opens a branch, pursue it before moving on.
- **Challenge, don't confirm.** Find holes, not validation.
- **Use 5-Why.** When the user states a decision, ask why until the real reason surfaces.
- **Priority order:** [BRANCH] items → [UNCLEAR] items → blind spots you introduce.
- **Surface blind spots last:** edge cases, alternatives, contradictions, resource constraints the user didn't raise.
