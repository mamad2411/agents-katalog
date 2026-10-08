---
name: "nuxt-office-base"
description: "Stable entrypoint for generated Nuxt guidance in this repository. Use for Nuxt SSR, hydration, pages, `runtimeConfig`, Nitro/h3, plugins, Nuxt UI, Nuxt Content, or Nuxt module work. If generated content is missing, regenerate it with `nuxt prepare`."
---

# Nuxt Skill Wrapper

This is the stable entrypoint for Nuxt guidance in this repository.
The full generated skill tree lives in the Nuxt build directory so the checked-in skill surface stays small.

## Generated content
- Entry: [../../../apps/office/base/node_modules/.cache/nuxt/.nuxt/skill-hub/nuxt-office-base/SKILL.md](../../../apps/office/base/node_modules/.cache/nuxt/.nuxt/skill-hub/nuxt-office-base/SKILL.md)
- Root: [../../../apps/office/base/node_modules/.cache/nuxt/.nuxt/skill-hub/nuxt-office-base](../../../apps/office/base/node_modules/.cache/nuxt/.nuxt/skill-hub/nuxt-office-base)

## Required workflow
1. Check whether the generated entry exists.
2. If it exists, open it and follow that generated skill instead of extending this wrapper.
3. If it does not exist, Run `nuxt prepare` from this project before continuing.
That regenerates the Nuxt build directory, refreshes types, and writes the generated Nuxt skill content.

## Notes
- Generated content is ephemeral and may be refreshed by Nuxt.
- This wrapper is the stable file that should remain in version control.
