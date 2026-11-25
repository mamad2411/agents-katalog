---
name: fabrico-reverse-engineering-spec
description: "Reverse-engineer a complete, platform-agnostic SPEC.md from a running legacy web application by inspecting it with the Playwright MCP (Chrome automation): crawl routes, capture every screen, infer the data model, roles, flows, and integrations, then synthesize features into user stories with acceptance criteria. Use when modernizing an old web app to a newer stack or porting it to mobile/iOS. Produces a SPEC.md compatible with /fabrico-autopilot."
---

# Reverse-engineering a spec from a running web app

Turn an existing (often legacy) web application into a clean, **platform-agnostic** `SPEC.md` that
`/fabrico-autopilot` (or a migration build) can use to rebuild it on a modern stack or port it to mobile.

You observe the running app through the **Playwright MCP** (it drives a real Chromium/Chrome). You describe
*what the app does* (behavior, data, roles, flows) — NOT how the old code is written. The output is a behavioral
spec, not a code transliteration.

## Inputs you need before starting

- **Base URL** of the running app (production, staging, or localhost).
- **Access**: if any area is behind login, the credentials or a logged-in session. Auth-gated areas you cannot
  reach must be flagged, not guessed.
- **Scope**: whole app, or specific areas/roles. If unspecified, cover everything reachable.

If the URL is missing or auth blocks a required area → STOP and ask the user (this is a true blocker).

## Output artifacts

- `SPEC.md` — the deliverable, following the structure of `SPEC.template.md`, plus a **Target (fill at build time)**
  section (platform-agnostic) and a **Source mapping** appendix.
- `legacy-inventory.md` — sitemap/route inventory with per-screen notes.
- `legacy-capture/` — screenshots and saved accessibility snapshots per screen (evidence).
- `reverse-spec-notes.md` — open questions, uncertainties, and assumptions for the user to confirm.

## Process (track progress with this checklist)

```
Reverse-engineering progress:
- [ ] Step 1: Scope & access confirmed
- [ ] Step 2: Route/page inventory (sitemap)
- [ ] Step 3: Per-screen capture loop complete
- [ ] Step 4: Data model inferred
- [ ] Step 5: Roles, permissions & flows inferred
- [ ] Step 6: Integrations & non-functional inferred
- [ ] Step 7: Features synthesized into user stories with acceptance criteria
- [ ] Step 8: SPEC.md written + coverage gate passed
```

### Step 1 — Scope & access
Confirm base URL, credentials, and scope. Open the app with the Playwright MCP and verify you can reach it.
For the concrete browser recipe (which `mcp__playwright__*` tools to call and in what order), follow
[`references/playwright-capture.md`](references/playwright-capture.md).

### Step 2 — Route / page inventory
Crawl the app to build a sitemap: follow navigation, menus, links, and obvious URL patterns (e.g. `/users`,
`/users/:id/edit`). Record every distinct screen/state in `legacy-inventory.md`. Note auth-gated areas and which
role they belong to. Don't recurse infinitely — collapse list/detail pages into one representative example each.

### Step 3 — Per-screen capture loop
For each screen in the inventory: take a screenshot, capture the accessibility-tree snapshot, and record the
meaningful elements — **forms** (fields, types, validation hints, required markers), **tables/lists** (columns,
filters, sorting, pagination), **actions** (buttons and what they do), **navigation**, and visible **states**
(empty, error, loading, modals). Exercise key interactions (open a form, submit, paginate) to reveal behavior and
validation. Save evidence under `legacy-capture/`.

### Step 4 — Infer the data model
From forms, tables, detail pages, and URL patterns, infer the entities and their relationships (e.g. a "Users"
table + "Edit user" form + `/users/:id/orders` ⇒ `User 1—* Order`). Capture fields, types, and obvious constraints.
Express it as the lightweight entity sketch used in `SPEC.template.md` §5 — schemas are designed later by the architect.

### Step 5 — Roles, permissions & flows
Compare what's visible/possible across roles (anonymous vs logged-in vs admin). Infer the role set and what each
can do. Trace multi-step **flows** (e.g. checkout, onboarding, approval) end to end and document the steps.

### Step 6 — Integrations & non-functional
From network requests and page content, identify external integrations (payment providers, maps, auth/SSO,
analytics, email, third-party widgets) and note which are core vs incidental. Capture non-functional signals:
languages/i18n, responsive behavior, auth model, file uploads, anything that affects a rebuild.

### Step 7 — Synthesize features → user stories
Group screens/flows into epics and write concrete **user stories with testable acceptance criteria** (same shape
as `SPEC.template.md` §4). Base every acceptance criterion on observed behavior; where behavior is unclear, write a
provisional criterion and list the open question in `reverse-spec-notes.md`. Do NOT invent features the app
doesn't have, and do NOT silently drop features you saw.

### Step 8 — Write SPEC.md + coverage gate
Assemble `SPEC.md` using the `SPEC.template.md` structure, with two additions:
- A **"Target (fill at build time)"** section: keep the spec platform-agnostic; list candidate targets
  (modern web / iOS / React Native) and instruct that the concrete target is chosen by `/fabrico-modernize` or
  by editing this section before `/fabrico-autopilot`. UX described in behavioral terms (what the screen does),
  not pixel layouts, so it ports across platforms.
- A **"Source mapping"** appendix: table of *old screen/URL → epic/story* so nothing is lost and parity is checkable.

**Coverage gate:** every screen in `legacy-inventory.md` maps to at least one story (or is explicitly marked
out-of-scope with a reason). If not, go back. Then summarize open questions from `reverse-spec-notes.md` for the user.

## Important guidance

- **Behavior over implementation.** Describe what the app does for users and data, not the legacy framework's quirks.
- **Don't guess behind auth.** If you can't reach an area, flag it — never fabricate its features.
- **Handle SPAs/dynamic content.** Wait for content to load; interact to reveal hidden states (tabs, modals, lazy lists).
- **Representative sampling for big lists.** Document the pattern once; note volume rather than capturing every row.
- **Mark every uncertainty.** Anything inferred-but-unconfirmed goes to `reverse-spec-notes.md` with a clear question.
- **Keep the spec platform-agnostic** so the same SPEC.md can target modern web, iOS, or React Native.
