---
name: springboot-prototype-ui
description: >
  Trigger when the user says "prototype the UI", "mock up the pages", "design the interface first",
  "create a static HTML mockup", "show me what the app will look like", "run springboot-prototype-ui",
  or wants to see the UI before setting up any backend code. Also trigger when the user asks to
  "validate the design", "get a visual preview", "generate fake data pages", or "start with the design".
  This skill runs as a short interactive design session and produces self-contained HTML prototypes
  that open in any browser with no server and no build step.
---

# springboot-prototype-ui

Run a short collaborative design session with the user, then generate polished, client-presentable
HTML prototypes. Output files are self-contained HTML with embedded CSS and vanilla JS — open in
any browser instantly, no Spring Boot required.

---

## Beginner-friendly explanation (show when `beginner_friendly: true`)

> **What is a prototype and why do we build it first?**
>
> A prototype is a static HTML page that looks exactly like the real app but has no working backend —
> it runs entirely in the browser with fake data written directly into the JavaScript. Think of it as
> a detailed sketch before building the house.
>
> **Why prototype first?**
> - You can share it with clients or teammates and get feedback before writing any Java code
> - Design mistakes are cheap to fix at this stage (edit HTML) vs. expensive later (refactor controllers + templates + CSS)
> - It forces you to think through every screen, every status state, and every user action before coding
>
> Once you confirm the prototype looks right, the backend skills will wire the real data in.

---

## Phase 0 — Language detection (very first step)

Before doing anything else:

1. Try to read `.spring-config.json`. If it exists and has a `language` field, **switch immediately to that language** for all further output — questions, options, confirmations, post-generate prompts, everything.
2. If the file does not exist or has no `language` field, ask:
   ```
   What language should I use?
   (1) English
   (2) 繁體中文 (Traditional Chinese)
   (3) Other — specify
   ```
   Then proceed in whichever language the user selects.

**Critical language note:**
- `"zh-TW"`, `"Traditional Chinese"`, or `"繁體中文"` → always use **繁體中文 characters**
- Never use Simplified Chinese (简体中文) — they are different writing systems. Taiwan and Hong Kong use Traditional Chinese. Mainland China uses Simplified. If in doubt about which the user wants, ask explicitly.
- This applies to: all UI copy in generated HTML (nav labels, buttons, table headers, form labels, status text, section headings, placeholders), all fake data (names, places, organizations should feel culturally appropriate), and all Claude's conversational prompts during this skill session.

---

## Phase 1 — Read config (silent)

Read `.spring-config.json` from the project root. Extract:
- `app_name` — used as default for the app name question
- `brand_name` — used in sidebar logo and footer
- `language` — already handled in Phase 0; continue in this language throughout
- `beginner_friendly` — show the explanation block above if true

If `.spring-config.json` does not exist, note the app name is unknown — ask the user in Phase 2.

---

## Phase 2 — Start the design conversation

Do NOT generate anything yet. Run through these questions one at a time (or bundle naturally if context makes answers obvious). The goal is to feel like a collaborative design session, not a form fill.

---

### Q0 — Do you already have a mockup?

```
Do you already have a mockup or wireframe?

  (1) No — build from scratch (start fresh)
  (2) Yes — I'll describe it in words
  (3) Yes — I have an existing HTML file (give me the path or paste it)
```

- If **(3)**: read the file (or accept pasted HTML). Use it as the structural reference. Your job is to:
  - Clean up the layout and apply the design system
  - Replace placeholder data with domain-appropriate fake data
  - Ensure it's fully self-contained and all interactions work
  - Skip questions that the existing mockup already answers

---

### Q1 — What does the app do?

```
Tell me about your app in 1–2 sentences. What does it do, who uses it?
(This helps me generate realistic fake data — "John Doe" placeholders ruin demos.)
```

If `.spring-config.json` exists, propose what you know:
```
Based on your config, this looks like a [description]. Is that right, or would you describe it differently?
```

---

### Q2 — Which portals to generate?

```
Which portals should I generate?

  [x] Member-facing portal  — what logged-in members see
  [x] Admin backend         — management dashboard for admins
  [ ] Public landing page   — unauthenticated page (apply, sign up, etc.)

(Defaults checked. Adjust as needed.)
```

