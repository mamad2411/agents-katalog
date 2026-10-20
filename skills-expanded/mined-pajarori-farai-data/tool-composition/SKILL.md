---
name: tool-composition
description: How to choose and chain farai's own tools during offensive work — when to use a typed recon tool vs shell_exec vs the browser, how to reach the Kali catalog, and how to record results into a campaign. Use when unsure which tool fits a step, when tempted to reach for shell_exec by default, or to compose tools into an efficient workflow.
metadata:
  domain: offensive-security
  tier: spine
---

# tool composition

farai already ships a large, purpose-built toolset. use it deliberately: a typed
tool gives normalized, deduplicated, bounded output and records cleanly; ad-hoc
`shell_exec` gives raw text you must parse and does not integrate. reach for the
specific tool first, `shell_exec` only for genuine gaps.

## decision order

1. **is there a typed tool for this?** prefer it. (see `resources/tool-map.md` for the full
   situation → tool table.)
2. **interactive or authenticated web state?** use `browser_*` with a named
   `browser_context`.
3. **one exact protocol request?** `http_request` (captured by the managed proxy in
   explicit mode).
4. **a Kali command with no typed tool?** the security context already carries a map
   of the official Kali catalog — select the command directly with `shell_exec`. do
   not run `which`/`command -v` first. use `kali_tool_search` only after exit 127,
   drift, or real ambiguity.
5. **record it**: turn a factual result into `campaign_observe`, an asset into
   `campaign_asset`, and keep raw proof with `evidence_save`.

## don't duplicate views

the browser, the proxy, and `http_request` are complementary views of the same
application, not three ways to repeat one request. `browser_navigate` already
returns a snapshot — call `browser_snapshot` only if it is missing or stale. in
explicit proxy mode, browser and `http_request` traffic is captured automatically;
inspect it with `proxy_sitemap`, `proxy_flows`, `proxy_flow_get`, and replay with
`proxy_replay` instead of re-issuing requests blindly.

## typed tool families (grounding)

- **passive discovery**: `subdomain_enum`, `url_discover` (never the same as
  interactive exploration).
- **validation / inventory**: `dns_probe`, `http_probe`, `tls_probe`, `port_scan`
  (naabu + targeted nmap), `nmap_scan`.
- **app mapping**: `web_crawl`, `dir_enum`.
- **signals / intel**: `vulnerability_scan` (pinned nuclei templates),
  `vulnerability_lookup` (cve/product intel), `exploit_search` (offline exploit-db).
- **interactive web**: `browser_context` and the `browser_*` actions;
  `email_*` for account/registration and out-of-band verification flows.
- **out-of-band**: `callback_oast` for blind ssrf/xxe/command/injection callbacks;
  `callback_host_info` + `callback_listen` for reverse-shell/callback catching.
- **proxy**: `proxy_scope` (recording scope), `proxy_policy` (upstream tls /
  passthrough), `proxy_intercept`, `proxy_replay`, `proxy_sitemap`, `proxy_flows`.
- **campaign / evidence**: `campaign_*`, `evidence_save`, `notes_add`,
  `report_add_finding`.

## cost and rate awareness

expensive modes (headless crawl, cipher enumeration, full port ranges, oast) cost
time and generate load. enable them only when the objective needs them. avoid
firing many parallel workers at one target when a bounded sequential probe answers
the question — enthusiasm can degrade an authorized target's availability.

## delegation

for bounded parallel work, use the lanes: `recon` (discovery), `web` (browser +
http + shell), `verify` (independent check). give parallel `agent_spawn` workers
non-overlapping ownership and keep synthesis in the parent.

resource: `resources/tool-map.md` — situation → best tool → why, and the recon→map→test→verify
chain.
