---
name: algorithm-contract-scan
description: Find input that breaks an algorithm's contract — unsorted search, unstable ties, key collapse, biased draws, geodesy.
kind: skill
pack: algorithms
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: algorithm-contract-scan

## Premise

Every algorithm assumes something about its input, and none of them checks it. A binary search
assumes the array is sorted by the same key and collation; a multi-pass sort assumes ties keep their
order; a `Map` built from rows assumes the key is unique; a shuffle assumes every permutation is
equally likely; a bucket assigner assumes the hash is non-negative and stable across restarts; a
distance formula assumes a plane, metres and a known axis order. When the data breaks the
assumption, the code returns a plausible wrong answer — a missed search hit, a reordered page, a
silently dropped row, an unfair draw, a store that "isn't within 5 km" — and no exception is thrown.
CWE files them under **CWE-697** (incorrect comparison), **CWE-193** (off-by-one), **CWE-330**
(insufficiently random values, here as a distribution), **CWE-190** and **CWE-682** (incorrect
calculation).

**Every finding cites the algorithm `<file:line>` + its class + the contract it assumes + the path
that feeds it input breaking that contract (or the library convention it violates) + the entry point
+ the proof + the fix.** A grep hit is never a finding, and "no contract defect" is never printed
without the class-coverage block (§ Output).

