---
name: r2-notebooklm-artifact-portal
description: Use when publishing, validating, or debugging public NotebookLM artifacts hosted on Cloudflare R2, including artifact inventories, public URLs, MIME types, cache headers, audio/video playback, and notebook visibility claims.
cluster: cloudflare
version: 1.0.0
---

# R2 NotebookLM Artifact Portal

## Purpose

Validate that NotebookLM artifacts are real, public, correctly typed, cacheable, and usable from an Astro/wiki/press-kit portal.

## Required Routing

- Use `notebooklm` before claiming a notebook exists, sources are attached, or artifacts were generated.
- Use `cloudflare`, `wrangler`, or `cloudflare-manager` for Cloudflare account/bucket operations.
- Use this skill for the portal contract: public URLs, MIME, cache headers, inventory, embed/playback, and reader-facing labels.

## Artifact Contract

Every portal artifact should have:

- Stable `id`
- Reader-facing `title`
- Public `href`
- `type` such as `report`, `infographic`, `deck`, `audio`, `video`, `table`, `flashcard`, `quiz`, or `mindMap`
- Expected extension and MIME
- Optional `thumbnail`
- Reader-facing description

## MIME Expectations

| Extension | Expected content type contains |
| --- | --- |
| `.mp3` | `audio/` |
| `.mp4` | `video/` |
| `.pdf` | `application/pdf` |
| `.png` | `image/png` |
| `.csv` | `text/csv` or `application/octet-stream` |
| `.json` | `application/json` or `application/octet-stream` |
| `.md` | `text/`, `markdown`, or `application/octet-stream` |

## Validation Workflow

1. Check live NotebookLM visibility with `notebooklm list --json` or explicit notebook ID.
2. Check local artifact inventory, usually `src/data/artifacts.json`.
3. HEAD every remote artifact URL.
4. Fail on 4xx/5xx, missing content type, incompatible MIME, or missing cache headers for large immutable assets.
5. Verify audio/video pages use playable embeds or clearly labeled direct links.
6. Verify public copy says `Source artifact`, `Open artifact`, or `Download`, not `Raw artifact path`.

## Reader-Facing Copy Rules

- Say `NotebookLM companion artifact`, not `raw output`.
- Say `R2-hosted source artifact`, not local file path.
- Do not expose bucket internals unless the URL itself is the public contract.
- Do not claim NotebookLM flow completion without live account verification or an explicit local-only caveat.
