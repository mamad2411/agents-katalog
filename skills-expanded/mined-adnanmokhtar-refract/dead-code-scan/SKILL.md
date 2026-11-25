---
name: dead-code-scan
description: Find code nothing reaches — unused files and exports, unreachable statements, dead flag branches, commented-out code — each proved by a tool report, a zero-importer search and a boot after removal.
kind: skill
pack: code-quality
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: dead-code-scan

## Premise

Dead code is paid for on every read: it shows up in searches, it is migrated on every upgrade, it
keeps a dependency installed, and a reviewer cannot tell it from the live path next to it. Deleting
live code is paid for once, in production, and costs more. Every dead-code tool reports "unused"
**relative to the entry points it knows about**. A file that a framework loads by convention, a
glob loader reads by pattern, or a container builds from a string token has no importer, and it is
not dead. Measured on a real TypeScript monorepo (2026-10-05): knip, run with no dependencies
installed, could not load 8 configs and listed 3,190 "unused" files. A basename zero-importer
search listed 107. After the entry-point map, **1** was dead.

**Every finding cites the dead item `<file:line>` + why nothing reaches it (the importer search
across every path form, the entry-point map, and the tool lane's verdict) + the removal + the
proof that removing it changes nothing.** A grep hit is never a finding by itself. "No dead code"
is never printed without the class-coverage block (§ Output). Age is not a signal: how long ago a
line changed says nothing about whether anything reaches it.

**The proof is a removal, not a reading.** Delete the item on a scratch branch. Build, boot or
import every entry module (`smoke-verify`, this pack), and run the suite. All green, plus the tool
lane quiet on the item, proves it dead. This is the *Boot* row of
[`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Code quality (Oracle taxonomy), with
variant V86. Removal is **behaviour-preserving**, so the fix goes to `/simplify` (a diff) or
`/optimize` (a whole repo), pinned first. **One exception** is a dead branch that was meant to run:
an `if (false && quotaExceeded)`, or a check after an early `return`. There the intended behaviour
is missing, so it is a correctness claim. Its proof is a test of the intended behaviour, which
fails today. Its fix changes behaviour, so it goes to `/quality-fix`, failing-first.

## The rule

A candidate is dead when all four hold:

1. **Nothing names it.** No import, require, re-export or call in any path form: relative,
   aliased (`@/…`, `tsconfig` `paths`), barrel re-export, dynamic `import()` with a literal, or a
   string in a config, a Dockerfile, a CI job, a `package.json` script or a cron entry.
2. **No entry map reaches it.** Not a manifest entry (`main` / `bin` / `exports`,
   `[project.scripts]`, Cargo `[[bin]]`). Not a framework convention (Next.js `app/`, NestJS
   `*.module.ts`, Django `INSTALLED_APPS`, Rails autoload, Spring `@Component`). Not a pattern
   loader (`import.meta.glob`, `require.context`, an ORM `entities` glob). Not reflection or DI by
   name (§ 65). Not a public API that consumers outside the repo use (§ 64).
3. **The tool lane agrees** — knip, vulture, `deadcode`, `U1000`, the compiler — or the stack has no
   lane, and the run says `NO LANE`, and the candidate stays Investigate.
4. **Removing it changes nothing observable.** Build, boot and suite are green with it gone.

**On a diff** the finding is what the change did: something used at the merge-base is unused at
head, because the diff orphaned it, or the diff adds an unused file or export. Dead code the diff did
not create is **Pre-existing** (`precedents/code-quality.md § 61`). On a whole-repo run every item is
reported in its bucket. A maintainability finding is never critical.

## Boundaries

- **Unused dependencies** (§2) → `@dependency-auditor` (this pack). This skill prints the tool's
  dependency list and hands it over; it never judges a package.
- **Reachable but knowingly suboptimal** code (dated `TODO`s, deprecated-API calls, version lag) →
  `debt-ledger` (this pack). Stale or blanket suppressions → `suppression-scan` (this pack).
- **Duplicated code** → `duplication-scan` (this pack). A copy that is also unreachable is
  reported here once, and duplication-scan cites it.
- **An unreachable branch that hides an intended check** is reported here (§3) and closed by
  `/quality-fix`. A swallowed error that makes a branch unreachable is `error-handling-scan` (this
  pack). One site, two classes: dedupe by `<file:line>`, credit both.
- **Retiring a whole subsystem** that a newer one superseded is `@legacy-modernizer`'s phased plan.
  It is not a delete list.
- Investigate-bucket triage at symbol, file, flag and fixture scale can be handed to
  `@dead-code-finder` (this pack). It reads the same evidence this skill collects.

## Adapt to the codebase — the reachability lanes

Read what the project already runs (grep 0a) before adding flags. A rule at **error** level in CI
owns its class (`precedents/code-quality.md § 2`). The finding, if any, is that the rule is off,
at warn, or not run in CI. Print the lanes you ran in the output header.

| Lane | §1 unused files / exports (whole program) | §3 unreachable / constant condition | Traps |
|---|---|---|---|
| **TS / JS** | knip 6.39.0: `npx --no knip --reporter json` (add `--production` to drop test and dev entries; `--include files,exports,types` to narrow). `ts-prune` is superseded: its last npm release is 0.10.3, from 2022-05 | ESLint `no-unreachable`, `no-constant-condition`, `no-constant-binary-expression`, run with the project's own config plus `--rule` overrides; `tsc --noEmit` with `allowUnreachableCode: false` (TS7027) and `noUnusedLocals` | knip needs the dependencies **installed**: a `Error loading <config>` line means a plugin's entries are missing and every file it would have found looks unused, so that run is `blocked`. Never `--include-entry-exports` on a library. ESLint 10.12 rejects `--no-eslintrc`. Its flat-config replacement `--no-config-lookup` drops the TS parser too, so keep the project config |
| **Python** | vulture 2.16: `vulture <pkg> whitelist.py --min-confidence 80` (`--make-whitelist` records the reviewed false positives) | Ruff `F401` / `F811` / `F841`; `mypy --warn-unreachable` | Framework hooks, pytest fixtures, `__getattr__`, pydantic validators and Celery tasks by name are invisible to vulture |
| **Go** | `deadcode -test ./...` when installed (to enable: `go install golang.org/x/tools/cmd/deadcode@latest`; an audit never fetches it) (reachability from `main`; `-whylive=<func>` explains a survivor); staticcheck `U1000` (golangci `unused`) | the compiler rejects unused imports and locals; staticcheck `SA4*`; `go vet` | `deadcode` needs a `main` package. On a library module, every exported function looks unreachable |
| **JVM** | PMD `UnusedPrivateMethod` / `UnusedPrivateField`; detekt `UnusedPrivateMember` / `UnusedPrivateClass`. No mature whole-program OSS tool: public members stay Investigate | `javac` rejects unreachable statements; detekt `UnreachableCode` | Spring beans, JPA no-arg constructors and Jackson setters are reached by reflection (§ 65) |
| **C#** | IDE0051 (unused private member), IDE0052 (unread private member), IDE0060 (unused parameter) | compiler unreachable-code warning as error | DI registration by assembly scan |
| **PHP** | shipmonk/dead-code-detector 1.4.2 (a PHPStan extension; it finds dead cycles too) | PHPStan `deadCode.unreachable` | Laravel facades and container bindings by string |
| **Ruby** | debride 1.15.2: `debride --rails --whitelist whitelist.txt app lib` | RuboCop `Lint/UnreachableCode`, `Lint/LiteralAsCondition` | `before_action :symbol`, `send`, autoload |
| **Rust** | rustc `dead_code` (crate-private items only; `pub` in a library is never flagged) | rustc `unreachable_code` | cargo-machete 0.9.2 / cargo-udeps 0.1.61 are dependency tools → §2 |

Versions are from the code-quality research catalog (2026-10-05). knip 6.39.0, ts-prune 0.10.3 and
vulture 2.16 were re-read from their registries, and the ESLint 10.12.0 flags were run, on
2026-10-05. A stack whose row names no whole-program tool runs §1 by grep 1 and reads every hit:
its coverage line says `grep only`. A row whose tool errored is `blocked`, never a quiet lane.

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep
**N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.`): `rg` given no path
reads stdin whenever stdin is a pipe, and under an agent's shell that is a silent zero-hit run. Lane
absence comes from the lane count the block prints first, never from a quiet grep. Any `rg` error on
stderr (exit 2) is a failed grep, never zero hits.

```bash
# Not production code: vendored, built, tests, specs, mocks, fixtures, stories, migrations, seeds, generated, catalogs, env files, docs, ai/.
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/*.min.*' -g '!**/*.d.ts'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,stories,migrations,migrate,seeds,generated,__generated__,locales,i18n}/**'
   -g '!**/*.{spec,test,e2e-spec,mock,stories,test-data,fixture,fixtures}.*' -g '!**/{*_test,*_spec,test_*,conftest}.*' -g '!*.{md,mdx,json,lock,snap,map,svg,yml,yaml,sql,html}' -g '!**/.env*' -g '!docs/**' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')   # drops comment-only lines
# Entry conventions: CLI and tooling folders, framework-loaded files, configs. A file matching these is reached by its runner.
ENTRY='(?:^|/)(?:scripts|bin|tools|cli|cmd)/|(?:\.(?:module|controller|resolver|gateway|processor|consumer|subscriber|listener|handler|entity|orm-entity|config|cli|setup)|(?:^|/)(?:main|server|app|manage|wsgi|asgi|settings|urls|admin|apps|conftest|vite-env))\.\w+$|(?:^|/)[\w.-]*config\.\w+$'
# pages/ app/ routes/ are entries ONLY under a file-based router; in a plain React app a page nothing imports is dead
# (counting them as entries hid 8 dead pages on a real monorepo). An index.* is judged by its folder name, which is what imports name.
rg -q --pcre2 '"(?:next|nuxt|@remix-run/[\w-]+|@react-router/dev|@sveltejs/kit|astro|expo-router|@tanstack/router-plugin|gatsby|@solidjs/start)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . && ENTRY="$ENTRY|/(?:pages|app|routes)/"
for t in ts js py go java kotlin cs rust php ruby; do printf '%-7s %s\n' "$t" "$(rg --files -t "$t" "${X[@]}" . | wc -l)"; done   # 0 = lane absent

# 0. Context: 0a the reachability tools and compiler switches already configured; 0b the entry-point map's loaders
#    that reach files by pattern or by name (a file they load has no importer and is not dead). `js.configs.recommended`
#    turns on no-unused-vars and no-unreachable (gate 4 for §1 locals and §3). A project's own dead-export spec is a lane.
rg --files -g '*{every-export-is,unused-export,dead-export,dead-code,unimported}*.{test,spec}.{ts,tsx,js,mjs,py}' -g '*{every-export-is,unused-export,dead-export}*.json' -g '!**/node_modules/**' .
rg -n --pcre2 '"(?:knip|ts-prune|ts-unused-exports|unimported)"\s*:|\b(?:vulture|deadcode|debride|cargo-(?:udeps|machete)|deptry)\b|^\s*-\s*unused\b|\bnoUnused(?:Locals|Parameters)\b|\ballowUnreachableCode\b|\bno-unreachable\b|\bno-constant-condition\b|\bjs\.configs\.recommended\b|\beslint:recommended\b' -g '{package.json,pyproject.toml,setup.cfg,.golangci.y*ml,tsconfig*.json,eslint.config.*,.eslintrc*,Makefile,knip.json*,.knip.json*}' -g '!**/node_modules/**' .
rg -n --pcre2 '\bimport\.meta\.glob(?:Eager)?\s*(?:<[^>\n]*>)?\s*\(|\brequire\.context\(|\bimportlib\.import_module\(|\b__import__\(|\bClass\.forName\(|\bAssembly\.(?:Load\w*|GetTypes)\b|\bINSTALLED_APPS\b|\bautoload(?:_paths)?\b|\bentities\s*:\s*\[\s*["\x27][^"\x27\n]*\*|\bglob(?:Sync)?\(\s*["\x27][^"\x27\n]*\*' "${X[@]}" . | "${NC[@]}"

# 1. TS / JS source files whose basename no import names, grouped by folder; entry conventions dropped. A folder that a
#    0b loader reads is one group, not N findings. (Other stacks: the tool lane, then this question by hand.)
rg -o --no-filename --pcre2 '(?:\bfrom\s+|\bimport\s*\(\s*|\brequire\s*\(\s*|^\s*import\s+|\bexport\s+\*\s+from\s+)["\x27]\K[^"\x27]+' -t ts -t js -g '!**/node_modules/**' -g '!**/dist/**' . | sed -E 's#.*/##; s#\.(ts|tsx|js|jsx|mjs|cjs)$##' | sort -u > "${TMPDIR:-/tmp}/dcs-imported.txt"
rg -o --no-filename --pcre2 '(?:\bfrom\s+|\bimport\s*\(\s*|\brequire\s*\(\s*|^\s*import\s+|\bexport\s+\*\s+from\s+)["\x27]\K[^"\x27]+' -t ts -t js "${X[@]}" . | sed -E 's#.*/##; s#\.(ts|tsx|js|jsx|mjs|cjs)$##' | sort -u > "${TMPDIR:-/tmp}/dcs-imported-prod.txt"   # production importers only
rg --files -t ts -t js "${X[@]}" . | rg -v --pcre2 "$ENTRY" | while IFS= read -r f; do b=${f##*/}; b=${b%.*}; [ "$b" = index ] && { d=${f%/*}; b=${d##*/}; }
  if ! grep -qxF "$b" "${TMPDIR:-/tmp}/dcs-imported.txt"; then echo "$f"; elif ! grep -qxF "$b" "${TMPDIR:-/tmp}/dcs-imported-prod.txt"; then echo "TEST-ONLY $f"; fi; done | sed -E 's#/[^/]+$##' | sort | uniq -c | sort -rn
# 1b. The resolver lane: files no PRODUCTION import resolves to (tsconfig paths, workspace exports and barrels resolved, so a dead
#     file cannot hide behind another file's basename — 2 did on a real monorepo). Tests are not importers here.
RK="$HOME/.claude/scripts/rank-source-files.py"; [ -f "$RK" ] && python3 "$RK" . --format json 2>/dev/null | python3 -c 'import json,re,sys; E=re.compile(sys.argv[1]); N=re.compile(r"(^|/)(test|tests|__tests__|spec|specs|e2e|__mocks__|mocks|fixtures|__fixtures__|testdata|stories|migrations|migrate|seeds|generated|__generated__|locales|i18n|docs|ai)/|\.(spec|test|e2e-spec|mock|stories|test-data|fixtures?|d)\.\w+$"); [print(r["path"]) for r in json.load(sys.stdin)["rows"] if r["importers"]==0 and not E.search(r["path"]) and not N.search(r["path"])]' "$ENTRY" | sed -E 's#/[^/]+$##' | sort | uniq -c | sort -rn

# 3. Unreachable statements: 3a a constant condition; 3b a statement at the same indentation right after return / throw /
#    raise / exit / panic (a continuation, a chain or a template line is indented deeper or starts with . or `, so it is skipped).
rg -n --pcre2 '\b(?:if|while)\s*\(\s*(?:true|false|0|1|null|undefined|!0|!1)\s*\)|^\s*(?:if|elif|while)\s+(?:True|False|0|1|None)\s*:|^\s*if\s+(?:true|false)\s*\{|\bif\s*\(\s*(?:false|true)\s*(?:&&|\|\|)' "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '^([ \t]+)(?:(?:return|throw|raise)\b(?:[^\n]*[^\n({\[,=+\-*/&|?:.\\])?|process\.exit\([^)\n]*\);?|os\.Exit\([^)\n]*\)|panic\([^\n]*\)|sys\.exit\([^)\n]*\))[ \t]*\n(?:[ \t]*(?://|#)[^\n]*\n|[ \t]*\n)*\1(?![ \t.`]|\}|\)|\]|case\b|default\b|else\b|elif\b|except\b|finally\b|catch\b|end\b|rescue\b|ensure\b|//|#|/\*|\*)\K[^\n]+' -t ts -t js -t py -t go -t java -t kotlin -t cs -t php -t ruby "${X[@]}" . | "${NC[@]}"

