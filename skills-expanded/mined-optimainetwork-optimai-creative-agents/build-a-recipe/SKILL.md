---
name: build-a-recipe
description: Build, validate and share an OptimAI Creative Agents recipe (a portable v1 agent.json manifest). Use when asked to create or edit a creative agent, recipe or agent.json, pick a reviewed template, fix manifest validation errors, or prepare a recipe's prompt in the optimai-creative-agents SDK.
license: MIT
---

# Build a Creative Agents recipe

A recipe is a small JSON file (`agent.json`, manifest v1.0) that names one **reviewed template**, sets some of its **approved settings** and adds a **creative brief**. It is data, not code. Hosts such as OptimAI Studio import it and run the template's own engine.

Run every command from the SDK root (the folder with `package.json` named `@optimai/creative-agents`). Nothing here needs `npm install`, an account, a model or the network.

## Rules that never bend

- Never add fields. The manifest and `recipe` are closed objects: scripts, URLs, model names, credentials or extra keys fail validation.
- `capabilities` is always exactly `{ "network": "none", "execution": "declarative", "dataAccess": "selected-inputs" }` and `license` is always `"MIT"`.
- `recipe.templateId` must be one of the reviewed template IDs. You cannot invent a template in a recipe; a new engine is a code contribution (see `CONTRIBUTING.md`).
- `recipe.values` may only hold settings the chosen template declares, with values inside their bounds. Omitted settings use the template default, so set only what the creator asked for.
- `category` must equal the template's category. Copy it from the scaffold; do not guess it.
- Do not put personal data, secrets or private file paths in `title`, `description` or `brief`. Recipes are shared.
- Do not publish, push or upload anything. The commands below only write local files.

## Steps

### 1. Choose a template

List every template with what it really does:

```sh
npm run verify
```

Each line is `id: capability`. The capability tells the creator what to expect: *browser* templates produce a result on the device, *local-model* templates write text with a model the creator installs, and *studio-guided* templates prepare a prompt for a host to produce. Say which kind you picked; never describe a studio-guided template as generating media by itself. The grouped list is in `docs/catalog.md`.

### 2. Read the template's settings

```sh
node --input-type=module -e 'import { getAgentFormSchema } from "./src/form-schema.mjs"; console.log(JSON.stringify(getAgentFormSchema("poster-lab").properties, null, 2));'
```

This prints JSON Schema for `recipe.values`: each setting's type, `enum` options, `minimum`/`maximum`, `pattern` and `default`. Use only these keys and values. Numbers are JSON numbers, not strings. Colors are `#rgb` or `#rrggbb`.

### 3. Scaffold

```sh
npm run create -- sunrise-poster --template poster-lab
```

This writes `agents/sunrise-poster/agent.json` and a README, and refuses to overwrite an existing folder. The ID is a lowercase slug (`^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`, at most 64 characters) and must match the `id` in the file.

### 4. Edit the manifest

Change only `title` (1–80 characters), `description` (1–600), `recipe.values` and `recipe.brief` (at most 4,000 characters). Keep `version` as plain `x.y.z`. A finished recipe looks like this:

```json
{
  "schemaVersion": "1.0",
  "id": "sunrise-poster",
  "version": "1.0.0",
  "title": "Sunrise Poster",
  "description": "A tall cinema-style poster with a warm headline for a morning event.",
  "category": "video",
  "license": "MIT",
  "capabilities": {
    "network": "none",
    "execution": "declarative",
    "dataAccess": "selected-inputs"
  },
  "recipe": {
    "templateId": "poster-lab",
    "values": {
      "title": "Rise early",
      "ratio": "9:16",
      "treatment": "cinema",
      "color": "#ffd38a"
    },
    "brief": "Warm first light over a quiet city. Keep the headline short and leave room around it."
  }
}
```

The brief is creative direction in plain language: subject, mood, what to keep, what to avoid. Do not restate the settings in it.

### 5. Validate

```sh
node scripts/verify.mjs agents/sunrise-poster/agent.json
```

Success prints `Validated sunrise-poster (poster-lab).` On failure every line names the path and the fix, for example `recipe.values.treatment: choose editorial, cinema, minimal.` or `recipe.values.nope: this template has no such setting.` Fix exactly what is named and run it again. Do not loosen the manifest to make an error go away, and never report a recipe as done before this command passes.

### 6. Prepare the prompt (optional)

```sh
node --input-type=module -e 'import { readFile } from "node:fs/promises"; import { validateAgentManifest, compileAgentPrompt } from "./src/index.mjs"; const result = validateAgentManifest(JSON.parse(await readFile("agents/sunrise-poster/agent.json", "utf8"))); if (!result.success) throw new Error(result.errors.join("\n")); console.log(compileAgentPrompt(result.manifest));'
```

This prints the text a host would receive. It calls no model and makes no image or video.

### 7. Hand over

Tell the creator the file path, the template and its capability kind, which settings you changed from the defaults, and that validation passed. They can import `agent.json` into a host's saved recipes or share the file.

## Working in code instead of files

```js
import { createAgentManifest, validateAgentManifest } from '@optimai/creative-agents';

const recipe = createAgentManifest('poster-lab', { id: 'sunrise-poster', title: 'Sunrise Poster', brief: 'Warm first light over a quiet city.' });
recipe.recipe.values = { ratio: '9:16', treatment: 'cinema' };
const result = validateAgentManifest(recipe);
if (!result.success) throw new Error(result.errors.join('\n'));
```

`createAgentManifest` fills the category, license and capabilities for you. Every public module has a `.d.mts` declaration; `llms.txt` maps them and `llms-full.txt` inlines them. If you change SDK code or declarations rather than a recipe, run `npm test` and `npm run typecheck`.

## When the request does not fit

- **A setting the template lacks:** say so, and put the wish in the brief if it is creative direction. Do not add the key.
- **A template that does not exist:** offer the closest reviewed template from `npm run verify`.
- **Running the recipe:** canvas, vision, camera, 3D and music templates run in a browser (`examples/playground/`); writing templates need a local model (`npm run run -- --help`). Neither is part of building the recipe.
