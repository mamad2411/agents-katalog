---
name: ui-edge-spotter
description: >
  Spot uncovered UI/UX edge cases in frontend code or ticket descriptions by asking "what if" questions 
  about layout, states, content, and interactions. Outputs issues the dev can evaluate — does NOT generate code.
  Use when: reviewing UI component code (dropdown, form, modal, table, input, search, stepper, OTP, tooltip, toggle), 
  checking tickets for missing edge cases, doing frontend code review, or when someone asks 
  "what UI issues am I missing", "spot edge cases", "review this component", "what could break", 
  "what did I forget", "UI audit", "what edge cases", or "QA check".
  Also triggers when user pastes React/Vue/Svelte/HTML/CSS/TypeScript code for any interactive component.
  Covers: layout overflow, empty/loading/error states, text overflow, responsive, touch targets, 
  dropdown positioning, form validation, keyboard navigation, and component-specific edge cases.
license: MIT
metadata:
  author: crazyads69
  version: "1.1.0"
  tags: ["ui", "ux", "edge-cases", "frontend", "code-review", "react", "what-if", "accessibility", "mobile"]
---

# UI Edge Spotter

Spot uncovered UI/UX edge cases by thinking in "what if" questions.

## Step 0 — Load the checklist (REQUIRED)

Before outputting anything, read the full contents of `references/checklist.md` in this skill's directory. It contains all the "what if" questions organized by component type. Do not skip this step — the checklist IS the skill.

## Step 1 — Identify components and pick sections

Look at the user's code or ticket. Identify which component(s) are present, then check ONLY the relevant sections:

| If you see... | Check these sections |
|---|---|
| Dropdown, select, combobox | Dropdown + Universal |
| Text input, textarea, password | Input + Universal |
| Form with submit | Form + Input + Button + Universal |
| Table, list, data grid | Table + Universal |
| Modal, dialog, drawer, sheet | Modal + Universal |
| Button, CTA, submit | Button + Universal |
| Search bar, filter input | Search + Universal |
| File upload, drag-and-drop | File Upload + Universal |
| Toast, snackbar, notification | Toast |
| Pagination, infinite scroll | Pagination + Universal |
| Tabs, accordion, collapse | Tabs + Universal |
| Image, video, media | Image |
| Date picker, time picker | Date Picker + Universal |
| Nav, menu, sidebar | Navigation |
| Card, tile, grid item | Card + Universal |
| OTP input, verification code | OTP + Universal |
| Stepper, wizard, multi-step | Stepper + Form + Universal |
| Tooltip, popover, hover card | Tooltip + Universal |
| Toggle, switch, checkbox | Toggle + Universal |
| Skeleton, loading placeholder | Skeleton |
| Badge, tag, chip | Badge + Universal |
| Any data mutation (create/update/delete) | Data Mutations |

Skip all other sections. Don't audit OTP when the user only has a dropdown.

## Step 2 — Run the what-if questions

For each relevant section, check every "what if" question against what's implemented. If the answer is "not handled" — that's a gap to flag.

## Step 3 — Output the audit

Use this exact format:

```
### 🔍 What-If Audit: [Component Name]

**Context**: [One sentence — what was analyzed]

---

#### ⚠️ What if [specific scenario]?
**Currently**: [What happens now, or "not handled"]
**Impact**: 🔴 Critical / 🟡 Should-have / 🟢 Nice-to-have
**Suggest**: [One-line direction, no code]

---

#### ✅ Already handled
- [Things done well — give credit]

#### 📊 Summary
🔴 N critical · 🟡 N should-have · 🟢 N nice-to-have
```

## Rules

1. **DO NOT generate code.** Only describe the issue and suggest a direction.
2. **Be specific.** "What if user has 50+ phone numbers? → dropdown pushes submit off-screen" — not "consider long lists."
3. **3-8 focused issues.** Lead with critical, skip trivial. Quality over quantity.
4. **Give credit** for what IS handled well.
5. **The dev decides** what to fix. Frame as questions, not demands.

## When NOT to flag

- Don't audit components the user didn't ask about. If they said "check the dropdown", don't audit the form.
- Don't flag mobile issues for explicitly desktop-only admin tools.
- Don't flag edge cases that require architectural changes for a small bugfix ticket.
- If unsure whether something is in scope, ask the user.

## Severity

- **🔴 Critical** — Breaks layout, makes feature unusable, loses user data, blocks main flow
- **🟡 Should-have** — Poor but functional, missing loading/error/empty state, broken on mobile, not keyboard-accessible
- **🟢 Nice-to-have** — Polish, < 1% of users affected, animation, micro-copy

## Example

Input: "Phone number dropdown, no height limit. What edge cases?"

```
🔍 What-If Audit: Phone Number Dropdown

Context: Custom select dropdown for phone numbers, no max-height set.

⚠️ What if user has 50+ phone numbers?
Currently: Dropdown grows forever, pushes submit button off-screen
Impact: 🔴 Critical
Suggest: Set max-height (~10 items visible) with overflow-y scroll

⚠️ What if user has 0 phone numbers?
Currently: Not handled — blank dropdown or nothing renders
Impact: 🟡 Should-have
Suggest: Empty state message with "Add a number" CTA

⚠️ What if dropdown opens near the bottom of the viewport?
Currently: List renders below trigger, gets cut off by viewport edge
Impact: 🟡 Should-have
Suggest: Flip dropdown upward when insufficient space below

⚠️ What if phone label is very long? (+84 123 456 789 — Số công ty chính)
Currently: Text overflows dropdown width, breaks layout
Impact: 🟡 Should-have
Suggest: Truncate with text-overflow ellipsis, show full text on hover/focus

⚠️ What if user wants to find a specific number in a long list?
Currently: Must scroll through entire list manually
Impact: 🟢 Nice-to-have
Suggest: Add search/filter input when list has 10+ items

✅ Already handled
- Dropdown opens/closes on click
- Selected value displays in trigger

📊 Summary
🔴 1 critical · 🟡 3 should-have · 🟢 1 nice-to-have
```