# 4. Feature-flag reads, any SDK shape (LaunchDarkly, Unleash, GrowthBook, OpenFeature, Flagsmith, Statsig, Flipper,
#    env-var flags): the key list that a flag config and a last-evaluation record settle.
rg -n -o --pcre2 '\b(?:isEnabled|isFeatureEnabled|isOn|isOff|useFlag|useFeature(?:Flag|IsOn|Value)?|boolVariation|variation|getBooleanValue|getFeatureValue|hasFeature|checkGate|feature_enabled|is_enabled|flag_enabled)\s*\(\s*["\x27`][\w.:-]+["\x27`]|\bFlipper\.enabled\?\s*\(\s*:\w+|\b(?:process\.env|import\.meta\.env|os\.environ(?:\.get)?|os\.getenv|ENV|env|config|cfg|settings)\s*[\[.(]\s*["\x27]?(?:FEATURE|FF|FLAG|ENABLE|DISABLE|USE)_\w+' "${X[@]}" . | "${NC[@]}"   # `env.X` / `config.X`: a validated env object

# 5. 5a commented-out code: runs of >= 3 comment lines that parse as statements (count per file, one per run);
#    5b keys in an env template that no source file reads.
rg -U --count-matches --pcre2 '(?:^[ \t]*(?://|#)[ \t]*(?:(?:const|let|var|return|await|import|export|function|class|if|for|while|def|from|elif|try|except|func|public|private)\b[^\n]*|[\w.$\[\]]+\s*(?:\([^\n]*[;{(),:]|=[^=\n][^\n]*)|\}[^\n]*)[ \t]*\n){3,}' "${X[@]}" .
rg -o --no-filename --hidden --pcre2 '^(?:#[ \t]*)?\K[A-Z][A-Z0-9_]*(?==)' -g '**/.env.example' -g '**/.env.sample' -g '!**/node_modules/**' . | sort -u | while IFS= read -r k; do rg -q -w -F "$k" "${X[@]}" . || echo "unreferenced env key: $k"; done   # a commented `# KEY=` is an optional key, still a key
```

A finding is a hit **plus** the importer search in every path form **plus** the entry-point map
**plus** the tool lane's verdict. Three blind spots are structural:

- **Grep 1 matches basenames.** Two files named `utils.ts` hide each other: the one nothing imports
  survives, because the other is imported. Grep 1b resolves real specifiers (tsconfig `paths`,
  workspace `exports`, barrels) and has no such collision; where it is absent, run the lane's tool,
  or search the full specifier (`rg -n "from ['\"].*/<folder>/<name>['\"]" .`).
- **A test is not a user.** A file only tests import is printed `TEST-ONLY` by grep 1 (and is a
  zero-importer row in 1b): the code ships but nothing in production runs it — gate 1 fails for
  any defect in it, and a copy of a server rule kept alive only by its own test is this skill's
  (§ 90), not a duplication finding.
- **Exports are not files.** Grep 1 finds dead files. An unused *export* inside a live file needs
  the tool lane (knip `exports` / `types`, vulture, `U1000`) or `rg -w <symbol> .` read hit by hit.
- **Registration by string is invisible.** A NestJS provider resolved by token, a Celery task
  routed by name, a Spring bean, a Rails callback symbol. Grep the symbol as a string before
  reporting it (§ 65).

**Measured** (2026-10-05). On a real NestJS-on-Fastify + MikroORM + React monorepo (about 14,200
tracked files; the script runs in about 13 s): lanes ts 5,875 and js 171. 0a: 0 (no dead-code tool
configured). 0b: 1 loader, a design-system registry `import.meta.glob('./*.doc.tsx')`. Grep 1: 107
files in 2 folders. 106 sit in the folder that loader reads: one cited line clears them. **1 is
dead**: a DI-token barrel that re-exports tokens nothing imports from it. Grep 3: 2 hits, both false
(a line inside a multi-line SQL template, a line inside a block comment), so 0. Grep 4: 0 (no flag
SDK). Grep 5a: 0 runs; the code-shaped comment lines in that repo quote legacy code as
documentation. Grep 5b: 21 keys, 0 unreferenced. knip 6.39.0 on the same checkout with no
dependencies installed printed 8 config-load errors and listed 3,190 files and 2,199 exports as
unused under `--production`: `blocked`, not a result. Fixtures: grep 1 returns `web-dashboard` 5
files in 3 folders (the fixture has no app entry: Investigate); `slow-marketplace` 1, the mail
receipt template, which nothing imports; `review-decoys` 6, its base and change snapshots; 0b
`slow-marketplace` 2 (a Django `INSTALLED_APPS` list, a NestJS service's MikroORM `entities` glob). Greps 3, 4 and 5 are
0 on every fixture. A seeded sample confirmed that 3a, 3b and 5a fire on TS and Python: an
`if (false)`, a statement after `return`, and a three-line commented-out block. **Re-measured
2026-10-15** on the same monorepo (history re-rooted): grep 1 had grown to 110 files in 3 folders
because `pages/`, `app/` and every `index.*` counted as entries in a React app with no file-based
router; gated on the router dependency, with barrels judged by their folder name and a
production-only importer list, it prints 38 groups — 133 dead files (108 in the glob-loaded docs
folder, 8 page shells, about 20 barrels nothing imports) and 17 `TEST-ONLY` files. Grep 1b (the
resolver lane) 48 production files with no production importer, the DI-token barrel among them;
0a found the project's own export-liveness spec and ledger and `js.configs.recommended`; grep 4
1 (`env.ENABLE_DEV_BOOTSTRAP`, a validated env object, missed before); grep 5b reads 73 keys (20
before: commented `# KEY=` lines are keys), 0 unreferenced.

