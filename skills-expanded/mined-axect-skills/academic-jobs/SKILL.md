---
name: academic-jobs
description: >
  Find and curate academic opportunities through AJO/InspireHEP and official
  institution/group-direct recruitment. Broad personal postdoc searches include
  both tracks by default, with one deduplicated result separating current vacancies,
  standing application routes, research-fit leads and conflicting/expired evidence.
  Respect explicit board-only requests; support named labs, changes since a previous
  search, field presets, stored postings and individual posting inspection.
  Triggers: academic jobs, AJO, InspireHEP, postdoc openings, Physics and AI jobs,
  research-group recruitment, 포닥 공고, 채용 공고, 연구실 채용, 잡 마켓.
---

# Academic Jobs Skill

The user-facing entry point for academic opportunity discovery. **Broad postdoc
curation runs both board searches and official institution/group-direct discovery.**
The user does not need another skill. The `ajo` CLI remains the board collector;
this integration changes the assistant workflow, not CLI source options.

## Request routing

| Request | Execution |
|---|---|
| Broad personal postdoc search, e.g. Physics×AI 포닥을 추려줘 | Both boards plus bounded official institution/group discovery; one integrated result |
| Explicit AJO-only / Inspire-only / board postings only | Only the requested board(s); no direct expansion |
| Named lab/institution, e.g. Tübingen AI postdocs | Official research and recruitment pages first; board identity checks for duplicates, no global fetch |
| Changes since previous search | Refresh the previous scope in both tracks and compare snapshots; preserve any explicit board-only restriction |
| Maintenance: config/list/show/enrich/mark-seen/prune, including “검색 preset 설정을 보여줘” | Maintenance only: execute the requested CLI operation, no board search, direct discovery or snapshot comparison |
| Faculty or PhD opportunities | Rank-appropriate board and employer sources; do not use the postdoc-only direct ledger for other ranks |

## Integrated curation workflow

1. Ground rank, research/method axes, target start and region policy in the current
   profile, saved preset and user decisions. Use the same policy in both tracks.
2. For broad postdoc searches, execute the board flow below AND
   [references/direct-discovery.md](references/direct-discovery.md). Start with
   2–3 relevant institutional ecosystems in preferred regions and declare the scope;
   expand for promising leads or requested breadth. This is not a global census or
   a quota of recommendations. Do not ask whether to add this track. When Europe
   is in scope, also read recent academics.de and AcademicPositions alert mails from
   Proton Mail as leads (never scrape either site; see the alert-mail section of the
   direct reference).
3. Read official research, recruitment policy and linked calls. The direct reference
   owns the evidence/status schema and uses the bundled
   `scripts/direct_ledger.py` validator/diff. No managed or externally installed
   companion skill is required. Reuse board results for identity checks rather
   than recursively restarting this workflow.
4. Deep-read both sources. Board candidates require `ajo show` and the complete
   stored body; direct candidates require the official page and linked call.
   Follow the full-body extraction instructions in `references/curation.md` when
   display truncation hides conditions. Targeted untyped searches can recover
   blank/mixed-rank fellowships; verify the postdoc branch in the body.
5. Deduplicate verified identical appointments by employer, group/PI, project,
   reference number, dates and application URL. Preserve all source links and
   `(source,id)` matches in one row. Different projects remain separate; a general
   application route is not an extra vacancy. A local DB miss does not prove
   absence from either live board.
6. Deliver ONE result with four sections:
   - **Current applicant-facing vacancies:** verified board and direct vacancies
     together, preference tier then actual application urgency; no invented dates
     for undated rolling calls.
   - **Standing application routes:** ongoing applications, current funded capacity
     not established.
   - **Research-fit leads:** no verified hiring, ranked by fit.
   - **Conflicting/expired/closed or host-funding-only findings:** reasons and
     evidence, excluded from open-vacancy totals. Host support is not employment.
7. Use the ten-field curation contract below. Separate method fit, scientific-domain
   fit, transition cost and start compatibility. Fit is not selection probability.
   Missing facts remain 명시 없음/null. An open banner against an expired linked PDF
   is a conflict, not permission to ignore the deadline.
8. Report board candidates/details/truncation, direct institutions/groups/calls
   actually read, and deduplicated counts by status. Do not sum overlapping fetches
   as unique jobs. Distinguish newly discovered records from newly posted calls.
9. Store direct evidence separately under `~/.local/share/academic-direct-opportunities/`,
   never as fabricated valid rows in AJO jobs.db. Validate dated snapshots and
   compare them with the bundled helper. Refresh sources before claiming a change;
   unobserved records and failed URLs are not automatically closed.

