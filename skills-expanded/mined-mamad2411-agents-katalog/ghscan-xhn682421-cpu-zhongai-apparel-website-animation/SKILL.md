# Diyuan Apparel Animation Skill

Use this workflow when adding or reviewing motion, scroll reveals, hover transitions, or animated section entrances on the Diyuan Apparel website.

## Motion Intent

Use animation to clarify hierarchy and make technical factory content feel modern. Motion must remain quiet, fast, and secondary to readability and inquiry conversion.

## Approved Patterns

- Fade-up section entrances
- Staggered capability or product items
- Small hover lift on interactive cards
- Subtle image scale on hover
- Short opacity and position transitions
- Timeline progress or step emphasis when it improves understanding

## Avoid

- Bouncing, spinning, floating loops, or dramatic parallax
- Large zoom transitions
- Animating every text line
- Long delays that hide content
- Scroll-jacking or forced horizontal scrolling
- Motion that changes layout dimensions

## Framer Motion Rules

- Use `framer-motion` only in focused client components.
- Keep server components as the default; isolate animation boundaries.
- Prefer transforms and opacity for performance.
- Use shared variants for repeated reveal behavior.
- Keep common entrance duration around 0.35-0.6 seconds.
- Keep hover scale subtle, generally no more than `1.02`.
- Trigger scroll reveals once unless replay has a clear purpose.
- Respect `prefers-reduced-motion` with `useReducedMotion` or equivalent behavior.

## Suggested Reveal Values

```ts
const reveal = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};
```

Adjust distance and timing to the component. Do not apply one animation indiscriminately across the entire site.

## Validation

- Confirm content remains visible and usable without JavaScript animation.
- Check that motion does not delay the primary CTA.
- Test reduced-motion behavior.
- Check mobile performance and layout shift.
- Run `npm run lint` and `npm run build`.
