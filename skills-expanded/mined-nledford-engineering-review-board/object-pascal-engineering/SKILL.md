---
name: object-pascal-engineering
description: Object Pascal and Delphi engineering guidance. Use when adding, changing, reviewing, testing, packaging, or refactoring Object Pascal or Delphi source, .pas/.dpr/.dpk/.inc files, Delphi or Free Pascal projects, .dproj/.dpr/.lpi/.lpk project files, VCL/FMX/LCL forms and frames, units, packages, compiler directives, or build tooling. Use for ordinary Object Pascal implementation and project mechanics; use object-pascal-design-patterns for pattern choice, object-pascal-antipatterns for smell-focused review, object-pascal-testing-quality for test-lane work, and photo-supreme-scripting for Photo Supreme's embedded scripting environment. Do not use for database-native schema/query design, checked-in CI/release-provider configuration, Docker/OCI/Compose configuration, or a public API contract; use the owning SQL, CI/release, container, or API skill instead.
---

# Object Pascal and Delphi Engineering

Use this skill for project-neutral Object Pascal implementation and the
Delphi/Free Pascal toolchain, RTL, VCL/FMX/LCL, package, and build mechanics that
the target repository actually uses. Inspect the repository before selecting a
compiler, dialect, framework, package, or command.

## Use When

- Adding, changing, reviewing, testing, packaging, or refactoring `.pas`, `.dpr`,
  `.dpk`, `.inc`, `.dproj`, `.lpi`, `.lpk`, or `.dfm`/`.lfm`/`.fmx` files.
- Selecting repository-native compiler, build, package, and quality commands.
- Working with Delphi (RAD Studio), Free Pascal, or Lazarus projects.

Do not use this as the primary skill for pattern selection, smell-only review,
test strategy, or Photo Supreme scripting; route those to the sibling skills.

## Scope And Routing

Own Object Pascal language, RTL, VCL/FMX/LCL, package, and build mechanics. Load
[`object-pascal-design-patterns`](../object-pascal-design-patterns/SKILL.md) for
positive design choices,
[`object-pascal-antipatterns`](../object-pascal-antipatterns/SKILL.md) for
evidence-backed smells,
[`object-pascal-testing-quality`](../object-pascal-testing-quality/SKILL.md) for
tests and quality lanes, and
[`photo-supreme-scripting`](../photo-supreme-scripting/SKILL.md) for Photo
Supreme's embedded interpreter.

- Use [`api-design`](../api-design/SKILL.md) for HTTP, RPC, SDK, CLI, event,
  serialization, versioning, or error contracts; keep Object Pascal handlers and
  types here.
- Use [`sql-engineering`](../sql-engineering/SKILL.md) plus the matching engine
  skill for database-native schema, query, transaction, index, privilege,
  migration, or plan behavior. This skill owns FireDAC/dbExpress/ADO adapter
  mechanics, not database semantics.
- Use [`ci-release-engineering`](../ci-release-engineering/SKILL.md) for
  checked-in hosted workflow/release behavior and
  [`container-engineering`](../container-engineering/SKILL.md) for Docker/OCI or
  Compose behavior. This skill owns the Object Pascal commands those workflows
  invoke.
- Use [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md),
  [`security-review`](../security-review/SKILL.md), and
  [`security-review-evidence`](../security-review-evidence/SKILL.md) before
  executing an input that can restore, load, generate, compile, or run
  third-party code.
- Use [`parallelism-engineering`](../parallelism-engineering/SKILL.md) when
  CPU-bound partitioning, worker bounds, reductions, cancellation across workers,
  or oversubscription is the design problem. Keep ordinary
  `TThread`/`TTask`/`TParallel` mechanics here.
- Use [`observability-engineering`](../observability-engineering/SKILL.md) for
  telemetry semantics; keep Object Pascal logging and instrumentation mechanics
  here.
- Use [`documentation-engineering`](../documentation-engineering/SKILL.md) for
  XMLDoc/PasDoc and reader-facing docs, and
  [`ux-accessibility-review`](../ux-accessibility-review/SKILL.md) for rendered
  VCL/FMX/LCL UI review.

## Repository-First Workflow

