# Plugin boundary

- Import lifecycle APIs from `@termco/kernel` and product contracts from their owning `@termco/*-base` packages; `termco-plugin.json` is the dependency source of truth.
- Do not import `src/`, `electron/`, `@/`, or another plugin directory.
- Keep browser views, CDP state, sessions, observation, automation, and tests here.
- Use declared capabilities for application events and other shared services.