## The 3,000-hit path

knip and vulture on a large legacy repo list thousands of items. Triage in this order, and record
every step in the coverage block:

1. **Settle the lane first.** If the tool printed a config-load error, it is `blocked`: install
   dependencies or declare the entries (`knip.json` `entry` / `project`), then re-run. Never triage
   a blocked run's list.
2. **Group by folder and by kind** (file, export, type, member):
   `jq -r '.issues[] | select(.files|length>0) | .file' knip.json | sed -E 's#/[^/]+$##' | sort | uniq -c | sort -rn`.
   A folder of 100 hits is usually one missing entry, not 100 dead files.
3. **Match each large group to the entry map**: a loader in 0b, a framework convention, a manifest
   entry. One cited line clears the group.
4. **Rank what is left.** Files before exports. Production folders before tooling. A file the diff
   touched first.
5. **Read the top 30 groups fully** with the read-the-code questions of their §.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues
   them. Never `checked`.

## Scans for

| § | Class | Default severity |
|---|---|---|
| 1 | Unused files and exports | low; Safe-bucket items are Hardening on a whole repo; on a diff, low when the diff orphaned it |
| 2 | Unused dependencies | handed over to `@dependency-auditor` (medium for an unused runtime dependency, per its rules) |
| 3 | Unreachable statements and constant conditions | low; **high** when the unreachable code is a check that was meant to run (a quota, an authorization, a validation), proven by the intended-behaviour test |
| 4 | Dead feature-flag branches | low; medium when the dead branch is the one an incident rollback would rely on |
| 5 | Commented-out code; orphaned env keys, fixtures and config | Hardening by default |

