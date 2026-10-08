@RTK.md

# Global CLAUDE.md

> Applies to ALL projects. Per-project CLAUDE.md files add project-specific rules.

## New Project Setup

Run `/init-project` from any project root. No arguments needed — fully automated.

What it auto-detects:
- **Project name** — from `package.json`, `Cargo.toml`, `go.mod`, or directory name
- **Stack** — from dependencies (React, Next.js, Vite, FastAPI, Django, Go, Rust, etc.)
- **Entry points** — from `package.json` scripts + common file patterns
- **Data layer** — from ORM/DB dependencies (Prisma, SQLAlchemy, Mongoose, pg, etc.)

What it does:
1. Registers the project in `~/.claude/file-map.db` (assigns `project_id`)
2. Generates `CLAUDE.md` with all detected info pre-filled

After running: fill in **Purpose** + add any project-specific Architecture Rules / Conventions.

Script: `~/.claude/scripts/init-project.sh`

---

## Project Overview Template

Document each project with:
- **Purpose**: one sentence on what the project does
- **Stack**: languages, frameworks, major libraries
- **Entry points**: where code starts (main file, routes, etc.)
- **Data layer**: how state/data is stored (DB, files, API, etc.)

Record this in the project's own CLAUDE.md. Do NOT put project details here.

## Architecture Rules

1. **Read before write** — query file map before opening any file
2. **Smallest change wins** — edit only files necessary, don't refactor adjacent code unless asked
3. **Types are contracts** — trace all call sites before changing a shared type
4. **No silent fallbacks** — don't add defaults that hide missing required config
5. **Imports must resolve** — verify the export exists before adding an import

## Conventions

- **Datetime format** — UTC+0: `YYYY/MM/DD HH:mm`
- **File keys** — short, snake_case, unique per project (e.g. `app`, `sdui_types`)
- **Descriptions** — one sentence, present tense, capital start, no trailing period
- **Exports column** — comma-separated names exported by the file
- **Path format** — relative to project root (e.g. `src/App.tsx`)

## File Map

Global database: `~/.claude/file-map.db`

### Session Start — Register Project

```bash
# Register/update project (UNIQUE path — safe to re-run)
sqlite3 ~/.claude/file-map.db "
INSERT INTO projects (path, session_id) VALUES ('<abs_path>', '<session_id>')
ON CONFLICT(path) DO UPDATE SET session_id = '<session_id>';"

# Get project_id (use in all queries below)
sqlite3 ~/.claude/file-map.db "SELECT id FROM projects WHERE path = '<abs_path>';"
```

### Search Files

```bash
sqlite3 ~/.claude/file-map.db \
  "SELECT key, path, description, exports FROM files
   WHERE project_id = <project_id>
   AND (description LIKE '%<keyword>%' OR path LIKE '%<keyword>%')"
```

### Check File History

```bash
sqlite3 ~/.claude/file-map.db \
  "SELECT datetime, changes FROM updates
   WHERE project_id = <project_id> AND file_key = '<key>'
   ORDER BY datetime DESC LIMIT 5"
```

### Register New File

```bash
sqlite3 ~/.claude/file-map.db \
  "INSERT INTO files (key, project_id, path, description, exports)
   VALUES ('<key>', <project_id>, '<rel_path>', '<description>', '<exports>')"
```

### Log a Change

```bash
sqlite3 ~/.claude/file-map.db \
  "INSERT INTO updates (project_id, file_key, datetime, changes)
   VALUES (<project_id>, '<key>', '<YYYY/MM/DD HH:mm>', '<what changed>')"
```

### Cross-Project Queries

```bash
# Find file across all projects
sqlite3 ~/.claude/file-map.db \
  "SELECT p.path as project, f.key, f.path FROM files f
   JOIN projects p ON f.project_id = p.id WHERE f.path LIKE '%<name>%'"

# List all projects
sqlite3 ~/.claude/file-map.db "SELECT id, path, session_id FROM projects;"
```

## Pre-Edit Protocol

1. Query file map by keyword — `exports` often enough to act without opening the file
2. Check recent history — understand what changed last
3. Only then open the file — never read speculatively

## Update Protocol

1. Log change: INSERT INTO updates (UTC+0 datetime)
2. If new file: INSERT INTO files first
3. If project conventions/architecture changed: update the project's CLAUDE.md
4. Never put project-specific content in this file
