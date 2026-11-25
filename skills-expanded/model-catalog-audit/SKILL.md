---
name: model-catalog-audit
description: Audit the in-tree model catalog against each provider's live API (Anthropic, OpenAI, Google, OpenRouter, xAI) using the keys in .env. Surfaces new models the catalog is missing, catalog models a provider no longer returns, and price/context drift on the curated OpenRouter subset, so the catalog stays current. Works on both stacks (docker containers or host venv). Run periodically or when a provider ships new models / changes pricing.
---

Keep `src/uniffy/data/models/catalog.json` current by diffing
it against what the providers actually serve. The catalog is the source of truth
for the model list, pricing, capabilities, and image-gen support (see
`.agents/rules/agents.md`), so it drifts as providers ship and retire models.

## When to use

- Periodically (e.g. monthly) to catch new models and retirements.
- When someone reports a missing model, or a provider announces a launch.
- After a pricing change announcement (the audit finds the models; you research
  the prices).

## Steps

1. **Detect the stack** (same protocol as the stack notes in `AGENTS.md`) - never
   assume:

   ```bash
   docker compose ps -q --status running backend
   ```

   - Output non-empty -> **docker stack**: the backend container has the venv,
     the repo bind-mounted at `/app`, and `.env` injected via `env_file`.
   - Empty -> local ONLY if `.venv/bin/python` exists on the host. A bare
     `.venv` directory does NOT count (empty or root-owned leftovers happen and
     `uv` will fail trying to populate them).
   - Neither -> **docker**: the command below falls back to a one-off
     `run --rm` backend container (compose builds the dev image on first use).
     Never fix a broken host `.venv` by letting `uv` sync onto the host.

2. **Run the audit** from the repo root. `deps run -s backend` is a raw `uv`
   passthrough that targets whichever stack you detected:

   ```bash
   # docker stack (default)
   ./manage.py deps run -s backend run python .agents/skills/model-catalog-audit/scripts/audit_models.py

   # local stack
   ./manage.py deps run -s backend --stack local run python .agents/skills/model-catalog-audit/scripts/audit_models.py
   ```

   It loads provider keys from `.env` (`CLAUDE_API_KEY`, `OPENAI_API_KEY`,
   `GOOGLE_GENAI_API_KEY`, `XAI_API_KEY`), lists each provider's live models,
   and diffs against the catalog. A provider with no key in `.env` is skipped.
   OpenRouter uses a public endpoint and needs no key, so it always runs. It is
   read-only - it never edits the catalog.

3. **Read the report.** Per provider:
   - **NEW** - a live model the catalog does not resolve. These are candidates
     to add. Expect noise from OpenAI/Google: embeddings, `tts-*`, `whisper-*`,
     `gpt-realtime-*`, `*-moderation`, `aqa`, `deep-research-*`, `computer-use-*`,
     `sora-*` are **not chat or image-generation models** - skip them unless we
     add a code path. Focus on chat models and image-gen models.
   - **UNSEEN** - a catalog model this key did not return. Often just means the
     account lacks access or it is a dated snapshot; do not delete blindly.
   - **openrouter** - different semantics. The catalog holds a deliberately
     curated subset of 400+ upstream models, so the script never reports NEW
     there. Instead it reports **MISSING UPSTREAM** (a catalog slug or alias
     the live list no longer serves - candidate for replacement or
     deprecation), **PRICE DRIFT** (catalog `cost_per_1m_*` vs live per-token
     prices times 1M, beyond a small tolerance), and **CONTEXT DRIFT** (catalog
     `context_window` vs live `context_length`).
   - **xai** - standard NEW/UNSEEN via `XAI_API_KEY`. When the richer
     `/v1/language-models` endpoint responds with pricing, the same PRICE DRIFT
     report runs; otherwise the plain `/v1/models` list is used.

4. **Review the findings with the user** before adopting anything.

5. **Decide what to adopt.** For each NEW model worth adding (a real chat or
   image-gen model), and for any model whose pricing may have changed:
   - **Research capabilities + pricing on the web** - the anthropic/openai/
     google APIs do not return pricing. Use the provider's official
     pricing/docs page (this is the same flow used to add the Gemini "Nano
     Banana" models). Record the source. For openrouter entries the audit's
     PRICE DRIFT output already carries the live rates.
   - Confirm context window, max output tokens, vision/tools/reasoning support,
     and reasoning effort levels.

6. **Edit `catalog.json`** (catwalk-shaped - match existing entries):
   - Chat model: `id`, `name`, `cost_per_1m_in/out`, `cost_per_1m_in_cached`
     (cache write) + `cost_per_1m_out_cached` (cache read), `context_window`,
     `default_max_tokens`, `can_reason` (+ `reasoning_levels` /
     `default_reasoning_effort` when it reasons), `supports_attachments`.
   - Image model: set `supports_image_generation: true` and either
     `image_prices` (size/quality matrix) or `cost_per_image` (flat). Leave
     pricing out if genuinely unknown - the model is still selectable, cost just
     stays unrecorded.
   - Use `aliases` for `-preview` / `-latest` / dated variants that should
     resolve to one canonical entry.
   - For confirmed retirements, set `deprecated: true` and `sunset_date` rather
     than deleting, so existing references still resolve.

7. **Verify** on the same stack you detected in step 1 (add `--stack local` for
   the host venv). The loader re-reads on file change:

   ```bash
   ./manage.py deps run -s backend run python -c "from uniffy.domains.agents.providers.catalog import loader; loader.load_catalog(); print('catalog valid')"
   ./manage.py deps run -s backend run pytest src/uniffy/tests/test_pricing.py -q
   ```

   A malformed catalog raises on load (hard fail), so a clean load means the
   schema is satisfied.

## Notes

- Price drift IS auto-detected for openrouter (its API exposes per-token
  prices), and for xai when `/v1/language-models` reports pricing. Anthropic,
  OpenAI, and Google expose no pricing, so their price changes remain a manual
  web-research step.
- New entries are picked up live (mtime reload); no restart needed to test.
- Do not commit anything from `.env` or print key values.
