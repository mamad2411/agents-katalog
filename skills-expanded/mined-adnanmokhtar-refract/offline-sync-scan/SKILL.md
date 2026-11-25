---
name: offline-sync-scan
description: Find offline-write defects in mobile apps — RAM-only queues, replays with no idempotency key, poison heads, optimistic writes with no rollback, cross-account residue, reachability as truth — proved by a kill or a dropped response.
kind: skill
pack: mobile
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: offline-sync-scan

## Premise

A mobile screen says "Saved" long before the server has the write. Between the two, the OS kills the process, the network drops the response after the server committed, the head of the queue fails forever, a background refetch overwrites the optimistic value, and a second person signs in on the same phone. Every class here is a gap between the promise the UI made and what the device can honour. None of it shows on a test network: the request always answers and the process never dies.

**Every finding cites the promise (`<file:line>` where the UI acknowledges) + the store the write reaches (or does not) + the event that breaks it (kill, lost response, failed head, refetch, account switch, flaky link) + the version gate + the oracle at its tier (or the command that settles it) + the fix in the project's stack.** A grep hit is never a finding by itself, and "no offline defect found" is never printed without the class-coverage block (§ Output).

**Detect statically, prove on a device.** Tiers D / I / A / S are [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § The claim, restated. Durability and identity need **D** (a real kill, a real sign-out); replay and rollback accept **I** with a mock server that drops or rejects the response. **No booted device means `SKIPPED`, never PASS**, and a candidate below its tier is **Unconfirmed** with the settling command ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6). `@offline-sync-auditor` (this pack) is the judge: it turns these candidates into its per-entity ledger and keeps its rule that a `durable` verdict without process-death evidence is `unproven`.

## The rule

A candidate is a finding when all five hold:

1. **A promise is made.** A screen acknowledges the write (toast, closed sheet, row moved to "sent", optimistic cache value) before the server confirmed it, or the product promises offline use for that entity. A queue nobody acknowledges is design debt, not a broken promise.
2. **It ships.** Release build, a real entry point, not `__DEV__` / `kDebugMode` / a test target.
3. **The version gate holds.** The library behaviour cited exists in the lockfile's version (TanStack Query v5 persistence, zustand `persist` `version`/`migrate`, axios-retry's default condition, NetInfo's `null` before the first probe; Hive or drift write semantics in Flutter; Room and WorkManager in Kotlin; Core Data or SwiftData in Swift).
4. **Nothing neutralizes it.** A write-through wrapper, a server-side dedupe the backend confirms, a single-writer entity, a drain trigger in another module.
5. **The event occurs** (the OS kills backgrounded apps; responses get lost; heads fail; people share phones) — and the oracle at the class's tier fires, or the candidate stays Unconfirmed.

## Boundaries

- **When** the OS lets the queue drain — process-death restoration of screens, background scheduling, FGS limits, the push token at logout → `mobile-lifecycle-scan` (this pack). § 5 here skips push tokens; the two runs dedupe by `<file:line>`.
- Network timeouts and the unhandled rejection on a screen → `mobile-lifecycle-scan` § 4. A retry storm with no backoff stays here (§ 2c).
- Whether a token is stored securely (plaintext vs Keychain) → `mobile-security-scan` when the security pack is installed; without it, this skill does not judge storage — note the store as `security-class (owner pack not installed)` ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 8). § 5b here owns only *whose* session survives a reinstall.
- The offline, stale, pending and error copy the user reads → `ui-state-scan` when the ui-ux pack is installed; without it, record `floor: not audited (ui-ux pack absent)`.
- Server-side idempotency and dedupe → `@api-architect` when the backend pack is installed; without it, record `server dedupe: unconfirmed` — never assume it.
- Whether a screen should work offline at all → `@mobile-architect` (this pack). Its works / degrades / blocks classification is an input.
- A browser client's service worker or IndexedDB → the frontend pack.

## Adapt to the codebase — lanes

Read the versions grep 0 prints and print the lanes you ran in the output header.

| Lane | Durable queue | Replay key | Conflict | Reachability | Lint lane (project config, keep only the rule) |
|---|---|---|---|---|---|
| **React Native / Expo** | `expo-sqlite`, op-sqlite, WatermelonDB, MMKV, AsyncStorage; TanStack Query `PersistQueryClientProvider` + `resumePausedMutations()` + `setMutationDefaults`; zustand / redux-persist with `version` + `migrate` | `Idempotency-Key` from the row id, minted at enqueue | `onMutate` → `cancelQueries` + snapshot, `onError` rollback, `onSettled` refetch; RTK `.undo()`; Apollo `optimisticResponse` rolls back itself | NetInfo `isInternetReachable` (null until known), the request result as truth | `@typescript-eslint/no-floating-promises` (1c) |
| **Flutter** | drift, Isar, Hive (awaited), sqflite, ObjectBox | key stored in the row | server `version` / ETag, not `DateTime.now()` | `connectivity_plus` is a hint only; the request decides | `discarded_futures`, `unawaited_futures` (very_good_analysis; not in `flutter_lints`) (1c) |
| **Android** | Room (+ `@Dao` suspend writes), DataStore; WorkManager `CoroutineWorker`, unique work, `setBackoffCriteria` | `@Header("Idempotency-Key")` from the row | `If-Match` / version column | `NET_CAPABILITY_VALIDATED`, not `activeNetworkInfo` | lint `InvalidPeriodicWorkRequestInterval` |
| **iOS** | Core Data, SwiftData, GRDB; `BGTaskScheduler`, background `URLSession` | stored `UUID` per op | `If-Match` / version | `NWPathMonitor` as a hint, `waitsForConnectivity` | — |

