---
name: doc-sample-scan
description: "Doc samples that must run: fences compile, doctests print what they say, embeds in sync, harness in CI, spec examples."
kind: skill
pack: documentation
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: doc-sample-scan

## Premise

A code sample is the part of a doc readers copy without reading. It drifts silently: an export is renamed and the README's `import { createOrderClient }` no longer compiles; a rounding change makes `>>> to_minor(1.005)` print `100` while the doc says `101`; a snippet pasted from `src/retry.ts` keeps the old backoff after the source changed; the spec's `example` for an order still carries a field the schema dropped. Naive execution of more than 600 tutorials succeeded for 26% of code blocks, and no tutorial ran every step (Docable, FSE 2020). The projects that keep samples true **run** them: pydantic's `pytest-examples`, FastAPI's `docs_src` imported by its tests, `cargo test --doc`, Go `Example` tests, CPython's doctest job.

This skill owns DC-1 (a fence does not compile or import), DC-2 (a stated output is wrong), DC-3 (an embedded snippet diverged from its source), DC-4 (a sample harness exists but no CI step runs it) and DA-2 (a spec example is invalid against its own schema, or a placeholder) (§1–§5). Paths, scripts and flags a shell fence names are `doc-drift-scan`'s; executing the setup section is `quickstart-verify`'s.

**Every finding cites the fence (`doc:line`, language, the scratch file) and the compiler, runner or validator output that failed, with its exit code read through the tool's own map.** An engine row or a fence classified `candidate` is a candidate, never a finding. "Samples are fine" is never printed without the class-coverage block (§ Output).

## The rule

A candidate becomes a finding only when all four hold:

1. **The fence claims to run.** It is a complete program, a fence the project marks runnable (twoslash, mdBook `rust`, a doctest block, a harness glob), or a "copy and run" step; never an excerpt with `...`, a `text` / `diff` / `console` fence, rustdoc `ignore` / `no_run`, a statement fragment with no import, or a recipe that says to adapt the nouns ([precedents § 6, § 14](../../../../snippets/precedents/documentation.md)).
2. **The project's own toolchain ran it**, in a scratch copy, at the pinned version, with the package's own config (`tsconfig`, venv, `Cargo.toml`); a lane whose toolchain is absent is `NOT-RUN (no install)`, never PASS (§ 33).
3. **It failed for a reason in the sample**: a missing export, a wrong arity, a type error, a different printed value, a snippet that differs from its region, an example that breaks its schema. A failure from the environment (no install, no network, a secret) is not the sample's.
4. **No record makes it intentional**: a fence marked to skip, non-deterministic output patched by the harness, a generated reference regenerated from source (§ 17).

## Boundaries

- Commands in shell fences (scripts, flags, paths, endpoints) → `doc-drift-scan` §1–§4, §11; the setup sequence run end to end → `quickstart-verify`.
- The committed spec against code or runtime → backend `http-contract-scan` §10 (+ Schemathesis), when the backend pack is installed; §5 here takes the spec's **examples** against the spec's own schemas. Without the backend pack the spec-vs-code half is out of scope and the coverage block says so.
- Docstring coverage and docstring-vs-signature → `docstring-coverage`; docstring **examples** that are doctests run in §2 here.
- The test suite's own strength → the testing pack; §4 only asks whether the doc-sample harness the repo configured is run by CI.
- Links and anchors inside samples → `doc-structure-scan`.

## Lanes

Every lane runs in a scratch copy (`git archive HEAD | tar -x -C "$OUT/copy"`) or on the engine's extracted fences under `$OUT`, never in the tree; caches go to `$OUT` (`CARGO_TARGET_DIR`, `GOCACHE`, `-p no:cacheprovider`). Telemetry off: `CI=true DO_NOT_TRACK=1 REDOCLY_TELEMETRY=off NEXT_TELEMETRY_DISABLED=1`. Installed binaries only, never `npx -y`.

