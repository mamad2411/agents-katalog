---
name: impeccable-polish
description: "Performs a final quality pass fixing alignment, spacing, consistency, and micro-detail issues before shipping. Use when the user mentions polish, finishing touches, pre-launch review, something looks off, or wants to go from good to great."
user-invocable: true
argument-hint: "[target]"
license: Apache 2.0. Based on pbakaus/impeccable polish skill.
---

## MANDATORY PREPARATION

Invoke `/impeccable-design` — it contains design principles, anti-patterns, and the Context Gathering Protocol. Follow the protocol before proceeding. Additionally gather: quality bar (MVP vs flagship).

---

Perform a meticulous final pass to catch all the small details that separate good work from great work. The difference between shipped and polished.

## Pre-Polish Assessment

1. **Review completeness**: Is it functionally complete? What's the quality bar? When does it ship?
2. **Identify polish areas**: Visual inconsistencies, spacing/alignment, interaction state gaps, copy inconsistencies, edge cases, loading/transition smoothness

**CRITICAL**: Polish is the last step, not the first. Don't polish work that's not functionally complete.

## Polish Systematically

### Visual Alignment & Spacing
- Pixel-perfect alignment — everything lines up to grid
- Consistent spacing — all gaps use spacing scale (no random 13px gaps)
- Optical alignment — adjust for visual weight (icons may need offset for optical centering)
- Responsive consistency — spacing and alignment work at all breakpoints

### Typography Refinement
- Hierarchy consistency — same elements use same sizes/weights throughout
- Line length: 45-75 characters for body text
- No widows & orphans
- Font loading: no FOUT/FOIT flashes

### Color & Contrast
- All text meets WCAG contrast standards
- Consistent token usage — no hard-coded colors
- Tinted neutrals — no pure gray or pure black (add subtle chroma: 0.01)
- **NEVER**: Gray text on colored backgrounds — use a shade of that color or transparency

### Interaction States — Every interactive element needs ALL states:
- Default, Hover, Focus (never remove without replacement), Active, Disabled, Loading, Error, Success

### Micro-interactions & Transitions
- All state changes animated: 150-300ms
- Consistent easing: ease-out-quart/quint/expo. **Never bounce or elastic.**
- 60fps — only animate transform and opacity
- Respects `prefers-reduced-motion`

### Content & Copy
- Consistent terminology throughout
- Consistent capitalization (Title Case vs Sentence case applied consistently)
- No typos, no grammar errors
- Punctuation consistency (periods on sentences, not on labels)

### Icons & Images
- Consistent style (same icon family)
- Proper optical alignment with adjacent text
- All images have descriptive alt text
- No layout shift (proper aspect ratios)

### Forms & Inputs
- All inputs properly labeled
- Required indicators clear and consistent
- Error messages helpful and consistent
- Logical keyboard navigation (tab order)

### Edge Cases
- Loading states for all async actions
- Helpful empty states (not blank space)
- Clear error messages with recovery paths
- Success confirmation
- Handles very long names/descriptions gracefully
- No horizontal scroll

### Responsive
- Test: mobile, tablet, desktop
- Touch targets ≥ 44×44px
- No text smaller than 14px on mobile

### Code Quality
- Remove all console.log
- Remove commented-out code
- Remove unused imports
- No TypeScript `any` or ignored errors

## Polish Checklist

- [ ] Visual alignment perfect at all breakpoints
- [ ] Spacing uses design tokens consistently
- [ ] Typography hierarchy consistent
- [ ] All interactive states implemented
- [ ] All transitions smooth (60fps)
- [ ] Copy is consistent and polished
- [ ] Icons are consistent and properly sized
- [ ] All forms properly labeled and validated
- [ ] Error states are helpful
- [ ] Loading states are clear
- [ ] Empty states are welcoming
- [ ] Touch targets ≥ 44×44px
- [ ] Contrast ratios meet WCAG AA
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] No console errors or warnings
- [ ] No layout shift on load
- [ ] Respects reduced motion preference
- [ ] Code is clean (no TODOs, console.logs, commented code)

## Final Verification

Before marking done:
- **Use it yourself**: Actually interact with the feature
- **Test on real devices**: Not just browser DevTools
- **Check all states**: Don't just test happy path
- **Compare to design**: Match intended design

**NEVER**: Polish before functionally complete. Introduce bugs while polishing. Perfect one thing while leaving others rough.

Remember: You have impeccable attention to detail and exquisite taste. Polish until it feels effortless, looks intentional, and works flawlessly. Sweat the details — they matter.
