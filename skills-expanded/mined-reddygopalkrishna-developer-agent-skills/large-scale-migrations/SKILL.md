---
name: large-scale-migrations
description: Plans and executes large codebase and platform migrations incrementally - JavaScript to TypeScript, AngularJS to React, Java 8 to 21, .NET Framework to modern .NET, monolith to services, on-premises to cloud - using a deliberate strategy, an inventory, codemods, dual-running, a ratcheting progress metric, and decommissioning of the old path. Use when moving a codebase or system from one framework, language, runtime or platform to another, or planning a strangler-fig rewrite. Not for routine version bumps (use dependency-upgrades) or schema changes (use database-migrations).
license: MIT
---

# Large-Scale Migrations

Migrate incrementally, with the system working and shippable at every step. Every migration needs a strategy chosen on purpose, an inventory, a progress metric that only moves forward, a rollback for each step, and an end where the old path is deleted.

## When to use

- Changing language or type system (JS to TS, Python 2 leftovers, Java to Kotlin).
- Changing framework (AngularJS to React or Angular, ASP.NET to ASP.NET Core, a legacy web framework to a modern one).
- Jumping runtime generations (Java 8 to 21, .NET Framework to .NET 8+).
- Changing architecture (monolith to services, services back to a modular monolith).
- Changing platform (on-premises to cloud, VMs to containers, one cloud to another).

Not for: in-place version bumps of one library (dependency-upgrades), database schema changes (database-migrations), or splitting a frontend into independently deployed parts (micro-frontends). For any migration over a few weeks, write a design doc first (design-docs).

## Workflow

1. **Define why and the end state.** The problem being solved, the target, what is out of scope, and the hard deadline driver (end-of-life date, contract, security). If the "why" is weak, say so before starting.
2. **Inventory what must move.** Count the units: files, modules, components, routes, endpoints, jobs, services, consumers. Build a dependency graph (who imports or calls what), e.g. `npx madge --circular src/` or `npx madge --image graph.svg src/` for JS/TS, `jdeps` for Java. Identify leaves (migrate first) and hubs (migrate late, or put behind an interface).
3. **Choose a strategy** from the table below and write down why.
4. **Define a progress metric and automate it.** Examples: % of files in TypeScript, count of `any` and `@ts-ignore`, % of routes served by the new app, % of traffic on the new service. Add a CI check that fails if the legacy count goes **up** (a ratchet).
5. **Build the bridge** so old and new run side by side (interop layer, routing facade, shared auth and config). See the playbooks below.
6. **Pilot one representative slice end to end,** including production deploy. Record every surprise in a migration playbook. Estimate the rest from the pilot's real cost, not from guesses.
7. **Automate the mechanical work with codemods.** They handle the repetitive majority; humans handle the rest. See [references/codemods.md](references/codemods.md).
8. **Migrate in small, releasable batches.** One module, route or endpoint per PR. Merge to the main branch continuously; never run a long-lived migration branch.
9. **Verify equivalence** for each slice: tests, contract tests at the boundary, dual-run or shadow comparison, and metric parity (latency, error rate, business KPIs).
10. **Cut over per slice behind a flag** and ramp (for example 1%, 10%, 50%, 100%), watching metrics, with the flag as the rollback.
11. **Freeze the legacy path:** no new features there. Enforce it with CODEOWNERS, lint rules, or the CI ratchet.
12. **Decommission.** Delete the old code, the bridge, the flags, unused dependencies, old infrastructure and docs. The migration is not done until the old path is gone.

## Choose the strategy

| Strategy | How it works | Use when | Main risk |
|---|---|---|---|
| Big bang | Rewrite, then switch everything at once | Small system, features can freeze, output easy to verify | Everything fails at once; long time with no value delivered |
| Incremental in place | Convert module by module inside one codebase and build | Old and new can coexist in one build (JS/TS, Java versions, project file formats) | Mixed codebase lingers if not driven to 100% |
| Strangler fig | New system beside the old; a facade routes slices to the new one; old shrinks | Old and new cannot share a process (framework or architecture change) | Facade and dual infrastructure cost; data sync |
| Parallel run | Both systems process the same input; compare outputs; old stays source of truth until parity | Correctness-critical logic: billing, pricing, calculations, data pipelines | Doubled compute; must avoid duplicate side effects |
| Branch by abstraction | Put an interface in front of the old component, build the new one behind it, switch, remove the old | Replacing a library or component used in many places in one codebase | Abstraction leaks if designed from the old implementation only |

Default to incremental or strangler fig. Choose big bang only when the system is small and you can prove equivalence quickly.

## Playbooks by migration type

**JavaScript to TypeScript**
- Enable `allowJs` so `.js` and `.ts` coexist; keep `strict: true` for converted files from day one where possible.
- Convert leaves first, then hubs. Rename with `git mv` to keep history.
- Ratchet the counts of `any`, `@ts-ignore` and `@ts-expect-error`; allow `@ts-expect-error` only with a comment.