| Stack | §1 compile / import | §2 doctest | §3 embeds | §4 harness configured | Trap |
|---|---|---|---|---|---|
| **TS / JS** | `tsc --noEmit --incremental false` on a scratch `tsconfig` that `extends` the package's own; typescript-docs-verifier or twoslash when the repo uses them | — | embedme `--verify`, `file=` (remark-code-import), `!!raw-loader` | a `typescript-docs-verifier` script, twoslash in the site | `@eslint/markdown` turns off `no-undef`; `eslint-plugin-jsdoc` `check-examples` is dead on ESLint ≥ 8; build the package first for self-imports |
| **Python** | `ast.parse` for every candidate, then the import in the project venv | `pytest --doctest-glob='*.md' --doctest-modules -p no:cacheprovider`; pytest-examples; Sybil; pytest-markdown-docs | `literalinclude` (Sphinx), `--8<--` (pymdownx.snippets) | `[tool.pytest.ini_options] addopts` with `--doctest-glob`, a `pytest-examples` test, a Sybil `conftest.py` | doctest-glob runs only `>>>` prompts; exit **5** = nothing collected (NOT-RUN); Sybil skips unknown fence languages |
| **Rust** | `cargo test --doc --offline` (`mdbook test` for a book) | the same | — | `doctest = false` in `[lib]` silences it | `ignore` / `no_run` / `compile_fail` are intentional; rustdoc lints are warnings |
| **Go** | `go vet ./...` | `go test -run Example ./...` (`// Output:` checked) | — | `Example` functions exist | no `// Output:` means compile only |
| **JVM / Kotlin** | `javac` against the build classpath only when Gradle or Maven resolves offline [K?] | kotlinx-knit `knitCheck` (incubator) [K?] | `{@snippet}` (JEP 413: javadoc does not compile snippets) | — | partial lane |
| **Elixir** | `mix compile` | `doctest_file "README.md"` under `mix test` | — | `doctest` in a test module | opaque `#Name<…>` output is a comment |
| **OpenAPI** (§5) | — | — | — | — | engine `specex` (JSON); `REDOCLY_TELEMETRY=off redocly lint` (`no-invalid-media-type-examples`, `no-invalid-schema-examples`); Spectral with an explicit ruleset (`oas3-valid-media-example`, `oas3-valid-schema-example`) — no ruleset lints nothing |

Runme executes arbitrary shell from docs and its telemetry is unverified: never a lane. A [K?] or partial lane prints `checked · partial`.

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). The engine's `--fences` mode writes every fence of every in-scope doc to `$OUT/fences/<doc>__L<line>.<ext>` with `fences.tsv` (`file · doc · line · lang · kind · reason · info`; kind `candidate`, `doctest`, `fragment`, `excerpt`, `transcript`, `shell`, `config`, `not-code`, `skip-marked`, `unknown`). Every grep ends in `ck`.

