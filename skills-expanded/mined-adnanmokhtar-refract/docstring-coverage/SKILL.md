---
name: docstring-coverage
description: "Public API reference: undocumented exports (ratchet), docstrings that contradict the signature, broken doc-comment links. Read-only."
kind: skill
pack: documentation
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: docstring-coverage

## Premise

The API reference a consumer reads is generated from doc comments, so it rots the way code comments rot: a parameter is renamed and the `@param` keeps the old name, a function grows a `currency` argument the `Args:` section never mentions, an `{@link OrderClient}` survives the class it points to, and a new export ships with nothing at all. The reference renders green throughout, because TypeDoc's `notDocumented` is off by default and exits 0 on warnings unless they are promoted, rustdoc lints are warnings, `revive` and `dart analyze` exit 0 by default, and ruff's `DOC` rules do nothing without `--preview`. Code–comment inconsistencies appear in at least 11% of doc–code pairs (DocPrism).

This skill owns the **public API reference** classes: DD-1 a public export with no doc comment, gated as a **ratchet** (§1); DD-2 a doc comment that contradicts its signature: a `@param` / `Args:` name the signature does not have, a parameter it omits, a documented return or throw the code does not produce (§2); DD-3 an intra-doc or cross-reference link that resolves to nothing (§3). Prose docs that name symbols are `doc-drift-scan` §2; docstring **examples** that run as doctests are `doc-sample-scan` §2.

**Every finding cites the symbol at `path:line`, the public-surface evidence (the export, `__all__`, `pub`), the tool rule id or the census row, and the V-number.** A census row is a candidate, never a finding. "The API is documented" is never printed without the class-coverage block (§ Output). This skill is **read-only**: it prints why-first stubs, never writes them.

## The rule

A candidate becomes a finding only when all four hold:

1. **The symbol is public.** It is reachable from the package's entry: `package.json` `exports` / `main` / `types` and what they re-export, `__all__` (else the non-underscore names of the package's top-level modules), Rust `pub` items reachable from `lib.rs`, Go exported identifiers of a non-`internal` package, Java / Kotlin `public` in an exported module, Dart `lib/` outside `src/`. Application code that no other package imports is advisory (precedents § 23).
2. **The project's own convention was read**: the docstring style it configures (Google, NumPy, Sphinx; TSDoc / JSDoc), the rules it enables, the threshold it declares. This skill reports against that, never against a preference.
3. **The comment is missing, or contradicts the code**: no comment; a parameter name that is not in the signature; a parameter the signature has and a documented-parameters section omits; a `@throws` / `Raises:` the body cannot raise; a link to nothing. A comment that is merely terse is not a finding (the DocPrism lesson: report incorrectness, not taste).
4. **No record makes it intentional**: `@internal`, `@hidden`, `#[doc(hidden)]`, an override that inherits the contract (`@inheritDoc`, an interface implementation), generated code (protobuf, ORM, OpenAPI clients).

## Boundaries

- Prose docs naming a symbol the code no longer has → `doc-drift-scan` §2; a deprecated symbol presented as current in prose → §5 there. Here, only the doc comment attached to the symbol.
- Docstring examples executed as doctests → `doc-sample-scan` §2; fenced samples in Markdown → §1 there.
- The OpenAPI description of an endpoint → `@api-documenter` authors it; the committed spec against the code → backend `http-contract-scan` §10 (when the backend pack is installed).
- Comment debt (`TODO`, `FIXME`) in code → code-quality `debt-ledger` (when installed); a comment that encodes logic the code should carry → code-quality `correctness-smell-scan` (when installed).

## Lanes

Every tool lane runs **in a scratch copy** (`git archive HEAD | tar -x -C "$OUT/copy"`) with caches redirected to `$OUT`, from the repo's own installed binaries (`node_modules/.bin`, the project venv, the toolchain on the PATH), never `npx -y` or a global install; telemetry off (`CI=true DO_NOT_TRACK=1`). Each prints `ran (exit n) / NOT-RUN (<why>)`; NOT-RUN is never PASS (precedents § 33). The stdlib census below always runs.

