---
name: webassembly-engineering
description: WebAssembly engineering guidance for Wasm/WAT modules, WASI, WIT and the Component Model, host/guest contracts, runtime and target selection, capability grants, memory/ABI/serialization, lifecycle/errors, testing, packaging, and deployment. Use when a WebAssembly artifact, host embedding, runtime, component, or WASI boundary is being designed, changed, tested, reviewed, packaged, or deployed. Do not use for source-language/compiler mechanics, generic dependency work without a Wasm boundary, or a product comparison without repository and current-doc evidence.
---

# WebAssembly Engineering

Use this skill for the boundary between a WebAssembly artifact and the host that
loads, instantiates, calls, grants authority to, packages, or deploys it. Treat
the exact core module/component, host, runtime release, backend, target, and
capability implementation as one compatibility and security decision.

Do not infer support, portability, isolation, performance, or authority from a
`.wasm` suffix, successful local build, core validation, a WASI name, or a
runtime's general marketing claim.

## Scope and routing

This skill owns:

- Wasm binary and WAT text artifacts, core imports/exports, and embedding
  boundaries;
- WASI profile and import selection; WIT packages/worlds; Component Model and
  Canonical ABI compatibility;
- host/guest contract shape, values, linear memory, ownership, serialization,
  resource handles, lifecycle, traps, exit/error mapping, and resource limits;
- runtime/backend/OS/CPU/AOT-or-JIT/browser target evidence, packaging, and
  deployment validation; and
- capability grants and the host implementation of filesystem, network,
  environment, clock, random, process, browser, and download surfaces.

Source-language, compiler, package-manager, binding-generator implementation,
and framework mechanics remain with the matching language/framework skill. For
example, Rust ownership, Cargo, `wasm-bindgen`, generated Rust bindings, and
Rust-target implementation belong to [`rust-engineering`](../rust-engineering/SKILL.md),
[`rust-async-web`](../rust-async-web/SKILL.md), and
[`rust-testing-quality`](../rust-testing-quality/SKILL.md) as applicable. This
skill defines the host/guest and target evidence those implementations must meet;
it does not replace their source-level guidance.

Use [`api-design`](../api-design/SKILL.md) for a published service, SDK, CLI, or
event contract beyond the host/guest boundary. Use
[`documentation-engineering`](../documentation-engineering/SKILL.md) for
reader-facing documentation after the contract is settled. Use
[`ci-release-engineering`](../ci-release-engineering/SKILL.md) for checked-in
release automation and [`container-engineering`](../container-engineering/SKILL.md)
for OCI/Compose implementation.

## Mandatory executable-input gate

Treat modules, components, runtimes, toolchains, compilers, bindgen/component
composers, generated bindings, packages, registries, downloaded artifacts, host
integration code, and browser-delivered Wasm as untrusted executable
supply-chain inputs. Before downloading, installing, generating, loading,
instantiating, compiling, testing, or otherwise executing any such input:

1. Load [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md),
   [`security-review`](../security-review/SKILL.md), and
   [`security-review-evidence`](../security-review-evidence/SKILL.md).
2. Inspect repository policy and use static evidence first: origin, immutable
   version or revision, digest/signature/provenance where available, manifest and
   lockfile state, generated/vendored diff, transitive native/build inputs, and
   intended host integration.
3. Identify every proposed effect: filesystem writes and reads, network egress,
   inherited environment/credentials, subprocesses, executable memory, browser
   origin/storage/downloads, caches, and artifact locations. Authorization to
   run a command does not contain its transitive effects.
4. Obtain the required execution authority and use isolation appropriate to the
   repository trust decision. If provenance, security review, evidence handling,
   authority, or isolation is unresolved, stop before execution and report the
   blocked evidence.

This gate also applies to an apparently passive browser flow: fetching,
streaming, compiling, instantiating, or downloading Wasm crosses delivery and
execution boundaries. Do not treat a lockfile, checksum, typed binding, browser
sandbox, or runtime validation as a complete trust or isolation claim.

## Repository-first workflow

1. Inspect the repository's manifests, lockfiles, artifact build/package paths,
   host embedding code, WIT/WAT/Wasm assets, target configuration, tests,
   deployment descriptors, CI, runtime pin, and existing capability policy.
   Preserve unrelated changes.
2. Classify the artifact precisely: core module or component; WAT source or
   binary; selected core features; exported/imported functions; for components,
   Component Model/Canonical ABI generation plus WIT package versions and world.
3. Define the host/guest contract before changing code. Name each import/export,
   value and serialization representation, linear-memory allocation and
   ownership rule, string/list encoding, resource-handle lifetime, reentrancy
   constraint, trap versus recoverable error behavior, start/initialize/stop
   sequence, cancellation, and resource quota.
