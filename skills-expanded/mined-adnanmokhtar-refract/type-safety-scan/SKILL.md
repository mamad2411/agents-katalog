---
name: type-safety-scan
description: Find where types lie at runtime — boundary values cast with no validator, non-null assertions on values that can be missing, checker strictness switched off, untyped exported signatures — each proved by a malformed-input test or the checker's own diagnostic.
kind: skill
pack: code-quality
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: type-safety-scan

## Premise

A type is a promise the checker keeps only for values it watched being built. A value that arrives
from outside the program — a request body, a queue message, a cache entry written by last week's
deploy, a `localStorage` key, an environment variable — has whatever shape the sender gave it, and
`JSON.parse(raw) as Order` does not check it: the cast tells the checker to stop asking. The same
goes for `user!.email` on a lookup that can miss, and for a `tsconfig` that sets `strict: false`.
The code compiles, the happy-path tests pass, and the first malformed or missing value crashes deep
inside the call, or worse, is written as if it were valid. "The types say it can't be null" is the
most common wrong dismissal in code review (`precedents/code-quality.md`, rationalizations).

**Every finding cites the escape `<file:line>` + where the value comes from (the boundary or the
lookup) + the entry point that reaches it + what a malformed or missing value does there + the
proof (or the test that would settle it) + the fix.** A grep hit is never a finding by itself, and
"no type escapes" is never printed without the class-coverage block (§ Output).

