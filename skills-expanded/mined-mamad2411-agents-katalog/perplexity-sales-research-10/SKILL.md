---
name: perplexity-sales-research-10
description: Ten copy-paste research prompts for sales prep (company overview, recent news and triggers, earnings insights, buyer pain points, competitive intel, stakeholder mapping, industry trends, tech stack discovery, buying signals, champion research) plus the three usage rules. Use before outreach, a discovery call or an account plan. Source SalesDaily.co "Perplexity for Sales Research" (Batch 102). The prompts work in any research-capable assistant; in Claude use WebSearch and cite sources.
---

# Perplexity for sales research - 10 prompts

Replace the {braces}. Quoted from the slide. Run one with `/sales-research <1-10> <details>`.

| # | Use case | Prompt | What you get |
|---|---|---|---|
| 1 | Company overview | Summarize what {company} does, who they serve, how they make money, and their 3 most recent strategic moves. Cite a source for each claim. | One-page brief with checkable sources |
| 2 | Recent news and triggers | List the 5 most important news items about {company} from the last 90 days. Focus on hiring, funding, product launches and leadership changes. Add dates and links. | Trigger events to open with |
| 3 | Earnings insights | Pull the 3 biggest themes from {company}'s latest earnings call. What did the CEO emphasize? What did analysts push on? Works for public companies. | Talking points their executives already care about |
| 4 | Buyer pain points | What are the top 5 business problems a {title} at a {size} {industry} company faces in 2026? Cite recent surveys, research and articles. | Pain points to lead with |
| 5 | Competitive intel | Compare {product} vs {competitor}. What do customers say in G2, Capterra and Reddit reviews? Where does each win and where does each lose? | Honest strengths and weaknesses of both sides |
| 6 | Stakeholder mapping | Who leads {function} at {company}? List names and roles found in press releases, news, conference talks and the company website, with links. | Org hints for multi-threading |
| 7 | Industry trends | What are the 3 biggest shifts in {industry} right now that a {role} would care about? Include data points and cite each one. | Insight hooks for warm openers |
| 8 | Tech stack discovery | What technology does {company} use, based on their job postings, case studies, integration pages and engineering blog? | Integration angles and tech-fit signals |
| 9 | Buying signals | Has {company} posted jobs in {function} in the last 60 days? Any RFPs, vendor announcements, partnerships or expansion news? | Hard signals that budget is moving |
| 10 | Champion research | Research {first name last name}, {title} at {company}: podcast appearances, conference talks, interviews and articles they wrote or were quoted in. | Personalization that does not feel creepy |

## The slide's three rules
- **Pick the mode.** Deep Research for #1, #3 and #5 (it reads hundreds of sources); normal search is enough for the rest.
- **Open the citations.** Click through before you use a number in an email.
- **Skip LinkedIn asks.** Profiles and posts sit behind a login, so ask for press, talks and podcasts instead.

## In this repo
`/sales-research` runs a prompt with web search and refuses to present an uncited claim. For named people (#6, #10) keep to public professional material; do not compile private details. Related: `perplexity-research-workflow`, `company-research`, `client-research-web`, `buying-signals` in `fable5-outbound-5-stage-map`.
