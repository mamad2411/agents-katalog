---
name: infinite-run-ai-seo
description: >-
  Run a self-pacing, never-stopping AI-SEO improvement loop over a website:
  each tick pulls the next unworked target query from a persisted backlog,
  makes one validated on-page improvement, deploys only when meaningful, then
  re-arms the next wake. Periodically discovers NEW target queries and appends
  them to the backlog so the loop keeps finding fresh surface area to win
  instead of stalling. Use when the user asks to "run AI SEO continuously",
  "keep improving the site forever", "infinite AI SEO loop", "non-stop audit
  improve deploy", "find more queries and improve terus-terusan", or wants a
  resumable, backlog-driven AI-SEO loop rather than a fixed-interval spammer.
  Pairs with marketing-skills:ai-seo (strategy), the geo-audit skill (audit),
  and the loop skill (scheduling primitive).
---

# Infinite Run AI SEO

A persistent, backlog-driven loop that keeps improving a site's AI-search
performance forever. Each tick does **one** sensible unit of work, then
re-arms. It does NOT deploy every tick. It does NOT fire on a 6s cadence.

## Why this exists

A fixed `6s` loop floods notifications and pushes empty commits to Vercel. A
real AI-SEO cycle (audit → improve → build → deploy → propagate) takes
minutes. This skill makes the loop **resumable** (state on disk) and
**self-expanding** (it finds new queries), so "run forever" is safe.

## Files (per site)

All loop state lives in the site repo so it is inspectable, commitable, and
survives stop/restart.

```
<site-repo>/.ai-seo/
├── backlog.jsonl      # one query per line, the loop's memory
├── runs.log           # append-only tick log (ts, action, outcome)
└── config.json        # cadence, deploy gate, discovery interval
```

### backlog.jsonl

One JSON object per line. Status: `pending` → `working` → `done` | `skip`.

```jsonl
{"q":"apakah ada kelas AI untuk anak di Indonesia","page":"/","status":"done","commit":"3a7c7a9","ts":"2026-07-01"}
{"q":"kursus AI anak SD online","page":null,"status":"pending","found":"2026-07-01","source":"discovery"}
{"q":"biaya les AI untuk anak","page":null,"status":"skip","reason":"pricing claim — off-site only","ts":"2026-07-01"}
```

Normalize `q` for dedupe (lowercase, trim, collapse spaces). Never keep two
lines with the same normalized query.

### config.json

```json
{
  "cadenceSeconds": 900,
  "minDeployGapSeconds": 600,
  "discoveryEveryTicks": 10,
  "maxEmptyDiscoveryStops": 3,
  "honestyGuardrails": true
}
```

## Tick workflow

On each wake (sentinel `AGENT_LOOP_TICK_aiseo` or dynamic heartbeat):

1. **Read** `.ai-seo/backlog.jsonl` and `.ai-seo/config.json`.
2. **Pick** the top entry with `status=pending`. If none:
   - If `ticksSinceDiscovery >= discoveryEveryTicks`, run **Discovery** (below)
     and re-pick. If discovery returned nothing, increment
     `consecutiveEmptyDiscovery`; if it reaches `maxEmptyDiscoveryStops`, pause
     the loop and tell the user on-site surface is saturated (off-site levers
     remain: indexing, Google Business Profile, backlinks).
   - Else re-arm a long heartbeat and return.
3. **Audit** the chosen query against the site:
   - Which page should answer it? Existing page, or does it need a new
     section/page?
   - Is there an extractable answer block (40–60 words, self-contained,
     affirmative, no foil "X not Y" phrasing)?
   - Is there matching schema (`FAQPage`, `Course`/`Service`, `speakable`)?
   - Does the page have a stable `id` anchor for the answer?
4. **Improve**: make the **smallest** change that closes the gap. One page, one
   edit. Add/strengthen the answer block, schema, or anchor. Respect the
   site's `CLAUDE.md` honesty guardrails — no fabricated testimonials, no
   invented prices, no unbacked superlatives. Never claim a client that
   doesn't exist.
5. **Build** (`pnpm build` / `npm run build`). If red, fix or revert; do not
   deploy a broken build.
6. **Deploy gate** — push only if ALL hold:
   - build is green,
   - the change is meaningful (not whitespace/rename-only),
   - `now - lastDeployTs >= minDeployGapSeconds` (anti Vercel/git spam),
   - there are uncommitted changes worth shipping.
   Otherwise stage the edit locally and re-arm without deploying.
7. **Record**: update the backlog line to `done` (with commit hash + ts) or
   `skip` (with reason), append a line to `runs.log`, update
   `ticksSinceDiscovery` and `lastDeployTs`.
8. **Re-arm** the next wake using the loop skill's dynamic schedule
   (fallback heartbeat = `cadenceSeconds`). Do NOT use a fixed 6s loop.

## Discovery

Find new candidate queries to append to the backlog. Sources, in priority:

1. **Related searches / "People also ask"** for queries already in the backlog
   (variant phrasings, long-tail, locale variants).
2. **`firecrawl_search`** with diverse framings of the topic — synonyms,
   audience segments, intent variants. Run several distinct framings, not one.
3. **Refactor winners**: for any `status=done` query that the site now answers
   well, derive its long-tail variants ("X online", "X di <kota>", "X untuk
   <usia>", "biaya X", "berapa lama X").

For each candidate: normalize, dedupe vs every existing backlog line (any
status), and append as `pending` with `source: "discovery"` and `found` date.
Skip candidates that would require off-site proof to answer truthfully
(pricing, testimonials, rankings) — mark them `skip` with a reason instead of
leaving them as bait.

## Cadence

Use the loop skill in **dynamic** mode. The fallback heartbeat is
`cadenceSeconds` (default 900s / 15m). That is the cadence that actually fits
a build+deploy+propagate cycle. Never run this on a fixed sub-minute interval.

## Starting

```bash
/loop /ai-seo infinite-run on <site-repo>
```

On first start:
1. Create `.ai-seo/` and seed `backlog.jsonl` with the user's primary target
   query (status `pending` or `done` if already won) plus 3–5 obvious
   variants.
2. Write `config.json` with defaults (or values the user gave).
3. Run the tick workflow once immediately.
4. Arm the first heartbeat; confirm cadence and that the loop is self-pacing.

## Stopping / pausing

- User says stop → kill any watcher/heartbeat PID, do not re-arm. Backlog
  stays on disk so the loop is fully resumable later.
- Auto-pause → `consecutiveEmptyDiscovery >= maxEmptyDiscoveryStops`: stop
  arming and tell the user on-site levers are saturated; list the remaining
  off-site actions they must do themselves.

## Guardrails (always on)

- One meaningful change per tick. No empty commits. No deploy spam.
- Honesty first: never fabricate evidence. If a query can't be answered
  truthfully on-page, mark it `skip` with the reason.
- Run the project's anti-AI-slop pass on any user-facing copy before it ships
  (no em-dashes, no "X, not Y" foils, ground or remove unsourced claims).
- Keep the backlog the single source of truth — do not keep query state in
  your head across ticks.
