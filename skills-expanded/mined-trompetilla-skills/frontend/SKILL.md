---
name: Frontend
description: Build polished user interfaces across web and mobile with consistent UX patterns.
metadata: {"clawdbot":{"emoji":"🖥️","os":["linux","darwin","win32"]}}
---

## Loading States

- Skeleton screens for content with known layout—less jarring than spinners
- Spinners for unknown-duration actions—but show within 100ms
- Never blank screens during load—always visual feedback
- Progressive disclosure: show content as it arrives—header first, then body

## Empty States

- Empty screens always have a call to action—not just "No items"
- Illustration or icon + explanation + action button—guide user forward
- First-time empty vs cleared empty may differ—onboarding opportunity

## Error Recovery

- Every error screen has a recovery path—Retry, Go Back, Contact Support
- Preserve user input on form failure—never lose their work
- Offline mode degrades gracefully—show cached content, queue actions
- Toast/snackbar for transient errors—inline for persistent ones

## Immediate Feedback

- Every tap/click acknowledged within 100ms—button state change, animation, sound
- Optimistic updates for fast-feeling actions—show success, rollback if fails
- Progress indicators for operations over 1 second—user knows system is working
- Disable buttons during submission—prevent double-tap

## Touch and Interaction

- Touch targets minimum 44x44 points—fingers are imprecise
- Adequate spacing between interactive elements—prevent mis-taps
- Swipe actions discoverable—hint or onboarding; don't assume users know
- Pull-to-refresh where expected—but indicate it's available

## Visual Hierarchy

- One primary action per screen—other actions visually secondary
- Consistent spacing scale—8pt grid or similar system
- Typography hierarchy clear—title, body, caption distinguishable
- Color conveys meaning consistently—red for destructive, green for success

## Motion and Animation

- Animation communicates, not decorates—shows relationship, guides attention
- Duration 150-300ms for interactions—fast enough to feel responsive
- Respect reduced motion preference—provide static alternative
- Exit animations as important as enter—completes the interaction loop

## Consistency

- Same action, same pattern everywhere—don't reinvent navigation per screen
- Design tokens for colors, spacing, typography—single source of truth
- Reusable components over one-off designs—reduces cognitive load
- Platform conventions respected—iOS feels iOS, Android feels Android, web feels web

## Accessibility

- Screen reader testing—not just visual inspection
- Sufficient color contrast—don't rely on color alone for meaning
- Keyboard/switch control works—every action reachable without touch
- Focus order logical—follows visual reading order

## Responsiveness

- Design mobile-first, enhance for larger—not desktop shrunk down
- Test on real devices—simulators miss performance and interaction
- Landscape orientation considered—don't break if user rotates
- Content reflows gracefully—no horizontal scroll, no cut-off text

## Performance Perception

- Time to interactive matters more than full load—prioritize interactivity
- Lazy load below-the-fold content—don't block first interaction
- Image placeholders prevent layout shift—dimensions known before load
- Cache aggressively—instant loads on return visits

## Microcopy

- Button labels describe action: "Save Changes" not "Submit"
- Error messages explain what to do—not just what went wrong
- Confirmation dialogs clear about consequences—"Delete permanently?"
- Loading text specific when possible—"Uploading photo..." not "Loading..."
