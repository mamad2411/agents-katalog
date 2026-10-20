---
name: web-ux-responsive-design
description: Use when implementing or reviewing web UX responsive design outcomes with deterministic breakpoint, touch-target, layout, and device-adaptation checks and evidence-backed release recommendations.
---

# Web UX Responsive Design

## Specialization

Evaluate responsive design and multi-device adaptation for consistent usability, accessibility, and performance across viewport sizes and device types.

Responsive design is foundational for modern web: poor breakpoint strategy, undersized touch targets, and layout reflow issues degrade UX on mobile and tablet. This skill encodes deterministic checks for viewport strategy, touch-target sizing, reflow coherence, and device-parity across breakpoints.

## Objective

Produce a severity-ranked findings report and a pass/warning/block release recommendation for responsive design covering:

- Viewport configuration and responsive breakpoint strategy
- Touch-target sizing (minimum 44x44px, 48x48px recommended)
- Layout reflow and content reordering at breakpoints
- Text readability and zoom support
- Consistent interaction patterns across device classes
- Performance impact of responsive images and layout shifts

## Trigger Conditions

- A release targets multiple device types (mobile, tablet, desktop)
- Layout changes are made affecting breakpoint logic
- Touch interactions are introduced or modified
- Device-specific usability complaints surface
- Responsive design audit or multidevice testing reveals issues

## Scope Boundaries

**In scope:**
- Viewport configuration and meta viewport tags
- CSS media queries and breakpoint alignment
- Touch-target sizing across surfaces
- Layout reflow logic and content reordering
- Responsive image strategy (srcset, picture element)
- Text scaling and zoom support
- Safe areas and notch handling on mobile
- Cumulative Layout Shift (CLS) measurement across breakpoints

**Out of scope:**
- Content strategy or information architecture changes (covered by IA skill)
- Typography at different sizes (covered by content-clarity skill)
- Performance optimization beyond layout impact (covered by performance skill)

## Inputs

- Deployed prototype or staging URL with responsive breakpoints
- Responsive design specification or breakpoint strategy document
- Device test matrix (mobile phones, tablets, 2-in-1s, large desktop, ChromeOS)
- Touch interaction documentation (buttons, forms, gestures)
- Analytics data on device and screen-size distribution if available

## Required Outputs

- Responsive Design Findings Report (`.md`) with severity tagging
- Breakpoint and Layout Reflow Matrix (mapping viewport ranges, layout type, content changes)
- Touch-Target Audit Report (documenting touch-target sizes across interactive elements)
- Multi-Device Test Matrix (capturing viewport, OS, browser, and usability outcome per device)
- CLS and Reflow Impact Assessment (documenting layout-shift cost across breakpoints)
- Unified Release Recommendation with pass/warning/block disposition

## Deterministic Workflow

### Phase 1: Viewport Configuration Audit
1. Inspect HTML `<meta viewport>` tag and CSS media queries.
2. Verify viewport tag includes `width=device-width, initial-scale=1, viewport-fit=cover` (or project-specific variant).
3. Verify user-scalability is not disabled (`user-scalable=no` is a critical finding).
4. Document all defined breakpoints (mobile, tablet, desktop thresholds).

### Phase 2: Breakpoint and Layout Reflow Audit
1. For each defined breakpoint:
   - Test at exact breakpoint width and 1-2px around the threshold.
   - Verify layout reflow is smooth with no content jumping.
   - Document content reordering (sidebar moves, columns collapse, etc.).
   - Check for horizontal scrolling or layout overflow.
2. Log layout issues as high-severity findings if they affect core user tasks.

### Phase 3: Touch-Target Sizing Audit
1. For each interactive element (button, link, checkbox, input field):
   - Measure interactive area in device pixels.
   - Verify minimum 44x44px (accessible); prefer 48x48px (comfortable on mobile).
   - Check spacing between touch targets (minimum 8px recommended).
   - Test with browser DevTools device emulation and real touch device if available.
2. Mark undersized touch targets as high-severity findings on mobile; medium on desktop.

### Phase 4: Text Readability and Zoom
1. Measure base font size on each breakpoint.
2. Verify minimum 16px font size on mobile for body text (WCAG level AAA).
3. Test zoom functionality: pinch-zoom should work; text zoom should not break layout.
4. Verify line-height >= 1.5 and column width <= 80 characters for readability.

### Phase 5: Responsive Image and Layout Shift Assessment
1. Profile `srcset` and `picture` element usage for responsive images.
2. Measure CLS across breakpoints using Lighthouse or WebVitals.js.
3. Identify layout shifts caused by image loading, ad rendering, or widget expansion.
4. Document CLS impact; flag high CLS (>0.1) as high-severity finding.

### Phase 6: Multi-Device Testing
1. Test on representative device mix:
   - Mobile: iOS iPhone 14+, Android Pixel 7+ (or similar current-generation devices)
   - Tablet: iPad 12.9", Android tablet (if in scope)
   - Desktop: macOS, Windows with 1920x1080 and 2560x1440 resolutions
2. For each device, document:
   - Viewport size and orientation (portrait/landscape)
   - Interaction success (buttons clickable, forms usable, no horizontal scroll)
   - Visual consistency against design spec
   - Performance: page load time, interaction latency

### Phase 7: Severity and Recommendation
1. Tally findings by severity: critical, high, medium, low.
2. Apply recommendation rules:
   - **Block**: User-scalability disabled; critical touch-target sizing gap on primary flow; layout collapse affecting core task.
   - **Warning**: Touch-target sizing issue on secondary surface; reflow jerky but not breaking; CLS slightly elevated.
   - **Pass**: All findings at medium/low severity or explicitly deferred with owner.