No lint rule covers §§ 1a, 1b, 1d or 2–6; the greps below and the read are the coverage.

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is context. The root and exclusion block is `mobile-lifecycle-scan`'s, unchanged, so the two scans agree on what ships. Every `rg` names its path; set-differences use `while read` with an explicit file. A line tagged `1a`–`6d` is a set-difference result; the rest are grep hits. Any `rg` error on stderr is a failed grep, never zero hits.

```bash
# Mobile roots: RN/Expo package.json dirs, Flutter pubspec dirs, Android modules, Xcode project dirs; nested roots folded.
ROOTS=()
while IFS= read -r d; do ROOTS+=("$d"); done < <(
  { rg -l --pcre2 '"(?:react-native|expo)"\s*:' -g 'package.json' -g '!**/node_modules/**' .
    rg -l --pcre2 '^\s+sdk:\s*flutter\b' -g 'pubspec.yaml' -g '!**/.dart_tool/**' .
    rg --files -g '**/src/main/AndroidManifest.xml' -g '!**/{build,node_modules,.gradle}/**' . | sed 's#/src/main/AndroidManifest\.xml$#/x#'
    rg --files -g '**/*.xcodeproj/project.pbxproj' -g '!**/{Pods,node_modules,DerivedData}/**' . | sed 's#/[^/]*\.xcodeproj/project\.pbxproj$#/x#'
  } | while IFS= read -r f; do dirname "$f"; done | sort -u | awk 'p != "" && index($0, p "/") == 1 { next } { print; p = $0 }')
[ ${#ROOTS[@]} -gt 0 ] || { echo 'no mobile project marker: every class N/A (no mobile surface)'; exit 0; }
printf 'root %s\n' "${ROOTS[@]}"
# Never shipped in a release build: deps, build output, tests, debug source sets, generated code, docs.
X=(-g '!**/{node_modules,Pods,build,.gradle,.dart_tool,.expo,DerivedData,dist,vendor,.cxx}/**' -g '!**/src/{test,androidTest,debug}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,fixtures,__fixtures__,testdata,e2e,integration_test,.maestro,docs,ai}/**'
   -g '!**/*{Tests,UITests}/**' -g '!**/*.{test,spec,stories}.*' -g '!**/*_test.dart' -g '!**/*.{g,freezed,mocks}.dart' -g '!**/app_localizations*.dart' -g '!**/*.{md,mdx,lock,snap,map}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')
JS=(-g '*.{js,jsx,ts,tsx}'); KT=(-g '*.{kt,java}'); DA=(-g '*.dart'); SW=(-g '*.swift'); MF=(-g 'AndroidManifest.xml')
SRC=(-g '*.{js,jsx,ts,tsx,kt,java,dart,swift,m,mm}')
IROOTS=(); for r in "${ROOTS[@]}"; do { [ -d "$r/ios" ] || rg --files -g '**/*.xcodeproj/project.pbxproj' "$r" | rg -q . || rg -q --pcre2 '"expo"\s*:' -g 'package.json' "$r"; } && IROOTS+=("$r"); done

# 0. Version gates and the stores each root can persist to; Atlas Device Sync (end of life 2025-09-30) in use.
rg -n --pcre2 '"(?:react-native|expo|@tanstack/(?:react-query|react-query-persist-client|query-[\w-]+-persister)|@react-native-community/netinfo|redux-persist|zustand|@redux-offline/redux-offline|axios-retry|react-native-mmkv|@react-native-async-storage/async-storage|expo-sqlite|@op-engineering/op-sqlite|@nozbe/watermelondb|realm|@realm/react|@apollo/client)"\s*:' -g 'package.json' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '^\s+(?:drift|isar\w*|hive\w*|sqflite\w*|objectbox|shared_preferences|connectivity_plus|internet_connection_checker\w*|dio_smart_retry|realm|powersync|brick_\w+):\s' -g 'pubspec.yaml' "${ROOTS[@]}"
rg -n --pcre2 'androidx\.(?:room|work|datastore)|io\.realm|realm-kotlin|\bGRDB\b|\bRealmSwift\b' -g '*.{gradle,kts,toml}' -g '{Podfile,Package.swift}' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\b(?:flexibleSync|FlexibleSyncConfiguration|SyncConfiguration|syncSession|AppConfiguration)\b' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"

# 1. Queue durability. 1a a queue declared as an in-memory collection, and queue classes with no durable store in the file;
#    1b TanStack persistence with no resume or no mutation defaults, and paused mutations with no persister;
#    1c a durable write not awaited before the acknowledgement (JS, Dart); 1d roots with a queue and no drain trigger.
Q='(?:outbox|pending_?(?:ops|operations|mutations|writes|requests|actions|changes|uploads)|(?:sync|offline|retry|mutation|upload|write|request)_?queue)'
QD="(?i)(?:\b(?:const|let|var|val|final|static)\s+(?:[\w<>?,\[\]]+\s+)*_?\w*$Q\w*\s*(?::[^=\n]+)?=\s*(?:\[\s*\]|(?:const\s+)?<[^>]*>\s*\[\]|(?:mutable|array)ListOf\b|ArrayDeque\b|LinkedList\b|ConcurrentLinkedQueue\b|mutableStateListOf\b|new\s+(?:Array|Map|Set)\b|ListQueue\b|Queue<)|\b$Q\w*\s*:\s*\[\s*\]\s*[,}])"
rg -n --pcre2 "$QD" "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
DS='\w*Dao\b|AsyncStorage|MMKV|SQLite|sqlite|op-sqlite|WatermelonDB|@nozbe|Realm|@Entity|@Dao|RoomDatabase|DataStore|NSPersistentContainer|NSManagedObject|@Model\b|ModelContext|GRDB|\bHive\b|\bBox<|Isar|drift|sqflite|ObjectBox|persistQueryClient|PersistQueryClientProvider|persistReducer|\bpersist\(|SharedPreferences|UserDefaults|FileManager|writeAsString|FileSystem'
rg -l -i --pcre2 "\bclass\s+\w*$Q\w*\b" "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 "$DS" "$f" || echo "1a no durable store in $f"; done
for r in "${ROOTS[@]}"; do
  if rg -q --pcre2 '\b(?:PersistQueryClientProvider|persistQueryClient(?:Restore)?)\b' "${JS[@]}" "${X[@]}" "$r"; then
    rg -q 'resumePausedMutations' "${JS[@]}" "${X[@]}" "$r" || echo "1b $r: persisted query client, no resumePausedMutations"
    rg -q 'setMutationDefaults' "${JS[@]}" "${X[@]}" "$r" || echo "1b $r: persisted query client, no setMutationDefaults (restored mutations have no mutationFn)"
  elif rg -q --pcre2 "networkMode:\s*['\"](?:offlineFirst|always)|onlineManager\." "${JS[@]}" "${X[@]}" "$r" && rg -q 'useMutation' "${JS[@]}" "${X[@]}" "$r"; then echo "1b $r: paused mutations, no persister"; fi; done
rg -l -i --pcre2 "$Q" "${JS[@]}" "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -H -n --pcre2 '^\s*(?!await\b|return\b|yield\b|unawaited\()(?:this\.|_|\w+\.)+(?:setItem|mergeItem|multiSet|runAsync|execAsync|put|putAll|add|addAll|writeTxn|insert|save)\((?!.*\bawait\b).*\);' "$f" | rg -v --pcre2 '\.(?:push|add|addAll)\(\w+\);$|\b(?:list|items|_?\w*[qQ]ueue|_?\w*[oO]utbox|_?\w*[pP]ending\w*)\.(?:add|addAll|push)\(' ; done
for r in "${ROOTS[@]}"; do rg -q --pcre2 "$QD|(?i)\bclass\s+\w*$Q\w*\b" "${SRC[@]}" "${X[@]}" "$r" || continue
  rg -l --pcre2 'NetInfo\.addEventListener|useNetInfo|onlineManager\.|AppState\.addEventListener|onConnectivityChanged|registerNetworkCallback|NWPathMonitor|\bdoWork\b|BGTaskScheduler|defineTask|executeTask|onStatusChange' "${SRC[@]}" "${X[@]}" "$r" |
    while IFS= read -r f; do rg -q -i --pcre2 '\b(?:drain|flush|replay|resend|resumePausedMutations|processQueue|sync\w*|upload\w*|doWork)\s*\(' "$f" && echo "$f"; done | rg -q . || echo "1d $r: a queue and no drain trigger outside the screen that fills it"; done

# 2. Replay identity. 2a files that retry or queue a POST/PATCH and carry no idempotency key; 2b a key minted on the
#    send line (a new key per attempt); 2c a retry with no backoff or one that retries every method.
PO='\.(?:post|patch)\(|@(?:POST|PATCH)\b|method:\s*["\x27](?:POST|PATCH)|httpMethod\s*=\s*"(?:POST|PATCH)"'
IK='(?i)idempotency[-_]?key|x-idempotency|x-request-id|client_?mutation_?id|request_?id|operation_?id|dedupe_?key'
rg -l -i --pcre2 "axios-?retry|\bretry(?:When|Count|Policy|Condition|Interceptor)?\s*[:(=]|\bretries\s*[:=]|setBackoffCriteria|dio_smart_retry|$Q" "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do
  rg -q --pcre2 "$PO" "$f" && ! rg -q --pcre2 "$IK" "$f" && echo "2a POST/PATCH retried or queued, no idempotency key: $f"; done
rg -n --pcre2 '(?i:idempotency[-_]?key|x-idempotency)["\x27]?\s*[:=,]\s*(?:await\s+)?(?:uuid(?:v4)?\(|v4\(|(?:crypto\.)?randomUUID\(|nanoid\(|ulid\(|(?:const\s+)?Uuid\(\)\.v4\(|UUID\(\)\.uuidString|UUID\.randomUUID\()' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '\baxiosRetry\(\s*\w+\s*,\s*\{(?![^}]*\bretryDelay\b)[^}]*\}|\bretryCondition:\s*\(\s*\w*\s*\)\s*=>\s*true\b' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"

# 3. Ordering and poison. 3a a drain that skips a failed row; 3c a drain defined with no attempt ceiling or terminal state;
#    3d temporary ids in queue files; 3b a queue drained in parallel; 3e a persisted store versioned with no migrate.
QF=$(rg -l -i --pcre2 "$Q|\bdrain\w*\s*\(|\bflush\w*\s*\(" "${SRC[@]}" "${X[@]}" "${ROOTS[@]}")
[ -z "$QF" ] || printf '%s\n' "$QF" | while IFS= read -r f; do
  rg -H -n -U --pcre2 '\bcatch\b[^{\n]*\{(?=(?:[^{}]|\{[^{}]*\})*?\bcontinue\b)' "$f"
  rg -q -i --pcre2 '(?:\b(?:function|fun|func|def|async)\s+|\bvoid\s+(?=\w+\s*\([^)]*\)[^;{]*\{)|Future<\w*>\s+|\b(?:const|let|val)\s+)(?:drain|flush|replay|resend|processQueue|sync(?:All|Pending))(?!\w*(?-i:On[A-Z]))\w*\s*[(=]' "$f" &&
    ! rg -q -i --pcre2 'attempts?\b|retry_?count|retries|max_?attempts|dead_?letter|\bfailed\b|poison|give_?up' "$f" && echo "3c drain with no attempt ceiling or terminal state: $f"
  rg -H -n --pcre2 '\b(?:temp|tmp|local|optimistic)_?[iI]d\b|["\x27](?:temp|tmp|local)[-_:]' "$f"; done
rg -n -i --pcre2 "(?:Promise\.all(?:Settled)?|Future\.wait|awaitAll)\s*\(\s*(?:this\.|_)?\w*$Q\w*\s*\.\s*map\b|\b\w*$Q\w*\s*\.\s*(?:forEach\(\s*async\b|map\s*\{\s*async\b)" "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '\b(?:persist|persistReducer)\s*[(<]' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 '\bversion\s*:' "$f" && ! rg -q --pcre2 '\bmigrate\s*[:(]' "$f" && echo "3e persisted store versioned with no migrate: $f"; done

# 4. Conflict policy. 4a optimistic cache writes with no rollback; 4b no cancelQueries before the optimistic write;
#    4c a full-object PUT with no precondition; 4d the device clock stamped onto a record or compared as the authority.
rg -l --pcre2 '\bonMutate\s*[:(]' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 '\bonError\s*[:(]|\bonSettled\s*[:(]' "$f" || echo "4a onMutate with no onError/onSettled: $f"
  rg -q 'setQueryData' "$f" && ! rg -q 'cancelQueries' "$f" && echo "4b optimistic setQueryData with no cancelQueries: $f"; done
rg -l 'updateQueryData' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q '\.undo\(\)' "$f" || echo "4a RTK updateQueryData with no undo(): $f"; done
rg -l --pcre2 '@PUT\b|\b(?:api|client|http|dio|axios|instance|service|\w+Api|\w+Client)\.put\(|method:\s*["\x27]PUT|httpMethod\s*=\s*"PUT"' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do
  rg -H -n -i --pcre2 'if-match|if-unmodified-since|\betag\b|expected_?version|\brevision\b|\b_rev\b' "$f" | "${NC[@]}" | rg -q . || rg -H -n --pcre2 '@PUT\b|\.put\(|method:\s*["\x27]PUT|httpMethod\s*=\s*"PUT"' "$f"; done
rg -n --pcre2 '\b(?:updated|modified|changed|edited|lastModified|lastWrite)_?(?:At|On|Time|Ts)?\s*[:=]\s*(?:Date\.now\(\)|new Date\(\)|DateTime\.now\(\)|Date\(\)|System\.currentTimeMillis\(\)|Instant\.now\(\)|Clock\.System\.now\(\)|LocalDateTime\.now\(\))|\.(?:updated|modified)_?[aA]t\w*\s*(?:\.isAfter\(|\.isBefore\(|\.compareTo\(|[<>]=?\s*\w)' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"

# 5. Identity bleed. 5a logout functions missing a wipe category the root uses (push tokens are mobile-lifecycle-scan § 6);
#    5b iOS-shipping roots that write the Keychain with no file that wipes it behind a first-launch marker.
for r in "${ROOTS[@]}"; do N=()
  rg -q --pcre2 '"(?:@tanstack/react-query|@apollo/client|swr|urql)"\s*:' -g 'package.json' "$r" && N+=('query-cache~\.clear\(\)|clearStore|resetStore|removeQueries|resetQueries|cache\.reset')
  rg -q --pcre2 '\bpersist(?:Reducer|QueryClient)?\s*[(<]|PersistQueryClientProvider' "${JS[@]}" "${X[@]}" "$r" && N+=('persisted-state~purge\(|clearStorage\(|persistor\.|AsyncStorage\.clear|clearAll\(|removeClient|\.clear\(\)')
  rg -q -i --pcre2 'expo-sqlite|op-sqlite|watermelondb|\brealm\b|^\s+(?:drift|sqflite|isar|hive|objectbox):|androidx\.room|RoomDatabase|NSPersistentContainer|ModelContainer|\bGRDB\b' -g 'package.json' -g 'pubspec.yaml' -g '*.{gradle,kts,swift}' "${X[@]}" "$r" && N+=('local-db~(?i)clearAllTables|deleteDatabase|DELETE\s+FROM|drop(?:Database|Table)|deleteAll|unsafeResetDatabase|delete\w*FromDisk|\.clear\(|truncate|destroy|deleteRealm')
  rg -q --pcre2 "$QD|(?i)\bclass\s+\w*$Q\w*\b" "${SRC[@]}" "${X[@]}" "$r" && N+=("outbox~(?i)$Q|outbox|queue|pending")
  rg -q --pcre2 'androidx\.work|BGTaskScheduler|expo-background-task|^\s+workmanager:' -g 'package.json' -g 'pubspec.yaml' -g '*.{gradle,kts,swift}' "${X[@]}" "$r" && N+=('scheduled-work~cancelAll\w*|unregister(?:All)?Tasks?\w*|cancel(?:All)?TaskRequest|cancelUniqueWork')
  rg -q --pcre2 'react-native-webview|^\s+(?:webview_flutter|flutter_inappwebview):|\bWKWebView\b|android\.webkit\.WebView' -g 'package.json' -g 'pubspec.yaml' -g '*.{kt,java,swift}' "${X[@]}" "$r" && N+=('web-cookies~removeAllCookies|clearCookies|CookieManager|WKWebsiteDataStore')
  [ ${#N[@]} -eq 0 ] || rg -l -i --pcre2 '\b(?:fun|func|function|Future<void>|const|def|void)\s+(?:log_?out|sign_?out)\b|\b(?:log_?out|sign_?out)\s*[:=]\s*(?:async\s*)?\(' "${SRC[@]}" "${X[@]}" "$r" | while IFS= read -r f; do m=""
    for n in "${N[@]}"; do rg -q --pcre2 "${n#*~}" "$f" || m="$m ${n%%~*}"; done; [ -z "$m" ] || echo "5a $f: logout wipes no$m"; done
  case " ${IROOTS[*]} " in *" $r "*) ;; *) continue ;; esac
  rg -q --pcre2 '\bSecItemAdd\b|KeychainWrapper|KeychainAccess|FlutterSecureStorage|flutter_secure_storage|SecureStore\.setItemAsync|setGenericPassword|setInternetCredentials' "${SRC[@]}" "${X[@]}" "$r" &&
    ! { rg -l -i --pcre2 'first_?(?:launch|run)|has_?(?:launched|run)|fresh_?install|\bis_?first' "${SRC[@]}" "${X[@]}" "$r" | while IFS= read -r f; do
          rg -q --pcre2 'deleteAll\(|SecItemDelete|reset(?:Generic|Internet)(?:Password|Credentials)|deleteItemAsync|removeAll\w*\(' "$f" && echo "$f"; done | rg -q .; } && echo "5b $r: Keychain written, no wipe on a fresh install"; done

# 6. Reachability as truth. 6a NetInfo isConnected with no isInternetReachable in the file; 6b connectivity_plus gating a
#    request; 6c native reachability preflights; 6d a reconnect handler that refetches or resyncs everything.
rg -l --pcre2 '\bisConnected\b' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q 'isInternetReachable' "$f" || rg -H -n --pcre2 '\bisConnected\b' "$f" | "${NC[@]}"; done
rg -n --pcre2 'ConnectivityResult\.none|\bcheckConnectivity\(\)' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\bSCNetworkReachability\w*|\bReachability\(\)|\bactiveNetworkInfo\b|\bisConnectedOrConnecting\b' "${KT[@]}" "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 'NetInfo\.addEventListener|onlineManager\.(?:subscribe|setEventListener)|onConnectivityChanged|registerNetworkCallback|pathUpdateHandler|onStatusChange' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do
  rg -H -n --pcre2 '\b(?:invalidateQueries|refetchQueries|resetQueries)\(\s*\)|\b(?:full|complete)(?:Re)?[sS]ync\(|\b(?:resync|refetch|reload)All\(' "$f"; done
```

