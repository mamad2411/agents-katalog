---
name: setup-rayleigh
description: >
  Install and initialize the rayleigh-coding plugin (skills + /vatsal-mode)
  for this Cursor environment and the user-global Cursor home. Detects Task
  slugs and writes the always-applied category rule (default / executor /
  wise-owl). Use for /setup-rayleigh, first-time install, "enable
  rayleigh-coding", "configure rayleigh models", or resetting those defaults.
---

# Setup rayleigh-coding

Install the **rayleigh-coding** plugin so its skills and `/vatsal-mode` are
available, then initialize model policy.

Do **not** ask which models to use. Do **not** set `disable-model-invocation`
on this skill or on `/vatsal-mode`. Write the ensemble below unless the human
in this session says to stay on `auto`.

## Goals

1. Plugin loadable in this environment (Cloud Agent env and/or local Cursor).
2. Same install available user-globally under `~/.cursor/plugins/local/`.
3. Always-applied model rule with three stable categories.
4. Confirm `/vatsal-mode` is the next step.

## Steps

### 1. Detect current state

Check, in order:

| Probe | Meaning |
|---|---|
| This skill is already executing from the plugin | Marketplace or local plugin is loaded for this session |
| `~/.cursor/plugins/local/rayleigh-coding/.cursor-plugin/plugin.json` exists | User-global local install present |
| Workspace `.cursor/rules/rayleigh-models.mdc` or `~/.cursor/rules/rayleigh-models.mdc` | Model rule already written |

Record what is missing. Do not invent host paths beyond `$HOME` / `~/.cursor`.

### 2. Install user-global (local plugin path)

Ensure Cursor can load the plugin from the documented local path. The loaded
directory itself must contain `.cursor-plugin/plugin.json` (nested marketplace
layout → symlink the nested plugin folder).

Prefer the bundled installer (handles absolute paths, git worktrees, dest
guards, and manifest validation):

```bash
bash <path-to-setup-rayleigh>/scripts/install_local.sh
```

`<path-to-setup-rayleigh>` is the directory that contains this `SKILL.md`
(plugin skills tree, local install, or marketplace cache). If you cannot
resolve that path, run the equivalent:

```bash
set -euo pipefail
mkdir -p ~/.cursor/plugins/local
SRC_RAW="${RAYLEIGH_CODING_SRC:-$HOME/.cursor/plugins/local/rayleigh-coding-src}"
SRC="$(python3 -c 'import os,sys; print(os.path.realpath(os.path.expanduser(sys.argv[1])))' "$SRC_RAW")"
if git -C "$SRC" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  TOPLEVEL="$(git -C "$SRC" rev-parse --show-toplevel)"
  if ! python3 -c 'import os,sys; raise SystemExit(0 if os.path.samefile(sys.argv[1], sys.argv[2]) else 1)' "$SRC" "$TOPLEVEL"; then
    echo "error: $SRC is inside git work tree $TOPLEVEL; set RAYLEIGH_CODING_SRC to the clone root" >&2; exit 1
  fi
  SRC="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$TOPLEVEL")"
  git -C "$SRC" pull --ff-only || echo "warning: pull failed; using existing tree"
elif [ -e "$SRC" ]; then
  echo "error: $SRC is not a git work tree" >&2; exit 1
else
  git clone https://github.com/VatsalSy/rayleigh-coding.git "$SRC"
fi
if [ ! -f "$SRC/scripts/validate_marketplace.py" ] || [ ! -f "$SRC/scripts/validate_skills.py" ]; then
  echo "error: missing validators under $SRC/scripts" >&2; exit 1
fi
python3 "$SRC/scripts/validate_marketplace.py"
python3 "$SRC/scripts/validate_skills.py"
DEST="$HOME/.cursor/plugins/local/rayleigh-coding"
if [ -e "$DEST" ] && [ ! -L "$DEST" ]; then
  echo "error: $DEST exists and is not a symlink; remove or rename it" >&2; exit 1
fi
ln -sfn "$SRC/plugins/rayleigh-coding" "$DEST"
test -f "$DEST/.cursor-plugin/plugin.json"
echo "installed: $DEST -> $SRC/plugins/rayleigh-coding"
```

