---
name: sast-scan
description: Runs the static analyzers that exist for the stack — semgrep, the language's security linter, gitleaks — records every tool as RAN or SKIPPED, and triages each hit to a confirmed file:line finding or a cited false positive. A tool that did not run is a coverage gap, never a pass.
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash, Write]
---

# Skill: sast-scan

## Premise

The class detectors in this pack (`injection-scan`, `xss-scan` and their siblings) are grep-and-read taint traces, and `secret-scan-method` / `deps-audit` run tools for their own narrow classes. This skill **runs the general-purpose static analyzers** — semgrep plus the stack's own security linter — so its output has two halves, and a run that delivers only one has not finished:

1. **A tool ledger.** Every analyzer the stack calls for gets one row: **RAN** (version, exit code, files scanned, raw hit count, output path), **SKIPPED** (with the reason — `n/a` only when pre-flight grep 1 proves the lane's language is absent; `errored` / `declined` otherwise), or **NOT-INSTALLED** (with the exact one-shot or install command printed). A tool that did not run is a coverage gap, never a pass: `/security-audit` § Phase 2 — Organize turns every non-`n/a` SKIPPED or NOT-INSTALLED row into a `COVERAGE:` gap, and a coverage gap forces `GO-UNVERIFIED`.
2. **A triage of every hit.** Each one ends as a **confirmed finding** — `<file:line>` + the tainted source or failing condition + the fix + severity + the detector skill that owns the class — or a **false positive with a cited reason**. "semgrep flagged it" is not a finding, and "semgrep found nothing" is not a clean bill: on this skill's own test sample `pickle.loads(request.data)` passed `p/python` + `p/flask` while bandit B301 caught it.

Ground rules:
- **The audit installs and downloads nothing.** Use the project's own pinned tool, a binary already on PATH, or a scanner image that is already local (`docker run --pull=never`). No one-shot downloader (`uvx`, `pipx run`, `npx -y`, `go run …@latest`, a `docker run` that pulls). An absent tool's row is NOT-INSTALLED with the exact install command (`brew`, `pipx install`, `gem install`, `docker pull`) printed for the user, not run.
- **Output goes to a scratch dir outside the repo** (`$SCAN`, created at the top of § Scans for). Never write scanner config into the repo — no `.semgrep.yml`, no ESLint config, no `psalm.xml`, no `composer require`. The only repo write this run feeds is the summary `/security-audit` writes in its Phase 5.
- **Not this skill's lanes:** committed secrets are `secret-scan-method`'s (§ 9 dispatches it — gitleaks is not re-run here); lockfile CVEs are `deps-audit`'s; Dockerfile / manifest / Terraform / CI-workflow rules are `iac-scan`'s.

## Adapt to the codebase

One row per language the repo actually contains (grep 1). The semgrep rulesets below were fetched from the registry on 2026-10-01; the ones marked † answer `200` but serve **few or no rules** to an anonymous fetch.

| Lane | semgrep `--config` (always add `p/owasp-top-ten p/secrets`) | Native security analyzer | Suppression pragma to inventory |
|---|---|---|---|
| **Node / TS** — Express, NestJS | `p/javascript p/typescript p/nodejs`; `p/expressjs` with Express only (`p/nestjs` †0 rules) — NestJS on Fastify gets **no** framework ruleset, so guard and permission decorators, `ValidationPipe` options (`whitelist` / `forbidNonWhitelisted`) and `@Public` routes are left to `@api-security-reviewer` and `@auth-reviewer` | `eslint-plugin-security` + `eslint-plugin-no-unsanitized` (§ 2) | `eslint-disable … security/*` · `no-unsanitized/*` · `no-restricted-*` and local-plugin rules (§ 10) · `nosemgrep` |
| **React / Next** | add `p/react` (†4 rules; `p/nextjs` †0) | same ESLint run — `no-unsanitized` covers the DOM sinks | same |
| **Vue / Nuxt, Angular, Svelte** | `p/javascript p/typescript` only — `p/vue`, `p/angular`, `p/svelte`, `p/nuxt` do not exist (404) | the project's own `vue/no-v-html` / `svelte/no-at-html-tags` if configured; the real raw-HTML coverage is `xss-scan` | `eslint-disable vue/no-v-html` |
| **Python** — Django, FastAPI, Flask | `p/python` + `p/django` / `p/flask` (`p/fastapi` †1 rule) | `bandit`; `ruff --select S` when the project lints with ruff (§ 3) | `# nosec` · `# noqa: S###` |
| **Go** | `p/golang` | `gosec` (§ 4) | `#nosec G###` · `//nolint:gosec` |
| **Java / Kotlin** — Spring | `p/java` / `p/kotlin` (`p/findsecbugs` is a semgrep port, not the analyzer) | SpotBugs + FindSecBugs on compiled classes (§ 5) | `@SuppressFBWarnings` · SpotBugs exclude filter |
| **Ruby / Rails** | `p/ruby` (+ `p/brakeman` port; `p/rails` does not exist) | `brakeman` (§ 6) | `config/brakeman.ignore` |
| **PHP / Laravel** | `p/php` + `p/phpcs-security-audit` (`p/laravel` does not exist) | Psalm `--taint-analysis` (§ 7) — PHPStan has no taint engine and does not fill this lane | `@psalm-suppress Tainted*` · `@psalm-taint-escape` |
| **C# / .NET** | `p/csharp` | Roslyn NetAnalyzers, security category (§ 8) | `#pragma warning disable CA####` · `[SuppressMessage("Security", …)]` · `.editorconfig` severity `none` |

Before trusting a ruleset name you have not used, count its rules — a `404` aborts the **whole** scan (exit 7) and a `200` with zero rules is a lane that silently scans nothing. The registry serves some rulesets as YAML and others as JSON (`p/owasp-top-ten` is JSON), so a `^- id:` count alone reads its ~560 rules as zero:

```bash
curl -s "https://semgrep.dev/c/p/<name>" -o "${TMPDIR:-/tmp}/rs.txt"
jq -r 'if .error then "no such ruleset" else (.rules | length) end' "${TMPDIR:-/tmp}/rs.txt" 2>/dev/null || grep -c '^- id:' "${TMPDIR:-/tmp}/rs.txt"
```

Counted on 2026-10-02: `p/typescript` serves the same 74 rule ids as `p/javascript`, and all 36 of `p/nodejs` are among them — passing all three adds no rules, so the ledger counts 74, not 184.

`--config auto` is the fallback when no lane row fits, but it needs network **and** refuses to run with `--metrics=off` (exit 2, "Cannot create auto config when metrics are off") — so it sends usage metrics. Say so in the ledger when you use it.

## Pre-flight greps

Run from the repo root. They decide which lanes run, what the project already wires, and what it has told its scanners to hide. Every `rg` names its path (`.`) explicitly — with no path and a non-terminal stdin (an agent harness, a CI step), `rg` searches stdin and waits forever.

```bash
# 1. Lane detection — source files per language; generated, vendored and prior-audit trees excluded.
rg --files . -g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' \
  -g '!/ai/{audits,design}/**' | sed -nE 's/.*\.(js|jsx|mjs|cjs|ts|tsx|vue|svelte|py|go|java|kt|rb|php|cs)$/\1/p' | sort | uniq -c

# 2. Framework signals — which optional rulesets and analyzers apply.
rg -n -i -g 'package.json' -g 'pyproject.toml' -g 'requirements*.txt' -g 'Pipfile' -g 'Gemfile' -g 'composer.json' \
  -g 'pom.xml' -g 'build.gradle*' -g '*.csproj' -g '!**/node_modules/**' \
  -e '"(express|@nestjs/core|next|react|vue|nuxt|@angular/core|svelte|@sveltejs/kit)"\s*:' \
  -e '^\s*(django|fastapi|flask)\b' -e '\b(django|fastapi|flask)\s*[=<>~]' -e 'gem [\x22\x27]rails' \
  -e 'laravel/framework' -e 'spring-boot' -e 'Microsoft\.AspNetCore' .

# 3. What the project already runs — its own config and CI wiring is the lane to prefer.
rg --files --hidden . -g '.semgrep.y*ml' -g '.semgrep/**' -g '.semgrepignore' -g '.bandit' \
  -g 'bandit.y*ml' -g 'eslint.config.*' -g '.eslintrc*' -g 'psalm.xml*' -g 'phpstan.neon*' -g 'brakeman.ignore' \
  -g '*spotbugs*.xml' -g '.golangci.y*ml' -g '.editorconfig' -g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' \
  -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' -g '!.git/**'
rg -n -i --hidden -g '*.y*ml' -g 'package.json' -g 'pom.xml' -g '*.gradle*' -g '*.csproj' -g 'composer.json' -g 'Gemfile' \
  -g 'pyproject.toml' -g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' \
  -g '!**/target/**' -g '!.git/**' 'semgrep|bandit|gosec|golangci|brakeman|psalm|spotbugs|findsecbugs|eslint-plugin-(security|no-unsanitized)|codeql|SecurityCodeScan|NetAnalyzers' .

# 4. Suppression pragmas on security rules — every hit is surfaced (§ 10). 4b inventories every rule an
#    eslint-disable names in code: a project's own guard (a no-restricted-* selector, a local plugin rule) shows up here.
#    Only a directive (`//` or `/*` right before it): prose and strings that mention one are not suppressions (22 → 14 rows
#    on a real monorepo, 2026-10-15; the 8 dropped were config comments and test strings).
rg -n --hidden --pcre2 -g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' \
  '(nosemgrep|#\s*nosec\b|nolint:[\w,]*gosec|eslint-disable[^\n]*\b(security|no-unsanitized)/|eslint-disable[^\n]*\bno-restricted-(syntax|imports|properties|globals)\b|noqa:[\s\w,]*\bS\d{3}|@SuppressFBWarnings|@psalm-suppress\s+Tainted|@psalm-taint-escape|#pragma warning disable[\s\w,]*\b(CA(2100|3\d{3}|5\d{3})|SCS\d{4})|SuppressMessage\(\s*"Security")' .
rg -o --no-filename --pcre2 -g '*.{js,jsx,mjs,cjs,ts,tsx,mts,cts,vue,svelte}' -g '!**/node_modules/**' -g '!**/dist/**' \
  '(?://|/\*)\s*eslint-disable(?:-next-line|-line)?\s+\K[^*\n]+?(?=\s*(--|\*/|$))' . | tr ',' '\n' | sed 's/^ *//; s/ *$//' | sort | uniq -c | sort -rn

# 5. Suppression by exclusion — paths, rules and fingerprints the scanners were told to skip.
rg -n --hidden --pcre2 -g '.semgrepignore' -g '.eslintignore' '^(?!\s*(#|$)).+' .
rg -n --hidden --pcre2 -g '.bandit' -g 'bandit.y*ml' -g 'pyproject.toml' -g 'brakeman.ignore' -g '.editorconfig' \
  -g 'eslint.config.*' -g '.golangci.y*ml' -g '!**/node_modules/**' \
  '\b(exclude_dirs|skips)\b|"fingerprint"|dotnet_diagnostic\.(CA(2100|3\d{3}|5\d{3})|SCS\d{4})\.severity\s*=\s*(none|silent|suggestion)|^\s*ignores\s*:|exclude-rules|excludes:\s*\[?\s*G\d{3}' .

# 6. Hidden Unicode in AI context files — the files an agent loads as instructions (the learning pack's KN-35
#    handover; its context-load-scan §5 prints the list). Overrides, isolates, zero-widths and tag characters only:
#    LRM / RLM (U+200E/F) inside Arabic or Hebrew prose are legitimate and never matched (precedents/learning.md P-26).
#    --no-ignore: a gitignored CLAUDE.local.md is still loaded every session.
rg -n --hidden --no-ignore --pcre2 -g '**/{CLAUDE,CLAUDE.local,AGENTS,GEMINI}.md' -g '**/.cursor/rules/**' -g '**/.cursorrules' -g '**/.github/copilot-instructions.md' \
  -g '**/.github/instructions/**' -g '**/ai/**/*.md' -g '**/.claude/**/*.md' -g '!**/node_modules/**' \
  '[\x{202A}-\x{202E}\x{2066}-\x{2069}\x{200B}-\x{200D}\x{2060}\x{FEFF}\x{E0000}-\x{E007F}]' .
```

The greps choose lanes and list pragmas; they find no vulnerabilities. A row in the findings list is a tool hit **plus** a read of the enclosing function (§ Triage).

## Scans for

Each lane below is one ledger row. Start every run with the scratch dir:

```bash
SCAN="$(mktemp -d "${TMPDIR:-/tmp}/sast-scan.XXXXXX")"; echo "$SCAN"     # outside the repo; every tool writes here
```

### 1. semgrep — the cross-language pass

```bash
CONFIGS=(--config p/owasp-top-ten --config p/secrets --config p/javascript --config p/typescript --config p/nodejs)  # from the lane table
EXCL=(--exclude node_modules --exclude vendor --exclude dist --exclude build --exclude .next --exclude target \
      --exclude coverage --exclude '*.min.js' --exclude fixtures --exclude __fixtures__ --exclude testdata)
semgrep scan --metrics=off "${CONFIGS[@]}" "${EXCL[@]}" \
  --json-output="$SCAN/semgrep.json" --sarif-output="$SCAN/semgrep.sarif" > "$SCAN/semgrep.txt"; echo "exit=$?"
# The same scan with inline suppressions disabled — the difference is what `nosemgrep` hides (§ 10):
semgrep scan --metrics=off --disable-nosem "${CONFIGS[@]}" "${EXCL[@]}" --json-output="$SCAN/semgrep-nosem.json" > /dev/null
```

Not installed → the `semgrep/semgrep` image, only when it is already local: `docker run --pull=never --rm -v "$PWD:/src:ro" -w /src semgrep/semgrep semgrep scan … --json > "$SCAN/semgrep.json"` (stdout, so nothing is written through the mount). Neither → NOT-INSTALLED; install for later: `brew install semgrep` / `pipx install semgrep` (Python ≥ 3.10).

Read it before believing it — the exit code says almost nothing:
```bash
jq '(.paths.scanned | length), (.errors | length)' "$SCAN/semgrep.json"        # files scanned (must be > 0), errors (account for every one)
jq -r '.errors[] | "\(.type | if type == "array" then .[0] else . end)\t\(.path // .spans[0].file // "?")"' "$SCAN/semgrep.json" \
  | awk -F'\t' '{c = ($2 ~ /(^|\/)(tests?|__tests__|e2e)\/|\.(test|spec|stories)\./) ? "test" : ($2 ~ /^(\.|ai\/)|(^|\/)(scripts|tools|bin)\//) ? "tooling" : "prod"; print $1, c}' | sort | uniq -c
jq -r '.results[] | "\(.path):\(.start.line)  \(.check_id | split(".") | last)  \(.extra.severity)"' "$SCAN/semgrep.json"
diff <(jq -r '.results[] | "\(.path):\(.start.line) \(.check_id)"' "$SCAN/semgrep.json" | sort) \
     <(jq -r '.results[] | "\(.path):\(.start.line) \(.check_id)"' "$SCAN/semgrep-nosem.json" | sort) | sed -n 's/^> //p'
```
```
BAD:   semgrep — clean, 0 results              // exit 7: p/rails 404'd; the JSON holds results: [] and two errors
GOOD:  semgrep 1.178.0  RAN  exit 0  214 files  7 rulesets  14 hits (+2 behind nosemgrep)  → $SCAN/semgrep.json
```

### 2. JS / TS — eslint-plugin-security + eslint-plugin-no-unsanitized

If grep 3 shows the project's ESLint config already loads both plugins, run it as-is: `npx --no eslint -f json -o "$SCAN/eslint.json" .`. That needs the project's `node_modules`; without them (a fresh worktree, an install you were not cleared to run) the row is `project eslint — SKIPPED (no node_modules; install declined)`, and the project's own security rules — a tenant guard written as a `no-restricted-syntax` selector or a local plugin — are then covered only by § 10's inventory of their disables. Either way, read the config's `plugins: { <name>: … }` entries and every `no-restricted-*` whose `message` names a security property (tenant, raw SQL, `innerHTML`, secrets): those are SAST rules the project wrote itself. Otherwise run the two plugins from a toolchain the user installed once (`$REFRACT_SAST_LINT`, default `~/.cache/refract/sast-lint`), with the config in `$SCAN` — the audit never installs it; absent, the row is NOT-INSTALLED with the exact command:

```bash
T="${REFRACT_SAST_LINT:-$HOME/.cache/refract/sast-lint}"; E="$SCAN/eslint"; mkdir -p "$E"
if [ -x "$T/node_modules/.bin/eslint" ]; then ln -s "$T/node_modules" "$E/node_modules"
else echo "eslint-security NOT-INSTALLED (to enable: mkdir -p \"$T\" && cd \"$T\" && echo '{\"private\":true}' > package.json && npm i --no-audit --no-fund eslint@9 eslint-plugin-security eslint-plugin-no-unsanitized typescript-eslint typescript)"; fi
cat > "$E/eslint.security.mjs" <<'EOF'
import security from 'eslint-plugin-security';
import nounsanitized from 'eslint-plugin-no-unsanitized';
import tseslint from 'typescript-eslint';
export default [
  { ignores: ['**/node_modules/**', '**/vendor/**', '**/dist/**', '**/build/**', '**/.next/**', '**/coverage/**', '**/*.min.js'] },
  { files: ['**/*.{js,jsx,mjs,cjs,ts,tsx,mts,cts}'],
    languageOptions: { parser: tseslint.parser, parserOptions: { ecmaFeatures: { jsx: true } } } },
  security.configs.recommended,
  nounsanitized.configs.recommended,
];
EOF
[ -e "$E/node_modules" ] && "$E/node_modules/.bin/eslint" --no-config-lookup -c "$E/eslint.security.mjs" --report-unused-disable-directives-severity off \
  -f json -o "$SCAN/eslint.json" .; echo "exit=$?"
```

```bash
jq 'length' "$SCAN/eslint.json"     # files linted — compare with the next line; a gap is unlinted code
rg --files --hidden --no-ignore-vcs -g '!.git' -g '*.{js,jsx,mjs,cjs,ts,tsx,mts,cts}' -g '!**/node_modules/**' -g '!**/vendor/**' \
  -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/coverage/**' -g '!**/*.min.js' . | wc -l   # ESLint 9 lints dot-dirs and ignores .gitignore
jq -r '.[] | .filePath as $f | .messages[] | select(.fatal == true) | "\($f):\(.line)  PARSE-ERROR  \(.message)"' "$SCAN/eslint.json"
jq -r '.[] | .filePath as $f | .messages[] | select(.ruleId != null and (.message | startswith("Definition for rule") | not)) | "\($f):\(.line)  \(.ruleId)"' "$SCAN/eslint.json"
jq -r '.[] | .filePath as $f | .suppressedMessages[] | "\($f):\(.line)  \(.ruleId)  justification=\(.suppressions[0].justification)"' "$SCAN/eslint.json"
```
A message with a null `ruleId` and no `fatal` is ESLint 9's "Unused eslint-disable directive" notice, not a parse error — the flag above turns it off. "Definition for rule '…' was not found" is an inline directive naming a rule the scratch config does not load; it is not a hit. `--no-inline-config` would silence both, but it also empties `suppressedMessages`, the reveal § 10 relies on — keep inline config on.
```
BAD:   eslint security — 0 problems          // the config had no `files` entry for .ts; 0 of 312 TS files were linted
GOOD:  eslint security  RAN  exit 1  312/312 files  9 hits  2 suppressed (no justification)
```

### 3. Python — bandit (or ruff's `S` rules)

```bash
EXCL_PY=./node_modules,./vendor,./.venv,./venv,./build,./dist,./tests
bandit -r . -x "$EXCL_PY" -f json -o "$SCAN/bandit.json" -q; echo "exit=$?"
bandit -r . -x "$EXCL_PY" -f json -o "$SCAN/bandit-nosec.json" -q --ignore-nosec      # what `# nosec` hides
# ruff projects (grep 3), ruff installed: ruff check --select S --output-format json --exit-zero . > "$SCAN/ruff-s.json"   (+ a pass with --ignore-noqa)
```
Not installed → NOT-INSTALLED; install for later `pipx install bandit` (never a `uvx` / `pipx run` one-shot). Read `jq -r '.results[] | "\(.filename):\(.line_number) \(.test_id) \(.issue_severity)"'`; `jq '.metrics._totals.skipped_tests'` counts hits a `# nosec` silenced.
```
BAD:   bandit — exit 1, failed               // exit 1 means "issues found", not a crash
GOOD:  bandit 1.9.4  RAN  exit 1  4 hits (+1 behind # nosec)
```

### 4. Go — gosec

```bash
gosec -fmt=json -out="$SCAN/gosec.json" -exclude-dir=vendor -exclude-dir=testdata -show-ignored ./...; echo "exit=$?"
```
Not installed → the `securego/gosec` image, only when it is already local: `docker run --pull=never --rm -v "$PWD:/src:ro" -w /src securego/gosec -fmt=json -exclude-dir=vendor -exclude-dir=testdata -show-ignored ./... > "$SCAN/gosec.json"`. Neither → NOT-INSTALLED; install for later `brew install gosec`. Read `jq '.Stats'` — `files` must be > 0 and `nosec` is the suppression count; `jq '.Issues[] | select(.nosec)'` lists the hits `#nosec` hid; every entry under `"Golang errors"` is a package that did not type-check and was **not** scanned.
```
BAD:   gosec — clean                          // run with -quiet: on zero issues it prints nothing, so the JSON file is empty
GOOD:  gosec  RAN  exit 1  38 files  6 hits  1 #nosec  0 Golang errors
```

### 5. JVM — SpotBugs + FindSecBugs

FindSecBugs reads **bytecode**, so it needs a JDK and a compiled build. If the build already wires the SpotBugs plugin with FindSecBugs, run that (`mvn -q -DskipTests compile spotbugs:spotbugs` → `target/spotbugsXml.xml`; `./gradlew spotbugsMain` → its report under `build/reports/spotbugs/`). Otherwise the CLI, from the scratch dir:

```bash
mvn -q -DskipTests compile        # or: ./gradlew classes — a failed build is SKIPPED (errored), never clean
curl -sL -o "$SCAN/fsb.zip" https://github.com/find-sec-bugs/find-sec-bugs/releases/download/version-1.14.0/findsecbugs-cli-1.14.0.zip
unzip -q "$SCAN/fsb.zip" -d "$SCAN/fsb" && tr -d '\r' < "$SCAN/fsb/findsecbugs.sh" > "$SCAN/fsb/fsb.sh"   # shipped with CRLF endings
bash "$SCAN/fsb/fsb.sh" -xml:withMessages -output "$SCAN/findsecbugs.xml" target/classes       # Gradle: build/classes/{java,kotlin}/main
rg -o 'BugInstance type="[A-Z_]+"' "$SCAN/findsecbugs.xml" | sort | uniq -c
```
The bundled `include.xml` limits results to the SECURITY category. The exit code is 0 with bugs found — read the XML. Source paths are package-relative; resolve them with `rg --files . -g '<Class>.java'`.
```
BAD:   FindSecBugs — clean                    // findsecbugs.sh run unconverted: "$'\r': command not found", nothing analysed
GOOD:  SpotBugs 4.9.3 + FindSecBugs 1.14.0  RAN  412 classes  3 hits (SQL_INJECTION_JDBC, PATH_TRAVERSAL_IN, COMMAND_INJECTION)
```

### 6. Ruby / Rails — brakeman

```bash
brakeman -q --no-pager -f json -o "$SCAN/brakeman.json" --show-ignored .; echo "exit=$?"
```
Not installed → `bundle exec brakeman` when it is in the Gemfile, or the image when it is already local: `docker run --pull=never --rm -v "$PWD:/code:ro" presidentbeef/brakeman -q --no-pager -f json --show-ignored > "$SCAN/brakeman.json"` (the image's working dir is `/code`). Neither → NOT-INSTALLED; install for later `gem install --user-install brakeman`. Brakeman exits non-zero when it reports warnings (`--[no-]exit-on-warn`, default on). It is Rails-only: a Ruby repo with no Rails app is `SKIPPED n/a` here and covered by semgrep `p/ruby`.
```
BAD:   brakeman — 0 warnings                  // config/brakeman.ignore silenced 4 fingerprints; --show-ignored was not passed
GOOD:  brakeman 8.1.0  RAN  2 warnings  4 ignored (listed under § 10)
```

### 7. PHP — Psalm taint analysis

```bash
vendor/bin/psalm --taint-analysis --no-cache --report="$SCAN/psalm.sarif"; echo "exit=$?"
```
Psalm needs the project's `psalm.xml`. Psalm missing from `vendor/` but a `psalm.xml` present → one-shot phar: `curl -sL -o "$SCAN/psalm.phar" https://github.com/vimeo/psalm/releases/latest/download/psalm.phar && php "$SCAN/psalm.phar" --taint-analysis --no-cache --report="$SCAN/psalm.sarif"`. No `psalm.xml` → **NOT-INSTALLED**, print `composer require --dev vimeo/psalm && vendor/bin/psalm --init` and ask before running it — it edits `composer.json` / `composer.lock` and writes `psalm.xml` into the repo. On Laravel, taint flow through facades and container magic is under-reported without `psalm/plugin-laravel`; say so in the ledger row.
```
BAD:   PHP — covered (phpstan level 8 passes)     // PHPStan checks types; no source-to-sink taint was traced
GOOD:  psalm --taint-analysis  NOT-INSTALLED  blocked — `composer require --dev vimeo/psalm && vendor/bin/psalm --init` (edits composer.json; asked)
```

### 8. .NET — Roslyn security analyzers

The CA3xxx taint rules (CA3001 SQL, CA3002 XSS, CA3003 file path, CA3006 process command, CA3007 open redirect …) ship in the SDK's NetAnalyzers but are **off** by default:

```bash
dotnet build --no-incremental -p:AnalysisModeSecurity=All -p:TreatWarningsAsErrors=false -nologo 2>&1 \
  | tee "$SCAN/dotnet-build.txt" \
  | rg -o --pcre2 '\S+\(\d+,\d+\): warning (CA(2100|3\d{3}|5\d{3})|SCS\d{4})\b' | sort -u
```
`--no-incremental` is load-bearing: an up-to-date build skips compilation, and analyzers run inside the compiler. Security Code Scan (`SCS####`) had its last release in 2022 — count its warnings if the project references it; do not add it.
```
BAD:   Roslyn — 0 security warnings           // incremental build, nothing recompiled, no analyzer ran
GOOD:  dotnet NetAnalyzers (AnalysisModeSecurity=All)  RAN  --no-incremental  5 warnings (CA2100 ×2, CA3001, CA5350, CA5359)
```

### 9. Secrets — dispatched to `secret-scan-method`

gitleaks is `secret-scan-method`'s lane and is not re-run here: dispatch that skill (its § Procedure steps 1 and 3, tree + history), or — inside a `/security-audit` run that already ran it — consume its result. semgrep `p/secrets` hits are handed to it for classification and deduplicated by `<file:line>`. The ledger row is `gitleaks — delegated → secret-scan-method: RAN there` or, if it did not run, `blocked`.

### 10. Suppressions and exclusions — what the tools were told not to say

Grep 4 lists inline pragmas, grep 4b counts every rule an `eslint-disable` names, grep 5 lists exclusion files, and each lane above has a reveal pass that shows the hidden hit. A project's own guard is a security rule too: when 4b shows hundreds of disables of a `no-restricted-syntax` selector or a local plugin rule that the config's message ties to tenant scope, raw SQL or secrets, inventory them like `security/*` pragmas — a bare one (no `--` reason) is read in full; one with a reason is read where the reason does not name the constant, the scope or the lock that makes it safe. The pass reveals: semgrep `--disable-nosem` diff, bandit `--ignore-nosec`, ruff `--ignore-noqa`, gosec `-show-ignored`, brakeman `--show-ignored`, ESLint's `suppressedMessages`. Every suppression on a security rule is listed for `/security-audit` § Phase 6 — Validate, which rates them as blockers. Each listing carries the triage of the hit it hides, so a justified waiver can be accepted explicitly instead of by silence. A justified waiver is a cited false positive whose reason is written in the pragma. **A suppression of a non-security rule** — a correctness, type-checker, async or style rule (`@ts-expect-error`, `# type: ignore`, `no-floating-promises`, `noqa: B904`, `//nolint:errcheck`), or a blanket directive naming no rule — is not this skill's: it goes to `suppression-scan` (code-quality pack, § 1–§ 3, with its unsuppressed re-run), and when that pack is not installed it is listed here as `quality-class (owner pack not installed)`, never rated. One directive that names both a security and a non-security rule is listed here for its security rule and cited to `suppression-scan` for the rest; dedupe by `<file:line>`.
```
BAD:   // eslint-disable-next-line security/detect-non-literal-fs-filename         (no reason; hides readFile(req.query.f))
GOOD:  // eslint-disable-next-line security/detect-object-injection -- key is from the STATUS enum (status.ts:4), never request input
```

## Triage — from hit to finding

1. **Read the enclosing function.** Name the source (request field, header, file content, queue message, model output) and the sink, and confirm nothing upstream parameterizes, validates or encodes it. The scanner's severity is an input, never the verdict.
2. **Confirmed** → `<file:line>` + source + fix + severity (`critical` / `high` / `medium` / `low`) + OWASP 2025 id + CWE (from the rule metadata: semgrep `extra.metadata.cwe`, bandit `issue_cwe.id`, gosec `cwe.id` (null on gosec's newer G7xx taint rules — take the CWE from the rule's class), FindSecBugs `<BugPattern>` / SARIF taxonomy) + the owning detector from the table below.
3. **False positive** → cite the reason: constant or server-derived input (`<file:line>` of its origin), sanitizer or allow-list at `<file:line>`, dead code, or framework auto-encoding on this exact path. "Looks fine" is not a reason.
4. **Test and fixture paths** (`test/`, `tests/`, `__tests__/`, `*_test.go`, `*.spec.*`, `*.test.*`, `fixtures/`, `testdata/`) → `note (test code)`, not a finding. Two exceptions: a `p/secrets` hit (a live key in a test is still a leak — hand it to `secret-scan-method`), and a test helper that production code imports. **Operator and agent tooling** (`scripts/`, `tools/`, `bin/`, `.claude/`, `.opencode/`, `ai/`) → `note (tooling)` once no image, deployed job or route runs it — cite the `rg` over Dockerfiles, deploy manifests and `package.json` that shows it; a CI-run script is still read for argv or env taken from the event.
5. **One finding per sink.** Two tools on the same `<file:line>` are one row carrying both rule ids. When a detector skill also traced that sink, the finding belongs to the detector and this skill's hit is listed under it as corroboration (`/security-audit` § Phase 2 — Organize, "Dedupe by `<file:line>`").
6. **Monorepo scale — classify, then read what can be a finding.** "Every hit triaged" does not mean every hit read one by one: measured on a real NestJS-on-Fastify monorepo (9.2k linted files), `eslint-plugin-security` returned 3,616 hits, 2,256 of them `detect-object-injection`. The sanctioned path: split by path class (rule 4), then split production `detect-object-injection` hits by the token after the flagged node — a **write** (`obj[k] = v`) or **call** (`obj[k](…)`) is read in full; a **read** is one class closed with one reason ("no write or call — an inherited key yields `undefined` or a function, which fails closed or throws") after a spot-read of every lookup that decides authorization or picks a handler. Every other production rule is read per hit. There it left 269 rows to read — 189 writes, 2 calls, 78 hits of other rules — out of 1,322 production hits.
```bash
python3 - "$SCAN" <<'EOF'
import json, os, re, sys, collections; S = sys.argv[1]; C = collections.Counter(); out = open(S + '/eslint-read-these.tsv', 'w')
PC = [('test', r'(^|/)(tests?|__tests__|__mocks__|e2e|fixtures|testdata)/|\.(test|spec|stories)\.\w+$'), ('tooling', r'(^|/)(scripts|tools|bin|\.claude|\.opencode|ai)/'), ('config', r'(^|/)[^/]*\.config\.\w+$')]
for f in json.load(open(S + '/eslint.json')):
    p = os.path.relpath(f['filePath']); cls = next((n for n, rx in PC if re.search(rx, p)), 'prod'); src = None
    for m in f['messages']:
        if not m.get('ruleId') or m['message'].startswith('Definition for rule'): continue
        kind = ''
        if cls == 'prod' and m['ruleId'] == 'security/detect-object-injection':
            src = src or open(f['filePath'], errors='replace').read().split('\n'); rest = src[m.get('endLine', m['line']) - 1][(m.get('endColumn') or m['column']) - 1:]
            kind = 'write' if re.match(r'\s*(=(?!=)|[-+*/?|&]{1,2}=|\+\+|--)', rest) else 'call' if re.match(r'\s*(\?\.)?\(', rest) else 'read'
        C[(cls, m['ruleId'], kind)] += 1
        if cls == 'prod' and kind != 'read': out.write(f"{p}:{m['line']}\t{m['ruleId']}\t{kind}\n")
for k, v in sorted(C.items()): print(v, *k)
EOF
```

| Hit class (rule family / CWE) | Owner the finding is filed under |
|---|---|
| SQL / NoSQL, OS command, eval / code, SSTI, XXE, deserialization, prototype pollution, ReDoS, CSV formula injection — CWE-89, 78, 94, 1336, 611, 502, 1321, 1333, 1236; bandit B301 / B506 / B602 / B608; gosec G201 / G202 / G204 | `injection-scan` |
| Path traversal, upload, archive extraction — CWE-22, 434; gosec G304 / G305; FindSecBugs `PATH_TRAVERSAL_*` | `file-access-scan` |
| XSS, raw-HTML sinks, CSRF — CWE-79, 352; `no-unsanitized/*` | `xss-scan` |
| Debug mode, stack traces, information exposure, secrets in logs — CWE-200, 209, 532; bandit B201 | `data-exposure-scan` |
| SSRF, open redirect — CWE-918, 601 | `ssrf-scan` |
| Hard-coded credential — CWE-798; `p/secrets` | `secret-scan-method` |
| TOCTOU / race — CWE-362, 367 | `logic-race-scan` |
| Weak hash or cipher, TLS verification off, weak random, unverified JWT signature — CWE-327, 328, 295, 338, 347; bandit B324 / B501; gosec G401 / G402 / G404 | **filed here** — no detector skill owns A04:2025 |
| Timing-unsafe compare of a secret, token or signature — CWE-208; `security/detect-possible-timing-attacks` | `data-exposure-scan` § 13 |
| Trojan-source / bidi control characters — CWE-1007, 451; `security/detect-bidi-characters` | **filed here** — a finding only where the character reorders how code or a comment reads; inside display text (RTL strings, a bidi-strip regex) it is a cited false positive |
| Hidden Unicode in an AI context file (pre-flight 6: `CLAUDE*.md`, `AGENTS.md`, `.cursor/rules`, Copilot instructions, `ai/**`, `.claude/**`) — CWE-1007; learning KN-35 | **filed here** — the reader is a model that obeys what a human reviewer cannot see, so an override, isolate, zero-width or tag character there is a finding (critical in a file loaded every session) wherever it sits, unless it is an LRM / RLM inside RTL prose (P-26). Measured 2026-10-19 over every tree under `benchmarks/fixtures`: 1 hit, the seeded U+202E/U+202C pair in `stale-knowledge/.claude/rules/commits.md:9`; its U+200F decoy in Arabic text is not matched |
| Package-manager supply-chain settings — CWE-829, 1104; semgrep `package_managers.*` on `.npmrc`, `pnpm-workspace.yaml`, `.yarnrc.yml`, `dependabot.yml` | `deps-audit` § Supply-chain settings |
| A rule that fired on a Dockerfile, manifest, Terraform file or workflow | `iac-scan` |

## Output

```
sast-scan — <repo>@<sha>          scratch: /tmp/sast-scan.k3J9 (outside the repo)

Tool ledger (= class coverage)
  ### 1  semgrep 1.178.0              RAN            exit 0 · 214 files · owasp-top-ten secrets javascript typescript nodejs python django
                                                     checked (14 hits → 2 findings)
  ### 2  eslint security              RAN            exit 1 · 96/96 files · checked (9 hits → 1 finding) · 2 suppressed
  ### 3  bandit 1.9.4                 RAN            exit 1 · checked (6 hits → 1 finding) · 1 behind # nosec
  ### 4  gosec                        SKIPPED        N/A (grep 1: no .go files)
  ### 5  SpotBugs + FindSecBugs       SKIPPED        N/A (grep 1: no .java/.kt files)
  ### 6  brakeman                     SKIPPED        N/A (no Rails app)
  ### 7  psalm --taint-analysis       NOT-INSTALLED  blocked (no vendor/bin/psalm, no psalm.xml) —
                                                     composer require --dev vimeo/psalm && vendor/bin/psalm --init   (edits composer.json; declined)
  ### 8  Roslyn security              SKIPPED        N/A (no *.csproj)
  ### 9  gitleaks                     delegated      → secret-scan-method: RAN there, result consumed
  ### 10 suppressions                 checked (5 pragmas + 1 .semgrepignore line → 1 hides a confirmed sink)
  COVERAGE: 1 gap (psalm) — the audit verdict cannot be a clean GO.

Findings: 3

1. src/reports/export.controller.ts:48                 critical  [report-with-fix]  → injection-scan
   semgrep code-string-concat + eslint security/detect-eval-with-expression
   eval(req.query.expr) — query string reaches eval, no allow-list.  A05:2025 · CWE-94
   Fix: remove eval; map the expression to a fixed function table or parse a whitelisted grammar.

2. app/billing/views.py:71                             high      [report-with-fix]  → injection-scan
   bandit B602, hidden by `# nosec` with no reason — subprocess(..., shell=True) built from request.GET["dir"].
   A05:2025 · CWE-78
   Fix: argv list with shell=False, `dir` checked against an allow-list; delete the # nosec.

3. src/web/Preview.tsx:22                              medium    [report-flagged]   → xss-scan
   no-unsanitized/property — el.innerHTML = props.html; props.html is CMS content any editor can set.  A05:2025 · CWE-79
   Fix: DOMPurify.sanitize at the boundary, or render as text.

False positives (11) — each with its reason, e.g.:
   src/lib/sql.ts:12      semgrep tainted-sql-string — table name comes from the TABLES constant map (src/lib/sql.ts:4).
   tests/seed_test.py:9   bandit B105 — note (test code).
```

## False positives / gotchas

Measured on this skill's own vulnerable sample on 2026-10-01 (semgrep 1.178.0, bandit 1.9.4, ruff 0.16.9, ESLint 9.39 + eslint-plugin-security 4.1.0, gosec via `securego/gosec`, brakeman 8.1.0, FindSecBugs 1.14.0):

- **semgrep's exit code hides both failure and findings.** Exit 0 with findings unless `--error`; exit 2 for `--config auto` with `--metrics=off`; exit 7 when one `p/` name is a 404 — and that one bad name aborts the whole scan. RAN means the JSON exists, `errors[]` was read and `paths.scanned` is non-empty.
- **A project `.semgrepignore` replaces semgrep's default ignore list.** Without one, semgrep skips `tests/` and the usual build dirs by itself; with one, those defaults go and only the project's entries apply. Read the file — every line is a suppression by path (§ 10).
- **`nosemgrep: <rule-id>` hides only that rule**; a bare `nosemgrep` hides every rule on the line. Results are not marked as ignored in the JSON — the `--disable-nosem` diff is the only way to see them.
- **`errors[]` is counted by class, read by exception.** On a real 10k-file TS monorepo semgrep logged 204 errors: 194 `PartialParsing` on test files (`<T,>()` generic arrows), 7 on tooling, 1 timeout, and 2 on production files — `export { type X }` barrels the TS parser only partly scans. Group with the jq above; read every production-file error (that file was partly unscanned — say so in the ledger) and record the rest as counted classes.
- **`package_managers.*` rules key on one manager's file and setting name.** On a pnpm repo the npm rule (`npm-missing-minimum-release-age`) fires on `.npmrc` even when it already sets the release-age key pnpm reads, and the pnpm rule fires on `pnpm-workspace.yaml` when the setting lives in `.npmrc`. Read which file and key the installed manager version honours before filing (`deps-audit` § Supply-chain settings).
- **The generic nginx rules match comments.** `request-host-used` fired on a `$host` inside a `#` comment as well as the real directive — check the line before triaging the class.
- **ESLint 9 lints only `.js` / `.mjs` / `.cjs` unless a `files` entry names the TS extensions** — a TS repo "passes" with zero TS files linted. Compare `jq length` with the file count. `eslint-plugin-security` rules are warnings, so exit 0 does not mean clean; `no-unsanitized` rules are errors.
- **bandit and ruff disagree on pragmas.** ruff ignores `# nosec` and bandit ignores `# noqa: S###`. Inventory both whichever tool ran.
- **`//nolint:gosec` is golangci-lint's pragma.** Standalone gosec still reports the line, so the two runners disagree on the same code. `#nosec G204` hides only G204, so newer rules on the same line still fire.
- **Docker one-shots can scan an empty directory.** A bind mount from a path Docker Desktop does not share comes up empty, and the tool reports "no packages" or zero files. Check the scanned-file count on every docker-run row.
- **FindSecBugs exits 0 with bugs found, and its shipped script fails under bash until the CRLF is stripped.** SpotBugs on a stale `target/classes` analyses yesterday's code — compile first.
- **Scanner disagreement is signal, not noise.** semgrep missed `pickle.loads(request.data)` that bandit caught, and missed an `exec.Command("sh", "-c", query)` that gosec caught. Run every lane the stack has; a clean semgrep run closes no class.

## When to run

- Every whole-repo `/security-audit`, and on a diff whenever the stack has an analyzer available — `/security-audit` § Phase 2 — Organize dispatches it.
- Before a release, after adding a language or framework to the repo, and after any change to a scanner config or ignore file.
- When a detector skill's grep set looks too clean for the codebase's size — the analyzers are the second net.

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`finding-verification.md`](../../../../snippets/finding-verification.md). Under `/security-audit` that happens in Phase 4; run standalone, it applies the protocol as a separate second pass, tags those rows `self-verified`, and lists the rest as Unconfirmed, Hardening or Refuted — never drops them.
- Halt on a ledger that omits a lane grep 1 detected. Every language present gets a row: RAN, SKIPPED with its reason, or NOT-INSTALLED with the command.
- Halt on `SKIPPED n/a` without the grep-1 evidence, and on RAN without the version, exit code and scanned-file count. A language present only in agent or audit tooling is `SKIPPED n/a (tooling only — <paths>)`, never a lane run on the product's behalf.
- Halt on any hit left untriaged. Every hit ends as a finding or as a false positive with a cited reason. "Scanner noise" in bulk is not a triage; a path class or a syntax class closed with one checked reason (§ Triage rules 4 and 6) is, and the ledger counts each class.
- Halt on a finding without `<file:line>` + source + fix + severity + owner. Do not report a scanner line as a finding before reading the enclosing function.
- Do not install anything globally, add a dependency, or write scanner config into the repo without asking. Do not write scan output inside the repo.
- Do not re-run gitleaks or a dependency audit here — dispatch `secret-scan-method` / `deps-audit`.

## Related

- `/security-audit` — dispatches this skill in § Phase 2 — Organize, turns its blocked rows into `COVERAGE:` gaps, and rates its suppression list in § Phase 6 — Validate. Its § Class coverage ledger has no row for this skill: the ledger above is this skill's coverage, and each confirmed finding lands in its owner's row.
- `injection-scan`, `file-access-scan`, `xss-scan`, `data-exposure-scan`, `ssrf-scan`, `logic-race-scan` — the owners in the triage table. Their greps and this skill's analyzers are two nets over the same sinks; findings dedupe by `<file:line>`.
- `secret-scan-method` — owns gitleaks / trufflehog and every secret hit (§ 9). `deps-audit` — owns lockfile CVEs. `iac-scan` — owns IaC and CI rulesets.
- `@security-auditor` — its Output names semgrep and the per-language security linters as its static tools; this skill is where they actually run.
- `rules/security-principles.md` — the MUSTs the confirmed findings are measured against.
