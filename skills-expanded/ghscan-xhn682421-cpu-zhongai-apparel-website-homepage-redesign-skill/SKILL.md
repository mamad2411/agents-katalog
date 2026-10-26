# Diyuan Apparel Homepage Redesign Skill

Use this workflow when redesigning or substantially improving the Diyuan Apparel homepage without changing its B2B factory positioning or verified content.

## Objective

Help an overseas buyer understand within the first viewport:

1. What Diyuan Apparel manufactures
2. Where the factory is located
3. Why the production setup is credible
4. Whether OEM/ODM support is available
5. How to send an inquiry

## Required Homepage Rhythm

1. **Hero**: Diyuan Apparel, Yiwu factory positioning, seamless underwear and sportswear, OEM/ODM CTA, real factory/product visual placeholder.
2. **Data strip**: 70 machines, product focus, OEM/ODM, AQL 2.5 OQC.
3. **Product categories**: underwear, women's panties, activewear, sports bra, yoga wear.
4. **Factory proof**: knitting, cutting/sewing, finishing, laboratory/washing, needle detection, showrooms.
5. **OEM/ODM process**: inquiry through shipment.
6. **Quality control**: yarn, raw white fabric 100%, dyed fabric 100%, garment 100%, AQL 2.5, needle detection.
7. **FAQ and inquiry CTA**.

## Composition Rules

- Build a stronger hero with asymmetry, depth, and a clear visual focal point.
- Use gradient backgrounds sparingly and only to support hierarchy.
- Replace repeated plain cards with a mix of data blocks, media bands, timelines, and bordered lists.
- Use `lucide-react` icons for capabilities, not as decoration.
- Add product-card hover feedback without making the site feel retail-oriented.
- Keep the brand or manufacturing offer visible in the first viewport.
- Preserve a hint of the next section on common desktop and mobile screens.

## Implementation Workflow

1. Read `AGENTS.md`, current homepage sections, and this design system.
2. Audit repeated content before changing layout.
3. Define the new section order and visual hierarchy.
4. Reuse existing components and data where practical.
5. Add motion only after the static layout is correct.
6. Keep English and `/zh` structures aligned when both versions are updated.
7. Use local placeholders until real assets are supplied.

## Conversion Rules

- Use `Send Inquiry` as the primary CTA.
- Use `View Products` or `Get OEM/ODM Support` as secondary CTAs.
- Keep factory facts close to relevant CTAs.
- Do not add fake urgency, testimonials, logos, certifications, or buyer counts.

## Validation

- Confirm one H1 and correct metadata.
- Check CTA destinations and language switching.
- Check 390px mobile and wide desktop layouts.
- Verify motion does not cause layout shift.
- Run `npm run lint` and `npm run build`.
