---
name: claude-tuneup
description: Clean, optimize and personalize a Claude Code installation — guided, step-by-step, fully undoable. Use whenever the user mentions claude-tuneup, or wants to clean/declutter/slim down their Claude Code install or ~/.claude, free disk space, remove unused skills/plugins/hooks/MCP servers, fix config integrity, improve or trim CLAUDE.md based on real usage, wire or de-duplicate AGENTS.md with CLAUDE.md, build a SOUL.md profile, or undo a previous tune-up ("claude-tuneup restore"). Also triggers on "my Claude Code is bloated/slow/messy" and pt-BR phrasings like "limpar/otimizar o Claude Code".
---

# Claude Tuneup Skill

> **To be used as a checklist by an AI agent to guide the developer.**

## Goal

Tune up a Claude Code installation in two halves: (1) **clean + optimize** the install — analyze each item, report size/content/status, ask the dev "delete or keep?", proceed step by step, never delete without explicit confirmation; then (2) **give it a soul** — propose a `SOUL.md` profile of the human so Claude knows who it's talking to. Cleanup removes the junk; SOUL adds the identity.

## Map of this skill (read only what you need)

This file holds the **routing, the UX contract, and the safety rules** — they apply to every group. The per-group playbooks live in `references/` and are loaded on demand. **Before running a group, read its reference file top to bottom; do not run a group from memory.** Don't read reference files for groups that aren't part of this run.

| Group | Steps | Playbook |
|-------|-------|----------|
| **cleanup** | 1–8 | `"$SKILL_DIR"/references/cleanup.md` |
| **claude.md** | 9 | `"$SKILL_DIR"/references/claude-md.md` |
| **soul.md** | 10 | `"$SKILL_DIR"/references/soul-md.md` |
| **summary** | 11 | below (always runs last) |

---

## How to ask the dev (MANDATORY)

Every delete/keep choice MUST be offered through the **AskUserQuestion** tool (clickable buttons) — never a free-text "y/n" or numbered list. Free-text prompts confuse the dev.

- One button option per concrete action, with size in the label (e.g. "Delete (frees 269M)").
- Batch related decisions from the same step into a single multi-question AskUserQuestion call instead of asking one by one.
- When listing candidates, show the **full path + size** for each so "which ones?" never needs a follow-up.

**"What does this do?" option (MANDATORY on EVERY question).** Every single AskUserQuestion in this skill must include one extra button worded simply — e.g. **"O que isso faz? / Explain first"** — no exceptions, whatever the decision is about (a file, dir, plugin, skill, agent, MCP, config key, anything). If the dev picks it:
1. Explain *that specific thing* in 1–3 plain lines — what it is, why it's there, what deleting/keeping it actually means. For a plugin/skill/agent/MCP, read its real source first (`SKILL.md`, `plugin.json`/`README`, agent frontmatter, MCP command). For an unknown file/dir, inspect it (`file`, `head`, `ls`, `du`) before explaining.
2. Then ask again whether they now have enough to decide — re-offer the original buttons **plus the explain button again** (they may want another item explained first).

Never make the dev decide on something they can't identify.

---

## Helper scripts (deterministic, cross-OS)

The mechanical, repeatable work lives in `"$SKILL_DIR"/scripts/*.mjs` — plain Node (no deps), so it runs the same on macOS, Windows and Linux via the `node` that Claude Code already bundles. **Prefer these over ad-hoc inline shell** — never reach for `python3`, which is not guaranteed to exist; the agent's job is judgment (classify, ask, decide), the scripts' job is gather/apply.

- `node scripts/scan.mjs [--section a,b]` → read-only discovery of the install as JSON. Sections: `skills`, `plugins`, `hooks`, `mcps`, `projects`, `stateDirs`, `rootFiles`, `usage`, `memory`. Run it **once per step with just that step's section** instead of re-scanning everything. Touches nothing.
- `node scripts/backup.mjs create` → make a restore point, print its path (`$RP`). Also `backup.mjs stash <RP> <path>` (move an item into the restore point, logged) and `backup.mjs log <RP> <msg>`.
- `node scripts/restore.mjs list` / `restore.mjs apply <RP> [--configs-only|--items-only]` → list restore points, or apply one (fully, or just configs / just removed items).
- `node scripts/insights.mjs [--no-cache]` → run `/insights` headless and return the useful report sections as JSON (cached 1h).
- `node scripts/consolidate.mjs <name> [--undo]` → move a skill from `~/.claude/skills/` to `~/.agents/skills/` and link back (junction fallback on Windows).
- `node scripts/validate-json.mjs <file...>` → confirm a JSON file still parses (use after every config edit).
- `node scripts/version-check.mjs` → compares the shipped version against the latest GitHub release (cached 24h, fails silently offline). Prints `update:true` + a one-line `message` only when behind. Relay that line; otherwise say nothing.

