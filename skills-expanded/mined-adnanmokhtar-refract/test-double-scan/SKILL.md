---
name: test-double-scan
description: Find test doubles that lie — the code under test mocked, untyped or loose doubles, mocks of libraries the project does not own, emulated databases, test seams and test-input special cases in shipped code — each proved by a typed double, the real engine or a broken SUT.
kind: skill
pack: testing
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: test-double-scan

## Premise

A test double stands in for something real so a test can be fast and focused. It lies in two ways. It can stand in for the **code under test** itself, so the test exercises the double and cannot fail whatever the code does. Or it can stand in for a **collaborator** while drifting from it — a method renamed on the real interface still "works" on a loose double, a mocked ORM answers in a way the real one never does, an in-memory database accepts the duplicate key Postgres rejects. Both pass green while production breaks. A third lie runs the other way: **production code that knows it is under test** — a `NODE_ENV === 'test'` branch, a literal copied from a test, an `__eq__` that always answers `True` — so the suite measures a path production never takes. In ImpossibleBench (arXiv 2510.20270, 2025-10-23), OpenAI models that cheated on impossible tasks mostly did it through operator overloading, recorded state and special-cased inputs, and LLM monitors caught only 42–65% of cheats on SWE-style tasks; the class is mechanical to find and mechanical to prove.

**Every finding cites the double or seam at `<file:line>` + the test(s) that rely on it + what it hides (the SUT, a drifted signature, an engine semantic, a production path) + the proof (or the probe that would settle it) + the fix.** A grep hit is never a finding by itself. "No lying double found" is never printed without the class-coverage block (§ Output).

**Detect statically, prove by execution.** Each class has a deterministic oracle in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Testing: break the SUT and watch the test stay green (§ 1); type the double against the real interface and watch the compiler or `spec` name the drift (§ 2–3); run the same test on the production engine (§ 4); run the production path with the test flag off (§ 5); feed the neighbouring input and watch the special case fall off (§ 6). A candidate with no harness to run its oracle is **Unconfirmed**, carrying the exact command.

## The rule

A double or seam is a finding when all four hold:

1. **A test relies on it for its verdict.** The double sits on the path from the test's input to its assertion; a mock of a module the test never exercises (a mailer, analytics) is isolation, not a lie.
2. **It can disagree with the real thing.** The SUT is replaced; or the double's shape is unchecked (no type, no `spec`, a cast through `unknown`); or the fake engine lacks a semantic the code uses (a constraint, a lock, a commit hook); or shipped code branches on being tested.
3. **Nothing already pins the real behaviour.** Search every layer for another test that exercises the real collaborator or engine on the same behaviour — an integration or e2e test on Testcontainers covers what a unit test's ORM mock cannot. Name that test before demoting.
4. **The oracle fires.** The probe in the class's **Proof** line shows the disagreement.

## Boundaries

- **Interaction-only assertions** (`toHaveBeenCalled` where an outcome exists, `verify(…, any())`) → `assertion-strength-scan` § 2, and **a stub's value echoed back through a SUT that transforms it** → `assertion-strength-scan` § 5. The double is fine there; the assertion is weak.
- **Consumer–provider contracts** (no Pact, pacts never verified, no `can-i-deploy`, an ungated schema change) → `contract-test`; a consumed API with no contract test at all → `coverage-gap` § 6. Here: a frontend or service mock body that is **not typed or validated** from the schema (§ 3d).
- **Concurrency invariants with only single-threaded tests** (a lost update or double spend never raced) → `coverage-gap`, with the oracle in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Invariant under concurrency; the database pack owns the production defect when installed.
- **A service with a database and no integration test at all** → `coverage-gap` § 5. **Shared or invalid fixtures** → `flake-source-scan` § 5 and `test-factories`. **Snapshot misuse** → `assertion-strength-scan` § 6.
- **On a diff**, the repo-baseline's `.claude/scripts/test-integrity.py` (when installed) is the owner of weakening in the change — but its v1 names `NODE_ENV === 'test'` branches and equality overrides as **not covered**. So § 5 and § 6 run on the diff too; dedupe by `<file:line>` with any row it does report.

## Adapt to the codebase — the lane table

Read the mock library, the runner and the ORM **with versions** from the lockfile, and the production engine from compose, Terraform or the ORM config ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, grep G1). Print the lanes you ran in the output header.

