---
name: ios-design-spec
description: Quick HIG audit, SwiftUI component selection, and accessibility check for simple iOS UI questions. Use on main agent for lightweight design decisions. Escalate to designer subagent for full screen design, navigation architecture, or complex interaction design.
---

# iOS Design Spec

## Overview

Fast HIG audit and component guidance for the main agent. Covers component selection, spacing rules, accessibility, and theme compliance — without spawning a full designer subagent.

**Announce at start:** "Using ios-design-spec skill for this design check."

**Use this skill when:**
- Picking the right SwiftUI component for a use case
- Checking HIG compliance of a proposed layout
- Quick accessibility review (touch targets, Dynamic Type, VoiceOver)
- Answering "what's the right pattern for X?" questions

**Escalate to `designer` subagent when:**
- Designing a full new screen from scratch
- Planning navigation architecture or flow changes
- Complex interaction design (gestures, transitions, animations)
- Multi-screen redesign

---

## HIG Quick Reference

### Spacing (8pt grid)
| Usage | Value |
|-------|-------|
| Standard margin | 16pt |
| Large title margin | 20pt |
| Section spacing | 24pt |
| Minimum touch target | 44×44pt |
| List row height (default) | 44pt |

### Typography (SF Pro)
| Style | Use |
|-------|-----|
| `.largeTitle` | Screen titles |
| `.title` / `.title2` | Section headers |
| `.headline` | List row primary label |
| `.body` | Default body text |
| `.caption` | Secondary/metadata |

### SwiftUI Component Decision Tree

**Scrollable list of items?**
→ `List` (if interactive rows) or `ScrollView + LazyVStack` (if custom layout)

**Modal sheet?**
→ `.sheet` for task-focused overlays, `.fullScreenCover` only if sheet swipe-dismiss would lose data

**Confirmation / destructive action?**
→ `.confirmationDialog` (not `Alert` unless no cancel needed)

**Picker with many options?**
→ `.pickerStyle(.wheel)` in sheet, `.menu` for compact inline

**Loading state?**
→ `ProgressView()` centered, skeleton views for content-heavy screens

**Empty state?**
→ `ContentUnavailableView` (iOS 17+) or custom VStack with icon + title + description

---

## Accessibility Checklist

- [ ] All interactive elements ≥ 44×44pt
- [ ] Text uses semantic styles (`.headline`, `.body`) not fixed sizes — supports Dynamic Type
- [ ] Images have `.accessibilityLabel` or `.accessibilityHidden(true)` if decorative
- [ ] Color is not the sole means of conveying information
- [ ] Contrast ratio ≥ 4.5:1 for normal text, ≥ 3:1 for large text
- [ ] Buttons have clear `.accessibilityLabel` when icon-only
- [ ] List rows have `.accessibilityElement(children: .combine)` when needed

---

## WhereWeGo Theme Compliance

| Token | default | summer | xmas |
|-------|---------|--------|------|
| Primary accent | System blue | Orange | Red |
| Background | System background | Light sand | Dark green |
| Implementation | `LSThemeManager.shared.theme` switch in private helper |

**Rule:** Never hardcode colors. Always route through the theme helper.

---

## Output Format

For each design question, provide:
1. **Recommendation** — specific SwiftUI component or pattern
2. **HIG rationale** — 1 sentence why
3. **Accessibility notes** — any required labels/modifiers
4. **Code snippet** — minimal SwiftUI example (if helpful)
5. **Escalate?** — flag if this needs full designer subagent
