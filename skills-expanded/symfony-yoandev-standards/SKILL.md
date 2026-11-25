---
name: symfony-yoandev-standards
description: >-
  Entry point for writing code in a Symfony project: detects the project's versions and
  conventions, states the five rules that apply to everything, and routes to the
  specialised skill for the task at hand. Load this FIRST whenever a request touches a
  Symfony codebase and the right specialised skill is not obvious — a feature described
  in plain language ("let people rate a book", "make a CRUD", "add this to the admin"),
  a vague instruction ("refactor this", "clean this up", "fix this bug", "finish this"),
  a task spanning several areas at once, or the very first change on an unfamiliar
  project. Also load it before starting anything if you are unsure which of
  symfony-yoandev-architecture, symfony-yoandev-http, symfony-yoandev-doctrine, symfony-yoandev-testing,
  symfony-yoandev-security, symfony-yoandev-frontend, symfony-yoandev-async, symfony-yoandev-console,
  symfony-yoandev-performance, symfony-yoandev-quality, symfony-yoandev-local-dev, symfony-yoandev-deployment,
  symfony-yoandev-observability, symfony-yoandev-storage or symfony-yoandev-upgrade applies.
  When the task is plainly inside one of those, load that one directly instead.
---

# Symfony standards — start here

Short on purpose. Detect the project, apply the five rules, load the skill that matches
the work.

## Step 0 — read the project before writing to it

Never assume versions or conventions. Once per session:

```bash
php -v | head -1
php -r '$l=json_decode(file_get_contents("composer.lock"),true);
foreach(array_merge($l["packages"],$l["packages-dev"]??[]) as $p)
  if(preg_match("#^(symfony/(framework-bundle|serializer|form|security-bundle|object-mapper|messenger|scheduler|lock|rate-limiter|asset-mapper|ux-live-component)|doctrine/orm|doctrine/doctrine-fixtures-bundle|phpunit/phpunit|twig/twig)$#",$p["name"]))
    echo str_pad($p["name"],40)." ".$p["version"]."\n";'
ls src/ config/packages/
```

What it tells you:

- **Symfony and PHP versions** → which attributes exist. Every skill states what to write
  instead when one is unavailable; the rule never disappears, only the means change.
- **Which optional components are installed** → what you can lean on without asking.
  Anything missing gets *proposed*, never installed silently.
- **The existing layout of `src/`** → the conventions to follow. If the project already
  groups code by domain, or puts DTOs somewhere else, follow it. Boundaries between
  layers are not negotiable; folder names are.

**`vendor/` outranks everything written in these skills.** Reading the source of an
attribute takes a second and is never wrong; memory and blog posts frequently are.

## The five rules

They apply everywhere, whatever the task.

**1. Write the test first, and watch it fail.** A test that was never red can be green
for the wrong reason — inverted assertion, permissive mock, never executed at all. Where
red-first is impossible, break the code and confirm the test notices.

**2. A controller translates, it does not decide.** HTTP in, service call, response out.
No business rule, no persistence.

**3. No DQL, QueryBuilder or SQL outside a repository.** Queries are named after the
caller's intent, not the mechanism. A service that builds a query cannot be tested
without a database.

**4. DTOs at both edges.** Input DTOs carry the validation; output DTOs carry the
contract. An entity never reaches a template or a JSON response.

**5. Every business rule lives in a service.** Entities hold data and mapping; they hold
no rules. That is the direct consequence of using maker-format entities, and it is
deliberate.

If a change seems too small to deserve a test, it is still covered by rule 1. If a rule
seems wrong for the case at hand, say so and explain why rather than quietly bending it.

## Two tiers: the core, and what the project has to earn

The five rules above are the whole **core**. They remove decisions and add no artefact:
a project that keeps only them still follows this standard. Everything else in the suite
is **on demand** — it adds a file, a tool or a ritual per feature, and it is switched on
by a real need, never pre-emptively. Each skill says which tier it is in, right under
its title.

