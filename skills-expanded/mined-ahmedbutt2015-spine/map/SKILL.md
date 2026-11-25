# /map

Use this skill from a repository root to generate the verified architecture map only, without the full onboarding synthesis.

## Current workflow

1. Run the deterministic scanner to detect repo shape and entry points.
2. Extract a verified spine from supported local language relationships.
3. Generate and validate a Mermaid diagram from the verified spine.
4. Print the Mermaid definition and the `mermaid.live` URL.

## Local command

```bash
npm run map -- .
```

## Product contract

- User-facing Claude Code command: `/map`
- Output: verified Mermaid diagram + `mermaid.live` link
- No `ONBOARDING.md` is written
- No LLM synthesis is executed

## Notes

This command is the lowest-friction entry point for users who want a deterministic, token-free preview of the codebase structure before running the full `/onboard` flow.
