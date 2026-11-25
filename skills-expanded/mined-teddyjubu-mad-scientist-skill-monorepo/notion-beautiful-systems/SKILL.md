---
name: notion-beautiful-systems
description: notion-beautiful-systems lets the user create, redesign, migrate, publish, and maintain beautiful Notion workspaces and pages, which is useful when they want a polished knowledge base, a clean team wiki, a well-organized CRM, or any Notion setup that looks professional and works effortlessly without needing to figure out Notion's design patterns themselves.
  Use this before creating, redesigning, migrating, publishing, or QA'ing any
  Notion page, database, workspace system, public Notion Site, product how-to
  guide, tutorial, SOP hub, dashboard, client portal, resource library, or
  agent-generated Notion deliverable where the result should look polished,
  premium, and easy to scan, not merely functional.
---

# Notion Beautiful Systems

Use this skill to make Notion work feel intentionally designed. The goal is a
Notion-native system that is elegant, scannable, publishable, and useful.

Pair this with the `notion-cli` skill for API/CLI execution and the Publisher
Agent workflow for the final published-link gate.

If Charles asks for a how-to guide for any product, default to this skill unless
he explicitly asks for a different format only. A product guide should include a
beautiful Notion page/system, screenshots or product visuals when useful, and
Publisher Agent validation before the final link is sent.

## What This Skill Does

This skill notion-beautiful-systems lets the user create, redesign, migrate, publish, and maintain beautiful Notion workspaces and pages, which is useful when they want a polished knowledge base, a clean team wiki, a well-organized CRM, or any Notion setup that looks professional and works effortlessly without needing to figure out Notion's design patterns themselves.

## Operating Standard

Every Notion deliverable should pass these rules before the user sees it:

- The first viewport explains what this is, who it is for, and what to do next.
- Navigation is obvious within 10 seconds.
- Visual hierarchy comes from structure: cover, icon, title, callouts, columns,
  database views, section rhythm, and restrained color.
- Databases have a purpose, clean properties, useful views, and templates.
- Public/client-facing pages hide internal clutter, scratch notes, and secrets.
- The final answer to Charles uses the published Notion Site URL when publishing
  is expected, never the internal `www.notion.so/...` workspace URL.

## First Moves

1. Classify the deliverable:
   - Public guide or Notion Site
   - Executive dashboard
   - Project/client portal
   - SOP or wiki hub
   - Resource library
   - Migration/index page
   - Internal operating system

2. Define the audience and action:
   - Who opens this page?
   - What decision or action should they take?
   - What belongs above the fold?
   - What can be hidden lower, in toggles, tabs, databases, or linked pages?

3. Choose a visual system:
   - One cover style: clean editorial image, product screenshot, branded image,
     or subtle abstract only when no real subject exists.
   - One icon style: Notion native icons, emoji, or simple external icons; do not
     mix styles randomly.
   - One accent color family plus neutral structure. Use color semantically, not
     as decoration.

4. Build the skeleton before filling content:
   - Page title, icon, cover
   - Short orientation callout
   - Compact navigation or command-center row
   - Main work sections
   - Databases/views or linked databases
   - Reference/archive area
   - QA and publish checklist

## Notion-Native Design Patterns

Use these primitives deliberately:

- Covers and icons for orientation and brand feel.
- `heading_1` for major zones only; `heading_2` for sections; `heading_3` for
  compact cards/lists.
- Callouts for semantic messages:
  - Blue: context, instructions, overview
  - Green: live, approved, success
  - Yellow: warning, review, needs decision
  - Red: blocker, risk, broken item
  - Gray: reference, archive, neutral note
- Columns for top-level dashboards and comparison blocks.
- Toggle headings for long reference material and optional detail.
- Table of contents for long guides and public pages.
- Dividers for rhythm between zones, not after every paragraph.
- Database views for different jobs: table for operations, board for workflow,
  calendar/timeline for time, gallery for visual libraries, list for simple
  navigation.
- Tabs when supported and useful for audience modes, such as Client/Internal,
  Setup/Runbook, Overview/Details.

## Page Recipes

