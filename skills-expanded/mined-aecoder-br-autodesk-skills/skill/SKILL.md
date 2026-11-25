# Skill Name

## Purpose

Describe the Autodesk API workflow this skill supports and the outcome it should help an assistant produce.

## Use When

- Use this skill when the user asks for...
- Use this skill when the task involves...
- Use this skill when the repository or product context includes...

## Do Not Use When

- Do not use this skill for...
- Hand off to another skill or workflow when...

## Workflow

1. Identify the Autodesk product, API family, version, and authentication context.
2. Load only the reference files needed for the task.
3. Confirm whether the task is documentation, implementation, troubleshooting, or review.
4. Apply the workflow-specific guidance.
5. Validate the result against official documentation, local tests, or reproducible evidence.
6. Call out version-sensitive assumptions.

## References

| Task | Reference |
| --- | --- |
| Overview | `references/overview.md` |
| Authentication | `references/authentication.md` |
| Examples | `references/examples.md` |

## Validation

- List the checks an assistant should run.
- Include expected outputs or failure signals when practical.
- State when live Autodesk documentation should be rechecked.

## Security

- Never expose Autodesk credentials, OAuth tokens, signed URLs, or private project data.
- Use placeholders for all secrets and private identifiers.
- Prefer least-privilege OAuth scopes in examples.

## Known Gaps

- List missing API areas, version gaps, or unverified behavior.
