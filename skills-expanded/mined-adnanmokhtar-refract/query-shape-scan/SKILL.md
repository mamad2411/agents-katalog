---
name: query-shape-scan
description: Find reads whose cost grows with the table — no LIMIT on a growing table, deep OFFSET, over-fetch, predicates no index can serve, filtering or paging in application code, counts used as existence checks, unbounded IN lists, unstable page order — each proved by a plan or a seeded-cap test.
kind: skill
pack: database
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: query-shape-scan

## Premise

A query can be correct today and wrong next year without a line changing. `findMany({ where: { sellerId } })` returns 40 rows in staging and 400,000 for the biggest seller; `ILIKE '%term%'` is instant on a 10,000-row table and a full scan on a 10-million-row one; `OFFSET 50000` reads and discards 50,000 rows before returning 20. These defects are visible in the code alone. They become outages when data grows, and they are the classes a model reviewing code without a checklist misses: in Neon's published skill evaluation (runs of 2026-03-11 to 03-15), the baseline flagged missing pagination in **0 of 89** runs and JOIN duplication of a wide parent in 28%; a per-class checklist raised them to 57% and 100%. This skill is that checklist with detection behind it.

**Every finding cites the statement `<file:line>` + the table and its growth class + the entry point that reaches it + the missing control (cap, keyset, projection, index-servable predicate, `EXISTS`, chunking, tiebreaker) + the proof or the probe that would settle it + the fix in the project's ORM.** A grep hit is never a finding by itself, and "no query-shape issues" is never printed without the class-coverage block (§ Output).

**Growth decides, syntax does not.** `findAll()` on a 250-row country table is fine; the same call on `orders` is the finding. Every candidate is read against the table's **growth class**: append-only or event, per-tenant growing, or bounded lookup. A cost claim needs its oracle to fire, a plan on production-shaped data or a seeded-cap test, before it is a Finding ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6). Without a database or harness the candidate is **Unconfirmed**, with the `EXPLAIN` or the test that would settle it. It is never dropped and never promoted on reading alone.

## Boundaries