4. Start from no authority. Derive required capabilities from actual imports or
   the selected WIT world, then grant only explicit, bounded host capabilities.
   Record the implementation and limits, not merely an interface name.
5. Select an artifact form, runtime, backend, and target using the repository's
   requirements plus current official, versioned evidence. Read
   [the target and runtime selection evidence workflow](references/target-runtime-selection.md)
   when selecting or asserting support for a runtime, target, component/WASI
   line, browser delivery, AOT/JIT mode, or deployment host. It is not a product
   matrix and cannot prove an unrecorded combination.
6. Design tests at the lowest useful boundary: import/export and WIT contract
   tests, invalid/oversized memory and serialization cases, trap/error mapping,
   denied-capability behavior, lifecycle cleanup, resource-limit exhaustion, and
   exact target-host smoke tests. Do not use a different runtime, backend, or
   browser as compatibility proof.
7. Package only the reviewed artifact and its declared metadata. Record artifact
   identity, producer/toolchain/runtime versions, WIT world/ABI/WASI profile,
   target, capability policy, delivery integrity requirements, and rollback or
   compatibility fallback. Validate deployment in the intended target environment
   after the executable-input gate is satisfied.

## Capability boundaries

Every host capability is a security boundary owned by the embedding and
deployment policy, not by core Wasm validation.

- **Filesystem:** use explicitly scoped/preopened paths, an explicit symlink and
  path-race policy, access modes, quotas, and cleanup ownership. A guest path is
  never proof of host containment.
- **Network and HTTP:** define allowed schemes, destinations, ports, DNS/redirect
  behavior, proxy rules, credentials, request/response limits, timeouts, and
  egress enforcement. An imported socket or HTTP interface is not ambient
  network authority.
- **Environment, process, clocks, and randomness:** allowlist environment values;
  explicitly map stdin/stdout/stderr and exit semantics; define process-spawn
  policy; provide intentional clock/random sources; never pass ambient host
  credentials by default.
- **Browser and download delivery:** origin, CORS, Content-Type, CSP, integrity,
  caching, storage, worker/thread availability, user-visible downloads, and
  browser APIs are separate host constraints. Bare browser Wasm does not imply
  WASI or Component Model support.
- **Custom imports:** version, authenticate, authorize, bound, and test each host
  function as an application API. Keep guest-controlled lengths, pointers,
  handles, callbacks, and serialized values validated at the host boundary.

Load `security-review` and `security-review-evidence` for these boundaries even
when a task does not execute artifacts; load `threat-modeling` when designing a
new authority model, untrusted-code boundary, plugin model, or sensitive data
flow.

## Contract and lifecycle rules

- Prefer WIT worlds/components when an independently versioned interface and
  Canonical ABI are the intended portable boundary; use a core-module import ABI
  only when the selected host documents and tests that boundary.
- Pin WIT package versions, selected world, Component Model/Canonical ABI line,
  WASI profile, and producer/consumer releases together. A matching `.wasm`
  extension does not make components and core modules interchangeable.
- Make ownership explicit across linear memory and lifting/lowering boundaries:
  who allocates, who frees, when borrowed data expires, maximum sizes, alignment,
  invalid pointer/length behavior, and how handles become invalid.
- Choose a serialization contract deliberately. Specify encoding, schema/version
  negotiation, bounds, canonicalization where needed, and failure behavior; do
  not pass opaque guest-controlled bytes into trusted host APIs unvalidated.
- Separate expected guest errors from traps, cancellation, timeout, host failure,
  fuel/epoch/resource exhaustion, and process exit. Map each to an observable,
  safe host result and ensure cleanup is idempotent.
- Specify instantiation, initialization, call concurrency/reentrancy, shutdown,
  restart, and resource-release ownership. Do not assume dropping a host handle
  rolls back external effects or terminates guest-spawned work.

## Completion evidence

Before handoff, report:

1. artifact form, core features, WIT world/package versions, ABI and WASI profile;
2. exact host/runtime/backend/toolchain and OS/CPU/target evidence, plus every
   unresolved support claim;
3. capability grants, implementation limits, and the corresponding security
   review/evidence status, using sanitized details only;
4. supply-chain/provenance review status for every executable/download/generator
   surface and whether any execution was intentionally blocked or skipped;
5. contract, denial, error/trap, lifecycle, resource-limit, and intended-target
   test results; and
6. packaging/deployment identity, delivery controls, rollback/fallback plan, and
   residual runtime, host, browser, or proposal risk.

Never turn missing versioned host evidence into a portability, sandboxing, or
security guarantee.
