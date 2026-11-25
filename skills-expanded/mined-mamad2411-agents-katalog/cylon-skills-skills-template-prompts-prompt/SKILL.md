# Prompt: [Prompt Name]

## Purpose

Describe what this prompt is designed to accomplish. When should it be used? Which persona invokes it?

---

## Prompt Template

```
You are [Persona Name], the [role description] of the Cylon Swarm.

Your task is to [describe the goal of this skill invocation].

## Context

[Include any relevant background or runtime context here]

## Inputs

- param_one: {{param_one}}
- param_two: {{param_two}}

## Instructions

1. [First instruction]
2. [Second instruction]
3. [Return your result in the following format:]

\`\`\`json
{
  "result": "<your output>",
  "status": true
}
\`\`\`

## Constraints

- [Constraint one]
- [Constraint two]
```

---

## Variables

| Variable      | Source         | Description                        |
|---------------|----------------|------------------------------------|
| `param_one`   | caller-provided | Description of param_one          |
| `param_two`   | caller-provided | Description of param_two          |

---

## Notes

Any additional guidance on tuning or adapting this prompt for specific runtime environments.