A finding is a grep hit **plus** a read of the write path from the acknowledgement to the store **plus** the version gate. Three blind spots are structural:

- **The queue and the promise live in different files.** 1a sees a declaration; the acknowledgement is often a screen that calls `enqueue`. Follow the call one hop each way before calling a queue durable or lossy — a class with no store in its own file (1a, second form) may delegate to a repository.
- **Per-root vocabulary is a heuristic.** 1d and 5a decide by what a root *uses* (a query library, a local DB, a scheduler). A drain trigger in a shared package outside the root, or a logout that calls a `resetAll()` helper, is invisible: read the helper before reporting a missing category.
- **A comment can satisfy a check.** 4c filters comment lines; the other `rg -q` evidence checks do not. Read the evidence line when a check comes back clean on a file you expected to fail.

**Measured** (2026-10-05, ripgrep 15.2.0; bash 3.2 and zsh give the same sorted hit set, with stdin piped or not; under 1 s). On the program's seeded multi-stack sample (Expo SDK 57, bare RN 0.82, Flutter 3.47, Kotlin at `targetSdk` 35, Swift; 29 offline positives and 22 decoys across the six classes) the script surfaces every positive and no decoy; the read step is left one known gap (a sign-out that deletes the Hive box but not the in-memory queue — § 1 already reports that queue). On every web and server fixture in `benchmarks/fixtures/*` it finds no mobile root and prints `N/A`; on `mobile-defects` (five mobile roots, measured 2026-10-10) it prints all 6 of its seeds in 23 lines, and the one decoy it prints (a key minted once at enqueue) is refuted by the read — its `DEFECTS.md` § Detector measurement. A first version printed 3 false 3c lines there: `void` counted as a declaration keyword, so JS `void flush();` (the operator on a call) and a Dart listener named `drainOnNetworkChange` read as drain definitions; `void` now needs a body and a name ending in `On…` is a trigger. On a read-only real Flutter app (1,167 files, 440 Dart) the first version printed **0** lines: the fresh-install evidence regex accepted an install id that is itself kept in the Keychain and an unrelated empty-state widget with "first run" in its name, and the per-root category gate skipped § 5b whenever a root had no wipe category. Requiring a first-launch marker **and** a Keychain wipe in the same file, and gating 5a alone, gives **1** line — § 5b, a true candidate (tokens in `flutter_secure_storage`, no wipe on a fresh install) — and 0 false.