| Stack | §1 coverage (ratchet) | §2 contradicts the signature | §3 xref | Trap |
|---|---|---|---|---|
| **Python** | `interrogate -v --fail-under <baseline> <pkg>`; `ruff check --select D1` | pydoclint 0.11 `--style=<the configured one>` (DOC101/102/103/201/501); ruff `D417` (google style only); ruff `DOC` only with `--preview` | Sphinx `-n` (nitpicky) | darglint is archived (2022): never a lane; the pydoclint baseline file regenerates itself, so read it, never trust its count |
| **TS / JS** | TypeDoc `--validation.notDocumented --treatValidationWarningsAsErrors`; API Extractor `ae-undocumented` (`api-extractor run`, never `--local` in a gate) | `eslint-plugin-jsdoc` `check-param-names`, `require-param`, `no-undefined-types` (only when the repo configures the plugin) | TypeDoc `validation.invalidLink` | `notDocumented` is off by default and warnings exit 0; `@internal` and `excludeInternal` change the surface |
| **Rust** | `RUSTFLAGS="-W missing_docs"` (`missing_docs` is a rustc lint) | — (read step) | `RUSTDOCFLAGS="-D rustdoc::broken_intra_doc_links" cargo doc --no-deps` | lints are warnings unless denied; `CARGO_TARGET_DIR="$OUT/target"` |
| **Go** | `revive` rule `exported` with `-set_exit_status` | — (read step) | — | revive exits 0 without `-set_exit_status` |
| **JVM** | `javadoc -Xdoclint:missing` | `-Xdoclint:params` | `{@link}` errors under `-Xdoclint:reference` | a build passing `-Xdoclint:none` is silencing it: grep for it (P2) |
| **Dart** | `public_member_api_docs` | — | `dart doc --dry-run` warnings [K?] | `dart analyze` exits 0 on infos without `--fatal-infos` |

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). `PKGS` overrides the public packages. Every grep ends in `ck`.

