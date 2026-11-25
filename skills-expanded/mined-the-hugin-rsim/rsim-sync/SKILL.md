# Skill: rsim-sync

**Purpose:** Pull RSIm skill updates from GitHub releases and apply locally — with security scan and per-change approval. Preserves local memory/.
**When:** Periodically to receive improvements. Reminded at session start if > 14 days since last sync.
**Requirements:** `gh` CLI installed and authorized, `git` installed.

---

## PROCESS

### Step 1 — Check state

1. Read `~/.claude/skills/sync-state.json`:
   - If not found — create from template (see rsim-export), notify user, continue
   - Extract `base_repo`, `last_sync`, `local_version`

2. If `base_repo` empty:
   ```
   Укажи URL базового репо (например: https://github.com/username/rsim):
   ```
   Wait for answer, save to `sync-state.json`.

3. Check `gh` CLI:
   ```bash
   gh --version
   ```
   If not found — show install instructions, stop.

4. Report:
   ```
   Последний sync: [last_sync или "никогда"]
   Локальная версия: [local_version или "неизвестна"]
   Проверяю последний релиз в [base_repo]...
   ```

---

### Step 2 — Online version check

```bash
BASE_REPO="[base_repo from sync-state.json]"
LATEST=$(gh release view --repo "$BASE_REPO" --json tagName --jq '.tagName')
LOCAL=$(cat "$HOME/.claude/skills/VERSION" 2>/dev/null | head -1 || echo "none")
```

Report:
```
Последний релиз: [LATEST]
Локальная версия: [LOCAL]
```

If `LATEST` == `LOCAL`:
```
Версия актуальна. Проверяю новые contribution PRs...
```
Skip Step 2.5 download — go to Step 2.6 (check merged PRs only).

If `LATEST` != `LOCAL` → proceed to Step 2.5.

---

### Step 2.5 — Download release assets

```bash
CACHE_DIR="$HOME/.claude/.rsim-base-cache"
mkdir -p "$CACHE_DIR"

gh release download --repo "$BASE_REPO" --dir "$CACHE_DIR" \
  --pattern "rsim-*.tar.gz" --clobber
tar -xzf "$CACHE_DIR"/rsim-*.tar.gz -C "$CACHE_DIR/extracted" --strip-components=1
```

Downloaded: `skills/` `commands/` `CLAUDE.md` `memory/semantic/patterns.md`

---

### Step 2.6 — Merged contribution PRs (if version same)

```bash
gh pr list --repo "$BASE_REPO" --state merged \
  --search "RSIm Contribution" \
  --json number,title,mergedAt \
  --jq '.[] | select(.mergedAt > "[last_sync]")'
```

If no new merged PRs:
```
Нет новых обновлений с [last_sync].
```
Go to Step 6.

---

### Step 3 — Security scan (REQUIRED before showing diffs)

Read `~/.claude/skills/rsim-security-scan/patterns.md` and apply all patterns
to every file from downloaded release that differs from local version.

**Scan targets:**
- All `SKILL.md` files that changed
- `CLAUDE.md` if changed
- New entries in `memory/semantic/patterns.md`

**Result per file:**
- Clean → enters diff queue
- Suspicious → BLOCKED:

```
⛔ SECURITY SCAN: подозрительный контент

Файл:      [filename]
Категория: [category]
Паттерн:   [pattern]
Строка:    "[quote]"

Этот файл пропущен. Проверь PR вручную: [base_repo]/pulls
```

After scan:
```
Security scan завершён:
  Чистых файлов: N (войдут в очередь)
  Заблокировано: M (пропущены)
```

---

### Step 4 — Show diffs and approve (SKILL.md + commands)

For each clean changed file — one at a time:

```
── Обновление N/Total: [type] ──────────────────
[type: "Новый скилл" / "Обновление скилла" / "Команда"]

ДОБАВЛЯЕТСЯ / ИЗМЕНЯЕТСЯ:
[content or diff]

Источник: [base_repo] (прошло куратора)
Применить? (да / нет / пропустить все оставшиеся)
```

Responses:
- `да` → apply
- `нет` / `пропусти` → skip, next
- `пропустить все` → finish with current results

---

### Step 4.5 — Semantic patterns opt-in

After all SKILL.md diffs — if new entries found in community `memory/semantic/patterns.md`:

```
── Community Semantic Patterns ─────────────────
Найдено N новых паттернов:
  - [Pattern title 1] (tags: ...)
  - [Pattern title 2] (tags: ...)

Добавить в local semantic/patterns.md? (да / нет / выбрать)
```

- `да` → append all new entries to `~/.claude/memory/semantic/patterns.md`
- `нет` → skip
- `выбрать` → show each pattern with full content, approve/skip individually

---

### Step 5 — Apply confirmed changes

**SKILL.md updates:**
- Copy file from cache to `~/.claude/skills/[name]/SKILL.md`

**New skills:**
- Copy entire directory to `~/.claude/skills/[name]/`
- Add row to `~/.claude/skills/index.md`:
  ```
  | `[name]` | [from SKILL.md description] | [tags] | 0 | ✅ Ready |
  ```
- Report: `✓ Новый скилл [name] установлен`

**Command updates:**
- Copy file to `~/.claude/commands/[name].md`
- Report: `✓ Команда [name] обновлена`

**Semantic patterns (if approved):**
- Append new entries to `~/.claude/memory/semantic/patterns.md`
- Report: `✓ Добавлено N паттернов в semantic/patterns.md`

---

### Step 6 — Update sync-state.json

Update `~/.claude/skills/sync-state.json`:
- `last_sync` → today's date
- `local_version` → LATEST (from Step 2)
- `latest_version` → LATEST
(keep all other fields unchanged)

Final report:
```
── Итог rsim-sync ──────────────────────────────

Версия:         [LOCAL] → [LATEST]
Применено:      N изменений
Пропущено:      M (вручную / заблокировано security scan)
Новые скиллы:   [list or —]
Паттерны:       K добавлено [or —]

✓ sync-state.json обновлён (last_sync: YYYY-MM-DD, local_version: LATEST)

Следующий sync рекомендован через 14 дней.
```