`SKILL_DIR` is shown when the skill loads. Inline shell from the playbooks is the fallback when a script can't run.

---

## STEP 0: Pick what to run (start here)

Don't assume the dev wants the whole thing. The 11 steps form 4 named groups (see the map above).

**Update nudge (token-cheap, do this first).** Run `node "$SKILL_DIR/scripts/version-check.mjs"` once at the very start. If it returns `update:true`, relay its one-line `message` to the dev before anything else. If `update:false` or `ok:false`, say nothing about versions and continue silently — never make the version check noisy or blocking. Skip it on `help`.

Routing:
- **`help` / `?`** → print the help card below and **stop** (run nothing):

  ```
  claude-tuneup — tune up your Claude Code install (undoable; asks before deleting)

  Groups:
    cleanup    steps 1–8   remove junk + fix config integrity
    claude.md  step  9      improve CLAUDE.md from real usage via /insights
    soul.md    step 10      interview you + build a SOUL.md profile
    summary    step 11      always runs last; shows what changed + how to undo

  How to trigger:
    claude-tuneup                 → asks which group to run
    claude-tuneup cleanup         → run a group by name
    claude-tuneup soul.md         → (cleanup | claude.md | soul.md | summary)
    claude-tuneup 1-3             → run a step range
    claude-tuneup 6,7             → run specific steps
    claude-tuneup claude.md soul.md → combine groups
    claude-tuneup restore         → undo a previous run from a backup
    claude-tuneup --dry-run       → scan + report what would change, touch nothing
    claude-tuneup help            → show this card

  Backups: every run snapshots configs + moved items to ~/.claude-tuneup/backups/<run-id>/.
  Undo anytime with "claude-tuneup restore".
  ```