## The 3,000-hit path

1. **Intersect** with promises: a queue or optimistic write no screen acknowledges is dismissed with one read (it is still a § 1 ledger row, `no promise`).
2. **Group** by entity, not by file: two screens writing one record share one durability story and one conflict policy. One shared HTTP client with `axiosRetry` is one § 2 group however many calls go through it.
3. **Rank** by what is lost: money and orders, then messages and user-authored content, then preferences. Field reports of duplicates or vanished records outrank code order.
4. **Read the top 30 groups fully** — the write path from acknowledgement to store to drain to dequeue.
5. **Prefer the bulk oracle at scale**: one offline-kill run per top entity (airplane mode → submit → background → `am kill` → relaunch → network on → count server records) settles § 1 and § 3 for that entity; one identity switch settles § 5 for the app.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity: **critical** when the entity moves money or exposes another account's data **and** the oracle fired; **high** for lost user writes and silent overwrite; **medium** for retry storms and cold-start sync blocks; **low** for a missing conflict UI where the server merges. The auditor label is the `@offline-sync-auditor` ledger term.

| § | Class | Auditor labels | Tier | Default |
|---|---|---|---|---|
| 1 | Queue durability: in-memory queue, acknowledged before the write lands, no drain trigger, TanStack paused mutations not persisted or not resumed | `ram-only-queue`, `ack-before-persist`, `queue-without-a-reader` | D | high |
| 2 | Replay identity: POST retried or replayed with no key, a key minted per attempt, retry with no backoff | `unkeyed-replay`, `key-regenerated-per-attempt` | I (mock) / D | high; critical for payments and orders |
| 3 | Ordering and poison: a failed row skipped, a parallel drain, no attempt ceiling, temp ids, a persisted queue discarded on a version bump | `skip-on-failure-reorder`, `poison-head`, `temp-id-orphan`, `silent-drop`, `schema-lock` | D | high |
| 4 | Conflict policy: optimistic write with no rollback, refetch clobbering a pending write, full-object PUT with no precondition, device clock as authority | `blanket-policy`, `revalidate-clobbers-pending`, `clock-as-authority`, `ceremony-without-concurrency` (refute) | I / D | high; low with a server merge |
| 5 | Identity bleed: logout that leaves a category the app uses; Keychain session surviving a reinstall | `identity-bleed` | D | critical when another account's data shows |
| 6 | Reachability as truth: `isConnected` without reachability, connectivity results gating a send, native preflights, full resync on reconnect | `reachability-as-truth`, `full-resync-on-reconnect` | D | medium |

