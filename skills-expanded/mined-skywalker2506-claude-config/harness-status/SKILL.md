---
name: harness-status
description: "On-demand harness status — MCP active servers, project index, graph cache freshness, session sync health. Use when user wants to see reference info previously auto-injected each session. Triggers: harness status, harness-status, mcp active, mcp listesi, graph cache, project info, session info."
---

## /harness-status

Reference info that used to bloat every SessionStart. Now on-demand only.

## What to report

Run these checks in parallel with Bash and render a compact summary.

### 1. MCP active servers
```bash
jq -r '.mcpServers | keys | join(", ")' ~/.claude/settings.json 2>/dev/null
```
Label: `🔌 MCP_ACTIVE: ...`

### 2. Project index (context-aware)
```bash
bash ~/Projects/claude-config/projects/scripts/project_index.sh 2>/dev/null || echo "PROJECT_INDEX: (no .claude/index.md in tree)"
```

### 3. Graph cache freshness (if present)
Check common cache paths; warn only if > 7 days old:
```bash
for f in ~/.claude/graph-cache.json ~/Projects/claude-config/cache/graph.json ~/.claude/cache/graph.json; do
  [ -f "$f" ] || continue
  age_days=$(( ( $(date +%s) - $(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f") ) / 86400 ))
  if [ "$age_days" -gt 7 ]; then
    echo "⚠️ GRAPH_CACHE: $f is $age_days days old — refresh recommended"
  else
    echo "✅ GRAPH_CACHE: $f ($age_days d old)"
  fi
done
```

### 4. Available secret keys (names only, never values)
```bash
SFILE="$HOME/.claude/secrets/secrets.env"
[ -f "$SFILE" ] && grep -v '^#' "$SFILE" | grep '=' | cut -d= -f1 | paste -sd ',' -
```
Label: `🔑 AVAILABLE_SECRETS: ...`

### 5. Session sync status
```bash
ls -la ~/Projects/claude-config/config/session_sync_claude_config.sh >/dev/null 2>&1 && echo "✅ SESSION_SYNC script present" || echo "⚠️ SESSION_SYNC script missing"
```

## Output format

```
=== Harness Status ===
🔌 MCP_ACTIVE: atlassian, codex, context7, ...
📁 PROJECT_INDEX: <terse signal or none>
📊 GRAPH_CACHE: <status or absent>
🔑 AVAILABLE_SECRETS: <comma list>
🔄 SESSION_SYNC: ok
```

Keep output under 15 lines. Do not echo secret values — only key names.
