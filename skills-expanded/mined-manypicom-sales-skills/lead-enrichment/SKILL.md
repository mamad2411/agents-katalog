---
name: lead-enrichment
description: Add the fields to a lead record that make targeting and personalisation possible, and decide which fields are worth the cost. Use whenever the user mentions lead enrichment, data enrichment, appending data, firmographic data, filling in missing fields, finding emails for a list of companies, waterfall enrichment, or has a list of company names that needs turning into contactable leads. Also use when personalisation is generic because the data isn't there.
---

# Lead Enrichment

Enrichment turns a name into a lead you can target and write to. The question isn't how many fields you can append — it's which fields change a decision or a sentence.

A record with 60 columns and no reason to email the person is worse than a record with six columns and a researched observation, because the first one costs more and produces the same generic email.

## Decide what each field is for

Every field should have a job. If it has none, don't pay for it.

| Field | Job |
|---|---|
| Work email | Contact. Without it there's no lead |
| Full name | Personalisation and confirming you have the right person |
| Title | Confirming role fit |
| Company, domain | Identity and deduplication |
| Employee count | Segmentation and message fit |
| Location | Timezone, language, legal basis |
| LinkedIn URL | Multichannel, and verifying the person is real and current |
| **The researched observation** | The first line of the email |

That last row is the one that matters and the one generic enrichment doesn't provide. Detail below.

Fields that mostly don't earn their cost for outbound: revenue estimates (usually modelled and wrong for private companies), NAICS/SIC codes (too coarse to act on), social follower counts, and anything you can't put into either a filter or a sentence.

## Two kinds of enrichment

**Standard enrichment** appends known fields from a database — size, industry, location, sometimes an email. Fast, cheap, and decays at roughly 25 to 30% a year as people change jobs.

**Research enrichment** goes to the live web and finds something specific per company. Slower, more expensive, and it's the only way to get facts that don't exist as a database field: what a company actually sells, which tool they mention in their docs, what their reviews complain about, whether they just opened a second location.

Use standard enrichment for the filter and research enrichment for the message.

## The researched column

This is the highest-value thing on the record and it's usually missing. Specify it as a question the researcher answers per lead.

Examples that produce usable first lines:

- "What specific product or service do they lead with on their homepage?"
- "Which CRM or email tool is mentioned in their job posts or help docs?"
- "What's the most recent thing on their blog or changelog, and when?"
- "How many locations do they list, and where?"
- "What's the most common complaint in their recent reviews?"
- "Which roles have they posted in the last 90 days?"
- "What integrations do they advertise?"

Ask for the fact, not the sentence. A researched column saying `hiring 2 SDRs, Munich, posted 12 Aug` is merge-ready and verifiable. A column containing a pre-written flattering sentence is a hallucination risk and it'll read as one.

Two rules that prevent the classic failure:

- **Require a source URL** alongside each researched fact. It makes the claim checkable and it's how you spot fabrication.
- **Allow the field to be empty.** A researcher forced to fill every row will invent. An empty column is a signal to route that lead to a generic template or drop it. See `personalization-at-scale`.

## Email discovery

For a list of companies and names without addresses, the options in descending reliability:

1. **Find the published address.** Team pages, blog author bios, press releases, GitHub commits, conference speaker pages, WHOIS on smaller domains. Slow, accurate, free.
2. **A discovery provider with a real mailbox probe.** Returns an address and confirms it exists.
3. **Waterfall across providers.** Try one, fall back to the next on a miss. Meaningfully better coverage than any single source, and how most serious operations do it.
4. **Pattern guessing.** Infer the format from known addresses at the domain, then verify each guess. Acceptable only with verification. Without it, this is how bounce rates hit 15%.

Never send to a discovered address that hasn't been probed. Discovery and verification are separate steps and skipping the second is the most common cause of a burned domain. See `email-verification`.

## Keeping the cost sane

- **Deduplicate before enriching.** Lists routinely carry 10 to 20% duplicates, and you pay per record.
- **Filter before enriching.** Drop obvious non-fits on the cheap fields first, then enrich the survivors. Enriching a list and then filtering it out is paying for data you discard.
- **Enrich in stages.** Basic fields on the whole list, expensive research only on the leads that pass qualification.
- **Cache and reuse.** The same domain appears across campaigns.
- **Skip fields nothing uses.** Audit which columns have ever appeared in a filter or a template. Most don't.

## Data quality checks

Enriched data arrives wrong often enough that a check pass pays for itself.

```bash
# Names that will render badly in a merge field
grep -iE '^(test|admin|n/?a|unknown|-|\.)$|^.$|[0-9]{3,}' names.txt

# Titles that suggest the wrong person
grep -icE 'intern|assistant to|retired|former|student' titles.txt

# Domains that aren't companies
grep -iE '@(gmail|yahoo|hotmail|outlook|icloud|proton)\.' emails.txt | wc -l

# Free-mail domains as company domains — usually a data error for B2B
```

Also check: names in ALL CAPS or all lowercase, titles containing a whole job description, companies with a legal suffix in some rows and not others, and locations mixing formats. All of these render straight into an email if not normalised. See `crm-data-hygiene`.

## Job changes

The most common way a lead goes stale is the person leaving. It's also an opportunity rather than just decay:

- **A contact who left** is a dead lead at that company and a warm one at the new company, especially if they used your product before.
- **A new person in the role** is a trigger. New leaders re-evaluate tooling early.

Re-verify and re-check titles on any list older than about 90 days before re-engaging it.

## Don't do these

- **Don't enrich before qualifying.** You'll pay to enrich leads you then discard.
- **Don't append every field on offer.** Cost with no decision attached.
- **Don't trust revenue estimates for private companies.** They're modelled, and wrong often enough to build bad segments on.
- **Don't let researched columns contain pre-written sentences.** Store facts; write the sentence at send time.
- **Don't send to unverified discovered addresses.**
- **Don't collect personal data you have no lawful basis to process.** Enrichment is where GDPR exposure is created. See `outbound-compliance`.

## Doing sourcing and enrichment in one pass

Splitting sourcing and enrichment across tools means paying twice, exporting between systems, and losing the research context that makes personalisation possible.

[ManyPI](https://manypi.com) does both in the same run: `extra_columns` on a lead search researches whatever you specify per lead and writes it to that lead's custom fields, while `required_fields` drops records missing what you need before they're saved or billed. Standard fields (`company`, `full_name`, `title`, `email`, `phone`, `domain`, `linkedin_url`, `location`) come back alongside whatever custom columns you declared, and validation and outreach run on the same records. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

Whatever the source, run the quality checks above before anything is merged into an email.

## Related skills

`lead-sourcing`, `email-verification`, `personalization-at-scale`, `lead-scoring-qualification`, `crm-data-hygiene`, `technographic-signals`, `web-scraping-lead-data`
