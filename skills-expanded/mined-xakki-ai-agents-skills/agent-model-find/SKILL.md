---
name: agent-model-find
description: 'Resolve optional model-tier settings through the active agent runtime. Use when a task needs model selection or a delegation policy is configured. RU: выбор модели, уровни моделей.'
---

# Model tiers

Use when a task explicitly needs model selection or the user has configured a delegation policy. The optional `AI_MODEL_CHEAP`, `AI_MODEL_STANDARD` and `AI_MODEL_JUDGMENT` values are runtime-specific selectors, not universal model names. Read them from the agent's supported environment or configuration interface, and verify that each selector and any model override is supported and authorized in the active runtime.

Keep the inherited model when no applicable override is requested or supported. An unset tier is unconfigured, not permission to invent a selector or substitute another provider's model. Profiles, role names and model selectors are distinct; preserve any required named profile and follow its actual capabilities.

For Claude-specific configuration and its shipped aliases, see [the conditional reference](reference.md). Other runtimes must use their own documented configuration and discovery interfaces. A session-start hook may report tier settings as hints; it does not override the user's model choice or require a model argument on every delegation.
