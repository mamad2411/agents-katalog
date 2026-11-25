---
name: coding-guidance-cpp
description: C++ implementation and review skill. Use when writing, modifying, refactoring, or reviewing C++ code, especially modern C++17/20/23 code that needs strong ownership, type safety, and testable design. Portable across C++ repos and build systems.
---

# C++ Coding Guidance

This skill adds portable C++ implementation, refactoring, and review guidance.

## Adjacent Skills

This skill provides portable C++ engineering principles. Compose with:

- **Workflow:** **thinking** (planning), **recursive-thinking** (stress-testing),
  **security** (threat modeling)
- **Domain overlays:** **backend-guidance** (server-side code),
  **ui-guidance** (graphical UI/web frontend),
  **project-core-dev** (repo-specific build/test commands)

## When Not to Lean on This Skill

- non-C++ work
- legacy or bare-metal environments where modern C++ guidance must be adapted
  selectively
- pure architecture or process work with no C++ design or code judgment needed

## Implementation Workflow

1. Read the touched code, build shape, existing tests, and any nearby docs or
   shorthand notes before editing.
2. If the request is partially specified, infer the intended behavior from the
   existing code and tests. Ask only when multiple plausible C++ designs would
   change semantics.
3. Choose the narrowest change that solves the problem without hiding ownership,
   lifetime, or error-handling contracts.
4. Implement with simple, strongly typed interfaces and modern C++ defaults.
5. Add or update tests close to the changed behavior.
6. Run the narrowest relevant format, build, test, sanitizer, and analyzer
   targets the repo supports.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current behavior, invariants, side effects, and risky hotspots.
2. Break the refactor into small slices that preserve behavior.
3. Remove duplication, long functions, or muddled responsibilities one step at
   a time.
4. Keep tests passing after each slice; add characterization coverage first when
   behavior is unclear.
5. Stop when the code is simpler and safer.

## Review Workflow

When reviewing (not implementing), skip the implementation workflow and use this
instead:

1. Read the change in full before commenting.
2. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
3. Prioritize bugs and regressions, ownership and lifetime errors, exception or
   error-path holes, thread-safety issues, security risks, performance mistakes
   with real impact, and missing tests.
4. State findings with concrete evidence and the likely consequence.

## C++ Rules

### First tier - causes bugs

- Treat raw pointers and references as non-owning; never transfer ownership by
  raw pointer or reference
- Avoid `new` and `delete`; bind resource lifetime to object lifetime with RAII
- Prefer `std::unique_ptr` by default; use `std::shared_ptr` only for real
  shared lifetime and `std::weak_ptr` to break cycles
- Prefer values and stack allocation over heap allocation when ownership is
  simple
- Avoid unchecked bounds access; prefer `.at()`, iterators, range-for, or
  `std::span` when bounds are uncertain
- Avoid silent narrowing conversions; use explicit casts or narrowing helpers
- Prefer compile-time checking to runtime checking when the type system can
  express the rule
- Do not mix exception and error-code styles inconsistently inside one path

### Second tier - prevents mistakes

- Avoid C-style casts; use `static_cast`, `const_cast`, `reinterpret_cast`, and
  `dynamic_cast` deliberately
- Prefer rule-of-zero types; if you write a destructor or custom special member
  function, justify it
- Use `const` and `constexpr` by default; mutability should be the exception
- Prefer `enum class` over plain enums and `nullptr` over `NULL`
- Prefer `std::array` over C arrays, `std::string_view` for non-owning strings,
  and `std::span` for non-owning ranges when lifetime rules are clear
- Prefer standard algorithms and ranges over open-coded loops when they make the
  intent clearer
- Use `[[nodiscard]]` when ignoring a result is likely a bug
- Avoid `using namespace std` in headers
- Keep warnings at zero in repo-owned code

### Modern feature selection

- Use C++20 or C++23 features when they make contracts clearer, not to signal
  modernity
- Use concepts to constrain templates when the constraint is part of the public
  contract; avoid them for local cleverness
- Use ranges when they improve readability; avoid long adaptor pipelines that
  hide cost or control flow
- Use `std::span` and `std::string_view` for non-owning parameters only when
  the caller can satisfy the lifetime contract clearly
- Use coroutines only when the repo already embraces them or when they simplify
  asynchronous control flow more than callback, future, or thread-based
  alternatives
- Prefer vocabulary types such as `std::optional`, `std::variant`, and
  `std::expected` when they encode real domain states better than sentinels or
  ad hoc conventions
- Do not introduce template metaprogramming, custom allocators, or exotic
  zero-cost abstractions unless measurement or reuse pressure justifies them

### Error and contract model

- Pick one primary error model per subsystem: exceptions, status-return, or
  `std::expected`; cross-model adapters should be explicit at boundaries
- Use exceptions for exceptional failures only when the repo and call graph are
  already built around exception safety