---

### Q3 — Main sections per portal

For each selected portal, ask what sections it needs. Offer two modes:

```
For the [member/admin] portal — what are the main sections?

Option A: Describe freely
  "Just tell me what a [member/admin] needs to do and I'll figure out the sections."

Option B: List them explicitly
  "List the section names and I'll build each one."
```

Use the app description from Q1 to propose sensible defaults:
```
Based on what you described, I'd suggest these sections for the [portal]:
  - [list of suggested sections with brief descriptions]

Add, remove, or rename any of these.
```

**Reference defaults** (from the sleep-beauty prototype — use as starting point if the domain fits):

Member portal default sections:
- Dashboard / progress overview
- Submit / apply (member submits items for review)
- Browse / listings (available items or courses)
- My profile (read-only)

Admin portal default sections:
- Overview (stats cards + filterable member table)
- Review queue (submitted items, pending/approved/rejected tabs)
- New member review (onboarding applications)
- Notification center (send reminders by status group)

---

### Q4 — Layout style

```
What layout style would you like?

  (1) Tab-based — recommended
      Single page, content switches between tabs. Clean, simple, works well
      for member portals and small admin backends.

  (2) Sidebar + main content
      Fixed sidebar navigation, separate panel per section. Professional admin
      feel. Recommended for admin backends with 4+ sections.

  (3) Dashboard tiles
      Grid of card-style overviews with quick actions. Good for dashboards
      where users need a high-level snapshot rather than deep tables.

  (4) Describe your own layout
```

Recommend based on context:
- Member portal → default (1)
- Admin portal with 4+ sections → default (2)
- Simple overview-only page → (3)

---

### Q5 — Color accent

```
What accent color would you like?

  (1) Teal     — #4f7d84  calm, professional, healthcare/wellness feel
  (2) Indigo   — #4f46e5  modern SaaS, tech-forward
  (3) Navy     — #1e3a5f  trust, finance, corporate
  (4) Purple   — #6b4fa0  creative, education, premium
  (5) Rose     — #be4a6e  warm, personal brand, boutique
  (6) Slate    — #475569  neutral, minimal, enterprise
  (7) Custom   — enter a hex code

(Default: teal — the reference prototype used teal and it tested well with
 professional service businesses.)
```

Map each option to a `primary / dark / light` triplet:
- Teal    → `#4f7d84` / `#3a5e64` / `#eef4f5`
- Indigo  → `#4f46e5` / `#3730a3` / `#eef2ff`
- Navy    → `#1e3a5f` / `#152a47` / `#e8edf5`
- Purple  → `#6b4fa0` / `#52397a` / `#f3eeff`
- Rose    → `#be4a6e` / `#9b3557` / `#fdf0f3`
- Slate   → `#475569` / `#334155` / `#f1f5f9`
- Custom  → use as primary, derive dark by mixing with black at 20%, light by mixing with white at 90%

---

### Q6 — Confirm and generate

Summarize the choices and ask:

```
Ready to generate:

  App: [name]
  Portals: [list]
  Layout: [choice]
  Accent: [color + hex]
  Sections:
    Member portal: [list]
    Admin portal: [list]

  Output: ./prototype/member-portal.html and/or ./prototype/admin-portal.html

Generate? (yes / adjust something first)
```

---

## Phase 3 — Generate the HTML files

Create `./prototype/` directory and write the selected files.

**Language in generated HTML:**
- Set `<html lang="zh-TW">` (or the correct BCP 47 tag for the chosen language)
- All visible UI text must be in the selected language:
  - Navigation labels, tab names, section headings
  - Button text (Submit, Approve, Reject, Send reminder, Clear)
  - Table column headers
  - Form labels and placeholder text
  - Status badge labels (Approved / Pending / Rejected equivalents)
  - Empty-state messages
  - Info banners and notes
- Fake data must feel culturally authentic:
  - Traditional Chinese: use Taiwanese-style given names (two-character names common), Taiwanese organizations, cities (台北, 台中, 高雄, etc.), and relevant professional contexts
  - Do NOT mix Simplified and Traditional Chinese characters in the same file

---

## Design System

