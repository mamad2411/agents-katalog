---
name: web-ux-motion-animation
description: Use when implementing or reviewing web UX motion and animation outcomes with deterministic reduced-motion, coherence, and performance checks and evidence-backed release recommendations.
---

# Web UX Motion and Animation

## Specialization

Evaluate motion and animation UX for accessibility compliance, perceived-performance coherence, user delight, and motion-sensitivity accommodation.

Motion is a first-class UX dimension: poorly executed animations degrade accessibility, increase perceived latency, and undermine interface clarity. This skill encodes deterministic checks for WCAG animation guidance, reduced-motion support, animation coherence, and performance impact.

## Objective

Produce a severity-ranked findings report and a pass/warning/block release recommendation for motion and animation UX covering:

- Reduced-motion support (prefers-reduced-motion media query and fallback behavior)
- Animation performance and jank detection
- Animation coherence and purpose clarity
- Flash and flicker avoidance
- Animation timing and user interaction predictability

## Trigger Conditions

- A release includes new animations, transitions, or motion-heavy interactions
- Motion or animation creates user friction, accessibility, or performance risk
- Reduced-motion support is missing or incomplete
- Accessibility audit or usability evidence surfaces animation concerns

## Scope Boundaries

**In scope:**
- Entrance, exit, and state-change animations
- Transitions between states and page regions
- Parallax, scroll-triggered, and gesture-based motion
- Loading state and progress animations
- Reduced-motion alternatives and fallback behavior
- Animation impact on perceived performance and trust

**Out of scope:**
- Video content (covered separately)
- Real-time data stream visualization (covered by data-dense-interfaces skill)
- Animation authoring frameworks or specific tool recommendations

## Inputs

- URL or deployed prototype link for live motion testing
- Animation documentation (design specs, interaction patterns, intended duration/easing)
- Browser and device test matrix (desktop, mobile, tablet, accessibility testing tools)
- Known motion constraints or design system animation tokens if applicable
- Previous accessibility audit findings related to animation or motion

## Required Outputs

- Motion and Animation Findings Report (`.md`) with severity tagging (critical, high, low)
- Animation Coherence Matrix (mapping animation type, duration, easing, accessibility support)
- Reduced-Motion Audit Report (documenting prefers-reduced-motion coverage per surface)
- Flash/Flicker Risk Assessment
- Performance Impact Assessment (scroll-jank, animation frame drops, battery impact on mobile)
- Unified Release Recommendation with pass/warning/block disposition

## Deterministic Workflow

### Phase 1: Audit Setup
1. Collect animation documentation and deploy test link.
2. Enable browser DevTools animation inspector and reduced-motion simulation.
3. Set test matrix: Windows/macOS desktop, iOS/Android mobile, screen readers enabled.

### Phase 2: Reduced-Motion Compliance
1. For each animated surface:
   - Verify `prefers-reduced-motion: reduce` CSS media query is applied.
   - Confirm fallback animation or instant transition is perceptible and coherent.
   - Test with Windows High Contrast mode and reduced-motion enabled simultaneously.
2. Log any missing or incomplete reduced-motion support as high-severity findings.

### Phase 3: Animation Coherence and Purpose
1. For each animation type (entrance, exit, state-change, micro-interaction):
   - Verify animation purpose is clear (e.g., guides attention, clarifies causality, provides feedback).
   - Check animation duration aligns with animation type (entrance <= 300ms, exit <= 200ms, state <= 200ms).
   - Confirm easing function matches interaction cost and motion type (entrance: ease-out, state: ease-in-out).
2. Mark animations without clear purpose or misaligned timing as medium-severity findings.

### Phase 4: Flash and Flicker Risk
1. Run axe-core and Lighthouse accessibility audit; capture animation-related findings.
2. Manually inspect for:
   - Rapid content swaps (>3 times per second) triggering seizure risk.
   - Large area flashing (>25% of viewport) with brightness/color contrast shifts.
3. Any flash/flicker risk detected at all is a critical-severity finding; recommend immediate fix or removal.

### Phase 5: Performance Impact
1. Profile animation performance:
   - Use Chrome DevTools Performance tab; record animation playback.
   - Measure: frame rate consistency, main-thread blocking, paint cost.
   - Compare with reduced-motion variant if available.
2. Detect jank (frame drops below 60fps) or battery-drain indicators on mobile.
   - Mark as high-severity if jank occurs during core user interactions.
   - Mark as medium-severity if jank occurs in peripheral motion (e.g., idle animations).

### Phase 6: Severity and Recommendation
1. Tally findings by severity: critical, high, medium, low.
2. Apply recommendation rules:
   - **Block**: Any critical finding (seizure risk, critical accessibility gap, motion trap).
   - **Warning**: High-severity findings without critical impact (reduced-motion missing on secondary surface, jank in non-core flow).
   - **Pass**: All findings at medium/low severity or explicitly deferred with owner.