**AngularJS to React (or Angular)**
- AngularJS long-term support ended on December 31, 2021; treat it as unsupported.
- Strangler inside the app: mount new React components inside AngularJS views through a wrapper directive, migrate leaf components first, then whole routes, then remove the AngularJS bootstrap when the last route moves.
- Expose shared state and services to both sides through one adapter; do not duplicate business logic.
- For a move to modern Angular, Angular's `ngUpgrade` provides the hybrid mode.

**Java 8 to 21**
- Step through LTS releases (8 to 11 to 17 to 21), building and testing at each step.
- Known breakpoints: Java EE modules such as JAXB and JAX-WS were removed from the JDK in 11 (add them as dependencies); internal APIs are strongly encapsulated from 17 (reflective access needs `--add-opens` or a library upgrade); moving to Jakarta EE 9+ or Spring Boot 3 renames `javax.*` to `jakarta.*`.
- Find internal API usage with `jdeps --jdk-internals`. Use OpenRewrite migration recipes (e.g. `org.openrewrite.java.migrate.UpgradeToJava21`) for mechanical changes.

**.NET Framework to modern .NET**
- Convert projects to SDK-style and `packages.config` to `PackageReference` first.
- Move shared libraries to `netstandard2.0` or multi-target so both sides can use them during the transition.
- Replace unsupported technologies: WCF server (CoreWCF or gRPC), .NET Remoting and AppDomains (redesign), Web Forms (rewrite the UI). Move `web.config` settings to `appsettings.json` and the options pattern.
- For ASP.NET to ASP.NET Core, Microsoft documents an incremental approach: a new ASP.NET Core app in front with YARP proxying unmigrated routes to the old app, plus System.Web adapters. Microsoft's migration tooling changes often; check current Microsoft guidance before recommending a specific tool.

**Monolith to services**
- Extract only with a reason: independent scaling, deploy cadence, or team ownership. Consider a modular monolith first.
- Cut by business capability with clear data ownership. Each service owns its tables; no shared writes across the boundary.
- Start with a low-coupling capability. Route through a facade; sync data with events and a transactional outbox, not dual writes.

**On-premises to cloud**
- Decide per application: rehost, replatform, refactor, repurchase, retire, or retain.
- Map dependencies (network calls, shared file systems, batch jobs, hard-coded IPs) and migrate in waves of related systems.
- For data: replicate continuously, verify with counts and checksums, then cut over in a planned window. Lower DNS TTLs well before the cutover. Keep the old environment ready for rollback until the new one has run a full business cycle.

## Progress metrics that work

| Migration | Metric | Ratchet in CI |
|---|---|---|
| JS to TS | `.js` files remaining; `any` and `@ts-ignore` count | Fail if either count increases |
| Framework swap | Components or routes still on the old framework | Fail on new imports of the old framework |
| Runtime upgrade | Modules building and passing tests on the new runtime | Build the new runtime in CI; fail on regressions |
| Monolith to services | % of traffic or endpoints served by the new services | Dashboard plus a lint rule blocking new code in extracted modules |
| On-prem to cloud | Applications cut over per wave; data in sync | Reconciliation job reporting mismatches |

Publish the metric where the team sees it (README badge, dashboard, weekly update). A visible number keeps the migration moving.

## Keeping both paths working

- **Feature flags per slice,** with an instant kill switch back to the old path.
- **Contract tests** at the boundary so old and new agree on inputs and outputs.
- **Backward-compatible interfaces:** the new path accepts everything old callers send.
- **Shadow traffic:** mirror real requests to the new path, discard its responses, and diff them. Only shadow side-effect-free paths, or stub the side effects (writes, emails, payments, webhooks).
- **Dual-run diffs:** log both outputs with a request ID, categorize mismatches, fix until the mismatch rate is below an agreed threshold.

## Safety

Stop and get explicit confirmation before: shifting production traffic, running a data cutover, deleting legacy code, infrastructure or data, or changing DNS. Prefer reviewing a codemod's diff on a sample before applying it across the whole repo.

## Anti-patterns

- **Rewrite against a moving target** — the old system keeps getting features while the new one is built. Freeze or route new work to the new path.
- **Long-lived migration branch** — merge pain grows every day. Merge to main behind flags.
- **No progress metric** — "90% done" for a year. Measure and ratchet.
- **Migrate and redesign at once** — port first, improve after; otherwise you cannot tell migration bugs from design changes.
- **Hardest part first** — pilot on a representative but manageable slice.
- **Shadowing writes** — duplicate charges, emails or records.
- **Unreviewed codemods** — a transform that is 99% right still breaks 1% of thousands of files.
- **Permanent bridges** — shared databases, adapters and flags left behind become the new legacy.

## Done when

- [ ] The progress metric reads 100% for the inventory.
- [ ] The old path has received zero traffic for an agreed period that covers a full business cycle (month-end jobs, seasonal flows).
- [ ] Old code, bridges, flags, unused dependencies, infrastructure and docs are removed.
- [ ] CI blocks reintroducing the old technology.
- [ ] Runbooks, onboarding docs and architecture diagrams describe the new state only.

## References

- [references/codemods.md](references/codemods.md) — read when automating mechanical code changes with jscodeshift, ts-morph, ast-grep, OpenRewrite, LibCST, Roslyn, gofmt, cargo fix or Comby.
