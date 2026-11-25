---
name: scaffold
description: >-
  Use when one aggregate, entity, value object, domain event, error, service, port,
  repository, adapter, gateway, policy, job, background job, state machine, process manager,
  event handler, builder, end-to-end spec or context is needed, or the guard refuses a
  hand-written file.
argument-hint: "<kind> <context> <Name> [options]"
allowed-tools:
  - Read
  - Edit
  - Bash(npx ddd-ts-kit generate *)
  - Bash(npx ddd-ts-kit move-to-module *)
  - Bash(npx ddd-ts-kit check *)
  - Bash(npx ddd-ts-kit list *)
---

# Scaffold one file

Requested: `$ARGUMENTS`

Boilerplate is generated, never typed: the generator and the checker share one definition of
the tree, so a generated file conforms by construction and costs no tokens. A whole feature is
skill `ddd-ts-kit:use-case`; events between contexts, skill `ddd-ts-kit:integration-event`.

## Procedure

1. **Name from the glossary** of the context's `CONTEXT.md`. A missing term is added in the
   same command with `--term "<Term>=<meaning>"`. Technical words (`Manager`, `Helper`,
   `Data`, `Info`, `Impl`, `Model`, ...) are refused (`language/no-technical-name`):
   find the business word; `--allow-name` only when the word really is the business term.
   A generator that derives its name from another argument (`event-handler`,
   `integration-handler`) takes `--name <Name>` when the design names it otherwise.
   A new aggregate names the fact it is born with: `generate aggregate <ctx> <Name> --birth "<Fact>"`.
   In a context that declares modules of the model (`## Modules` of its `CONTEXT.md`), add
   `--module <module>` to a kind whose usage shows `[--module <module>]`, the module whose
   glossary terms the name uses; the generator refuses without it and lists the modules. The
   other kinds (`test-world`, `route-group`, `guard`, `schema`, `e2e`, ...) write
   what no module holds, in `shared/`, and refuse `--module`; `builder` takes it. A new module: `generate module <ctx> <module> --purpose
   "..."`, after the owner agreed (`docs/concepts/modules.md`).
2. **Run with `--json`** (`--dry-run` first when unsure):
   ```bash
   npx ddd-ts-kit generate <kind> ... --json
   ```
   Exact arguments of every kind: [kinds.md](kinds.md), or `npx ddd-ts-kit generate <kind> --help` for one. A
   worker confined to one context adds `--local-only`: the command refuses, and writes
   nothing, when it would write a shared file.
3. **Open only the `todos` places**, each a `file:line` holding a `TODO(domain)` that states
   the decision expected. Decide, write, delete the marker. A marker you cannot resolve is a
   question for the user, not a guess. `notes` says what the generator could not do.
4. **Replace each `it.todo`** of the generated spec by a real test (skill
   `ddd-ts-kit:testing`).
5. `npx ddd-ts-kit check --changed-since HEAD` and the tests of the context.

## What the generator settles for you

- **Registration.** In the declared style (the default on the containers of the kit) the class carries its
  decorator, and the declarations of its layer (`application/application.declarations.ts`)
  and `<context>.declarations.ts`, which re-exports them, are rewritten; never edit them.
  In the explicit style the binding is added between the markers of `<context>.module.ts`.
- **Dependencies.** A generated class states what it depends on in its constructor, each
  parameter typed by a port, and its decorator lists nothing: the generator reads the
  signature into the generated file of the context. Add a dependency by adding a parameter,
  then `npx ddd-ts-kit docs` (skill `ddd-ts-kit:wiring`).
- **Names.** A generated handler names the aggregate after its concept,
  `const invoice = Invoice.create(..)`, and a generated search names its lines after what it
  searches (`invoice`, `invoices`). Keep the business word when you fill the `TODO(domain)`:
  never `target`, `data` or `item` (`naming/business-name`).
- **Access.** `command` and `query` are refused without `--permission <aggregate>.<action>`
  or `--public`; the permission joins `<context>.permissions.ts`. With roles, add
  `--grant <role>`: the role that holds it, written in the roles of the platform
  (`authz/granted`).
- **Ports.** A port is an abstract class, used as its own injection token: no constant, no
  token file. `port` and `repository` write the fake and the contract suite with it.
- **Dependencies between kinds.** A missing repository or domain event is created; a
  missing aggregate, port, use case or route stops the command with the one to run first.
- **Value objects.** `value-object` writes a class extending `ValueObject` of the kernel, a
  private constructor, a static factory that checks the rules (`create`, renamed after what it
  builds when there are several: `of`, `between`, `closed`) and the type of its props. A value
  is always this class, never a function answering a plain object nor an exported object
  literal (`domain/value-object-class`, under `"stack.values": "classes"`, which `init`
  writes; `npx ddd-ts-kit explain domain/value-object-class` says what it reads): the class
  compares by value (`equals`), checks its invariants once, keeps its operations next to its
  data and is recognised with `instanceof` by a mapper.
- **No role fits?** A type or a function alone is a missing concept, never a new folder: a
  method of the value object, a `domain-service`, a `value-object`, or an abstract service with
  one `domain-service` per variant (`docs/ARCHITECTURE.md`, a concept with no role of its own).
- `route` writes a controller class in its own folder (or a `defineRoute` function under
  `"stack.routes": "functions"`); `controller` always writes the class; `route-group` writes a
  group with its prefix and guards, `guard` a guard of the project with its spec;
  `representation <context> <UseCase> xml,csv` adds what a controller answers in besides JSON,
  `form <context> <UseCase>` the hints of its form.
- `schema` writes one shape of the HTTP contract several routes use, declared once and shared,
  in `presentation/http/shared/` of the context (`shared/presentation/http/shared/` with modules), or in `presentation/` of the shared kernel with
  `schema shared-kernel <Name>`; a command route answers an identifier with `acceptedSchema`.
- **The shared kernel** takes a value at least two contexts use and its refusals, nothing else:
  `value-object shared-kernel <Name> --term "<Term>=<meaning>"`, then `error shared-kernel
  <Refusal> <factory>` (`domain-error` under `classes`). They land at its root, specs beside
  them, and their terms in its own glossary, `<sharedKernelDir>/CONTEXT.md`. Any other kind
  given `shared-kernel` is refused: it belongs to the context that owns it. A worker confined
  to its context does not write there (`--local-only` refuses it): report the need.
- **Documents.** The generated lists of `CONTEXT.md` and the generated documentation are
  refreshed.

Never change the structure the generator produced (constructor visibility, factories,
suffixes, folders, decorators). If it does not fit, the model is probably wrong: go back to
`ddd-ts-kit:glossary` or `ddd-ts-kit:bounded-contexts`.