### 1. Unused files and exports

```
BAD:   src/finance/commands/checkout.tokens.ts — a barrel re-exporting DI tokens; nothing imports it
       export function legacyTaxFor(...) — 0 callers since the tax module moved; knip lists it
GOOD:  delete both, after the importer search, the string search and a green boot
       a docs/*.doc.tsx page with no importer, loaded by import.meta.glob('./*.doc.tsx') → not dead
```
**Read the code:** Is the name found in any path form — relative, alias, barrel, dynamic
`import()`, a string in config or CI? Does a 0b loader's pattern match the path? Is it a manifest
entry, a framework convention or a public API (§ 64)? Is it registered by string (§ 65)? Is it
generated (§ 54)? Is a test the only importer? Then the test goes with it, and the production code
is dead. **Finding when** no path, loader, convention or consumer reaches it and the tool lane agrees.
**Proof:** remove it on a scratch branch; the build, the boot or the import of every entry module,
and the suite are green; the tool lane no longer lists it; `git diff --exit-code` after restore.

### 2. Unused dependencies

Not judged here. Print the tool's dependency arrays (knip `dependencies`, `devDependencies` and
`unlisted`; `deptry` DEP002; `cargo machete`) with their count, and hand them to
`@dependency-auditor` (this pack). It owns the lockfile evidence and the removal.

