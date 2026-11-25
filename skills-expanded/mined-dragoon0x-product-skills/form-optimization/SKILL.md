---
name: form-optimization
description: "Reduce abandonment in every form, signup, and checkout flow. Multi-step logic, field reduction, inline validation, and completion micro-copy. Use when building signup flows, checkout pages, or any multi-field input."
---

# Form Optimization

Reduce abandonment in every form, signup, and checkout flow.

## How to use

- `/form-optimization` Apply form optimization constraints to this conversation.

## Constraints

### Field Reduction
- MUST justify every field. If you can't explain why it's needed now, remove it.
- SHOULD collect the minimum at signup, gather the rest during onboarding
- Name fields: only ask if you'll use the name in the product experience
- Phone number: only ask if you'll actually call or text them
- NEVER ask for information you can infer or look up

### Multi-Step Logic
- Break forms with 5+ fields into steps
- Show progress: "Step 2 of 3" with a visual indicator
- Group related fields in the same step
- MUST save progress between steps (don't lose data on back navigation)
- Final step should feel like a confirmation, not another form

### Validation
- MUST validate inline (as the user completes each field, not on submit)
- Error messages MUST say what went wrong AND how to fix it
- NEVER clear the form on submission error
- SHOULD use positive confirmation (green checkmark) for valid fields
- Password requirements: show them before the user types, not after they fail

### Micro-Copy
- Labels above fields, not inside (placeholders disappear and confuse)
- Help text below fields for anything non-obvious
- Button text should describe the outcome: "Create account" not "Submit"
- MUST show what happens after submission ("We'll email you a confirmation")