**The contract is checked at both ends.** A sortedness claim cites the sort (or its absence) on every
path to the search; a uniqueness claim cites the constraint, the `GROUP BY` or the validator (or
their absence); an axis-order claim cites the library's convention and the caller's order. Behaviour
is proved by a differential test, a chi-square with a fixed seed or a reference vector
([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Algorithms, V599–V607).

## The rule

A site is a finding when all four hold:

1. **A production path runs it** — a route, a job, a consumer, a page on a real route.
2. **The input that breaks the contract occurs.** Unsorted or differently-collated data reaches the
   search; equal keys exist and their order is observable; two rows share the key; the draw decides
   something a user can see; coordinates come from more than one convention or cross ±180°.
3. **No control restores the contract.** A sort by the same key on that path, a stable sort or a
   total tie-break, a unique constraint in the same scope, a vetted shuffle, `crypto.randomInt`, an
   unsigned hash, a `::geography` cast, a boundary validator.
4. **The oracle fires failing-first** (V599–V607), or the two-ended static fact is cited (V601's
   constraint, V606's convention, V605's column type). Without either the row is Unconfirmed with the
   test written out.

**Severity.** **High** when a collapse or a precondition violation loses or misattributes persisted
data, a draw or a bucket decides money, eligibility or fairness, or a distance or axis error decides
delivery or pricing; **medium** for wrong-but-visible results (a search hit missed, a page reordered)
and job paths; **low** for one browser view or admin-only paths.

## Boundaries

A comparator, parse or date expression wrong for one input — no comparator on numbers, a boolean
comparator, subtraction overflow, a non-transitive tolerance, NaN keys — is code-quality
`correctness-smell-scan` §4 (and §2 for equality, §6 for dates); a database sort key that is not
unique, and deep `OFFSET`, are database `query-shape-scan`; a predictable secret, OTP, nonce or
prize from a non-cryptographic generator is security `sast-scan` (CWE-338; gosec `G404`, Ruff `S311`
and sonarjs S2245 are security's lanes); a spatial index is database `index-coverage-scan`;
`ORDER BY random()` cost is performance's. This skill owns what an algorithm assumes about its input
— sortedness, stability, key uniqueness — and the distribution of random draws and the geometry of
coordinates. Each cross-pack route applies when that pack is installed; without it the row is listed
here, tagged `<class> (owner pack <x> not installed)`, and never graded as the owner would grade it.

## Adapt to the codebase — lanes

Read every analyzer's version from the lockfile or manifest (grep 0a); a lane whose binary is not in
the project is `NOT-RUN (<reason>)`, never PASS and never installed from the network. Semgrep, when a
team owns local rules for these classes, runs with `--metrics=off` and only those rules.

| Lane | Analyzer rules (version from the lockfile) | Stable sort? | Primitives the fix names |
|---|---|---|---|
| **TS / JS** | — | yes (ES2019+) | `crypto.randomInt`, lodash `shuffle`, `Map.groupBy`, turf / geographiclib |
| **Python** | — (`S311` is security's) | yes | `bisect` on a list sorted by the same key, `random.shuffle`, `secrets`, `hashlib`, geographiclib / pyproj |
| **Go** | staticcheck `SA4030` (a `rand` call that always returns 0) | `sort.Slice`, `slices.SortFunc` no; `sort.SliceStable`, `slices.SortStableFunc` yes | `rand.Shuffle`, `rand.Perm`, `hash/fnv` unsigned |
| **JVM** | SpotBugs `RV_REM_OF_HASHCODE`, `RV_REM_OF_RANDOM_INT`, `RV_ABSOLUTE_VALUE_OF_HASHCODE`, `RV_ABSOLUTE_VALUE_OF_RANDOM_INT`, `DM_NEXTINT_VIA_NEXTDOUBLE`, `DMI_RANDOM_USED_ONLY_ONCE` (STYLE codes need the threshold raised); Error Prone `RandomCast`, `RandomModInteger`, `MathAbsoluteNegative` | object sorts yes | `Collections.shuffle`, `Math.floorMod`, `ThreadLocalRandom.nextInt(a, b)`, a `TreeSet` comparator consistent with `equals` |
| **.NET** | — (`DOTNET_CLI_TELEMETRY_OPTOUT=1`) | `List.Sort`, `Array.Sort` no; LINQ `OrderBy().ThenBy()` yes | `Random.Shared.Next(a, b)`, `RandomNumberGenerator.GetInt32` |
| **Ruby** | — | UNVERIFIED (not researched) — add the index as a tie-break where ties matter | `shuffle`, `sample`, `index_by` with a uniqueness check |
| **PHP** | — | `usort` stable from PHP 8.0 (read the `php` constraint, grep 0a) | `random_int`, `shuffle` |
| **Rust** | — | `sort_unstable*` no; `sort_by` yes; ≥ 1.81 a non-total `Ord` may panic | `rand::seq::SliceRandom::shuffle` |
| **SQL / PostGIS** | — | `ORDER BY` stability is database's | `::geography`, `ST_DistanceSphere`, a projected metric SRID, `ST_MakePoint(lon, lat)` |

## Pre-flight

Run as **one** bash script from the repo root, with `ROOTS` set to the production source roots.
Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path, every exit code is
printed, and an exit 2 fails the step instead of reading as zero hits. Nothing is written and nothing
touches the network.

```bash
set -u
declare -p ROOTS >/dev/null 2>&1 || ROOTS=(.)   # production source roots, e.g. ROOTS=(apps/api/src apps/web/src)
RC=0; st() { printf '# %-3s rc=%s\n' "$1" "$2"; [ "$2" != 2 ] || RC=2; }   # rg: 0 hits, 1 none, 2 FAILED
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**'
   -g '!**/.venv/**' -g '!**/coverage/**' -g '!**/*.min.*' -g '!**/*.d.ts' -g '!**/*.{md,mdx,lock,map,svg,json,snap,yml,yaml,css,scss,html}')
T=(-g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,seeds,seeders,migrations,locales,i18n,generated,__generated__,docs}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,fuzz-spec,test-data,fixture,bench}.*' -g '!**/{*_test,*_spec,test_*,conftest}.*' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')
for t in js ts py go java kotlin cs ruby php rust cpp sql; do printf '%-7s %s\n' "$t" "$(rg --files -t "$t" "${X[@]}" "${T[@]}" "${ROOTS[@]}" | wc -l)"; done

# 0. Context: 0a analyzer and property-harness pins (lanes, the fix's harness, the PHP version for usort); 0b geo libraries
#    and spatial column types (the GE lane exists only when 0b or greps 8–10 hit). Migrations are read here: they are the schema.
rg -n --no-heading --pcre2 '<artifactId>(?:spotbugs|error_prone_core)[\w-]*</artifactId>|com\.github\.spotbugs|net\.ltgt\.errorprone|honnef\.co/go/tools|"(?:fast-check|@fast-check/\w+|php)"\s*:\s*"[^"]+"|^\s*(?:hypothesis|semgrep)\b[^\n]*\d|\bjqwik\b|\bproptest\b|pgregory\.net/rapid|\bFsCheck\b|\bCsCheck\b' -g 'package.json' -g 'composer.json' -g 'pyproject.toml' -g 'requirements*.txt' -g 'go.mod' -g 'pom.xml' -g 'build.gradle*' -g 'Cargo.toml' -g '*.csproj' -g '!**/node_modules/**' .; st 0a $?
rg -n --no-heading --pcre2 '"(?:@turf/[\w-]+|geolib|geographiclib[\w-]*|leaflet|mapbox-gl|maplibre-gl|@googlemaps/[\w-]+|proj4|h3-js|kdbush|geokdbush)"\s*:|^\s*(?:shapely|geopy|pyproj|geographiclib|geopandas|h3)\b|(?i:\bcreate\s+extension\b[^\n]*\bpostgis\b)|\bgeography\s*\(|\bgeometry\s*\(\s*\w+\s*,\s*\d+|github\.com/(?:golang/geo|paulmach/orb|twpayne/go-geom)|\borg\.locationtech\.jts\b|\bNetTopologySuite\b|\brgeo\b' -g 'package.json' -g 'pyproject.toml' -g 'requirements*.txt' -g 'go.mod' -g 'pom.xml' -g 'build.gradle*' -g 'Gemfile' -g '*.csproj' -g '*.sql' -g '*.prisma' -g '**/migrations/**' -g '!**/node_modules/**' .; st 0b $?

# 1. OC-1 sorted-input precondition: 1a binary search / bisect / groupby / sortedIndex; 1b adjacent-dedupe and merge shapes.
rg -n --pcre2 '\bbinarySearch\(|\bbisect\.\w+\(|\bbisect_(?:left|right)\(|\binsort(?:_left|_right)?\(|\bsort\.Search(?:Ints|Strings|Float64s)?\(|\bslices\.BinarySearch(?:Func)?\(|\bsortedIndex\w*\(|\bitertools\.groupby\(|(?<![\w.])groupby\(|\b(?:Collections|Arrays|Array)\.(?:binarySearch|BinarySearch)\(|\.BinarySearch\(|\.binary_search(?:_by(?:_key)?)?\(|\bbsearch\(' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 1a "${PIPESTATUS[0]}"
rg -n --pcre2 '\b(\w+)\[\s*(\w+)\s*\]\s*!==?\s*\1\[\s*\2\s*-\s*1\s*\]|\b(\w+)\[\s*(\w+)\s*-\s*1\s*\]\s*!==?\s*\3\[\s*\4\s*\]|\bwhile\s*\(?\s*\w+\s*<\s*[\w.]+\.(?:length|size\(\)|Count)\s*&&\s*\w+\s*<\s*[\w.]+\.(?:length|size\(\)|Count)' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 1b "${PIPESTATUS[0]}"

# 2. OC-2 sorts that are not stable (Go, .NET, Rust, C++, PHP < 8.0). JS (ES2019+), Python and Java object sorts are stable.
rg -n --pcre2 '\bsort\.(?:Slice|Sort)\(|\bslices\.SortFunc\(|\.sort_unstable(?:_by(?:_key)?)?\(|\bstd::sort\(|\bArray\.Sort\(|\b\w+\.Sort\(\s*(?:\)|\(|delegate\b|\w+\s*=>|new\s|Comparer)|\bu[ak]?sort\(' -t go -t cs -t rust -t cpp -t php "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 2 "${PIPESTATUS[0]}"

# 3. OC-3 an index or ordered container whose key can collapse rows: 3a keyed by anything but an id; 3b the id-keyed count
#    (one query's rows keyed by their primary key cannot collapse — context only); 3c sorted containers with a comparator.
rg -n --pcre2 '\bnew\s+Map\(\s*[\w$.?]+\.map\(\s*\(?\s*(\w+)\s*\)?\s*=>\s*\[\s*\1\.(?!(?:id|uuid|pk|_id|externalId)\b)|\bObject\.fromEntries\(\s*[\w$.?]+\.map\(\s*\(?\s*(\w+)\s*\)?\s*=>\s*\[\s*\2\.(?!(?:id|uuid|pk|_id)\b)|\b_\.keyBy\(|\bkeyBy\(\s*[\w$.]+\s*,\s*["\x27](?!id["\x27])|\bCollectors\.toMap\(|\.associateBy\s*[({]|\.ToDictionary\(|\.index_by\b|\{\s*\w+\.(?!(?:id|pk|uuid)\b)\w+\s*:\s*\w+\s+for\s+\w+\s+in\b' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 3a "${PIPESTATUS[0]}"
rg -c --pcre2 '\bnew\s+Map\(\s*[\w$.?]+\.map\(\s*\(?\s*(\w+)\s*\)?\s*=>\s*\[\s*\1\.(?:id|uuid|pk|_id)\b' "${X[@]}" "${T[@]}" "${ROOTS[@]}"; st 3b $?
rg -n --pcre2 '\bnew\s+(?:TreeSet|TreeMap|ConcurrentSkipListSet|ConcurrentSkipListMap)\s*<[^>\n]*>?\s*\(\s*(?:\(|\w+\s*->|Comparator|\w+::)|\bnew\s+Sorted(?:Set|Dictionary|List)\s*<[^>\n]*>\s*\(\s*(?:new\s|\w)|\bstd::(?:set|map|multiset)<[^>\n]*,\s*\w+\s*>|\bsortedcontainers\b|\bSortedList\(\s*key\s*=' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 3c "${PIPESTATUS[0]}"

# 4. OC-4 hand-rolled search, sort, heap, LRU and polygon tests (is there a primitive?).
rg -n --pcre2 '\bwhile\s*\(?\s*(?:lo|low|left|l|start|begin)\s*<=?\s*(?:hi|high|right|r|end)\b|\bclass\s+\w*(?:Heap|PriorityQueue|LRU|LruCache|MinHeap|MaxHeap)\b|\binside\s*=\s*!\s*inside\b|\b(?:function|def|func|fun)\s+(?:quick|merge|heap|insertion|bubble)_?[Ss]ort\b' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 4 "${PIPESTATUS[0]}"

# 5. RD-1 biased shuffles: sort by a random comparator, a random sort key, ORDER BY random() as a shuffle, hand-rolled shuffles.
rg -n --pcre2 '\.sort\(\s*(?:\(\s*\)\s*=>|function\s*\(\s*\)\s*\{\s*return)\s*(?:Math\.random\(\)\s*-\s*0?\.5|0?\.5\s*-\s*Math\.random\(\))|\bsorted\([^\n]*\bkey\s*=\s*lambda[^:\n]*:\s*random\.random\(\)|\.OrderBy\(\s*\w+\s*=>\s*(?:\w+\.Next\(|Guid\.NewGuid\(\))|(?i:\border\s+by\s+(?:random|rand)\(\))|\b(?:function|def|func|fun)\s+\w*[Ss]huffle\w*|\b(?:const|let|var)\s+\w*[Ss]huffle\w*\s*=' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 5 "${PIPESTATUS[0]}"

# 6. RD-2 range, bias and weight errors in a draw; 6b every Math.random() call (a read list: jitter and keys are § 21).
rg -n --pcre2 'Math\.round\(\s*Math\.random\(\)\s*\*|Math\.floor\(\s*Math\.random\(\)\s*\*\s*\(\s*[\w.]+\s*-\s*[\w.]+\s*\)\s*\)|\brandomBytes\(\s*\d+\s*\)\s*\[\s*\d+\s*\]\s*%|\b(?:rand|random|mt_rand)\(\)\s*%|\.nextInt\(\)\s*%|\(int\)\s*\(?\s*[\w.]+\.nextDouble\(\)\s*\*|\bnew\s+Random\(\s*\)\s*\.\s*next|\brandom\.randint\(|\bMath\.random\(\)\s*[<>]=?\s*[\w.]*(?i:weight|prob|ratio|rate|chance|percent|share)' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 6a "${PIPESTATUS[0]}"
rg -n --pcre2 '\bMath\.random\(\)|\brandom\.(?:random|choice|choices|uniform|sample)\(|\brand\.(?:Intn|Float64|Perm)\(|\bnew\s+Random\(' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 6b "${PIPESTATUS[0]}"

# 7. RD-3 bucketing by a signed, salted or n-dependent hash.
rg -n --pcre2 '\bhashCode\(\)\s*%|\bMath\.abs\(\s*[\w.]+\.hashCode\(\)\s*\)|(?<![\w.])hash\(\s*[\w.]+\s*\)\s*%|\bGetHashCode\(\)\s*%|\bcrc32\([^)\n]*\)\s*%|\b\w*[Hh]ash\w*\s*%\s*(?:\d+|[\w.]*(?:[Bb]uckets?|[Ss]hards?|[Pp]artitions?|[Vv]ariants?|[Cc]ount|len|length|size)\b)' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 7 "${PIPESTATUS[0]}"

# 8. GE-1 distance: 8a Euclid on coordinates, 8b degrees into trig with no conversion on the line, 8c earth radii,
#    8d PostGIS distance/buffer calls (read the column type and casts; migrations INCLUDED for the type).
rg -n --pcre2 '\b(?:Math|math|np)\.(?:sqrt|hypot)\([^\n]*(?:\b(?:lat|lng|lon|latitude|longitude)\d?\b|\b\w*(?:Lat|Lng|Lon|Latitude|Longitude)\d?\b|\b\w*_(?:lat|lng|lon)\d?\b)|(?:\b(?:lat|lng|lon)\d?\b|\b\w*(?:Lat|Lng|Lon)\d?\b)\s*\)?\s*\*\*\s*2|\bMath\.pow\(\s*\(?\s*[\w.]*(?:lat|lng|lon|Lat|Lng|Lon)\d?\b' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 8a "${PIPESTATUS[0]}"
rg -n --pcre2 '\b(?:Math|math|np)\.(?:sin|cos|tan|atan2|asin|acos)\(\s*[^)\n]*(?:\b(?:lat|lng|lon|latitude|longitude)\d?\b|\b\w*(?:Lat|Lng|Lon|Latitude|Longitude)\d?\b|\b\w*_(?:lat|lng|lon)\d?\b)' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | rg -v --pcre2 '(?i)pi\s*/\s*180|radians|torad|deg2rad|deg_to_rad|\brad\b|\w+Rad\b' | "${NC[@]}"; st 8b "${PIPESTATUS[0]}"
rg -n --pcre2 '\b(?:6371(?:\.0+)?|6371008\.8|6371000|6378137|6378\.137|3958\.8|3959)\b|\b(?:EARTH_RADIUS\w*|earthRadius\w*|R_EARTH)\b' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 8c "${PIPESTATUS[0]}"
rg -n --pcre2 '(?i)\bST_(?:Distance|DWithin|Buffer|Length|Area|Intersects)\s*\(|\bST_SetSRID\s*\(\s*ST_(?:MakePoint|Point)\b' "${X[@]}" -g '!**/{test,tests,__tests__,spec,e2e}/**' "${ROOTS[@]}" | "${NC[@]}"; st 8d "${PIPESTATUS[0]}"

# 9. GE-2 axis order at a boundary: lat-first into lon-first APIs (PostGIS points, GeoJSON coordinates, Mongo 2dsphere).
rg -n --pcre2 '(?i)\bST_(?:MakePoint|Point)\(\s*[\w.$\{]*\blat|\bcoordinates\s*:\s*\[\s*[\w.]*\b(?:lat|latitude)\w*|\[\s*[\w.]*\b(?:lat|latitude)\w*\s*,\s*[\w.]*\b(?:lng|lon|longitude)\w*\s*\]' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 9 "${PIPESTATUS[0]}"

# 10. GE-3 wrap-around: longitude range tests and BETWEEN, bbox corners, bearing arithmetic.
rg -n --pcre2 '(?:\b\w*(?:lng|lon|Lng|Lon|longitude|Longitude)\w*)\s*>=?\s*[\w.]*(?i:min|west|left|sw)\w*[^\n]{0,80}(?:&&|\band\b)[^\n]{0,80}(?:lng|lon|Lng|Lon|longitude)\w*\s*<=?|(?i)\b(?:lng|lon|longitude)\w*\s+between\b|\bbearing\w*\s*[-+]=' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 10 "${PIPESTATUS[0]}"
echo "# pre-flight exit $RC"; [ "$RC" -eq 0 ]
```

A finding is a hit **plus** a read of the algorithm **plus** every path that feeds it **plus** the
contract's other end (the sort, the constraint, the convention). Two blind spots are structural:

- **Sortedness and uniqueness live elsewhere.** The search or the `Map` is in one file and the sort,
  the `GROUP BY` or the unique constraint in another — or in a migration. Follow the collection to
  its query; read the migration for the constraint (database `schema-integrity-scan`, when
  installed, prints them).
- **Coordinates hide behind names.** `pos[0]`, `point.x`, `geo.a` defeat identifier greps; when grep
  0b shows a geo library or a spatial column, read every call into it, not only the hits.

**Measured** (2026-10-19, read-only, about 2 s) on a real NestJS 11 + MikroORM 6 + React monorepo,
`ROOTS=(apps/api/src apps/web/src packages/contracts/src)`, 6,930 TS files: 3a returns 152 `Map`
indexes keyed by a field other than an id (by key: `key` 36, `orderId` 21, `userId` 14, `productId`
9, then a long tail) — the OC-3 read list, closed group by group with the constraint or the query's
`GROUP BY` cited; one read in the eval found a phone-key index backed by a tenant-scoped unique
constraint (§ 20); 3b counts 99 files of id-keyed indexes (context, § 2); 4 returns one text-trim
loop (`while (start < end && …)`, not a search); 6b returns the two `Math.random()` calls that build a
client draft id and a tracking id (§ 21; two more are comments explaining the switch to
`crypto.randomInt`, dropped by the comment filter); every other grep returns 0 — no binary search,
unstable sort, shuffle, draw, hash bucket, geo library, spatial column or coordinate math. On the 28
`benchmarks/fixtures`, 6b lists 7 backoff-jitter and id-suffix calls in 4 fixtures (§ 21), 3a two
indexes keyed by a `GROUP BY` column and a slug, 3b two, 0a one; nothing else. On `algo-defects` (2026-10-19, staged
without its key; TS, Python, Go, Java, PostGIS; 0.3 s; no `rg` exit 2) all 20 of its seeds print:
1a 2, 2 3 (two seeds and the decoy with a total tie-break on a unique id, § 19), 3a 2 (a seed and the
decoy keyed by a tenant-scoped unique phone key, § 20), 3c 1, 4 2, 5 2, 6a 2, 6b 5 (the seeds, the
`crypto.randomInt` decoy's comment, a routed OTP, a per-call `new Random()`), 7 2, 8a 1, 8d 2, 9 2,
10 2, 0b 2 (the PostGIS extension and a `geometry(Point, 4326)` column). **GE has no real-repo
measurement**: no geo repo is in the allowed set, so the GE lane is fixture-measured only.

## The 3,000-hit path

1. **Group by contract, not by line.** OC-3 hits group by key field and source query; OC-1 by the
   collection searched; RD by generator; GE by the library or column.
2. **Close a group with one citation.** A key backed by a unique constraint in the same scope (§ 20),
   a `GROUP BY` on the key, an id-keyed index of one query's rows (§ 2), a `Math.random()` used for
   jitter or keys (§ 21), a Leaflet call (§ 24): cite it once in the coverage block.
3. **Read the top 20 groups fully**, ranked by what the result decides (money, eligibility,
   delivery, persisted rows first).
4. **Prefer the oracle at scale.** One differential property test over a module (V599, V601) settles
   every search or index it calls.
5. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the grep that continues them.

## Scans for

| § | Class | CWE | Default severity |
|---|---|---|---|
| 1 | OC-1 sorted-input precondition violated | CWE-697, CWE-193 | medium (high on persisted data) |
| 2 | OC-2 stability assumed from an unstable sort | CWE-697 | medium |
| 3 | OC-3 index or ordered container whose key collapses distinct elements | CWE-697 | high when a row is lost or misattributed; else medium |
| 4 | OC-4 hand-rolled search, sort, heap, LRU or geometry predicate with a boundary defect | CWE-193, CWE-835 | medium |
| 5 | RD-1 biased shuffle | CWE-330 | high for draws, raffles and assignment fairness; low for demo data |
| 6 | RD-2 range, bias and weight errors in a draw | CWE-330 | medium |
| 7 | RD-3 bucketing by a signed, salted or n-dependent hash | CWE-330, CWE-190 | medium (high when it decides price or eligibility) |
| 8 | GE-1 planar or unit-wrong distance on geographic coordinates | CWE-682 | high |
| 9 | GE-2 axis order swapped at a boundary | CWE-682 | high |
| 10 | GE-3 wrap-around (antimeridian, longitude and bearing normalisation, poles) | CWE-682 | medium |

### 1. Sorted-input precondition (OC-1)

```
BAD:   const i = _.sortedIndex(prices, p);           // prices built by Object.values(map): insertion order
       for k, g in itertools.groupby(rows, key=day)  # rows ordered by id, not by day: one day → many groups
GOOD:  prices.sort((a, b) => a - b) on the same path (or keep it sorted on insert) · groupby(sorted(rows, key=day), key=day)
```
**Read the code:** Is the input sorted by the same key, direction and collation on **every** path to
here (a database `ORDER BY name` under a locale collation vs a code-point compare)? Is a merge or an
adjacent dedupe (1b) fed two cursors in the same order? A constant table asserted sorted is § 34.
**Finding when** one reachable path delivers input out of the assumed order. **Proof:** V599.

### 2. Stability assumed from an unstable sort (OC-2)

```
BAD:   sort.Slice(rows, byScore)  // then rows[0] "wins" ties; or a second pass that expects the first order kept
       list.Sort((a, b) => a.Rank.CompareTo(b.Rank)) followed by paging in memory
GOOD:  sort.SliceStable · slices.SortStableFunc · OrderBy(r => r.Rank).ThenBy(r => r.Id) · an explicit total tie-break
```
**Read the code:** Are the keys unique (§ 19)? Is tie order observable — a "first wins", a two-pass
sort, in-memory paging, a rendered list users compare? Is the runtime's sort stable (§ 18)? **Finding
when** equal keys occur and their order changes a visible result. **Proof:** V600.

### 3. Key collapse in an index or ordered container (OC-3)

```
BAD:   const byOrder = new Map(lines.map((l) => [l.orderId, l]));     // two lines per order: the first is lost
       new TreeSet<>(Comparator.comparing(Item::price))               // two items at one price: one is dropped
       Collectors.toMap(X::name, x -> x)                              // throws on a duplicate name
GOOD:  Map.groupBy(lines, l => l.orderId) · a comparator that ties only equal elements (thenComparing(Item::id))
       a unique constraint in the same scope, cited · toMap with a merge function that is a decision, not a guess
```
**Read the code:** Is the key unique — a unique constraint on the same columns in the same tenant
scope (§ 20), a `GROUP BY` on the key, a validator? Are the rows from one query or concatenated from
two sources? Does a `TreeSet`/`SortedSet` comparator agree with equality (`BigDecimal` 2.0 vs 2.00)?
**Finding when** two distinct records can share the key and one is dropped, overwritten or throws.
**Proof:** V601 (or the two-ended static fact: no constraint, a path that writes duplicates).

### 4. Hand-rolled primitive with a boundary defect (OC-4)

```
BAD:   while (lo < hi) { const mid = (lo + hi) >> 1; if (a[mid] < x) lo = mid; else hi = mid; }   // never shrinks: lo = mid
GOOD:  the stdlib primitive (bisect, sort.Search, Arrays.binarySearch, a heap module), or a differential test against it
```
**Read the code:** Does a primitive exist in the language or a dependency already in the lockfile?
Does the interval strictly shrink? Are the heap's child indexes `2i+1`/`2i+2`? Does a ray-casting
polygon test handle vertices and horizontal edges? A text trim loop is not a search. **Proof:** V602.

### 5. Biased shuffle (RD-1)

```
BAD:   items.sort(() => Math.random() - 0.5)   · for (i…) swap(a, i, rand(0, n − 1))   · j drawn from [0, i) (Sattolo: no fixed points)
GOOD:  lodash.shuffle · random.shuffle · Collections.shuffle · rand.Shuffle · Fisher–Yates with j in [0, i]
```
**Read the code:** What does the order decide — a raffle, an assignment, a "random" featured product,
an A/B arm, or demo data (§ 22)? Is the generator also a security question (a prize: CWE-338 →
security)? **Finding when** the order decides something fairness or money depends on. **Proof:** V603.

### 6. Range, bias and weight errors in a draw (RD-2)

```
BAD:   Math.floor(Math.random() * (max - min)) + min      // max never drawn
       Math.round(Math.random() * n)                      // 0 and n at half weight
       randomBytes(1)[0] % 6 · rand() % n                  // modulo bias · (int)(r.nextDouble() * n) · new Random() per call
GOOD:  crypto.randomInt(min, max + 1) (bounds stated) · random.randrange / randint with the inclusive end stated · rejection sampling
       random.choices(population, weights=w) · one generator per process
```
**Read the code:** Is the range inclusive or exclusive in the spec, and does the expression match?
Are weights normalised and non-zero? Is the generator re-seeded per call? `Math.random()` for jitter,
keys or draft ids is § 21. **Finding when** a reachable value is impossible or over- or under-weighted
in a draw users see. **Proof:** V604.

### 7. Bucketing by a signed, salted or n-dependent hash (RD-3)

```
BAD:   Math.abs(key.hashCode()) % 100   // MIN_VALUE stays negative · hash(user_id) % 100  # salted: buckets move on restart
       variant = hash(user) % variants.length   // adding a variant reassigns most users
GOOD:  Math.floorMod(h, n) on a stable unsigned hash (murmur, xxhash, SHA-256 prefix) · rendezvous or consistent hashing when n changes
```
**Read the code:** Is the assignment supposed to stick (an experiment, a shard, a sticky price)? Is
the hash stable across processes and releases? Can it be negative? **Finding when** a reachable key
lands outside `[0, n)`, moves between processes, or most keys move when n changes. **Proof:** V604.

### 8. Planar or unit-wrong distance (GE-1)

```
BAD:   Math.sqrt((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2) * 111    // a degree of longitude shrinks with cos(lat)
       Math.sin(lat1)                                               // degrees into trig
       ST_DWithin(geom, point, 5000) on geometry(Point, 4326)       // 5,000 DEGREES
GOOD:  haversine with radians and one earth radius in metres · ST_DWithin(geom::geography, point::geography, 5000)
```
**Read the code:** Which unit is each value in (degrees, radians, metres, km, miles)? What is the
column type and SRID (grep 0b reads migrations)? Is the distance a UX estimate (§ 26) or a decision
(a delivery radius, a fee band)? **Finding when** the formula or the unit is wrong for the surface
the data lies on. **Proof:** V605.

### 9. Axis order swapped at a boundary (GE-2)

```
BAD:   ST_MakePoint(lat, lng) · { type: 'Point', coordinates: [lat, lng] } · Mongo 2dsphere fed [lat, lng]
GOOD:  ST_MakePoint(lng, lat) · coordinates: [lng, lat] (RFC 7946 § 3.1.1) · a boundary validator |lat| ≤ 90
```
**Read the code:** Which convention does each library on the path expect (GeoJSON, PostGIS, Mapbox
and Mongo are lon-first; Google and Leaflet are lat-first, § 24)? Where is the mapping between them?
**Finding when** one hop passes the other convention's order. **Proof:** V606.

### 10. Wrap-around (GE-3)

```
BAD:   p.lng >= box.minLng && p.lng <= box.maxLng       // a box across ±180 has east < west: matches nothing
GOOD:  split the box at the antimeridian, or test (lng >= west || lng <= east) when east < west; normalise to [−180, 180)
```
**Read the code:** Can the service area cross ±180° or reach a pole (§ 35)? Are bearings normalised
to [0, 360)? **Proof:** V607.

## Output

```
algorithm-contract-scan — lanes: ts; spotbugs, error prone, staticcheck absent → NOT-RUN; no geo library, no spatial column (0b)

Findings: 1 · Unconfirmed: 1

1. src/orders/fulfilment-board.service.ts:58                      [report-with-fix]   high
   §3 key collapse — new Map(lines.map(l => [l.orderId, l])) over order LINES; an order with two
   lines keeps the last one, so the board under-counts picks. No unique constraint on order_lines
   (order_id) — two lines per order are normal (migrations/0007_order_lines.sql:12). Reached by
   GET /fulfilment/board. Proof: test/fulfilment/board.collapse.spec.ts — 2 lines in, 1 out (fails).
   Fix: Map.groupBy(lines, l => l.orderId) and sum per group.

2. src/experiments/bucketing.py:21                                    [report-flagged]    medium
   §7 salted bucket — hash(user_id) % 100 decides the experiment arm; CPython salts str hashes per
   process, so arms move on every restart. Unproven link: whether PYTHONHASHSEED is pinned in the
   deploy (not in the repo). Settling test (V604): two processes with different PYTHONHASHSEED.

Verification: 6 candidates → 1 finding · 1 unconfirmed · 3 hardening · 1 refuted

Class coverage:
  §1  sorted-input precondition    checked (0 hits)
  §2  unstable sort                N/A (no Go, .NET, Rust, C++ or PHP files)
  §3  key collapse                 checked (152 hits / 31 key groups: 29 closed by a constraint or GROUP BY, 2 read → 1 finding)
  §4  hand-rolled primitive        checked (1 hit → 0: a text trim loop)
  §5  biased shuffle               checked (0 hits)
  §6  draw range and bias          checked (2 hits → 0: client ids, § 21)
  §7  hash bucketing               checked (1 hit → 1 unconfirmed)
  §8  geodesic distance            N/A (no geo library, spatial column or coordinate math: 0b, 8a–8d all 0)
  §9  axis order                   N/A (same)
  §10 wrap-around                  N/A (same)
```

`[report-with-fix]`: both ends of the contract are cited, the entry point is traced, the
differential, distribution or reference test failed, and the fix uses the language's primitive.
`[report-flagged]`: one link is unproven (a deploy setting, a path not read, a library version), and
the row names it and the settling test. The coverage block lists **all ten** classes on every run:
`checked (k → m)` only when the grep ran on a present lane; `N/A (<reason>)` only when the repo has no
such surface (cite 0b for GE); `blocked (<reason>)` when a grep exited 2. A partial review reads
`Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/algorithms.md`](../../../../snippets/precedents/algorithms.md)
(§ 18–§ 28, § 34–§ 35 for this skill) and
[`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones met most: a
stable runtime sort (§ 18) or unique keys (§ 19); a key backed by a unique constraint in the same
scope (§ 20); `Math.random()` for jitter, keys or draft ids (§ 21); demo-data shuffles (§ 22);
`crypto.randomInt` and unsigned hashes (§ 23); Leaflet's `[lat, lng]` (§ 24); a `::geography` cast
(§ 25); haversine for UX distances (§ 26); `.sort()` on machine keys (§ 28, code-quality's anyway).

## When to run

- On any diff that adds or changes a binary search, `groupby`, merge or adjacent dedupe; a sort whose
  ties matter; a `Map`/dict/`toMap`/`keyBy` index or a sorted container; a shuffle, draw, weighted
  pick or hash bucket; any coordinate, distance, bounding box or spatial query — the
  `/analyze-complexity` dispatch signal.
- On every whole-repo `/analyze-complexity`, reporting all ten classes.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed
  it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 1–§ 8. Under
  `/analyze-complexity` that is `@algorithm-designer` in refute mode plus `@verifier`; run standalone,
  apply the protocol as a separate second pass and tag those rows `self-verified`. Never drop them.
- Halt when any `rg` exits 2: the class it feeds is `blocked`, never `checked`.
- Halt on any finding without the site `<file:line>`, both ends of the contract, the entry point and
  the fix.
- Do not mark a row `[report-with-fix]` without a differential, distribution or reference test that
  failed first, or the two-ended static fact for a static class.
- Do not propose "sort it again just in case", a retry, or a larger tolerance as the fix; restore the
  contract at its source (one sort on the path, a stable sort or a tie-break, grouping, a vetted
  generator, a geodesic formula).
- Do not print "no contract defect" without the class-coverage block. Do not grade a comparator
  expression, a database sort key or a predictable secret (§ Boundaries).

## Related

- `/analyze-complexity` dispatches this skill with `complexity-scan` and `numeric-stability-scan`;
  `/design-algorithm --from-audit` closes its findings failing-first with the project's property
  harness (testing `property-invariants`, when installed, supplies the frameworks).
- `correctness-smell-scan` §2/§4/§6 (code-quality pack, when installed) owns the comparator, equality
  and date expressions; `query-shape-scan` and `schema-integrity-scan` (database pack, when installed)
  own database sort keys and the unique constraints this skill cites; `sast-scan` (security pack, when
  installed) owns predictable randomness.
- `rules/algorithm-principles.md` — "use the proven primitive", which §4 enforces.
