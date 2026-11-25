---
name: scraperapi-cli
description: >
  Product-usage reference for the official ScraperAPI command-line tool (`sapi`, distributed as
  `scraperapi-cli`). Use this skill whenever the user wants to scrape, run async jobs, fetch
  structured data, manage crawls, check account credits, or drive DataPipeline projects from a
  terminal or shell script — anywhere a one-liner is more convenient than writing SDK code.
  Trigger on: "scrape this URL from the terminal", "use sapi to fetch X", "ScraperAPI CLI",
  "ScraperAPI from bash", "sapi scrape", "sapi cost", "sapi jobs", "sapi structured amazon",
  "pipe ScraperAPI into jq", "shell one-liner to scrape Y", "scrape from a Makefile / cron / CI",
  "check my ScraperAPI credits from the command line", "submit 10000 URLs as a batch from a file".
  Covers install, auth resolution order, every top-level command (`scrape`, `cost`, `jobs`,
  `structured`, `crawler`, `pipeline`, `account`, `config`, `init`), JSON / piping behaviour,
  pre-flight cost checks, and common shell recipes.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "⌨️"
    homepage: https://www.scraperapi.com/
---

# ScraperAPI CLI (`sapi`)

`sapi` is the official ScraperAPI command-line tool. It is the right choice when:

- The user is already in a terminal and wants a result *now* without writing a script.
- A scrape is part of a shell pipeline (`sapi … | jq …`, `xargs`, `make`, GitHub Actions).
- A one-off scheduled task (cron, launchd, systemd timer) needs to hit ScraperAPI without a project setup.
- The user is exploring — testing whether `--render` or `--premium` unblocks a target before committing the choice to code.

If the user is writing application code in Python, Node, PHP, Ruby, or Java, point them at the matching SDK skill instead — the CLI is for shells, not application logic.

## Install and authenticate

```bash
npm install -g scraperapi-cli    # requires Node.js 18+
sapi init                        # interactive: prompts for the key and validates it
```

Non-interactive setup (for CI / Dockerfiles):

```bash
sapi init --api-key "$SCRAPERAPI_API_KEY"
```

### Key resolution order

`sapi` looks for the API key in this order, stopping at the first hit:

1. `--api-key <key>` flag on the command
2. `SCRAPERAPI_API_KEY` environment variable
3. `~/.config/scraperapi/config.json` (written by `sapi init`)

In CI, prefer the env var — it keeps the key out of shell history and config files.

## Output contract — important for piping

| Stream | What goes there |
|--------|-----------------|
| stdout | The data (page body, JSON, table rows) |
| stderr | Spinners, warnings, errors |

When stdout is not a TTY (a pipe or redirect), `sapi` automatically switches to JSON mode:

```bash
sapi scrape https://example.com | jq .body            # auto-JSON
sapi scrape https://example.com > out.json            # auto-JSON
sapi scrape https://example.com                       # human output (page body to stdout)
```

Force JSON mode in a TTY with `--json`. Force a specific body format with `--output html|markdown|text|json|csv` — `--output` overrides the non-TTY auto-JSON rule, so you can pipe raw HTML or markdown into another tool without it being wrapped in JSON.

