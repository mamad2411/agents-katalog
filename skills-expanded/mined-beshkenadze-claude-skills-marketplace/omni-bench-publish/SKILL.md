---
name: omni-bench-publish
description: Publish a scored omni-bench result (ASR or text-generation) to a leaderboard platform (e.g. bench.bshk.app) via its write API. Use when asked to publish, upload, submit, or "send a report" for an omni-bench result.json or parity-report.json — sharing ASR WER/RTFx numbers or text-generation TTFT/tok-per-s/prompt-cache numbers. Covers the one modality-agnostic `omni-bench publish` command and the MANDATORY secret handling: the api-key is injected from a secrets manager (1Password `op run` / AgentVault `av run`) at runtime, never read into context, never hardcoded.
version: 1.0.1
---

# Publishing omni-bench results (ASR or text generation)

Upload a **scored** `result.json` (and optionally a `parity-report.json`) to an
omni-bench results platform (default `https://bench.bshk.app`) via `POST
/api/v1/results`. The command is **identical for every modality** — ASR
(WER / RTFx) and text generation (tok/s / TTFT / prompt-cache): the scorer already
wrote the correct row shape and the platform detects the modality from it.

## Prerequisites

- A scored document from `omni-bench score` (publish the `result.json`, never a raw run-artifact).
- An **api-key** for the platform, held in a secrets manager (see the secret-handling section — do NOT paste it anywhere).
- The platform base URL.

## The command (same for ASR and text-gen)

`omni-bench publish` reads the key from `$OMNI_BENCH_API_KEY`; ownership is taken from the
key's principal server-side, never from the document body.

```
omni-bench publish --result runs/<run>.result.json [--parity runs/<run>.parity.json] --url https://bench.bshk.app
# → published result: <resultId> ({"resultId": …, "identityKey": "sha256:…"})
```

Add `--private` to stage the upload owner-only (`x-omni-visibility: private`).

## Secret handling — inject the key, NEVER read or hardcode it

Never `echo`/`cat` the key, never pass `--api-key <literal>` in scripts, never write
it to a committed file. Inject it into the publish command's **environment** at
runtime so the value never enters your shell or context. In order of preference:

- **1Password (`op run`) — recommended.** Put an `op://` *reference* (not the value) in an env-file:
  ```
  printf 'OMNI_BENCH_API_KEY=op://<vault>/<item>/api-key\n' > .env.omni
  op run --env-file .env.omni -- omni-bench publish --result runs/x.result.json --url https://bench.bshk.app
  ```
  If the field lives in a section, the reference includes it (`op://<vault>/<item>/<section>/api-key`); run `op item get <item> --format json` and copy the field's `reference` verbatim.
- **AgentVault (`av run`).** `av add OMNI_BENCH_API_KEY` (value entered at the TTY prompt, never an argument); an `agentvault.yaml` maps a profile to `{ ref: av://file/OMNI_BENCH_API_KEY, tier: normal }`; then
  `av run --profile <p> -- omni-bench publish --result runs/x.result.json --url https://bench.bshk.app`.
- **CI / other manager.** Expose `OMNI_BENCH_API_KEY` in the publish step's env only — e.g. GitHub Actions `env: { OMNI_BENCH_API_KEY: ${{ secrets.OMNI_BENCH_API_KEY }} }`.

`op read` / `av read` print a raw value — they are **human-at-a-TTY** tools (they refuse pipes/files), not for the agent. Always use the `run` wrappers, which resolve the reference into the subprocess env and keep the value out of your context.

## Full flow (either modality)

```
omni-bench prepare <task_id>          # e.g. asr.fleurs.ru.v1  OR  textgen.shared_prefix.en.v1
# Run YOUR host adapter over the manifest → run-artifact.jsonl:
#   Python: omni-bench run --adapter pkg.mod:factory --manifest data/<task>/manifest.json --out runs/x.jsonl
#   Swift:  Producer.run(transcriber: …)   (ASR)   |   Producer.run(generator: …)   (text-gen)
omni-bench score --artifact runs/x.jsonl --references data/<task>/references.jsonl --out runs/x.result.json
op run --env-file .env.omni -- omni-bench publish --result runs/x.result.json --url https://bench.bshk.app
```

**Never reimplement scoring** in a host — the centralized Python scorer is the trust anchor; emit hypotheses/generations and let it grade them.

## Response + verify

- `201 { resultId, identityKey }` on success.
- `401` wrong/missing key · `409` run_id already owned by another principal (or an identity race — retry) · `413` document > 4 MB · `422` schema (unsupported `schema_version`, or a degenerate row with no sortable metric).
- Verify on the board: `<url>/leaderboard?board=asr` (ASR) or `?board=textgen` (text generation); the run's detail at `<url>/result/<identityKey>`.

## Notes

- Schema is pinned; current omni-bench emits `0.1.0` (re-cut 2026-07-04 — the earlier pre-release 0.1.0/0.2.0 shapes are retired and rejected with 422; the platform accepts only the re-cut 0.1.0).
- Identity fields (`model.sha256`, `backend.build_sha`, `hardware.soc/mem_gb`, `run_profile.decode`) feed `identity_key` — fill them honestly or the parity join / dedupe breaks.
- A text-gen result with no references legitimately has `quality: null` — it still publishes (the ingest guard rejects only a row with no headline metric: ASR needs `quality`, text-gen needs `tok_per_s` or `ttft_s_p50`).
