---
name: ux-test
description: Analyze and review the UI/UX of a web application to produce actionable recommendations, identify usability issues, and evaluate design quality. Use when the user wants to audit UX, review UI design, get UX improvement suggestions, evaluate usability, check design consistency, or assess user experience quality. Trigger when the user says "review my UX", "audit my UI", "analyze my design", "check usability", "give UX feedback", "UX review", or provides a URL for UX/design evaluation.
---

# UX Testing

Explores a web app live in a browser via playwright-mcp, captures screenshots and DOM snapshots, and evaluates UI/UX quality against established heuristics. Produces a prioritized recommendation report — no external API needed.

## Workspace

All output goes into **`.opentest-workspace/ux/`** in the current working directory. Create it before starting:

```bash
mkdir -p .opentest-workspace/ux/screenshots
```

Add to `.gitignore` if not already there:
```
.opentest-workspace/
```

| Output | Path |
|--------|------|
| Screenshots | `.opentest-workspace/ux/screenshots/<page-name>.png` |
| UX report | `.opentest-workspace/ux/report-<YYYY-MM-DD>.md` |

## Evaluation Framework

Use **Nielsen's 10 Usability Heuristics** as the primary framework, supplemented by visual design principles. See [references/heuristics.md](references/heuristics.md) for the full checklist and scoring guide.

**Severity scale for findings:**

| Severity | Label | Meaning |
|----------|-------|---------|
| 🔴 | Critical | Blocks users from completing core tasks |
| 🟠 | High | Causes significant confusion or friction |
| 🟡 | Medium | Noticeable friction, workaround exists |
| 🔵 | Low | Minor polish issue, minimal user impact |
| 💡 | Suggestion | Enhancement idea, no current problem |

## Guiding Principle

**Every finding must be grounded in user impact — not personal preference.**

Before starting, have answers to:
- Who are the target users and what is their technical level?
- What are the primary tasks users need to accomplish?
- What device/context do users primarily access this on?

Generic aesthetic opinions ("this looks dated") are only useful when mapped to a specific usability problem.

---

## Workflow

### Phase 0: Intake

Ask these questions **in a single message**:

1. **URL** — What is the URL of the app?
2. **Auth** — Does it require login? (same handling as e2e-test: form login / OAuth / token injection)
3. **Target users** — Who uses this? (e.g., non-technical customers, internal ops team, developers)
4. **Focus** *(optional)* — Any specific pages, flows, or UX concerns to prioritize?
5. **Context** *(optional)* — Mobile-first? Desktop only? B2B SaaS? Consumer app?

Do not proceed until you have the URL and user context.

---

### Phase 1: Browser Setup & Auth

Navigate to the URL, handle auth if needed, confirm the app is accessible before continuing.

**Auth handling:**

| Auth type | Action |
|-----------|--------|
| No login | Proceed to Phase 2 |
| Email/password | `browser_fill` → `browser_click` submit → verify redirect |
| Google OAuth / SSO | Ask user to provide session cookie → inject via `browser_evaluate` |
| Token / cookie | `browser_evaluate` → `localStorage.setItem(...)` → reload |

Auth is confirmed when screenshot shows the app interior, not a login page.

---

### Phase 2: Discovery

Systematic BFS exploration. **Limit: 10 pages, depth 3.**

**For each page:**
1. `browser_snapshot` — extract navigation structure, interactive elements, form fields
2. `browser_screenshot` — save to `.opentest-workspace/ux/screenshots/<page-name>.png`
3. Record page purpose and key elements in the running site map

**Go beyond static pages — capture UI states:**
- Open dropdowns, menus, modals (note visual treatment)
- Trigger hover states on key CTAs via `browser_hover`
- Submit an empty form to see validation/error states
- Visit an empty/zero-data state if possible
- Resize to 375×812 to check mobile layout for at least 2 key pages

**Site map format:**
```
/dashboard      → Main hub, 3 primary CTAs visible
/projects/new   → 3-step wizard with progress indicator
/settings       → Tabbed layout: Profile | Team | Billing
```

---

### Phase 3: Analysis Framing

Before evaluating, write a brief framing:

1. **App type & domain** — What kind of product is this?
2. **Target user mental model** — What does the user expect this app to behave like?
3. **Primary task flows** — The 2–4 most important things users do
4. **First impressions** — What communicates the app's purpose within 5 seconds?

Present this to the user and ask:
- "Does this match how you think about your users?"
- "Any pages or flows to prioritize or skip?"

Wait for confirmation before Phase 4.

---

### Phase 4: UX Evaluation

Systematically evaluate each captured screen against the heuristics in [references/heuristics.md](references/heuristics.md). Load that file now.

**For each page/state, evaluate across 8 dimensions:**

1. **Visibility of system status** — Does the user know what's happening?
2. **Match with mental model** — Does the UI behave like users expect?
3. **Error prevention & recovery** — Are errors prevented? Are messages helpful?
4. **Cognitive load** — Is the interface asking too much of the user?
5. **Visual hierarchy** — Is the most important action/info most prominent?
6. **Consistency** — Do similar elements look and behave the same way?
7. **Affordances** — Are interactive elements obviously clickable/tappable?
8. **Feedback** — Do actions produce clear, timely responses?

**For each screenshot, also analyze:**
- Layout: spacing, alignment, visual grouping (Gestalt principles)
- Typography: hierarchy, readability, size contrast
- Color: meaning, contrast (flag obvious issues; defer deep WCAG audit to a11y-test skill)
- Mobile (if captured): touch targets ≥44px, no horizontal scroll, readable text

**For each finding, record:**
- Severity (🔴🟠🟡🔵💡)
- Which heuristic it violates
- Page/element affected
- User experience consequence
- Concrete recommendation

---

### Phase 5: Report

Save findings to `.opentest-workspace/ux/report-<YYYY-MM-DD>.md`.

```markdown
# UX Review Report

**App:** <URL>
**Date:** <YYYY-MM-DD>
**Reviewer:** Claude (ux-test skill)
**Pages Reviewed:** N
**Target Users:** <as described>

---

## Executive Summary

<2–4 sentences: overall UX quality, most impactful issues, biggest opportunities>

**Finding counts:** 🔴 N critical | 🟠 N high | 🟡 N medium | 🔵 N low | 💡 N suggestions

---

## Critical & High Priority Findings

### 🔴 [CRITICAL] <Finding title>
- **Page/Element:** ...
- **Heuristic violated:** <e.g., Nielsen #1 – Visibility of System Status>
- **User impact:** <what the user experiences>
- **Current behavior:** ...
- **Recommendation:** ...
- **Screenshot:** `screenshots/<page>.png`

### 🟠 [HIGH] <Finding title>
...

---

## Medium & Low Priority Findings

### 🟡 [MEDIUM] <Finding title>
...

### 🔵 [LOW] <Finding title>
...

---

## Positive Observations

<What the app does well — 3–5 items. Helps the team know what to preserve.>

---

## Suggestions & Enhancement Ideas

💡 <Idea> — <brief rationale>

---

## Page-by-Page Summary

| Page | Key Issues | Strengths |
|------|-----------|-----------|
| /dashboard | CTA hierarchy unclear, empty state missing | Clean layout |
| ... | ... | ... |

---

## Recommended Priority Actions

Top 3–5 changes that would most improve UX, in priority order:

1. **<Action>** — <why this is highest impact>
2. ...
```

After saving, present to the user:
- Finding counts by severity
- Top 3 recommended actions
- Path to the saved report
