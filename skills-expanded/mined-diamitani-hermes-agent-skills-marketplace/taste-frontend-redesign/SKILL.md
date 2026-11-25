---
name: taste-frontend-redesign
description: Taste-driven frontend redesign with dual quality-control agents. Use when the user asks to redesign, restyle, or apply "taste", "taste-skill", "high-end", or "aesthetic" directives to an existing frontend project.
version: 1.0.0
---

# Taste-Driven Frontend Redesign

You are a taste-driven frontend redesign specialist. Your job: take an existing frontend project, apply Leonxlnx/taste-skill design directives, and produce a $150k-agency-tier result — validated by quality control agents.

## When to Load This Skill

Load this skill when the user:
- Says "use taste skill", "taste-skill", "taste frontend", or "high-end design"
- Asks to redesign/restyle an existing frontend with aesthetic direction
- Requests "$150K agency quality" or "high-end visual design"
- Mentions `npx skills add Leonxlnx/taste-skill`
- Wants to apply specific taste parameters (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY)

## Prerequisites

Install the taste skills BEFORE beginning any work:

```bash
npx skills add Leonxlnx/taste-skill --yes --skill design-taste-frontend-v1
npx skills add Leonxlnx/taste-skill --yes --skill high-end-visual-design
```

Then load both skills via `skill_view` to get the full directives.

## The Pipeline (5 Phases)

### Phase 1: Audit Existing Frontend

Read the existing project files to understand:
- Current framework (Next.js, React, etc.)
- Styling approach (Tailwind, CSS modules, etc.)
- Component structure and page count
- Current color palette, fonts, layout patterns
- What needs redesign vs what stays

### Phase 2: Compile Taste Directives

Extract from the loaded taste skills and user input:

```yaml
taste_params:
  DESIGN_VARIANCE: <1-10>    # 1=Symmetry, 10=Artsy Chaos
  MOTION_INTENSITY: <1-10>   # 1=Static, 10=Cinematic
  VISUAL_DENSITY: <1-10>     # 1=Airy, 10=Cockpit/Packed

vibe_archetype: "Ethereal Glass | Editorial Luxury | Soft Structuralism"
layout_archetype: "Asymmetrical Bento | Z-Axis Cascade | Editorial Split"

mandatory:
  fonts: "Geist + JetBrains Mono (Inter BANNED)"
  icons: "@phosphor-icons/react (NOT lucide-react)"
  background: "#050505 or #020617 (NEVER #000000)"
  accent: "SINGLE accent color — cyan #22d3ee recommended"
  hero: "NO centered heroes when DESIGN_VARIANCE > 4"
  grids: "NO 3-column equal card grids"
  purple: "BANNED — no purple/violet gradients or glows"
  emoji: "BANNED — zero emojis in code, text, or markup"

card_architecture:
  pattern: "Double-Bezel (db-outer → db-inner)"
  outer: "rounded-[2rem], hairline border, p-1.5"
  inner: "shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)], smaller radius"

button_pattern: "Button-in-Button (rounded-full pill + nested icon circle)"

motion:
  library: "framer-motion"
  physics: "type: spring, stiffness: 100, damping: 20"
  transitions: "cubic-bezier(0.32,0.72,0,1)"
  reveals: "staggerChildren + whileInView with delay cascade"
  perpetual: "pulse, float, typewriter, carousel on dashboard cards"

forbidden:
  fonts: ["Inter", "Roboto", "Arial", "Open Sans", "Helvetica"]
  icons: ["lucide-react", "FontAwesome", "Material Icons"]
  colors: ["purple gradients", "blue-purple combos", "pure #000000"]
  layouts: ["text-center hero", "grid-cols-3 equal cards", "h-screen"]
  motion: ["linear easing", "ease-in-out", "window.addEventListener('scroll')"]
  content: ["emojis", "John Doe", "Acme", "99.99%", "Seamless/Elevate/Unleash"]
```

### Phase 3: Delegate Redesign

Use `delegate_task` to send the redesign to a specialist sub-agent with ALL taste directives in the context. The context must include:
1. The full taste parameter block above
2. The specific vibe and layout archetypes chosen
3. List of all files to rewrite
4. The forbidden patterns list
5. Existing project files for reference

Example delegation:

```
delegate_task(
    goal="Redesign the [project] dashboard using taste-skill directives...",
    context="[full taste params + archetypes + forbidden list + file paths]",
    toolsets=["file", "terminal"]
)
```

### Phase 4: Dual QC Agents

After the redesign, launch TWO quality control agents in parallel:

**Technical QC Agent** — line-by-line violation scan:
- Check every font declaration for banned fonts
- Check every gradient for purple
- Check every grid for 3-column equal cards
- Check every hero for centered text
- Verify `@phosphor-icons/react` imported, not `lucide-react`
- Verify `framer-motion` in package.json with spring physics
- Verify `min-h-[100dvh]` instead of `h-screen`
- Verify Double-Bezel pattern present on cards
- Verify no `window.addEventListener('scroll')`
- Verify no emojis in any file
- Verify no `backdrop-blur` on non-fixed elements
- Return: PASS/FAIL for each check with file:line

**Visual QC Agent** — 8-dimension aesthetic rating (scale 1-10):
1. Vibe Fidelity — Does it match the chosen archetype?
2. Layout Uniqueness — Asymmetrical bento, no generic patterns
3. Haptic Depth — Double-Bezel feel, shadows, materiality
4. Motion Quality — Spring physics, staggered reveals
5. Typography — Font pairing, size hierarchy, tracking
6. Originality — No AI slop patterns
7. Spacing & Rhythm — Macro-whitespace, breathing room
8. Overall Polish — Production-ready, "$150K agency" impression
- Return: Score per dimension + final verdict (SHIP IT / NEEDS REVISION)

Use parallel dispatch:
```
delegate_task(tasks=[
    {goal: "Technical QC scan...", context: "...", toolsets: ["file"]},
    {goal: "Visual quality rating 1-10...", context: "...", toolsets: ["file"]}
])
```

### Phase 5: Fix and Verify

1. Read both QC reports
2. Fix ALL technical QC failures first (concrete, faster)
3. Address any fatal visual QC issues (scores < 5)
4. Re-verify fixes with targeted reads
5. Report final status with before/after comparison

## Anti-Patterns (Pitfalls)

### False QC Positives
The QC agents may flag things that aren't actually violations:
- A `lucide-react` import claim might be wrong if the file was already rewritten — RE-READ the actual file before fixing
- An import-error claim ("X not exported from mock") might be stale if mock data was updated — verify directly
- A "3-column grid" claim might be about stat cards (4-columns, which is fine) — check context

### Sub-Agent Race Conditions
The redesign sub-agent and QC agents run in parallel. The QC may read OLD files if the redesign hasn't finished. Always re-read files after QC before applying fixes.

### Over-Patching
Don't apply patches to files the redesign sub-agent has already rewritten. The sub-agent's version may already be correct. Read first, verify, then patch only if the violation is confirmed.

## Quality Checklist

Before delivering to the user:
- [ ] All technical QC failures resolved or confirmed as false positives
- [ ] No banned fonts, colors, layouts, or motion patterns remain
- [ ] Double-Bezel present on major cards
- [ ] Button-in-Button CTAs
- [ ] Framer Motion springs (stiffness: 100, damping: 20)
- [ ] Staggered reveals (whileInView + delay cascade)
- [ ] Geist + JetBrains Mono font pairing
- [ ] @phosphor-icons/react for all icons
- [ ] Single accent color, no purple, no emojis
- [ ] Dashboard feels "$150K agency" — not "template with nice fonts"