```bash
OUT="$(mktemp -d "${TMPDIR:-/tmp}/docstring.XXXXXX")"; export GIT_OPTIONAL_LOCKS=0 CI=true DO_NOT_TRACK=1; : > "$OUT/stamp"
ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/{dist,build,vendor,.venv,target,coverage,generated,__generated__}/**' -g '!**/{test,tests,__tests__,spec,fixtures,testdata}/**')
# P1. What is published (DD-1 severity) and where each package's public entry is.
rg -n --pcre2 '"(?:private|main|types|exports|name)"\s*:' -g '**/package.json' "${X[@]}" .; ck P1a $?
rg -n --pcre2 '^\[project\]|^name\s*=|^__all__\s*=|^\[lib\]|^publish\s*=\s*false' -g '**/pyproject.toml' -g '**/Cargo.toml' -g '**/__init__.py' "${X[@]}" .; ck P1b $?
# P2. The convention and the gates the repo already declares (mirror them; a silenced gate is a §1 row, not a style note).
rg -n --pcre2 '\[tool\.(?:interrogate|pydoclint)\]|fail[-_]under|pydocstyle|convention\s*=|select\s*=.*\bD\d*\b|"?notDocumented"?|treatValidationWarningsAsErrors|invalidLink|ae-undocumented|eslint-plugin-jsdoc|jsdoc/|missing_docs|broken_intra_doc_links|-Xdoclint|public_member_api_docs|\bexported\b' -g '*.{toml,cfg,ini,json,jsonc,yml,yaml,mjs,cjs,js,ts,rs,gradle,kts,xml}' -g '!**/package-lock.json' -g '!**/pnpm-lock.yaml' "${X[@]}" .; ck P2 $?
# P3. The stdlib census: public symbols, their doc comments, and the comment-vs-signature contradictions (§1–§3 candidates).
python3 -I - "${PKGS:-}" > "$OUT/census.tsv" <<'PY'
import ast, json, os, re, sys
PRUNE = {'node_modules', 'dist', 'build', '.venv', 'venv', 'target', 'tests', 'test', '__tests__', 'spec', 'fixtures', 'generated', '.git'}
def walk(top):
    for d, ds, fs in os.walk(top):
        ds[:] = [x for x in ds if x not in PRUNE and not x.startswith('.')]
        yield d, fs
pkgs = [p for p in sys.argv[1].split(',') if p] or sorted({d for d, fs in walk('.') for f in fs if f in ('package.json', 'pyproject.toml')})
def out(c, f, *r): print('\t'.join([c, os.path.normpath(f)] + [str(x) for x in r]))
for pk in pkgs:
    pj = os.path.join(pk, 'package.json'); pub = 'app'
    if os.path.isfile(pj):
        m = json.load(open(pj)); pub = 'private' if m.get('private') else 'published'
        entry = next((os.path.join(pk, c) for c in ('src/index.ts', 'src/index.tsx', 'index.ts', 'src/index.js') if os.path.isfile(os.path.join(pk, c))), None)
        if not entry: continue
        files, seen = [entry], set()
        while files:
            f = files.pop()
            if f in seen or not os.path.isfile(f): continue
            seen.add(f); t = open(f, encoding='utf-8', errors='replace').read(); L = t.split('\n')
            for rel in re.findall(r'export\s+(?:\*|\{[^}]*\})\s+from\s+[\'"](\.[^\'"]+)[\'"]', t):
                b = os.path.normpath(os.path.join(os.path.dirname(f), re.sub(r'\.(?:js|mjs|cjs)$', '', rel))); files += [b + e for e in ('.ts', '.tsx', '/index.ts')]
            names = set(re.findall(r'export\s+(?:declare\s+)?(?:async\s+)?(?:function|class|const|interface|type|enum)\s+(\w+)', t))
            for i, l in enumerate(L):
                m2 = re.match(r'\s*export\s+(?:declare\s+)?(?:default\s+)?(?:async\s+)?(function|class|const|interface|type|enum)\s+(\w+)\s*(?:<[^>]*>)?\s*(\(([^)]*)\))?', l)
                member = not m2 and re.match(r'\s+(?:public\s+|static\s+|async\s+)*(?!if\b|for\b|while\b|switch\b|return\b|catch\b)(method)?(\w+)\s*(\(([^)]*)\))\s*(?::[^{=]*)?\{\s*$', l)
                if member: m2 = member   # a class member: graded for DD-2 / DD-3 only, never DD-1
                if not m2: continue
                j = i - 1
                while j >= 0 and (L[j].strip().startswith('@') and not L[j].strip().startswith('@param')): j -= 1
                doc = ''
                if j >= 0 and L[j].strip().endswith('*/'):
                    k = j
                    while k >= 0 and '/**' not in L[k]: k -= 1
                    doc = '\n'.join(L[k:j + 1]) if k >= 0 else ''
                if re.search(r'@internal|@hidden|@inheritDoc', doc): continue
                if not doc:
                    if not member: out('DD-1', f, i + 1, m2.group(2), pub, 'no doc comment')
                    continue
                params = [re.sub(r'[?:=\s].*$', '', p.strip().lstrip('.')) for p in (m2.group(4) or '').split(',') if p.strip()]
                for dp in re.findall(r'@param\s+(?:\{[^}]*\}\s+)?\[?(\w+)', doc):
                    if m2.group(4) is not None and dp not in params:
                        at = next((k + 1 for k in range(i - 1, -1, -1) if re.search(r'@param\s+(?:\{[^}]*\}\s+)?\[?' + dp + r'\b', L[k])), i + 1)
                        out('DD-2', f, at, '%s @param %s' % (m2.group(2), dp), pub, 'not in the signature (%s)' % ', '.join(params))
                for ln in re.findall(r'\{@link(?:code|plain)?\s+([\w.]+)', doc):
                    if ln.split('.')[0] not in names and not re.search(r'\b(?:class|interface|type|function|const|enum|import)\b[^\n]*\b' + re.escape(ln.split('.')[0]) + r'\b', t):
                        at = next((k + 1 for k in range(i - 1, -1, -1) if '{@link' in L[k] and ln in L[k]), i + 1)
                        out('DD-3', f, at, '{@link %s}' % ln, pub, 'no such symbol in this module or its imports')
    elif os.path.isfile(os.path.join(pk, 'pyproject.toml')):
        pub = 'published' if re.search(r'^\[project\]', open(os.path.join(pk, 'pyproject.toml')).read(), re.M) else 'app'
        defined = {n.name for d, fs in walk(pk) for fn in fs if fn.endswith('.py') for n in ast.walk(ast.parse(open(os.path.join(d, fn), encoding='utf-8', errors='replace').read())) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
        for d, fs in walk(pk):
            for fn in fs:
                if not fn.endswith('.py'): continue
                src = open(os.path.join(d, fn), encoding='utf-8', errors='replace').read().split('\n')
                for k, x in enumerate(src):   # DD-3: mkdocstrings [text][pkg.name] and Sphinx :func:`name` targets
                    for ref in re.findall(r'\]\[([\w.]+)\]|:(?:func|class|meth|obj):`~?([\w.]+)`', x):
                        r = (ref[0] or ref[1]).split('.')[-1]
                        if r and r not in defined: out('DD-3', os.path.join(d, fn), k + 1, r, pub, 'xref target defined nowhere in the package')
        for d, fs in walk(pk):
            for fn in fs:
                if not fn.endswith('.py') or fn.startswith('test'): continue
                f = os.path.join(d, fn); tree = ast.parse(open(f, encoding='utf-8', errors='replace').read())
                allv = next((n.value for n in tree.body if isinstance(n, ast.Assign) and any(getattr(t_, 'id', '') == '__all__' for t_ in n.targets)), None)
                allow = {e.value for e in getattr(allv, 'elts', []) if isinstance(e, ast.Constant)} if allv is not None else None
                for n in tree.body:
                    if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) or n.name.startswith('_'): continue
                    if allow is not None and n.name not in allow: continue
                    doc = ast.get_docstring(n)
                    if not doc: out('DD-1', f, n.lineno, n.name, pub, 'no docstring'); continue
                    if isinstance(n, ast.ClassDef): continue
                    sig = [a.arg for a in n.args.args + n.args.kwonlyargs if a.arg not in ('self', 'cls')]
                    m3 = re.search(r'(?ms)^(?:Args|Arguments|Parameters)\s*:?\s*\n(?:-+\n)?(.*?)(?:\n\s*\n|\Z)', doc)
                    named = re.findall(r'(?m)^\s{0,8}(\w+)\s*(?:\([^)]*\))?\s*:', m3.group(1)) if m3 else []
                    raw = n.body[0].value.value.split('\n'); d0 = n.body[0].lineno
                    for p in named:
                        if p not in sig: out('DD-2', f, d0 + next((k for k, x in enumerate(raw) if re.match(r'\s*' + p + r'\s*(?:\([^)]*\))?\s*:', x)), 0), '%s Args %s' % (n.name, p), pub, 'not in the signature (%s)' % ', '.join(sig))
                    for p in (sig if named else []):
                        if p not in named: out('DD-2', f, n.lineno, '%s Args omits %s' % (n.name, p), pub, 'parameter undocumented while others are')
PY
echo "census: $(wc -l < "$OUT/census.tsv" | tr -d ' ') rows"; cut -f1,5 "$OUT/census.tsv" | sort | uniq -c
# Tool lanes, scratch copy only (each NOT-RUN when its binary is absent; never npx -y).
mkdir "$OUT/copy" && git archive HEAD | tar -x -C "$OUT/copy"
[ -x node_modules/.bin/typedoc ] && { (cd "$OUT/copy" && "$OLDPWD/node_modules/.bin/typedoc" --validation.notDocumented --validation.invalidLink --treatValidationWarningsAsErrors --out "$OUT/typedoc" > "$OUT/typedoc.txt" 2>&1); echo "typedoc exit $? (non-zero = warnings promoted: read the rows)"; } || echo "typedoc NOT-RUN (not installed)"
PY_BIN=python3; [ -x .venv/bin/python ] && PY_BIN="$PWD/.venv/bin/python"
"$PY_BIN" -m pydoclint --version >/dev/null 2>&1 && { (cd "$OUT/copy" && "$PY_BIN" -m pydoclint --quiet . > "$OUT/pydoclint.txt" 2>&1); echo "pydoclint exit $?"; } || echo "pydoclint NOT-RUN (not installed)"
"$PY_BIN" -m interrogate --version >/dev/null 2>&1 && { (cd "$OUT/copy" && "$PY_BIN" -m interrogate -v --fail-under 0 . > "$OUT/interrogate.txt" 2>&1); echo "interrogate exit $? — $(grep -m1 -i 'actual' "$OUT/interrogate.txt")"; } || echo "interrogate NOT-RUN (not installed)"
command -v cargo >/dev/null && [ -f Cargo.toml ] && { (cd "$OUT/copy" && CARGO_TARGET_DIR="$OUT/target" RUSTFLAGS="-W missing_docs" RUSTDOCFLAGS="-D rustdoc::broken_intra_doc_links" cargo doc --no-deps --offline > "$OUT/rustdoc.txt" 2>&1); echo "rustdoc exit $?"; } || echo "rustdoc N/A or NOT-RUN"
find . -newer "$OUT/stamp" -type f -not -path './node_modules/*' -not -path './.git/*' | head -3; echo "write check done (empty = nothing written)"
```