| Lane | Checked double (the fix) | Unchecked shape (the candidate) | Real engine / real dependency | Schema-checked HTTP mock |
|---|---|---|---|---|
| **TS / JS** (Jest 30, Vitest 4 / 5) | `jest.Mocked<T>`, `vi.mocked(…)`, a literal checked with `satisfies Partial<T>` before any cast | `{ … } as unknown as T`, `as any` into a constructor or a Nest `useValue`; `jest.mock` of the SUT's module | Testcontainers node 12.2.0; PGlite 0.5.8 (real Postgres SQL, one connection) | openapi-msw 2.1.0 typed handlers; `prism proxy openapi.yaml <url> --errors` (Prism 5.16.0); MSW 3.0.2 is a new major — re-check handler APIs |
| **Python** | `create_autospec(X, spec_set=True)`, `MagicMock(spec=X)` | `MagicMock()` / `Mock()` with no spec; `Mock(unsafe=True)`; `@patch` of the function then called | testcontainers-python 4.15.0; pytest-django 4.14.0 `django_capture_on_commit_callbacks` | responses / respx bodies validated against the schema |
| **Go** | mockery v3.8.0 or uber-go/mock v0.6.0 mocks generated from the interface | testify `mock.Anything`, `.Maybe()`; gomock `.AnyTimes()` | testcontainers-go v0.44.0 | `httptest` handlers built from the schema types |
| **JVM** | Mockito with `MockitoExtension` (strict stubs by default) | `RETURNS_DEEP_STUBS`, `lenient()`, mockk `relaxed = true`; a `@Spy @InjectMocks` SUT | testcontainers-java 2.0.5; a `flush()` before asserting in `@DataJpaTest` | Spring Cloud Contract 5.0.3 stubs |
| **.NET** | Moq `MockBehavior.Strict` | `MockBehavior.Loose` — Moq's default | Testcontainers .NET 4.15.0 (EF `UseInMemoryDatabase` is not a relational engine) | — |
| **Ruby / PHP** | read the double library in use; no pattern here is verified for them | — | a container of the production engine | — |

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.`): given no path, `rg` reads stdin whenever stdin is a pipe, and under an agent's shell that is a silent zero-hit run. Any `rg` error on stderr is a failed grep, never zero hits. `rg`'s positive `-g` globs override `-t`, so test files are selected by glob per stack family (TJ, TO), and shipped code by excluding them (XP).

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' -g '!**/.venv/**'
   -g '!**/*.min.*' -g '!**/__snapshots__/**' -g '!**/docs/**' -g '!ai/**' -g '!**/{load,loadtest,k6,benchmarks}/**')
TJ=(-g '*.{test,spec,e2e-spec,cy}.{js,jsx,ts,tsx,mjs,cjs,mts,cts}' -g '**/{__tests__,test,tests,e2e,cypress,playwright}/**/*.{js,jsx,ts,tsx,mjs,cjs,mts,cts}')
TO=(-g 'test_*.py' -g '*_test.py' -g 'conftest.py' -g '**/tests/**/*.py' -g '*_test.go' -g '**/src/test/**/*.{java,kt}' -g '*{Test,Tests,IT}.{java,kt,cs}'
    -g '*_spec.rb' -g '**/spec/**/*.rb' -g '*_test.rb' -g '*Test.php' -g '**/tests/**/*.{php,rs}' -g '**/*.Tests/**/*.cs')
# Shipped code only (5, 6): tests, fixtures, mocks, stories, seeds, migrations and generated code dropped.
XP=(-g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,seeds,seeders,migrations,stories,storybook,generated,__generated__}/**'
    -g '!**/*.{test,spec,e2e-spec,cy,stories,mock,mocks,fixture,fixtures,test-data,test-utils,test-helpers}.*' -g '!**/{test_*,*_test,conftest}.*' -g '!**/*{Test,Tests,IT}.{java,kt,cs}'
    -g '!**/*.{md,mdx,json,lock,snap,yml,yaml,svg,map,sql,txt,csv}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')   # drops comment-only lines

# 0. Context, not a detector. 0a: double-reset and strictness settings in runner config; 0b: the test-side engines and
#    harnesses in the manifests (the production engine comes from refute-before-report.md § 2, grep G1).
rg -n --pcre2 '\b(?:restoreMocks|resetMocks|clearMocks|automock|mockReset|unstubGlobals)\b\s*:|\bstrictness\b|STRICT_STUBS|MockBehavior\.Strict' -g '*{jest,vitest}*.config.*' -g 'package.json' -g '{pytest.ini,pyproject.toml,setup.cfg}' -g '**/src/test/resources/**' "${X[@]}" .
rg -n --pcre2 '\b(?:testcontainers|@testcontainers/\w+|PostgreSqlContainer|MySqlContainer|MongoDBContainer|@electric-sql/pglite|pg-mem|better-sqlite3|sqlite3|mongodb-memory-server|com\.h2database|hsqldb|Microsoft\.EntityFrameworkCore\.(?:InMemory|Sqlite)|pytest-postgresql|testing\.postgresql|dockertest)\b' -g 'package.json' -g '{pyproject.toml,requirements*.txt,setup.cfg,Pipfile}' -g '{pom.xml,build.gradle*,go.mod,Gemfile,composer.json}' -g '*.csproj' "${X[@]}" .

# 1. The double replaces the SUT. 1a JS/TS: a mocked path whose basename is the test file's own subject; 1b JS/TS: a module
#    auto-mocked AND imported by the same test; 1c Python: the patched name is called in the test body; 1d JVM: a spied SUT.
rg -l0 --pcre2 '\b(?:jest|vi)\.(?:mock|doMock)\(' "${TJ[@]}" "${X[@]}" . | while IFS= read -r -d '' f; do b=$(basename "$f" | sed -E 's/\.(test|spec|e2e-spec)\.[cm]?[jt]sx?$//'); rg -Hn --pcre2 "\b(?:jest|vi)\.(?:mock|doMock)\(\s*['\"\x60][^'\"\x60]*/\Q$b\E(?:\.[cm]?[jt]sx?)?['\"\x60]" "$f"; done
rg -l0 --pcre2 '\b(?:jest|vi)\.mock\(\s*([\x27"])[^\x27"]+\1\s*\)' "${TJ[@]}" "${X[@]}" . | while IFS= read -r -d '' f; do rg -o --no-filename --pcre2 '\b(?:jest|vi)\.mock\(\s*([\x27"])\K[^\x27"]+(?=\1\s*\))' "$f" | while IFS= read -r m; do rg -Hn --pcre2 "^import\s+(?!type\b)[^;]*\bfrom\s+['\"]\Q$m\E['\"]" "$f"; done; done
rg -n -U --pcre2 '@patch(?:\.object)?\(\s*["\x27]([\w.]+)\.(\w+)["\x27][^\n]*\)\s*\n(?:\s*@[^\n]*\n)*\s*(?:async\s+)?def\s+test\w*\([^)]*\)[^\n]*:(?:\n(?!\s*(?:async\s+)?def\s)[^\n]*)*?\b\2\(|with\s+patch\(\s*["\x27][\w.]+\.(\w+)["\x27][^\n]*:\s*\n(?:\s+[^\n]*\n){0,15}?\s+[^\n]*\b\3\(' "${TO[@]}" "${X[@]}" .
rg -n -U --pcre2 '@Spy\b[^\n]*\n\s*@InjectMocks\b|@InjectMocks\b[^\n]*\n\s*@Spy\b|@(?:Spy|SpyK)\b[^\n]*\n\s*@(?:InjectMocks|InjectMockKs)\b' "${TO[@]}" "${X[@]}" .

# 2. Doubles the type system cannot check: 2a TS literals or `as any` cast to a collaborator; 2b other stacks' loose doubles.
rg -n -U --pcre2 '(?:new\s+[A-Z]\w*\([^;]{0,300}?|useValue\s*:\s*(?:\{[^{}]{0,400}\}|\w+)\s*|\}\s*\)?\s*)\bas\s+(?:any\b|unknown\s+as\s+\w*(?:Repository|Repo|Port|Service|Producer|Consumer|Gateway|Client|Adapter|Provider|Store|Queue|Bus|Publisher|Mailer|Sender|Directory|Gate|Guard|Dao|Api)\b)' "${TJ[@]}" "${X[@]}" . | rg --pcre2 '\bas\s+(?:any|unknown)\b'
rg -n --pcre2 '\b(?:Magic|Async)?Mock\(\s*\)(?!\.)|\bmock\.(?:Magic|Async)?Mock\(\s*\)|mockk<[^>]+>\(\s*relaxed\s*=\s*true|MockBehavior\.Loose|RETURNS_DEEP_STUBS|\blenient\(\)|\bmock\.Anything\b|\.Maybe\(\)|\.AnyTimes\(\)|Mock\(\s*unsafe\s*=\s*True' "${TO[@]}" "${X[@]}" . | "${NC[@]}"

# 3. Doubles of what the project does not own: 3a module mocks of drivers, SDKs and the framework; 3b casts to third-party
#    persistence and I/O types; 3c other stacks' patches of client libraries; 3d hand-written HTTP mock bodies.
rg -n --pcre2 '\b(?:jest|vi)\.mock\(\s*[\x27"](?:axios|node-fetch|undici|got|ky|fs|fs/promises|node:fs(?:/promises)?|pg|mysql2(?:/promise)?|mongoose|mongodb|@prisma/client|typeorm|sequelize|knex|drizzle-orm|@mikro-orm/[\w-]+|ioredis|redis|bullmq|@aws-sdk/[\w-]+|@google-cloud/[\w-]+|stripe|nodemailer|twilio|firebase-admin|@nestjs/[\w-]+)[\x27"]' "${TJ[@]}" "${X[@]}" .
rg -n --pcre2 '\bas\s+(?:unknown\s+as\s+)?(?:EntityManager|SqlEntityManager|EntityRepository<|Repository<|PrismaClient|PrismaService|DataSource|Knex|Redis|Queue|S3Client|Stripe|Transporter|Pool|PoolClient|Db|MongoClient)\b' "${TJ[@]}" "${X[@]}" .
rg -n --pcre2 '\bpatch(?:\.object)?\(\s*[\x27"](?:requests|httpx|urllib3?|boto3|botocore|sqlalchemy|redis|stripe|smtplib|psycopg2?|socket)\b|\bmock\(\s*(?:EntityManager|JdbcTemplate|RestTemplate|WebClient|HttpClient|Session|DataSource|Connection)(?:::|\.)class\s*\)|\bmockk<(?:EntityManager|JdbcTemplate|RestTemplate|WebClient|HttpClient)>' "${TO[@]}" "${X[@]}" .
rg -l0 --pcre2 '\bHttpResponse\.json\(\s*[\[{]|\bres\(\s*ctx\.json\(|\broute\.fulfill\(\s*\{|\bcy\.intercept\([^)\n]*,\s*\{|\bnock\([^)\n]*\)[^\n]*\.reply\(' "${TJ[@]}" "${X[@]}" . | xargs -0 -r rg -l --files-without-match --pcre2 '\bcreateOpenApiHttp\b|openapi-msw|\borval\b|\bsatisfies\s+\w+|paths\[[\x27"]/'

# 4. Engine substitution: 4a an emulated database in test config or tests; 4b the repository or ORM mocked in an
#    integration-named test; 4c commit-time behaviour a rolled-back test never reaches.
rg -n --hidden --pcre2 '\bsqlite3?\b|:memory:|jdbc:(?:h2|hsqldb):|\bnewDb\(|\bMongoMemoryServer\b|\bUseInMemoryDatabase\(|\bUseSqlite\(|\bbetter-sqlite3\b|\bpg-mem\b' "${TJ[@]}" "${TO[@]}" -g '*{test,testing}*.{properties,yml,yaml,json,cfg,ini,py,toml,env}' -g '.env.test*' -g '*{jest,vitest}*.config.*' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 'overrideProvider\(\s*\w*(?:Repository|Repo|EntityManager|PrismaService|DataSource|Dao)\b|provide\s*:\s*(?:getRepositoryToken\([^)]*\)|\w*(?:Repository|Repo|EntityManager|PrismaService|DataSource|Dao)\b)[^\n]*useValue|\b(?:jest|vi)\.mock\([^)\n]*(?:repositor|\brepo\b|dao)\w*|@MockBean\s+(?:private\s+)?\w*(?:Repository|Dao)\b|@MockitoBean\s+(?:private\s+)?\w*(?:Repository|Dao)\b|patch(?:\.object)?\([^)\n]*(?:repository|repo|session|objects)\b' -g '*.{e2e-spec,e2e,int,integration,it}.{js,ts}' -g '**/{e2e,integration,it}/**/*.{js,ts,py}' -g '**/*IT.{java,kt}' -g '**/tests/integration/**/*.py' "${X[@]}" .
rg -l0 --pcre2 '@DataJpaTest\b|@Transactional\b' -g '**/src/test/**/*.{java,kt}' "${X[@]}" . | xargs -0 -r rg -l --files-without-match --pcre2 '\bflush\(|saveAndFlush\(|TestTransaction\.end\('
[ -n "$(rg -l --pcre2 '\bon_commit\(' -g '*.py' "${XP[@]}" "${X[@]}" . | head -1)" ] && rg -l --pcre2 '\b(?:django\.test\.)?TestCase\b' -g 'test_*.py' -g '*_test.py' -g '**/tests/**/*.py' "${X[@]}" . | xargs -r rg -l --files-without-match --pcre2 'captureOnCommitCallbacks|django_capture_on_commit_callbacks|TransactionTestCase'

# 5. Test seams in shipped code: 5a test-mode branches, stack sniffing, a NODE_ENV set membership and a guard-off switch
#    (`THROTTLE_DISABLED`, `SKIP_AUTH`); 5b test helpers and `*.test-data` / `*.fixture` files imported by shipped code
#    (those files themselves are test code, never shipped — XP drops them).
rg -n --pcre2 '\bNODE_ENV\b\s*[!=]==?\s*[\x27"\x60]test[\x27"\x60]|[\x27"\x60]test[\x27"\x60]\s*[!=]==?\s*process\.env\.NODE_ENV|\bprocess\.env\.(?:JEST_WORKER_ID|VITEST(?:_\w+)?|NODE_TEST\w*)\b|\bimport\.meta\.env\.(?:VITEST|MODE\s*[!=]==?\s*[\x27"]test)|\bsettings\.TESTING\b|[\x27"]pytest[\x27"]\s+in\s+sys\.modules|\bRails\.env\.test\?|\brunningUnitTests\(|\btesting\.Testing\(\)|\bnew\s+Error\(\)\.stack\b|\bprocess\.argv\b[^\n]*\b(?:jest|vitest|mocha|test)\b|\bif\s*\(\s*!?\s*(?:isTest(?:ing|Env|Mode)?|IS_TEST\w*)\s*(?:\(\s*\))?\s*\)|\.(?:has|includes)\(\s*(?:process\.env\.|\w+\.)?NODE_ENV\b|\b(?:[A-Z]+_)*(?:THROTTL\w*|RATE_?LIMIT\w*|CAPTCHA|CSRF|GUARDS?|SIGNATURE_CHECK|WEBHOOK_VERIFY\w*|AUTH_CHECK)_(?:DISABLED?|OFF|SKIP|BYPASS)\b|\b(?:SKIP|BYPASS)_(?:THROTTL\w*|RATE_?LIMIT\w*|AUTH\w*|CAPTCHA|CSRF|GUARDS?|SIGNATURE\w*|MFA|OTP)\b|\bDISABLE_(?:THROTTL\w*|RATE_?LIMIT\w*|CAPTCHA|CSRF|GUARDS?|SIGNATURE_CHECK)\b' "${XP[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 "from\s+['\"][^'\"]*(?:/tests?/|/__mocks__/|/fixtures/|\.(?:test|spec|test-data|test-utils|test-helpers|fixtures?|mocks?)['\"])|require\(\s*['\"][^'\"]*(?:/tests?/|/__mocks__/|\.(?:test|spec|test-data|fixtures?|mocks?)['\"])|^\s*(?:from|import)\s+tests?\.\w+" "${XP[@]}" "${X[@]}" . | "${NC[@]}"

# 6. Special-cased test inputs in shipped code: 6a equality / conversion overrides that answer a constant; 6b comparisons in
#    shipped code against a literal the tests use that appears nowhere else in shipped code (lists written to $TMPDIR).
rg -n -U --pcre2 'def\s+__eq__\s*\([^)]*\)\s*(?:->\s*bool\s*)?:\s*\n\s*return\s+True\b|\bequals\s*\([^)]*\)\s*\{\s*\n?\s*return\s+true\s*;|\[Symbol\.toPrimitive\]\s*\(|\bvalueOf\s*\(\s*\)\s*\{\s*return\s+[\d\x27"]|\bfunc\s*\(\s*\w+\s+\*?\w+\s*\)\s*Equal\([^)]*\)\s*bool\s*\{\s*return\s+true\b' "${XP[@]}" "${X[@]}" .
TD="${TMPDIR:-/tmp}/tds"; Q='(?<![\w.$#-])\d{3,}(?:\.\d+)?(?![\w.])|(?<=["\x27])[^"\x27\n\s]{3,40}(?=["\x27])'
rg -o --no-filename --pcre2 "$Q" "${TJ[@]}" "${TO[@]}" "${X[@]}" . | sort -u > "$TD-test"
rg -o --no-filename --pcre2 "$Q" "${XP[@]}" "${X[@]}" . | sort | uniq -c | awk '$1==1{print $2}' > "$TD-once"
rg -n -o --pcre2 '(?:[!=]==?|\bcase\s+)\s*\K(?:"[^"\n]{3,40}"|\x27[^\x27\n]{3,40}\x27|\d{3,}(?:\.\d+)?)(?![\w.])' "${XP[@]}" "${X[@]}" . | sed -E "s/:[\"']/:/; s/[\"']$//" | awk -F: 'FILENAME==ARGV[1]{t[$0]=1;next} FILENAME==ARGV[2]{o[$0]=1;next} {l=$0; sub(/^[^:]*:[^:]*:/,"",l)} (l in t)&&(l in o)' "$TD-test" "$TD-once" -
```

