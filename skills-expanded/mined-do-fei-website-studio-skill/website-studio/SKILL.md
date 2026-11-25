---
name: website-studio
description: Plans, designs, builds, validates, and prepares polished responsive websites and lightweight web apps from brief through hosting handoff. Use when creating or redesigning a landing page, portfolio, editorial site, knowledge hub, directory, dashboard, portal, tracker, internal tool, microsite, or small web app, especially when the agent must adapt to available design, browser, data, authentication, upload, connector, and deployment capabilities.
license: MIT
compatibility: Agent Skills-compatible coding agent. Browser preview recommended; optional validators require Node.js 20+.
metadata:
  version: "1.0.0"
  author: "Do-fei"
  homepage: "https://github.com/Do-fei/website-studio-skill"
---

# Website Studio

Turn a website request into a complete, visually intentional, usable, and honestly verified product. Preserve existing project constraints and adapt to the tools actually available; never pretend a missing browser, database, connector, or deployment capability exists.

## Route before building

1. Inspect whether the project is empty or existing; preserve its framework, package manager, scripts, lockfile, architecture, and hosting configuration.
2. Classify the primary website recipe. Use one main recipe and at most one supporting recipe.
3. Choose the simple path only for a small content-led site with no durable data, identity, uploads, external connectors, or complex write flows. Everything else uses the capability path.
4. Record access mode: public anonymous, authenticated, or internal. Record whether the deliverable is local, private preview, or public.
5. Inventory available capabilities using `references/capability-routing.md`. Do not choose architecture from unavailable platform features.

## Seven-gate workflow

### 1. Brief

Ask only for missing high-impact context: audience, primary job, required content, desired feeling, capabilities, and release boundary. If direction is complete or the user delegates decisions, continue without blocking. Use `references/discovery.md` and `assets/website-brief.template.md`.

### 2. Design direction

Derive the visual system from the subject and user job. When a high-impact choice is unresolved, compare exactly three meaningful options using shared content and viewport; never exceed four sequential choice rounds. If visual tools are unavailable, provide implementation-grade text directions. Use `references/design-choice-flow.md` and `references/design-quality.md`.

### 3. Content and product shape

Define routes, hierarchy, primary actions, content model, critical flows, and normal/empty/loading/error/permission states before implementation. Use realistic copy and data. Follow `references/content-and-ux.md`.

### 4. Build

Choose the smallest architecture that satisfies the requested product. Implement semantic structure, responsive behavior, keyboard and touch use, state feedback, metadata, and failure handling together. Remove starter content and unused scaffolding. Follow `references/implementation.md`.

### 5. Capability work

Load only the requested capability recipes: `recipes/capability-data.md`, `recipes/capability-auth.md`, `recipes/capability-uploads.md`, or `recipes/capability-connectors.md`. Keep authorization server-side, secrets out of source, blobs out of databases, and durable product data out of browser-only storage.

### 6. Verify

Run the real build and deterministic checks, then inspect the real page at wide desktop, tablet, 390 px, and 320 px when browser control exists. Test critical flows, keyboard focus, image crops, overflow, console errors, and required states. If browser tools are absent, say visual QA remains incomplete. Follow `references/responsive-accessibility.md` and `references/qa-and-release.md`.

### 7. Publish and hand off

Publish the exact validated version through the selected adapter. Default to local or private preview unless public release is requested or already established. Verify public sites anonymously and protected sites against their expected anonymous behavior. Follow `references/hosting-handoff.md`.

## Choose a website recipe

- `recipes/landing-page.md` — launch, product, campaign, or conversion page.
- `recipes/portfolio.md` — personal, studio, or project showcase.
- `recipes/editorial-story.md` — story, archive, cultural feature, or memorial.
- `recipes/knowledge-hub.md` — documentation, learning, or resource hub.
- `recipes/directory-catalog.md` — searchable and filterable collection.
- `recipes/dashboard.md` — metrics, monitoring, and analytical views.
- `recipes/portal-internal-tool.md` — role-based portal, operations surface, or internal tool.
- `recipes/tracker-workflow.md` — record creation, status transitions, history, and workflow.

## Choose an adapter

- Use `adapters/sites.md` when Sites is available or `.openai/hosting.json` exists.
- Use `adapters/existing-project.md` for an established repository.
- Use `adapters/static.md` for a small framework-free site.
- Use `adapters/generic-framework.md` when routes, components, server rendering, or capabilities justify a framework.

## Non-negotiable quality

- The first viewport expresses the specific product, not generic dashboard or landing-page chrome.
- No broken media, placeholder copy, accidental horizontal overflow, inaccessible controls, or unexplained empty space.
- Images have a purpose, rights status, alt strategy, and deliberate crop; unrelated hero imagery is rejected.
- Public factual or third-party media work follows `references/source-and-rights.md`.
- Public pages have accurate language, title, description, icons, and social metadata when a valid asset exists.
- Never claim visual review, live data, authentication, deployment, or public access without direct evidence.

## Deliverable

Hand off the brief, selected direction, implementation, capability matrix, build and test evidence, desktop/mobile QA evidence, rights status when relevant, and a verified URL or an explicit “prepared but not deployed” boundary.
