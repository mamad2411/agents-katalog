---
name: atomic-instruction-milestone
description: Applies when an instruction describes a single, atomic action that can be directly translated into one executable milestone.
---
## Overview
This skill addresses instructions that are inherently simple and do not require complex decomposition into multiple sequential or parallel steps. It recognizes when an entire instruction can be treated as a single, self-contained unit of work, avoiding unnecessary sub-planning.
## When to Apply
- The instruction describes a singular, direct operation.
- The operation appears to be executable by a single primary tool or service.
- No explicit intermediate steps or data dependencies are stated or strongly implied.
## Procedure
1. Identify the core action and its direct target from the instruction.
2. Create a single milestone that encapsulates the entire instruction verbatim.
3. Assign the most appropriate primary tool or service for the identified action to this milestone.
## Key Patterns
- **Atomic Action Identification:** Recognize when an instruction represents a single, indivisible operation rather than a sequence of sub-tasks.
- **Direct Instruction Mapping:** The content of the milestone is a direct, unedited representation of the original instruction, indicating no further decomposition is needed.
## Common Pitfalls
- Attempting to decompose an inherently atomic instruction into unnecessary sub-steps.
- Misidentifying an instruction as atomic when it implicitly requires data retrieval or multiple distinct actions.
- Assigning an incorrect or overly generic tool when a specific one is clearly implied by the instruction.
