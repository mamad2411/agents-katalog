---
name: marketing-analytics
description: Pull Search Console and GA4 for drwho.me via the sibling analytics-toolkit and write a dated markdown report to docs/internal/analytics/ (gitignored). Use when asked how drwho.me is doing in search, or to check traffic to the tools or the MCP server.
---

# drwho.me analytics report

Read-only. Scope is ONLY `drwho.me`. Ignore every other property on the account
(domainposture.com has its own skill in its own repo). Never invent a number.

**Toolkit:** `~/Workspace/hikmah/analytics-toolkit` (sibling repo, shared with
Domain Posture). Default window 28 days; override with `DAYS=<n>`.

## Procedure

1. **Resolve node.** Bare `node` may be an nvm lazy-load function that recurses.
   `NODE="$(ls -d "$HOME"/.nvm/versions/node/*/bin/node | sort -V | tail -1)"` and
   use `"$NODE"` for every command.
2. **Auth check.** `"$NODE" ~/Workspace/hikmah/analytics-toolkit/discover.mjs`. If it
   fails with `invalid_grant` / `invalid_rapt` / `ADC refresh failed`, stop and ask the
   owner to run `bash ~/Workspace/hikmah/analytics-toolkit/login.sh` in an interactive
   terminal. From the output keep only `sc-domain:drwho.me` and the GA4 property for
   drwho.me (`properties/533500563` as of 2026-09; it also holds the pre-split history
   of the old site, so compare only windows after 2026-09-17).
3. **Pull.**
   - `DAYS=<n> "$NODE" ~/Workspace/hikmah/analytics-toolkit/gsc.mjs sc-domain:drwho.me`
   - `DAYS=<n> "$NODE" ~/Workspace/hikmah/analytics-toolkit/ga.mjs properties/533500563`
   - `DAYS=<n> "$NODE" ~/Workspace/hikmah/analytics-toolkit/ga-mcp.mjs properties/556540241`
     (the separate "drwho.me MCP" property; MCP events never go to 533500563).
   - Bing: run `traffic`, `pages` and `queries` with `https://drwho.me/` via
     `"$NODE" ~/Workspace/hikmah/analytics-toolkit/bing.mjs`.
   The site's own Cloudflare beacon is the primary page-view count; GA4 is secondary.
4. **Write** `docs/internal/analytics/YYYY-MM-DD.md` (the directory is gitignored — the
   repo is public and these notes name private infrastructure). Sections: header and
   window; totals with deltas against the previous file; top tool pages; top queries;
   MCP usage; three concrete actions.

   **MCP usage: report real use, never the raw total.** Most MCP traffic is directories and
   registries probing the server (glama, mcpbeat, tendle, `*-probe`, `*-health`, …). On
   2026-10-02 about 340 sessions came from ~57 clients and one was a real agent. Headline
   number = `REAL USE` from `ga-mcp.mjs` (tool calls from known agents + unclassified
   clients). Show the agent and unknown rows in full; give probes one summary line. If a new
   client name looks like a real agent or a probe, add it to the lists in `ga-mcp.mjs`.
   Treat `python-httpx` and `(no client name)` as unclassified, not as people.
5. Show the owner a short summary and the file path. Do not commit.
