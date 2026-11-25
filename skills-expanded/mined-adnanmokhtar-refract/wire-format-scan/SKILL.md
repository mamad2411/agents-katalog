---
name: wire-format-scan
description: "Wire format: Decimal and 64-bit numbers, serializer reshaping, float money in carriers, time binding and offsets — read-only."
kind: skill
pack: backend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: wire-format-scan

## Premise

The value in the database is right and the value in the domain is right; the bytes on the wire are not. A `Decimal("10.10")` leaves as `10.1` because one serializer setting says so; `1000.00` leaves as `1E+3`; an id above 2^53 arrives in a JavaScript client one digit off; a JavaScript `BigInt` answers 500; a Fastify response schema turns `12.7` into `12` and `"no"` into `true` with a 200; a job payload carries `float(amount)` because `json.dumps` refuses a `Decimal`; a request binder accepts `2026-03-29T10:00` with no zone and stores a different instant under each server `TZ`; a serializer rewrites `+03:00` to `Z` or cuts microseconds off a cursor. Nothing fails loudly — only a round trip of the **rendered bytes** shows it. This skill finds the settings, binder field types, serializers and carrier calls that change a value between the domain and the wire, and proves each with the seeded value that came out different. Read-only: it never edits code.

Backend owns **the wiring between the HTTP framework and the domain** (eval § 4.1); here that is framework settings, the binder's field types, the rendered body and payload carriers. **Arithmetic and the clock in code** — minor units, a sum across currencies, the rounding point, a hand parser, `now()` — are code-quality's. It owns `/backend-audit`'s wire rows (`wire-format-scan §1–§8`); `@api-reviewer` (this pack) judges them in refute mode.

**Every finding cites the setting, field or call `<file:line>` + the wiring row it depends on (the serializer and its options, the process zone) + the seeded value and what came out + the oracle that showed it, or the request that would settle it + the fix in the project's own primitive** (its mapper, its money type, its date helper). A grep hit is a candidate. "The wire format looks fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/backend.md`](../../../../snippets/precedents/backend.md). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Backend, V338, V339, V347–V349 and V357.

## The rule

A candidate is a finding when all four hold — `precedents/backend.md` § Reading the seven gates for backend, applied to the wire.

1. **Part A holds: this is the serializer that ships, on a mounted route or a registered producer.** The serializer comes from the bootstrap: the global interceptor (`ClassSerializerInterceptor`), the Fastify instance and its route schemas, `REST_FRAMEWORK`, the `ObjectMapper` bean (and every hand-built `new ObjectMapper()` beside it), `JsonSerializerOptions`, the tRPC `transformer`. A carrier is the producer wrapper the app registers, not a script.
2. **Part B holds at the installed version.** Serializer, ORM, driver and date-library versions come from the lockfile (F1); without one they are `UNREAD` and every version-gated row is Unconfirmed (V357). Defaults moved across majors here: pydantic v1 → v2 (Decimal float → string), Jackson 2 → 3, Fastify 4 → 5, the ORM's bigint mapping.
3. **Nothing already controls it**, across files: a mapper that converts every read of a `bigint` column with a pinned-set test (B-D5); dates kept as strings with a strict validator (B-D12); a documented `number` contract the client parses with a decimal library (B-R2); amounts already in integer minor units; a documented UTC normalisation; banker's rounding chosen in the spec (B-R4).
4. **The oracle fired, or the fact is two-ended.** V339/V347–V349 through the real bootstrap (tier U) shows the value changed, or the static fact cites both ends (tier S: `COERCE_DECIMAL_TO_STRING = False` and the `DecimalField` it renders; the `bigint` column typed `number` and the response that reads it raw). Without one, the row is `[report-flagged]` / Unconfirmed with the seed written out (P2).

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration (`precedents/backend.md` § Owned elsewhere).
- **Arithmetic, minor units, mixed currencies, the rounding point, hand parsers and the clock in code** (`amount * 100`, `toFixed(2)` round-tripped, `new Date(req.body.x)`, `Time.now`) → code-quality `correctness-smell-scan` §4 and §6, when the code-quality pack is installed. **The rule is the expression's location:** inside a carrier call or a serializer setting → here; elsewhere → code-quality. Without the pack the hits are listed tagged `money arithmetic (owner pack code-quality not installed)`, never graded here.
- **Column types** — money in a float column, an instant stored as wall time, a 32-bit key — → database `schema-integrity-scan` §4, §5 and §7, when the database pack is installed; without it they are listed tagged `column type (owner pack database not installed)`. This skill owns what the column's value becomes on the wire.
- **A sensitive field over-returned** (no `response_model`, no `.output()`, a `passwordHash` in the body) → security `data-exposure-scan` §4, when the security pack is installed (P3). §3 here owns a field **dropped** or a value **changed**; without the pack the over-return is listed tagged `over-returning (owner pack security not installed)`.
- **Cross-service event schemas and their evolution** → distributed-systems `event-contract-scan`; redelivery and consumer idempotency → `messaging-scan`, when that pack is installed. §5 here owns the float amount inside one payload; without the pack the schema rows are listed tagged `event contract (owner pack distributed-systems not installed)`.
- Same pack: **spec versus runtime drift** → `http-contract-scan` §10 (both cite V338; the serializer line is §3 here, the spec line is theirs); **request-side number coercion** (`3.7` → 3, `"12"` → 12) → `validation-boundary-scan` §4; **`@Type(() => Date)`** is graded here (§6) and `validation-boundary-scan` §3 lists the same line as corroboration; **a job payload's drift across deploys** and **a schedule's zone** → `job-lifecycle-scan` §3 and §6; **cursor ordering and tiebreaks** → `http-contract-scan` §7 (§7 here owns the precision the cursor encoder keeps).

## Adapt to the codebase — the lanes

Read the serializer **with its version** (F1) and the wiring (grep 0) first. `[V]` ran, `[K]`/`[K?]` docs or secondary (§ Sources); a `[K?]` default makes its verdict Unconfirmed until the oracle runs.

