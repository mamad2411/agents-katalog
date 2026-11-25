---
name: android-localization-accessibility
description: |
  Localization and accessibility patterns for Android/Compose - string resources, pluralization, RTL, semantics, screen reader support, focus order, and inclusive UI review. Use this skill whenever adding user-facing copy, localizing screens, improving accessibility, or reviewing whether a Compose UI works well across languages and assistive technologies. Trigger on phrases like "localization", "translations", "RTL", "TalkBack", "semantics", "accessibility", "plural", or "screen reader".
---

# Android Localization and Accessibility

## Core Principles

- User-facing text must be localizable by default.
- Accessibility is a product requirement, not a later polish step.
- UI must remain understandable with screen readers, keyboard/focus navigation, and larger text.
- Layouts should tolerate language expansion and RTL direction.
- Semantics should describe intent, not just visual structure.

---

## String Resources

Do not hardcode user-facing copy in composables or ViewModels when the text should be localized.

Use resources for:
- labels
- button text
- error messages
- content descriptions
- snackbar/toast messages
- empty/loading state copy

```kotlin
Text(text = stringResource(R.string.notes_empty_title))
```

Dynamic values that are never resource-backed can remain plain `String`. See the **android-presentation-mvi** skill for `UiText` guidance.

---

## Plurals and Formatting

Use plural resources and formatted strings instead of concatenation:

```kotlin
Text(
    text = pluralStringResource(
        R.plurals.note_count,
        state.count,
        state.count
    )
)
```

Avoid:
- string concatenation for localized sentences
- assuming English grammar/order
- embedding untranslated units in dynamic strings

---

## RTL Support

Design for bidirectional layouts:
- avoid hardcoded left/right concepts when start/end is correct
- prefer `start`/`end` padding and alignment
- verify icons and directional affordances in RTL
- ensure custom layouts do not assume left-to-right ordering

A screen that works only in LTR is incomplete.

---

## TalkBack and Screen Readers

Make interactive UI understandable without sight.

Guidelines:
- every actionable element should have clear semantics
- related content may need merged semantics
- decorative content should not create noise
- duplicate or redundant announcements should be reduced

Examples:
- icon-only buttons need meaningful labels
- custom cards may need explicit click/action semantics
- status chips may need state descriptions if color alone conveys meaning

---

## Content Descriptions

Use `contentDescription` intentionally:
- meaningful non-text image/icon -> localized description
- decorative image/icon -> `null`
- avoid describing information already adjacent as visible text unless needed for clarity

Over-describing everything creates noisy screen reader output.

---

## Semantics and Roles

Use semantics to express UI meaning:
- button role
- selected/checked state
- headings where they help navigation
- progress/state descriptions
- test tags only when needed for testing, not as a substitute for semantics

Custom components often need explicit semantics because visuals alone are not enough.

---

## Focus and Navigation

Users may navigate by keyboard, switch access, D-pad, or accessibility focus.

Check that:
- focus moves in a logical order
- dialogs and sheets trap or restore focus appropriately
- hidden/inactive content is not focusable
- important actions are reachable without precision gestures

---

## Text Scaling and Layout Resilience

Verify screens with larger font and display sizes.

Look for:
- clipped text
- overlapping controls
- unusable buttons
- fixed-height layouts that break with longer translations

Guidelines:
- avoid rigid heights for text-heavy content
- let content wrap naturally
- prefer responsive layouts over pixel-tight assumptions

---

## Color and Contrast

Do not rely on color alone to convey state.

Examples:
- error state should not be red text only; it may need icon/text/state label
- selected/unselected states should remain understandable without color perception

Contrast should remain strong enough for readability across themes.

---

## Forms and Error Messaging

Accessible forms should provide:
- clear labels
- helpful hints where needed
- explicit error text
- focus behavior that helps users recover

A red border alone is not an accessible validation strategy.

---

## Testing Guidance

Review with:
- screen reader enabled
- larger font size
- RTL locale
- keyboard/focus navigation where applicable
- common translated string expansion scenarios

Test:
- semantics for key actions
- plural/resource usage
- layout resilience under text growth
- announcements and focus behavior for dialogs/snackbars/forms

---

## Checklist: Localization and Accessibility Review

- [ ] Move user-facing strings into resources where appropriate
- [ ] Use plurals and formatted resources instead of concatenation
- [ ] Check layouts in RTL and with larger text
- [ ] Add or refine semantics for interactive/custom UI
- [ ] Use meaningful `contentDescription` only when needed
- [ ] Ensure focus order, error messaging, and state cues are accessible