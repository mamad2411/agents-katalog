# Capture Module

Owns cross-store capture target selection and its operator/agent surfaces.
The selected store remains the write owner.

## Ownership

- `commands.ts` owns chat empty-input handling, request construction and plain-text
  replies. Channels supply the selected scope client, parsed input and target.

- `CaptureProviderImpl` owns classification and explicit-target selection.
- `store-writer.ts` is the only cross-store persistence transform. It maps the
  selected target to `MemoryProvider.save`, `KnowledgeProvider.create`, or the
  repo-tasks mutation boundary and returns those domain outcomes directly.
- Memory owns versioned decoding and publishes an in-memory mutation only after
  its atomic JSON replacement succeeds. Knowledge owns atomic markdown
  replacement; interrupted temporary files are outside its `.md` record set,
  so restart observes the prior or replacement record. Both stores own record
  identity and provenance metadata. Repo-tasks owns task/inbox validation, safe
  paths, mutation authorization, logical resources, durable outcomes, and recovery.
- Routes own untrusted JSON decoding and scope selection. The generated routine
  transport owns daemon request/response decoding for clients.
- The CLI, tool, channels, and shared UI own only confirmation or rendering.

## Contract

- Explicit targets bypass classification and retain the complete capture text.
  Without a target, classification may select memory or knowledge; rough work
  requests, uncertain notes, and captures without a classifier go to inbox.
  Only an explicit task target creates a task, with its complete body in one
  write. Empty input writes nothing.
- `CaptureResult` tags direct memory, knowledge, task, and inbox domain results
  with `target`. Do not add copied record envelopes or compatibility result arms.
- Store exceptions become `write_failed` at the cross-store boundary. Typed
  store rejections such as `invalid_slug` and `already_exists` remain unchanged.
- Every write receives a resolved scope context. Unknown scopes fail at the
  route/client boundary; default-provider fallbacks are not valid multi-scope
  behavior.

Scope resolution for both cross-store surfaces is composed in
`src/modules/store-scope-context.ts`; memory and knowledge retain their own
provider and storage boundaries.

## Boundaries

- Do not restore a contributor registry. The four shipped targets are one
  closed product capability; adding a target updates the target union,
  classifier descriptions, and the exhaustive store transform.
- Do not write task or inbox files directly. Canonical writes dispatch through
  the repo-tasks mutation workflow.
- Keep dynamic prompt text conditional on the effective `capture` tool policy.
- Test target selection and observable store outcomes at their owning layer.
  Channel and CLI tests cover parsing/rendering only; do not mirror every result
  arm or manufacture runtime evidence from mocked transports.
