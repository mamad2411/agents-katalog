---
name: skill-author
description: Design or improve a reusable Claude Agent Skill with precise activation criteria, focused instructions, examples, verification, and safe boundaries. Use when creating or refactoring a SKILL.md.
---

# Skill Author

Create skills that are reusable, testable, and easy for another contributor to understand.

## Process

1. Define one clear job for the skill.
2. Write an activation description that states when it should be used.
3. Keep instructions focused on behavior, not background exposition.
4. Separate required steps from optional guidance.
5. Include failure conditions and safety boundaries.
6. Add examples when they clarify invocation or expected output.
7. Define verification that can expose common failures.
8. Move large reference material outside the main skill.
9. Test against representative tasks.
10. Revise based on observed failures.

## Quality checklist

- Is the purpose specific?
- Is the trigger description useful?
- Are assumptions explicit?
- Is the output format clear?
- Can the skill be tested?
- Does it avoid unnecessary permissions or destructive actions?
- Does it duplicate an existing Atlas resource?

## Output

Return:

- Skill purpose
- Activation description
- Instructions
- Examples
- Verification plan
- Known limitations
