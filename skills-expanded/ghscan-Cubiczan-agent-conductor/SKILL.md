---
name: shared-ledger
description: Apply shared ledger helpers that live outside the billing module directory. Use when invoice math needs cross-module skills resolved from the extra source root.
version: 0.1.0
tools: [Read]
---

# Shared Ledger

This skill lives under `shared/`, not under `modules/billing`. A loader that
only walks the module directory will miss it. Declare `shared` as a workspace
root so discovery can resolve the extra sourceSet.
