---
name: wiki-health-check
description: Use when you want to audit a project wiki for quality issues — stale version claims, contradictions between pages, orphan pages, broken wiki links, missing cross-references, or misalignment between wiki content and the actual codebase state.
argument-hint: "[--fix] [--versions-only] [--deep]"
---

<objective>
Perform a systematic health check of the project wiki: detect stale data, internal contradictions, structural issues, and drift between wiki content and the real codebase. Use project instructions from supported agents, exclude third-party generated guidance, and produce a prioritized, actionable report.
</objective>

<quick_start>
**Full health check:**
```
/wiki-health-check
```

**Only check version claims:**
```
/wiki-health-check --versions-only
```

**Deep check (includes code/wiki alignment scan):**
```
/wiki-health-check --deep
```

**Fix minor issues automatically (broken links, formatting):**
```
/wiki-health-check --fix
```
</quick_start>

<methodology>

## Step 1 — Locate the Wiki

Read project-level agent instructions for wiki location hints and project-specific rules:
- `CLAUDE.md` for Claude Code projects
- `AGENTS.md` for Codex/OpenAI agent projects
- `AGENT.md` as a legacy or singular fallback if present

When several files exist, read all of them and merge only user-maintained project instructions. If the files conflict, prefer the most specific project-local instruction and call out the ambiguity in the report.

Common patterns to check:
- `wiki/` symlink → resolve its real path
- `docs/`
- `obsidian_projects/<project>/`
- Reference in `CLAUDE.md`, `AGENTS.md`, or `AGENT.md` like `wiki/ est un symlink relatif vers ...`

Ignore generated blocks or sections inserted by third-party tools in agent instruction files. Do not treat those sections as wiki requirements and do not add them to the wiki.

Examples of content to ignore:
- Laravel Boost generated guidance or injected tool instructions
- Framework/tool boilerplate marked as generated, managed, auto-generated, or do-not-edit
- Vendor, plugin, or package instructions that describe the tool itself rather than the user's project

Read `wiki/index.md` (or equivalent entry point) to build the page inventory.

## Step 2 — Build the Page Index

For every `.md` file in the wiki:
- Record its path and title (first `# heading`)
- Extract all `[[WikiLink]]` references it makes
- Extract all `[text](path)` markdown links
- Note what external URLs it references

## Step 3 — Run Health Checks

Run ALL checks unless flags restrict the scope.

### 3a. Version Staleness `[VERSIONS]`

Read actual version sources from the codebase:
- `package.json` → npm packages and their versions
- `composer.json` → PHP packages and versions
- `pyproject.toml` / `requirements.txt` → Python deps
- `Dockerfile` / `.env.example` → runtime versions

For each version claim found in the wiki, compare with real values.

Flag: `[STALE]` if wiki version ≠ installed version.

### 3b. Orphan Pages `[STRUCTURE]`

An orphan is a wiki page that no other page links to.

Build the inbound-link map (which pages link to each page). Flag any page with 0 inbound links and that isn't the index/root.

### 3c. Broken WikiLinks `[STRUCTURE]`

For every `[[WikiLink]]` found, check the referenced file exists in the wiki.

Flag: `[BROKEN]` if target page does not exist.

### 3d. Internal Contradictions `[COHERENCE]`

Look for the same fact stated with different values across pages:
- Package versions (`laravel/framework v11` on one page, `v12` on another)
- Database table names or column types
- Architectural decisions (e.g., "we use Redis" vs "we use database queue")
- URLs, ports, env variable names

Strategy: extract all factual claims about versioned or enumerable things, group by topic, flag conflicts.

### 3e. Dead File References `[COHERENCE]`

Find references to specific file paths (e.g., `app/Models/User.php`, `resources/js/Pages/Auth/Login.vue`) in the wiki.

Check each referenced path exists in the codebase. Flag: `[DEAD REF]` if file is missing.

### 3f. Missing Important Pages `[GAPS]` *(--deep only)*

Look for user-maintained project concepts mentioned frequently in wiki pages, agent instruction files, or README that have no dedicated page.

Agent instruction files include `CLAUDE.md`, `AGENTS.md`, and `AGENT.md`. Exclude third-party generated blocks before extracting concepts.

Also: check codebase for major modules/features (top-level `app/` subdirectories, major Vue pages) not covered by any wiki page.

### 3g. Missing Cross-References `[GAPS]`

When a page mentions a concept that has its own page, check if it links to it. Flag missing links when the gap would confuse a reader navigating the wiki.

### 3h. Code/Wiki Alignment `[COHERENCE]` *(--deep only)*

Spot-check architectural claims:

| Wiki claim type | How to verify |
|---|---|
| "Domain layer has zero Illuminate imports" | `grep -r "use Illuminate" app/Domain/` |
| Tech stack / package names | Compare with composer.json / package.json |
| Database schema (table names, columns) | Run `database-schema` tool if available |
| Artisan commands mentioned | `vendor/bin/sail artisan list` |

## Step 4 — Generate Report

Structure the report by severity:

```
## Wiki Health Report — <project> — <date>

### 🔴 Critical (must fix)
- [BROKEN] [[features/auth]] links to [[features/login]] which doesn't exist
- [STALE] wiki/technical/stack.md claims laravel/framework v11, composer.json has v12

### 🟡 Important (should fix)
- [DEAD REF] wiki/design/architecture.md references app/Http/Kernel.php (removed in Laravel 11)
- [CONTRADICTION] Two pages disagree on queue driver: "Redis" vs "database"

### 🔵 Suggestions (nice to have)
- [ORPHAN] wiki/queries/2024-auth-analysis.md has no inbound links
- [GAP] LangGraph pipeline mentioned 4× but has no dedicated wiki page
- [MISSING LINK] wiki/technical/database.md mentions learner_stats view but doesn't link to wiki/features/learner-profile.md

### ✅ Summary
X critical · Y important · Z suggestions
Wiki last updated: <git log date on wiki files>
```

## Step 5 — Fix Mode (`--fix`)

If `--fix` is passed, auto-apply safe fixes only:
- Add missing cross-reference links
- Fix broken `[[WikiLink]]` casing/path issues if target exists under a different path
- Update version numbers that are clearly stale (with git diff shown before applying)

Never auto-fix contradictions or delete pages — report them for human review.

</methodology>

<flags>
| Flag | Behavior |
|---|---|
| *(none)* | Runs checks 3a–3c + 3d + 3g |
| `--versions-only` | Only 3a (version staleness) |
| `--deep` | All checks including 3f and 3h |
| `--fix` | After report, apply safe auto-fixes |
</flags>

<important>
- Always read available project agent instruction files (`CLAUDE.md`, `AGENTS.md`, `AGENT.md`) to find the wiki location — never hardcode paths.
- Treat third-party generated content in agent instruction files as non-authoritative. Ignore it for wiki gap analysis and never copy it into the wiki.
- If the wiki is a symlink, resolve the real path before reading files.
- Use the `database-schema` and `tinker` Boost MCP tools (if available) to verify database claims.
- Report only genuine issues — avoid false positives from conditional/future content.
- When in doubt about a contradiction, quote both sources verbatim in the report.
</important>
