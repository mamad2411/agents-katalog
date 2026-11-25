---
name: rtl-design-engineer
description: "Design, adapt, or package synthesizable RTL into meaningful clean testcases or reusable modules. Use when the user wants a new RTL block, wants to trim an existing open-source design into a standalone module, or needs a macro-free testcase with real functionality for synthesis/place/CTS experiments."
---

# RTL Design Engineer

## Role Boundary

This skill owns RTL-level work:
- selecting a realistic function block,
- building or trimming the RTL dependency closure,
- enforcing synthesizability and macro-free testcase constraints,
- and handing off a clean testcase package to synthesis / P&R flow.

This skill does **not** own final P&R conclusions. After testcase packaging, execution returns to `workflow-scoped-execution` or stage flows.

## Use This Skill When

Use this skill for requests such as:
- "build a clean testcase with no macro",
- "extract a meaningful RTL submodule from an open-source design",
- "design a standalone UART/AES/FIFO/router testcase",
- "prepare RTL that is synthesis-ready and suitable for placement/CTS experiments",
- "remove black-box or memory-macro dependencies from a testcase".

## Inputs

Provide or derive:
1. target function or candidate source RTL,
2. realism requirement (`real function`, not toy-only),
3. clean testcase constraints,
4. expected output contract.

## Output Contract

Return:
1. chosen testcase name,
2. why it is realistic,
3. why it is macro-free,
4. package paths,
5. unresolved risks before synthesis.

## Operational References

1. `references/clean-testcase-contract.md`
2. `references/testcase-workflow.md`
3. `references/package-and-validation.md`
