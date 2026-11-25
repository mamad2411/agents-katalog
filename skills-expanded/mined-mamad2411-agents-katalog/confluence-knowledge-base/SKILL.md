---
name: confluence-knowledge-base
description: Guide for creating and maintaining a product-specific Confluence knowledge base where all teams share understanding of the product, features, decisions, and customer insights in plain language. ALWAYS use this skill when the user requests ANY Confluence operation—creating pages, documenting features, setting up structures, managing business rules, or updating content. Use for both single pages and full space architecture. The knowledge base is product-focused, may contain product-related business rules, and should be accessible to design, engineering, sales, and support teams.
version: 1.0.1
license: MIT
---

# Confluence Knowledge Base

Use this skill to design, create, update, and govern a product-focused Confluence knowledge base that is understandable across design, engineering, sales, and support.

## Goal

Build and maintain a single source of truth for product features, customer insights, product decisions, and product-specific business rules in plain language.

## When To Use

Use this skill whenever the user requests any Confluence work, including:

- Creating pages or full Confluence space structures
- Documenting product features and behavior
- Recording product decisions and rationale
- Managing product-specific business rules (pricing, access, constraints)
- Capturing customer insights and use cases
- Improving discoverability, consistency, and governance of product documentation

## MCP Default Requirement

- Use `atlassian-rovo-mcp` as the default integration path for Confluence operations in this skill.
- Before falling back to generic guidance, check whether the MCP is available in the current environment.
- If MCP tools are unavailable or not configured, explicitly ask the user to set up the MCP first.
- Share setup links when asking the user to configure it:
 - Before falling back to generic guidance, check whether the MCP is available in the current environment.
 - If MCP tools are unavailable or not configured, explicitly ask the user to set up the MCP first.
 - If the environment does not have the MCP installed, recommend installing the `install-atlassian-rovo-mcp` skill and provide the install command the user can run:
    ```
    npx skills add https://github.com/bondansebastian/agent-skills --skill install-atlassian-rovo-mcp
    ```
 - Share setup links when asking the user to configure it:
   - Atlassian Forge MCP and Rovo Dev CLI docs: https://developer.atlassian.com/platform/forge/forge-mcp/#rovo-dev-cli
   - GitHub search results for `atlassian-rovo-mcp`: https://github.com/search?q=atlassian-rovo-mcp&type=repositories
- If the user cannot set up MCP immediately, continue with manual Confluence planning/content drafting and clearly mark it as a temporary fallback.

## Core Principles

- Write for a broad audience; avoid jargon or explain it in a glossary.
- Keep content product-focused (what and why), not implementation-focused (how code is built).
- Prefer linking over duplication; maintain one source of truth.
- Keep navigation shallow (3-4 levels max).
- Every page has an owner and a visible last review date.
- Archive outdated content instead of deleting it.

## Space Skeleton

Use this as the default space blueprint:

```text
[Product Name] Knowledge Base/
|- Home (quick links, upcoming reviews, key contacts)
|- Product Overview/
|  |- What We Built & Why
|  |- Key Terminology (Glossary)
|  |- Customer Problems Solved
|  `- Success Metrics
|- Features/
|  `- [Feature Name]/
|     |- What It Is & Why We Built It
|     |- Customer Problem Solved
|     |- How It Works (overview for all roles)
|     |- Key Product Rules
|     |- Design & User Experience
|     |- Launch Plan & Timeline
|     `- Decisions Made & Alternatives Considered
|- Product Rules & Constraints/
|  |- Rules Index
|  |- Pricing & Access Rules
|  |- Feature Limitations & Why
|  `- Edge Cases
|- Customer Knowledge/
|  |- Use Cases & Success Stories
|  |- Customer Feedback & Insights
|  `- Common Questions & Issues
|- Releases & Updates/
|  |- Communication Guidelines
|  |- Escalation Procedures
|  `- Incident & Issue Resolution
`- Releases & Announcements/
   |- Latest Updates
   `- [Release Name] Information
```

## Required Practices

### 1) Product Rules Index

- Maintain a master table with: Rule, Why It Exists, Affected Feature, Priority, Owner, Last Reviewed.
- Use plain language, not technical internals.
- Link each rule to features that enforce or depend on it.
- Focus on product behavior and constraints.

### 2) Feature Page Template

Apply this structure for every feature page:

- Status badge at top (Draft / Approved / Active / Retired)
- Required page owner
- 2-3 sentence summary: what it is and why it was built
- Customer problem solved
- How it works (visual and plain language)
- Product rules and constraints
- Design and UX assets (Figma/screenshots)
- Launch timeline and rollout plan
- Decision log with alternatives considered
- Last reviewed and next review dates

### 3) Organization & Navigation

- Keep hierarchy shallow (3-4 levels maximum).
- Use consistent naming conventions.
- Keep internal process docs out of this space unless directly product-related.
- Create index pages for high-traffic sections.

### 4) Linking & Cross-References

- Link related features instead of duplicating text.
- Link customer problems to the features that solve them.
- Link product rules to affected features.
- Embed visuals directly (Figma, mockups, diagrams).

### 5) Governance & Maintenance

