---
name: geno-init
description: Initialize an OpenGeno feature tree for a project. Asks the user to pick a documentation language (English or Chinese, default English), a drift mode, and a generation mode (stub-only by default, or one-shot full docs that fills every L3 section now). Scans the codebase, proposes a module breakdown, generates the L1 root index, L2 module indexes and L3 feature docs in the chosen language, writes .feat-tree.json, and injects the OpenGeno workflow rules into CLAUDE.md (and AGENTS.md if present). Use when starting OpenGeno on a new project. Run once per project.
user-invocable: true
allowed-tools: "Read Write Edit Bash Glob Grep AskUserQuestion"
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "S=\"\"; for P in \"${CLAUDE_SKILL_DIR:-}/scripts/post-edit-warn.sh\" \"${CLAUDE_PLUGIN_ROOT:-}/skills/geno-init/scripts/post-edit-warn.sh\" \"${CLAUDE_PLUGIN_ROOT:-}/scripts/post-edit-warn.sh\" \"$HOME/.claude/skills/geno-init/scripts/post-edit-warn.sh\" \".claude/skills/geno-init/scripts/post-edit-warn.sh\"; do [ -f \"$P\" ] && S=\"$P\" && break; done; [ -n \"$S\" ] && bash \"$S\" 2>/dev/null || true"
  Stop:
    - hooks:
        - type: command
          command: "S=\"\"; for P in \"${CLAUDE_SKILL_DIR:-}/scripts/stop-check.sh\" \"${CLAUDE_PLUGIN_ROOT:-}/skills/geno-init/scripts/stop-check.sh\" \"${CLAUDE_PLUGIN_ROOT:-}/scripts/stop-check.sh\" \"$HOME/.claude/skills/geno-init/scripts/stop-check.sh\" \".claude/skills/geno-init/scripts/stop-check.sh\"; do [ -f \"$P\" ] && S=\"$P\" && break; done; [ -n \"$S\" ] && bash \"$S\" || true"
metadata:
  version: "0.1.0"
---

# /geno-init

Bootstrap an OpenGeno feature tree for a project. Run **once** per
project. If `feat-tree/` already exists, abort and direct the user to
`/geno-sync` instead.

This skill is the only command needed to set up the tree — and the only
way to introduce the OpenGeno workflow rules into CLAUDE.md / AGENTS.md.

## Pre-flight

```bash
test -d feat-tree && echo "tree exists, abort" || echo "ok to init"
```

If the tree exists, **stop**. Tell the user to use `/geno-sync` for
drift, or to manually add new feature docs from the templates in this
skill's `templates/` directory.

## Workflow

### Step 1 — Pick the documentation language

Use `AskUserQuestion`:

- Question: "Which language should OpenGeno write the feature tree in?"
- Options (English first, marked recommended):
  1. **English** (Recommended)
  2. **中文 (Chinese)**

Store the choice as `LANG = "en"` or `LANG = "zh"`. **Critical**: from
this point on, every file you write under `feat-tree/`, every section
heading, every prose line, every comment, every example value, every
TODO placeholder MUST be in the chosen language. Do not mix languages
within the tree.

If the user picks Chinese, you must write Chinese exclusively for the
rest of this skill's execution. Do not silently fall back to English
even for "small" things like field labels — the user will read every
doc in their chosen language; mixing is jarring.

### Step 2 — Pick the drift mode

Use `AskUserQuestion`, phrased in the chosen language:

- Options:
  1. **Warn** (default): print drift summary at session-end, do not block
  2. **Block**: refuse to end session if drift exists

Store as `DRIFT_MODE`.

### Step 3 — Pick the generation mode

Use `AskUserQuestion`, phrased in the chosen language:

- Options:
  1. **Stub** (Recommended): shallow scan, generate L3 stubs, fill on demand
  2. **One-shot full docs**: deeper scan, attempt to fill every L3 section now

Store as `MODE = "stub"` or `MODE = "full"`.

