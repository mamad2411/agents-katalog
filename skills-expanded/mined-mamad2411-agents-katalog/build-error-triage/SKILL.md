---
name: build-error-triage
description: Systematic triage workflow for build/compilation errors — classify by root cause (missing symbol, signature mismatch, instantiation failure), then isolate the first error before chasing cascades.
category: debug
tags: [build, compilation, java, javac, errors, triage]
triggers: [Unresolved compilation, Cannot instantiate, method is undefined, cannot find symbol, compilation error]
source_project: manual
version: 1.0.0
---

# Build Error Triage

See `content.md` for the full workflow. Trigger this skill whenever a build fails with one or more compilation errors and it's unclear which to fix first.
