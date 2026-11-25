---
name: references-not-moods
description: Anchor visual direction to specific named references, not adjectives; concrete coordinates beat moods the model will average away.
---

# References, not moods

"Make it bold" is a mood, and the model will average it into something safe. "In the spirit of Emigre magazine, 1994" or "like the type system on Koto.studio" gives actual coordinates to work from. Specific references steer; adjectives drift.

## Patterns

- Name real references — designers, studios, eras, publications, products — not feelings ("clean", "modern", "premium").
- Give three reference points for a direction, plus three things the direction explicitly would NOT do.
- When a screenshot or comp exists, paste it: the model reads layout, type contrast, spacing, and color relationships from an image faster and more accurately than from prose.
- If the output is generic, the prompt was a mood. Replace it with a reference and try again.

## Examples

```text
// BAD — mood-based prompt; model averages to safe and forgettable
"Make the typography feel bold and editorial."

// GOOD — specific references give the model real coordinates
"Typography direction: early Emigre magazine (Rudy VanderLans era) — large, heavy
 grotesque headers, tight tracking, flush left. References: Emigre 1994, Koto studio
 wordmarks, Neue Haas Grotesk. NOT: web-safe fonts, centered headlines, rounded weights."
```

## Why it matters

A reference is a shared coordinate. An adjective is an invitation to average. The more specific the input, the less the model falls back to what it has seen everywhere.
