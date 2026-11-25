---
name: error-tracking-scan
description: "Tracker fidelity: missing release/env, no process hooks, unsymbolicated builds, uncaptured 500s — test-transport proved."
kind: skill
pack: observability
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: error-tracking-scan

## Premise

An error tracker is the one signal that groups a failure, counts it, ties it to the deploy that caused it and points at the line. It fails quietly in four ways:
- **An init with no `release` or `environment`.** Events carry no deploy, so a regression cannot be tied to the release that shipped it. Staging events can count as production: the Python SDK's environment defaults to `production`.
- **A process with no process-level hook.** A worker's unhandled rejection or a goroutine's panic kills the process. The crash only shows as a restart and a block of stderr text the JSON log store cannot parse.
- **A minified browser build with no source-map upload.** Every frame reads `index-4f2a.js:1:88213`.
- **A global filter that turns every exception into a 500 and neither captures nor logs it.** The tracker sees nothing.

Every one of these passes review, because the init is *there*.

This skill finds those defects in the trackers real repos ship: Sentry (JS 10 browser and Node, NestJS, Python, Go, Java, .NET, Ruby, PHP), Bugsnag, Rollbar, Honeybadger, Datadog RUM and APM error tracking, and the mobile SDKs (Crashlytics, Sentry Android, Sentry React Native). It proves each one with a **tracker test transport**: initialise the SDK as production does, record the event it would send, and assert on its fields. It owns `/obs-audit`'s Error tracking rows §1–§4 (`ownership.json` row `obs-error-tracking`). `@observability-reviewer` (this pack) judges its rows.

**Every finding cites:**
- the init, hook site, build config or handler `<file:line>`;
- the process type or bundle it belongs to;
- what the event lacks (`release`, `environment`, a resolved frame) or never sends;
- the oracle that showed it, or the test that would settle it;
- the fix in the project's own init, build or handler.

A grep hit is a candidate, never a finding. "Error tracking looks fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/observability.md`](../../../../snippets/precedents/observability.md). The oracle is [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability, *Tracker test transport*, variant V202.

## The tracker gate — run before any §

Pre-flight 0a decides whether the repo ships a tracker. Print `gate: open (<file:line> <sdk> <version>)` or `gate: closed (no tracker SDK)` in the header.

**Gate closed.** §1 and §3 print `N/A (no tracker SDK)`. §2 and §4 still run, because their class is "wired to a log **or** a tracker". A process that dies on an unhandled rejection with no hook and no tracker loses the error the same way. "No tracker" is itself a design gap, but it belongs to `/add-telemetry`, not to this detector.

## The rule

A candidate is a finding when all four hold. These are the protocol's gates as `precedents/observability.md` § Reading the seven gates applies them to error tracking.

1. **A production process or bundle reaches it.** The init runs in a process type that 0b names, or in the bundle a production build ships. A dev-only init (`import.meta.env.DEV`, a `*.dev.*` file) and a one-shot CLI are not one (precedents § 30, § 44).
2. **The failure really happens there.** A worker can reject outside a handler, a request can throw past the controllers, and a browser error can occur in a minified frame.
3. **Nothing already supplies it.** None of these is present:
   - `SENTRY_RELEASE` / `SENTRY_ENVIRONMENT` (or the vendor's equivalent) in the manifest production loads (1d);
   - an SDK that installs the hook by default (§ Adapt);
   - a global filter that captures or logs the cause (precedents § 39);
   - debug-ID injection, which matches maps without a release.
4. **The oracle fired.** The test transport shows the event without the field, or the hook never fires. Alternatively, for a static-fact class (an init with no release anywhere, a build with no upload step), both ends are cited: the config production loads and the init or build it feeds. That row stays `[report-flagged]` until the transport runs.

## Boundaries

- **Publicly served source maps** go to security `xss-scan` § 13 when the security pack is installed (precedents P2). A build that emits `.map` files into its public output with no `filesToDeleteAfterUpload` (or a server rule denying `*.map`) is that skill's row. This skill owns only "the tracker cannot symbolicate". `sourcemap: 'hidden'` plus delete-after-upload satisfies both.
- **The tracker DSN in client code is not a secret.** Sentry's DSN page (fetched 2026-10-10) says DSNs only allow submitting new events and give no read access. A browser SDK cannot send events without one. Do not report it, and do not route it to `secret-scan-method`. Event spam through a public DSN is mitigated by inbound filters and rotation, not by hiding the key. A Sentry **auth token** (`SENTRY_AUTH_TOKEN`, `sntrys_…`) in source *is* a secret and goes to security `secret-scan-method`.
- **What an event may carry** (`sendDefaultPii`, `dataCollection`, `include_local_variables`, a `beforeSend` scrubber) goes to security `data-exposure-scan` § 6 when the security pack is installed. JS SDK 10 deprecated `sendDefaultPii` for `dataCollection`, so grep R covers both spellings (precedents § 47). Without the security pack, R rows are tagged `security-class (owner pack not installed)`, listed and never graded.
- **A dropped or swallowed error** (an empty catch, a success-shaped return) goes to code-quality `error-handling-scan` when that pack is installed. §2 here starts only when nothing catches it at all, and §4 only when the boundary maps it to a 5xx.
- **The error log's fidelity** (stack lost, wrong level) belongs to `log-signal-scan` §2 and §4. A boundary that logs without the stack is that skill's row, not §4's.
- **Native symbol upload** (dSYM, R8/ProGuard mapping, `debug-files upload`) is the mobile pack's class (the batch-4 eval's ownership table), but no mobile skill detects it yet. Rows are listed as `mobile-class (no owner detector)` and are not graded here. This skill keeps release, environment and hooks for mobile SDKs.
- **Tracker-based tracing** (`tracesSampleRate`, `traces_sample_rate`) goes to `trace-propagation-scan` § 9 (this pack). Flushing the last event on SIGTERM goes to its § 5.

