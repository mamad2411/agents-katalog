---
name: project-map
description: >
  Generates a professional, interactive HTML/React API & project map from any input — an API README,
  a list of endpoints, a project description, a feature spec, or an uploaded file. Output is a
  fully self-contained interactive widget rendered inline, ready to copy and share with a team.
  Use this skill whenever the user uploads a project file, describes a system they want to document,
  shares API routes, pastes a spec or README, or says anything like "map this", "create a map",
  "visualize this project", "make this easy to understand for developers", "generate a reference map",
  "turn this into something my team can use", or "I have a new project/feature/API to document".
  Also trigger when the user shares an API doc, backend README, or implementation spec — even
  if they don't use the word "map". The goal is always the same: turn raw project information
  into a structured, searchable, interactive reference that developers can use immediately.
---
 
# Project Map Skill
 
Turn any project input into a professional, interactive developer reference map.
 
---
 
## When This Skill Triggers
 
- User uploads any file (README, spec, API doc, feature list, schema)
- User pastes routes, endpoints, or a system description
- User says "map this", "create a map", "visualize this", "make this readable for devs"
- User describes a new project, API, or feature they need to implement
- User wants a shareable reference for their team
---
 
## Step 1 — Read & Analyze the Input
 
Before writing any code, extract the following from the user's input:
 
```
INPUT_TYPE     → api_doc | feature_spec | project_idea | schema | mixed
MODULES        → logical groupings (Auth, Products, Orders, etc.)
ENDPOINTS      → method + path + description for each route
RULES          → critical constraints, warnings, business logic
ENTITIES       → data models or key concepts mentioned
ROLES          → user roles and permissions if present
NOTES          → unconfirmed / stub sections to flag
```
 
If the input is a file, read it in full before proceeding.
If the input is a vague project idea with no routes, switch to IDEA MODE (see below).
 
---
 
## Step 2 — Choose the Map Mode
 
### MODE A — API / Endpoint Map
Use when: input has HTTP routes (GET/POST/PATCH/PUT/DELETE), sections, or endpoint lists.
 
Output structure:
- Global rules panel (currency, auth, critical warnings)
- Stats row (total endpoints, modules, roles, etc.)
- Module accordion (collapsible per logical group)
- Per endpoint: method badge + path + description + expand for details
- Search input (filters all endpoints live)
- Method filter buttons (ALL / GET / POST / PATCH / PUT / DELETE)
- Click-to-expand detail panels (params, body fields, warnings, notes)
### MODE B — Feature / Idea Map
Use when: input is a project idea, feature spec, or system description without specific routes.
 
Output structure:
- Project summary card (name, purpose, tech if mentioned)
- Module/feature grid (each feature as a card with icon, title, description)
- Data flow or dependency section if relationships are clear
- Key rules / constraints panel
- Implementation phases if a sequence is implied
- Open questions panel for unclear or unconfirmed parts
### MODE C — Mixed / Schema Map
Use when: input combines both (e.g. a full-stack spec with models + routes).
Combine both MODE A and MODE B sections, with a top-level tab or clear visual separation.
 
---
 
## Step 3 — Build the Interactive Widget
 
Use the `show_widget` tool with HTML mode. Follow ALL rules below exactly.
 
### Design Rules (non-negotiable)
 
1. **Self-contained** — no external dependencies except Tabler icons already loaded.
2. **CSS variables only** — use `var(--color-text-primary)`, `var(--color-background-secondary)`, etc.
   Never hardcode hex colors. The map must work in both light and dark mode.
3. **Flat design** — no gradients, no box shadows, no blur effects.
4. **Fonts** — `var(--font-sans)` for all text, `var(--font-mono)` for paths and code.
5. **Borders** — always `0.5px solid var(--color-border-tertiary)`.
6. **Sentence case** — all labels, headings, tags. Never ALL CAPS or Title Case.
7. **No fixed positioning** — no modals, no sticky headers. Everything in normal flow.
8. **No `display:none` during initial render** — use JS to toggle after load.
### Method Badge Colors (use these exactly)
```
GET    → background #eaf3de  color #3b6d11
POST   → background #e6f1fb  color #185fa5
PATCH  → background #faeeda  color #854f0b
PUT    → background #fbeaf0  color #993556
DELETE → background #fcebeb  color #a32d2d
```
 
### Warning / Alert Box Colors
```
Critical (blocking)  → background #fcebeb  color #501313  border #f09595
Warning (caution)    → background #faeeda  color #633806  border #f0c070
Info (note)          → background #e6f1fb  color #042c53  border #85b7eb
Success              → background #eaf3de  color #173404  border #c0dd97
```
 
### Module Icon Colors (cycle through these per module)
```
Auth         → background #e6f1fb  color #185fa5  icon: ti-lock
Products     → background #faeeda  color #854f0b  icon: ti-bowl
Categories   → background #eaf3de  color #3b6d11  icon: ti-layout-grid
Options      → background #fbeaf0  color #993556  icon: ti-list
Orders       → background #e6f1fb  color #185fa5  icon: ti-shopping-cart
Publish      → background #eaf3de  color #3b6d11  icon: ti-rocket
Links        → background #fcebeb  color #a32d2d  icon: ti-link
Settings     → background #eeedfe  color #534ab7  icon: ti-settings
Uploads      → background #e1f5ee  color #0f6e56  icon: ti-upload
Users        → background #faeeda  color #854f0b  icon: ti-users
Analytics    → background #eeedfe  color #534ab7  icon: ti-chart-bar
Misc / Other → background #eeedfe  color #534ab7  icon: ti-dots
```
For modules not listed, pick the closest color by meaning. Keep icon choices from Tabler outline set.
 
