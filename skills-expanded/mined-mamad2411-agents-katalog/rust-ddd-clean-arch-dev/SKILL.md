---
name: rust-ddd-clean-arch-dev
description: Implement Rust code with Domain-Driven Design and Clean Architecture - entities, value objects, ports, use cases, and adapters in the correct layer, with typed errors and no panics. Use this skill whenever the Developer role writes or changes Rust code, adds a feature, creates a new aggregate or use case, or must decide in which crate or module a type belongs, even for small changes.
---

# rust-ddd-clean-arch-dev

The Developer builds what the requirements and the Architect's design say. The layer rules are in `ddd-clean-architecture/references/layers.md`. Read them and the wiki pages `Architecture Overview`, `Domain Model`, and the ADRs before writing code.

## Procedure

1. Read the issue and its comments. Find the requirement IDs. If the design is missing or contradicts the requirement, do not invent one. Return the issue as `blocked`.
2. Write the test first (`rust-tdd`). Then write the smallest code that passes it.
3. Put code in the right layer:
   - Business rule or invariant: `domain` (entity, value object, domain service).
   - Workflow that uses rules: `application` (use case). It talks to the outside only through ports.
   - Database, file, network, clock: `infrastructure` (implements a port).
   - Wiring and input handling: `interface`.
4. For a new aggregate, generate the skeleton and then edit it:

```bash
python3 $AGENT_INFRA_DIR/harness/library/skills/rust-ddd-clean-arch-dev/scripts/scaffold_aggregate.py crates/domain Order
```

5. Follow `nasa-rules-solid` while coding. In short: short functions, bounded loops, no recursion, no `unwrap`, no `unsafe`, every error handled, zero warnings.
6. Run the gate before you finish:

```bash
$AGENT_INFRA_DIR/harness/library/skills/rust-tdd/scripts/tdd_cycle.sh
python3 $AGENT_INFRA_DIR/harness/library/skills/principles-check/scripts/rust_rules_scan.py crates/
```

7. Commit with the issue number in the message. Finish with `issue-completion`: list requirement IDs covered and the test result.

## Coding rules

- Make invalid states impossible: validate in the constructor of a value object, and return `Result`.
- Each layer owns its error enum. Convert at the border with `From`.
- Prefer small functions and explicit types over clever generics.
- Do not add features, options, or abstractions that no requirement asks for. Every extra line is a line to test and maintain.
- Do not add a crate before `crate-download-filter` has passed it.
