# AGENTS.md

How I want you to write code. Read this before writing anything.

---

## Talking to Me

- **Brief, and in simple terms.** Short answer, plain words. That's the default for every response, not just the last one.
- **Elaborate only when I ask.** Detailed technical language, full reasoning, alternatives, background, a walkthrough of what you did — I'll ask when I want them.
- **Answer the question, then stop.** No preamble, no recap, no summary of a summary.

---

## Verification Protocol

Before declaring a task done, run the project's own checks in this order. Fix all failures before proceeding to the next step:

1. **Tests** — the whole suite passes.
2. **Types** — no type errors, where the language has a type checker.
3. **Lint and format** — clean.
4. **Build** — a production build succeeds, where the project produces one.

**Find the real commands in the project, don't assume them.** Its `AGENTS.md`, its README, its package scripts, its CI config. A gate the project doesn't have is skipped; a gate it has and you didn't run is not done.

Never skip a step. Never mark a task complete with failing checks. If a check doesn't exist yet, create it. Trust but verify — agent-generated code is not correct by default. Tests prove it.

---

## Agent Behaviour

- **Ask for help when uncertain.** If you don't know the answer, say so. Flag uncertainty. Pretending certainty causes downstream defects.
- **Stop when blocked.** If you've tried two approaches and neither works, stop and explain the problem. Don't keep guessing.
- **Small steps.** One change, verify, then the next. Don't make ten changes and hope they all work.
- **Spec before code.** Write or ask for a specification before implementing. Vague prompts produce vague code.
- **Don't run unbounded.** If a task is growing beyond scope, stop and report. Scope creep is a defect.

---

## Architecture: Ports & Adapters

Default architecture. Every project follows it unless there's a documented reason not to.

```
src/
 domain/     # Pure business logic. No framework imports. No I/O.
 adapters/
  inbound/   # HTTP handlers, CLI commands, event listeners. Thin glue.
  outbound/  # Databases, APIs, file systems, email. Implements port interfaces.
 ports/      # Interfaces the domain depends on. Contracts for swapping implementations.
 config/     # Environment config, wiring, composition root. The only place that knows which adapters are plugged in.
```

1. **Domain has zero imports from outside `domain/`.** No framework, no database driver, no HTTP library. If the domain can't compile without an external package, the boundary is wrong.
2. **Adapters depend on ports, not the other way round.** The domain never knows an adapter exists.
3. **The composition root wires everything.** This is the only file that imports both domain and adapters.
4. **Every side effect goes through a port.** Database writes, API calls, file reads — all of it.
5. **Test the domain with in-memory adapters.** No test should need a database or external service.

---

## Functional Programming over OOP

Prefer FP. Use OOP only when the problem genuinely demands stateful objects with identity (rarely).

- **Pure functions by default.** Same input, same output, no side effects. Push impurity to the boundary.
- **Immutable data.** Never mutate. Return new objects. Spread, don't assign.
- **Composition over inheritance.** No class hierarchies deeper than one level. Prefer `pipe`, `compose`, or function chains.
- **`map`/`filter`/`reduce` over loops.** If you're writing a `for` loop, there's a declarative alternative.
- **Avoid `class` unless there's a compelling reason.** Use `interface` or `type`. Factory functions return plain objects.
- **Railway-oriented error handling.** Return `Result<T, E>` types rather than throwing. Exceptions are for truly exceptional situations.

---

## SOLID — Always SRP

Apply all five, but **Single Responsibility is non-negotiable**.

- **S:** Every module, function, and file has exactly one reason to change. If it does two things, split it.
- **O:** Extend by adding code, not modifying existing code. Composition and dependency injection.
- **L:** Subtypes must be fully substitutable. No overrides that narrow preconditions.
- **I:** Prefer narrow, focused interfaces. No consumer depends on methods it doesn't use.
- **D:** Depend on abstractions (port interfaces), not concretions. Inject dependencies.

---

## Clean Code

