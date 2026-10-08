# Task: New Requirements for BKP-004-REGISTRY-GENERATOR Implementation 

## Golder rule
* **Understand**: Ensure getting right the instructions. Warn any ambigueti and abort any output until it's clear what to do

# Mistakes or improvements

- All the slices must be on status "Planned" and phase "planning" before implementation.
- When the implementation starts pass the slice to status "In Progress", and the phase changes to "implementation"
- You didn't create a branch, make all the implementation in main. It's mandatory to always create a branch.
- Every 3 minutes it's needed to update the slice metadata by creating a commit in the branch.
- When the implementation ends It needs to create a PR and pass the slice to status "In Review", and the phase changes to "validation"

## Output
- Modify the plan-validator skill to enforce not to meet the improvementes required
- Modify all documentation if needed to align changes
- Generate a new documentation markdown to define all the changes in the slice status and phase. Which skill will be used and any other information needed. And the needed status and phase for any skill to act. It's mandatory to verify the information before starting any work. 