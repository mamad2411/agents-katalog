---
name: codex-enable-web-search-catalog
description: Download the latest official Codex models.json from openai/codex main, generate codex-model-catalog.json with Responses Lite disabled for every model, enable live Web Search, and set the active custom provider display name to OpenAI. Use when a Windows Codex API installation loses hosted web_search tools, routes GPT-5.6 tools through input[].additional_tools, has no models_cache.json, or needs optional custom model aliases cloned from official model metadata.
---

# Enable Codex Web Search Catalog

Download the latest official model catalog on every run and make only the client compatibility changes needed for non-Lite hosted Web Search.

## Workflow

1. Locate Codex home from `CODEX_HOME`, falling back to `~/.codex`.
2. Confirm that `config.toml` exists. Do not require or read `models_cache.json`.
3. Preview the operation:

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/Enable-CodexWebSearchCatalog.ps1 -Preview
   ```

4. Explain that every run downloads the current `main` version of:

   ```text
   https://raw.githubusercontent.com/openai/codex/main/codex-rs/models-manager/models.json
   ```

5. Explain that the script will:
   - preserve every official model, including `codex-auto-review`;
   - set every model's `use_responses_lite` to `false`;
   - preserve official context windows, reasoning levels, modalities, tool modes, and other metadata;
   - write the result to `codex-model-catalog.json`;
   - back up `config.toml` before changing it;
   - set top-level `model_catalog_json = "codex-model-catalog.json"` and `web_search = "live"`;
   - set `name = "OpenAI"` only in the active `[model_providers.<model_provider>]` section.
6. Do not ask about custom names by default. When the user explicitly provides a custom model name, obtain an exact `custom-slug=official-base-slug` mapping and pass it with `-CustomModel`.
7. Obtain confirmation before changing the user's Codex home, then run without `-Preview`.
8. Validate the generated JSON, unique slugs, `codex-auto-review` preservation, and provider section.
9. Tell the user to fully restart Codex.

## Custom model aliases

Clone an official entry only when the user explicitly requests it:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/Enable-CodexWebSearchCatalog.ps1 `
  -CustomModel 'company/gpt-5.6-sol=gpt-5.6-sol'
```

Pass multiple aliases as repeated values or a PowerShell array:

```powershell
-CustomModel 'company/sol=gpt-5.6-sol','company/terra=gpt-5.6-terra'
```

The script copies the complete official base entry and changes only `slug`, `display_name`, and the final non-Lite setting.

## Custom paths

```powershell
powershell -ExecutionPolicy Bypass -File scripts/Enable-CodexWebSearchCatalog.ps1 `
  -CodexHome C:\path\to\.codex
```

Override provider selection only if `config.toml` has no usable top-level `model_provider`:

```powershell
-ProviderKey custom
```

## Boundaries

- Never print API keys, authorization headers, or the complete `config.toml`.
- Never replace the whole config; patch only the three named settings.
- Never remove or disable `codex-auto-review`.
- Never invent model context windows or capabilities.
- Fail without modifying files if the download, JSON parse, catalog validation, or alias mapping fails.
- Do not claim this guarantees Web Search. The gateway must preserve the top-level `web_search` tool and route it to a backend that supports hosted search.
- This avoids the Responses Lite request layout; it does not implement `/v1/alpha/search`.
- The user requested the unpinned `main` catalog. Warn that a future catalog may require a newer Codex client.

## Resource

Run `scripts/Enable-CodexWebSearchCatalog.ps1` for all changes.