- Prefer return-value error models where failure is routine, expected, or part
  of normal control flow
- State ownership, nullability, lifetime, and thread-safety contracts in the
  type system when possible, and in comments only when the type system cannot
  express them cleanly
- Public APIs should make invalid states hard to represent and expensive states
  visible to callers

### Headers and interfaces

- Minimize header surface; prefer forward declarations when they reduce stable
  dependencies without obscuring the contract
- Do not put heavy includes, macros, or implementation-only dependencies in
  public headers without a clear reason
- Keep inline and template-heavy code in headers only when required by the
  language or justified by measurement
- Prefer free functions or narrow interfaces over large classes that force
  unnecessary rebuild and dependency coupling
- Be explicit when ABI stability, plugin boundaries, or C interop constrain the
  design
- Treat rebuild surface, transitive include fan-out, and template instantiation
  cost as design costs, not just build-system problems

### Concurrency and synchronization

- Make thread ownership and synchronization strategy explicit; “probably
  thread-safe” is not a contract
- Prefer message passing, task ownership, or data partitioning before shared
  mutable state
- Protect invariants, not individual fields; lock scope should match the real
  consistency boundary
- Use atomics only when the memory-ordering contract is understood and simpler
  locking would not be clearer
- Treat coroutine, callback, and thread handoff points as lifetime hazards

### API and abstraction discipline

- Functions should do one thing, stay at one level of abstraction, and justify
  more than two meaningful parameters
- Treat boolean flag parameters as a design smell; split behavior or introduce a
  parameter object when that makes the contract clearer
- Prefer composition and value semantics over inheritance unless polymorphism is
  the actual domain model
- Avoid “config bag” APIs where many weakly related booleans, enums, or strings
  simulate a missing type
- Make ownership and mutation visible at API boundaries; hidden allocation,
  caching, or global state is a design smell in “clean-looking” code
- Be suspicious of abstractions that look tidy but add virtual dispatch,
  allocation, copies, or lifetime coupling without a clear benefit
- Be suspicious of public template abstractions that improve local elegance but
  increase compile time, error verbosity, or rebuild cost across the repo
- Prefer moving implementation detail out of headers when doing so preserves the
  contract and reduces dependency drag

## Decision Heuristics

Use these when the right choice is not obvious:

- **Scope check:** if a change touches more than 3 public interfaces, stop and
  plan before continuing; the change is bigger than it looks.
- **Ownership clarity:** if ownership is not obvious from the type signature,
  redesign the interface or add a one-line contract comment.
- **Error-model consistency:** do not mix exceptions, error codes, and
  `expected`-style returns within one subsystem unless the boundary is explicit.
- **Repo conventions:** if the repo has established rules for exceptions,
  containers, ownership types, or naming, follow them unless they create a
  correctness or safety problem.
- **Feature pressure:** do not introduce concepts, ranges, coroutines, or
  metaprogramming unless they make the code simpler for this repo's likely
  maintainers.
- **Interface pressure:** if a header starts dragging in broad dependencies or
  exposing implementation detail, narrow the interface before adding more code.
- **Build-surface pressure:** if a design pushes more logic, templates, or
  dependencies into public headers, justify the compile-time and rebuild cost.
- **Parameter pressure:** when adjacent parameters have the same type, or the
  function needs more than 2-3 meaningful inputs, prefer a named type or helper
  struct.
- **Test setup size:** if test setup exceeds about 20 lines, extract a fixture
  only when the setup is reused or the test intent becomes unclear.
- **Narrowness vs. quality:** implement the narrowest change that solves the
  problem. When narrowness conflicts with correctness or safety, prefer
  correctness. When it conflicts with style alone, prefer narrowness unless the
  task is explicitly a cleanup.
- **Refactor boundary:** outside explicit refactor work, fix at most one small
  adjacent issue while you are in the file.
- **Abstraction threshold:** three similar code blocks or repeated API-shaping
  pain is a pattern; before extracting, check whether a free function, helper
  type, or composed object is the simpler move.
- **Performance rule:** optimize only after measurement, except for obvious
  ownership, allocation, or algorithmic mistakes on hot paths.
- **UB-sensitive optimization:** treat optimizations that rely on subtle
  lifetime, aliasing, or memory-order assumptions as high-risk until proven by
  evidence and tooling.

## Validation

A change is done when:

- the code compiles without new warnings, unless the repo explicitly treats a
  known warning set as baseline debt outside the change
- existing tests pass
- new or changed behavior has test coverage, or the lack of coverage is called
  out with a concrete reason
- the repo's formatter has been run
- configured static analyzers report no new findings
- available sanitizers are clean for the touched paths when the change affects
  memory safety, threading, or undefined-behavior risk
- performance-sensitive changes are measured instead of justified by intuition
- review findings at `Critical` and `Important` severity are addressed
