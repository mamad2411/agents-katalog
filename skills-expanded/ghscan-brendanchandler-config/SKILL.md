---
name: planit
description: Create concise plan.md for new feature implementation details.
---

## Instruction
1. Read the user's feature description in carefully.
2. Write the plan to @./plan.md in the CURRENT WORKING DIRECTORY (not in source dirs).
3. Do NOT implement any code -- only produce the plan document.
4. Use markdown format with clear sections: Goal, Current State, Changes Needed, Files Affected, Testing Steps, Todo List.
5. If the user leaves inline "NOTE:" entries in plan.md, update the plan accordingly.
6. Ask clarifying questions in the plan document and the user will add "NOTE:" comments responding to them.
7. When the plan involves generating or modifying code, include complete and thorough source code snippets (use unified diff format for modifications to existing files, plain code blocks for new code) to specify the intended implementation.

Here is the user's feature description:  $ARGUMENTS
