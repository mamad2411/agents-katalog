---
name: audit-local-plugins
argument-hint: '[plugin-name | all] — omit to audit every plugin under plugins/'
description: >
  Project skill for this repo (ember-claude-toolkit). Diffs Sara's local
  Claude Code and Cursor installs (~/.claude/skills, ~/.claude/agents,
  ~/.cursor/skills, ~/.cursor/agents) against the canonical sources under
  plugins/, reports what drifted, and asks whether to promote local→kit,
  reinstall kit→local, or skip. Trigger on "/audit-local-plugins", "audit
  local plugins", "check local vs kit", "did my local skills drift", or
  "should we update the kit from local".
---

# audit-local-plugins

Reconcile **what Sara actually runs locally** with **what this repo ships**.

This is the missing middle between day-to-day editing under `~/.claude/skills/`
(and Cursor copies) and `/refresh-plugins` (publish kit → marketplace). Local
installs are often **copies**, not live symlinks — they drift. This skill
finds that drift, shows what changed, and **asks** before moving anything.

Read-only until Sara explicitly picks an action. Never auto-promote, never
auto-reinstall, never commit/tag/push.

## 1. Run the audit

```
bash .claude/skills/audit-local-plugins/scripts/audit.sh [plugin-name|all]
```

If Sara named a plugin when invoking `/audit-local-plugins`, pass that name.
Otherwise pass `all` (or omit — the script defaults to `all`).

Read the full output. Status meanings:

| Status | Meaning |
|---|---|
| `LIVE` | Local path is a symlink into this repo — edits here are already what she runs |
| `SAME` | Local is a real copy, content identical to kit |
| `DRIFTED` | Local and kit both exist, content differs |
| `MISSING_LOCAL` | Kit has it; no local install at the expected path |
| `MISSING_KIT` | Expected kit path missing (unusual — broken plugin layout) |
| `NOT_PLUGIN_ROOT` | `~/.claude/skills/<plugin>` exists but is a flat skill/copy, not a plugin-root install — real drift is under `[claude-skill]` |

Also note:

- **`[plugin-link]`** — `~/.claude/skills/<plugin-name>` as a whole-plugin
  symlink/copy (the `@skills-dir` shape `/refresh-plugins` assumes).
- **`[claude-skill]` / `[claude-agent]`** — flat installs Claude Code loads
  directly (`~/.claude/skills/<skill>`, `~/.claude/agents/<agent>.md`).
- **`[cursor-skill]` / `[cursor-agent]`** — Cursor port copies under
  `~/.cursor/…` vs `plugins/<name>/cursor/…`.
- **`local-only`** — skills under `~/.claude/skills/` that are not part of
  any kit plugin (email, skippy, resume-*, etc.). List them; do **not** offer
  to add them to the kit unless Sara explicitly asks (that is a new-plugin
  flow, not this skill).

## 2. Summarize drift for Sara

Lead with the summary counts from the script footer.

Then, for every `DRIFTED` item, give a short human summary:

1. Plugin + kind + name
2. The file list the script already printed (do not dump full file contents
   unless Sara asks, or the drifted set is tiny — e.g. a single SKILL.md)
3. A one-line guess at direction from mtimes (`local looks newer` /
   `kit looks newer` / `unclear`) — **mtime is a hint only**, not proof

Call out a common trap when both exist:

- A `LIVE` plugin-root symlink **and** a `DRIFTED` flat `claude-skill` with
  the same logical skill (e.g. `delivery-team` linked + `~/.claude/skills/team-intake`
  as a stale copy). Flat copies can still be what the tool loads. Say so
  plainly.

If nothing drifted and nothing material is `MISSING_LOCAL`, report that and
stop — no question needed.

## 3. Human gate — ask before any write

Use a question (AskUserQuestion when available, otherwise ask in chat) with
**per-plugin** choices when multiple plugins drifted. Offer:

- **Promote local → kit** — copy local content into `plugins/<name>/…`
- **Reinstall kit → local** — overwrite local install from the kit
- **Skip** — leave this plugin alone
- **Skip all** — stop

Do **not** combine promote and reinstall for the same pair in one pass.
Do **not** touch `local-only` skills in this gate.

If Sara picks nothing / cancel / skip-all: stop. Report what was audited,
write nothing.

## 4. Apply the chosen action

### Promote local → kit

For each approved plugin, copy **only the drifted pairs Sara approved**:

| Kind | From | To |
|---|---|---|
| `claude-skill` | `~/.claude/skills/<skill>/` | `plugins/<plugin>/skills/<skill>/` |
| `claude-agent` | `~/.claude/agents/<agent>.md` | `plugins/<plugin>/agents/<agent>.md` |
| `cursor-skill` | `~/.cursor/skills/<skill>/` | `plugins/<plugin>/cursor/skills/<skill>/` |
| `cursor-agent` | `~/.cursor/agents/<agent>.md` | `plugins/<plugin>/cursor/agents/<agent>.md` |

Rules:

- Prefer `cp -R` (or equivalent) over hand-editing file-by-file.
- **Never** promote through a `LIVE` symlink pair — there is nothing to
  promote; local already *is* the kit.
- Warn before overwriting kit files that look like shared templates with
  personal runtime state mixed in (e.g. `config/library-locations.json`,
  fattened `memory/*` logs). If unsure, ask Sara whether to include those
  paths or leave the kit versions.
- After promote: working tree under `plugins/<name>/` is dirty. Tell Sara
  the next steps are **`/sanitize-plugins <name>`** then
  **`/refresh-plugins <name>`** — do **not** run them automatically unless
  she asks in the same turn.
- Do not commit, tag, or push from this skill.

### Reinstall kit → local

For each approved plugin:

**Claude Code — preferred (live symlink), if Sara agrees:**

```
# plugin-root (loads nested skills/agents from the repo)
ln -sfn "$(pwd)/plugins/<plugin>" ~/.claude/skills/<plugin>
```

When a flat `~/.claude/skills/<skill>` **copy** is also drifted and Sara
wants the kit to win, either:

- **Remove the flat copy** so only the plugin-root symlink remains (cleaner
  long-term — ask first; deleting local skills is destructive), or
- **Overwrite the flat copy** from `plugins/<plugin>/skills/<skill>/`.

Same for agents: overwrite `~/.claude/agents/<agent>.md` from
`plugins/<plugin>/agents/<agent>.md` when she chose reinstall for those
pairs.

**Cursor:**

```
node scripts/install.mjs cursor <plugin>
```

That copies `plugins/<plugin>/cursor/{skills,agents}/` into `~/.cursor/`.
Remind Sara to restart Cursor (or reload skills) afterward.

Never hand-edit `~/.claude/plugins/cache/…`.

## 5. Re-audit and report

Re-run the audit script for the plugins that were touched. Confirm they
moved to `LIVE` or `SAME` as expected. End with:

- What was promoted / reinstalled / skipped
- Anything still drifted
- Reminders: sanitize + refresh-plugins after a promote; restart tool after
  a reinstall

## Notes

- Source of truth for publishing is always `plugins/<name>/` in this repo —
  never `~/.claude/plugins/cache/…`.
- This skill does not replace `/sanitize-plugins` or `/refresh-plugins`; it
  feeds them.
- Gemini / Antigravity installs are out of scope unless Sara asks to extend
  the audit — Cursor + Claude Code cover the drift she hit.
