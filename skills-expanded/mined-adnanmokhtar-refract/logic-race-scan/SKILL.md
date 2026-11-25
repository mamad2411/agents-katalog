---
name: logic-race-scan
description: Flaws no pattern scanner sees — client-trusted prices and quantities, skippable workflow steps, negative and overflow values, missing idempotency, check-then-act races (double spend, double redeem), and a per-role authorization matrix proved route by route.
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: logic-race-scan

## Premise

A pattern scanner finds a dangerous call. A business-logic flaw has none: `orders.create({ total })` is a safe line until you notice `total` came from the browser, and every line of an exploited double-spend is individually correct — the bug is the gap *between* two of them. OWASP files these under **A06:2025 Insecure Design** (CWE-840 business logic, CWE-362 / CWE-367 races) and the per-role authorization they lean on under **A01:2025**. This skill finds them in two moves: greps that locate the candidate surfaces (the vocabulary of value — money, quantity, balance, coupon, quota, status, role, invite — and the shapes of a race — read-modify-write, find-then-update, check-then-insert), then a read of each candidate that **names the invariant and decides whether the server enforces it atomically**.

**Every finding cites the sink `<file:line>` + the invariant it breaks + the failing condition (the client-chosen value, the unguarded transition, the gap between check and act) + the fix.** "Coupons might be raceable" with no cited check, no cited write and no missing primitive is not a finding.

**Boundary.** IDOR / BOLA and mass assignment belong to `@api-security-reviewer` (API1, API3); cross-tenant access to `@tenant-isolation-reviewer`; the token, session and reset-token ceremony to `@auth-reviewer`. This skill builds the per-role matrix and flags the cells nobody proved — it does not re-run their detectors. Transaction defects that are not abuse of a value belong to the database pack's `transaction-scan` when it is installed: lock order and deadlocks, retry on serialization failure, I/O held inside a transaction, queue claims without `SKIP LOCKED`, long transactions, savepoints in a loop, hot rows, write skew, and lost updates on fields that carry no money, stock, quota or single-use value. A site both skills flag is one finding, deduped by `<file:line>` and credited here when the value is abused.

## Adapt to the codebase

Name the project's five primitives before reading anything. The BAD/GOOD blocks below are shapes; the fix is written in this row. **Read the ORM and its version from the lockfile or manifest** (`pnpm-lock.yaml`, `package-lock.json`, `poetry.lock`, `go.mod`, `Gemfile.lock`, `composer.lock`), never from a brief, a stack note or a pattern file: the primitives differ per ORM, and a run that assumes the wrong one reads every safe site as a race and misses the real ones.

| Stack | Atomic conditional update (check rows affected) | Row lock | Unique-constraint upsert | Idempotency key storage | Per-role test primitive |
|---|---|---|---|---|---|
| **SQL (any)** | `UPDATE t SET bal = bal - :n WHERE id = :id AND bal >= :n` | `SELECT … FOR UPDATE` in the same transaction | `UNIQUE (…)` + `INSERT … ON CONFLICT DO NOTHING` / `INSERT IGNORE` | `idempotency_keys` row, `UNIQUE (principal_id, key)` | — |
| **Node/TS** (Express, NestJS) | Prisma `updateMany({ where: { id, bal: { gte: n } }, data: { bal: { decrement: n } } })` → `count`; TypeORM `repo.decrement({ id, bal: MoreThanOrEqual(n) }, 'bal', n)` → `affected`; MikroORM `em.nativeUpdate(E, { id, bal: { $gte: n } }, { bal: raw('bal - ?', [n]) })` → affected count; Knex `.where('bal','>=',n).decrement('bal', n)`; Mongoose `updateOne({ _id, bal: { $gte: n } }, { $inc: { bal: -n } })` → `modifiedCount` | Prisma `$transaction` + `$queryRaw` `FOR UPDATE`; TypeORM `setLock('pessimistic_write')`; MikroORM `{ lockMode: LockMode.PESSIMISTIC_WRITE }` inside `em.transactional` — the enum, never a number: `lockMode: 2` is `PESSIMISTIC_READ` in 6.x — or optimistic `@Property({ version: true })`; Knex `.forUpdate()`; Sequelize `lock: t.LOCK.UPDATE`; Mongo: none — use the conditional update | Prisma `@@unique` + catch `P2002`; TypeORM `.orIgnore()`; MikroORM `@Unique()` + catch `UniqueConstraintViolationException`; Knex `.onConflict(k).ignore()`; Mongo unique index + `upsert: true`, retry `E11000` | Express middleware / Nest interceptor writing the row inside the same `$transaction` / `transaction()` as the side effect | supertest `.set('Authorization', tokenFor(role))` inside `it.each(matrix)`; Nest e2e through the real guard |
| **Python** (Django, FastAPI, Flask) | Django `filter(pk=id, bal__gte=n).update(bal=F('bal') - n)` → count; SQLAlchemy `update(T).where(T.id == id, T.bal >= n).values(bal=T.bal - n)` → `rowcount` | Django `select_for_update()` in `transaction.atomic()`; SQLAlchemy `.with_for_update()` | `UniqueConstraint` + `get_or_create` (safe only with it) / `bulk_create(ignore_conflicts=True)`; SQLAlchemy `insert().on_conflict_do_nothing()` | Django middleware / FastAPI dependency inside `transaction.atomic()` or the session transaction | `pytest.mark.parametrize` over (role, status) + DRF `force_authenticate` / `client.force_login`; FastAPI `TestClient` overriding only the current-user dependency |
| **Go** | `res, _ := tx.ExecContext(ctx, "UPDATE … WHERE id = $2 AND bal >= $1", n, id)` → `res.RowsAffected()`; GORM `Where("bal >= ?", n).Update("bal", gorm.Expr("bal - ?", n))` → `RowsAffected` | `FOR UPDATE` inside a `sql.Tx`; GORM `Clauses(clause.Locking{Strength: "UPDATE"})` | `ON CONFLICT DO NOTHING`; GORM `Clauses(clause.OnConflict{DoNothing: true})` | middleware + `INSERT … ON CONFLICT DO NOTHING RETURNING` in the handler's `Tx` | table-driven test over `[]struct{ role string; want int }` with `httptest.NewRecorder` and a real token per role |
| **Java/Kotlin** (Spring) | `@Modifying @Query("update Account a set a.bal = a.bal - :n where a.id = :id and a.bal >= :n") int debit(…)` → 0 means refuse | `@Lock(LockModeType.PESSIMISTIC_WRITE)` finder inside `@Transactional`; optimistic `@Version` | unique constraint in the migration + catch `DataIntegrityViolationException` | `HandlerInterceptor` + entity with unique `(principal, key)` saved in the same `@Transactional` | `MockMvc` + `@WithMockUser(roles = …)` or `.with(jwt())`, `@ParameterizedTest` |
| **Ruby** (Rails) | `where(id:).where('bal >= ?', n).update_all(['bal = bal - ?', n])` → count | `record.with_lock { … }` / `Model.lock.find(id)`; optimistic `lock_version` | `add_index …, unique: true` + `create_or_find_by` / `insert_all(…, unique_by:)` — not `find_or_create_by`, not `validates uniqueness` | `around_action` + model with a unique index, saved in the same `transaction` | request specs with `sign_in` per role + Pundit policy specs (`permissions :update?`) |
| **PHP** (Laravel) | `Account::whereKey($id)->where('bal', '>=', $n)->decrement('bal', $n)` → affected rows | `lockForUpdate()` inside `DB::transaction` | unique index + `createOrFirst` / `insertOrIgnore` / `upsert` — not `firstOrCreate` | middleware + model with a unique index inside `DB::transaction` | `actingAs($user)->postJson(…)->assertForbidden()` over a Pest dataset / PHPUnit `@dataProvider` |

Anything outside its row — an `if` in application code, a cache read, a model-level uniqueness validation, a mutex in one process — is **not** a concurrency primitive once two requests run at once.

## Pre-flight greps

