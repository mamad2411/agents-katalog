---
name: wp-divi-5-site-audit
description: Audits a Divi 5 site for design-system drift, page and Theme Builder coverage, responsive defects, accessibility barriers, broken journeys, frontend parity, and visitor-perceived performance. Use before launch or after substantial sitewide changes.
---

# wp-divi-5-site-audit

Use this skill for a whole-site quality pass. Use the narrower skills first when the task is only one page, one template, or one accessibility review.

## Audit Scope

Include:

- Homepage and core landing pages.
- Main navigation and footer.
- Single posts and relevant custom post types.
- Archives, taxonomy views, search results, no-results, and 404.
- Forms and primary calls to action.
- Representative Loop Builder output.
- Logged-out frontend on supported browsers and devices.
- Design Variables, Option Group Presets, Element Presets, and local-style drift.

## Audit Principles

- Experience the site as a first-time logged-out visitor.
- Test critical journeys, not only isolated modules.
- Fix repeated defects at the variable, preset, or template layer when that layer owns the problem.
- Do not hide functional, accessibility, or performance defects behind cosmetic polish.
- Separate builder defects from WordPress, cache, extension, hosting, or operational issues and escalate them appropriately.

## Workflow

Use [`workflows/audit-divi-site-workflow.md`](workflows/audit-divi-site-workflow.md).

## Resource

Use [`resources/site-audit-checklist.md`](resources/site-audit-checklist.md).

## Completion Evidence

Produce an audit record with scope, environment versions, tested URLs, templates, devices, breakpoints, journeys, findings by severity, owners, retest status, and explicitly deferred work.
