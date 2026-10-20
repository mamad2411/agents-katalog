---
name: invision-style-storefronts
description: Master skill for creating high-converting, Invision Community (IPS / Nexus) and Tomware-style dark gamer storefronts for SellAuth, Next.js, and custom HTML. Use when asked to build or customize gaming cheat stores, software marketplaces, game hubs, or Invision/Nexus themes.
risk: low
source: custom
---

# Invision Style Storefronts & Gaming Marketplaces

Build elite Invision Community (IPS / Nexus), Tomware, and BearCheats style storefronts optimized for game cheats, software marketplaces, and digital downloads.

## Core Architectural Blueprint

### 1. Aesthetic DNA & Visual Tokens
- **Base Background**: Deep Obsidian / Midnight Slate (`#0a0d14`, `#0d1117`, `#0e121a`).
- **Surface Layering**: Glassmorphism cards with `rgba(255, 255, 255, 0.05)` to `rgba(255, 255, 255, 0.1)` backgrounds and 1px crisp semi-transparent borders (`rgba(255, 255, 255, 0.08)`).
- **Accents**: Neon Cyber accents — Orange (`#f97316`), Electric Purple (`#9333ea`), Toxic Green (`#22c55e`), Cyan (`#06b6d4`).
- **Hero Section**: Hardware-accelerated Faststart WebM/MP4 streaming background overlaid with bottom gradient fade (`linear-gradient(to top, rgb(var(--cl-background)), transparent 70%)`).
- **Card Hierarchy**:
  - **Category / Game Groups**: Dual-layer artwork stack (Primary Artwork -> Action/Character Hover Artwork) with 0.4s-0.5s smooth crossfade and subtle `1.03x` scale.
  - **Individual Cheat Cards**: Dedicated cheat poster, status badge (`UNDETECTED`, `UPDATING`, `TESTING`), starting price pill, and high-contrast "Buy Now" CTA.

---

## Critical Rules & Pitfalls

> [!CAUTION]
> **Avoid Tailwind Purge Traps in SellAuth**:
> SellAuth themes pre-compile Tailwind CSS at build time. Arbitrary classes like `group-hover:opacity-100` are PURGED from production stylesheets if not in the initial build. Always use scoped `<style>` blocks or explicit CSS classes (e.g. `._obh:hover .groupImage_secondary`).

> [!WARNING]
> **Never Let Dual-Image Containers Collapse**:
> Never set both images in a card to `position: absolute` without an explicit height. The primary image must remain `position: relative; width: 100%; height: auto; display: block;` to naturally establish container height, while the secondary image uses `position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0;`.

> [!TIP]
> **Hero Video Optimization**:
> Never use raw 50MB+ GIFs. Always use lightweight (under 1MB) WebM/MP4 video files with `playsinline autoplay loop muted preload="auto"` streamed from high-speed CDNs (Catbox, Discord CDN, R2, S3, or SellAuth Theme Assets).

---

## Component Implementation Library

Load specific references based on the implementation stack:

| Stack / Need | Reference File |
|---|---|
| Complete SellAuth Theme Integration (`hero.njk`, `products.njk`, `group-card.njk`, `product-card.njk`) | `references/sellauth-architecture.md` |
| Standalone HTML/Tailwind/CSS Components (News Banner, Cheat Cards, Modals) | `references/standalone-components.md` |
| Design Tokens, Color Palettes & Pure CSS Animations | `references/design-tokens-and-css.md` |

---

## Quick Workflow Checklist for New Client Projects

1. **Brand & Color Theme Selection**: Determine client accent color (Orange, Purple, Blue, Green, Red).
2. **Hero Setup**: Integrate lag-free background video (`hero.njk`) with radial gradient fade and headline bindings.
3. **News & Payment Methods Banner**: Add `.newsBanner.ipsBox` showcasing instant payment gateways (ApplePay, CashApp, Crypto, PayPal, Cards) and Discord CTA.
4. **Group Categories Grid**: Configure `group-card.njk` with dual-image crossfade for top games (Apex, Rust, COD, CS2, Fortnite, Arc Raiders, R6, Valorant, Spoofer, Marvel Rivals).
5. **Cheat Product Cards**: Configure `product-card.njk` with clean status badges (`UNDETECTED`), price formatting, and modal buy buttons.
6. **Live Validation**: Test hover-in, hover-out, mobile responsive wrap, and modal click triggers.
