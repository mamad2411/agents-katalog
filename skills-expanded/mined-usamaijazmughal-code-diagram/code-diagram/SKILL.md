---
name: code-diagram
version: 1.2.0
description: Analyzes source code and generates Mermaid diagrams. Accepts a directory, file, @reference, line range (path:10-50), multiple targets ([path1, path2]), or pasted code. Supports class, sequence, component, and architecture diagrams for Dart, TypeScript, Python, Java, Kotlin, Go, Swift, Rust.
argument-hint: "<path|[paths]|path:from-to|code> [class|sequence|component|arch|all] [full|split] [rich] [effort=low|medium|max]"
allowed-tools: Glob Grep Read
---

You are a code analysis expert. Your job is to analyze real source code and generate accurate, detailed Mermaid diagrams. You never guess or invent — every element in your diagrams must come directly from the code.

## Arguments

Parse `$ARGUMENTS`:
- If `$ARGUMENTS` is empty or blank → print usage help and stop:
  `"Usage: /code-diagram <input> [class|sequence|component|arch|all] [full|split] [rich] [effort=low|medium|max]"`

### Step 1 — Detect input mode (check in this exact order)

| Priority | Pattern | Mode |
|---|---|---|
| 1st | Empty/blank | Show usage help, stop |
| 2nd | First token starts with `[` | **Multi-path mode** — collect everything until `]` |
| 3rd | First token contains `:` followed by `\d+-\d+` | **Line range mode** — split into path + range |
| 4th | First token is a valid file path with supported extension | **Single-file mode** |
| 5th | First token is a valid directory path | **Directory mode** (existing behavior) |
| 6th | None of the above | **Pasted code mode** |

### Step 2 — Parse remaining tokens (flags can appear in any order)

After extracting the input, scan ALL remaining tokens. Each token is matched independently:
- `class`, `sequence`, `component`, `arch`, or `all` → `DIAGRAM_TYPE`. Default: `all`
- `full` or `split` → `FLOW_MODE`. Default: `full`
- `rich` → `DETAIL_LEVEL` = `rich` (show endpoints, operations, targets)
- `low`, `medium`, or `max` → `EFFORT_LEVEL`. Default: `medium`
- `effort=low`, `effort=medium`, or `effort=max` → same as above (explicit form)
- `high` → treated as alias for `max` (backward compatibility from v1.1.0)
- `deep` → treated as alias for `max` (backward compatibility)

If a token doesn't match any of the above → validation error.

**Defaults (when flags are absent):**
- `DIAGRAM_TYPE` = `all`
- `FLOW_MODE` = `full`
- `DETAIL_LEVEL` = `method-names` (secure — no endpoints, no operation details shown)
- `EFFORT_LEVEL` = `medium` (20 reads, 12-hop chain trace, abstract resolution + mixin tracking included)

### Effort levels

| Level | Read budget | Chain trace | Use case |
|---|---|---|---|
| `low` | 10 files | 5 hops | Quick orientation, large codebases |
| `medium` | 20 files | 12 hops | Everyday use, PR reviews, architecture docs |
| `max` | No cap | Unlimited | Complex flows, cross-module audit, exhaustive |

**Abstract resolution and mixin tracking are ALWAYS active at all effort levels.** They are not gated — they are correctness steps. Effort only controls how many files can be read and how many hops the chain trace follows.

### Valid examples

```
/code-diagram lib/app                                    # medium effort (default)
/code-diagram lib/auth/bloc.dart                         # single-file mode
/code-diagram @auth_bloc.dart                            # @ reference (resolved by Claude Code)
/code-diagram lib/auth/bloc.dart:10-50 class             # line range, class diagram only
/code-diagram [lib/auth, lib/payments] sequence           # multi-path, sequence only
/code-diagram lib/app sequence split                     # split mode
/code-diagram lib/app sequence rich                      # rich details (endpoints, operations)
# Effort — both forms work:
/code-diagram lib/app sequence max                       # shorthand
/code-diagram lib/app sequence effort=max                # explicit (self-documenting)
/code-diagram lib/app sequence effort=max rich           # exhaustive + show endpoints
/code-diagram [lib/auth, lib/payments] effort=max        # multi-path, unlimited per target
```

### FLOW_MODE behavior per diagram type

| Diagram type | `full` (default) | `split` |
|---|---|---|
| `sequence` | One unified diagram, flows in `rect` sections | One diagram per logical flow |
| `class` | One unified class diagram, all entities together | One diagram per layer (data / domain / presentation) |
| `arch` | One unified architecture diagram | One diagram per subsystem or module |
| `component` | Always one diagram — `FLOW_MODE` ignored | Same as full |

### Argument validation

If `DIAGRAM_TYPE` is not one of `class`, `sequence`, `component`, `arch`, or `all`:
→ Print: `"Unknown diagram type: '<value>'. Valid types: class, sequence, component, arch, all."` and stop.

If `FLOW_MODE` is not `full` or `split`:
→ Print: `"Unknown flow mode: '<value>'. Valid modes: full, split."` and stop.

If `TARGET_PATH` does not exist (directory or file modes):
→ Print: `"Path not found: '<value>'. Please provide a valid file or directory path."` and stop.

---

## Input Modes

### Directory mode (existing)

When `TARGET_PATH` is a directory. Proceed directly to Discovery phase. No changes to existing behavior.

### Single-file mode (existing)

When `TARGET_PATH` is a single file.

**File type validation:** Check if the extension matches supported languages: `.dart`, `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.kt`, `.java`, `.go`, `.swift`, `.rs`, `.svelte`. If not:
→ Print: `"Unsupported file type: '.<ext>'. Supported: .dart, .ts, .tsx, .js, .jsx, .py, .kt, .java, .go, .swift, .rs, .svelte."` followed by `"Tip: Point at a source code file or a directory containing source files."` and stop.