1. Inspect project files (`.dproj`, `.dpr`, `.dpk`, `.lpi`, `.lpk`,
   `.groupproj`), compiler directives, search paths, conditional defines, package
   references, `.inc` files, `.dfm`/`.lfm`/`.fmx` form files, test projects, CI,
   README/AGENTS guidance, and existing build/format/test commands. Record the
   compiler and dialect (Delphi vs FPC mode), target platforms, framework
   (VCL/FMX/LCL), runtime-package policy, and existing commands.
2. Classify the change: language behavior, build/project graph, dependency,
   public contract, UI/form, data adapter, database behavior, test, or
   deployment. Load only the companion skills whose boundary the evidence
   reaches.
3. Derive commands from target evidence. Prefer its documented recipe,
   checked-in scripts, CI command, and pinned compiler. If none exists, select
   only a command available in the resolved toolchain and state the assumption.
4. Complete the pre-execution provenance gate before a command can restore, load,
   generate, compile, or execute external inputs. Then specify behavior and edge
   cases before editing. Use
   [`test-driven-development`](../test-driven-development/SKILL.md) for focused
   behavior/regression work and
   [`behavior-driven-development`](../behavior-driven-development/SKILL.md) for
   user-visible workflows.
5. Keep domain policy independent of VCL/FMX/LCL, data-access, transport,
   persistence, and UI details unless the project intentionally makes the code an
   adapter. Load the appropriate architecture skill when that boundary is the
   design problem.
6. After the gate, run the narrowest repository-approved build, test, or
   target-environment check first, then the broader applicable lane. Report
   commands not run and the version-sensitive reason.

## Executable Input and Provenance Gate

Treat the following as executable supply-chain inputs, even when their extension
or purpose suggests configuration rather than code:

- a compiler selected by project files, `.inc`/`.cfg`/`.dof` options, build
  scripts, or IDE configuration;
- every package (`.dpk`/`.lpk`), runtime package, design-time package, component
  library, IDE expert, or third-party unit;
- every external library, DLL, static library, or generated unit whose source is
  not already trusted; and
- any invocation of the compiler (`dcc32`/`dcc64`/`dccaarm`/`dccaarm64`/`fpc`),
  `msbuild`, `lazbuild`, `brcc32`/`cgrc`, a package build, or a custom build
  script that can cause one of those inputs to be restored, loaded, generated,
  compiled, or executed.

