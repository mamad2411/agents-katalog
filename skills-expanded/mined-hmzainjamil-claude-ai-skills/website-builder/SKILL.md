# Website Builder — $10K Site From One Prompt
## Triggers: build website, build a site, create website, website builder, website from prompt, one line website, 10k website, ai website, framer motion, website-builder-setup, /website-builder-setup

---

## THE STACK (4 tools, zero coding)

| Tool | Role | Status |
|---|---|---|
| **Claude Code** | Writes entire site file by file from one prompt | ✅ Active |
| **UI/UX Pro Max** | 50+ styles, 161 color palettes, 57 font pairings — no generic AI slop | Install once |
| **Framer Motion** | Real animations: page transitions, hover effects, scroll reveals | `npm install framer-motion` |
| **21st.dev Magic** | 100+ polished React components — production-quality building blocks | `npx shadcn@latest add` |

---

## MASTER AGENT WORKFLOW

### ACTOR 1 — Brief Extractor (Kimi 8K, 0 tokens from Claude)
Extracts from user message:
- Business type + what it does
- Target audience
- Vibe/style (minimal/bold/corporate/playful/luxury)
- Key sections needed
- Brand colors (or "choose for me")
- Domain/existing assets

### ACTOR 2 — Design Director (UI/UX Pro Max skill)
- Selects style from 50+ design system options
- Picks color palette from 161 options
- Picks font pairing from 57 options
- Generates Stitch/Nano mockup prompt
- Outputs: design spec JSON for Actor 3

### ACTOR 3 — Component Selector (21st.dev MCP / Kimi K2.5)
Queries 21st.dev for:
- Hero section component
- Feature cards (3-col)
- Testimonials / social proof
- Pricing table
- CTA block
- Footer
Outputs: component URLs + HTML/CSS snippets

### ACTOR 4 — Site Builder (Claude Code — main session)
Receives: design spec + components + brief
Builds: complete Next.js + Tailwind + Framer Motion site
Structure:
```
/app
  layout.tsx      ← font + metadata
  page.tsx        ← homepage assembly
  globals.css     ← design tokens
/components
  Hero.tsx        ← animated hero (Framer Motion)
  Features.tsx    ← scroll-reveal cards
  Testimonials.tsx
  Pricing.tsx
  CTA.tsx
  Footer.tsx
/lib
  animations.ts   ← Framer Motion variants
```

### ACTOR 5 — QA & Deploy (Kimi K2.6 vision)
- Screenshots site via Playwright MCP
- Compares against design spec
- Flags: spacing drift / color mismatch / mobile breakpoints
- Auto-fix loop: 3 passes max
- Deploy command: `npx vercel --prod`

---

## ONE-PROMPT WORKFLOW (what user types)

```
Build me a premium website for [BUSINESS].
Audience: [WHO].
Vibe: [STYLE].
Colors: [HEX or "choose for me"].
Sections: Hero, Features, Testimonials, Pricing, CTA, Footer.
Use Framer Motion animations. Pull components from 21st.dev.
Apply UI/UX Pro Max design system.
Output: production-ready Next.js + Tailwind. Deploy to Vercel.
```

---

## SETUP (one-time)

```bash
# 1. Install UI/UX Pro Max
npm install -g uipro-cli && uipro init --ai claude

# 2. Install Framer Motion (in project)
npm install framer-motion

# 3. 21st.dev components (on demand)
npx shadcn@latest add [component-name]
# Browse: https://21st.dev

# 4. website-builder-setup command (already installed)
# Type: /website-builder-setup in Claude Code
```

---

## FRAMER MOTION — ANIMATION LIBRARY

```tsx
// Standard animation variants — paste into animations.ts
export const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
}
export const staggerContainer = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.15 } }
}
export const scaleIn = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.5 } }
}

// Usage in component:
import { motion } from "framer-motion"
import { fadeUp, staggerContainer } from "@/lib/animations"

<motion.section variants={staggerContainer} initial="hidden" whileInView="visible" viewport={{ once: true }}>
  <motion.h1 variants={fadeUp}>Your Headline</motion.h1>
  <motion.p variants={fadeUp}>Your copy</motion.p>
</motion.section>
```

---

## BUSINESS MODEL (AGENCY PLAY)

| Offer | Price | Delivery | Tool cost |
|---|---|---|---|
| Starter site (5 pages) | $1,500 | 2 hours | ~$0 |
| Growth site (10 pages + animations) | $3,500 | 4 hours | ~$0 |
| Premium site (custom design + CMS) | $8,000 | 1 day | ~$50 (Vercel) |
| Monthly maintenance retainer | $500/mo | Ongoing | ~$0 |

**Cold pitch:** Generate free demo site for prospect's business → DM: "Built this for you in 10 min. Want the real version?"

---

## REPOS WIRED

```
~/installed-repos/website-builder-setup/   ← official setup skill
~/installed-repos/ui-ux-design-pro-skill-main/  ← design system
~/installed-repos/ui-ux-pro-max-skill-main/     ← Pro Max version
~/installed-repos/frontend-design/              ← frontend patterns
~/installed-repos/ai-design-team/               ← design agent refs
~/.claude/commands/website-builder-setup/       ← /website-builder-setup command
```

---

## AUTO-AGENTS ACTIVATED

- **UX Architect** — CSS systems, design tokens, responsive breakpoints
- **Frontend Developer** — Next.js + Tailwind + Framer Motion build
- **UI Designer** — visual hierarchy, spacing, component selection
- **Rapid Prototyper** — fast MVP → iterate in real time
- **Kimi K2.6 QA** — screenshot diff, visual validation, mobile check