### 3. Unreachable statements and constant conditions

```
BAD:   return result;  audit.log(result);              // never runs
       if (false && order.total > limit) { throw new LimitExceeded(); }   // the limit check was switched off
       while (0) { … } · if False: · if (DEBUG_OLD_FLOW) where the constant is false in every build
GOOD:  the dead line deleted; or, when it was meant to run, the check restored with a test
       default: { const _: never = status; throw new Error(status); }   // exhaustiveness sentinel — keep (§ 28)
```
**Read the code:** Does a linter or compiler at error level in CI already report it (§ 2)? Is the
constant a build flag, `NODE_ENV` or `DEBUG` that differs between builds (§ 40)? Is it an
exhaustiveness sentinel (§ 28)? Did the author mean the unreachable code to run? Name the
behaviour it implements: a check, a log, an audit row. **Finding when** no build makes the branch
live. **Severity rule:** a dead check that was meant to guard money, authorization, quota or
validation is high, and correctness. Anything else is low. **Proof:** for plain dead code, the lint
rule or compiler diagnostic at the line, then the removal proof of §1. For a dead check, a test of
the intended behaviour ("an order over the limit is refused") that fails today. That is a
behaviour-changing fix, routed to `/quality-fix`.

### 4. Dead feature-flag branches

```
BAD:   if (flags.isEnabled('new-checkout')) { … } else { …old flow, 400 lines… }   // on for every cohort since launch
GOOD:  the old branch and the flag deleted in one cleanup change, the flag archived in the platform
```
**Read the code:** What is the flag's value in every environment's config, and in the flag
platform? Does the platform record last evaluation per variant? That record is the evidence; a
git-blame age is a weak fallback. Is the flag stable because the rollout finished (all cohorts on
one value, no rollback in the window, no experiment scheduled), or because nothing has exercised
it yet (unlaunched, not dead)? Do other consumers read it (an admin override, an A/B framework, a
mobile client)? **Finding when** one value holds in every environment through a finished rollout
and no other consumer reads the key. State the window you checked. **Proof:** the config and
platform values cited per environment, then the removal proof of §1 with the flag pinned to its
live value.

