---
name: symfony-yoandev-upgrade
description: >-
  Keep a Symfony application alive across versions: the release lifecycle and what "no BC
  break in a minor" really guarantees, triaging deprecations between your own code and
  your dependencies, replaying Flex recipes that drifted since the project was created
  (composer recipes), Rector for mechanical rewrites, and the ordered procedure for a
  major-version jump. Use this skill whenever someone asks to upgrade to Symfony 8 or 7,
  bump the framework, update dependencies, update Doctrine or PHPUnit, or says "our
  Symfony is old", "we are still on 6.4", "what are these deprecation warnings", "can we
  update Doctrine", "this bundle is not compatible", "composer refuses to update", "is it
  safe to upgrade", "how long is this version supported", "how much work is catching up".
  Also use it when a project has been left untouched for a year, when someone wants to
  run Rector, when `composer recipes` reports something outdated, and when a dependency
  turns out to be abandoned or has no version compatible with the target.
---

# Upgrading

> **Tier: on demand** — read when a deprecation, a recipe update or a new major is on the table. The one standing rule is the last-minor-first order.

The recurring cost nobody budgets, and it is invisible until you pay it.

A team that ignores deprecations for two years feels nothing. Then 7.4 → 8.0 becomes a
three-month project instead of an afternoon, because Symfony's contract is that
**everything you must fix is announced on the last minor of the current major**. Skip
the announcements and you meet them all at once, as fatal errors, with no runnable
application in between to tell you which change broke what.

## Where you are

```bash
php bin/console about
```

```
  Version              v8.1.5
  Long-Term Support    No
  End of maintenance   01/2027 (in +154 days)
  End of life          01/2027 (in +154 days)
```

Those dates are compiled into `Symfony\Component\HttpKernel\Kernel` as
`END_OF_MAINTENANCE` and `END_OF_LIFE`, so they are facts about the installed code, not
a claim this skill is making. Read them rather than trusting any table, here included.

On a standard minor the two dates are identical — bug fixes and security fixes stop on
the same day. Only an LTS separates them, and by years.

Then look at what pins you:

```bash
php -r '$j = json_decode(file_get_contents("composer.json"), true); echo $j["extra"]["symfony"]["require"], PHP_EOL;'
```

`extra.symfony.require` is a Flex setting, and it is the reason a `composer update` on a
neglected project reports "nothing to update" while three minors have shipped. Flex
installs a `PackageFilter` that hides every `symfony/*` release outside that constraint
from the resolver. The environment variable `SYMFONY_REQUIRE` overrides it, which is how
you try the next minor without touching `composer.json` (see `references/major-upgrade.md`).

## The lifecycle, and why the last minor matters

- A **minor** every six months. It adds features and it adds *deprecations*, and it
  breaks nothing: code that runs on x.0 runs on x.4.
- A **major** every two years. It removes what was deprecated, and nothing else — that
  is the whole promise.
- The **last minor of a major** (x.4) is an LTS and carries every deprecation notice you
  will need. Running x.4 with zero deprecations is very nearly the definition of being
  ready for (x+1).0.

The practical consequence, and the reason this skill exists: **you never jump from x.2 to
(x+1).0.** You go to x.4 first, get green there, clear the deprecations there — on an
application that still boots and whose tests still run — and only then bump the major.
Each of those steps is reversible on its own. A single leap is not.

"No BC break in a minor" does not mean "nothing changes". A minor can change a recipe,
change a default in a configuration file it no longer owns, or deprecate the option your
`services.yaml` depends on. It means your *code* keeps working, not that your project is
identical to a freshly generated one. That gap is what `composer recipes` measures.

## Deprecations: whose problem is it?

A deprecation you can fix and a deprecation you can only wait for look identical in the
output. Sorting them is the whole job, and PHPUnit 13 does it for you — it classifies
every deprecation by *who called whom*, using `<source>` to decide what counts as your
code:

| Class | Meaning | Yours? |
|---|---|---|
| **self** | Triggered inside a file under `<source>` (or a test) | Yes — delete the deprecated code |
| **direct** | Your code called a third-party API that then deprecated itself | Yes — fix the call site |
| **indirect** | Third-party code called third-party code | No — upgrade the dependency, or wait |

The recipe's `phpunit.dist.xml` ships `ignoreIndirectDeprecations="true"`, so the suite
already fails on the first two categories and stays silent on the third. That is the
right default: it is a gate on work you can actually do. Measured on PHPUnit 13.3.2,
one test each:

| Deprecation | Exit code |
|---|---|
| `trigger_deprecation()` from a class in `src/` (self) | `1` |
| test calls a deprecated vendor method (direct) | `1` |
| vendor calls vendor (indirect) | `0`, not even displayed |
| same, with `ignoreIndirectDeprecations="false"` | `1` |

Two traps in that output. The summary line still reads **`OK, but there were issues!`**
while the exit code is `1` — the human reading the terminal and the CI job disagree, and
CI is right. And `ignoreSuppressionOfDeprecations="true"` is not optional: Symfony's
`trigger_deprecation()` is `@trigger_error(...)`, silenced, so without that attribute
PHPUnit ignores every Symfony deprecation there is.

Flipping `ignoreIndirectDeprecations` to `false` for one run is the upgrade-planning
move, not the daily setting: it shows you which of your dependencies are themselves not
ready for the next major.

