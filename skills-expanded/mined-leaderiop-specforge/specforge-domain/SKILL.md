---
name: Specforge Domain
description: "SpecForge product knowledge -- the domain-free engine that turns what an organisation knows (its things, their relationships and the rules they must obey) into one typed, validated graph that people and AI agents read and change through CLI, MCP and LSP. Covers the five parts (extensions, graph, validation, surfaces, AI models), the five structural keywords, the builtin starter extensions, what is shipped versus planned, and the CLI. Use when explaining what SpecForge is, reasoning about the compiler or extension model, modelling any domain (software, product, marketing, pharma/GxP, operations) as extensions, or deciding whether something belongs in the graph."
---

# Specforge Domain

SpecForge is a domain-free engine. It turns what an organisation knows -- its things, how they relate, and the rules
they must obey -- into one typed, validated graph that people and AI agents read and change through standard
protocols. Software specification is one of its biggest use cases, not its definition.

## The five parts

| Part | What it is | Plain words |
|------|------------|-------------|
| **Extensions** | WASM packages that declare entity kinds, fields, edges, validation rules and commands | the "apps": they teach SpecForge a domain |
| **The graph** | every entity and link, compiled from `.spec` files | the "memory", the single source of truth |
| **Validation** | the extensions' rules plus structural checks, on every compile and every edit | the "referee": a change that breaks a rule is refused, whoever made it |
| **Surfaces** | CLI, MCP, LSP (with the VS Code extension) and the package registry today; AG-UI and HTTP planned | the "doors" |
| **AI models** | Claude or any agent, driving SpecForge from outside, mostly over MCP | the "brain": bring your own |

## The core knows five keywords

The grammar has five structural keywords: `spec` (the root entity), `ref` (a typed link outside the graph), `use` (an
import), `define` (reserved, registers nothing: W143) and `defaults` (file-level field defaults). Everything else --
`behavior`, `persona`, `invariant`, a GSD `phase`, a pharma `procedure` -- exists only because a loaded extension
declares it. A project's kinds depend only on the `extensions` list in `specforge.json`; with none, SpecForge runs in
structural-only mode (I002).

So the first question about any project is "which extensions does it load?" -- `specforge extensions`,
`specforge schema`, `specforge infer-guide` (MCP: `specforge.extensions`, `specforge.schema`). Write only the kinds
those declare; for a custom domain, its extension's declarations are the reference.

## The builtin extensions: a starter set

These ship inside the binary as examples of what an extension can declare. They are not the base.

| Extension | Declares |
|-----------|----------|
| `@specforge/software` | kinds `behavior`, `event`, `type`, `port` |
| `@specforge/product` | kinds `feature`, `journey`, `persona`, `channel`, `deliverable`, `milestone`, `module`, `term`, `release`; extension commands (`specforge product features`, ...) |
| `@specforge/governance` | kinds `invariant`, `decision`, `constraint`, `failure_mode` |
| `@specforge/formal` | kinds `property`, `axiom`, `protocol`, `refinement`, `process`; adds `requires`/`ensures`/`maintains`/`abstract`/`refines`/`sync` to behaviors; analysis passes |
| `@specforge/testing` | no kinds: which kinds owe `verify` obligations and with which verify kinds, and the coverage pass |
| `@specforge/cargo-test`, `@specforge/vitest` | test collectors for `specforge collect` |
| `@code/core`, `@rust/cargo`, `@rust/source`, `@javascript/source` | code facts placed in source (`package`, `item`, `test`): a Rust test attribute naming an entity anchors it |

`specforge model` renders the kinds and relationships the loaded extensions declare; it is the authoritative list.

## Use cases

- **Software specification** -- the builtins above. Spec frameworks can be modelled as extension families: a GSD
  family `@gsd/*` is being designed (its model lives under `gsd/`, nothing built yet); BMAD, OpenSpec and SpecKit
  extensions are not started.
- **Product management and marketing** -- features, personas, channels, journeys, releases, milestones.
- **Regulated industries** -- e.g. pharma/GxP: procedures, decisions, failure modes and an audit trace, with kinds a
  domain extension declares.
- **Any business with entities and rules worth checking.** SpecForge can be the product itself, or the harness a
  business runs on: extensions are its domain, AI models are the brain.

## Shipped vs planned (never blur these)

Shipped: the compiler and validator; the extension SDK and WASM runtime (`specforge extension init|build|validate`);
the builtin extensions; the CLI; the MCP server; the LSP and the VS Code extension; the package registry
(`add`, `extensions search`, `publish`); typed edits (`new`, `set`, `unset`, `link`, `unlink`, `delete`); `collect` (runs the test
runners that extensions declare, after approval, and the source collectors of the code packs); anchors (the edges
between entities and the facts placed in source: `specforge anchors`, MCP `find_implementation` /
`find_spec_for_source`, and in the editor Go to Implementation and the lenses, hover, references and rename in Rust,
TypeScript and JavaScript files); `infer-*` (guides for agents writing specs from existing code).

