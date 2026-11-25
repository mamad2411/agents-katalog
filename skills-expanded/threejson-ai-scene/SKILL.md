---
name: threejson-ai-scene
description: Generate or adjust ThreeJSON scenes and plan semantic texture needs through the explicit AI and texture entries.
---

# ThreeJSON AI Scene Skill

## Entry points

Import scene AI from `threejson/ai`, never from the engine root. Import the provider-neutral texture core from `threejson/texture`.

```js
import { createSceneAiClient, createSceneTexturePlanner } from "threejson/ai";
import { planSceneTextures, runSceneTexturePipeline } from "threejson/texture";
```

## Scene workflow

1. A new conversation's first user message is generation without a generate-vs-adjust model call.
2. In automatic mode, negotiation selects complete generation or incremental construction from actual scene/output complexity.
3. Render the first valid scene as soon as it is available.
4. Adjust existing scenes with commands first, JSON Patch second, and full JSON only as fallback.
5. Stop when the model returns `# done`, no concrete remaining work, or repeated/no-op output. Round limits are safety guards only.

Scene authoring must use standard ThreeJSON (`threeJsonId`, `sceneConfig`, heterogeneous `objectList`) and preserve unrelated fields during edits. Visible text requires `objType: "text"` and `content`; metadata names do not render glyphs.

## Texture workflow

1. Scan real material capabilities with `listMaterialTextureSlots`.
2. Call `planSceneTextures` once with `createSceneTexturePlanner`. The plan contains semantics only and must not contain URLs.
3. Let a host-injected `TextureAcquisitionProvider` search, generate, or persist candidates.
4. Reject unknown-license candidates from automatic application unless the user explicitly enabled that risk.
5. Use `applyTextureAssignmentAsync` so every map is preloaded before descriptor/runtime commit.
6. Keep a usable base material when any texture task fails.

Supported slots are base color, normal, roughness, metalness, AO, emissive, opacity, bump, and displacement. Ordinary image generation supplies base color only. Full PBR output requires explicit `pbr-set` or `pbr-derive` capability.

Poly Haven, Openverse, image generation, R2, proxying, and archival are service/host concerns. They must not be imported by `threejson`, `threejson/core`, or the pure texture module. A plain cube and an AI call without a texture Provider must issue no texture network requests.

The former texture Pointer, image Provider, and Sink APIs no longer exist and must not be recreated as wrappers.
