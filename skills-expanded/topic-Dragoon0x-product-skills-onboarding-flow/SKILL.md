---
name: onboarding-flow
description: "Design first-run experiences that create the aha moment fast. Reduces time-to-value by sequencing actions, progressive disclosure, and contextual guidance. Use when building signup flows, product tours, or empty states."
---

# Onboarding Flow

Design first-run experiences that create the aha moment fast.

## How to use

- `/onboarding-flow` Apply onboarding constraints to this conversation.

## Constraints

### Time to Value
- MUST identify the product's "aha moment" and design the fastest path to it
- MUST get the user to experience core value within the first session
- NEVER front-load setup. Let people use the product, then configure.
- SHOULD show real output (even with sample data) before asking for input
- The first action should produce a visible, valuable result

### Sequencing
- Step 1: One meaningful action (not account settings)
- Step 2: Show the result of that action
- Step 3: Invite the next step based on what they just did
- NEVER show all features at once. Progressive disclosure.
- MUST allow skipping. Not everyone needs the same path.

### Guidance Patterns
- Tooltips: for single-element focus. Max 2 per session.
- Checklists: for multi-step setup. Show progress. Celebrate completion.
- Empty states: treat as onboarding surfaces, not error states.
- NEVER use modal tutorials that block the interface
- SHOULD use contextual hints that appear when relevant, not all at once

### Anti-Patterns
- Mandatory product tours that can't be dismissed
- Asking users to invite their team before they've used the product
- Settings pages as the first screen after signup
- Feature tours that explain what things do instead of why they matter
- Congratulating users for completing setup (celebrate value, not admin)
