---
name: css-scroll-driven-animations
description: >
  Implement CSS scroll-driven animations (animation-timeline: scroll()/view(),
  scroll-timeline, view-timeline) on owned frontends with accessibility and
  performance in mind. Use for scroll-linked progress, parallax-like effects,
  and view-progress reveals without main-thread scroll listeners when supported.
---

# CSS Scroll-Driven Animations

## Scope And Authorization

- **In scope:** Front-end UIs you maintain.
- **Out of scope:** Forcing motion on users without `prefers-reduced-motion` respect; injecting into third-party sites.
- Progressive enhancement: content must work without these features.
- Pair with accessibility checklist skills and `code-quality-standards`.

## When To Use

- Scroll progress bars linked to document/scroller.
- Section reveals tied to element visibility (`view()`).
- Replacing JS `scroll` listeners for simple transform/opacity effects.
- Design systems documenting motion patterns.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General CSS specificity | `css-specificity-debugging` |
| Container queries | `css-container-queries` |
| Web animation JS timeline complex orchestration | WAAPI deep skills |
| CSS security injection | `css-injection-exfiltration` |
| Implementation quality baseline | `code-quality-standards` |

## Core concepts

| API | Role |
| --- | --- |
| `animation-timeline: scroll()` | Drive animation by scroll progress of scroller |
| `animation-timeline: view()` | Drive by subject visibility progress |
| `scroll-timeline-name` / `view-timeline-name` | Named timelines |
| `animation-range` | Start/end offsets within timeline |
| `timeline-scope` | Raise timeline names to ancestors |

Browser support is evolving — gate with `@supports` and document matrix.

## Workflow

### 1. Confirm scope and success criteria

1. Effect list; must-have vs nice-to-have motion.
2. Success: works in supporting browsers; no layout shift of critical content; reduced-motion disables non-essential effects; no jank on mid-tier mobile.

### 2. Prefer CSS over scroll listeners

```css
@supports (animation-timeline: scroll()) {
  @keyframes grow {
    from { transform: scaleX(0); }
    to { transform: scaleX(1); }
  }

  .progress {
    transform-origin: left;
    animation: grow linear;
    animation-timeline: scroll();
  }
}
```

### 3. View timelines for element reveals

```css
@supports (animation-timeline: view()) {
  @keyframes fade-up {
    from {
      opacity: 0;
      transform: translateY(1rem);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .reveal {
    animation: fade-up ease both;
    animation-timeline: view();
    animation-range: entry 0% cover 40%;
  }
}
```

Tune `animation-range` so content is readable before animation completes.

### 4. Named scroll timelines

```css
.scroller {
  overflow: auto;
  scroll-timeline-name: --main;
  scroll-timeline-axis: block;
}

.indicator {
  animation: progress linear;
  animation-timeline: --main;
}
```

### 5. Accessibility

```css
@media (prefers-reduced-motion: reduce) {
  .reveal,
  .progress {
    animation: none !important;
    opacity: 1;
    transform: none;
  }
}
```

1. Never hide critical content only in the end keyframe without a non-motion path.
2. Avoid large parallax that triggers vestibular issues.
3. Keep focus order independent of visual motion.

### 6. Performance notes

1. Animate `transform`/`opacity` primarily.
2. Avoid scroll-driven animations that trigger layout each frame (width/height/top).
3. Limit number of simultaneous complicated view timelines on huge lists — virtualize content first.
4. Test on throttled CPU.

### 7. Verify

```bash
# Manual: Chrome flags if needed for older builds; current stable preferred
# Storybook interaction + reduced-motion OS setting
```

Check: without support, static layout OK; with support, effect matches design; reduced-motion disables.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Enhancement | @supports gated | Content invisible without animation |
| Properties | transform/opacity | Top/left scroll thrash |
| A11y | prefers-reduced-motion | Mandatory parallax |
| Ranges | Readable mid-scroll | Fully transparent until late |
| JS mix | CSS for simple cases | Duplicate scroll listeners fighting CSS |

## Output Checklist

- [ ] Effects listed with enhancement priority
- [ ] `scroll()` / `view()` usage chosen
- [ ] Ranges tuned
- [ ] `@supports` + reduced-motion handled
- [ ] Critical content visible without feature
- [ ] Performance checked on mobile
- [ ] Browser matrix documented
- [ ] Design system notes updated
- [ ] No security sink introduced via user CSS
- [ ] Residual fallbacks accepted

## Rules

- Motion is optional; content is not.
- Prefer compositor-friendly properties.
- Focus on **CSS scroll-driven animations**.
