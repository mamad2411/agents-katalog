# Diyuan Apparel Page Layout Skill

Use this workflow when creating or refining product, factory, OEM/ODM, quality-control, contact, or future SEO page layouts for Diyuan Apparel.

## Page Goals

Every page should answer one buyer intent, provide factory evidence, and lead to a relevant inquiry action. Keep the layout operational and easy to scan rather than editorial or retail-focused.

## Core Structure

1. Page hero with eyebrow, one H1, direct explanation, and CTA
2. Primary content answering the page's search intent
3. Verified factory or process evidence
4. Relevant internal links
5. Bottom inquiry CTA

## Layout Patterns

- Use asymmetric two-column heroes where appropriate.
- Use full-width bands to separate major information groups.
- Use data strips for machine count, inspection percentages, and AQL 2.5.
- Use timelines for OEM/ODM and quality-control sequences.
- Use media placeholders with stable aspect ratios until real images arrive.
- Use icon-based feature cards selectively for services and capabilities.
- Avoid page sections styled as floating cards and avoid cards inside cards.

## Page-Specific Guidance

- **Products**: category image, B2B description, customization, buyer type, inquiry CTA.
- **Factory**: equipment, workshop process, partner boundaries, showrooms, real images.
- **OEM/ODM**: customization scope, sample process, approvals, production workflow.
- **Quality Control**: inspection sequence, 100% checks, AQL 2.5 OQC, needle detection.
- **Contact**: company identity, direct channels, concise form, clear non-submission state until backend exists.

## Responsive Rules

- Collapse multi-column sections without changing content order.
- Keep navigation and language switching usable at 390px.
- Make buttons full-width only where mobile ergonomics benefit.
- Prevent long URLs and technical terms from overflowing.
- Keep fixed-format elements stable with grid tracks and aspect ratios.

## Content Guardrails

- Separate in-house production from qualified dyeing and finishing partners.
- Do not invent MOQ, lead time, certification, output, customer, or machine-brand claims.
- Keep English and Chinese facts synchronized.

## Validation

- Confirm one H1, metadata, canonical, and language alternates.
- Check all links and CTAs.
- Check desktop and mobile screenshots.
- Run `npm run lint` and `npm run build`.