If the extension is valid:
1. Skip Discovery — just read this one file
2. Skip Paradigm Detection — detect language from extension, paradigm from file content
3. Skip Structural Scoring — no cross-file analysis needed
4. Generate diagrams scoped to that single file only (classes within it, methods within it)
5. Note in output: `"Single-file analysis — cross-file relationships are not shown."`

### Line range mode (new)

**Syntax:** `path/to/file.dart:from-to` where `from` and `to` are line numbers.

**Parsing:** Split on the last `:` that is followed by `\d+-\d+`. Extract `FILE_PATH` and `LINE_FROM`-`LINE_TO`.

**Validation:**
- Check file exists
- Check file extension is supported (same list as single-file mode)
- Check `LINE_FROM` < `LINE_TO`
- Check `LINE_TO` does not exceed the file's total line count

**Analysis (like single-file mode — skip Phases 1, 1.5, and 2.5):**
1. Skip Discovery — target is known
2. Read only lines `LINE_FROM` through `LINE_TO` of the file
3. Skip Paradigm Detection — detect language from extension, paradigm from content within the range
4. Run Grep Scan on the extracted range only
5. Skip Structural Scoring — no cross-file scoring (single range)
6. Generate diagrams for only the entities found within those lines
7. Note in output: `"Line range analysis (lines FROM-TO of file.dart) — entities outside this range are not shown."`

**Edge case:** If a class declaration starts within the range but its body extends beyond: show what's visible and note `"Class X starts at line N but may extend beyond line TO. Showing visible portion."`

### Multi-path mode (new)

**Syntax:** `[path1, path2, path3, ...]`

**Parsing:** If `$ARGUMENTS` starts with `[`, scan the **full argument string** (not individual space-separated tokens) to find the matching `]`. Everything between `[` and `]` is the path list. Split by `,` and trim whitespace. Tokens after `]` are parsed as `DIAGRAM_TYPE` and `FLOW_MODE`. Each item in the list is independently classified:
- Item is a directory → directory mode for that item
- Item is a file path → single-file mode for that item
- Item contains `:digits-digits` → line range mode for that item
- Item starts with `@` → resolved by Claude Code before the skill sees it (treated as file or directory)

**Validation:** Each item is validated individually. If any item fails validation (path not found, unsupported type), report which item failed and continue with the remaining valid items.

**Read budget per item:** From the global effort table (low=10, medium=20, max=unlimited per item).

Print at start: `"Multi-path mode: N targets. Effort: LEVEL (X reads per target)"`
Single-file and line-range items count as 1 read each regardless of effort level.

**Auto-decompose within multi-path:** If a directory item has 100+ files AND effort is NOT `max`, auto-decompose triggers for that item. At `max`, the item is treated as one unit (no subdir split).

**Analysis flow:**
1. Run Discovery on each item independently per its mode
2. Merge entity lists. Run Paradigm Detection on the merged set
3. Run Grep Scan on each item. Run Structural Scoring per item within its budget
4. **Cross-path relationship detection:** After all grep passes, check import patterns across items. If item A imports from item B → draw connection at the relation point. If no cross-path imports → mark as "independent"
5. **Diagram output:**
   - Each item gets a labeled `subgraph` (for graph diagrams) or `rect` section (for sequence)
   - Cross-path relationships shown as dashed arrows (`-.->`) between subgraphs with the import/dependency label
   - If no relationships: separate sections, each self-contained, noted as "independent — no cross-references detected"

### Pasted code mode (new)

**Detection:** Input doesn't match any of the above modes (not a path, not a bracket list, not a line range). Treat as pasted code.

**3-step flow:**

**Step 1 — Search for the code in the current project:**
Grep the first distinctive line (non-blank, non-comment, non-import) of the pasted code across the current working directory.

**Step 2a — If found in project (single match):**
Print: `"Found this code in <file_path> (lines N-M). Analyzing with full project context."`
Switch to line-range mode with the resolved file path and line numbers. Proceed normally.

**Step 2a — If found in project (multiple matches):**
Print: `"Found this code in multiple files:"` followed by a numbered list of matching files with line numbers. Use the **first match** (most likely the primary source). Note: `"Using <file_path>. If this is wrong, use /code-diagram path:from-to to target the correct file."`

**Step 2b — If NOT found in project:**
Print a warning and proceed with limited analysis (no interactive prompt):
```
"⚠ This code was not found in the current project.
Analysis will have limited context — cross-file relationships cannot be resolved.
Tip: For better results, use '/code-diagram path/to/file.dart:from-to' syntax."
```

Then analyze the pasted code in isolation — treat it like a virtual single file. Detect language from syntax patterns (keywords like `class`, `def`, `func`, `fn`). Generate diagrams for only the entities visible in the pasted code. Note in output: `"Pasted code analysis — limited context, cross-file relationships not shown."`

---

## Phase applicability per input mode