The census is a candidate generator: TypeScript is read by regex from each package's entry and the modules it re-exports one hop at a time, Python by `ast` with `__all__`; Rust, Go, JVM and Dart rely on their tool lanes. A census row the tool lane contradicts loses.

## Measured

Measured 2026-10-19 on the seeded `benchmarks/fixtures/doc-drift` copy (write check empty): P1 10, P2 5 (ruff `D` with the google convention and `[tool.pydoclint]` in `py-money`, TypeDoc `treatValidationWarningsAsErrors` in the SDK), no grep exited 2. The census printed 7 rows over two published packages, **all six DD seeds** (an undocumented exported `verifyWebhookSignature` reached through a `./webhooks.js` re-export, `allocate` with no docstring, `@param includeVoided` on a method whose signature takes `opts`, `Args: rounding` on `to_minor`, `{@link OrderClient}` to a removed class, a mkdocstrings `[split_even][py_money.split_even]` to nothing) plus one twin (`@param limit` on the same method). Its first version printed 2 rows: it appended `.ts` to `./webhooks.js` re-exports (ESM TypeScript writes the `.js` extension), read only `export` lines (class methods were invisible to DD-2), and had no Python xref lane; all three are fixed. typedoc, pydoclint and interrogate printed `NOT-RUN (not installed)`. No other fixture publishes a library with a public doc-comment surface; on them the census prints only `app` rows, advisory under § 23.