### 5. Commented-out code; orphaned env keys, fixtures and config

```
BAD:   // const old = computeLegacy(order);  // if (old > limit) {  //   return old;  // }
       FEATURE_X_URL= in .env.example, read by nothing · test/fixtures/catalog-4mb.json loaded by no spec
GOOD:  deleted; version control keeps the history
```
**Read the code:** Is the block documentation that quotes code (a migration note, a legacy
reference with its source)? That is prose, not dead code. Does the env key feed a Dockerfile, a
compose file or a deploy manifest that grep 5b excludes? Is the fixture loaded by a glob? **Finding
when** nothing reads it. **Proof:** the search output; removal with the suite green. Hardening by
default. A commented-out check in a security, money or authorization path is read as §3's dead
check.

## Proof

The oracles are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Code quality:
*Boot* (Oracle taxonomy), *Metric ratchet* for the diff form ("no new dead code": the tool lane at
the merge-base and at head, nothing new at head), and variant V86. The removal is
behaviour-preserving, so pin first. Commit a characterization test or confirm coverage with
`test-shield` (this pack), delete one kind per commit, then run `smoke-verify` and the suite.
**Never a fix:** commenting the code out, adding a `// knip-ignore` or a whitelist entry with no
reason, or deleting a public API with no in-repo caller without asking (*The fix loop*,
proof-oracles.md § Code quality).