## Severity Model

| Severity | Example Finding | Action |
|---|---|---|
| Critical | User-scalability disabled; primary CTA button 20x20px on mobile; layout completely breaks at tablet breakpoint | Do not release without fix |
| High | Touch-target 36x36px on mobile; CLS 0.15 caused by image loading; content reordering confusing on one breakpoint | Document deferral owner; recommend fix before release |
| Medium | Touch-target 40x40px (close to 44px); CLS 0.12 from non-critical widget; spacing slightly tight between targets | Track for next refinement; release allowed |
| Low | Desktop layout slightly tight; secondary interactive element slightly undersized; documentation missing | No action required |

## Evidence Contract

**Responsive Design Findings Report** (`.docs/changes/<id>/responsive-design-findings.md`):
```md
### Viewport Configuration
- Meta viewport tag present: yes/no
- User-scalability enabled: yes/no
- Viewport-fit cover: yes/no

### Breakpoint Strategy
| Breakpoint | Width | Layout Type | Content Reordering | Notes |
|---|---|---|---|---|
| mobile | 320px | single-column | sidebar hidden | pass |
| tablet | 768px | two-column | sidebar visible | pass |
| desktop | 1024px | three-column | full layout | pass |

### Touch-Target Audit
| Element | Mobile Size | Tablet Size | Desktop Size | Status | Finding |
|---|---|---|---|---|---|
| Primary CTA | 48x48px | 48x48px | 48x48px | pass | meets minimum |
| Secondary button | 40x40px | 48x48px | 48x48px | warning | below 44px on mobile |

### Multi-Device Test Results
| Device | OS | Screen | Orientation | Load Time | Interaction Success | Visual Consistency | Finding |
|---|---|---|---|---|---|---|---|
| iPhone 14 | iOS | 393x852 | portrait | 2.1s | pass | pass | pass |
| Pixel 7 | Android | 412x915 | portrait | 2.3s | pass | pass | pass |

### CLS and Reflow Impact
- Desktop: 0.08 (good)
- Tablet: 0.12 (fair; caused by image loading)
- Mobile: 0.10 (good)

### Consolidated Findings
- <RD-ID>: <finding text> [severity]
```

**Breakpoint and Layout Reflow Matrix** (`.docs/changes/<id>/breakpoint-reflow-matrix.md`):
Detailed mapping of each breakpoint, layout type, and content reordering.

**Touch-Target Audit Report** (`.docs/changes/<id>/touch-target-audit.md`):
Complete inventory of interactive elements and their sizes per device class.

**Multi-Device Test Matrix** (`.docs/changes/<id>/multidevice-test-matrix.md`):
Test results for each device/OS/viewport combination.

**Unified Release Recommendation** (`.docs/changes/<id>/ux-quality-gate-recommendation.md`, responsive section):
Responsive Design: `pass | warning | block`

## Source Governance Summary

| Source | Status | Relevance | Authority | Freshness | Actionability | Notes |
|---|---|---|---|---|---|---|
| [WCAG 2.2 Mobile Accessibility](https://www.w3.org/TR/WCAG22/#target-size) | active | Touch-target sizing and zoom requirements | W3C standard | current | encode SC 2.5.5 checks | minimum 44x44px at level AA |
| [Mobile-First Responsive Design](https://www.mobileFirst.org/) | active | Responsive breakpoint strategy | design best practice | current | map breakpoint layout type | systematic scaling approach |
| [Responsive Web Design Fundamentals](https://web.dev/responsive-web-design-basics/) | active | Layout reflow and viewport configuration | web.dev best practice | current | implement media-query checks | CSS media query patterns |
| [Touch Target Size Guidelines](https://www.nngroup.com/articles/touch-target-size/) | active | Touch-target ergonomics | NN/g research | current | apply 48px+ recommendation | comfort vs. minimum threshold |
| [Web Vitals CLS Optimization](https://web.dev/cls/) | active | Cumulative Layout Shift measurement | web.dev best practice | current | profile CLS across breakpoints | layout-shift cost assessment |

## Pragmatic Stop Rule

Stop and proceed to recommendation when:

1. Viewport configuration audit is complete.
2. Breakpoint strategy is mapped and reflow tested at each boundary.
3. Touch-target sizing is audited for at least mobile and desktop.
4. Multi-device testing is complete for at least 2 representative mobile and 1 desktop device.
5. CLS measurement is captured and documented.
6. All findings are severity-tagged and have associated remediation owners or deferrals.

**If token budget is exhausted before 6 is complete:**
- Defer tablet testing and advanced multi-device scenarios to follow-up.
- Prioritize mobile touch-target and viewport configuration audits.
- Document incomplete scope in recommendation and defer non-critical findings.

## Done Criteria

- [ ] Responsive Design Findings Report created with at least critical and high findings documented.
- [ ] Breakpoint and Layout Reflow Matrix covers all defined breakpoints.
- [ ] Touch-Target Audit Report documents sizes across at least mobile and desktop.
- [ ] Multi-Device Test Matrix includes at least 2 mobile and 1 desktop result.
- [ ] CLS measurement is captured for each breakpoint.
- [ ] All findings are severity-tagged (critical/high/medium/low).
- [ ] Unified recommendation is unambiguous: pass, warning, or block.
- [ ] Remediation owners are assigned for all deferred findings.