### 1. Queue durability

```
BAD:   const pendingMutations: Mutation[] = []; enqueue(m) { pendingMutations.push(m); showToast('Saved') }
       final List<PendingOp> _syncQueue = [];          private val pendingUploads = ArrayDeque<PendingUpload>()
       void add(...) { _box.put(id, note); _onSaved(); }            // not awaited: "Saved" before disk
       <PersistQueryClientProvider persistOptions={{ persister }}>   // no resumePausedMutations, no setMutationDefaults
GOOD:  await db.runAsync('INSERT INTO outbox …', op.id, …); onSaved()   // write-through, then acknowledge
       queryClient.setMutationDefaults(key, { mutationFn }); onSuccess={() => queryClient.resumePausedMutations()}
       NetInfo / onlineManager / WorkManager / BGTaskScheduler trigger that calls drain() outside the screen
```
**Read the code:** Where does the UI acknowledge, and is the durable write awaited before that line? Is the in-memory collection a write-through buffer of a durable store (precedents § 73), or the only copy? For TanStack Query v5 persistence: only mutation *state* is persisted, so a restored paused mutation needs a default `mutationFn` (`setMutationDefaults`) and an explicit `resumePausedMutations()` after restore (TanStack mutations guide, read 2026-10-05). What drains the queue when the screen that filled it is closed — reconnect, app start, the platform scheduler? Does the project use Realm's Atlas Device Sync (`SyncConfiguration`, `flexibleSync`)? It reached end of life on 2025-09-30 (MongoDB Atlas Device SDKs deprecation page, via search 2026-10-05): a sync layer with no server behind it. **Finding when** an acknowledged write exists only in memory, the acknowledgement precedes the durable write, or nothing outside the filling screen drains the queue. **Severity:** high. **Proof:** offline kill (§ Proof) — airplane mode, submit, background, `am kill`, relaunch, network on: the server count is 0 before the fix and 1 after.

