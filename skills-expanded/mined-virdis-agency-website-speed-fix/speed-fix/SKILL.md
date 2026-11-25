---
name: speed-fix
description: |
  Audit a URL with Google PageSpeed Insights and apply concrete speed fixes to the
  current working directory. Detects stack (Next.js, Vite, Astro, SvelteKit, Nuxt,
  WordPress, plain HTML), maps PSI audits to remediation steps via audits.md, applies
  stack-specific recipes from playbooks.md, and verifies with a post-apply re-audit.
  Plan-then-apply by default: never edits without user approval unless `--apply` is passed.
trigger: /speed-fix
user-invocable: true
---

# /speed-fix

Run a PageSpeed Insights audit against a URL, produce a ranked, file-linked remediation plan for the current working directory, and apply approved fixes. Covers the long tail of Lighthouse opportunities — LCP render delay, render-blocking CSS/JS, legacy polyfills, oversized images, unused JS, font loading, preconnect hygiene, third-party weight.

## Usage

```
/speed-fix <url>                       # audit mobile, produce plan, wait for approval
/speed-fix <url> --strategy desktop    # desktop audit instead
/speed-fix <url> --strategy both       # audit both; plan from the worst-scoring audits
/speed-fix <url> --apply               # skip the approval gate, edit + rebuild + verify
/speed-fix                              # no URL → infer from repo config
```

## API key (optional, recommended)

Set `GOOGLE_PAGESPEED_API_KEY` to avoid the ~1 req/s anonymous rate limit. The skill resolves the key in this order — first hit wins:

1. `$GOOGLE_PAGESPEED_API_KEY` in the current shell environment
2. `~/.claude/skills/speed-fix/.env` — a single line `GOOGLE_PAGESPEED_API_KEY=AIza...`
3. anonymous (no key) — still works, just rate-limited

Get a free key at <https://console.cloud.google.com/apis/credentials> → _Create credentials_ → _API key_ → restrict to the _PageSpeed Insights API_. No quota cost for the free tier.

To use the local-file option:
```bash
echo 'GOOGLE_PAGESPEED_API_KEY=YOUR_KEY_HERE' > ~/.claude/skills/speed-fix/.env
chmod 600 ~/.claude/skills/speed-fix/.env
```
The file is gitignored by this repo.

## Flow

When invoked, execute these steps in order. Output should be terse: one-line status per step, a full plan table at step 6, and a before/after diff at step 9.

### 1. Resolve the target URL

If `<url>` is passed, use it. Otherwise infer:
- `package.json` → `homepage` field
- `next.config.*` → `aeo.url` / `metadataBase` / any string literal `https://...`
- `astro.config.*` → `site`
- `vercel.json` / `netlify.toml` → production domain
- `.env*` → `NEXT_PUBLIC_SITE_URL`, `SITE_URL`, `PUBLIC_URL`, etc.

If multiple candidates or none, ask the user once.

### 2. Detect the stack

Check project root (in order; first hit wins):

| Marker | Stack | Playbook section |
|---|---|---|
| `next.config.{ts,js,mjs}` | `nextjs` | `playbooks.md#nextjs` |
| `nuxt.config.{ts,js}` | `nuxt` | `playbooks.md#nuxt` |
| `astro.config.{ts,js,mjs}` | `astro` | `playbooks.md#astro` |
| `svelte.config.{js,ts}` | `sveltekit` | `playbooks.md#sveltekit` |
| `vite.config.{ts,js,mjs}` (and not Astro/SvelteKit) | `vite` | `playbooks.md#vite` |
| `wp-config.php` | `wordpress` | `playbooks.md#wordpress` |
| otherwise | `generic` | `playbooks.md#generic` |

State the detected stack on one line (e.g. `stack: nextjs (next.config.ts)`).

### 3. Fetch PSI

```bash
# Resolve API key: env var, then ~/.claude/skills/speed-fix/.env, else anonymous
KEY="${GOOGLE_PAGESPEED_API_KEY:-}"
ENV_FILE="$HOME/.claude/skills/speed-fix/.env"
if [ -z "$KEY" ] && [ -f "$ENV_FILE" ]; then
  KEY=$(grep -E '^GOOGLE_PAGESPEED_API_KEY=' "$ENV_FILE" | head -1 | cut -d= -f2- | tr -d '"'"'" )
fi

STRATEGIES=("mobile")        # or ("desktop") or ("mobile" "desktop") for --strategy both
HOST=$(echo "$URL" | sed -E 's|https?://||; s|/.*||')
TS=$(date +%s)
mkdir -p /tmp/speed-fix
for S in "${STRATEGIES[@]}"; do
  curl -sS --max-time 60 \
    "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$(printf '%s' "$URL" | jq -sRr @uri)&strategy=$S&category=PERFORMANCE${KEY:+&key=$KEY}" \
    > "/tmp/speed-fix/psi-$HOST-$S-$TS.json"
done
```

On non-200 or missing `lighthouseResult`, surface the error and stop.

