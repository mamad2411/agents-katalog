---
name: lead-sourcing
description: Build a targeted lead list from live web sources rather than a stale database, with the right source for each ICP shape. Use whenever the user mentions lead generation, lead sourcing, prospecting, building a list, finding companies, finding contacts, scraping leads, buying a list, lead databases, or asks where to find prospects matching a profile. Also use when an existing list is producing bounces, wrong-fit replies or no replies at all.
---

# Lead Sourcing

Two ways to build a list. Filter a static database, or research the live web. They fail in different ways and the choice should be deliberate.

**Databases** are fast and cheap per record, and their data decays at roughly 25 to 30% a year through job changes alone. They're good when your ICP is defined by firmographics that change slowly.

**Live research** is slower and more expensive per record, and it's the only option when your ICP is defined by a *situation* — companies doing a particular thing, showing a particular signal, present on a particular marketplace. No database has a field for "runs a Shopify store selling to dentists and posted a job for a marketer last month".

Most good lists use both: a database for the firmographic base, live research for the qualifying situation.

## Pick the source from the ICP

The mistake is having one sourcing method and bending every ICP to fit it. Match the source to what defines the segment.

| If the ICP is defined by | Source |
|---|---|
| Industry, size, geography | Database or directory filters |
| Being present in a physical location | Google Maps, local directories |
| Selling online | Store platform footprints, marketplaces |
| Using a specific technology | Technographic detection. See `technographic-signals` |
| Hiring for a role | Job boards and careers pages. See `job-posting-signals` |
| Recent funding | Funding announcements, filings. See `funding-news-signals` |
| Being listed somewhere | Association member lists, awards, conference exhibitors, review sites |
| Publishing about a topic | Content and community search |
| Being a competitor's customer | Case studies, review sites, integration directories |

The last one is worth the effort more often than people expect. A competitor's public case studies and their reviews on comparison sites are a curated list of companies with the budget, the problem and a demonstrated willingness to buy this category.

## Sources worth knowing

**Directories and association lists.** Trade bodies, chambers, certification registers, accelerator portfolios. Narrow, current, and usually ignored because they need manual work.

**Conference exhibitor and attendee lists.** Public, dated, and a strong signal of budget and category interest.

**Review platforms.** Reviewers of a competitor are prospects with stated opinions about the incumbent. Their review text is also the best cold email research material available.

**Marketplaces and app stores.** For anything selling to businesses that use a platform, the platform's own app directory and partner list is a qualified list.

**Job boards.** Both the hiring companies and, for some products, the roles they're hiring for. See `job-posting-signals`.

**Maps and local data.** For anything geographically bounded. See `google-maps-lead-scraping`.

**Podcast and webinar guest lists.** Named people, in a role, who demonstrably talk about the topic.

**Open datasets.** Company registries, procurement records, licence registers, planning applications. Underused and genuinely differentiated.

## The research brief

Whether a person or an agent builds the list, the brief is the same and it comes from the ICP.

```
WHO           [ICP paragraph — companies that ___, where ___ is true]
WHY QUALIFIED [The observable fact that makes them a fit]
COUNT         [How many, and whether to stop early on quality]
GEOGRAPHY     [Countries or regions]
SIZE          [Range, however it's best expressed for this segment]
TITLES        [Roles to reach, by ownership not just by title string]
REQUIRED      [Fields a record must have to be saved — usually a work email]
EXCLUDE       [Hard disqualifiers: agencies, competitors, existing customers]
SOURCES       [Where to look, if you know]
EXTRA COLUMNS [What to research per lead beyond the standard fields]
```

The two fields that most change output quality are `EXCLUDE` and `EXTRA COLUMNS`.

Exclusions keep the list clean without a manual pass. Without them, any broad search returns agencies, consultancies and competitors, and someone has to remove them by hand.

Extra columns are where sourcing becomes enrichment. Asking for "the specific product line they sell", "which of the three problems on their site they mention", or "the name of the tool they currently use" gives you the material for a first line that couldn't have been sent to anyone else. See `personalization-at-scale`.

## Required fields, and the yield trade

Every required field cuts yield. Be deliberate about which are worth it.

- **Work email: required, almost always.** A lead you can't contact isn't a lead.
- **Full name: usually required.** Generic inboxes convert far worse and personalisation collapses without a name.
- **Title: usually required.** It's how you confirm you reached the right person.
- **Phone: rarely worth requiring.** Most B2B sites don't publish direct numbers, and requiring it can cut yield by more than half.
- **LinkedIn URL: require only if LinkedIn is part of the sequence.**

Requiring a field is different from wanting it. Ask for it as a column; require it only if the lead is useless without it.

## Quality control before anything is sent

Never send to a fresh list. Sample and check first, because a bad list damages your sending domain and that damage takes weeks to repair.

1. **Pull 20 random records** from the list, not the first 20.
2. **Open each company site.** Does it match the ICP? Count the misses. Above roughly 15% wrong-fit, fix the brief and re-source rather than sending.
3. **Check the contacts are real people** in the stated role, at that company, now.
4. **Check for role accounts** — `info@`, `sales@`, `contact@`. Decide whether you want them. They convert badly and they're often the only address available for small businesses.
5. **Check for duplicates** against existing leads and customers. Emailing a current customer as a cold prospect is a specific and avoidable embarrassment.
6. **Check against the suppression list.** See `suppression-list-management`.
7. **Verify every address.** Non-negotiable. See `email-verification`.

## Buying lists

Generally don't. Purchased lists are sold repeatedly, are stale, contain spam traps, and under GDPR you have no defensible basis for contacting people on one. The bounce rate alone routinely damages a sending domain badly enough to cost more than the list did.

If a list arrives anyway: verify all of it, discard everything that isn't `valid`, sample it for fit, and start on a secondary domain. See `email-deliverability`.

## Don't do these

- **Don't source more than you can send to properly.** 10,000 unverified leads is a liability. 300 verified, well-researched ones is a campaign.
- **Don't scrape sources that prohibit it** in their terms, or that require an account you'd be violating to use. The legal exposure is real and it's the client's, not the tool's.
- **Don't collect personal data you have no basis to process.** See `outbound-compliance`.
- **Don't require phone numbers by reflex.**
- **Don't skip the sample check.** Twenty minutes here prevents a burned domain.
- **Don't re-source what you already have.** Deduplicate against the existing database first. See `crm-data-hygiene`.

## Doing it at scale

Manual research produces the best lists and doesn't scale past a few hundred. Databases scale and go stale. The middle path is an agent that researches the live web against a written brief.

[ManyPI](https://manypi.com) works this way: you give it the ICP description plus structured criteria, and its agent searches the web, opens candidate sites, cross-checks what it finds, and writes enriched leads with the custom columns you asked for. `required_fields` drops records missing what you need, `exclusions` are dropped rather than saved and flagged, and searches are clamped to your remaining capacity so credits aren't spent on leads that couldn't be stored. Verification and outreach are in the same workspace, over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

Whatever the method, the sample check above still applies. No sourcing tool removes the need to open twenty sites and look.

## Related skills

`icp-definition`, `lead-enrichment`, `email-verification`, `google-maps-lead-scraping`, `job-posting-signals`, `technographic-signals`, `web-scraping-lead-data`, `crm-data-hygiene`