This design system was reverse-engineered from production Spring Boot admin prototypes. The component patterns below are the *recommended defaults* — they produce polished output. Apply them unless the user chose different layout/color in Phase 2.

### CSS Variables (embed in `<style>` block)

```css
:root {
  --accent:       /* primary color from Q5 */;
  --accent-dark:  /* dark variant from Q5 */;
  --accent-light: /* light tint from Q5 */;
  --yellow:       #fcd853;   /* always yellow — active nav indicator, logo text on dark bg */
  --bg:           #f5f3ee;   /* warm off-white page background */
  --surface:      #ffffff;   /* card/panel backgrounds */
  --surface2:     #f0ede6;   /* table header rows, subtle bg fills */
  --text:         #1a1a1a;
  --text-muted:   #6b6b6b;
  --green:        #3d8b6e;   --green-light:  #e8f5f0;   /* success */
  --red:          #c0392b;   --red-light:    #fdecea;   /* danger/error */
  --orange:       #d97706;   --orange-light: #fef3e2;   /* warning */
  --border:       #e2ddd5;
}
```

### Typography

```
Fonts (Google Fonts CDN):
  Noto Sans TC — body text, UI labels, buttons
  DM Mono      — ONLY for numeric/data values: stat card numbers, progress ring center,
                 hours/credits in tables, verification codes, IDs

Body: 13–14px / 400
Section/card titles: 14–15px / 600
Stat values: 26px / 700 / DM Mono
Labels (admin field labels): 11–12px / 600 / uppercase / letter-spacing 0.05–0.1em / muted
```

---

## Component Library

These patterns produce the polished "production-ready" look. Follow them exactly.
If the user chose a different layout in Q4, adapt as needed while keeping the color system.

### Sidebar (Layout 2)

Fixed 220px sidebar, `--accent-dark` background, full viewport height.

```
Logo block (padding 24px 20px 20px, bottom border rgba(255,255,255,0.1)):
  - App emoji/icon (22px)
  - Brand title in --yellow, 13px 700, line-height 1.3
  - Subtitle (tagline or "Admin") in rgba(255,255,255,0.5), 10px

Nav section labels:
  - 10px 700, rgba(255,255,255,0.3), uppercase, letter-spacing 0.1em
  - padding: 10px 20px 4px

Nav items:
  - padding: 10px 20px; color: rgba(255,255,255,0.7); font-size: 13px
  - border-left: 3px solid transparent
  - hover: rgba(255,255,255,0.07) bg, white text
  - active: rgba(252,216,83,0.12) bg, --yellow text and border-left, font-weight 500
  - icon: emoji 15px, fixed 18px width
  - badge (count): --yellow bg, --accent-dark text, 10px 700, rounded pill, margin-left auto

Footer: padding 14px 20px; top border rgba(255,255,255,0.1); 11px rgba(255,255,255,0.35)
```

Sidebar scrollbar (thin, unobtrusive):
```css
.sidebar::-webkit-scrollbar { width: 4px; }
.sidebar::-webkit-scrollbar-track { background: transparent; }
.sidebar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 4px; }
.sidebar { scrollbar-width: thin; scrollbar-color: rgba(255,255,255,0.2) transparent; }
```

### Topbar

```css
/* Admin topbar (with sidebar) */
height: 56px; background: --surface; border-bottom: 1px solid --border;
padding: 0 28px; position: sticky; top: 0; z-index: 50;
display: flex; align-items: center; justify-content: space-between;
/* Left: page title 15px 600 --accent-dark | Right: status alerts */

/* Member portal topbar (no sidebar, dark) */
background: --accent-dark; height: 56px; padding: 0 24px;
display: flex; align-items: center; justify-content: space-between;
/* Left: emoji + app name in --yellow 14px 700 | Right: user email rgba(255,255,255,0.7) 13px */
```

### Tab Navigation (Layout 1)

```css
.tabs-nav { background: --surface; border-bottom: 1px solid --border; padding: 0 24px; display: flex; }
.tab-nav-item {
  padding: 14px 20px; font-size: 13.5px; font-weight: 500;
  cursor: pointer; color: --text-muted;
  border-bottom: 2px solid transparent; transition: all 0.15s;
}
.tab-nav-item:hover { color: --accent; }
.tab-nav-item.active { color: --accent; border-bottom-color: --accent; }

/* Member portal content area (centered, max-width) */
.content { max-width: 860px; margin: 0 auto; padding: 28px 24px; }
```

