---
name: replicate-model-selection
description: Find the right model on Replicate, catalog navigation, official models, current popular image, video, and language models, and how to compare cost and quality. Use when the user asks which model to run.
---

# Choosing models on Replicate

The catalog is thousands of models and moves fast: search live (the MCP
server has search tools; the site has https://replicate.com/explore and
curated collections at https://replicate.com/collections) rather than
trusting a memorized list.

## Prefer official models

Replicate maintains 100+ official models (collection:
https://replicate.com/collections/official). They need no version pinning,
run via `/v1/models/{owner}/{name}/predictions`, stay warm, and bill
predictably per output. Default to an official model when one covers the
task.

## Current landmarks (verify before quoting; the catalog rotates)

- Images: the FLUX family from black-forest-labs
  (`black-forest-labs/flux-1.1-pro` for quality, schnell variants for
  speed) and ByteDance Seedream for high-fidelity text-to-image.
- Video: Google Veo and Wan are among the official video options; several
  Kling and Hailuo variants also run on the platform.
- Language and audio: open-weight LLMs (Llama and DeepSeek families) and
  speech models are available; for LLM work compare token pricing against
  dedicated providers first.

## Selection checklist

1. **Task fit**: read the model page README and example gallery; the
   gallery is real output, not marketing.
2. **Input schema**: check the API tab for supported parameters (aspect
   ratio, duration, reference images). A model without the control you need
   is the wrong model regardless of quality.
3. **Cost**: model page shows pricing, per output for official models, per
   hardware-second for community ones. Video is orders of magnitude more
   expensive than images; quote cost before batch runs.
4. **Popularity and freshness**: run count and last-updated date are decent
   proxies for reliability; a community model with few runs will cold-start
   slowly and may be unmaintained.
5. **License**: open models carry their own licenses (some are
   non-commercial); check the model page before shipping outputs in a
   product.

## Comparison workflow

For "which model should I use" questions, do a bakeoff: pick 2 or 3
candidates, run the same prompt/input through each (cheap sizes first),
and show the user outputs with per-run cost. The MCP server can search,
inspect schemas, and run candidates in one session.

## When nothing fits

If no hosted model matches (custom weights, fine-tunes, private models),
package and push your own with Cog, then optionally put a deployment in
front of it: see the `replicate-deploy` skill.
