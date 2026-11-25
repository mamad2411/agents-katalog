---
name: symfony-yoandev-quality
description: >-
  Set up and run the quality gate on a Symfony project: PHPStan at level max with the
  Symfony and Doctrine extensions, deptrac to enforce the layer contract, php-cs-fixer
  for style, and a CI pipeline that runs all of it. Ships ready-to-commit configuration
  files and a Make or Castor task entry point, with every tool running from the
  jakzal/phpqa Docker image so it never enters composer.json. Use this skill whenever
  someone asks to set up static analysis, add PHPStan or deptrac or php-cs-fixer,
  configure CI or a GitHub Actions workflow, fix a PHPStan error, add a baseline,
  enforce architecture rules mechanically, add a Makefile or castor.php, check for
  vulnerable dependencies, or asks why the build is failing on style or types. Also use
  it when introducing this standard to an existing codebase that has never had static
  analysis.
---

# Quality gate

> **Tier: core for PHPStan and php-cs-fixer, on demand for deptrac** — the layer contract holds by itself; deptrac verifies it mechanically and is worth adopting when more than one person, or one agent, writes to the codebase. The shipped tasks skip it when `deptrac.yaml` is absent.

Static analysis, code style, layer enforcement and the CI pipeline.

Everything here is about making rules *verifiable*. A standard that lives only in a
document is a standard people follow until they are in a hurry. PHPStan and php-cs-fixer
are the core of that: cheap, silent when nothing is wrong, and they run on every
project. deptrac is the on-demand part — the layer contract in `symfony-yoandev-architecture`
holds by itself, and the tool that checks it mechanically earns its place when more
than one person, or one agent, writes to the codebase. **Adopt it deliberately:** copy
`deptrac.yaml` when you do, and until then the shipped tasks skip it.

## The tools do not go in composer.json

