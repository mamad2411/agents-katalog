---
name: image-ad-clone-arcads-mcp
description: >-
  Reverse-engineer an existing image ad into a reusable prompt template and validate it through the optional Arcads MCP server. Picks gpt-image-2 or Nano Banana 2, optionally cross-validates against the other backend, and polls with arcads_watch_asset. Use only when the user explicitly requests Arcads MCP or has selected MCP transport and the tools are available in the current Cursor session. For normal image-ad cloning, use the REST/local image-ad-clone skill.
---

# image-ad-clone (Arcads MCP)

Reverse-engineer an **existing image ad** the user provides into a **reusable,
parameterizable template** (with `{placeholders}`), validated by generating it
through the Arcads **MCP server**, then save it to the shared prompt library.

**This is the MCP-native version** of `image-ad-clone`. The teardown/templating brain
is unchanged; only the validation round-trip swaps from REST to MCP — no `.env`, no
`generate_image.py`, no presigned-upload scripts.

| REST `image-ad-clone` step | MCP replacement |
|---|---|
| curl auth / `.env` + `generate_image.py` validation | `arcads_generate_image_gpt` **or** `arcads_generate_image_nano_banana` |
| (manual) describe the source ad | your own image vision (Read the file) **or** `arcads_analyze_media` (Gemini) |
| presigned upload + PUT for product refs | `arcads_get_upload_url` + PUT (explicit — see Uploading) |
| `GET /v1/assets/{id}` polling | `arcads_watch_asset` (status **and** URL in one call) |
| N parallel POSTs | `nbGenerations` (1–10) in a single call |

## Tools used (Arcads MCP)

| Tool | Role |
|---|---|
| `arcads_analyze_media` | (Optional) Gemini teardown of the source ad — layout, text, hierarchy, palette, style. Returns `data.generatedText`. |
| `arcads_generate_image_gpt` | Validate the template on **gpt-image-2** (typography / UI-mimicry ads). |
| `arcads_generate_image_nano_banana` | Validate the template on **nano-banana-2** (photoreal / lifestyle / multi-ref ads). |
| `arcads_get_upload_url` | Presigned S3 URL for the source ad (if analyzing via MCP) and any product reference. |
| `arcads_watch_asset` | Poll status **and** fetch the signed `downloadUrl`. Primary poll tool. |

## Read order

1. **This file** — the MCP workflow.
2. **[../../shared/skills/image-ad-prompting/prompting/template-format.md](../../shared/skills/image-ad-prompting/prompting/template-format.md)** — the entry skeleton new templates must follow.
3. **[../../shared/skills/image-ad-prompting/prompting/prompt-library.md](../../shared/skills/image-ad-prompting/prompting/prompt-library.md)** — where the finished template is saved; study neighbors for voice + Model-notes format.
4. **[../../shared/skills/image-ad-prompting/prompting/safety-suffixes.md](../../shared/skills/image-ad-prompting/prompting/safety-suffixes.md)** — guards baked into every template.

## Hard rules — never relax

1. **Input is an existing ad image.** If the user wants a fresh ad, redirect to `chatgpt-image-ad-arcads-mcp` / `nano-banana-image-ad-arcads-mcp`.
2. **Parameterize, don't memorize.** The output template must use `{brand}`, `{product}`, `{headline}`, `{palette}`, etc. — reusable across brands/products. Never hard-code the source brand.
3. **Validate before saving.** Always generate at least one round-trip through the MCP and visually QA it against the source before adding to the library.
4. **Pick the backend at Phase 1** based on the ad's nature (typography/UI → gpt-image-2; photoreal/lifestyle/multi-ref → nano-banana-2). Optionally cross-validate against the other at Phase 8.
5. **Aspect ratios on this backend:** `1:1`, `16:9`, `9:16` only. If the source is `4:5`/`2:3`, validate at the nearest ratio and note the crop in the template.
6. **Credit cost is an estimate** — present before each validation round; wait for confirmation. (Daily-limit workspaces show `creditsCharged: 0`.)

## Uploading reference files (remote agent clients)

> ⚠️ Local paths fail when the MCP server cannot access the client's filesystem,
> including Cursor's remote MCP transport: `File not found … Use arcads_get_upload_url`.
> Needed when (a) analyzing the source ad via `arcads_analyze_media`, or (b) the
> template uses a real product image as a reference during validation.