### Stat Cards (Admin Overview)

```css
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
.stat-card {
  background: --surface; border: 1px solid --border;
  border-radius: 12px; padding: 16px 18px;
  position: relative; overflow: hidden;
}
/* Color accent: 3px top strip using ::before with position:absolute, top:0 */
.stat-card.green::before  { background: --green; }
.stat-card.orange::before { background: --orange; }
.stat-card.red::before    { background: --red; }
.stat-card.accent::before { background: --accent; }

/* Inside: */
.stat-label { font-size: 11.5px; color: --text-muted; margin-bottom: 6px; }
.stat-value { font-size: 26px; font-weight: 700; font-family: 'DM Mono', monospace; }
.stat-sub   { font-size: 11px; color: --text-muted; margin-top: 2px; }
```

### Data Table

```css
.table-wrap { background: --surface; border: 1px solid --border; border-radius: 12px; overflow: hidden; }

/* Header bar (search + filter controls) */
.table-header { display: flex; justify-content: space-between; align-items: center; padding: 14px 20px; border-bottom: 1px solid --border; }
.table-title  { font-size: 14px; font-weight: 600; }

table { width: 100%; border-collapse: collapse; }
th { background: --surface2; padding: 10px 16px; text-align: left; font-size: 12px; font-weight: 600; color: --text-muted; }
td { padding: 11px 16px; font-size: 13px; border-bottom: 1px solid --bg; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: #fafaf8; }

.search-input { padding: 7px 12px; border: 1px solid --border; border-radius: 8px; font-size: 13px; outline: none; }
.search-input:focus { border-color: --accent; }

/* Inline progress bar in table cell */
.progress-bar  { height: 6px; background: --bg; border-radius: 4px; overflow: hidden; display: inline-block; width: 80px; vertical-align: middle; }
.progress-fill { height: 100%; border-radius: 4px; }
.progress-fill.done   { background: --green; }
.progress-fill.warn   { background: --orange; }
.progress-fill.danger { background: --red; }
```

### Status Badges

```css
.badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 9px; border-radius: 20px;
  font-size: 11.5px; font-weight: 500;
}
.badge-green  { background: --green-light;  color: --green;  }
.badge-orange { background: --orange-light; color: --orange; }
.badge-red    { background: --red-light;    color: --red;    }
.badge-accent { background: --accent-light; color: --accent; }
.badge-gray   { background: #f0ede6;        color: #888;     }
.dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; display: inline-block; }
```

Example: `<span class="badge badge-green"><span class="dot"></span> Approved</span>`

### Review Cards (Admin Approve/Reject Queue)

```css
.review-card {
  background: --surface; border: 1px solid --border;
  border-radius: 12px; margin-bottom: 12px; overflow: hidden;
}
.review-card-header { display: flex; justify-content: space-between; align-items: flex-start; padding: 16px 18px; }
.review-name    { font-size: 14px; font-weight: 600; margin-bottom: 3px; }
.review-sub     { font-size: 13px; color: --text-muted; }
.review-date    { font-size: 12px; color: --text-muted; margin-top: 2px; }
.review-actions { display: flex; gap: 8px; align-items: center; flex-shrink: 0; margin-left: 16px; }
.review-body    { padding: 12px 18px 14px; border-top: 1px solid --surface2; }

/* Key number (e.g. transfer code, hours): DM Mono 22px 700 */
.key-number { font-family: 'DM Mono', monospace; font-size: 22px; font-weight: 700; color: --accent-dark; }

/* Detail grid */
.field-label { font-size: 10.5px; color: --text-muted; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 3px; }
.field-value { font-size: 13px; font-weight: 500; }

/* Action buttons */
.btn-approve { background: --green-light; color: --green; border: 1px solid #b8ddd1; }
.btn-reject  { background: --red-light;   color: --red;   border: 1px solid #f0c4bf; }
```

### Within-panel Tabs (Pending / Approved / Rejected)

