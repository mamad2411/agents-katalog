---
name: employers
description: >-
  Adds or removes employers from the JobScan scanner's registry, updates the job titles it matches, and
  re-runs feed discovery so the change takes effect. Also grows the registry from a real search rather than
  from memory. Use when the user wants the scan to watch a new company or organization, stop watching one, or
  says "add employers to my job scan", "find employers for my job scan", "update my job titles", or "my scan
  is finding nothing".
---

# Employers and job titles

The scanner pulls open roles straight from employers' own job boards. Two files decide what it finds, and
both are meant to change often:

- **`<data_path>/ats/employers.json`** — who to watch.
- **`<data_path>/ats/triage-config.json`** — which job titles count, which are rejected outright, and the
  salary floor applied for free before anything is read.

A registry grows all year. **Someone remembering an employer eight months after setup is the normal case,
not an exception**, and it should cost them one sentence.

## Resolve first

Read `~/.claude/jobscan-data/jobscan-config.md` for `data_path`. Everything below is under
`<data_path>/ats/` — **never** inside the plugin, which `/plugin update` replaces wholesale. Scripts are at
`${CLAUDE_PLUGIN_ROOT}/scripts/`; if that variable is empty, derive the absolute path from where this
`SKILL.md` sits (the plugin root is two levels above `skills/employers/`).

Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/paths.mjs"` once if anything looks like it resolved oddly.

## Adding an employer

1. Ask only for the name. Never ask for a slug, an ATS, or a URL — that is what discovery is for.
2. Add it to `employers.json`. The quickest route is to pipe the name in and let the slug guessing happen
   for you, which also merges rather than overwrites:
   ```
   echo "Acme Group | industry" | node "${CLAUDE_PLUGIN_ROOT}/scripts/harvest-employers.mjs"
   ```
   Editing the file by hand is fine too — display name, a `sector` tag consistent with the ones already
   there, and **several candidate slugs** (`acme`, `acmeinc`, `acme-group`). Probing is free, so guess
   widely. If you already know the real slug, pass it as a third field: `Acme Group | industry | acmejobs`.
3. Re-run discovery:
   ```
   node "${CLAUDE_PLUGIN_ROOT}/scripts/discover-ats.mjs"
   node "${CLAUDE_PLUGIN_ROOT}/scripts/discover-workday.mjs"    # large employers only
   ```
   Both write `ats-feeds.json` into `<data_path>/ats/` themselves.
4. Verify and report: `node "${CLAUDE_PLUGIN_ROOT}/scripts/fetch-ats.mjs" --summary`. Say how many open
   roles that employer has right now — that is the number that tells the user it worked.

**If discovery finds nothing**, say so plainly rather than leaving them assuming it's registered. Most
misses are one of: the employer uses Workday (run `discover-workday.mjs`), the slug is spelled differently
(search `site:job-boards.greenhouse.io <employer>` or `site:jobs.lever.co <employer>` and try again), or they
genuinely run their own careers page with no public feed — in which case say the weekly web-search sweep will
have to cover them, and add them to `<data_path>/sources.md` so it does.

## Growing the registry from a search rather than from memory

"Find employers for my job scan", a registry under about a dozen, or a scan that keeps falling back to web
search: the fix is not to ask the user to remember more names. They already named everyone they could at
setup. The names they cannot supply are in the search results the scan is already paying for.

Run a sweep for their job titles across their sectors, collect the employer behind **every** posting that
matches — not only the ones worth applying to, because the point is next month's opening, not this one —
then:

```
node "${CLAUDE_PLUGIN_ROOT}/scripts/harvest-employers.mjs" --sector university < names.txt
node "${CLAUDE_PLUGIN_ROOT}/scripts/discover-ats.mjs"
node "${CLAUDE_PLUGIN_ROOT}/scripts/discover-workday.mjs"
```

`names.txt` is one employer per line, `Name | sector`, blank lines and `#` comments ignored. Harvesting
merges: existing employers keep their sector and their hand-corrected slugs, and gain only guesses they did
not already have, so running it twice is safe.

Report the pair of numbers that means something — how many names went in, how many came out with a live
feed — and what it changes: those boards are now pulled directly every week for nothing. `job-search` runs
this itself on a first scan; here it is on demand.

## Removing one

Drop it from `employers.json` and its entries from `ats-feeds.json`. Say what stops arriving. Removing an
employer does **not** un-see postings already screened out; that is the seen-URL cache's job and it is
correct.

## Changing job titles

`matchTitlePatterns` is the single most load-bearing setting in the pipeline: it is what makes a feed of
thousands into a shortlist. Patterns are case-insensitive JavaScript regex source strings.

- Take the titles in the user's own words, then write the pattern yourself:
  "grants manager" → `"\\bgrants?\\s+(manager|administrator|specialist)\\b"`.
- Keep `\\b` word boundaries — without them, `nurse` matches `nursery`.
- If the user is seeing junk, the fix is usually `excludeTitlePatterns`, not a narrower match pattern.
- If they are seeing nothing, check the shipped example patterns weren't left in place, and widen.

**Test before saying it's done:** `node "${CLAUDE_PLUGIN_ROOT}/scripts/test-triage.mjs"`, then a
`--summary` run, and report the match count. A pattern with a typo silently matches nothing, which looks
exactly like a quiet job market.

## Sanity check any time

`node "${CLAUDE_PLUGIN_ROOT}/scripts/doctor.mjs"` reports the registry size, the feed count and whether the
titles are still the shipped demo ones.
