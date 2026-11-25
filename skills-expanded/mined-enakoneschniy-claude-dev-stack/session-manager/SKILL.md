---
name: session-manager
description: >
  Fallback for manual session logging when auto-capture is disabled or fails, plus
  explicit resume/handoff/status requests. Auto-capture via
  hooks/session-end-capture.mjs is the primary Stop-time path — this skill is a
  safety net. Triggers on end-of-session signals ("done", "end", "всё", "хватит",
  "finish", "конец") and resume-intent requests ("resume", "продолжи",
  "что делали", "handoff", "what did we do").
---

# Session Manager Skill

> Context is loaded at SessionStart by `hooks/session-start-context.sh`.
> This skill only handles end-of-session logging (`/end`) and explicit resume requests (`/resume`).

Manage development session lifecycle for multi-project work. Eliminates Claude Code "amnesia" by maintaining session logs and project context in an Obsidian vault.

## Vault Location
Default: `~/vault/`
Override with env var: `VAULT_PATH`

## Commands

### /resume
Explicit re-load of project context. The SessionStart hook (`hooks/session-start-context.sh`)
already loads context at session start — use this command only to force a re-read
mid-session (e.g., after manually editing `context.md` or after switching projects).

```bash
VAULT="${VAULT_PATH:-$HOME/vault}"
PROJECT_NAME=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
PROJECT_DIR="$VAULT/projects/$PROJECT_NAME"
CURRENT_DIR=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

# SSR-01: if the SessionStart hook already loaded context <60 min ago,
# skip redundant cat — context is already in the model's prompt.
MARKER="$CURRENT_DIR/.claude/.session-loaded"
if [ -f "$MARKER" ]; then
  NOW=$(date +%s)
  MTIME=$(stat -f %m "$MARKER" 2>/dev/null || stat -c %Y "$MARKER" 2>/dev/null || echo 0)
  AGE=$(( NOW - MTIME ))
  if [ "$AGE" -lt 3600 ] && [ "$AGE" -ge 0 ]; then
    echo "📋 Context pre-loaded at $(cat "$MARKER" 2>/dev/null) by SessionStart hook — skipping redundant cat."
    return 0 2>/dev/null || exit 0
  fi
fi

cat "$PROJECT_DIR/context.md" 2>/dev/null || echo "No context.md found for $PROJECT_NAME"

# Last 3 session logs
for f in $(ls -t "$PROJECT_DIR/sessions/"*.md 2>/dev/null | head -3); do
  echo "=== $(basename "$f") ==="
  cat "$f"
  echo ""
done
```

### /end or /done
Create session log and update context.

```bash
PROJECT_NAME=$(basename $(git rev-parse --show-toplevel 2>/dev/null || pwd))
VAULT=${VAULT_PATH:-~/vault}
PROJECT_DIR="$VAULT/projects/$PROJECT_NAME"
SESSION_FILE="$PROJECT_DIR/sessions/$(date +%Y-%m-%d)-SESSION_SLUG.md"

# Create session log
cat > "$SESSION_FILE" << 'EOF'
# Session: DATE — DESCRIPTION

## Что сделано
- (list concrete changes: files modified, features added, bugs fixed)

## Решения
- (architectural decisions made, if any)

## TODO на следующую сессию
- [ ] (specific actionable items)

## Проблемы
- (bugs encountered, workarounds used, tech debt noted)

## Изменённые файлы
- (list key files that were modified)

## Зависимости
- (new packages added, version changes)
EOF

# Update context.md "Session History" section (D-01, D-02)
# Invokes the same Node wrapper the Stop hook uses — idempotent by filename.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" && pwd)"
UPDATER="$REPO_ROOT/hooks/update-context.mjs"
if [ -f "$UPDATER" ]; then
  VAULT_PATH="$VAULT" CDS_PROJECT_NAME="$PROJECT_NAME" \
    node "$UPDATER" "$(basename "$SESSION_FILE")" 2>/dev/null || true
fi

# ── Auto-ADR Capture (Phase 26, ADR-02) ────────────────────────
# Scans the session transcript and writes architectural decisions to vault.
# Fail-open: never blocks /end if the bridge errors.
ADR_BRIDGE="$REPO_ROOT/lib/adr-bridge-session.mjs"
if [ -f "$ADR_BRIDGE" ]; then
  # SESSION_ID may be substituted by Claude from its runtime context.
  # If unset, the bridge falls back to most-recent-mtime JSONL detection.
  ADR_RESULT=$(VAULT_PATH="$VAULT" CDS_PROJECT_NAME="$PROJECT_NAME" \
    node "$ADR_BRIDGE" \
    --session-log "$(basename "$SESSION_FILE")" \
    --cwd "$REPO_ROOT" \
    ${SESSION_ID:+--session-id "$SESSION_ID"} \
    2>/dev/null) || ADR_RESULT='{"newAdrs":[],"superseded":[],"error":"bridge failed"}'
  # ADR_RESULT is valid JSON: {"newAdrs":[...],"superseded":[...],"error":null|string}
  # Claude reads this variable and formats a one-line summary for the user.
  echo "$ADR_RESULT"
fi
# ────────────────────────────────────────────────────────────
```