Mail, applications, calendar tasks, scheduled watchers, pruning and mark-seen are
not implicit in discovery. Respect the user's authorization for each.

## Board collector

The `ajo` CLI fetches **valid** postings from two boards into a local SQLite store:

- **AJO** — Academic Jobs Online (`academicjobsonline.org`), HTML scraping, all fields.
- **InspireHEP** — the HEP/astro jobs board (`inspirehep.net/jobs`), via its public JSON API.

By default `ajo fetch` searches **both** boards with the same keywords and merges the
results, deadline-sorted. Each posting carries a `source` (`ajo` or `inspire`); the two
boards use overlapping integer ids, so everything is keyed by `(source, id)`.

## Quick Reference

| Intent | Command | Reference |
|--------|---------|-----------|
| Integrated postdoc curation | Board CLI + official-source research | `references/direct-discovery.md`, `references/curation.md` |
| Validate / compare direct snapshots | `python3 scripts/direct_ledger.py validate FILE` / `diff BEFORE AFTER` | `references/direct-discovery.md` |
| Show / edit field presets | `ajo config [...]` | `references/presets.md` |
| Fetch current open postings | `ajo fetch [--preset N \| --keyword K] [--source ajo\|inspire\|both] [--preferred TIERS] [--excluded LIST] [--detail-cap N]` | `references/fetch.md` |
| Show stored postings | `ajo list [--valid] [--new] [--source S]` | `references/schema.md` |
| Inspect one posting (stored-first) | `ajo show {id} [--source ajo\|inspire] [--refresh]` | `references/fetch.md` |
| Fetch missing detail bodies | `ajo enrich [--source ajo\|inspire] [--detail-cap N] [--include-expired]` | `references/fetch.md` |
| Emit curation skeleton | `ajo report [--source S] [--preferred TIERS] [--excluded LIST] [--out PATH]` | `references/curation.md` |
| Mark postings as seen | `ajo mark-seen --all` | `references/fetch.md` |
| Drop expired postings | `ajo prune` | `references/schema.md` |

## Running the CLI

The CLI lives in this skill directory. Always invoke it through `uv`:

```bash
uv run --project <skill-dir> ajo <command> [...]
```

where `<skill-dir>` is the directory containing this file. Add `--json` to any command
when you (Claude) need to post-process the output; the default is a human table.

First run auto-creates the data dir, the SQLite DB, and a default `physics-ml` preset.

## Curation rule (read before writing a report)

Deep-read every reported board posting with `ajo show {id} --source S` and its
complete stored body. For direct opportunities, read the official recruitment page
and linked call. Never judge either source from titles or keyword matches alone.

Every posting in a report must fill the mandatory 10-field schema:

1. 직급/seniority
2. 기관, 그룹, 국가
3. 연구주제, PI
4. 자격/eligibility
5. 기간, 급여, 시작일
6. 마감 체계 (hard/rolling/etc.)
7. 지원 서류
8. fit 근거 + 등급
9. 신빙성/주의 플래그
10. 출처 URL

Use `ajo report` only for the board skeleton, then add verified direct records and
the integrated result sections. The complete curation procedure is in
`references/curation.md`. Reports are saved to
`~/Dropbox/AJO/AJO_YYYY-MM-DD.md` in Korean.

## Core behaviour you must understand

### Two board sources, one CLI view
- `ajo fetch` runs the preset's keywords against **every board in the preset's `sources`**
  (default `["ajo", "inspire"]`), merges, dedups within each board, and stores everything
  keyed by `(source, id)`.
- Override per run with `--source ajo` (AJO only), `--source inspire` (InspireHEP only), or
  `--source both`. With an ad-hoc `--keyword`, both boards are searched unless `--source` says
  otherwise.
- The same preset filters apply to both boards: `position_types` is matched against the AJO
  "Position Type" and against the InspireHEP `ranks` (e.g. `postdoc` matches `POSTDOC`);
  `countries` is matched against the institution string (plus InspireHEP `regions`).

### AJO validity (HTML)
**Validity is judged from the detail page, not the list.** The AJO list page only shows a
deadline for *some* postings, and a missing list deadline does NOT mean "no deadline". So
`ajo fetch` fetches each AJO candidate's detail page by default and judges validity from the
**effective deadline** = firm `Appl Deadline` if present, else the `listed until` date.
`--fast` skips AJO detail pages (faster but deadlines are approximate and many valid postings
will be missed). Prefer the default detail mode for correctness. `--fast` does not affect
InspireHEP.

### InspireHEP validity (API)
The InspireHEP API is queried with `status=open` (server-side), so closed postings never
arrive. The structured `deadline_date` is used directly, no detail fetch needed.