1. `arcads_get_upload_url(mimeType)` → `{presignedUrl, filePath}`.
2. `curl -s -o /dev/null -w "%{http_code}\n" -X PUT -H "Content-Type: image/png" --upload-file "<local>" "<presignedUrl>"` → expect `200`.
3. Use the returned **`filePath`** in `referenceImages` (or `arcads_analyze_media`'s `referenceImages`).

**Gotcha:** temp `filePath`s are **single-use** — upload a fresh copy before each tool call that consumes it (e.g. analyze, then re-upload for the validation generate).

## Polling & fetching the result

**Poll with `arcads_watch_asset(assetId)`** — returns `status` and, once generated, the `downloadUrl`. While `pending` no `downloadUrl` (re-call every ~15–20s). `arcads_analyze_media` returns its result in `data.generatedText` (poll until `generated`, then read that field — no `watch_asset` needed for the text).

> ⚠️ `arcads_get_asset` can return `-32602 (tool not found)` on the current build — use `arcads_watch_asset`.

## Workflow

### Phase 1 — Receive ad + pick backend
Take the source ad image. Classify it: **typography / UI-mimicry / dense text** → validate on **gpt-image-2**; **photoreal / lifestyle / multi-reference / product-in-scene** → validate on **nano-banana-2**. State your pick and why; ask if the user wants the other backend cross-validated at Phase 8.

### Phase 2 — Teardown
Describe the source precisely. Use your own image vision (Read the file) for a static ad; for a richer structured teardown, optionally upload it and call `arcads_analyze_media` ("Describe this ad's layout, every text element verbatim, visual hierarchy, color palette with hex guesses, typography, photographic vs graphic style, and the 3 traits that make it recognizable"). Capture: layout grid, each text block, hierarchy, palette, type treatment, imagery style, defining traits.

### Phase 3 — Parameterize
Convert the teardown into a template with `{placeholders}` for everything brand/product-specific (brand name, product, headline, subhead, palette, imagery subject). Keep structural/compositional language fixed. Append the standard safety guards (no-chrome, edge-safe, glyph-safety).

### Phase 4 — Fill with a test brand
Pick a plausible *different* test brand/product (not the source's) to prove reusability. Fill the placeholders.

### Phase 5 — Credit estimate (MANDATORY)
Present `~credits × variants` for the validation round; wait for confirmation.

### Phase 6 — Upload refs (if the template uses a product image)
Per **Uploading reference files** — fresh upload.

### Phase 7 — Validate (round-trip)
Generate with the Phase-1 backend:
```
# typography / UI ad:
arcads_generate_image_gpt(prompt="<filled template>", model="gpt-image-2", aspectRatio="<r>", nbGenerations=2)
# photoreal / lifestyle ad:
arcads_generate_image_nano_banana(prompt="<filled template>", model="nano-banana-2", aspectRatio="<r>", referenceImages=[...], nbGenerations=2)
```
Poll with `arcads_watch_asset`; download; **Read the output** and compare to the source: does it reproduce the layout, hierarchy, and feel? Is the text legible (gpt-image-2) / are hands/materials clean (nano-banana)? If it drifts, refine the template wording and re-validate (cap 2 refine loops). Log each call.

### Phase 8 — (Optional) cross-validate
If requested, fire the same filled template through the *other* backend and note in the template's Model-notes which backend renders it best and any caveats.

### Phase 9 — Save to the library
Append the finished template to `prompt-library.md` using `template-format.md`'s skeleton: title, the parameterized prompt, `{placeholder}` list, Model notes (gpt-image-2 vs nano-banana verdict + aspect-ratio note), and a one-line "best for." Show the user the new entry and the validation image(s).

## Constraints quick reference

| Constraint | Impact |
|---|---|
| Aspect ratios | `1:1`, `16:9`, `9:16` only — note native-ratio crops in the template. |
| gpt-image-2 refs | Max 5. nano-banana refs: max 14. S3 `filePath`s, single-use. |
| `nbGenerations` | 1–10 in one call — use 2–3 to judge template stability. |
| Validation | Always at least one round-trip + visual QA before saving. |

## Error recovery

| Symptom | Fix |
|---|---|
| Template renders inconsistently across `nbGenerations` | Tighten compositional language; add explicit placement/anchoring; pick the more stable backend. |
| `File not found` / `REFERENCE_FILE_NOT_FOUND` | Upload first / re-upload fresh before the call. |
| `-32602 arcads_get_asset not found` | Poll with `arcads_watch_asset`. |
| Text garbled on a typography template | Move it to gpt-image-2; enlarge text; note "gpt-image-2 only" in Model notes. |

## Out of scope
- **Fresh ad generation** → `chatgpt-image-ad-arcads-mcp` / `nano-banana-image-ad-arcads-mcp`.
- **Cloning a video ad** → `clone-video-ad-seedance-arcads-mcp`.
- **Meta upload** → `meta-ad-builder`.

## See also
- [image-ad-clone](../image-ad-clone/SKILL.md) — the REST/script version.
- [chatgpt-image-ad-arcads-mcp](../chatgpt-image-ad-arcads-mcp/SKILL.md) / [nano-banana-image-ad-arcads-mcp](../nano-banana-image-ad-arcads-mcp/SKILL.md) — fresh generation from the resulting templates.
- [arcads-mcp](../arcads-mcp/SKILL.md) — broad Arcads-MCP generation conventions.
