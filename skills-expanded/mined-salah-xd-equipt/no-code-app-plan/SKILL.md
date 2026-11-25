---
name: no-code-app-plan
description: "Plans no-code application builds with tool selection, feature mapping, and user flow design. Use when building apps or tools without writing code."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# No-Code App Plan

## When to Use This Skill

Use this skill when you need to:
- Plan a no-code application build from concept to launch
- Select the right no-code tools for your specific use case
- Map features and user flows before building
- Create a phased build plan with milestones

**DO NOT** use this skill for custom software development, no-code tool tutorials, or website-only projects (use standard web design approaches). This is for functional applications built with no-code platforms.

---

## Core Principle

NO-CODE IS A BUILDING TOOL, NOT A SHORTCUT — PLAN THE APPLICATION BEFORE YOU TOUCH THE BUILDER. A CLEAR PLAN PREVENTS THE MOST COMMON NO-CODE FAILURE: BUILDING YOURSELF INTO A CORNER.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **App concept** | "What does the app do in one sentence?" | No default — must be provided |
| **Target user** | "Who will use this app? Describe the primary user." | No default — must be provided |
| **Core problem** | "What problem does this solve for the user?" | No default — must be provided |
| **Key features** | "List the top 5 features the app must have at launch." | No default — must be provided |
| **No-code experience** | "Have you built with no-code tools before? Which ones?" | Beginner |
| **Budget** | "What is your monthly budget for tools and hosting?" | Under $50/month |
| **Timeline** | "When do you need this live?" | 4-6 weeks |

**GATE: Confirm the brief before selecting tools or designing flows.**

---

## Phase 2: Design

### Feature Priority Map

Categorize features into launch phases:

| Feature | Priority | Phase |
|---------|----------|-------|
| [Feature 1] | Must-have | MVP (v1) |
| [Feature 2] | Must-have | MVP (v1) |
| [Feature 3] | Must-have | MVP (v1) |
| [Feature 4] | Nice-to-have | v2 |
| [Feature 5] | Nice-to-have | v2 |
| [Feature 6] | Future | v3+ |

**Rule:** MVP includes only the features required for a user to accomplish the core task. Everything else is v2 or later.

### User Flow Diagrams

Map the primary user journey:

```
## Primary User Flow

[Landing Page]
  → [Sign Up / Login]
    → [Dashboard / Home]
      → [Core Action 1]
        → [Result / Confirmation]
      → [Core Action 2]
        → [Result / Confirmation]
    → [Settings / Profile]
    → [Logout]
```

For each screen, note:
- What the user sees
- What actions they can take
- Where each action leads
- What data is created or displayed

### Data Model

Define the data structure:

```
## Data Model

**Users**
- Name, email, password, role, created_date

**[Primary Entity]**
- [Field 1]: [type]
- [Field 2]: [type]
- [Field 3]: [type]
- Relationships: belongs_to [User]

**[Secondary Entity]**
- [Field 1]: [type]
- Relationships: belongs_to [Primary Entity]
```

**GATE: Confirm features, user flow, and data model before selecting tools.**

---

## Phase 3: Build Plan

### No-Code Tool Selection

| Use Case | Recommended Tools | Best For |
|----------|------------------|----------|
| **Web app with database** | Bubble, Softr, Glide | Full-featured web apps |
| **Mobile app** | Adalo, FlutterFlow, Glide | Native mobile experience |
| **Internal tool** | Retool, Notion, Airtable | Team dashboards, admin panels |
| **Marketplace** | Sharetribe, Bubble | Two-sided platforms |
| **Directory or listing site** | Softr + Airtable | Simple listings and search |
| **Form-based workflow** | Tally + Airtable + Zapier | Data collection and processing |
| **Landing page with app features** | Carrd + Airtable + Zapier | Lightweight MVP |

### Recommended Tool Stack

```
## Tool Stack for [App Name]

**Frontend:** [Tool] — $[X]/month
**Database:** [Tool] — $[X]/month
**Authentication:** [Built-in / Auth0 / Firebase]
**Payments:** Stripe — per-transaction
**Automation:** Zapier / Make — $[X]/month
**File storage:** [Tool] — $[X]/month
**Total monthly cost:** $[X]
```

### Build Schedule

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| 1 | Setup and data model | Database structure, user auth, basic navigation |
| 2 | Core feature 1 | Primary user action working end-to-end |
| 3 | Core feature 2-3 | Remaining MVP features |
| 4 | Polish and test | UI cleanup, mobile responsiveness, bug fixes |
| 5 | Beta testing | 5-10 users testing the app |
| 6 | Launch | Public launch with feedback loop |

---

## Phase 4: Polish

### 1. Pre-Launch Testing

```
## Testing Checklist

- [ ] All user flows work end-to-end (signup → core action → result)
- [ ] Data saves and displays correctly
- [ ] Authentication works (login, logout, password reset)
- [ ] Mobile responsive (test on phone and tablet)
- [ ] Edge cases handled (empty states, errors, long inputs)
- [ ] Payment processing works with test transactions (if applicable)
- [ ] Page load time under 3 seconds
- [ ] 5 real users have tested and provided feedback
```

### 2. Scalability Considerations

- **User limits:** Check the no-code tool's plan limits (rows, users, API calls)
- **Performance:** Test with realistic data volume (100+ records)
- **Backup:** Export data regularly — never rely solely on the no-code platform
- **Exit strategy:** Can you export your data if you need to migrate later?

### 3. Quality Checklist

```
## No-Code App Plan Checklist

- [ ] App concept described in one sentence
- [ ] Target user and problem clearly defined
- [ ] Features prioritized into MVP vs. future phases
- [ ] Primary user flow mapped screen by screen
- [ ] Data model defined with entities and relationships
- [ ] No-code tools selected with cost estimates
- [ ] Build schedule broken into weekly milestones
- [ ] Testing checklist prepared for pre-launch
- [ ] Scalability limits of chosen tools understood
- [ ] Data export and backup plan documented
```

---

## Example

**App:** Client project tracker for freelancers
**Tool stack:** Softr (frontend) + Airtable (database) + Stripe (payments)
**Monthly cost:** $49 (Softr Pro) + $20 (Airtable Plus) = $69/month

**User flow:**
```
Client receives link → Views project dashboard → Sees deliverables and timeline
Freelancer logs in → Creates project → Adds milestones → Tracks time → Generates invoice
```

**Data model:**
- Clients: name, email, company
- Projects: name, client (linked), status, start_date, end_date
- Milestones: project (linked), name, due_date, status
- Time entries: project (linked), date, hours, description

---

## Anti-Patterns

- **Building without a plan** — jumping into the builder and figuring it out as you go creates spaghetti that is impossible to maintain.
- **Too many features in v1** — the MVP should do ONE thing well. Add features after you confirm people use the core.
- **Ignoring data model** — the database structure is the foundation. Getting it wrong means rebuilding everything later.
- **Choosing tools based on hype** — choose based on your specific use case, not what is trending on social media.
- **No exit plan** — if your no-code platform shuts down, can you get your data out? Always verify data portability.

---

## Recovery

- **Hit a tool limitation mid-build:** Check if the limitation is a plan limit (upgrade) or a platform limit (may need to switch tools). Switching tools is easier in weeks 1-2 than week 5.
- **Build is taking longer than planned:** Cut features from v1. Ship the minimum viable version and add features in v2.
- **Users do not understand the app:** The UX is too complex. Simplify the primary flow and add a tutorial or onboarding sequence.
- **Need custom code after all:** Many no-code tools allow custom code snippets. Use them for the 10% that no-code cannot handle before rebuilding entirely.