```css
.tabs { display: flex; border-bottom: 2px solid --border; margin-bottom: 20px; }
.tab {
  padding: 10px 20px; font-size: 13.5px; font-weight: 500; cursor: pointer;
  color: --text-muted; border-bottom: 2px solid transparent; margin-bottom: -2px;
}
.tab.active { color: --accent; border-bottom-color: --accent; }
.tab-count { background: --yellow; color: --accent-dark; font-size: 10px; font-weight: 700; border-radius: 10px; padding: 1px 6px; margin-left: 6px; }
```

### Progress Ring (Member Dashboard)

SVG circle showing progress toward a goal:

```html
<div style="position:relative;width:100px;height:100px;flex-shrink:0">
  <svg style="width:100%;height:100%;transform:rotate(-90deg)" viewBox="0 0 100 100">
    <circle fill="none" stroke="#f0ede6" stroke-width="8" cx="50" cy="50" r="40"/>
    <circle fill="none" stroke-width="8" stroke-linecap="round" cx="50" cy="50" r="40"
      stroke="COLOR"
      stroke-dasharray="CIRC"
      stroke-dashoffset="OFFSET"/>
  </svg>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <span style="font-family:'DM Mono',monospace;font-size:20px;font-weight:700;color:COLOR">VALUE</span>
    <span style="font-size:11px;color:--text-muted">UNIT</span>
  </div>
</div>
```

Formula: `r=40, circ = 2*Math.PI*40 ≈ 251.33, offset = circ*(1 - pct/100)`

Color: `--green` if 100%+, `--orange` if 20–99%, `--red` if 0–19%

### Status Summary Card (Member Dashboard)

```css
/* Large card: progress ring left + info right */
display: flex; gap: 24px; align-items: center;
background: --surface; border: 1px solid --border; border-radius: 16px; padding: 24px;

/* Info section */
.status-name { font-size: 18px; font-weight: 700; margin-bottom: 4px; }
.status-meta { font-size: 13px; color: --text-muted; margin-bottom: 12px; }

/* Horizontal progress bar inside */
height: 8px; background: --bg; border-radius: 8px; overflow: hidden;
/* fill: same color as ring */
```

### Forms

```css
.form-section { background: --surface; border: 1px solid --border; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
.form-title   { font-size: 14px; font-weight: 600; margin-bottom: 16px; color: --accent-dark; }
.form-row     { margin-bottom: 14px; }
.form-label   { font-size: 12px; font-weight: 600; color: --text-muted; margin-bottom: 5px; display: block; }
.form-input   { width: 100%; padding: 9px 12px; border: 1.5px solid --border; border-radius: 8px; font-size: 13px; font-family: inherit; outline: none; background: --bg; }
.form-input:focus { border-color: --accent; background: #fff; }
.form-grid    { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-note    { font-size: 11.5px; color: --text-muted; margin-top: 4px; line-height: 1.5; }

/* Info banner in form */
background: --orange-light; padding: 10px 12px; border-radius: 8px; color: --orange; font-weight: 500; font-size: 12px;

/* Buttons */
.btn         { padding: 9px 20px; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; border: none; font-family: inherit; transition: all 0.15s; }
.btn-primary { background: --accent; color: #fff; }
.btn-primary:hover { background: --accent-dark; }
.btn-ghost   { background: transparent; border: 1.5px solid --border; color: --text-muted; padding: 8px 18px; }
.btn-sm      { padding: 5px 11px; font-size: 12px; }

/* Success banner */
background: --green-light; border: 1px solid #b8ddd1; color: --green;
padding: 10px 14px; border-radius: 8px; font-size: 13px; font-weight: 500;
```

### Item/Course Cards

```css
display: flex; justify-content: space-between; align-items: flex-start;
background: --surface; border: 1px solid --border; border-radius: 12px;
padding: 16px; margin-bottom: 10px;

/* Type tag */
font-size: 10.5px; font-weight: 600; padding: 2px 8px; border-radius: 10px;
/* internal: --accent-light bg, --accent text */
/* external: --orange-light bg, --orange text */

/* Item name: 14px 600 */
/* Meta: 12px --text-muted */
/* Right side value: DM Mono 18px 700 --accent */
```

### Profile Section

