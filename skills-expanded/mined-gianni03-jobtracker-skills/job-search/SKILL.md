---
name: job-search
description: "Trigger: buscar trabajo, buscar ofertas, buscar empleos, job search, scrape jobs, new jobs, ofertas laborales, vagas, buscar vacantes, hay algo nuevo. Search live job postings across LinkedIn, GetOnBoard, Computrabajo, RemoteOK, freehire, and public Telegram channels; filter by location and recency; deduplicate across runs; score against a configurable profile; and render an interactive HTML report with applied / out-of-scope feedback that trains the next run."
license: Apache-2.0
metadata:
  author: "giannipasquinelli"
  version: "1.0"
---

## Activation Contract

Use this skill when the user wants to **find** job postings: "buscar trabajo", "qué hay
nuevo", "buscar ofertas de frontend", "alguna vacante remota", "/scrape". The skill only
**discovers, filters, and ranks** candidates. It never writes a CV or a cover letter —
pair it with a separate application skill for that.

Everything personal lives in `profile.json`. The skill ships with
`profile.example.json`; a real user copies it to `profile.json` and edits it. No code
change is needed to target a different role, country, or seniority.

## Hard Rules

- **Never fabricate a posting.** Every row must trace to real CLI output or a real search
  result. No guessed companies, titles, URLs, or deadlines. If a search fails, say so.
- **Personal use only.** The LinkedIn CLI uses public `jobs-guest` endpoints, and
  automated access is against LinkedIn's ToS. Keep volume low: one search per query
  category per run, never a crawl, never pagination past page 2.
- **Respect the date window.** `profile.json` sets it (default 7 days). A posting older
  than the window is not shown even if it was never seen before. Do not widen it
  silently.
- **Deduplicate before presenting.** A job already in `state/seen_jobs.json` is not new.
- **Only public Telegram channels.** A private invite link (`t.me/+...`) has no web
  preview and needs a logged-in MTProto client, which this skill does not do.
- **Never invent an email** that a posting or recruiter post does not state.
- **Flag distribution patterns, never accuse.** The same posting repeated across many
  cities is a caution signal about distribution, not evidence of fraud.
- **No automated people lookups.** Referral links are search URLs for the user to open.

## Setup — profile.json

Copy the example and edit it. Every rule the scorer applies comes from this file:

```bash
cp profile.example.json profile.json
$EDITOR profile.json
```

| Key | What it controls |
|---|---|
| `candidate` | Display name only; nothing is scored from it |
| `roles.high` | Title fragments that make a posting a strong match |
| `roles.medium` | Adjacent titles worth reading |
| `roles.specialist` | An extra high-signal family (AI building, security, whatever your edge is) |
| `stack.reject` | Title fragments that mean "wrong discipline", dropped entirely |
| `stack.reject_unless` | e.g. `{"backend": ["data"]}` — backend-only is rejected unless it also names data |
| `seniority.below` | Junior / intern / entry-level titles, dropped |
| `seniority.above` | Staff / principal / architect titles, demoted high → medium |
| `location.home` | Your city / region / country, the first report group |
| `location.region` | Remote-friendly places that are still realistic, the second group |
| `location.out_of_scope` | Places you cannot or will not work from, dropped |
| `search.jobage` | Freshness window in days |
| `search.limit` | Results requested per search |
| `search.role_gate` | Title pre-filter applied before scoring (cheap, removes the worst noise) |
| `search.searches` | The actual queries per portal |
| `blocked_domains` | Paywalled aggregators: dropped from the list, surfaced with search links instead |

See `assets/profile-guide.md` for a field-by-field walkthrough and
`assets/search-recipes.md` for portal-specific query patterns.

`profile.json` and `state/` are personal and gitignored. Never commit them.

## Portals

Invocations go through thin wrappers that resolve their own directory.