---
 
## Step 4 — Required Interactive Features
 
Every map must include ALL of these:
 
### Search
```html
<input type="text" id="searchInput" placeholder="Search..." oninput="filterItems(this.value)">
```
Filter on: path, description, tags, params. Show/hide rows. When searching, auto-expand matching modules.
 
### Method Filter (API mode only)
Buttons: ALL / GET / POST / PATCH / PUT / DELETE
Active state: `background: var(--color-text-primary); color: var(--color-background-primary)`
Default state: transparent with border
 
### Collapsible Modules
Click header → toggle endpoint list. Chevron rotates 180° when open.
Default state: all modules open.
 
### Click-to-Expand Detail Panels
Each endpoint/feature row is clickable. Clicking opens a detail panel below it showing:
- Body fields (for POST/PATCH/PUT)
- Query params (for GET)
- Response shape
- Critical warnings or notes
- Only one panel open at a time
### Stats Row
Show 3–5 key numbers at the top:
- Total endpoints / features
- Number of modules
- Number of roles (if present)
- Other meaningful counts from the input
---
 
## Step 5 — Global Rules Panel
 
Always render a 2×2 (or 2×3) grid of rule cards above the module list.
 
Each card has:
- An icon (Tabler outline)
- A short title (≤5 words)
- 2–3 lines of explanation
Extract rules from the input. Common rule types:
- Currency / units (e.g. halala, cents, grams)
- Auth (headers required, token format)
- Availability flags (isAvailable vs isActive, etc.)
- Replace-all / destructive endpoint warnings
- Protected contracts (mobile app, external API, etc.)
- Snapshot / immutability rules
If no explicit rules exist in the input, infer from context (e.g. if JWT auth is mentioned, add an auth rule card).
 
---
 
## Step 6 — Tags & Warnings
 
### Inline tags on each endpoint row
Render as small pills after the description. Extract from input:
- Query param names
- Role requirements (`admin+`, `kitchen`, `public`)
- Special behaviors (`no body`, `multipart/form-data`, `auth required`)
### Special warning tags (use sparingly, only when genuinely warranted)
```html
<!-- Replace-all warning -->
<span style="font-size:10px;padding:1px 7px;border-radius:10px;background:#faeeda;color:#854f0b;border:0.5px solid #f0c070;font-weight:500">⚠ replace-all</span>
 
<!-- Mobile / protected contract -->
<span style="font-size:10px;padding:1px 7px;border-radius:10px;background:#e6f1fb;color:#185fa5;border:0.5px solid #85b7eb;font-weight:500">🔒 protected</span>
 
<!-- Unconfirmed / stub -->
<span style="font-size:10px;padding:1px 7px;border-radius:10px;background:#f1efe8;color:#5f5e5a;border:0.5px solid #d3d1c7;font-weight:500">? unconfirmed</span>
```
 
---
 
## Step 7 — Output Quality Checklist
 
Before finalizing the widget, verify:
 
- [ ] Every endpoint/feature from the input is represented
- [ ] No hardcoded hex colors (all use CSS vars or the method/alert palettes from Step 3)
- [ ] Works in dark mode (all text uses CSS vars)
- [ ] Search filters correctly — matching modules auto-expand
- [ ] Method filter buttons work correctly
- [ ] Detail panels open/close on click — only one open at a time
- [ ] All critical warnings from the input appear as alert boxes or warning tags
- [ ] Stats row numbers are accurate
- [ ] Global rules panel is present with ≥2 cards
- [ ] Module icons are relevant (not all the same)
- [ ] No `position: fixed`, no gradients, no hardcoded pixel fonts below 11px
- [ ] `<h2 class="sr-only">` with a one-sentence screen reader summary at the top
---
 
## Idea Mode (Feature Spec / No Routes)
 
When input has no HTTP endpoints, build a feature map instead:
 
```
Feature card grid (2 columns)
  └── Icon + name + description + status badge (planned / in-progress / done)
 
Data model section (if entities described)
  └── Entity cards with key fields listed
 
Implementation phases (if sequence implied)
  └── Numbered steps, each collapsible
 
Open questions panel
  └── Anything unconfirmed or ambiguous flagged in yellow
```
 
Use the same color system, search, and CSS rules. Replace method badges with status badges:
```
planned     → background #e6f1fb  color #185fa5
in-progress → background #faeeda  color #854f0b
done        → background #eaf3de  color #3b6d11
stub        → background #f1efe8  color #5f5e5a
```
 
---
 
## Loading Messages
 
Always provide 4 loading messages to `show_widget`. Make them specific to the project:
- Line 1: what you're reading (e.g. "Reading all 26 sections...")
- Line 2: what you're extracting (e.g. "Mapping every endpoint...")
- Line 3: what you're building (e.g. "Building interactive reference...")
- Line 4: finishing up (e.g. "Almost ready...")
---
 
## Notes
 
- If the input file is very large (>500 lines), read it in full before starting. Never skip sections.
- If sections are marked "not confirmed" or "coming soon" in the source, add the `? unconfirmed` tag and collapse the module by default.
- Always prioritize developer usability: the map should answer "what endpoint do I call and what do I send?" in 2 clicks or less.
- The output widget is meant to be copy-paste ready — no extra setup needed.