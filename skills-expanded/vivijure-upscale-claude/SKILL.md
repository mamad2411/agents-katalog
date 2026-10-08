# CLAUDE.md

Guidance for Claude Code (and the crew) working in this repo.

> Default branch is **`main`**. Commit via PR (branch-protected, no direct pushes); CI must pass.

## What this is

**The GPU backend for Vivijure's `upscale` finish module (#191).** A single RunPod serverless image
that upscales video with **Real-ESRGAN** run on PyTorch/CUDA via
[spandrel](https://github.com/chaiNNer-org/spandrel): stream frames through ffmpeg pipes -> upscale in
BATCHES on the GPU (fp16) -> re-encode (NVENC), audio copied through when present. No per-frame PNG disk
roundtrip; the GPU is the bottleneck, not I/O. Finish-class: it raises the assembled film's resolution,
and is the natural partner that returns a MuseTalk-synced shot to delivery res.

This repo is the image + the RunPod handler; the studio-side `upscale` module worker (thin module on
`vivijure-cf` / `vivijure-local`, types from `vivijure-core`) is what calls this endpoint. Image:
`ghcr.io/skyphusion-labs/vivijure-upscale`. Pin by versioned tag from git tags / GHCR (latest `v*`);
do not freeze a single version here as current forever.

## The Vivijure constellation

```
   vivijure-cf / vivijure-local  (panels; core: vivijure-core)
            |
            v
   vivijure-backend + finish satellites
            |
     musetalk | upscale (THIS) | audio-upscale | wan-train | local-12/16gb
```

## Handler contract (the job, `handler.py`)

One typed in / one typed out, three dispatch modes (`handler(job)` branches on the input keys):

- **R2 finish-chain mode** (the endpoint reads/writes the shared bucket itself, no creds on the wire):
  `{ clip_key, output_key?, target_height?, scale?, model? }`. Returns the new key as `clip_key` so the
  finish chain carries the upscaled clip downstream, with `applied:["upscale:<n>x"]` or
  `applied:["upscale:<h>h"]` when a height was requested. Also reports `out_w` / `out_h`.
- **Presigned mode** (credentialless: the caller presigns R2): `{ video_url, output_url, output_key, target_height?, scale?, model? }`.
- **Selftest:** `{ "selftest": true, "scale"? }` generates a real 720p24x3s clip, upscales it end to
  end, and PROVES the result is GPU-bound: it reports the actual `encoder` + `nvenc_used`, the per-phase
  wall-clock split (`phase_s`), sampled GPU/encoder util (`gpu_sample`), `peak_vram_mib`, and
  `batch`/`fp16`. Doubles as the endpoint health check.

`target_height` is the studio contract (exact output height; 4x inference then GPU interpolate).
`scale` is `2` or `4` only (the models are 4x native; a 2x is the 4x inference GPU-downscaled /2, no
CPU Lanczos). A value that is not 2 or 4 is refused, never collapsed. An unsatisfiable height
(beyond 4x, a downscale, a no-op, a long-edge cap that would change the request) is `ok: false`.
`model` is `realesr-animevideov3` (anime/fast, default) or `RealESRGAN_x4plus` (general).
**A non-ok result is a soft-degrade signal** the module honors by passing the original clip through,
never a drop.

## GPU-bound by design (do not regress)

The whole pipeline keeps the GPU fed and the CPU out of the hot path; these are load-bearing:
- **No disk roundtrip; batched fp16.** Frames stream via ffmpeg `rawvideo` pipes; Real-ESRGAN runs on
  BATCHES (`UPSCALE_BATCH`, default 16) in fp16 autocast (weights stay fp32, no `model.half()`). The
  warm-worker model cache is `_MODELS`.
- **GPU rescale + NVENC encode.** Final-size resize is a GPU `interpolate`; the re-encode uses
  `h264_nvenc` when usable. NVENC is probed once per worker (listed AND a real test encode succeeds);
  if not usable it falls back to bounded `libx264` and **reports which encoder ran** (`encoder`), so a
  CPU fallback is never silent.
- **Output cap + wall-clock guards.** Output long edge capped (`MAX_OUTPUT_LONG_EDGE`, default 3840 =
  4K UHD); every ffmpeg phase has a hard `FFMPEG_TIMEOUT` (default 1200s) so a pathological clip
  degrades instead of hanging to the RunPod execution-timeout.

History: `:0.2.5` moved the encode off CPU `libx264` onto `h264_nvenc`; `:0.2.6` made the upscale loop
GPU-bound by removing the per-frame PNG roundtrip and batching in fp16 (issue #7).

## Commands

This is a Python / RunPod image, NOT an npm package. There is no local test suite; verification is the
build-time NVENC assert plus the GPU-gated selftest.

```bash
# Build the image locally (CI does this on push). The build FAILS if h264_nvenc is not compiled into ffmpeg.
docker build -t vivijure-upscale:dev .

# Lint the handler without a GPU.
python -m py_compile handler.py

# GPU verify: send {"selftest": true} on a pinned endpoint / live pod; assert ok:true AND nvenc_used:true.
```

**Tunables (endpoint env):** `MAX_OUTPUT_LONG_EDGE`, `FFMPEG_TIMEOUT`, `UPSCALE_BATCH`, `UPSCALE_TILE`,
`UPSCALE_FP16`, plus the R2 creds (`R2_ENDPOINT_URL` / `R2_BUCKET` / `R2_ACCESS_KEY_ID` /
`R2_SECRET_ACCESS_KEY`). Size `UPSCALE_BATCH` to the card's VRAM (B16 ~8.7 GiB at 720p, ~17 GiB at
1080p). See the README "Tunables" table.

**Release / deploy mechanics.** `.github/workflows/build-image.yml` builds + pushes to GHCR on a push to
`main` (touching the build inputs) as `:latest` + `:<sha>`; a pushed SemVer tag (`vMAJOR.MINOR.PATCH`)
ALSO publishes the matching bare `:MAJOR.MINOR.PATCH` (pin prod to that immutable tag, not `:latest`
alone). PUBLIC repo; CI on GitHub-hosted `ubuntu-latest`. Operator sets endpoint image tag, GPU type,
and R2 env (**never freeze endpoint IDs here**). Registry-auth is MCP/API-manageable
(`containerRegistryAuthId` on template).

## RunPod GPU config

GPU-bound module, so the endpoint should pin a card with hardware NVENC and enough VRAM for the batch,
NOT the cheapest card (GPU-rationing thesis: a faster card finishes in fewer billed seconds). Recommended:
an Ada / Blackwell-Pro card with NVENC (L4 / L40S sm_89, or RTX PRO 6000 sm_120). Avoid cards without
usable NVENC. **No `TORCH_CUDA_ARCH_LIST` to maintain here** (unlike the sibling musetalk image): nothing
compiles from source, torch kernels come from the `runpod/pytorch` cu1281 base, so the image is
GPU-agnostic. GPU type is set on the endpoint, not in this repo.

## Homelab serve overlay (the resident LOCAL_FINISH door)

`Dockerfile.serve` + `serve.py` + `runpod_http_serve.py` layer a RunPod-compatible `/run` +
`/status` HTTP server on the SAME base image the serverless worker ships, so the door runs resident
on our own GPU boxes instead of paying a serverless cold start per job.

- **Published, not hand-built.** `build-image.yml` publishes `<version>-serve`,
  `<major>.<minor>-serve` and `sha-<short>-serve` alongside every release tag, from the same job,
  with the base pinned to the release image that job just built. Evidence about a door has to be
  evidence about a SHA; a locally-built tag cannot be re-pulled, re-verified or rolled back by
  anyone else (#89 item 1). Before that bake existed, both live video doors ran hand-built local
  tags.
- **`UPSCALE_IMAGE` has no default** and a hand build must pass it. The old literal default drifted
  two releases behind the current version, and its failure mode is a door that WORKS on a stale
  base (#89 item 2). Docker refuses an empty `FROM` at parse time, before any pull. The resulting
  `InvalidDefaultArgInFrom` warning is the intended shape, not a defect to "fix" back.
- **Port 8012** by default (`PORT`); the speech door (`vivijure-audio-upscale`) is 8013, so both
  can be resident on one card without a collision. Bind the published port to the VLAN address,
  never `0.0.0.0`.
- **`/health` is auth-free liveness only** and never touches the GPU, the model or the handler.
  The deploy check that CAN fail is `POST /run {"selftest": true}`, which this overlay FORWARDS to
  the handler (#88 -- it used to intercept it, which made the documented check structurally
  incapable of failing). Use `/health` as the control that the door is reachable and the selftest
  as the measurement.
- **A default selftest also runs an R2 leg.** `_selftest` invokes `_selftest_r2` opportunistically
  and skips it only when credentials are ABSENT, which on a door they are not. For a GPU check with
  **zero bucket traffic**, pass an explicit model and no `r2` flag:
  `{"selftest": true, "model": "realesr-animevideov3"}` -- with a `model` and without `r2`, the R2
  leg is never called at all. Covered by a test asserting on a call recorder, so it stays true.

**VRAM behaviour, measured on an RTX 4000 SFF Ada (20475 MiB) 2026-08-07.** Unlike the speech door,
**this one gives its memory back**: `handler.py` calls `torch.cuda.empty_cache()` after upscale so
the NVENC encoder (a separate CUDA context that cannot use torch's reserved pool) has room to
initialise. Measured across a real job at 0.5s sampling: **192 MiB resident before, 6392 MiB at
peak, 192 MiB after.** The peak is transient working memory proportional to frame size and batch,
so it is a property of the JOB and not of the door -- do not quote it as a resident footprint. On a
card shared with a resident speech door the concurrent peak was **18797 of 20475 MiB**, which is
the number to check before co-tenanting anything else on that card.

## Verifying changes

After any handler or Dockerfile change: build clean (the NVENC assert is a build-time fail-fast), then
run the **pre-prod GPU gate** below and confirm `ok:true`, `nvenc_used:true`, and a GPU-bound
`gpu_sample` before cutting a release tag / repinning prod. Verify the **artifact**, not only the
pipeline. fp16 is effectively lossless here (PSNR ~66 dB vs fp32).

## Pre-prod GPU test spend (Conrad, 2026-08-06) -- do not thrift here

**Never hold back RunPod spend when proving an image before it is production-pinned.** A green bake is
not a proven upscale. Pre-prod verification is **expected spend**, not an escalation. Community pods
are not the gate. (This is the **video upscale** satellite image repo `vivijure-upscale`.)

Pick **one** of these for the gate (either is fine; pick what fits the change):

| Path | How | When |
| --- | --- | --- |
| **SecurePod** | Spin a SecurePod (or equivalent dedicated pod) on the candidate image; run `{"selftest": true}` (and a real short job if needed); verify the **artifact** (`ok:true`, `nvenc_used:true`, GPU-bound `gpu_sample`). | Prefer for isolated image proof without touching prod traffic. |
| **Serverless endpoint** | Deploy/pin the candidate image on the upscale serverless endpoint, set **active workers (min idle / `workersMin`) to 1** so cold-start does not fake a hang or a false timeout, run the same selftest / short job, verify the artifact. | Prefer when the proof needs the real endpoint shape (env, network, R2). |

### HARD: restore workers after serverless test

If you raised the serverless endpoint's active / min workers **above 0** for testing, **bring it
back to 0 when the test is done** (same session, before you walk away). Leaving `workersMin` /
active workers at 1+ burns idle GPU money with no proof benefit. Max workers can stay at the
prod pin; the restore rule is about the **floor that keeps a warm worker** (min/active = 0 in
steady state unless Conrad ruled otherwise for prod capacity).

Do **not** skip the restore because "we might test again tomorrow." Re-raise to 1 at the next
test if needed. Document the before/after values in the PR or runlog when you change them.

Never trust: CI green alone or bake green alone.

## Source provenance

`handler.py` + `requirements.txt` were RECOVERED verbatim from the published image
`ghcr.io/skyphusion-labs/vivijure-upscale:0.2.2` (the original pod was terminated, never committed); the
Dockerfile is reconstructed from `docker history` (functionally faithful, not byte-identical). The
GPU-bound encode pipeline (NVENC, res cap, GPU rescale, wall-clock guards) was added on top in `:0.2.3`.
Treat the image-extracted files as the source of truth they reconstruct.

## Conventions

- **No em-dashes (U+2014) or en-dashes (U+2013) anywhere.** Use commas, semicolons, parentheses, or `--`.
- Handle / username is `skyphusion` across all services.
- **A CPU fallback is never silent** (report `encoder`); **a degrade is never silent** (the #245 / #249
  discipline): a non-ok result is the module's passthrough signal, never a drop, and never a fake tag.
- Minimal deps; the engine choice (CUDA Real-ESRGAN via spandrel, NOT video2x/Vulkan -- RunPod has no
  working Vulkan stack, proven 2026-06-20) is deliberate. Justify any new dependency.
- Real-ESRGAN (BSD-3-Clause) + spandrel (MIT) + FFmpeg are listed in `THIRD_PARTY_NOTICES.md`; keep it
  current.

## Crew + identity

- The FIRST command in any op is the member's own login shell: `sudo -u <member> bash -lc '<ops>'`
  (loads their `$HOME`, their `~/dev/vivijure-upscale` clone, their gh / RunPod / R2 creds). Commits and
  PRs land under the member's `skyphusion-<member>` identity, never Conrad's.
- **Pre-prod GPU proof spend is authorized** (SecurePod or serverless workersMin=1). Do not thrift
  out of the proof. **Serverless min/active workers back to 0 when the test ends.**
- Operating memory for the vivijure family lives in the per-project memory under
  `~/.claude/projects/-home-conrad-dev-vivijure/memory/` (`seg-vivijure-modules`); load it before acting.
- **HARD AUP line:** the CSAM bright line is absolute. Non-negotiable.
- **Ignore Cursor `AGENTS.md`.** No endpoint-ID freezes.

## Commits & versioning

Conventional Commits (`feat(scope):`, `fix(scope):`, `docs:`); body explains the why. SemVer-style
`0.MINOR.PATCH` while pre-1.0 (PATCH for fixes / backend tweaks, MINOR for features). A release is a
pushed `vMAJOR.MINOR.PATCH` git tag on `main` (CI publishes the matching immutable image tag).

## Release / deploy

**Tag-gated production deploy.** Merges to `main` run CI only; they do not ship production.
Cut an annotated SemVer tag on `main` to release (`git tag -a vX.Y.Z -m "..." && git push origin vX.Y.Z`).
Deploy workflows assert the tag commit is an ancestor of `origin/main`.