### 2. Replay identity

```
BAD:   axiosRetry(api, { retries: 5, retryCondition: () => true })  + api.post('/orders', …)   // no key, no delay
       http.post(url, body, { headers: { 'Idempotency-Key': uuid() } })                       // new key per attempt
GOOD:  key = row.id minted at enqueue, persisted with the row, sent on every attempt; axiosRetry(… retryDelay: axiosRetry.exponentialDelay)
```
**Read the code:** Is the call idempotent by HTTP semantics (GET, PUT of a full resource, DELETE)? Then no key is needed (precedents § 74). axios-retry's **default** condition retries only network errors and 5xx on idempotent methods and its default delay is none (axios-retry README, read 2026-10-05) — a custom `retryCondition` that admits POST is the defect, and the missing `retryDelay` is the storm. Is a client-generated id in the body (`clientMutationId`) the dedupe key the server uses? Where is the key minted — at enqueue (good) or on the send line (2b, decorative)? **Finding when** a POST or PATCH can be delivered twice and nothing lets the server tell. **Severity:** high; critical for payments and orders. **Proof:** lost-response replay — a proxy or mock server commits the first POST and drops the response; after the client's retry the server count is 2 before the fix and 1 after.

### 3. Ordering and poison

```
BAD:   for (const row of rows) { try { await send(row) } catch { …; continue } }      // the next row may depend on this one
       await Future.wait(_syncQueue.map((op) => api.send(op.path, op.body)));        // parallel: order lost
       while (pending.length) { try { … } catch { await sleep(2000) } }               // no ceiling: the head blocks forever
       persist(…, { name: 'outbox-drafts', version: 2 })                              // no migrate: stored drafts discarded
GOOD:  strict order per entity; attempts column + terminal `failed` state surfaced to the user; payload `version` + migrate
```
**Read the code:** Are the queued rows causally dependent (create then update; delete then re-create)? Then skipping a failed head reorders them; only rows declared independent may be skipped. Does an update reference a temporary id the server has not issued yet (3d)? Where does a row that can never succeed end — a terminal state the user sees, or a silent loop? zustand `persist`: when the stored `version` differs and no `migrate` is given, the stored state is discarded with only a console error (zustand `persist.ts`, read 2026-10-05) — for a store holding an outbox that is silent loss on the next update. The same question applies to a Room, drift or Core Data schema change under queued rows: migrate them, or discard them and tell the user. **Finding when** a failed or old row can reorder, block, or vanish without the user being told. **Severity:** high. **Proof:** offline kill with a poisoned head (the mock answers 4xx for row 1) and with the previous app version's payload; the V159 variants ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Mobile).

