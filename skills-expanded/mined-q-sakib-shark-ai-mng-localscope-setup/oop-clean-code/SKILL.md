# OOP / Clean Code Skill


Apply to application code unless the language/framework strongly favors another paradigm.

## Rules
- One reason to change per class/module where practical.
- Encapsulate invariants.
- Keep public interfaces small.
- Prefer dependency injection.
- Prefer composition over inheritance unless inheritance models a real substitutable relationship.
- Avoid god classes and god services.
- Avoid boolean-flag APIs that hide multiple behaviors.
- Keep business logic independent of UI/framework details.
- Name according to domain intent.
- Avoid premature abstractions.

## Review
For each substantial class/service, ask:
- What responsibility does it own?
- What dependency does it require?
- Can it be tested without infrastructure?
- Is it cohesive?
- Is the abstraction buying anything?
