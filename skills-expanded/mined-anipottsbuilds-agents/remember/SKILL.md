---
name: remember
description: capture decisions, lessons, reminders, and todos into the lore knowledge graph
tools: Bash, Read, AskUserQuestion
---
<!-- tested with: claude code v2.1.122 -->

When the user runs `/lore:remember`, your job is to persist what they want to keep into the `notes` table of `~/.claude/lore/lore.db`. This is the user-controlled layer of the knowledge graph -- the parts of memory that can't be inferred from JSONL alone.

## locate notes.py

The CLI is shipped with the plugin. Resolve it once and reuse the path.

`````bash
NOTES=""
for p in "${CLAUDE_PLUGIN_ROOT}/scripts/notes.py" \
         "$HOME/.claude/plugins/marketplaces/anipotts/claude-code-tips/plugins/lore/scripts/notes.py" \
         $(find "$HOME/.claude/plugins" -path "*/lore/scripts/notes.py" 2>/dev/null | head -1); do
  if [ -n "$p" ] && [ -f "$p" ]; then NOTES="$p"; break; fi
done
if [ -z "$NOTES" ]; then echo "could not find notes.py -- is the lore plugin installed?"; exit 1; fi
echo "using: $NOTES"
`````

If the resolution fails, tell the user and stop. Don't fall back to writing raw SQL -- the helper validates types and timestamps.

## intents

Map the user's request to one of these intents. If the input is ambiguous (e.g. they say "remember the auth work was hard"), default to `add` with `--type lesson`.

| user phrasing | intent | call |
|---|---|---|
| "remember <X>", "save <X>", "log decision <X>" | add | `notes.py add "<title>" [--body ...] [--type ...] [--tags ...] [--project ...] [--session ...] [--file ...]` |
| "show notes", "list lessons", "what did i remember" | list | `notes.py list [--type ...] [--project ...] [--tag ...] [--limit N]` |
| "find note about X", "search notes" | search | `notes.py search "X"` |
| "show note 5", "get note 5" | get | `notes.py get 5` |
| "edit note 5", "update note 5", "change tags on 5" | update | `notes.py update 5 [--title ...] [--body ...] [--type ...] [--tags ...]` |
| "delete note 5", "remove note 5" | delete | `notes.py delete 5 --yes` (only after confirming with the user) |

## type discipline

Pick the type that fits, don't make one up. Valid types: `note`, `decision`, `lesson`, `reminder`, `tag`, `todo`. Ask the user only if the type is genuinely ambiguous.

- `decision` -- "we chose X over Y because Z"
- `lesson` -- "next time, do/don't X" (a thing learned from outcomes)
- `reminder` -- "before doing X, check Y" (forward-looking checklist item)
- `todo` -- discrete unfinished task tied to current scope
- `tag` -- short label/tag with no body
- `note` -- default, freeform

## scoping

When adding, infer scope from context:
- if pwd is inside a project the user is actively working in, set `--project <name>`
- if you're inside a clearly relevant file, optionally set `--file <abs-path>`
- otherwise leave both blank (global note)

## body authoring

If the user gives a one-liner, treat it as the title and skip `--body`. If they give a paragraph, split: first sentence becomes title, rest becomes body. Do NOT pass huge amounts of text into `--title` -- it shows up in `list` output and clutters quickly.

When the body is multi-line, use a heredoc:

`````bash
BODY=$(cat <<'EOF'
choice: D1 over Supabase
why: bundle size, edge runtime, no cold start
tradeoff: less mature ecosystem
EOF
)
python3 "$NOTES" add "use D1 for brands_emails ingest" --body "$BODY" --type decision --tags d1,migration --project anipotts.com
`````

## confirming destructive actions

Never call `delete --yes` until the user has explicitly confirmed in this turn. The first invocation should be `delete <id>` (without `--yes`), which prints a confirmation prompt; if the user agrees, run it again with `--yes`.

## output

After a successful `add`, repeat the saved title and id back to the user in one short line. After `list` or `search`, the helper's output is already human-readable -- pass it through, don't restructure.
