---
name: responsive-native
version: 1.0.0
min_mindforge_version: 10.4.0
status: stable
triggers: responsive native design, adaptive layout mobile, platform-specific UX, mobile accessibility design, gesture handling mobile, mobile UX pattern, responsive breakpoint mobile, dynamic type scaling, safe area design, tablet adaptation, foldable device support, mobile navigation pattern
---

# Skill — Responsive Native UI & Platform-Specific Design

## When this skill activates
This skill activates when designing adaptive mobile interfaces, implementing platform-specific UX patterns, ensuring accessibility, handling gestures, or supporting diverse screen sizes including tablets and foldables.

## Mandatory actions when this skill is active

### Before writing any code
1. Define responsive breakpoints and layout strategies for phone, tablet, foldable, and landscape orientations
2. Review platform design guidelines (Apple HIG, Material Design) to ensure platform-appropriate patterns
3. Establish accessibility requirements: screen reader support, dynamic type scaling, color contrast, touch target sizes
4. Plan gesture handling strategy considering platform conventions (iOS swipe gestures vs Android navigation patterns)

### During implementation
- Use platform-appropriate navigation patterns (iOS tab bar + navigation stack, Android bottom nav + drawer)
- Implement safe area handling for notched devices (SafeAreaView, WindowInsets, notch cutouts)
- Support dynamic type scaling — use relative font sizes, test with largest accessibility sizes
- Implement proper touch target sizes (minimum 44x44pt iOS, 48x48dp Android) with adequate spacing
- Use semantic colors and avoid hardcoded values to support dark mode automatically
- Implement platform-specific gesture handlers (swipe back on iOS, hardware back button on Android)
- Handle keyboard interactions properly (dismiss on scroll, avoid keyboard covering inputs, proper focus management)

### After implementation
- Test on multiple screen sizes: smallest supported phone, largest phone, tablet, foldable (if applicable)
- Verify accessibility with screen readers (VoiceOver, TalkBack), ensure all interactive elements are labeled
- Test with maximum dynamic type size settings and ensure UI remains functional
- Validate gesture handling: swipe navigation, pull to refresh, long press actions work intuitively
- Check dark mode appearance, ensure proper contrast and no hardcoded light-mode colors

## Self-check before task completion
- [ ] Layout adapts correctly across all target screen sizes without clipping or awkward spacing
- [ ] Platform-specific patterns are used (no Android-style navigation on iOS, and vice versa)
- [ ] Accessibility score passes WCAG 2.1 AA minimum (contrast ratios, touch targets, screen reader support)
- [ ] Safe areas are properly handled on devices with notches, rounded corners, and home indicators
- [ ] Gestures work intuitively and don't conflict with system gestures or platform conventions
- [ ] Dynamic type scaling is supported with proper layout adjustments for large text sizes