| Lane | Where the wire format is set | Defaults that decide verdicts | Decoy shape |
|---|---|---|---|
| **NestJS** (either adapter) | `ClassSerializerInterceptor`, `@SerializeOptions`, `@Exclude`/`@Expose`, the mapper that builds the response DTO | no response schema unless the app adds one, so `JSON.stringify`: `Date` → UTC ISO with ms, `BigInt` → 500 [V Fastify 5.12.7]; `excludeExtraneousValues: true` drops every undecorated field [K] | a mapper that converts `bigint` reads with `Number()` under a pinned-set test (B-D5) |
| **Fastify** (plain) | route `schema.response`, `setSerializerCompiler` | response schema: `integer` 12.7 → `12`, `boolean` `"no"` → `true`, `string` `null` → `""`, object → `"[object Object]"`, unlisted fields dropped, a missing required field or `"7abc"` for an integer → 500 [V 5.12.7] | a schema that hides internals on purpose (B-A12) |
| **Express / Koa** | `res.json`, `app.set('json replacer')` | `JSON.stringify`: `BigInt` throws; `JSON.parse` turns `9007199254740993` into `…992` on the client [V Node 22.14] | — |
| **tRPC** | `.output(...)`, the `transformer` | no `.output()` → every field returned (a `secret` leaked) [V 11.19.0]; with `.output()` a wrong value → 500 [V]; `superjson` carries `BigInt`/`Date` [K] | `.output()` on every procedure |
| **Prisma / MikroORM / TypeORM / Drizzle on `pg`** | the column mapping and the TS type it is read into | node-postgres returns `int8` and `numeric` as **strings** [K]; the ORM's bigint mode is version- and option-dependent [K?]; Prisma `Decimal` is decimal.js, whose `toJSON` drops trailing zeros (`"10.1"`) [V decimal.js 10.6.0]; Drizzle `bigint({ mode: 'number' })` loses past 2^53 [K] | a `numeric` rate typed `string`; a measure in `double` |
| **Django REST Framework** | `REST_FRAMEWORK`, serializer fields, `DjangoJSONEncoder` | `COERCE_DECIMAL_TO_STRING` default renders `"10.10"`, `False` renders `10.1`; `DecimalField(decimal_places=2)` rejects `10.105` on input but rounds half-even on output (`10.125` → `10.12`); naive input read in `TIME_ZONE`; `DjangoJSONEncoder` cuts µs to ms [V DRF 3.18.3, Django 6.1.2] | `USE_TZ = True`, `TIME_ZONE = "UTC"` |
| **FastAPI / pydantic v2** | `response_model`, `field_serializer`, `PlainSerializer`, field types | `Decimal` → `"10.10"` (string) [V 2.14.1; v1 was a float, BF-FA-07]; naive `datetime` accepted and re-emitted naive, an epoch int read as UTC, `AwareDatetime` rejects naive [V]; `response_model` drops undeclared keys [V FastAPI 0.143.0]; `json.dumps(Decimal)` raises, so carriers pre-convert with `float()` [V] | `date` fields; `AwareDatetime` |
| **Spring + Jackson** | the `ObjectMapper` bean, `spring.jackson.*`, every `new ObjectMapper()` | `BigDecimal("1E+3")` → `1E+3` unless `WRITE_BIGDECIMAL_AS_PLAIN`; `stripTrailingZeros()` gives `1E+2`; `ADJUST_DATES_TO_CONTEXT_TIME_ZONE` rewrites `+03:00` to `Z`; a hand-built mapper writes `LocalDateTime` as an array and `Instant` as an epoch; `readTree` money is a double unless `USE_BIG_DECIMAL_FOR_FLOATS` [V 2.20.1]; Jackson 3 / Boot 4 [K?] | a `double` ratio or score |
| **ASP.NET Core** | `AddJsonOptions`, EF value converters | `DateTime` read from EF comes back `Kind.Unspecified` and serializes with no offset; `DateTimeOffset` keeps it [K] | `DateTimeOffset` DTOs |
| **Go `encoding/json`** | struct tags (`json:",string"`), `Decoder.UseNumber` | numbers through `any` become `float64` (`…993` → `…992`); `time.Parse` with no zone in the layout returns UTC for a local time; `json` into `int` rejects `19.99` [V go1.27.2] | typed structs with `int64` fields |
| **Rails / Laravel** | `config.time_zone`, ActiveJob/Sidekiq args, casts | `Time.now` (system zone) vs `Time.current` (app zone) [V docs]; ActiveJob serializes `BigDecimal`, Sidekiq JSON args need a string [V guide 8.1 / K] | — |

## Tool lane and ledger

Each tool prints `ran` / `blocked (<why>)` / `NOT-RUN (<why>)` in the output header. No linter reads a serializer setting together with the field it renders: the rendered-body round trip is the oracle.

| Tool | Command | Covers | Limits |
|---|---|---|---|
| Schemathesis 4.31 | `st run <spec> --url <base> --checks response_schema_conformance --max-examples 50 --seed 1` on a local or `--live` non-production base | §3 (a body that disagrees with the documented type) | never sees `10.10` → `10.1` when the spec says `number`; `NOT-RUN` without a spec and a running app |
| Prism 5.16 | `prism proxy <spec> http://localhost:<port> --errors` in front of the project's own e2e run | §3 response-schema violations on the traffic the suite sends | sees only that traffic |
| Django warnings gate | `python -W error::RuntimeWarning manage.py test` (scope the filter to `django.db.models.fields`) | §6 a naive datetime saved [V Django 6.1.2] | Django only |
| RuboCop Rails 2.38 | `rubocop --only Rails/TimeZone,Rails/Date` | §7 `Time.now`/`Date.today` against `config.time_zone` | not run by the research (host Ruby too old) [K]; `NOT-RUN` without `rubocop-rails` in the Gemfile |

## Pre-flight greps

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds detector **§N**; F1 and grep 0 are the gates every § reads first. Every `rg` names its path — `.` or `"${ROOTS[@]}"`: with no path, `rg` reads stdin under an agent's shell and reports a silent zero. Include globs come **first**, exclusions last (rg-glob-order). With an explicit root, globs match relative to it, so exclusions start with `**/`. Any `rg` exit 2 is a failed grep, never zero hits. A two-line property (a `bigint` decorator over a `number` field, a `field_serializer` returning `float(`) is matched with `-U`, never with `-A<n> | rg -v` (rg-context-negation); a `-U` match prints each of its lines.