```css
.profile-avatar {
  width: 64px; height: 64px; border-radius: 50%;
  background: --accent-light; color: --accent-dark;
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; font-weight: 700; flex-shrink: 0;
}
/* Avatar content: first letter of name */

.profile-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
/* Field label: 11px 600 --text-muted uppercase letter-spacing 0.05em */
/* Field value: 13px 500 */
```

### Notification Center

```css
.notify-section { background: --surface; border: 1px solid --border; border-radius: 12px; margin-bottom: 14px; overflow: hidden; }
.notify-header  { display: flex; justify-content: space-between; align-items: center; padding: 14px 18px; border-bottom: 1px solid --border; }
.notify-item    { display: flex; justify-content: space-between; align-items: center; padding: 11px 18px; border-bottom: 1px solid --bg; }
.notify-item:last-child { border-bottom: none; }
```

### Empty State

```css
text-align: center; padding: 32px; color: --text-muted; font-size: 13px;
```

Use a celebratory emoji when empty is a positive outcome (e.g. no pending items → "🎉 All caught up!").

---

## Fake Data Quality Rules

The prototype fake data must be domain-appropriate. Generic placeholders ruin demos.

**Process:**
1. Use the app description from Q1 to understand the domain
2. Generate names, categories, and values plausible for that domain
3. Include a full mix of status values so every UI state is visible
4. Minimum 10 rows in any member/item table
5. Minimum 3 entries in review queues (spread across pending, approved, rejected)
6. Numbers must be internally consistent: total = sum of parts
7. Dates should be recent and realistic
8. For progress systems: show entries at 0%, ~40%, ~80%, and 100%+

**Domain inference guide (derive from Q1 answer):**
- Professional certification / CPE → credentials, course titles, credit hours, cohorts
- Membership / association → member tiers, renewal dates, dues, joining dates
- Event management → event names, attendance, check-in statuses
- Healthcare / wellness → practitioner names, session types, appointment counts
- E-learning platform → course names, completion percentages, certificates
- SaaS / subscription → plan tiers, usage metrics, billing dates
- Non-profit / volunteer → project names, volunteer hours, participation records

---

## Page Checklists

Use these as a checklist to ensure no section is incomplete. Adapt sections to what the user chose in Q3.

### Member Portal

**Dashboard / Progress tab:**
- [ ] Status summary card: ring + name + plan/tier + expiry
- [ ] Progress bar with current/goal label
- [ ] Status badge (achieved / in progress / not started)
- [ ] Recent activity list (item name, source, date, value, status badge)
- [ ] Empty state if no activity

**Submit / Apply tab:**
- [ ] Info note explaining what to submit
- [ ] Form: item name, org/source, date, quantity/value, evidence link if relevant
- [ ] 2-column grid for short fields
- [ ] Submit + Clear buttons (right-aligned)
- [ ] Success banner (auto-hides after 4 seconds)
- [ ] Required field validation via `alert()`

**Browse / Listings tab:**
- [ ] Section for "internal" items (auto-counted): header + subtitle
- [ ] Section for "external/recommended": header + subtitle
- [ ] Item cards: type tag, name, org, description, value, action button
- [ ] At least 3 internal + 3 external items

**Profile tab:**
- [ ] Avatar (first letter, colored circle)
- [ ] Name + email + status badge
- [ ] 2-column field grid with uppercase labels
- [ ] Read-only note (contact admin to edit)

---

### Admin Portal

**Overview panel:**
- [ ] 4 stat cards (at least one per status + total), each with correct color strip
- [ ] Member table: search input + filter dropdown
- [ ] Table columns: name, type/role, plan, progress bar + value, status badge, last activity
- [ ] Filter and search actually work (JS filters array + re-renders)
- [ ] Empty state when no results

**Review queue (submitted items):**
- [ ] 3 tabs: Pending (count badge) / Approved / Rejected
- [ ] Pending: cards with approve + reject buttons
- [ ] Approved/Rejected: cards with final status badge (no action buttons)
- [ ] Approve/Reject mutates data array, re-renders, updates count badges
- [ ] Empty state on pending tab after all reviewed

**New member review:**
- [ ] Same 3-tab pattern
- [ ] Pending cards: name, email, submission date, key verification value (DM Mono large), all submitted fields in detail grid
- [ ] Same interactivity as review queue

