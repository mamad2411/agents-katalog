---
name: site-mapper
description: "Use when converting app ideas into site maps, page specifications, and prompts for code/design tools. Plans web application structure."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [site-map, information-architecture, web-planning, wireframing, app-design]
---

# Site Mapper

## Overview

Transform app ideas and product briefs into structured site maps, page-by-page specifications, and ready-to-use prompts for code generation and design tools. Bridges the gap between "I have an idea" and "here's exactly what to build" — producing the information architecture and functional specs that developers and AI coding tools need to start building.

## When to Use

- "Turn my app idea into a site map" — information architecture planning
- "What pages do I need for a [type] app?" — page inventory for a new project
- "Create detailed specs for each page of my app" — page-level specifications
- "Generate prompts for building [app idea]" — AI coding tool prompts
- "Plan the structure of my web application" — pre-development planning

**Don't use for:** visual design mockups (use `sketch` or `claude-design`), database schema design (use `backend-dev`), or content writing (use the content itself as input).

## How It Works

**Understand the Idea → Map the Structure → Spec Each Page → Generate Build Prompts**

The output is a living document that serves as the single source of truth for what needs to be built, in what order, and how each piece connects.

## Steps

### 1. Understand the Idea
- Ask: What does the app do? Who is it for? What's the core workflow?
- Identify: authenticated vs. public pages, user roles, key interactions
- Determine: is this a marketing site, a SaaS app, an e-commerce store, a tool, or a platform?

### 2. Create the Site Map

Output a hierarchical map with page types labeled:

```
🏠 Home (Public)
├── 📄 Features (Public)
├── 💰 Pricing (Public)
├── 📝 Blog (Public)
│   └── 📄 Blog Post (Public)
├── 🔐 Sign Up (Public)
├── 🔐 Log In (Public)
├── 📊 Dashboard (Authenticated)
│   ├── 📊 Overview
│   ├── 📋 Projects
│   │   ├── 📋 Project Detail
│   │   └── ➕ New Project
│   ├── ⚙️ Settings
│   │   ├── 👤 Profile
│   │   ├── 🔔 Notifications
│   │   └── 💳 Billing
│   └── 📈 Analytics
├── ❓ Help / Docs (Public)
└── 📄 404 (Public)
```

Use these icons for clarity:
- 🏠 Home/Landing | 📄 Content page | 🔐 Auth page | 📊 Dashboard
- 📋 List/Index | ➕ Create/New | ⚙️ Settings | ❓ Help/Support
- 💰 Pricing | 📝 Blog | 📈 Analytics | 📄 Static page

### 3. Spec Each Page

For every page in the map, produce a concise spec card:

```markdown
### 📊 Dashboard

**Route:** `/dashboard`
**Access:** Authenticated users only
**Purpose:** Central hub showing user's activity and quick actions

**Components:**
- Welcome message with user's name
- Summary cards: total projects, recent activity, account status
- Quick-action buttons: "New Project", "View All Projects"
- Recent projects list (last 5, with links)
- Activity feed (last 10 events)

**Data Needs:**
- GET `/api/user/profile` — name, avatar, plan
- GET `/api/projects?limit=5` — recent projects
- GET `/api/activity?limit=10` — recent events

**States:**
- **Loading:** Skeleton cards with pulse animation
- **Empty (new user):** "Welcome! Create your first project to get started" with CTA
- **Error:** Toast notification + retry button
- **Populated:** Full dashboard with data

**Edge Cases:**
- User with very long name (truncate with ellipsis)
- No recent activity (show "No recent activity" message)
- Slow API response (show partial data as it arrives)
```

### 4. Generate Build Prompts

For AI coding tools (Claude, Codex, Cursor, etc.), translate each page spec into a targeted prompt:

```markdown
## Build Prompt: Dashboard Page

Create a responsive dashboard page at route `/dashboard` for an authenticated user. Use React + TypeScript + Tailwind CSS.

**Layout:**
- Top: Welcome bar ("Welcome back, {user.name}") with avatar
- Grid below: 3-4 summary stat cards (projects count, storage used, plan type, team members)
- Left column (2/3 width): Recent projects list with project name, last modified date, status badge
- Right column (1/3 width): Activity feed with timestamps

**API contracts (mock these for now):**
- GET /api/user/profile → { name, email, avatar_url, plan }
- GET /api/projects?limit=5 → { projects: [{ id, name, updated_at, status }] }
- GET /api/activity?limit=10 → { events: [{ id, type, description, created_at }] }

**States to handle:**
- Loading: show skeleton placeholders
- Empty: show onboarding message with CTA
- Error: show error state with retry

**Accessibility:** All interactive elements keyboard-navigable, proper ARIA labels, semantic HTML.
```

### 5. Prioritization & MVP Scoping
- Mark pages as **P0** (MVP must-have), **P1** (launch soon after), **P2** (nice to have)
- Identify the minimum set of pages needed for a functional v1
- Note dependencies: "Settings requires Auth first"

## Common Pitfalls

1. **Designing every page before validating the core.** Build and validate the critical path (signup → core action → result) before adding settings, profiles, and admin pages. MVP should be as few pages as possible.

2. **Missing auth pages in the map.** Every authenticated app needs sign-up, log-in, password reset, and email verification pages. These are often forgotten in initial planning.

3. **Under-specifying edge cases.** Empty states, error states, and loading states are not "nice to have" — they're required for every data-dependent component. Spec them from the start.

4. **Vague data needs.** "Gets user data" is not enough. Specify exact endpoints, response shapes, and what happens when data is missing. This prevents backend-frontend misalignment.

5. **No prioritization.** A map with 40 pages is a wishlist, not a plan. Rank pages by user value and technical dependency. Build in order.