## The 3,000-row path

An unannotated codebase prints thousands of DD-1 rows. A coverage number is not a list of findings.
1. **Surface first.** Drop `app` rows to one advisory count (§ 23); keep published packages and workspace-boundary exports.
2. **Ratchet, never a fixed bar.** The baseline is, in order: the threshold the project declares (`fail-under`, `#![deny(missing_docs)]`, TypeDoc validation in CI); the coverage a previous `/doc-refresh` recorded in `ai/dynamic/drift-log.md`; else this run's number, printed as the proposed baseline. A finding is a **decline** against the baseline or an undocumented symbol **added by the diff**; the backlog is one Hardening row with its count.
3. **DD-2 and DD-3 are read one by one**: they are wrong statements, not absences, and they are few.
4. **Group by root cause**: one renamed parameter repeated across overloads is one finding.
5. **Ledger the rest** as `Live, unreviewed (k packages)` with the `PKGS=` command that continues it.

## Scans for

| § | Class | Census / lane | Finding when | Default | Oracle |
|---|---|---|---|---|---|
| 1 | DD-1 public export undocumented (ratchet) | census DD-1 · interrogate · ruff D1 · TypeDoc `notDocumented` · `ae-undocumented` · `missing_docs` · revive `exported` · `-Xdoclint:missing` · `public_member_api_docs` | coverage declines against the baseline, or the diff adds an undocumented public symbol | MEDIUM for a published package; LOW otherwise; advisory for `app` (§ 23) | V444 |
| 2 | DD-2 doc comment contradicts the signature | census DD-2 · pydoclint DOC101/102/103/201/501 · ruff D417 · jsdoc `check-param-names` / `require-param` · `-Xdoclint:params` | a documented name the signature lacks, a parameter omitted while others are documented, a return or throw the body cannot produce | MEDIUM | V444 |
| 3 | DD-3 xref unresolved | census DD-3 · TypeDoc `invalidLink` · `broken_intra_doc_links` · Sphinx `-n` · `{@link}` doclint | the link resolves to no symbol the docs can render | LOW | V444 |