**Notification center:**
- [ ] One section per status group (danger / warning)
- [ ] Section header + bulk "Send All" button
- [ ] Member rows: name + current value + individual "Send reminder" button
- [ ] Buttons show `alert()` feedback
- [ ] Empty state with celebratory message when clean

---

## JavaScript Patterns

Vanilla JS only. No frameworks. All data hardcoded in arrays at the top of the `<script>` block.

```javascript
// Tab/nav switching
function switchNav(el, panel) {
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + panel).classList.add('active');
  const titles = { overview: 'Overview', /* ... */ };
  document.getElementById('page-title').textContent = titles[panel] || panel;
}

// Within-panel tab switching
function switchTab(el, section, tab) {
  el.closest('.tabs').querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  renderSection(section, tab);  // call appropriate render fn
}

// Approve/reject
function actReview(id, newStatus) {
  allItems.find(i => i.id === id).status = newStatus;
  renderReviewList('pending');
  updateBadges();
}

// Filter + search
let currentFilter = 'all', currentSearch = '';
function renderTable() {
  let data = allMembers;
  if (currentFilter !== 'all') data = data.filter(m => m.status === currentFilter);
  if (currentSearch) data = data.filter(m => m.name.toLowerCase().includes(currentSearch.toLowerCase()));
  if (!data.length) {
    document.getElementById('table-wrap').innerHTML = '<div class="empty">No results found.</div>';
    return;
  }
  // render table rows
}

// Progress ring
const r = 40, circ = 2 * Math.PI * r;  // ≈ 251.33
const offset = circ * (1 - Math.min(pct, 100) / 100);

// Form submit with validation
function submitForm() {
  const name = document.getElementById('f-name').value.trim();
  if (!name /* check others */) { alert('Please fill all required fields (*)'); return; }
  clearForm();
  const banner = document.getElementById('submit-success');
  banner.style.display = 'block';
  setTimeout(() => banner.style.display = 'none', 4000);
}
```

---

## HTML File Structure

Both files are **fully self-contained** — no external files beyond CDN links.

```html
<!DOCTYPE html>
<html lang="[language code]">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[App Name] — [Portal]</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    /* CSS variables + all component styles */
    /* Note: pure custom CSS, no Tailwind needed — the component system above is self-sufficient */
  </style>
</head>
<body>
  <!-- layout + panels -->
  <script>
    // data arrays at top
    // render functions
    // event handlers
    // initialization calls at bottom
  </script>
</body>
</html>
```

Must work with `file://` protocol (no CORS issues, no `fetch()` calls, no network requests in JS).

---

## Phase 4 — Post-generation dialogue

After generating, show:

```
✓ Generated:
  ./prototype/member-portal.html      [if selected]
  ./prototype/admin-portal.html       [if selected]

Open both files in your browser (double-click — no server needed).

Check:
  ✓ All tabs/nav items switch correctly
  ✓ Approve/reject actions update the count badges
  ✓ Search and filter work on the member table
  ✓ Form submission shows success banner

How does it look?

  (a) Looks good — commit it
  (b) Adjust layout or colors
  (c) Add, remove, or rename sections
  (d) Regenerate with different fake data
  (e) Something specific needs fixing — describe it
```

Handle each response:
- **(a)**: run git commit (see below)
- **(b)**: ask which layout/color to change, update the relevant CSS variables or layout structure, regenerate
- **(c)**: ask what to add/remove/rename, update the section list, regenerate
- **(d)**: regenerate only the data arrays with fresh domain-appropriate values, keep HTML structure
- **(e)**: apply the described fix, show what changed, re-prompt

Stay in the dialogue loop until the user picks (a) or explicitly says they're done.

---

## Git commit (after user confirms)

```bash
git add prototype/member-portal.html prototype/admin-portal.html
git commit -m "feat: add UI prototype (member portal + admin portal)"
```

Only run after explicit confirmation from the user.

---

## Implementation notes

- The `prototype/` directory is **not** in `.gitignore` — the prototypes are a design artifact to be committed and shared
- If `springboot-scaffold` has already been run, still write to `./prototype/` — these files are not part of the app source tree
- If the user is running this skill after the backend is partially built, they may want to compare the prototype to the actual rendered pages — mention this as a quality check option