Print one summary line per strategy:
```
mobile: Perf 62 | LCP 3.9s | CLS 0.04 | TBT 680ms | TTFB 280ms
```
Pull from `lighthouseResult.categories.performance.score` (×100) and `lighthouseResult.audits.metrics.details.items[0]`.

### 4. Parse audits

For each `audit` in `lighthouseResult.audits` where any of:
- `score !== null && score < 0.9`
- `details.overallSavingsMs > 100`
- `details.overallSavingsBytes > 5120`
- `details.type === "opportunity"` with non-empty `items`

…record `{ id, title, savingsMs, savingsBytes, items }`. If `--strategy both`, merge on audit id and take the worse score.

Look up each `id` in `audits.md`. If the id isn't in the table, bucket it as `investigate` and include verbatim in the plan; extend `audits.md` opportunistically after the run.

### 5. Map audits to files

For each remediation, use Grep/Glob to locate the concrete files — e.g.:

| Audit id | Grep targets |
|---|---|
| `render-blocking-resources` | `<link rel="stylesheet"` in `app/layout.*`, `pages/_document.*`, `public/**/*.html`; `<script[^>]*src=` without `defer`/`async` |
| `legacy-javascript` | `browserslist` in `package.json`, `.browserslistrc`; `target` in `tsconfig.json`, `vite.config.*`, `next.config.*` |
| `uses-responsive-images` | `<Image ` / `<img ` with `sizes=`, `srcset=`, or missing them |
| `uses-optimized-images` | image extensions in `public/`, `src/assets/`, `static/` |
| `uses-rel-preconnect` | `<link rel="preconnect"` in `<head>` templates |
| `third-party-facades` | script tags / dynamic imports matching known third-parties (YouTube, Intercom, Drift, HubSpot, GTM, Cal.com) |

Annotate each item with `file:line` when found. If you can't locate a clean file target, mark the item as `advisory` — include it in the plan but don't propose an automated edit.

### 6. Render the plan

Output a ranked markdown table grouped by category. Column order:

```
| # | audit | category | est. savings | file(s) | proposed change |
```

Rank primarily by `savingsMs` (descending), then `savingsBytes`. Group headings in this order: `LCP critical path`, `Payload reduction`, `Images`, `Fonts`, `Third-party`, `Build config`, `Advisory`.

Below the table, list explicit file edits as `path:line → change`, short enough to scan.

### 7. Gate on approval

Unless `--apply`, stop here:
- **In plan mode:** call `ExitPlanMode`. The plan content is the markdown from step 6.
- **Outside plan mode:** print the plan and ask `Apply these fixes? (yes / pick / no)`. `pick` lets the user mark items to skip.

### 8. Apply fixes

For each approved item, perform the Edit/Write/Bash actions listed in `playbooks.md` under the detected stack. Rules:

- **One category at a time.** Apply LCP fixes, type-check, then payload, then images, etc. This makes it easy to isolate a regression to a single group.
- **Never commit.** Even if the prior session committed — the `/speed-fix` skill edits files only. User runs `git commit` when satisfied.
- **Re-run verification commands** after each group: if `package.json` has `typecheck`, run it; if it has `build`, run it. On failure, stop and report — do not keep applying.
- **Skip anything marked `advisory`.** Surface it in the final report as a follow-up.

### 9. Verify

Re-fetch PSI for the same strategy (or strategies). Emit a before/after line per strategy and per fixed audit:

```
mobile: Perf 62 → 81 | LCP 3.9s → 2.1s | TBT 680ms → 240ms
  legacy-javascript:  failed (14 KiB) → passing
  uses-responsive-images: 48 KiB → 8 KiB
  render-blocking-resources: 380 ms → 120 ms
```

If any audit regressed, flag it in red and do not proceed to further edits — ask the user how to handle.

### 10. Write the run report

Append `.speed-fix/<ISO-ts>.md` to the project with:

- Before/after PSI snapshot (score + CWV)
- List of applied fixes with file paths and short rationale
- List of skipped `advisory` items
- Raw PSI JSON path in `/tmp/speed-fix/` (for later diffing)

Ensure `.speed-fix/` is in `.gitignore` — if not, prepend it.

## References

- `audits.md` — PSI audit id → remediation mapping. Consult this in step 4.
- `playbooks.md` — per-stack recipes. Consult this in steps 5 and 8.

## Design notes (why this works)

- **Plan-first is load-bearing.** Some fixes (tightening `browserslist`, aliasing polyfill-module, setting `experimental.inlineCss`) have non-obvious blast radius. A user-reviewed plan catches mistakes the skill can't.
- **Skill is prompt, not code.** Claude does the work with Bash/Read/Edit. No bundled JS, no install step, no version drift.
- **Stack detection is cheap but critical.** A Next.js fix applied to a Vite repo will either error or silently no-op; the detection step prevents both.
- **Verification closes the loop.** Re-running PSI after edits is what turns this from "checklist of advice" into "measurable improvement."
