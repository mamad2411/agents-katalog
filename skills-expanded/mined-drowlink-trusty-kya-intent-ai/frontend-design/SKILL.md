---
name: frontend-design
description: Create distinctive, production-grade, highly engaging frontend user interfaces with purposeful motion, intentional typography, vibrant brand color palettes, and strong visual hierarchy. Use whenever designing, polishing, animating, or refining web interfaces to eliminate generic AI aesthetic clichés and elevate brand presence.
metadata:
  version: 1.0.0
---

# Frontend Design Skill

This skill guides the creation of distinctive, award-winning, production-grade web interfaces with high conviction, purposeful motion, and exceptional craft.

## 1. Brand Anchoring & Logo Dominance
- **Never hide the logo**: The brand identity is the emotional anchor. Logos should have ample breathing room, crisp resolution, subtle depth (ambient glow or glass badge), and instant recognition.
- **Full Omnipresence in Metadata**:
  - `og:image` and `twitter:image` pointing to the official logo/card.
  - `icons.icon`, `icons.shortcut`, `icons.apple` pointing to high-res icon assets.
  - JSON-LD `Organization` and `SoftwareApplication` embedding the official logo URL.
  - Manifest.json referencing the logo.

## 2. Motion & Micro-Interactions
- Use purposeful CSS animations:
  - **Ambient Drift**: Radial glow pulses and subtle mesh motion in the background.
  - **Interactive Hover Depth**: Smooth elevation lifts (`transform: translateY(-2px)`), radiant border highlights, and soft shadows.
  - **Telemetry Radar**: Pulsing status indicators and scanline sweeps for security and real-time data feeds.
  - **Smooth View Transitions**: Staggered fade-ins (`animation: fadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1)`).

## 3. Typography & Hierarchy
- Strong, deliberate contrast between headlines, subheadings, and data monospace values.
- Pair a bold display sans-serif (Inter, Plus Jakarta Sans, Outfit) with a calibrated tabular monospace font for metrics, numbers, and code.
- Avoid low-contrast or muddy gray text. Ensure WCAG AAA readability in both light and dark modes.

## 4. Light & Dark Mode Excellence
- **Light Mode**: Crisp white `#ffffff` canvas, elevated `#f8fafc` cards, subtle borders `#e2e8f0`, deep navy text `#0a192f`, and high-energy electric blue / cyan accents.
- **Dark Mode**: Deep OLED/navy `#070a11` canvas, dark elevated `#0d131f` cards, subtle borders `rgba(255,255,255,0.08)`, and neon accent glows.