In both cases:
- valid  → effective deadline is in the future
- expired → effective deadline has passed (excluded)
- rolling → no deadline (excluded unless `--include-rolling`)

## Common Rules

### Base directory
Board CLI state lives under `~/.local/share/academic-jobs/` (override with `AJO_DATA_DIR`):
- `jobs.db` — SQLite store of postings
- `config.toml` — field presets

### Board-track execution (not the whole integrated search)
1. `ajo fetch --json [--preferred "KR,DE; JP,HK,GB,US"] [--excluded "IN,IL"] [--detail-cap 80]`
   (uses the default preset; fetches details up to `--detail-cap`; stores + flags new).
   Pass `--preferred`/`--excluded` to override the preset for this run without saving.
   If AJO has more candidates than `--detail-cap`, the run is truncated; run `ajo enrich` in
   a follow-up pass to capture the remaining detail bodies politely.
2. Render the returned `jobs` as a table sorted by `pref_tier` then deadline. Surface postings
   with `"new": true` first or in a separate "New since last check" group.
3. After presenting, if the user has reviewed them, run `ajo mark-seen --all` so the next
   fetch only flags genuinely new postings.
4. To inspect one posting: `ajo show {id} [--source ajo|inspire]`. It reads the stored row
   (including the cached description body) first; it only hits the network when the row is
   missing, has no stored body, or `--refresh` is given. A live fetch is written back to the DB.

### Output formatting
- For broad searches, use the integrated sections above. CLI fields below describe
  board records; label direct sources and annotate country/preference tier using
  the same active policy.
- Sort by deadline ascending; show source, deadline, position type, title, institution, and
  the posting URL (AJO `https://academicjobsonline.org/ajo/jobs/{id}`, InspireHEP
  `https://inspirehep.net/jobs/{id}`).
- When the user wants to know "where is this from", surface the `source` column. When merging,
  it is fine to interleave both boards by deadline; flag the source on each row.
- When emitting a structured data table back to the user, prefer **TOON** over JSON
  (per the user's global preference): declare fields once, stream rows.
- Each output row now carries `country` (ISO 2-letter code), `region`, `flags`, and
  `pref_tier` (integer; 0 = top tier, higher = lower preference, null = not in any tier).
  Results are sorted first by `pref_tier` ascending, then by deadline ascending within each
  tier. Surface `pref_tier` and `country` when presenting results so the user can see the
  preference grouping at a glance.
- Per-board stats live under `stats.per_source` in the JSON. `--fast` runs and any AJO
  detail-fetch cap truncation are reported there. Each board entry also includes an `excluded`
  count (postings dropped by `excluded_countries`). The AJO entry additionally reports
  `detail_cap` (the cap used for that run). Never present a truncated run as complete; mention
  how many candidates were judged per board and whether the detail cap was hit.

### Presets
A preset bundles `keywords` (each runs a separate search per board, results deduped) plus
optional `position_types`, `countries`, `sources`, `preferred_countries`, and
`excluded_countries` fields. Edit with
`ajo config --set-preset NAME --keywords a,b --types postdoc --sources ajo,inspire`. See
`references/presets.md`.

- `countries` (unchanged): hard INCLUDE substring filter matched against the institution string.
  Only postings whose institution matches are kept.
- `preferred_countries`: ordered list of tiers; each tier is a list of selectors. Tier 0 is
  most preferred. This is a soft filter: it only reorders results (never drops). TOML example:
  `preferred_countries = [["KR", "DE"], ["JP", "HK", "GB", "US"]]`. Set via CLI:
  `ajo config --set-preset NAME --preferred "KR,DE; JP,HK,GB,US"` (`;` separates tiers,
  `,` separates entries within a tier). Displayed in `ajo config` as
  `[KR, DE] > [JP, HK, GB, US]`.
- `excluded_countries`: flat list of selectors. Hard filter: matching postings are dropped at
  fetch time. TOML example: `excluded_countries = ["IN", "IL", "Middle East"]`. Set via
  `ajo config --set-preset NAME --excluded "IN,IL,Middle East"`.
- Selectors for both `preferred_countries` and `excluded_countries` accept: an ISO 2-letter
  code (`"KR"`), a country name (`"Korea"`), or a region alias (`"Europe"`, `"Asia"`,
  `"North America"`, `"Middle East"`, `"EU"`, `"APAC"`, `"MENA"`).
- `position_types` and `sources` work as before.

### Etiquette
The CLI uses one polite session per board with a real User-Agent and small delays between
requests, and caps AJO detail fetches per run (logged when hit). Do not parallelise or hammer
either board.