Planned or in progress -- say so, never imply they work:

- AG-UI and HTTP surfaces, and with them a UI for business users (today they reach SpecForge through an AI agent).
- Live connectors to business systems. WASM extensions are pure (one exported `call`, no imports), and providers
  register ref schemes with no host reader yet: SpecForge does not fetch or sync a CRM, Jira or GitHub.
- The GSD, BMAD, OpenSpec and SpecKit extension families.
- Evidence beyond tests: `verify` and `collect` are test-centred (`unit`, `property`, `integration`, ... as
  `@specforge/testing` declares them). Collecting domain evidence (a signed batch record, an audit) is future work.

## Compiler pipeline

```
.spec files -> Parser -> Resolver -> Graph -> Validation -> Surfaces
               (tree-     (imports,   (nodes,   (structural    (CLI output, MCP tools,
               sitter)    references) edges)    + extension    LSP diagnostics, exports)
                                                rules)
```

1. **Parser** -- a tree-sitter grammar with no domain knowledge: any keyword parses as a generic block.
2. **Resolver** -- binds every reference to an entity across the whole project (`use` is optional) and checks the
   target kind each field declares.
3. **Graph** -- in memory, rebuilt on each compile, incrementally under `specforge watch` and `specforge-lsp`. No database.
4. **Validation** -- structural checks (unknown kind E024, missing required field E006, wrong value E061, unresolved
   reference E003, wrong target kind E022, ...) plus each loaded extension's rules. `specforge explain <code>` explains
   every code (the catalog's anywhere, an extension's own inside the project that loads it); `docs/diagnostics.md`
   lists the catalog's.
5. **Surfaces** -- the same graph behind every door.

## Extension model

An extension is a WASM component built with the Rust SDK (`specforge-extension-sdk`). Its declaration contributes:

- **kinds** with typed fields (string, identifier, enum, enum_list, reference (one kind or a union), reference_list, string_list, date,
  integer (optionally bounded), bool, block and block_list (typed members), file references from the spec root or the
  project root), required flags, who writes each (`computed` by a compute pass, `harness` by a command's plan; E082/E083),
  history flags (`immutable` E084, `append_only` E085, judged against git), and an inference guide;
- **edges** between kinds, and **enhancements** that add fields to another extension's kind;
- **validation rules** (each with a diagnostic code), **passes** (e.g. formal analysis), **collectors** (test runners)
  and **commands** surfaced as `specforge <extension> <command>` and as MCP tools.

`specforge extension init` scaffolds one, `build` compiles it to `wasm32-wasip2`, `validate` loads it and reports its
declaration's diagnostics. `specforge add` installs from a builtin name, a `.wasm` file or a registry.

## CLI Commands

```bash
specforge init --extensions @specforge/product   # new project (specforge.json + spec/)
specforge add <ext> / remove <ext> / extensions  # manage what the project loads
specforge check [--strict] [--format json]       # parse, resolve, validate
specforge explain <code>                         # a diagnostic code
specforge infer-guide [kind]                     # what each declared kind holds and how to find it in code
specforge schema [--kind K] / model              # the declared kinds, fields and edges
specforge new|set|unset|link|unlink|delete       # typed edits (refuse one that adds errors: E080)
specforge query / trace <id> / explore / review  # read the graph (<id>: a path such as v1.0/03/D-01, or a unique short form)
specforge stats / export / format / migrate
specforge analyze                                # analysis passes declared by extensions (e.g. formal)
specforge collect                                # run declared test runners, record what their tests prove
specforge anchors <id> | --file <path>           # the code anchored to an entity, or the entities a file holds
specforge watch / mcp                            # incremental rebuild; MCP server over stdio
specforge-lsp                                    # the language server: a separate binary (the VS Code extension starts it)
specforge extension init|build|validate          # author an extension
specforge search <text>                          # entities by id, title or text
specforge extensions search / publish / login / update  # registry
specforge <extension> <command>                  # an extension's own commands, e.g. specforge product features
```

## What NOT to Do

- Do not call SpecForge "a software specification tool" -- software is one use case of a domain-free engine
- Do not present builtin kinds as "SpecForge's entity types" -- they are what the builtin extensions declare
- Do not write a kind before checking which extensions the project loads
- Do not claim live connectors, AG-UI/HTTP, a business-user UI, or non-test evidence collection exist -- they are planned
- Do not configure in the `spec` block or use `define` -- configuration is `specforge.json`, kinds come from extensions
- Do not assume a database or a server: the graph is in memory and every surface reads the same compile
- Do not hand-write traceability matrices or indexes -- `specforge trace` and `specforge export` generate them