## Severity Model

| Severity | Example Finding | Action |
|---|---|---|
| Critical | Flash/flicker risk detected; reduced-motion not supported on primary flow; animation trap (focus or pointer locked by motion) | Do not release without fix |
| High | Reduced-motion missing on secondary surface; animation causes jank on mobile during core interaction; animation purpose unclear to test users | Document deferral owner; recommend fix before release |
| Medium | Animation timing slightly misaligned with interaction cost; easing choice suboptimal; animation missing on low-end devices | Track for next refinement; release allowed |
| Low | Peripheral animation has minor timing inconsistency; documentation incomplete | No action required; update if possible |

## Evidence Contract

**Motion and Animation Findings Report** (`.docs/changes/<id>/motion-animation-findings.md`):
```md
### Reduced-Motion Compliance
- [x] Primary surfaces: reduced-motion supported with fallback behavior
- [x] Secondary surfaces: reduced-motion support status
- [ ] Critical gaps documented and owned

### Animation Coherence
| Animation Type | Surface | Duration | Easing | Purpose Clear? | Finding |
|---|---|---|---|---|---|
| entrance | hero section | 250ms | ease-out | yes | pass |
| state-change | form submit button | 150ms | ease-in-out | yes | pass |

### Flash/Flicker Risk
- Axe-core violations: 0 critical, 0 serious
- Manual inspection: no rapid flashes detected

### Performance Impact
- Frame rate: 60fps maintained throughout animation sequence
- Mobile jank: none detected
- Battery impact: negligible

### Consolidated Findings
- <FBK-ID>: <finding text> [severity]
```

**Animation Coherence Matrix** (`.docs/changes/<id>/animation-coherence-matrix.md`):
```md
| Feature | Animation Type | Element | Duration | Easing | Accessibility Support | Status |
|---|---|---|---|---|---|---|
| Navigation expand | state-change | sidebar | 200ms | ease-in-out | reduced-motion alt provided | pass |
```

**Reduced-Motion Audit Report** (`.docs/changes/<id>/reduced-motion-audit.md`):
Explicit log of every animated surface and its reduced-motion support status.

**Unified Release Recommendation** (`.docs/changes/<id>/ux-quality-gate-recommendation.md`, motion section):
Motion and Animation: `pass | warning | block`

## Source Governance Summary

| Source | Status | Relevance | Authority | Freshness | Actionability | Notes |
|---|---|---|---|---|---|---|
| [WCAG 2.2 Animation and Motion](https://www.w3.org/TR/WCAG22/#animation-from-interactions) | active | Critical for accessibility compliance | W3C standard | current | encode success criteria into checklist | SC 2.3.3, 2.3.4 guidelines |
| [prefers-reduced-motion CSS Media Query](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) | active | Motion-risk mitigation | MDN/vendor standard | current | deterministic implementation checks | browser support >95% |
| [Web Animations Performance](https://web.dev/animations-guide/) | active | Performance impact assessment | web.dev best practices | current | profile metrics extraction | LCP/CLS/jank detection |
| [APG Animation and Motion Guidelines](https://www.w3.org/WAI/ARIA/apg/patterns/) | active | Component animation coherence | W3C guidance | current | map interaction patterns to timing | component-specific motion rules |
| [Seizure and Photosensitivity in Web Animation](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html) | active | Flash/flicker risk detection | W3C Understanding docs | current | encode flash detection rules | 3+ flashes/sec threshold |

## Pragmatic Stop Rule

Stop and proceed to recommendation when:

1. Reduced-motion audit is complete for all animated surfaces.
2. Animation coherence matrix covers all distinct animation types and surfaces.
3. Flash/flicker audit is complete (axe-core + manual inspection).
4. Performance profile is captured and jank assessment is documented.
5. All findings are severity-tagged and have associated remediation owners or deferrals.

**If token budget is exhausted before 5 is complete:**
- Defer animation coherence and performance checks to a follow-up pass.
- Prioritize reduced-motion and seizure-risk audits (accessibility must-haves).
- Document incomplete scope in recommendation and defer non-critical findings.

## Done Criteria

- [ ] Motion and Animation Findings Report created with at least critical and high findings documented.
- [ ] Reduced-Motion Audit Report confirms coverage status across all animated surfaces.
- [ ] Animation Coherence Matrix maps animation type to timing and easing with purpose clarity.
- [ ] Flash/flicker risk assessment is complete; any critical findings trigger block recommendation.
- [ ] Performance impact (frame rate, jank, battery) is measured and documented.
- [ ] All findings are severity-tagged (critical/high/medium/low).
- [ ] Unified recommendation is unambiguous: pass, warning, or block.
- [ ] Remediation owners are assigned for all deferred findings.

