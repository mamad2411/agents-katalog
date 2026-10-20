---
name: maycrest-web-design
description: "Use when designing the Maycrest website or TIE Platform — building pages, components, or dashboards, choosing fonts and colors, applying the brand aesthetic, or seeking web design inspiration."
---

# Maycrest Web Design

## Overview

Design system and web design strategy for Maycrest — an Agentic-Enabled Managed Intelligence Provider serving SMBs in Indianapolis. Three service arms: Creative Services, AI Solutions, and Cybersecurity.

## Brand Identity

### Positioning
- "Enterprise intelligence at SMB prices"
- AI-augmented managed services
- Indianapolis-rooted, nationally capable
- Not a generic MSP — a strategic intelligence partner

### Visual Tone
- **Premium but approachable** — not corporate stiff, not startup casual
- **Dark-mode forward** — deep backgrounds with luminous accents
- **Data-informed aesthetic** — subtle grid patterns, node networks, clean data visualization
- **Motion with purpose** — animations that communicate, not just decorate

## Design Tokens

### Colors
```
Primary:        #0A0F1C (Deep Navy — backgrounds)
Secondary:      #1A1F35 (Elevated surfaces)
Accent:         #00D4AA (Cyber Teal — CTAs, highlights)
Accent Alt:     #7B61FF (Electric Purple — AI/innovation)
Warning:        #FF6B35 (Alert Orange — security)
Text Primary:   #F0F0F5 (Near white)
Text Secondary: #8A8FA3 (Muted)
Surface:        #12172B (Cards, panels)
Border:         #2A2F45 (Subtle dividers)
```

### Typography
- **Headlines**: Inter or Space Grotesk — clean, modern, technical
- **Body**: Inter — readable, professional
- **Code/Data**: JetBrains Mono — technical credibility
- **Scale**: 12, 14, 16, 18, 20, 24, 32, 40, 48, 64

### Spacing
- Base unit: 4px
- Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96

## Page Architecture

### Homepage
1. Hero — Bold value proposition + animated background
2. Service Arms — Three-card layout (Creative, AI, Cyber)
3. Intelligence Dashboard Preview — Interactive demo
4. Social Proof — Logos, testimonials, case study snippets
5. CTA — "Schedule Your Intelligence Briefing"

### Service Pages (x3)
- Creative Services
- AI Solutions
- Cybersecurity

Each follows: Hero → Problem → Solution → Features → Case Study → CTA

### TIE Platform Page
- Product hero with screenshot/demo
- Feature grid
- Pricing tiers
- Integration showcase
- "Request Demo" CTA

## Component Library

### Navigation
- Sticky header with glass morphism
- Service arm mega menu
- Mobile: slide-out drawer

### Hero Sections
- Full-width with particle/node animation
- Split layout (text left, visual right)
- Centered headline with gradient text

### Cards
- Service cards with icon + description
- Stat cards with animated counters
- Testimonial cards with avatar + quote
- Feature cards with hover reveal

### CTAs
- Primary button: Accent fill + subtle glow
- Secondary button: Ghost/outline
- Floating action: "Schedule Briefing" persistent

### Data Visualization
- Threat level indicators
- Service status dashboards
- ROI calculators
- Interactive timelines

## Motion Design

### Principles
- Purposeful — every animation communicates something
- Subtle — enhance, don't distract
- Performance — no jank, 60fps minimum
- Accessible — respect prefers-reduced-motion

### Patterns
- Scroll-triggered reveals (fade up, scale in)
- Number counters on viewport entry
- Hover states with depth (translateY + shadow)
- Page transitions (cross-fade between routes)
- Loading states (skeleton screens, not spinners)

## Competitive Positioning

Maycrest should look NOTHING like:
- Generic MSP sites (stock photos of headsets, blue gradients)
- Cookie-cutter IT company templates
- Overly complex enterprise software sites

Maycrest should feel like:
- A premium SaaS product (Linear, Vercel, Stripe)
- A design-forward consultancy (IDEO, Pentagram)
- A modern intelligence platform (Palantir, CrowdStrike)

## DESIGN.md — Authoritative Design System Reference

The Maycrest Digital website has a comprehensive `DESIGN.md` file at the repo root (`website/DESIGN.md`) that codifies the entire design system in the Google Stitch 9-section format. This file is the **single source of truth** for AI coding agents when generating UI.

**When building or modifying Maycrest web pages:**
1. Reference `DESIGN.md` for exact token values (colors, typography, spacing, shadows, motion)
2. Use the card hierarchy documented there: `.observation-window` → `.glass-card` → `.intel-card` → `.story-card` → `.cta-card`
3. Follow the Agent Prompt Guide (Section 9) for component generation patterns
4. The design tokens in this skill file are strategic — DESIGN.md has the precise implementation values

**Key DESIGN.md specifics not in this skill:**
- Fluid typography scale using `clamp()` (not fixed px values)
- Glass morphism blur hierarchy (24px → 16px → 12px)
- Accent glow shadow system per service arm
- Section spacing classes (`.section-hero`, `.section-feature`, `.section-proof`, `.section-cta`)
- Framer Motion patterns with exact easing curves

The `maycrest-create:design-system-architect` skill owns DESIGN.md creation and auditing.

## Rules

- Dark mode is the primary experience
- No stock photography — use illustrations, icons, data viz
- Every page must have a clear single CTA
- Mobile-first responsive design
- Performance budget: < 3s LCP, < 100ms FID
- Accessibility: WCAG AA minimum
- All animations respect prefers-reduced-motion
- Always reference `DESIGN.md` for exact implementation values when building components
