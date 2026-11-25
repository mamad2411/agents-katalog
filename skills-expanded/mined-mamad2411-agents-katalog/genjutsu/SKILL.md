# Genjutsu

Award-winning UI skill for Claude Code. Build premium, polished interfaces with strong creative direction and structured layouts.

Repo: `AThevon/genjutsu`

## Capabilities

- Award-winning user interface patterns
- Premium-quality animations
- Refined visual polish
- Strong creative direction
- Modern, structured layouts

## Core Patterns

### Hero section with premium polish

```html
<!-- Genjutsu-style hero: dark background, large type, subtle grain -->
<section class="genjutsu-hero">
  <div class="hero-noise"></div>
  <div class="hero-content">
    <span class="eyebrow">Est. 2024</span>
    <h1 class="display">Craft that<br><em>moves people.</em></h1>
    <p class="sub">Premium digital experiences for brands that refuse to be average.</p>
    <a href="#" class="cta-pill">Start a project →</a>
  </div>
</section>
```

```css
.genjutsu-hero {
  position: relative;
  min-height: 100vh;
  background: #0a0a0a;
  display: grid;
  place-items: center;
  overflow: hidden;
}
.hero-noise {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,..."); /* SVG grain */
  opacity: 0.04;
  pointer-events: none;
}
.display {
  font-size: clamp(3rem, 8vw, 7rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.05;
  color: #f5f5f0;
}
.display em { color: #c9a96e; font-style: normal; }
.cta-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 2rem;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 999px;
  color: #f5f5f0;
  font-size: 0.9rem;
  letter-spacing: 0.02em;
  transition: background 0.2s, border-color 0.2s;
}
.cta-pill:hover { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.3); }
```

## Prompt

```
Act as a Genjutsu-level UI designer — award-winning craft, premium animations, refined polish.

Design a [component / page / section] for [context].
Requirements:
- Aesthetic: [dark luxury / clean minimal / editorial / brutalist]
- Key interaction: [hover state / scroll reveal / page transition / micro-animation]
- Color mood: [midnight / sand / ice / forest]
- Typography feel: [editorial serif / geometric sans / mono]

Deliver: HTML + CSS (or React + Tailwind) with inline animation code.
Polish level: production-ready, not prototype.
```