```bash
DC="${DC:-.claude/skills/doc-drift-scan/scripts/doc-claims.py}"
OUT="$(mktemp -d "${TMPDIR:-/tmp}/doc-sample.XXXXXX")"; export GIT_OPTIONAL_LOCKS=0 CI=true DO_NOT_TRACK=1 REDOCLY_TELEMETRY=off NEXT_TELEMETRY_DISABLED=1; : > "$OUT/stamp"
ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
python3 -I "$DC" . --lanes=embeds,specex --fences="$OUT/fences" > "$OUT/claims.tsv" 2> "$OUT/ledger.txt"
echo "doc-claims exit $? — 0 clean · 1 candidates (DC-3 / DA-2 rows) · 2 BLOCKED"; tail -4 "$OUT/ledger.txt"; cut -f2,3 "$OUT/claims.tsv" | sort | uniq -c
[ -f "$OUT/fences/fences.tsv" ] || { mkdir -p "$OUT/fences"; : > "$OUT/fences/fences.tsv"; echo "fences BLOCKED (no fences.tsv): §1 and §2 are blocked, never clean"; }
awk -F'\t' 'NR>1{print $5, $4}' "$OUT/fences/fences.tsv" | sort | uniq -c | sort -rn | head -12        # kind · language
X=(-g '!**/node_modules/**' -g '!**/{dist,build,vendor,.venv,target,coverage}/**' -g '!ai/**' -g '!.claude/**')
# P1. Sample harnesses the repo configured (§4).
rg -n --pcre2 '\-\-doctest-(?:glob|modules)|doctest_optionflags|pytest[-_]examples|pytest-markdown-docs|\-\-markdown-docs|\bSybil\(|phmdoctest|typescript-docs-verifier|twoslash|mdbook\s+test|^\s*doctest\s*=\s*false|\bembedme\b|markdown-code-runner|\bdoctest_file\b' -g '*.{toml,ini,cfg,json,yml,yaml,py,js,ts,mjs,exs}' -g '**/Makefile' "${X[@]}" .; ck P1 $?
# P2. CI steps that could run them (§4): direct, or through a package script that turbo / pnpm -r / nx run.
#     --hidden: .github/ and .circleci/ are dot-directories rg skips without it (0 hits would read as "no CI runs it").
rg -n --hidden --pcre2 '\-\-doctest-glob|pytest[-_]examples|\-\-markdown-docs|typescript-docs-verifier|mdbook\s+test|cargo\s+test(?!\s+--lib)|embedme\s+--verify|\bpytest\b|\bturbo\s+run\b|\bnx\s+run-many\b|\bpnpm\s+(?:-r\s+|--recursive\s+)?(?:run\s+)?test\b|\bmix\s+test\b|\bgo\s+test\b' -g '.github/workflows/*.{yml,yaml}' -g '.gitlab-ci.yml' -g '.circleci/*.yml' -g '.pre-commit-config.yaml' .; ck P2 $?
# P3. Doctest prompts in docs (§2): a --doctest-glob run over docs with none tests nothing (pytest exit 5).
rg -c --pcre2 '^\s*>>>\s' -g '*.{md,mdx,rst,txt}' -g '!**/CHANGELOG*' "${X[@]}" .; ck P3 $?
# §1 Python: syntax of every candidate fence, no writes (ast.parse, not py_compile).
awk -F'\t' '$5=="candidate" && $4 ~ /^(py|python|python3)$/ {print $1}' "$OUT/fences/fences.tsv" | while read -r f; do
  python3 -I -B -c 'import ast,sys; ast.parse(open(sys.argv[1]).read())' "$OUT/fences/$f" 2> "$OUT/$f.err" || echo "§1 py syntax FAIL $f: $(tail -1 "$OUT/$f.err")"; done
# §1 TS: each candidate against the nearest package tsconfig, with the repo's own tsc (no install: NOT-RUN, never PASS).
TSC=""; [ -x node_modules/.bin/tsc ] && TSC="$PWD/node_modules/.bin/tsc"
awk -F'\t' '$5=="candidate" && $4 ~ /^(ts|typescript|tsx)$/ {print $1"\t"$2}' "$OUT/fences/fences.tsv" | while IFS="$(printf '\t')" read -r f doc; do
  [ -n "$TSC" ] || { echo "§1 ts NOT-RUN $f (no node_modules/.bin/tsc: install in a scratch copy first)"; continue; }
  d=$(dirname "$doc"); while [ "$d" != "." ] && [ ! -f "$d/tsconfig.json" ]; do d=$(dirname "$d"); done
  [ -f "$d/tsconfig.json" ] || { echo "§1 ts blocked $f (no tsconfig above $doc)"; continue; }
  printf '{"extends":"%s/%s/tsconfig.json","compilerOptions":{"noEmit":true,"incremental":false,"composite":false,"skipLibCheck":true},"include":[],"files":["%s/fences/%s"]}\n' "$PWD" "$d" "$OUT" "$f" > "$OUT/$f.tsconfig.json"
  "$TSC" -p "$OUT/$f.tsconfig.json" > "$OUT/$f.tsc" 2>&1; r=$?; [ $r -eq 0 ] && echo "§1 ts ok $f" || echo "§1 ts exit $r $f: $(grep -m2 'error TS' "$OUT/$f.tsc" | tr '\n' ' ')"; done
# §2 Python doctests in a scratch copy, only when docs carry >>> (exit 5 = nothing collected = NOT-RUN).
PY=python3; [ -x .venv/bin/python ] && PY="$PWD/.venv/bin/python"
if rg -q --pcre2 '^\s*>>>\s' -g '*.{md,rst}' "${X[@]}" . && "$PY" -c 'import pytest' 2>/dev/null; then mkdir "$OUT/copy" && git archive HEAD | tar -x -C "$OUT/copy"
  (cd "$OUT/copy" && "$PY" -m pytest --doctest-glob='*.md' --doctest-glob='*.rst' -p no:cacheprovider -q $(rg -l --pcre2 '^\s*>>>\s' -g '*.{md,rst}' "${X[@]}" .) > "$OUT/doctest.txt" 2>&1); echo "§2 doctest exit $? — 0 pass · 1 failures · 5 NOT-RUN (nothing collected) · other BLOCKED"
else echo "§2 doctest N/A or NOT-RUN (no >>> in docs, or no pytest)"; fi
# §5 tool lane: Redocly (telemetry off) or Spectral with an explicit ruleset; else the engine's specex rows stand.
SPEC=$(rg --files -g '{openapi,swagger}*.{json,yaml,yml}' "${X[@]}" . | head -1)
if [ -n "$SPEC" ] && [ -x node_modules/.bin/redocly ]; then node_modules/.bin/redocly lint "$SPEC" --format=json > "$OUT/redocly.json" 2>&1; echo "§5 redocly exit $? (read no-invalid-*-examples rows only)"
elif [ -n "$SPEC" ] && [ -x node_modules/.bin/spectral ] && ls .spectral.* >/dev/null 2>&1; then node_modules/.bin/spectral lint "$SPEC" -f json > "$OUT/spectral.json" 2>&1; echo "§5 spectral exit $?"
else echo "§5 tool lane NOT-RUN (no spec, or no redocly / spectral with a ruleset installed)"; fi
find . -newer "$OUT/stamp" -type f -not -path './node_modules/*' -not -path './.git/*' | head -3; echo "write check done (empty = nothing written)"
```