- **`restore`** → undo a previous run, even in a later session. Do NOT run any cleanup step:
  1. List restore points: `node "$SKILL_DIR/scripts/restore.mjs" list` (timestamp, how many items removed, log size).
  2. Ask (AskUserQuestion, with the mandatory "What does this do?" button) which restore point to use.
  3. Ask the **scope**: "Full restore" / "Configs only" / "Removed items only" (plus the explain button). Configs-only is the safe pick when the dev just wants a botched `CLAUDE.md`/`.claude.json` edit undone; items-only brings back deleted skills/dirs without touching configs.
  4. **Warn before applying.** A restore copies *old* configs back over the current ones. `.claude.json` carries live state (projects, session pointers) — so restoring it can drop projects/sessions created **after** the backup. Say this explicitly and confirm. The script protects you two ways: it first saves the **current** configs into a `pre-restore-…` folder (so the restore is itself reversible), and it never overwrites a newer item that re-took a removed path (those land at `<path>.restored-<ts>` instead).
  5. Apply: `node "$SKILL_DIR/scripts/restore.mjs" apply <RP> [--configs-only|--items-only]` — prints `restored`, `collisions` (items that couldn't take their original path and where they went), `preRestoreSnapshot` (the pre-restore safety copy, when configs were restored), and `manualReAdd` (marketplaces/plugins for you to replay).
  6. Validate restored JSON: `node "$SKILL_DIR/scripts/validate-json.mjs" ~/.claude.json ~/.claude/settings.json`. Report `collisions` to the dev so they resolve any `.restored-<ts>` items by hand. Offer to keep or purge the restore point + the pre-restore snapshot afterward.
- **`--dry-run`** → run STEPS 1–8 and 9 in **read-only mode**: scan, show what would be removed/consolidated/changed, include sizes, but **ask zero delete questions** and touch nothing — and that includes STEP 0.5: a dry run changes nothing, so do **NOT** create a restore point (it would only litter `~/.claude-tuneup/backups/` with empty entries). Skip stash/move/rm entirely. Report "DRY RUN — nothing was changed" in the summary. Good for first-time users.
- **Argument given** (a group/steps) → run exactly that. Accept group names (`cleanup`, `claude.md`, `soul.md`, `summary`), step numbers, or ranges (`1-3`, `step 5`, `6,7`). Then run STEP 11. Be lenient on aliases (`insights` → `claude.md`, `soul` → `soul.md`).
- **No argument** → offer the choice via AskUserQuestion before touching anything: options = "Full tune-up (1–11)", "Cleanup only (1–8)", "CLAUDE.md from /insights (9)", "Build SOUL.md (10)". Let them pick one (multiSelect ok for combining claude.md + soul.md).

Always finish a run with STEP 11 (summary) scoped to whatever ran. Announce each step as you enter it. Once the run's groups are decided, read the matching `references/*.md` playbook(s) before starting.

---

### STEP 0.5: Restore point (before ANY change)

A tune-up must be undoable. Before the first **mutation** of the run (not on dry runs), create a restore point and log every action into it.

Backups live in a **stable location outside the skill** — `~/.claude-tuneup/backups/<run-id>/` (override with `$CLAUDE_TUNEUP_STATE`). This is on purpose: a skill update, reinstall, or move between `~/.claude/skills` and `~/.agents/skills` must **not** take the undo history with it. Snapshots are chmod-restricted (owner-only) because `.claude.json` can carry tokens. `restore` still scans the legacy in-skill `.backups/` too, so older restore points keep working.

```bash
RP=$(node "$SKILL_DIR/scripts/backup.mjs" create)   # snapshots configs, prints the restore-point path
```

`backup.mjs create` snapshots the small irreplaceable config files (`.claude.json`, `settings*.json`, `CLAUDE.md`, `SOUL.md`), seeds `actions.log` + `removed.json`, and names the restore point with a collision-proof run id (so two runs in the same second never clobber each other).

Deletion policy:
- **Unique / irreplaceable** (real skills, project data, configs, anything the dev can't easily regenerate) → `node "$SKILL_DIR/scripts/backup.mjs" stash "$RP" <path>` (moves it into the restore point, logged + restorable), never `rm`.
- **Self-regenerating artifacts** (venvs, plugin caches) → hard `rm` is fine; they rebuild. OS cruft (`.DS_Store`, `Thumbs.db`) → skip entirely.
- **Marketplace / plugin removals** → can't move; record the re-add command: `node "$SKILL_DIR/scripts/backup.mjs" log "$RP" "marketplace removed: <name> (re-add: claude plugin marketplace add <url>)"`.
- Config edits are covered by the snapshot above.

Tell the dev the restore point exists and how to undo (see STEP 11). Only ONE restore point per run; if a step is skipped, the snapshot is still valid.

---

## Main flow

1. STEP 0 routing decided which groups run.
2. For each selected group, **read its playbook** (`references/cleanup.md`, `references/claude-md.md`, `references/soul-md.md`) and execute its steps in order, announcing each step.
3. Finish with STEP 11 below.

---

### STEP 11: Final summary

Report total size after cleanup (`du -sh ~/.claude/` or sum the scan sizes), removed items (with sizes), skills consolidated in `~/.agents/skills/`, links created, `SOUL.md` created + wired (if the dev opted in), and pending suggestions.

**How to undo** — always show this, pointing at the run's restore point `$RP` (`~/.claude-tuneup/backups/<run-id>/`):
- Restore everything, or selectively: `node "$SKILL_DIR/scripts/restore.mjs" apply $RP [--configs-only|--items-only]`.
- Recover a single removed item by hand: it's in `$RP/removed/` — move it back.
- Re-add a marketplace/plugin: see the exact command in `$RP/actions.log`.
- Self-regenerating artifacts (venvs/caches) weren't backed up — they rebuild on next use.

Then, via AskUserQuestion, ask if the result looks good:
- **"Looks good — purge restore point"** → `rm -rf $RP` (frees the space held by removed items).
- **"Keep backup for now"** → leave `$RP`; mention old restore points under `~/.claude-tuneup/backups/` can be pruned later.
- **"Undo everything"** → `node "$SKILL_DIR/scripts/restore.mjs" apply $RP`, then replay re-add commands from `actions.log`.

---

## Rules

1. **NEVER delete without explicit confirmation** from the dev
2. Always show size and a summarized content before asking
3. Advance step by step, don't skip
4. When editing JSON (`.claude.json`, `settings.json`), validate after every edit with `node "$SKILL_DIR/scripts/validate-json.mjs" <file>` (never assume `python3` exists). Back up the file first if it isn't already in the restore-point snapshot.
5. Before deleting a directory, confirm it isn't a symlink to something important
6. **All decisions via AskUserQuestion buttons** — never free-text y/n. **EVERY question must include a "What does this do?" button** (no exceptions, even an obvious-looking delete); picking it inspects + explains that item, then re-asks. See "How to ask the dev".
7. **Size beats labels** — measure everything, drill into any dir ≥ 50M even if marked "internal/keep"
8. **Verify deletes stuck** — re-measure after deleting big artifacts; if it regenerated, the real fix is disabling the owning plugin
9. **`CLAUDE.md` + `SOUL.md` stay lean** — each ≤ 200 lines / ~1500 tokens; every line must change behavior. They load into every session, so bloat is a permanent token tax — and **imports load at launch too**, so in an AGENTS.md shim setup the budget covers the *combined* total (`memory` scan's `combinedApproxTokens`). Trim before adding.
10. **Trust scan flags over assumptions** — if `plugins.listingReliable` is `false`, never propose uninstalls based on the listing; if an MCP's `transport` is `remote`, never touch it as a local file.
