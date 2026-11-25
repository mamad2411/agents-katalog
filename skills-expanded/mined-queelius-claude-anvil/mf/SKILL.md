---
name: mf
description: Use mf (metafunctor) to manage papers, projects, series, packages, publications, and posts for the metafunctor.com Hugo site, plus site health checks. For cross-posting, use the crier plugin. Invoke from ANY repo; mf works globally.
argument-hint: "[intent, e.g. 'new post about X', 'sync papers', 'health check']"
---

# mf: Metafunctor Site Management

Interpret the user's intent, then run the right `mf` CLI workflow. mf does the mechanics (database CRUD, Hugo content generation, front matter edits); you do the judgment (choosing and sequencing commands, writing content).

## Preflight

1. **Right binary.** TeX Live ships a `/usr/bin/mf` (Metafont) that shadows the metafunctor CLI when the latter is not earlier on PATH. Before the first `mf` command in a session, run `mf --version` and expect `mf, version ...`. Anything else (a `This is METAFONT` banner, or a prompt waiting for input) means the CLI is not on PATH: stop and tell the user to install it with `uv tool install -e ~/github/repos/mf` (which puts it in `~/.local/bin`), rather than running commands against the wrong program.
2. **Site facts.** Resolve the site root: `mf config path` prints `<site root>/.mf/config.yaml` (it honors `MF_SITE_ROOT` and the global config). Then Read `<site root>/CLAUDE.md` before writing or editing content. It is the single source of truth for taxonomies and their front-matter keys, front matter fields, bundle types, build and deploy, and site gotchas. Do not rely on memory for these. `ls <site root>/content/` is the authoritative section list; read a section's `_index.md` before adding to it.

Field lists for the databases come from the CLI itself: `mf papers fields`, `mf projects fields`, `mf series fields`, `mf packages fields`.

## Content Source Model

| Content | Ground truth | mf role | Database |
|---------|-------------|---------|----------|
| Projects | GitHub repos | import/sync + overrides + generate | `projects_db.json` |
| Papers | Built paper repos (LaTeX) | ingest + set + generate | `paper_db.json` |
| Series | External source repos (`source_dir`) | sync (pull by default) + landing pages | `series_db.json` |
| Publications | Venue lifecycle (submissions, acceptances, DOIs) | add/update/log/pull + generate | `pubs_db.json` (independent of `paper_db`) |
| Packages | PyPI/CRAN registries | add/sync + generate | `packages_db.json` |
| Posts | The `.md` file | `mf posts` front matter edits | none |
| Writing, essays, other sections | The `.md` file | none | none |

**Key principle:** databases exist only for content whose ground truth lives elsewhere.

## Intent Mapping

| User says... | Workflow |
|-------------|----------|
| "new paper", "add a paper" | New Paper (below) |
| "new project", "add repo" | New Project (below) |
| "new post", "write about X", "synthesis post" | New Post (below) |
| "health check", "audit site" | Health Pass (below) |
| "deploy", "push to prod" | Pre-Deploy (below) |
| "feature X" | `mf {type} feature <slug>` (`--off` to unfeature) |
| "star this paper" | `mf papers set <slug> stars 5` |
| "tag X with Y" | `mf {type} tag <slug> --add Y` |
| "sync papers" | `mf papers status` (staleness), then `mf papers ingest <slug>` + `mf papers generate --slug <slug>` |
| "sync projects" | `mf projects sync` |
| "sync series" | `mf series sync <slug>` (or `--all`); `--dry-run` first |
| "cross-post", "share on socials" | Hand off to the crier plugin (`/crier`) |
| "what content do I have" | `mf analytics summary` |
| "find broken links" | `mf health links` |
| "clean up tags" | `mf taxonomy audit`, then `mf taxonomy normalize --from <old> --to <new> [--field tags\|categories] --dry-run`, then rerun without `--dry-run` |

### New Paper
1. Build the paper in its own repo first (`make html pdf` there); the slug must already exist in paper_db
2. `mf papers ingest <slug>` (pulls the built HTML/PDF into the site)
3. `mf papers set <slug> stars 5` (and any other metadata; `mf papers fields` lists them)
4. `mf papers generate --slug <slug>`
5. If peer-reviewed, register it in the independent publications registry: `mf pubs add <slug> --title "..." --type "journal article"` (both required; `mf pubs add --help` lists allowed types and statuses), or `mf pubs update <slug> --status ...` / `mf pubs log <slug> --event ...` for an existing entry, then `mf pubs generate --slug <slug>` (the registry does not render on its own)
6. Pre-Deploy (below)
7. Cross-post: hand off to `/crier`

Check staleness anytime with `mf papers status`; preview drift with `mf papers diff`.

### New Project
1. Add to `.mf/projects_db.json` (or `mf projects import --user <github-user>`)
2. `mf projects sync`
3. Pre-Deploy (below)

