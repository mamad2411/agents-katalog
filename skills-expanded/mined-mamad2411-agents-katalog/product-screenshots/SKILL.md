---
name: product-screenshots
description: "Capture and maintain product screenshots for marketing and support use. Use when you need to capture UI screenshots, refresh outdated screenshots, or check if screenshots need updating after UI changes. Triggers on: capture screenshots, update product images, refresh screenshots, screenshot the feature, marketing screenshots."
---

# Product Screenshots Skill

Capture and maintain product screenshots for use in marketing pages and support articles.

---

## The Job

1. Determine what screenshots are needed
2. Check the screenshot registry for existing screenshots
3. Capture new or updated screenshots using Playwright
4. Update the registry
5. Report what was captured and where it's used

---

## Screenshot Registry

Location: `docs/marketing/screenshot-registry.json`

This file tracks all product screenshots, their capture configuration, source components, and usage locations.

### Registry Structure

```json
{
  "screenshots": [
    {
      "id": "calendar-month-view",
      "description": "Calendar showing month view with events",
      "path": "public/screenshots/calendar-month-view.png",
      "captureConfig": {
        "url": "/dashboard/calendar?view=month",
        "viewport": { "width": 1280, "height": 800 },
        "theme": "light",
        "waitFor": "[data-testid='month-view']",
        "actions": []
      },
      "sourceComponents": [
        "apps/web/components/calendar/MonthView.tsx"
      ],
      "usedIn": [
        { "type": "marketing", "location": "/features/scheduling" },
        { "type": "support", "article": "calendar-views" }
      ],
      "lastUpdated": "2026-02-18T10:00:00Z",
      "gitHash": "abc123"
    }
  ]
}
```

---

## Capture Modes

### Mode 1: Capture New Screenshot

When you need a screenshot that doesn't exist:

1. Define the capture configuration:
   - **URL**: Which page to capture
   - **Viewport**: Size (default 1280x800)
   - **Theme**: light or dark (default light for marketing)
   - **Wait for**: Selector to ensure content loaded
   - **Actions**: Any interactions before capture

2. Invoke @screenshot-maintainer:

```
@screenshot-maintainer: Capture new screenshot.

ID: calendar-week-view
Description: Calendar showing week view with resources
URL: /dashboard/calendar?view=week
Viewport: 1280x800
Theme: light
Wait for: [data-testid='week-view']
Actions:
  - wait 500

Source components:
  - apps/web/components/calendar/WeekView.tsx
  - apps/web/components/calendar/ResourceColumn.tsx

Will be used in:
  - Marketing: /features/scheduling
```

3. Screenshot will be saved to `public/screenshots/[id].png`

4. Registry will be updated automatically

### Mode 2: Check for Updates

After UI changes, check if screenshots need refreshing:

1. Invoke @screenshot-maintainer:

```
@screenshot-maintainer: Check and update screenshots.

Changed files:
- apps/web/components/calendar/MonthView.tsx
- apps/web/components/calendar/EventBlock.tsx
```

2. The maintainer will:
   - Check which screenshots have these files in sourceComponents
   - Regenerate affected screenshots
   - Update registry timestamps
   - Report what was updated

### Mode 3: Full Refresh

To regenerate all screenshots:

```
@screenshot-maintainer: Full refresh of all screenshots.
```

---

## Capture Actions

Use these action types in `captureConfig.actions`:

| Action | Format | Example |
|--------|--------|---------|
| Wait | `{ "type": "wait", "ms": 500 }` | Wait 500ms |
| Click | `{ "type": "click", "selector": "button" }` | Click element |
| Type | `{ "type": "type", "selector": "input", "text": "..." }` | Type text |
| Hover | `{ "type": "hover", "selector": ".menu" }` | Hover element |
| Wait for selector | `{ "type": "waitForSelector", "selector": ".modal" }` | Wait for element |
| Scroll | `{ "type": "scroll", "y": 200 }` | Scroll down |
| Evaluate | `{ "type": "evaluate", "script": "..." }` | Run JS |

### Example: Capture Modal

```json
{
  "url": "/dashboard/calendar",
  "actions": [
    { "type": "click", "selector": "[data-testid='create-event']" },
    { "type": "waitForSelector", "selector": "[role='dialog']" },
    { "type": "wait", "ms": 300 }
  ]
}
```

### Example: Capture Dropdown Open

```json
{
  "url": "/dashboard",
  "actions": [
    { "type": "click", "selector": "[data-testid='profile-dropdown']" },
    { "type": "wait", "ms": 200 }
  ]
}
```

---

## Screenshot Best Practices

### For Marketing

- **Use light mode** — Better readability in most contexts
- **1280x800 viewport** — Standard desktop size
- **Show realistic data** — Not empty states
- **Capture key workflows** — Creation, editing, views
- **Keep UI clean** — No debug overlays or dev tools

### For Support Articles

- **Focus on relevant area** — Can crop or use element screenshot
- **Show the specific step** — Match the article instructions
- **Include context** — User should know where they are
- **Consistent viewport** — Same size across article

### File Naming

Use descriptive, kebab-case names:
- ✅ `calendar-month-view.png`
- ✅ `create-event-modal.png`
- ✅ `resource-settings-panel.png`
- ❌ `screenshot1.png`
- ❌ `img_2026_02_18.png`

---

## Integration with Other Skills

### With public-page skill

When building a marketing page, the public-page skill will:
1. Check screenshot-registry.json for needed screenshots
2. If missing, invoke this skill to capture them
3. Reference screenshots in the page implementation

### With support-article-writer

When writing support articles:
1. Check if needed screenshots exist
2. If missing, invoke this skill
3. Reference screenshots in article markdown

### With developer

After completing UI stories:
1. Developer checks if modified components are in sourceComponents
2. If yes, invokes @screenshot-maintainer to update
3. Changes committed with the feature

---

## Initializing the Registry

If `docs/marketing/screenshot-registry.json` doesn't exist, create it:

```json
{
  "screenshots": []
}
```

Then add screenshots as needed using Mode 1.

---

## Common Screenshots to Capture

For a typical SaaS product, capture these key screens:

| Screenshot | What to Capture |
|------------|-----------------|
| Dashboard | Main dashboard overview |
| Calendar views | Month, week, day views |
| Create/edit forms | Event creation, settings |
| Settings panels | Key configuration screens |
| Mobile views | Responsive layout at 375px |
| Dark mode | Key screens in dark theme |

---

## Output

After capturing screenshots:

```markdown
## Screenshot Capture Report

### Captured

| ID | Path | Used In |
|----|------|---------|
| calendar-month-view | public/screenshots/calendar-month-view.png | /features/scheduling |
| event-creation-modal | public/screenshots/event-creation-modal.png | support:creating-events |

### Registry Updated

- Added 2 new screenshots
- Updated docs/marketing/screenshot-registry.json

### Notes

- Used test data from seed
- Captured in light mode at 1280x800
```
