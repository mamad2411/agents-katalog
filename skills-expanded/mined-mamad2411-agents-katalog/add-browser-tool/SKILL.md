---
name: add-browser-tool
description: Add a browser-native or cloud tool to ZeroAgent Studio. Use for file, network, speech, provider APIs, custom script capabilities, or manifest presets.
paths:
  - src/tools/**/*
  - src/lib/ports.ts
  - src/lib/nodePorts.ts
  - src/orchestrator/dag.ts
  - src/types/**/*
  - src/components/**/*
  - tests/**/*
---

# Add Tool (registry)

## Choose a path

| Path | When | Files |
|------|------|-------|
| **Manifest preset** | Simple text/JSON transform, no UI, no side effects | One row in `src/tools/manifests/index.ts` + engine preset in `src/tools/engines/*Runner.ts` |
| **Curated module** | File picker, mic, fetch, cloud API, custom inspector | `src/tools/<tool>.ts` + entry in `CURATED_TOOLS` inside `src/tools/registry.ts` |

Most new utilities should be **manifest presets** — the palette has 180+ manifest entries backed by shared runner engines (`stringRunner`, `encodingRunner`, `hashRunner`, `jsonRunner`, `listRunner`, `mathRunner`, `dateRunner`, `validateRunner`, `flowRunner`, `regexRunner`, `generateRunner`, `htmlRunner`, `markdownRunner`, `csvRunner`, `compareRunner`). Use `getSiteStats()` for live counts — do not hardcode.

## Manifest preset (preferred for transforms)

1. Add a preset handler in the matching `src/tools/engines/<engine>Runner.ts` if needed
2. Add a row to `MANIFEST_TOOLS` in `src/tools/manifests/index.ts`:

```ts
textTool('my-tool-id', 'My Tool', 'Description', '🔧', 'string', 'trim', 'text')
// or custom entry with JSON_IN / JSON_OUT for json engine
```

3. Registry auto-merges manifests via `manifestToToolDefinitions()` — no manual `TOOL_REGISTRY` push
4. Add engine fixture tests in `tests/tools/engines/allRunners.test.ts`
5. `catalog.test.ts` enforces ≥100 tools, unique ids, and port defs

Manifest tools get default `inputs`/`outputs` (`text` → `text` or `json` → `text`). Inspector shows description + port legend + Test button only.

## Curated module (file / network / cloud / sandbox)

1. `src/tools/<tool>.ts` — implement `run` with typed ports:

```ts
run: async (inputs, config, ctx) => {
  const input = getPrimaryInput(inputs)
  const result = await doWork(input, config, ctx)
  return singleTextOutput(result)
}
```

2. `src/tools/registry.ts` — add one entry to `CURATED_TOOLS` with `inputs`, `outputs`, `paletteGroup`, `browserSubcategory: 'curated'`, `requirement`, `run` (or `wrapLegacyRun` during migration)
3. `src/components/inspector/ToolInspectorFields.tsx` — config fields + optional Test button
4. `tests/tools/<tool>.test.ts` — permissions denied, empty input, network/API errors

**Do not** add a `switch` in `dag.ts` or hardcode tools in `NodePalette.tsx` — the registry drives palette, icons, inspector labels, and execution.

## Registry entry checklist

- `id`: kebab-case (e.g. `text-transform`) — becomes `ToolType`
- `inputs` / `outputs`: `PortDef[]` from `src/lib/ports.ts` (`TEXT_IN`, `TEXT_OUT`, `JSON_IN`, …)
- `paletteDragType`: `tool-<id>` (e.g. `tool-text-transform`)
- `getPaletteTutorialTarget(dragType)` — add `palette-<id>` target (legacy aliases kept for quests)
- `paletteGroup`: `browser` | `cloud` | `custom`
- `browserSubcategory`: for browser tools — `curated` | `text` | `encoding` | `json` | `list` | `math` | `date` | `validate` | `flow`
- `requirement`:
  - `{ kind: 'none' }` — always available
  - `{ kind: 'browser', feature: 'speechRecognition' | 'speechSynthesis' | 'clipboard' }`
  - `{ kind: 'apiKey', provider: 'groq' | 'gemini' | 'openrouter' }`
- `run`: `(inputs: Record<string, PortValue>, config, ctx) => Promise<Record<string, PortValue>>`

## Ports & connections

- Chat: output `message` (text only)
- Agent: input `context` (text, multiple edges OK), output `out`
- Tools: from registry `inputs` / `outputs`
- `canConnect()` in `src/lib/ports.ts` — json→text OK; text→json blocked at connect time
- Edges persist `sourceHandle` / `targetHandle`; legacy workflows migrate on load (`src/lib/workflowMigration.ts`)

## Constraints

- No backend — client-only APIs (`fetch`, File System Access, Web Speech, Web Worker for custom script)
- Permissions: mic/file/clipboard only on explicit run; graceful cancel messages
- Scraper: text extraction; never inject raw HTML into React DOM
- Custom script: Web Worker sandbox, no network in v1, 8 KB / 8 s limits
- Log via `ctx.log` → orchestrator → `debugStore` (Activity log)

## Validate

```bash
npm run ci
```

Manual: wire tool node → agent → chat; run on canvas.

**Docs sync** (user-facing changes):

| Change type | Update |
|-------------|--------|
| New tool / ports | `GuidePage.tsx` Tools section if notable; `README.md` tool table if essential |
| Quest step / tool | `tutorialQuests.ts`, `tutorialValidators.ts`, Guide quests section, README quest table |
| Port rules | Guide wiring section, README typed ports, this skill |

**Rules:** `.cursor/rules/zeroagent-engineer.mdc` · `.cursor/rules/zeroagent-test-engineer.mdc`