Run every tool from the [`jakzal/phpqa`](https://github.com/jakzal/phpqa) image.

Two reasons, and the honest one first. **One pinned version of every tool, identical on
every machine and in CI**, with the PHPStan extensions already installed, and nothing to
add to the project but a Docker daemon. A tool that runs from the image cannot be at
one version on a laptop and another in the pipeline, which is where "it passes locally"
comes from.

The second reason applies to one tool only, and the suite used to overstate it.
**php-cs-fixer** depends on `symfony/console`, `symfony/finder` and friends, and its
constraint on them can hold the application back on the day of a Symfony upgrade.
**PHPStan and deptrac do not have that problem**: both ship as self-contained,
prefixed phars with no dependency surface, and installing `phpstan/phpstan` through
Composer conflicts with nothing. If a project prefers Composer-managed tools, PHPStan
and deptrac in `require-dev` are fine, and php-cs-fixer through `phive` or
`php-cs-fixer/shim` sidesteps its dependencies. The image is the default here for the
first reason, not the second.

The image already contains `phpstan-symfony`, `phpstan-doctrine`,
`phpstan-strict-rules`, `phpstan-deprecation-rules`, `php-cs-fixer`, `deptrac`,
`composer-require-checker`, `composer-unused` and `infection`. Nothing to install
beyond Docker.

## Setting it up

Copy the files from `assets/` to the project root and commit them. `assets/README.md`
says what each one does and what must be adapted — read it before copying, because
three of the files need project-specific values and will silently do nothing useful if
left as-is.

```
phpstan.dist.neon          level max, Symfony + Doctrine extensions
deptrac.yaml               the layer contract
.php-cs-fixer.dist.php     style
phpunit.dist.xml           the recipe's file plus the two things it is missing
castor.php                 task entry point — the default
alternatives/Makefile      the fallback, only when Castor cannot be installed
github-workflow-ci.yml  →  .github/workflows/ci.yml
```

Then:

```bash
castor qa        # or: make qa
```

**`castor.php` is the entry point; the Makefile is the fallback, and a project commits
one, never both.** They expose the same task names — `qa`, `test`, `stan`,
`stan-baseline`, `cs`, `cs-check`, `deptrac`, `audit`, `lint`, `container-cache`,
`update` — so a runbook written for one stays true for the other. Castor is the default because tasks are
real PHP: typed arguments, conditionals that stay readable past the tenth target. Make is
the answer when Castor genuinely cannot be installed, since it needs nothing beyond
Docker. Committing both leaves a project with two entry points that drift apart, and then
nobody knows which one CI actually runs.

## What each tool is actually for

| Tool | Catches |
|---|---|
| **deptrac** | A `QueryBuilder` that crept into a service, a controller that reaches for the entity manager, a form bound to an entity |
| **PHPStan** | Wrong types, impossible branches, dead code, deprecated APIs, service ids that do not exist |
| **php-cs-fixer** | Everything nobody should ever discuss in review |
| **`composer audit` / `importmap:audit`** | Known vulnerabilities, in PHP **and** in JavaScript |
| **`lint:container`** | A service that cannot be built — before production finds out. It does catch a mistyped `#[Target]`, loudly. What escapes it: a service reached only through a lazy locator (a controller, an `#[AutowireLocator]` collection), which compiles as a `container.error` and throws on first instantiation; `#[Autowire(service: '…')]` typed to an interface the service does not implement, which passes and `TypeError`s at runtime; and `#[WithMonologChannel('typo')]`, which silently invents the channel (`symfony-yoandev-architecture`, `symfony-yoandev-observability`) |
| **`doctrine:schema:validate`** | Mapping that no longer matches the database |

`importmap:audit` is the one people forget. With AssetMapper there is no `npm audit`
in the loop, so nothing else reports a vulnerable JavaScript dependency.

### Tools deliberately not used

The phpqa image ships around a hundred tools. Three of them look like they belong
here and do not.

| Not used | Why |
|---|---|
| **`local-php-security-checker`** | **Archived.** Its own repository points at `composer audit` as the replacement. It is still in the image, so it is still easy to pick by mistake — do not. |
| **`symfony check:security`** | Works, and reads the FriendsOfPHP advisory database rather than Packagist's. But it duplicates `composer audit`, which is built into Composer since 2.4 and needs no extra tooling. One vulnerability check, not two. |
| **PHP_CodeSniffer** | Deliberate: php-cs-fixer is the single style tool. Two formatters that disagree correct each other in a loop, and most of what phpcs would add on top is already covered by PHPStan at level max — by a tool that understands types rather than only syntax. |

If a project already uses phpcs, leave it: migrating a working setup is not worth the
churn. Just do not add it alongside php-cs-fixer.

## PHPStan at level max

Level max, with `phpstan-symfony`, `phpstan-doctrine`, `phpstan-strict-rules` and
`phpstan-deprecation-rules`. It is consistent with the strict typing this standard
already requires everywhere: settling for level 5 while writing fully typed code means
paying the annotation cost without collecting the benefit.

**Warm the container first.** The Symfony extension reads
`var/cache/dev/App_KernelDevDebugContainer.xml` to resolve service ids and route
names. Without it the extension does not fail — it goes quiet, and rules that should
have caught something silently pass. The `stan` task warms the cache for you; if you
run PHPStan by hand, do it yourself.

Common errors and how to fix them properly: `references/phpstan.md`.

## deptrac: the layer contract, enforced (on demand)

The contract is a rule people can follow without a tool. deptrac is for the day that
stops being true — a second developer, an agent working unsupervised, a codebase large
enough that a `QueryBuilder` in a service goes unnoticed in review. Until then, do not
copy `deptrac.yaml`: the `qa` task, the Makefile target and the CI job all skip deptrac
when the file is absent. When you do adopt it, the file declares which layer may depend
on which:

- a **controller** may reach HttpFoundation, services, DTOs, forms, entities (for the
  EntityValueResolver and `#[IsGranted(subject:)]`) and voter constants — never
  Doctrine;
- a **service** may reach repositories, DTOs, entities and exceptions, plus
  `EntityManagerInterface` for the `flush()` it owns — never DBAL, never `QueryBuilder`,
  never `HttpFoundation`;
- a **repository** is the only place allowed to touch Doctrine;
- an **entity** may reach the `#[ORM\…]` mapping attributes, the `Collection` classes
  and `Types` — and nothing else of Doctrine's, and nothing of ours but enums;
- a **message handler** is a controller for messages: services and repositories, since
  a message carries identifiers and the handler reloads.

The shipped file is verified against the deptrac in the `jakzal/phpqa` image (4.7.1 at
the time of writing): clean on a sample of every layer above, exit code 1 the moment a
`QueryBuilder` enters a service. Its collectors are `classNameRegex` with delimited
patterns; the `className` type that older examples use no longer exists.

Run it with `--report-uncovered`, and read the report. An *uncovered* dependency is one
on a class outside every layer — `AbstractController`, `LoggerInterface`, most of
`vendor/` — so the list is long by nature. What matters in it is a class under `src/`:
that is a directory nobody collected, and it is not being checked. **`--fail-on-uncovered`
is not used**, deliberately: it would fail on the first vendor class a controller extends.
Directories the shipped file leaves out on purpose — `src/Command`, `src/EventListener`,
`src/Serializer` — are listed in its header comment.

Adapting the layers to a project that groups code by domain rather than by technical
role: `references/deptrac.md`.

## Adopting this on an existing codebase

Level max on a codebase that has never seen static analysis produces thousands of
errors, and the usual outcome is that someone removes the tool a week later. Freeze
the debt instead:

```bash
castor stan-baseline    # or: make stan-baseline
```

Commit `phpstan-baseline.neon`, uncomment the `includes` line, and hold one rule:
**the baseline may shrink, never grow.** New code is written at level max. A pull
request that adds entries to the baseline is adding debt deliberately, which deserves
a conversation rather than a silent commit.

Same approach for deptrac: run it, read the report as a map of the real architecture,
fix violations domain by domain, then add the task to CI. It is blocking on violations
from day one; there is no baseline to freeze, and it should not need one.

## When a check fails

Fix the cause. The three tempting shortcuts, and why they are worse than the problem:

- **Adding to the PHPStan baseline** to make a new error go away — the baseline is for
  existing debt, not for today's code.
- **`@phpstan-ignore-next-line` without a reason** — if the ignore is genuinely
  right, the reason is worth one line of comment; if it is not worth explaining, it is
  not right.
- **Relaxing a deptrac rule** because a class does not fit — that class is telling you
  it is in the wrong layer. Move it.

The one legitimate case: the tool is wrong. It happens, mostly with generics and with
Doctrine's dynamic returns. Ignore it explicitly, name the reason, and move on.

## CI

The workflow in `assets/` runs the jobs in parallel, so a style error does not hide
behind a five-minute test suite. Everything that can fail before production fails
there: tests, PHPStan, style, layers, linters, audits.

### phpunit.dist.xml is part of this gate

The Symfony recipe generates one, and it is missing two things. `assets/phpunit.dist.xml`
is that file with both added.

**`failOnPhpunitNotice="true"`.** The recipe ships `failOnDeprecation`, `failOnNotice`
and `failOnWarning`, and `failOnNotice` covers *PHP* notices only. The
mock-without-expectations warning PHPUnit 11+ emits is a **PHPUnit** notice, which is a
different category. Measured on PHPUnit 13.3.2, one test creating a mock with no
expectation:

| Flag | Exit code |
|---|---|
| none | `0` |
| `failOnNotice` | `0` |
| `failOnPhpunitNotice` | `1` |
| `failOnAllIssues` | `1` |

Add `failOnPhpunitNotice="true"`, and `displayDetailsOnPhpunitNotices="true"` alongside
it so the report names the test rather than only counting it. Without the first flag the
safety net is decorative. The rule and the reasoning live in `symfony-yoandev-testing`.

**The DAMA extension registration.** Database isolation comes from
`dama/doctrine-test-bundle`, and PHPUnit 10+ registers its extension in the config file:

```xml
<extensions>
    <bootstrap class="DAMA\DoctrineTestBundle\PHPUnit\PHPUnitExtension"/>
</extensions>
```

This is the half of the setup that lives in *this* skill; the other half is a
`['test' => true]` line in `config/bundles.php`. **Either one alone is worse than
neither.** The extension without the bundle finds no static connection to wrap, so every
test commits — and the suite stays green while it fills the database. Nothing in the
PHPUnit output says so, which is why the CI workflow runs
`php bin/console --env=test debug:config dama_doctrine_test` before the suite: it exits
`1` when the bundle is not enabled in the test environment, and `0` when it is.

**Deprecations are not this skill's.** `phpunit.dist.xml` ships `failOnDeprecation` and
`ignoreIndirectDeprecations`, so a deprecation can fail the build here — but triaging one
between your code, a call site and a dependency that is not ready, and deciding what to
clear before a major, is `symfony-yoandev-upgrade`. Same for `phpstan-deprecation-rules` findings.

Two points that decide whether CI is worth anything:

- **The database service must match production.** The workflow ships with PostgreSQL
  16. Testing on SQLite and shipping on PostgreSQL means the differences show up in
  production instead of in CI.
- **Migrations belong in CI too** if the project has any: run them against the
  previous schema. That is what catches the migration that works locally and fails on
  real data.

## Reference files

| File | When to read it |
|---|---|
| `assets/README.md` | Before copying anything — says what to adapt |
| `references/phpstan.md` | A PHPStan error you are about to ignore |
| `references/deptrac.md` | Adapting layers to a project's real structure |
