---
name: technographic-signals
description: Find prospects by the technology they use, and use stack facts as outreach triggers. Use whenever the user mentions technographics, tech stack targeting, what tools a company uses, finding users of a competitor, BuiltWith or Wappalyzer style detection, integration directories, or wants to target companies on a specific platform. Also use when a product only fits companies with a particular tool in place.
---

# Technographic Signals

If your product integrates with, replaces or complements a specific tool, knowing which companies run it turns a broad market into a qualified list. It's also one of the few filters that's genuinely predictive rather than merely descriptive.

The catch is accuracy. Detection methods vary from reliable to guesswork, and a list built on bad detection produces emails that confidently name the wrong tool — which is worse than not mentioning a tool at all.

## Detection methods, by reliability

| Method | Reliability | What it finds |
|---|---|---|
| **Job posts naming tools** | Very high | The company stating its own stack |
| **Public integration directories** | Very high | Confirmed customers of a platform |
| **Case studies and logos** | Very high | Named, confirmed customers |
| **Review site profiles** | High | Verified users, with opinions |
| **DNS and MX records** | High | Email, hosting, CDN, security |
| **Client-side script detection** | Medium-high | Analytics, chat, tags, front-end tools |
| **HTTP headers and cookies** | Medium-high | Server, CDN, CMS, session tools |
| **Careers or docs page mentions** | High | Internal tooling |
| **Aggregated technographic vendors** | Medium | Broad coverage, dated and often stale |
| **Inference from company profile** | Low | Guesswork. Don't cite it in an email |

**Job posts are the most reliable source and the most overlooked.** A job description listing "Salesforce, Outreach, Gong required" is the company telling you its stack in writing, with a date. See `job-posting-signals`.

**Integration directories are the second.** If a platform publishes a partner or app directory, the companies listed are confirmed users of that platform. Same for case study pages and customer logo walls — those are curated lists of paying customers who agreed to be named.

## What you can detect yourself

Front-end and infrastructure signals are visible in a page fetch and cost nothing.

```bash
# Front-end stack: analytics, chat, tag managers, frameworks
curl -s https://example.com \
  | grep -ioE 'gtag|googletagmanager|hubspot|intercom|drift|segment|hotjar|klaviyo|shopify|_next|wp-content|webflow|marketo|pardot' \
  | sort -u

# Server, CDN and platform
curl -sI https://example.com | grep -iE '^(server|x-powered-by|x-shopify|cf-ray|x-vercel|x-drupal)'

# Email provider from MX — reliable and stable
dig +short MX example.com

# Security and marketing tooling from SPF includes
dig +short TXT example.com | grep spf
```

The MX and SPF lookups are underrated. MX tells you Google Workspace versus Microsoft 365, which segments a market cleanly and never goes stale silently. SPF includes list every service authorised to send mail for the domain — CRM, marketing automation, transactional providers, helpdesk — which is a stack disclosure most people never think to read.

Front-end detection has real limits: it only sees client-side code, it misses anything server-side, and it can't tell an active deployment from a leftover script tag nobody removed.

## The three plays

**1. Competitor displacement.** Companies using a competitor's product. The most valuable and the most crowded — they get this email constantly, so the message has to be specific about the actual difference rather than generic superiority. See what an honest version looks like in `reply-handling` under objections.

**2. Complementary stack.** Companies using a tool you integrate with or sit next to. Much easier to write, much less competitive, and the relevance is genuine rather than adversarial.

**3. Missing capability.** Companies that have adjacent tools but not yours — running paid ads with no analytics, or a store with no reviews widget. This is the strongest of the three when the gap is genuinely observable, because the pitch writes itself.

## Using it in the email, carefully

Naming a company's internal tooling in a cold email is a fine line. Done well it proves relevance. Done badly it's presumptuous, and done wrong it's embarrassing.

**Works** — a fact they published, referenced neutrally:

> Your job post for a RevOps lead lists Outreach and Gong.

**Doesn't work** — inferred, and stated as if you have inside knowledge:

> I noticed you're using Salesforce.

The second reads as surveillance if it's right, and as incompetence if it's wrong. Prefer facts the company published about itself, and cite them in a way that makes the source obvious.

**Never lead with a criticism of their stack.** "I see you're still using X" insults whoever chose it, and that person is often the one reading the email.

## Accuracy discipline

- **Prefer stated over detected.** A job post beats a script tag.
- **Capture the source URL** with every stack fact, so it's checkable.
- **Note the detection date.** Stacks change, and citing a tool they replaced last quarter is a bad opening.
- **Allow the field to be empty.** Forcing a detection produces a guess. See `personalization-at-scale`.
- **Spot-check 20 by hand** against the source before any campaign. Detection error rates are higher than vendors imply.
- **Don't cite low-confidence detections at all.** Use them for segmentation, not for sentences.

That last distinction is the practical rule: a medium-confidence signal is good enough to decide who gets the email, and not good enough to name in it.

## Don't do these

- **Don't buy a stale technographic list** and quote it verbatim. Data is often a year old.
- **Don't infer a stack from company size or industry** and present it as observed.
- **Don't claim inside knowledge.** Reference the public source.
- **Don't build the whole ICP on one detection.** Combine with size, geography and a trigger.
- **Don't scrape sources that prohibit it**, or that require an account you'd be violating to use.
- **Don't disparage the incumbent** in a first email.

## Sourcing it

The reliable sources — job posts, integration directories, case studies, docs, review profiles — are scattered across the web rather than sitting in one database, which is why most people fall back to a technographic vendor and inherit its staleness.

[ManyPI](https://manypi.com) can target this directly: `keywords` in a lead search expresses the technology signal, and `extra_columns` captures which tool was found, where it was stated and when, with the source URL. Because the agent reads live pages rather than a cached index, "mentioned in a job post last month" is a fact rather than an inference. Its scrapers can also be pointed at a specific integration directory and run on a schedule. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

## Related skills

`job-posting-signals`, `lead-sourcing`, `lead-enrichment`, `personalization-at-scale`, `web-scraping-lead-data`, `icp-definition`