Run from the repo root. Each numbered block names the detectors (`§N`) its hits feed, and the commands inside a block are cited as a, b, c in order (grep 5b is block 5's second command). The shared definitions come first, and `rg` with PCRE2 is assumed. Every search names its path (`.`) — with none, `rg` reads stdin whenever stdin is not a terminal, and an agent's shell can hang there. Any `rg` error on stderr (exit 2) is a failed grep, not zero hits.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' -g '!**/*.min.js' -g '!**/*.{md,lock,map,svg}')
# Never a production path: tests, mocks, fixtures, snapshots, JSON data (i18n catalogs, audit dumps), ai/.
# Every grep takes it except 13c and 13d, which read the tests on purpose.
T=(-g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,__snapshots__,testdata}/**' -g '!**/*.{spec,test,e2e-spec,mock,stories}.*' -g '!**/{*_test,*_spec,test_*}.*' -g '!**/*.snap' -g '!**/*.json' -g '!ai/**')
# Route registration, every stack: decorators, router calls, Django/Rails/Laravel route files, Go muxes.
ROUTE='@(Get|Post|Put|Patch|Delete|All)\(|@\w+\.(route|get|post|put|patch|delete|api_route)\s*\(|@(Get|Post|Put|Patch|Delete|Request)Mapping\b|\b\w*(router|app|bp|blueprint|server|fastify)\.(get|post|put|patch|delete|all|route|api_route)\s*\(|\b(re_)?path\s*\(\s*r?["\x27]|@(api_view|action)\s*\(|\.(GET|POST|PUT|PATCH|DELETE|Handle|HandleFunc|Get|Post|Put|Patch|Delete)\s*\(\s*"(/|(GET|POST|PUT|PATCH|DELETE) /)|^\s*(get|post|put|patch|delete|match|resources?)\s+[:"\x27]|Route::(get|post|put|patch|delete|any|match|resource|apiResource)\s*\('
# Server-owned fields a client must never choose.
F='(unit_?|base_?|sale_?|list_?|sub_?)?(price|amount|total|discount|fee|tax|shipping|cost|balance|credits?)(_?(cents|minor|amount|price|percent|pct|rate|value|fee|cost))?|percent_?off|currency|role|roles|is_?admin|is_?staff|plan|tier|tenant_?id|org_?id|owner_?id|user_?id|status|state|quantity|qty'
# Counters whose value a race or a lost update corrupts.
C='balance|credits?|stock|quantity|qty|points|uses|use_?count|used_?count|usage_?count|redemptions?|remaining|seats|quota|inventory|available|votes?'

# 1. Surface map — files ranked by value vocabulary. Read the top of this list first.
rg -c -i '(price|amount|total|discount|coupon|voucher|promo|gift_?card|balance|wallet|credit|points|reward|referral|quota|quantity|qty|stock|seat|refund|withdraw|payout|transfer|redeem|invit|vote|approv|subscription|trial)' "${X[@]}" "${T[@]}" . | sort -t: -k2 -nr | head -40

# 2. Server-owned values read from the request (§1, §3, §13). Excludes the authenticated principal (req.user…).
rg -n -i --pcre2 "\b(req|request|ctx\.request|params|body|payload|input|dto|(c|ctx|r)\.(FormValue|PostForm|Query|DefaultQuery|Param|QueryParam|FormParam))\b(?![.\-]>?(user|auth|session|principal)\b)[\w.\[\]\"'?>(:\$-]{0,40}?\b(?:get_?)?($F)\b" "${X[@]}" "${T[@]}" .
rg -n -i --pcre2 "\{[^}]*\b($F)\b[^}]*\}\s*=\s*(await\s+)?(req|request|ctx\.request|c\.req)\b" "${X[@]}" "${T[@]}" .

# 3. Request schemas that ACCEPT a server-owned field (§1, §2). 3a: -B2 shows the validators above each field, in
#    request-shaped files and handlers only (RQ): unanchored, every response and view schema's `status:` / `role:`
#    printed (13,808 lines on a real monorepo; 1,475 with RQ). 3b ranks ALL schema files, so a request model kept
#    elsewhere (FastAPI `schemas.py`) still surfaces there; read 3b's top files that RQ left out.
RQ=(-g '*{[Rr]equest,[Ii]nput,[Bb]ody,[Cc]ommand,[Dd]to,DTO,[Ff]orm,[Pp]ayload,[Pp]arams,[Ss]erializer,[Cc]ontroller,views,routes,[Hh]andler}*' -g '**/{dto,dtos,requests,inputs,forms,serializers,controllers}/**')
S='\b(class|interface|type|record|struct)\s+\w*(Dto|DTO|Request|Req|Input|Payload|Command|Body|Params|Form|Schema|Serializer)\b|\((BaseModel|Schema|\w*Serializer|\w*Form)\)|extends FormRequest|->validate\(\s*\[|\.permit\(|z\.object\(|Joi\.object\('
SF="^\s*(?:(?:public|private|protected|readonly|final|val|var|declare|@\w+(?:\([^)]*\))?)\s+)*(?:[\w<>\[\],.?]+\s+)?\\\$?($F)[?!]?\s*[:=;]|[\"']($F)[\"']\s*(=>|:)|permit\([^)]*:($F)\b|json:\"($F)[,\"]"
rg -l0 --pcre2 "$S" "${RQ[@]}" "${X[@]}" "${T[@]}" . | xargs -0 -r rg -n -i --pcre2 -B2 "$SF"
rg -l0 --pcre2 "$S" "${X[@]}" "${T[@]}" . | xargs -0 -r rg -c -i --pcre2 "$SF" | sort -t: -k2 -nr

# 4. Numbers that go out of range (§2): money stored in a binary float — a type position (column, ORM type,
#    declaration), never the word in a comment; request values coerced to numbers; narrow ints; then 4d, a
#    ceiling checked one requested line at a time — `min(req.qty, line.returnable)`, `if (line.qty > cap)`.
M='price|amount|total|sub_?total|balance|cost|fee|tax|discount|credit|payout|refund'
rg -n -i --pcre2 "^(?!\s*(?://|#|\*|/\*|--))[^\n]*?(?:\b\w*($M)\w*\b[\"'\x60]?\s*[:=\s]\s*(?:[\w.]*\(\s*)?(?:\w+\.)?(?:double precision|float[48]?|float32|float64|real|double|FloatField|Float)\b|\b(?:double|float|float32|float64|Float|Double)\s+\w*($M)|\b(?:type|columnType)\s*:\s*[\"'](?:double(?: precision)?|float[48]?|real)[\"']|\bColumn\(\s*[\"'](?:double(?: precision)?|float[48]?|real)[\"'])" "${X[@]}" "${T[@]}" .
rg -n --pcre2 '\b(parseInt|parseFloat|Number|float|int|Decimal|BigDecimal|Integer\.parseInt|Double\.parseDouble|strconv\.(Atoi|ParseInt|ParseFloat)|intval|floatval)\s*\([^)\n]*\b(req|request|params|query|body|input|payload)\b|\b(params|request)\b[^\n]*\.(to_i|to_f|to_d)\b' "${X[@]}" "${T[@]}" .
rg -n -i --pcre2 '\b(int16|int32|uint16|uint32|smallint|tinyint|(?-i:INTEGER))\b[^\n]{0,40}\b\w*(quantity|qty|count|balance|amount|points|credits?|stock|total)|\b\w*(quantity|qty|count|balance|amount|points|credits?|stock|total)\w*\b[^\n]{0,40}\b(int16|int32|uint16|uint32|smallint|tinyint|(?-i:INTEGER))\b' "${X[@]}" "${T[@]}" .
Q='quantity|qty|count|units|amount'
W='returnable|refundable|available|remaining|left|outstanding|max\w*|limit|ceiling|cap'
rg -n -i --pcre2 "\b(?:Math\.)?min\s*\([^)\n]*\b\w+\.\w*(?:$Q)\w*\b[^)\n]*\b\w*(?:$W)\w*|\b\w+\.\w*(?:$Q)\w*\s*>=?\s*[\w.]*\b\w*(?:$W)\w*|\b\w*(?:$W)\w*\s*<=?\s*\w+\.\w*(?:$Q)\b" "${X[@]}" "${T[@]}" .
#    4e: an idempotency or ledger key built from a request line's fields — repeated lines share one key, so the ledger
#    replays the second leg while the document keeps every line (§2, the repeated-line shape at the ledger).
rg -n --pcre2 "(?i:idempotency_?key|idem_?key|dedupe?_?key|operation_?key)[\"']?\s*[:=]\s*(?:\x60[^\x60\n]*\\$\{\s*|f[\"'][^\"'\n]*\{\s*|[^;\n]*[+,(]\s*)(?:line|item|row|l|receipt|piece|entry|it|ln|li)\.(?:product_?[Ii]d|key|sku_?[Ii]d|variant_?[Ii]d|item_?[Ii]d|id)\b" "${X[@]}" "${T[@]}" .

# 5. State transitions (§3): every write of a literal state, then where any precondition lives.
#    A file in 5a with no line in 5b is read first; a file in both still needs each write checked.
rg -n --pcre2 '\b(?i:status|state|stage|phase)["\x27]?\s*(?:(?<![=!<>])=(?![=>~])|:|=>)\s*(["\x27][A-Za-z_]+["\x27]|:[a-z_]+\b|[A-Z]\w*\.[A-Z_]+\b|Status[A-Z]\w*)|\bset(Status|State|Stage)\(\s*(["\x27]|[A-Z]\w*\.[A-Z_]+)' "${X[@]}" "${T[@]}" .
rg -n -i --pcre2 '\bwhere\b[^\n;{]*\b(status|state)\b\s*(=|in\b)|\bwhere\b\s*:?\s*\{[^}]*\b(status|state)\b\s*:|\b(filter|find_by|findOne\w*|findFirst|update_all|updateMany|nativeUpdate)\s*\([^)]*\b(status|state)\b\s*[=:]|\b(status|state)\b\s*(===?|!==?|==|!=|<>|not in|in)\s*[\[(\x27":\w]|get(Status|State)\(\)\s*(==|!=|\.equals)|can_?transition|transition_?to|may_\w+\?|aasm|state_machine|statesman|FSMField|@transition|xstate|createMachine|looplab/fsm|StateMachine' "${X[@]}" "${T[@]}" .

# 6. Side effects that must happen once (§4) — provider calls, credit grants, paid sends, webhook consumers —
#    then the idempotency evidence. A file in the first two with no line in the third has none.
rg -n -i --pcre2 '\b(charges|paymentIntents|refunds|transfers|payouts|invoices|checkout\.sessions)\.(create|capture|confirm|send)\b|\b(charge|capture|refund|payout|transfer|withdraw|disburse|issue_?(credit|refund)|grant_?credits?|add_?credits?|credit_?account|send_?sms|send_?otp)\w*\s*\(' "${X[@]}" "${T[@]}" .
rg -n --pcre2 "$ROUTE" "${X[@]}" "${T[@]}" . | rg -i 'webhook|callback|notify|ipn|hook'
rg -n -i 'idempoten|dedup|processed_?events|event_?id.*unique|unique.*event_?id' "${X[@]}" "${T[@]}" .

# 7. Read-modify-write on a counter (§5): loaded, changed in memory, written back — `x.bal -= n`,
#    `{ bal: x.bal - n }`, `setBal(getBal() - n)`. 7b is the unit-of-work form: a counter assigned on a loaded
#    entity (`wallet.balance = next`, `em.assign(wallet, { balance })`) and flushed later.
K='balance|credits?|stock|quantity|qty|points|redemptions?|remaining|seats|quota|use_?count|used_?count|usage_?count'
rg -n -i --pcre2 "(\.|->)\s*($C)\s*([-+]=|\+\+|--)|\b(?<g>$C)[\"']?\s*(:|=>|=)\s*\\\$?\w+(\.|->)\k<g>\s*[-+]|\bset(?<s>$C)\s*\([^)]*get\k<s>\(\)\s*[-+.]" "${X[@]}" "${T[@]}" .
rg -n -i --pcre2 "\b(?:em|manager|entityManager|repo\w*|this\.\w+|Object)\.(?:assign|merge)\(\s*[\w.]+\s*,\s*\{[^}]*\b\w*(?:$K)(?:_?cents)?\s*:|^(?!\s*(?://|#|\*))[^\n]*?\b(?!this\.)[a-z]\w*\.\w*(?:$K)(?:_?cents)?\s*=(?![=>])" "${X[@]}" "${T[@]}" .

# 8. Check-then-act (§5, §6): a guard on a value a later statement changes; a code or token checked unused;
#    8c, a debit that clamps at zero instead of refusing — the shape that turns a §5 race into free usage.
rg -n -i --pcre2 "\b(if|unless|when|guard)\b[^\n]*\b($C|limit|max_?\w+)\b[^\n]*[<>]" "${X[@]}" "${T[@]}" .
rg -n -i --pcre2 '\b(if|unless|when|guard)\b[^\n]*(\b(redeemed\w*|consumed\w*|used_?at|is_?used|max_?uses|use_?count|times_?used|claimed_?at|accepted_?at)\b|\b\w*(coupon|voucher|promo|invite|invitation|token|code|gift_?card|reward|referral|otp)\w*(\.|->)(used|accepted|claimed|redeemed|valid|active)\b)' "${X[@]}" "${T[@]}" .
rg -n -i --pcre2 "\b(?:Math\.)?max\s*\(\s*0\s*,[^)\n]*\b\w*(?:$C)\w*[^)\n]*-|\bGREATEST\s*\(\s*0\s*,[^)\n]*-|\b\w*(?:$C)\w*\s*[-+]\s*[\w.]+\s*<\s*0\s*\?|\bcoerceAtLeast\(\s*0\s*\)" "${X[@]}" "${T[@]}" .

# 9. Atomic evidence (§5–§7): locks, version guards, conditional updates, upserts. The set difference
#    against 7, 8 and 10 is the candidate list — a guard file with no line here has no primitive.
rg -n -i --pcre2 '\bfor update\b|forUpdate\(|lockForUpdate|select_for_update|with_for_update|with_lock|\.lock\(|\block\.find|PESSIMISTIC_WRITE|\blockMode\s*:|@Lock\(|setLock\(|LOCK\.UPDATE|clause\.Locking|@Version\b|\bversion\s*:\s*true\b|lock_version|on conflict|on duplicate key|insert ignore|onConflict|orIgnore|insertOrIgnore|createOrFirst|create_or_find_by|\bupsert|\bnativeUpdate\(|\braw\(\s*["\x27\x60][^"\x27\x60]*[-+]\s*\?|\b(decrement|increment)\s*\(|\$inc\b|\bF\(["\x27]|gorm\.Expr|update_all|updateMany|serializable|pg_advisory|get_lock\(|\bsetnx\b|(?-i:\bNX\b)|redlock' "${X[@]}" "${T[@]}" .

# 10. Find-or-create and exists-then-insert (§7), then the unique constraints that would make them safe.
rg -n -i --pcre2 '\b(findOrCreate|find_or_create_by|find_or_initialize_by|get_or_create|update_or_create|firstOrCreate|firstOrNew|updateOrCreate|FirstOrCreate|FirstOrInit)\b|\b(if|unless)\b[^\n]*\b(exists?(?!\w*Sync)\w*|existing\w*|already\w*|has_?(voted|claimed|redeemed|applied))\b|\b(ErrRecordNotFound|ErrNoRows|DoesNotExist|RecordNotFound|NoResultException|EmptyResultDataAccessException|ModelNotFoundException)\b' "${X[@]}" "${T[@]}" .
rg -n -i '\bunique\b|@@unique|UniqueConstraint|unique_together|uniqueIndex|uniqueConstraints' "${X[@]}" "${T[@]}" .

# 11. State that lives in one process (§8), then how many processes there are — replicas, autoscaler
#     bounds (HPA, KEDA), workers per host, and jobs in flight per worker.
rg -n --pcre2 '^(export\s+)?(const|let|var)\s+\w+\s*(:\s*[^=]+)?=\s*(new\s+(Map|Set|LRUCache|NodeCache)\b|\{\s*\}\s*;?\s*$)|^[A-Z_][A-Z0-9_]*\s*(:\s*[^=]+)?=\s*(\{\}|dict\(\)|defaultdict\(|TTLCache\(|LRUCache\()|^var\s+\w+\s*=\s*map\[|@(functools\.)?lru_cache|\bsync\.Map\b|rate\.NewLimiter|ConcurrentHashMap|Caffeine\.newBuilder|Bucket\.builder\(|MemoryStore|memory://|:memory_store|ThrottlerModule\.forRoot|\brateLimit\s*\(|\bslowDown\s*\(|Rack::Attack|RateLimiter::(for|attempt|hit)|throttle:' "${X[@]}" "${T[@]}" .
rg -n --pcre2 '^\s*(replicas|minReplicas|maxReplicas|minReplicaCount|maxReplicaCount|instances|desired_count|min_size|numReplicas|replica_count)\s*[:=]\s*["\x27]?([2-9]|\d{2,}|max|-1)\b|exec_mode\s*[:=]\s*["\x27]cluster|--(workers|concurrency)[ =]+\d|^\s*workers\s*[=(]|^\s*workers\s+\S|\b(WEB|WORKERS?|QUEUE|JOBS?|CELERYD?)_CONCURRENCY\b|^\s*concurrency\s*:|cluster\.fork\(|HorizontalPodAutoscaler|ScaledObject|pm\.max_children' "${X[@]}" "${T[@]}" .

# 12. Abuse-prone business actions (§9), then every limiter attachment. A route in the first with no
#     limiter on its chain is the candidate.
rg -n --pcre2 "$ROUTE" "${X[@]}" "${T[@]}" . | rg -i 'otp|verif|2fa|mfa|totp|coupon|voucher|promo|gift|redeem|invit|sms|resend|referr|reward|forgot|reset|balance|apply'
rg -n -i --pcre2 '\b(rate_?limit\w*|throttle\w*|slow_?down|limiter|RateLimiter|Bucket4j|Rack::Attack|ratelimit\w*|SkipThrottle)\b' "${X[@]}" "${T[@]}" .

# 13. The authorization matrix (§15): rows (routes), enforcement points (guards, policies, and custom guard
#     decorators such as @RequirePermission or @Roles), proof (role tests), test-side guard bypasses.
rg -n --pcre2 "$ROUTE" "${X[@]}" "${T[@]}" .
rg -n --pcre2 '@(\w*(Permission|Role|Guard|Grant|Polic(y|ies)|Abilit(y|ies))\w*|Require[A-Z]\w*|Scopes|Public|AllowAnonymous|PreAuthorize|PostAuthorize|Secured|RolesAllowed|PermitAll|DenyAll|login_required|permission_required|user_passes_test|staff_member_required|Authorized?)\s*\(|permission_classes|IsAuthenticated|IsAdminUser|Depends\(\s*\w*(auth|user|admin|role|perm)\w*|before_action\s+:\w*(auth|login|admin|role|require)\w*|\bauthorize[!(\s]|policy_scope|\bcan\?|Gate::(allows|denies|authorize)|->can\(|->authorize\(|middleware\(\s*\[?\s*["\x27](auth|can:|role:|permission:|verified|subscribed)|requireAuth|requireRole|isAuthenticated|hasRole|hasAuthority|hasPermission|RequireRole|casbin|\.Enforce\(' "${X[@]}" "${T[@]}" .
rg -n --pcre2 'actingAs\(|force_authenticate\(|force_login\(|@WithMockUser|@WithUserDetails|\.with\(\s*(user|jwt|oauth2Login)\(|\bsign_in\b|login_as\(|\b(tokenFor|loginAs|asUser|asAdmin|authAs|authHeader)\w*\(' "${X[@]}" .
rg -n --pcre2 'overrideGuard\(|overrideProvider\([^)]*(Guard|Policy)|dependency_overrides\[[^\]]*(perm|role|admin|require)|skip_authorization|skip_before_action\s+:\w*(auth|authorize)|withoutMiddleware\(' "${X[@]}" .

# 14. Account state on the auth path (§11): every file that admits a principal — strategy, guard, principal
#     loader, login, refresh, session, the user/membership entity — with its count of account-state reads.
#     A 0 admits a principal without consulting its state; read it first. Then entitlement reads (§10).
rg --files "${X[@]}" "${T[@]}" . | rg -i '(strateg|guard|principal|login|sign_?in|refresh|session|authenticat|current_?user|passport|membership|(user|member|account)s?[._-](entity|model|orm|schema))[^/]*$' | tr '\n' '\0' | xargs -0 -r rg -c --include-zero -i --pcre2 '\b(deleted_?at|is_?active|active|is_?enabled|is_?disabled|suspended\w*|banned\w*|deactivated\w*|disabled_?at|locked_?(at|until)|account_?status|soft_?delete\w*|SoftDeletes|paranoid|discard(ed)?_at)\b'
rg -n -i --pcre2 '\b(trial_?ends?_?at|trial_?expires?\w*|current_?period_?end|subscription_?(status|state|ends?_?at)|plan_?expires?\w*|grace_?period\w*|is_?(pro|premium|paid|subscribed)|has_?active_?subscription|entitle\w*|plan|tier)\b\s*(===?|!==?|==|!=|<|>|\))' "${X[@]}" "${T[@]}" .

# 15. Gates in the UI (§12) — comparisons, gate components (<Can>, <…Gate>, <…Guard>) and permission hooks —
#     then the server-side entitlement checks they must be mirrored by.
rg -n -i --pcre2 '\b(is_?pro|is_?premium|is_?paid|has_?feature|can_?use\w*|feature_?flags?|plan|tier|entitlements?|max_?seats|seat_?limit|is_?admin|role)\b\s*(===?|!==?|\.includes|&&)|(?-i:<(Can|[A-Z]\w*Gate|[A-Z]\w*Guard|Protected[A-Z]\w*)\b|\buse(Can|Permissions?|Entitlements?|Abilit(y|ies)|FeatureFlags?|Feature|HasRole|Roles?)\s*\()|v-if="[^"]*\b(plan|role|admin|can|feature|pro)|\*ngIf="[^"]*\b(plan|role|admin|can|feature|pro)|\{#if [^}]*\b(plan|role|admin|can|feature|pro)|\{%-?\s*if [^%]*\b(plan|role|admin|pro|premium|feature|perm)|<%-?\s*if [^%]*\b(plan|role|admin|pro|premium|can)|@can\(' \
  -g '*.{tsx,jsx,vue,svelte,html,erb,twig}' -g '*.blade.php' "${X[@]}" "${T[@]}" .
rg -n -i --pcre2 '\b(entitle\w*|has_?feature|feature_?enabled|is_?feature_?enabled|can_?use\w*|plan_?limit\w*|max_?(seats|projects|users|members)|seat_?limit|quota\w*|usage_?limit\w*|requires?_?plan|subscribed)\b|\b(plan|tier)\b\s*(===?|!==?|==|!=|in\b)' -g '!*.{tsx,jsx,vue,svelte,html,erb,twig}' "${X[@]}" "${T[@]}" .

# 16. Privilege grants and account-takeover flows (§13, §14) — including the routes that act on ANOTHER
#     member (password, status, restore) and the ones that mint a credential — then the re-auth markers.
rg -n --pcre2 "$ROUTE" "${X[@]}" "${T[@]}" . | rg -i 'password|email|phone|2fa|mfa|totp|otp|recovery|backup|passkey|webauthn|api[_-]?key|token|secret|role|member|owner|invite|profile|settings|/me\b|restore|activat|resume|suspend|status'
rg -n -i --pcre2 '\b(current_?password|old_?password|password_?confirmation|confirm_?password|verify_?password|re_?auth\w*|step_?up\w*|sudo_?mode|recent(ly)?_?(login|auth)\w*|fresh_?(login|auth)|requires?_?fresh|auth_?time)\b' "${X[@]}" "${T[@]}" .
```

**Measured on a real repo** (a NestJS-on-Fastify monorepo with MikroORM, ~11,400 files): `T` cut 5a from 3,884 lines to 737 and 2a from 1,281 to 703 — test and data files were 45–85 % of every list. Anchoring 14a to the auth path turned 5,140 lines into 83 files, 50 of them at 0. 13b had matched 3 of the 1,092 `@RequirePermission`-style decorators; it now matches all of them. 4a fell from 162 lines to 5 (four float money columns and one rating), because a courier's cash "float" and a "double count" are not types. 4d, 7b, 8c and the 11b worker terms each found a shape that only a reading had found before: a refund line repeated in one request, a wallet balance assigned and flushed, a debit that clamps, and worker concurrency × KEDA replicas.

## From candidate to finding

A grep hit is a place to read, never a finding. For each candidate:

1. **Trace to an entry.** Walk callers up to the route, consumer or job that reaches the line. No reachable entry → dismiss as dead code, and say so.
2. **State the invariant in one sentence, in business terms** — "an order is charged at most once", "a balance never goes below zero", "only a paid order ships", "a member cannot grant a role above their own". If no invariant can be stated, the hit is not this skill's.
3. **Find the enforcement point and classify it.**
   - none → finding;
   - client-side only (UI gate, hidden field, a value the request chose) → finding (§1, §12);
   - server-side, but a separate statement from the write → race finding (§5–§8), unless a row lock, version guard, conditional update or unique constraint ties check and act together;
   - atomic with the write → dismiss, citing that primitive's `<file:line>` from grep 9.
4. **Grade by what the attacker gets.** **critical** — money or credit created or moved without payment (client-chosen total, negative quantity refunded, confirmed double-spend), or self-escalation to admin. **high** — a paid or approval step skipped, a single-use code reusable, a deactivated account still acting, a double charge on retry, a grant above the grantor, an OTP with no attempt ceiling. **medium** — plan limits enforced only in the UI, an in-process limiter split across replicas, float rounding drift, entitlement fixed at login. **low** — overflow beyond any realistic value, a state skip with nothing of value behind it.
5. **Prove it, or mark it UNVERIFIED.** A test, the probe in § Proving a race, or a traced path from entry to write. A race read from code with no primitive between check and act stands as a finding even when the probe does not reproduce it — the window can be microseconds.

## Scans for

### 1. Client-trusted values (CWE-602, CWE-472)

```
BAD:   const { items, total, discount } = req.body
       await psp.charge({ amount: total })                      // attacker posts total: 1
GOOD:  const quote = await pricing.quote(cartId, user)          // catalog price, coupon, tax, currency reloaded
       await psp.charge({ amount: quote.total, currency: quote.currency })
```
Server-owned: price, unit price, total, subtotal, discount, tax, shipping, fee, **currency** (100 charged in the wrong currency is a 100× swing), role / admin flags, plan / tier, the owner / user / tenant id stamped on a create, and status. Grep 2 finds the reads, grep 3 the schemas that accept them. When 3a runs to thousands of lines, read in 3b's order. Classify each field once per route role: it is **input** on a route whose caller owns the value (a catalog admin sets the price) and **server-owned** on one whose caller does not (a buyer's checkout). Put that per-field allow-list in the report, so the next run reads only the fields nobody has classified. A hit is a finding when the value reaches a persistence write, a payment call or an authorization decision without being recomputed or overwritten server-side in the same flow. **Validation is not recomputation** — `@IsPositive() total` still lets the buyer choose the price. A whole-body bind is mass assignment: cite `@api-security-reviewer` API3 rather than re-reporting it; a tenant id from the request is `@tenant-isolation-reviewer`'s probe C.

### 2. Out-of-range numbers (CWE-1284, CWE-190, CWE-1339)

```
BAD:   quantity: number                         // -3 → negative line total → checkout refunds the card
       if (qty > stock) return reject()         // qty = NaN → every comparison is false → passes
       price: float                             // 0.1 + 0.2 != 0.3; rounding drifts per line
GOOD:  @IsInt() @Min(1) @Max(100) quantity      // integer, bounded on both sides
       money as integer minor units or a decimal type; reject non-finite input before any comparison
```
For every numeric input on a value path, try `-1`, `0`, `0.5`, `1e9`, `2147483648`, `NaN`, `Infinity`, `""`, `"12abc"`. Coercions accept more than they look: `Number("")` is `0`, `parseInt("12abc")` is `12`, `float("nan")` and `Decimal("NaN")` parse, `"abc".to_i` and `intval("abc")` are `0`. Flag money in `float` / `double` / `FloatField` / `float64` / `DOUBLE PRECISION` (grep 4a); a negative amount on a transfer (moves money backwards); a discount over 100 %; and a balance, points or ledger total in a 32-bit integer (`INTEGER`, `int32`, Java `int`) that aggregates — it wraps at 2,147,483,647 minor units. When the backend pack is installed, its `request-validation` pattern is the bounds contract (§ Bounds — nothing unbounded); without it, the GOOD above is.

**A ceiling checked one requested line at a time is bypassed by repeating the line** (grep 4d). `lines: [{ key: K, qty: 2 }, { key: K, qty: 2 }]` against 2 returnable units passes `min(requested, returnable)` or `if (line.qty > cap)` twice and refunds 4 — a till refund, a return credit, a stock reservation, a seat allocation. A lock on the request does not help, because the two lines are in one request. For each 4d hit that iterates the request's own lines, find where the lines are grouped by key. Either sum per key before the check, or refuse duplicates — `@ArrayUnique((l) => l.key)`, `unique_items`, a `Set` of keys. A unit test that sends a repeated key is the regression test.

**The same bug one layer down** (grep 4e). For each 4e hit, find where the lines are summed per key **before** the key is built. A document that stores one row per request line, plus a ledger leg keyed per product, is the repeated-line bug: the second leg's key already exists, the ledger replays it as a no-op, and the document still carries both lines. The source is debited once while the transfer or return records twice the quantity, and a later receipt or refund pays against the document. A `new Map(lines.map((l) => [key(l), l]))` lookup on the other side silently keeps the last duplicate, so a fit check reads a line nobody updated. Measured 2026-10-15 on a real NestJS + React monorepo: 8 hits, 2 true (a warehouse transfer's dispatch and receive legs, which let a member with only the transfer permission create stock), 1 integrity defect, 5 safe because the lines were aggregated first. Grep 4a also matches superseded migrations: before keeping a float-money hit, read the latest migration that touches that column.

### 3. Workflow step skipping (CWE-841)

```
BAD:   post('/orders/:id/ship', …) → update(id, { status: 'shipped' })    // from any state, paid or not
       order.status = req.body.status                                    // the client picks the state
GOOD:  UPDATE orders SET status = 'shipped' WHERE id = :id AND status = 'paid'   -- 0 rows → 409
       one transition table ({ paid: ['shipped', 'refunded'], … }) checked in one place
```
For each state write (grep 5a), name the states it is legal *from* and find that precondition — in the write's `WHERE`, behind a lock, or in a state machine (grep 5b). An `if` on a copy loaded earlier is §5 as well. Shapes: ship / fulfil / deliver without paid; **approve your own request** (approver equals requester); re-open closed, cancelled or refunded; refund an already-refunded order; call step 3 of a wizard directly when no server record says step 2 completed; status set from the request body; a late provider event (`charge.failed` after `refunded`) re-opening a settled record. A `status` field in a request is safe only when it is an *action* mapped through the transition table against the current state.

### 4. Missing idempotency on money and side-effect endpoints (CWE-837)

```
BAD:   post('/orders/:id/pay', …) → await psp.charge(amount); await markPaid(id)
       // client retry, double-click, proxy retry → a second charge
GOOD:  Idempotency-Key required; INSERT INTO idempotency_keys (principal_id, key, request_hash) inside the
       transaction that writes the payment row; a replay returns the stored response; the outbound charge
       carries the provider's idempotency key derived from the order id
```
Targets (grep 6): every endpoint that moves money, issues credit, creates an order, or sends something that costs money, and every webhook consumer — providers redeliver by design, so the provider's event id is stored under a unique constraint in the same transaction as the business write. A status check (`if (order.paid) return`) is not idempotency under concurrency; it is §5. When the distributed-systems pack is installed, its `idempotency` pattern is the storage contract (§ Server-side storage (stack-agnostic schema), § State transitions with preconditions); when the backend pack is installed, `webhook-flow` owns the replay window and `request-validation` the key's shape (§ Idempotency-key / header validation). Without either, the GOOD above is the contract. **Queue and webhook-job consumers** that move money or credit: when the distributed-systems pack is installed, those rows arrive from its `messaging-scan` §2 with the redelivery or stall evidence (a stalled job that runs twice, an ack after the effect) — grade the money impact here, never re-derive the delivery semantics; without the pack, §4 reads the consumer itself.

### 5. Check-then-act on a balance, stock or limit (CWE-362, CWE-367)

```
BAD:   const w = await wallets.get(userId)
       if (w.balance >= amount) {                                        // 20 requests all read 100
         await wallets.update(userId, { balance: w.balance - amount })   // all write 100 - 80
         await payout(amount)                                            // 20 × 80 paid from 100
       }
GOOD:  UPDATE wallets SET balance = balance - :amt WHERE user_id = :u AND balance >= :amt
       -- rows affected 0 → insufficient funds; check and act are one statement; payout after commit
```
Grep 8a gives the guard, grep 7 the in-memory read-modify-write (`stock -= 1; save()` — a lost update even without a guard), grep 9 the primitives. Close it with, in order: the atomic conditional update; a row lock held across check and act; an optimistic version guard with retry; and, for an invariant across rows ("at most 5 projects on the free plan" — count then insert), a lock on the parent row or `SERIALIZABLE` with retry. **Wrapping the two statements in a transaction at the default isolation level does not close it.** When the backend pack is installed, its `transaction-boundary` pattern (the isolation table and detector 3) sets the isolation and retry rules; when the database pack is installed, `transaction-isolation` covers locking and write skew. Without them, the order above is the rule. A check-then-act inside a **queue consumer or scheduled job** (a balance debited by a job that can re-run after a stall or run on two workers) arrives, when the distributed-systems pack is installed, from `messaging-scan` §2 / §6 or `coordination-scan` §4 (a lease shorter than the work) with the redelivery, stall or overlap evidence; §5 grades the money side and does not re-derive it.

**The clamped debit** (grep 8c) is the variant to look for when check and act are far apart. The shape is: a pre-flight read of the balance (`canAfford()`), then an expensive side effect (a paid model call, an SMS, a provider charge), then a debit that **clamps at zero** instead of refusing (`max(0, balance - cost)`, `balance + delta < 0 ? -balance : delta`). Every concurrent request passes the read, and every one gets its side effect. Because the debit cannot fail, the overrun is never even recorded. The bound is the number of requests in flight at once — worker concurrency × replicas from grep 11b — not "one unlucky request". Fix: reserve before the side effect (lock, refuse when short, debit, commit; refund on failure), or one conditional `UPDATE … WHERE balance >= :cost`. A debit that clamps is acceptable only where the side effect is free. **When the 8c hit is a shared helper** (a wallet module's `applyCredits()`), the race is at each caller, not in the helper: list them (`rg -n '\b<helperName>\(' .`) and read each for a lock taken before the affordability read. Measured on a real monorepo: one clamping helper, 8 callers, 1 vulnerable (it read the balance unlocked before a paid model call), 7 locked first.

### 6. Single-use enforced by read-then-write (CWE-837, CWE-367)

```
BAD:   const c = await coupons.findByCode(code)
       if (c.usedAt) return conflict()
       await coupons.update(c.id, { usedAt: now })            // 20 parallel requests all saw usedAt = null
       await credit(user, c.value)
GOOD:  UPDATE coupons SET used_at = now(), used_by = :u WHERE code = :c AND used_at IS NULL
       -- 1 row → this request owns the redemption; 0 rows → already used
       per-user-once: INSERT INTO redemptions (coupon_id, user_id) under UNIQUE (coupon_id, user_id)
```
Coupons, vouchers, gift cards, invite tokens, password-reset and magic-link tokens, email verification, referral bonuses, one vote per user, one free trial per account. A `max_uses` counter is the same bug: `uses < max_uses` then `uses += 1` becomes `… SET uses = uses + 1 WHERE id = :id AND uses < max_uses`. Consuming a token is a conditional delete or update that returns the row (`DELETE … RETURNING`), never a read followed by a delete.

### 7. Find-or-create without a unique index (CWE-362)

```
BAD:   if (!await votes.exists({ userId, pollId })) await votes.create({ userId, pollId })
       User.find_or_create_by(email: params[:email])            # no unique index on users.email
GOOD:  UNIQUE (user_id, poll_id) in a migration + insert-on-conflict-do-nothing,
       or create and treat the unique violation as "already exists"
```
A helper is only as safe as the constraint under it: Django `get_or_create`, Rails `create_or_find_by` and Laravel `createOrFirst` rely on one; Rails `find_or_create_by`, Laravel `firstOrCreate`, Sequelize `findOrCreate` and GORM `FirstOrCreate` are a find then an insert. A model-level uniqueness validation is a read, not a constraint. Grep 10a lists the helpers and exists-then-insert shapes, 10b the constraints — the finding is a helper on a column set no unique constraint covers. Check normalisation too: `UNIQUE (email)` with a case-insensitive lookup lets `A@x.com` and `a@x.com` both sign up for the free trial — index `lower(email)` or a case-insensitive type. Duplicates matter when they carry value: double trials, double seats, double votes, double referral rewards.

### 8. Limits, quotas and counters held in one process (CWE-362, CWE-799)

```
BAD:   const attempts = new Map()                        // per process: 4 workers × 3 pods = 12 counters
       rateLimit({ windowMs: 60_000, max: 5 })           // default store is process memory
GOOD:  a shared store — Redis INCR + EXPIRE, the limiter's Redis / database store, or a DB counter
       advanced by an atomic conditional update
```
Attempt counters, quotas, daily limits, "last sent at", single-flight locks and dedupe sets in a module-level map, an LRU, `lru_cache`, `sync.Map`, `ConcurrentHashMap`, a process-local mutex, or a limiter's default memory store are per process (grep 11a). Multiply by workers per host — gunicorn / uvicorn `--workers`, PM2 cluster, Puma workers, Node `cluster`, PHP-FPM children — and by replicas (grep 11b); every deploy resets them. A mutex (`synchronized`, `sync.Mutex`, an async lock) around a database check-then-act fixes it on one process only. Severity follows what the limit protects — an OTP attempt ceiling is high, a paid-resource quota medium. When the backend pack is installed, its `rate-limiting` pattern is the shared-counter contract (§ Distributed counter store); without it, the GOOD above is.

### 9. No rate limit on abuse-prone business actions (CWE-799, CWE-307, CWE-770)

Actions where every request is a guess or costs money: OTP / 2FA / email-code verification (a 6-digit code is 10⁶ guesses), coupon, promo and gift-card check or redeem (code enumeration), invite send, SMS and phone-verification send (SMS pumping — the attacker earns on your toll bill), referral claim, gift-card balance check, password-reset request. For each route grep 12 lists: a limiter is attached server-side; it is keyed by the thing being guessed (the challenge, the account, the code space), not only by IP; it uses a shared store (§8); and the guess budget is bounded over the code's lifetime — lock the challenge after N attempts, not N per minute forever. When the backend pack is installed, its `rate-limiting` pattern sets the key choice (§ Key dimension — what to limit by); without it, key by the guessed thing as above. Login brute force is `@auth-reviewer`'s; generic route caps and anti-automation are `@api-security-reviewer` API4 / API6. This detector owns the business actions a login limiter never covers.

### 10. Subscription, trial and plan checked at the wrong time (CWE-367, CWE-613)

```
BAD:   plan stamped into the access token at login, read on every request   // cancelled: Pro until refresh
       if (trialEndsAt > body.clientNow) …                                   // the client's clock
GOOD:  entitlement read server-side at the action, from billing's source of truth or a cache the billing
       webhook invalidates
```
Grep 14b. Flag: plan or entitlement held in a token claim or long-lived session; expiry compared against a client-sent time; a check on *start* of a multi-step flow but not on *commit* (start checkout at the trial price on day 13, confirm on day 20); a usage period boundary read once and cached; a downgrade that keeps the seats, projects or storage of the old plan.

### 11. Deactivated, suspended or soft-deleted accounts still able to act (CWE-613, CWE-285)

```
BAD:   verify(token) → req.user = claims                    // a suspended user's token works until exp
       User.findById(id)                                    // a soft-deleted row still resolves
GOOD:  the principal loader rejects inactive / suspended / deleted on every request, or every state change
       revokes the account's sessions, refresh tokens and API keys
```
Read every file in grep 14a, the zeros first, and check three doors, not only the loader: **login**, **refresh**, and the per-request principal. A 0 on a file that admits nobody (a DTO or guard whose name merely contains "session" or "refresh") is expected — 64 of 77 files on a real monorepo; drop it after one look at what the file does. A loader that empties a paused member's permission set still leaves them signed in. So intersect the deactivated column (§15) with every route that needs **no** permission — own-account, self-scoped, "the session is the subject" — and check whether membership liveness is read there. Emptying the key set closes nothing on a route that never asked for a key. Also:
- API keys and tokens minted by a deactivated user, still working;
- a member removed from an organisation who keeps a cached membership;
- invitations from a paused or removed inviter that still redeem. Pause and remove should revoke them, or accept should re-check the inviter's current grants.

Revocation mechanics are `@auth-reviewer`'s; this detector owns whether the account state is consulted at all.

### 12. Feature flags and plan limits enforced only in the UI (CWE-602)

```
BAD:   {user.plan === 'pro' && <ExportButton/>}   →   POST /api/export with no plan check
GOOD:  the handler checks the same entitlement; the UI gate is cosmetic
```
For each gate grep 15a lists, find the API call behind the gated control and its handler; the handler checks the entitlement (grep 15b) or it is a finding. Same for seat, project and file-size limits enforced only in form validation, and for flags evaluated client-side that gate a server capability. UI role gates — a `<Can>` wrapper in React, a `v-if` in Vue, an `*ngIf` in Angular, an `{#if}` in Svelte — are proved server-side in the matrix (§15).

### 13. Privilege grants beyond the grantor (CWE-269, CWE-266)

```
BAD:   members.update(id, { role: dto.role })            // an admin grants 'owner'; a member grants 'admin'
GOOD:  rank(dto.role) <= rank(actor.role) && actor manages the target's organisation;
       ownership transfer is its own flow; the last owner cannot be demoted
```
Invite with a role, change a member's role, mint an API key or token with scopes beyond the creator's, transfer ownership, map an SSO or SCIM group whose name the attacker controls. Accepting an invite binds to the invited identity and is single-use (§6). A role reaching the entity through a whole-body profile update is mass assignment — `@api-security-reviewer` API3; this detector covers the flows that take a role on purpose. Three grants hide under other names; each must pass the same grant-only-what-you-hold check (target keys ⊆ actor keys) as a role change:
- **A credential, minted or revealed.** Read the authenticator, not the minting route. Ask which principal the key, token or integration secret resolves to on use. A key minted by a delegated member that authenticates as the **owner** is a grant of the owner's whole key set. It must resolve to its minter, be bounded by the minter's keys, and die with the minter. A "view" permission that reveals a secret which writes is the same grant.
- **Becoming a colleague.** Any act that lets the actor sign in as another member grants that member's keys: a password reset by an admin, a login-identifier change, a session minted for them, impersonation.
- **Re-activation.** Resuming a paused member, restoring a deleted one, or re-enabling a paused role hands its key set back. Pausing grants nothing; the way back does.

Grep 16a lists these routes.

### 14. Account-takeover flows without re-authentication or binding (CWE-620, CWE-640)

Password change, email or phone change, 2FA disable or reset, recovery-code regeneration, passkey add or remove, API-key creation (grep 16). Each requires, on the action itself and server-side: re-authentication (current password, a fresh `auth_time`, or step-up); an email change confirmed at the **new** address and notified at the **old**; a token bound to user + purpose + the current address, single-use (§6) and short-lived; and other sessions revoked after a password change. Token storage, TTL and the step-up ceremony are `@auth-reviewer`'s (§ Passwords, § Step-up bypass); this detector owns the flow precondition — can step N run without step N-1 having happened for *this* user and *this* purpose.

### 15. Per-role authorization matrix — every cell proved (CWE-285, CWE-862, CWE-863)

1. **Rows** — routes from grep 13a: on a diff, the changed routes plus every route sharing their guard chain; on a whole-repo run, all of them. Collapse routes with an identical guard chain into one **guard class**: prove the class once, then prove each route belongs to it. Grep 13a gives the line, not the chain. On a whole repo, build a route table with a short script: per handler, the verb and the full path (class prefix + route path), the decorator stack above it with multi-line decorators joined, and the class-level decorators. Then key each guard class on the set of guard decorators. Only the table shows a route that two guards admit, or a guard set once on the class.
2. **Columns** — anonymous · user · other-tenant user · admin · deactivated user · expired-subscription user · **a credential minted by a delegated member** (API key, sheet or integration key, MCP or service token), plus the project's own roles from grep 13b. On a single-tenant app the other-tenant column is `n/a`; with no machine credential, the minted-credential column is.
3. **Expected value** per cell from the declared policy — role decorators, policy classes, an ADR, a roles doc. A mutating route with no declared policy is itself a finding: `policy undeclared`.
4. **Proof** per cell, one of: `test:<file:line>` — a test that authenticates as that role through the **real** guard and asserts the status (grep 13c; a test listed by 13d stubs the guard and proves nothing); `trace:<route file:line>→<guard file:line>` — the guard is unconditional on that path; `probe:<status>`. Anything else is `UNPROVED`.
5. **Flag** every UNPROVED cell whose expected value is deny on a mutating or data-returning route, and every observed allow where the policy says deny (`FAIL`). The deactivated, expired-subscription and minted-credential columns are where matrices are usually empty — and where they fail.

Vertical escalation shows up as an allowed cell on a guard class above the column's role (a user or deactivated account reaching an admin route); horizontal escalation as the user column allowed on another user's object. Both reach this skill only as FAIL or UNPROVED cells. A cell that fails on object ownership goes to `@api-security-reviewer` (API1 / API5), on the tenant boundary to `@tenant-isolation-reviewer`, on the token or session to `@auth-reviewer`. This skill reports the matrix and its unproved cells; it does not re-derive their findings.

## Proving a race

Run only against a local or staging instance the operator has named, with a disposable test account and the payment provider in test mode — never production.

```bash
BASE=http://localhost:3000; TOKEN='<test-user token>'; N=20
curl -s -H "Authorization: Bearer $TOKEN" "$BASE/api/wallet"                 # 1. record the invariant's input
seq "$N" | xargs -P "$N" -I{} curl -s -o /dev/null -w '%{http_code}\n' \
  -X POST "$BASE/api/coupons/redeem" -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' -d '{"code":"WELCOME10"}' | sort | uniq -c   # 2. N requests at once
curl -s -H "Authorization: Bearer $TOKEN" "$BASE/api/wallet"                 # 3. re-read the invariant
```

**Pass:** exactly one `2xx`, `N-1` rejections, the state changed once. **Fail:** more than one `2xx`, or the state changed more than once — a confirmed race, graded by the invariant. The idempotency variant sends one fixed `Idempotency-Key` header with all N: one side effect, N identical responses. The per-process limiter variant sends three times the limit and counts the `429`s. A pass does not clear code that shows check-then-act with no primitive; tighten the window (an HTTP/2 single-packet send, or a test seam that pauses between check and act) or let the static finding stand. The regression test that proves the fix runs two calls concurrently (`Promise.all`, a thread pool, goroutines) against a **real** database — a mocked repository cannot race.

## Output

```
logic-race-scan — <scope>

Findings: 4

1. src/wallet/withdraw.service.ts:41                       [report-with-fix]   critical
   Invariant: a balance never goes below zero. Check (:38 `if (w.balance >= amt)`) and debit
   (:41 `update({ balance: w.balance - amt })`) are separate statements, no lock, no version.
   Probe: 20 parallel withdrawals of 80 from 100 → 7 × 200, balance -460.
   Fix: UPDATE wallets SET balance = balance - :amt WHERE user_id = :u AND balance >= :amt;
   0 rows → 409; payout after commit.

2. src/checkout/checkout.controller.ts:22                  [report-with-fix]   critical
   Invariant: the buyer pays the catalog price. `total` read from req.body (:19) is passed to
   psp.charge (:22); no recomputation on the path.
   Fix: price the cart server-side from catalog + coupon + tax; accept ids and quantities only.

3. src/orders/fulfilment.controller.ts:57                  [report-with-fix]   high
   Invariant: only a paid order ships. `update(id, { status: 'shipped' })` with no state precondition.
   Fix: UPDATE … SET status = 'shipped' WHERE id = :id AND status = 'paid'; 0 rows → 409.

4. src/auth/verify-code.controller.ts:15                        [report-flagged]    high
   Invariant: a 6-digit code survives guessing. Limiter (src/middleware/limiter.ts:3) uses the default
   memory store; 3 replicas (k8s/deploy.yaml:4) × cluster mode → per-process counters, no per-challenge cap.
   Fix: shared store + lock the challenge after 5 attempts. Flagged: needs the shared store provisioned.

Authorization matrix — 14 routes in 5 guard classes × 6 roles: 61 proved · 17 UNPROVED · 2 FAIL
  route                      class       anon       user       other-tenant  admin      deactivated  expired-sub
  POST /orders/:id/refund    G2 admin    401 test   403 test   UNPROVED      200 test   UNPROVED     n/a
  POST /exports              G1 auth     401 trace  200 test   n/a           200 trace  FAIL (200)   FAIL (200)
  …

Class coverage
  §1  client-trusted values           checked (9 hits → 1 finding)
  §2  out-of-range numbers            checked (12 hits → 0 findings)
  §3  workflow step skipping          checked (21 hits → 1 finding)
  §4  idempotency                     checked (6 hits → 0 findings)
  §5  check-then-act                  checked (7 hits → 1 finding)
  §6  single-use read-then-write      checked (3 hits → 0 findings)
  §7  find-or-create                  checked (4 hits → 0 findings)
  §8  in-process limits               checked (2 hits → 1 finding, merged into #4)
  §9  abuse-prone rate limits         checked (5 routes → 1 finding)
  §10 entitlement timing              N/A (no subscription or plan model in the repo)
  §11 inactive accounts               checked (1 loader → 0 findings; matrix FAIL cells cited)
  §12 UI-only gates                   checked (8 gates → 0 findings)
  §13 privilege grants                checked (2 flows → 0 findings)
  §14 account-takeover flows          N/A (authentication delegated to an external IdP; no local flows)
  §15 authorization matrix            checked (14 routes → 17 UNPROVED, 2 FAIL)
```

`[report-with-fix]` — the fix is a local patch in the project's primitive. `[report-flagged]` — the fix needs a design or infrastructure decision (an idempotency contract with clients, a state-machine owner, a shared store to provision). Every detector appears in the coverage block as `checked (k hits → m findings)`, `N/A (<reason: no such surface in the repo>)` or `blocked (<reason>)` — "found nothing" and "did not look" must read differently.

## False positives / gotchas

- **A transaction is not a lock.** `BEGIN; SELECT balance; UPDATE …; COMMIT` at `READ COMMITTED` races exactly like no transaction, and a plain `SELECT` under MySQL's `REPEATABLE READ` reads a snapshot. Only a conditional update, `FOR UPDATE`, a version guard, a unique constraint or `SERIALIZABLE` with retry closes it.
- **One thread does not save you.** Every `await` between check and act is a yield point in Node; a GIL serialises bytecode, not your two database round trips.
- **Seller versus buyer.** A price from the request is correct on a catalog-admin route guarded for that role — the field is server-owned for buyers and input for sellers. Read who calls it.
- **A unique index on the wrong columns** (unique on `code` when the rule is once per `(code, user)`) is still §6 / §7.
- **No hit in grep 11b is not evidence of a single instance.** Rolling deploys run two copies, autoscalers add more, and a worker count above 1 splits memory on one host.
- **A webhook arriving twice or out of order is the provider working as designed** — the finding is the consumer that assumes otherwise.
- **A test hit that gets past `T`** is not a production path. That means a test folder under another name, a seed or one-off script under `scripts/`, or a fixture in source. Dismiss it, keep it out of the coverage count, and add the folder to `T` for the rest of the run.
- **A lock mode written as a number** (`lockMode: 2`) is read as what the ORM's enum says, not what the author meant. In MikroORM 6, `2` is `PESSIMISTIC_READ`: a shared lock, so two readers both pass the check.

## When to run

- On any diff touching money, quantity, balance, coupon / invite / redeem, a status transition, a role grant, or a find-then-write sequence — `/security-audit`'s signal for this skill.
- On every whole-repo `/security-audit` run, regardless of signal.
- Before launching payments, promotions, referrals, a free trial, public sign-up, or a new paid plan.
- After an incident involving duplicate charges, negative balances, reused codes or an unexpected role.

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`finding-verification.md`](../../../../snippets/finding-verification.md). Under `/security-audit` that happens in Phase 4; run standalone, it applies the protocol as a separate second pass, tags those rows `self-verified`, and lists the rest as Unconfirmed, Hardening or Refuted — never drops them.
- Halt on any finding without the sink `<file:line>` + the invariant + the failing condition + the fix.
- Do not report a grep hit as a finding — each one gets the read described in § From candidate to finding, nothing less.
- Do not run the race probe (§ Proving a race) against production, against a host the operator has not named, or with real payment instruments.
- Do not mark a matrix cell proved from a decorator you saw — proof is a test through the real guard, a traced unconditional guard, or a probe.
- Do not propose an in-process lock, a transaction at the default isolation level, or a model-level uniqueness validation as a race fix.
- Do not re-report IDOR, mass assignment, cross-tenant access or token findings — cite the owning agent's line.
- Do not end without the class coverage block.

## Related

- `/security-audit` — dispatches this skill on its A06 signal and on every whole-repo run; reads the class coverage block into its class ledger.
- `/security-fix` — closes these findings; the race probe or the concurrent regression test is the failing-first exploit test.
- `@security-auditor` — its A06 Insecure Design bullet is the detector; this skill is the executor behind it.
- `@api-security-reviewer` — API1 BOLA and API3 mass assignment (hand-offs from §1, §13, §15); API4 / API6 caps and anti-automation (adjacent to §9).
- `@tenant-isolation-reviewer` — the other-tenant column's failures; tenant id from client input (its probe C).
- `@auth-reviewer` — login brute force, session and token revocation, reset-token storage, step-up enforcement (adjacent to §9, §11, §14).
- `threat-model-method` — enumerate the business flows and their invariants before a new feature ships; its output is this skill's invariant list.
- `backend/ai-patterns/transaction-boundary.md`, `backend/ai-patterns/rate-limiting.md`, `backend/ai-patterns/request-validation.md`, `backend/ai-patterns/webhook-flow.md` — the contracts behind §2, §4, §5, §8 and §9 when the backend pack is installed. Without it, the lane table and the GOOD blocks here are the whole contract.
- `distributed-systems/ai-patterns/idempotency.md` — the idempotency storage contract for §4 when the distributed-systems pack is installed; without it, §4's GOOD block.
- `database` `transaction-scan` (database pack, when installed) — the transaction side of §5: lock order (§3), retry on serialization failure (§4) and write skew (§7) there, with `database/ai-patterns/transaction-isolation.md` as the method. Without the database pack, §5's ordered fixes.
- `rules/security-principles.md` — the Should on server-enforced flow ordering and anti-automation.