```bash
ROOTS=(.)   # server code; in a monorepo name the apps: ROOTS=(apps/api services/billing). Manifests and config always search .
SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/wf.XXXXXX")}"; mkdir -p "$SCAN"
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,java,kt,cs,go,php,rb}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
   -g '!**/*.{spec,test,e2e-spec,stories}.*' -g '!**/test_*.py' -g '!**/*_test.go' -g '!**/*.d.ts' -g '!**/*.min.*'
   -g '!**/{migrations,migration,db/migrate,seeders,seeds}/**' -g '!**/{locales,locale,i18n,translations}/**'
   -g '!**/{openapi,swagger}*.{json,yaml,yml}' -g '!**/{docs,ai,.claude}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\[))')   # drops comment-only lines
M='(?:amount|price|total|fee|balance|cost|subtotal|tax|charge|refund|payout|credit|debit|discount|money|wage|salary)'   # money-named identifiers, any case
# F1 serializer, ORM, decimal and date library versions — ranges from manifests, exact from lockfiles (gate 3; V357)
rg -n --no-heading --pcre2 '"(@nestjs/(?:common|core|platform-fastify|platform-express)|class-transformer|fastify|fast-json-stringify|express|@trpc/server|superjson|json-bigint|decimal\.js|big\.js|bignumber\.js|dinero\.js|@prisma/client|@mikro-orm/core|typeorm|drizzle-orm|pg|luxon|dayjs|date-fns|moment(?:-timezone)?)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .
rg -n --no-heading --pcre2 '"node_modules/(?:@nestjs/core|@nestjs/platform-fastify|class-transformer|fastify|fast-json-stringify|express|@trpc/server|superjson|json-bigint|decimal\.js|@prisma/client|@mikro-orm/core|typeorm|drizzle-orm|pg|luxon|dayjs|date-fns|moment)":\s*\{|^\s*["\x27]?/?(?:@nestjs/core|@nestjs/platform-fastify|class-transformer|fastify|fast-json-stringify|express|@trpc/server|superjson|json-bigint|decimal\.js|@prisma/client|@mikro-orm/core|typeorm|drizzle-orm|pg|luxon|dayjs|date-fns|moment)@\d[\w.-]*' -g '**/{package-lock.json,pnpm-lock.yaml,yarn.lock}' -g '!**/node_modules/**' .
rg -n --no-heading -i --pcre2 '^\s*["\x27]?(pydantic|djangorestframework|django|fastapi|marshmallow)\b\s*[=<>~!^]|\b(jackson-databind|jackson-datatype-jsr310|spring-boot-starter-(?:web|json))\b|"laravel/framework"\s*:|^\s*gem\s+["\x27](?:rails|oj|money-rails)["\x27]|<PackageReference Include="(Newtonsoft\.Json|NodaTime)"' -g '**/{pyproject.toml,requirements*.txt,Pipfile,poetry.lock,pom.xml,build.gradle*,composer.json,Gemfile,*.csproj}' -g '!**/node_modules/**' .
# 0 THE WIRING — the serializer and its settings, the process zone. Every later § reads this first (P5)
rg -n --no-heading --pcre2 '\bClassSerializerInterceptor\b|@SerializeOptions\s*\(|\bexcludeExtraneousValues\s*:|\bsetReplySerializer\s*\(|\bsetSerializerCompiler\s*\(|\bserializerOpts\s*:|\btransformer\s*:\s*superjson\b|\bBigInt\.prototype\.toJSON\b|\bJSONbig\b|\bCOERCE_DECIMAL_TO_STRING\b|\bjson_encoders\s*=|\bser_json_\w+\s*=|\bcls\s*=\s*\w*JSONEncoder\b|\bJackson2ObjectMapperBuilder\w*\b|\bnew\s+ObjectMapper\s*\(|\bJsonMapper\.builder\s*\(|\b(?:WRITE_BIGDECIMAL_AS_PLAIN|USE_BIG_DECIMAL_FOR_FLOATS|ADJUST_DATES_TO_CONTEXT_TIME_ZONE|WRITE_DATES_AS_TIMESTAMPS|WRITE_DATES_WITH_ZONE_ID)\b|\bJsonSerializerOptions\b|\bTimeZone\.setDefault\s*\(|\bprocess\.env\.TZ\s*=|\bSettings\.defaultZone\b|\b(?:dayjs\.tz|moment\.tz)\.setDefault\s*\(|^\s*(?:USE_TZ|TIME_ZONE)\s*=|\bconfig\.(?:time_zone|active_record\.default_timezone)\s*=|\bdate_default_timezone_set\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 'spring\.jackson\.[\w.-]+\s*[:=]|^\s*(?:time-zone|serialization|deserialization|generator)\s*:|^\s*(?:ENV\s+)?TZ\s*[=:]|\bname\s*:\s*TZ\b|["\x27]timezone["\x27]\s*=>' -g '**/{application*.yml,application*.yaml,application*.properties,Dockerfile*,*.Dockerfile,docker-compose*.yml,docker-compose*.yaml,app.php,.env.example}' -g '!**/node_modules/**' -g '!**/{test,tests}/**' .
# 1 Decimal leaves as a float or loses scale (1a DRF/pydantic settings and serializers · 1b Jackson money doubles, scientific notation · 1c JS Decimal-to-number at the edge · 1d the column count)
rg -n --no-heading -U --pcre2 '\bCOERCE_DECIMAL_TO_STRING["\x27]?\s*[:=]\s*False\b|\bcoerce_to_string\s*=\s*False\b|\bPlainSerializer\s*\(\s*float\b|\bjson_encoders\s*=\s*\{[^}]*\bDecimal\s*:\s*float\b|@field_serializer\s*\([^)]*\)\s*\n(?:\s*@\w+[^\n]*\n)*\s*def\s+\w+\s*\([^)]*\)[^:\n]*:\s*\n\s*return\s+float\s*\(' -g '*.py' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 "(?i:\\b(?:private|protected|public|val|var)?\\s*(?:final\\s+)?(?:double|Double|float|Float)\\s+\\w*$M\\w*\\s*[;=,)])|\\bstripTrailingZeros\\s*\\(\\s*\\)" -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 "\\.toNumber\\s*\\(\\s*\\)|\\b(?:Number|parseFloat)\\s*\\(\\s*[\\w.?!\\[\\]\"']*(?i:$M)\\w*\\s*\\)" -g '**/*{controller,mapper,presenter,serializer,serialiser,resolver,response,view,dto,transformer,router,handler}*.{ts,js,mjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
echo "1d decimal/numeric/float/double columns (read each: money, rate or measure; the type it is read into): $(rg -c --no-heading --pcre2 "\\b(?:type|columnType)\\s*:\\s*['\"](?:decimal|numeric|float|double|real|money)(?:\\(\\d+(?:,\\s*\\d+)?\\))?['\"]|@db\\.(?:Decimal|DoublePrecision|Real|Money)\\b|^\\s+\\w+\\s+(?:Decimal|Float)\\b[?]?|\\bmodels\\.(?:DecimalField|FloatField)\\s*\\(|\\bColumn\\s*\\(\\s*(?:Numeric|Float|DECIMAL)\\b|\\bnumeric\\s*\\(\\s*['\"]\\w+['\"]" -g '*.{ts,prisma,py}' "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}')"
# 2 64-bit numbers on the wire (2a bigint columns read into a JS number, Drizzle mode 'number' included · 2b BigInt-to-JSON patches · 2c Go decode into any without UseNumber)
rg -n --no-heading -U --pcre2 "\\b(?:type|columnType)\\s*:\\s*['\"](?:bigint|int8)['\"][^\\n]*\\)\\s*\\n?\\s*(?:readonly\\s+)?\\w+[!?]?\\s*(?::\\s*number\\b|=\\s*-?\\d+\\s*;)|@Column\\s*\\(\\s*['\"](?:bigint|int8)['\"][^\\n]*\\)\\s*\\n?\\s*\\w+[!?]?\\s*(?::\\s*number\\b|=\\s*-?\\d+\\s*;)|\\bbigint\\s*\\(\\s*['\"]\\w+['\"]\\s*,\\s*\\{\\s*mode\\s*:\\s*['\"]number['\"]" -g '*.{ts,js}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
echo "2a all bigint/int8 columns: $(rg -c --no-heading --pcre2 "\\b(?:type|columnType)\\s*:\\s*['\"](?:bigint|int8)['\"]|@Column\\s*\\(\\s*['\"](?:bigint|int8)['\"]|@db\\.BigInt\\b|^\\s+\\w+\\s+BigInt\\b|\\bmodels\\.BigIntegerField\\s*\\(|\\bBigInteger\\b" -g '*.{ts,js,prisma,py}' "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}')   ·  2b BigInt-to-JSON patches and parsers: $(rg -c --no-heading --pcre2 '\bBigInt\.prototype\.toJSON\b|\bjson-bigint\b|\bJSONbig\b|\bsuperjson\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}')"
# 1d/2a project column types: a class over the ORM's own type (MikroORM Type/DecimalType/BigIntType, TypeORM ValueTransformer, Drizzle customType, SQLAlchemy TypeDecorator).
#   1d and 2a count string column types only, so `type: MinorUnitsType` is in neither: read each class once (column type, what it reads into, the write guard); its uses are ONE wiring row
rg -n --no-heading -o -r '$1$2$3$4' --pcre2 '\bclass\s+(\w+)\s+extends\s+(?:\w+\.)?(?:Type|DecimalType|BigIntType|DoubleType|FloatType|IntegerType)\b|\bclass\s+(\w+)\s+implements\s+ValueTransformer\b|\bconst\s+(\w+)\s*(?::\s*ValueTransformer\b[^=\n]*=|=\s*customType\s*<)|^\s*class\s+(\w+)\s*\(\s*(?:\w+\.)*TypeDecorator\s*\)' -g '*.{ts,mts,cts,js,mjs,cjs,py}' "${X[@]}" "${ROOTS[@]}" | while IFS=: read -r f l c; do   # assigned first: inside echo "$(…)" with these nested quotes, bash 3.2 brace-expanded the -g '*.{…}' and ran rg once per extension
  k=$(rg -c --no-heading --pcre2 "\\b(?:type|columnType|transformer)\\s*:\\s*(?:new\\s+)?$c\\b|\\b(?:Column|mapped_column)\\s*\\(\\s*(?:[\"']\\w+[\"']\\s*,\\s*)?$c\\b|\\b$c\\s*\\(\\s*[\"']" -g '*.{ts,mts,cts,js,mjs,cjs,py}' "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF; f++} END {print s+0 " uses in " f+0 " files"}')
  echo "1d/2a project column type $c ($f:$l): $k"; done
rg -l0 --pcre2 '\bjson\.(?:Unmarshal|NewDecoder)\b' -g '*.go' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 --pcre2 '\bmap\[string\](?:any|interface\{\})|\[\](?:any|interface\{\})' | xargs -0 -r rg --files-without-match --pcre2 '\bUseNumber\s*\('
# 3 output reshaped by the serializer (3a Fastify response schemas, with `-U` because prettier puts the status code on its own line; FastAPI response_model, Jackson views, DRF field lists, class-transformer projection · 3b tRPC procedures with no .output)
rg -n --no-heading -U --pcre2 "\\bresponse\\s*:\\s*\\{\\s*['\"]?(?:[1-5]\\d\\d|[1-5]xx|default)['\"]?\\s*:|\\bresponse_model\\s*=|@JsonView\\s*\\(|^\\s*fields\\s*=\\s*(?:\\(|\\[|['\"]__all__['\"])|\\bexcludeExtraneousValues\\s*:\\s*true\\b" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading -U --pcre2 '\b\w*[Pp]rocedure\b(?:\s*\.\s*(?:use|input|meta|concat|unstable_concat)\s*(?<p>\((?:[^()]++|(?&p))*\)))*\s*\.\s*(?:query|mutation)\s*\(' -g '*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4 output rounding differs from input or compute rounding (DRF DecimalField with no rounding=, quantize with no mode, setScale with no mode)
rg -n --no-heading --pcre2 '\bDecimalField\s*\((?![^)\n]*\brounding\s*=)[^)\n]*\bdecimal_places\s*=|\.quantize\s*\(\s*[^,()\n]+(?:\([^()\n]*\))?\s*\)|\.setScale\s*\(\s*\d+\s*\)' -g '*.{py,java,kt}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 5 money as a float inside a carrier: a queue, event, cache or outbound body built with a float conversion of an amount (5a); double amounts in event schemas (5b)
rg -n --no-heading -U --pcre2 "(?:\\.(?:add|addBulk|send|sendMessage|dispatch)|\\b(?:delay|apply_async|send_task|publish|emit|enqueue|perform_later|perform_async|produce)|\\b(?:cache|redis|store)\\w*\\.(?:set|setex|hset)|\\bJSON\\.stringify|\\bjson\\.dumps)\\s*\\((?:[^()]|(?<p>\\((?:[^()]++|(?&p))*\\)))*?(?:\\b(?:float|Number|parseFloat)\\s*\\(\\s*[\\w.?!\\[\\]\"']*(?i:$M)|\\.(?:toNumber|doubleValue|floatValue)\\s*\\(\\s*\\))" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading -U --pcre2 "\\b(?:double|float)\\s+\\w*(?i:$M)\\w*\\s*=\\s*\\d+|\"name\"\\s*:\\s*\"\\w*(?i:$M)\\w*\"\\s*,\\s*\"type\"\\s*:\\s*(?:\"(?:double|float)\"|\\[[^\\]]*\"(?:double|float)\")" -g '*.{proto,avsc,avdl}' "${X[@]}" "${ROOTS[@]}"
# 6 time input binding (6a naive datetime types in request models · 6b coercion to an instant before a strict check · 6c calendar dates typed as instants · 6d Go layouts with no zone)
rg -n --no-heading --pcre2 '^\s+\w+\s*:\s*(?:Optional\[)?(?:datetime\.)?datetime\b(?!\.)|\bLocalDateTime\s+\w+\s*[;,)]|\bpublic\s+DateTime\??\s+\w+\s*\{' -g '**/*{request,Request,dto,Dto,DTO,command,Command,input,Input,schema,schemas,model,models,serializer,serializers,form,forms}*.{py,java,kt,cs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '@Type\s*\(\s*\(\)\s*=>\s*Date\s*\)|\bz\.coerce\.date\s*\(|\bz\.date\s*\(\s*\)|\bJoi\.date\s*\(\s*\)(?![^\n]*\.iso\s*\()' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
echo "6 strict date validators (the B-D12 control): $(rg -c --no-heading --pcre2 '@Is(?:ISO8601|DateString|RFC3339)\b|\.iso\.(?:datetime|date)\s*\(|\.datetime\s*\(\s*\{[^}\n]*\boffset\b|\bAwareDatetime\b|\bFutureDatetime\b|\bOffsetDateTime\b|\bDateTimeOffset\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}')"
# 6 project date primitives: exported zod/joi/yup helpers named for a date, day, instant or timestamp, in ROOTS' shared dirs or a workspace package (packages/, libs/: where a
#   monorepo's request schemas live) — the B-D12 control under the project's own names. Read each definition (an instant that requires Z or an offset? a real-date check?)
DP='^export\s+const\s+(\w*(?:Date|Day|Instant|Timestamp)\w*|(?:date|day|instant|timestamp)\w*)\s*(?::[^=\n]+)?=\s*(?:z|Joi|yup)\s*\.\s*(?:string|date|iso|coerce\s*\.\s*date)\b'
{ rg -U -n --no-heading -o -r '$1' --pcre2 "$DP" -g '**/{contracts,contract,schemas,schema,primitives,validation,validators,shared,common}/**/*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}"
  rg -U -n --no-heading -o -r '$1' --pcre2 "$DP" -g '{packages,libs}/**/*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" .; } | sed 's#^\./##' | sort -u > "$SCAN/wf-dateprims"
DPP=("${ROOTS[@]}"); while IFS=: read -r f l n; do inr=0; for r in "${ROOTS[@]}"; do r=${r#./}; case "$f" in "$r"/*) inr=1 ;; esac; [ "$r" = . ] && inr=1; done
  [ "$inr" = 1 ] && continue; d=$(dirname "$f"); while [ "$d" != . ] && [ ! -f "$d/package.json" ]; do d=$(dirname "$d"); done; [ "$d" = . ] && d=${f%%/*}
  case " ${DPP[*]} " in *" $d "*) ;; *) DPP+=("$d") ;; esac; done < "$SCAN/wf-dateprims"
while IFS=: read -r f l n; do k=$(rg -c --no-heading --pcre2 "\\b$n\\b" "${CODE[@]}" "${X[@]}" "${DPP[@]}" | awk -F: '{s+=$NF} END {print s-1}')
  echo "6 project date primitive $n ($f:$l): $k uses — read the definition (an instant that requires Z or an offset? a real-date check?)"; done < "$SCAN/wf-dateprims"
DPN=$(cut -d: -f3 "$SCAN/wf-dateprims" | sort -u | paste -sd'|' -)
[ -n "$DPN" ] && echo "6 project date-primitive uses over ${DPP[*]} (lines; definitions excluded): $(( $(rg -c --no-heading --pcre2 "\\b(?:$DPN)\\b" "${CODE[@]}" "${X[@]}" "${DPP[@]}" | awk -F: '{s+=$NF} END {print s+0}') - $(wc -l < "$SCAN/wf-dateprims") ))"
rg -n --no-heading --pcre2 "\\b(?!(?:created|updated|deleted|modified|sent|paid|processed|published|scheduled|started|ended|completed|cancell?ed|last|run|expired|archived|synced|verified|confirmed|issued|posted)(?:[A-Z_]))(?:dob|birth(?:day|_?date)|\\w*(?:Date|_date)|due(?:On|_on|Date|_date)?|valid(?:From|Until|_from|_until)|expires?(?:On|_on))\\s*[?!]?\\s*:\\s*(?:Date|datetime)\\b(?!\\s*\\|\\s*string)" -g '*.{ts,py}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\btime\.Parse\s*\(\s*(?:"(?![^"]*(?:Z07|-07|MST))[^"]*"|time\.(?:DateTime|Kitchen|ANSIC|Stamp\w*))' -g '*.go' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 7 offset or precision lost on output (7a instant types rendered without an offset · 7b wall-time columns and cursor encoders · 7c Rails clock calls); the Django, Spring, Node and Laravel zone settings are grep 0's
rg -n --no-heading --pcre2 '\bDjangoJSONEncoder\b|\bDateTimeKind\.Unspecified\b|\bSpecifyKind\s*\(|\b(?:LocalDateTime|java\.util\.Date)\s+\w+\s*[;,)]|\bpublic\s+DateTime\??\s+\w+\s*\{' -g '**/*{response,Response,dto,Dto,DTO,view,View,views,serializer,serializers,resource,Resource,presenter,Presenter}*.{py,java,kt,cs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 "\\b(?:type|columnType)\\s*:\\s*['\"]timestamp(?:\\s+without\\s+time\\s+zone)?['\"]|\\b(?:encode|serialize|serialise|to|make|build)Cursor\\s*\\(" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
echo "7c Rails Time.now / Date.today (WF §7 only when grep 0 shows a non-UTC config.time_zone, as with Django TIME_ZONE or spring.jackson.time-zone; otherwise code-quality §6): $(rg -c --no-heading --pcre2 '\bTime\.now\b|\bDate\.today\b' -g '*.rb' "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}')"
# 8 the clock seam (enabler): searched in tests too — a seam lives where the proofs run
echo "8 clock seams: $(rg -c --no-heading --pcre2 '\b(?:useFakeTimers|setSystemTime|advanceTimersByTime|FakeTimeProvider|TimeProvider|Clock\.fixed|MutableClock|freeze_time|freezegun|time_machine|travel_to|Carbon::setTestNow|synctest|clockwork|benbjohnson/clock)\b|\bimplements\s+\w*Clock\b|\binterface\s+\w*Clock\b|\bClock\s+\w+\s*[;,)=]' "${CODE[@]}" -g '!**/node_modules/**' -g '!**/vendor/**' "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}')"
```