### 1. Public export undocumented (DD-1)

```
BAD:   packages/sdk/src/index.ts:14   export function createClient(opts: ClientOptions) {     (no /** */; package published)
GOOD:  /** Creates a client bound to one API key. Throws ConfigError when baseUrl is not https. */
```
**Read the docs and the code:** Is the symbol reachable from the package entry (follow the re-exports, not the file name)? Is the package published (`private` absent, a `[project]` table, `publish` not false) or imported across a workspace boundary? Does it inherit its contract (an override, an interface implementation)? Is it `@internal`? Did coverage decline against the baseline, or did this diff add it? **Finding when** a public symbol is undocumented and the ratchet says so. **Proof:** V444, the tool rule (or the census) exits clean on the symbol and coverage is not below the recorded baseline. The fix prints a why-first stub (the contract, what it assumes, what it raises); a stub that restates the signature is the defect this class exists to catch.

### 2. Doc comment contradicts the signature (DD-2)

```
BAD:   packages/py-money/money/minor_units.py:22   def to_minor(amount, currency):    Args: amount, rounding    (no `rounding`; `currency` undocumented)
       packages/sdk/src/orders.ts:31          @param limit   list(opts: ListOptions)                    (the positional `limit` is gone)
GOOD:  the Args / @param list equal to the signature, in order, each with its contract
```
**Read the docs and the code:** Is the convention one the census parses (Google `Args:`, NumPy `Parameters`; TSDoc `@param`)? `**kwargs` / rest parameters, and destructured options documented as `opts.limit`, are fine. Does the body raise what `Raises:` says (follow one call)? **Finding when** the comment states a name, a parameter set or a throw the code contradicts. **Proof:** V444 (pydoclint or jsdoc on the symbol exits clean after; the census prints no row).

### 3. Cross-reference unresolved (DD-3)

```
BAD:   packages/sdk/src/client.ts:8   /** Wraps {@link OrderClient}. */        (OrderClient was removed in 2.0)
GOOD:  {@link Client} · or the sentence rewritten
```
**Read the docs and the code:** Is the target exported from another module the census did not read (an imported type is fine)? An external crate or package link is fine when the dependency documents it. **Finding when** the link resolves to nothing the docs can render. **Proof:** V444 (TypeDoc `invalidLink` / `broken_intra_doc_links` exits clean after).

## Output

