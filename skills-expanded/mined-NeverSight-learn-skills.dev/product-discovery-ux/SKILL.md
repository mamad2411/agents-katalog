---
name: product-discovery-ux
description: "Plan a professional website before visual implementation: stakeholder discovery, goals, personas, top tasks, information architecture, user journeys, sitemap, wireframes, scope, risks, and measurable acceptance criteria. Use before design or coding for any serious website."
version: 1.0.0
---

# Product Discovery & UX

A professional website is a service before it is a collection of screens. Do not start with a hero section. First understand what the organisation is trying to achieve, who needs the service, and which tasks must become easy.

## Discovery output

Produce a short project blueprint before coding:

1. **Business outcome** — what changes for the organisation after launch.
2. **Audience and context** — primary users, secondary users, devices, constraints, language, ability, urgency, and trust concerns.
3. **Top tasks** — rank the three to seven actions that matter most; do not let stakeholder preferences outrank user needs without recording the trade-off.
4. **Content and service inventory** — existing pages, documents, data sources, owners, freshness, legal status, and migration risk.
5. **Integration inventory** — CMS, search, forms, CRM, email, payments, maps, booking, authentication, analytics, and third-party embeds.
6. **Success measures** — task completion, qualified enquiries, registrations, search success, organic discovery, performance, accessibility, and editorial independence.
7. **Risks and decisions** — unknowns, assumptions, dependencies, owners, and the date by which each decision is needed.

## Research questions

Ask only questions that can change the product:

- Who uses the site, and what are they trying to do right now?
- What do people currently search for, call about, or abandon?
- Which content is authoritative, and who approves it?
- Which systems are the source of truth?
- What must work without an account, JavaScript, cookies, or a fast connection?
- What is explicitly out of scope?
- What would make the launch unsuccessful six weeks later?

If answers are unavailable, state assumptions visibly and design the smallest reversible solution.

## Information architecture

Create a sitemap in task language. For each route define:

- purpose and primary audience;
- primary call to action;
- parent and canonical URL;
- content owner and update frequency;
- related routes and breadcrumbs;
- loading, empty, error, permission, and offline states;
- SEO/indexing status;
- analytics events;
- accessibility and privacy considerations.

Use navigation labels people recognise. Keep institutional or technical jargon out of primary navigation unless users actually use it.

## User journeys

Write the happy path and failure path for every top task. Include:

- entry points from search, social, direct links, and internal navigation;
- the minimum information needed at each step;
- confirmation and next step;
- validation, retry, cancellation, timeout, no-result, and duplicate-submission behavior;
- keyboard, mobile, screen-reader, and low-bandwidth behavior.

A journey is not complete until the user knows what happened and what to do next.

## Scope and phasing

Separate delivery into:

- **Launch-critical** — required for the primary tasks and legal/technical safety.
- **Launch-useful** — valuable but can follow without weakening the core service.
- **Later experiments** — ideas requiring evidence, budget, or integration work.

For each feature record value, complexity, dependency, risk, owner, acceptance test, and fallback. Never hide an integration or content migration inside a vague “frontend” task.

## Deliverables before visual polish

- stakeholder map;
- top-task ranking;
- sitemap and route inventory;
- two or more critical user flows;
- content matrix and ownership model;
- integration decision record;
- risk register;
- phased backlog;
- measurable done-criteria;
- open questions and explicit assumptions.

## Acceptance criteria

A discovery phase is done when another person can implement the first release without guessing the target users, routes, content ownership, integrations, success measures, or boundaries of scope.

## Handoff

Pass this blueprint to `brand-content-strategy`, `frontend-design`, `frontend-architecture`, and `cms-integrations`. Do not allow a visual decision to silently change a top task or compliance requirement.