`stub` is the default because deeper code reading is expensive and
hallucination-prone — the user should opt in deliberately. `full` is
useful when the codebase is small and stable, and the user wants a
complete first-pass tree to review wholesale rather than incrementally.

`MODE` controls two things downstream: scan depth in Step 4, and L3
body content in Step 8. Everything else is identical between modes.

### Step 4 — Scan the codebase

Scan depth depends on `MODE`:

- `MODE=stub` → shallow scan, structure only (current behavior).
- `MODE=full` → after the shallow pass identifies features, open the
  relevant route/controller/page/screen files for each feature and
  read enough to populate L3 sections in Step 8.

Glob for likely feature surfaces. Useful patterns:

| Stack | Look at |
|-------|---------|
| Flutter | `lib/features/**/`, `lib/pages/**/`, `lib/screens/**/`, route files |
| React/Next.js | `app/**/page.tsx`, `pages/**/*.tsx`, `src/features/**/`, `src/routes/**/` |
| iOS (Swift) | `*ViewController*`, `Scene*`, navigation graph |
| Android | `*Activity*`, `*Fragment*`, navigation graph |
| Backend | route/controller files, top-level service classes |

Identify:

1. **Top-level modules** — major user-facing areas (auth, profile, feed, …)
2. **Sub-features** within each — specific screens, flows, or logic units
3. **Out-of-scope items** — i18n, theming, build tooling, analytics

For `MODE=stub`, keep the scan shallow — the goal is a *proposal*, not
a finished tree. For `MODE=full`, the proposal pass is still shallow;
the deeper read happens per-feature during Step 8.

### Step 5 — Propose, in the user's language

Show the user the draft module list with one-line descriptions, **in
the chosen language**. Use `AskUserQuestion` (also in the chosen
language) to ask whether the proposal is acceptable.

Iterate until they accept.

### Step 6 — Generate L1 root index

Pick the right template:

- `LANG=en` → `templates/root-index.md`
- `LANG=zh` → `templates/root-index.zh.md`

Write `feat-tree/index.md` from the template, replacing placeholders:

- `{{PROJECT_NAME}}` — from package.json / pubspec.yaml / go.mod / etc.
- One row per accepted module
- `last_synced_commit:` left empty

All generated prose (module descriptions, etc.) must be in the chosen
language.

### Step 7 — Generate L2 module stubs

For each accepted module, write `feat-tree/<module>/index.md` from
`templates/module-index.md` or `templates/module-index.zh.md`. List the
proposed features as table rows. Module description and any free-form
text in the chosen language.

### Step 8 — Generate L3 feature docs

For each proposed feature, write an L3 doc using:

- UI feature → `templates/feature-ui.md` (en) or `templates/feature-ui.zh.md` (zh)
- Logic feature → `templates/feature-logic.md` (en) or `templates/feature-logic.zh.md` (zh)

Frontmatter is the same in both modes:

- `type`, `kind`, `feature`, `module` filled in
- `code:` filled from scan when known
- `last_synced_commit: ""` (always empty at init — the doc has not
  been reviewed against code yet, even in `full` mode)
- `last_reviewed:` today's date

Section bodies depend on `MODE`:

- **`MODE=stub`** (default): all section headings present in chosen
  language; section bodies set to placeholder text — `TODO` (English)
  or `待补充` (Chinese). L3 details get filled in incrementally on the
  first real task that touches each feature, driven by the workflow
  rules in CLAUDE.md.

- **`MODE=full`**: read the feature's source files (identified in
  Step 4) and write best-effort prose for each section, in the chosen
  language. Keep `last_synced_commit: ""` regardless — full-mode
  output is unverified by definition and a stale-or-empty SHA is
  what tells `/geno-sync` (and the user) that the doc still needs a
  review pass before any session bumps the SHA. Be honest in tone:
  if a section can't be inferred from the code, leave it as the
  placeholder text rather than guessing.

