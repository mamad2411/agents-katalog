# Model

This directory contains the `ModelClient` interface, registry, adaptive model
routing, the `Preset` abstraction, and streaming behavior.

- Implementations (Anthropic SDK, OpenAI-compatible) live in
  `src/modules/model-clients/`.
- Avoid adding provider-specific implementation here; extend the registry
  through the module instead.
- `preset.ts` is the single shipped registry of `(harness, defaultModel,
  tiers, defaultEffort, authEnv)` bundles. `authEnv: []` means the harness
  authenticates through its own local login state and its adapter readiness
  must expose a non-network auth probe. New model ids land here when a vendor
  releases a tier; do not duplicate the mapping at consumer sites.
- `output-token-limits.ts` is the neutral request-budget resolver for shipped
  preset model ids. KOTA-native `ModelClient` callers use it after model
  routing; unknown operator model ids need an explicit
  `modelOutputTokenLimits` entry instead of a fallback literal.
- Resolution priority: `--preset` flag > `KOTA_PRESET` env > `config.defaultPreset`
  > shipped default. An explicitly named preset that does not exist throws
  loudly instead of falling through.
- `DEFAULT_MODEL_TIERS` in `model-router.ts` is the shipped default preset's tiers
  for requests that do not carry a resolved preset; consumers should query the active preset via
  `mergePresetTiers(preset, overrides)` instead of importing the constant
  directly.
- Model tests cover registry validation, resolution precedence, override
  behavior, adapter propagation, rejection, and observable routing. Do not copy
  shipped preset ids, model names, tier maps, token limits, or pricing rows into
  expected test catalogs; derive behavioral expectations from the canonical
  registry.

Scripted model responses are internal test support. They are not exported by
the production model barrel or included in the runtime build.
