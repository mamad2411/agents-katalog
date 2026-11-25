---
name: sylph-setup-skill
description: Set up a specific Sylph skill by auto-pulling examples from the web, deriving insights, and configuring the skill. Run as `/sylph-setup-skill <skill-name>`.
---

# Setup Skill

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Web Search | Find existing content, profiles, and examples |
| Web Fetch | Read blog posts, social profiles, published content |
| GitHub | Clone blog repos, read published articles |

## Core principle: ask less, derive more

**Ask the user as few things as possible.** For most channels, the agent can find existing content online (website, LinkedIn, blog, Twitter, Substack). Pull it, analyze it, derive insights and voice - then show the user for confirmation. Only ask when you genuinely can't find something.

## When to use

Run `/sylph-setup-skill <name>` after completing `/sylph-setup` (global setup). Run it once per channel or skill you want to activate.

## Usage

```
/sylph-setup-skill linkedin
/sylph-setup-skill blog
/sylph-setup-skill newsletter
/sylph-setup-skill outbound
/sylph-setup-skill crm
...
```

## How it works

1. Read the setup guide for the requested skill (from this folder)
2. Auto-discover and pull existing content from the web or connected repos
3. Copy the best examples to `_published/` and `_examples/`
4. Derive insights (voice, tone, format, what works) from the examples
5. Update the skill's SKILL.md with derived rules
6. Update the channel's `_insights.md` with derived patterns
7. Show the user for confirmation and corrections

---

## Available setup guides

Each guide is a markdown file in this folder:

| Skill | Guide | What it sets up |
|-------|-------|-----------------|
| LinkedIn | `setup-linkedin.md` | Post voice, format rules, _insights, _examples |
| Blog | `setup-blog.md` | Article structure, SEO patterns, _insights, _examples |
| Newsletter | `setup-newsletter.md` | Format, length, audience, _insights, _examples |
| Substack | `setup-substack.md` | Long-form voice, article structure, _insights |
| X / Twitter | `setup-x.md` | Tweet voice, thread format, _insights, _examples |
| Reddit | `setup-reddit.md` | Subreddit targets, tone, post types, _insights |
| Website | `setup-website.md` | Copy voice, page templates, update workflow |
| Email | `setup-email.md` | Email voice, opener/closer patterns, templates |
| Outbound | `setup-outbound.md` | Campaign structure, sequences, ICP targeting |
| CRM | `setup-crm.md` | CRM connection, pipeline stages, field mapping |
| Events | `setup-events.md` | Event types, templates, promotion workflow |
| Investor updates | `setup-investor-update.md` | Format, metrics, cadence |
| Brand | `setup-brand.md` | Visual identity, voice guide, asset templates |
| HR | `setup-hr.md` | Screening criteria, job templates, evaluation rubric |
| Slack community | `setup-slack-community.md` | Community tone, response patterns, channel rules |
| Customer report | `setup-customer-report.md` | 360 report template, data source mapping |
| Customer success | `setup-customer-success.md` | Follow-up cadence, CS backlog, templates |
| Zero inbox | `setup-zero-inbox.md` | Triage rules, routing logic, proxy senders |
| Create issue | `setup-create-issue.md` | GitHub issue conventions, labels, format |
| Contracts | `setup-contracts.md` | Legal details, contract templates, review rules |

---

## Dispatch logic

When the user runs `/sylph-setup-skill <name>`:

1. Map the name to the corresponding setup guide file:
   - `linkedin` -> read `setup-linkedin.md`
   - `blog` -> read `setup-blog.md`
   - `newsletter` -> read `setup-newsletter.md`
   - `substack` -> read `setup-substack.md`
   - `x` or `twitter` -> read `setup-x.md`
   - `reddit` -> read `setup-reddit.md`
   - `website` -> read `setup-website.md`
   - `email` -> read `setup-email.md`
   - `outbound` -> read `setup-outbound.md`
   - `crm` -> read `setup-crm.md`
   - `events` -> read `setup-events.md`
   - `investor-update` or `finance` -> read `setup-investor-update.md`
   - `brand` -> read `setup-brand.md`
   - `hr` or `screening` -> read `setup-hr.md`
   - `slack-community` or `slack` -> read `setup-slack-community.md`
   - `customer-report` -> read `setup-customer-report.md`
   - `customer-success` or `cs` -> read `setup-customer-success.md`
   - `zero-inbox` or `inbox` -> read `setup-zero-inbox.md`
   - `create-issue` or `issues` -> read `setup-create-issue.md`
   - `contracts` or `create-contract` or `review-contract` -> read `setup-contracts.md`

2. Follow the guide step by step
3. After setup, generate a test piece to verify quality

If the name doesn't match any guide, list available options and ask the user to pick one.

---

## Universal setup pattern

Every skill setup follows the same 4-step pattern:

### Step 1: Auto-discover existing content

Before asking the user anything, search for and pull her existing content:

- **LinkedIn**: search her company LinkedIn page, read recent posts
- **Blog**: ask for the repo URL or blog URL, clone/read articles, copy to `_published/`
- **Twitter/X**: search her company/personal handle, read recent tweets
- **Substack**: find her Substack, read recent articles
- **Newsletter**: ask for archive URL or pull from Substack/website
- **Website**: read key pages from the company website (already in CONTEXT.md)

For each piece found:
- Save to `<channel>/_published/YYYY-MM-DD_slug.md` with proper frontmatter
- Promote the 2-3 best to `<channel>/_examples/`

### Step 2: Derive insights automatically

From the collected content, analyze and write to `<channel>/_insights.md`:

- **Voice patterns**: sentence length, vocabulary, tone, favorite constructions
- **Format patterns**: what types of content she writes most, how she structures them
- **Topic patterns**: recurring themes, angles, positioning
- **What works**: engagement signals (likes, comments, shares if visible)
- **Cadence**: how often she publishes (derive from dates)

Show the insights to the user:

> Here's what I learned from your existing [channel] content. What would you change?

### Step 3: Configure the skill

Update the skill's SKILL.md with derived rules:
- Voice rules specific to this channel (from analyzed content)
- Format constraints (from patterns observed)
- Platform-specific rules (from what she actually does)

### Step 4: Test generation

Generate one piece of content using the newly configured skill. Ask the user to review. Capture any edits as the first learning cycle in `_insights.md`.
