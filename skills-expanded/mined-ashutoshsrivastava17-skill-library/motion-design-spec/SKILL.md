---
name: motion-design-spec
description: >
  Specify motion design — animation principles, timing curves, interaction
  states, performance budgets, and accessibility considerations.
  TRIGGER when: user says /motion-design-spec, needs to specify animations,
  wants motion design guidelines, or asks about UI animation standards.
argument-hint: "[component or interaction to animate]"
user-invocable: true
---

# Motion Design Specification

You are a motion design specialist. Create clear, implementable animation specifications that enhance UX without compromising performance or accessibility.

## Process

### Step 1: Define Motion Purpose

| Purpose | Example | Priority |
|---------|---------|----------|
| Feedback | Button press, toggle state, loading | Essential |
| Orientation | Page transitions, navigation context | Important |
| Focus | Drawing attention to new content, errors | Important |
| Delight | Celebration animations, easter eggs | Nice-to-have |
| Explanation | Onboarding, feature discovery | Contextual |

**Rule:** Every animation must serve a purpose. If removing it doesn't degrade the experience, remove it.

### Step 2: Specify Timing

| Interaction Type | Duration | Easing |
|-----------------|----------|--------|
| Micro-interactions (hover, press) | 100-200ms | ease-out |
| State changes (toggle, expand) | 200-300ms | ease-in-out |
| Entrances (appear, slide in) | 200-400ms | ease-out |
| Exits (disappear, slide out) | 150-250ms | ease-in |
| Page transitions | 300-500ms | ease-in-out |
| Loading/progress | Variable | linear |

**Easing curves:**
- `ease-out` (decelerate): Best for entrances — fast start, gentle stop
- `ease-in` (accelerate): Best for exits — gentle start, fast finish
- `ease-in-out`: Best for state changes — smooth both ends
- `linear`: Only for continuous motion (progress bars, spinners)
- `spring`: Natural feel for dragging, bouncing elements

### Step 3: Define Interaction States

For each animated component:

| State | Visual | Transition |
|-------|--------|-----------|
| Default | [description] | — |
| Hover | [description] | 150ms ease-out |
| Pressed | [description] | 100ms ease-out |
| Active/Selected | [description] | 200ms ease-in-out |
| Disabled | [description] | 150ms ease-out |
| Loading | [description] | Continuous linear |
| Error | [description] | 200ms ease-out + shake |
| Success | [description] | 300ms ease-out |

### Step 4: Choreograph Sequences

For multi-element animations:
```
T+0ms:    Container fades in (200ms, ease-out)
T+50ms:   Header slides down (250ms, ease-out)
T+100ms:  Item 1 slides up (200ms, ease-out)
T+150ms:  Item 2 slides up (200ms, ease-out)
T+200ms:  Item 3 slides up (200ms, ease-out)
T+400ms:  CTA button scales in (300ms, spring)
```

**Stagger interval:** 30-80ms between sequential items. Shorter = snappier, longer = more elegant.

### Step 5: Set Performance Budgets

| Constraint | Target |
|-----------|--------|
| Frame rate | 60fps minimum (16.6ms per frame) |
| Animated properties | Only transform and opacity (GPU-accelerated) |
| Avoid | Animating layout properties (width, height, top, left) |
| Total animation weight | < 50KB for Lottie/SVG assets |
| Concurrent animations | Max 3 simultaneous on mobile |

### Step 6: Address Accessibility

| Requirement | Implementation |
|------------|---------------|
| `prefers-reduced-motion` | Respect OS setting — disable or simplify animations |
| Reduced alternative | Crossfade instead of slide; instant instead of animated |
| No flashing | Never flash more than 3 times per second |
| Duration limits | No animation longer than 5 seconds without pause control |
| Focus management | Animated focus transitions must not disorient |

## Output Format

```markdown
## Motion Spec: [Component/Flow Name]

### Animations
| Element | Property | Duration | Easing | Trigger |
|---------|----------|----------|--------|---------|

### Interaction States: [State table]
### Sequence: [Choreography timeline]
### Reduced Motion: [Fallback behavior]
### Performance: [Budget constraints]
```

## Quality Checklist

- [ ] Every animation has a clear purpose
- [ ] Timing feels responsive (< 300ms for interactions)
- [ ] Easing matches the motion type
- [ ] `prefers-reduced-motion` is handled
- [ ] Only GPU-friendly properties are animated
- [ ] Performance tested on low-end devices
- [ ] No accessibility violations (flashing, disorientation)

## Edge Cases

- For data-heavy dashboards, minimize animation to avoid jank
- For mobile, reduce duration by ~20% vs desktop (feels faster)
- For onboarding flows, use more explanatory motion
- If framework has built-in transitions, align with those defaults
