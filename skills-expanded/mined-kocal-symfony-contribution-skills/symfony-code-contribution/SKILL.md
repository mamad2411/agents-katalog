---
name: symfony-code-contribution
description: PHP coding standards, naming conventions, deprecations and the backward-compatibility promise for contributing code to Symfony (core, bundles, UX, AI). Use when writing or reviewing PHP for a Symfony pull request.
---

## When to Activate

Use when writing, modifying, or reviewing **PHP** code for a contribution to Symfony core or any Symfony-maintained PHP package (bundles, UX PHP side, AI, Mailer, Messenger, Recipes' PHP, etc.).

Do **not** apply these rules to JavaScript/TypeScript projects such as **Webpack Encore** or the Stimulus/UX frontend assets — follow that project's own `CONTRIBUTING` and standards instead. For documentation (`.rst`) changes, use the `symfony-docs-contribution` skill.

## Core Rules

1. **Run PHP CS Fixer before every commit.** Most style below is auto-enforced by the project's `.php-cs-fixer.dist.php` — never hand-format against it: `php ./vendor/bin/php-cs-fixer fix -v`.
2. **Never break the backward-compatibility promise on a maintenance/minor branch.** Public and protected APIs are frozen: deprecate, never remove or change signatures. Breaking changes land only on the next major branch.
3. **Target the right branch.** Bug fixes -> oldest maintained branch that still has the bug (it merges up automatically). New features and deprecations -> current development branch. Never add a feature on a patch branch.
4. **Ship every deprecation complete, in the same PR:** a `trigger_deprecation()` call, an `@deprecated` PHPDoc tag, a `CHANGELOG.md` entry, and the `UPGRADE-*.md` entries.
5. **Add the MIT license header** at the top of every new PHP file, before the `namespace`.
6. **One class per file. Add tests.** The only exception: private helper classes never instantiated from outside. Do not write PHPDoc that only restates the signature.

## Coding Standards

Based on PSR-12 (code style) and PSR-4 (autoloading). The rules below are what PHP CS Fixer enforces and what reviewers check.

**Formatting**
- One space after each comma.
- One space around binary operators (`==`, `&&`, `||`, ...) **except** concatenation (`.`).
- Unary operators (`!`, `--`, `++`) stick to their variable, no space.
- No spaces around `[` / `]` in array access: `$a[0]`, not `$a [0]`.
- Multi-line arrays: trailing comma after **every** item, including the last.
- Add a `use` statement for every class outside the global namespace.

**Control flow & returns**
- Always brace control-structure bodies, even single statements.
- Blank line before `return`, unless the `return` is alone inside a statement group (e.g. an `if`).
- No `else`/`elseif`/`break` after an `if`/`case` branch that already returns or throws.
- `return null;` when returning null; bare `return;` for void. Do **not** add a `void` return type to test methods.

**Comparisons**
- Identical comparisons (`===` / `!==`) unless you explicitly need type juggling.
- Yoda conditions when comparing a variable to an expression (`==`, `!=`, `===`, `!==`): `if (null === $value)`.

**Class layout**
- Declare inheritance and all implemented interfaces on the same line as the class name.
- Properties before methods. Methods ordered public -> protected -> private, except constructors, `setUp()` and `tearDown()` which come first.
- Use parentheses when instantiating, regardless of argument count: `new Foo()`.
- All method/function arguments on the same line as the name — **except** constructor property promotion, where each parameter goes on its own line with a trailing comma.

**Types**
- In PHPDoc and casts, use `bool`, `int`, `float` (never `boolean`/`Boolean`/`integer`/`double`/`real`).
- In PHPDoc `@param`/`@return` type lists, put `null` **last**: `string|null`.

**PHPDoc**
- Add a block only when it adds information the name/native types/context (e.g. `instanceof` checks) don't already give.
- Only annotations and types from the PHPDoc reference, plus, for static analysis: generics (not `@template-covariant`), conditional return types via `@psalm-return`, class constants, and callable types.
- No one-line PHPDoc blocks, even for a single tag.
- Omit `@return` when the method returns nothing.
- Group annotations: same type together, a single blank line between different types.
- On a new class or a significant change, you may add or expand an `@author` tag with contact info.

**Exception & error messages**
- Build with `sprintf()`, not raw concatenation.
- Capital first letter, trailing period.
- `get_debug_type($x)` for class names in messages (deprecation messages too), not `$x::class`.
- Double quotes around technical elements — `The "foo" option ...` — never backticks.

## Naming

| Element | Case |
|---|---|
| variables, functions, methods, arguments | `camelCase` |
| classes, interfaces, traits, enums (always namespaced) | `UpperCamelCase` |
| enum cases | `UpperCamelCase` |
| constants | `SCREAMING_SNAKE_CASE` |
| config params, route names, Twig vars | `snake_case` |
| PHP files | `UpperCamelCase.php` |
| templates & web assets | `snake_case` |

- Prefix new abstract classes with `Abstract` (except PHPUnit `*TestCase`); some early classes don't, for BC reasons. Suffix `*Interface`, `*Trait`, `*Exception`. No other suffix such as `Class` or `Enum`.
- Service-config attributes prefixed `As` (`#[AsCommand]`, `#[AsEventListener]`); controller-argument attributes prefixed `Map` (`#[MapEntity]`, `#[MapCurrentUser]`).
- Service id = the class FQCN. Several services for one class: FQCN for the main one, lowercase underscored ids for the rest, optionally dot-grouped (`fos_user.something.service_name`). Alias the class FQCN to public services.
- Parameter names lowercase (except `%env(VARIABLE_NAME)%`).
- Command and option names use the English imperative: `run`, `list` (not `runs`, `lists`).

**Method naming for collections.** Use `get` `set` `has` `all` `replace` `remove` `clear` `isEmpty` `add` `register` `count` `keys` only when the class has one clear "main" relation (a `CookieJar` -> its cookies; a `Container` -> its services, not its parameters; a Console `Input` has none). For other relations, suffix with the thing: `getXxx` `setXxx` `replaceXxx` `hasXxx` `getXxxs` (for `all`) `setXxxs` (for `replace`) `removeXxx` `clearXxx` `isEmptyXxx` `addXxx` `registerXxx` `countXxx`; no `keys` equivalent. `setXxx()` may add or replace; `replaceXxx()` must **not** add and throws on an unknown key.

## Deprecations

- PHPDoc tag: `@deprecated since Symfony X.Y, use Bar instead.` — state the version and, whenever possible, the replacement (FQCN if in another namespace).
- Runtime trigger (needs `symfony/deprecation-contracts`):
  ```php
  trigger_deprecation('symfony/package', '7.3', 'The "%s" class is deprecated, use "%s" instead.', Foo::class, Bar::class);
  ```
  For a deprecated class, place the call after the `use` block, before the class definition.
- Document in the **same PR**, all mandatory: `CHANGELOG.md` (component root), `UPGRADE-X.Y.md` (this minor, under the component heading), `UPGRADE-X.0.md` (next major, the consequence: ``* Remove the `Foo` class, use `Bar` instead``).
- Introduce deprecations only on the next minor (exceptionally on an older maintained branch when critical). Never introduce a new class/interface/trait as deprecated or containing deprecated methods, nor a new method as deprecated.
- Remove deprecated code only on the next major, with a `CHANGELOG.md` entry (``* Remove the `Foo` class, use `Bar` instead``) in the same PR.

**`CHANGELOG.md` entries** (new features and deprecations, at the root of the modified component, bridge or bundle):
- Main title `CHANGELOG`; each entry is a list item under a minor-version section (`7.3`); no third-level sections.
- Short, capitalized, no trailing period, imperative verb first: ``* Deprecate the `Foo` class, use `Bar` instead``.
- New entries go on top.
- Never edit the generated `CHANGELOG-*` files at the `symfony/symfony` root.

## Backward Compatibility

Minor releases keep BC; only majors may break it. When unsure, keep the old API and deprecate. Excluded from the promise: `@internal`, `@experimental` and `*\Tests\` code, plus Symfony's security/validation translations. A BC break is tolerated only when required to fix a security issue.

**Never, on public/protected API:** remove, rename or re-namespace a class/interface/trait/method/property/constant; make a class `final` or `abstract`; remove an implemented interface; remove a constructor or destructor; add an argument without a default (constructors included); add an optional argument to a method (use the recipe below); remove an argument other than the last optional one(s); change or remove a default value; add a default to a method argument; add or change an argument type; add, remove or change a return type (removing `void` is allowed); reduce visibility; make a protected member public; flip static/non-static.

**Allowed:** add public/protected methods, properties and constants, an interface, a destructor; add a constructor argument **with a default, at the end** (anywhere after the required ones under `@optional-arguments-by-name`/`@arguments-by-name`); add a default to a constructor argument (not under `@optional-arguments-by-name`); remove a constructor argument's type; rename an argument whose name is not covered (see below); change the parent class if the original stays an ancestor; move a member to a parent class; anything on a class's `private` members.

**Avoid, and document in the UPGRADE file if done:** adding a constructor without mandatory arguments; changing a constant's value. Never change a constant used in YAML/XML config (e.g. event names) or likely to be serialized.

**`final` loosens the rules.** A class/method that is native `final` or plain `@final` (not `@final since Symfony x.y`) also allows: removing, renaming, reducing or publicizing protected members; adding optional arguments and defaults (not under `@optional-arguments-by-name`); adding, removing or changing argument and return types (arguments -> parent type only, returns -> child type only); turning non-static into static.

**Interfaces are strictest:** you may add a parent interface that introduces no new method, move a method to a parent interface, add constants, and change a constant's value (same caveats). Nothing else.

**Traits:** never give one a constructor or destructor. Private members are covered too, since using classes call them: don't remove, rename or change their signature; you may make them public/protected or move them to a used trait.

**Parameter names** are covered only for Attribute-class constructors and methods tagged:
- `@optional-arguments-by-name`: optional params' names covered (not order), required params' order covered (not names).
- `@arguments-by-name`: all names covered, not order.
- `@stable-parameter-names`: names and order covered.

Covered names never change. A tag on a class/interface/trait/enum applies to all its public and protected methods (private ones too in traits). When implementing or overriding a tagged method (constructors excepted), keep the same parameter names.

**Adding a new argument to a public method** (last position only):
1. Comment it out in the signature: `public function say(string $text, /* bool $stripWhitespace = true */): void` (drop `= true` if it will be required).
2. Document it: `@param bool $stripWhitespace`.
3. Read it with `$stripWhitespace = 2 <= \func_num_args() ? func_get_arg(1) : false;` — the fallback keeps the current behavior.
4. If the future default changes behavior, warn:
   ```php
   trigger_deprecation('symfony/COMPONENT', 'X.Y', 'Not passing the "bool $stripWhitespace" argument explicitly is deprecated, its default value will change to X in Z.0.');
   ```
5. If it has no default (required in the next major), warn when absent:
   ```php
   if (\func_num_args() < 2) {
       trigger_deprecation('symfony/COMPONENT', 'X.Y', 'The "%s()" method will have a new "bool $stripWhitespace" argument in version Z.0, not defining it is deprecated.', __METHOD__);

       $stripWhitespace = false;
   } else {
       $stripWhitespace = func_get_arg(1);
   }
   ```
6. Next major (`Z.0`): uncomment the argument, drop the PHPDoc if it adds no description, remove the `func_get_arg()` code and the warning.

**`final` keyword**
- Making a class, method, property or constant `final` is a BC break. So is adding a plain `@final` in a minor.
- Announce it with `@final since Symfony x.y`. In the next major, switch to native `final` or drop the `since Symfony x.y` part.
- `DebugClassLoader` copies the text after `@final` verbatim into the deprecation message (`The "..." class is considered final since Symfony 8.1`): keep it short and accurate.

**Experimental features:** tag classes/methods `@experimental`. One minor version at most (the core team may extend by one); never introduced in an LTS. The `CHANGELOG` must explain every BC-incompatible change and how to upgrade.

## Patch-Version Policy (Maintenance)

Patch releases of a maintained minor ship monthly and accept only tightly-scoped changes. When targeting a maintained branch, fix the bug and nothing else.

**Accepted in a patch:** bug fixes that keep valid tests green, add a covering test, and don't change buggy behavior widely used as a "feature"; support for newer PHP or popular OS versions (Linux, macOS, Windows) — never new PHP *features*; translation updates and additions (always on the oldest maintained branch); external-data refreshes (e.g. ICU); raising a dependency's *minimum* version (not to a new major, never the PHP minimum); tests that raise coverage.

**Generally rejected (case by case, mostly for security fixes):** performance work (unless local to one class, algorithmic, and backed by real-world numbers); coding-standard/refactor churn (only for consistency, non-invasive, no complex merge-up); new classes, public/protected methods or global functions; new config options (never); new deprecations (none once a version is stable); adding/updating annotations (fixing wrong ones may pass).

**Never in a patch — do it on the next minor/major:** new features; security hardening; BC breaks (unless no other way to fix a security issue); support for new external platforms (e.g. Google App Engine); changing exception messages (automated tools rely on them); new Composer deps or support for new majors of existing ones; web-design changes to built-in pages (exceptions, toolbar, profiler).

When docs or PHPDoc disagree with the code, the code is authoritative.

## Workflow

1. Fork the canonical repo (`symfony/symfony` or the target package) to your account; clone; `git remote add upstream <canonical>`.
2. Branch from the correct base (Core Rule 3): `git checkout -b my_change upstream/<branch>`.
3. Write the change **and** tests; keep one topic per PR.
4. If deprecating: add `trigger_deprecation` + `@deprecated` + `CHANGELOG.md` + `UPGRADE-*.md`.
5. `php ./vendor/bin/php-cs-fixer fix -v` and run the component tests (`./phpunit src/Symfony/Component/Xxx`).
6. Commit; push to **your fork**; open the PR against the base branch and fill the PR table (branch, bug fix?, new feature?, deprecations?, BC breaks?, tickets, license).
7. Address CI and review; push follow-ups to the same branch.

## Reference

Canonical sources live in `symfony/symfony-docs` and stay in sync — read the `.rst` when a case is unclear:
- `contributing/code/standards.rst`
- `contributing/code/conventions.rst`
- `contributing/code/bc.rst`
- `contributing/code/maintenance.rst`

## Examples

| Bad | Good |
|---|---|
| `if ($value == null)` | `if (null === $value)` |
| `throw new \RuntimeException('Invalid '.$type.' given')` | `throw new \RuntimeException(sprintf('Invalid "%s" given.', $type))` |
| ``throw new \LogicException('The `debug` option ...')`` | `throw new \LogicException('The "debug" option ...')` |
| `$class = $object::class;` (in a message) | `$class = get_debug_type($object);` |
| removing a public method in 7.x | `@deprecated` it in 7.x, remove in 8.0 |
| adding `bool $strict` as a real param in a minor | comment it out, read via `func_get_arg()`, deprecate if needed |
| adding `@final` to a class in a minor | `@final since Symfony 8.2`, native `final` in 9.0 |
| renaming a parameter of an `@arguments-by-name` method | keep the name; covered names never change |
| `public function all() { ... }` renamed to `getAll()` | keep `all()`; it is the standard main-relation name |
