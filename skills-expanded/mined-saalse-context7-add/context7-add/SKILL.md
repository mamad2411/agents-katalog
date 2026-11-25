---
name: context7-add
description: Add a repo, docs website, llms.txt, OpenAPI spec or PDF/DOCX file to Context7 when it is missing, then allow it in the teamspace policy (allowlist / wild-card list) so the Context7 MCP and API actually serve it. Use whenever the user asks to add, index, submit, whitelist or allowlist something in Context7, says "make X available in context7", or when a Context7 lookup fails with "not accessible", "not included in your allowed libraries", access_denied, or finds no library for a dependency the user is working with. Also use to check whether a library is already indexed and allowed.
license: MIT
compatibility: Requires Python 3.8+ (standard library only), network access to context7.com and api.github.com, and a Context7 API key (owner or admin role to change policies).
metadata:
  author: Alex Samson
  homepage: https://saalse.com
  repository: https://github.com/saalse/context7-add
  version: "1.2.0"
---

# Context7: add and allow

Context7 teamspaces can restrict which libraries their API keys may read (dashboard →
Policies). In **select** mode only libraries on the allowlist are served; in **quality** mode
libraries must pass filters unless they are on the wild-card list. So "making docs available"
is usually two steps: **index** the source if Context7 lacks it, then **allow** its library id.

## Available scripts

**`scripts/c7.py`** does every call. Run it from this skill's folder. It reads the API key
from `$CONTEXT7_API_KEY`, or else from the `context7` MCP server entry in `~/.claude.json`, and
never prints it. Every command that changes something is a **dry run unless `--apply`**.
Results are JSON on stdout; progress and errors go to stderr.

Exit codes: 0 ok · 1 API/network error · 2 bad input or file too large · 3 key/role/plan ·
4 not found · 5 refused by policy · 6 rate limited · 7 unprocessable or not a docs site ·
8 `wait` timed out · 9 submission queue full · 130 `add` interrupted (partial summary printed).

```bash
python3 scripts/c7.py whoami                       # plan, role, policy mode, which list admits libraries
python3 scripts/c7.py check <url|/org/repo|name>…  # indexed? fresh? allowed? which entry covers it?
python3 scripts/c7.py allow /org/repo [--remove] [--apply]   # dry run shows library count before/after
python3 scripts/c7.py add <url>… [--type …] [--base-url URL] [--private] [--queue [--queue-timeout SEC]] [--apply]
python3 scripts/c7.py upload <file.pdf|.docx|openapi.yaml> [--title …] [--description …] [--skip-size-check] [--apply]
python3 scripts/c7.py refresh /org/repo [--apply]  # re-crawl / re-parse a stale library
python3 scripts/c7.py wait /org/repo [--changed]   # until indexed; --changed: until a refresh lands
python3 scripts/c7.py log                          # what this skill changed before (registry.jsonl)
```

If the official Context7 Admin MCP (`https://admin.mcp.context7.com/mcp`) is connected, its
`add_library`, `get_library` and `update_library_policies` tools make the same calls; the
workflow below still applies.

## Gotchas

These come from real runs and contradict reasonable assumptions:

- **Search hides refused libraries.** `libs/search` and the MCP `resolve-library-id` only
  show what the policy allows, so "no result" doesn't mean "not indexed". `check` probes ids
  directly, which reports refused libraries as `blocked_by_policy_or_plan`.
- **Searching by name ranks loosely.** "RFC 5545" returns unrelated libraries. Turn a name into
  its official source first (repo URL, or docs URL: an RFC is
  `https://www.rfc-editor.org/rfc/rfcNNNN.html`) and check that.
- **Website ids drop parts of the URL.** `docs.` / `www.`, `.com` / `.org` / `.net` and a
  `docs` path segment are removed: `docs.github.com/en` → `/websites/github_en`,
  `example.com/docs/guide` → `/websites/example_guide`. `check` guesses these shapes (`guessedIds`).
- **A domain entry is about docs sites, not repo hosts.** A `github.com` entry does not admit
  GitHub repos; each repo needs its own entry or an owner entry.
- **"Already exists" is a 400, not a 409.** Submitting a repo or site Context7 already has
  returns `library-already-exists` with the id in the message; nothing is created. The script
  reports that id (exit 0), so `add` doubles as a safe lookup for a source you would add anyway.
- **Exists is not the same as covered.** A library can be months old and missing pages, or
  empty (`unprocessable`) while a more specific sibling has the content.
- **Crawls only follow the site's menu.** Pages the navigation never links stay out even after
  a refresh. The site's llms.txt files (`siteLlmsFiles` in `check`) list every page.
- **Only exact llms.txt names are accepted:** `llms.txt`, `llms-full.txt`, `llms-small.txt`.
  A per-section `llms-<name>.txt` is refused (the script stops before submitting).
- **Tiny libraries are rejected and stay public.** A section of one or two short pages ends
  `unprocessable` / `no_code_found`, and the failed library remains in Context7's index. Say
  so and skip it rather than submit.
- **The library count ignores empty libraries.** `accessibleLibraryCount` doesn't move when you
  allow something empty or still processing.
- **Claiming needs a Write-access key.** Policies and public submits work with a normal key,
  but the management API (`/v2/teamspaces/…`: claim, owned-library settings, Docs7 sites)
  answers 403 `write_access_required` unless the key was created with **Write access**
  ticked. Otherwise send the user to the dashboard for those steps.
