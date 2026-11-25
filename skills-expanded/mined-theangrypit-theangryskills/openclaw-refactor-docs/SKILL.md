---
name: openclaw-refactor-docs
description: "Use when refactoring an OpenClaw docs page while preserving source-backed behavior, moving detail and verifying links."
---

# Openclaw Refactor Docs

Codex adaptation of the pinned OpenClaw source. Repository-specific commands apply only to a verified OpenClaw checkout; portable debugger commands apply to their selected process.

## Preserve the contract before rewriting
Resolve the requested docs page and read its existing content and scoped instructions. Read the packaged upstream refactor workflow, plus `references/technical-documentation/SKILL.source.md` and the applicable framework references there. Those dependency files are reference material, not additional installable skills or delegation authority.

Classify the intended page as guide/topic/reference/troubleshooting. Inventory behavior-sensitive facts: commands/flags, defaults, precedence, state transitions, limits, auth/approval, compatibility, setup and errors. Give each fact a kept location, explicit moved destination or source-backed retirement reason before shortening.

Verify behavior against current schemas, CLI implementation/help, runtime/tests or exported APIs, not another summary. Keep common decisions and reliable verification in the main page; move exhaustive contracts and rare failure detail to linked references. Preserve the 80/20 path without losing relevant semantics.

Resolve repository docs navigation and existing generation ownership; update a generator rather than hand-editing generated truth. Use the actual repository's doc frontmatter and focused docs/link/format checks; pinned upstream doc-schema advice applies only where current source supports it.

Compare old/new fact coverage and follow links into moved details. Examples involving live data, credentials, installs or service changes need their real scope. Keep public-facing copy free of private operator details. Report kept/moved/retired facts, source verification, checks and unverified claims; editing docs does not authorize publishing them.

## Selective installation

No mandatory installed companion from this pack is required. Checkout/runtime prerequisites and the conditional source references still apply.

## Source procedures and boundary

Read [the packaged upstream entrypoint](references/upstream/SKILL.source.md) when using this workflow; its supporting files remain beside it. This root owns Codex invocation, target resolution and authorization. Upstream examples are reference procedures, not grants of access, installation, deployment, publication or another model/provider. Use native Codex tools where capable and preserve an actual refusal. The operator's chosen model, project instructions and source-trust policy remain authoritative.

For repository-owned dependencies and original relative links, use [the source link map](references/upstream-link-map.json) against the verified checkout or its pinned GitHub reference. The pack does not claim that a linked release/channel skill or runtime is installed. Inspect the current owning source before executing a version-sensitive example.

[Provenance and adaptation record](PROVENANCE.md) identifies the source commit, retained resources and changes.