The money-name list `M` is a candidate filter, not a verdict: a `total` that is a count is a decoy found by the read step; a money field the list misses (`grandSum`) is found from the response DTO the § reads.

### Measured (2026-10-14)

- **Real repo, read-only, full tree** (a NestJS 11 monorepo on Fastify with MikroORM 6 on Postgres, 3,722 `.ts` files under the API's `src`, `ROOTS=(apps/api/src)`; the pnpm lockfile and the workspace contracts package present): the block runs in about 1.5 s and prints 99 lines, 0 `rg` errors, 0 files written into the tree. **F1 reads the pnpm lockfile** (pnpm 9's indented, single-quoted keys, the reader `validation-boundary-scan` uses): MikroORM 6.6.16, Nest 11.2.6, Fastify 5.12.3, class-transformer 0.5.1, decimal.js 10.6.0, luxon 3.7.2, pg 8.20.0 — and `express` 5.2.1, locked only as an optional peer of `@nestjs/core` (`/backend-audit`'s F1 tags it `[peer-only]`; the adapter is Fastify). Before that line a run of this skill alone printed ranges only and read every version-gated row `UNREAD`. Grep 0 printed **nothing** — no serializer setting, no response schema, no zone setting (no `TZ` in the image or manifests: the process runs in UTC): every route renders through `JSON.stringify`. **§1** 4 edge conversions, all in the order mapper: 3 are `Number()` on `bigint` reads (B-D5, below) and a `numeric(12,2)` discount value typed `string` in the entity, converted with `Number()` and rendered as a JSON number (`12.50` → `12.5`) → **refuted** now that the contract is readable: the contracts package declares that field `z.number()` ("percent 0–100, else minor units"), so the number is the declared wire shape (B-R2), not lost scale. 1d counted **9** decimal/float columns: 1 measure (a weight), 1 percentage, 1 `double` rate, 5 exchange and interest rates (B-R2) and the discount above; the earlier copy's `double` price columns are gone. **§2** 19 `bigint` columns, 18 typed `number` (annotated or initialised with `= 0`) and 1 `string` → **0 findings, B-D5 cited**: a unit test pins the set of `bigint` columns, and reads convert with `Number()` in the mapper and in each projection's item builder. Most money columns are in neither count — 1d and 2a match string column types — so the **project column type** line finds the classes over the ORM's own type and counts their uses: 3 classes, **165 uses in 45 files** of an integer minor-units type (an `integer` column read as `::float8` into a JS number, writes past 2^53 refused), 7 of a quantity type and 2 of a unit-price type (both over `DecimalType`: exact `numeric` in the database, a JS number in memory, a value the column cannot hold exactly refused). Each class is read once as a wiring row; before the line, the 165 columns were found only by hand. **§3** 0 response schemas, 0 `response_model`, 0 tRPC. **§5** 0 carrier conversions (amounts travel as integer cents). **§6** 0 `@Type(() => Date)`, 0 `z.coerce.date`; the strict-validator count reads 0 under the API's `src` — the request schemas live in the contracts package — so the **project date primitive** lines find that package's exported zod helpers by name and shape and count their uses over ROOTS plus the package: 6 primitives, **270 lines** — the instant (an ISO regex that requires `Z` or an offset, then a real-date refine) and the calendar day (the same two steps) account for **222**, the B-D12 control. Read by hand, one of the other four is as strict (a day or an exact instant, 3 uses) and three are §6 candidates, Unconfirmed until V347: a list-filter bound that takes a day **or an instant without an offset** (30 uses — a naive bound read in the process zone), and two day primitives that check the shape only (15 uses — `2026-02-30` passes; one says so in its doc comment, for a filter external clients already send). 15 calendar-named fields typed `Date`: the expiry day is still parsed with `new Date("YYYY-MM-DD")` (UTC midnight) into a `timestamptz` column; its renderers either slice the UTC ISO day (exact) or use the process-local day helper, which round-trips while the process runs in UTC → Hardening (a process zone west of UTC would render the day before; the parse is code-quality §6, the column database §5). **§7** 0. **§8** 2 seams under `src` (the tests live beside it, outside ROOTS). An earlier partial copy (no lockfile, no contracts package, class-validator DTOs under `src`) printed 76 lines: 18 decimal columns, 58 strict validators, 30 seams. An earlier draft matched cursor lines (`cursor.toISOString()` inside Redis consumers, 24 lines) — those are distributed-systems cursors, so 7b now reads cursor **encoders** only; and 2a first missed the 8 initialised `= 0` fields.
- **Fixtures** (`benchmarks/fixtures/*`, 18 roots; none seeds a WF class yet — `backend-defects` is a later build item): 15 roots print 0 lines. `slow-marketplace`: 5 MikroORM `bigint` cent columns typed `number` (§2 candidates: the services read them with `Number()`; no pinned-set test, so B-D5 is not met), 1 DRF serializer field list (§3), 1 `quantize(Decimal("0.01"))` with no mode on a rendered report value (§4: half-even by default, a report not a charge → Hardening unless rendered = charged, B-R4); a `float(row["amount"])` into a model `defaults=` stays quiet (arithmetic and storage, code-quality's). `half-built-crm`: 8 FastAPI `response_model` rows (§3 reads). `quality-mix`: 1 Go handler decoding a webhook into `map[string]any` with no `UseNumber()` and storing the map (§2, BF-GO-03).
- **Research labs and a paired sample** (the research's Fastify, tRPC and semgrep samples; a POS/NEG sample of 40 lines across TS, Python, Java, Go, Protobuf and Avro): every POS found — `COERCE_DECIMAL_TO_STRING: False`, `PlainSerializer(float)`, a multi-line `field_serializer` returning `float(`, a `double totalAmount`, `stripTrailingZeros()`, `.toNumber()` in a mapper, annotated and initialised `bigint` columns, Drizzle `mode: 'number'`, a Go `any` decode, Fastify response schemas (6 in the research lab), tRPC procedures without `.output()` (4 of 6, multi-line chains included), `DecimalField` and `quantize`/`setScale` with no mode, float amounts inside `queue.add`, `emit` (multi-line), cache `set`, Python `publish`, Protobuf and Avro `double` amounts, naive `datetime` and `LocalDateTime` request fields, `@Type(() => Date)`, `z.coerce.date()`, Go layouts with no zone; the NEG lines (`count`, `ratio`, a raw integer-cents payload, `rounding=` present, `.output()` present, `RFC3339`, `createdDate`, a `Date | string` union) stayed quiet. The research's semgrep sample (retries, enqueue-in-transaction, unchecked status) printed 0 WF lines.
- **`backend-defects` fixture** (2026-10-14, after the fixture's IR-3): grep 3a runs with `-U`, so a prettier-formatted Fastify schema (`response: {` with `200: {` on the next line) prints as two lines. It prints BD-WF-3a (`fx.routes.ts`, `amount` typed `integer`) and the catalog feed schema BD-DECOY-42, which one read clears (B-A12). Before `-U` both printed 0. Re-run after the lockfile line, the project column type line and the project date primitive lines (2026-10-14): 59 lines (F1 adds 6 lockfile lines), the same seeds and decoys; the two new lines print nothing here (string column types, class-validator DTOs) — the synthetic pair that exercised them found a TypeORM `ValueTransformer` (class and object), a Drizzle `customType`, a SQLAlchemy `TypeDecorator` and three date primitives in a workspace package, and stayed quiet on `updateUserSchema = z.string()` and `dayCount = z.coerce.number()`.

## The 3,000-hit path

The wiring row decides most of a large run (P5). One serializer setting (`COERCE_DECIMAL_TO_STRING = False`, `ADJUST_DATES_TO_CONTEXT_TIME_ZONE`, a global `excludeExtraneousValues`) is **one** finding with N fields. Then, in order: §5 carrier rows (few, high); §2 grouped by entity — one read of how the mapper converts, then only the reads that bypass it; §1 grouped by mapper; §6 request fields on public and money routes first; §3 grouped by router file; §7 by response DTO. A group may be closed with **one cited reason** (`18 bigint columns: pinned-set test at file:line, Number() at every projection, 8 bypass reads sampled`) when the reason is checked, not assumed. Shipped money fields are never bulk-closed by name.

## Scans for

| § | Class (research id) | Default severity | Oracle |
|---|---|---|---|
| 1 | Decimal → JSON float, scale or plain notation lost (BM-01, BM-02, BF-FA-07) | high; blocker when a client re-submits the value to a charge | V339 |
| 2 | 64-bit ids and amounts on the wire (BA-16, BF-GO-03) | high on money or an id used as a key; a `BigInt` → 500 is high | V339 |
| 3 | output reshaped by the serializer (BV-15, BN-06, BN-12, BF-FA-02) | high when a value changes; medium when a field is dropped | V338 |
| 4 | output rounding ≠ input or compute rounding (BM-04) | medium; high when the rendered amount is the charged amount | V348 |
| 5 | money as a float in carriers (BM-07) | high | V348 |
| 6 | time input binding (BA-17, BM-08, BM-13, BF-GO-05, BF-NET-04) | high for an instant; medium for a calendar date | V347 |
| 7 | offset or precision lost on output; zone setting vs code (BM-09, BM-11, BF-RA-03) | medium; high on a cursor or an idempotency window | V349 |
| 8 | no clock seam (BM-15, enabler) | never a finding | none |

Every lane row that rests on a framework default also carries V357: the oracle ran on the installed version and the finding states it.

### 1. Decimal leaves as a float, or loses scale

```
BAD:   REST_FRAMEWORK = {"COERCE_DECIMAL_TO_STRING": False}       // Decimal("10.10") renders 10.1
       amount: Annotated[Decimal, PlainSerializer(float)]  ·  @field_serializer("total") def s(v): return float(v)
       private double totalAmount;  ·  price.stripTrailingZeros()   // 100.00 → 1E+2  ·  toDto: total: order.total.toNumber()
GOOD:  the string default ("10.10")  ·  pydantic v2's string Decimal  ·  BigDecimal + WRITE_BIGDECIMAL_AS_PLAIN
       integer minor units + a currency  ·  decimal.toFixed(scale) as a string in the mapper
```
**Read the code:** what does the contract say the field is — string decimal, integer minor units, or a documented `number` the client parses with a decimal library (B-R2, B-G24)? Which serializer renders it (grep 0)? Is the value money, or a rate, a ratio or a measure (B-R2)? Does a client sum it, compare it as a string, or send it back to a charge? Prisma `Decimal` and decimal.js render `"10.1"` — is scale part of the contract? A pydantic v1 → v2 upgrade flips floats to strings for JS clients doing arithmetic (BF-FA-07): does the lockfile show the upgrade? **Finding when** a seeded value comes out with fewer digits, other digits, scientific notation or a different JSON type than the contract. **Proof:** V339 — seed `10.10`, `0.10`, `1000.00`, `-0.00`, `9007199254740993.00`; GET the list, the detail, the export and the webhook; parse the text with the client's parser; digits and scale equal the seed.

### 2. 64-bit ids and amounts on the wire

```
BAD:   @Property({ type: 'bigint' }) totalCents!: number;    // pg hands back "20000": '100' + '200' is '100200'
       res.send({ id: 9007199254740993n })                    // "Do not know how to serialize a BigInt" → 500
       var raw map[string]any; json.Unmarshal(b, &raw)        // …993 becomes …992 when re-encoded
GOOD:  ids as strings on the wire  ·  one mapper converting every bigint read + a test pinning the set (B-D5)
       dec := json.NewDecoder(r); dec.UseNumber()  ·  typed structs with int64 fields
```
**Read the code:** what does the driver return for the column on the installed version (string, number, bigint — lane table)? Does every read reach the response through the mapper, or does one projection pass it raw (B-D5's flip)? Can the value pass 2^53 (a sequence, a sum, a Snowflake id) — cite the generator? Who decodes the body: a JS client, `JSON.parse`, a Go `any`? A project column type (the 1d/2a line) decides every column it declares: read its read path and write guard once, then only the reads that bypass it. **Finding when** an id or amount above 2^53 changes, a `BigInt` reaches `JSON.stringify` (500), or a `bigint` read reaches the wire as a string where the contract says number (or the reverse). **Proof:** V339 — seed an id and an amount above 2^53, GET it, compare as a string; and the `bigint` read through each projection.

### 3. Output reshaped by the serializer

```
BAD:   schema: { response: { 200: { properties: { total: { type: 'integer' } } } } }   // total 12.7 → 12 with a 200
       @router.get("/x", response_model=OrderOut)   (a field added to the row, not to OrderOut: dropped)
       t.procedure.input(In).query(...)   (no .output(): every column of the row ships)
GOOD:  the response schema generated from the same type the handler returns  ·  .output(Out) on every procedure
       a DTO test asserting the response equals the domain object projected to the documented fields
```
**Read the code:** is the projection on purpose (B-A12: hiding internals is the point) or drift (a field added in code that the schema drops)? Does any schema type disagree with the value the handler returns (`integer` over a decimal, `string` over a nullable column → `""`, `boolean` over a string)? A field leaking because nothing projects is security's (§ Boundaries). **Finding when** a value changes, or a documented field never reaches the client. **Proof:** V338 — the response equals the domain object projected to the documented fields with no value changed (`12.7`, `"no"`, `null` seeded); capture the pre-serialization object in an `onSend` hook beside `inject()`.

### 4. Output rounding differs from input or compute rounding

```
BAD:   amount = serializers.DecimalField(max_digits=10, decimal_places=2)   // input rejects 10.105; output rounds half-even: 10.125 → 10.12
       total.quantize(Decimal("0.01"))   ·   amount.setScale(2)   (no mode on a rendered value)
GOOD:  DecimalField(..., rounding=ROUND_HALF_UP) where the PSP rounds half-up  ·  quantize(Decimal("0.01"), ROUND_HALF_UP)  ·  setScale(2, RoundingMode.HALF_UP)
```
**Read the code:** what rounding does the compute use, and what does the PSP or the invoice use? Is the rendered amount the amount charged (B-R4: banker's rounding chosen and written is the decoy)? Is the compute precision wider than the field's places? The rounding **point** (per line or per total) is code-quality §4's. **Finding when** a tie renders differently from the amount charged or stored. **Proof:** V348 — ties `x.xx5` positive and negative; the rendered amount equals the amount sent to the PSP stub.

### 5. Money as a float in carriers

```
BAD:   queue.add('charge', { orderId, amount: Number(order.totalAmount) })   ·   publish("order.paid", {"amount": float(o.amount)})
       cache.set(key, JSON.stringify({ price: dec.toNumber() }))   ·   message OrderPaid { double amount = 1; }
GOOD:  { amountMinor: 1999, currency: 'EUR' }  ·  {"amount": str(o.amount)}  ·  int64 amount_minor + string currency
```
**Read the code:** `json.dumps(Decimal)` raises, so the producer converted — to what? Is the consumer a service that re-submits the amount (a charge, a payout, a ledger write)? Messages already in the queue keep the old shape: does the change ship with a dual-read? Schema evolution across services is distributed-systems'; the payload's drift across one service's deploys is `job-lifecycle-scan` §3. **Finding when** an amount crosses a queue, an event, a cache or an outbound body as a binary float. **Proof:** V348 — enqueue `19.99` through the real producer and read the **raw** broker payload (Redis `LRANGE`, an SQS receive, the cache value): a string decimal or integer minor units.

### 6. Time input binding

```
BAD:   paid_at: datetime   (pydantic: "…T10:00:00" with no zone accepted)  ·  private LocalDateTime deliverAt;  (an instant)
       @Type(() => Date) @IsDate() from: Date   ("2026-02-30" → 2 March)  ·  due_date: datetime  ·  dueDate: Date
       time.Parse("2006-01-02 15:04", s)   (no zone: read as UTC)  ·  public DateTime PaidAt { get; set; }
GOOD:  paid_at: AwareDatetime  ·  OffsetDateTime / Instant  ·  DateTimeOffset  ·  @IsISO8601({ strict: true }) kept as a string (B-D12)
       due_on: date  ·  time.ParseInLocation(layout, s, loc) or a layout with Z07:00
```
**Read the code:** is the field an instant (paid, expires, created) or a wall-clock or calendar value (opening hours, a birthday, a due day — B-R3)? What zone does the binder assume for naive input — the process `TZ`, `TIME_ZONE`, UTC? Is `TZ` set in the image and manifests (grep 0)? A calendar date carried as an instant shows the previous day west of UTC: where is it rendered? The parse inside a handler (`new Date(req.body.x)`) is code-quality §6. A project date primitive (grep 6) is the control when its definition requires an offset and a real date; one that takes a naive instant or checks the shape only is the candidate, its use count the N. **Finding when** one input stores different instants under two server zones, a naive instant is accepted where the contract says RFC 3339 with offset, an impossible date passes, or a calendar day shifts. **Proof:** V347 — the same body under `TZ=UTC` and `TZ=Pacific/Kiritimati` (and `Asia/Kathmandu`): one stored instant, or 422 for naive input; `2026-02-30` → 400; date-only strings unchanged.

### 7. Offset or precision lost on output; zone setting versus code

```
BAD:   ADJUST_DATES_TO_CONTEXT_TIME_ZONE (default on)        // "+03:00" rewritten to "Z" where the contract keeps the offset
       new ObjectMapper()  (no JavaTimeModule config)          // LocalDateTime as [2026,3,29,10,0], Instant as an epoch
       DjangoJSONEncoder on a cursor key                       // µs cut to ms: the next page skips rows
       USE_TZ = False  ·  TimeZone.setDefault(...) beside spring.jackson.time-zone  ·  Time.now with config.time_zone = "Riyadh"
GOOD:  the injected mapper bean everywhere  ·  OffsetDateTime with the offset contracted  ·  cursors encoded at the column's precision
       USE_TZ = True  ·  Time.current
```
**Read the code:** does the contract keep the offset, or normalise to UTC by design (documented UTC is the decoy)? Is a hand-built mapper used beside the configured bean? What precision does the column have, and what does the cursor encoder keep? Do two zone settings disagree (the process, the framework, the JDBC session, the ORM)? **Finding when** the same instant comes out with another offset or precision than the contract, or one endpoint answers differently under two server zones. **Proof:** V349 — round-trip `…10:00:00.123456+03:00`; identical responses under two server zones; US and EU DST gap and overlap dates.

### 8. No clock seam (enabler)

```
BAD:   expiry computed from new Date() / timezone.now() / Instant.now() with no Clock, TimeProvider or fake timers anywhere
GOOD:  an injected Clock bean · .NET 8 TimeProvider · vi.setSystemTime / jest fake timers · time-machine · Go testing/synctest
```
**Read the code:** does any proof in §6, §7 or `job-lifecycle-scan` need a fixed or moving clock? Never a finding on its own: the row prints `blocked (no clock seam)` on the proof it blocks, and the seam is named in the settling step.

## Output

```
wire-format-scan — lanes: nestjs 11.2.6 on fastify 5.12.3, @mikro-orm/core 6.6.16, pg 8.20.0 (pnpm-lock.yaml) · express 5.2.1 locked only as an optional peer
Wiring: no serializer setting, no response schemas (JSON.stringify on every route) · process TZ: not set in the image or manifests (UTC)
        column types: 3 project classes over the ORM's type (minor units 165 columns, quantity 7, unit price 2) · date primitives: 6 in the contracts package (270 uses)
Tools: schemathesis NOT-RUN (no running app in this run) · prism NOT-RUN (same) · django gate N/A · rubocop N/A

Findings: 0 · Unconfirmed: 2 · Hardening: 1

1. packages/contracts/src/primitives/request-fields.schema.ts:200 (30 uses)           Unconfirmed  medium
   §6 — a list-filter bound takes a day or an instant with no offset: "2026-03-29T10:00" is read in the process zone (UTC today).
   A filter, not a stored instant. Settling: V347 — the same query under TZ=UTC and TZ=Asia/Kathmandu returns one result set, or 400.
2. packages/contracts/src/orders/request-fields.schema.ts:14 (+ 1 primitive; 15 uses)  Unconfirmed  low
   §6 — two calendar-day primitives check the shape only: "2026-02-30" passes (one documents it, for a filter external clients send).
   Settling: V347 with 2026-02-30 → 400, or the documented roll. Fix: the package's own real-date refine.
3. src/inventory/stock-scans.port.ts:152                                             Hardening    low
   §6 — a calendar expiry day parsed as new Date("YYYY-MM-DD") into a datetime column; rendered by the UTC day slice or the process-local
   day helper, exact while the process runs in UTC. Parse → code-quality §6; column → database §5.

Verification: 53 candidate rows → 0 findings · 2 unconfirmed (3 primitives) · 1 hardening · 49 refuted (self-verified; 22 B-D5, 10 B-R2, 3 B-D12 primitives, 14 instant or day-sliced names)

Class coverage:
  §1 decimal → float          checked (4 edge conversions → 0: 3 B-D5, 1 B-R2 with the contract read; 9 columns → 9 B-R2; 3 column types read once)
  §2 64-bit                   checked (19 bigint, 18 typed number → 0, B-D5 cited: pinned-set test; 165 minor-units columns through one type, writes past 2^53 refused)
  §3 serializer reshaping     checked (0 response schemas, 0 response_model, 0 tRPC procedures)
  §4 rounding                 N/A (no Decimal type and no serializer rounding setting: integer minor units)
  §5 carriers                 checked (0 float conversions inside a carrier call)
  §6 time binding             checked (0 coercions to Date; 0 strict validators under src; 6 project primitives → 3 control (222 + 3 uses), 2 unconfirmed; 15 calendar names → 1 hardening)
  §7 offset / precision       checked (0 settings, 0 cursor encoders)
  §8 clock seam               N/A (2 seams present under src; the tests sit outside ROOTS)
```

`[report-with-fix]`: the oracle failed on the rendered bytes through the real bootstrap on the installed version, and the fix is local to the project's serializer setting, mapper, money type or date helper. `[report-flagged]`: one link is unproven (no oracle run, the version or the contract `UNREAD`, the driver's return type not read); the row names it and the settling seed. The coverage block lists **all eight** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep or tool>)`, `→ <owner> (k)` or `Live, unreviewed (k)`. A missing line is printed by `/backend-audit` as `not run`.

## False positives / precedents

The verifier reads [`precedents/backend.md`](../../../../snippets/precedents/backend.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **B-D5** a `bigint` column typed `number` whose every read is converted and whose set a test pins; **B-D12** dates kept as strings with a strict validator.
- **B-R1** a library default that is safe on the installed version (pydantic v2 renders `Decimal` as a string; Go `json` into `int` rejects `19.99`) — report the override, never the library; **B-R2** a float that is a ratio, score or rate, or a documented `number` contract the client parses with a decimal library; **B-R3** a wall-clock or date-only field; **B-R4** banker's rounding chosen and written.
- **B-A12** a response schema that hides internals on purpose; **B-G24** money as an amount + ISO 4217 currency, RFC 3339 date-times.
- **P1** cite the contract the value breaks; **P2** show the seed and the bytes; **P3** an over-returned secret is security's; **P4** prove on the serializer and versions that ship; **P5** one finding at the setting or the mapper, N fields.

Shapes this skill must not report: amounts already in integer minor units; a `numeric` rate typed `string`; a `double` measure or quantity; a `toISOString()` on an instant whose contract is UTC; a cursor inside a consumer (distributed-systems'); a `total` that is a count.

## When to run

- On any diff that touches a serializer setting, a response DTO or schema, a mapper, an entity's numeric or date column, a producer call, an event schema, a request model's date field or a zone setting — `/backend-audit`'s "a DTO, serializer or producer file" signal.
- On every whole-repo `/backend-audit`, reporting all eight §s; before upgrading pydantic, Jackson, Fastify, DRF, the ORM or its driver across a major (V357).

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets part A (the serializer row), part B (the version line), the field and the seed — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/backend.md`. Under `/backend-audit` that is `@api-reviewer` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Halt before any § when grep 0 is unread.** A verdict on a field without the serializer that renders it is invalid; when the serializer is configured in code grep 0 cannot see, read the bootstrap by hand and quote it.
- **Halt on any finding missing its anchors:** the `file:line`, the serializer row, the version, the seed and the bytes, the fix in the project's own primitive.
- **No `[report-with-fix]` without V338/V339/V347–V349 on the rendered bytes** through the project's own bootstrap on the installed version (or a two-ended static fact). Asserting on the object the handler returned is not one.
- **No proposed fix may hide the class:** never round in the test, never widen a response schema to `number` to silence a coercion, never compare money with a tolerance, never pin `TZ=UTC` in the test process only.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "the wire format looks fine"** without the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/backend-audit` dispatches this skill and folds its coverage block into its wire ledger rows; `/backend-fix` closes findings failing-first through the real bootstrap and re-runs this detector.
- `http-contract-scan`, `validation-boundary-scan`, `job-lifecycle-scan` (this pack) are the neighbours named in § Boundaries; `endpoint-test-method` (this pack) drives the V339 and V347 requests against a running app; `@api-reviewer` judges these rows.
- code-quality `correctness-smell-scan` §4/§6, database `schema-integrity-scan` §4/§5/§7, security `data-exposure-scan` §4 and distributed-systems `event-contract-scan` / `messaging-scan`, when those packs are installed.

## Sources

Defaults tagged `[V]` were run by the backend research (labs A and B, 2026-10-14): Fastify 5.12.7 response serialization and the `BigInt` 500, tRPC 11.19.0 with and without `.output()`, Node 22.14 `JSON.parse` and decimal.js 10.6.0, pydantic 2.14.1 and FastAPI 0.143.0, DRF 3.18.3 / Django 6.1.2 (decimal coercion, output rounding, `DjangoJSONEncoder`, naive input), Python 3.14 `json.dumps(Decimal)`, Jackson 2.20.1 with jsr310 on JDK 21.0.12, Go 1.27.2; Rails 8.1 rows are from the Rails guides as read by the research. `[K]` rows (node-postgres string mapping, Drizzle `mode: 'number'`, class-transformer `excludeExtraneousValues`, `superjson`, System.Text.Json and EF `DateTime.Kind`, Sidekiq JSON args, RuboCop Rails 2.38) are vendor documentation as read by the research; `[K?]` the ORM bigint mode per version and Jackson 3 / Boot 4 defaults. The real-repo and fixture counts are from a read-only run of the block above on 2026-10-14. Paraphrased; no text reproduced beyond identifiers.
