# AGENTS.md — src/providers/fetch/github/

## Purpose
LLM-optimized GitHub fetcher. Domain breaker for `github.com` / `gist.github.com` / `raw.githubusercontent.com`. Dispatches to resource-specific handlers based on URL shape (file, directory, repo overview, issue, PR, gist, release, commit, wiki, actions, user profile). The largest provider folder by far — 11 files.

## Files

- **`index.ts`** — `GitHubFetchProvider` class. Parses URL via `url-parser.ts`, switches on `resource_type` to call the matching handler.
- **`url-parser.ts`** — `parse_github_url(url)` returns `{ resource_type, owner, repo?, ref?, path?, resource_id? }`. Recognizes 8+ URL shapes: user/org profiles, repo overview, file (`/blob/<ref>/<path>`), raw file (`/raw/<ref>/<path>`), directory (`/tree/<ref>/<path>`), issues (`/issues`, `/issues/<n>`), PRs (`/pull/<n>`, `/pulls`, `/pull/<n>/files`), gists (`gist.github.com/<user>/<id>`), raw URLs (`raw.githubusercontent.com/...`), releases (`/releases`, `/releases/tag/<tag>`, `/releases/latest`), commits (`/commits`, `/commits/<ref>`, `/commit/<sha>`), wiki, actions.
- **`api.ts`** — HTTP wrappers for REST + GraphQL. `github_get`, `github_get_raw`, `github_get_safe` (REST) — `_safe` returns `undefined` on 404 instead of throwing, used for optional enrichment. `github_graphql` for GraphQL queries. Manages `Authorization: Bearer <token>` + `X-GitHub-Api-Version: 2022-11-28`.
- **`types.ts`** — `ParsedGitHubUrl`, `RepoOverviewData`, generic `GitHubAny`.
- **`handlers.ts`** — Resource handlers (~13 of them): `fetch_issue`, `fetch_issue_list`, `fetch_pr_list`, `fetch_pull_request`, `fetch_release_list`, `fetch_release`, `fetch_release_latest`, `fetch_commit_list`, `fetch_commit`, `fetch_user_profile`, `fetch_gist`, `fetch_actions`, plus re-exports of file/directory handlers.
- **`handlers-file.ts`** — `fetch_file`, `fetch_directory`, `fetch_wiki_page`. Resolves ambiguous ref/path by trying GitHub Contents API splits.
- **`repo-overview.ts`** — Dedicated handler for repo overview (root URL `github.com/owner/repo`). GraphQL primary path with REST fallback. Pulls README, language breakdown, AI context files, tree structure, recent commits, activity, open issues/PRs/releases.
- **`markdown-builder.ts`** — Repo-overview markdown renderer: identity table, stats, languages, depth-2 tree, docs listing, AI context files, activity, issues/PRs/releases.
- **`formatters.ts`** — Pure formatters: `format_date`, `format_size`, `format_language_breakdown`, `escape_table_cell`, `snippet_two_sentences`, `format_docs_listing`, `format_ai_rules_listing`, `format_depth2_tree`.
- **`constants.ts`** — Pagination + truncation: `LIST_PER_PAGE=100`, `COMMENTS_PER_PAGE=50`, `PATCH_MAX_CHARS`, `RELEASE_BODY_MAX_CHARS`, `CONTEXT_FILE_LIMITS`, binary extensions, AI-rules directory list.
- **`graphql.ts`** — GraphQL query strings + tree merge/filter helpers used by `repo-overview.ts`.

## Vendor

- **Vendor**: GitHub
- **Endpoints**: `https://api.github.com` (REST) and `https://api.github.com/graphql` (GraphQL)
- **Auth**: `Authorization: Bearer <GITHUB_API_KEY>` + `X-GitHub-Api-Version: 2022-11-28`
- **Env var**: `GITHUB_API_KEY`
- **Returns**: per-resource markdown documents — issues with metadata + body + comments, PRs with patch diffs, commits with stats + diffs, releases with asset tables, repo overviews with README + tree + activity, etc.

## Conventions / Invariants

- **API-native** — included in `API_NATIVE_PROVIDERS = ['github', 'supadata']`. The fetch orchestrator's 200-char minimum AND challenge-pattern check are both bypassed (gists can be 50 chars; docs can mention "access denied" legitimately).
- **Domain-breaker only** — runs before the general waterfall for the three github hostnames.
- **All resource handlers return markdown** as `FetchResult.content`.
- **GraphQL fallback**: `repo-overview.ts` tries GraphQL first (richer data in one call). On failure, falls back to REST. Don't lose the fallback path.
- **Truncation discipline**: `PATCH_MAX_CHARS` and `RELEASE_BODY_MAX_CHARS` cap the size of patches and release bodies before they're embedded in the markdown — prevents enormous diffs from blowing the LLM context.
- **AI context files surfaced**: the repo overview handler reads `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md` and embeds them in the overview markdown so an LLM dropping into a repo gets the context immediately.

## Gotchas

- **Unsupported types throw `INVALID_INPUT`** so the fetch waterfall falls through to scrapers: `action_run`, `compare`, `discussion`, `discussion_list` are parsed by `url-parser.ts` but not handled here. Throwing returns a non-200, the breaker registers as failed, and `run_fetch_race` proceeds to the next tier (which is the general waterfall).
- **`raw.githubusercontent.com` URLs parse as `raw_file`** and route to the file handler, which resolves the combined `<ref>/<path>` segment.
- **Large diffs**: PR-with-files mode pulls the patch diff. `PATCH_MAX_CHARS` truncation applies per-file.

## Related

- Registered as `github` in `../../unified/fetch.ts`.
- Domain breaker in `../../../server/fetch_orchestrator.ts CONFIG.breakers.github` — runs FIRST (before the YouTube and social_media breakers).
- `../../../common/http.ts` for HTTP transport + tracing.
