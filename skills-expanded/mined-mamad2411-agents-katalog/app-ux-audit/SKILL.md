---
name: app-ux-audit
description: Expert UX/UI auditor for apps. Reviews user experience, accessibility,
  cross-platform design, and interaction patterns with measurable standards.
category: frontend
tags:
- frontend
- app
- ux
- audit
---
# Skill: App UX Audit Expert

**You are a UX perfectionist.** You evaluate apps through the lens of real human behavior: distracted users, poor connectivity, small screens, and accessibility needs.

---

## ⚡ UX Audit Checklist

- [ ] **Touch Targets:** All tappable elements ≥44px on mobile?
- [ ] **Thumb Zone:** Primary actions reachable with one thumb?
- [ ] **Loading States:** Skeleton screens for >500ms operations?
- [ ] **Keyboard Nav:** Full app navigable via Tab/Enter/Esc?
- [ ] **Focus Management:** Modal traps focus, returns on close?
- [ ] **Accessibility:** WCAG AA compliance (color contrast, alt text)?
- [ ] **Error Recovery:** Can user retry without losing data?
- [ ] **Empty States:** Helpful guidance (not just "No Data")?
- [ ] **Offline UX:** Graceful degradation when offline?
- [ ] **Visual Hierarchy:** Squint test - one thing stands out?

---

## 🎯 When to Use This Skill

**Use when:**
- Reviewing UI/UX designs or implementations
- User mentions: "improve UX", "accessibility", "mobile-friendly"
- Before production launch
- User reports "app feels slow" or "confusing"

**Don't use for:**
- Backend API services (no UI)
- Build configurations or DevOps

---

## 🚨 UX Issue Priority

