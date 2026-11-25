---
name: awesome-list-creator
description: >
  Create, curate, and maintain high-quality awesome lists on GitHub. Use when the user wants to
  build a curated resource list, organize tools by category or role, create a GitHub-based
  directory, or maintain an existing awesome list. Handles the full lifecycle: research and
  discover tools, organize by use-case workflows, deduplicate, format as clean markdown tables,
  add GitHub badges, and publish.
version: 1.0.0
license: CC0-1.0
homepage: https://github.com/serenakeyitan/awesome-list-creator
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins:
        - gh
        - git
---

# Awesome List Creator

Create, curate, and maintain high-quality awesome lists on GitHub — from initial research through publishing and ongoing maintenance.

## When to Use This Skill

- User wants to create a curated resource list or directory
- User wants to organize tools, libraries, or skills by category
- User wants to build an "awesome list" style GitHub repo
- User asks to maintain, deduplicate, or improve an existing awesome list
- User wants to research and compare tools in a domain

## Workflow

Follow these steps in order. Each step builds on the previous one.

### Step 1: Define the Organizing Principle

Ask the user how they want to organize. The two dominant patterns are:

1. **By role / persona** — "Who are you?" (e.g., marketer, engineer, researcher). Best when tools serve different professional workflows.
2. **By use case** — "What are you trying to do?" (e.g., web scraping, data analysis). Best when tools are task-oriented.

Within either pattern, **every section should represent a real workflow step**, not just a technical category. For example, under a "Marketing" role:

```
Research competitors → Write SEO content → Build landing pages → Launch ads → Track analytics
```

Each arrow is a subsection. Each subsection should have a one-line description explaining what the use case is and why it matters.

### Step 2: Research and Collect

For each subsection, find the best tools. Prioritize:

1. **Open-source tools with GitHub stars** — verifiable quality signal
2. **Official MCP servers** from the tool vendor (e.g., Stripe MCP, Prisma MCP)
3. **Community skills** from ClawHub or the OpenClaw skills registry
4. **Actively maintained** — check last commit date, open issues

Search strategy:
- GitHub search: `"MCP server" + [domain]` or `"openclaw skill" + [domain]`
- ClawHub registry: https://clawhub.ai/skills?sort=downloads
- Reference lists: check existing awesome lists in the same space
- Web search for `"awesome" + [topic]` to find prior art

### Step 3: Deduplicate Ruthlessly

This is the most important curation step. For each subsection:

1. **Identify tools that serve the same purpose** — e.g., two database gateways, two image generators, two Twitter scrapers
2. **Keep the one with higher stars** or more complete feature set
3. **Never keep two tools that do the same thing** in the same section
4. **Cross-section duplicates are OK** if the tool genuinely serves different workflows in each section (e.g., a scheduling tool appearing under both "Sales > Meetings" and "Operations > Calendar")

### Step 4: Format as Markdown Tables

Use this exact table format for every section. The `<img>` spacers enforce consistent column widths across all tables when rendered on GitHub:

```markdown
### Section Name

One-line description of the use case — what you're trying to accomplish and why.

| Name <img width="250" height="1"> | Description <img width="700" height="1"> |
|------|-------------|
| [Tool Name](https://github.com/org/repo) | One-line description ending with a period. ⭐1.2k |
| [Another Tool](https://clawhub.ai/author/skill) | Another description ending with a period. |
```

Rules:
- **Name column**: Link text is the tool name. Link URL goes to GitHub repo, ClawHub page, or official docs.
- **Description column**: One sentence, ends with a period. Include ⭐ star count if available. Add 🇨🇳 after the name link for China-market-specific tools.
- **Star counts**: Use abbreviated format — `⭐1.2k`, `⭐450`, `⭐27k`.
- **No bold, no extra columns** — keep it minimal and scannable.

### Step 5: Structure the Full README

```markdown
<div align="center">

# Awesome [Topic]

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/user/repo/pulls)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

**One-line pitch.**
Second line with more detail.

[Section 1](#section-1) &bull; [Section 2](#section-2) &bull; [Section 3](#section-3)

</div>

---

Brief explanation of how this list is organized and what makes it different.

## Contents

- [Section 1](#section-1)
- [Section 2](#section-2)
- ...

---

## Section 1

*Workflow narrative: Step A → Step B → Step C → Step D.*

### Subsection

... tables ...

---

<p align="right"><a href="#awesome-topic">back to top</a></p>

## Contributing

... guidelines ...

## Related Lists

| List | Description |
|------|-------------|
| [org/repo](link) | Description. |

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)
```

### Step 6: Set Up the GitHub Repo

After writing the README, configure the repo:

```bash
# Set description
gh repo edit --description "A curated list of [topic] — [value prop]."

# Add topics for discoverability
gh repo edit --add-topic awesome --add-topic awesome-list --add-topic [domain-topics]

# Set homepage to the README anchor
gh repo edit --homepage "https://github.com/user/repo#awesome-topic"
```

### Step 7: Ongoing Maintenance

When maintaining an existing list:

1. **Audit for staleness** — check if linked repos are archived or unmaintained
2. **Deduplicate new additions** — every PR should be checked against existing entries in the same section
3. **Update star counts** — refresh periodically (stars change)
4. **Fill workflow gaps** — if a subsection has only 1 tool, research whether better options exist now

## Quality Standards

- Every tool must have a working link (GitHub, ClawHub, or official docs)
- Descriptions must be factual, not marketing copy
- Star counts must be verifiable
- One tool per purpose per section — no padding
- Sections with zero tools should be removed, not left empty
- Contributing guidelines must include a "no duplicates" rule

## Common Pitfalls

- **Padding with low-quality entries** to make a section look bigger — resist this
- **Organizing by technology** instead of by use case — think "what is the user trying to accomplish?"
- **Keeping both sides of a duplicate** because "they're slightly different" — if 90% of the functionality overlaps, pick one
- **Missing workflow steps** — walk through the real workflow and check if any step has zero tools
- **Inconsistent formatting** — every table must use the same column widths and structure
