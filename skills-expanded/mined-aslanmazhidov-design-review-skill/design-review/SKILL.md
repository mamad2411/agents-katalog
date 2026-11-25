---
name: design-review
description: Visual design review of an HTML file or URL using Playwright MCP. Opens the page in a real browser, captures desktop / tablet / mobile screenshots, audits typography, contrast, rhythm, spacing, hierarchy, color, and alignment, and proposes concrete fixes. With user consent — applies them in place. Trigger when the user says "review this design", "how does this look", "what's wrong with the layout", or invokes "/design-review".
---

# Design Review Skill

Turns Claude into a design reviewer that **sees** the result instead of guessing from the code.

## When to invoke

- The user asks to review an HTML page, landing, or artifact
- After generating new HTML — proactively offer a review
- The user complains that something looks "off", "ugly", or "broken"

## Dependencies

- **Playwright MCP** (`@playwright/mcp`) must be installed and connected. Verify by checking for tools prefixed with `mcp__playwright__*`.
- If Playwright MCP is unavailable — tell the user and offer to install it:
  ```bash
  claude mcp add playwright -- npx -y @playwright/mcp@latest
  ```

## Arguments

The skill accepts:

- A local file path (for example `./index.html` or `~/site/index.html`) — open via a `file://` URL
- A URL (`http://...` or `https://...`) — open as-is
- If nothing is passed — ask the user for a path or URL before continuing

## Workflow

### 1. Open the page

Use `mcp__playwright__browser_navigate` to load the page.

### 2. Capture screenshots at three widths

Use `mcp__playwright__browser_resize` followed by `mcp__playwright__browser_take_screenshot`:

- **Desktop**: 1440 × 900
- **Tablet**: 768 × 1024
- **Mobile**: 375 × 812

Save the screenshots into a `.design-review/` folder next to the file under review, with clear names (`desktop.png`, `tablet.png`, `mobile.png`).

After capturing them — **read them back through the Read tool** to actually look at the result. This step is critical: without reading the screenshots, you are not *seeing* the design.

### 3. Snapshot the DOM

Use `mcp__playwright__browser_snapshot` to grab the accessibility tree — it exposes hierarchy and semantics without the noise of raw HTML.

### 4. Audit by checklist

Walk through these axes; for each, log concrete findings (with section and coordinates, not vague observations):

**Typography**
- Size hierarchy (h1 → h2 → h3 → body) — is the contrast clear?
- Line-height for long-form text (target 1.4–1.7)
- Line length (50–75 characters is optimal)
- Font pairing — any conflicts?

**Color & contrast**
- Text-to-background contrast (WCAG AA: 4.5:1 for body, 3:1 for large text)
- Palette — no more than 3–4 accents
- States (hover, active, disabled) — are they visible?

**Rhythm & space**
- Vertical rhythm between sections
- Section padding — anything cramped?
- Spacing scale — multiples of 8 / 16 / 24 / 32 / 48 / 64?
- Breathing room around CTAs?

**Composition & hierarchy**
- What hits the eye first? Is that the primary message?
- F-pattern / Z-pattern legible?
- Grouping by proximity working?
- Alignment — is the grid respected?

**Responsive**
- On mobile, does anything overflow the viewport?
- Mobile font sizes readable (≥ 14–16 px for body)?
- Touch targets ≥ 44 × 44 px?
- Hero not cropped on mobile?

**Polish**
- Border-radius consistent?
- Shadows — soft and natural, not flat?
- Icons consistent in style and weight?
- Images sharp, not stretched?

### 5. Deliver the report

```
## Design Review: <file>

### What's working
- ...

### Critical issues (must fix)
1. **<section> — <issue>**
   Why: ...
   Fix: <concrete CSS or HTML>

### Recommended improvements
1. ...

### Screenshots
- Desktop: .design-review/desktop.png
- Tablet: .design-review/tablet.png
- Mobile: .design-review/mobile.png
```

### 6. Offer to apply fixes

At the end, ask: **"Apply the critical fixes now?"**

If yes — walk through the list, edit the source via the Edit tool, then re-run `/design-review` on the same file to verify the result.

## Rules

- **Never guess from code.** Always open the page in the browser and look at the screenshots. The skill is useless without the visual step.
- **Be specific, not vague.** Not "bad typography" — but "h1 in the hero is 32 px while body is 18 px; the hierarchy is weak, bump h1 to at least 56 px".
- **Respect the user's design system.** Before editing, check for design tokens or variables already in the project (CSS custom properties, theme files, etc.) and reuse them instead of inventing new values.
- **Don't break the existing theme.** If the page uses a specific palette or aesthetic, fixes should land inside it.
- After any fix — **always re-run the review** on the same file. One pass rarely gets to perfect.

## Example invocation

```
/design-review ./index.html
```

or just:

```
/design-review
```

(then ask the user for the path)

---

🇷🇺 Russian version: [SKILL.ru.md](SKILL.ru.md)