Rust, Go and Elixir lanes run the project's own command in `$OUT/copy` with caches redirected (`CARGO_TARGET_DIR="$OUT/target" cargo test --doc --offline`; `GOCACHE="$OUT/gocache" GOFLAGS=-mod=readonly go test -run Example ./...`; `MIX_BUILD_PATH="$OUT/_build" mix test`) when the toolchain at the pinned version is on the PATH; else `NOT-RUN (toolchain)`.

## Measured

Measured 2026-10-19 (`doc-claims 1.0`, self-test 46/46).

- **A real NestJS + React monorepo** (read-only, write check empty). Fences in the 66 in-scope human docs: 171 shell, 68 unknown (PromQL and LogQL in runbooks), 20 config, 11 TS fragments, 10 TS candidates, 5 not-code (mermaid). 7 of the 10 candidates sit in `apps/api/RECIPE.md`, a how-to that says to adapt the nouns (§ 6): Unconfirmed at best. No `node_modules`, so §1 TS prints `NOT-RUN (no install)` for each candidate, never PASS. DC-3 N/A (no embed markers), DA-2 0 (the committed JSON spec carries no examples), DC-2 N/A (no `>>>` in docs), DC-4 0 (P1 0 harnesses configured). Greps: P1 0 · P2 0 (CI runs typecheck, lint and format steps; no doc harness and no test step the pattern names) · P3 0; no grep exited 2.
- **Fixtures**: no fixture carries a doc sample corpus; the engine's self-test seeds the fence classifier and the specex lane. P1 0 and P3 0 on every fixture; P2 1 on `ci-defects` (its test job), 0 elsewhere; no grep exited 2.
- **The `doc-drift` fixture** (2026-10-19): fences 32 (shell 21, candidate 3, doctest 2, excerpt 2, not-code 2: `pseudo` and mermaid, config 1); the engine printed the two DC-3 and the two DA-2 seeds (4 candidates; the `pseudo` and `// ...` decoys were classified not-code and excerpt, never compiled). §1 TS printed `NOT-RUN` for the 3 candidates (no `node_modules`): the two DC-1 seeds stay Unconfirmed until a scratch install. §2: P3 found the `>>>` README and pytest was absent from the interpreter, so `NOT-RUN`; run by hand in a scratch copy (Python 3.13) the doctests print `Expected 101 / Got 100` and `NameError: format_minor`, the two DC-2 seeds. **P2 printed 0 on its first run**: rg skips `.github/` without `--hidden`, so every harness read as "not in CI"; P2 now passes `--hidden` and prints 2 here (`pnpm -r test`, `pytest packages/py-money/tests`, neither collecting `*.md`: the DC-4 seeds), 7 on `ci-defects`, 3 on `brittle-suite`, 1 on `quality-mix`, 2 on the in-progress `business-rules` tree, 0 elsewhere. P1 4, P3 1; no grep exited 2.

