# talktype — Claude Code instructions

Local-first AI voice dictation. Fork of [OpenWhispr](https://github.com/OpenWhispr/openwhispr) (pinned in `UPSTREAM.md`) with a `wrapper/` reliability layer.

## Golden rule

**`app/` is upstream. `wrapper/` is ours.**

- Changes to `app/` must be minimal and committed as numbered patches under `app/patches/` so `scripts/sync-upstream.sh` can rebase them cleanly.
- All novel logic (routing, fallback, health, prompts, hooks) lives in `wrapper/` and is unit-tested.
- `wrapper/` exports a single typed interface (`WrapperHooks` in `wrapper/src/index.ts`) that `app/` imports.

## Tech stack

- **App:** Electron + TypeScript (from OpenWhispr)
- **Wrapper:** TypeScript, tested with vitest
- **LLM providers:** Ollama (local, default) and Anthropic Claude Haiku 4.5 (cloud)
- **STT:** whisper.cpp (local) via upstream, optional NVIDIA Parakeet
- **Backend orchestration:** docker-compose (Ollama + optional services)
- **Config:** zod-validated JSON at `~/Library/Application Support/talktype/config.json`

## Commands

```bash
./scripts/bootstrap.sh          # one-shot setup (clone upstream, install, pull models)
./scripts/doctor.sh             # health diagnostic
./scripts/sync-upstream.sh      # rebase wrapper patches on upstream main

cd wrapper && npm test          # vitest unit tests
cd wrapper && npm run lint      # eslint

cd app && npm run dev           # launch dev app
cd app && npm run build         # production build

docker compose -f docker/docker-compose.yml up -d ollama        # backend
docker compose -f docker/docker-compose.yml --profile observability up -d   # + loki/grafana
```

## Coding conventions

- TypeScript strict mode everywhere. No `any` without a `// reason:` comment.
- All external I/O (LLM calls, file writes, Ollama, Anthropic) goes through a provider interface so it can be mocked in tests.
- Errors are typed (`WrapperError` union in `wrapper/src/reliability/errors.ts`) with a category, user message, and fallback action.
- No silent catches. Every catch logs through the structured logger.
- Config is read once at launch via zod parse; runtime mutations go through `config.update()` which re-validates.

## Reliability invariants

These must hold at all times:

1. **Never lose audio.** If STT or LLM fails, the last 60 s of raw audio is written to `~/Library/Logs/talktype/panic/` with a timestamp.
2. **Fallback ladder:** cloud LLM → local LLM → raw transcription → surfaced error. Never block the user on a failing provider.
3. **Health probes on every hotkey press**, not just at startup. Stale state is worse than no state.
4. **Config fails loud, early.** If config is invalid, the app refuses to start and prints the zod error path.

## When in doubt

- New feature → decide if it belongs in `app/` (UI, upstream-ish) or `wrapper/` (logic). Default to `wrapper/`.
- Upstream bug → check if it's fixed on OpenWhispr main first. Don't patch `app/` for bugs upstream will fix.
- Adding a dependency → prefer adding to `wrapper/` not `app/`. Keep `app/` as close to upstream as possible.

## Project context

Part of the `mosaleh-2Brain/` workspace. Sibling projects: `Life_logger/` (embedded audio pendant), `starframe/` (pre-internship framework). Future integration with the Second Brain goes through `wrapper/src/hooks/post-transcript.ts` — do not hard-code 2Brain logic into the app.