- **Only 5 submissions in flight per user.** More get `400 user-has-active-task` (exit 9).
  Pass all URLs to one `add … --queue --apply` and run it in the background. It waits for free
  slots, so don't write your own retry loop. Without `--queue`, resubmit the output's
  `notSubmitted` list later. URLs refused for other reasons, or lost to a network error, are in
  `failed`, and the exit code is the first such failure. `--type` and `--base-url` need one URL per call.
- **Uploads stop at about 4.5 MB** (`413 FUNCTION_PAYLOAD_TOO_LARGE`). `upload` refuses larger
  files before sending. Split a PDF by pages (`qpdf --empty --pages in.pdf 1-3 -- in-p1-3.pdf`),
  one upload per part, with the page range in the file name and `--title`.
- **An upload's id comes from the file name, not `--title`** (`/pdf/<prefix>-<file name>-<hash>`).
  Rename an opaque file name before uploading.
- **"Not a documentation website" is final.** `422 not_documentation_website` (exit 7) means
  Context7 scored the site too low (marketing pages, blogs). Look for a docs subdomain or
  llms.txt; otherwise list it as "read on the web".
- **A fresh submit looks missing.** Right after `add`, the id answers `no_snippets_found`
  (`processing_or_empty`) until parsing finishes. Use `wait`, not a single probe.

## Workflow

Progress:
- [ ] 1. Orient: `whoami`
- [ ] 2. Check every input: `check`
- [ ] 3. Decide per item (table below)
- [ ] 4. Show the plan with dry runs; apply what the request covers, ask for the rest
- [ ] 5. `wait`, then verify with `query-docs`
- [ ] 6. Report

### 1. Orient (once per session)

Note the role (only `owner`/`admin` can change policies or add private sources) and
`allowList`: `select.allowedLibraries` (the allowlist), `quality.exceptedLibraries` (the
wild-card list; libraries that pass the filters are already served), or `null` (no filter:
only indexing can be missing). Don't switch the policy mode: it changes what the whole
teamspace can read.

### 2. Check every input

Run `check` with all inputs at once: repo URLs, `owner/repo`, library ids, context7.com
library URLs, docs site URLs, llms.txt or OpenAPI URLs, GitHub user/org URLs, or names. Read
`state` (`ready`, `processing`, `processing_or_empty`, `blocked_by_policy_or_plan`,
`unprocessable`, `not_found`), `coveredBy` (entries that already admit it), and for ready
libraries `lastUpdateDate` / `totalSnippets`.

For a docs site, compare that with the site itself (its `sitemap.xml` lists the pages) and
spot-check one recent page with `query-docs`. For a GitHub user/org URL, `check` lists the
owner's repos with their states: each repo is its own library; skip forks in favour of the
upstream repo.

### 3. Decide per item

| Situation | Action |
|---|---|
| ready and covered | Nothing to do. Say which entry covers it. |
| ready but stale or missing pages | `refresh <id>`, then `wait <id> --changed` (daily refresh limit) |
| pages still missing after refresh | propose the site's exact-named llms.txt as an `llmstxt` source if it lists them; else a narrow website (`add <section url> --base-url <section url>`) only if the section has real content |
| exists but not covered | `allow <exact id>` |
| exists but empty (`unprocessable`) | look for a more specific sibling (`guessedIds`, or `add` returns it); don't allow the empty one |
| public repo not found | `allow <exact id>`, then `add <url>`, then `wait` |
| website / llms.txt / OpenAPI not found | `add <url>`, then `allow <libraryId from the response>` |
| add refused with `access_denied` | the submit is gated by the policy: allow the docs host, retry, allow the exact id, offer to remove the host entry |
| private repo | `add <url> --private` (paid plan; account connected in the dashboard, or `--git-token-env VAR`). Private sources aren't gated by the public allowlist |
| several missing sources | `allow` the exact ids of the public repos first (the add is gated by the policy), then one `add <url> <url> … --queue --apply` in the background, then `allow` each new `libraryId` from the results (websites, llms.txt, OpenAPI) |
| PDF / DOCX / OpenAPI file | `upload <file>`; private to the teamspace, no `allow` needed; over ~4.5 MB, split it first (a PDF by pages) |
| Notion, Confluence | needs connected accounts: send the user to https://context7.com/add-library |

**Allow the narrowest entry that works.** The allowlist is a security control: `/owner/repo`
admits one library, `/owner` everything that owner publishes now or later, a domain every
library documented on that host. Use exact ids unless the user wants the wider scope.

### 4. Confirm, then apply

Show a short table: input → action → entry → dry-run count change. When the user names
specific sources and asks to add or allow them, that covers submitting exactly those and
allowing their exact ids: apply. Ask first (one question for everything) before owner or
domain entries, anything the user didn't name, removals, private repos or uploads (content
leaves the machine), and narrow-section submissions. A public submission is indexed for every
Context7 user; never submit something the user called internal without `--private`.

### 5. Wait and verify

Run `wait <id>` in the background (indexing takes minutes). On `ready`, verify with the MCP
`query-docs` tool using a question the user cares about. `blocked_by_policy_or_plan` means the
allow step is missing or used the wrong id (ids are lowercase; follow `redirectUrl` on a 301).
`unprocessable` means no usable docs: suggest a narrower `--base-url`, or a `context7.json` in
the repo listing the folders to index.

### 6. Report

One line per input: library id, what was done (indexed / refreshed / allowed / already
available / skipped and why), the entry that admits it, and the verified state. Mention
anything still processing and any entry the user may want to remove.

## Notes

- Applied changes are appended to `registry.jsonl` next to this file (`scripts/c7.py log`).
- Each `check` probe and `wait` poll is one API request; `wait` polls every 20 s.
- References: https://context7.com/docs/api-guide, https://context7.com/docs/howto/policies,
  https://context7.com/openapi.json.