## The 3,000-row path

1. **Classify before compiling.** `fences.tsv` kinds decide the work: only `candidate` and `doctest` rows run; `fragment`, `excerpt`, `transcript` and `skip-marked` are counted, never compiled (§ 14). More than half the candidates in one doc that reads as a recipe or template is § 6: read the doc's intro before compiling any.
2. **Group by failing symbol.** Run each candidate once, then group the compiler errors by the missing export or changed signature: one removed export used by 30 fences is **one finding with 30 sites**.
3. **Read in this order:** published SDK or package READMEs (the registry renders them), quickstarts, then guides.
4. **Close a group with one checked reason** (`22 TS2307 rows: workspace not installed — NOT-RUN, not a finding`).
5. **Ledger the rest** as `Live, unreviewed (k groups / n fences)`.

## Scans for

| § | Class | Lane | Finding when | Default (primary) | Oracle |
|---|---|---|---|---|---|
| 1 | DC-1 fence does not compile or import | `--fences` candidates + the stack's compiler | the project's compiler rejects the fence for a reason in the fence | HIGH in a published SDK / package README; else MEDIUM | V441 |
| 2 | DC-2 stated output wrong | doctest runner | the runner prints another value than the doc states | MEDIUM | V442 |
| 3 | DC-3 embedded snippet diverged | engine `embeds` + embedme `--verify` | the committed snippet differs from its region, or the region or file is gone | MEDIUM | V443 |
| 4 | DC-4 harness not in CI | P1 × P2 | a harness is configured (or a doctest flag set) and no CI step on the PR path runs it | MEDIUM | V432 |
| 5 | DA-2 spec example invalid or placeholder | engine `specex` + Redocly / Spectral | an example fails its schema, or is `"string"`, `0`, `"example"` | MEDIUM | V440 |

### 1. Fence does not compile or import (DC-1)