Replace SESSION_SLUG with a kebab-case summary (e.g., "fix-auth-flow", "add-telegram-pipeline").
Replace placeholders with actual session data.

After session log and context.md are updated, auto-ADR capture runs (Phase 26 — D-04).

### /handoff
Generate a comprehensive handoff document for continuing work in a new session or by another developer.

```bash
PROJECT_NAME=$(basename $(git rev-parse --show-toplevel 2>/dev/null || pwd))
VAULT=${VAULT_PATH:-~/vault}

# Generate handoff
echo "# Handoff: $PROJECT_NAME — $(date +%Y-%m-%d)"
echo ""
echo "## Current State"
cat "$VAULT/projects/$PROJECT_NAME/context.md"
echo ""
echo "## Recent Changes (git)"
git log --oneline -10 2>/dev/null
echo ""
echo "## Uncommitted Changes"
git diff --stat 2>/dev/null
echo ""
echo "## Active TODO"
grep -r "TODO" "$VAULT/projects/$PROJECT_NAME/sessions/" 2>/dev/null | tail -20
```

### /status
Quick overview of all projects.

```bash
VAULT=${VAULT_PATH:-~/vault}
echo "# Project Status Overview"
echo ""
for dir in "$VAULT/projects"/*/; do
  [ "$(basename $dir)" = "_template" ] && continue
  project=$(basename "$dir")
  last_session=$(ls -t "$dir/sessions/"*.md 2>/dev/null | head -1)
  if [ -n "$last_session" ]; then
    last_date=$(basename "$last_session" | cut -d'-' -f1-3)
    echo "## $project (last: $last_date)"
    grep "^- \[ \]" "$last_session" 2>/dev/null | head -5
  else
    echo "## $project (no sessions yet)"
  fi
  echo ""
done
```

## Auto-ADR Capture (Phase 26 — D-04, D-05)

After the `/end` bash block runs, `$ADR_RESULT` contains a JSON summary of ADRs created or superseded during the session. Claude reads this and reports a one-line summary to the user:

- If `newAdrs` or `superseded` is non-empty: `Session logged. {N} new ADRs (#NNNN topic, ...). {M} superseded (#NNNN topic, ...).`
- If both empty: `Session logged.` (stay silent about ADRs)
- If `error` is non-null: `Session logged. (ADR capture unavailable: {reason})`

Never block /end on ADR capture. If the bridge errors, complete the flow silently.

The bridge is `lib/adr-bridge-session.mjs` in the project repo. It uses Claude Haiku 4.5 via `claude -p` subprocess to extract decisions from the session transcript and writes them to `vault/projects/{project}/decisions/` following the template in D-10.


## ADR Creation

When an architectural decision is made during the session:

```bash
VAULT=${VAULT_PATH:-~/vault}
PROJECT_NAME=$(basename $(git rev-parse --show-toplevel 2>/dev/null || pwd))
ADR_DIR="$VAULT/projects/$PROJECT_NAME/decisions"
NEXT_NUM=$(printf "%04d" $(($(ls "$ADR_DIR"/*.md 2>/dev/null | wc -l) + 1)))

cat > "$ADR_DIR/${NEXT_NUM}-DECISION_SLUG.md" << 'EOF'
# ADR-NNNN: Title

**Дата**: YYYY-MM-DD
**Статус**: accepted

## Контекст
Why the question arose

## Решение
What we chose

## Альтернативы
What we considered and why we rejected it

## Последствия
What this changes in the project
EOF
```

## Best Practices
1. Context loads automatically at SessionStart — use /resume only to force a re-read mid-session
2. Always use /end at session end — future you will thank you
3. ADRs are cheap to write and expensive to not have
4. Session logs should be specific: file names, function names, not vague descriptions
5. TODOs should be actionable: "implement X in file Y" not "finish feature"
