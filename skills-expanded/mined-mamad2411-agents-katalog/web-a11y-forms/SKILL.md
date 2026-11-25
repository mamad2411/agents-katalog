---
name: web-a11y-forms
description: Designs and reviews accessible forms, search, validation, errors, grouping, required state, multi-step flows, and recovery behavior. Use when implementing or auditing form-heavy UI.
---

# Web A11y Forms

## Form Rules

For label and validation examples, see [EXAMPLES.md](EXAMPLES.md).

1. Every field needs a persistent programmatic label.
2. Placeholder text must not be the only label or instruction.
3. Use native inputs and controls unless a custom widget is truly required.
4. Group related controls with `fieldset` and `legend` when the group label matters.
5. Associate help, constraints, and errors with the relevant control.
6. Preserve user input and focus context after validation failures.

## Checklist

```markdown
Forms checklist

- [ ] Labels are explicit and durable
- [ ] Required/optional state is clear
- [ ] Help text and constraints are discoverable
- [ ] Errors are specific, linked to fields, and recoverable
- [ ] Error summary supports quick navigation when useful
- [ ] Search exposes query context, result count, and no-result guidance
- [ ] Multi-step forms expose current step and progress
```

## Output

Document labeling strategy, validation flow, error recovery, focus behavior, and test steps for invalid and corrected input.
