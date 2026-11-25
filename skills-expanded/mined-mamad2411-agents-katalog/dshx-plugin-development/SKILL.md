---
name: dshx-plugin-development
description: Create, modify, diagnose, review, package, or Preview-publish an out-of-tree DeepSeek Harness plugin authored with DSHX. Use for @becomeopc/dshx, create-dshx, dshx.config.ts, Host/Client contributions, defineLocale, Prompt, Settings, typed API, Slots, Conversation Components, dshx check/build/dev/inspect/add, and DSH Profile verification. Do not use for DSH core implementation or Framework Hub administration.
---

# DSHX Plugin Development

Build the requested plugin from project evidence and verify the actual DSH path it depends on. Keep DSHX build-time and runtime-thin; official DSH and Cordis retain runtime ownership.

## Establish the project contract

Read [references/development-workflow.md](references/development-workflow.md) before changing files. Classify the workspace as a new plugin, an existing DSHX plugin, or the DSHX framework repository. Inspect git state, lockfile/package manager, package manifest, config, entries, installed versions, Profile evidence, and tests. Use pnpm for DSHX repository work and generated Preview examples. Preserve unrelated work.

Prefer evidence in this order:

1. installed package types, manifest, and lockfile;
2. offline `dshx check` diagnostics;
3. runtime `dshx inspect` results for the active Composition;
4. current published DSHX references;
5. adjacent DSH source only for investigation, never as published compatibility proof.

## Route to the required authoring surface

Read only the relevant section of [references/api-map.md](references/api-map.md). Do not reconstruct public signatures from memory.

- Keep Node, secrets, filesystem, validation, and privileged actions in Host code.
- Keep React and Hooks in Client code; shared modules must remain portable contracts.
- Use `defineLocale()` for plugin-owned `zh`/`en` copy. Do not ask authors to augment `LocaleNamespaceMap`; raw namespace strings are only for provider-owned advanced integrations.
- Declare official runtime/provider packages at the manifest boundary. Generated Cordis injects do not replace `dsh.client.inject` package edges.
- Let official services own registries, scope, ordering, Prompt assembly, persistence, transport, replay, HMR, and disposal. Register long-lived resources with the official lifecycle.
- Treat Conversation Components and programmatic Tooling as Experimental.

## Prove the requested behavior

At minimum run the plugin's offline check, relevant tests, and build. Use runtime check and a real `dshx dev` session when the result depends on a Profile, registration, transport, UI, restart, or HMR. Verify the exact user path; distinguish offline/type/build evidence from real DSH evidence.

If packaging or Preview publication is requested, also read [references/release-checklist.md](references/release-checklist.md). Inspect the actual archive and preserve npm `latest`. Publishing, pushing, deploying, catalog submission, and Profile mutation beyond the requested development loop require explicit authorization.
