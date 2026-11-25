# AGENTS.md - Yishe Nuxt Design & Architecture Guidelines

## UI/UX Design Intelligence (UI-UX-Pro-Max / Taste-UI)

All front-end UI design, component building, layout adjustments, and styling work in `yishe-nuxt` MUST follow **UI-UX-Pro-Max / Taste-UI** design intelligence standards (`/Users/jackie/.gemini/config/skills/ui-ux-pro-max/`).

### Core Aesthetic Guidelines:
1. **Design System & Palette (E-commerce / Luxury & Fashion)**
   - Reject generic default colors (plain red/blue/green/gray).
   - Use site-specific brand accent tokens defined in `woonuxt-theme.css`:
     - `shop-mug`: `#C4704B` (Warm Terracotta / Amber)
     - `shop-kitchen`: `#2D6A4F` (Forest Emerald)
     - `shop-painting`: `#C9A96E` (Classic Gold)
     - `shop-wall-art`: `#5B7E8A` (Slate Blue)
     - `shop-keychain`: `#6C5CE7` (Vibrant Indigo/Violet)
   - Accent CTA buttons must be high contrast (WCAG contrast ratio ≥ 4.5:1).
   - Subtle background gradients, card border-radius (8-16px), and soft ambient shadows (`0 10px 30px -10px rgba(0,0,0,0.08)`).

2. **Typography & Hierarchy**
   - Modern typography: Use Inter / Nunito with fluid typography scales via `clamp()`.
   - Maintain clear font size scale: H1 (2.5rem–3.5rem), H2 (1.75rem–2.25rem), H3 (1.25rem–1.5rem), Body (1rem/1.125rem).

3. **Motion & Transitions**
   - Subtle micro-animations for card hover: `transform: translateY(-4px)`, smooth scale transitions (`transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`).
   - Smooth image reveal and double-image hover switch logic for product cards.
   - Use `IntersectionObserver` for section scroll-in fade animations.

4. **Independent Site Layout & Components**
   - Follow Woonuxt design patterns (Hero header with overlay gradient, high-res lifestyle backgrounds, responsive category grids, multi-column layout).
   - Mobile touch targets ≥ 44px, bottom nav/header adaptability.

## Technical Architecture & Scripts

- **Framework**: Nuxt 3/4 + Tailwind CSS + PrimeVue/Headless UI
- **Sub-applications**:
  - `npm run dev:main` (Port 15201)
  - `npm run dev:card` (Port 15202)
  - `npm run dev:couplet` (Port 15204)
  - `npm run dev:mug` (Port 15206)
  - `npm run dev:kitchen` (Port 15208)
  - `npm run dev:painting` (Port 15210)
  - `npm run dev:wallart` (Port 15212)
  - `npm run dev:keychain` (Port 15214)
  - `npm run dev:mousepad` (Port 15216)

- **Guidelines**:
  - Keep `index.vue` `<script setup>` logic intact, only customize `<template>` and `<style scoped>`.
  - Use `woonuxt-theme.css` for shared design token definitions.