Optional override: set `RAYLEIGH_CODING_SRC` to an existing clone or worktree
(absolute or relative to the current working directory).

### 3. Marketplace / Cloud Agent environment

If this session is a Cursor Cloud Agent or the user prefers Import Marketplace:

1. Tell them (once): **Settings → Plugins → Import Marketplace** →
   `https://github.com/VatsalSy/rayleigh-coding` → enable **rayleigh-coding**.
2. For a Cloud Agents environment, enable the same marketplace plugin on that
   environment so new agent runs inherit it.
3. Ask them to **Developer: Reload Window** (or start a new agent) after install
   if skills are not yet visible.

Do not pretend the UI click succeeded without a receipt (plugin path present,
or this skill / `/vatsal-mode` resolving after reload).

### 4. Write model rules (ensemble by default)

Categories are stable. Concrete slugs are the current Cursor mapping and can
be swapped later without renaming the categories.

| Category | Job | Family (current) |
|---|---|---|
| `default` | Lead chat and anything the user reads | latest Cursor Grok |
| `executor` | Grunt `Task` / swarm / parallel waves once the brief is complete | latest Composer |
| `wise-owl` | Rare second opinion. Advise only. High effort only | latest Cursor Grok at high effort |

`auto` / `inherit-parent` remain first-class: omit the Task `model` field so
the child follows the parent chat. Write all three as `auto` only when the
human in this session says to stay on Auto, or on an explicit "reset to auto".

Touch **only** these two files when writable (never other `.cursor/rules`
files):

1. User-global: `~/.cursor/rules/rayleigh-models.mdc`
2. This workspace / env: `.cursor/rules/rayleigh-models.mdc`

Create parent directories as needed.

**Detect, then pick. Never invent a slug.**

1. Enumerate the slugs the `Task` tool accepts in *this* session. That list
   is the dependable source. A models API or CLI may complete it, but every
   real slug you write must still be in the Task set.
2. Run the bundled picker (same directory as this skill's `scripts/`):

```bash
python3 <path-to-setup-rayleigh>/scripts/pick_models.py --format rule -- <detected slugs...>
```

Use `--policy auto --format rule` when the human asked to stay on Auto.
If you cannot detect any slugs, run `--policy auto` and say so.

The picker allowlists only Grok and Composer (Cursor first-party models).
Every third-party family (Claude/Opus/Sonnet, GPT/Codex, Gemini, Kimi,
DeepSeek, Llama, ...) is forbidden even when it appears in the Task set.
Wise-owl accepts Grok at **high** effort only (not max, not extra-high). A missing family becomes `auto`.

**Write policy (no confirmation gate):**

- Human said "stay on auto" / "reset to auto": overwrite both files with the
  picker `--policy auto` rule.
- Otherwise write the detected ensemble. Overwrite the old six-role shape
  (`code`, `judgment`, `review`, `swarm workers`, `parallel-task`).
- If a file already has `default` / `executor` / `wise-owl` set to a real
  slug that is still in the detected set **and** eligible for that category
  under the picker, keep that pin. Replace `auto`, unavailable, and
  ineligible slugs with the new pick unless the human asked to stay on Auto.

Do not prompt for model picks. Do not write a slug the picker did not emit.

### 5. Confirm

Tell the user:

- Local plugin path (if installed) and whether marketplace enablement is still needed
- The three category values written (and which family fell back to `auto`)
- Which rule paths were written or skipped, and why
- New chats / reloaded windows pick up the rule
- Next command: `/vatsal-mode`

Re-running `/setup-rayleigh` is safe: pull + relink + rewrite the three
categories from the current Task set (respecting the pin / auto rules above).
