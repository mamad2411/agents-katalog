---
name: job-posting-signals
description: Use hiring activity as a buying signal — find companies whose job posts reveal budget, priorities, tech stack and pain. Use whenever the user mentions job postings, hiring signals, job boards, careers pages, recruitment data as intent, or wants to find companies that are growing or building a specific function. Also use when looking for timely triggers to open a cold email with.
---

# Job Posting Signals

A job post is a company publicly committing budget to a problem. It's dated, specific, written by someone inside the company, and free to read. For outbound it's one of the highest-quality signals available and it's under-used because it takes slightly more work than filtering a database.

Three distinct things a job post tells you, and most people only use the first.

## 1. They're building the function you serve

The obvious use. If you sell to sales teams and a company posts two SDR roles, they're investing in outbound and will need tooling around it.

Map your product to the roles that imply it:

| You sell | They're hiring |
|---|---|
| Outbound tooling | SDR, BDR, Head of Sales, RevOps |
| Analytics | Data analyst, BI, first data hire |
| Support software | Support lead, CX manager, first support hire |
| Recruiting tools | Recruiter, Head of Talent, TA coordinator |
| Marketing tooling | Growth, demand gen, content lead |
| Finance software | Controller, FP&A, first finance hire |
| Security | Security engineer, compliance, first DevSecOps |

**The first hire in a function is the strongest version.** A company hiring its first RevOps person has just decided the problem is real and has nobody with an entrenched tool preference. That's a much better prospect than a company with an established team on a competitor's platform.

## 2. The tech stack, stated openly

Job descriptions list required tools far more accurately than any technographic detection.

> "Experience with Salesforce, Outreach and Gong required. Familiarity with Clay a plus."

That's a complete stack disclosure. It tells you what they use, what they're adding, and what integrations matter. Detection tools infer from scripts on a website and are frequently wrong. A job post is the company telling you.

Search for competitor names in job posts to find their customers, and for complementary tools to find companies whose stack you fit into.

## 3. The pain, in their own words

The "responsibilities" and "what you'll be doing" sections describe problems the company has right now.

> "You'll own our outbound motion end to end — right now it's spreadsheets and a shared Gmail account, and we need someone to build a real process."

That's a specific, current, self-described pain, published voluntarily. It's better cold email material than anything you could infer, and it can be quoted almost directly.

## Finding the posts

**Company careers pages.** Most accurate and current, and the ones that never make it to the aggregators. Requires visiting each site, which is why it's under-used.

**Job boards and aggregators.** Broad coverage, searchable by keyword, location and date. Good for finding companies you didn't know about.

**LinkedIn Jobs.** Wide coverage, and the posting person is often visible, which sometimes gives you the hiring manager directly.

**Niche boards.** Industry-specific boards carry roles that never reach the big aggregators, and the companies posting there are more specific fits.

**Funding-adjacent hiring.** A company that raised recently and is now hiring across functions is the strongest combined signal there is. See `funding-news-signals`.

## Building the search

```
WHO           Companies hiring [roles] in [locations]
WINDOW        Posted in the last 30-90 days
SIZE          [employee range]
CAPTURE       role title, post date, location, tools named in the
              description, the sentence describing the current pain,
              source URL
EXCLUDE       Recruitment agencies posting on behalf of clients,
              job boards themselves, staffing firms
```

The exclusion matters more than it sounds. A large share of aggregator results are agencies reposting, and they're not the hiring company. Filter on whether the post is on the company's own domain, or check the poster.

**Capture the source URL.** You'll want to re-read the post when writing, and it's how you verify the fact is real.

## Recency

The signal decays fast.

| Age | Value |
|---|---|
| 0-14 days | Strongest. Actively hiring, budget just approved |
| 15-45 days | Good. Still open, still relevant |
| 46-90 days | Weakening. May be filled |
| 90+ days | Either filled or the post is stale. Don't reference it |

Referencing a role they filled two months ago makes you look like you're reading a stale list, which is exactly what you're trying not to look like. Re-check before sending if the list is older than a few weeks.

## Writing with it

The fact goes in the first line, and the connection sentence does the work.

> Saw you're hiring two SDRs in Munich — third sales role this quarter.
>
> The teams we work with usually hit the same wall right after that: reps in seat, no verified list to work, and week one goes on manual research.
>
> Worth 10 minutes before they start?

That works because the timing is genuinely relevant. The problem arrives when the reps do, and the email lands before it does rather than after.

What to avoid:

- **Don't congratulate them on growing.** It's filler and everyone does it.
- **Don't pitch recruitment services** unless that's what you sell. Every company hiring gets twenty of those a week and the annoyance is transferred to you.
- **Don't reference the post without connecting it** to why you're writing. A fact with no connection is worse than no fact.
- **Don't email the hiring manager about something unrelated** to the role. They're in hiring mode and will forward you to nobody.

## Who to contact

Usually not the person named in the post — they're often a recruiter and they're busy.

- The **hiring manager**, if identifiable from the post's reporting line
- The **function owner** the role reports into
- The **founder or department head** at smaller companies

The role being hired is the signal. The buyer is whoever owns the outcome that role serves.

## Don't do these

- **Don't treat any hiring as a signal.** A company hiring a warehouse operative isn't a signal for sales software. Match roles to your product precisely.
- **Don't include agency reposts.**
- **Don't use posts older than 90 days.**
- **Don't scrape sources that prohibit it** in their terms, or that require an account you'd be violating to use.
- **Don't build the whole programme on one signal.** Combine hiring with funding and stack signals for a much tighter list.

## Sourcing it

Job-signal lists go stale weekly, which means this is a recurring search rather than a one-off build, and that's where it usually gets abandoned.

[ManyPI](https://manypi.com) handles it as a lead search with the signal expressed in the brief — `keywords` for the roles and tools, `exclusions` for agencies, and `extra_columns` to capture the role title, post date, the tools named and the pain sentence with its source URL. Because the agent searches the live web rather than a static database, the recency is real. Re-running the search on a schedule keeps the list current. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

## Related skills

`lead-sourcing`, `funding-news-signals`, `technographic-signals`, `personalization-at-scale`, `icp-definition`, `lead-scoring-qualification`