### New Post
1. `mf posts create --title "Title" -t tag -c Category [--series slug] [--description "..."]`; it prints the created path (a date-prefixed bundle) and sets `draft: true`
2. Write the content in that file, following the front matter conventions in the site CLAUDE.md
3. `mf posts set <slug> draft false` when ready (`<slug>` without the date prefix works)
4. Pre-Deploy (below)
5. Cross-post: hand off to `/crier`

### Health Pass
1. `mf health links`: broken internal links
2. `mf health descriptions`: posts missing `description`
3. `mf health images`: posts missing `featured_image`
4. `mf health stale`: project content whose description diverged from the DB
5. `mf integrity check`: database consistency
6. `mf content audit --extended`: linked_project references plus extended checks (`--list-checks` shows them)
7. `mf taxonomy audit`: near-duplicate terms

### Pre-Deploy
1. `mf status`: any render drift between DBs and generated pages?
2. `mf integrity check`: databases ok?
3. Verify the build without touching `docs/`: `hugo --gc --minify --destination /tmp/mf-check` (a bare `hugo` overwrites the committed `docs/`). The site CLAUDE.md lists the full validation suite.
4. `mf health links`: no broken links?
5. Deploy per the site CLAUDE.md (`make deploy` builds `docs/`; pushing master is the production deploy)

## Command Groups

Most database groups (papers, projects, series, packages) share a core of `list`, `show`, `set`, `unset`, `feature`, `tag`, `fields`, `stats`, `diff`. The table lists what each group adds or lacks; `mf <group> --help` is authoritative.

| Group | Distinctive verbs | Notes |
|-------|-------------------|-------|
| `papers` | ingest, generate, status, zenodo, fetch-cff, cff-status | Built paper repo → DB → Hugo |
| `projects` | import, sync, generate, refresh, hide, make-rich, list-rich, clean, fetch-codemeta, codemeta-status, rate-limit | GitHub → DB → Hugo |
| `series` | create, sync, scan, add, remove, delete, add-featured, add-link, add-related, artifacts, audit, audit-nav, classify-frontmatter | `sync` pulls by default (`--push` to push, `--ours`/`--theirs` for conflicts, `--interactive`); `diff` compares against the source repo |
| `packages` | add, remove, sync, generate | PyPI/CRAN → DB → Hugo |
| `posts` | create, list, set, unset, tag, feature | Direct front matter edits; no `show`, `fields`, `stats`, or `diff` |
| `pubs` | add, update, log, pull, check, generate, zenodo | Edits go through `update`/`log` (no `set`, `unset`, `feature`, `tag`, `fields`); `migrate` is a one-time paper_db seed |
| `content` | match-projects, about, list-projects, audit | Cross-content linking |
| `taxonomy` | audit, orphans, stats, normalize | Tag/category hygiene |
| `health` | links, descriptions, images, drafts, stale | Read-only content checks |
| `analytics` | summary, gaps, tags, timeline, suggestions, projects | Content insights |
| `integrity` | check, fix, orphans | Database consistency |
| `backup` | list, rollback, clean, status | Backup management |
| `config` | show, get, set, path, reset | Configuration |
| (top level) | `init`, `status` | `init` creates `.mf/`; `status` is the read-only render-drift dashboard |

### Generate vs Sync

- **generate** = rebuild Hugo pages from the database (read-only on the DB, idempotent)
- **sync** = pull from external sources into the database (mutates the DB)
- Always `sync` before `generate` if you want fresh data, and `generate` (or `sync`) before deploying
- Preview drift before acting: `mf status` (all modules, `-v` for pages) or `mf <group> diff` for one group
- Papers and publications are independent registries: a paper change does NOT update pubs (use `mf pubs update`/`log` when venue status changes)

### Dry runs and flags

- The global `mf -n`/`--dry-run` is honored only by `papers`, `projects`, `packages`, `pubs`, `series`, and `content`. **`posts` ignores it and writes anyway**: `mf -n posts set ...` edits the file. Preview a post edit by reading the front matter instead.
- Own `--dry-run` flags: `taxonomy normalize`, `series sync`, `integrity fix`, `backup clean`, `backup rollback`, `content audit` (`-n`).
- `--regenerate` (rebuild Hugo pages after the edit) exists on `set`, `feature`, and `tag` for `papers` and `projects` only.
- `--json` output is available on `posts list`, the `health` checks, `integrity check`, `analytics summary`, and `content audit`.

## Site Root Resolution

The CLI resolves the site root in this order, which is why it works from any directory:
1. `MF_SITE_ROOT` environment variable
2. Walk up from cwd looking for a `.mf/` directory
3. Global config at `~/.config/mf/config.yaml` (a `site_root: ~/github/repos/metafunctor` line; edit the file directly, since `mf config set` does not manage `site_root`)

## Hand-off to crier

Content flows **mf (create/update) → Hugo (render) → crier (distribute)**. After content changes are deployed, suggest cross-posting and hand off to the crier plugin (`/crier`); it owns the publishing workflow, rewrites, and failure handling.