## Adapt to the codebase — the tracker lanes

Read each SDK and plugin **with its version** from the manifest or lockfile (grep 0a), and print the lanes in the header.

| Lane | SDKs | Default hooks (§2) | Release / environment source (§1) |
|---|---|---|---|
| **Node** (incl. NestJS, Next server) | `@sentry/node`, `@sentry/nestjs`, `@sentry/nextjs` 10; Bugsnag; Rollbar; `dd-trace` | Sentry: `OnUncaughtException` and `OnUnhandledRejection` are auto-enabled (Sentry Node integrations page, 2026-10-10) | `release`, else `SENTRY_RELEASE` on the server; `environment`, else `SENTRY_ENVIRONMENT` |
| **Browser** | `@sentry/react` / `browser` / `vue` / `angular` 10; Datadog RUM; Bugsnag | Global `onerror` / `onunhandledrejection` by default | `release` in code or injected at build time (`release.inject` of the bundler plugin [K?: read the plugin's options at the installed major]); the browser has no process env |
| **Python** | `sentry-sdk` 2; Rollbar; Bugsnag | `sys.excepthook` integration by default; threads and asyncio tasks [K?: integration list at the installed version] | `release`, else `SENTRY_RELEASE`, else auto-detected; `environment` defaults to **`production`** (Sentry Python options, 2026-10-10) |
| **Go** | `sentry-go`, `bugsnag-go` | **None.** A panic in any goroutine ends the process; the HTTP middleware's `recover()` covers only handler goroutines | `ClientOptions.Release` / `Environment`, or `SENTRY_RELEASE` |
| **JVM** | `sentry` (Spring Boot starter), Bugsnag | Uncaught-exception handler; executor tasks keep their exception in the `Future` | `sentry.release` / `sentry.environment` properties |
| **.NET** | `Sentry.AspNetCore` | AppDomain unhandled; `TaskScheduler.UnobservedTaskException` fires only on finalisation | `Release` / `Environment` options or env |
| **Mobile** | Crashlytics, `sentry-android`, `@sentry/react-native` | the SDK's crash handler | Native SDKs derive a release from the app version [K?: per SDK]. Symbol upload: § Boundaries |

**Node without a tracker.** Since Node v15 the default `--unhandled-rejections=throw` turns an unhandled rejection into an uncaught exception when no `unhandledRejection` hook is set (Node CLI docs, 2026-10-10). The process exits, and the stack goes to stderr as text, outside the JSON logger.

**Source maps and debug IDs.** With debug IDs injected (the bundler plugins, or `sentry-cli sourcemaps inject`), Sentry matches a minified file to its map by the ID alone. Creating a release is no longer required for matching (Sentry *Debug IDs* page, 2026-10-10). So a release-name mismatch between build and SDK no longer breaks symbolication. It breaks only release association: regressions, suspect commits and release health. The Vite guide requires map generation to be on (`'hidden'`, `true`, …) and recommends `filesToDeleteAfterUpload` for client builds (Sentry Vite guide, 2026-10-10). sentry-cli 3 has no `sourcemaps explain`. A proof or CI step that names it is a defect (precedents § 49).

## Pre-flight greps

Run as **one** bash script from the repo root (bash 3.2-safe: no `mapfile`). Grep **N** feeds detector **§N**; 0 is context; R is routed. Every `rg` names its path; any exit 2 is a failed grep, never zero hits. File-level negatives use `--files-without-match`, never `rg -L` (that is `--follow`). Browser and mobile packages stay **in** scope here, unlike `log-signal-scan`, because the browser bundle is where §3 lives.

```bash
ROOTS=( . )   # or the service roots from _extracted-codebase.md
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,target,bin,obj,vendor,.venv,venv,__pycache__,coverage,.next,.nuxt,.output,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,playwright,cypress}/**'
   -g '!**/*.{spec,test,e2e,e2e-spec,stories,story}.*' -g '!**/*_test.go' -g '!**/test_*.py' -g '!**/conftest.py'
   -g '!**/{migrations,migration,seeders,seeds,db/migrate,alembic/versions}/**' -g '!**/{locales,locale,i18n,translations,messages,lang}/**'
   -g '!**/{docs,ai,.claude}/**' -g '!*.{md,mdx,snap,lock}' -g '!**/*.min.*' -g '!**/{jest,vitest}.setup.*' -g '!**/setup{Tests,-tests}.*')
J=(-g '*.{ts,tsx,js,jsx,mjs,cjs}'); PY=(-g '*.py'); GO=(-g '*.go'); JV=(-g '*.{java,kt,kts}'); CS=(-g '*.cs'); RB=(-g '*.rb'); PHP=(-g '*.php')
CFG=(-g '*.{yml,yaml,json,toml,env,tf,properties}' -g '**/Dockerfile*' -g '**/Procfile' -g '.env*' -g '!**/node_modules/**' -g '!**/package-lock.json' -g '!**/{docs,ai,.claude}/**')
BUILD=(-g '**/{vite,webpack,rollup,next,nuxt,astro,svelte,remix}.config.*' -g '**/angular.json' -g '**/vue.config.*' -g '**/metro.config.*' -g '!**/node_modules/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#)')   # drops comment-only hit lines
TR='\b(?:Sentry\.(?:init|start)|sentry_sdk\.init|sentry\.Init|SentrySdk\.Init|UseSentry|SentryAndroid\.init|SentrySDK\.start|Bugsnag\.(?:start|configure)|Rollbar\.(?:init|configure)|new\s+Rollbar\s*\(|datadogRum\.init|Honeybadger\.configure|Raven\.config)\s*\('
CAP='captureException|capture_exception|CaptureException|Sentry\.capture|Bugsnag\.notify|\.notify\(|rollbar\.(?:error|critical)|Rollbar\.(?:error|critical)|Honeybadger\.notify|addError\('
# 0a GATE: tracker SDKs, bundler plugins and CLIs with versions (gate 3) — Sentry, Bugsnag, Rollbar, Datadog RUM / APM error tracking, Honeybadger, Crashlytics.
rg -n --no-heading --pcre2 '"(?:@sentry/[\w-]+|@bugsnag/[\w-]+|rollbar|@datadog/browser-(?:rum|logs)|dd-trace|@honeybadger-io/[\w-]+|@sentry/cli|@bugsnag/source-maps|@datadog/datadog-ci)"\s*:|^(?:sentry-sdk|bugsnag|rollbar|ddtrace|honeybadger)\b|getsentry/sentry-go|bugsnag/bugsnag-go|<artifactId>sentry[\w-]*<|io\.sentry:|Sentry(?:\.AspNetCore)?"\s+Version|gem\s+["\x27](?:sentry-\w+|bugsnag|rollbar)|"sentry/sentry(?:-laravel|-symfony)?"|firebase-crashlytics' -g '**/{package.json,requirements*.txt,pyproject.toml,go.mod,pom.xml,build.gradle*,*.csproj,Gemfile,composer.json}' -g '!**/node_modules/**' "${ROOTS[@]}"
# 0b process types and their start commands (§2): Dockerfile CMD / ENTRYPOINT, compose command, Procfile, k8s command, package.json start scripts.
rg -n --pcre2 '^\s*(?:CMD|ENTRYPOINT)\b|^\s*command:\s*\S|^\w[\w-]*:\s+\S|"(?:start(?::\w+)?|worker|cron)"\s*:\s*"' -g '**/Dockerfile*' -g '**/{docker-compose,compose}*.y*ml' -g '**/Procfile' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
# 1a tracker inits; 1b init files with no release; 1c with no environment (read the object: a spread or a factory hides keys); 1d the deploy-side env that supplies them.
INIT=(); while IFS= read -r f; do INIT+=("$f"); done < <(rg -l --pcre2 "$TR" "${X[@]}" "${ROOTS[@]}")
[ ${#INIT[@]} -gt 0 ] && rg -n -H --pcre2 "$TR" "${INIT[@]}" | "${NC[@]}"
[ ${#INIT[@]} -gt 0 ] && rg --files-without-match --pcre2 '\brelease\b|\bappVersion\b|\bcode_version\b|\bversion\s*[:=]' "${INIT[@]}"
[ ${#INIT[@]} -gt 0 ] && rg --files-without-match --pcre2 '\benvironment\b|\breleaseStage\b|\benv\s*:' "${INIT[@]}"
rg -n --pcre2 '\b(?:SENTRY_(?:RELEASE|ENVIRONMENT)|DD_(?:VERSION|ENV)|BUGSNAG_(?:APP_VERSION|RELEASE_STAGE)|ROLLBAR_(?:ENV|CODE_VERSION)|VITE_(?:SENTRY_)?RELEASE|NEXT_PUBLIC_SENTRY_RELEASE)\b' -g '**/.github/workflows/*' "${BUILD[@]}" "${CFG[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2a process-level hooks wired to a log or a tracker; 2b Node server / worker / cron entry files; 2c Go goroutine spawns in files with no recover().
rg -n --pcre2 'process\.on\(\s*["\x27](?:unhandledRejection|uncaughtException)|\b(?:sys|threading)\.excepthook\s*=|set_exception_handler\(|TaskScheduler\.UnobservedTaskException|AppDomain\.CurrentDomain\.UnhandledException|setDefaultUncaughtExceptionHandler\(|Thread\.UncaughtExceptionHandler' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 'NestFactory\.create\w*\s*[<(]|\.listen\(\s*(?:\{|\d|port|PORT|process\.env)|new\s+Worker\s*\(|@Processor\(|cron\.schedule\(|new\s+CronJob\(|consumer\.run\(' "${J[@]}" "${X[@]}" "${ROOTS[@]}"
rg -l --pcre2 '^\s*go\s+(?:func\b|\w+(?:\.\w+)*\()' "${GO[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg --files-without-match --pcre2 '\brecover\(\)'
# 3a builds that emit source maps; 3b upload mechanisms (bundler plugin, sentry-cli, datadog-ci, bugsnag-source-maps); 3c release names on the build side; 3d removed CLI verbs (precedents § 49).
rg -n --pcre2 '\bsourcemap\s*:\s*(?:true|["\x27](?:hidden|inline)["\x27])|\bdevtool\s*:\s*["\x27][\w-]*source-map|\bproductionBrowserSourceMaps\s*:\s*true|"sourceMap"\s*:\s*true|\bGENERATE_SOURCEMAP\s*=\s*true' -g '**/.env*' "${BUILD[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'sentry(?:Vite|Webpack|Rollup|Esbuild)Plugin\(|withSentryConfig\(|@sentry/(?:vite|webpack|rollup|esbuild)-plugin|sentry-cli\s+(?:sourcemaps\s+(?:inject|upload)|debug-files\s+upload)|datadog-ci\s+sourcemaps\s+upload|bugsnag-source-maps\s+upload|filesToDeleteAfterUpload' -g '**/package.json' -g '**/.github/workflows/*' -g '*.{sh,mk}' -g '**/Makefile' "${BUILD[@]}" "${CFG[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 'release\s*:\s*\{[^}]{0,200}?\bname\s*:\s*[^,\n}]+' "${BUILD[@]}" "${ROOTS[@]}"
rg -n --pcre2 'sentry-cli\s+(?:sourcemaps\s+explain|releases\s+files)' -g '**/.github/workflows/*' -g '*.{sh,mk}' -g '**/Makefile' -g '**/package.json' "${CFG[@]}" "${ROOTS[@]}"
# 4a boundary handlers that map an exception to a status (filters, advice, error middleware, framework hooks);
# 4b of those, the files with no tracker capture and no error-level log (read the 5xx branch of each).
BH=(); while IFS= read -r f; do BH+=("$f"); done < <(rg -l --pcre2 '@Catch\(|implements\s+ExceptionFilter|setErrorHandler\(|\(\s*err\w*\s*(?::\s*\w+)?\s*,\s*req\w*\s*(?::\s*\w+)?\s*,\s*res\w*\s*(?::\s*\w+)?\s*,\s*next\b|@(?:Rest)?ControllerAdvice|@ExceptionHandler\(|exception_handler\(|add_exception_handler\(|errorhandler\(|def\s+process_exception\(|handler500\s*=|UseExceptionHandler\(|IExceptionHandler\b|rescue_from\b|->renderable\(|function\s+render\(\s*\$request\s*,\s*Throwable' "${X[@]}" "${ROOTS[@]}")
echo "boundary handlers: ${#BH[@]}"; [ ${#BH[@]} -gt 0 ] && printf '  %s\n' "${BH[@]}"
[ ${#BH[@]} -gt 0 ] && rg --files-without-match --pcre2 "$CAP|\b(?:logger|log|LOG|LOGGER|_log|this\.logger|self\.logger|Log|logging)\.(?:error|exception|critical|fatal|warn(?:ing)?|LogError|LogCritical)\(|\bLog(?:Error|Critical)\(|console\.(?:error|warn)\(|process\.stderr\.write\(|System\.err\.|printStackTrace\(|traceback\.print_exc\(|super\.catch\(|\braise\b|\bthrow\b(?!\s+new\s+HttpException)" "${BH[@]}"
# R routed to security when installed (listed, never graded here): event payload policy (precedents § 47) and maps a build ships to its public output.
rg -n --pcre2 '\b(?:sendDefaultPii|send_default_pii|dataCollection|include_local_variables|includeLocalVariables|beforeSend|before_send)\b' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

A finding is a hit **plus** a read of the init object, the process that loads it and the manifest it reads. Three blind spots are structural:
- **Spread and factory inits.** An init of the form `Sentry.init({ ...baseOptions })` or `init(makeOptions())` hides its keys from 1b/1c. Read the factory once; it settles every caller.
- **Env injected outside the repo** (a platform's build env, a secrets manager). 1d cannot see it. The row stays `[report-flagged]` with "settling: print the event's `release` from the test transport in the deployed image".
- **A boundary that rethrows to a base filter.** `super.catch(…)` hands the error to Nest's `BaseExceptionFilter`, and 4b treats that as handled. Read whether the base logs the 5xx at the installed version before clearing a row that relies on it.

### Measured (2026-10-10, the script above)

| Tree | Hits that matter | Verdict |
|---|---|---|
| Seeded sample: 3 Vite web apps (React 19, `@sentry/react` / `browser` 10.17.0, `@sentry/vite-plugin` 4.3.0), a NestJS 11 API (`@sentry/nestjs` 10.17.0), two BullMQ workers, FastAPI + `sentry-sdk` 2.39.0, Go worker + chi API, Spring advice, a React Native app; 8 seeds + 1 hand-off, 8 decoys; 0.25 s | every seed caught (8/8, hand-off routed) | 1b/1c: `web` (no release, no environment), `py-svc` (neither, and no `SENTRY_*` for it in compose), `mobile` (read: native release default). `api` has no `release`, but 1d shows `SENTRY_RELEASE` in compose: **refuted** (env-only decoy). 2b+2a: `worker` has no hook and no tracker, so it is a candidate; `worker-ok` sets both hooks. 2c: the Go worker's bare goroutines; the chi API's `middleware.Recoverer` is not a goroutine spawn. 3a/3b: `web` emits maps with no upload step (ET-03, plus maps in the public output, routed to security); `web-mismatch` has plugin `release.name` = `GIT_SHA` against SDK `'web-mismatch@1.4.0'`, a release-association row only (Hardening, debug IDs); `web-ok` (`hidden` + delete after upload) stays clean. 4b: 3 of 4 boundary files (Nest `@Catch()`, FastAPI `exception_handler`, Spring `@ControllerAdvice`); the Sentry global filter is excluded. R: `sendDefaultPii: true` routed. The literal DSNs: 0 rows (§ Boundaries) |
| `benchmarks/fixtures/*` (15 trees, about 0.2 s each) | mobile-defects 0a/1a/1b/1c 1 (`SentryAndroid.init` with only a DSN) · brittle-suite / quality-mix / slow-marketplace / vuln-fullstack 2b entry files · node-api 4a 1 · 3a 3 (`sourcemap: true` / `'hidden'`, no tracker) | The Android init is a read: native SDKs derive the release from the app version. The node-api error middleware writes `err.stack` to stderr, so it is logged; it left 4b when stderr writes counted as a log, and its unstructured shape is `log-signal-scan` §3. The three `sourcemap` builds have no tracker, so ET-03 is N/A and their maps are a security row. Two FP classes were removed on the way. A `jest.setup.ts` `server.listen(` (msw) counted as an entry point; setup files are now excluded. A server `tsconfig` `"sourceMap": true` counted as a browser map; tsconfig was dropped from 3a. Excluded trees: 0 hits |
| Real NestJS + Fastify + BullMQ monorepo with a React/Vite web app, read-only; 0.75 s | gate **closed** (no tracker SDK in any manifest) · 2a 0 · 2b 13 entry files (1 API process hosting 8 BullMQ processors, 1 rollup job, 1 CLI) · 4a 3 handlers → 4b 0 | §1 and §3: N/A (no tracker SDK). **§2: 1 candidate.** `main.ts` registers only SIGTERM/SIGINT, and the image runs Node 22, so an unhandled rejection in a processor exits the API with a stderr stack outside pino. It stays `[report-flagged]` until the V202 spawn test runs. §4: all 3 boundary handlers capture or log, refuted at the grep. `git status` was clean after the run |

## The 3,000-hit path

1. **Intersect** with the process map (0b) and the production build list: a tracker init or handler no production process loads is dismissed with one read.
2. **Group** by init factory, by bundle (one Vite config is one group), by process type (§2 is one row per process, never per entry file), and by boundary base class.
3. **Rank** by path: payment, auth, checkout and consumer processes and bundles first, then workers before the API (they have no request to fail loudly).
4. **Read the top 30 groups.**
5. **Run the bulk oracle:** one test-transport run per process type. It boots the real bootstrap with a recording `beforeSend`, throws one handled 500 and one unhandled rejection, and settles §1, §2 and §4 for that process at once.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing grep id>)`. Never mark them `checked`.

## Scans for

Severity is what on-call loses on a reachable path. Raise one step when the process or bundle is the only signal on a payment, auth or consumer path. Drop one step for internal tooling.

| § | Class | Default |
|---|---|---|
| 1 | ET-01 tracker init without `release` / `environment` | medium |
| 2 | ET-02 no process-level hook wired to a log or a tracker | medium; high in a worker or consumer process |
| 3 | ET-03 tracker cannot symbolicate (no upload, no debug IDs); release mismatch | medium; mismatch with debug IDs is Hardening |
| 4 | ET-04 boundary handler maps to 5xx with no capture and no log | medium; high when it is the only signal on a critical path |

### 1. Tracker init without `release` or `environment` (ET-01)

```
BAD:   Sentry.init({ dsn }) in the browser bundle   ·   sentry_sdk.init(dsn=…) with no SENTRY_RELEASE / SENTRY_ENVIRONMENT in the manifest
GOOD:  Sentry.init({ dsn, release: import.meta.env.VITE_RELEASE, environment: import.meta.env.MODE })
       Node: environment in code + SENTRY_RELEASE=api@${GIT_SHA} in the manifest production loads (env-only is fine)
```
**Read the code:**
- Which process or bundle loads this init, and which manifest feeds its env (1d, gate 7)?
- Server SDK: does the production manifest set `SENTRY_RELEASE` / `SENTRY_ENVIRONMENT`? Then it is no finding.
- Browser: is the release injected at build time (a `define`, the plugin's `release.inject`)? There is no process env at runtime.
- Is `environment` a fixed string (`'production'`) in a bundle that also deploys to staging?
- Mobile: does the native SDK default the release from the app version?

**Finding when** the event a production process sends carries no release, or an environment that does not tell the deploy apart. **Proof (V202):** test transport, as below. Boot with the production env, send one event, and assert `event.release` and `event.environment` equal the deploy's values.

### 2. No process-level hook (ET-02)

```
BAD:   a BullMQ worker process with no process.on('unhandledRejection') and no tracker  ·  go func(){ for { process(ctx) } }() with no recover()
       a Python worker on asyncio with no loop exception handler and no tracker integration
GOOD:  process.on('unhandledRejection', (r) => logger.fatal({ err: r }, 'unhandled rejection'))  (then exit or let the SDK)
       @sentry/node / @sentry/nestjs loaded first in that process (auto-enabled hooks)  ·  defer func(){ if r := recover(); r != nil { … } }() in each goroutine body
```
**Read the code:**
- Which process types exist (0b)? Judge **each**: API, worker, cron, consumer. A worker sharing the API process shares its hooks.
- Does a tracker SDK that installs the hooks by default load **in this process**, and early enough (before the work starts)?
- Does the hook log at fatal with the error object and then exit, or swallow and keep running in an unknown state? The second is code-quality's (§ Boundaries).
- Go: does each goroutine body recover, or does a supervisor restart the process and alert on the restart?

**Finding when** a production process can die, or lose a task, on an error that reaches no log line at error or fatal and no tracker event. **Proof (V202):** spawn the real process type with the test transport (or a captured logger). Raise an unhandled rejection or panic in a spawned task, then assert one event or one fatal JSON line carrying the stack. It fails on the unfixed code.

### 3. Tracker cannot symbolicate; release mismatch (ET-03)

```
BAD:   build: { sourcemap: true } with no sentryVitePlugin / sentry-cli sourcemaps inject+upload step  ·  a CI step calling `sentry-cli sourcemaps explain` (removed in 3.0)
GOOD:  build: { sourcemap: 'hidden' } + sentryVitePlugin({ sourcemaps: { filesToDeleteAfterUpload: ['./dist/**/*.map'] } })
       or: sentry-cli sourcemaps inject dist && sentry-cli sourcemaps upload --release "$RELEASE" dist  (sentry-cli 3.x)
```
**Read the code:**
- Does the production build emit maps at all (3a)? Without maps there is nothing to upload: the fix is the build flag plus the upload.
- Is there an upload step (3b) in the build config, `package.json` scripts or CI, and does it run on the production build?
- Are debug IDs injected (the plugins do; `sourcemaps inject`)? Then a release mismatch (3c vs 1a) is release association only: Hardening.
- Are the maps then left in the public output? That half is security's (§ Boundaries).

**Finding when** a production bundle reports minified frames: maps not generated, not uploaded, or matched by neither debug ID nor release. **Proof (V202, L-tier):** one backend event shows resolved frames. Without a backend the row is `NO-DATA(tracker)` with the upload command written out. The static half (no upload step for a bundle that ships a tracker) is two-ended and stays `[report-flagged]`.

### 4. Boundary maps to 5xx without capture or log (ET-04)

```
BAD:   @Catch() filter → reply.status(500).send(…) and nothing else  ·  @ExceptionHandler(Exception.class) → ResponseEntity 500  ·  FastAPI exception_handler → JSONResponse(500)
GOOD:  if (status >= 500) { Sentry.captureException(exception); this.logger.error({ err: exception }, 'unhandled'); }   ·   super.catch(exception, host) to a base that logs
```
**Read the code:**
- Does the 5xx branch capture (`captureException`, `notify`) or log at error with the error object?
- Does the SDK's own framework integration capture before this handler runs, for example Sentry's Nest global filter or a Spring integration? Check that it is registered.
- Does a 4xx branch log at error? That is `log-signal-scan` §4, not this §.

**Finding when** a request that fails with a 5xx through this handler leaves no tracker event and no error log. **Proof (V202):** drive a throwing route through the real app (`fastify.inject`, `TestClient`, `MockMvc`). Assert one transport event (or one captured error line) per 500, and none for a 404.

## Proof — the tracker test transport

[`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability, *Tracker test transport* (V202):
- Initialise the SDK through the project's own init: the same file and the same env as production.
- Record events with a `beforeSend` / `before_send` that stores the event and returns `null` / `None`, or with the SDK's test transport.
- Then assert, per process type:
  - the event carries `release` and `environment` (§1);
  - an unhandled rejection or panic raised in a spawned child of the real process reaches it, or reaches a fatal JSON line when no tracker exists (§2);
  - a boundary 500 sends exactly one event and a 404 sends none (§4).
- Symbolication (§3) is L-tier: one backend event shows resolved frames. Otherwise `NO-DATA(tracker)` with `sentry-cli sourcemaps inject <dist> && sentry-cli sourcemaps upload --release <release> <dist>` written out.

A mocked SDK proves what was called, not what was sent; use one only for a façade with no transport. A fix is accepted only when all of these hold:
- the transport goes green on every process type of the group;
- the 404 control stays silent;
- the owning grep goes quiet;
- for an init or `beforeSend` change, security's canary (`data-exposure-scan` § 6) still passes.

Never accepted: `enabled: false` or a DSN removed to quiet the test, `sampleRate: 0`, a `beforeSend` that drops all events, or `ignoreErrors: [/.*/]`.

## Output

```
error-tracking-scan — gate: open (web/package.json:2 @sentry/react 10.17.0; api/package.json:2 @sentry/nestjs 10.17.0; py-svc/requirements.txt:2 sentry-sdk 2.39.0)
Lanes: browser (vite 7.1.5, @sentry/vite-plugin 4.3.0 in 2 of 3 apps), node (nest 11 on fastify), python (fastapi), go (no tracker), jvm (spring), mobile (react-native)
Processes: api (compose:2), worker (compose:12), py-svc (compose:8), go worker, go api

Findings: 2 · Unconfirmed: 3 · Hardening: 1

1. api/src/filters/catch-all.filter.ts:6                             [report-with-fix]   medium
   §4 ET-04 — @Catch() maps every non-HttpException to 500 and sends a body; no capture, no log.
   Proof: test/obs/tracker.e2e-spec.ts — GET /boom → 500, 0 transport events (fails). Fix: capture + logger.error({ err }) on status ≥ 500.

2. worker/src/main.ts:5 (process: worker, compose:12)               [report-with-fix]   high
   §2 ET-02 — BullMQ worker process with no unhandledRejection hook and no tracker; Node 22 exits with a stderr stack.
   Proof: spawn + rejected detached promise → exit 1, 0 JSON lines at fatal (fails). Fix: process.on hooks logging { err } at fatal.

3. web/src/sentry.ts:4 · web/vite.config.ts:6                        [report-flagged]    medium
   §1 ET-01 + §3 ET-03 — browser init with no release/environment; the build emits maps with no upload step.
   Unproven link: no backend. Settling: transport event fields; NO-DATA(tracker) for frames.

4. py-svc/app/main.py:5                                               [report-flagged]    medium
   §1 ET-01 — no release/environment and no SENTRY_* for py-svc in compose; environment defaults to production.

5. go-svc/cmd/worker/main.go:12                                       [report-flagged]    medium
   §2 ET-02 — goroutines without recover(); a panic ends the worker. Settling: V202 panic test.

Hardening: web-mismatch/vite.config.ts:6 — plugin release GIT_SHA ≠ SDK 'web-mismatch@1.4.0' (debug IDs resolve frames; release association only)
Routed: api/src/instrument.ts:6 sendDefaultPii → security data-exposure-scan § 6 · web/vite.config.ts:6 maps in dist → security xss-scan § 13

Verification: 17 candidates → 2 findings · 3 unconfirmed · 1 hardening · 0 pre-existing · 11 refuted (self-verified)

Class coverage:
  gate  tracker SDK                 open (3 SDKs, 5 process types, 3 browser builds)
  §1  release / environment (ET-01)  checked (6 inits → 2 unconfirmed; api env-only refuted; web-ok clean; mobile: native default)
  §2  process hooks (ET-02)          checked (5 processes → 1 finding, 1 unconfirmed; api: SDK hooks; worker-ok hooks)
  §3  symbolication (ET-03)          checked (3 builds → 1 unconfirmed, 1 hardening) · frames NO-DATA(tracker)
  §4  boundary capture (ET-04)       checked (4 handlers → 1 finding, 2 unconfirmed; Sentry global filter clean)
```

`[report-with-fix]`: the process or bundle is traced, the transport (or capture) test failed, and the fix is local to the project's init, build or handler. `[report-flagged]`: one link is unproven (no harness, env injected outside the repo, no backend for frames); the row names it and the settling test.

The coverage block lists the gate and **all four** §s on every run:
- `checked (k hits → m findings)` only when the greps ran on present surfaces;
- `N/A (no tracker SDK)` for §1 and §3 on a closed gate (§2 and §4 still run);
- `blocked (<reason>)` when a grep failed;
- `NO-DATA(tracker)` for the frame half of §3;
- `Live, unreviewed (k groups / n hits)` for a partial review, never `checked`.

## False positives / precedents

The verifier reads [`precedents/observability.md`](../../../../snippets/precedents/observability.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10. The ones this skill meets most:
- **An env-only release** (`SENTRY_RELEASE` in the manifest production loads) is not ET-01. Gate 7 decides which manifest that is.
- **A literal DSN in client code** is not a finding of any kind (§ Boundaries).
- **A global filter that captures or logs the cause** clears its route's ET-04 (§ 39). Two captures of one error is noise, not ET-04.
- **A dev-only init or config** is noise (§ 30). Only what production loads counts.
- **`process.exit` in a CLI's error path** is not ET-02 (§ 44).
- **`sendDefaultPii` / `dataCollection`** is security's verdict (§ 47, P2).
- **`sentry-cli sourcemaps explain`** in a proof is a proof defect (§ 49). Use `sourcemaps inject` + `upload`.
- **"We log the message, the stack is in Sentry"** is accepted only with the capture shown on that path (rationalizations).
- **A release mismatch with debug IDs injected** is release association, not symbolication: Hardening.
- **"Noisy tracker" or "too many events"** is behavioural: `NO-DATA(tracker)` without the project's event counts (§ 36).

## When to run

- On any diff that touches a tracker init, a bundler or build config, a CI build or release step, a process entry point or start command, or a global exception filter, advice or error middleware. This is `/obs-audit`'s "a tracker init or bundler config" dispatch signal.
- On every whole-repo `/obs-audit`, reporting the gate and all four §s.
- After `/add-telemetry` wires a tracker: the transport test is its acceptance check.

## Halt conditions

- **A high or critical row needs a separate refuter.** Do not report it as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10.
  - Under `/obs-audit`, that happens in its verification phase.
  - Run standalone, apply the protocol as a separate second pass and tag those rows `self-verified`.
  - List the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- **Halt before any § when the gate is unread.** Without the 0a result printed, no §1 or §3 row may be graded.
- **Halt on any finding missing its anchors:** the `<file:line>`, the process type or bundle, the manifest that feeds it, and the fix in the project's own init, build or handler.
- **No `[report-with-fix]` without a transport or capture test that failed.** Without one, the row is `[report-flagged]` / Unconfirmed.
- **Do not assert an SDK's default hooks, release detection or environment default from memory.** Cite the installed version and the fetched page, or run the transport.
- **Do not grade a DSN, an auth token, an event payload policy or publicly served maps.** Route them (§ Boundaries).
- **Do not print "error tracking looks fine".** Print the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/obs-audit` dispatches this skill and folds its block into the Error tracking ledger row. `/obs-fix` closes findings with the failing-first transport test, the fix at the init or base filter, a re-run of this detector, and the sibling search.
- `log-signal-scan` (error-log fidelity, levels) and `trace-propagation-scan` (§5 flush, §9 tracker sampling) are this pack's neighbours. `@observability-reviewer` judges these rows.
- `data-exposure-scan` § 6, `xss-scan` § 13 and `secret-scan-method` (security, when installed), `error-handling-scan` (code-quality, when installed): § Boundaries. Native symbol upload has no owner detector yet (§ Boundaries).

## Sources

Fetched 2026-10-10:
- Sentry *DSN explainer*: a DSN is safe to keep public and allows event submission only.
- Sentry JS Node options: `release` / `SENTRY_RELEASE`, `environment` / `SENTRY_ENVIRONMENT`, `dataCollection` from 10.57.0.
- Sentry Node integrations: `OnUncaughtException` and `OnUnhandledRejection` are auto-enabled.
- Sentry Python options: `environment` defaults to `production`.
- Sentry *Debug IDs*: matching needs no release.
- Sentry Vite source-map guide: maps must be generated; `filesToDeleteAfterUpload`.
- Node.js CLI docs: `--unhandled-rejections`, default `throw` since v15.

Carried from the observability research catalog and the batch-4 eval: the ET-01..ET-04 class rows, sentry-cli 3.0.0's removal of `sourcemaps explain` and the tool versions. Paraphrased; no text is reproduced beyond identifiers.
