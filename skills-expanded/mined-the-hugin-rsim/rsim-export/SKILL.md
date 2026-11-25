# Skill: rsim-export

**Purpose:** Collect local RSIm skill improvements (skills/ + commands/) and publish to GitHub as a PR.
**When:** After improve cycles with accumulated skill changes. Auto-suggested after `/improve`. Reminded at session start if > 7 days since last export.
**Requirements:** `gh` CLI installed and authorized (`gh auth login`), `git` installed.

---

## PROCESS

### Step 1 — Check state

1. Read `~/.claude/skills/sync-state.json`:
   - If not found — create from template (see below) and continue
   - Extract `base_repo`, `last_export`, `local_version`

2. If `base_repo` empty or null:
   ```
   Укажи URL базового репо (например: https://github.com/username/rsim):
   ```
   Wait for answer, save to `sync-state.json`.

3. Check `gh` CLI:
   ```bash
   gh --version
   ```
   If not found:
   ```
   gh CLI не установлен.
   Установи: https://cli.github.com/
   После установки выполни: gh auth login
   ```
   Stop.

4. Report to user:
   ```
   Последний экспорт: [last_export или "никогда"]
   Собираю изменения скиллов новее этой даты...
   ```

---

### Step 2 — Collect

Read `~/.claude/skills/changelog.md`. Find all lines where date > `last_export`
(if `last_export` = null — take all lines).

Extract:
- List of changed skill names (from changelog second column)
- For each unique skill — read full `~/.claude/skills/[name]/SKILL.md`

Scan `~/.claude/commands/` — list files modified after `last_export`.
Read each changed command file.

Ask:
```
Экспортировать новые записи из memory/semantic/patterns.md? (да / нет)
```
If "да" — read `~/.claude/memory/semantic/patterns.md`, extract entries added after `last_export`.

If nothing new (no skill changes, no command changes):
```
Нет новых улучшений для экспорта с [last_export].
Экспортировать нечего.
```
Stop.

---

### Step 2.2 — Pre-flight: personal data check

Before packaging, check collected skills for scripts/ subdirectories — these may contain
personal or project-specific scripts not intended for public distribution.

For each collected skill, check if `~/.claude/skills/[name]/scripts/` contains any files.

If scripts/ files found:
```
⚠️ Найдены файлы в scripts/:
  skills/[name]/scripts/[file]
  ...

scripts/ может содержать личные данные или проектные скрипты.
Исключить из экспорта? (да / нет)
```
- "да" (default) → exclude all scripts/ content from this skill's export, continue
- "нет" → include, but run security scan (Step 2.5) with extra scrutiny on these files

If no scripts/ files found → continue silently.

---

### Step 2.5 — Security scan

Read `~/.claude/skills/rsim-security-scan/patterns.md` and apply all patterns
to every collected file.

If suspicious pattern found:
```
⛔ SECURITY SCAN: подозрительный контент

Файл:      [filename]
Категория: [category]
Паттерн:   [pattern]
Строка:    "[quote]"

Этот фрагмент пропущен из экспорта.
```
Continue without that fragment. Do not stop the entire export.

---

### Step 3 — Preview + confirm

Show summary:
```
Готово к экспорту:
  Скиллы:           N изменений — [list]
  Commands:         M изменений — [list or —]
  Semantic patterns: K записей (opt-in)

Экспортировать? (да / нет)
```
Wait for explicit "да".

---

### Step 4 — Prepare contribution file

Form `contribution-YYYY-MM-DD.md`:

```markdown
# RSIm Contribution — YYYY-MM-DD
> exported via /rsim-export

## Modified Skills (N)

### skills/[name]/SKILL.md
[full content]

---
[repeat for each modified skill]

## Commands (M)

### commands/[name].md
[full content]

---
[repeat for each changed command]

## Semantic Patterns (K, opt-in)

[entries]
```

---

### Step 5 — Push to GitHub

```bash
CACHE_DIR="$HOME/.claude/.rsim-base-cache"
BASE_REPO="[base_repo from sync-state.json]"

# Clone or update cache
if [ -d "$CACHE_DIR/.git" ]; then
  cd "$CACHE_DIR" && git pull
else
  gh repo clone "$BASE_REPO" "$CACHE_DIR"
fi

# Create branch
cd "$CACHE_DIR"
BRANCH="contribution/$(date +%Y-%m-%d)"
git checkout -b "$BRANCH"

# Apply changes
# Copy changed SKILL.md files to skills/[name]/SKILL.md
# Copy changed command files to commands/
# Write contribution-YYYY-MM-DD.md to root
# If semantic patterns opted-in: append entries to memory/semantic/patterns.md

git add -A
git commit -m "feat: RSIm contribution from $(date +%Y-%m-%d)"
git push -u origin HEAD

gh pr create \
  --title "RSIm Contribution — $(date +%Y-%m-%d)" \
  --body "[auto-generated: N skill changes, M commands, K patterns]" \
  --base main
```

Show user the PR URL.

---

### Step 6 — Update sync-state.json

Read `~/.claude/skills/VERSION` first line → `local_version`.

Update `~/.claude/skills/sync-state.json`:
- `last_export` → today's date
- `local_version` → value from VERSION file
- `exported_counts.skill_changes` → N
- `exported_counts.pattern_entries` → K (0 if opt-in declined)
(keep all other fields unchanged)

Final message:
```
✓ PR создан: [URL]
✓ sync-state.json обновлён (last_export: YYYY-MM-DD)

Куратор получит уведомление о новом PR.
```

---

## sync-state.json template

```json
{
  "base_repo": null,
  "last_export": null,
  "last_sync": null,
  "local_version": null,
  "latest_version": null,
  "exported_counts": {
    "skill_changes": 0,
    "pattern_entries": 0
  }
}
```
