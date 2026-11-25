---
name: voice-prompt-md5-two-tier-cache
description: Cache expensive voice-cloning prompts by content-hashing the reference audio plus text, with RAM + disk tiers.
category: architecture
version: 1.0.0
version_origin: extracted
tags: [caching, tts, voice-cloning, two-tier-cache, md5]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# Voice prompt MD5 two-tier cache

## When to use
Voice-cloning TTS builds a "voice prompt" (tokenized reference audio + embedding tensors) from a user's reference clip. The prompt is deterministic per `(audio_bytes, reference_text)` and takes hundreds of ms to rebuild. You want repeat generations to skip that cost entirely.

## Steps
1. Compute the key as `md5(audio_bytes || reference_text.encode("utf-8"))`. MD5 is fine here — you're not defending against a collision attacker, you're deduping content.
2. First tier: a process-local `dict[str, VoicePrompt]` keyed by the hex digest. O(1) on a hit and skips disk I/O entirely.
3. Second tier: `<data_dir>/cache/<key>.prompt` serialized via `torch.save`. `torch.save` handles both raw tensors and dict-of-tensors, so the same file format survives a schema change from tensor-only to dict-of-tensors.
4. On load, use `torch.load(path, weights_only=True)`. It's safer against malicious pickles if you ever need to import a cache file from elsewhere.
5. On a corrupted cache file (any exception during load), unlink it and fall through to recomputation. Never raise — the cache must be best-effort.
6. Write-through: on cache miss, compute, populate both tiers. Expose a cache-clear that wipes both tiers and any derived artefacts (e.g. combined audio WAVs) under the same directory.
7. Provide `clear_profile_cache(profile_id)` that removes only `combined_<profile_id>_*.wav` etc. — useful when a profile is edited without wiping the entire cache.

## Counter / Caveats
- Include the reference text in the hash. Two clones with the same audio but different reference transcripts produce different prompts and must not collide.
- Do not pickle the tensors with `pickle` directly — `torch.save` handles the device and dtype metadata across versions.
- Bound the RAM tier if you ever accept many distinct profiles per session; `dict` grows without limit. An `OrderedDict` + `move_to_end` LRU is a cheap upgrade.
- If users move the app's `data_dir` between platforms, treat the cache as ephemeral — `.prompt` files are torch-version sensitive and may not load on a newer torch build. Add a `CACHE_VERSION` prefix to the filename if you want eager invalidation.

Source references: `backend/utils/cache.py`.
