# Diyuan Apparel Design System Skill

Use this workflow when creating or reviewing visual components, tokens, cards, navigation, CTAs, or reusable patterns for the Diyuan Apparel website.

## Brand Positioning

Diyuan Apparel is a Yiwu-based seamless underwear and sportswear OEM/ODM manufacturer. Design for overseas buyers, sourcing teams, private label brands, importers, and wholesalers.

Communicate these verified strengths when relevant:

- 70 digital circular seamless knitting machines
- Seamless underwear and sportswear production
- OEM/ODM private label support
- AQL 2.5 outgoing quality control
- Yiwu-based manufacturing
- Underwear and sportswear showrooms

Do not invent certifications, customers, output, MOQ, lead time, machine brands, or performance claims.

## Visual Direction

Use **Modern Seamless Tech Factory** as the visual concept:

- Modern, technical, premium B2B
- Factory-direct and trustworthy
- Clean but not plain
- Dynamic but not flashy
- International and activewear-inspired
- Visually connected to seamless knitting technology

Avoid generic white-gray card grids, consumer-fashion styling, fake luxury, excessive gradients, and decorative effects without business meaning.

## Color System

Build a restrained palette around:

- Deep navy or charcoal navy for primary surfaces and CTAs
- Soft ivory or off-white for warm page backgrounds
- Graphite gray for headings
- Light neutral gray for dividers and quiet sections
- One accent only: electric blue or mint green

Do not combine both accents in the same primary composition. Avoid cheap pink, bright red, and multi-color palettes.

## Component Rules

- Use `lucide-react` icons when an icon improves scanning or clarifies a capability.
- Use data blocks for machine count, inspections, and factory facts.
- Use asymmetry for hero and factory compositions when it improves hierarchy.
- Use cards only for distinct repeated items; do not nest cards.
- Keep card radius at 8px or less.
- Pair product cards with real product imagery when supplied; use local placeholders until then.
- Use strong inquiry CTAs and clear internal links.
- Use `cn()` from `@/lib/cn` for conditional Tailwind classes.

## Typography and Spacing

- Keep headings compact and factual.
- Use readable body widths and comfortable line height.
- Use strong section rhythm: large hero, compact data strip, product range, process, proof, CTA.
- Do not scale type directly with viewport width.
- Verify long English and Chinese text at mobile widths.

## Accessibility and Validation

- Preserve semantic headings and one H1 per page.
- Use visible focus states and sufficient contrast.
- Respect reduced-motion preferences.
- Check desktop and 390px mobile layouts for overflow.
- Run `npm run lint` and `npm run build`.
