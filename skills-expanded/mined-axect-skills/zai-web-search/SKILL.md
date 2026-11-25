---
name: zai-web-search
description: Search the live web via z.ai web_search_prime (GLM Coding Plan MCP server). Use when the user wants current information, recent trends, news, blog posts, docs, or any web resource that academic-database search (reference-search) does not cover. Triggers on web search, 웹 검색, search the web, 최근 동향, 최신 트렌드, latest trends, find online, 인터넷에서 찾아, what's new, current state of X, search z.ai, GLM web search.
---

# zai-web-search

Live web search through z.ai's `web_search_prime` MCP server, included with the **GLM Coding Plan** subscription (no separate API recharge needed — see `references/protocol_notes.md` for why this matters and why the script uses MCP and not the REST API).

The single Python script handles the MCP streamable-HTTP handshake, SSE parsing, and the multiply-escaped JSON response so you can just call it.

## Division of labor with `reference-search`

These two skills are **complementary**, not competing:

| Skill | Sources | Best for | Output shape |
|---|---|---|---|
| **`reference-search`** | InspireHEP / OpenAlex / Semantic Scholar APIs | Academic papers, metadata, BibTeX, abstracts, citation context, baselines | Markdown-ready citations with quoted match sentences |
| **`zai-web-search`** (this) | Live web via z.ai search-prime | Recent trends, news, blogs, docs, non-academic resources, "what is the field doing right now" | title / link / snippet per result |

**Default routing**:
- "Find papers on X", "baseline citation for Y", "section needs references" → `reference-search`
- "Latest trends in X", "what is the community doing about Y", "search the web for Z", anything outside academic DBs → **`zai-web-search`**
- A claim that needs both a primary source (academic) and current context (web) → run both and merge.

## Trigger conditions

Invoke this skill when the user says any of:
- "search the web for X", "웹 검색", "인터넷에서 찾아봐"
- "latest / recent trends in X", "최근 동향", "최신 트렌드", "what's new in X"
- "current state of X", "how is the field approaching Y"
- a web-lookup need that is clearly not an academic-DB query (news, blogs, docs, repos, product pages)
- explicit "z.ai search" / "GLM web search" / "use the web"

## Prerequisites

The key is the **single source of truth** — pi's own credential store, not a duplicate:

    test -f ~/.pi/agent/auth.json
    python3 -c "import json,os;print(json.load(open(os.path.expanduser('~/.pi/agent/auth.json')))['zai-coding-cn']['key'])" >/dev/null

If either fails, tell the user:
> The z.ai key is not configured in `~/.pi/agent/auth.json` under `zai-coding-cn.key`. This key ships with the GLM Coding Plan login — it is the same key pi already uses for the default model. Re-login via pi if it is missing.

Do **not** create a second credential file. Do **not** ask the user to paste the key into a skill config. `auth.json` is the SoT.

## Script usage

    python3 scripts/web_search.py "<query>" [--limit 8] [--domain example.com] [--json] [--auth PATH]

Arguments:
- `query` (positional or `--query` / `-q`): the search query. MCP recommends ≤70 chars; the script hard-rejects >200.
- `--limit` / `-n` (default 8): max results.
- `--domain` : restrict to a domain (e.g. `arxiv.org`, `nature.com`). Optional. Results are also checked locally because the upstream filter may return off-domain items.
- `--json` : machine-readable output for piping into another script. Default is human-readable `[i] title / link / snippet`.
- `--auth` (default `~/.pi/agent/auth.json`): override the credential path (rarely needed).

Resolve the script path relative to this `SKILL.md` (skill dir + `scripts/web_search.py`).

### Examples

    # human-readable, top 6 results
    python3 scripts/web_search.py "autoregressive sampler Ising correlation failure" -n 6

    # restrict to arXiv, JSON for downstream processing
    python3 scripts/web_search.py "flow sampler critical slowing down" --domain arxiv.org --json

    # pipe into a quick relevance filter
    python3 scripts/web_search.py "..." --json | python3 -c "import sys,json; ..."

## How to use the results

- The script prints title / link / snippet. Snippets are short summaries from the search engine, not the page content — do not treat them as quotes from the source.
- For anything you plan to **cite**, open the link and verify the claim against the real page before quoting. Web-search snippets are for discovery and triage, not citation.
- When a result looks like an arXiv/paper link and you need BibTeX or abstract text, hand off to `reference-search` or `bibtex-gen` with the arXiv ID / DOI.

## Error handling

| Exit code | Meaning | Action |
|---|---|---|
| 0 | success | use the printed results |
| 1 | bad argument (query empty / too long) | fix the call |
| 2 | `auth.json` missing or no `zai-coding-cn.key` | user must (re-)configure pi login |
| 3 | auth rejected (HTTP 401 / MCP -401) | key invalid or expired → re-login via pi |
| 4 | search-side error (429, 5xx, MCP error) | surface the message; retry once after a short wait for transient 429 |
| 5 | network or parse failure | transient HTTP/TLS failures are retried twice; then show stderr and check connectivity |
| 64 | usage error | show `--help` |

Do not auto-retry on auth errors (exit 2/3). For 429, a single retry after 20–60s is reasonable; persistent 429 means either rate-limit or (for the REST endpoint) insufficient balance — but the MCP endpoint used here is covered by the Coding Plan, so persistent 429 on MCP is a rate-limit, not a billing issue.

## Limits and honest use

- Snippets are short and may truncate; do not over-claim what a page says from the snippet alone.
- The upstream domain filter is not always strict; `--domain` therefore applies a client-side hostname check (the requested domain and its subdomains are accepted).
- Web search can return stale or SEO-heavy results — cross-check claims that matter.
- This is a discovery tool. Pair with `reference-search` for citation-grade literature and with direct page reads (curl / a reader tool) when you need to quote.

## References

- `references/protocol_notes.md` — why MCP-not-REST, the streamable-HTTP handshake, SSE + multiply-escaped JSON parsing, and the gotchas that made this skill necessary.