- **Functions under 25 lines.** If longer, extract. No exceptions.
- **Files under 250 lines.** If longer, it's doing too much.
- **React components under 100 lines.** Extract hooks and sub-components.
- **Intention-revealing names.** No `data`, `info`, `mgr`, `handler`, `util`, `helper`, `misc`.
- **Comments are a liability.** Default to none. See Comments below.
- **No dead code.** If it's not called, delete it. Version control remembers everything.
- **No speculative abstractions.** No interfaces with one implementation. No factories for a single use case. Add abstraction when you have three concrete examples, not before.
- **No unnecessary dependencies.** If the standard library or ten lines of code can do it, don't install a package.

---

## Comments

Comments are a liability. They rot, they get read instead of the code, and they cost attention. Default to none.

- **If code needs a comment to explain what it does, fix the code.** Rename, extract, restructure. The name is the documentation.
- **Comments say why, never what.** Write one only when the code cannot carry it: a constraint, a trade-off, a non-obvious invariant, a workaround for a known bug (with a link).
- **No narration.** No section headers, no restating the next line, no play-by-play of the obvious.
- **No history.** No "Added …", "Changed for …", "Removed …", authorship or AI-attribution banners. Git is the history.
- **No commented-out code.** Delete it. Version control remembers everything.
- **No TODO without a ticket.** A TODO only goes in if it references the issue that tracks it.
- **Doc comments only at boundaries.** Public APIs and exported types, and only what the signature doesn't already say.
- **A stale comment is a defect.** If a change invalidates a nearby comment, fix or delete the comment in the same change. A wrong comment is worse than none.

---

## Intent & Decisions

Decisions live in separate documents alongside the repo — not in code comments, not in this file. Keep them lean: stale documentation is worse than none.

- **Record decisions, not activity.** Write a record when a choice is non-obvious, constrains future work, or would otherwise be re-litigated: library choices, data models, trade-offs, "never do X". Don't record what the code or its tests already show.
- **One decision, one file.** Short ADR-style records (Context, Decision, Consequences) in `docs/decisions/`. Atomic and append-only: never edit an accepted record — supersede it with a new one that references the old.
- **Scope it.** State which files or areas the decision governs, so agents load only what applies to the code in front of them.
- **Imperative and verifiable.** Prefer MUST / MUST NOT phrasing, and include a check where possible — a grep, a lint rule, a test — so compliance can be proven, not intended.
- **Link, don't duplicate.** Reference records by ID from code, PRs, or this file. The same decision lives in exactly one place; copies drift and contradict.
- **Prune ruthlessly.** When the code a record governs changes, update or supersede the record in the same change. Delete records that no longer change any decision. Review the set periodically for duplicates and contradictions — agents pick arbitrarily between conflicting rules.
- **No journals.** No meeting notes, status reports, or changelogs in the repo. That's what the issue tracker and commit history are for.

---

## Twelve Factor

- **Config in environment.** All environment-specific values come from env vars. Never hard-code config. Never commit secrets.
- **Backing services as attached resources.** Treat Postgres, Redis, S3 as interchangeable resources referenced by URL/env var.
- **Stateless processes.** No in-memory session state. No local disk state that must survive a restart.
- **Dev/prod parity.** Same runtime version, same database engine. Avoid environment-specific code paths.
- **Logs as event streams.** Log to stdout/stderr as structured events. Never write to log files.
- **Disposability.** Processes start fast and shut down gracefully on SIGTERM.
- **Build, release, run separation.** Build artefacts are immutable. Config is injected at runtime.

---

## XP Practices

- **Test-first.** Write the test before the implementation. Red, green, refactor. Every time.
- **Refactor after green.** Once the test passes, clean up. Don't skip this step.
- **Root-cause every bug.** Five Whys. Write a system-level test that would have caught it. Don't patch symptoms.
- **Small commits.** Each commit is one coherent change that builds, passes tests, and makes sense on its own.
- **Small PRs.** Target under 400 lines changed. Split: preparatory refactor first, then the feature.
- **Incremental design.** Design in the light of experience. Defer complexity until it's necessary. The most effective time to invest in design is after the first feature works, not before.
- **Pair on hard things.** If a change touches core domain logic or crosses boundaries, talk it through before coding.