```
docstring-coverage — 2 public packages (@acme/sdk published, py-money published) · 1 app · convention google (pyproject) · TSDoc
Coverage: @acme/sdk 81% (17/21, baseline 86% from drift-log 2026-09-30 → DECLINE) · py-money 90% (9/10)
Lanes: census ran · typedoc NOT-RUN (not installed) · pydoclint NOT-RUN (not installed) · interrogate NOT-RUN

Findings: 3
1. packages/sdk/src/index.ts:14     [report-with-fix]  MEDIUM · §1   createClient — exported, published, no doc comment (added by this diff).
   Stub: /** Creates a client for one API key. <what it assumes> <what it throws> */
2. packages/py-money/money/minor_units.py:22  [report-with-fix]  MEDIUM · §2   to_minor — Args names `rounding` (not in the signature); omits `currency`.
3. packages/sdk/src/client.ts:8      [report-with-fix]  LOW · §3      {@link OrderClient} — no such symbol (removed 2.0).

Verification: 9 candidates → 3 findings · 0 unconfirmed · 5 hardening (app symbols, § 23) · 1 refuted (@inheritDoc override)

Class coverage:
  §1 undocumented export   checked (31 public symbols → 4 undocumented → 1 decline finding; 1 backlog row)
  §2 contradicts signature checked · census (25 documented → 1)
  §3 xref                  checked · census (6 links → 1); typedoc invalidLink NOT-RUN
```

`[report-with-fix]`: the symbol is public, the convention was read, the contradiction or absence is cited; the fix is the comment (printed, never written). `[report-flagged]`: one link unproven (is the package published? does the override inherit?), named with its settling probe. Every run prints **all three** §s as `checked (k → m)`, `checked · census`, `N/A (no public package)`, `NOT-RUN (<tool>)`, `blocked (<reason>)` or `Live, unreviewed`.

## Precedents

The verifier reads [`precedents/documentation.md`](../../../../snippets/precedents/documentation.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most: § 17 generated references are fixed at the source, § 23 application code docstrings are advisory, § 32 per-tool exits (TypeDoc warnings exit 0), § 33 NOT-RUN is never PASS, § 34 archived tools (darglint). The oracle is [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Documentation, V444.

## When to run

- On every whole-repo `/doc-refresh --audit`, printing all three §s.
- On a diff that adds, renames or changes the signature of an exported symbol, edits a doc comment, or changes a package's `exports`, `__all__` or `private` flag.
- Before publishing a package: §1 against the recorded ratchet, §2 and §3 on the whole surface.

## Halt conditions

- Do not report a HIGH or BLOCKER row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md); under `/doc-refresh --audit` that is `@verifier` in refute mode. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and keep the rest Unconfirmed, Hardening or Refuted. Never drop them.
- Refuse a coverage claim without the enumerated public surface and how it was delimited; refuse a threshold without its provenance (the declared one, the recorded ratchet, or "this run, proposed"). A round number with no source is an unsourced magnitude.
- Never write or edit a doc comment here, and never generate one that restates the signature; print the why-first stub. `/doc-refresh --from-audit` applies a DD-2 fix as a comment-only edit, proved by a diff that touches comment lines only.
- Never impose a docstring convention the project has not chosen; never run a tool lane in the tree or let it write caches there. The write check must print nothing.
- A tool lane whose binary is absent is `NOT-RUN`, never PASS; do not print "the API is documented" without the class-coverage block.

## Related

- `doc-drift-scan` (this pack) — prose docs naming symbols (§2) and deprecated APIs presented as current (§5); `doc-sample-scan` runs docstring doctests (§2) and compiles fenced samples.
- `/doc-refresh` — runs this skill in its non-prose gate and its audit; the default mode records the coverage line the ratchet reads back.
- `@doc-writer` writes the contract prose a stub asks for; `@api-documenter` owns the endpoint descriptions in the spec.
- `.claude/rules/doc-principles.md` — the WHY-not-WHAT rule a signature-restating comment breaks.
