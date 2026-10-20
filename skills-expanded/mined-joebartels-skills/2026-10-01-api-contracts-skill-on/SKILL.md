---
name: go-api-contracts
description: Use when Go work creates or changes an exported API or consumer-visible CLI, wire, file, or error contract, including compatibility and release migrations. Not for private implementation edits with no observable contract change.
---

# Go API contracts

Choose the change against the project's supported consumers and release policy. A compatible signature is only part of a compatible API.

Read affected public documentation, call sites, tests, module path, supported Go versions, and release decisions. Identify what is promised, what consumers actually use, and what the task deliberately changes. A missing downstream repository limits the evidence; it does not establish that no consumers exist. Build a small representative consumer when necessary and distinguish it from a real integration. Ask only for missing policy that would change the implementation decision. Go's standard-library compatibility promise is not automatically a third-party module's policy.

Inspect the surface that the change can affect:

| Surface | Contract check |
| --- | --- |
| Functions and methods | Exact function types, return types and method sets, as well as ordinary calls. |
| Exported interfaces | External implementers and embedded interfaces; adding a required method can break them. |
| Exported values | Supported zero initialization, literals, embedding and constructors; behavior of existing values after adding state. |
| CLI and wire/file formats | Names, tags, omitted versus empty values, ordering, bytes where promised, stdout/stderr and exit status. |
| Errors and partial results | Documented identity/type checks, exposed causes and what results remain usable on failure. |

For example, changing `func Open(string) *Client` to `func Open(string, ...Option) *Client` preserves `Open("x")` but breaks `var factory func(string) *Client = Open`. When compatibility is required, choose an additive entry point or another compatible shape appropriate to the callers. An interface extension likewise needs evidence from external implementations, not just the package's own implementation. Package placement and whether an interface/options abstraction is necessary are separate decisions.

Before changing an exported type's representation, exercise its existing supported creation paths. Constructor examples alone do not make a previously usable exported zero value unsupported. Inspect any constructor-only precondition and the project's policy; when zero initialization is supported, preserve its observable behavior alongside new configuration. Distinguish an absent setting from an explicitly supplied empty/zero setting when they mean different things. A new field's zero value may silently change old values even when every existing constructor still works. This is a compatibility check, not a requirement to make every type zero-value usable.

Keep internal names and representations separate from promised external semantics. A private field rename can change serialization; initializing an empty slice can change `null` to `[]`. Decide from the schema and consumer contract instead of a universal preference. Preserve promised error behavior without automatically exposing new underlying errors or adding new sentinels.

When a breaking release is explicitly intended, implement it consistently: align module/import paths where required, update owned callers, and document old-to-new usage, changed semantics, and migration steps. Retain compatibility shims only when the release plan calls for them. A deliberate v2 contract does not require the v1 signature to survive in the new module.

Verify the affected contract at a consumer boundary. Compile representative function assignments or interface implementations; test supported zero/default and explicitly configured states; check relevant serialized outputs or CLI streams/status. Include the requested new behavior and a regression for the old behavior that must remain. Use focused checks suited to the actual change and supported toolchain. Report the contract decision, evidence and verification limits; do not infer compatibility solely from passing package-local tests.

This skill owns consumer-visible shape and evolution. Package responsibility/import direction belong to package-boundary work; abstraction necessity, construction design and resource ownership belong to composition work. Use those boundaries when relevant without requiring additional skills or redesigning unrelated code.
