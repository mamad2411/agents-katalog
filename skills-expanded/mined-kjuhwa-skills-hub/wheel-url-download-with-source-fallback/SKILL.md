---
name: wheel-url-download-with-source-fallback
description: Override `bdist_wheel` to first attempt downloading a pre-built wheel from a GitHub Release URL (composed from CUDA/torch/Python versions) and fall back to local source build only on HTTP failure.
category: build-system
version: 1.0.0
version_origin: extracted
tags: [wheel, bdist-wheel, github-releases, cuda, setup-py, prebuilt, fallback]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/deepseek-ai/DeepGEMM.git
source_ref: main
source_commit: 7f2a703ed51ac1f7af07f5e1453b2d3267d37d50
source_project: DeepGEMM
source_paths:
  - setup.py
imported_at: 2026-04-18T13:30:00Z
---

# Wheel URL Download Override With Source-Build Fallback

## When to use
Your Python package builds a CUDA extension that takes 10-30 minutes to compile from source. You publish pre-built wheels to GitHub Releases (or S3/CDN) for common CUDA × PyTorch × Python combos. You want `pip install <pkg>` to:
1. Attempt to pull the matching pre-built wheel — fast path.
2. Fall back to `python setup.py build` only when the pre-built is missing or the URL is unreachable.

The user doesn't pick; the setup machinery picks by matching the current environment.

## Steps
1. **Define the URL template** with placeholders for the matrix:
   ```python
   base_wheel_url = 'https://github.com/DeepSeek-AI/DeepGEMM/releases/download/{tag_name}/{wheel_name}'
   ```
2. **Compose the filename** from local versions — match on CUDA major, Torch major.minor, Python major.minor, cxx11abi, platform:
   ```python
   wheel_filename = f'deep_gemm-{ver}+cu{cu_major}-torch{torch_major}.{torch_minor}-cxx11abi{abi}-cp{py_major}{py_minor}-linux_{machine}.whl'
   ```
   The `{tag_name}` is `v{ver}` (your release tag convention).
3. **Subclass `_bdist_wheel`:**
   ```python
   from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

   class CachedWheelsCommand(_bdist_wheel):
       def run(self):
           if DG_FORCE_BUILD or DG_USE_LOCAL_VERSION:
               return super().run()   # always build locally when forced
           wheel_url, wheel_filename = get_wheel_url()
           try:
               with urllib.request.urlopen(wheel_url, timeout=1) as response:
                   with open(wheel_filename, 'wb') as out_file:
                       out_file.write(response.read())
               # place into the expected dist_dir/<properly-named>.whl location
               if not os.path.exists(self.dist_dir):
                   os.makedirs(self.dist_dir)
               impl_tag, abi_tag, plat_tag = self.get_tag()
               archive_basename = f'{self.wheel_dist_name}-{impl_tag}-{abi_tag}-{plat_tag}'
               wheel_path = os.path.join(self.dist_dir, archive_basename + '.whl')
               os.rename(wheel_filename, wheel_path)
           except (urllib.error.HTTPError, urllib.error.URLError):
               print('Precompiled wheel not found. Building from source...')
               super().run()  # fall back to source build
   ```
4. **Register via `cmdclass={'bdist_wheel': CachedWheelsCommand}`** so `pip install` (which calls `bdist_wheel`) goes through your override.
5. **Respect opt-outs:**
   - `DG_FORCE_BUILD=1` — skip the URL attempt entirely (CI matrix runs).
   - `DG_USE_LOCAL_VERSION=1` — the default for dev installs; the version string gets a `+<sha>` suffix that will never match a release filename, so skip the URL.
6. **Short timeout (1s).** On a bad network, waiting 30s to fall back frustrates users. Failing fast to source build is the right default.

## Evidence (from DeepGEMM)
- `setup.py:83-99`: `get_wheel_url` — composes the exact filename and release URL.
- `setup.py:168-192`: `CachedWheelsCommand` — try-URL-then-fallback flow.
- `setup.py:22-23`: the `DG_FORCE_BUILD` / `DG_USE_LOCAL_VERSION` env var opt-outs.

## Counter / Caveats
- **Filename collisions are silent.** If your release has `cu12` but you built for `cu13`, the URL 404s correctly. If instead a wheel was uploaded with a slightly different name (e.g. you renamed a tag), the fallback kicks in and users silently build from source — you won't notice unless you track usage.
- **GitHub rate-limits unauthenticated release-asset downloads.** Fine for a 1-connection-per-install pattern; not fine for high-concurrency CI. Mirror to a CDN.
- **`urllib.error.HTTPError` catches 404/5xx** but not `ConnectionResetError` from a partial download. Use a 2-try loop or download to a temp file + move-on-success.
- **The `dist_dir` rename dance is brittle.** If `bdist_wheel`'s tag format changes between wheel package versions, the filename you compute doesn't match the filename `_bdist_wheel` expects. Pin `wheel` version.