---

## Git

- **Conventional Commits:** `type(scope): description` — e.g. `feat(api): add rate limiting to public endpoints`.
- **Commit body explains why, not what.** The diff shows what.
- **Never bundle unrelated changes.** Formatting, dependency updates, and feature work are separate commits.

---

## Runtime & Tools

- **Follow the project's existing choices.** Runtime, package manager, test runner, build tool — the repository has already decided. Don't introduce a second one alongside it.
- **Prefer the platform to a package.** If the runtime, its standard library, or the language itself ships the capability, use that rather than a dependency.
- **One toolchain over four.** A single tool that runs, tests, and builds beats four that disagree about configuration.
- **Strict typing, escape hatches justified.** Turn strictness on where the language offers it. No `any`, `@ts-ignore`, or equivalent without a comment saying why.
- **Modern module syntax.** ESM in JavaScript and TypeScript. No CommonJS in new code.

Where nothing has been decided yet, my defaults are Bun, TypeScript in strict mode, and ESM.

---

## Testing

- **Domain tests are fast and in-memory.** No database, no HTTP server, no external service.
- **Adapter tests use real implementations** against real services or realistic fakes. Integration tests prove the adapter works.
- **Every change gets a test.** If you changed code, add or update a test. No exceptions.
- **Test behaviour, not implementation.** Test the output, not the internal calls.
- **Coverage is a regression signal.** Don't delete or weaken tests to make them pass. If PR coverage drops, that's a warning.

---

## Error Handling

- **Errors are not optional.** Handle them. Don't swallow them. Don't `console.log` and move on.
- **Use Result types in the domain.** Return `{ ok: true, value }` or `{ ok: false, error }`. Reserve exceptions for truly exceptional situations.
- **Adapters translate external errors into domain errors.** The domain never sees a Postgres error code.
- **If you're unsure, say so.** Don't guess and present it as fact.

---

## Security

- Never commit secrets, keys, tokens, or credentials. Use environment variables.
- Validate all inputs at the boundary. Never trust user input.
- Review new dependencies for vulnerabilities before adding them. Justify every dependency.
- Sanitize output to prevent XSS. Parameterise queries to prevent SQL injection.
- No hardcoded URLs, IPs, or credentials in source code.
- Don't make external calls or exfiltrate data beyond what the task requires.

---

## What not to do

- Don't build features I didn't ask for. No scope creep. No "improvements" that weren't requested.
- Don't add files, layers, wrappers, or configs that aren't needed right now. The default is to add — resist it.
- Don't over-engineer. No framework when a function will do. No architecture for scale that doesn't exist yet.
- Don't suppress errors to make tests pass.
- Don't write comments that describe what you wish the code did instead of what it actually does.
- Don't reach for a library, pattern, or framework just because it's popular. Earn the answer by thinking.

---

## Known Pitfalls

- Deleting or weakening tests to make them pass — worse than no tests.
- Suppressing errors to make the build green — hides real problems.
- Adding dependencies without justification — every dependency is attack surface.
- Refactoring working code without a test covering the behaviour — you can't verify you didn't break it.
- Making changes outside the scope of the task — scope creep compounds.

---

## The filter

If you're ever unsure what to do, run it through this:

1. **Does this actually matter?** If yes, make it as good as it can be. If no, remove it.
2. **Is this honest?** Does the code do what it says? Does the test test what matters? Does the name mean what it says?
3. **Does it feel inevitable?** If you can imagine an equally good alternative, keep working until you can't.

Subtract what doesn't matter. Keep what does. Don't lie about the difference.

---

## Living document

Update this file when you learn something new. Add recurring mistakes to "Known Pitfalls". Add new conventions as rules, not philosophy. Keep every line actionable and verifiable.