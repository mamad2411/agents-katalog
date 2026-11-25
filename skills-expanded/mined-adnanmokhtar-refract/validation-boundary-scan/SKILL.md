---
name: validation-boundary-scan
description: "Validation boundary: bodies the pipe never sees, coercion before validation, null via optional, unknown keys — read-only."
kind: skill
pack: backend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: validation-boundary-scan

## Premise

A global validation pipe looks like a guarantee: every route has a DTO, every DTO has decorators, `whitelist: true` is set. It is not one. The pipe validates only what the framework hands it **as a class**: a body typed as an interface, a `type` alias, `Dto[]`, `Partial<Dto>`, `Record<…>`, `unknown` or a union such as `Dto | null` reaches it as `Object` or `Array` and passes untouched — `whitelist` strips nothing there either. A transform can run **before** the validator (`enableImplicitConversion` turns `"false"` into `true` and `""` into `0`), `@IsOptional()` lets `null` through to a NOT NULL write, a nested object is checked only when `@ValidateNested` **and** `@Type` sit on the same property, and the unknown-key policy differs per library (zod strips, joi rejects, Fastify's ajv strips silently). Nothing fails loudly: the request answers 200 or 201 with a wrong value, or 500 two layers down. This skill finds those places in the wiring, the DTOs and the binders, and proves each with the payload that got through the project's **own** bootstrap. Read-only: it never edits code.

Backend owns **the wiring between the HTTP framework and the domain** (eval § 4.1): whether validation runs and on what, and what the transform does to a value before the validator sees it. It owns `/backend-audit`'s validation rows (`validation-boundary-scan §1–§9`); `@api-reviewer` (this pack) judges them in refute mode.

**Every finding cites the param or property `<file:line>` + the wiring row it depends on (the pipe and its options, quoted from the bootstrap) + the payload that got through + the oracle that showed it, or the request that would settle it + the fix in the project's own primitive** (its pipe subclass, its DTO base, its local validator such as an `IsAbsentOr()`). A grep hit is a candidate. "Validation looks fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/backend.md`](../../../../snippets/precedents/backend.md). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Backend, V340–V344 and V357.

## The rule

A candidate is a finding when all four hold — `precedents/backend.md` § Reading the seven gates for backend, applied to validation.

1. **Part A holds: this is the pipe that ships, on a mounted route.** The pipe comes from the bootstrap — `main.ts`, the `APP_PIPE` provider (often a subclass: an `I18nValidationPipe` registered in the app module, not `useGlobalPipes` in `main.ts`), the shared `configureApp` function, `create_app()`, the Spring context. A unit test that builds its own `new ValidationPipe()` proves nothing about what ships (B-D7). The controller's module is imported by the app module the bootstrap uses.
2. **Part B holds at the installed version.** Framework, validator and transformer versions come from the lockfile (F1); without one they are `UNREAD` and every version-gated row is Unconfirmed (V357). The Nest rows below were **measured on Nest 12.1.3 with class-validator 0.15.1** (research lab A, 2026-10-14, both adapters). **Nest 11 was not run**: the `forbidUnknownValues` default, `enableImplicitConversion` and the `X | null` metatype on a Nest 11 project are Unconfirmed until V340/V341 runs on the installed version.
3. **Nothing already controls it**, across files: a `@Transform` on every boolean, a `Parse*Pipe` or an `assert*()` guard before use (B-D10), a hand parser that bounds every field of a deliberate `unknown` body (B-D1), a local `IsAbsentOr()` (`ValidateIf(v !== undefined)`) in place of `@IsOptional`, a use case that rejects `null` before the write, a documented tolerant reader (B-A11, B-G17).
4. **The oracle fired, or the fact is two-ended.** V340–V344 through the real bootstrap (tier U) shows the payload through, or the static fact cites both ends (tier S: the pipe options and the DTO that depends on them; the `@IsOptional` field and the NOT NULL column it reaches). Without one, the row is `[report-flagged]` / Unconfirmed with the request written out (P2: every finding carries the payload).

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration (`precedents/backend.md` § Owned elsewhere).
- **Operator objects and mass assignment** (`{"$gt":""}` into a filter, a body key bound onto a privileged column) → security `injection-scan` §3 and `@api-security-reviewer` § "API3 — Broken Object Property Level Authorization (BOPLA)", when the security pack is installed: §7 here reports that a named primitive param *can* receive an object (the validation half); the attacker reading goes there (P3). Without the pack the row is listed tagged `operator object (owner pack security not installed)`, never graded as injection. A `Record<string, unknown>` body deep-merged into settings is security `injection-scan` §12.
- **Out-of-range client numbers and repeated-key caps** (a negative quantity, a client-chosen price) → security `logic-race-scan` §1/§2. §4 here owns the binder's silent coercion (`3.7` → 3, missing → 0), not the range.
- **`(await res.json()) as T`, `req.body as Foo`** → code-quality `type-safety-scan` §1 (B-A16). §1 here owns "the pipe cannot see the type".
- **Unbounded arrays as a size or CPU problem** → performance `request-path-scan` §13 (inbound limits) and §11; §9 here owns "one and many behave alike, over-max rejected".
- **Config validated at boot, lazy config reads** → devops `deploy-safety-scan` §6. §4 here owns the parse itself (`"false"` truthy, `parseInt("10s")`).
- Same pack: **defaults applied on PATCH** (an initialiser on an Update DTO, BV-14) → `http-contract-scan` §5; **a validator exception answered 500** (BV-16) → `edge-error-scan` §6; **output not validated or reshaped** (BV-15) → `wire-format-scan` §3; **consistency of 400 vs 422 across routes** → `api-consistency-audit` #2.
- **Cross-pack modes of `dto-types.py`** (this skill's script, never copied): `--routes` adds `mounted` (the full path after the global prefix and its `exclude`, URI version and `RouterModule`), `version` and `class_decorators` to HANDLER rows, and a `values` column (`member=value`) to `--enums` rows. The migration pack's `paired-inventory` calls both for its Nest I-ROUTES, I-AUTHZ, I-RULES and I-ENUM lanes, when the migration pack is installed. No § here reads those columns; without the migration pack the flags are simply unused.

## Adapt to the codebase — the lanes

Read the validator **with its version** (F1) and the wiring (grep 0) first. Defaults below are tagged `[V]` (ran) or `[K]`/`[K?]` (docs or secondary, not run) with their source in § Sources; a `[K?]` default makes its verdict Unconfirmed until V341 runs.

| Lane | Where validation is wired | Defaults that decide verdicts | Decoy shape |
|---|---|---|---|
| **NestJS + class-validator/class-transformer** (either adapter) | `APP_PIPE` provider or `useGlobalPipes` (often a subclass), `@UsePipes`, a Nest 12 `StandardSchemaValidationPipe` | `toValidate()` skips `String, Boolean, Number, Array, Object, Buffer, Date` metatypes; the constructor sets `forbidUnknownValues: false` unless passed (undoing class-validator's 0.14 default); `@IsOptional` skips `null` and `undefined`; arrays of nested are validated without `each` [V 12.1.3] | a deliberate `@Body() body: unknown` with a bounding parser (B-D1); `PartialType(Dto)` is a class and is validated [V] |
| **Fastify** (plain, or its ajv under Nest routes with schemas) | `ajv: { customOptions }` in the `Fastify()` / `FastifyAdapter` options; route `schema` | `@fastify/ajv-compiler` 4.0.7: `coerceTypes: 'array'`, `removeAdditional: true`, `useDefaults: true`, `allErrors: false` [V] | `additionalProperties` in an LLM tool schema is not a route schema |
| **Express / Koa + zod, joi, yup, valibot** | middleware (`validateRequest`, `celebrate`, `zValidator`) or `schema.parse(req.body)` in the handler | zod/valibot strip unknown keys, joi rejects, yup keeps; zod `.optional()` rejects `null` [V] | `z.coerce.number()` on a `.positive()` field; env parsing at boot (B-A13) |
| **Django REST Framework** | `Serializer` fields; `partial=` in views | unknown keys dropped silently; `required=False` still rejects `null` (`allow_null` off) [V 3.18.3] | — |
| **FastAPI / pydantic v2** | `BaseModel` fields, `model_config` | `extra='ignore'` (unknown keys dropped); `Optional[int]` with no default is **required** (BF-FA-01) [V 2.14.1] | `Optional[X] = None` is optional |
| **Spring Boot + Jackson + Bean Validation** | `@Valid`/`@Validated`, `spring.jackson.*`, `Jackson2ObjectMapperBuilder` | nested needs `@Valid` on the field and `List<@Valid T>` [K]; unknown ignored, `3.7` → 3, `"3"` → 3, missing primitive → 0 on Jackson 2.20.1 [V]; Jackson 3 / Boot 4 defaults [K?] | an internal DTO fed by a schema-validated producer |
| **ASP.NET Core** | `[ApiController]`, `AddJsonOptions`, FluentValidation | System.Text.Json web defaults: case-insensitive, numbers read from strings, unknown members ignored; a value type is never "missing" (0) without `[JsonRequired]` [K] | — |
| **Go: `encoding/json`, gin, echo** | `json.NewDecoder`, `c.ShouldBind*`/`c.Bind*`, struct tags | unknown fields ignored, case-insensitive keys, duplicate key last-wins, `Decoder` ignores trailing data; gin `binding:"required"` fails on `0` and `false`; echo `c.Bind` lets a body `id` override the path `id` [V go1.27.2, gin v1.12.0, echo v4.16.0] | a pointer field (`*int`) with `required` |
| **Laravel** | Form Requests | `$request->all()` after a Form Request bypasses `validated()` (BF-LA-01) [K] | `->validated()` / `->safe()` |

## Tool lane and ledger

Each tool prints `ran` / `blocked (<why>)` / `NOT-RUN (<why>)` in the output header.

| Tool | Command | Covers | Limits |
|---|---|---|---|
| `scripts/dto-types.py` (this skill), Python 3 stdlib | `python3 -I "$VB/dto-types.py" --params --decorator-blocks --enums --flagged "${ROOTS[@]}"` · `--self-test` (75/75); `--json`, `--include-tests`, `--action-words=a,b` | PARAM rows (every `@Body`/`@Query`/`@Param`/`@MessageBody`/`@Payload`/`@Args`, its type bucket and the metatype TypeScript emits, resolved through imports, barrels, `export type *`, default exports and tsconfig paths; **project param decorators** followed to their declaration — a wrapper that calls `Body()`/`Query()` with a pipe buckets `custom-pipe(<Pipe>)` with decorator `Name>Body`, a `createParamDecorator` that reads `.body`/`.query`/`.params` buckets `custom-pipe(none)` unless the call site passes a pipe, and the ledger prints one `custom param decorator` line per wrapper with its pipe and count), PROP rows with block flags (`validate-nested-no-type`, `type-no-validate-nested(child=X validators=N)`, `optional-admits-null`, `no-each(<IsX>)`, `array-no-max`, `initialiser(<expr>)` on a validated field), HANDLER rows (HC's flags), ENUM rows (`numeric`/`string`/`mixed`); comments and strings are masked first; stderr is the ledger (raw vs parsed param counts, every `UNPARSED` row, resolution rate, `strictNullChecks` per param) | it does **not** join a DTO field to its entity column's nullability, and does **not** read a use case's generic signature injected through the constructor (`UseCase<In, X \| null>`): §5 reads both by hand from the VB5 list. `X \| null` emits `Object` only under `strictNullChecks`; a tsconfig chain it cannot read prints `UNREAD`, never a guess. TypeScript only |
| `@darraghor/eslint-plugin-nestjs-typed` 7.5.x | the project's own eslint with `nestjsTyped.configs.flatRecommended` and `parserOptions.projectService: true` | §2 `validated-non-primitive-property-needs-type-decorator`; §6 `all-properties-are-whitelisted`, `validation-pipe-should-use-forbid-unknown` [V on 7.2.5] | misses interface / `Dto[]` bodies, implicit conversion and `@IsOptional` + `null` [V]; `validate-nested-of-array-should-set-each` is style (arrays of nested are validated anyway) [V]. `NOT-RUN` when the project has no typescript-eslint config: never install a linter into the user's tree to run it |
| Schemathesis 4.31 | `st run <spec> --url <base> --checks negative_data_rejection,positive_data_acceptance --max-examples 50 --seed 1` on a local or `--live` non-production base | §1–§4, §9 through the running app (BV-01..11) | needs a spec and a running app; flags a documented tolerant reader (B-A11); `NOT-RUN` without both |

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2-safe). Grep **N** feeds detector **§N**; F1 and grep 0 are the gates every § reads first. Every `rg` names its path — `.` or `"${ROOTS[@]}"`: given no path, `rg` reads stdin under an agent's shell and reports a silent zero. Include globs come **first**, exclusions last (the rg-traps lint, rg-glob-order). With an explicit root, globs match relative to it, so exclusions start with `**/`. Any `rg` exit 2 is a failed grep, never zero hits. A block property ("`@ValidateNested` with no `@Type`") is read by `dto-types.py` or a `-U` pattern, never by `-A<n> | rg -v` (a per-line negation cannot prove an absence: rg-context-negation).

```bash
ROOTS=(.)   # server code; in a monorepo name the apps: ROOTS=(apps/api apps/admin). Manifests and config always search .
VB="${VB:-.claude/skills/validation-boundary-scan/scripts}"; SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/vb.XXXXXX")}"; mkdir -p "$SCAN"
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,java,kt,cs,go,php,rb}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
   -g '!**/*.{spec,test,e2e-spec,stories}.*' -g '!**/test_*.py' -g '!**/*_test.go' -g '!**/*.d.ts' -g '!**/*.min.*'
   -g '!**/{migrations,migration,db/migrate,seeders,seeds}/**' -g '!**/{locales,locale,i18n,translations}/**'
   -g '!**/{openapi,swagger}*.{json,yaml,yml}' -g '!**/{docs,ai,.claude}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\[))')   # drops comment-only lines (doctrine comments were 7 of 106 @ValidateNested hits)
# F1 validator, framework and binder versions — ranges from manifests, exact from lockfiles (gate 3; V357)
rg -n --no-heading --pcre2 '"(@nestjs/(?:common|core|platform-fastify|platform-express|microservices|websockets)|class-validator|class-transformer|zod|joi|yup|valibot|ajv|fastify|@fastify/ajv-compiler|express|nestjs-i18n|nestjs-zod)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .
rg -n --no-heading --pcre2 '"node_modules/(?:@nestjs/common|class-validator|class-transformer|zod|fastify|@fastify/ajv-compiler)":\s*\{|^\s*["\x27]?/?(?:@nestjs/common|class-validator|class-transformer|zod|fastify)@\d[\w.-]*' -g '**/{package-lock.json,pnpm-lock.yaml,yarn.lock}' -g '!**/node_modules/**' .
rg -n --no-heading -i --pcre2 '^\s*["\x27]?(pydantic|pydantic-settings|djangorestframework|django|fastapi|marshmallow)\b\s*[=<>~!^]|\b(jackson-databind|spring-boot-starter-(?:web|validation))\b|github\.com/(gin-gonic/gin|labstack/echo/v4|go-playground/validator/v10)\s+v|"laravel/framework"\s*:|<PackageReference Include="(FluentValidation[\w.]*)"' -g '**/{pyproject.toml,requirements*.txt,Pipfile,poetry.lock,pom.xml,build.gradle*,go.mod,composer.json,*.csproj}' -g '!**/node_modules/**' .
# 0 THE WIRING — every pipe and its options, quoted; the bootstrap that registers it; transports that bypass it. Every later § reads this first (P5)
rg -n --no-heading -U --pcre2 '\bnew\s+\w*ValidationPipe\s*\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)|\bclass\s+\w+\s+extends\s+\w*ValidationPipe\b|\bAPP_PIPE\b|\buseGlobalPipes\s*\(|@UsePipes\s*\(|\bStandardSchemaValidationPipe\b|\bZodValidationPipe\b|\bconnectMicroservice\s*\(|\binheritAppConfig\b|@WebSocketGateway\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bajv\s*:\s*\{|\bcustomOptions\s*:|\bnew\s+Ajv\s*\(|\b(?:removeAdditional|coerceTypes)\s*:|\bsetValidatorCompiler\s*\(|\b(?:celebrate|validateRequest|zValidator|validator)\s*\(\s*\{|\bmodel_config\s*=|\bclass\s+Config\s*:|\bextra\s*=\s*["\x27](?:forbid|ignore|allow)|\bpartial\s*=\s*True\b|\[ApiController\]|\bJsonSerializerOptions\b|\bUnmappedMemberHandling\b|\bNumberHandling\b|\bInvalidModelStateResponseFactory\b|\b(?:FAIL_ON_UNKNOWN_PROPERTIES|ACCEPT_FLOAT_AS_INT|FAIL_ON_NULL_FOR_PRIMITIVES)\b|\.(?:ShouldBind\w*|Bind\w*)\s*\(|\bDisallowUnknownFields\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 'spring\.jackson\.(?:deserialization|mapper)\.[\w.-]+\s*[:=]|^\s*(?:deserialization|mapper)\s*:' -g '**/application*.{yml,yaml,properties}' -g '!**/node_modules/**' -g '!**/{test,tests}/**' .
# 1, 2, 5, 7, 9 the param types and decorator blocks: dto-types.py resolves every @Body/@Query/@Param type through imports, barrels and tsconfig paths, and reads decorator BLOCKS (never -A<n> | rg -v)
python3 -I "$VB/dto-types.py" --params --decorator-blocks --enums --flagged "${ROOTS[@]}" > "$SCAN/vb.tsv" 2> "$SCAN/vb.ledger"; echo "dto-types exit $?"; cat "$SCAN/vb.ledger"
T="$SCAN/vb.tsv"   # the § work lists: 1 bodies/queries the pipe cannot see · 2 nested, both directions · 5 optional-admits-null on Update/Patch DTOs first · 7 named primitives with no pipe · 9 arrays
awk -F'\t' '$1=="PARAM" && $3!="Param" && $4=="-" && $7 !~ /^custom-pipe/ {print "VB1", $2, $3, $6, $7, $8}' "$T"
awk -F'\t' '$1=="PARAM" && $7=="custom-pipe(none)" {print "VB8-custom", $2, $3, $6}' "$T"   # a createParamDecorator over req.body/query with no pipe; custom-pipe(<Pipe>) rows are one wiring read each (the ledger's `custom param decorator` lines)
awk -F'\t' '$1=="PROP" && $5 ~ /validate-nested-no-type|type-no-validate-nested/ {print "VB2", $2, $3, $5}' "$T"
awk -F'\t' '$1=="PROP" && $5 ~ /optional-admits-null/ {n++; if ($3 ~ /^[A-Za-z]*(Update|Patch|Edit|Change|Rename|Set)[A-Za-z]*\./) {u++; print "VB5", $2, $3, $4}} END {print "VB5 optional-admits-null:", n+0, "props;", u+0, "on Update/Patch DTOs (listed)"}' "$T"
awk -F'\t' '$1=="PARAM" && $4!="-" && $7 ~ /primitive|union/ && $10=="-" {if ($3=="Param" && $6=="string") p++; else print "VB7", $2, $3, $4, $6} END {print "VB7 named path params typed string with no pipe:", p+0, "(a path segment is always a string: read only for a format the column needs)"}' "$T"
awk -F'\t' '$1=="PROP" && $5 ~ /no-each|array-no-max/ {print "VB9", $2, $3, $5}' "$T"
awk -F'\t' '$1=="ENUM" && $4=="numeric" {print "VB4-enum", $2, $3}' "$T"
# 2 (Spring) a nested DTO field or List element with no @Valid on the line above; the @RequestBody with no @Valid
rg -n --no-heading -U --pcre2 '^(?![ \t]*@Valid\b)[^\n]*\n[ \t]*(?:private|protected|public)?\s*(?:final\s+)?(?:List|Set|Collection)<(?!@Valid\b)[A-Z]\w*(?:Dto|Request|Command|Input|Item|Line)>\s+\w+\s*[;=]|@RequestBody\s+(?!@Valid\b|@Validated\b)(?:final\s+)?[A-Z]\w*\s+\w+' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\bList<|\bSet<|\bCollection<|@RequestBody'
# 3 conversion before validation; the copy the handler receives
rg -n --no-heading --pcre2 '\benableImplicitConversion\s*:\s*true\b|@Type\s*\(\s*\(\)\s*=>\s*(?:Boolean|Date)\s*\)|\btransform\s*:\s*false\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
echo "@Type(() => Number) fields: $(rg -c --no-heading --pcre2 '@Type\s*\(\s*\(\)\s*=>\s*Number\s*\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}')   (read only beside an empty-string-sensitive bound: Number(\"\") is 0)"
# 4 coercion per validator and in env loaders (4a schema coercion, 4b hand parses of request values, 4c binder tags, 4d env parses)
rg -n --no-heading --pcre2 '\bz\.coerce\.(?:boolean|number|bigint|date|string)\s*\(|\bcoerceTypes\s*:|\bconvert\s*:\s*true\b|\bJoi\.boolean\(\)\.truthy\(|\bstringbool\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\b(?:parseInt|parseFloat|Number|Boolean)\s*\(\s*(?:req|request|ctx\.request|c\.req)\.(?:query|params|body|headers)\b|!!\s*(?:req|request)\.(?:query|body)\.' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '^\s+\w+\s+(?:u?int(?:8|16|32|64)?|float(?:32|64)|bool)\s+`[^`\n]*binding:"[^"\n]*\brequired\b' -g '*.go' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bbool\s*\(\s*os\.(?:getenv|environ)|!!\s*process\.env\.|\bprocess\.env\.\w+\s*===?\s*["\x27](?:true|false|1|0)["\x27]|\b(?:parseInt|Number)\s*\(\s*process\.env\.|\bif\s*\(\s*process\.env\.\w+\s*\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 5 the join dto-types does NOT do: column nullability (5a) and the use-case guard that lets null through (5b); pydantic Optional with no default, Spring required=false (5c)
rg -l --pcre2 '@Entity\s*\(|^model\s+\w+\s*\{|\bclass\s+\w+\s*\(\s*(?:models\.Model|Base|DeclarativeBase|SQLModel)\b' -g '*.{ts,prisma,py}' "${X[@]}" "${ROOTS[@]}" | wc -l   # entity files: each 5 candidate is joined to its column there (MikroORM/TypeORM nullable, Prisma ?, Django null=)
rg -n --no-heading --pcre2 '\b(?:dto|data|input|body|cmd|command|patch|payload)\.\w+\s*!==?\s*undefined\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | wc -l   # guards that let null through; read the one each VB5 field reaches (5b)
rg -n --no-heading --pcre2 '^\s+\w+\s*:\s*(?:Optional\[[^\]\n]+\]|[\w.\[\]]+\s*\|\s*None)\s*$|@RequestBody\s*\(\s*required\s*=\s*false\s*\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 6 unknown-key policy outside the Nest pipe (6a schema-level, 6b Fastify route schemas, 6c Go request-body decoders with no DisallowUnknownFields — a provider-response decoder is a tolerant reader, 6d echo Bind, 6e Laravel all() beside a FormRequest)
rg -n --no-heading --pcre2 '\.(?:passthrough|strict|strip|nonstrict)\s*\(\s*\)|\b(?:looseObject|strictObject)\s*\(|\ballowUnknown\s*:|\.unknown\s*\(\s*(?:true)?\s*\)|\bnoUnknown\s*\(|@JsonIgnoreProperties\s*\(\s*ignoreUnknown\s*=\s*true' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '\b(?:body|querystring|params)\s*:\s*\{\s*(?:\$ref|type)\b|\bschema\s*:\s*\{\s*(?:body|querystring)\b' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -c --pcre2 '\badditionalProperties\s*:\s*false'   # route schemas only (LLM tool schemas also say additionalProperties)
rg -l0 --pcre2 '\bjson\.NewDecoder\s*\(\s*(?:(?:http\.MaxBytesReader|io\.LimitReader)\s*\(\s*(?:\w+\s*,\s*)?)?(?:r|req|request|c\.Request|c\.Request\(\)|ctx\.Request\(\))\.Body\b' -g '*.go' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\bDisallowUnknownFields\s*\('
rg -n --no-heading --pcre2 '\bc\.Bind\s*\(' -g '*.go' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '\bextends\s+FormRequest\b|\b\w+Request\s+\$request\b' -g '*.php' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\$request->(?:all|input)\s*\(\s*\)' | "${NC[@]}"
# 8 contexts the global pipe never reaches: custom param decorators (8a; dto-types already followed every one used on a param: VB8-custom above), Nest 12 schema bodies (8b), raw adapter routes (8c), gateway and consumer files that take messages with no pipe (8d)
rg -n --no-heading --pcre2 '\bcreateParamDecorator\s*\(|\bvalidateCustomDecorators\b|@(?:Body|Query|Param)\s*\(\s*\{\s*schema\b|\bgetHttpAdapter\s*\(\s*\)\s*\.\s*(?:get|post|put|patch|delete|all)\s*\(|\b(?:getInstance|getHttpAdapter\(\)\.getInstance)\s*\(\s*\)\s*\.\s*(?:get|post|put|patch|delete|route)\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '@SubscribeMessage\s*\(|@(?:MessagePattern|EventPattern)\s*\(' -g '*.ts' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '@UsePipes\s*\(|\bValidationPipe\b'
# 9 validation groups that skip un-grouped validators (arrays: the VB9 list above)
rg -n --no-heading --pcre2 '@\w+\s*\([^\n]*\bgroups\s*:\s*\[|\bvalidat(?:e|eSync|eOrReject|orOptions)\b[^\n]*\bgroups\s*:|\b(?:always|strictGroups)\s*:\s*true\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

When `python3` is absent, §1, §2, §5, §7 and §9 print `blocked (python3 absent)`; never fall back to a one-line regex for a two-step or block question.

### Measured (2026-10-14)

- **Real repo, read-only, full tree** (a NestJS 11 monorepo on Fastify with MikroORM, 3,722 `.ts` files under the API's `src`, `ROOTS=(apps/api/src)`; pnpm workspace with its lockfile and `tsconfig.base.json`): the block runs in about 4.5 s (`dto-types.py` 3.3 s) and prints 68 lines, 0 `rg` errors, 0 files written into the tree. F1 read the lockfile only after the lockfile regex learned pnpm 9's indented, single-quoted keys (`  '@nestjs/common@11.2.6':`): Nest 11.2.6, class-validator 0.15.1, class-transformer 0.5.1, Fastify 5.12.3, zod 4.5.4 — before that fix it printed nothing on a lockfile that was there. Grep 0 printed the one global pipe (an `APP_PIPE` i18n `ValidationPipe` subclass with `{ transform: true, whitelist: true }`). `dto-types.py`: 1,374 params of 1,374 raw hits, 0 `UNPARSED`, `strictNullChecks` on for all 1,374 (read through `tsconfig.base.json`), every named type resolved once `export type *` re-exports were followed (10 had failed before). **748 of the 758 bodies and queries go through two project decorators** — `@ContractBody(schema)` (493) and `@ContractQuery(schema)` (255), each a wrapper that calls `Body(new ContractPipe(schema))` / `Query(…)` with a zod pipe — and bucket `custom-pipe(ContractPipe)`; before the script followed project decorators, the ledger saw 626 params and §1/§8 undercounted every one of them. The pipe was read once: zod strips unknown keys (one §6 wiring row, the same policy as `whitelist`), an absent body parses as `{}`, a refusal is the global pipe's own exception (same 400 envelope). **VB1** 12 rows, all B-D1 (OAuth and MCP protocol endpoints with `unknown` bodies and `Record` queries); the earlier copy's TRUE row (`@Body() dto: X | null`) is gone — that route now takes its body through the contract pipe. **VB2** 0, **VB5** 2 props (0 on Update/Patch DTOs), **VB9** 0: only 2 class-validator body DTOs remain. **VB7** 11 listed + 36 path strings counted. Grep 3: 0 implicit conversion, 0 `@Type(() => Number)`. Grep 8: 3 `createParamDecorator` — all return the principal or an auth flag, so dto-types printed no `VB8-custom` row. An earlier copy of this repo (no lockfile, no `tsconfig.base.json`, class-validator DTOs) measured 1,365 params, VB1 13 → 1 TRUE, VB2 2 TRUE, VB5 1 TRUE; those DTOs have since moved to the contract package. Re-read at HEAD, all three are gone: the union-body route, the two `@Type`-only nested DTOs (the nested `orderId` is now an id schema) and the `@IsOptional` name (now `.optional()`, which refuses `null` — a probe on zod 4.6.7, not the locked 4.5.4, answered `invalid_type` for `{"name": null}`) each parse through the contract pipe.
- **Research labs** (the NestJS 12.1.3 probes and the grep sample with paired POS/NEG lines): every validation POS found — interface, `Dto[]`, `type` alias, `Partial<Dto>` and `any` bodies (VB1), `@ValidateNested` without `@Type` (VB2), `@IsString` on `string[]` without `each` (VB9), a named primitive body (VB7), `enableImplicitConversion: true` and `@Type(() => Boolean | Date)` (grep 3), `z.coerce.boolean/number` (grep 4), a grouped validator (grep 9), a numeric enum (VB4-enum); the NEG lines (a class body, `@ValidateNested @Type` together, `PartialType`) stayed quiet.
- **Fixtures** (`benchmarks/fixtures/*` with NestJS code; none seeds a VB class yet — the `backend-defects` fixture is a later build item): `vuln-fullstack` 11 VB1 rows (inline-object, interface and `Record` bodies on Nest 10 — true in VB terms, graded in that fixture by security), 4 VB5 on an Update DTO; `slow-marketplace` 3 VB1 (two interface bodies, one `Buffer`); `quality-mix` 3 VB1; `obs-defects` 2 `UNRESOLVED` (the type's module is absent from the fixture — reported, never guessed).
- **`backend-defects` fixture** (2026-10-14, after the fixture's IR-7): 6c names request-body decoders only (`r.Body`, `c.Request.Body`, through `MaxBytesReader`/`LimitReader`). It lists 2 Go handler files, BD-VB-6b and the BD-DECOY-08 tolerant webhook reader (the internal ops port sets `DisallowUnknownFields`). It no longer lists the `upstream/catalog.go` provider-response decoder.

## The 3,000-hit path

The wiring row decides most of a large run (P5). A global pipe with `whitelist` and no `forbidNonWhitelisted` is **one** §6 row with N routes; a global `enableImplicitConversion: true` is one §3 row. Then, in order: VB1 and VB2 rows (each a whole DTO that never validates — read all, they are few); VB5 grouped by DTO class, Update/Patch DTOs on public and money routes first, one representative field per class taken to the column and the use case; VB7 rows on Body and Query; VB9 grouped by DTO. A group may be closed with **one cited reason** (`41 array-no-max: 38 bounded by a kernel cap at file:line, 3 read`) when the reason is checked, not assumed. Shipped DTOs are never bulk-closed by name.

## Scans for

| § | Class (research id) | Default severity | Oracle |
|---|---|---|---|
| 1 | the pipe sees no class (BV-01) | high on a write route, medium on a read | V340 |
| 2 | nested never validated, both directions (BV-02, BF-SP-02) | high | V340 |
| 3 | conversion before validation; validated copy ≠ handler copy (BV-03/04) | high for a boolean filter or permission, else medium | V341 |
| 4 | coercion per validator and env loader (BV-07/11/12, BM-03, BN-07, BC-02, BF-SP-03, BF-NET-02/03, BF-GO-02/06) | high on qty, cents, booleans that gate; else medium | V341 |
| 5 | optional admits null; pydantic `Optional` required; `required=false` bodies (BV-05, BF-FA-01, BF-SP-05) | high on a 500 or a cleared value, else medium | V342 |
| 6 | unknown-key policy silently wrong (BV-06, BF-GO-02/07, BF-LA-01) | medium | V343 |
| 7 | named primitive param bypasses the pipe (BV-08) | high where it reaches a query builder (→ security), else medium | V340 |
| 8 | contexts the pipe never reaches (BV-09) | high | V340 |
| 9 | arrays and validation groups (BV-10/13) | medium | V344 |

Every lane row that rests on a framework default also carries V357: the oracle ran on the installed version and the finding states it.

### 1. The pipe sees no class

```
BAD:   @Body() dto: UpsertPriceListDto | null        // TS emits Object for a union under strictNullChecks: nothing validates, whitelist strips nothing
       @Body() input: CreateOrderInput  (interface) · @Body() items: OrderDto[] · @Body() p: Partial<OrderDto> · @Query() q: Record<string, string>
GOOD:  @Body() dto: UpsertPriceListDto               // a class; nullability decided by the DTO, not the param
       @Body(new ParseArrayPipe({ items: OrderDto })) items: OrderDto[]   ·   @Body() dto: UpdateOrderDto  (PartialType(OrderDto) is a class)
```
**Read the code:** what does the VB1 row's metatype column say — `Object`, `Array`, `UNREAD(strictNullChecks)`? For a union, is `strictNullChecks` on in the chain the app compiles with (with it off, `X | null` emits `X` and validates)? Is the body a deliberate protocol endpoint (RFC 7591/6749 OAuth, JSON-RPC) with a hand parser that bounds **every** field (B-D1, cite the parser)? An inline-object type (`{ email: string }`) is the same class. A `custom-pipe(<Pipe>)` row is **not** a §1 row (B-D16): a project decorator such as `@ContractBody(schema)` hands the body to its own pipe (a zod or schema pipe), and the global pipe's skip does not matter — read that pipe **once**, as a wiring row beside grep 0 (P5): what it parses with, its unknown-key policy (§6), what it does with `null` and an absent body (§5), and whether its refusal reaches the project's error envelope (`edge-error-scan` §6). **Finding when** a client-reachable body or query reaches the domain with no validation of a field the DTO meant to check. **Proof:** V340 — a wrong-typed required field and an unknown key through the real bootstrap → 400; or tier S, `Reflect.getMetadata('design:paramtypes', Controller.prototype, '<handler>')` printing `Object`.

### 2. Nested never validated — both directions

```
BAD:   @ValidateNested() address: AddressDto;                       // no @Type: children never checked
       @Type(() => OrderKeyDto) orders!: OrderKeyDto[];            // no @ValidateNested: the child's @IsUUID never runs
       private List<LineDto> lines;   (Spring, no @Valid)
GOOD:  @ValidateNested({ each: true }) @Type(() => OrderKeyDto) orders!: OrderKeyDto[];   ·   private List<@Valid LineDto> lines;
```
**Read the code:** `type-no-validate-nested(child=X validators=N)` names the child and how many validators it carries — N = 0 means nothing is lost. Does the parent reach a route through a re-export (`export { A as B }`)? Free-form `@IsObject()` metadata is a decoy. **Finding when** the child carries validators and a route accepts the parent. **Proof:** V340 — `{"orders":[{"orderId":"x"}]}` → 400 naming `orders.0.orderId`.

### 3. Conversion before validation; the copy the handler receives

```
BAD:   new ValidationPipe({ transform: true, transformOptions: { enableImplicitConversion: true } })   // "false" → true, "" → 0, 5 → "5" passes @IsString
       @Type(() => Boolean) @IsBoolean() active: boolean      // ?active=false turns the filter ON
       new ValidationPipe({ whitelist: true }) + @Type(() => Number) page   // transform off: the handler gets the RAW string "2"
GOOD:  @Transform(({ value }) => value === 'true') @IsBoolean() active: boolean   ·   transform: true with explicit @Transform per boolean
```
**Read the code:** does every boolean query field carry an explicit `@Transform`? With `transform` off and more than one validator option set, the pipe hands the handler `classToPlain(instance)`, otherwise the raw value — which does this pipe do [V 12.1.3 source]? `@Type(() => Date)` accepts `"2026-02-30"` and rolls to March 2 — that row is graded in `wire-format-scan` §6 (time input binding, V310), listed here with `→ wire-format-scan §6` and never graded twice; dates kept as strings with `@IsISO8601` are the decoy, B-D12. **Finding when** a value the client sent as false, empty or invalid reaches the handler as true, 0 or a valid value. **Proof:** V341 — `GET ?active=false` → the handler sees `false`; `{"name": 5}` → 400.

### 4. Coercion per validator and env loader

The table is the variant list; every row is from a run unless tagged.

| Validator (version) | bool `"false"` | number `""` | `null` → number | `"12"` → int | `3.7` → int | unknown key |
|---|---|---|---|---|---|---|
| class-validator via Nest pipe, no implicit conversion (0.15.1 / 12.1.3) | 400 (`@IsBoolean` on a string) | 400 | `@IsOptional` skips it | 400 on `@IsInt` | 400 | kept; `whitelist` strips; `forbidNonWhitelisted` 400 |
| same + `enableImplicitConversion` | **`true`** | **`0`** | — | 12 | — | as above |
| zod 4.6.7 `z.coerce.*` | **`true`** (also `"0"`) | **`0`** | **`0`**; `coerce.date(null)` = epoch | 12 | — | stripped; `strictObject` throws |
| zod 4 `z.stringbool()` | `false` | — | — | — | — | — |
| Fastify 5.12.7 ajv defaults | `false` (`"0"` rejected) | 400 | **`0`** / **`false`** | 12 | 400 (`1.5` on integer) | **removed silently** with `additionalProperties:false`, kept without |
| joi 18.2.9 (`convert: true`) | `false`; `"no"` rejected | rejected | — | 42-style accepted | — | **rejected** |
| pydantic 2.14.1 | `False` (also `"0"`, `"no"`, `"off"`) | rejected | rejected | 12 (also `"12.0"`) | rejected (`12.5`); **`True` → 1** | ignored (`extra='ignore'`) |
| DRF 3.18.3 | `False` (also `"0"`, `"no"`, `"off"`) | rejected | rejected | 3 (also `"3.0"`) | rejected | **dropped silently** |
| Jackson 2.20.1, Boot-like mapper | — | — | missing primitive → **0** | 3 | **3** | ignored |
| System.Text.Json web defaults [K] | — | — | missing value type → **0** | 12 (numbers from strings) | — | ignored |
| Go `encoding/json` / gin | — | — | missing → **0** | — | `19.99` into `int64` → error | ignored; gin `required` fails on `0`/`false` |
| Env: `bool(os.getenv)` / `!!process.env.X` | **True** / **true** | `Number("")` = 0 | — | `parseInt("10ms")` = 10 | — | — |

```
BAD:   active: z.coerce.boolean()  ·  FEATURE_X: !!process.env.FEATURE_X  ·  bool(os.getenv("PAYMENTS_ENABLED"))
       @IsEnum(Status) status  (numeric TS enum: the KEY "Active" validates through the reverse mapping)
       int qty;  (Jackson, ACCEPT_FLOAT_AS_INT on)  ·  Qty int `binding:"required"`  (gin: 0 rejected)
GOOD:  z.stringbool()  ·  a string enum or @IsIn([...values])  ·  Integer qty + @NotNull + ACCEPT_FLOAT_AS_INT off  ·  Qty *int `binding:"required"`
```
**Read the code:** which values of the V341 table can reach this field (body, query, params, headers, form)? An env loader read once at boot where empty cannot occur by deployment config is a decoy (B-A13); a schema loader (pydantic-settings, envalid, zod 4 `stringbool`) parses correctly. **Finding when** a value from the table reaches the handler as a different typed value with 2xx. **Proof:** V341 — each value rejected or becoming the documented value; env strings into the project's loader at boot.

### 5. Optional admits null

```
BAD:   @IsOptional() @IsString() name?: string;   +   if (dto.name !== undefined) product.rename(dto.name)   // {"name": null} → name.trim() → 500
       x: Optional[int]   (pydantic v2: required, no default)  ·  @RequestBody(required = false) Order o
GOOD:  @IsAbsentOr() @IsString() name?: string    // ValidateIf(v => v !== undefined): absent allowed, null refused
       @IsOptional() @IsString() @ValidateIf(o => o.name !== null) name?: string   ·   x: Optional[int] = None
```
**Read the code** (the join `dto-types.py` does not do): from each VB5 field, find the entity column (MikroORM/TypeORM `nullable`, Prisma `?`, Django `null=`) and the guard the use case applies (5b: `!== undefined` lets `null` through, `!= null` does not). Does a use case reached through a constructor-injected `UseCase<In, Out>` re-validate the field? Is `null` a documented "clear" (B-A5, B-G23)? **Finding when** `null` reaches a NOT NULL write or a method on the value (500), or silently clears a field the API does not document as clearable. **Proof:** V342 — PATCH `{"<field>": null}` → 400 (or the documented clear), never 500.

### 6. Unknown-key policy silently wrong

```
BAD:   new ValidationPipe({ whitelist: true })          // {"discountCode": "X", "dicsountCode": "Y"} → the typo is stripped, 200 with the default
       body schema with additionalProperties:false on Fastify (stripped, not rejected)  ·  json.NewDecoder(r.Body).Decode(&in)  ·  echo c.Bind (body id overrides path id)
GOOD:  whitelist + forbidNonWhitelisted: true  ·  ajv customOptions { removeAdditional: false }  ·  dec.DisallowUnknownFields()  ·  a documented tolerant reader
```
**Read the code:** what does the API document — reject (Azure) or tolerate (Zalando), B-G17? Go 6c lists request-body decoders only (`r.Body`, `c.Request.Body`, through `MaxBytesReader`/`LimitReader`); a decoder of a provider's response is a tolerant reader, never this §. Nest's pipe turns `forbidUnknownValues` off unless passed: is `validate()` ever called on a plain object, or with a group that has no validators (§9)? **Finding when** an undocumented silent drop changes behaviour (a misspelled optional field falls back to its default with 200), or two routes of one API disagree. A documented tolerant reader is Refuted (B-A11). **Proof:** V343 — a valid body plus `{"typoField": 1}` at top level, nested and inside array items → the documented policy, identically.

### 7. Named primitive param bypasses the pipe

```
BAD:   @Body('sku') sku: string            // {"sku": {"$gt": ""}} arrives as an object: the pipe skips String metatypes
       @Query('status') status: string     // Fastify: ?status=a&status=b arrives as string[]
GOOD:  @Body() dto: SkuDto  ·  @Query('status', new ParseEnumPipe(Status)) status: Status  ·  an assert*() guard before use (B-D10)
```
**Read the code:** does a guard run before any use? Does the value reach a query builder (route the operator reading to security `injection-scan` §3, P3)? Path params are always strings: the VB7 count line is read only where the column needs a format (a UUID column given `x` is `edge-error-scan` §2's 500). **Finding when** an object or array reaches code that assumes a scalar. **Proof:** V340 — the object and the repeated key through the real app → 400.

### 8. Contexts the pipe never reaches

```
BAD:   app.connectMicroservice(opts)                 // no { inheritAppConfig: true }: global pipes do not apply to the transport
       @SubscribeMessage('x') handle(@MessageBody() m: Dto)   // gateway with no @UsePipes
       @CurrentUser() custom decorators with client input  ·  @Body({ schema }) on Nest 12 without StandardSchemaValidationPipe  ·  app.getHttpAdapter().post(...)
GOOD:  connectMicroservice(opts, { inheritAppConfig: true })  ·  @UsePipes(pipe) on the gateway  ·  validateCustomDecorators: true where a decorator returns client data
```
**Read the code:** does the transport take messages from outside the trust boundary? A push-only gateway, or a custom decorator returning the authenticated principal, is not input (dto-types prints no row for a `createParamDecorator` that reads only `.user`). A `VB8-custom` row is a `createParamDecorator` that returns `req.body`/`.query`/`.params` with no pipe at the call site: the global `ValidationPipe` skips it unless `validateCustomDecorators: true` is in the grep-0 options. A trusted internal producer is a decision to record. **Finding when** an external payload reaches a handler through a context the pipe does not cover. **Proof:** V340 — an invalid message through each real transport → rejected.

### 9. Arrays and validation groups

```
BAD:   @IsString() tags: string[]               // no { each: true }: VALID input rejected
       ids: string[]  (no @ArrayMaxSize)  ·  @IsInt() @Max(10) qty + validate(o, { groups: ['create'] })   // un-grouped validators skipped
GOOD:  @IsString({ each: true }) @ArrayMaxSize(100) tags: string[]  ·  groups with always: true, or no groups
```
**Read the code:** does the one-value query form (`?ids=1`) and the many form (`?ids=1&ids=2`) reach the handler as the same type? Is the array bounded upstream (a kernel cap)? **Finding when** valid input is rejected, a group lets an invalid value through, or one and many disagree. Size as a DoS is performance's (§ Boundaries). **Proof:** V344 — `[]`, one, many, over-max; every group with an invalid value.

## Output

```
validation-boundary-scan — lanes: nestjs 11.2.6 on fastify 5.12.3, class-validator 0.15.1, zod 4.5.4 (pnpm-lock.yaml) · Nest 11 not run by the research: its default rows stay Unconfirmed (V340/V341)
Wiring: APP_PIPE src/app.module.ts:190  I18nValidationPipe { transform: true, whitelist: true }  (forbidNonWhitelisted absent; forbidUnknownValues forced off)
        @ContractBody / @ContractQuery → ContractPipe src/shared/contract.pipe.ts:16 (zod safeParse; unknown keys stripped; an absent body parses as {}; refusal → the same 400)
Tools: dto-types ran (1,374/1,374 params, 0 UNPARSED, strictNullChecks on ×1,374; 748 custom-pipe(ContractPipe)) · nestjs-typed NOT-RUN (no typescript-eslint config) · schemathesis NOT-RUN (no running app)

Findings: 0 · Unconfirmed: 1

1. src/app.module.ts:190 + src/shared/contract.pipe.ts:16 (748 contract params, 2 class bodies)    Unconfirmed  medium
   §6 — unknown keys are stripped, never refused (whitelist without forbidNonWhitelisted; zod's default strip): a misspelled optional
   field is dropped and its default applied. Read: the API's stated policy (B-G17). Settling: V343 — {"typoField": 1} at top level, nested and in array items.

Verification: 26 candidates → 0 findings · 1 unconfirmed · 25 refuted (self-verified; 12 B-D1, 11 B-D10, 2 read to depth)

Class coverage:
  §1 pipe sees no class        checked (12 → 0; 12 B-D1: OAuth and MCP protocol endpoints with unknown bodies and Record queries)
  §2 nested                    checked (0 in either direction; the nested ids are contract schemas)
  §3 conversion first          checked (0 implicit conversion, 0 @Type(Boolean), 0 @Type(Number))
  §4 coercion                  checked (1 numeric enum, never in @IsEnum → 0; 0 z.coerce; env: → devops deploy-safety-scan §6 (0))
  §5 optional admits null      checked (2 props, 0 on Update/Patch DTOs → 0; contract .optional() refuses null)
  §6 unknown keys              checked (2 wiring rows → 1 unconfirmed)
  §7 named primitives          checked (11 + 36 path strings → 0; 11 B-D10) · → security injection-scan §3 (0)
  §8 other contexts            checked (3 param decorators, all principal → 0; 1 gateway, push-only → 0)
  §9 arrays / groups           checked (VB9 0: 2 class-validator body DTOs left; contract arrays read in their schemas) · → performance request-path-scan §13 (0)
```

`[report-with-fix]`: the oracle failed through the real bootstrap on the installed version and the fix is local to the project's pipe, DTO base or local validator. `[report-flagged]`: one link is unproven (no oracle run, `strictNullChecks` or the version `UNREAD`, the column not read); the row names it and the settling request. The coverage block lists **all nine** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep or tool>)`, `→ <owner> (k)` or `Live, unreviewed (k groups / n hits)`. A missing line is printed by `/backend-audit` as `not run`.

## False positives / precedents

The verifier reads [`precedents/backend.md`](../../../../snippets/precedents/backend.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **B-D1** a deliberate `unknown` body or a `Record` query on a protocol endpoint with a bounding hand parser; **B-D7** a unit test that builds its own pipe with the same options while the e2e harness imports the real module; **B-D10** a named primitive param followed by an `assert*()` guard or a registry lookup.
- **B-D12** dates kept as strings with `@IsISO8601`; **B-D13** initialisers on query DTOs (an initialiser on an Update DTO is `http-contract-scan` §5); **B-D16** a body parsed by a project schema pipe (`custom-pipe(<Pipe>)`): one wiring read, not N §1 rows.
- **B-A11 / B-G17** a documented tolerant reader; **B-A13** coercion in env parsing at boot; **B-A16** `req.body as Foo` is code-quality's; **B-A5 / B-G23** `null` as a documented clear.
- **P2** every finding shows the payload; **P3** "an attacker can…" goes to security; **P4** prove on the pipe and adapter that ship; **P5** one finding at the pipe, N routes.

Shapes this skill must not report: `PartialType(Dto)` bodies (a class); `@IsObject()` free-form metadata without `@Type`; a `Buffer` body on a raw upload route (the upload is `file-access-scan`'s); arrays of nested without `each` (validated anyway); a push-only gateway; `createParamDecorator` returning the authenticated principal.

## When to run

- On any diff that touches a DTO, a controller signature, the pipe or its options, the Fastify/ajv options, a validator schema, a serializer's input fields, a binder setting or an env loader — `/backend-audit`'s "a DTO, pipe or validator file" signal.
- On every whole-repo `/backend-audit`, reporting all nine §s; before upgrading Nest, class-validator, zod, pydantic, Jackson or Fastify across a major (V357); after `/add-endpoint`, whose gate cites V340 and V342.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets part A (the wiring row), part B (the version line), the dto-types row and the payload — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/backend.md`. Under `/backend-audit` that is `@api-reviewer` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Halt before any § when grep 0 is unread.** A verdict on a DTO without the pipe that validates it is invalid; when the pipe is built in a function grep 0 cannot see, read the bootstrap by hand and quote the options.
- **Halt on any finding missing its anchors:** the param or property `file:line`, the wiring row, the version, the payload, the fix in the project's own primitive.
- **No `[report-with-fix]` without V340–V344 through the project's own bootstrap** on the installed version (or a two-ended static fact). A hand-built pipe, `Fastify()` or `express()` in a test is not one.
- **No proposed fix may hide the class:** never `whitelist: false`, never add `@IsOptional` to quiet a 400, never `enableImplicitConversion` to make a query DTO pass, never `@Allow()` on a field to survive `forbidNonWhitelisted`.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "validation looks fine"** without the coverage block; a § whose grep or script did not run is `blocked`, never `checked`.

## Related

- `/backend-audit` dispatches this skill and folds its coverage block into its validation ledger rows; `/backend-fix` closes findings failing-first through the real bootstrap and re-runs this detector.
- `http-contract-scan`, `edge-error-scan`, `wire-format-scan` and `api-consistency-audit` (this pack) are the neighbours named in § Boundaries; `endpoint-test-method` (this pack) drives the V340–V344 requests against a running app; `@api-reviewer` judges these rows.
- security `injection-scan` §3/§12 and `logic-race-scan` §1/§2, code-quality `type-safety-scan` §1, performance `request-path-scan` §11/§13 and devops `deploy-safety-scan` §6, when those packs are installed.

## Sources

Defaults tagged `[V]` were run: NestJS 12.1.3 with class-validator 0.15.1 and class-transformer 0.5.1 on both adapters, Fastify 5.12.7 (`@fastify/ajv-compiler` 4.0.7 `lib/default-ajv-options.js`), zod 4.6.7 and 3, joi 18.2.9, yup 1.7.1, ajv 8.20.0, `@darraghor/eslint-plugin-nestjs-typed` 7.2.5, Jackson 2.20.1, Go 1.27.2, gin v1.12.0, echo v4.16.0 (backend research notes A and B, labs A and B, 2026-10-14; Nest's `validation.pipe.js` read there for `forbidUnknownValues`, `toValidate()` and the transform-off return). pydantic 2.14.1 and DRF 3.18.3 / Django 6.1.2 rows were re-run for this skill on 2026-10-14 (bool, int, unknown-key and null probes). `[K]` rows (Spring `@Valid` nesting, System.Text.Json web defaults, Laravel Form Requests) are from the vendors' documentation as read by the research; `[K?]` Jackson 3 / Boot 4 defaults are secondary. Nest 11 was not run. The real-repo counts are from a read-only run on 2026-10-14 (batch-5 eval § 3, re-measured here with the block above). Paraphrased; no text reproduced beyond identifiers.