Before executing any such surface, load
[`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md),
[`security-review`](../security-review/SKILL.md), and
[`security-review-evidence`](../security-review-evidence/SKILL.md). Establish
the applicable package/component/tool identity, version or digest, publisher and
source, transitive and build-time effects, and repository approval policy.
Perform the security review and retain only sanitized evidence. A previous
successful build is evidence to assess, not permission to execute. If provenance
or policy is unresolved, do not run the command; report the blocked input and
missing evidence instead.

## Toolchain and Version Discipline

- Treat the compiler, dialect, target platform, framework, and package graph as a
  compatibility set. A compiler accepting syntax does not prove the target
  runtime, RTL, framework, or OS supports it.
- Delphi and Free Pascal are related but distinct dialects. Do not assume a
  Delphi-only feature (inline variables, anonymous methods, attributes,
  `System.Threading`, `TParallel`) exists in FPC mode, or that an FPC extension
  exists in Delphi. Inspect the compiler mode (`{$MODE DELPHI}`/`{$MODE OBJFPC}`),
  `{$IFDEF}` guards, and target.
- Do not silently change the compiler, dialect mode, target platform, framework,
  runtime-package policy, or conditional defines. These alter build selection or
  behavior.
- Preserve the repository's project-file structure and existing property/option
  policy. Avoid overriding inherited options or using broad conditional-
  compilation changes for a local concern without proving their affected build
  set.
- Treat warnings, hints, range/overflow checks, and assertions as part of the
  compilation contract. Follow the repository's configured diagnostic policy
  rather than blanket-suppressing warnings or disabling checks.
- Select build/test/package mechanics from checked-in scripts, CI, and the
  resolved toolchain. Do not assume a command's default configuration, target,
  or output; record each explicitly when it matters.

## Idiomatic Object Pascal

- Follow the repository's naming and formatting conventions. Where none exist,
  the common Object Pascal convention is `T` for types, `I` for interfaces, `E`
  for exceptions, `F` for fields, `A` for parameters, `L` for locals, `c`/`sc`
  for constants, and `rs` for resource strings; use `PascalCase` and avoid type
  prefixes on variables.
- Keep units cohesive: interface section for the public contract, implementation
  section for private detail, `initialization`/`finalization` only when genuinely
  needed. Group `uses` logically and keep implementation-only units in the
  implementation `uses` clause.
- Prefer `const` parameters for immutable inputs and `var`/`out` for outputs.
  Make ownership and mutation visible in signatures.
- Prefer `try..finally` for resource release and `FreeAndNil` over `.Free` for
  owned object fields. Use `try..except` only where the boundary can handle the
  error meaningfully.
- Prefer generics and the generic collections (`TList<T>`, `TObjectList<T>`,
  `TDictionary<TKey,TValue>`, `TQueue<T>`, `TStack<T>`) over untyped `TList` or
  `TStrings` used as a data structure. Use `TArray<T>` for fixed-size sequences.
- Prefer records with methods/operators for small value types; use `class` for
  identity and polymorphism. Use `{$SCOPEDENUMS ON}` and qualified enum values in
  new code.
- Prefer interfaces for substitution seams and reference-counted ownership;
  understand that interface references and object references to the same instance
  have different lifetime rules.
- Prefer `for..in` over index loops when the collection supports enumeration.
  Prefer `case` with explicit branches over long `if..else if` chains.
- Make string encoding explicit. Delphi `string` is `UnicodeString`; distinguish
  `AnsiString`, `WideString`, `UTF8String`, and `TEncoding` conversions at
  boundaries. Do not assume byte length equals character count.
- Make culture-sensitive formatting explicit: use `TFormatSettings` for
  `Format`/`StrToFloat`/`FloatToStr`/date parsing rather than relying on the
  process locale.
- Keep `with` out of new code; qualify identifiers instead.
- Prefer `TStopwatch`/`TTimeSpan` over manual tick arithmetic and
  `System.DateUtils` over raw `TDateTime` `Double` math.

## Modern Language Features

Use these only when the target compiler and dialect support them and the
repository already uses them:

- Inline variables (`var` in `begin..end`) and inline `for var i := ...`
  (Delphi 10.3+).
- Generics, generic methods, and constrained type parameters.
- Anonymous methods and method references (`TProc`, `TProc<T>`, `TFunc<T>`,
  `TMethod`).
- Records with methods, operators, and helpers; class helpers and record helpers.
- Attributes and RTTI-driven behavior.
- `for..in` enumerators, `TEnumerable<T>`, `TComparer<T>`,
  `TEqualityComparer<T>`.
- `System.Threading` (`TTask`, `IFuture<T>`, `TParallel`),
  `System.Generics.Collections`, `System.Generics.Defaults`.
- `TStringHelper` and `TStringBuilder` for string building.
- `System.SysUtils` `TFile`/`TPath`/`TDirectory`, `System.Classes` streams,
  `System.Net.HttpClient`, `System.NetEncoding`, `System.JSON`.

Do not introduce a feature merely because the newest compiler supports it; match
the repository's declared compatibility range.

## Memory and Resource Ownership

- Make the owner of every object, stream, handle, and interface reference clear.
  The code that creates or explicitly takes ownership performs the matching
  cleanup.
- Use `try..finally` around owned resources; initialize owned fields to `nil`
  before the `try` so `FreeAndNil` is safe on partial construction.
- Understand interface reference counting: a `TInterfacedObject` frees itself
  when its last interface reference is released; mixing object and interface
  references, circular references, or `TComponent` ownership can leak or
  double-free. Use `TComponent` ownership for component trees and interfaces for
  substitution, not both for the same lifetime.
- Do not dispose an injected or shared dependency. Do not free an object owned by
  a `TComponent`, `TObjectList`, or collection.
- Use `TObjectList<T>.Create(True)` (owns objects) deliberately; document when
  ownership is not transferred.
- Close and free data-access objects (`TDataSet`, `TFDQuery`, `TFDConnection`)
  with explicit ownership; do not rely on form destruction for correctness in
  non-UI code.
- Prefer `TStream`/`TFileStream`/`TMemoryStream`/`TStringStream` with
  `try..finally`; use `TEncoding` for text streams.

## Concurrency

- Keep UI work on the main thread. Use `TThread.Queue`/`TThread.ForceQueue` to
  marshal results back; use `TThread.Synchronize` only when the caller must
  block, and never from the main thread.
- Prefer `TTask`/`TParallel`/`IFuture<T>` for short-lived parallel work over
  hand-rolled `TThread` subclasses. Use `TThread` subclassing when the work has a
  real lifetime and state.
- Guard shared mutable state with `TMonitor`, `TCriticalSection`, or
  `TInterlocked`; prefer immutable data and message passing over shared mutation.
- Bound worker counts and queue sizes; do not oversubscribe the CPU or create
  unbounded `TThreadedQueue<T>`.
- Check `Terminated` in long loops; do not use deprecated `Suspend`/`Resume`. Be
  careful with `FreeOnTerminate` combined with `WaitFor`.
- Do not call `Application.ProcessMessages` to fake concurrency; it causes
  reentrancy.

## Errors and Exceptions

- Model expected failures with typed exceptions or explicit result/error paths.
  Raise specific exception classes; do not raise bare `Exception` for control
  flow.
- Preserve diagnostic context; do not swallow exceptions with empty `except`
  blocks. When suppression is genuinely required (logging, finalization), comment
  why and provide a fallback.
- Translate infrastructure exceptions only where the caller contract requires it.
  Do not expose internal or sensitive details across a trust boundary.
- Use `Assert` for internal invariants that must hold in debug builds, not for
  input validation.

## Strings, Unicode, and Encoding

- Treat `string` as UTF-16 `UnicodeString` in Delphi. Convert explicitly at file,
  network, and interop boundaries with `TEncoding`.
- Do not cast `string` to `PChar`/`PAnsiChar` or use `Move`/`FillChar` on managed
  types without a proven, documented reason.
- Use `TStringBuilder` for repeated concatenation in loops.
- Use `TFormatSettings` for culture-sensitive parsing and formatting.

## Build, Packages, and Project Files

- Delphi: `dcc32`/`dcc64`/`dccaarm`/`dccaarm64` compile; `msbuild` builds
  `.dproj`/`.groupproj`; `brcc32`/`cgrc` compile resources. Runtime packages
  (`.bpl`) and design-time packages change deployment and must be preserved
  deliberately.
- Free Pascal/Lazarus: `fpc` compiles; `lazbuild` builds `.lpi`/`.lpk`; the
  dialect is selected by `{$MODE}`. Do not assume Delphi RTL units exist.
- Preserve the repository's target platforms, output directories, search paths,
  conditional defines, and package references. Do not hand-edit generated project
  files when a maintained source exists.
- Treat `.dfm`/`.lfm`/`.fmx` form files as generated or IDE-owned unless the
  repository edits them as source; prefer the form designer or a deliberate,
  reviewed edit.

## Testing Routing

Use [`object-pascal-testing-quality`](../object-pascal-testing-quality/SKILL.md)
for DUnitX, DUnit, fpcunit, integration, UI, and quality lanes. Use
[`test-driven-development`](../test-driven-development/SKILL.md) for behavior
changes and [`systematic-debugging`](../systematic-debugging/SKILL.md) for active
failures.

## Pattern Routing

Use [`object-pascal-design-patterns`](../object-pascal-design-patterns/SKILL.md)
for interfaces, factories, adapters, repositories, value objects, observers, and
resource ownership.

## Documentation Routing

Use [`documentation-engineering`](../documentation-engineering/SKILL.md) for
XMLDoc comments and PasDoc output. Native types and signatures come first; XMLDoc
records caller-relevant facts the signature cannot express.

## API, Database, and Observability Routing

Use [`api-design`](../api-design/SKILL.md) for public contracts, the SQL skills
for database-native behavior, and
[`observability-engineering`](../observability-engineering/SKILL.md) for durable
telemetry design.

## Security and Supply-Chain Routing

Use [`security-review`](../security-review/SKILL.md) for trust boundaries: input,
files, paths, deserialization, SQL, outbound requests, secrets, and error
disclosure. Use
[`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
before trusting packages, components, DLLs, or IDE experts.

## Anti-Patterns

Avoid `with` abuse, global mutable state, missing `try..finally`, empty `except`
blocks, blanket warning suppression, disabled range/overflow checks, `Variant`
overuse, untyped collections, string-built SQL, and `Application.ProcessMessages`
reentrancy. Use
[`object-pascal-antipatterns`](../object-pascal-antipatterns/SKILL.md) for an
evidence-backed refactoring review.

## Successful Use

Report the supported compiler/dialect/target evidence, changed language or
project surface, selected compatibility policy, checks run, and remaining
unverified host, framework, or platform assumptions.
