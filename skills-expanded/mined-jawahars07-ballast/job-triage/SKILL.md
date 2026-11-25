---
name: job-triage
description: Turn a raw list of job postings into a short, honest short-list by screening the requirements block for hard gates before anything reaches the digest. Use when triaging scraped or pasted postings, refreshing a pipeline, or producing a daily job digest. Screens on stated requirements only, never on responsibilities.
---

# Job Triage

Raw postings in, a short-list of two or three worth real effort out — plus an auditable record
of what got screened out and why.

This skill does not scrape. Bring it postings from wherever you get them: an export, a board, a
pasted list, an ATS API. It does the judging.

## Load first

- `profile.yml` — target archetypes, exclusions, location rule, granted exceptions
- `applications.tsv` — so nothing already tracked resurfaces
- A dedup history file, if you keep one

## Steps

### 1. Coarse filter

Drop, before reading anything closely:

- Seniority mismatches. A search for apprentice roles should never surface "Senior Staff X"
- Excluded functions from `profile.yml`
- Locations outside the commutable zone, unless `profile.yml` grants that role an exception
- Anything already in `applications.tsv` at any status

If results look suspiciously global, your location filter has broken. Check it before blaming
the source.

### 2. The requirements-block screen

For each survivor, fetch the posting and read the **requirements block only**: "Requirements",
"Your profile", "Qualifications", "Profil recherché", "Type d'études", "À propos de toi".

Apply `jd-analyser`'s hard gates:

| Gate | Kill signal in the requirements block |
|---|---|
| Degree field | Names a field the candidate does not hold |
| Specialised school | Names a school type they are not in, as an exclusive |
| Stated language | "fluent French", "proficiency in X", "bilingual" above their level |
| Hard tool bar | A named tool listed as *required* with no evidence in `facts.md` |
| Portfolio requirement | A required portfolio, book, or prior placement in a craft the candidate has not done |
| Location | Outside the zone with no exception granted |

### The mission-block screen

Two things are **not** gates, because nothing is stated, and still make a role unbuildable. For
these, read the **missions** — and read them only as a description of the day job, never as an
inferred requirement.

| Screen | Kill signal in the MISSION block | Why |
|---|---|---|
| **Authorship as the deliverable** | "write articles, newsletters, white papers", "editorial content", "SEO copy", "press relations", "editorial calendar" | The job *is* producing polished copy in a language the candidate does not write at that level. No CV craft closes that |
| **Design tooling as the deliverable** | "infographics", "banners", "high-fidelity mockups", "design system", "visual identity", "video editing", "brand assets" | Check `facts.md` honestly. Product-side UX is not graphic design, and a tool listed as an aspiration is not a skill |

**This does not touch the stated-language rule.** Never infer a language bar from the fact that a
posting is written in a given language — that rule stands. This screen reads what the *work
produces*, which is a different question from what the employer *requires*. One posting stated no
language bar at all and was still unbuildable, because the deliverable was editorial copy.

Use this screen only where the mission block is unambiguous about the core deliverable. It is
deliberately narrow: two categories, both tied to something `facts.md` explicitly cannot claim.

**A gate or screen hit means the role does not enter the digest.** Log it under a `Screened out` section
with the one-line reason, so every decision the filter made stays auditable and the user can
overrule any of them.

**Read the requirements block, never the responsibilities.** Three roles in a row once had
responsibilities matching the candidate well and were each disqualified by a gate.
Responsibilities describe the job. Requirements decide whether you can hold it.

**Only the stated bar counts.** A posting written in French that names no French requirement
does not get a French gate. Never infer a language bar from the posting's language or the
company's country.

### 3. Rank the survivors

By archetype fit from `profile.yml`. Note contract length where the posting states it.

### 4. Write the digest

```markdown
# Today — YYYY-MM-DD

N new roles found. M survived screening.

## Worth evaluating
1. **Company** — Role
   url · source · duration · why it ranks

## Also live
...

## Screened out
- **Company** — Role — gate: stated language ("maîtrise du français")
```

Keep it scannable. Recommend **at most two or three** for full evaluation. Everything else stays
in the pipeline.

## Rules that exist because of real mistakes

- **Never present raw output as a short-list.** Unfiltered feeds surface senior roles for a
  junior search. Filter seniority before showing anything.
- **Never gate on contract duration.** A shorter-than-preferred contract is a flag and a
  demotion. It is the user's decision, not the filter's.
- **Never screen out on a soft preference.** Only the gates above kill a role. "Ideally",
  "a plus", "nice to have" are BONUS and stay in the digest.
- **Dedup against the tracker, not just the scan history.** A role already at Applied must never
  reappear.
- **Do not assume a scheduled scan ran.** Check the newest timestamp in your source before
  claiming the data is fresh. A silently broken scheduled job once made a stale pipeline look
  current for weeks.
