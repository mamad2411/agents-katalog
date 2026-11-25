---
name: devbox-perf
description: Measuring and speeding up the dashboard and devd. Use when the user says "it loads slowly", "make it faster", "why does it take so long", "the page takes long to load", "it's stuck", or when you are about to claim that something is faster. Also applies to verifying a speed-up after a change — most false results arise here, not in the optimization itself.
---

# devbox-perf

Speeding up the dashboard/devd stands or falls on measurement. **Never claim a speed-up you
have not measured against a readable "before".** This skill is mainly a catalog of the ways
measurement can be fooled — and of four architectural facts that are already verified, so that they
are not measured again.

## Iron rule

Every measurement must print **the HTTP code and the response size**. A dead server returns
`0.0002 s / 0 B` and in a table it looks like a thousandfold speed-up.

```bash
# wrong: speed without proof that it responded at all
curl -s -o /dev/null -w "%{time_total}" "$URL"

# right
curl -s -o /dev/null -w "%{time_total}s %{size_download}B HTTP %{http_code}\n" "$URL"
```

In comparison scripts, add a sanity check at the start and on a non-200 measurement **stop**,
do not just log it.

## Traps that produce false results

| Trap | How it shows | What to do |
|---|---|---|
| Dead server in the "after" branch | Everything 0.0002 s and 0 B | Print the HTTP code (see above) |
| Proxy passes `content-encoding` through | The dashboard reports "connection to devd lost"; it looks like a product bug | Bun `fetch` decompresses the body — in the proxy, delete both `content-encoding` and `content-length` |
| `networkidle` in Playwright | The run hangs, no output | The dashboard polls every 5 s; wait for a specific element/text with your own timeout |
| Reload in the same browser context | "Without cache headers nothing is downloaded anyway" | The browser cache can only be observed via `launchPersistentContext` and a fresh launch |
| A single measurement | Swings of 2–3× (CRON 3180 ms vs 1501 ms) | Median of 3 runs |
| Buffered stdout of a background bun script | Output is empty, the run looks stuck | Do not cancel it prematurely; the output appears at the end (or use `process.stdout.write`) |
| Sampling `<main>` right after a click | "Data in 0 ms" | That is the content of the PREVIOUS page; look for a marker of the new one |

## How to measure

### Endpoints from the server side

The fastest way to a time breakdown. Run on the VPS against `127.0.0.1:4300`, each endpoint
3× and take the settled value. Distinguish **the first and the second call** — for cached endpoints
that is exactly where the difference is.

### A/B of two versions side by side

The most honest comparison: both versions of `devd/src` on the same machine over **a copy of the live DB**
(`sqlite3 devd.sqlite ".timeout 20000" ".backup /tmp/copy.sqlite"`), each on its own
port, via `createApp` — not via the whole devd, which has side effects.

Replace external calls (`gh repo list`, `docker run`) with a stub that **sleeps exactly as
long as they take live**. Otherwise you are measuring the speed of GitHub, not of the code.

### Browser

Persistent profile, median of 3, and measure two different things separately:
- **when content appears** (the skeleton counts)
- **when the data arrives** (the last request)

A per-phase breakdown of the load (`requestAnimationFrame` + `performance.getEntriesByType`)
shows whether the gap is in the network, in waiting for `/api/vault`, or in the Suspense fallback.

## What is already verified — do not measure again

**devd has a single JS thread and `bun:sqlite` is synchronous.** One slow query also delays
static files and endpoints unrelated to it. Diagnostics:

```bash
for i in 1 2 3 4 5 6; do curl -s -o /dev/null "$URL/api/stats/live" & done
sleep 0.05; curl -s -o /dev/null -w "%{time_total}\n" "$URL/api/health"; wait
```

The healthy state is single-digit ms. Seconds = something is blocking the thread.

**A covering index over `metrics` must be over plain columns.** SQLite does not use a VIRTUAL generated
column as covering and computes the value from `attrs` anyway
(0.117 s vs 0.026 s on the same query). The attributes are filled on INSERT, see `ATTR_COLUMNS`
in `devd/src/db.ts`.

**Do not merge metrics into `name IN (?,?,?)`.** It is slower (0.202 s) than three
separate queries (0.024 + 0.06 + 0.03 s) — it scans three times as many index entries.

**A query that does not read `attrs` is an order of magnitude faster.** Where a
`SELECT attrs … JSON.parse` in JS is left over, it is a candidate for a covering index.

## After a frontend change

Code splitting and lazy routes take a UX toll that the numbers do not show:

- The Suspense fallback must not be empty — the user reads an empty area as stuck.
- On a route switch, React **keeps the previous page** until the new one finishes, so
  without `key={location.pathname}` on the Suspense boundary no indication is visible.
- Show the skeleton with a delay (~120 ms), otherwise a fast switch flickers.

Verify by clicking in **two rounds**: the first time the chunks are downloaded (the skeleton should be visible),
the second time they are in the cache (nothing should show, just the switch).

## Deploy

`git pull` → `bun run build:dashboard` → `systemctl restart devd`.

**Every devd restart locks the vault.** Until it is unlocked, the dashboard shows only the gate,
`/api/hardware` returns 503 and the clipboard and notifications silently do not work. Count on
having to ask for the unlock — and on not being able to verify anything visually until then.
The watchdog (`infra/devd-watch.ts`) sends a Pushover notification about the lock.

The migration over `metrics` (376 k rows) takes ~2.5 s at startup and inflates the DB by ~130 MB.
Make a `.backup` before it.