### 4. Conflict policy

```
BAD:   onMutate: (n) => qc.setQueryData(['notes'], …)                   // no cancelQueries, no snapshot, no onError
       @PUT("notes/{id}") suspend fun putNote(@Path("id") id: String, @Body note: NoteDto)   // no If-Match, no version
       n.updatedAt = DateTime.now();  …  local.updatedAt.isAfter(remote.updatedAt) ? local : remote
GOOD:  await qc.cancelQueries({ queryKey }); const prev = qc.getQueryData(…); … onError: rollback(prev); onSettled: invalidate
       req.setValue(etag, forHTTPHeaderField: "If-Match")   ·   remote.version >= local.version ? remote : local
```
**Read the code:** Can two devices or two sessions write this entity? A single-writer record needs no conflict machinery, and adding it is `ceremony-without-concurrency` (precedents § 78). Is the policy written down per entity, or inherited from the library? Does an in-flight refetch overwrite the optimistic value — TanStack's guide cancels outgoing refetches in `onMutate` for exactly this. Is `updatedAt` a server timestamp, or a device clock the user can set? **Finding when** a rejected write stays on screen as if accepted, or a stale copy silently overwrites a newer one. **Severity:** high; low when the server merges and the client only lacks a conflict UI. **Proof:** conflict and rollback — the mock answers 409/500: the screen must roll back and say so; two sessions edit offline then sync: the written policy holds.

### 5. Identity bleed

```
BAD:   export async function logout() { await AsyncStorage.removeItem('session'); }   // query cache, persisted store, outbox untouched
       SecItemAdd(q as CFDictionary, nil)   // and nothing wipes the Keychain on a fresh install
GOOD:  queryClient.clear(); await persistor.purge(); await db.runAsync('DELETE FROM outbox'); cancel scheduled work
       on first launch (a flag in UserDefaults / SharedPreferences, which uninstall does clear): wipe the Keychain
```
**Read the code:** Which stores does this root use (the grep prints what is missing by category)? Does logout call a helper that wipes them (read it)? What happens to rows still queued at sign-out — discarded with notice, or drained under the old session first, never replayed under the next account? On iOS, Keychain items survive an uninstall: does a reinstall start signed in as the previous user? Push tokens at logout are `mobile-lifecycle-scan` § 6. **Finding when** account B can see, send or inherit anything of account A. **Severity:** critical when the oracle shows another account's data; high otherwise. **Proof:** identity switch — A signs in, loads, queues a write, signs out; B signs in; inspect the screen, `run-as <pkg> ls databases files shared_prefs`, the simulator container; delete and reinstall on iOS.

### 6. Reachability as truth

```
BAD:   const s = await NetInfo.fetch(); if (!s.isConnected) return;                 // null at cold start; captive portals pass
       if (result.contains(ConnectivityResult.none)) return;  ·  cm.activeNetworkInfo?.isConnected == true
       onlineManager.subscribe((online) => { if (online) queryClient.invalidateQueries(); })   // refetch everything
GOOD:  attempt + queue; treat the flag as a scheduling hint; invalidate only the entity keys the queue touched
```
**Read the code:** Is the flag only driving a banner (precedents § 76) or gating a send? NetInfo's `isConnected` and `isInternetReachable` are `null` until known (NetInfo README, v12.0.1, per the research catalog), so `!isConnected` treats "unknown" as offline at cold start. Does reconnect refetch every query (battery, data, and a clobber risk for pending writes)? TanStack's own `refetchOnReconnect` refetches only active stale queries (precedents § 75). **Finding when** a real send is skipped on a flag, or a reconnect resyncs everything. **Severity:** medium; high when the skipped send is the only drain. **Proof:** cold start offline, then online: the queued write is sent without a relaunch; behind a captive portal the queue holds rather than marking rows sent.

## Proof — the device oracles

The oracle shapes, per stack, and the whole-class variants are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Mobile (offline kill, lost-response replay, identity switch, conflict and rollback); `device-harness` (this pack) boots the device. The offline kill, because it is the one most often run wrong:

```bash
adb shell svc wifi disable && adb shell svc data disable     # airplane mode (Maestro: setAirplaneMode: enabled)
# submit the write in the app, then background it — `am kill` is a no-op on a foreground app
adb shell input keyevent KEYCODE_HOME && adb shell am kill "<application.id>"
adb shell ps -A | grep "<application.id>"                    # must print nothing, else the kill did not land: SKIPPED
adb shell svc wifi enable && adb shell svc data enable       # relaunch from Recents; count the records on the server: exactly 1
```

