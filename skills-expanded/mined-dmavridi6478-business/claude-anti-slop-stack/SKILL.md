---
name: claude-anti-slop-stack
description: 10-rule design system from @futurewithai.dev for making Claude produce real, specific UI — use Figma references, design tokens, component libraries, and feedback loops instead of letting Claude invent everything from scratch.
---

# Claude Anti-Slop Stack
*From @futurewithai.dev*

Claude's defaults produce generic UX. This 10-rule design system makes it produce specific, production-quality UI by removing the sources of visual ambiguity one by one.

---

## Rule 1 – Stop Accepting Claude's Default Aesthetic

Claude's defaults come from its training data, not your brand. If you don't override them, every UI looks like a demo.

---

## Rule 2 – Provide References, Not Descriptions

Don't describe what you want. Show it. Descriptions are interpreted; references are copied.

```
Bad:  "Make it look modern and clean"
Good: [Attach a Figma frame or screenshot of the exact style]
```

---

## Rule 3 – Feed Claude a Real Design System

Give Claude your actual design system file. Without it, Claude invents one — and it won't match yours.

```
Attach: design-system.md or tokens.json
Tell Claude: "Use only the components and tokens in this file."
```

---

## Rule 4 – Don't Ask Claude What Good UX Looks Like

Claude will answer. The answer will be generic best-practice soup. You already know what good UX looks like for your product — tell Claude, don't ask it.

```
Bad:  "What's the best way to design this onboarding flow?"
Good: "Build this onboarding flow. It must complete in 3 steps, use our card component, and match the attached reference."
```

---

## Rule 5 – Use Design Tokens, Not Color Names

Design tokens lock Claude to your palette. Color names give Claude room to improvise.

```
Bad:  "Use a blue button"
Good: "Use --color-primary-500 (#2563EB) for the primary CTA"
```

Tokens → consistent output across every component Claude generates.

---

## Rule 6 – Figma Removes Visual Ambiguity

Figma isn't just a picture. It gives Claude structured information about what the interface is supposed to be.

Figma → Claude pipeline:
- Frames → structure
- Components → component mapping
- Variables → design tokens
- Typography → type system
- Spacing → spacing system
- Tokens → exact values

Less visual ambiguity → fewer invented decisions.

```
FIGMA REFERENCE → EXTRACT SYSTEM → MAP COMPONENTS → IMPLEMENT
```

---

## Rule 7 – Stop Letting Claude Invent Every Component

Map your existing components to Claude before you start. Then Claude assembles, not invents.

```
Tell Claude: "Use Button.tsx for all primary actions. Use Modal.tsx for all overlays.
Do not create new component files unless I ask."
```

---

## Rule 8 – Give Claude a Feedback Loop

Claude can't see the screen. Build a feedback loop into your prompt.

```
After generating:
1. Describe what looks wrong
2. Attach a screenshot if possible
3. Specify the exact fix: "The card padding is 24px, not 16px"
```

Vague feedback → vague fixes. Specific feedback → surgical fixes.

---

## Rule 9 – Lock the System, Not the Components

Don't lock every pixel. Lock the system rules. Claude has room to solve problems within constraints — that's when it's useful.

```
Lock: tokens, component library, spacing scale, type scale
Leave open: layout decisions, component composition, interaction patterns
```

---

## Rule 10 – The Anti-Slop Stack (Full System)

| Layer | What to provide |
|---|---|
| References | Figma frames, screenshots, design precedents |
| Tokens | Color, spacing, type in a tokens file |
| Components | Your existing component library |
| Rules | Explicit constraints on what Claude may or may not invent |
| Feedback | Specific, visual, iterative corrections |

When all five layers are present, Claude stops guessing and starts building.
