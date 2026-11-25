---
name: prototype-ascii
description: Generate ASCII wireframe prototypes for UI design. Triggered when the user asks for wireframes, UI prototypes, page layouts, or screen mockups.

---

# Prototype ASCII Wireframe

## Overview

Use the provided component library to create simple ASCII wireframes for UI prototype design. Output ASCII charts only — no explanations, no code.

## When to Use
- User requests "prototype design", "wireframe"
- User wants a visual representation of a UI layout
- Output should be pure ASCII art (the chart itself should not use Markdown code blocks)

## Key Rules

**Must use component library:**
- Button: use `[ text ]` format
- Input box: use `┌──────────────────┐` / `└──────────────────┘`
- Card: use `┌─────────────┐` / `│` / `└─────────────┘`
- Modal: use `╔═══╗` / `╚═══╝` double-line border

**Alignment rules (most important):**
- **Full-width container**: use outer frame spanning full width `┌────┐`
- **Nested elements**: when using inner cards/inputs, ensure right border aligns with outer frame
- **Label + input combination**: place label **above** the input, not inside it
- **Consistent spacing**: maintain uniform margin (2-4 spaces) from border to content
- **No floating borders**: every `┐` must connect to vertical `│` lines

**Prohibited:**
- Do not use `+` at corners (use `┌` `┐` `└` `┘`)
- Do not use single horizontal line `---` (use `─` if needed)
- Do not use `+---+` style borders

## Core Patterns

### Layout Principles
1. **Grid-based**: components arranged in rows and columns
2. **Left to right, top to bottom**: standard reading order
3. **Consistent spacing**: use spaces to align elements
4. **Component-first**: select components from library first, then layout

### Component Library Reference

**Card**
```
┌─────────────┐
│ title       │
│─────────────│
│ content     │
│             │
└─────────────┘
```

**Tabs**
```
[ Active ]  Inactive  Inactive
───────────────────────────────
```

**Button**
```
[ Primary Button ]
[ Secondary Button ]
Link →
```

**Input**
```
┌──────────────────┐
│ placeholder...   │
└──────────────────┘
```

**Badge**
```
(12) [New]
```

**Progress Bar**
```
████░░░░ 58%
```

**Dropdown**
```
┌──────────────────┐
│ select-option  ▾ │
└──────────────────┘
```

**Toggle**
```
[●━━━] On
[━━━●] Off
```

**Checkbox/Radio**
```
☑ Checked
☐ Unchecked
(●) Selected
( ) Unselected
```

**Modal**
```
╔═══════════════════╗
║ title           ✕ ║
╠═══════════════════╣
║ content           ║
║                   ║
║ [cancel]  [ok]    ║
╚═══════════════════╝
```

**Avatar**
```
(JD) or [IMG]
```

**Table**
```
┌────────┬────────┐
│ field  │ field  │
├────────┼────────┤
│ data1  │ data2  │
└────────┴────────┘
```

**Icons**
```
🔍 ⚙️ 🔔 ✓ ✕
← → ▲ ▼ ▸ ▾
```

**Accordion**
```
▸ Collapsed section
▾ Expanded section
   └ Content here
```

**Status**
```
✓ Success
⚠ Warning
✕ Error
◉ Active
○ Inactive
```

**Navigation**
```
▸ Active item
  Inactive
  Inactive
```

### Quick Reference

| Component | ASCII |
|-----------|-------|
| Card | `┌────┐` `│` `└────┘` |
| Input | `┌──────┐` `└──────┘` |
| Button | `[ text ]` |
| Checkbox | `☑` / `☐` |
| Radio | `(●)` / `( )` |
| Badge | `(12) [New]` |
| Avatar | `(JD)` / `[IMG]` |
| Toggle | `[●━━━]` / `[━━━●]` |
| Modal | `╔═══╗` `╚═══╝` |
| Progress | `████░░░░ 58%` |

## Implementation Steps

### Step 1: Identify Components
List all required UI components (inputs, buttons, cards, etc.)

### Step 2: Select from Library
Match each component with the library examples

### Step 3: Layout
Arrange in reading order, maintain consistent spacing

### Example - Login Page (Correct)

```
┌─────────────────────────────────┐
│  ┌───────────────────────────┐  │
│  │          Login            │  │
│  └───────────────────────────┘  │
│                                 │
│  Username                       │
│  ┌───────────────────────────┐  │
│  │                           │  │
│  └───────────────────────────┘  │
│  Password                       │
│  ┌───────────────────────────┐  │
│  │                           │  │
│  └───────────────────────────┘  │
│                                 │
│  ☑ Remember me      [Forgot?]   │
│                                 │
│      ┌───────────────────┐      │
│      │       Login       │      │
│      └───────────────────┘      │
│                                 │
│    No account? [Register] →     │
│                                 │
└─────────────────────────────────┘
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using box-drawing chars (`+`, `-`, `\|`) instead of components | Use components exactly as in the library |
| Adding explanations | Output ASCII chart only |
| Inconsistent spacing | Use uniform margins |
| No visual hierarchy | Use larger/more prominent elements for important items |
| Floating borders (broken right border) | Use full-width outer frame, align nested elements |
| Label inside input | Place label **above** input, not inside |
| Right border not aligned | All right `│` must align vertically |

## Output Format
- Do not use Markdown code fences
- Do not add explanatory text
- Output pure ASCII art only
- If outputting to a markdown file, wrap in ``` code blocks to avoid layout issues during markdown preview.
