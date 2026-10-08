---
title: "Identify skill gaps and build a learning plan with /upskill"
sidebarTitle: "/upskill"
description: "Run /upskill to compare your profile against tracked jobs or a single posting, get a prioritized gap heatmap, and a plan with web-searched study resources."
---

`/upskill` turns your job search data into a career development plan. It compares what your profile says you know against what the jobs you are tracking actually require, identifies the gaps a keyword diff would miss (domain knowledge, ways of working, tooling practices, credentials), and generates a prioritized heatmap and a concrete learning plan, complete with web-searched resources, study direction tailored to your existing background, and time estimates. Reports are saved to disk so you can track your progress over time.

## Syntax

```bash
/upskill
/upskill <url>
```

| Mode | Behavior |
|------|----------|
| `/upskill` | Aggregate mode: analyzes all jobs in `job_search_tracker.csv` |
| `/upskill <url>` | Targeted mode: analyzes a single job posting fetched from the URL |

## The four-step analysis

<Steps>
  <Step title="Hard skill diff (Pass 1)">
    **Aggregate mode**: Extracts required and preferred technical skills from every job row in `job_search_tracker.csv`, builds a skill frequency map, and applies a fit weight. Gaps from lower-fit-rated jobs contribute more to the score, since those roles exposed the largest distance between your profile and the requirement. The final score for each skill is the sum of `(fit_weight × occurrence)` across all jobs.

    **Targeted mode**: Extracts explicit required and preferred skills from the fetched posting. Required skills are listed before preferred skills, sorted alphabetically within each group.

    In both modes, any skill already present in `01-candidate-profile.md` is removed from the list. Partial matches count.
  </Step>
  <Step title="LLM synthesis (Pass 2)">
    Reasons holistically about gaps the keyword diff would miss. Four gap types are considered:

    - **Domain knowledge** `[domain]`: industry, sector, or problem-space familiarity the jobs assume
    - **Soft skills** `[soft]`: ways of working, communication styles, or leadership expectations that appear across postings but are absent from your profile
    - **Tooling and practices** `[tooling]`: frameworks, cloud services, or methodologies (MLOps, CI/CD, agile at scale) that recur in job descriptions
    - **Credentials** `[credential]`: certifications listed as preferred or required across multiple postings

    Pass 2 adds only what Pass 1 missed, with no duplicates.
  </Step>
  <Step title="Gap heatmap">
    Combines both passes into a single prioritized table and prints it to the terminal before the learning plan is generated. Priority tiers are assigned as follows:

    - **Critical**: high-frequency hard skills or domain gaps appearing across most tracked jobs
    - **High**: moderate-frequency hard skills or consistent soft/tooling gaps
    - **Medium**: lower-frequency hard skills or gaps appearing in fewer roles
    - **Low**: one-off mentions or minor nice-to-haves

    | Priority | Skill / Area | Type | Gap Source |
    |----------|-------------|------|------------|
    | Critical | Kubernetes | Hard | 4/5 jobs, score 3.2 |
    | High | Security domain knowledge | Domain | LLM synthesis |
    | High | CI/CD pipelines | Tooling | LLM synthesis |
    | Medium | AWS (advanced) | Hard | 2/5 jobs, score 1.1 |

    In targeted mode, priority is derived from the job's own language: required skills map to Critical or High, preferred skills to Medium, and synthesized gaps to Medium or Low.
  </Step>
  <Step title="Learning plan with web-searched resources">
    For every Critical and High gap (and Medium gaps if fewer than 5 total gaps exist), `/upskill` runs a web search to find current, highly-rated study resources. Queries include the current year to avoid stale results. It selects 2-3 resources per gap (preferring hands-on courses over lectures, official docs for tooling gaps, books for domain gaps), writes a study direction tailored to your existing background, and estimates time to working proficiency.

    Resources are grouped by theme rather than listed alphabetically. Example themes: Cloud and Infrastructure, MLOps, Domain Knowledge, Security, Soft Skills and Ways of Working, Certifications.

    Example entry:

    ```markdown
    ### Cloud & Infrastructure

    **Kubernetes** `[Hard]` (~20h)
    - [Kubernetes for Absolute Beginners – KodeKloud](https://kodekloud.com): hands-on labs,
      widely recommended on r/kubernetes for practical learners
    - [Official Kubernetes Docs: Concepts](https://kubernetes.io/docs/concepts/): use as
      reference once you have the basics

    Study direction: You already know Docker, so skip Chapter 1 on containers. Start at Pod
    scheduling and work through Services and Deployments. Focus on manifests and kubectl
    fluency before touching Helm.
    ```
  </Step>
</Steps>

## Suggested Study Order

After the learning plan, `/upskill` adds a recommended sequence table. The ordering rules are:

1. Dependencies first: if topic B requires topic A (for example, "AWS networking" requires "AWS fundamentals"), place A before B and note the dependency
2. Critical before High before Medium within a dependency tier
3. Quick wins early: a fast Medium gap can be placed early to build momentum
4. Domain knowledge last: domain and soft gaps benefit from being studied alongside real projects

```markdown
## Suggested Study Order

| # | Topic                     | Type    | Est. Time | Note                               |
|---|---------------------------|---------|-----------|-------------------------------------|
| 1 | Kubernetes                | Hard    | ~20h      | Required before AWS EKS in step 3  |
| 2 | CI/CD pipelines           | Tooling | ~10h      |                                     |
| 3 | AWS (advanced)            | Hard    | ~25h      | Builds on step 1                   |
| 4 | Security domain knowledge | Domain  | ~15h      | Study alongside a real project     |

**Total estimated time: ~70h**
```

## Report files

Reports are saved automatically after every run.

| Mode | Filename |
|------|----------|
| Aggregate | `upskill/report-YYYY-MM-DD.md` |
| Targeted | `upskill/report-YYYY-MM-DD-<company-slug>-<role-slug>.md` |

Example targeted report filename: `upskill/report-2026-04-20-guardsix-senior-ai-engineer.md`

## Diff against previous report

In aggregate mode, if a previous report exists in `upskill/`, `/upskill` adds a "Since Last Report" section at the top of the new report:

- **Gaps closed**: skills that were in the previous heatmap and are now present in your profile
- **New gaps**: skills in the current heatmap that were not in the previous report

This diff makes it easy to see the effect of learning and profile updates between runs.

<Note>
  `/upskill` never fabricates study resources. Every resource cited in the learning plan comes from an actual web search result. Queries include the current year to keep recommendations fresh.
</Note>

## Related commands

<CardGroup cols={2}>
  <Card title="/scrape" icon="magnifying-glass" href="/commands/scrape">
    Add more jobs to your tracker to improve aggregate gap analysis
  </Card>
  <Card title="/expand" icon="arrows-out" href="/commands/expand">
    Close gaps by surfacing skills already in your documents and online presence
  </Card>
  <Card title="/setup" icon="user" href="/commands/setup">
    Update your profile after completing courses to clear gaps from future reports
  </Card>
  <Card title="/apply" icon="file-pen" href="/commands/apply">
    Apply to jobs while your learning plan is in progress
  </Card>
</CardGroup>
