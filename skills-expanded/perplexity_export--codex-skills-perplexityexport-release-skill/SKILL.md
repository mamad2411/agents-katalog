---
name: perplexityexport-release
description: Validate and release perplexity_export with reproducible artifacts, Python 3.12/3.13 coverage, pinned CI, and secret-free publication gates.
---

# Perplexityexport Release

Use this skill for CI/CD changes, release preparation, or compatibility claims
about `perplexity_export`.

## Release contract

- CI must run offline regression tests and a real `curl_cffi` import/client
  construction on Python 3.12 and 3.13, with the existing cross-platform
  coverage retained where practical.
- Workflows use full commit-SHA action pins, least-privilege permissions,
  bounded timeouts, cancellation for superseded runs, and no account cookies or
  live Perplexity requests.
- Source packages use the explicit allowlist in `scripts/build_release.py`.
  Build them twice to prove byte reproducibility, verify the SHA-256 manifest,
  reject symlinks, and inspect the exact archive member set.
- Tag-triggered publishing must depend on CI and security jobs and must not
  silently publish from an unverified or tampered artifact.

## Local gate

Use the direct Python executables when the Windows `py` launcher is unavailable:

```powershell
C:\py3dot12\python.exe -m unittest -v
C:\python3dot313\python.exe -m unittest -v
C:\py3dot12\python.exe -m compileall -q pplx_export.py live_verify.py scripts test_export.py test_ci.py test_resilience.py
C:\py3dot12\python.exe scripts/build_release.py
C:\py3dot12\python.exe scripts/verify_release.py dist/perplexity_export.zip dist/SHA256SUMS.txt
```

Install `requirements.txt` only into temporary per-interpreter environments
when validating the runtime dependency. Report unavailable network, package,
or interpreter evidence instead of calling it a code failure.

Do not create tags, merge branches, or push releases unless the user explicitly
authorizes that publication step.