## Output

```
dead-code-scan — lanes: ts (knip 6.39.0 --production, deps installed; eslint no-unreachable via project config; tsc allowUnreachableCode:false); python, go, jvm, c#, php, ruby, rust absent
Context: entry map — package.json main/exports (2), NestJS *.module.ts, import.meta.glob (1 folder), Django none

Findings: 2 · Unconfirmed: 1

1. src/finance/commands/checkout.tokens.ts:1                         [report-with-fix]   low
   §1 unused file — a token barrel; 0 importers in any path form, no loader matches, knip lists it.
   Proof: removed on scratch branch — build, boot (smoke-verify) and suite green.
   Fix (/simplify): delete the file. Bucket: Safe.

2. src/orders/limits.ts:48                                          [report-with-fix]   high
   §3 dead check — `if (false && total > merchant.creditLimit)` has disabled the credit-limit refusal
   since 2026-06. Proof: test/orders/credit-limit.spec.ts — an order over the limit is accepted (fails).
   Fix (/quality-fix): restore the check behind the documented limit; failing-first.

3. FLAG new-checkout (src/checkout/checkout.page.tsx:22)              [report-flagged]    low
   §4 dead flag branch — on in prod and staging config. Unproven link: the platform's last-evaluation
   record for the `off` variant. Settling read: the flag platform's evaluation history for 30 days.

Verification: 140 candidates → 2 findings · 1 unconfirmed · 0 hardening · 0 pre-existing · 137 refuted (106 by one loader line)

Class coverage:
  §1  unused files / exports     checked (knip 107 files / 9 groups → 1 finding; 106 glob-loaded → refuted by the 0b loader) · Live, unreviewed (exports: 4 groups / 61 — continue with knip --include exports on src/legacy)
  §2  unused dependencies        handed over (3 → @dependency-auditor)
  §3  unreachable / constant     checked (2 hits → 1 finding; 1 false: a line in a SQL template)
  §4  dead flag branches         checked (1 key → 1 unconfirmed)
  §5  commented-out / orphaned   checked (0 runs; 21 env keys, 0 unreferenced)
```

