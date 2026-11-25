---
name: team-ux
description: UX design specification writing. Screen flows, state inventory, component list, accessibility and mobile behavior. The playbook of the ux role.
---

# UX Design Specification

You are writing a **specification**, not pixels. Implementation details are the developer's job.

## 1. Main flow

For each flow:

```
Flow: <what they want to do>
1. <screen> — what the user sees, what they can do, what decision they make
2. <screen> — ...
3. <result screen>
```

Each step must answer "what can the user do here?". If there is no answer, the step is unnecessary.

## 2. Screen inventory

| Screen | Purpose | Entry | Exit | States |
|---|---|---|---|---|

**The states column is mandatory for every screen:**

| State | What is shown | What can be done |
|---|---|---|
| Loading | skeleton loader | cancel |
| Empty | text explaining what to do + a primary action | trigger the action |
| Error | what happened + what will happen | try again / support |
| Populated | the content | interact with the content |
| Unauthorized | access denied + why | go back / support |

The empty state is the most frequently forgotten one and the most expensive one: the user meeting an empty screen on first open kills the product.

## 3. Component inventory

| Component | Where it is used | States | Note |
|---|---|---|---|

If the same button style was copied in three places, it should be a single component. Every repeated interface piece goes in here.

## 4. Accessibility (WCAG 2.1 AA)

Check for each screen:

- **Keyboard**: all interactive elements are keyboard reachable, the tab order is logical, when a modal opens the focus stays inside and Esc closes it.
- **Focus**: a visible focus ring (do not remove it). When the page changes, focus moves to the top.
- **Contrast**: text 4.5:1, large text and icons 3:1.
- **Screen reader**: meaningful `aria-label`, `role`, `aria-live` (for state changes), form errors linked with `aria-describedby`.
- **Color does not carry meaning alone**: an error is not only red, it also has an icon + text.
- **Motion**: `prefers-reduced-motion` is supported.
- **Touch target**: at least 44x44 px.

## 5. Mobile behavior

- Screen < 768px: which components are hidden, which are rearranged?
- Table: horizontal scroll or cards?
- Modal: full screen?
- Form: single column or grouped?
- Is there a bottom navigation, and how many items?

## 6. Tone and microcopy

- Button text: names the action ("Save Invoice", "Send", not "OK").
- Error message: what happened + what to do ("The invoice could not be uploaded. The file must be smaller than 10 MB.")
- Empty state text: what will happen ("You have no invoices yet. Upload your first invoice" + button).
- Confirmation: is it reversible, or not?

## Common mistakes

| Mistake | The right way |
|---|---|
| Giving color codes | Define hierarchy and behavior |
| Only the "happy path" | Empty/error/loading/unauthorized are mandatory |
| Skipping the error state | Show errors on every form field |
| Thinking about accessibility later | An AA check for every screen |
| "John Doe" sample data | Realistic, localized sample data |

## Output format

Markdown. Sections: Main flow / Screen inventory / Component inventory / Accessibility notes / Mobile behavior / Microcopy.

In the user's language (Turkish or English).
