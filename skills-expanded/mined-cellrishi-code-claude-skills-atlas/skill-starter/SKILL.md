---
name: "{{skill-name}}"
category: "{{category}}"
tags: ["{{tag-1}}", "{{tag-2}}"]
---

# {{Skill Title}}

## Purpose

Explain the specific task this skill helps an agent or user complete, and the intended outcome. Keep the purpose focused and distinct from existing Atlas resources.

## When to use

Describe the situations, user requests, or conditions where this skill is useful. Also mention when an existing skill or a different workflow is a better fit.

## Instructions

Write clear, ordered instructions that an agent can follow. State important constraints, expected decision points, and how to handle uncertainty. Do not include secrets or instructions that compromise unrelated users, tools, or systems.

1. {{First actionable step}}
2. {{Second actionable step}}
3. {{Review the result and handle failures}}

## Inputs

List the information, files, tools, or context needed to use the skill. Mark optional inputs and explain any assumptions.

- Required: {{required input}}
- Optional: {{optional input or "none"}}

## Outputs

Describe the expected deliverable and its format. Explain what the agent should report if it cannot complete the task or lacks enough information.

- Expected output: {{deliverable and format}}
- Failure/uncertainty behavior: {{what to report}}

## Example

**Input:** {{representative user request or input}}

**Expected behavior:** {{briefly describe the main steps the skill should take}}

**Expected output:** {{illustrative result or output structure}}

## Limitations

Document known limitations, dependencies, unsupported cases, safety boundaries, and situations that require human review.

- {{Known limitation or boundary}}

<!-- Before submitting, replace every {{placeholder}}, confirm the frontmatter fields are valid, and add realistic examples. -->