| Tier | What is in it | Switched on by |
|---|---|---|
| **Core** | The five rules; the layer contract; Input and Output DTOs; `dama/doctrine-test-bundle`; PHPStan and php-cs-fixer; the local dev loop | Nothing — it applies to every Symfony project this suite touches |
| **On demand** | Query-count tests; deptrac; Messenger, Scheduler and prioritised queues; application and HTTP caches; correlation ids, health checks, alert sinks; signed URLs and object storage; Live Components and Mercure | A measured slowness, a second worker, a real queue, a real deploy target, a real upload, a real second developer |

The test for any rule you are about to apply or add: **does it remove a decision, or
does it add an artefact?** The first kind is free and there can be a hundred of them.
The second kind is paid on every feature, and it needs the trigger in the right-hand
column before it is worth paying.

## What the rules do not require

The five rules are read strictly on the boundaries and generously on the ceremony. None
of the following bends a rule; each is the rule applied with judgement:

- **A GET with nothing but route parameters needs no Input DTO.** `#[MapQueryString]`
  is for a query string that must be validated, not for `show(int $id)`.
- **A `SELECT NEW` projection that already matches the contract *is* the Output DTO.**
  The Read layer exists for the case where the query's shape and the API's shape
  differ; when they do not, there is one class, in `src/Dto/Output/`.
- **One Output DTO per shape, not per endpoint.** A list row and a detail view share
  the class when their fields are the same.
- **A business exception exists only for a failure a caller can actually hit.** An
  invalid input is a 422 produced by the DTO's constraints, not an exception class.
- **A class with no rule gets no unit test of its own.** A DTO without normalisation,
  a controller, a command, a getter: the functional or smoke test that proves the wiring
  is the whole coverage they need. Rule 1 is about behaviour, not about files.
- **A read service may hold every read of one resource.** `ShelfReader::shelf()` and
  `ShelfReader::book()` in one class is the intent; one class per query is not.

## Where to go next

| The work is about | Load |
|---|---|
| Where a class goes, layers, DTOs, services, DI, patterns, why a rule exists | `symfony-yoandev-architecture` |
| Writing or fixing tests, fixtures, mocks, the TDD loop | `symfony-yoandev-testing` |
| Controllers, routes, request payloads, JSON responses, forms, Twig pages | `symfony-yoandev-http` |
| Entities, repositories, queries, relations, migrations | `symfony-yoandev-doctrine` |
| Login, permissions, voters, CSRF, tokens, hardening | `symfony-yoandev-security` |
| JavaScript, CSS, Stimulus, Turbo, components, AssetMapper | `symfony-yoandev-frontend` |
| Background work, emails, queues, scheduled jobs | `symfony-yoandev-async` |
| Console commands, imports, cleanup scripts | `symfony-yoandev-console` |
| Something is slow, too many queries, caching | `symfony-yoandev-performance` |
| PHPStan, deptrac, code style, CI pipeline | `symfony-yoandev-quality` |
| Running the project locally, Docker services, the dev server | `symfony-yoandev-local-dev` |
| Shipping to production, migrations at deploy, server settings | `symfony-yoandev-deployment` |
| Logs, alerting, health checks, knowing what production is doing | `symfony-yoandev-observability` |
| Uploaded files: where they go, how they are served, orphans | `symfony-yoandev-storage` |
| Deprecations, updating dependencies, moving to a new Symfony major | `symfony-yoandev-upgrade` |

Most real tasks touch two or three. A feature request typically means
`symfony-yoandev-architecture` to decide where the pieces go, `symfony-yoandev-testing` to start, then
the one matching the surface being built. Load them as you reach them rather than all at
once.

## Before handing back

- [ ] The tests were written first, seen red, and now pass — and you ran them.
- [ ] `vendor/bin/phpunit` result reported as it actually is, failures included.
- [ ] No business rule in a controller, no query outside a repository, no entity crossing
      an edge.
- [ ] Anything you had to decide for the user is stated plainly, not buried.
- [ ] Anything you could not do is named, rather than silently dropped.

The last two matter as much as the code. A change that works but hides a decision is a
change someone will have to reverse-engineer later.