| Portal | Access | Coverage | Status |
|---|---|---|---|
| `linkedin` | Public `jobs-guest` endpoints | Any location, free text, global | Vendored CLI |
| `freehire` | Public REST API | Tech only, structured facets | Vendored CLI |
| `getonbrd` | Public JSON API, no auth | LatAm tech | Native source |
| `computrabajo` | Public HTML, stable `box_offer` markup | Argentina, city-level | Native source |
| `remoteok` | Public JSON API | Remote worldwide | Native source (attribution required) |
| `telegram` | Public `t.me/s/<handle>` preview | Whatever channels are configured | Native source |

`bin/portals` runs the four native sources behind one flag contract. `--source all`
runs every one; a failing source is reported and never aborts the run.

```bash
skills/job-search/bin/portals search -q "react" -l "<city>" --jobage 7 -n 20 -f json
skills/job-search/bin/portals list
```

## Execution

```bash
python3 tools/run.py --posts /tmp/opencode/posts.json
```

`run.py` reads `search.searches` from `profile.json`, runs every declared search in
parallel, applies the role gate, deduplicates, renders both files, and stores what it
saw. A source with no declared search is **reported**, never silently skipped.

Output:

- `ofertas/<YYYY-MM-DD>_ofertas.html` — self-contained, interactive, every posting a
  working link. Serve it with `tools/serve.py` so button clicks reach disk.
- `ofertas/<YYYY-MM-DD>_ofertas.md` — same rows, readable and diffable.

Two failure modes are handled inside `run.py` and must not be reintroduced:

- **stdout goes to a file, never a pipe.** Bun truncates at the 64 KB pipe boundary when
  the reader is a Python subprocess, silently returning half a JSON document. This cost
  a whole source before it was found.
- **Searches retry.** freehire occasionally answers with a truncated body under
  concurrent load; three attempts recover it.

Use `--dry-run` to see what would be new without writing, `--workers 3` if a source
starts failing, and `--no-store` to skip recording.

## Location matrix

`--location` means different things per source, and that difference is real:

| Target | How to ask | Behaviour |
|---|---|---|
| City-level presencial | `bin/portals -s computrabajo -q "<role>" -l "<city>"` | Only Computrabajo filters by city server-side; the URL becomes `trabajo-de-<role>-en-<city>` |
| Province / state | `-l "<province>"` | Loose match; also returns neighbouring cities and some capital noise |
| Remote worldwide | `-s remoteok,freehire` with `-l "Remote"` | No city filter; screen timezone yourself |
| LatAm tech | `-s getonbrd` | `countries` tells you whether it is `Remote` or a country |

`getonbrd` and `remoteok` have no server-side place filter, so `--location` is applied
client-side by substring against the posting's own location text. A posting with no
location text is kept rather than hidden — unknown is not the same as "elsewhere".

## Deduplication

The promise is: **a posting presented once is never presented again.** Enforced by
`state/seen_jobs.json`, owned by `tools/dedupe.py`; never edit that file by hand.

A job is already seen when either holds:

- its normalized URL matches (tracking parameters and `#fragments` stripped), or
- its canonical `company + title` matches, with separators collapsed so `Ryz Labs` and
  `RyzLabs` are one employer and `Desarrollador (SSR).` and `Desarrollador SSR` collapse.

Duplicates inside a single run are caught too, which matters when two portals return the
same posting under different URLs.

What it does **not** do: merge the same job across portals when the title is worded
differently and the URL differs. That needs fuzzy matching, and a false positive silently
hides a real opportunity.

Maintenance:

```bash
python3 tools/dedupe.py report --days 7            # what was seen this week
python3 tools/dedupe.py prune --days 180 --dry-run # bounded state, dry run first
```

`store` is mandatory at the end of every run. Skipping it is the only way a posting can
reappear tomorrow.

## Feedback loop

The report is not read-only. Every row carries **Aplicado** and **Fuera de rango**
buttons, and marking a row is how the skill learns.

| State | Meaning |
|---|---|
| **Aplicado** | Strongest positive signal |
| **Fuera de rango** | Rejected, with a reason: seniority, stack, location, language, company, closed |
| **Sin marcar** | Counted as pending. Silence is **not** rejection — never treat it as a no |

```bash
python3 tools/serve.py
```

Serves the latest report and appends each mark to `state/feedback.jsonl` immediately.
Opening the `.html` directly still works: it falls back to `localStorage` plus an
**Exportar feedback** button that downloads JSON.

