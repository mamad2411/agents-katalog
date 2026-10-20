# Continuation Edit

## When To Use

Use this skill when the user asks to modify work created in a prior turn or earlier in the current page or workspace.

Use it for revision workflows where the user wants changes to existing work rather than a new artifact from scratch.

Do not use it for:

- first-pass drafting with no prior artifact
- pure navigation or fact-finding tasks
- structured forms where the real challenge is field mapping rather than revision

## Procedure

1. Load relevant workspace turn memory.
2. Identify the current artifact being revised.
3. Read the existing content before editing.
4. Preserve prior requirements unless the user explicitly replaces them.
5. Apply the requested delta in place when possible.
6. Verify the requested change is present and no stable prior constraint was lost unintentionally.

## Required Evidence

- Relevant prior-turn memory
- Existing artifact contents before editing
- Updated artifact contents after editing

## Common Failures

- Overwriting prior constraints that were not revoked
- Editing the wrong field or artifact
- Re-drafting from scratch when the task is a revision

## Verification

- Use hybrid verification: deterministic checks for visible content changes plus LLM confirmation for tone or wording requirements when needed.

## Relevance

This is one of the strongest real-world workflow skills because revision across turns is a common browser-agent task.

Current strongest E2E targets:

- `tests/e2e/continuation.test.ts`
- `tests/e2e/continuation-cross-page-compose.test.ts`

Additional candidate targets:

- `tests/e2e/email-compose.test.ts`