`[report-with-fix]`: nothing reaches the item, the entry map is cited, and the removal (or the
intended-behaviour test) was run. `[report-flagged]`: one link is unproven — a loader not yet read,
a flag platform not queried, no harness — named with the settling step. The coverage block lists
**all five** classes on every run: `checked (k hits → m findings)` only when the grep or the tool
ran on a present lane; `grep only` when the stack has no whole-program tool; `NO LANE (<reason>)`
when nothing could decide reachability; `N/A (<reason>)` only when the repo has no such surface;
`blocked (<reason>)` when a grep or a tool failed. A partial review reads
`Live, unreviewed (k groups / n hits)`, never `checked`. Buckets for the human reader: **Safe**
(tool + search + removal proof), **Investigate** (a loader, reflection or public-API question is
open), **Monitor** (flags not yet stable, commented code inside the current release cycle).

## False positives / precedents

The verifier reads [`precedents/code-quality.md`](../../../../snippets/precedents/code-quality.md)
(maintainability § 51–70) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md)
§ 4, § 5 and § 10. The ones this skill meets most:

- **Framework-mandated shapes** (§ 56) and **composition roots** (§ 57): Next.js `page.tsx`,
  NestJS modules, Django `admin.py` and `apps.py`.
- **A public API with no in-repo caller** (§ 64): `package.json#exports`, `__all__`, exported Go
  identifiers in a module others import, `pub` in a library crate. Not dead.
- **Reflection and convention** (§ 65): DI by string (NestJS providers by token, Spring beans),
  pytest fixtures, Celery tasks, Rails callbacks, decorators, `go:linkname`, serde defaults.
- **Generated code** (§ 54): the generator is the fix site, never the output.
- **Exhaustiveness sentinels** (§ 28) and **build-flag constants** (§ 40) are not dead branches.
- **A defect found outside the diff** on a diff run is Pre-existing (§ 49, § 61), never Refuted.

## When to run

- On any diff that deletes or renames an export, a route, a handler, a flag or a module, or that
  moves code between files: the orphan check. This is the `/review-changes` and `/quality-audit`
  dispatch signal.
- On every whole-repo `/quality-audit`, reporting all five classes, and before a `/optimize`
  sweep, to clear the cruft so its diffs stay small.
- After a flag's rollout finishes, and after a major upgrade that retires handlers or error types.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/quality-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the `<file:line>`, the importer search, the entry-point map and the removal proof (or, for a dead check, the intended-behaviour test).
- **Refuse a clean verdict from an unresolved lane.** A tool that printed a config-load error is `blocked`; a stack with no reachability tool is `NO LANE` or `grep only`. Zero findings from a tool that never ran reads exactly like success.
- Halt if the build does not compile: reachability on broken types is unreliable.
- Never delete in this skill. Propose; the removal ships as its own cleanup change through `/simplify`, `/optimize` or `@refactorer`, or through `/quality-fix` for a dead check.
- Ask before removing anything with no in-repo caller that may be public API, a stored-data reader, or a migration.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `/quality-audit` dispatches this skill and folds its coverage block into the class ledger; `/quality-fix` closes §3 dead checks failing-first; `/simplify` and `/optimize` remove the rest.
- `@dead-code-finder` (this pack) reads Investigate-bucket items at symbol, file, flag and fixture scale; `@dependency-auditor` owns §2; `debt-ledger` owns reachable debt; `test-shield` and `smoke-verify` are the pin and the boot this skill's removal proof uses.
- `duplication-scan` (this pack) owns copies; `error-handling-scan` (this pack) owns a branch made unreachable by a swallowed error.

Rule ids, versions and tool traps come from the code-quality research catalog for this pack (2026-10-05).