A finding is a grep hit **plus** a read of the test **plus** the double followed to the real thing it stands for **plus** the oracle run. Four blind spots are structural:

- **Test names that do not mirror the SUT.** 1a matches a mocked path whose basename is the test file's; a behaviour-named test (`a-refund-is-idempotent.spec.ts`) mocking `refund.service` is missed, and 1b catches only automocks the test also imports. For each test of a money, auth or write path, read the `jest.mock` / `patch` list against the module the test claims.
- **Doubles built in helpers.** A factory in `test/support` that returns `{…} as unknown as Repo` shows up once in 2a, however many tests use it. Count its callers before ranking it.
- **Alias paths.** `jest.mock('@/orders/orders.service')` is caught by 1a only when the alias keeps the basename; a barrel (`@/orders`) is not. Resolve aliases from `tsconfig` `paths` for the SUT modules you read.
- **6b sees comparisons only.** A special case written as a lookup (`{ 250: 3 }[cents]`), a `switch` on a computed value, or a literal split across a constant is missed. The diff form is cheaper: on a fix branch, `git diff` the shipped code for any literal that also appears in a test file.

**Measured** (2026-10-05, read-only). On a real NestJS-on-Fastify + MikroORM API (Jest 30, Testcontainers Postgres for e2e) with a React web app (Vitest 4) — about 14,200 tracked files, 3,328 JS/TS test files — the script runs in about 3 s and returns: 0a 2 (`clearMocks` in both Jest configs, no `restoreMocks`); 0b 2 (`testcontainers`, `@testcontainers/postgresql`); 1a 0 of 1,584 relative-module mocks; 1b 0; 2a 346 lines of partial doubles cast `as unknown as <Port | Repository | …>` into constructors (66 `OrderRepository`) — a drift-prone shape, settled in bulk by the conformance codemod in § The 3,000-hit path, not a finding per line; 3a 1 (`vi.mock('ky', …)`); 3b 128 casts to third-party types (`EntityManager` 106, `Redis` 10, `Queue` 6); 3d 2 e2e support files with hand-written route bodies; 4a 0 (a `pg-mem` alternation without a word boundary first matched `pg-member…` in an email literal; fixed); 5a 0 (a domain field named `isTest` matched an earlier form; the grep now keys on an `if` gate); 5b 1 (a test render helper under `src/` importing `@/test/query-wrapper`); 6a 0; 6b 26 comparisons whose literal appears once in shipped code and also in a test — all protocol method names and error codes (precedent). Python, Go and JVM lines: no such tests in the repo. On the research corpus of seeded doubles, every positive hits (the SUT mock, the automocked import, the patch-then-call, loose doubles in five stacks, H2 / SQLite `:memory:` / pg-mem) and no decoy does (`MagicMock(spec=…)`, `create_autospec`, a mailer mock, PGlite). On a scratch copy of `benchmarks/fixtures/reward-hack` with `if (cents === 250) return 3;` and a `NODE_ENV === 'test'` gate added to `src/points.js`, 6b and 5a each return exactly the seeded line; the unmodified fixtures return 0 on every grep. Re-measured 2026-10-15 on the same monorepo: the whole script 691 → 601 lines — 94 were `*.test-data.ts` / `*.fixture.tsx` files under `src/` read as shipped code (5b, 6b); XP now drops them, and 5b keeps any shipped import of one. 5a 0 → 4: the `THROTTLE_DISABLED` switch (env schema, a `.has(read.NODE_ENV)` opt-out set, the local stack script) — a seam that fails closed, so a hardening row, but no longer invisible. The fixtures are unchanged.

