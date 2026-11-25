---
name: plan-context
description: >
  Build the context catalog: scan the repo into platform.md, or ingest a
  company/project/plan source (repo, PDF, paste, website, transcript, MCP).
  Use when starting a plan, adding context, attaching a brand guide or call
  notes, before specifying, or when the user runs /ultimate-sdd:context.
license: MIT
metadata:
  author: andrewr303
  version: "2.1"
---

Context is two kinds (code / business) and three levels (company / project / plan).

**Supporting files:** `references/context.md`, `references/model.md`, `templates/platform-context-template.md`, `templates/context-source.md`, `templates/context-catalog.md`.

## Modes

Detect from the user:

| Signal | Mode |
|---|---|
| No args, or "scan" / "codebase" / a path in the repo | **Scan** → `platform.md` |
| Path, URL, paste, PDF, `.vtt`, "Confluence", "add context" | **Ingest** → CTX-n |
| "show context" / catalog | **List** CATALOG.md |

For Scan or Ingest, create missing `docs/plan/context/{company,project,plan}` and `CATALOG.md` without replacing existing files. List is read-only. Resolve paths in the target repo, not the plugin.

## Scan (code, project level)

1. Read applicable project instructions, README, the existing catalog, and `context/platform.md` before scanning or writing.
2. Bound the scan to root manifests and entry points relevant to the requested work. Reuse existing context; follow only enough source to establish the relevant runtime paths, modules, and documented commands. Skip secrets, generated output, dependencies, and unrelated subtrees.
3. Capture the map using `templates/platform-context-template.md`. For an existing map, make targeted updates after reading it; preserve human additions, constraints, and unresolved questions. Flag conflicting facts rather than silently erasing authored notes.
4. Mark facts `[verified]` with `path:line`, interpretations `[inferred]`, and unsupported choices as explicit unresolved gaps. Record what was examined and skipped. A command found in a manifest is declared, not evidence it passed.

- Env: key names only, from safe templates or documented usage; do not open secrets to extract them.
- Do-not-reinvent entries name real inspected modules; API rows use verified query/path params.
- Do not guess stack choices or executable commands, or force a style inventory beyond the work's needs.
- For greenfield, record `greenfield`, evidenced or user-selected choices, and undecided gaps. No codebase is not permission to invent a stack.

Register in CATALOG: `CTX` is not required for `platform.md` itself — the catalog row may be `PLATFORM | project | code | repo | Platform map | .`. Preserve existing rows and avoid duplicate PLATFORM entries.

For missing project scaffolding rather than a context refresh, use `plan-setup` and `references/recovery.md`.

## Ingest (one source)

1. Classify `level` (ask if unclear: company vs project vs this plan).
2. Classify `kind` (code vs business) and `type` (`references/context.md`).
3. Next `CTX-n` from disk.
4. Write `context/<level>/CTX-n-<slug>.md` — excerpt decisions, not the whole document.
5. Append a CATALOG row.
6. **Re-score:** any REQ whose gaps this source could close → re-open `req-specify` Refine for those gaps only, or note "CTX-n may close gap X on REQ-m".

Fetching:

- Local file / paste: read it
- Website: fetch the URL
- MCP (Confluence, Notion, Linear doc): use the connected MCP; if missing, ask for an export
- Transcript: keep quotes that are decisions; drop small talk

Never copy secrets.

## List

Print CATALOG grouped by Company / Project / Plan (Plansmith sidebar). Offer "Add context". If absent, report it without creating artifacts.

## Afterward

After Scan/Ingest writes, update INDEX's context-source count and use graph-derived Next, not an assumed Frame/Specify action:

```
python <plugin>/scripts/plan.py next --root docs/plan --json
python <plugin>/scripts/plan.py validate --root docs/plan
```

Run from the target repo with its resolved plan root. Surface validation errors and unresolved gaps; do not claim a complete platform map beyond the inspected scope.

Offer the next supported planning action using this catalog.

## Guardrails

- Do not write a PRD (`prd-from-code`).
- Do not merge two sources into one CTX or overwrite an existing source to reuse its ID.
- Repo observation is read-only; only scoped planning context/catalog/INDEX artifacts are written. No application code, project configuration/workflow, dependency installs, command execution discovered from the scan, or git changes.
