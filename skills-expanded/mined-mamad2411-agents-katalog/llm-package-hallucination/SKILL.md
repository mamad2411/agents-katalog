---
name: llm-package-hallucination
description: Verify every LLM-suggested dependency exists in the registry before installing — hallucinated package names are a real supply-chain attack surface (slopsquatting).
---

# LLM package hallucination (slopsquatting)

LLMs routinely invent dependencies that do not exist. In a large study of generated code, roughly **5.2% of packages suggested by commercial models** and **~21.7% from open models** referenced non-existent packages. Worse, the hallucinations are **reproducible** — the same fake names recur across runs — which turns them into an attack: an adversary registers a frequently-hallucinated name (**"slopsquatting"**) and waits for someone to `install` it on a model's say-so.

## Rules

- **Never install a dependency just because the model suggested it.** Verify the package exists in the real registry (npm, PyPI, etc.) and is the intended, reputable one before adding it.
- Treat an unfamiliar package name in generated code as **unverified until checked** — confirm the name, owner, download history, and repository, not just that `install` succeeds (a slopsquatted package will also install cleanly).
- Be most suspicious of plausible-but-slightly-off names (`requests-oauth` vs `requests-oauthlib`) and of packages that appear in generated code but not in the project's existing manifest.
- Pin and lock verified dependencies, and scrutinize lockfile additions during code review — a new dependency in generated code is exactly the moment to run the existence check.

## Mitigations that work

- Ground suggestions in a **trusted package index** (RAG over a known-good allowlist/registry snapshot) rather than the model's parametric memory.
- Ask the model to **self-verify** — when prompted to check, models flag their own hallucinated packages over **75%** of the time; self-refinement and retrieval substantially cut the rate.

## Examples

```sh
# BAD — install a model-suggested package without verification
npm install requests-oauth   # model suggested it; package does not exist on npm
# a slopsquatted "requests-oauth" could install and run malicious code silently

# GOOD — verify before installing
# 1. Check the registry: https://www.npmjs.com/package/requests-oauth → "Not found"
# 2. Model likely meant: npm install requests-oauthlib (Python) or passport-oauth (Node)
# 3. Confirm name, owner, download count, and repo before adding to package.json
npm install passport-oauth   # verified: 350k weekly downloads, maintained, correct repo
```

## Source

Spracklen et al., "We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs," *USENIX Security* 2025 — <https://arxiv.org/abs/2406.10279>. The ~5.2% / ~21.7% rates, the reproducibility that enables slopsquatting, and the >75% self-detection / mitigation results are from the paper.
