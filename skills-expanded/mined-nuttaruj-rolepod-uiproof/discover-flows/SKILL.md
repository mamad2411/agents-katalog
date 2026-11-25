---
name: discover-flows
description: Black-box flow discovery — crawl a running app (no source needed), map pages/links/forms, and propose a TC-ID/P1-P2 test-case table whose step sequences feed /verify-ui unchanged. Read-only; destructive actions are flagged, never executed.
---

# /discover-flows

Single-backend skill. Calls **`discover_flows`** on the rolepod-uiproof
MCP server. No fallback (D-024).

## When to use

- A running app must be tested but nobody can enumerate its flows up
  front — client sites, third-party apps, production WordPress reached
  via wplab. No source access required.
- Before writing a verify/e2e plan: get a flow map + proposed test-case
  table to review, then feed the chosen flows into `/verify-ui` (steps
  round-trip unchanged) and `/scaffold-e2e`.

## When NOT to use

- The flows are already known (you have the source or a spec) — write
  `/verify-ui` steps directly; a crawl only burns budget.
- You need deep interaction coverage (multi-step wizards behind POST
  forms) — discovery is read-only and will only flag those, not walk them.
- The target is not yours to probe. Crawl only apps you are authorized
  to test.

## Boundaries (read-only crawl)

- GET navigation only, same-origin by default. Cross-origin needs
  `allow_patterns`; `deny_patterns` always wins.
- Destructive-looking actions (delete / pay / send / publish / logout, …
  — English + Thai keywords, plus URL path/query patterns like
  `?action=delete`) are classified, listed as flows flagged
  `destructive: true`, and **never executed**.
- Redirects, iframes, and popups can't smuggle the crawler onto a
  destructive URL: every HTTP redirect chain is pre-flighted hop-by-hop
  (each Location vetted before it is ever requested), and a context-wide
  navigation guard aborts in-page redirects (meta refresh / scripted),
  iframe embeds, and `window.open` popups whose target is destructive or
  out of scope. Blocked hops surface in `page_errors`. A start URL that
  is deny-listed or itself destructive is refused before any request.
- `interact_forms: true` (opt-in) submits **GET forms only** with dummy
  data (search/filter discovery). POST forms are never submitted — that
  would mutate the target.
- Hard budget caps (`max_pages` ≤ 50, `max_depth` ≤ 5, `max_time_ms` ≤
  300000) with small defaults (10 / 2 / 60000). Anything truncated is
  reported in `truncated` — never silent.

## Inputs

- `url` — start URL (required).
- `max_pages` / `max_depth` / `max_time_ms` *(optional)* — crawl budget.
- `allow_patterns` / `deny_patterns` *(optional)* — regex URL filters.
- `setup_steps` *(optional)* — steps run once before the crawl (e.g. a
  login sequence), in the same step vocabulary `/verify-ui` uses. Never
  pass raw credentials as config — express login as steps.
- `interact_forms` *(optional, default false)* — opt in to GET-form
  submission with dummy data.
- `report_format` — `json` (default) | `markdown` (adds `flow-map.md`).
- `phase` *(optional)* — manifest phase hint; defaults to `build`
  (discovery produces test-plan artifacts, like `/scaffold-e2e`).

## Outputs

- `flows` — machine-readable flow list; each flow's `steps`/`expect` are
  `/verify-ui`-compatible and run unchanged (discover → verify →
  scaffold round-trip).
- `test_cases` — proposed table with stable `TC1…` ids, `P1`/`P2`
  priority, human-readable steps, expected result — the same convention
  the `/scaffold-e2e` handoff uses, so parent `rolepod-qa` consumes it
  directly and `check-work` can grep the IDs.
- `pages` / `page_errors` — crawl inventory.
- `destructive_count` + per-flow `destructive`/`executed` flags.
- `truncated` — `{hit, reasons, pages_not_visited}`; budget hits are
  visible, never silent.
- `report_path` (`flow-map.json`), optional `markdown_path`, `manifest`.

## Process

1. Build `discover_flows` input — start with defaults; raise budget only
   when the first run reports truncation.
2. Call the tool.
3. Review the test-case table with the user: confirm P1 rows, decide
   what (if anything) to do about flagged destructive flows.
4. Feed chosen flows into `/verify-ui` (steps as-is), then `/scaffold-e2e`
   for the keepers.

## Evidence routing

Run artifacts are saved under:

- **Standalone:** `.rolepod-uiproof/artifacts/discover_<ts>_<uuid>/`
- **With `rolepod` parent** (detected via the marker file `<git-root>/.rolepod/parent-active` written by the parent's SessionStart hook): `<git-root>/.rolepod/evidence/<ts>-rolepod-uiproof-discover-flows-<uuid6>/`

Either way the run directory contains `flow-map.json` and a
`manifest.json` per Extension Protocol v1 (default `phase: "build"`).

## If the tool is unavailable

Surface plainly:

> The `/discover-flows` skill needs the **rolepod-uiproof** MCP server
> (v0.16+), which is not currently available. Confirm the plugin is
> installed and up to date, then try again.

Do not attempt another backend (D-024).

## Examples

### Discover a small demo site

```json
{
  "url": "https://demo.example.com"
}
```

Returns (abridged):

```json
{
  "run_id": "discover_…",
  "status": "pass",
  "pages_visited": 6,
  "flows": [
    {
      "id": "flow-1",
      "name": "Navigate to Pricing",
      "kind": "navigation",
      "destructive": false,
      "executed": true,
      "steps": [
        { "kind": "navigate", "url": "https://demo.example.com/" },
        { "kind": "click", "query": "Pricing" }
      ],
      "expect": [{ "kind": "url_matches", "pattern": "/pricing" }]
    }
  ],
  "test_cases": [
    {
      "id": "TC1",
      "priority": "P1",
      "name": "Navigate to Pricing",
      "steps": ["navigate https://demo.example.com/", "click \"Pricing\""],
      "expected_result": "URL matches //pricing/",
      "destructive": false
    }
  ],
  "truncated": { "hit": false, "reasons": [], "pages_not_visited": 0 }
}
```

### Logged-in crawl with a bigger budget

```json
{
  "url": "https://app.example.com/dashboard",
  "max_pages": 25,
  "max_depth": 3,
  "deny_patterns": ["/admin/", "\\?action="],
  "setup_steps": [
    { "kind": "navigate", "url": "https://app.example.com/login" },
    { "kind": "fill_form", "fields": [
      { "query": "Email", "value": "qa@example.com" },
      { "query": "Password", "value": "…" }
    ]},
    { "kind": "click", "query": "Log in" },
    { "kind": "wait_for", "condition": { "kind": "url_matches", "pattern": "/dashboard" } }
  ]
}
```
