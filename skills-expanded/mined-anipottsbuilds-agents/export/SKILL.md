---
name: export
description: export the lore knowledge graph or its slices to json, csv, or markdown
tools: Bash, Read, AskUserQuestion
---
<!-- tested with: claude code v2.1.122 -->

When the user runs `/lore:export`, write a portable snapshot of the lore data they care about. Default destination is the current working directory; respect any path the user gives.

## locate the database

`````bash
DB="$HOME/.claude/lore/lore.db"
[ -f "$DB" ] || DB="$HOME/.claude/mine.db"
if [ ! -f "$DB" ]; then echo "no lore.db -- run /lore once to seed it"; exit 0; fi
`````

## intents

| user phrasing | export | format |
|---|---|---|
| "export notes", "save my notes" | notes table | json (default) or markdown |
| "export sessions" | sessions table | json or csv |
| "export project X" | project slice (sessions + notes + file list) | json bundle |
| "export cooccurrences" | file_cooccurrences view | csv (large -- prefer csv) |
| "export everything", "full snapshot" | all tables | json bundle in a directory |

If the user doesn't specify a format, infer: bulk graph data → csv (smaller), structured/nested → json, anything they'll read by eye → markdown.

## destination

Default: `./lore-export-<YYYYMMDD>.<ext>` in cwd. If the user gives a path, use it. If a file already exists at the destination, ask before overwriting.

## queries

### notes (json)

`````bash
OUT="${1:-./lore-notes-$(date +%Y%m%d).json}"
sqlite3 -json "$DB" "SELECT * FROM notes ORDER BY created_at DESC;" > "$OUT"
echo "wrote $OUT ($(wc -l < "$OUT") lines)"
`````

### notes (markdown)

`````bash
OUT="${1:-./lore-notes-$(date +%Y%m%d).md}"
{
  echo "# lore notes export — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  sqlite3 "$DB" "SELECT id, note_type, title, project_name, tags, created_at, body FROM notes ORDER BY created_at DESC;" |
    awk -F'|' '{
      printf "## #%s [%s] %s\n", $1, $2, $3;
      if ($4 != "") printf "- project: %s\n", $4;
      if ($5 != "") printf "- tags: %s\n", $5;
      printf "- created: %s\n\n", $6;
      if ($7 != "") printf "%s\n\n", $7;
    }'
} > "$OUT"
echo "wrote $OUT"
`````

### sessions (csv)

`````bash
OUT="${1:-./lore-sessions-$(date +%Y%m%d).csv}"
sqlite3 -header -csv "$DB" "SELECT id, project_name, model, start_time, duration_active_seconds, total_input_tokens, total_output_tokens FROM sessions WHERE is_subagent = 0 ORDER BY start_time DESC;" > "$OUT"
echo "wrote $OUT"
`````

### project bundle (json)

`````bash
PROJECT="$1"
OUT="${2:-./lore-$PROJECT-$(date +%Y%m%d).json}"
python3 <<PY > "$OUT"
import json, sqlite3
db = sqlite3.connect("$DB")
db.row_factory = sqlite3.Row
project = "$PROJECT"
def rows(sql, *args):
    return [dict(r) for r in db.execute(sql, args).fetchall()]
bundle = {
  "project": project,
  "exported_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
  "sessions": rows("SELECT * FROM sessions WHERE project_name = ? AND is_subagent = 0 ORDER BY start_time DESC", project),
  "notes": rows("SELECT * FROM notes WHERE project_name = ? ORDER BY created_at DESC", project),
  "files": rows(
    "SELECT input_summary AS path, COUNT(DISTINCT session_id) AS sessions FROM tool_calls tc JOIN sessions s ON tc.session_id = s.id "
    "WHERE s.project_name = ? AND tc.tool_name IN ('Edit','Read','Write','MultiEdit') AND tc.input_summary IS NOT NULL "
    "GROUP BY input_summary ORDER BY sessions DESC", project),
}
print(json.dumps(bundle, indent=2, default=str))
PY
echo "wrote $OUT"
`````

### cooccurrences (csv)

`````bash
OUT="${1:-./lore-cooccurrences-$(date +%Y%m%d).csv}"
echo "this view recomputes -- the export may take ~5s on a populated db"
sqlite3 -header -csv "$DB" "SELECT * FROM file_cooccurrences ORDER BY session_count DESC;" > "$OUT"
echo "wrote $OUT ($(wc -l < "$OUT") rows)"
`````

### full snapshot (directory of json files)

`````bash
DIR="${1:-./lore-snapshot-$(date +%Y%m%d)}"
mkdir -p "$DIR"
for table in sessions messages tool_calls errors notes; do
  sqlite3 -json "$DB" "SELECT * FROM $table" > "$DIR/$table.json"
  echo "  $table.json: $(wc -c < "$DIR/$table.json") bytes"
done
sqlite3 -json "$DB" "SELECT * FROM file_cooccurrences" > "$DIR/file_cooccurrences.json"
echo "wrote $DIR/"
`````

A full snapshot can be large -- warn the user before writing if `messages` would exceed ~50MB (rough check: `sqlite3 ... "SELECT COUNT(*) FROM messages;"` -- bail if >100k unless they confirm).

## confirming destructive overwrites

If the destination file or directory already exists, list what would be overwritten and ask before clobbering. Never silently overwrite a non-empty export directory.

## output

After a successful write, print the path and size in one line. If the user asked for a format the schema can't satisfy (e.g. "export the graph as graphml"), explain what's available rather than inventing an exporter.