- A query per element of a loop, a resolver per parent, rows multiplied by a multi-collection join → `n-plus-one-scan` (this pack). This skill owns the **shape of one statement**.
- Which index a predicate needs, composite order, redundant and unused indexes → `index-coverage-scan` (this pack). §4 here owns predicates **no** index can serve as written, and the rewrite or expression index that changes that.
- The pagination **contract** (envelope, cursor format, max page size as an API rule) → backend's `pagination.md`, when the backend pack is installed. This skill finds where the contract is missing or bypassed.
- A filter that can vanish (an `undefined` key) and so returns another tenant's rows → this skill reports the query shape. The cross-tenant read goes to `@tenant-isolation-reviewer`, when the security pack is installed; without it the row is tagged `security-class (owner pack not installed)` ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 9).
- Full buffering of a large result into a response, and memory growth from it → `request-path-scan` § 6 (performance pack, when installed). The unbounded **query** behind it is §1 here.
- Plan diagnosis of one known slow statement → `@query-optimizer` / `/optimize-query`. The full-text design → `full-text-search.md` (this pack's pattern).
- A multi-page **extract** (an export, a dump, a sync) over a table that changes while it is read — whether the copy is faithful and consistent → data-engineering `extract-scan` §1, when installed. §2/§8 here keep the deep-OFFSET cost and the paged API's sort key.

## Adapt to the codebase

Read the ORM, engine and version from the lockfile, compose image or Terraform, not from memory; the ORM lane table in `n-plus-one-scan` § Adapt lists the versions this pack keys on. Print the lanes you ran. The primitives per lane:

| Lane | Read with no cap (§1) | Cap + keyset primitive (§1, §2, §8) | Projection (§3) | Index-servable search (§4) | Existence (§6) |
|---|---|---|---|---|---|
| **MikroORM** 6 / 7 | `em.find(E, where)` with no `limit`; `findAll()` | `limit` + `orderBy`; `em.findByCursor(E, where, { first, after, orderBy })`, which also runs a `count` unless `includeCount: false` (6.6.16) | `fields`, `exclude`, `@Property({ lazy: true })` on wide columns | `$ilike: '%q%'` needs a `pg_trgm` GIN index; `$like: 'q%'` a pattern-ops or C-collation index | `em.findOne(E, where, { fields: ['id'] })` |
| **TypeORM** 0.3 / 1.x | `find()` / `findBy()` / `getMany()` with no `take` | `take`, keyset `where: { id: MoreThan(cursor) }` ordered by id | `select` | `ILike('%q%')` needs trigram | `findOne({ select: { id: true }, where })` |
| **Prisma** 6 / 7 | `findMany()` with no `take`. A key set to `undefined` is treated as absent (Prisma docs, *null and undefined*), so a missing value widens the filter | `take` + `cursor: { id }, skip: 1` | `select` | `contains` is an infix match and `mode: 'insensitive'` a case-insensitive one: read the emitted SQL, then index that expression | `findFirst({ where, select: { id: true } })` |
| **Sequelize** 6 | `findAll()` with no `limit` | `limit`, keyset on `[Op.gt]` | `attributes` | `[Op.iLike]: '%q%'` needs trigram | `findOne({ attributes: ['id'] })` |
| **Drizzle** 0.45 | `db.select().from(t)` with no `.limit()` | `.limit()` + `where(gt(t.id, cursor))` | `select({ … })`, relational `columns` | `ilike(col, '%q%')` | `.limit(1)` |
| **SQL / Knex / pg / mysql2** | `SELECT … FROM` with no `LIMIT` | `LIMIT` + `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC` | explicit column list | `ILIKE '%q%'` → `pg_trgm` GIN; `lower(col) = $1` → index on `lower(col)` | `SELECT EXISTS (…)`, `LIMIT 1` |
| **Mongoose** 9 | `find({})` with no `.limit()` | `.limit()`, `_id` range | `.select()`, `.lean()` | an unanchored or `i`-flag `$regex` cannot use an index range efficiently | `exists()` |
| **Django / DRF** | `.all()` / `.filter()` returned unsliced; a DRF list view with no `pagination_class` and no `DEFAULT_PAGINATION_CLASS` | `qs[:n]`, `CursorPagination`; `.iterator(chunk_size=…)` in jobs | `.only()`, `.values()`, `.defer()` | `__icontains` / `__iexact` match case-insensitively, so a plain B-tree cannot serve them: index the expression the backend emits (query log) | `.exists()`, not `.count() > 0`; `len(qs)` loads every row |
| **SQLAlchemy** 2.x | `.scalars(…).all()` with no `.limit()` | `.limit()`, keyset | `load_only()`, `defer()` | `ilike('%q%')` | `select(exists().where(…))` |
| **Rails** 7.2–8.1 | `Model.all.each`, `where(…).each` | `limit`, `find_each` / `in_batches` (ordered by primary key) | `select(:a, :b)`, `pluck` | `where("name ILIKE ?", "%#{q}%")` needs trigram | `exists?`; `.size` runs a `COUNT` only when the relation is not loaded (Rails API, *Relation#size*) |
| **Laravel** 12 / 13 | `::all()`, `->get()` | `->cursorPaginate()` (keyset; it needs a unique, non-null ordering), `->simplePaginate()` (OFFSET, no count), `->paginate()` (OFFSET + count); `chunkById` / `lazyById` in jobs | `->select([…])` | `where('name', 'like', "%{$q}%")` | `->exists()`, not `->count() > 0`. `paginate()` counts every matching row first (Laravel docs, *Pagination*) |
| **Spring Data / JPA** (Hibernate 6.6 / 7) | `findAll()`; `List<T> findBy…` with no `Pageable` | `Slice<T>` (no count query), `Page<T>` (runs one; Spring Data JPA docs), `Pageable`, `Limit`, `findFirst10By…`. A collection `JOIN FETCH` + `setMaxResults` pages **in memory** (`HHH90003004`) | DTO / interface projections | a derived `…ContainingIgnoreCase` is an infix `like` on `upper(col)` | `existsBy…` |
| **GORM** v1.31 | `Find(&rows)` with no `Limit` | `Limit`, keyset `Where("id > ?", c)`, `FindInBatches` | `Select("a", "b")` | `Where("name ILIKE ?", "%"+q+"%")` | `Limit(1).Find` |
| **EF Core** 10 | `.ToListAsync()` with no `.Take()` | `.Take()`, keyset `.Where(x => x.Id > c)` | `.Select(x => new { … })` | `.Contains(q)` / `EF.Functions.ILike` (Npgsql) are infix matches: read the emitted SQL | `.AnyAsync()`, not `.CountAsync() > 0` |
| **GraphQL** connections | `first:` / `limit:` argument with no server maximum | a clamped `first`, cursor `after` | the selection set | — | a `totalCount` resolved for every page is §6 |

## Context before hunting

On a whole-repo run, build one map before reading any candidate. Every later decision reads it:

1. **Growth class per table** a candidate touches: append-only or event (orders, messages, ledger, audit), per-tenant growing, or bounded lookup (countries, currencies, settings, enums). Read it from the entity name, the migrations and the code that inserts. With a reachable copy, read the real sizes: `SELECT relname, reltuples::bigint FROM pg_class WHERE relkind = 'r' ORDER BY reltuples DESC LIMIT 30;` (MySQL: `information_schema.TABLES.TABLE_ROWS`).
2. **Where the caps live.** A base repository or list-projection helper, a global paginator (`DEFAULT_PAGINATION_CLASS`, a Nest interceptor), DTO maximums (`@Max`, zod `.max()`), and the search indexes (grep 4e).
3. **Workload, if any.** `pg_stat_statements` (`rows / calls`, `total_exec_time`) or MySQL `performance_schema.events_statements_summary_by_digest` (`SUM_ROWS_SENT / COUNT_STAR`, `SUM_NO_INDEX_USED`) ranks the statements that already return too much. Read `stats_reset` first: empty or freshly reset stats are "no evidence", not "no problem".

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**. Every `rg` names its path (`.`): with none, `rg` reads stdin whenever stdin is a pipe, which under an agent's shell is a silent zero-hit run. A lane line that prints `No files were searched` is an `N/A` reason. Any `rg` error on stderr (exit 2) is a failed grep, never zero hits.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**'
   -g '!**/.venv/**' -g '!**/*.min.*' -g '!**/*.{md,lock,map,svg,json,snap,yml,yaml}')
T=(-g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,seeds,seeders,migrations,migrate,locales,i18n,generated,__generated__,.prisma,temp}/**'
   -g '!**/*.{spec,test,e2e-spec,mock,stories,test-data,doc}.*' -g '!**/{*_test,*_spec,test_*,conftest}.*' -g '!ai/**' -g '!docs/**')
C='^(?![ \t]*+(?://|/?\*|#(?!\{)|--|<!--))[^\n]*?'      # skip comment lines: JSDoc, docstrings and SQL comments quote queries
LIM='take|limit|first|last|top|perPage|per_page|pageSize|page_size|paginate|cursor|offset|skip|batchSize|chunk|\$in|in'
SQ='(?i:select)\s+(?:distinct\s+)?(?:\*|[\w."]+\s*(?:,|\bas\b|\bfrom\b|\()|\w+\()'   # a select list, not the English word

# 1. Unbounded reads. 1a JS/TS list calls with no cap option up to the statement's `);` (an id-set `$in` / `in:` is §7's);
#    1b SQL literals with no LIMIT (catalog tables, aggregates and `WHERE id =` lookups dropped); 1c other stacks;
#    1d DRF list views and whether a default paginator exists; 1e a cap read raw from the request; 1f a filter that can vanish.
rg -n -U --pcre2 "$C"'\K(?:\bem|\bprisma\.\w+|\b\w*(?:[Rr]epo|[Rr]epository)\b|\bmanager|\bdb\.query\.\w+|\b[A-Z][a-z]\w*)\.(?:findMany|findAll|findAndCount\w*|find|findBy)\s*(?:<[^>\n]*>)?\((?=(?:(?!\b(?:'"$LIM"')\b\s*:)[^;])*?\)\s*;)|'"$C"'\K\.(?:getMany|getManyAndCount)\(\)|'"$C"'\K\bdb\.select\([^)\n]*\)\.from\((?=(?:(?!\.limit\()[^;])*;)' -t js -t ts "${X[@]}" "${T[@]}" .
Q1B="$C"'\K([\x22\x27\x60])\s*(?!(?i:select)\s+(?:distinct\s+)?(?i:count|exists|max|min|sum|avg)\s*\()'"$SQ"'(?=(?:(?!\1|\b(?i:from)\b)[\s\S])*?\b(?i:from)\b\s+(?!(?i:information_schema|pg_\w+|sqlite_master|sys\.)))(?!(?:(?!\1|\b(?i:from)\b)[\s\S])*?\b(?i:count|exists|max|min|sum|avg)\s*\()(?!(?:(?!\1)[\s\S])*?\b(?i:limit|fetch\s+first|top\s*\(?\d)\b)(?!(?:(?!\1)[\s\S])*?\b(?i:where)\s+(?:\w+\.)?(?i:id)\s*=\s*(?:\$\d+|\?|:\w+|%s|@\w+))'   # a leading aggregate (`select count(*)`, `select exists (`) is tested before $SQ consumes it
rg -n -U --pcre2 "$Q1B" -g '!**/scripts/**' "${X[@]}" "${T[@]}" .
rg -c -U --pcre2 "$Q1B" -g '**/scripts/**' "${X[@]}" "${T[@]}" . | awk -F: '{s+=$2} END {print "1b scripts/: " s+0 " statements in " NR " files (dev tools: one read shows no production entry point imports them)"}'
rg -n --pcre2 "$C"'(?<!\w)(?:\w+\.objects\.(?:all|filter|exclude)\([^\n]*\)(?!\s*\[|[^\n]*\.(?:iterator|first|get|exists|count|aggregate|update|delete)\()|\.scalars\([^)\n]*\)\.all\(\)|\bsession\.query\([^\n]*\.all\(\)|\b[A-Z][a-z]\w*\.(?:all|where\([^\n]*\))(?![^\n]*\b(?:limit|page|find_each|in_batches|find_in_batches|first|take|count|exists\?|pluck)\b)|::all\(\)|->get\(\)|\bfindAll\(\s*\)|\bList<\w+>\s+find\w*By\w*\((?![^)\n]*Pageable)|\.Find\(&\w+\)(?![^\n]*Limit)|\.ToList(?:Async)?\(\))(?![^\n]*\b(?:'"$LIM"'|Take|Limit|paginate|cursorPaginate|chunkById|lazyById|iterator)\b)' -T js -T ts "${X[@]}" "${T[@]}" .
#    1g. Project persistence wrappers (`projectMany(em, { … })`, `queryList(…)`, `listAll(…)`): calls with no cap key anywhere in
#    their balanced argument list (PCRE recursion, so a nested `where: { … }` does not end the scan). One line per call.
CAP='take|limit|first|top|perPage|per_page|pageSize|page_size|paginate|cursor|batchSize|chunk'
rg -n -U --pcre2 "$C"'\K\b(?:project|list|fetch|load|query|select)(?:Many|All|Rows|List)\w*(?=\s*(?:<[^>\n]*>)?(\((?:(?!\b(?:'"$CAP"')\b\s*[:,}])[^()]|(?1))*+\)))' -t js -t ts "${X[@]}" "${T[@]}" .
rg -n --pcre2 'class \w+\((?:[\w.]+\.)?(?:ListAPIView|ListCreateAPIView|ModelViewSet|ReadOnlyModelViewSet|ListModelMixin)\b|DEFAULT_PAGINATION_CLASS|pagination_class\s*=\s*None' -t py "${X[@]}" "${T[@]}" .
rg -n --pcre2 "$C"'(?:\b(?:take|limit|first|perPage|pageSize|per_page|page_size)\s*[:=(]\s*(?:Number\(|parseInt\(|\+|int\(|Integer\.parseInt\()?\s*(?:req|request)\.(?:query|body|params|GET|args|form)\b|\brequest\.(?:GET|args|query_params)\.get\(\s*["\x27](?:limit|page_size|per_page|size)["\x27]|\$request->(?:input|query|get)\(\s*["\x27](?:limit|per_page|page_size|size)["\x27]|\bparams\[:(?:limit|per_page|page_size)\])(?![^\n]*\b(?:min|clamp|Math\.min|max)\b)' "${X[@]}" "${T[@]}" .
rg -n --pcre2 "$C"'\.(?:findMany|findFirst|find(?:One)?(?:By)?|count|updateMany|deleteMany|update|delete)\(\s*\{\s*(?:where:\s*\{)?\s*\w+:\s*(?:req|params|query|body|dto|input)\.\w+\s*[,}]' -t js -t ts "${X[@]}" "${T[@]}" .

# 2. OFFSET pagination: skip / offset options (and the shorthand `{ offset, limit }`), `qb.limit(n, offset)`, OFFSET in SQL,
#    offset-style paginators (the shorthand only beside a limit/take/pageSize on the line). A shared page kernel shows up
#    here once: every list through it inherits its verdict.
rg -n --pcre2 "$C"'(?:\b(?:skip|offset)\s*:\s*(?!(?:number|string|integer|boolean)\b|\{)[\w(]|\b(?:limit|take|pageSize|page)\b[^\n]{0,60}\boffset\s*[,}]|\boffset\s*[,}][^\n]{0,60}\b(?:limit|take|pageSize)\b|\.limit\(\s*[^,()\n]+,\s*\w+\s*\)|\.(?:offset|skip|Skip|Offset)\(\s*[^)\s]|(?i:\boffset\s+(?:\$\d|\?|:\w|%s|\$\{|\{))|\b(?:PageNumberPagination|LimitOffsetPagination|PageRequest\.of)\b|->paginate\(|\[\s*\w*(?:offset|start)\w*\s*:\s*\w)' -T css -T html "${X[@]}" "${T[@]}" .

# 3. Over-fetch. 3a SELECT * ; 3b rows loaded only to be counted; 3c files declaring wide columns, most first (cross them with 1a–1c).
rg -n --pcre2 "$C"'(?:(?i:\bselect\s+(?:distinct\s+)?(?:\w+\.)?\*\s+from\b)|\.select\(\s*["\x27](?:\w+\.)?\*["\x27]\s*\))' "${X[@]}" "${T[@]}" .
rg -n -U --pcre2 '(?:const|let|var)\s+(\w+)\s*=\s*await\s+[^\n]*?\.(?:find\w*|getMany|query|all)\b[^\n]*\n(?:[^\n]*\n){0,10}?[^\n]*?\K\b\1\.length\b(?![^\n]*\b\1\b(?!\.length))|\blen\(\s*(?:\w+\.)*(?:objects\.\w+|all)\([^\n]*\)\s*\)|\.(?:all|where\([^\n]*\))\.(?:length|size)\b|->get\(\)->count\(\)|\.ToList\(\)\.Count\b' "${X[@]}" "${T[@]}" .
rg -c --pcre2 "$C"'(?:\b(?:type|columnType)\s*:\s*["\x27](?:json|jsonb|text|bytea|blob|longtext|mediumtext)["\x27](?![^\n]*\blazy\s*:\s*true)|\b(?:JSONField|BinaryField|TextField)\(|^\s+\w+\s+(?:Json|Bytes)\??\s|\b(?:jsonb?|bytea|text|blob)\(\s*["\x27]\w+["\x27]|\b(?:Column|mapped_column)\(\s*(?:JSONB?|Text|LargeBinary)\b|@Lob\b|columnDefinition\s*=\s*"(?:json|jsonb|text|bytea))' "${X[@]}" "${T[@]}" . | sort -t: -k2 -nr | head -20

# 4. Predicates no plain index serves. 4a a function around a column; 4b a leading wildcard; 4c ORM spellings of both;
#    4d NOT IN (subquery); 4e context — the search indexes that already exist (migrations included on purpose).
rg -n --pcre2 "$C"'(?i:(?:\b(?:where|and|or|on|having|when|not)\s+\(?\s*|[\x22\x27\x60]\s*)\K\b(?:lower|upper|date|cast|coalesce|to_char|trim|date_trunc|extract|substr(?:ing)?|concat|unaccent)\s*\(\s*["\x60]?[a-z_][\w.]*["\x60]?\s*(?:\)|,[^)\n]*\)|\s+as\s+\w+\))\s*(?:=|<>|!=|<=?|>=?|\bi?like\b|\bin\b|\bbetween\b))' "${X[@]}" "${T[@]}" .
rg -n --pcre2 "$C"'(?:(?i:\bi?like\s+(?:["\x27]%|concat\(\s*["\x27]%|["\x27]%["\x27]\s*\|\|))|["\x27\x60]%["\x27\x60]?\s*(?:\+|\.|\|\|)|\x60%\$\{|f["\x27]%\{|"%#\{|["\x27]%["\x27]\s*\.\s*\$|"%"\s*\+)' "${X[@]}" "${T[@]}" .
rg -n --pcre2 "$C"'(?:\$re\s*:|(?<![\w$])(?:contains|endsWith)\s*:\s*\w|mode\s*:\s*["\x27]insensitive|\bI?Like\(\s*\x60%|\[Op\.(?:i?like|substring|endsWith|iRegexp|regexp)\]|__(?:i?contains|iendswith|iexact|i?regex|year|month|day|date|week_day)\b|\bwhere\(\s*["\x27](?i:lower)\(|\bfind\w*(?:Containing|Like|IgnoreCase)\w*\(|EF\.Functions\.Like\(|\.ToLower\(\)\s*==)' "${X[@]}" "${T[@]}" .
rg -n --pcre2 "$C"'(?i:\bnot\s+in\s*\(\s*select\b)' "${X[@]}" "${T[@]}" .
rg -n --pcre2 '(?i:gin_trgm_ops|gist_trgm_ops|\bpg_trgm\b|text_pattern_ops|varchar_pattern_ops|\bcitext\b|create\s+(?:unique\s+)?index[^\n]*\(\s*(?:lower|upper|unaccent)\s*\(|to_tsvector|\bFULLTEXT\b)' "${X[@]}" -g '!ai/**' -g '!docs/**' .
#    4e′. Which of those still exist: a create later dropped by name is not a control. The schema map (index-coverage-scan H0)
#    holds only live objects; without it, each 4e index name is grepped for a later `drop index`.
SM=.claude/skills/index-coverage-scan/scripts/schema-map.py; RUN=$(mktemp -d "${TMPDIR:-/tmp}/db-scan.XXXXXX")
if command -v python3 >/dev/null 2>&1 && [ -f "$SM" ] && python3 -I -B "$SM" . > "$RUN/schema.sql"; then grep -i -B1 -E 'gin_trgm_ops|gist_trgm_ops|_pattern_ops|\((lower|upper|unaccent)\(|to_tsvector' "$RUN/schema.sql" | grep -v '^--$' || echo '4e′: no search index in the live schema'; else echo "4e′ NOT-RUN (schema-map.py absent): pair each 4e name with rg -n 'drop\s+index[^;]*<name>'"; fi

# 5. A fetched result filtered / sorted / aggregated / sliced in application code (5a JS/TS, 5b other stacks).
rg -n -U --pcre2 '(?:const|let|var)\s+(\w+)\s*=\s*await\s+[^\n]*?\.(?:find\w*|getMany\w*|query\w*)\b[^\n]*\n(?:[^\n]*\n){0,10}?[^\n]*?\K\b\1\.(?:filter|sort|reduce|slice|toSorted)\(|\(await\s+[^\n]*?\.(?:find\w*|getMany\w*|query\w*)\([^\n]*\)\)\.(?:filter|sort|reduce|slice)\(' -t js -t ts "${X[@]}" "${T[@]}" .
rg -n --pcre2 "$C"'(?:\b(?:sum|max|min|sorted|len)\(\s*\[?[^\n]*\bfor\s+\w+\s+in\s+[\w.]*objects\.|\[[^\n]*\bfor\s+\w+\s+in\s+[\w.]*objects\.\w+\([^\n]*\bif\b|\.(?:all|to_a)\.(?:select|reject|sort_by|sum|group_by|max_by|min_by)\b|(?:::all\(\)|->get\(\))->(?:filter|where|sortBy\w*|sum|groupBy|slice|take|first)\(|findAll\(\)\.stream\(\)\.(?:filter|sorted|limit|skip)|\.(?:ToList|AsEnumerable)\(\)\.(?:Where|OrderBy\w*|Skip|Take|Sum|Count)\()' -T js -T ts "${X[@]}" "${T[@]}" .

# 6. A count compared with zero (6a); an exact total computed beside every page (6b).
rg -n -U --pcre2 "$C"'(?:\bcount\w*\((?:[^()]|\((?:[^()]|\([^()]*\))*\)){0,400}?\)\)?\s*(?:>\s*0|>=\s*1|!==?\s*0|===?\s*0|<\s*1)\b|\.count\b\s*(?:>\s*0|>=\s*1|==\s*0|!=\s*0)|\bif\s*\(?\s*!?\s*(?:await\s+)?[\w.]+\.count\w*\()' "${X[@]}" "${T[@]}" .
rg -n --pcre2 "$C"'(?:\b(?:findAndCount\w*|getManyAndCount|findAndCountAll|findByCursor)\(|\bEXACT_COUNT\b|\bcount\s*:\s*EXACT\w*|\bPage<\w+>|->paginate\(|\bPageNumberPagination\b|\$transaction\(\s*\[[^\]\n]*\.count\()' "${X[@]}" "${T[@]}" .

# 7. IN lists: 7a sized by the request; 7b sized by an earlier result (`.map(`); 7c every IN spelling, files ranked by count.
rg -n --pcre2 "$C"'(?:\$in\s*:|\bin\s*:|\bIn\(|\binArray\([^,]+,|\bwhereIn\([^,]+,|\[Op\.in\]\s*:|__in\s*=|\.where\(\s*\w+:)\s*(?:dto|body|input|args|params|query|request|req\.(?:body|query))\.\w+' "${X[@]}" "${T[@]}" .
rg -n --pcre2 "$C"'(?:\$in\s*:|\bin\s*:|\bIn\(|\binArray\([^,]+,|\bwhereIn\([^,]+,|\[Op\.in\]\s*:|__in\s*=)\s*(?:\[\s*\.\.\.)?[\w.]+\.(?:map|flatMap)\(' "${X[@]}" "${T[@]}" .
rg -c --pcre2 "$C"'(?:\$in\s*:\s*(?!\[)[\w.]|\bin\s*:\s*(?!\[)[\w.]+\s*[,}]|\b(?:In|inArray|whereIn|ANY)\(\s*(?!\[)[\w.]+|\[Op\.in\]\s*:\s*(?!\[)\w|(?i:\bin\s*\(\s*(?:\$\{|\?\)|:\w+\)|%s\)))|= ANY\(\s*\$\d|__in\s*=\s*(?!\[)\w)' "${X[@]}" "${T[@]}" . | sort -t: -k2 -nr | head -20

# 8. One non-unique sort key on a paged read: 8a SQL and JS option objects, 8b chained builders.
rg -n -U --pcre2 "$C"'\K(?:(?i:order\s+by\s+(?!id\b)[\w."]+(?:\s+(?:asc|desc))?(?:\s+nulls\s+(?:first|last))?)(?=\s*(?i:limit|offset|fetch)\b)|orderBy\s*:\s*\{\s*["\x27]?(?!id\b|uuid\b)\w+["\x27]?\s*:\s*[^,{}\n]+\}(?=[^;]*?\b(?:take|skip|limit|offset|first|after|cursor)\s*[:,}]))' "${X[@]}" "${T[@]}" .
rg -n --pcre2 "$C"'(?:\.order_by\(\s*["\x27]-?(?!id\b|pk\b)\w+["\x27]\s*\)|\.order\(\s*(?::(?!id\b)\w+|(?!id\b)\w+:\s*:\w+|["\x27](?!id\b)\w+(?:\s+(?:asc|desc))?["\x27])\s*\)|->(?:orderBy|orderByDesc|latest|oldest)\(\s*(?:["\x27](?!id\b)\w+["\x27](?:\s*,\s*["\x27](?:asc|desc)["\x27])?)?\s*\)|\.OrderBy(?:Descending)?\([^)\n]*\))(?=[^\n]*(?:\.limit\(|\.page\(|->(?:paginate|simplePaginate|skip|take|limit)\(|\.Skip\(|\.Take\(|\[\s*\w*\s*:))' -T js -T ts "${X[@]}" "${T[@]}" .
```

A finding is a grep hit **plus** a read of the statement and its caller **plus** the table's growth class **plus** the hops to an entry point. Three blind spots are structural:

- **The statement is assembled elsewhere.** A base repository, a list-projection helper or a query-builder chain spread over many lines sets (or forgets) the cap. Grep 1a reads only to the first `);`; grep 1g lists every call of a project wrapper (`projectMany`, `queryList`, `listAll`, …) whose balanced argument list names no cap key. Read the helper once (does it apply a default cap?), then judge every call through it as one group.
- **The cap is upstream.** A DTO `@Max(100)`, a zod `.max()`, a global paginator or an interceptor may clamp a value the query receives unchecked. A hit is cleared only when the clamp is read and reaches **this** path.
- **Strings in other files.** SQL in `.sql` files, stored procedures, views and ORM `@Formula` / `@Query` annotations: grep 1b reads every quoted literal, but a view's definition lives in a migration. Read the view when a query selects from one.

**Measured** (2026-10-15) on a real NestJS + React monorepo (MikroORM 6.6, Postgres 16, FORCE RLS), before → after: 1b 117 → 11 (the aggregate test now runs before `$SQ` consumes `select count(` / `select exists (`, and 75 statements in `scripts/` print as one count line); new 1g 249 wrapper calls with no cap key (204 `projectMany(…)`; a bracket-matching script over the same tree counted 209); grep 2 5 → 17 (both OFFSET kernels now show: the shared `{ page, pageSize, offset, limit }` resolver and `qb.limit(n, offset)`; a CSS `outline-offset` dropped with `-T css`); 4a 59 → 50, 2 of them outside `scripts/` (both real; JS `lower(x) ===` and `new Date(a) > new Date(b)` dropped by the SQL-context prefix); 4e′ shows the four trigram indexes 4e lists were dropped by a later migration (the measured `~~*`-under-RLS decision, § 41); 6a 9 → 28 (`(await this.em.count(…)) > 0` spread over lines, 14 sites; 7 lines are a web `c.count > 0` property); 6b 0 → 13 (`EXACT_COUNT` on every list page). On the fixtures, only aggregates (`select count(*)`, `select max(…)`), CSS offsets and JS `lower()` calls left the output; every seeded line stays.

Earlier measurement (2026-10-02). On the same monorepo at about 13,000 tracked files, the script runs in about 4 s: grep 1, 113 lines (1a 48; 1b 64, of which 60 are in `scripts/` dev tools; 1f 1, a port `update` keyed by an input field); grep 2, 2; grep 3, 52 (3a 14, 3b 18, 3c the top 20 files); grep 4, 153 (4b 75: mostly `$ilike` with a leading `%` in search filters, crossed against 4e's trigram indexes in the migrations); grep 5, 6; grep 6, 17; grep 7, 82 (7a 8, 7b 54, 7c the top 20 files); grep 8, 36 (20 in `scripts/`). On `benchmarks/fixtures/node-api`, grep 1b returns 7 statements, including the seeded unbounded read, and grep 3a returns its `SELECT *`. On `half-built-crm`, grep 1b returns exactly four statements: the filtered and unfiltered branches of the two unpaginated list endpoints (`contacts.py`, `tasks.py`) behind its pagination defect. On `vuln-fullstack`, grep 4b finds the `ILIKE '%…%'` product search.

## The 3,000-hit path

1. **Intersect and dismiss.** Keep hits in backend code. Dismiss a whole directory (`scripts/`, a probe or tooling folder, a frontend app) with **one** read showing no production entry point imports it, and name it in the coverage block.
2. **Group by (helper or function, table).** One decision covers a group with the same table, predicate shape and caller.
3. **Rank by growth class × reachability.** Append-only and per-tenant tables reached from list, search, export and report endpoints come first; bounded lookups come last and usually go straight to Hardening.
4. **Read the top 30 groups fully.**
5. **Prefer workload evidence at scale.** `pg_stat_statements` ordered by `rows / calls` (the Neon method: rows per call exposes unbounded reads and over-fetch that code reading misses), or the e2e suite run with the query logger, flagging every statement that returns more rows than its page size. Statements found this way are anchored back to their `<file:line>`.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes a production entry point and a growing table. A bounded-lookup table is Hardening. Raise to **critical** only on production evidence (an incident, an APM trace of a timeout or OOM) or when §1's vanishing filter returns another tenant's rows.

| § | Class | CWE | Default |
|---|---|---|---|
| 1 | Unbounded result on a growing table (no cap, a client-chosen cap, a filter that can vanish) | CWE-770 | high on a user-reachable list / export, else medium |
| 2 | Deep OFFSET pagination on a large table | CWE-400 | medium; high on a public, crawlable list |
| 3 | Over-fetch: `SELECT *`, wide columns hydrated for a few fields, rows loaded to be counted | — | medium |
| 4 | Predicate no plain index can serve (function on the column, leading wildcard, implicit cast, `OR` across columns, `NOT IN (subquery)`) | CWE-1067 | high on a hot search path over a large table, else medium |
| 5 | Filter / sort / aggregate / page in application code after a fetch | CWE-770 when it pages in memory | medium; high when the fetch is unbounded |
| 6 | Count used as an existence test; an exact `COUNT(*)` on every page | — | low; medium on a large table on every list request |
| 7 | IN list sized by the request or by an earlier result, with no cap or chunking | CWE-770 | medium; high when request-sized and unauthenticated |
| 8 | One non-unique sort key on a paged read (no tiebreaker) | — | medium (duplicates and gaps across pages) |

### 1. Unbounded result on a growing table

```
BAD:   return this.em.find(Order, { seller });                              // the biggest seller's 400k rows
       Order.objects.filter(seller=s)  ·  ListAPIView with no pagination_class and no DEFAULT_PAGINATION_CLASS
       take: Number(req.query.limit)                                        // ?limit=1000000 is honoured
       prisma.order.findMany({ where: { sellerId: dto.sellerId } })         // sellerId undefined → every order
GOOD:  this.em.find(Order, { seller, id: { $lt: cursor } }, { limit: Math.min(dto.limit ?? 20, 100), orderBy: { id: 'desc' } })
       a jobs path streams instead: .iterator(chunk_size=…) · find_each · chunkById · findByCursor
```
**Read the code:** What is the table's growth class? Is the predicate a unique key (then one row), a parent key with a business cap, or only a tenant or owner on a growing table? Where is the cap: in this call, a base repository, a paginator default, a DTO maximum? Is the cap clamped server-side, or does `?limit=1e9` pass? Can a filter value be `undefined`? Prisma treats an `undefined` key as absent (docs, *null and undefined*); TypeORM 0.3 does the same and 1.x throws by default. The export, admin, background-job and GraphQL `first:` paths count. **Finding when** a growing table is read with no effective server-side cap from a production path. **Proof:** seed cap + 1 rows (or 10 × the page size), call the entry point with no limit, `limit=0`, `-1`, `1e9` and `abc`, and assert the response length ≤ cap **and** that the captured SQL carries `LIMIT`. It fails first.

### 2. Deep OFFSET pagination

```
BAD:   LIMIT 20 OFFSET ${(page - 1) * 20}  ·  skip: (page - 1) * size  ·  ->paginate()  ·  PageNumberPagination
GOOD:  WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT 20   // keyset
       findByCursor · cursor: { id }, skip: 1 · cursorPaginate() · CursorPagination
```
Postgres's own docs: "the rows skipped by an `OFFSET` clause still have to be computed inside the server; therefore a large `OFFSET` might be inefficient" (PostgreSQL 18, *LIMIT and OFFSET*). **Read the code:** Is the table large, and is the page number unbounded (crawlers walk to page 10,000)? Is jump-to-page a real requirement (an admin grid with a capped depth), or only next / previous? **Finding when** an unbounded page number reaches OFFSET on a growing table. **Proof:** `EXPLAIN (ANALYZE, BUFFERS)` of page 1 and page 1,000 on production-shaped, `ANALYZE`d data: buffers and rows read grow with the offset before the fix and stay flat after.

### 3. Over-fetch

```
BAD:   SELECT * FROM products WHERE …                     // description_html, specs jsonb, image blob — for a dropdown
       const users = await repo.find({ where }); return users.length;     // N rows to produce one number
GOOD:  em.find(Product, where, { fields: ['id', 'name'] }) · .only('id', 'name') · @Property({ lazy: true }) on the blob
       em.count(User, where) · SELECT count(*)
```
**Read the code:** Which columns does the consumer use? Is a wide column (`jsonb`, `text`, `bytea`; grep 3c) hydrated on a list path? Is the list returned or only counted? Is a wide parent repeated on every child row of a join (Neon's "JOIN duplication": select the child, then fetch the parents once)? **Finding when** a list path ships or hydrates columns the consumer never reads, and they are wide, or the rows are fetched only to be counted. **Proof:** response bytes and rows (or `pg_stat_statements` rows and blocks per call) before and after, on the same seeded data, plus `EXPLAIN (VERBOSE)` output columns. A count fix asserts the captured SQL is a `count`.

### 4. Predicate no plain index can serve

```
BAD:   WHERE lower(email) = $1                              // no index on lower(email)
       name ILIKE '%' || $1 || '%' · { name: { $ilike: `%${q}%` } } · contains: q, mode: 'insensitive'
       WHERE created_at::date = $1 · WHERE a = $1 OR b = $1 · WHERE id NOT IN (SELECT …)
GOOD:  CREATE INDEX … ON users (lower(email))  or a citext / case-insensitive collation
       CREATE INDEX … USING gin (name gin_trgm_ops)          // pg_trgm serves LIKE / ILIKE '%q%'
       WHERE created_at >= $1 AND created_at < $1 + 1 day   · UNION of two indexed lookups · NOT EXISTS
```
**Row-level security changes the answer** (`precedents/data.md` § 41): for a role the policies apply to, a predicate whose operator is not leakproof — `~~*` (`ILIKE`) among them — is evaluated after the policy quals, so it is never an index condition and a trigram index cannot serve it. Before proposing a trigram index on an RLS table, `EXPLAIN` as the application role (`SET ROLE`), never as a superuser or the table owner. 4e′ lists the search indexes that still exist; a 4e create dropped by a later migration is not a control. A trigram index serves infix `LIKE` / `ILIKE`, but "a pattern with no extractable trigrams will degenerate to a full-index scan" (PostgreSQL 18, *pg_trgm*), so patterns shorter than three characters need a minimum length. A prefix `LIKE 'q%'` uses a B-tree only in the C locale or with `text_pattern_ops` (PostgreSQL 18, *Operator Classes*). `NOT IN (subquery)` also returns **no rows** when the subquery yields a NULL, which is a correctness bug as well as a plan problem. **Read the code:** Is there an expression, trigram or full-text index for this exact predicate (grep 4e, plus the live catalog when reachable)? Does the parameter type match the column (a `uuid` column compared with `text`; a MySQL `VARCHAR` compared with a number casts every row)? Is the table large and the search hot? **Finding when** the predicate cannot use an index as written on a large table on a hot path. **Proof:** `EXPLAIN (ANALYZE, BUFFERS)` on production-shaped data with a ≥ 3-character term: `Seq Scan` with a large `Rows Removed by Filter` before, an index or bitmap index scan after. Also run the generic-plan variant (`SET plan_cache_mode = force_generic_plan`), since prepared statements switch plans. The index itself ships through `index-coverage-scan` → `/add-migration`.

### 5. Filter, sort, aggregate or page in application code

```
BAD:   const orders = await repo.find({ where: { seller } }); return orders.filter(o => o.status === s).slice(0, 20);
       sum(o.total for o in Order.objects.filter(seller=s))  ·  Order::all()->where('status', $s)->take(20)
GOOD:  repo.find({ where: { seller, status: s }, take: 20, order: … }) · .aggregate(Sum('total')) · ->where(…)->limit(20)->get()
```
**Read the code:** Could the database apply this predicate, order, sum or slice? Is there a reason it cannot (a computed field, a cross-store join)? If so, is the fetch at least bounded? A Hibernate collection `JOIN FETCH` with `setMaxResults` pages **in memory** and warns `HHH90003004`; `hibernate.query.fail_on_pagination_over_collection_fetch=true` makes it throw. **Finding when** rows are fetched to be discarded, sorted or summed on a growing table. **Proof:** the captured SQL carries the predicate / `ORDER BY` / `LIMIT` / aggregate after the fix, and the rows fetched fall from "all matching" to the rows returned.

### 6. Count used as existence; an exact count on every page

```
BAD:   if (await em.count(Order, { customer }) > 0) …       ·   Order.objects.filter(…).count() > 0
       findAndCount / Page<T> / ->paginate() on a 50M-row table, for a "page 1 of 2,481,903" nobody reads
GOOD:  em.findOne(Order, { customer }, { fields: ['id'] }) · .exists() · exists? · ->exists() · AnyAsync()
       Slice<T> · simplePaginate() · findByCursor(…, { includeCount: false }) · an estimate (reltuples) for the UI
```
**Read the code:** Is the count only compared with zero? Is the total shown, and does it need to be exact? MikroORM's `findByCursor` runs a count unless `includeCount: false` (6.6.16 types). **Finding when** a count scans a large set to answer yes or no, or an exact total is computed on every page of a large table. **Proof:** the captured SQL is `EXISTS` / `LIMIT 1` after the fix; `EXPLAIN (ANALYZE)` of the count before shows the scan.

### 7. IN lists with no cap or chunking

```
BAD:   em.find(Order, { id: { $in: dto.ids } })                // dto.ids has no @ArrayMaxSize
       knex('orders').whereIn('customer_id', allCustomers.map(c => c.id))
GOOD:  @ArrayMaxSize(500) on the DTO · chunk(ids, 1000) → one query per chunk · = ANY($1::uuid[]) with one array parameter
```
Each value is usually one bind parameter, and Postgres's Bind message carries the parameter count in an `Int16` field (PostgreSQL 18 protocol, *Bind*), so a list in the tens of thousands fails at the driver before the planner sees it. Large lists also bloat plans and plan caches. **Read the code:** Where does the list come from: the request (is it capped?), or an earlier query (is **that** bounded)? Does the driver expand `$in` into one parameter per value? **Finding when** the list is request-sized with no cap, or derived from an unbounded read, and sent unchunked. **Proof:** call with a list larger than the chunk (and one past the parameter limit) and assert it succeeds with ⌈n / chunk⌉ statements, or one array parameter.

### 8. One non-unique sort key on a paged read

```
BAD:   orderBy: { createdAt: 'desc' }, take: 20, skip      ·   ORDER BY created_at DESC LIMIT 20 OFFSET $1
GOOD:  orderBy: [{ createdAt: 'desc' }, { id: 'desc' }]   ·   ORDER BY created_at DESC, id DESC
```
"When using `LIMIT`, it is important to use an `ORDER BY` clause that constrains the result rows into a unique order. Otherwise you will get an unpredictable subset of the query's rows" (PostgreSQL 18, *LIMIT and OFFSET*). **Read the code:** Is the sort key unique (an id, a unique slug)? Can two rows share it (bulk inserts share a timestamp)? Does the keyset cursor include the tiebreaker? **Finding when** a paged read orders only by a non-unique key. **Proof:** seed rows with identical sort keys across a page boundary, walk every page (inserting rows concurrently on the second walk), and assert the union of pages equals the row set, with no duplicates and no gaps.

## Proof oracles

Each class's failing-first shape is in [`proof-oracles.md`](../../../../snippets/proof-oracles.md): *Plan shape* (with its `hypopg` and generic-plan notes) for §2, §4 and §6, the seeded-cap V3 for §1 and §7, and the walk-every-page V4 for §8; §3 and §5 assert on the SQL captured by the counter in *Counting queries per stack*. Plans count only on **production-shaped, `ANALYZE`d data**: a 100-row dev table proves nothing either way, and `SET enable_seqscan = off` proves only that an index *can* be used. `EXPLAIN ANALYZE` **executes** the statement, so wrap anything that writes in `BEGIN; … ROLLBACK;`, and never run probes against the production primary without the user's explicit go.

**Whole-class variants** a fix must survive: no `limit` / `0` / `-1` / `1e9` / `abc`; the export, CSV, admin, background-job and GraphQL `first:` paths; a nested collection inside one item (an order with 10,000 lines); an empty search term that matches everything; every filter combination and sort column the endpoint accepts; the first page and a deep page; a common value and a rare one (the largest tenant and the smallest); an `IN` list of 1 and of thousands; ties in the sort key, NULLs in it, descending order.

## Output

```
query-shape-scan — lanes: mikro-orm 6.6 (package.json), postgres 16 (docker-compose.yml); django, rails, laravel, jpa absent
Context: 41 tables classified (17 growing, 24 lookup) · caps: list-projection helper (limit ≤ 100), no DTO max on 3 list DTOs

Findings: 2 · Unconfirmed: 1

1. src/products/products.port.ts:212                             [report-with-fix]   high
   §4 leading wildcard — `{ name: { $ilike: `%${q}%` } }` on products (growing, ~2.1M rows in the restored copy);
   no gin_trgm_ops index on products.name (grep 4e lists orders.code only). Reached by GET /products?q= (typeahead).
   Proof: EXPLAIN (ANALYZE, BUFFERS) 'lamp' → Seq Scan, Rows Removed by Filter 2,104,331, 41,882 buffers (measured).
   Fix: CREATE INDEX CONCURRENTLY … USING gin (name gin_trgm_ops) via /add-migration; min query length 3. CWE-1067

2. src/orders/orders.controller.ts:58                            [report-with-fix]   high
   §1 client-chosen cap — `limit: Number(req.query.limit)` passed to em.find; ?limit=1000000 honoured.
   Proof: test/orders/orders.limit.e2e-spec.ts — 120 seeded rows, ?limit=1e9 returns 120 (cap 100), fails.
   Fix: Math.min(Math.max(limit, 1), 100) in ListOrdersQuery, plus @Max(100) on the DTO. CWE-770

3. src/reports/exports.service.ts:77                             [report-flagged]    high
   §1 unbounded — em.find(Payment, { merchant }) feeding the CSV export; payments grow per merchant.
   Unproven link: no copy with production volume. Settling probe: seed 50k payments for one merchant, run the export,
   assert a streamed cursor (findByCursor / chunked) and flat memory. Fix: stream in 1,000-row keyset pages.

Verification: 23 candidates → 2 findings · 1 unconfirmed · 12 hardening · 0 pre-existing · 8 refuted

Class coverage:
  §1  unbounded result              checked (113 hits / 40 groups → 1 finding, 1 unconfirmed; scripts/ dismissed with one read)
  §2  deep OFFSET                   checked (2 hits → 0 findings: admin grid capped at page 50)
  §3  over-fetch                    checked (32 hits → 0 findings)
  §4  non-sargable predicate        checked (153 hits / 19 groups → 1 finding; 11 searches covered by trigram indexes)
  §5  in-app filter / page          checked (6 hits → 0 findings)
  §6  count as existence            checked (17 hits → 0 findings; 2 Hardening on small tables)
  §7  IN lists                      checked (52 hits / 18 groups → 0 findings) · Live, unreviewed (12 groups / 30 hits — continue with grep 7b)
  §8  unstable page order           checked (36 hits → 0 findings; 16 non-script hits order by unique keys)
```

`[report-with-fix]`: the statement, its growth class and its entry point are cited, the oracle fired, and the fix is local. `[report-flagged]`: one link is unproven (no production-shaped data, the cap's helper not read, a growth class assumed), and the row names it and the settling probe. Numbers carry their label, **measured** or **estimated**; a number no tool produced is deleted. The coverage block lists **all eight** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the repo has no such surface; `blocked (<reason>)` when a grep failed or code could not be read; `Live, unreviewed` for groups left after triage.

## False positives / precedents

The verifier reads [`precedents/performance.md`](../../../../snippets/precedents/performance.md) (cost classes: precedents 4, 7, 13 and 20–22 decide most of this skill's candidates; 38 and 39 settle public and admin lists) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **Unbounded is about growth, not syntax.** A lookup, enum or configuration table whose size is fixed by the domain is Hardening; per-tenant reference data that grows with the tenant is not.
- **A job that streams or chunks** (`iterator`, `find_each`, `chunkById`, `lazyById`, `findByCursor`, `FindInBatches`, `yield_per`) is the correct shape for "every row". The same read buffered into memory, or returned from a request, is the finding.
- **A batch job ordered by a non-unique key that deletes or marks the rows it reads** re-queries every batch, so ties cannot skip rows. It is not a paging defect.
- **A Seq Scan on a small table, or for a low-selectivity predicate, is the right plan**, and a plan from a dev database is not proof either way.
- **A trigram index present covers a leading-wildcard search** for patterns of three or more characters. Shorter patterns need a minimum-length rule, not a new index.
- **A count on a small or bounded set**, or a total the product needs and the table can afford, is Hardening.
- **An IN list capped by validation** (`@ArrayMaxSize`, a max-length schema) or by a bounded upstream read is fine.

## When to run

- On any diff that adds or changes a list, search, export, report or admin endpoint, a repository or query-builder method, a DTO with paging fields, a GraphQL connection, or raw SQL: the `/db-audit` dispatch signal.
- On every whole-repo `/db-audit`, reporting all eight classes. `/perf-audit` dispatches it when the database pack is installed; without it, the performance pack's ledger lists these rows as `N/A (owner pack database not installed)`.
- When `pg_stat_statements` shows a statement with high `rows / calls`, a growing `total_exec_time`, or temp blocks on an OLTP path.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/db-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the statement `<file:line>`, the table's growth class, the entry point, and the fix in the project's ORM.
- Halt on a finding that names a table, column or index that exists in no migration, schema file or live catalog. It is fabricated: Refute it.
- Do not mark a cost finding `[report-with-fix]` without its oracle having fired on production-shaped data or a seeded-cap test. Otherwise it is `[report-flagged]` / Unconfirmed, with the probe written out.
- Do not propose a cache, a bigger instance or a longer timeout as the fix. The fix changes the statement's shape (cap, keyset, projection, sargable predicate, `EXISTS`, chunking, tiebreaker) or adds the index the predicate needs.
- Do not change a public endpoint's pagination or cap silently. A new cap or a switch from OFFSET to keyset is a contract change for `/db-fix` to STOP and ask about.
- Do not print "no query-shape issues" without the class-coverage block. A class whose grep did not run is `blocked`, never `checked`.

## Related

- `/db-audit` dispatches this skill and folds its coverage block into the class ledger. `/db-fix` closes the findings with a failing-first oracle, the root-cause rewrite, a re-run of this detector on the patched line, and the sibling search.
- `n-plus-one-scan` (this pack) owns per-element queries and the shared ORM lane table. `index-coverage-scan` (this pack) owns the index a fixed predicate needs; `@query-optimizer` and `/optimize-query` judge the plan; `/add-migration` ships the index.
- `full-text-search.md` (this pack's pattern) is the design when infix search outgrows trigram indexes.
- Backend's `pagination.md` (when the backend pack is installed) owns the pagination contract and the envelope. `request-path-scan` § 6 (performance pack, when installed) owns buffering a large result into a response.
- `@tenant-isolation-reviewer` (security pack, when installed) owns the cross-tenant consequence of a filter that can vanish.
- `rules/database-principles.md` and `rules/performance-principles.md` (when installed) hold the MUSTs for paginated lists and bounded results that this skill enforces.
