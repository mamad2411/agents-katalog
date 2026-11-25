# /onboard

Use this skill from a repository root to generate an onboarding tour for an unfamiliar codebase.

## Current workflow

1. Run the deterministic scanner to detect repo shape and entry points.
2. Extract a verified spine from supported local language relationships.
3. Generate and validate a Mermaid diagram from the verified spine.
4. Cluster the remaining files into heuristic subsystems.
5. Build a synthesis prompt that only contains verified structure and short code signatures.
6. **When running as Claude Code skill**: Write prompt to file, ask Claude to synthesize JSON, then read JSON back to generate `ONBOARDING.md`.
7. Write `ONBOARDING.md` into the target repo root.

## Local command

```bash
npm run onboard -- .
```

Optional token-free preview first:

```bash
npm run map -- .
```

Optional prompt export:

```bash
npm run onboard -- . --prompt-out .onboard-prompt.txt
```

Optional synthesis input (for Claude Code skill flow):

```bash
npm run onboard -- . --synthesis-input .onboard-response.json
```

Optional external synthesis command:

```bash
npm run onboard -- . --synthesis-command "your-command-here"
```

## Product contract

- Repo brand: `spine`
- User-facing Claude Code command: `/onboard`
- Companion map-only command: `/map`
- Diagram rule: verified edges only, never guessed
- Output target: `ONBOARDING.md`

## Launch positioning

The clearest user story is:

1. `/map` shows the verified architecture preview
2. `/onboard` writes the full guide
3. `.claude/REPO_CONTEXT.md` keeps future Claude sessions grounded in the repo
