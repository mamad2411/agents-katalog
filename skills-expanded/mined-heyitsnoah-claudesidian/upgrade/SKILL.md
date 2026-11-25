---
name: upgrade
description: Intelligently upgrade claudesidian with new features while preserving user customizations using AI-powered semantic analysis. Use when the user wants to upgrade claudesidian, pull in upstream changes, or update their installation.
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, WebFetch, Grep, Glob]
---

# Smart Upgrade

Pulls the latest claudesidian from GitHub and merges it into the user's vault,
preserving customizations.

## Layout assumptions (READ FIRST)

claudesidian stores skills under **`.agents/skills/<name>/SKILL.md`** as the
canonical location. Symlinks live at `.claude/skills/<name>` and
`.pi/skills/<name>` pointing back to canonical. Edit canonical, all consumers
follow.

If the user is on a pre-conversion claudesidian (anything before the
commands→skills migration) they will have `.claude/commands/*.md` instead and
no `.agents/skills/`. **Do not run a normal upgrade in that case** — see
"Migration from legacy layout" at the bottom of this file.

If the user's local repo has `.agents/skills/` populated, proceed normally.

## Process

### 1. Version check

- Read current version from `package.json`
- Fetch upstream version:
  ```bash
  CURRENT=$(grep '"version"' package.json | head -1 | cut -d'"' -f4)
  LATEST=$(curl -s https://raw.githubusercontent.com/heyitsnoah/claudesidian/main/package.json | grep '"version"' | head -1 | cut -d'"' -f4)
  if [ "$CURRENT" = "$LATEST" ]; then
    echo "✅ Already on $CURRENT"
    exit 0
  fi
  ```
- Detect layout: `test -d .agents/skills && echo NEW || echo LEGACY`. If
  LEGACY, jump to "Migration from legacy layout".

### 2. Backup

```bash
BACKUP_DIR=".backup/upgrade-$(date +%Y-%m-%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r .agents .claude .pi .scripts package.json "$BACKUP_DIR/" 2>/dev/null
cp CHANGELOG.md README.md "$BACKUP_DIR/" 2>/dev/null || true
echo "✅ Backup created at $BACKUP_DIR"
```

### 3. Fetch upstream

```bash
git clone --depth=1 --branch=main \
  https://github.com/heyitsnoah/claudesidian.git \
  .tmp/claudesidian-upgrade
```

The user's working repo stays disconnected from origin throughout — we only
ever read from `.tmp/`.

### 4. Build upgrade checklist

System files we care about:

- **Skills**: `.agents/skills/<name>/SKILL.md` (canonical) — also resources
  inside skill dirs (helper scripts, references).
- **Hooks**: `.claude/hooks/*.sh`
- **Settings**: `.claude/settings.json`
- **MCP servers**: `.claude/mcp-servers/*`
- **Scripts**: `.scripts/*`
- **Core**: `package.json`, `CHANGELOG.md`, `README.md`

Files we **never touch**:

- User content folders: `00_Inbox/`, `01_Projects/`, `02_Areas/`,
  `03_Resources/`, `04_Archive/`, `05_Attachments/`, `06_Metadata/` (except
  `06_Metadata/Templates/` if upstream changes them)