**Two kinds of proof.** A cast or assertion at a boundary (§1, §2) is a **correctness** claim: the
proof is a **boundary value vector** — the malformed or null value at the real entry point crashes
or writes wrong data before the fix, and is refused with a typed error after
([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Code quality). Strictness switched off
(§3) is a **static fact**: the proof is the **checker diagnostic** from a scratch config that turns
it on. An untyped surface or a double cast (§4) is **maintainability** unless a caller with a wrong
shape is shown: on a diff the proof is the **metric ratchet**, base against head.

## The rule

An escape is a correctness finding when all four hold:

1. **The value can be wrong at run time.** It crosses a boundary the checker did not see built
   (parse, network, queue, storage, environment, cache, another service's version), or comes from a
   lookup that can miss.
2. **Nothing checks it first.** No validator runs on it on every path before the cast or the
   assertion (zod `parse`, a `ValidationPipe`, a pydantic model, serde typed deserialization, Bean
   Validation, a hand-written guard). The validator is read, not assumed (`precedents/code-quality.md § 26`).
3. **A real entry point reaches it.**
4. **A wrong value does damage:** a crash on a request path, a wrong write, a wrong value shown as
   fact, a contract broken downstream.

## Boundaries

- A route with **no** request validation at all, mass assignment and over-posting → security `@api-security-reviewer` (API3), with backend `ai-patterns/request-validation.md` as the method, when those packs are installed. A cast value that reaches an interpreter sink is security's `injection-scan`. This skill reports the crash and corruption a cast causes, not its exploitability.
- Line-level suppressions — `@ts-ignore`, `@ts-expect-error`, `# type: ignore`, `@SuppressWarnings("unchecked")`, `//nolint:forcetypeassert` → `suppression-scan` (this pack). File-wide and project-wide opt-outs are §3 here.
- The cast of a body whose HTTP status was never checked → `error-handling-scan` § 3 owns the unchecked status; this skill owns the unvalidated shape. One site, two classes: dedupe by `<file:line>`, credit both.
- A nullable column the code assumes non-null → database `schema-integrity-scan` owns the constraint, when the database pack is installed; the dereference is §2 here.
- Contract drift between services (a renamed field, an unknown enum value from a newer client) → backend `api-snapshot` and testing `contract-test`; this skill reports the cast that hides the drift.
- A broker message or event parsed and cast (`JSON.parse(msg.value) as OrderEvent`) is §1 here — distributed-systems `event-contract-scan` §2 routes these casts to this skill. That skill owns the contract half when installed: a breaking schema change between releases (§1) and a topic whose schema exists but is read without its schema or registry deserializer, and what a malformed event does to the consumer (§2). One site, two classes: dedupe by `<file:line>`.

## Adapt to the codebase — the checker lanes

Read the checker, its version and its strictness from the config (grep 0a) before judging. A rule
configured at **error** in CI owns its class (`precedents/code-quality.md § 2`); the grep is the
fallback for what it cannot see. Print the lanes you ran in the output header.

| Lane | §1 unchecked cast | §2 non-null assertion | §3 strictness | §4 escape type on the surface | Ratchet |
|---|---|---|---|---|---|
| **TypeScript** — tsc 5.x, typescript-eslint 8.71 | `consistent-type-assertions`, `no-unsafe-assignment` / `-member-access` / `-return` / `-argument` (type-aware) | `no-non-null-assertion`, `no-unnecessary-condition` (type-aware) | `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes` | `no-explicit-any` | `npx --no type-coverage --at-least <base %> --strict --detail --ignore-catch` (2.30.3) |
| **Python** — mypy 2.4.0, pyright 1.1.414, Ruff 0.16.10 | `cast()` by reading; pyright strict `reportUnknown*` | pyright `reportOptionalMemberAccess` / `Subscript` / `Call`; mypy `union-attr` | `mypy --strict`; pyright `typeCheckingMode: "strict"` | Ruff `ANN401` | mypy `warn_unused_ignores` |
| **Go** — golangci-lint v2.14 | `forcetypeassert` | nilaway (module plugin; candidate generator only) | — | by reading | — |
| **JVM** — javac, Error Prone 2.50 + NullAway 0.14.2, detekt 1.23 | `-Xlint:unchecked,rawtypes -Werror`; detekt `UnsafeCast` | NullAway; detekt `UnsafeCallOnNullableType` | NullAway's annotated packages | raw types via `-Xlint:rawtypes` | — |
| **C#** — Roslyn | by reading | nullable warnings CS8600–CS8625 as errors | `<Nullable>enable</Nullable>` + `<WarningsAsErrors>nullable</WarningsAsErrors>` | `dynamic` by reading | — |
| **PHP** — PHPStan 2.2, Psalm 6 | PHPStan level max | `*.nonObject` at level ≥ 8 | `level` in `phpstan.neon` | `mixed` by reading | PHPStan baseline only shrinks |
| **Rust** — clippy | `.unwrap()` / `.expect()` on parsed input | clippy `unwrap_used`, `expect_used` (restriction, opt-in) | — | — | cargo-geiger for `unsafe` |
| **Ruby** — Sorbet | `T.cast`, `T.unsafe` by reading | `T.must` by reading | `# typed:` sigil per file | `T.untyped` in `sig` | — |

Versions are from the code-quality research catalog (2026-10-05). The checker's own run is the best
§2 and §3 lane: `npx --no tsc --noEmit -p <tsconfig>`, `mypy --strict <pkg>`, `npx --no pyright --outputjson`,
`dotnet build -warnaserror` (C# / .NET), `vendor/bin/phpstan analyse -l max <src>`. A lane that errors is
`blocked`, never a quiet lane.

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep
**N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.`): `rg` given no path
reads stdin whenever stdin is a pipe, and under an agent's shell that is a silent zero-hit run. Lane
absence comes from the lane count the block prints first, never from a quiet grep. Any `rg` error on
stderr (exit 2) is a failed grep, never zero hits.

```bash
# Not production code: vendored, built, tests, specs, mocks, fixtures, stories, migrations, seeds, generated, catalogs, docs, ai/.
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/*.min.*' -g '!**/*.d.ts'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,stories,migrations,migrate,seeds,generated,__generated__,locales,i18n}/**'
   -g '!**/*.{spec,test,e2e-spec,mock,stories,test-data,fixture,fixtures}.*' -g '!**/{*_test,*_spec,test_*,conftest}.*' -g '!*.{md,mdx,json,lock,snap,map,svg,yml,yaml,sql,html}' -g '!docs/**' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')   # drops comment-only lines
A='(?!unknown\b|const\b|never\b)'                                         # a cast that is not a widening to unknown / as const
for t in ts js py go java kotlin cs swift rust php ruby; do printf '%-7s %s\n' "$t" "$(rg --files -t "$t" "${X[@]}" . | wc -l)"; done   # 0 = lane absent

# 0. Context: 0a the checker settings that decide §3 (and whether a §2 nullable is even tracked); 0b files that import
#    a runtime validator — the upstream control that clears a §1 cast once it is shown to run first.
rg -n --pcre2 '"(?:strict|strictNullChecks|noImplicitAny|strictPropertyInitialization|noUncheckedIndexedAccess|exactOptionalPropertyTypes|useUnknownInCatchVariables|checkJs)"\s*:\s*(?:true|false)|^\s*(?:strict|ignore_errors|disallow_untyped_defs|disallow_any_\w+|warn_unused_ignores|follow_imports)\s*=|"?typeCheckingMode"?\s*[:=]|^\s*level:\s*\w+|\berrorLevel="\d"|<Nullable>\w+</Nullable>|<WarningsAsErrors>[^<]*nullable' -g '{tsconfig*.json,jsconfig*.json,pyproject.toml,mypy.ini,.mypy.ini,setup.cfg,pyrightconfig.json,phpstan.neon*,psalm.xml*,*.csproj,Directory.Build.props}' -g '!**/node_modules/**' .
rg -c --pcre2 '\bfrom\s+["\x27](?:zod|zod/v4|valibot|yup|joi|ajv|@sinclair/typebox|io-ts|superstruct|class-validator|arktype|typia|@effect/schema)["\x27]|^\s*(?:from|import)\s+(?:pydantic|marshmallow|attrs|cattrs)\b|\bserde::Deserialize\b|\b(?:jakarta|javax)\.validation\b|\bFluentValidation\b|\bgo-playground/validator\b' "${X[@]}" . | rg -c ':'

# 1. A value from outside the program cast to a type with no runtime check: 1a TS (JSON.parse / .json() / request,
#    message, env and storage values cast with `as T` or `<T>`); 1b Python cast() / ** of parsed JSON;
#    1c Go type assertion without `, ok`; 1d Kotlin `as`, Swift `as!` / `try!`; 1e Rust unwrap on parsed input;
#    1f Java / C# casts of a deserializer's result.
rg -n --pcre2 'JSON\.parse\([^\n]*\)\s*as\s+'"$A"'|<'"$A"'[A-Z][\w.]*(?:<[^>\n]*>)?(?:\[\])?>\s*JSON\.parse\(|\.json\(\)\s*\)?\s*as\s+'"$A"'|\.json\(\)\s*as\s+Promise<|\b(?:req|request|ctx\.request)\.(?:body|query|params|headers|cookies)\s+as\s+'"$A"'|\b(?:event|message|msg|job|payload|response|res)\.(?:data|payload|body|detail)\s+as\s+'"$A"'|\bprocess\.env(?:\.\w+|\[[^\]\n]+\])\s+as\s+'"$A"'|\b(?:localStorage|sessionStorage)\.getItem\([^)\n]*\)\s*(?:!|as\s+'"$A"')' -t ts "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bcast\(\s*[^,\n]+,\s*(?:json\.loads|await\s+[\w.]+\.json\(\)|[\w.]+\.json\(\)|request\.(?:json|get_json\(\)|data|form|args)|os\.environ)|(?<![\w.])[A-Z]\w*\(\s*\*\*\s*(?:json\.loads\(|[\w.]*\.json\(\)|request\.(?:json|get_json\(\)))' -t py "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '^(?![^\n]*,\s*ok\s*:?=)(?![^\n]*\bswitch\b)[^\n]*\b\w+(?:\.\w+|\(\)|\[[^\]\n]*\])*\.\((?!type\))\*?[\w.\[\]{}]+\)' -t go "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bas\s+(?!\?)[A-Z][\w.]*(?:<[^>\n]*>)?(?![\w?])' -t kotlin "${X[@]}" . | "${NC[@]}"; rg -n --pcre2 '\bas!|\btry!' -t swift "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '(?:serde_json::from_(?:str|slice|value|reader)\([^\n]*\)|\.parse::<[^>\n]+>\(\)|\.parse\(\))\s*\.(?:unwrap|expect)\(' -t rust "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\(\s*[A-Z][\w.<>?, ]*\)\s*(?:\w*[Mm]apper|gson|om|serializer)\.\w+\(|\breadValue\([^,\n]+,\s*(?:Object|Map|HashMap)\.class\)|\(\s*[A-Z]\w*\s*\)\s*JsonConvert\.DeserializeObject\(|JsonSerializer\.Deserialize<[^>\n]+>\([^)\n]*\)!' -t java -t kotlin -t cs "${X[@]}" . | "${NC[@]}"

# 2. A nullable asserted non-null: TS / C# / Swift postfix `!` before a member, index or call; Kotlin `!!`;
#    Rust unwrap on a lookup; Python `assert x is not None` (removed under -O).
rg -n --pcre2 '[\w$\)\]]!(?=[.\[(])(?!=)' -t ts -t cs -t swift "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '!!(?=[.\[(\s;,)])' -t kotlin "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\.(?:get|first|last|find|next|pop|max|min|get_mut)\b[^;\n]*?\.(?:unwrap|expect)\(' -t rust "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*assert\s+[\w.\[\]"\x27]+\s+is\s+not\s+None\b' -t py "${X[@]}" . | "${NC[@]}"

# 3. The checker switched off: a strict flag set false, a per-file opt-out, a module-wide ignore, a low analysis level.
rg -n --pcre2 '"(?:strict|strictNullChecks|noImplicitAny|strictPropertyInitialization)"\s*:\s*false' -g '{tsconfig*.json,jsconfig*.json}' -g '!**/node_modules/**' .
rg -n --pcre2 '^\s*(?://|/\*+|\*)?\s*@ts-nocheck\b|^\s*#\s*(?:mypy:\s*ignore-errors|pyright:\s*(?:basic|off)\b|type:\s*ignore\s*$)|^\s*#nullable\s+disable\b|^\s*#\s*typed:\s*(?:false|ignore)\b' "${X[@]}" .
rg -n --pcre2 '^\s*ignore_errors\s*=\s*[Tt]rue|"typeCheckingMode"\s*:\s*"(?:off|basic)"|^\s*typeCheckingMode\s*=\s*"(?:off|basic)"|^\s*level:\s*[0-4]\s*$|\berrorLevel="[5-8]"|<Nullable>(?:disable|annotations)</Nullable>' -g '{pyproject.toml,mypy.ini,.mypy.ini,setup.cfg,pyrightconfig.json,phpstan.neon*,psalm.xml*,*.csproj,Directory.Build.props}' -g '!**/node_modules/**' .

# 4. Escapes that switch the checker off for one value or one API: 4a TS double casts (`as unknown as`); 4b an exported /
#    public signature typed with the escape type (TS any, Python Any, Go interface{} / any, C# dynamic, PHP mixed, Java raw types).
rg -n --pcre2 '\bas\s+unknown\s+as\b|<unknown>\s*<[A-Z]' -t ts "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*export\s+(?:default\s+)?(?:declare\s+)?(?:async\s+)?(?:function\b|const\s+\w+\s*(?::[^=\n]*)?=\s*(?:async\s*)?(?:<[^>\n]*>)?\(|class\b|interface\b|type\b)[^\n]*(?::\s*any\b|<any>|\bany\[\]|Promise<any>|Record<string,\s*any>)|^\s*(?:public\s+|protected\s+)?(?:static\s+)?(?:async\s+)?(?!if\b|for\b|while\b|switch\b|catch\b|function\b)[a-z]\w*\s*\([^)\n]*:\s*any\b[^)\n]*\)\s*(?::[^{\n]*)?\{' -t ts "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*(?:async\s+)?def\s+(?!_)\w+\([^)\n]*:\s*Any\b|^\s*(?:async\s+)?def\s+(?!_)\w+\([^\n]*\)\s*->\s*Any\b' -t py "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '^func\s+(?:\([^)]*\)\s*)?[A-Z]\w*(?:\[[^\]]*\])?\([^\n]*\b(?:interface\{\}|any)\b' -t go "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bpublic\b[^\n;=]*\bdynamic\b|\bpublic\s+(?:static\s+)?function\s+\w+\([^)\n]*\bmixed\b|\bpublic\s+(?:static\s+)?function\s+\w+\([^\n]*\)\s*:\s*\??mixed\b|\bpublic\b[^\n;=(]*\b(?:List|Map|Set|Collection|Iterable|Class)\s+\w+\s*[(;=]' -t cs -t php -t java "${X[@]}" . | "${NC[@]}"
```

A finding is a grep hit **plus** a read of where the value came from **plus** the validator search
**plus** the hops to an entry point. Three blind spots are structural:

- **A generic helper hides every cast.** `get<T>(path)` that returns `(await res.json()) as T`
  appears **once** in grep 1a and casts every response the app reads. Treat it as one finding with
  N callers; the fix is a schema parameter at the helper.
- **Implicit `any` needs no cast.** `res.json()` returns `any` in the DOM typings, and assigning it
  to a typed variable compiles with no `as` at all. The type-aware lane (`no-unsafe-assignment`,
  `no-unsafe-return`) sees those; without it, read every function that returns a parsed body.
- **A cache or a queue is a boundary across deploys.** `JSON.parse(await redis.get(k)) as Feed`
  reads what the previous release wrote. Its shape is the old type's until the key expires.

**Measured** (2026-10-05). Fixtures: `slow-marketplace` 1a 10 — cache reads
`JSON.parse(cached) as HomeFeed` (3), Redis pub/sub messages `JSON.parse(message) as PriceEvent`
(2), `(await res.json()) as Recommendation[]` (2), a `localStorage` cart, an inbox client and the
generic `api<T>` helper; 3 → `api/tsconfig.json:9` `strictPropertyInitialization: false`; 4a 1 (a
stream type bridged with `as unknown as`, § 30). `vuln-fullstack` 1a 4 — a webhook body
`JSON.parse(req.rawBody…) as PaymentEvent` (2: a valid signature proves the sender, not the
shape), a stored session, the generic helper; 2 → 4 `req.session!.userId` (read the auth guard
before reporting); 3 and 4a 1 each. `web-dashboard` 1a 2 (its generic API client). `node-api`,
`review-decoys`, `reward-hack` and `half-built-crm` 0 (JavaScript or Python with no casts). On a real
NestJS-on-Fastify + MikroORM + React monorepo (about 14,200 tracked files; the script runs in
about 2 s): 0a 4 (`strict`, `strictNullChecks` and `noImplicitAny` on), validators imported in 334
files; 1a 61 — 35 `JSON.parse … as` (13 of them Redis, session and cache payloads), 21 queue and
event payloads `event.payload as { … }`, 2 storage, 2 request; 2 199 — 98 an index after a bound
(`xs[i]!`, § 27 to verify), 19 on a lookup call (`map.get(k)!`, `config.get('jwt')!`), the rest
optional members; 3 0; 4a 201 (175 in the API, nearly all ORM rows re-typed `r as unknown as Row`,
§ 30); 4b 0 (`no-explicit-any` is at error there, so the tool owns it). **Re-measured 2026-10-15**
on the same monorepo (history re-rooted): 0a 4, validators imported in 439 files; 1a 60 → 56
once `*.test-data.*` builders were excluded; 2 190 (about 110 `xs[i]!` outside the one package with
`noUncheckedIndexedAccess`, optional mapper methods called with `!`); 3 0; 4a 179 (173 in the API, ORM
rows). Go: `quality-mix` 1c 4 —
`raw["id"].(string)` on a decoded `map[string]any` (the commonest decoded-JSON shape; the first cut
of 1c matched only `v.(T)` and `f().(T)` and missed all four, so an index before the assertion is now
part of the receiver). JVM, C#, PHP, Rust and Ruby greps are not measured: no measured repo has that
code.

## The 3,000-hit path

Non-null assertions and double casts run to hundreds on a strict codebase. Triage in this order and
record every step in the coverage block:

1. **Path class.** Scripts, probes and tooling close with **one** cited read showing no deployed
   entry point runs them.
2. **Group.** By (source of the value, target type): every `event.payload as { id }` in consumers of
   one topic is one group; every `xs[i]!` after a length check in one module is one group;
   `rg --json … | jq -r 'select(.type=="match") | "\(.data.path.text):\(.data.line_number)"'`.
3. **Rank by source.** Values from other processes first — webhooks, queues, caches, storage, other
   services — then request fields past the validation layer, then lookups that can miss, then index
   access after a bound.
4. **Read the top 30 groups fully** with the read-the-code questions of their §.
5. **Prefer the checker as the bulk oracle.** Turn the strictness on in a scratch config (§3 proof)
   and run the type-aware lane: every diagnostic is a located candidate, and the count is the size
   of the blind zone.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues
   them. Never `checked`.

## Scans for

Severity assumes a production entry point. Raise one step when money, persisted data or a public
contract is the sink; drop one for admin-only paths. CWE ids are MITRE's, cited under the CWE Terms
of Use.

| § | Class | CWE | Default |
|---|---|---|---|
| 1 | A value from outside the program cast to a type with no runtime check | CWE-704 | high when the value is written, charged or passed on to another system; medium when a wrong shape only crashes the request |
| 2 | A non-null assertion on a value that can be missing | CWE-476 | high on a request path where the miss comes from input, a nullable column or a lookup; medium on configuration read at boot; low after a bound the compiler cannot see |
| 3 | Checker strictness switched off — project-wide, per module or per file | — (a measure) | medium; high when the blind zone covers request handlers and the strict run shows a diagnostic at a reachable line |
| 4 | Escapes on a whole value or API: double casts, `any` / `Any` / `interface{}` / `dynamic` / `mixed` / raw types on an exported signature | — (a measure) | on a diff, medium in production code when the count on changed files grew, low in tests; on a whole repo, Hardening unless a caller with a wrong shape is shown |

### 1. A value from outside the program cast with no runtime check

```
BAD:   const event = JSON.parse(req.rawBody.toString('utf8')) as PaymentEvent;   // signature ok, shape unchecked
       if (cached) return JSON.parse(cached) as HomeFeed;                           // written by the previous release
       return (await res.json()) as T;                                              // every caller trusts the server
       payload = cast(Order, json.loads(body)) · v := msg.(*Order) · serde_json::from_str(s).unwrap()
GOOD:  const event = PaymentEvent.parse(JSON.parse(raw))          // zod: a typed error on a wrong shape
       const feed = HomeFeedSchema.safeParse(JSON.parse(cached)); if (!feed.success) return rebuild();
       get(path, OrderSchema) · Order.model_validate_json(body) · v, ok := msg.(*Order); if !ok { … }
```
**Read the code:** Where was the value built, and by which version of which program? Does a
validator run on it on every path before this line (grep 0b lists the files that import one; read
the call)? What does a wrong shape do here: a `TypeError` three calls deeper, an `undefined`
written to a column, a wrong amount charged, a value forwarded to another service? Is it a generic
helper that every caller inherits? For a cache, what happens when the type changes and old entries
remain? **Finding when** a wrong or missing field reaches a sink with no check, on a path a real
entry point drives. **Proof:** boundary value vector — the entry point fed the null family, a wrong
type, a missing and an extra field, an unknown enum value and truncated JSON; before the fix it
crashes deep or writes the bad value; after, a typed refusal at the boundary.

### 2. A non-null assertion on a value that can be missing

```
BAD:   const user = users.get(id)!;            // a lookup that can miss
       host: config.get<SmtpConfig>('smtp')!.host      // an unset key crashes at first use, not at validation
       order.customer!.billingAddress!.country  // a nullable relation · val!! (Kotlin) · map.get(&k).unwrap() (Rust)
       assert user is not None                  # removed under python -O
GOOD:  const user = users.get(id); if (!user) throw new NotFound('user', id);
       config.getOrThrow('smtp') with the config schema validated at boot
       const country = order.customer?.billingAddress?.country; if (!country) throw new MissingBillingAddress(order.id);
```
**Read the code:** Where does the value come from — a lookup, an optional field, a nullable column,
an unset key, a DOM query, the first element of a list? Is there a check the compiler cannot see in
the same function with no `await` or callback in between (§ 27)? With `noUncheckedIndexedAccess`
on, every `xs[i]!` after a bound is § 27 — verify the bound, then it is Hardening. Is the field
container-injected (§ 27)? **Finding when** a miss can happen on a reachable path and turns into a
crash or a wrong value. **Proof:** make the source miss (the map without the key, the relation
null, the key unset) at the entry point; before the fix a `TypeError` / NPE / panic, after a defined
path (typed error, 404, the spec's default).

### 3. Checker strictness switched off

```
BAD:   "strict": false · "strictNullChecks": false · // @ts-nocheck at the top of a 900-line service
       [[tool.mypy.overrides]] module = "app.billing.*" ignore_errors = true · # pyright: basic
       <Nullable>disable</Nullable> · #nullable disable · phpstan level: 3 · # typed: false
GOOD:  strict on, with a dated per-folder migration plan and a ratchet on the opt-out list
```
A static fact: the switch either is in the config or is not. Its size is what turning it on finds.
**Read the code:** Which files sit in the blind zone? Is the opt-out documented as a migration with
an owner and a date (then Hardening with its count)? `strictPropertyInitialization: false` is
common with decorator-built entities (ORMs, DTOs) and narrower than `strict: false`: report it only
when the strict run shows an uninitialised property read on a reachable path. **Finding when** the
switch is off on production code. **Proof:** the checker diagnostic from a scratch config with the
switch on, filtered to the blind zone — the count, and each diagnostic at a reachable line as a §1 /
§2 candidate of its own.

### 4. Escapes on a whole value or API

```
BAD:   export function toRow(input: any): any · def handle(payload: Any) -> Any · func Decode(v interface{}) interface{}
       r as unknown as PayoutAccount           // the checker is told two unrelated types are the same
       public dynamic Load(...) · public function get(): mixed · public List items()   // raw type
GOOD:  export function toRow(input: OrderInput): OrderRow · a generic with a constraint · a typed row mapper
       a schema-derived type (`z.infer<typeof Order>`) at the edge, real types inside
```
**Read the code:** Who calls the exported API, and can one of them pass a shape that compiles and
fails at run time? Is the double cast bridging two library types that are known to match at run
time (§ 30), or claiming a shape the value never had? **On a diff:** run the metric ratchet on the
changed files; a count that grew is the finding. **On a whole repo:** Hardening with the count,
unless a caller with a wrong shape is shown — then it is a §1 correctness finding with a value
vector. **Proof:** the metric ratchet (base and head escape counts on changed files, or
`type-coverage` base % → head %); for the correctness form, the value vector.

## Proof

The oracles, their per-stack shapes and the variants are in
[`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Code quality (*Boundary value vector*,
*Checker diagnostic*, *Metric ratchet*; variants V80–V82). The fix validates at the boundary with the
project's own validator — a schema at the parse, a guard at the lookup, the strict flag on with the
diagnostics fixed — never a wider type, another cast, or a suppression. It changes behaviour on
purpose (a malformed value is now refused), so it is failing-first, never characterization-first.

## Output

```
type-safety-scan — lanes: ts (tsc 5.7 strict on; typescript-eslint 8.69 recommended, no type-aware rules); python, go, jvm, c#, php, rust, ruby absent
Context: strict, strictNullChecks, noImplicitAny on (tsconfig.base.json) · validators imported in 120 files (zod, class-validator)

Findings: 2 · Unconfirmed: 1

1. src/invoices/consumers/invoice-paid.consumer.ts:64           [report-with-fix]   high
   §1 unchecked cast — `event.payload as { invoiceId: string; amount: number }` in the consumer;
   the producer moved to `amountMinor` in a later release, and queued v1 events still drain.
   Proof: test/invoices/invoice-paid.vectors.spec.ts — a payload without `amount` books a NaN
   payment (fails). Fix: InvoicePaidSchema.parse(event.payload) and dead-letter on failure. CWE-704

2. src/catalog/menu.service.ts:52                               [report-with-fix]   medium
   §1 unchecked cast — `JSON.parse(cached) as MenuTree` reads entries written by the previous
   release (TTL 24 h). Proof: a cached v1 entry without `sections` → TypeError in render (fails).
   Fix: safeParse; rebuild on mismatch; version the key. CWE-704

3. src/mail/mailer.factory.ts:12                                [report-flagged]    medium
   §2 non-null — config.get('smtp')!.host. Unproven link: whether the config schema validated
   at boot requires `smtp`. Settling test: boot with SMTP_HOST unset → expected a schema error
   naming the key, not a TypeError.

Verification: 27 candidates → 2 findings · 1 unconfirmed · 19 hardening · 0 pre-existing · 5 refuted

Class coverage:
  §1  unchecked boundary cast     checked (61 hits / 14 groups → 2 findings)
  §2  non-null assertion          checked (199 hits / 23 groups → 1 unconfirmed; 98 index-after-bound verified as § 27) · Live, unreviewed (6 groups / 31 hits — continue with grep 2 on web/src/features)
  §3  strictness off              checked (0 hits; tsc strict on)
  §4  escapes on value / API      checked (201 double casts → Hardening as erosion; whole-repo run, no wrong-shape caller shown; 0 exported any — no-explicit-any at error)
```

`[report-with-fix]`: the source of the value is named, no validator runs first, the vector test
failed, and the fix validates at the boundary. `[report-flagged]`: one link is unproven — a
validator not yet read, a producer version unknown, no harness — named with the settling test. The
coverage block lists **all four** classes on every run: `checked (k hits → m findings)` only when the
grep ran on a present lane; `N/A (<reason>)` only when the repo has no such surface;
`blocked (<reason>)` when a grep or the checker failed. A partial review reads
`Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/code-quality.md`](../../../../snippets/precedents/code-quality.md)
(types and nulls are § 26–32; version precedents § 71–83) and
[`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10. The ones this
skill meets most:

- **A cast after a validator** (§ 26): cite the validator call and show every path runs it.
- **An assertion after a check the compiler cannot see** (§ 27) — most `xs[i]!` after a length check.
- **Exhaustiveness sentinels** (`assertNever`, `const _: never`) are controls (§ 28); **escapes in tests, mocks and stories** are Advisory (§ 29); **internal re-typing** that never crosses a boundary is erosion, not correctness (§ 30).
- **An untyped third-party library** shimmed with `declare module` or `# type: ignore[import-untyped]` is not the project's escape (§ 32).
- **A signed webhook is still a boundary.** A valid signature proves who sent the body, not that its shape matches the type.

## When to run

- On any diff that adds or changes a parse (`JSON.parse`, `.json()`, `json.loads`, a deserializer),
  a queue or webhook consumer, a cache read, a storage read, a non-null assertion, a type assertion,
  or a checker config (`tsconfig*.json`, `[tool.mypy]`, `pyrightconfig.json`, `<Nullable>`,
  `phpstan.neon`) — the `/review-changes` and `/quality-audit` dispatch signal.
- On every whole-repo `/quality-audit`, reporting all four classes.
- When a production error is a `TypeError`, NPE or panic on a field "the types said" was present.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/quality-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the escape `<file:line>`, the source of the value, the validator search, the entry point and the fix.
- Do not report a grep hit as a finding, and do not dismiss a group without reading where its value comes from.
- Do not propose a wider type, another cast, `any`, `!`, or a suppression as the fix. The fix checks the value where it enters, or handles the miss.
- Do not print "no type escapes" without the class-coverage block. A class whose grep or checker did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `/quality-audit` dispatches this skill and folds its coverage block into the class ledger; `/quality-fix` closes the findings failing-first and re-runs this detector on the patched line.
- `error-handling-scan` (this pack) owns the unchecked HTTP status in front of a cast; `suppression-scan` (this pack) owns line-level type-checker suppressions.
- `rules/quality-principles.md` and `rules/engineering-principles.md` (this pack) state the rule "no `any` at boundaries"; this skill is its executor.
- Security `@api-security-reviewer` (API3) and backend `ai-patterns/request-validation.md` own request validation and over-posting, when installed; database `schema-integrity-scan` owns nullable-column constraints.

Rule ids and versions come from the code-quality research catalog for this pack (2026-10-05).
