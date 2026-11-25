---
name: model-capability-proof
description: Proves model and provider capability claims before changing agent defaults. Use when swapping models, checking context windows, reasoning effort, tool use, streaming, media support, OAuth entitlement, fallback behaviour, or provider-specific runtime paths.
---

# Model Capability Proof

## Overview

Use this skill before trusting a model listing, launch post, provider doc, benchmark, or config file.

A model being listed is not the same as your agent being able to use it with your account, tools, context window, and runtime path.

## When to Use

- Changing an agent's default model or provider.
- Verifying a new model announcement.
- Checking context length or reasoning modes.
- Debugging fallback to the wrong provider.
- Testing whether tool calls, streaming, images, audio, or structured output work.
- Comparing builder and reviewer model stacks.

## Capability Dimensions

Check each separately:

1. **Model availability**: provider accepts the model ID.
2. **Account entitlement**: your account or subscription can run it.
3. **Context length**: runtime uses the claimed window, not registry folklore.
4. **Reasoning controls**: effort flags are accepted and included in request body.
5. **Tool use**: real client-side or server-side tools work.
6. **Streaming**: deltas arrive and UI/backend preserves them.
7. **Structured output**: schemas or JSON mode work if needed.
8. **Media**: image, audio, or video inputs/outputs work if claimed.
9. **Fallback behaviour**: no silent fallback to an old provider or smaller model.
10. **Gateway/API path**: the production agent path works, not just a direct SDK call.

## Proof Ladder

Run proofs in this order:

1. Read config and provider registry.
2. Dry-run request construction if the harness supports it.
3. Direct no-tools smoke.
4. Normal agent chat smoke.
5. Tool-capable smoke.
6. Gateway/API smoke.
7. Real task smoke in the intended lane.

Stop at the first failure and label exactly which capability failed.

## Report Format

```text
Model:
Provider:
Account/auth path:
Context configured:
Context runtime:
Reasoning configured:
Reasoning request proof:
No-tools smoke:
Tool smoke:
Streaming proof:
Fallback providers:
Gateway/API proof:
Verdict: usable / partially usable / not usable for this lane
```

## Common Failure Modes

- Docs list a model, but account entitlement blocks it.
- Direct API works, but agent tool schema fails.
- Chat completions works, but responses API is required.
- Reasoning effort is accepted by one model variant and rejected by another.
- Config says large context, compressor still uses a smaller auxiliary model.
- CLI smoke works, gateway still runs old config until restart.
- Fallback hides the failure by silently using another provider.

## Rule

Do not change a production builder or reviewer model until the exact intended path passes: same profile, same auth, same tools, same gateway or CLI surface.