In neither mode should you set `last_synced_commit` to current HEAD —
the SHA represents *verified-against-code*, and init has not done that
work.

### Step 9 — Write `.feat-tree.json`

Copy `templates/feat-tree.json` to project root, then patch
`drift_mode` and `gen_mode` to the chosen values:

```json
{
  "version": 1,
  "tree_path": "feat-tree",
  "drift_mode": "warn",
  "gen_mode": "stub"
}
```

This file controls downstream behavior:

- `drift_mode` is read by the Stop hook at session-end.
- `gen_mode` records which generation mode the tree was bootstrapped
  with. `/geno-sync` reads it to distinguish empty-SHA docs that are
  *unwritten stubs* from empty-SHA docs that are *written-but-unverified
  full-mode prose* — the two need different reconciliation actions.

### Step 10 — Inject workflow rules into CLAUDE.md / AGENTS.md

Read the corresponding injection template:

- `LANG=en` → `templates/claude-md-injection.md`
- `LANG=zh` → `templates/claude-md-injection.zh.md`

Then for each of `CLAUDE.md` and `AGENTS.md` that already exists at
project root: **append** the injection text. Don't overwrite existing
content. Don't insert above existing content.

If neither file exists at project root, create `CLAUDE.md` with just
the injection text (`AGENTS.md` only created if it already exists).

The injection block is wrapped in `<!-- BEGIN OpenGeno -->` /
`<!-- END OpenGeno -->` markers so future re-runs or removals can
target it precisely.

If a `BEGIN OpenGeno` marker already exists in the target file, abort
the injection for that file (it was already injected) and warn the
user.

### Step 11 — Report

Print a summary in the chosen language:

- Documentation language chosen
- Drift mode chosen
- Generation mode chosen (`stub` or `full`)
- Number of modules created
- Number of L3 docs created
- Whether `CLAUDE.md` / `AGENTS.md` was created or appended
- Suggested next step:
  - `MODE=stub`: "Fill in L3 details on demand as you work — the first
    task that touches each feature should expand its stub."
  - `MODE=full`: "L3 bodies were generated from a one-shot code read
    and are **unverified**. Review each doc against the code before
    letting any session bump `last_synced_commit`. `/geno-sync` will
    keep flagging them as `STUB` until the SHA is set."

## Language enforcement (read this twice)

The user picked a language; they expect the tree to be in that language
end-to-end.

- All headings: chosen language
- All prose, table cells, descriptions: chosen language
- All examples and placeholder text: chosen language
- Code paths, slugs, frontmatter keys: stay as-is (they're identifiers,
  not language)
- File names: kebab-case English slugs even in Chinese projects
  (file-system-friendly, AI-stable)

If you find yourself about to write English in a Chinese tree because
"it's just a placeholder" or "the term is hard to translate" — stop
and translate. The user will notice; they will be annoyed.

The injection text in CLAUDE.md / AGENTS.md tells the AI on **future**
sessions to keep writing in the chosen language. Get it right on this
first pass and the rule perpetuates.

## Anti-patterns

| Don't | Why |
|-------|-----|
| Mix languages within the tree | Defeats the language-selection contract; will be visibly wrong |
| Auto-fill all L3 docs from code without the user opting in | Expensive, hallucination-prone — only do this when the user explicitly chose `full` mode in Step 3, and warn them in Step 11 that the output needs review |
| Set `last_synced_commit` to HEAD on a `full`-mode doc | Defeats the whole drift system — `full` output is unverified; SHA must stay empty until a human reviews against code |
| Silently merge with an existing tree | Risks overwriting hand-written content |
| Use the AI's first-pass module guess without user review | Module boundaries are a project-specific judgment call |
| Treat infra items (i18n, theme tokens, etc.) as features | Pollutes the tree, dilutes the signal |
| Set `last_synced_commit` to current HEAD on a stub | Misleading — stubs aren't synced |
| Forget to inject rules into CLAUDE.md / AGENTS.md | Without these, future sessions have no instruction to follow the workflow |