## The 3,000-hit path

1. **Intersect with what runs.** Keep test files a runner config collects; dismiss a probe or tool directory with one read and name it in the coverage block.
2. **Group.** One group = (the double's target type or module, the helper that builds it). 2a's 346 lines on the measured repo are about 60 groups by target type.
3. **Rank by risk surface.** Doubles of money, auth, tenant, webhook and write-path collaborators first; within those, the ones no integration or e2e test exercises for real.
4. **Read the top 30 groups fully.**
5. **Prefer the bulk oracle.** For 2a, run the conformance codemod in a scratch worktree and let the compiler read every double at once: `rg -l --pcre2 '\}\s*\)?\s*as unknown as \w' "${TJ[@]}" "${X[@]}" . | xargs perl -0pi -e 's/\}(\s*\)?)\s*as unknown as ([\w.]+(?:<[^>\n]*>)?)/}$1 satisfies Partial<$2> as unknown as $2/g'`, then `npx --no tsc --noEmit -p <the tsconfig that includes the tests>`. Each error on a rewritten line is a drifted double: measured with TypeScript 7.0.2 on 2026-10-05, a drifted return or parameter type reports TS2322 and a method name the interface no longer has reports TS2561, while the same literal behind a plain `as unknown as` cast reports nothing. Discard the worktree. For Python, the same move is `create_autospec(<Real>, instance=True)` in place of `MagicMock()` and one run of the suite.
6. **Ledger the rest.** `Live, unreviewed (k groups / n hits)` with the continuing command; never `checked`.

## Scans for

Severity: **high** when the double or seam sits on a money, auth, tenant or write path and no other layer pins the behaviour; otherwise the class default. Demote one step when another test exercises the real collaborator or engine on the same behaviour (cite it). Research classes MK-01 and MK-04…MK-06 and DB-01…DB-03 map as listed; the rest of that family (MK-02, MK-03, CT-01…04, DB-04, PY-01, FX-01…03, GM-01, NE-01…03) is routed in § Boundaries.

| § | Class | Research ids | Default |
|---|---|---|---|
| 1 | The double replaces the code under test | MK-01 | high |
| 2 | Doubles the type system or `spec` cannot check | MK-04 | medium |
| 3 | Doubles of what the project does not own; hand-written HTTP mock bodies | MK-05, MK-06 | medium; high for money or auth payloads |
| 4 | Engine substitution: an emulated database, a repository mocked in an integration test, commit-time behaviour never reached | DB-01, DB-02, DB-03 | high for DB-01 on a constraint or transaction the code relies on; else medium |
| 5 | Test seams in shipped code | — | high when the seam skips a guard, a validation or a write; else medium |
| 6 | Special-cased test inputs and equality overrides in shipped code | — | high |

### 1. The double replaces the code under test

```
BAD:   jest.mock('../src/orders.service') in orders.service.spec.ts, then expect(service.total(cart)).toBe(42)
       @patch("app.billing.pay", return_value=3) then assert pay() == 3
       @Spy @InjectMocks OrderService service; doReturn(42).when(service).total(cart)
GOOD:  mock the SUT's collaborators, never the SUT; a partial mock keeps the export under test real
       (jest.mock(path, () => ({ ...jest.requireActual(path), sendEmail: jest.fn() })))
```
**Read the code:** Which export does the test call, and is it the real one? A `requireActual` partial mock that keeps the function under test real is fine ([`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 39). For a spy: is the stubbed method the one the test claims, or a collaborator method on the same object? **Finding when** the value the test asserts comes from a double, not from the code it names. **Proof:** break the SUT — make the function return a wrong value of the right type (never a `throw`) and run the test; green proves it ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Break the SUT; V70). After the fix the three probes (a constant, an empty value, the wrong member) all go red.

### 2. Doubles the type system cannot check

```
BAD:   new RefundService({ findById: jest.fn() } as unknown as OrderRepository)   // findById renamed to findOne: still compiles
       gw = MagicMock()                                                            # gw.chargee(...) "works"
       @Mock(answer = RETURNS_DEEP_STUBS) · mockk<Repo>(relaxed = true) · m.On("Save", mock.Anything).Maybe()
GOOD:  new RefundService({ findById: jest.fn() } satisfies Partial<OrderRepository> as unknown as OrderRepository)
       create_autospec(Gateway, spec_set=True) · Mockito strict stubs · MockBehavior.Strict · mockery-generated mocks
```
**Read the code:** Which methods does the SUT call on the collaborator, and does the double provide them with today's signatures? Is the double built once in a helper (count the callers)? `as any` on a deliberately invalid input to a negative test is a precedent, not a double. CPython ≥ 3.12 rejects `assert_*` typos on a mock, but not a misspelled ordinary method ([`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 5). **Finding when** the double's shape differs from the real interface on a method the SUT uses, or nothing checks it and the interface changed since the double was written (`git log -L` on the interface). **Proof:** interface conformance — the codemod or `spec` in § The 3,000-hit path names the drift at the cited line ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Interface conformance, real-engine parity, env parity; V70). With no drift today, the unchecked shape alone is Hardening, fixed by typing it.

### 3. Doubles of what the project does not own

```
BAD:   jest.mock('axios') · vi.mock('ky', …) · patch("requests.post") · mock(EntityManager.class)
       { findOne: jest.fn().mockResolvedValue(null) } as unknown as EntityManager      // assumes how the ORM answers
       http.get('/api/orders', () => HttpResponse.json({ id: 1, total: '12.00' }))    // the API sends totalCents: number
GOOD:  a port the project owns (OrderReader, EmailGateway) doubled in unit tests, and the adapter tested against the
       real library (Testcontainers, a local server); handlers typed from the schema (openapi-msw), or bodies passed
       through `prism proxy` / ajv against the OpenAPI response schema
```
**Read the code:** Does the test assert behaviour that depends on the library's semantics (an ORM's null-vs-throw, an identity map, a flush, an HTTP client's retry or error shape)? Is there an e2e or integration test on the real library for the same path (then demote)? For an HTTP mock: is the body typed or validated from the schema, and do its error shapes (4xx/5xx, pagination envelope, enums, nullable fields) match? Mocking a port the project owns is the recommended shape (§ 39). **Finding when** the double encodes an assumption about third-party behaviour that a real run contradicts. **Proof:** real-engine parity — the same test against the real dependency or the schema validator fails where the double passed (V70).

### 4. Engine substitution

```
BAD:   DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}   # production is Postgres
       spring.datasource.url=jdbc:h2:mem:test;MODE=PostgreSQL · newDb() (pg-mem) · UseInMemoryDatabase()
       overrideProvider(OrderRepository).useValue({ … }) in checkout.e2e-spec.ts
       @DataJpaTest: repo.save(order); assertThat(repo.findAll()).hasSize(1)   // no flush: the unique violation never fires
GOOD:  Testcontainers pinned to the production major · PGlite for single-connection SQL semantics
       flush() / saveAndFlush() before asserting · django_capture_on_commit_callbacks(execute=True) · TransactionTestCase
```
**Read the code:** What is the production engine (G1), and does the code under test rely on a semantic the fake lacks — unique and FK enforcement (SQLite needs `PRAGMA foreign_keys=ON`), length and type checks, `ON CONFLICT`, partial indexes, JSONB, collation, `FOR UPDATE`, isolation, a Mongo transaction (needs a replica set)? Is the integration-named test mocking only external services (fine) or the repository (the finding)? Does a rolled-back test reach an `on_commit` hook or a flush-time error? SQLite in tests is fine when production is SQLite; PGlite is fine except for locking and concurrency ([`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 40). **Finding when** a test's verdict depends on an engine semantic the fake does not have. **Proof:** real-engine parity — the duplicate key, over-length value or FK violation that passes on the fake fails on Testcontainers; for commit time, adding the flush or the capture makes the hidden error appear (V70; the constraint oracles in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Constraint rejection take it from there).

### 5. Test seams in shipped code

```
BAD:   if (process.env.NODE_ENV === 'test') return true;          // in a guard
       if settings.TESTING: skip_signature_check()  ·  if (process.env.JEST_WORKER_ID) …
       import { createQueryWrapper } from '@/test/query-wrapper'   // in a module the app ships
GOOD:  inject the dependency the test wants to replace (a clock, a verifier, a transport) and pass a double in the test;
       keep test helpers under the test globs, never imported by shipped entry points
```
**Read the code:** What does the branch skip or change — a guard, a signature or validation check, a write, a delay? Is the flag set anywhere outside tests (a misconfigured production `NODE_ENV` turns the seam on in production)? For a helper import: does any shipped entry point reach that module (follow the import graph, or run the bundler's or knip's unused-file report)? **Finding when** shipped code takes a different path under test than in production on behaviour a test asserts, or ships a test-only module. **Proof:** env parity — run the production path with the flag off (`NODE_ENV=production`, `TESTING=False`) on the test's input; a different outcome proves the suite never tested the production path (V72).

### 6. Special-cased test inputs and equality overrides

```
BAD:   if (cents === 250) return 3;            // 250 is the input of the refund test, and appears nowhere else
       def __eq__(self, other): return True    ·  [Symbol.toPrimitive]() { return 42 }
       let calls = 0; export function tier(b) { return ++calls > 1 ? 'gold' : 'silver' }   // answers by call count
GOOD:  the rule the spec states, for every input; equality over the fields that define identity
```
**Read the code:** Is the literal a domain constant the tests also use (a protocol method, an error code, an enum value — precedent) or a test's specific input or expected value with no meaning in the domain? Does the override answer a constant or depend on call order? Was the line added in the same change that made a failing test pass (`git log -S'<literal>'`)? **Finding when** shipped code returns the tested answer for the tested input only. **Proof:** feed the neighbouring input (251 for 250, the same object with one field changed) to the SUT and compare with the spec's rule — the special case falls off; on a change, old test on new code: the base test against head source ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Old test on new code, and the anti-cheat rule; V72). A special case found in an agent's own fix diff is a tampering failure of that fix, not a finding to schedule.

## Output

```
test-double-scan — lanes: ts/jest 30.5 (apps/api), ts/vitest 4.1 (apps/web); python, go, jvm absent
Context: clearMocks only · production engine postgres 17 (compose) · e2e on @testcontainers/postgresql 12

Findings: 1 · Unconfirmed: 2

1. test/unit/refund-policy.spec.ts:31                                 [report-with-fix]  high
   §2 drifted double — { findById } as unknown as OrderRepository; the interface method is findOne(id, opts)
   since a1b2c3d. Proof: conformance codemod → TS2561 at :31; break the SUT's lookup → test still green.
   Fix: build the double from a typed helper (satisfies Partial<OrderRepository>); assert on the refund row. V70

2. test/unit/session.spec.ts:14                                        [report-flagged]   medium
   §3 vi.mock('ky') encodes ky's retry-after behaviour. Unproven link: whether an e2e test covers the
   real client. Settling probe: run the session flow against a local server returning 429 + Retry-After.

3. src/test-support/render-list.tsx:3                                 [report-flagged]   medium
   §5 test helper under src/ imports @/test/query-wrapper. Unproven link: whether a shipped entry imports it.
   Settling probe: the bundler's unused-file report or knip on the web app.

Verification: 34 candidates → 1 finding · 2 unconfirmed · 27 hardening · 0 pre-existing · 4 refuted

Class coverage:
  §1  SUT mocked                     checked (1,584 relative mocks → 0 by basename; 0 automock-and-import)
  §2  unchecked doubles              checked (346 hits / 61 groups via conformance codemod → 1 finding)
  §3  not-owned / HTTP bodies        checked (1 + 128 + 2 → 0 findings; e2e on Testcontainers covers the ORM paths) · 1 Unconfirmed
  §4  engine substitution            checked (0 hits; Testcontainers on the production major)
  §5  test seams                     checked (1 hit → 1 Unconfirmed)
  §6  special cases / overrides      checked (26 literal matches → 0 findings: protocol names and error codes)
```

`[report-with-fix]`: the double is followed to the real thing, the oracle fired, and the fix is local. `[report-flagged]`: one link is unproven (no harness, a layer not searched, an import graph not walked) and the row names it with the settling command. The coverage block lists **all six** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the repo has no such surface (no Python tests, no integration-named tests); `blocked (<reason>)` when a grep failed or code could not be read. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/testing.md`](../../../../snippets/precedents/testing.md) (§ 20–21 and 39–40 for doubles and engines) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **Mocks of collaborators are the point of a unit test**; a `requireActual` partial mock keeps the SUT real (§ 39). A mock of a module the test never exercises is isolation.
- **An interaction on a port the project owns** is the outcome when the arguments are pinned (§ 20); a pass-through echo is `assertion-strength-scan`'s call (§ 21).
- **Engines** — Testcontainers on the production major is real; PGlite is real Postgres SQL but not locking; SQLite tests are fine for a SQLite product (§ 40).
- **A domain constant shared by test and code** — a protocol method, an error code, an enum member, a status — is not a special case.
- **`as any` to build a deliberately invalid input** for a negative test is not a double.
- **A generated client compiled in the same CI** is the frontend's contract; its mock bodies are typed by construction.

## When to run

- On any diff that adds or changes a test double, a `jest.mock` / `patch` list, a test database config, a provider override in an integration test, or a shipped line that mentions `test` — the `/review-changes` dispatch signal for test files, beside `assertion-strength-scan` and `flake-source-scan`.
- On every whole-suite test audit, reporting all six classes.
- After an interface or schema change: run 2a's conformance codemod and 3d's schema check before trusting a green unit suite.
- On every fix diff `/test-fix` or `/flaky-test-hunt` produces: § 5 and § 6 must return nothing new — a special case or seam in a fix is the anti-cheat rule failing.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/testing.md`](../../../../snippets/precedents/testing.md). Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the double or seam `<file:line>`, the test that relies on it, what it hides, and the fix.
- Do not report a grep hit as a finding. Do not demote a candidate to "covered elsewhere" without naming the other test and its assertion.
- Do not propose deleting the test, loosening its assertion, or a new special case as the fix. The fix makes the double honest or removes the seam.
- Do not print "no lying double found" without the class-coverage block; a class whose grep did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `assertion-strength-scan` (interaction-only and echo assertions), `flake-source-scan` (shared fixtures, real network), `contract-test` (consumer–provider contracts), `coverage-gap` (missing integration and negative tests), `mutation-probe` (break the SUT, automated), `test-factories` (typed builders that replace hand-cast doubles) — this pack.
- `/test-fix` and `/add-test` close the findings: failing-first, the oracle re-run, and the anti-cheat self-check on the fix's own diff. `/flaky-test-hunt` is the runtime harness when a lying double surfaces as a flake.
- [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Testing and [`precedents/testing.md`](../../../../snippets/precedents/testing.md) — the oracles and the settled precedents.
- `ai-patterns/test-doubles.md` — the method (mock vs stub vs fake, when each fits); this skill is its executor.
- The database pack's constraint and concurrency oracles (`proof-oracles.md` § Data) take over once § 4 shows the engine matters, when that pack is installed; without it, § 4's parity run is the proof and the constraint list in § 4 is the checklist.