- The user's `CLAUDE.md`
- `.obsidian/` (user's Obsidian settings)
- `vault-config.json`
- `.mcp.json` (contains API keys)
- Anything in `.git/`

Build the checklist:

```bash
# Skills that exist in both, or only upstream, or only local
diff -qr .agents/skills .tmp/claudesidian-upgrade/.agents/skills 2>/dev/null

# Hooks, settings, mcp-servers, scripts
diff -qr .claude/hooks .tmp/claudesidian-upgrade/.claude/hooks 2>/dev/null
diff -q .claude/settings.json .tmp/claudesidian-upgrade/.claude/settings.json 2>/dev/null
diff -qr .claude/mcp-servers .tmp/claudesidian-upgrade/.claude/mcp-servers 2>/dev/null
diff -qr .scripts .tmp/claudesidian-upgrade/.scripts 2>/dev/null

# Core files
diff -q package.json .tmp/claudesidian-upgrade/package.json
diff -q README.md .tmp/claudesidian-upgrade/README.md
diff -q CHANGELOG.md .tmp/claudesidian-upgrade/CHANGELOG.md
```

Write findings to `.upgrade-checklist.md`, grouped by category, with status
markers `[ ] pending`, `[x] updated`, `[-] skipped`.

### 5. File-by-file review

**Hard rules — do not skip:**

- Always show the diff before modifying anything.
- Always wait for the user's choice. Never auto-pick.
- Never use `cp -f`. Use `cat src > dest` for non-interactive overwrite.
- Update `.upgrade-checklist.md` after every file.

For each file in the checklist:

1. Show `diff -u local upstream`.
2. Determine state:
   - **No local edits, no upstream edits** → mark `[-]` skipped, move on.
   - **Upstream changed, no local edits** → ask: apply / keep / view full
     diff.
   - **Both changed (local customization)** → ask: keep yours / take upstream
     / view full diff / AI-merge.
3. Ask the user:
   ```
   File: <path> has updates.
   1. Apply update (take upstream)
   2. Keep your version
   3. View full diff
   4. AI-merge

   Choice (1/2/3/4):
   ```
   **Wait for input. Do not auto-select.**
4. Apply the chosen action:
   ```bash
   # Option 1
   if [ -f ".tmp/claudesidian-upgrade/$path" ]; then
     mkdir -p "$(dirname "$path")"
     cat ".tmp/claudesidian-upgrade/$path" > "$path"
     echo "✅ Updated $path"
   fi
   ```
5. Mark in checklist and continue.

### 6. Symlink hygiene (skills only)

After updating any skill in `.agents/skills/<name>/`, verify the symlinks in
`.claude/skills/<name>` and `.pi/skills/<name>` still resolve:

```bash
for name in $(ls .agents/skills); do
  for agent in claude pi; do
    link=".${agent}/skills/${name}"
    target="../../.agents/skills/${name}"
    mkdir -p ".${agent}/skills"
    if [ -L "$link" ]; then
      # Symlink exists — verify it points to the right place
      current="$(readlink "$link")"
      if [ "$current" != "$target" ]; then
        rm "$link"
        ln -s "$target" "$link"
        echo "✅ Repaired symlink $link (was → $current)"
      fi
    elif [ -e "$link" ]; then
      # Real file or directory at this path — do not trample user data
      echo "⚠️  $link exists as a real file/dir, not a symlink. Skipping."
      echo "    Manual fix: inspect, back up if needed, then rm and rerun."
    else
      # Nothing there — create
      ln -s "$target" "$link"
      echo "✅ Created symlink $link"
    fi
  done
done
```

The `-L` test is critical: a broken symlink (target missing) returns false from
`-e` but true from `-L`, so checking `-e` alone would try to `ln -s` over the
existing broken link and fail with "File exists". Conversely, a symlink
pointing the wrong way would pass `-e` (because the wrong target still exists)
and silently stay wrong. Always check `-L` first, then verify the target with
`readlink`, then fall through to `-e` for real files, then create if nothing
exists.

If upstream introduced a brand-new skill, this loop also creates its symlinks.

### 7. Verification

Re-run the diff commands from step 4. The only differences should be files the
user explicitly chose to keep (marked `[-]` or `[x] customized` in the
checklist). Anything still pending `[ ]` is a bug — report it and let the user
decide whether to retry.

### 8. Final steps

- Update `package.json` version to match upstream
- `rm -rf .tmp/claudesidian-upgrade`
- Save the final `.upgrade-checklist.md` to the backup dir for reference
- Print a summary: updated count, skipped count, customized count

## Conflict resolution philosophy

When a skill has both upstream and local edits, prefer **AI-merge** over
"take upstream." The user's local edit usually represents an intentional
preference (their voice, their workflow conventions). The upstream edit
usually represents a new feature or bug fix. Almost always you can keep both.

Show your merge proposal as a concrete diff before applying. Don't paraphrase.

## Update categories

### Auto-safe (low risk, default to "apply")

- Brand-new skills upstream introduced (additive — just symlink in)
- Hook script updates (`.claude/hooks/*.sh`) when local hasn't changed
- `package.json` dependency bumps in `dependencies` / `devDependencies`
  (preserve user-added scripts in the `scripts` section)
- `CHANGELOG.md` (always replace with upstream version)
- New files in `.scripts/`

### Needs review (always ask)

- Skills the user has touched
- `.claude/settings.json` (often has user-added hooks)
- `package.json` `scripts` section
- `README.md`
- MCP server files

### Never touch

See the "files we never touch" list in step 4.

## Error handling

- **No internet** → fail gracefully, suggest retry
- **GitHub rate limit** → wait + retry once, then fail with the rate-limit
  reset time
- **Merge conflict during AI-merge** → show both versions, ask user to pick
- **`rm -rf .tmp/claudesidian-upgrade` fails** → leave it, warn the user

## Rollback

The backup directory from step 2 is the rollback target. Manual rollback:

```bash
cp -r .backup/upgrade-<timestamp>/.agents .
cp -r .backup/upgrade-<timestamp>/.claude .
cp .backup/upgrade-<timestamp>/package.json .
# etc.
```

Don't try to be clever with selective rollbacks — restore the whole snapshot.

## Migration from legacy layout

If `test -d .agents/skills` returns false, the user is on a pre-conversion
claudesidian. Their skills live in `.claude/commands/*.md`. **A normal upgrade
will not work** — the diff will show every command as "removed locally" and
every skill as "added upstream."

The migration path:

1. **Stop and explain.** Tell the user their layout predates the
   commands→skills conversion and offer to migrate.
2. **Backup first** (step 2 above, but include `.claude/commands/`).
3. **Move command files** to skill dirs:
   ```bash
   mkdir -p .agents/skills
   for f in .claude/commands/*.md; do
     [ -f "$f" ] || continue
     name=$(basename "$f" .md)
     [ "$name" = "README" ] && continue
     mkdir -p ".agents/skills/$name"
     mv "$f" ".agents/skills/$name/SKILL.md"
   done
   ```
4. **Add `name`/`description` frontmatter** to any file that lacks it. Use the
   `add-frontmatter` skill.
5. **Create symlinks** for `.claude/skills/` and `.pi/skills/` (see step 6).
6. **Validate frontmatter.** Use the `quick_validate.py` script bundled with
   the `skill-creator` skill in this repo:
   ```bash
   for d in .agents/skills/*/; do
     uv run --with pyyaml python \
       .agents/skills/skill-creator/scripts/quick_validate.py "$d"
   done
   ```
   This enforces the full skill schema (name, description, allowed-tools,
   compatibility, license, metadata) and will reject any file with extra or
   missing required keys.

   If `uv` is not installed or `skill-creator` is somehow missing, fall back
   to this minimal inline check that only verifies `name` and `description`
   are present:
   ```bash
   for f in .agents/skills/*/SKILL.md; do
     dir=$(basename "$(dirname "$f")")
     awk '
       BEGIN { in_fm=0; has_name=0; has_desc=0 }
       /^---$/ { in_fm++; next }
       in_fm==1 && /^name:/ { has_name=1 }
       in_fm==1 && /^description:/ { has_desc=1 }
       END {
         if (!has_name) print "  ✗ missing name"
         if (!has_desc) print "  ✗ missing description"
         if (has_name && has_desc) print "  ✓ ok"
       }
     ' "$f" | sed "s|^|  $dir: |"
   done
   ```
7. **Then run the normal upgrade flow** to pull in any additional upstream
   changes.

This migration is one-time. After it runs successfully, future upgrades use
the normal flow.

## Selective upgrades

Common subset commands the user may ask for:

- "Just update skills" → only diff `.agents/skills/`
- "Just dependencies" → only update `package.json` deps
- "Just hooks" → only diff `.claude/hooks/`

Treat these as filters on the checklist. Same review/confirm rules apply.