```
BAD:   packages/sdk/README.md   ```ts import { createOrderClient } from '@acme/sdk' ```     (index.ts exports createClient)
       ```ts client.orders.list(10, true) ```                                                (list(opts: ListOptions))
GOOD:  import { createClient } from '@acme/sdk'   ·   client.orders.list({ limit: 10 })
```
**Read the docs and the code:** Is the fence a candidate by its kind, or a fragment the classifier promoted because it imports? Did the scratch `tsconfig` extend the right package config, with `paths` to the workspace sources (self-imports need the build or a `paths` map)? Which errors are the fence's (TS2305 missing export, TS2554 arity, TS2339 property) and which are the environment's (TS2307 cannot find module without an install: NOT-RUN)? For Python, `ast.parse` proves syntax only; an import check needs the venv. **Finding when** the compiler rejects the fence for a reason in the fence. **Proof:** V441, the compiler's own error, failing before and passing after across every fence of the same API.

### 2. Stated output wrong (DC-2)

```
BAD:   packages/py-money/README.md   >>> to_minor(1.005)
                                      101                     (the function rounds half-even: prints 100)
GOOD:  >>> to_minor(1.005)   100   ·   or the rounding restored when the doc is the contract (§ 16)
```
**Read the docs and the code:** Did the runner collect anything (pytest exit 5 = nothing: NOT-RUN)? `--doctest-glob='*.md'` runs `>>>` prompts only; a plain ```` ```python ```` fence with a printed comment is not a doctest. Is the output non-deterministic (time, random, dict order, memory addresses) and unpatched? **Finding when** the runner prints another value. **Proof:** V442.

### 3. Embedded snippet diverged (DC-3)

```
BAD:   docs/retries.md   ```ts // src/retry.ts#L10-L18  …old backoff… ```     (embedme committed; the source changed)
       docs/api.md       --8<-- "examples/create-order.sh"                     (file deleted)
GOOD:  re-embedded from the current region (prefer region markers to line ranges), or the include repointed
```
**Read the docs and the code:** Is the embed committed (embedme: drift is real) or resolved at build (remark-code-import, `!!raw-loader`, `literalinclude`: only the file and the range can break)? Did the line range shift so it now embeds the wrong lines? **Finding when** the committed snippet differs from its source region, or the embedded file or range is gone. **Proof:** V443 (`embedme --verify` in a scratch copy, or the engine's `embeds` rows).

### 4. Harness exists, CI never runs it (DC-4)

```
BAD:   pyproject.toml   [tool.pytest.ini_options] addopts = "--doctest-glob='*.md'"     CI: pytest tests/   (docs never collected)
       Cargo.toml       [lib] doctest = false
GOOD:  CI runs `pytest` from the root with the glob (or `pytest docs/`), and the step runs on pull requests
```
**Read the docs and the config:** Does the CI step reach the harness through a package script (`turbo run test`, `pnpm -r test`, `nx run-many`): resolve the script per package before concluding? Does it run on PRs or only on `main`? A pre-commit hook the CI also runs counts. **Finding when** no CI step on the PR path invokes the configured harness. **Proof:** V432, the mutation: plant a broken example in a scratch copy and the CI command must fail.

### 5. Spec example invalid or placeholder (DA-2)

```
BAD:   openapi.json   Order.example: { "id": 1, "status": "void" }      schema: id string, status enum [placed, cancelled]
       requestBody example: { "name": "string" }
GOOD:  { "id": "ord_123", "status": "cancelled" }   ·   a realistic value per field
```
**Read the docs and the spec:** Does the engine's `specex` lane cover the spec (JSON; a YAML spec needs the Redocly or Spectral lane)? Is the example an `externalValue`? Is the schema itself stale against the code (that is backend `http-contract-scan` §10's)? **Finding when** the example fails its own schema or is a placeholder on a published API. **Proof:** V440.

## Output

```
doc-sample-scan — doc-claims 1.0 · fences 286 (candidate 14, doctest 3, fragment 31, excerpt 9, shell 171, …) · tsc 5.9 (node_modules) · pytest 9.0

Findings: 2 · Unconfirmed: 1