Never `am force-stop` or Maestro `stopApp` as the kill ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 9 — they discard state by design, and a promised-durable outbox must survive the real kill). "Exactly once" is a server-side count or request log. Each oracle **fails before the fix**. No device: the row is `[report-flagged]`, Unconfirmed, with the run written out — never PASS.

## Output

```
offline-sync-scan — lanes: expo SDK 57 / react-native 0.87, @tanstack/react-query 5.90 + persist-client (expo-app/package.json),
                    flutter 3.47 + hive (flutter_app/pubspec.yaml), androidx.room + work (android-native/app/build.gradle.kts)
Roots: 6 · Device: emulator-5554 (API 35); no iOS simulator → iOS rows Unconfirmed · server dedupe: unconfirmed (backend pack absent)

Findings: 2 · Unconfirmed: 1

1. rn-app/src/sync/outbox.ts:7                                                [report-with-fix]   high
   §1 ram-only-queue — `pendingMutations` is a module array; enqueue() shows "Saved" (outbox.ts:11) and the only drain is
   the orders screen. Proof: offline kill — submit, Home, am kill, relaunch, network on: server count 0 (fails).
   Fix: write-through to the app's AsyncStorage/SQLite outbox before the toast; drain on NetInfo reconnect and app start.

2. expo-app/src/offline/send.ts:6                                             [report-with-fix]   high
   §2 key-regenerated-per-attempt — `Idempotency-Key: uuid()` on the send line; the drain retries (drain.ts:10).
   Proof: mock commits the first POST and drops the response; after the retry the server has 2 orders (fails).
   Fix: send the row's own id (queue.ts:8 mints it at enqueue) as the key.

3. ios-app/Acme/Offline/TokenStore.swift:11                                   [report-flagged]    high
   §5b identity-bleed — the session token is added to the Keychain and nothing wipes it on a fresh install.
   Unproven link: no iOS simulator. Settling run: sign in, delete the app, reinstall, launch — it must start signed out.

Verification: 29 candidates → 2 findings · 1 unconfirmed · 2 hardening · 0 pre-existing · 24 refuted
Routed: push token at logout → mobile-lifecycle-scan §6 · offline copy → ui-state-scan (ui-ux installed)

Class coverage:
  §1  queue durability          checked (11 hits → 1 finding; queue.ts write-through is precedents § 73)
  §2  replay identity           checked (4 hits → 1 finding)
  §3  ordering and poison       checked (5 hits / 4 groups → 0 findings; folded into §1 and §2 roots)
  §4  conflict policy           checked (5 hits → 0 findings; NoteDto is single-writer per its ADR: precedents § 78)
  §5  identity bleed            checked (2 hits → 1 unconfirmed)
  §6  reachability as truth     checked (5 hits → 0 findings; the banner monitor is precedents § 76)
```

`[report-with-fix]`: the promise, the store, the event and the version gate are cited, the oracle failed at the class's tier, and the fix is local. `[report-flagged]`: one link is unproven (no device, a helper not read, server dedupe unconfirmed), and the row names it and the settling run. The coverage block lists **all six** classes on every run: `checked (k hits → m findings)`; `N/A (<reason>)` only when the repo has no such surface (no queue, no optimistic write, no sign-in); `blocked (<reason>)` when a grep failed; `Live, unreviewed (k groups / n hits)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) (§ 3 CNG, § 4 lint, § 7 one finding per root cause, § 9 force-stop is not process death, § 12 a cached repository read) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The offline-specific ones, each with the evidence that flips it back: a write-through buffer (§ 73); idempotent by method (§ 74); library defaults that are safe (§ 75); a reachability flag that drives only a banner (§ 76); one wipe covers all (§ 77); single-writer entities (§ 78); a queue nobody acknowledges (§ 79).

## When to run

- On any diff that adds or changes a queue, outbox, optimistic update, retry wrapper, persisted store, local schema, logout path or connectivity check — the `/mobile-audit` dispatch signal.
- On every whole-repo `/mobile-audit`, reporting all six classes; `@offline-sync-auditor` turns the result into its durability ledger.
- When the field reports duplicated or vanished records, or another account's data after a switch.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) and the O-precedents above. Under `/mobile-audit` that is its verification phase; standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the acknowledgement `<file:line>`, the store (or its absence), the breaking event and the fix.
- Do not call an entity durable without a process-death run that killed the app between enqueue and send; without one it is `unproven`.
- Do not use `am force-stop`, Maestro `stopApp` or a swipe from Recents as the kill.
- Do not assume server-side dedupe: without the backend's confirmation, record `server dedupe: unconfirmed`.
- Do not recommend a retry count, backoff curve, TTL or queue cap as a number; read the value at a `<file:line>` or label it the project's budget.
- Do not print "no offline defect found" without the class-coverage block; a class whose grep did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Route it.

## Related

- `/mobile-audit` dispatches this skill and folds its coverage block into the class ledger; `/mobile-fix` closes findings failing-first and re-runs this detector on the patched line.
- `@offline-sync-auditor` (this pack) judges the candidates per entity (durable / lossy / unproven); `device-harness` runs the D-tier oracles.
- `mobile-lifecycle-scan` (this pack) owns process death, background windows, timeouts and push tokens; `store-compliance-scan` owns account deletion as a store duty.
- `ai-patterns/offline-sync.md`, `native-storage.md`, `mobile-api-contract.md` (this pack) hold the design these classes are checked against.
