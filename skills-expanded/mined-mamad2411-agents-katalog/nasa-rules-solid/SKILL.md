---
name: nasa-rules-solid
description: Apply NASA's 10 rules and the SOLID principles while writing or checking Rust code - short functions, bounded loops, no recursion, no unwrap or unsafe, small traits, dependency inversion. Use this skill whenever the Developer role writes Rust code, the Reviewer or Architect checks code against safety and design rules, or a task mentions NASA rules, SOLID, safety-critical style, or coding standards.
---

# nasa-rules-solid

These rules exist because the software may run in places where a crash or a silent wrong result is costly. They also make code easier to read and test.

## Procedure

1. Read the mapping to Rust in `references/nasa-rules-rust.md` and the SOLID notes in `references/solid-rust.md`. The project file `$RUST_DEV_ENV/reference-projects/PRINCIPLES.md` has priority if it differs.
2. While coding, keep the short list in mind: functions of about 60 lines or fewer, bounded loops, no recursion, no `unwrap`/`expect`/`panic!`, no `unsafe`, every `Result` handled, smallest scope, zero warnings.
3. After coding, run the scanner on your crates:

```bash
python3 $AGENT_INFRA_DIR/harness/library/skills/principles-check/scripts/rust_rules_scan.py crates/ --strict
```

4. Fix each finding or write why it is acceptable in a code comment (`// Rule 7: value checked above`) and in the issue comment.
5. For SOLID, check each new type and trait against the table in `references/solid-rust.md`.

## Rules

- Do not weaken a rule to make code pass. Change the code.
- A deviation needs a reason that another person can check.
- If a requirement forces a deviation (for example allocation in a loop), say so to the Coordinator. They decide whether to record an ADR.