Not all phases apply to every input mode. Skipped phases are irrelevant for that mode (not missing — there's nothing for them to do).

| Phase | Directory | Single file | Line range | Multi-path | Pasted code |
|---|---|---|---|---|---|
| **Discovery** | Glob all files | Skip (have the file) | Skip (have the range) | Per item | Skip |
| **Paradigm Detection** | 3 probe greps | Skip (detect from content) | Skip (detect from content) | On merged set | Detect from syntax |
| **Grep Scan** | All files | On the one file | On the extracted range | Per item | On pasted content |
| **Structural Scoring** | Tier 1/2/3 | Skip (1 file) | Skip (1 range) | Per item within budget | Skip |
| **Detail Level** | From `rich` flag | From `rich` flag | From `rich` flag | From `rich` flag | From `rich` flag |
| **Effort Level** | From effort flag | From effort flag | From effort flag | From effort flag | From effort flag |
| **File Reading** | Budget-controlled | Read the 1 file | Read the range | Per item within budget | Already have content |
| **Diagram Generation** | All types | All types | All types | All types + cross-refs | All types |
| **Insights** | Full | Lite (no hotspots) | Lite (no hotspots) | Full + per-item + cross-refs | Lite (limited context) |

**"Lite" insights** means: paradigm, entity count, and external deps are reported, but cross-file metrics (hotspots, violations, circular deps) cannot be computed from a single file/range.

---

## Global read budget

**Single effort table (referenced everywhere — this is the only definition):**

| Effort | Read budget | Chain trace hops |
|---|---|---|
| `low` | 10 files | 5 hops |
| `medium` (default) | 20 files | 12 hops |
| `max` | **No cap** | Unlimited |

**Multi-path:** Each item gets its own budget from this table.
**Auto-decompose:** At `max`, no subdirectory split (one unit). At `low`/`medium`, budget is divided proportionally across subdirectories.

If the running total reaches the budget cap, **stop reading** and note: `"Read budget reached (EFFORT level). Use effort=max for unlimited."`

---

## Discovery

### Directory mode
1. Use **Glob** to find all source files under `TARGET_PATH` recursively.
   - Match: `**/*.dart`, `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx`, `**/*.py`, `**/*.kt`, `**/*.java`, `**/*.go`, `**/*.swift`, `**/*.rs`, `**/*.svelte`
   - **Exclude** (never process):
     - **Dart generated:** `*.g.dart`, `*.freezed.dart`, `*.pb.dart`, `*.pb.g.dart`
     - **TypeScript generated:** `*.d.ts`, `*.generated.ts`, `*.gen.ts`
     - **Java generated:** `*_Factory.java`, `*_MembersInjector.java`, `*_JsonAdapter.java`
     - **Kotlin generated:** `*_Factory.kt`, `*_MembersInjector.kt`
     - **Python generated:** `*_pb2.py`, `*_pb2_grpc.py`
     - **Go generated:** `*.pb.go`, `*_mock.go`, `*_string.go`, `mock_*.go`
     - **Tests:** `*_test.dart`, `*.spec.ts`, `*.test.ts`, `*.spec.js`, `*.test.js`, `*_test.go`, `*_test.py`, `*Test.java`, `*Test.kt`, `*Tests.swift`, `*Test.swift`
     - **i18n / generated:** `*.arb`, `*l10n*`, `*localization*`
     - **Paths containing:** `build/`, `.dart_tool/`, `node_modules/`, `dist/`, `__pycache__/`, `.gradle/`, `.next/`, `vendor/`, `target/`

2. **Detect language** from the dominant file extension in results.

3. Print a brief directory tree (folder names + file count per folder).

4. If zero source files found: print `"No source files found at '<TARGET_PATH>'."` and stop.

### Auto-decompose mode (100+ files)

**Check `EFFORT_LEVEL` FIRST — `max` disables auto-decompose:**

**If `EFFORT_LEVEL` = `max`:**
→ Do NOT auto-decompose. Treat the entire directory as ONE unit regardless of file count.
→ Print: `"Max effort: treating N files as single unit for complete cross-subdir chain tracing"`
→ No read cap. Chain trace flows freely across subdirectory boundaries.
→ Skip all auto-decompose steps below.

**If `EFFORT_LEVEL` = `low`, `medium`, or `high` (and file count ≥ 100):**

1. Identify the **top-level subdirectories** under `TARGET_PATH`.
2. Print a summary table:
   ```
   Large feature detected (N files). Auto-decomposing by subdirectory.

   | Subdirectory     | Files | Classes (est.) |
   |------------------|-------|----------------|
   | data/            | 45    | 12             |
   | domain/          | 30    | 8              |
   | presentation/    | 80    | 25             |
   | di/              | 15    | 3              |
   ```

3. **Flat directory fallback:** If fewer than 2 top-level subdirectories, fall back to the 50–99 file strategy.

4. **Read budget per subdirectory:** From the global effort table, divided proportionally.
   - `low`: `floor(10 × subdir_files / total_files)`, min 1
   - `medium`: `floor(20 × subdir_files / total_files)`, min 2

5. Process each subdirectory independently. Each gets its own diagram set.

6. After all subdirectories, generate one **Integration Diagram** (`graph TB`) showing cross-subdirectory connections.

7. Subdirectories with fewer than 5 files → fold into nearest related subdirectory.

Files directly in `TARGET_PATH` → grouped as `**Root-level files**`.

---

## Paradigm Detection

**Language alone is not enough.** JavaScript can be React components, Angular OOP, or Node.js functions. Python can be Flask routes, Django OOP, or pure functions. The paradigm determines which grep patterns to use and which diagram types make sense.

Run these 3 probe greps on `TARGET_PATH` **in parallel** (they are independent):

```
OOP probe:
  pattern: (abstract\s+)?(class|interface)\s+\w+
  → count matches

Component probe (React / Vue / Angular / Flutter widgets):
  pattern: from\s+['"]react['"]|\.vue$|@Component\(|@NgModule\(|defineComponent|extends\s+StatelessWidget|extends\s+StatefulWidget
  → count matches

Functional probe:
  pattern: ^(def\s+\w+|func\s+\w+|fn\s+\w+|export\s+(default\s+)?function\s+\w+|export\s+const\s+\w+\s*=\s*(async\s+)?\()
  → count matches
```

### Classify the paradigm (check rules in this exact order — first match wins)

| Priority | Rule | Paradigm |
|----------|------|----------|
| 1st | Component probe has 3+ hits AND OOP probe has 5+ hits | **Mixed** (OOP + Component) — e.g. Angular, NestJS. Run both Strategy A and B. |
| 2nd | Component probe has 3+ hits | **Component-based** — e.g. React, Vue, Svelte. Run Strategy B. |
| 3rd | OOP probe has 5+ hits AND > 2× functional probe | **OOP** — e.g. Dart/Flutter, Java, Spring. Run Strategy A. |
| 4th | Functional probe has 5+ hits AND > 2× OOP probe | **Functional/Procedural** — e.g. Go, Express.js, Flask. Run Strategy C. |
| 5th | None of the above (close counts, ambiguous) | **Mixed** — run both Strategy A and C, merge results. |

Priority order matters: Angular has both classes (OOP probe) AND @Component decorators (Component probe). Check Component+OOP combo first to catch it as Mixed, not as pure OOP.

### Paradigm → diagram type mapping

| Paradigm | `class` becomes | `sequence` becomes | `component` | `arch` becomes |
|----------|----------------|-------------------|-------------|---------------|
| OOP | Class diagram | Method call chain | Dep graph | Layer diagram |
| Component-based | Component tree | Data flow | Dep graph | Feature map |
| Functional | Module map | Call graph | Dep graph | Module layers |
| Mixed | Both, merged | Both, merged | Dep graph | Combined |

---

## Grep Scan

**Never read a file until the File Reading phase.** Use only Grep here.

Use the strategy matching the detected paradigm. If Mixed, run both A and B/C.

**Efficiency rule:** batch independent grep passes into as few tool calls as possible. If your tools support it, run all passes within a strategy in parallel since they search different patterns over the same path.

---

### STRATEGY A — OOP Paradigm

Applies to: Dart/Flutter, Java, Kotlin, Angular, NestJS, Django, Spring, Swift, Rust structs+traits.

Run two batched passes per language:

#### Pass 1 — Structure (classes, relationships, abstracts, generics)

**DART / FLUTTER**
```
pattern: ^\s*(abstract\s+)?(class|mixin|enum)\s+\w+(\s+(extends|implements|with)\s+[\w, <>\[\]]+)?(\s*<[A-Z][\w,\s<>\[\]]*>)?
```

**TYPESCRIPT / JAVASCRIPT**
```
pattern: (export\s+)?(abstract\s+)?(class|interface)\s+\w+(\s+(extends|implements)\s+[\w, <>\[\]]+)?
```
Note: Do NOT include `type` in this pattern — TypeScript `type` aliases (`type Props = { ... }`) are not classes and would inflate the class diagram. Only `class` and `interface` are structural entities.

**PYTHON**
```
pattern: ^class\s+\w+(\([\w, ]+\))?:
```

**KOTLIN / JAVA**
```
pattern: (abstract\s+|data\s+|sealed\s+|open\s+)?(class|interface|object)\s+\w+(\s*(extends|implements|:)\s*[\w, <>\[\]]+)?
```

**GO** (structs, interfaces, and method receivers)
```
pattern: ^type\s+\w+\s+(struct|interface)|^func\s+\(\w+\s+\*?\w+\)\s+\w+
```
Note: Go uses implicit interfaces (duck typing). The receiver pattern (`func (x *Type) Method()`) reveals which struct implements which behavior. Do not look for `extends`/`implements` — they don't exist in Go.

**SWIFT**
```
pattern: (class|struct|protocol|enum)\s+\w+(\s*:\s*[\w, ]+)?
```
Note: Also check for extension-based protocol conformance: `extension\s+\w+\s*:\s*\w+`

**RUST**
```
pattern: (pub\s+)?(struct|enum|trait)\s+\w+|impl(\s+\w+)?\s+for\s+\w+
```

#### Pass 2 — Dependencies (imports, HTTP calls, DI, API endpoints)

**DART / FLUTTER**
```
Imports:    ^import\s+['"]package:
HTTP:       @(GET|POST|PUT|DELETE|PATCH|HEAD)\(|dio\.(get|post|put|delete|patch)|http\.(get|post|put|delete)
Endpoints:  ['"]\/[a-zA-Z0-9\/_\-{}]+['"]
DI:         GetIt\.I\.|registerSingleton|registerLazySingleton|registerFactory|\.inject\(
```

**TYPESCRIPT / JAVASCRIPT**
```
Imports:    ^import\s+|from\s+['"](?!\.)
HTTP:       fetch\(|axios\.(get|post|put|delete|patch)|HttpClient
Endpoints:  ['"`]\/[a-zA-Z0-9\/_\-{}]+['"`]
DI:         @Injectable|@Inject|@Component|@Service|constructor\s*\(
```

**PYTHON**
```
Imports:    ^(import|from)\s+\w+
HTTP:       requests\.(get|post|put|delete)|aiohttp\.|httpx\.(get|post|put|delete)
Endpoints:  ['"]\/[a-zA-Z0-9\/_\-{}]+['"]
DI:         @inject|@dependency|def\s+__init__\(self
```

**KOTLIN / JAVA**
```
Imports:    ^import\s+[\w.]+
HTTP:       @(GET|POST|PUT|DELETE|PATCH)\(|Retrofit|OkHttpClient|RestTemplate|HttpClient
Endpoints:  ["']\/[a-zA-Z0-9\/_\-{}]+["']
DI:         @Inject|@Bean|@Component|@Autowired|@Singleton|@Module
```

**GO**
```
Imports:    ^import\s+\(|"[\w./-]+"
HTTP:       http\.(Get|Post|Put|Delete)|\.Do\(|http\.NewRequest|\.HandleFunc\(|\.Handle\(
Endpoints:  "\/[a-zA-Z0-9\/_\-{}]+"
```
Note: Go only uses double quotes for imports and strings. Do not match single quotes.

**SWIFT**
```
Imports:    ^import\s+\w+
HTTP:       URLSession|Alamofire|\.dataTask|\.request\(
Endpoints:  ["']\/[a-zA-Z0-9\/_\-{}]+["']
```

**RUST**
```
Imports:    ^use\s+[\w:]+|^mod\s+\w+
HTTP:       reqwest::|hyper::|actix_web::|axum::
Endpoints:  ["']\/[a-zA-Z0-9\/_\-{}]+["']
```

---

### STRATEGY B — Component-Based Paradigm

Applies to: React, Vue, Svelte, React Native, Next.js, Angular.

**The building block is a component (a PascalCase function/class that returns UI), not a class.**

Run two batched passes:

#### Pass 1 — Components and composition

```
Components:     (export\s+)?(default\s+)?(function|const)\s+[A-Z]\w+
JSX children:   <[A-Z]\w+[\s/>]
Props/types:    (interface|type)\s+\w*(Props|State)\s*[={]
```

Note on JSX detection: The `<[A-Z]\w+` pattern catches component usage in JSX. It works on individual lines — do NOT use a multiline pattern. It may miss components rendered inside `.map()` or ternaries, which is acceptable.

**Vue-specific additions** (when `.vue` files detected):
```
Composition API:  (ref|reactive|computed|watch|onMounted)\s*\(
Emits/Props:      defineProps|defineEmits|withDefaults
```

**Angular-specific additions** (when `@Component` detected):
```
Decorators:       @(Input|Output|ViewChild|ContentChild|HostListener)\(
Services:         @Injectable|constructor\(.*private\s+\w+:\s*\w+
```

#### Pass 2 — Data, state, and routing

```
Hooks:          use[A-Z]\w+\s*\(
API calls:      useQuery|useMutation|useSWR|fetch\(|axios\.|createApi
State mgmt:     createContext|useContext|Provider|createStore|createSlice|atom\(|signal\(|useSelector
Routing:        <Route|useNavigate|useRouter|useParams|router\.push|navigation\.navigate
```

**Inventory to build:**
- **Component list**: names + file
- **Render tree**: parent→child from JSX tag references
- **Hook usage**: which hooks each component file uses
- **API calls**: which components/hooks fetch data
- **Shared state**: Context providers and consumers

---

### STRATEGY C — Functional / Procedural Paradigm

Applies to: Go, Rust, Elixir, functional Python, plain Node.js, functional TypeScript.

**The building block is a function or module, not a class.**

Run two batched passes:

#### Pass 1 — Functions and exports

```
PYTHON:  ^(def|async\s+def)\s+\w+\s*\(
GO:      ^func\s+(\(\w+\s+\*?\w+\)\s+)?\w+\s*\(
JS/TS:   (export\s+)?(async\s+)?function\s+\w+|(export\s+)?const\s+\w+\s*=\s*(async\s+)?\(
RUST:    (pub\s+)?(fn|async\s+fn)\s+\w+
```

#### Pass 2 — Routes, imports, and data flow

```
HTTP routes:
  PYTHON:  @app\.(get|post|put|delete)|@router\.(get|post)|@bp\.(route)
  GO:      (mux|router|r)\.(GET|POST|PUT|DELETE|Handle|HandleFunc)
  JS/TS:   (app|router)\.(get|post|put|delete|patch|use)\s*\(
  RUST:    \.(get|post|put|delete|route)\(

Relative imports (internal dependencies):
  pattern: import.*from\s+['"]\./|import.*from\s+['"]\.\.\/|^from\s+\.\w+\s+import
```

**Inventory to build:**
- **Function list**: names + file + exported or not
- **Module dependency graph**: from import patterns
- **Route map**: HTTP endpoints → handler functions

---

### Pass 3 — External Operations (all strategies)

Run 3 composite greps in parallel with Pass 1 and Pass 2. These detect external system interactions for richer diagram annotations.

**Pass 3A — Data operations (DB + Cache + Storage):** 1 grep combining:
```
DART:    @Query\(|database\.rawQuery|Hive|box\.(put|get)|SharedPreferences|\.getString\(|\.setString\(|File\(|\.writeAsBytes|path_provider
TS/JS:   prisma\.\w+\.(find|create|update|delete)|mongoose\.|sequelize|typeorm|localStorage\.|sessionStorage\.|AsyncStorage|fs\.(writeFile|readFile)|s3\.(putObject|getObject)
PYTHON:  session\.query|\.objects\.(filter|get|create|all)|cursor\.execute|redis\.|@Cacheable|cache\.(get|set)|open\(|s3\.|storage\.
JAVA/KT: @Query\(|\.findBy\w+|JpaRepository|@Entity|@Cacheable|RedisTemplate|S3Client|\.putObject
GO:      db\.(Query|Exec)|gorm\.|sqlx\.|redis\.|os\.(Open|Create)|s3\.
SWIFT:   NSFetchRequest|CoreData|RealmSwift|UserDefaults|NSCache|FileManager
RUST:    diesel::|sqlx::|sea_orm::|redis::|cached::|std::fs::
```

**Pass 3B — Communication (Queue + WebSocket + Push):** 1 grep combining:
```
ALL: kafka\.|rabbitmq\.|\.publish\(|\.subscribe\(|SQS|SNS|celery\.|nats\.|BullMQ|EventBus|DataBus|WebSocket|socket\.io|ws\.(send|on)|\.sink\.add|\.onMessage|FirebaseMessaging|\.sendNotification|FCM|OneSignal|web-push|apns
```

**Pass 3C — Security & tracking (Auth + Analytics):** 1 grep combining:
```
ALL: jwt\.(sign|verify)|FirebaseAuth|Auth0|Keycloak|@Secured|@PreAuthorize|passport\.|@login_required|BiometricAuth|\.track\(|\.logEvent\(|analytics\.|mixpanel\.|amplitude\.|gtag\(|MicroAnalytics
```

**False positive guard:** These patterns are candidates. Confirm against the file's imports — `.find()` in a file importing `prisma` = DB operation. `.find()` in a file with only standard library imports = array method. Ignore unconfirmed matches.

---

### After all grep passes — build inventory

For **OOP**: class list, relationship map, API calls, external deps, DI registrations
For **Component-based**: component list, render tree, hook usage, API calls, shared state
For **Functional**: function list, module deps, route map
For **Mixed**: merge all; tag each entity with its paradigm type
**All strategies**: external operation list (DB, cache, storage, queue, websocket, push, auth, analytics) with file locations

---

## Structural Scoring

**This phase identifies which files are foundational using structural signals — never class names.**

A class called `ViewModel`, `Payments`, or `XYZ` can be a root base class. Name means nothing. Structure reveals everything.

### Three priority tiers (replace arithmetic scoring)

Instead of computing a numerical score, classify each file into a tier using simple rules:

**TIER 1 — Must read (foundational)**
A file qualifies if ANY of these are true:
- It contains an `abstract` class, `protocol`, or `trait`
- Its classes/interfaces are extended or implemented by **3 or more** other files (from Pass 1 results)
- It is imported by **5 or more** other files in the target directory
- It has generic type parameters (e.g. `class X<T, R>`) AND is extended by at least 1 other file

To determine import frequency: run one additional grep across all files in `TARGET_PATH` using the pattern for the detected language:

```
DART:       ^import\s+['"]package:[^'"]+['"]
TYPESCRIPT: ^import\s+.*from\s+['"][^'"]+['"]|^import\s+['"][^'"]+['"]
PYTHON:     ^(from|import)\s+[\w.]+
JAVA/KT:    ^import\s+[\w.]+;?
GO:         ^\s+"[\w./-]+"
SWIFT:      ^import\s+\w+
RUST:       ^use\s+[\w:]+|^mod\s+\w+
```
Count how many files import each unique file path or module name. Files imported by 5+ are Tier 1.

**Barrel file guard (TypeScript):** If a file is named `index.ts` or `index.js` and only contains re-exports (`export.*from`), it is NOT foundational — it's a barrel. Downgrade it to Tier 3 regardless of import count.

**TIER 2 — Read if budget allows**
- DI registry / module files (`*module*`, `*registry*`, `*container*`, `*locator*`, `*injection*`)
- Entry points (`main.*`, `app.*`)
- Files with 2+ class relationships but not qualifying for Tier 1
- Manifest files: `pubspec.yaml`, `package.json`, `go.mod`, `Cargo.toml` (read for package name context only)

**TIER 3 — Grep only, no full read**
- Everything else: models, widgets, screens, simple entities
- Generated files (already excluded but if any slip through)

### Cross-boundary resolution

Foundational files are often outside the target directory (e.g. `lib/core/`, a shared package).
For each Tier 1 class NOT found within `TARGET_PATH`:
1. Grep one directory level above `TARGET_PATH` for its declaration
2. If not found, grep the project root (two levels up max)
3. Add the resolved file to the Tier 1 read list
4. Cap cross-boundary search at **2 levels up** from `TARGET_PATH`

### Output of this phase

Print a ranked list before reading anything:
```
TIER 1 (will read — foundational):
  lib/core/base/view_model.dart       (abstract, extended by 12 files)
  lib/core/domain/use_case.dart       (abstract, generic<I,O>, extended by 8)
  lib/features/payments/payments.dart  (imported by 6 files)

TIER 2 (will read if budget allows):
  lib/features/payments/di/module.dart (DI registry)
  lib/features/payments/bloc/bloc.dart (2 relationships)

TIER 3 (grep only):
  ... remaining N files
```

---

## Detail Level (determined by `rich` flag)

**`DETAIL_LEVEL` is set by the `rich` flag in arguments. No interactive prompt.**

- **No `rich` flag (default):** `DETAIL_LEVEL` = `method-names`. Safe, secure. Only class/method names in diagram labels. Identical to v1.0.1 output.
- **`rich` flag present:** `DETAIL_LEVEL` = `rich`. Shows endpoints, operation types, and targets. For internal/trusted use.

This applies to ALL diagram types across all input modes.

---

## File Reading

**Key principle:** Grep covers ALL files cheaply. Full reads are expensive. Read budget is set by `EFFORT_LEVEL`.

### Reading strategy per diagram type

#### CLASS DIAGRAM
- Read Tier 1 files (foundational — abstract classes, heavily-inherited contracts)
- Read Tier 2 DI registry files (to confirm what implements what)
- Read concrete implementors of abstract classes found in Tier 1

#### SEQUENCE DIAGRAM — 5-step chain trace (unconditional)

**These 5 steps ALWAYS execute at every effort level. No conditions, no "if high/max".**

1. **Read entry point** — identify the screen / controller / main handler via grep, read it
2. **Follow the call** — find the first outbound method call, grep for the called class, read its file
3. **Resolve abstracts** — if the class is abstract/interface/protocol/trait:
   - First check DI registry files for a concrete binding:
     ```
     DART (GetIt):     registerSingleton<AbstractType>(() => ConcreteImpl())
     JAVA/KOTLIN:      @Binds abstract fun bind(impl: ConcreteImpl): AbstractType
     SPRING:           @Bean public AbstractType name() { return new ConcreteImpl(); }
     TS/NESTJS:        { provide: AbstractType, useClass: ConcreteImpl }
     ```
   - If no DI binding: grep `extends AbstractClassName` / `implements AbstractClassName` to find concrete class
   - Read the concrete class, continue from there
   - If multiple found: read the most likely, note others
4. **Resolve mixins/composition** — if the class has composition attachments:
   ```
   DART:      with MixinA, MixinB → grep `mixin MixinA`, read it, include its methods
   KOTLIN:    by delegateImpl → grep for delegate class, read it
   PYTHON:    class Foo(MixinA, MixinB, Base) → read each mixin
   ```
5. **Repeat** steps 2-4 until you hit an HTTP call, external SDK, data store, or the read budget

**Do NOT read sideways** (sibling classes not in the call chain).

If abstract resolution fails at any step (no DI binding, no concrete class), note in diagram:
`"Abstract boundary — concrete impl not statically resolvable"`

**Effort only controls the budget and hop limit:**

| Effort | Max hops | Max reads | Cross-boundary |
|---|---|---|---|
| `low` | 5 | 10 | No |
| `medium` | 12 | 20 | 1 level up |
| `max` | Unlimited | No cap | 2 levels up |

#### COMPONENT DIAGRAM — zero reads
Import statements + HTTP patterns from grep tell you everything about external dependencies.
**Do NOT read Tier 1 files** — they add no value to a dependency graph.

#### ARCHITECTURE OVERVIEW — zero reads
Directory structure + class declarations from grep fully determine layer membership.
**Do NOT read Tier 1 files** — layer placement is determined by directory path, not file content.

#### ALL (default) — combine class + sequence reads only
Read Tier 1 files + sequence chain-trace files. Component and arch diagrams are generated from grep data that was already collected. With overlap, total is usually 10–18 files.

### Scale rules

| Input mode | Scale | Strategy |
|---|---|---|
| **Directory** — 1-49 files | Small | Standard — full read budget |
| **Directory** — 50-99 files | Medium | Grep-first, auto-split class diagrams, happy-path sequence only |
| **Directory** — 100+ files | Large | Auto-decompose by subdirectory, integration diagram at end |
| **Single file** | — | Read the file directly, focused diagrams |
| **Line range** | — | Read the range only, focused diagrams |
| **Multi-path** | Per item | Each item follows its own scale rule based on its type and size |
| **Pasted code** | — | Analyze in isolation or resolve to line-range if found in project |

---

## Diagram Generation

Generate only the diagram types requested by `DIAGRAM_TYPE`. For `all`, generate all four.

### Output format rules (strictly follow these)

1. Print a single line of prose before each diagram block explaining what it shows.
2. Every Mermaid diagram MUST be wrapped in a fenced code block tagged `mermaid` — nothing outside the fence.
3. When using `split` mode, each sub-diagram gets:
   - A bold heading: `**Section — Name**` followed by one explanation sentence
   - Then immediately the fenced ```mermaid block
   - Then a blank line before the next section
4. **Never** mix prose text inside a mermaid code fence — no titles, no headings, no `---` separators inside the fence.
5. After all diagrams, add: `> Each diagram block above can be pasted individually into any Mermaid renderer (mermaid.live, GitHub, Notion, GitLab).`

### Mermaid compatibility guardrails

- **Dark theme (all diagrams):** Always add `%%{init: {'theme': 'dark'}}%%` as the very first line of **every** Mermaid diagram — sequence, class, component, and architecture. This ensures consistent dark background with light text across all outputs.
- **Participant labels (sequence only):** No `<br/>`, no HTML tags, no special characters. Use short aliases: `participant MBA as MoniepointBusinessAnalytics`. Max 30 characters per alias.
- **`rect` blocks (sequence only):** Inside dark-themed sequence diagrams, use `rect rgba(255, 255, 255, 0.1)` and `rect rgba(255, 255, 255, 0.05)` (alternating subtle transparency) to separate flows. Never use opaque or bright colors — they clash with the dark theme. Some older renderers may not support `rect` — note this in the output.
- **`namespace` in classDiagram:** Only supported in Mermaid 10.3+. Prefer `%% --- Layer Name ---` comment separators for wider compatibility.
- **`autonumber` in sequence:** Numbering is cumulative across the entire diagram — it does NOT reset inside `rect` blocks. This is expected behavior.

### Detail level rules (applied to ALL diagram types below)

**When `DETAIL_LEVEL` = `method-names` (default):** Current behavior. Use class/method names only. No endpoints, no operation details. Identical to v1.0.1 output.

**When `DETAIL_LEVEL` = `rich`:** Apply these rules per diagram type:

**Sequence diagram (rich):**
- HTTP: full endpoint path as arrow label. `Repository->>API: POST /api/v1/payments`. Add `Note` for request payload fields.
- DB: operation type + entity only. `Repository->>DB: WRITE transactions`. **Never show query text.**
- Cache/Queue/WS/Auth/Analytics/Push: compact operation + target. `Service->>Cache: GET user session`
- Add external participants for each detected category (`participant API as External API`, `participant DB as Database`, etc.). Only add what was found.

**Class diagram (rich):**
- Annotate repository/service methods with their operation: `+processPayment() POST /api/v1/payments`
- Annotate data-layer classes with DB entity stereotype: `<<DB: transactions>>`

**Component diagram (rich):**
- Edge labels show actual targets: `-- POST /api/v1/payments -->` instead of `-- HTTP -->`
- DB edges show entity: `-- READ users -->` instead of `-- database -->`

**Architecture diagram (rich):**
- External layer nodes show specific services: `API: /api/v1/payments`, `DB: users, transactions`

**Security guardrail (all diagrams, all modes):**
- DB: operation type + entity name ONLY (`READ users`, `WRITE transactions`). Never query text, columns, filters, or schema.
- Auth: Never surface token values. Only `VERIFY token`.

**Reference table (rich mode, sequence only, 15+ steps):**
After sequence diagrams with 15+ steps, add a reference table:
```
| Step | Category | Operation | Target | Source |
|------|----------|-----------|--------|--------|
| 4 | HTTP | POST | /api/v1/payments | datasource.dart:42 |
| 7 | Database | WRITE | transactions | repository.dart:28 |
```
Skip for diagrams under 15 steps.

---

### `class` — Structure Diagram

#### FLOW_MODE: `full` (default)

Produce a **single** diagram containing all entities.

**OOP paradigm → `classDiagram`**
- Every class/interface/mixin/struct found
- `<<abstract>>`, `<<interface>>`, `<<enum>>` stereotypes
- Inheritance `<|--`, composition `*--`, dependency `..>`
- 3–5 key public fields and methods per class
- If `DETAIL_LEVEL` = `rich`: annotate methods with endpoint, add `<<DB: entity>>` stereotypes
- Group layers with `%% --- Layer Name ---` comment separators

**Component paradigm → `graph TB` (Component Tree)**
- Each component as a node (actual names from grep)
- Parent→child rendering edges
- Annotate each node with its primary hook or state dependency
- Group by feature area using `subgraph`

**Functional paradigm → `graph LR` (Module Map)**
- Each module/file as a node
- Exported functions as annotations
- Import arrows between modules

#### FLOW_MODE: `split`

Produce **one diagram per layer**:
- **Data layer** — repositories, data sources, models, DTOs, network clients
- **Domain layer** — use cases, entities, interfaces, business logic
- **Presentation layer** — ViewModels, BLoCs, Controllers, UI state
- **Core/Shared** — base classes, utilities, DI (if present)

Each layer gets a bold heading, one sentence, and its own fenced mermaid block.
Cross-layer relationships shown as `..>` dependency arrows (don't duplicate entities across diagrams).
Skip a layer if it has fewer than 2 entities — mention it in a note.

---

### `sequence` — Flow Diagram

First, identify all distinct logical flows (e.g. initialization, happy-path, error, background sync). Then apply `FLOW_MODE`:

#### FLOW_MODE: `full` (default)

Produce a **single** `sequenceDiagram` containing all flows.
Separate flows using `rect` blocks with alternating subtle transparency on dark theme:

```
%%{init: {'theme': 'dark'}}%%
sequenceDiagram
  autonumber
  participant A
  participant Z

  rect rgba(255, 255, 255, 0.1)
    Note over A,Z: Flow 1 — SDK Initialization
    ... interactions ...
  end

  rect rgba(255, 255, 255, 0.05)
    Note over A,Z: Flow 2 — Event Dispatch
    ... interactions ...
  end
```

Rules:
- Always start with `%%{init: {'theme': 'dark'}}%%` as the first line
- All participants declared once at the top (union of all flows)
- Alternate between `rgba(255, 255, 255, 0.1)` and `rgba(255, 255, 255, 0.05)` for flow rects
- Use `Note over` at the start of each rect to label it
- Numbering with `autonumber` is cumulative (does not reset per rect) — this is normal
- If a unified diagram would exceed **60 interactions**, print a note recommending `split` mode and still attempt the diagram

**OOP:** entry point → layer by layer → external API, using actual class/method names
**Component:** user action → hook → API → state update, using actual component/hook names
**Functional:** handler → business logic → I/O → external, using actual function names

#### FLOW_MODE: `split`

Produce one **separate** `sequenceDiagram` per logical flow.
Each flow gets a bold heading, one sentence, and its own fenced mermaid block with only its participants.

---

### `component` — Dependency Diagram

**`FLOW_MODE` is ignored — always produces one unified diagram.**

**All paradigms → Mermaid `graph LR`**
- Internal modules as rectangular nodes, external services/packages as rounded nodes `(( ))`
- If `DETAIL_LEVEL` = `rich`: edge labels show actual targets (`-- POST /api/v1/payments -->`, `-- READ users -->`)
- If `DETAIL_LEVEL` = `method-names`: edge labels are generic (`-- HTTP call -->`, `-- database -->`)
- Sources: all HTTP calls + all external package imports + Pass 3 external operations from grep

---

### `arch` — Architecture Overview

#### FLOW_MODE: `full` (default)

Produce a **single** `graph TB` with all layers in one view.

**OOP / Clean Architecture:**
- `subgraph Presentation`, `subgraph Domain`, `subgraph Data`, `subgraph External`
- Each entity in its correct layer (determine by directory path and class role)
- Cross-layer arrows only at interfaces/abstractions
- Flag any layer violation (e.g. Presentation → Data bypassing Domain)
- If `DETAIL_LEVEL` = `rich`: External layer nodes show specific services (`API: /api/v1/payments`, `DB: users, transactions`)
- If `DETAIL_LEVEL` = `method-names`: External nodes are generic (`External API`, `Database`)

**Component paradigm:**
- `subgraph Pages`, `subgraph Components`, `subgraph Hooks`, `subgraph Services`, `subgraph State`
- Show UI → hooks → services → APIs dependency chain
- Annotate state management approach
- If `DETAIL_LEVEL` = `rich`: service nodes show actual endpoints

**Functional paradigm:**
- `subgraph Handlers`, `subgraph BusinessLogic`, `subgraph DataAccess`, `subgraph External`
- Each function in its layer by responsibility
- If `DETAIL_LEVEL` = `rich`: external nodes show specific targets

#### FLOW_MODE: `split`

Produce **one diagram per subsystem** (determined from top-level subdirectories under `TARGET_PATH`).
Each subsystem with 2+ entities gets a bold heading, one sentence, and its own fenced mermaid block.
After all subsystem diagrams, add one **Integration diagram** showing how subsystems connect.

---

## Insights

After the diagrams, add a brief **Key Insights** section (bullet points, tailored to paradigm):

**Always include:**
- Paradigm detected and confidence level (e.g. "OOP — 20 class declarations, 2 abstract contracts, high confidence")
- Total entities found and distribution across layers
- External APIs/services the feature depends on
- Read budget usage (e.g. "14 of 20 reads used (medium effort)" or "unlimited reads used (max effort)")

**For OOP:**
- Architectural layer violations spotted
- Class with the most inbound dependencies (hotspot)
- Circular dependencies detected

**For Component-based:**
- Deepest component nesting level (prop drilling risk)
- Components with the most hook dependencies (complexity hotspot)
- Shared state scope (local, context, global store)

**For Functional:**
- Modules with the most inbound calls (hotspot)
- Side-effect functions mixed into pure logic layers

**For Multi-path mode (additional):**
- Per-item summary: entities found, reads used, paradigm per item
- Cross-path relationships: which items import from which, connection points
- Items with no cross-references noted as "independent"

---

## Guardrails

- **Never invent** entity names, method names, or relationships not found in the code
- **Never apply OOP diagram patterns to a component or functional codebase** — use the correct paradigm strategy
- **Never exceed the effort level's read budget** (low=10, medium=20, max=unlimited) — note when budget is hit
- If a directory has no source files, say so and stop
- If the path doesn't exist, report it and stop
- Keep each diagram focused — **30 nodes max** per diagram; split into sub-diagrams if larger
- If a diagram type yields no meaningful content (e.g. no HTTP calls for component diagram), skip it and explain why
- If paradigm detection is ambiguous, state your confidence and reasoning before proceeding
