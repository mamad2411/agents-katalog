---
name: visual-feedback
description: >
  Visual feedback tool — annotate your page to show exactly
  what to change. Triggers: feedback, annotate, review page, mark changes,
  preview. Do NOT use for: deploying, analytics, A/B tests.
---

# Visual Feedback Skill

## Overview

Injects the [Agentation](https://agentation.dev) component into the user's
local dev server so they can visually annotate their page. The user clicks,
highlights, and comments on specific elements — then tells Claude what to
change. Agentation captures element selectors, positions, and user notes,
giving Claude exact context for surgical code edits.

Agentation is installed locally on the user's system as a dev dependency.
No MCP server required — it runs entirely in the browser.

## When To Use

- User says "let me see the page and mark what I want changed"
- User says "I want to give visual feedback"
- User says "annotate my landing page"
- User says "open the preview so I can click on what to fix"
- User says "review the page visually"
- Before deploying — user wants a final visual review
- After building a page — user wants to point at specific elements

## Prerequisites

- `agentation` package installed locally (`npm install agentation -D`)
- A running page (live at {handle}.10x.in or local dev server)
- Node.js 18+

## How It Works

1. Detects the user's framework (React, Next.js, Vite, plain HTML)
2. Injects the `<Agentation />` component into the app root (dev mode only)
3. User opens their page in the browser
4. Annotation overlay activates — user clicks elements, highlights areas,
   adds text notes directly on the page
5. User tells Claude what they marked and what they want changed
6. Claude reads the annotation data from the local session file and makes
   precise code edits targeting the exact elements
7. User refreshes to see changes, annotates again if needed

## Framework Detection & Injection

### React / Next.js / Vite (React)
```jsx
// Injected into App.tsx or layout.tsx
import { Agentation } from "agentation";

// Added before closing tag:
{process.env.NODE_ENV === "development" && <Agentation />}
```

### Plain HTML
```html
<!-- Injected before </body> -->
<script src="node_modules/agentation/dist/browser.js"></script>
<script>
  Agentation.init();
</script>
```

## Installation

Agentation is installed as a local dev dependency in the user's project:

```bash
npm install agentation -D
```

This is handled automatically by `/setup`. No cloud services, no MCP
wiring — everything runs locally in the browser.

## Workflow

```
1. User builds page with /landing-page or edits existing page
2. User runs /feedback to start visual review
3. Local page opens with annotation overlay
4. User clicks, highlights, comments on elements
5. User tells Claude what to change (annotations provide context)
6. Claude makes targeted code edits
7. User refreshes page → sees changes → annotates more or approves
8. When satisfied, user runs /deploy to push live
```

## After Feedback

- Annotations are stored in the browser session
- Each annotation includes: element selector, bounding box, user comment
- Claude uses this to make surgical edits — no guessing what the user means
- The `<Agentation />` component is only active in dev mode and never
  ships to production

## Integration with Other Skills

- **landing-page**: Build first, then `/feedback` to review
- **lp-design**: Visual feedback drives design refinements
- **lp-copy**: User can highlight text and say "change this headline"
- **lp-audit**: Run audit, then `/feedback` to verify fixes visually
- **deploy**: After visual approval, deploy to live
