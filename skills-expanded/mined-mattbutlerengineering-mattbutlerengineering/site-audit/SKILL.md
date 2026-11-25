---
name: site-audit
description: "Audit mattbutlerengineering.com: smoke/sweep/scout modes. Invoke: /site-audit [smoke|sweep|scout]."
user-invocable: true
---

# Site Audit

Inventory-tracked 3-mode audit: smoke (regression), sweep (zone rotation), scout (improvements).

## Inventory

`.audit-state/inventory.json` tracks surfaces, check times, scores via agent-core: `buildInventory()`, `loadInventory()`, `saveInventory()`, `mapFilesToSurfaces()`, `findStalestZone()`, `updateSurfaceScore()`, `detectRegression()`.

```bash
cat .audit-state/inventory.json 2>/dev/null || echo "No inventory"
```

**Persist every real check result** — this is what feeds `findStalestZone()` and
regression detection; skipping it is why the inventory used to sit at
`checkCount: 0` forever (#4899). One-time per session: `pnpm --filter @mbe/agent-core build`
(the script imports agent-core's compiled dist). Then, after each live check:

```bash
node scripts/record-audit-check.mjs --surface "$SURFACE_ID" \
  --performance "$PERF" --accessibility "$A11Y" --best-practices "$BEST_PRACTICES" --seo "$SEO"
# check failed outright (5xx, timeout, blocked) — no scores, record the failure instead:
node scripts/record-audit-check.mjs --surface "$SURFACE_ID" --error "$ERROR_MESSAGE"
```

**Auth0-gated surfaces (`hospitality`, `gen`) are never skipped silently.** An unrecorded
surface keeps `lastChecked: null`, which makes `findStalestZone()` treat its zone as infinitely
stale and ranks it after earlier never-checked zones forever (#8419). Check the public response
(curl + Lighthouse on the login landing — no credentials), and record it with the method used:

```bash
node scripts/record-audit-check.mjs --surface gen:playground \
  --auth-gated "public login landing via Lighthouse" \
  --performance "$PERF" --accessibility "$A11Y" --best-practices "$BEST_PRACTICES" --seo "$SEO"
# no scores available: still record that it was checked and how
node scripts/record-audit-check.mjs --surface gen:playground --auth-gated "curl 200 on /gen, login landing"
```

The weekly `audit-sweep.yml` run records the same per-surface state automatically in the
**tracked** `metrics/audit-coverage.jsonl` (auth0 surfaces reachable only at the login page are
`auth-gated`, failures `error`, never-visited `unchecked`); the `auditCoverage` sensor and
`/ideate` read that, not the gitignored inventory (#8419).

Authenticated depth (E2E fixture) is separate; see [Auth](#auth-hospitality--gen).

## Environment Reachability (preflight — run FIRST, before any live check)

The agent proxy gateway in remote (claude.ai/code) containers may reject CONNECT
tunnels to the live site with HTTP 403 ("policy denial or upstream failure").
This is a **sandbox egress limitation, not a site defect** — the site is healthy;
this container simply has no route out. It surfaces as a curl **connection**
failure (exit 56 / `http_code == 000`), NOT an HTTP 403 _body_ (which is the
separate Cloudflare case — see [Access Restrictions](#access-restrictions)).

```bash
PROBE=$(curl -sS -o /dev/null -w "%{http_code}" --max-time 20 "https://mattbutlerengineering.com" 2>/dev/null)
PROBE_EXIT=$?
if [ "${PROBE:-000}" = "000" ]; then
  echo "ENVIRONMENT-BLOCKED: sandbox cannot reach the live site (proxy/CONNECT denial, curl exit ${PROBE_EXIT})."
  echo "The site is NOT down and NOT restricted — this container has no egress."
  echo "Run the audit from a local checkout instead (no agent proxy):"
  echo "  /site-audit <mode>"
  # Do NOT file 'site unreachable' / regression / infrastructure issues — a blinded
  # audit cannot judge the site, and doing so files noise (see #2913). Exit clean.
  exit 0
fi
```

Only proceed to the modes below once the probe returns a real HTTP status
(200/301/403/5xx). A `000` means "cannot see the site", never "site is broken".

## Mode 1: Smoke (per-commit)

1. `git diff HEAD~1 --name-only`
2. Map via `mapFilesToSurfaces()`: `apps/<app>/src/pages/*` → surface, `components/**` → all app surfaces, `packages/rialto/**` → all frontend, `services/*` → all API, `infrastructure/**` → all, else skip.
3. Parallel subagents: Pages → Lighthouse (perf+a11y), API → curl check.

**Curl pattern:**

```bash
AUDIT_CURL_OPTS=(-sf -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
[ -n "${AUDIT_TOKEN:-}" ] && AUDIT_CURL_OPTS+=(-H "X-Audit-Token: $AUDIT_TOKEN")
HTTP_STATUS=$(curl -o /dev/null -w "%{http_code}" "${AUDIT_CURL_OPTS[@]}" "$URL")
[ "$HTTP_STATUS" = "403" ] && echo "ACCESS-RESTRICTED: $URL"
```

4. Detect regressions (>0.05 drop vs lastScore), create issues (labels: `ci-fix`+`audit`), then persist the result for every surface checked via `node scripts/record-audit-check.mjs --surface "$SURFACE_ID" --performance ... --accessibility ... --best-practices ... --seo ...` (see [Inventory](#inventory)).

## Mode 2: Sweep (weekly zone rotation)

| Zone               | Surfaces | Auth  |
| ------------------ | -------- | ----- |
| `marketing`        | 1        | none  |
| `hospitality`      | 11       | auth0 |
| `rialto`           | 7        | none  |
| `gen`              | 1        | auth0 |
| `api:users`        | 1        | none  |
| `api:reservations` | 1        | none  |
| `api:agent`        | 1        | none  |

1. Load inventory, find stalest via `findStalestZone()`.
2. For each surface: `git log --since='$LAST_CHECKED' --name-only -- $SOURCE_FILES | head -1` → skip if empty, include if non-empty or never checked.
3. Parallel (5-wave max): availability (curl), Lighthouse, mobile (375x812), console errors, network (flag 4xx/5xx/>3s), dead links.
4. Create issues <0.9 or console errors. >50% blocked → one `[Audit] Infrastructure: Site unreachable` + stop. For every surface checked, persist the result via `node scripts/record-audit-check.mjs --surface "$SURFACE_ID" --performance ... --accessibility ... --best-practices ... --seo ...` (or `--error "$MESSAGE"` for a blocked/failed check) — see [Inventory](#inventory).

## Mode 3: Scout (monthly)

1. Analyze `checkHistory`: degrading 3+, below-threshold.
2. `pnpm outdated | head -30`
3. `grep -r "TODO\|FIXME" apps/ services/ packages/ --include="*.ts" --include="*.tsx" -l | head -20`
4. `ls -lh apps/*/dist/assets/*.js`
5. `gh issue list --state closed --limit 20 --json title,labels,closedAt`
6. Max 3 issues: `feature` or `meta-improvement` with evidence.

## Issue Creation

**Dedup:** `gh issue list --label audit --state open --search "<phrase>" --json number,title` → skip if exists.

**Closed-fix dedup (#9047):** also run `gh issue list --label audit --state closed --search "<phrase>" --json number,title,closedAt` and compare against the finding. On a match closed in the last 14 days, do NOT file a new "follow-up to #N" issue. Comment on the closed issue with the live evidence (command output, which acceptance bullets still fail), and reopen it (`gh issue reopen N`) if the defect is still present. If the closed issue's PR merged <24h ago, first check that the deploy and any data refresh (snapshots, dashboards, caches) have landed; if not, skip and re-check next run. File a new issue only when nothing matches or the match is older than 14 days, and then link the closed one.

**Title:** `[Audit] <Category>: <Finding>`

**Labels:** `audit`+`ready`+category:

- `performance` — perf, slow, bundles
- `accessibility` — labels, contrast, nav
- `seo` — meta, scores
- `ux` — links, visuals, responsive

Regressions: +`ci-fix`.

**Body:**

```markdown
## Finding

[Description]

## Evidence

[Score/error/trend]

## Location

[Surface/URL/component]

## Fix

[Suggestion or "Investigate"]

## Acceptance

- [ ] [One line per expected outcome; the closer ticks each with live evidence, and files any unmet remainder as a linked issue at close time (#9047)]

---

_Audit ({{mode}}) YYYY-MM-DD_
```

## Auth (Hospitality + Gen)

Auth0 surfaces via E2E fixture:

```typescript
import { test, expect } from "./fixtures.js";
test("loads", async ({ authPage }) => {
  await authPage.goto("/reservations");
  await expect(authPage.getByTestId("dashboard-layout")).toBeVisible();
});
```

## Access Restrictions

403 from Cloudflare Bot Management (curl **completes** with an HTTP 403 body — distinct
from the preflight `000` CONNECT-denial case in [Environment Reachability](#environment-reachability-preflight--run-first-before-any-live-check)):

1. Log `ACCESS-RESTRICTED: <url>`
2. Mark `restricted` in inventory
3. Skip Lighthouse/Playwright
4. Continue
5. > 50% blocked → one infrastructure issue + stop

**Enable (one-time):**

1. Cloudflare Security → WAF → Custom Rules
2. `X-Audit-Token == <secret>` → Skip Bot Fight
3. `wrangler secret put AUDIT_TOKEN`
4. Export `AUDIT_TOKEN=<secret>`

## Lighthouse

Check availability:

```bash
if command -v google-chrome &>/dev/null || command -v chromium &>/dev/null || command -v chromium-browser &>/dev/null; then
  LIGHTHOUSE_AVAILABLE=1
fi
```

Run only if available. Missing → null, note report, no issues.

## Config

Base: `https://mattbutlerengineering.com`
Threshold: 0.9 all categories

```bash
npx @lhci/cli collect --url="<url>" --settings.preset=desktop --numberOfRuns=1
npx @lhci/cli assert --assertions.categories:performance="error,minScore,0.9" --assertions.categories:accessibility="error,minScore,0.9" --assertions.categories:best-practices="error,minScore,0.9" --assertions.categories:seo="error,minScore,0.9"
```

## Rules

- Read-only
- Max 5 issues/run
- Dedup first
- Full down (5xx) → one issue + stop
- 403 ≠ down
- `ENVIRONMENT-BLOCKED` (proxy/CONNECT denial, curl exit 56 / http `000`) ≠ down and ≠ restricted → run preflight, skip, run locally, file **no** issues
- Regressions → `ci-fix`
