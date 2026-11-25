---
name: design-review
description: Awwwards Jury design review engine. Evaluates every generated design across 8 categories with a mandatory 95/100 approval threshold.
---

# 🏆 14 - Awwwards Jury Design Review Engine

## 🎯 Purpose
Act as an uncompromising **Awwwards Jury Member**. After every generated page or major component, perform a rigorous audit across 8 key evaluation categories. No design output is allowed to pass to production delivery unless every category meets or exceeds the **95/100 threshold**.

---

## 🛠️ The 8 Jury Evaluation Categories & Scoring Standards

### 1. Typography (Weight: 15% | Threshold: 95/100)
- **Checklist**: Intentional font pairing, fluid `clamp()` responsive type scaling, optical alignment, character tracking (`-0.03em` on display headers), reading line length (`45ch`-`75ch`), vertical rhythm.
- **Deductions**: -10 for fixed px font sizes without fluid scaling; -15 for generic default font stacks.

### 2. Spacing & Baseline Grid (Weight: 15% | Threshold: 95/100)
- **Checklist**: Strict adherence to the 8px baseline spatial grid (`8px`, `16px`, `24px`, `32px`, `48px`, `64px`, `96px`, `128px`), generous negative whitespace balance, clear container boundaries.
- **Deductions**: -10 for ad-hoc pixel offsets (`margin-top: 13px`); -10 for cramped content density.

### 3. Visual Hierarchy & Composition (Weight: 15% | Threshold: 95/100)
- **Checklist**: Unambiguous visual entry point, scale contrast between primary and secondary elements, clear scanning path, asymmetric visual interest.
- **Deductions**: -15 for visual clutter or competing focal points.

### 4. Motion & Animation Timing (Weight: 15% | Threshold: 95/100)
- **Checklist**: 60 FPS hardware acceleration (animating strictly `transform` and `opacity`), spring dampening physics, Lenis smooth scroll ticker sync, purposeful scroll-driven reveals.
- **Deductions**: -20 for animating layout properties (`width`, `height`, `margin`); -10 for linear mechanical easing without dampening.

### 5. Originality & Art Direction (Weight: 15% | Threshold: 95/100)
- **Checklist**: Non-derivative bespoke visual identity, custom color palette hierarchy, bespoke micro-interactions. Zero generic template feel.
- **Deductions**: -30 for generic AI templates or Bootstrap looks; -20 for uninspired direct clones.

### 6. Interaction & Tactile Feel (Weight: 10% | Threshold: 95/100)
- **Checklist**: Sub-50ms reaction loops, magnetic button physics, custom cursor dynamics, hover states, active press feedback (`scale: 0.97`).
- **Deductions**: -10 for delayed hover transitions; -10 for static CTAs without press scale feedback.

### 7. Performance & Optimization (Weight: 10% | Threshold: 95/100)
- **Checklist**: LCP < 2.5s, INP < 200ms, CLS < 0.1, dynamic importing of WebGL/Three.js heavy libraries, zero memory leaks in animation loops.
- **Deductions**: -15 for blocking main thread synchronous scripts; -10 for uncompressed image assets.

### 8. Accessibility & Ergonomics (Weight: 5% | Threshold: 95/100)
- **Checklist**: WCAG 2.1 AA/AAA contrast ratios (>= 4.5:1), custom high-contrast focus rings (`:focus-visible`), 100% keyboard navigability (`Tab`/`Enter`), screen reader landmarks.
- **Deductions**: -20 for removing outline without custom focus styling; -15 for poor text contrast ratios.

---

## 📋 Mandatory Jury Scorecard Template

```markdown
### 🏆 Awwwards Jury Review Scorecard

| Category | Score (/100) | Status | Defect / Note |
| :--- | :--- | :--- | :--- |
| **1. Typography** | 98 | PASS | Fluid clamp scale & Geist pairing verified. |
| **2. Spacing** | 96 | PASS | 8px grid geometry compliant. |
| **3. Hierarchy** | 95 | PASS | Clear display contrast. |
| **4. Motion** | 97 | PASS | 60 FPS compositor acceleration verified. |
| **5. Originality** | 95 | PASS | Bespoke monochromatic luxury aesthetic. |
| **6. Interaction** | 96 | PASS | Sub-50ms magnetic button pull. |
| **7. Performance** | 98 | PASS | LCP < 2.1s, zero CLS. |
| **8. Accessibility**| 100 | PASS | WCAG 2.1 AAA contrast compliant. |
| **OVERALL SCORE** | **96.8 / 100** | **APPROVED** | Ready for delivery. |
```

---

## 🛑 Failure Protocol & Redesign Cycle

> ⚠️ **REDESIGN MANDATE**: If ANY category score is below **95 / 100**, the AI Assistant MUST:
> 1. Explicitly list the failing categories and exact defects.
> 2. Redesign and refactor the code to resolve every defect.
> 3. Re-score the design using the scorecard until 100% of categories score **>= 95**.
