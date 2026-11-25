---
name: complexity-scan
description: Find super-linear work on data-sized input, uncapped recursion, cycles and stalled loops; caps resolved, counted proof.
kind: skill
pack: algorithms
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: complexity-scan

## Premise

A complexity defect is a procedure whose work, depth or iteration count grows faster than the budget
as a collection the users or the data control grows: a lookup that scans a list per element, an
accumulator copied per step, a front-removal that shifts the array, a sort or a `Set` rebuilt every
iteration, two collections joined by nested loops, a product generated before the cap is applied, a
recursion as deep as the input, a walk that never meets a visited set, an exponential self-call, a
loop whose cursor can stall. CWE files them under **CWE-407** (inefficient algorithmic complexity),
**CWE-1050/1046/1176** (resource-consuming loop shapes), **CWE-674** (uncontrolled recursion) and
**CWE-835** (a loop with an unreachable exit). Every function is fast on the three rows in the test
fixture; the cost appears when a tenant has 50,000.

**Every finding cites the site `<file:line>` + its class + the cap on each collection (or its absence,
with where the size comes from) + `n_max × m_max` against the budget + the entry point that reaches it
+ the proof + the fix.** A grep hit is never a finding, and "no complexity defect" is never printed
without the class-coverage block (§ Output).

**Resolve caps before reading, count operations to prove.** On a real NestJS + React monorepo the
naive greps returned 97 linear-lookup hits, 264 nested loops, 31 sorts in callbacks and 179
self-calls, and every one was refuted by the same reads: what bounds each collection, and whether the
recursion carries a depth or cycle guard. `scripts/algo-sites.py` does those reads first and prints
the arithmetic, so a reader opens the short list. The proof is an **operation count** at N and 4N
([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Algorithms, V590–V598), never a
model-asserted complexity class, and never a single wall-clock run.

## The rule

A site is a finding when all four hold:

1. **A production path runs it.** A route, resolver, consumer, scheduled job, or a page rendered on a
   real route. Scripts, seeds, CLIs, benchmarks and test helpers fail here.
2. **The size, depth or cycle comes from users or data.** Cite the cap on each collection — a schema
   `.max(N)`, a `limit:`/`take:`, `Math.min(…, N)`, `.slice(0, N)`, a constant, a body limit — or
   its absence at every entry point. A side capped at ≤ 50 makes the work linear in the other.
3. **No control on the path stops it.** An index built once, a memo, a depth cap and a visited set,
   a unique cursor with strict `>`, a short-page exit, a cap enforced before generation.
4. **The oracle fires failing-first** (V590–V598), or, for a cap that is absent, the two-ended static
   fact (the collection's source and every entry point with no bound) is cited. Without either the
   row is Unconfirmed with the test written out.

**Severity.** **High** when a server path's work or depth is set by an unauthenticated or
tenant-sized input past the budget, or a recursion or loop can crash or hang a shared worker;
**medium** for job and worker paths and authenticated request paths with a cap above the budget;
**low** for one browser tab or an admin-only path. Drop one step when a cap exists but sits above the
budget. The budget is the pack rule's: `n ≤ 5e3 → O(n²)`, `n·m ≤ ~1e6` operations per request.

## Boundaries

Per-call construction (a regex, validator or client built per call) is performance
`request-path-scan` §8; memory held across requests is `memory-growth-scan` (an unbounded
process-lifetime set §1, a per-request clone of a large constant §8); a query per element (N+1) is
database `n-plus-one-scan`; ReDoS is security `injection-scan` §13; a loop bound taken from untrusted
input with no limit (CWE-606) is security's input validation. This skill owns the growth class of a
procedure on data-sized input, its recursion depth and cycles, and whether its loops terminate.
**Without this pack, `request-path-scan` §11 grades CX-1…CX-5** (performance pack); with it installed
§11 prints `→ complexity-scan` and does not grade. GraphQL query depth is `@api-security-reviewer`'s;
body-size limits are `request-path-scan` §13 (this skill reads them as the RC-1 bound). Retry loops
with no cap are distributed-systems `retry-deadline-scan`. A comparator, parse or date expression
wrong for one input is code-quality `correctness-smell-scan`. Each cross-pack route applies when that
pack is installed; without it the row is listed here, tagged `<class> (owner pack <x> not installed)`,
and never graded as the owner would grade it.

## Adapt to the codebase — lanes

Read every analyzer's version from the lockfile or manifest (grep 0a); a lane whose binary is not in
the project (its `node_modules/.bin`, its virtualenv, its build) is `NOT-RUN (<reason>)`, never PASS
and never installed from the network. No linter in any stack flags a linear lookup inside a loop:
§1 is the script plus a read in every lane.

| Lane | Shape-exact analyzer rules (version from the lockfile) | Parsed by `algo-sites.py` | Fix primitive |
|---|---|---|---|
| **TS / JS** | Biome `lint/performance/noAccumulatingSpread` (reduce only; misses `acc.concat` and loops); oxlint `oxc/no-accumulating-spread` (reduce and loops); unicorn `prefer-set-has` is style (constant arrays) — never a CX finding | yes (masking scanner; `.vue`/`.svelte` script blocks) | `Set`/`Map` index, `push` + one copy, a head index or deque, hoist, `Map` group-by |
| **Python** | Ruff `RUF017` (`sum(lists, [])`); `PERF*` rules are constant-factor — never report them as CX | yes (`ast`) | `set`/`dict`, `list.extend`, `collections.deque`, hoist, `itertools.chain` |
| **Go** | staticcheck `SA6000` (`regexp.Match*` in a loop; issue #1502 false positive on a switch in a map range) | counted, greps 1a, 3–5, 9a, 10 | `map[K]struct{}`, `strings.Builder`, a ring buffer, compile once |
| **JVM** (Java, Kotlin) | SpotBugs `SBSC_USE_STRINGBUFFER_CONCATENATION`, `IIL_PATTERN_COMPILE_IN_LOOP[_INDIRECT]` (bytecode); PMD `UseStringBufferForStringAppends` (`AvoidInstantiatingObjectsInLoops` is noise); CodeQL `java/unreachable-exit-in-loop`, `java/constant-loop-condition` (optional, GHAS) | counted, greps 1b, 2c, 2e, 3–5, 9b, 10 | `HashSet`/`HashMap`, `StringBuilder`, `ArrayDeque`, a static `Pattern` |
| **.NET** | — (`DOTNET_CLI_TELEMETRY_OPTOUT=1` for any `dotnet` call) | counted, greps 1c, 2c, 3–5, 9b, 10 | `HashSet<T>`, `StringBuilder`, `Queue<T>`, `ToDictionary` once |
| **Ruby** | RuboCop Performance `CollectionLiteralInLoop`, `ConstantRegexp` (no cop for `include?` in a loop) | counted, greps 1d, 1e, 2d, 3, 9c, 10 | `Set`, `<<`, `index_by` once |
| **PHP** | — | counted, greps 1f, 3, 5, 9c, 10 | `isset($map[$k])` with `array_flip` once, `SplQueue` |
| **Rust** | Clippy `regex_creation_in_loops`, `manual_contains` (group UNVERIFIED) | counted, greps 1g, 4, 5, 10 | `HashSet`, `VecDeque`, a `LazyLock` regex |
| **SQL** | — | greps 7a, 7b, 7c, 8 | `CYCLE … SET` (PostgreSQL ≥ 14), a path array, a depth column, a unique key with strict `>` |

## Pre-flight

Run as **one** bash script from the repo root. Set `ROOTS` to the production source roots first
(`scripts/`, `test/`, seeds and CLIs are not roots unless the caller says so). Grep **N** feeds
detector **§N**; grep 0 is context. Every `rg` names its path; every exit code is printed, and an
exit 2 (a pattern or path error) makes the step fail rather than read as zero hits. Output goes to a
`mktemp -d` folder; nothing is written in the repo and nothing touches the network.

```bash
set -u
declare -p ROOTS >/dev/null 2>&1 || ROOTS=(.)   # production source roots, e.g. ROOTS=(apps/api/src apps/web/src)
S="${ALGO_SITES:-.claude/skills/complexity-scan/scripts/algo-sites.py}"
OUT="$(mktemp -d "${TMPDIR:-/tmp}/complexity-scan.XXXXXX")"; RC=0
st() { printf '# %-3s rc=%s\n' "$1" "$2"; [ "$2" != 2 ] || RC=2; }   # rg: 0 hits, 1 none, 2 FAILED (never "zero hits")
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**'
   -g '!**/.venv/**' -g '!**/coverage/**' -g '!**/*.min.*' -g '!**/*.d.ts' -g '!**/*.{md,mdx,lock,map,svg,json,snap,yml,yaml,css,scss,html}')
T=(-g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,seeds,seeders,migrations,locales,i18n,generated,__generated__,docs}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,fuzz-spec,test-data,fixture,bench}.*' -g '!**/{*_test,*_spec,test_*,conftest}.*' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')
for t in js ts py go java kotlin cs ruby php rust; do printf '%-7s %s\n' "$t" "$(rg --files -t "$t" "${X[@]}" "${T[@]}" "${ROOTS[@]}" | wc -l)"; done

# 0. Context: 0a analyzer pins (lane versions), 0b body-size / parser-depth / stack settings (the RC-1 bound).
rg -n --no-heading --pcre2 '"(?:@biomejs/biome|oxlint|eslint-plugin-unicorn|eslint)"\s*:\s*"[^"]+"|^\s*(?:ruff|staticcheck)\b[^\n]*\d|honnef\.co/go/tools\s+v|<artifactId>(?:spotbugs|pmd)[\w-]*</artifactId>|\brubocop-performance\b|com\.github\.spotbugs|\bpmd\b[^\n]*version' -g 'package.json' -g 'pyproject.toml' -g 'requirements*.txt' -g 'go.mod' -g 'pom.xml' -g 'build.gradle*' -g 'Gemfile' -g '!**/node_modules/**' .; st 0a $?
rg -n --no-heading --pcre2 '\bbodyLimit\s*:|\b(?:express|bodyParser)\.(?:json|urlencoded)\(\s*\{[^}\n]*\blimit\b|\bclient_max_body_size\b|\bDATA_UPLOAD_MAX_MEMORY_SIZE\b|\bsys\.setrecursionlimit\(|-Xss\d|--stack-size\b|\b(?:maxDepth|max_depth|depthLimit)\s*[:=]' "${X[@]}" "${T[@]}" . | "${NC[@]}"; st 0b "${PIPESTATUS[0]}"

# 1. CX-1 / CX-5 on the stacks algo-sites.py counts but does not parse: a lookup within 6 lines of a loop head.
#    1a Go, 1b JVM, 1c .NET, 1d Ruby block (multi-line) and 1e one-line, 1f PHP, 1g Rust, 1h lodash *With helpers (JS).
rg -n -U --pcre2 '^[ \t]*+for\b[^\n]*\{[ \t]*\n(?:[^\n]*\n){0,6}?[^\n]*?\K\bslices\.(?:Contains|ContainsFunc|Index|IndexFunc)\(' -t go "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 1a "${PIPESTATUS[0]}"
rg -n -U --pcre2 '^[ \t]*+(?:for\s*\([^\n]*[:)]|[\w.]+\.forEach\s*[({]|while\s*\()[^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*?\K(?:\b(?!this\b)[\w.]+\.(?:contains|indexOf|lastIndexOf)\(|\.stream\(\)\.(?:anyMatch|noneMatch|filter)\()' -t java -t kotlin "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 1b "${PIPESTATUS[0]}"
rg -n -U --pcre2 '^[ \t]*+(?:foreach|for)\s*\([^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*?\K\b[\w.]+\.(?:Contains|IndexOf|Any|First|FirstOrDefault|Where)\(' -t cs "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 1c "${PIPESTATUS[0]}"
rg -n -U --pcre2 '^[ \t]*+[^\n]*\.(?:each|each_with_index|each_with_object|map|flat_map|select|reject|filter_map|sum|count)\b[^\n]*\|[^|\n]+\|[ \t]*\n(?:[^\n]*\n){0,6}?[^\n]*?\K\b[\w.@]+\.(?:include\?|index|find|detect|any\?)' -t ruby "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 1d "${PIPESTATUS[0]}"
rg -n --pcre2 '\.(?:each|map|select|reject|count|any\?|all\?|find|detect)\s*\{\s*\|\w+\|[^\n}]*\b[\w.@]+\.(?:include\?|index|find|detect)\b' -t ruby "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 1e "${PIPESTATUS[0]}"
rg -n -U --pcre2 '^[ \t]*+foreach\s*\([^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*?\K\b(?:in_array|array_search)\(|\barray_(?:filter|map)\([^\n]*\bin_array\(' -t php "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 1f "${PIPESTATUS[0]}"
rg -n -U --pcre2 '^[ \t]*+for\s+\w+\s+in\b[^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*?\K\.(?:contains|iter\(\)\.(?:any|position|find))\(' -t rust "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 1g "${PIPESTATUS[0]}"
rg -n --pcre2 '\b_\.(?:differenceWith|intersectionWith|uniqWith|unionWith|xorWith|pullAllWith)\(|\bfrom\s+["\x27]lodash/(?:differenceWith|intersectionWith|uniqWith)["\x27]' -t js -t ts "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 1h "${PIPESTATUS[0]}"

# 2. CX-2 copy-per-iteration: 2a JS reduce spread/concat (cross-checks the script), 2b Python sum(…, []) / reduce(add),
#    2c string append in loops (JVM, .NET, Go), 2d Ruby inject with acc + [x] / non-bang merge, 2e Kotlin fold with +.
rg -n --pcre2 '\.reduce(?:Right)?\(\s*(?:async\s*)?\(\s*(\w+)\b[^)\n]*\)\s*(?::[^=\n]+)?=>[^\n]*?(?:\{\s*\.\.\.\1\b|\[\s*\.\.\.\1\b|(?<![\w$.])\1\s*\.\s*concat\(|Object\.assign\(\s*\{\s*\}\s*,\s*\1\b)' -t js -t ts "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 2a "${PIPESTATUS[0]}"
rg -n --pcre2 '\bsum\([^\n]*,\s*(?:start\s*=\s*)?\[\]\s*\)|\breduce\(\s*(?:operator\.)?(?:add|concat|iadd)\b' -t py "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 2b "${PIPESTATUS[0]}"
rg -n -U --pcre2 '^[ \t]*+(?:for|foreach|while)\b[^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*?\K(?:\b(\w+)\s*=\s*\1\s*\+\s*(?:"|\$")|\b\w+\s*\+=\s*(?:"|\$"|fmt\.Sprint|String\.format\())' -t java -t kotlin -t cs -t go "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 2c "${PIPESTATUS[0]}"
rg -n --pcre2 '\.(?:inject|reduce)\b[^\n]*\|\s*(\w+)\s*,[^\n]*\|[^\n]*?(?:\b\1\s*\+\s*\[|\b\1\.merge\()' -t ruby "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 2d "${PIPESTATUS[0]}"
rg -n --pcre2 '\.fold\([^\n]*\{\s*(\w+)\s*,[^\n]*->\s*\1\s*\+\s' -t kotlin "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 2e "${PIPESTATUS[0]}"

# 3. CX-3 O(n) per-operation container use (JVM, .NET, Go, PHP, Ruby; JS and Python are in the script).
rg -n --pcre2 '\.remove\(\s*0\s*\)|\.add\(\s*0\s*,|\.RemoveAt\(\s*0\s*\)|\.Insert\(\s*0\s*,|\bappend\(\s*\[\][\w.*]+\{[^}\n]*\}\s*,\s*[\w.]+\.\.\.\s*\)|\barray_(?:shift|unshift)\(|\.(?:shift|unshift)\b' -t java -t kotlin -t cs -t go -t php -t ruby "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 3 "${PIPESTATUS[0]}"

# 4. CX-4 loop-invariant work per iteration (JVM, .NET, Go, Rust): compile, formatter or sort within 8 lines of a loop head.
rg -n -U --pcre2 '^[ \t]*+(?:for|foreach|while)\b[^\n]*\n(?:[^\n]*\n){0,8}?[^\n]*?\K(?:\bPattern\.compile\(|\.matches\(\s*"|\.replaceAll\(\s*"|\bregexp\.(?:MustCompile|Compile|MatchString)\(|\bRegex::new\(|\bnew\s+Regex\(|\bDateTimeFormatter\.ofPattern\(|\bnew\s+SimpleDateFormat\(|\b(?:Collections\.sort|Arrays\.sort|slices\.Sort|sort\.(?:Slice|Strings|Ints))\(|\.(?:OrderBy|OrderByDescending)\()' -t java -t kotlin -t cs -t go -t rust "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 4 "${PIPESTATUS[0]}"

# 5. CX-5 nested loops joining on keys (Go, JVM, .NET, PHP, Rust): an inner loop ≤ 4 lines into an outer one, then an equality.
rg -n -U --pcre2 '^([ \t]*+)(?:for|foreach)\b[^\n]*\n(?:\1[ \t]+[^\n]*\n){0,4}?\1[ \t]++(?:for|foreach)\b[^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*?\K\b\w+\.\w+\s*(?:==|\.equals\()\s*\w+\.\w+' -t go -t java -t kotlin -t cs -t php -t rust "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 5 "${PIPESTATUS[0]}"

# 6. CX-6 combinatorial generators, every stack (read where the cap is enforced: before generation, not after).
rg -n --pcre2 '\bitertools\.(?:product|permutations|combinations(?:_with_replacement)?)\(|\b(?:function\s*\*?\s*|def\s+|func\s+|fun\s+)\w*(?:[Cc]ombinations|[Cc]artesian\w*|[Pp]ermutations|[Pp]ower[Ss]et|power_set|[Ss]ubsets|[Aa]ll[Pp]airs|all_pairs)\b|\b(?:const|let|var)\s+\w*(?:[Cc]ombinations|[Cc]artesian\w*|[Pp]ermutations|[Pp]ower[Ss]et|[Ss]ubsets|[Aa]ll[Pp]airs)\s*(?::[^=\n]+)?=\s*(?:async\s*)?(?:\(|function\b|\w+\s*=>)|\b(?:Sets|Lists)\.cartesianProduct\(|\bSets\.powerSet\(|\bR\.xprod\(' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 6 "${PIPESTATUS[0]}"

# 7. RC-1/RC-2 in SQL: 7a recursive CTEs in code, 7c in migrations (a view), 7b the guard each needs (CYCLE clause, depth bound); 8 self-referencing parent
#    keys (a cycle the data can hold; migrations INCLUDED — they are the schema); 9 self-calls on the unparsed stacks;
#    10 unconditioned loops on the unparsed stacks (JS/TS and Python RC rows come from the script below).
rg -n --pcre2 '(?i)\bwith\s+recursive\b' "${X[@]}" -g '!**/node_modules/**' "${ROOTS[@]}"; st 7a $?
rg -n --pcre2 '(?i)\bwith\s+recursive\b' -g '**/{migrations,migration,db/migrate,alembic/versions,sql}/**' -g '!**/node_modules/**' .; st 7c $?   # views and functions in migrations: outside ROOTS
rg -n --pcre2 '(?i)\bCYCLE\s+\w+(?:\s*,\s*\w+)*\s+SET\b|\b(?:depth|level|lvl)\s*<=?\s*\d+' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 7b "${PIPESTATUS[0]}"
rg -n --pcre2 '(?i)\bparent_?id\b[^\n]{0,120}\b(?:references|@ManyToOne|ForeignKey|belongs_to|foreignKey|@relation)\b|\b(?:references|@ManyToOne|ForeignKey|belongs_to)\b[^\n]{0,120}\bparent_?id\b' "${X[@]}" -g '!**/{test,tests,__tests__,spec,e2e}/**' -g '!**/*.{spec,test}.*' . | "${NC[@]}"; st 8 "${PIPESTATUS[0]}"
rg -n -U --pcre2 '^[ \t]*func\s+(?:\([^)\n]*\)\s*)?(\w+)\s*\([^\n]*\{[ \t]*\n(?:(?!func\b)[^\n]*\n){0,40}?[^\n]*?\K(?<![\w.])\1\(' -t go "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 9a "${PIPESTATUS[0]}"
rg -n -U --pcre2 '^[ \t]*(?:(?:public|private|protected|internal|static|final|override|suspend|open|async|virtual)\s+)+(?:fun\s+)?[\w<>\[\],.? ]*?\b(\w+)\s*\([^\n;]*\)[^\n;=]*\{?[ \t]*\n(?:(?![ \t]*(?:(?:public|private|protected|internal|static|override|fun)\s))[^\n]*\n){0,40}?[^\n]*?\K(?<![\w.])(?:this\.)?\1\(' -t java -t kotlin -t cs "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 9b "${PIPESTATUS[0]}"
rg -n -U --pcre2 '^[ \t]*(?:def\s+(?:self\.)?(\w+[?!]?)|(?:public\s+|private\s+|protected\s+|static\s+)*function\s+(\w+))\b[^\n]*\n(?:(?![ \t]*(?:def\s|(?:(?:public|private|protected|static)\s+)*function\s))[^\n]*\n){0,40}?[^\n]*?\K(?:(?<![\w.:>$])\1\(|\$this->\2\(|(?<![\w>$])\2\()' -t ruby -t php "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 9c "${PIPESTATUS[0]}"
rg -n --pcre2 '^\s*for\s*\{\s*$|\bwhile\s*\(\s*(?:true|1)\s*\)|^\s*loop\s*\{|\bloop\s+do\b|\buntil\s+false\b|\bdo\s*\{' -t go -t java -t kotlin -t cs -t rust -t ruby -t php "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 10 "${PIPESTATUS[0]}"

# The candidate tables (JS/TS and Python): sites with caps resolved, then recursion and loop progress. Exit 2 = blocked.
R="$(IFS=,; echo "${ROOTS[*]}")"
python3 -I -B "$S" --repo=. --roots="$R" --tsv --out="$OUT/sites.tsv"; st py1 $?
python3 -I -B "$S" --repo=. --roots="$R" --recursion --tsv --out="$OUT/rec.tsv"; st py2 $?
awk -F'\t' 'NR>1 && ($13=="uncapped" || $13=="over-budget")' "$OUT/sites.tsv" | sort -t$'\t' -k13,13r -k11,11nr | head -40
awk -F'\t' 'NR>1 && $10 ~ /^(RC-[123]\?|no-exit|read)$/' "$OUT/rec.tsv"
echo "# tables: $OUT/sites.tsv $OUT/rec.tsv · pre-flight exit $RC"; [ "$RC" -eq 0 ]
```

A finding is a table row or a grep hit **plus** a read of the enclosing function **plus** each cap
checked in the file it names **plus** the hops back to an entry point. Three blind spots are
structural, so work around them rather than trust a quiet run:

- **Receiver typing is heuristic.** The script types a receiver from its declaration in the same file
  (`new Set`, a `: string` annotation, a literal, a string method); an import, a destructured
  parameter or a `useState` pair is `array?`. Read the declaration before dismissing or keeping.
- **Recursion through another function** (mutual recursion, a callback registry, a visitor that
  dispatches by type) is not a self-call. Grep the walker's name across the file when a
  `walks=children|json` row appears without its partner.
- **Other stacks are grep-only.** Go, JVM, .NET, Ruby, PHP and Rust are counted by the script and
  searched by greps 1–10 with a 6–8-line loop window; a lookup further from its loop head is missed.
  Read every function that the lane's loop greps list in full.

**Measured** (2026-10-19, read-only) on a real NestJS 11 + Fastify + MikroORM 6 + React monorepo,
`ROOTS=(apps/api/src apps/web/src packages/contracts/src)`, 6,930 TS files, about 38 s for the whole
block: the sites table has 560 rows — 245 dismissed by the arithmetic (172 `const-small`, 35
`below-budget`, 32 `string`, 6 `set`) and 315 open (141 server, 171 browser, 3 shared contracts; one
`over-budget`: a group-by-scan over two lists each capped at 5,000, 2.5e7 comparisons worst case, to
read for the realistic size). The recursion table has 28 rows: 6 `json-tree`, 5 `guarded`, 6
`keyset` loops, 7 loops to read, 4 `RC-1?` (one is the client-side Cartesian-product walker grep 6
also lists — the one live CX-6 candidate). Grep 6 returns 3 (two generators, one assertion), 7a and
7b 1 each (one recursive CTE advancing on a strict key), 8 none, 0b the body limit and two redaction
depth caps; the other-stack greps search no file there. Against the naive greps the eval measured on
the same tree (97 / 264 / 31 / 179), the open list is ordered by side and cap, not shorter in rows:
**the read is still the precision step**, and the 3,000-hit path below is how it stays affordable.
On the 28 other `benchmarks/fixtures` the script prints 30 site rows (15 open, mostly role and
permission lists checked per required item) and 10 recursion or loop rows; greps 1–9 return nothing
beyond them, and grep 10 lists four process-lifetime loops (precedent § 32). On `algo-defects`
(2026-10-19, staged without its key; TS, Python, Go, Java; 0.6 s; no `rg` exit 2) the block prints all
20 of its seeds: `sites.tsv` 11 rows (9 uncapped — 7 seeds, a `find` on one seed's per-iteration copy, and the
capped-FIFO decoy, precedent § 8 — 1 `below-budget` decoy at 800 × 800, 1 `set`), `rec.tsv` 9 rows (2 `RC-2?`, 2 `RC-3?`, 1 `RC-1?`, 1
`read` cursor; the `json-tree`, `guarded` and `keyset` decoys stay out of the awk print; the root-down
walk decoy prints as `RC-2?` and is closed by § 14), and greps 2a, 2c, 4, 5, 6 (2), 7a, 8, 9a and 10
one hit each, every hit a seed. Building it found three gaps, fixed the same day: grep 7c now reads
recursive CTEs in migrations, a `>=` cursor is never hinted `keyset`, and `i + 1` self-calls count as
RC-3. Two blind spots stay: no Python lane for a regex compiled per iteration, and a precompiled
regex's method call in a loop is not CX-4 (correctly: compiled once).

## The 3,000-hit path

1. **Split by side.** Server roots first (request, consumer, job), shared packages second, browser
   last; a browser-only row is low severity at most.
2. **Trust the arithmetic, check one cap per source.** Rows with hint `set`, `string`, `const-small`
   or `below-budget` are not read one by one: read **one** row per cap source (`const:<NAME>`,
   `schema:<file:line>`, `limit:<NAME>`) to confirm the cap is real and enforced on the path, then
   close the group with that citation in the coverage block.
3. **Group the open rows** by (file, receiver) and by cap source; one read decides a group that shares
   a receiver and a loop source.
4. **Rank** by reachability (an unauthenticated route, a list or import endpoint, a consumer) and by
   `ops` where known; read the top 20 groups fully.
5. **Prefer the oracle at scale.** For a suspected hot module, run V590's counter over the module's
   own tests with the fixture size raised to N and 4N; every function whose count ratio is ≥ 12×
   is confirmed in one run.
6. **Ledger the rest** as `Live, unreviewed (k groups / n rows)` with the command that continues
   them (`awk -F'\t' '$13=="uncapped" && $1 ~ /<dir>/' "$OUT/sites.tsv"`). Never mark them `checked`.

## Scans for

| § | Class | CWE | Default severity |
|---|---|---|---|
| 1 | CX-1 linear lookup inside a loop over a data-sized collection | CWE-407, CWE-1067 | high on a request path with tenant-sized n; else medium |
| 2 | CX-2 copy-per-iteration accumulation | CWE-407, CWE-1046 | medium |
| 3 | CX-3 O(n) per-operation container use in a loop | CWE-407 | medium |
| 4 | CX-4 loop-invariant recompute per iteration | CWE-1176 | low–medium |
| 5 | CX-5 nested-loop join of two data-sized collections | CWE-407 | medium |
| 6 | CX-6 combinatorial generation without the downstream cap | CWE-407, CWE-770 | low (browser) – high (server) |
| 7 | RC-1 recursion depth set by input with no cap | CWE-674 | medium; high when unauthenticated or the runtime dies (Go) |
| 8 | RC-2 traversal of a structure that can hold a cycle, no visited set | CWE-835, CWE-674 | high (hang) |
| 9 | RC-3 exponential recursion over overlapping subproblems, no memo | CWE-407 | medium–high |
| 10 | RC-4 loop whose progress is not guaranteed | CWE-835 | high (hang) |

### 1. Linear lookup inside a loop (CX-1)

```
BAD:   orders.filter(o => ids.includes(o.id))            · for x in items: if x in seen_list: …
       for (String x : xs) if (ids.contains(x)) …       · xs.each { |x| ids.include?(x) } · in_array($x, $ids) in foreach
GOOD:  const wanted = new Set(ids); orders.filter(o => wanted.has(o.id))   · seen = set() · Set<String> · array_flip once
```
**Read the code:** What bounds each collection (the row's `n_src` / `m_src`, checked in the file it
names)? Is the receiver really a list — or a `Set`, a string, a constant? Is the work per request,
per job, per frame? Is the receiver pushed to in the same loop (a dedupe-by-scan, kind
`accumulator`)? Does a library already hash (`_.difference` at ≥ 200 items; `precedents/algorithms.md`
§ 3)? **Finding when** both sides grow with users or data past the budget on a production path.
**Proof:** V590 — a counter on the lookup at N and 4N (≈ 16× before, ≈ 4× after).

### 2. Copy-per-iteration accumulation (CX-2)

```
BAD:   xs.reduce((acc, x) => ({ ...acc, [x.id]: x }), {})   · out = [...out, x] in a loop · all = all.concat(x.items)
       acc = acc + [r] · sum(lists, []) · s = s + "," + x in a Java/C#/Go loop · inject { |a, x| a + [x] }
GOOD:  const byId = {}; for (const x of xs) byId[x.id] = x  · out.push(x) · acc.append(r) · itertools.chain · StringBuilder
```
`acc.concat(x)` is the non-fix a lint rule does not flag (`precedents/algorithms.md` § 3 for
lodash; Sentry #7910). **Read the code:** Is the accumulator a persistent structure (Immer,
Immutable.js: § 7)? Is the JS string only appended (§ 4) or a CPython local (§ 5)? **Finding when**
the accumulator grows with a data-sized loop. **Proof:** V591.

### 3. O(n) per-operation container use (CX-3)

```
BAD:   while (queue.length) { const n = queue.shift(); … }   · q.pop(0) · list.remove(0) · RemoveAt(0) · append([]T{x}, s...)
GOOD:  a head index (`for (let i = 0; i < q.length; i++)`) · collections.deque · ArrayDeque · Queue<T> · a ring buffer
```
**Read the code:** Is the queue capped (`if (q.length >= MAX) throw` — the row's `guard` source; a
bounded FIFO is § 8)? Does it grow with the input (a BFS frontier, an import buffer)? **Finding when**
the container grows with data and each operation shifts it. **Proof:** V592.

### 4. Loop-invariant recompute (CX-4)

```
BAD:   for (const u of users) { const sorted = rates.slice().sort(cmp); const s = new Set(allowed); … }
       for (const x of xs) new RegExp(pattern) · Pattern.compile(p) / regexp.MustCompile(p) in a loop · sorted(prices) per user
GOOD:  hoist above the loop: const sorted = …; const s = new Set(allowed); const re = new RegExp(pattern)
```
The script keeps a site only when nothing in its subject is a loop variable or is declared inside the
loop body. **Read the code:** Is the subject really invariant across iterations? Python's `re` cache
and a JS regex literal are § 9. A per-*call* construction (once per request) is `request-path-scan`
§8, not here. **Finding when** invariant work of size m runs n times on a data-sized loop.
**Proof:** V593 (a spy counts one call per invocation).

### 5. Nested-loop join (CX-5)

```
BAD:   for (const a of as) for (const b of bs) if (a.id === b.aId) …   · teams.map(t => ({ …t, members: all.filter(m => m.teamId === t.id) }))
GOOD:  const byA = Map.groupBy(bs, b => b.aId)  (or a Map built once);  as.map(a => byA.get(a.id) ?? [])
```
A `filter` inside a `map` over a second collection is the same class (the script reports it as CX-1
on the inner receiver). **Read the code:** Do both sides scale? Is one a fixed list? **Proof:** V590.

### 6. Combinatorial generation without the downstream cap (CX-6)

```
BAD:   const combos = cartesian(attributes.map(a => a.values));  …  if (combos.length > MAX_SKUS) reject();
GOOD:  generate lazily and stop at MAX_SKUS + 1 (then refuse) · or refuse at the input: Π |values| ≤ MAX_SKUS
```
**Read the code:** Where is the downstream limit (a maximum the server enforces) and does generation
stop at it, or filter after it? What caps the factors (attribute count × values each)? **Finding
when** the product of the factors can exceed the downstream cap by orders of magnitude before the cap
applies. **Proof:** V594.

### 7. Recursion depth set by input (RC-1)

```
BAD:   function render(node) { return [node, ...node.children.flatMap(render)]; }   // a user-built tree, no depth cap
GOOD:  function render(node, depth = 0) { if (depth > MAX_DEPTH) throw new TooDeep(); … }  · or an explicit stack
```
**Read the code:** Where does the depth come from — parsed JSON under a body limit (grep 0b; § 12), a
trusted AST (§ 17), a stored tree a user edits? What does the runtime do at the limit (Node
`RangeError`, catchable; Python `RecursionError`; Java `StackOverflowError`, often uncaught; Go grows
to 1 GB, then dies fatally)? Is the handler unauthenticated? A `json-tree` row is § 12's candidate;
an `RC-1?` row is read. **Finding when** input sets the depth with no cap and the overflow fails more
than the one request. **Proof:** V595 (a depth bomb in a child process; measure, never quote a frame
count).

### 8. Traversal that can meet a cycle (RC-2)

```
BAD:   const rootOf = (c) => (c.parent ? rootOf(c.parent) : c);       // parent editable by users
       WITH RECURSIVE t AS (… UNION ALL SELECT c.* FROM cat c JOIN t ON c.parent_id = t.id)   -- no CYCLE, no depth
GOOD:  a visited set and a depth cap · CYCLE id SET is_cycle USING path (PostgreSQL ≥ 14) · a strictly increasing key
```
**Read the code:** Can the data hold a cycle — a self-referencing parent key (grep 8) a user can set,
an imported graph, a `cause` chain? Is the walk root-down from `null` (§ 14)? Does a recursive CTE
advance on a strictly increasing key (§ 15)? **Finding when** a cycle is writable and the walk has no
visited set or depth bound. **Proof:** V596.

### 9. Exponential recursion without a memo (RC-3)

```
BAD:   const ways = (n) => (n < 2 ? 1 : ways(n - 1) + ways(n - 2));     // n from a request
GOOD:  a memo keyed on the full argument tuple · functools.cache · an iterative DP table
```
**Read the code:** Do the self-calls overlap? Is n user-sized or a small constant? Is the memo keyed
on every argument that changes the result (§ 16)? **Proof:** V597.

### 10. Loop progress not guaranteed (RC-4)

```
BAD:   for (;;) { const rows = await find({ createdAt: { $gte: after } }, { limit: 500 }); …; after = rows.at(-1).createdAt; if (!rows.length) break; }
GOOD:  a unique key (or a composite) with strict `>`, and exit on a short page: if (rows.length < 500) break
```
The recursion table prints each `for(;;)` / `while(true)` / `do … while` with its progress variable,
the cursor compare (`strict` / `non-strict`) and whether it exits on a short page. **Read the code:**
What strictly increases per iteration? Is the cursor unique? Is the exit an empty page a concurrent
insert can postpone, or a float compared with `!=`? A loop meant to run until shutdown is § 32.
**Finding when** a reachable input stalls the progress variable. **Proof:** V598.

## Output

```
complexity-scan — lanes: ts (algo-sites.py), python (algo-sites.py); eslint 10.10 present, biome/oxlint/ruff absent → NOT-RUN; go, jvm, .net, ruby, php, rust: no files
Context: body limit 1 MiB (src/main.ts:12) · tables: /tmp/complexity-scan.Ab12/sites.tsv, rec.tsv

Findings: 1 · Unconfirmed: 1

1. src/reports/roster-summary.service.ts:41                               [report-with-fix]   medium
   §5 nested-loop join — teams.map(t => members.filter(m => m.teamId === t.id)); teams ≤ 5,000 and
   members ≤ 5,000 (limit: MAX_REPORT_ROWS, src/reports/limits.ts:3) → 2.5e7 compares per call,
   budget 1e6. Reached by GET /reports/teams (admin). Proof: test/reports/roster-summary.ops.spec.ts —
   compares 16× from N=500 to N=2,000 (fails); after: 4×. Fix: group members once with Map.groupBy.

2. web/src/catalog/option-grid.ts:7                                [report-flagged]    low
   §6 combinatorial generation — the Cartesian product of every attribute's values is built before
   the server's MAX_SKUS = 500 applies; 20 attributes × 100 values are accepted. Unproven link: no
   component test harness. Settling test (V594): 6 × 10 values → generation stops at 501.

Verification: 9 candidates → 1 finding · 1 unconfirmed · 4 hardening · 3 refuted

Class coverage:
  §1  linear lookup in a loop      checked (553 rows: 245 closed by cap source, 9 groups read → 0) · Live, unreviewed (41 groups / 288 rows — continue with the awk line above on web/)
  §2  copy-per-iteration           checked (2 rows → 0: below budget)
  §3  O(n) container op            checked (8 rows → 0: two capped queues, § 8)
  §4  invariant recompute          checked (12 rows → 0)
  §5  nested-loop join             checked (4 rows → 1 finding)
  §6  combinatorial generation     checked (grep 6: 3 → 1 unconfirmed)
  §7  recursion depth              checked (10 rows: 6 json-tree under the body limit, 4 read → 0)
  §8  cycles                       checked (grep 8: 0 self-referencing parent keys; 7a: 1 CTE on a strict key, § 15)
  §9  exponential recursion        checked (0 rows)
  §10 loop progress                checked (13 loops: 6 keyset, 7 read → 0)
```

`[report-with-fix]`: the caps are cited, the entry point is traced, the counting test failed, and the
fix is a local change with the language's primitive. `[report-flagged]`: one link is unproven (no
harness, a cap read only in part, a recursion through code not read), and the row names it and the
settling test. The coverage block lists **all ten** classes on every run: `checked (k → m)` only when
the table or grep ran on a present lane; `N/A (<reason>)` only when the repo has no such surface (no
SQL, no unconditioned loop); `blocked (<reason>)` when a grep exited 2 or the script could not run. A
partial review reads `Live, unreviewed (k groups / n rows)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/algorithms.md`](../../../../snippets/precedents/algorithms.md)
(§ 1–§ 17, § 29–§ 33 for this skill) and
[`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones met most:
a side bounded by a cited constant (§ 1, § 29); an index built once outside the loop (§ 2); a bounded
FIFO (§ 8); parsed JSON under a body limit (§ 12); a walker with a depth cap and an ancestor set
(§ 13); a root-down parent walk (§ 14); a keyset loop on a unique key (§ 15); a memo (§ 16); a
process-lifetime loop (§ 32); a counted retry or Euclid's recursion (§ 33); an ORM `find(Entity, …)`
per element, which is database's N+1 (§ 30).

## When to run

- On any diff that adds or changes a loop over query results, request arrays or uploads; a
  `reduce`/`filter`/`find` inside another loop; a recursive function; a `for(;;)`/`while(true)`
  cursor loop; a recursive CTE; a generator of combinations — the `/analyze-complexity` dispatch
  signal.
- On every whole-repo `/analyze-complexity`, reporting all ten classes. `/perf-audit` lists §11's
  classes as `owner: algorithms` when this pack is installed.
- When a profile or a trace shows one function's time growing with a tenant's data size.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed
  it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 1–§ 8. Under
  `/analyze-complexity` that is `@algorithm-designer` in refute mode plus `@verifier`; run standalone,
  apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as
  Unconfirmed, Hardening or Refuted. Never drop them.
- Halt when any `rg` exits 2 or `algo-sites.py` exits 2: the class it feeds is `blocked`, never
  `checked`.
- Halt on any finding without the site `<file:line>`, the cap on each side (or the cited absence),
  the entry point, and the fix.
- Do not mark a row `[report-with-fix]` without an operation-count (or depth, cycle, progress) test
  that failed first. Never assert a complexity class from reading or from a model.
- Do not propose a cache, more replicas, a bigger stack (`--stack-size`, `setrecursionlimit`) or a
  timeout as the fix. The fix changes the data structure, adds the cap, the visited set, the memo or
  the strict cursor.
- Do not print "no complexity defect" without the class-coverage block.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `/analyze-complexity` dispatches this skill with `algorithm-contract-scan` and
  `numeric-stability-scan` and folds the coverage blocks into its class ledger;
  `/design-algorithm --from-audit` closes the findings failing-first and re-runs the class's greps.
- `complexity-derivation` (this pack) derives the bound a row's arithmetic states; `@algorithm-designer`
  judges rows in refute mode.
- `request-path-scan` §8, §11, §13 and `memory-growth-scan` §1, §8 (performance pack, when installed);
  `n-plus-one-scan` (database pack, when installed); `injection-scan` §13 (security pack, when
  installed).
- `rules/algorithm-principles.md` — the budget table and the "right container" MUST this skill
  enforces.
