---
name: portfolio-animations
description: "Implement GSAP timelines and scroll-linked effects."
---

# portfolio-animations

GSAP with @gsap/react is the existing animation stack; avoid additional animation libraries without an accepted reason. Scope selectors/timelines, clean up matchMedia/ScrollTriggers, and prevent duplicate drivers of the same property.

Keep animation hooks feature-local when cohesive. Provide reduced-motion and usable initial states. If elements start hidden, explicitly reveal visibility as well as opacity; do not leave content invisible with an opacity-only animation. Coordinate DOM refs and scene inputs before parallel work.