### Premium Guide

Use for how-to docs, tutorials, and public explanations.

1. Cover, icon, clear title.
2. Blue orientation callout: outcome, time needed, prerequisites.
3. Table of contents.
4. Step sections with screenshots or media where visual proof matters.
5. Troubleshooting toggle section.
6. Final checklist or next action.
7. Publisher Agent validation before delivery.

### Executive Dashboard

Use for daily/weekly operating views.

1. Small status strip: today, owner, health, last updated.
2. Three to five priority cards or columns.
3. Linked database views filtered to current work.
4. Decision/risk callouts.
5. Reference/archive material lower on the page.

### Client Portal

Use for client-safe shared spaces.

1. Client-facing title, cover, and icon.
2. Welcome/status callout with the current phase and next action.
3. Navigation row: Deliverables, Timeline, Tasks, Files, Decisions.
4. Filtered database views that show only client-relevant records.
5. Private/internal material on separate pages or excluded entirely.
6. Public-link validation before sending.

### SOP Or Wiki Hub

Use for operating manuals and team knowledge.

1. Purpose and ownership callout.
2. Search/TOC-friendly section names.
3. SOP database with properties: Status, Owner, Area, Review date, Last updated.
4. Templates for new SOPs with Scope, Steps, QA, Failure modes, Escalation.
5. Verified/maintained pages get visual status; stale pages are visibly marked.

### Resource Library

Use for screenshots, assets, links, vendors, prompts, or references.

1. Gallery or table view with preview images when useful.
2. Minimal required properties: Type, Status, Owner/Source, Tags, Last checked.
3. Curated top section for best/current resources.
4. Archive view for old or superseded items.

## Database Quality Rules

Every database should have:

- A plain-English purpose.
- Fewer properties than possible; only keep fields used for filtering, sorting,
  ownership, status, or display.
- At least two useful views for different tasks when the database matters.
- Consistent status names and ordering.
- Clean page templates for repeatable records.
- Relations and rollups only when they reduce duplication or improve navigation.

## Validation Rubric

Score each category 0-3:

- First viewport clarity
- Navigation and information architecture
- Visual hierarchy and rhythm
- Database/view usefulness
- Content polish and concision
- Client/public safety
- Publishing readiness

Minimum passing scores:

- Internal draft: 14/21
- Internal operating system: 16/21
- Client-facing page: 18/21
- Public Notion Site: 19/21

If a page fails, revise before publishing or sending.

## Common Anti-Patterns

- One giant page with no dashboard, TOC, or linked views.
- Too many callouts, colors, emojis, or icons competing for attention.
- Databases with every possible property but no clear view strategy.
- Pretty header followed by unstructured text.
- Client pages that expose internal notes, rough drafts, or private decisions.
- Any visible placeholder/test text such as "Placeholder", "Test icon fix",
  "TODO", "TBD", "insert screenshot", "lorem ipsum", or "replace this".
- Decorative glitches that look like repeated orphan icons, dash columns, empty
  callouts, or broken visual scaffolding.
- Sending an internal Notion URL when the user expects a published link.
- Using Notion as a static document when a small database/view system would make
  the work easier to maintain.

## API And Publishing Constraints

The Notion API supports many useful blocks but not every UI block type. Treat
unsupported blocks, custom CSS, arbitrary fonts, and pixel-level layout as out of
scope. Use Notion-native polish instead.

When creating content programmatically, respect API limits:

- Append children in batches of 100 or fewer.
- Avoid deeply nested block creation in one request.
- Expect rate limits and retry calmly.
- Set page `icon` and `cover` as top-level page fields.
- Use current Notion API docs for views, data sources, files, and block support.

Before final delivery, run the Publisher Agent validation workflow. If
`needsPublish=true`, publish in Notion, validate again, and only send the
published `finalLink`.

If Publisher Agent reports `draftArtifactCount>0`, revise the page before
sending. Placeholder/test artifacts are blocking issues for public pages.

Load `references/research-synthesis.md` for the source-backed design research.
Load `references/qa-rubric.md` for the stricter scoring checklist.
