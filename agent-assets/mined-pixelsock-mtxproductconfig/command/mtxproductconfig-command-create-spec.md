---
name: create-spec
description: Create a feature specification using Agent OS
---

Execute the Agent OS spec creation workflow by loading and running the instructions at `.agent-os/instructions/core/create-spec.md`.

This command will:
1. Identify the feature to spec (from roadmap or user input)
2. Gather requirements and context
3. Create spec documentation in `.agent-os/specs/YYYY-MM-DD-feature-name/`
4. Generate technical specifications and sub-specs as needed

Usage: `/create-spec [feature-description]`
       `/create-spec` (for next roadmap item)