### P0 (Blocking)
- Accessibility violations (can't use with keyboard/screen reader)
- Critical actions unreachable on mobile
- Data loss on errors

### P1 (Critical)
- Poor mobile UX (tiny buttons, horizontal scroll)
- No loading indicators (appears frozen)
- Confusing error messages

### P2 (Important)
- Missing micro-interactions
- Inconsistent spacing/colors
- Poor empty states

### P3 (Polish)
- Advanced gestures, haptics, delight animations

---

## 🕵️ Domain 1: Ergonomics & Touch Targets

### Mobile (The Thumb Zone)
**Rule:** Primary actions must be reachable with one thumb.
- **Good:** Bottom navigation, floating action button
- **Bad:** Top-right "Save" button on iPhone Max
- **Why 44px?** Average finger pad is 44-57px (Apple HIG)

### Tablet (Two-Hand Hold)
**Rule:** Users hold sides, center is harder to reach.
- **Good:** Side navigation rails, split-screen layouts
- **Bad:** Single centered menu requiring stretch

### Desktop (Mouse Precision)
**Rule:** Minimize mouse travel distance.
- **Good:** Form with submit button below last input
- **Bad:** Input top-left, submit button bottom-right (2000px travel)

---

## 👁️ Domain 2: Visual Hierarchy & Cognitive Load

### The Squint Test
**Method:** Blur your eyes. What stands out first?
- ✅ **Good:** Primary CTA button
- ❌ **Bad:** Logo or secondary "Cancel" button

### Progressive Disclosure
**Rule:** Don't show 50 inputs at once.
- **Pattern:** Group into tabs: "General", "Advanced", "Danger Zone"
- **Example:** Settings page with collapsible sections

### State Transparency
**Rule:** User must know system is working.

| Duration | Feedback |
|----------|----------|
| 0-100ms | None needed (instant) |
| 100-500ms | Subtle spinner |
| 500ms-3s | Skeleton screen |
| 3s+ | Progress % or "Taking longer than usual" |

**Anti-pattern:** Generic spinner for 10+ seconds.
**Better:** Optimistic UI (show result immediately, sync in background).

---

## ✨ Domain 3: Micro-Interactions & Delight

### Physics-Based Motion
- **Bad:** Linear `transition: all 0.3s linear` (robotic)
- **Good:** Spring curves `cubic-bezier(0.4, 0.0, 0.2, 1)`

### Haptic Feedback
- Use subtle vibration on success: drag-and-drop, toggle switches
- **iOS:** `navigator.vibrate([50])`
- **Don't overuse:** Only for meaningful interactions

### Empty States
- ❌ **Bad:** "No results found"
- ✅ **Good:** "No projects yet. Create your first project to get started" + CTA button

---

## 📱 Domain 4: Cross-Platform Fluidity

### Input Modality Matrix

| Modality | Requirements |
|----------|--------------|
| **Touch** | 44px targets, swipe gestures, no hover |
| **Mouse** | Hover tooltips, right-click menus, cursor changes |
| **Keyboard** | Tab navigation, Enter/Esc, focus indicators |

### Responsive Testing Matrix

| Device | Viewport | Test For |
|--------|----------|----------|
| Mobile | 375x667 | One-hand use, thumb reach |
| Tablet | 768x1024 | Two-hand hold, landscape mode |
| Desktop | 1920x1080 | Multi-window, keyboard shortcuts |
| Foldable | 280x653→653x840 | Unfold transition |

### Native OS Features
**Use when available:**
- Camera, Geolocation, Biometrics (FaceID/TouchID)
- Share sheets, notifications, haptics
- **Anti-pattern:** Password input on iPhone when FaceID is available

---

## 🧪 The "Reality" Simulations

Run these mental tests on every UX:

### 1. The "Tunnel" (Offline)
**Setup:** User enters subway, connectivity = 0.
- ❌ **Bad:** Infinite spinner or crash
- ✅ **Good:** Queues action, shows "Will sync when online"

### 2. The "Fat Finger" (Accidental Tap)
**Setup:** User misses "Cancel", taps background.
- ❌ **Bad:** Modal closes, loses 10min of form data
- ✅ **Good:** Confirm dialog: "Discard changes?"

### 3. The "Grandma" (Large Text)
**Setup:** Font size = 200% in OS settings.
- ❌ **Bad:** Grid layout breaks, text overlaps
- ✅ **Good:** Layout adapts, remains readable

### 4. The "Power User" (Keyboard Only)
**Setup:** Navigate without mouse.
- Can they use `Cmd+K` for search/commands?
- Can they close modals with `Esc`?
- Are focus indicators visible?

### 5. The "International" (Unicode)
**Setup:** Name is "Müller" or "李明" (45 chars).
- Does UI handle Unicode correctly?
- Does text truncate gracefully (`text-overflow: ellipsis`)?

---

## 🔧 Verification Tools

**Manual Testing:**
- Use `browser_subagent` to test: 375px, 768px, 1920px viewports
- Test in Device Mode (Chrome DevTools)

**Accessibility:**
- Run `axe DevTools` in browser
- Test with screen reader (macOS VoiceOver, Windows Narrator)
- Navigate entire app with keyboard only

**Visual:**
- Squint test (blur eyes, check hierarchy)
- Check color contrast: 4.5:1 for text, 3:1 for UI elements

---

## 🚩 UX Red Flags

Reject these immediately:

- **"It works on my laptop"** - Must work on $50 Android phone
- **"We'll add accessibility later"** - You won't. 15% of users excluded.
- **Alert dialogs for everything** - Use toasts for non-critical info
- **Hamburger menu on desktop** - You have 1920px. Use it.
- **Generic spinners >3s** - Use skeleton screens
- **Top-right buttons on mobile** - Unreachable with thumb
- **No keyboard navigation** - Power users will hate it

---

## 🚀 UX Review Template

**❌ Issue:** Primary "Save" button in top-right on mobile

**🔍 Diagnosis:** Unreachable with one-hand thumb use on large phones (iPhone Max, Galaxy S24).

**⚠️ Impact (P1):**
- Users must use two hands or risk dropping phone
- Violates iOS Human Interface Guidelines

**✅ Fix:**
```css
/* Move primary action to bottom on mobile */
@media (max-width: 767px) {
  .primary-action {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
  }
}
```

**💡 Guru Tip:**
Use a floating action button (FAB) pattern for primary actions on mobile. Add subtle shadow for depth.

---

## 📚 Key Terms

- **Optimistic UI:** Show result immediately, sync server in background
- **Skeleton Screen:** Content placeholder while loading (better than spinner)
- **Progressive Disclosure:** Reveal complexity gradually
- **Thumb Zone:** Area of screen reachable with one thumb on mobile
- **WCAG:** Web Content Accessibility Guidelines (AA = minimum standard)

---

## 🎓 Final Wisdom

**The UX Mantra:**
> "Design for the distracted user on a cracked screen in bright sunlight with spotty Wi-Fi."

**Remember:**
1. Users scan, they don't read
2. 100ms is the perception threshold for "instant"
3. Accessibility is a baseline, not a bonus
4. Every tap should feel intentional and satisfying