`sapi` does not prompt for confirmation on expensive calls. If you want to check what a request will cost before running it, use [`sapi cost`](#sapi-cost-url--preview-credit-cost).

## `sapi scrape <url>` — synchronous fetch

The workhorse command. Returns the page body to stdout.

```bash
sapi scrape https://example.com
sapi scrape https://example.com --render                       # +10 credits, JS rendering
sapi scrape https://example.com --render --wait-for "#main"    # wait for selector
sapi scrape https://example.com --country gb                   # geotarget UK
sapi scrape https://example.com --premium                      # +10 credits, residential proxies
sapi scrape https://example.com --ultra-premium                # +30 credits, hardest sites
sapi scrape https://example.com --autoparse --json             # structured JSON for supported sites
sapi scrape https://example.com --screenshot --json            # PNG (+10 credits) returned as base64 in JSON
sapi scrape https://example.com --async                        # submit as async job, prints jobId
```

### Escalation ladder

Always start at the cheapest option and only escalate when a request fails:

1. Default (1 credit). If 200 → done.
2. `--render` if the page loads content via JavaScript (SPA, hydrated tables, infinite scroll). +10 credits.
3. `--premium` if the site returns 403 / a block page from datacenter IPs. +10 credits.
4. `--ultra-premium` only for the hardest anti-bot sites (Cloudflare Turnstile, sophisticated fingerprinting). +30 credits.

Combining flags adds credits — `--render --premium` is ~20 credits per success.

### Flag reference

| Flag | Description | Credits |
|------|-------------|---------|
| `--render` | JavaScript rendering | +10 |
| `--premium` | Residential proxies | +10 |
| `--ultra-premium` | Advanced anti-bot bypass | +30 |
| `--screenshot` | PNG screenshot (base64 in JSON mode) | +10 |
| `--autoparse` | Auto-parsed JSON for supported sites | — |
| `--country <cc>` | ISO 3166-1 (e.g. `us`, `gb`, `de`) | — |
| `--device <type>` | `mobile` or `desktop` user-agent | — |
| `--output <fmt>` | `html`, `markdown`, `text`, `json`, `csv` | — |
| `--session <n>` | Sticky session number (reuse IP) | — |
| `--wait-for <sel>` | CSS selector to wait for (needs `--render`) | — |
| `--timeout <sec>` | Request timeout (default 70) | — |
| `--async` | Submit as async job, print job ID, exit | — |
| `--json` | Force JSON output mode | — |
| `--api-key <key>` | Override the configured API key for one call | — |

There is no interactive confirmation step — `sapi scrape` runs the request immediately. Use `sapi cost <url>` (below) to preview credit cost without spending credits.

## `sapi cost <url>` — preview credit cost

```bash
sapi cost https://example.com                   # base cost
sapi cost https://example.com --render          # with JS rendering
sapi cost https://example.com --render --premium
sapi cost https://example.com --render --json   # machine-readable
```

Accepts the same parameter flags as `sapi scrape` (everything except `--async` and `--timeout`) and prints something like `25 credits`. Useful as a pre-flight check before running an expensive batch — wire it into a script when you want to fail fast if a chosen flag combination is more expensive than expected.

## `sapi jobs` — async scraping

Use async for batches, slow targets, or fire-and-forget work.

```bash
sapi scrape https://example.com --async              # returns a jobId on stdout
sapi jobs list                                        # list all jobs
sapi jobs get <jobId>                                 # poll until done, print result
sapi jobs get <jobId> --no-poll                       # one-shot status check
sapi jobs cancel <jobId>                              # cancel a running job
sapi jobs batch urls.txt                              # submit up to 50,000 URLs from a file
```

`urls.txt` is one URL per line. Batches are the right tool whenever there are more than ~100 URLs — sync `sapi scrape` calls in a loop will burn through your concurrent request budget and hit 429s.

### Idiomatic batch pipeline

`sapi jobs batch` returns a JSON array — one entry per submitted job, each with its own `id`. Poll each child with `sapi jobs get`:

```bash
# 1. Submit a batch, grab every child job id.
sapi jobs batch urls.txt --json | jq -r '.[].id' > job-ids.txt

# 2. Wait for each one (`jobs get` polls automatically until finished).
while read -r ID; do
  sapi jobs get "$ID" --json >> batch-results.ndjson
done < job-ids.txt

# 3. Extract bodies that succeeded.
jq -s '[.[] | select(.status=="finished") | .response.body]' batch-results.ndjson
```

## `sapi structured` — pre-parsed JSON for supported sites

Whenever the target is Amazon, Google, Walmart, eBay, or Redfin, prefer `structured` over `scrape` + `--autoparse` + manual parsing. The endpoints return clean, schema-stable JSON.

```bash
# Amazon
sapi structured amazon product https://amazon.com/dp/B09XYZ
sapi structured amazon search "wireless headphones"
sapi structured amazon offers https://amazon.com/dp/B09XYZ
sapi structured amazon reviews https://amazon.com/dp/B09XYZ

# Google
sapi structured google serp "best espresso machine"
sapi structured google news "artificial intelligence"
sapi structured google jobs "software engineer remote"
sapi structured google shopping "standing desk"
sapi structured google maps "coffee shops near me"

# Walmart / eBay / Redfin
sapi structured walmart product https://walmart.com/ip/123456
sapi structured ebay product https://ebay.com/itm/123456
sapi structured redfin listing https://redfin.com/home/12345
sapi structured redfin search "Austin TX"
sapi structured redfin agents "Portland OR"
```

All structured commands accept `--json` for raw output (auto-on when piped). See [`docs.scraperapi.com`](https://docs.scraperapi.com/) for the schema of each vertical.

## `sapi crawler` — whole-site crawl

```bash
sapi crawler start example.com           # kick off a crawl, prints jobId
sapi crawler status <jobId>              # progress
sapi crawler results <jobId>             # list discovered URLs (human table)
sapi crawler results <jobId> --json      # JSON object: { jobId, urls: [...] }
```

The crawler is for discovering URLs across a domain. To then scrape each one, feed the result into `sapi jobs batch`:

```bash
sapi crawler results "$CRAWL" --json | jq -r '.urls[]' > urls.txt
sapi jobs batch urls.txt
```

## `sapi pipeline` — DataPipeline projects

Projects are configured in the [ScraperAPI dashboard](https://dashboard.scraperapi.com/); the CLI drives runs and reads results.

```bash
sapi pipeline list                  # list your projects
sapi pipeline run <projectId>       # trigger a run, prints jobId
sapi pipeline status <jobId>        # check run status
sapi pipeline results <jobId>       # fetch results
```

If the user wants recurring scraping but has no project yet, point them at the dashboard — `sapi` does not create projects.

## `sapi account` — credits and key management

```bash
sapi account                        # human summary: credits left, plan, period
sapi account --json                 # machine-readable
sapi account keys list              # list API keys on the account
sapi account keys create            # create a new key (returns once — copy it)
sapi account keys revoke <keyId>    # revoke a key
```

Always run `sapi account` before kicking off anything large — it's the cheapest way to confirm the key works and that there are enough credits.

## `sapi config` — persistent defaults

```bash
sapi config list
sapi config get api_key
sapi config set default_country gb
sapi config set default_output_format markdown
sapi config set default_timeout 90
```

Settable keys: `api_key`, `default_country`, `default_output_format`, `default_timeout`. Use `SCRAPERAPI_API_KEY` env var instead of `config set api_key` when the machine is shared.

## Shell recipes

### Scrape, extract a title with `pup`, append to CSV

```bash
URL="https://example.com"
TITLE=$(sapi scrape "$URL" --json | jq -r .body | pup 'title text{}')
echo "$URL,$TITLE" >> titles.csv
```

### Daily price check via cron

```bash
# crontab: 7am every day
0 7 * * * /usr/local/bin/sapi structured amazon product https://amazon.com/dp/B09XYZ --json \
  | jq '{ts: now, price: .pricing}' >> ~/prices.ndjson
```

### Parallel scrape with `xargs`

```bash
# Run 5 in parallel; --json puts one record per line (no prompts to worry about).
cat urls.txt | xargs -n1 -P5 sapi scrape --render --json > out.ndjson
```

Above ~100 URLs prefer `sapi jobs batch` over this — it sidesteps the concurrent request limit.

### Fail-loud in CI

`sapi` exits non-zero on any error, so `set -e` works as expected:

```bash
set -euo pipefail
sapi account --json | jq -e '.credits > 1000'             # fails the build if low
sapi scrape "$URL" --output markdown > page.md
```

### Escalate on block

```bash
sapi scrape "$URL" --output html > out.html \
  || sapi scrape "$URL" --render --output html > out.html \
  || sapi scrape "$URL" --premium --output html > out.html
```

Cheap → expensive, only paying for the next tier when the previous one fails. `--output html` keeps raw HTML in each redirect — without it the non-TTY rule would wrap the body in JSON.

## When NOT to reach for `sapi`

- **Inside application code** (Python, Node, PHP, Ruby, Java) — use the matching SDK skill; shelling out to a CLI is brittle.
- **Tight loops over thousands of URLs in a shell script** — submit a batch with `sapi jobs batch` instead so ScraperAPI handles concurrency and retries.
- **Long-running scheduled projects with webhook delivery** — DataPipeline (dashboard-configured) is the right product; the CLI drives runs but does not replace the project model.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `command not found: sapi` | Not installed, or `npm` global bin not on `$PATH` | `npm install -g scraperapi-cli`; check `npm config get prefix` |
| `401 Invalid API key` | Key missing or wrong | Run `sapi account` to confirm; re-run `sapi init` |
| `403` on a public page | Datacenter IP blocked | Retry with `--premium`, then `--ultra-premium` |
| `429` from `sapi` | Hit concurrent request limit | Switch to `sapi jobs batch` or add `xargs -P` cap |
| Hangs forever in a script | Default 70s timeout, target is slow | `--timeout 120`, or use `--async` |
| Output is JSON instead of HTML | stdout is piped → auto-JSON | Force with `--output html` if you want raw HTML in a pipe |

See [`docs.scraperapi.com`](https://docs.scraperapi.com/) for the full parameter reference and current credit costs.
