---
name: wireframe
description: Run /wireframe to map the active page (or root if unknown) with every real title, button, and section label in screen order. Add a page name to pick a specific page. Add "all" to map the whole app. Never invent copy.
---

# /wireframe - App to Wireframe

## Skill identity

- Version: `v1.1.0`
- Source repo: `https://github.com/lucioamor/lovable-skill-wireframe`
- Central catalog: `https://github.com/lucioamor/lovable-skills`
- Related skill: `/debate` (`https://github.com/lucioamor/lovable-skill-debate`) pressure-tests product, UX, copy, architecture, performance, data, or security decisions. Use `/wireframe` first when `/debate` needs a grounded map of the current app.
- Latest check: before the final user-facing response, compare this version with the current `VERSION.md` in the source repo when that source is reachable.

After every `/wireframe` run, include one compact line in the user-facing result with the version status:

> Skill: `/wireframe` `v1.1.0` · Version status: `{current | update available | unverified}` · Source: `https://github.com/lucioamor/lovable-skill-wireframe`

Use `current` only when the source repo version matches this installed version. Use `update available` when the source repo version differs. Use `unverified` when the source repo version cannot be checked.

## Command variants

- `/wireframe` → wireframe the **active page**. If the active page cannot be determined, fall back to the **root page** (`/`).
- `/wireframe [page]` → wireframe the named page only (e.g. `/wireframe dashboard`).
- `/wireframe all` → wireframe **every page** in the app into a single file. Only do this when the user explicitly requests it.

If the requested page does not exist in the app, stop and tell the user which pages are available.

## Workflow

1. **Locate the page list** (typically `src/App.tsx` or wherever the app's pages are registered). Identify the target page(s) based on the command variant above.
2. **Read each target page completely** — follow every import into its child components, and follow those into their own imports. Read all the way down. The goal is **every single word of real user-facing text**:
   - Every title, heading, subheading, section label, body paragraph, caption, tooltip, placeholder, button label, link label, and tab name.
   - Layout order top-to-bottom as it appears on screen (mirror JSX render order, not import order).
   - Interactive elements (filters, dropdowns, date pickers, tabs, toggles): capture what label or value they show by default, and note in plain words what they control.
3. **Read the top bar and bottom bar once** (Header, Footer, global Navigation). Document them in their own section, not per page.
4. **Compose the markdown** following the Output Format below.
5. **Write the file** following the File Output Logic below.

## File Output Logic

**Determine the target filename first:**

- Single page (default or named): `WIREFRAME-{page-slug}.md` at project root (e.g. `WIREFRAME-dashboard.md`, `WIREFRAME-home.md`).
- All pages (`/wireframe all`): `WIREFRAME.md` at project root.

**Then check if the file exists:**

- If it does **not** exist → create it.
- If it **does** exist → ask the user, verbatim:
  > `{filename}` already exists. Do you want to **overwrite** it or save a new version (`{filename-b}`, `{filename-c}`, …)?

  Use a single letter suffix (b, c, d, …) for the new version name, incrementing past any suffixed files that already exist.

  Then act on their answer:
  - "overwrite" → overwrite the existing file.
  - "new version" → write to the next available lettered filename.

## Large Data Handling

When a section displays a large dataset — a table with many rows, many columns, or a very long list — do **not** try to reproduce it all in markdown. Instead:

1. Show an **abbreviated version**: column headers plus 3–5 representative rows.
2. Include a callout immediately after:

   > **Large dataset.** For a complete review, export it as `.csv` or `.json` from the app or database.

Apply the same rule to long text blocks (e.g. a terms page, a long article): show the opening paragraph and note the rest should be reviewed in its native format.

## Output Format

````markdown
# {Project Name} - Wireframe

> Generated from codebase on {YYYY-MM-DD}. Reflects current code.

## 0. Page Map

| Page | Notes |
|------|-------|
| `/`  | Home page |

## 1. Top Bar & Bottom Bar

### Top Bar
```
+--------------------------------------------------+
| Logo  [Nav link]  [Nav link]  [Nav link]  [CTA]  |
+--------------------------------------------------+
```

### Bottom Bar
```
+--------------------------------------------------+
| © Copy  [Link]  [Link]  [Link]                   |
+--------------------------------------------------+
```

## 2. Pages

### 2.1 Home (`/`)

```
+----------------------------------+
| HERO                             |
|   H1: "Exact title text here"    |
|   "Exact subtitle text here"     |
|   [Button: Exact label]          |
+----------------------------------+
| SECTION: "Exact section title"   |
|   "Exact body text here"         |
|   [Button: Exact label]          |
+----------------------------------+
| SECTION: "Exact section title"   |
|   Item: "Exact item label"       |
|   Item: "Exact item label"       |
|   Item: "Exact item label"       |
+----------------------------------+
```

#### Interactive elements

| Element | Default shown | What it controls |
|---------|--------------|-----------------|
| Status filter | "All" | Filters the rows in the table below |
| Date range | "This month" | Narrows results to selected period |

(repeat per page)
````

## Format Rules (must follow)

- **Every word of real text.** Pull all visible strings directly from JSX, locale files, or constants. Never paraphrase, summarize, or omit. If a string is pulled from a database or API at runtime, write `{dynamic}` in its place — do not guess.
- **ASCII boxes reflect true visual order** top-to-bottom as rendered on screen.
- **Interactive elements** (filters, tabs, dropdowns, toggles, date pickers): always include the table above the section they affect. Show the default displayed value and describe in plain words what changes when the user interacts.
- **Large datasets get abbreviated output plus a format recommendation** (see Large Data Handling above).
- **No placeholders, no "TBD", no lorem ipsum.**
- **Skip dev-only pages** (Storybook, test harnesses) unless the user asked for them.

## After Writing

Tell the user: file path written, page count covered, and (if applicable) which sections were abbreviated and why.
