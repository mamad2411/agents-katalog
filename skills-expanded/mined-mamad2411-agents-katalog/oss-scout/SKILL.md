---
name: oss-scout
description: >
  Find high-impact open source repositories worth contributing to — ranked by how
  much a merged PR would boost your resume, GitHub profile visibility, and recruiter
  reach. Use this skill whenever the user asks to discover repos for open source
  contribution, wants to find "something good to contribute to," asks what OSS
  projects would look impressive on a resume, wants trending or high-impact repos
  in a particular stack, or says anything about finding open source projects to
  work on — even if they don't use the word "scout." Also trigger when they ask
  vague questions like "what should I contribute to this week" or "find me
  something in AI/agents/backend/fullstack." This is the repo-level discovery
  skill; it does NOT handle issue triage or implementation within a chosen repo.
---

# OSS Scout — Repository Discovery for Career Impact

You help the user find open source repositories where a merged contribution would
produce meaningful career signal — recruiter-visible project names, active
communities that actually review PRs, and domains aligned with fullstack/backend/
AI/agents hiring markets.

## What This Skill Does (and Doesn't)

**Does:** Discover and rank repositories by career-impact potential. Output is a
scored list of repos with reasoning.

**Does NOT:** Find specific issues, triage bugs, do codebase recon, or help with
implementation. That's oss-contribute's job. Once the user picks a repo from your
list, hand off.

## Workflow

### Step 1: Clarify Filters (if needed)

If the user gave you a language, topic, or target company, use those as filters.
If they said nothing specific, default to a broad scan across fullstack/backend/
AI/agents ecosystems. Don't ask unnecessary questions — if the prompt is clear
enough to act on, act.

Possible filters to extract from the user's request:
- Language preference (Python, TypeScript, Go, Rust, etc.)
- Domain (AI agents, backend, databases, CLI tools, etc.)
- Target company (repos maintained by a specific employer)
- Recency preference ("trending this week" vs "established and active")

### Step 2: Discover Candidate Repos

Use the API commands and tools documented in `references/discovery-api-cookbook.md`.
Read that file now — it contains every gh CLI command, API endpoint, and third-party
tool you need.

**Discovery strategy (run in parallel where possible):**

1. **GitHub Search API** — Query for repos matching the user's filters with
   `good-first-issues:>3`, `stars:>500`, `pushed:>` (last 30 days). Sort by
   `help-wanted-issues` to find contributor-friendly projects.

2. **Trending scan** — Check OSS Insight rankings or github-trending-api for
   repos gaining stars rapidly (star velocity signal).

3. **Company-org search** — If the user targets specific employers, search within
   their GitHub orgs using the company→org mapping in the cookbook.

4. **Foundational infrastructure** — Check Libraries.io or ecosyste.ms for high-
   dependent-count projects (packages that thousands of other projects depend on
   — these are resume gold regardless of star count).

Aim for 15-25 candidates before scoring. More is fine, fewer is acceptable if
filters are narrow.

### Step 3: Score Candidates (Two-Pass)

Scoring uses two passes to balance speed with accuracy.

**Pass 1 — Fast filter (all candidates):**
Run `scripts/score-repo.sh` for every candidate repo. This uses cheap API calls
(repo metadata, star count, push date, GFI count, contributor stats) to produce
an approximate score. It intentionally approximates PR review turnaround, merge
rate, star velocity, and foundational-infra status from proxies rather than making
expensive GraphQL/Libraries.io queries for 20+ repos.

**Pass 2 — Deep scoring (top 5-10 only):**
Take the top 5-10 repos from Pass 1 and run the real queries documented in
`references/scoring-rubric.md` and `references/discovery-api-cookbook.md`:

1. **PR review turnaround** — GraphQL query on last 10 merged PRs (time from
   open to first review). See scoring-rubric.md "How to Compute" under
   Contributability.
2. **PR merge rate** — GraphQL: merged vs closed PRs ratio.
3. **Star velocity** — Binary search on stargazers endpoint (cookbook Section 5,
   Approach A) or OSS Insight API (Approach B). ~13 API calls per repo.
4. **Foundational-infra dependents count** — Libraries.io API:
   `curl "https://libraries.io/api/github/OWNER/REPO?api_key=$KEY"` →
   `.dependents_count`

These four queries replace the proxies from Pass 1 with real data before the
final ranking. If rate limits or missing API keys prevent a query, keep the
Pass 1 approximation and note it in the report.

**The formula:**

```
Total Score = Recognizability (35%) + Contributability (35%) + Role/Ecosystem Relevance (30%)
```

Each factor is 0-100, weighted to produce a 0-100 composite. Read
`references/scoring-rubric.md` for the full rubric with metric tables and
thresholds.

### Step 4: AI Policy Flag

For each repo in your final ranked list, cross-reference against known AI-ban
projects:

**Known bans (do not silently exclude — FLAG with a warning):**
- Any repo under `gentoo` org
- `curl/curl` and related Daniel Stenberg projects
- Any repo whose CONTRIBUTING.md contains "forbidden.*ai" or "prohibited.*ai"

**Known disclosure requirements (flag as informational):**
- Linux kernel (`torvalds/linux`) — requires `Assisted-by:` tag
- Apache Foundation projects — recommends `Generated-by:` tag

If you spot a ban or disclosure requirement, include a `[AI-RESTRICTED]` or
`[DISCLOSURE REQUIRED]` flag in the output. Don't remove the repo from the list
— the user might still want to contribute manually.

### Step 5: Produce the Scout Report

Load `assets/scout-report-template.md` and fill it in. Output the top 5-10 repos
ranked by total score, with per-factor breakdowns and reasoning.

Key output requirements:
- Each entry gets its three sub-scores visible
- "Why it scored well" must tie to specific numeric factors, not vague praise
- "Market context" must say who uses this project and why it's relevant to hiring
- Flag any AI-policy restrictions

## When to Use Specific References

| Step | File to Read | Why |
|------|-------------|-----|
| Step 2 | `references/discovery-api-cookbook.md` | All API commands, gh CLI syntax, company-org table |
| Step 3 | `references/scoring-rubric.md` | Metric thresholds, weight breakdowns |
| Step 3 | `scripts/score-repo.sh` | Run for each candidate |
| Step 5 | `assets/scout-report-template.md` | Output format |
