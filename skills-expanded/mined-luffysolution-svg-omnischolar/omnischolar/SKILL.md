---
name: omnischolar
description: Orchestrate multi-step scholarly work with OmniScholar across literature discovery, read-only Zotero, PDF parsing, citations, materials and chemical data, scientific images, and local publication. Use when a request spans several research workflows or the correct specialist workflow is unclear.
license: MIT
---

# OmniScholar

Choose the smallest workflow that answers the request. Follow the user's language; keep tool names and configuration identifiers in their exact English form.

## Route the request

- Literature, patents, authors, citation graphs, recommendations, journals, snippets, or datasets: follow `scholar-search`.
- Local collections, metadata, notes, annotations, attachments, or PDF selection: follow `zotero-research`.
- Selecting a local PDF or preparing MinerU Markdown and assets: follow `paper-reading`.
- Complete or focused interpretation, evidence location, and figure/table/equation reading inside a parsed paper: follow `literature-reading`.
- Citation evidence, candidates, formatting, or insertion: follow `academic-citation`.
- Generated or edited illustrations: follow `scientific-figure`.
- Materials Project records and exports: follow `materials-project`.
- CAS substance records and contract status: follow `chemical-data`.

For an unfamiliar environment, call `omnischolar_status`, `omnischolar_capabilities`, and the relevant source-status tool before selecting a provider. For image work, call `omnischolar_image_models` with discovery enabled first: show usable models and their declared capabilities, ask the user to choose when multiple valid models materially differ, and otherwise select the newest usable model appropriate to the requested task. If no provider supports the requested capability, report the missing configuration or capability and offer an available non-equivalent workflow only with a clear label.

The generated configuration enables provider sections by default. Use providers with configured credentials and report `credential_required` when a selected provider is not configured.

## Safe multi-stage sequence

1. Search only when discovery is needed; preserve provider provenance and identifiers.
2. Match a local Zotero record by DOI, then normalized title/year/author. Never guess between ambiguous candidates.
3. Read the aggregate Zotero item and identify the intended attachment. If multiple PDFs are available, show the choices and ask the user to confirm one `attachmentKey` before parsing or synchronizing it.
4. Reuse an existing readable publication. When parsing is necessary and upload is authorized, call `omnischolar_parse` directly; it performs the MinerU cache/upload step before publication checks. Use `omnischolar_sync action=plan` for explicit synchronization decisions, not as a mandatory parse preflight.
5. Read the published Markdown and sibling assets progressively with the host's local file and image capabilities, then verify claims against the source.
6. Format citations only after identity and relevance checks.
7. Let `literature-reading` own interpretation, evidence location, and any optional Markdown output.
8. Route image work by declared capability, then inspect the result for scientific errors.

For Semantic Scholar, keep paper and author operations separate: use `literature_search`/`literature_get` for papers, `literature_graph` for recommendations and citation relations, and `literature_author` for author search, author detail, or an author's papers. Respect provider throttling and `Retry-After`; do not treat a transient 429 or 5xx as evidence that the API is unsupported.

For image calls, read each selected model's `supported_parameters` from `omnischolar_image_models` before calling `omnischolar_image_generate` or `omnischolar_image_edit`. Provider parameter support is not interchangeable: OpenAI GPT Image uses `size`, Google Gemini uses `aspectRatio`/`resolution`/`outputFormat`, Vertex Gemini uses `aspectRatio`/`resolution`/`outputFormat`/`n`, Fal varies by model, and native DashScope/Qwen uses `size`/`n`/`negativePrompt`/`seed` without background or quality controls. Qwen AI Platform uses the public DashScope endpoint and does not require a workspace; Bailian workspace endpoints are a separate regional configuration.

For custom providers, model discovery first uses `options.modelCatalogEndpoint` when configured and otherwise tries the OpenAI-compatible `baseUrl/models` endpoint. Treat catalog entries without explicit capability metadata as `model_capabilities_unpinned`; use the configured `models` contract to authorize image operations when the downstream provider has no usable catalog.

Multiple custom profiles are supported with distinct provider names and `providerType: "custom"`. Keep each profile's API key in its own environment variable. Declare per-model capabilities and `supportedParameters`; common OpenAI-compatible image routes are `images/generations` and `images/edits`, but endpoint names remain configurable.

Fal generation defaults to `options.sync_mode=true` to avoid downloading result CDN URLs; set it to `false` only for an endpoint that requires hosted output URLs.

## Boundaries

- Zotero is GET-only and local-only. Never expose port 23119 or request a write operation.
- Ai4Scholar is an explicitly selected paid source, not a silent literature fallback.
- MinerU uploads the selected PDF. A sync recovery action must not trigger a remote upload; repair or reparse may upload only when cache is insufficient and the user explicitly authorizes it.
- Preserve local modifications. On sync `conflict`, use the configured conflict candidate and ask the user how to reconcile it. Never overwrite an interpretation sidecar without confirmation.
- Never expose credentials, Authorization headers, signed URLs, or local private paths in answers.
- Do not blindly retry authentication failures, rate limits, ambiguous paid submissions, unsafe archives, or terminal jobs.
- AI-generated scientific images are illustrative drafts, never experimental results or measured data.

## Output

Write only beneath the configured output root. The default managed layout is:

```text
<output-root>/Literatures/<paper>/
├── <paper>.md
├── metadata.json
├── assets/
└── source/
    ├── paper.pdf
    └── zotero-reading-record.md
```

Use the bibliographic frontmatter in the MinerU Markdown and Zotero reading record for Obsidian properties and identity checks. Parsed image filenames begin with the Zotero key. Preserve full provenance in `metadata.json`, respect the user's citation style and language, and keep missing or uncertain values explicit.