1. packages/sdk/README.md:42                                     [report-with-fix]  HIGH · §1
   `import { createOrderClient } from '@acme/sdk'` — tsc TS2305: no exported member (packages/sdk/src/index.ts:3
   exports createClient). 4 more fences in docs/sdk/*.md: one finding, 5 sites. Fix: rename in all 5.
2. packages/py-money/README.md:18                                [report-with-fix]  MEDIUM · §2
   >>> to_minor(1.005) states 101; pytest doctest prints 100 (money.py:41 ROUND_HALF_EVEN). Contract question first (§ 16).
3. openapi.json #/components/schemas/Order/example                [report-flagged]   MEDIUM · §5
   status "void" not in enum [placed, cancelled]. Unproven link: is the spec published to clients?

Verification: 9 candidates → 2 findings · 1 unconfirmed · 2 hardening · 0 pre-existing · 4 refuted

Class coverage:
  §1  compile / import      checked (14 candidates → 6 errors → 1 group; 31 fragments, 9 excerpts not compiled § 14)
  §2  doctest output        checked (3 docs with >>> → 1; pytest exit 1)
  §3  embedded snippets     N/A (no embed markers)
  §4  harness not in CI     checked (1 harness: pytest --doctest-glob in pyproject.toml; CI runs pytest from the root → 0)
  §5  spec examples         checked (engine specex 22 examples → 1) · redocly NOT-RUN (not installed)
```

`[report-with-fix]`: the toolchain ran in scratch and failed for a reason in the sample; the fix is a docs edit (or the code, when the doc is the contract). `[report-flagged]`: one link unproven (an install the lane lacked, a publication question), named with its settling command. Every run prints **all five** §s as `checked (k → m)`, `N/A (<reason>)`, `NOT-RUN (<toolchain>)`, `blocked (<lane>: <reason>)` or `Live, unreviewed`; NOT-RUN is never PASS.

## Precedents

The verifier reads [`precedents/documentation.md`](../../../../snippets/precedents/documentation.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most: § 6 recipes and placeholders, § 14 fences that do not compile on purpose, § 16 the doc is the contract, § 17 generated references, § 29 a harness is proven by failing, § 32 per-tool exit codes, § 33 NOT-RUN is never PASS, § 34 telemetry and archived tools. The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Documentation, V432, V440–V443.

## When to run

- On every whole-repo `/doc-refresh --audit`, printing all five §s.
- On a diff that renames or removes an export, changes a public signature or a value a doctest prints, edits a fenced sample, an embedded source region, a doc harness config, a CI test step, or the committed spec's schemas or examples.
- Before publishing a package: §1 and §2 on its README, because the registry page renders it.

## Halt conditions

- Do not report a HIGH or BLOCKER row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md); under `/doc-refresh --audit` that is `@verifier` in refute mode. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and keep the rest Unconfirmed, Hardening or Refuted. Never drop them.
- Halt on any finding without the fence (`doc:line`, language, scratch file), the tool output with its exit code, and the V-number.
- Never compile or run a fence in the audited tree, never install into it, never let a tool write caches there; scratch copies under `$OUT` only, and the write check must print nothing. Never run Runme or a doc's shell fences here (that is `quickstart-verify`'s container lane).
- A lane whose toolchain is absent is `NOT-RUN`, and a runner that collected nothing (pytest exit 5) is `NOT-RUN`: never PASS, never a finding.
- Do not compile a fragment, an excerpt or a recipe as if it were a program (§ 6, § 14), and do not print "samples are fine" without the class-coverage block.

## Related

- `doc-drift-scan` (this pack) owns the engine `scripts/doc-claims.py` (`--fences`, `embeds`, `specex`); `doc-structure-scan` owns the docs gate (DL-4) this skill's §4 mirrors for sample harnesses; `quickstart-verify` runs the setup; `docstring-coverage` grades docstrings.
- `/doc-refresh --audit` runs this skill; `--from-audit` closes each finding failing first from its V-number.
- Backend `http-contract-scan` §10 (when installed) owns the spec against the code; the testing pack (when installed) owns the suite the harness lives in.
