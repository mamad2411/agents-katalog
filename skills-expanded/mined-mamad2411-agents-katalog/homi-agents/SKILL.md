# AGENTS.md for homi

## Project Shape

Homi is a static browser app.

- `/` is the public Homi introduction page.
- `/face` is the logged-in always-on face page.
- `/face/manage` is the logged-in face/data management page.
- `/engines/{engineId}` is the logged-in schedule or dictation editor.
- Ohmesh is the only persistence backend.

## Operations

After finishing a development change:

1. Run the relevant validation commands.
2. Stage only intended files.
3. Commit with `scripts/agent-commit.sh`.

Do not push or deploy unless explicitly requested.

Preferred commit format:

```sh
TYPE=feat SUMMARY="update face route" scripts/agent-commit.sh
```

## Validation Commands

- `pnpm run check`
- `pnpm run build`
