---
title: "Skill Gap Analysis and Learning Plans with /upskill"
sidebarTitle: "Upskill"
description: "Identify skill gaps against your tracked job postings. Get a prioritized heatmap and a learning plan with web-searched study resources and time estimates."
---

The `/upskill` command compares your candidate profile against the job postings you've been tracking and produces two outputs: a prioritized skill gap heatmap that shows which missing skills appear most frequently across your target roles, and a structured learning plan with concrete study resources, study directions tailored to your existing background, and realistic time-to-proficiency estimates. Resources are found via live web searches so they reflect current course offerings rather than stale recommendations. Use `/upskill` between application cycles for career planning, or immediately before a specific application to prepare for a role you know you want.

## Usage

```bash
/upskill
/upskill https://jobindex.dk/job/1234567
```

Invoking `/upskill` without arguments runs in **aggregate mode** over all jobs in your tracker. Passing a URL runs in **targeted mode** against that single posting.

## What You Get

Regardless of mode, `/upskill` produces a structured report saved to your `upskill/` folder:

**Gap Heatmap**

A prioritized table of every skill gap identified, labeled by priority (Critical / High / Medium / Low), skill type (Hard / Domain / Tooling / Soft / Credential), and the source of the gap — for example `4/5 jobs, score 3.2` in aggregate mode, or `required` / `preferred` in targeted mode. The heatmap is printed to the terminal as an intermediate output before the learning plan begins.

**Learning Plan**

For every Critical and High gap (and Medium gaps when the total gap count is small), the learning plan provides:
- **2–3 study resources** found via live web search — courses, documentation, or books — with a one-line rationale for each
- **A study direction** tailored to your background, specifying what to skip and where to start given what you already know
- **A time-to-proficiency estimate** (e.g. `~20h`, `~40h for a solid foundation`)

Resources are grouped by theme (Cloud & Infrastructure, MLOps, Domain Knowledge, etc.) rather than listed alphabetically. Every web search includes the current year to avoid stale results.

**Suggested Study Order**

A numbered sequence that respects dependencies (prerequisites come first), prioritizes Critical over High over Medium, and places domain knowledge last so it can be studied alongside practical projects.

## Broad vs. Targeted Analysis

`/upskill` operates in two distinct modes depending on how you invoke it:

**Aggregate mode** (`/upskill` with no argument) analyzes all jobs in `job_search_tracker.csv`. It builds a frequency-weighted skill gap map — skills that appear in more jobs, and in jobs where your fit rating was lower, score higher. This mode is suited to **career planning**: understanding what to build over the next few months to become more competitive across your target market.

**Targeted mode** (`/upskill <URL>`) fetches a single job posting and analyzes only that role's required and preferred skills. Required skill gaps are flagged as Critical or High; preferred gaps as Medium. This mode is suited to **focused interview prep**: knowing exactly what to brush up on before applying to or interviewing for a specific role.

## Output Location

Every report is saved as a Markdown file in the `upskill/` folder:

- **Aggregate reports:** `upskill/report-YYYY-MM-DD.md`
- **Targeted reports:** `upskill/report-YYYY-MM-DD-<company-slug>-<role-slug>.md` (e.g. `upskill/report-2026-04-20-guardsix-senior-ai-engineer.md`)

When you run aggregate mode again later, `/upskill` loads the most recent previous report and adds a **Since Last Report** diff section showing which gaps you've closed (skills added to your profile) and which new gaps have appeared from jobs tracked since then.

<Tip>
Use `/upskill` for career planning between applications, not just immediately before applying. Running it once a month gives you a rolling diff of where your profile is strengthening relative to your target market — and makes the learning plan easier to act on gradually rather than cramming before a deadline.
</Tip>
