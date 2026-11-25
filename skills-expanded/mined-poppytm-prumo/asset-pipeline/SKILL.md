# Asset Pipeline & Cooking

## Purpose
Design and implement deterministic asset pipelines: source ingestion, import cooking (texture compression, mesh optimization, audio transcoding), content-hashed caching, hot reloading, async streaming, and budget enforcement so cooked builds are reproducible, within memory/GPU limits, and never hitch the frame loop.

## Use when
- Adding or changing asset loaders, importers, cookers, or the content-addressed artifact cache.
- Implementing hot reload, live-relink, or background async streaming of textures, meshes, or audio banks.
- Compressing or baking textures (mipmaps, BCn/ASTC/ETC2), optimizing meshes (vertex cache, overdraw), or transcoding audio.
- Auditing cook determinism, cache invalidation, or asset memory budgets.

## Do not use when
- Designing runtime renderer internals or shader compilation strategies without asset I/O (use `rendering-pipeline`).
- Tuning ECS tick scheduling or physics stepping (use `game-engine-architecture`, `game-runtime`).
- Authoring final art or audio content rather than the pipeline that processes it.

## Required context
- Asset inventory: textures, meshes, audio banks with source formats and size budgets.
- Target GPU/texture constraints: max texture size, supported formats (BCn, ASTC, ETC2), memory ceiling.
- Hot-reload and streaming latency budgets plus cooking determinism requirements.

## Procedure
1. **Inventory & Budget**: Catalog every asset class (texture, mesh, audio, level) with source format, cooked format, and per-class memory ceiling. Example: hero textures cook to ASTC 6x6 with full mipmap chains, capped at 256 MB total on tier-2 GPUs.
2. **Cook Deterministically**: Each cooker (texture baker, mesh optimizer, audio transcoder) must be a pure function of source bytes + cooker version + settings hash. Emit content-addressed outputs (`sha256(source‖settings‖cooker_version)`) so identical inputs always hit the artifact cache.
3. **Compress & Bake**: Generate mipmaps for all color textures (no single-level textures except UI atlases); compress with the platform-optimal block format; quantize/transcode audio to Opus/Vorbis at the budgeted bitrate. Reject assets exceeding budget at cook time, never at runtime.
4. **Hot Reload Safely**: Watch source files; on change, re-cook off the hot path, swap handles atomically (double-buffer resource tables), and release the old revision only after all in-flight frames retire. Never mutate a live GPU resource in place.
5. **Stream Asynchronously**: Split large assets into chunks with explicit LOD/mip tiers; stream on a background job with a fixed bandwidth budget (e.g., 8 MB/frame) and priority queue (visible-before-prefetch). Guarantee a valid low-LOD fallback is resident before the high-LOD request completes.
6. **Verify**: Run `scripts/verify.sh`. Prove cook determinism (two cooks, byte-identical hashes), hot-reload swap without tearing, and streaming under budget with zero frame hitches over a scripted camera flythrough.

## Decision rules
- **Cook-Time Rejection**: Over-budget or malformed assets fail the cook with an actionable message, never the runtime.
- **Immutable Cooked Artifacts**: Cooked outputs are never edited in place; a settings change produces a new content hash.
- **No Hot-Path I/O**: The frame thread never touches the filesystem or network; all loads go through the async streaming queue.
- **Fallback Always Resident**: Every streamed asset has a valid low-fidelity placeholder (1x1 mip, bounding-box mesh, silent clip) before high fidelity arrives.

## Evidence required
- Cook determinism log: identical content hashes across two clean cooks.
- Hot-reload swap test with frame-time trace showing no hitch above budget.
- Streaming benchmark: bandwidth usage vs budget over scripted flythrough.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Asset cooking pipeline with content-hashed, compressed outputs.
- Hot-reload and async-streaming implementation with benchmark evidence.
- Texture-budget compliance report with zero frame-hitch violations.

## Stop conditions
- Cooked assets deterministic and within budget; hot-reload verified without frame hitches.
- Streaming stays within bandwidth budget with valid fallbacks for all assets.
- Token budget exhausted.

## Escalation rules
- Escalate to lead architect if a target GPU cannot meet visual bar within its memory ceiling (requires art-direction tradeoff, not pipeline tuning).
- Escalate immediately if cooked artifacts are nondeterministic across machines (toolchain or dependency leak).