```bash
python3 tools/feedback.py ingest --file feedback.json
python3 tools/feedback.py summary --days 30
python3 tools/feedback.py learn --min-signals 3
```

`learn` writes `state/learned-rules.json`, which `render.py` reads on every run. The
model is conservative and explainable:

- A word appearing in **3+ rejected** titles and **0 applied** titles becomes a demotion
  rule, carrying its evidence count.
- Demotion is capped at **high → medium**. It never deletes a posting.
- A word present in something applied is never demoted, even if it also appears in
  rejections.

Read `summary` before acting on rules. If one reason dominates, the fix may be the
profile rather than a learned rule.

## Blocked domains

Some aggregators exist only to route you into a paid subscription. `blocked_domains` in
the profile names them, and postings from those hosts:

1. are **removed from the main list** — they are not opportunities you can act on,
2. are **listed in a "Bloqueadas — buscar en otro lado" section** with the title and
   company preserved, and
3. get two working search links (Google and LinkedIn jobs) that find the same vacancy on
   a board that does not charge the candidate.

Nothing is fabricated: the links are ordinary searches, not invented posting URLs. Keep
the reason string short and factual; it is shown next to the row.

## Adding a Portal

A source exports one object in `portals/cli/sources/`:

```ts
export const myportal: Source = {
  name: "myportal",
  host: "myportal.com",
  async search({ query, location, jobage, limit }): Promise<Job[]> { /* ... */ },
};
```

Import it in `portals/cli/cli.ts` and append it to `SOURCES`. The CLI handles
parallelism, error isolation, location filtering, and output formatting.

Before writing one, check what the portal actually exposes. This is the result of real
probing, so it is not re-derived every time:

| Portal | Verdict | Evidence |
|---|---|---|
| `getonbrd` | **Built** | `/api/v0/search/jobs?query=` returns JSON; `expand[]=company` gives names |
| `computrabajo` | **Built** | `box_offer` articles carry title, company, location, modality, relative date |
| `remoteok` | **Built** | `/api` returns JSON; first array element is a legal notice |
| `telegram` | **Built** | `t.me/s/<handle>` renders ~20 posts with `data-post` and `<time datetime>` |
| `repelio` | Dead | returns 114 bytes |
| `s1jobs` | Wrong market | Scottish job board |
| `dice` | Not applicable | US-only; no remote-from-anywhere coverage |
| `chumi-it`, `bumeran`, `zonajobs`, `hiringroom` | Needs a browser | Listings are JS-rendered; no structured data in the initial HTML |
| `weromoto` | Fragile | Next.js RSC payload only; breaks on any deploy |
| `greenhouse` | Not a portal | It is an ATS; query one company at a time via `boards-api.greenhouse.io/v1/boards/<company>/jobs` |

"Needs a browser" means a headless Chromium dependency, which breaks the
zero-dependency rule this skill is built on. If one becomes essential, make it a separate
optional tool rather than a silent heavyweight dependency here.

## LinkedIn recruiter posts

A large share of hiring never reaches a job board: a recruiter posts the role and asks
for a CV by mail. LinkedIn's own content search requires a login, so this uses the
agent's web search tool instead.

```
site:linkedin.com/posts "<role>" "<stack>" "<city>"
site:linkedin.com/posts "hiring" OR "buscamos" "<role>" "<country>" <year>
```

Filter to posts that are fresh, an active search, and relevant. Write them to JSON and
pass to the renderer with `--posts`; they appear in their own section carrying their
**real age**.

Measured reality: one run of six queries returned posts from four different months, the
newest 58 days old. The public index lags by months, so this is **not** a freshness
feed. Its real value is a map of who hires this profile and the direct contact they
publish.

## Etiquette

These are public endpoints, unauthenticated, and every one can rate limit or block:

- One search per query category per run. Never paginate past page 2.
- Never run the same portal and query twice in a single run.
- Respect `robots.txt`, and stop on 429 instead of retrying in a loop.
- `remoteok` requires attribution and a follow link if results are republished.