Everything else — the three places deprecations surface, static detection, baselines,
and writing your own: `references/deprecations.md`.

## Recipes drift, and almost nobody looks

When the project was created, Flex ran a recipe for each package and wrote
`security.yaml`, `phpunit.dist.xml`, `Dockerfile`, `.env`. Those recipes have been
edited upstream ever since. Your files have not.

```bash
composer recipes           # everything, with a marker on what is outdated
composer recipes -o        # only the outdated ones
```

`-o` prints nothing at all when the project is current, which is the answer you want and
is easy to misread as a broken command. When something has moved:

```
 * symfony/framework-bundle (update available)
```

```bash
composer recipes:update symfony/framework-bundle
```

That command computes the original recipe, the new recipe and your current files, and
applies a three-way patch — **staged in git**, so `git diff --cached` is the review. It
refuses to run on a dirty index, which is the point: the diff must be yours to inspect.
Mechanics, conflicts, the `--force -v` fallback for recipes too old to fetch, and which
files are worth the churn: `references/recipes.md`.

This matters most on a major upgrade, because the new major's recipe is often where the
new configuration lives. Reading that diff is faster than reading the upgrade notes.

## Rector

Rector is in the `jakzal/phpqa` image already (2.6.2 in
`jakzal/phpqa:1.125.1-php8.4-alpine`), with the Symfony, Doctrine and PHPUnit rule sets
bundled. Nothing to add to `composer.json` — same reasoning as every other tool in
`symfony-yoandev-quality`.

```bash
docker run --rm -u $(id -u):$(id -g) -v "$PWD":/project -w /project \
  jakzal/phpqa:1.125.1-php8.4-alpine rector process --dry-run --no-progress-bar
```

`--dry-run` exits `2` when it would change something, which makes it usable as a check
as well as a tool.

**The version-numbered sets are gone.** `SymfonySetList` in rector-symfony now holds only
`COMPOSER_BASED`, `SYMFONY_CODE_QUALITY`, `SYMFONY_CONSTRUCTOR_INJECTION` and
`CONFIGS` — every blog post naming `SymfonySetList::SYMFONY_64` is describing a class
constant that no longer exists. The replacement binds each rule to the version of the
package you actually have installed:

```php
<?php

declare(strict_types=1);

use Rector\Config\RectorConfig;

return RectorConfig::configure()
    ->withPaths([__DIR__.'/src', __DIR__.'/tests'])
    ->withComposerBased(symfony: true, doctrine: true, phpunit: true);
```

Rector is excellent at mechanical rewrites across a whole codebase — annotations to
attributes, renamed classes, changed signatures — and useless at anything needing
judgement. It will happily turn a docblock into an attribute; it will not tell you that
the service should have been a Voter. So: **one concern per run, review the diff, commit
separately.** A single commit mixing three rule sets is unreviewable, and the day one of
them was wrong you cannot revert it alone.

Beware the convenience flags. Adding `->withImportNames()` to the config above took a
one-file diff to four files, rewriting fully-qualified names in tests that had no upgrade
change in them at all. Useful; not something to smuggle into an upgrade commit.

## The major-version jump, in order

1. **Check the dependencies first.** One bundle with no compatible release blocks the
   whole thing, and you want to know that before you start, not after a day of work.
   `composer why-not symfony/framework-bundle 9.0` names every package standing in the way.
2. **Get green on the last minor.** Tests pass, `composer audit` clean, recipes updated.
3. **Clear the deprecations** — self and direct, then re-check with indirect turned on to
   see what your dependencies still owe you.
4. **Bump the constraints**: `extra.symfony.require`, and the `symfony/*` lines in
   `require` / `require-dev` that Flex wrote as `8.1.*`.
5. **Resolve.** `composer update "symfony/*" --with-all-dependencies`, then read what
   Composer refuses.
6. **Run the suite, then the recipes**, then the application.

Detail for every step, including what to do when step 1 says no:
`references/major-upgrade.md`.

## An abandoned or incompatible dependency

`composer audit --abandoned=report` names packages whose authors have said they are done.
An abandoned package is not an emergency — it is a countdown that starts at the next
major. The options, worst to best: pin the major and stop upgrading (you have moved the
problem, not solved it); fork it (you now maintain it); replace it with the framework's
own mechanism, which is where a surprising number of them end up, since Symfony absorbed
a decade of bundles.

Say which one you are choosing and why. "We will deal with it later" is only honest when
someone writes down the date.

## Not this skill

| Question | Skill |
|---|---|
| CI configuration, PHPStan, `phpunit.dist.xml` contents | `symfony-yoandev-quality` |
| The deploy sequence once the upgrade is merged | `symfony-yoandev-deployment` |
| Writing or fixing a migration | `symfony-yoandev-doctrine` |
| Whether a test is worth keeping | `symfony-yoandev-testing` |

## Reference files

| File | When to read it |
|---|---|
| `references/deprecations.md` | A deprecation you cannot place, or planning what to clear before a major |
| `references/recipes.md` | `composer recipes` reports something outdated, or `recipes:update` conflicts |
| `references/major-upgrade.md` | Doing the jump: constraints, blocked dependencies, Rector runbook, rollback |