- Assign exactly one owner per page.
- Schedule quarterly reviews.
- Show Last Reviewed prominently on each page.
- Mark stale pages as Archived; preserve history.
- Keep language clear and accessible to non-engineering audiences.

## Confluence Formatting Conventions

- Use Confluence Status macros for lifecycle state (Draft / Active / Archived).
- Use icons or emojis to improve scanability where helpful.
- Add labels to pages (for example: sales, feature, archived, needs-review).
- Keep layout and section order consistent across similar page types.
- Prefer visual artifacts (flowcharts, screenshots, mockups) over long prose.

## Feature Page Template

Page title:

`[Feature Name] - Short description`

Quick info box at top:

- Status: Active / Draft / Planned / Retired
- Owner: Name or team
- Last Reviewed: YYYY-MM-DD
- Next Review: YYYY-MM-DD

Main sections:

1. **What & Why**
- What is this feature?
- What customer problem does it solve?
- Why is it valuable to customers?

2. **How It Works**
- Explain in simple terms how users interact with it.
- Include visuals (screenshots, mockups, flowcharts).
- Avoid internal implementation detail.

3. **Product Rules & Constraints**
- Rules that apply to this feature
- Limitations or restrictions and why they exist
- Access or availability constraints

4. **Design & User Experience**
- Embed Figma mockups or screenshots
- Show key workflows visually

5. **Launch & Timeline**
- Launch date or plan
- Phased rollout details
- Customer communication approach

6. **Decisions & Alternatives**
- Key choices
- Alternatives considered and rejected
- Decision makers and dates

7. **Related Information**
- Links to customer use cases and success stories
- Links to related features
- Links to product rules that affect the feature

## Product Rules Index Example

| Rule | Plain Language Explanation | Why It Exists | Affects Which Feature(s) | Priority | Owner | Last Reviewed |
|---|---|---|---|---|---|---|
| PR-001 | Users can only have one active account at a time | Fraud prevention and data integrity | Account Management | High | Product Team | 2026-01-15 |
| PR-002 | Free users see ads; paid users do not | Revenue model and user experience differentiation | Subscriptions | High | Product Team | 2026-02-01 |

## Page Health Checklist

Before publishing or after quarterly review, verify:

- Page has a clear owner.
- Last Reviewed is recent (within 90 days).
- Status is set (Active / Draft / Archived).
- Content is understandable to non-specialists.
- Key visuals are present.
- Related pages are linked.
- Decision rationale is documented.

## Common Pitfalls And Fixes

| Problem | Solution |
|---|---|
| Information duplicated across pages | Create one source-of-truth page and link to it |
| Nobody updates the knowledge base | Assign owners and tie updates to quarterly reviews |
| Pages are too technical | Rewrite for general audience and add glossary terms |
| Deep page nesting makes navigation hard | Flatten to 3-4 levels and improve top-level indexes |
| Decisions buried in chat/email | Require that decisions and rationale live in Confluence |
| Inconsistent page formatting | Enforce shared templates and section order |
| Pages become stale | Make owner accountable for recurring review and status updates |

## Agent Execution Guidance

On any Confluence request:

- Apply this skill's structure, tone, and governance rules.
- Use the Feature Page Template for feature pages.
- Update the Rules Index when rules are added or changed.
- Emphasize why decisions were made and what alternatives were rejected.
- Ensure all output is understandable outside engineering.

## Examples

Example product rule:

- Rule: Free users can only have 3 saved items; paid users have unlimited
- Why: Storage and infrastructure costs; supports premium upgrade
- Affects: Search, Saved Items, Subscription features
- Priority: High
- Owner: Product Team
- Last Reviewed: 2026-02-01

Example feature page titles:

- Smart Search - How It Finds What You Need
- Collections - Organize Content You Love
- Premium Subscription - What Paid Users Get

## Maintenance And Review Process

- Every page has a named owner.
- Set recurring quarterly calendar reminders.
- In each review, confirm accuracy and changes since the last update.
- Update Last Reviewed after each review.
- Keep a home/dashboard view of pages due for review.
- Run periodic spot-checks for readability and correctness.

## Quick Start Page Template

Use this scaffold when creating a new feature page:

```markdown
Title: [Feature Name] - [1-line description]

STATUS: [Draft / Active / Planned / Archived]
OWNER: [Name/Team]
LAST REVIEWED: [Date]

## What & Why
[2-3 sentences describing what this feature is and why it matters]

## How It Works
[Simple overview with visuals]

## Product Rules & Constraints
- Rule 1 and why it exists
- Rule 2 and why it exists

## Design & User Experience
[Screenshots or mockups]

## Timeline
[When launched / planned]

## Decisions Made
- Decision 1: Why chosen, what was rejected
- Decision 2: Why chosen, what was rejected

## Related Features
- Link to feature/rule X
- Link to feature/rule Y
```

## Success Tips

- Start with the highest-value features first.
- Rewrite until Sales, Support, Design, and Engineering can all follow the page.
- Keep documentation centered on product behavior and customer value.
- Prefer visual communication where possible.
- Link generously across related pages.
- Review regularly; stale documentation is harmful.
- Include cross-functional input so the knowledge base reflects real user impact.
