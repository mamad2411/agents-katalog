# Retract Module

Owns explicit cross-store retraction targeting and its operator/agent surfaces.
The selected store remains the removal owner.

## Ownership

- `commands.ts` owns chat empty-input handling, request construction and plain-text
  replies. Channels supply the selected scope client, parsed input and target.

- `RetractProviderImpl` owns dispatch by the closed `RetractTarget` union.
- `store-retractor.ts` is the only cross-store persistence transform. It maps a
  uniform `target` plus `identifier` request to `MemoryProvider.delete`,
  `KnowledgeProvider.delete`, or the repo-tasks mutation boundary and returns
  those domain outcomes directly.
- Memory owns identity lookup, not-found, and atomic snapshot replacement; a
  failed delete leaves both its prior in-memory and durable snapshots intact.
  Knowledge owns identity lookup and atomic file removal, while its atomic
  replacement and ignored temporary files make interrupted writes restart-safe.
  Repo-tasks owns task/inbox path validation, mutation authorization,
  logical resources, not-found, durable outcomes, and recovery.
- Routes own untrusted JSON decoding and scope selection. The generated routine
  transport owns daemon request/response decoding for clients.
- The destructive tool effect and scope policy own confirmation. CLI, channels,
  and shared UI only map input or render outcomes.

## Contract

- Every request has one explicit `target` and one non-empty `identifier`.
  Store-specific names such as `id`, `slug`, and `path` do not escape the store
  transform.
- `RetractResult` tags direct memory, knowledge, task, and inbox domain results
  with `target` and `identifier`. Do not add copied record envelopes or
  compatibility result arms.
- Store exceptions become `retract_failed` at the cross-store boundary. Typed
  store rejections such as `not_found`, `invalid_id`, and `already_in_state`
  remain unchanged.
- Task retraction means a repo-task transition to `dropped`; it is not a delete.
  Inbox removal must remain inside the verified inbox parent.

Scope resolution for both cross-store surfaces is composed in
`src/modules/store-scope-context.ts`; memory and knowledge retain their own
provider and storage boundaries.

## Boundaries

- Do not restore a contributor registry or target-specific public request
  variants. The four shipped targets are one closed product capability.
- Do not perform destructive filesystem operations above the owning store.
- Keep dynamic prompt text conditional on the effective `retract` tool policy.
- Test target mapping and observable store outcomes at their owning layer.
  Channel and CLI tests cover parsing/rendering only; do not mirror every result
  arm or manufacture runtime evidence from mocked transports.
