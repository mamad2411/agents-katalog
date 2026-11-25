---
name: naming-layout-scan
description: File, directory, identifier, synonym and placement names vs the naming rules the project declares (AL-16–19).
kind: skill
pack: align
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: naming-layout-scan

## Premise

A name is how the next person finds the code. A component file named `invoicelist.tsx` where the project writes `InvoiceList.tsx`, a `features/OrderHistory/` directory where every sibling is kebab-case, a `loading` prop where the project says booleans start with `is`, a `/clients/:id` route where the glossary says *customer*, a test under `__tests__/` where the project co-locates them: each one breaks a search, a glob, an import on a case-insensitive file system, or the next producer/consumer pair.

None of that is a finding by taste. A name is wrong only against a rule the **project declares** for that scope, and only when no framework mandates the name. This skill owns four align classes:

- **§ 1 AL-16** file and directory names;
- **§ 2 AL-17** identifier names (code-quality's CQ-M17 has no runnable skill, so align owns it);
- **§ 3 AL-18** synonym drift against a declared glossary;
- **§ 4 AL-19** placement: the declared module skeleton, test co-location, barrel policy.

`scripts/name-check.py` (this skill) checks every name against the rule table `convention-oracle` § 0 builds with `oracle-map.py`: ls-lint directory keys, check-file and unicorn globs, `@typescript-eslint/naming-convention`, Ruff `N`, and doc bullets that name a subject and a case, prefix, suffix or export match.

**Every finding cites the site `<path[:line]>` + the oracle row (rule id and config file, or doc `path:line` with its quote) + the expected and actual shape + the rename that closes it + whether any wire, DB, env or generated name depends on it.** A grep hit is never a finding by itself. "Names clean" is never printed without the class-coverage block (§ Output).

## The rule

A name is a finding when all four hold ([`precedents/align.md`](../../../../snippets/precedents/align.md), the claim restated):

1. **The rule is declared for this scope.** A T1 rule at `error` (ls-lint, check-file, unicorn `filename-case`, `naming-convention`, Ruff `N8xx`, IDE1006) or a T2 line written by a human. A T2g line makes the row **Unconfirmed** behind one ratification probe per rule (§ 28); a contested category is AL-02 in `convention-oracle` §2, not a naming row (§ 29). A majority of siblings is not a rule (§ 1).
2. **No framework mandates the name** (§ 13): Next.js `page|layout|loading|error|route.tsx`, `[id].tsx`, `$param.tsx`, `+page.svelte`, `_app`, `App.vue`, `index.*` barrels, `__init__.py`, `conftest.py`, timestamped migrations, `Dockerfile`, Go `_test.go`, Nest and Angular role files whose stems the CLI writes kebab.
3. **The name is not fixed by a contract** (§ 15): a JSON wire field (`@Expose({ name })`, `@JsonProperty`, `alias=`), a DB column (`db_column`, `@Column({ name })`), an env var, a third-party callback, a generated client. A rename there is a contract change for `/refactor` with an ADR.
4. **The rename is mechanical and provable** (V402): references resolve, types and build pass, no serialised name moves.

## Boundaries

- **A split in naming with no declared winner** ("half the hooks are kebab, half camel") → `convention-oracle` § 2 (AL-02): a census and a proposal, 0 ledger rows. `name-check.py --census` feeds it.
- **A doc rule the code consistently ignores** → `convention-oracle` § 4 (AL-04): the doc may be stale, and the code is not renamed until a human decides.
- **API field and path casing** (AL-24) → backend `api-consistency-audit` §3, when the backend pack is installed; `/polish` introduces a casing convention. Without the backend pack: `N/A (owner pack backend not installed)`.
- **i18n key namespace drift and missing keys** (AL-27) → frontend `i18n-scan` §2 (`catalog-parity.py`), when the frontend pack is installed. § 3 here reads i18n **keys** only for glossary synonyms.
- **Layer direction and private cross-module imports** (AL-20/21) → code-quality `architectural-diagnosis` §1–§2 (always installed). § 4 here checks only that declared module paths, barrels and test placement exist as declared.
- **A suppression of a naming rule** → `convention-ratchet-scan` §1 (AL-29). **A naming rule only at `warn`, or never run in CI** → `convention-oracle` §3 (AL-03).
- **Dead files** found while walking names → code-quality `dead-code-scan`, not a rename.

## Adapt to the codebase — the naming lanes

Read the tools **and their versions** from `$RUN/oracle/versions.tsv` and the gates from `gates.tsv`, never from memory. A tool lane that runs is the oracle's own verdict for its rules; `name-check.py` covers doc rules and every lane whose tool is absent. Tool facts are from the align research catalog (2026-10-18).

| Lane | T1 rule that may exist | Run it (project-local binary, offline) | Version gate | Fallback |
|---|---|---|---|---|
| **Any stack, files and directories** | ls-lint 2.3 `.ls-lint.yml` (`ls:` per directory, `.dir`, per extension, `ignore:`) | `node_modules/.bin/ls-lint` from the repo root | A deeper directory key **overrides** its parents for the whole subtree, so one key can loosen a scope by accident: read the effective key per directory | `name-check.py` reads `.ls-lint.yml` itself |
| **JS / TS** — React, Vue, Svelte, Angular, Node | `check-file/filename-naming-convention` and `folder-naming-convention` 3.3; `unicorn/filename-case` 78; `@typescript-eslint/naming-convention` 8.71 | `node_modules/.bin/eslint -f json` with no `--cache` (one run serves §1 and §2) | unicorn ≥ 65 also checks **directories** (a count jump after the bump is a rebaseline, § 3); `naming-convention` with `types` needs type info, so TS 7 without a `@typescript/typescript6` alias makes those selectors `NOT RUN (TS7, no programmatic API)`; check-file sees only files ESLint is configured to visit | `name-check.py` + grep 2c |
| **Vue / Svelte / Angular** | the same rules through the framework's ESLint parser; `vue/component-definition-name-casing`, `vue/multi-word-component-names` | as JS / TS | `App.vue`, `+page.svelte`, Angular `*.component.ts` stems are framework names (§ 13) | `name-check.py` |
| **Python** | Ruff `N8xx` (N801 class, N802 function, N806 variable, N815/N816 mixed case, N999 module) | `ruff check --no-cache --select N --output-format concise` | Ruff 0.17 | `name-check.py` |
| **Go** | revive `var-naming` (initialisms allowlist); lower-case package names are built in | the user's own `golangci-lint run` (GPL-3.0: run, never vendor) | v2 config | grep by hand per declared rule |
| **Java / Kotlin** | Checkstyle naming checks, detekt naming rules, ArchUnit / Konsist naming tests | the project's lint or test task | detekt 2.x needs a regenerated baseline | the rule's own test |
| **.NET** | `.editorconfig` `dotnet_naming_rule.*` + IDE1006 | the .NET build (`dotnet build`) with `EnforceCodeStyleInBuild` | only the **IDE1006 diagnostic severity** is enforced at build; a per-naming-rule severity is ignored there | read `.editorconfig` |
| **Ruby / PHP** | RuboCop `Naming/*`; PHP_CodeSniffer naming sniffs | `rubocop --only Naming`; `vendor/bin/phpcs` | — | grep by hand |

A tool that is absent prints `blocked (<tool> not installed)` for its lane, and `name-check.py` still runs. Never `npx -y`; `--online` installs only into `$RUN/tools`. Before any CLI: `DO_NOT_TRACK=1 CI=true`.

## Pre-flight

Run as **one** bash script from the repo root. Step **N** feeds detector **§N**. Every `rg` names its path; any `rg` exit 2 is a failed search, never zero hits. Tests, stories and specs **stay in** the file list: naming and placement apply to them unless § 11 or § 13 says otherwise. The file list reaches `name-check.py` only through `--files=<list>` (or `--files=-` on a pipe). The script never reads stdin implicitly: an agent shell's open stdin hung the earlier read-when-not-a-terminal rule until a 120 s timeout (measured 2026-10-18).

```bash
[ -n "${BASH_VERSION:-}" ] || { echo "pre-flight: run it with bash (save it, then bash <file>): PIPESTATUS and arrays are bash-only, and under zsh every exit prints blank"; exit 2; }
ROOTS=(.)   # code roots; in a monorepo name them: ROOTS=(apps/web apps/api packages)
CO="${CO:-.claude/skills/convention-oracle/scripts}"; NL="${NL:-.claude/skills/naming-layout-scan/scripts}"
RUN="${RUN:-$(mktemp -d "${TMPDIR:-/tmp}/align.XXXXXX")}"; mkdir -p "$RUN"; echo "RUN=$RUN"
export GIT_OPTIONAL_LOCKS=0 DO_NOT_TRACK=1 CI=true
# Generated, vendored and build trees only (§ 16). W also drops tests and docs, for the identifier and synonym greps.
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/third_party/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**'
   -g '!**/.venv/**' -g '!**/__generated__/**' -g '!**/*.gen.*' -g '!**/*.min.*')
W=(-g '!**/*.{spec,test,stories,story}.*' -g '!**/{test,tests,__tests__,e2e,__mocks__,fixtures,migrations}/**' -g '!**/*.md' -g '!ai/**' -g '!docs/**')

# 0. The oracle map (convention-oracle § 0), built once per run and shared; then the gates that change what a lane can see.
[ -s "$RUN/oracle/rules.tsv" ] || { python3 -I "$CO/oracle-map.py" . --out="$RUN/oracle" --age-buckets; echo "oracle-map exit $?"; }
awk -F'\t' '$1 ~ /^(ts7-no-api|unicorn-dirs|eslint-major|peer<=9)$/' "$RUN/oracle/gates.tsv"

# 1 + 2 + 4. File, directory and identifier names, and the declared skeleton (module paths, test placement, barrels).
rg --files "${ROOTS[@]}" "${X[@]}" > "$RUN/files.txt"; echo "rg files exit $? ($(wc -l < "$RUN/files.txt" | tr -d ' ') files)"
python3 -I "$NL/name-check.py" . --files="$RUN/files.txt" --oracle="$RUN/oracle" --skeleton > "$RUN/names.tsv" 2> "$RUN/names.ledger"
echo "name-check exit $? (0 none · 1 candidates · 2 usage or an empty list)"; cat "$RUN/names.ledger"; cut -f1,2,4,5,6,8,9 "$RUN/names.tsv"
#    1b + 2b. Tool lanes, project-local binaries only; a missing binary is `blocked` and the script rows stand.
if [ -x node_modules/.bin/ls-lint ]; then node_modules/.bin/ls-lint > "$RUN/ls-lint.txt" 2>&1; echo "ls-lint exit $?"; else echo "ls-lint: blocked (not installed)"; fi
if [ -x node_modules/.bin/eslint ]; then
  node_modules/.bin/eslint -f json "${ROOTS[@]}" > "$RUN/eslint.json"; echo "eslint exit $? (2 = config error or crash, not findings)"
  python3 -I -c 'import json,sys,re; n=re.compile(r"naming-convention|check-file/|filename-case|^camelcase$|^id-match$")
for f in json.load(open(sys.argv[1])):
    for m in f["messages"]:
        if m.get("ruleId") and n.search(m["ruleId"]): print("%s:%s\t%s\t%s" % (f["filePath"], m.get("line"), m["ruleId"], m["message"][:90]))' "$RUN/eslint.json"
else echo "eslint lane: blocked (not installed)"; fi
RUFF=$(command -v .venv/bin/ruff || command -v ruff)
if [ -n "$RUFF" ] && rg -q --pcre2 '"N\d*"|\bN8\d\d\b' -g '{pyproject.toml,ruff.toml,.ruff.toml}' "${X[@]}" .; then "$RUFF" check --no-cache --select N --output-format concise "${ROOTS[@]}"; echo "ruff N exit $? (1 = violations)"; else echo "ruff N: N/A or blocked"; fi
#    2c. Grep fallback for a DECLARED identifier rule no tool ran. Example rule: booleans start with is/has/should/can.
rg -n --pcre2 '\b(?:const|let|var)\s+(?!(?:is|has|should|can|was|did|will)[A-Z])([a-z]\w*)\s*(?::\s*boolean\b|=\s*(?:true|false)\b)|^\s*(?!(?:is|has|should|can)[A-Z])([a-z]\w*)\??\s*:\s*boolean\b' -g '*.{ts,tsx,vue,svelte}' "${X[@]}" "${W[@]}" "${ROOTS[@]}" > "$RUN/bool.txt"; echo "rg 2c exit $? ($(wc -l < "$RUN/bool.txt" | tr -d ' ') lines; read only under a declared rule)"

# 3. AL-18: only with a declared glossary. Each avoided term becomes a camel-aware pattern
#    (`client`, `clientId`, `ClientCard`, `fetch_clients`; not `clientele`), searched in code and route strings, then i18n KEYS.
#    A table row is read in the column its header names (`Not`, `Avoid`, `Synonyms`, `Aliases`, `Deprecated`): the header is
#    found above the row in the cited file, never assumed to be column 2. A headerless two-column table reads column 2; a wider
#    table whose header names no such column prints a line to read by hand, never a silent N/A.
awk -F'\t' '$4=="glossary"' "$RUN/oracle/docs.tsv" > "$RUN/glossary.tsv"
python3 -I -c 'import re,sys
terms=set(); AV=re.compile(r"(?:not|avoid(?:ed)?|synonyms?|aliases?|aka|deprecated|forbidden|banned|do not use|never|instead of)\b",re.I)
cells=lambda s: [x.strip(" `") for x in s.strip().strip("|").split("|")]
def col(src, width):
    p, _, n = src.rpartition(":")
    try: L = open(p, encoding="utf-8", errors="replace").read().split("\n")[:int(n)]
    except (OSError, ValueError): L = []
    for k in range(len(L) - 1, 0, -1):
        if not L[k].lstrip().startswith("|"): break
        if re.fullmatch(r"\s*\|?(?:\s*:?-+:?\s*\|)+\s*:?-*:?\s*\|?\s*", L[k]):
            m = [i for i, h in enumerate(cells(L[k - 1])) if AV.match(h)]
            return m[0] if m else (1 if width == 2 else None)
    return 1 if width == 2 else None
for l in open(sys.argv[1]):
    f=l.rstrip("\n").split("\t"); q=f[-1]; src=f[-2] if len(f)>1 else ""
    if not q.lstrip().startswith("|"):
        terms.update(m.group(1).lower() for m in re.finditer(r"\b(?:not|never|avoid|instead of|synonyms?:?|aka)\s+(?:(?:say|use|write|call)\s+)?[`\x27\"]?([A-Za-z]{3,})", q, re.I)); continue
    c=cells(q); k=col(src, len(c))
    if k is None or k>=len(c): print("3: %s: no avoid column named in the table header; read it by hand" % src, file=sys.stderr); continue
    terms.update(t.strip(" `\x27\"").lower() for t in re.split(r"[,;/]", re.sub(r"\([^)]*\)", "", c[k])) if re.fullmatch(r"\s*[`\x27\"]?[A-Za-z]{3,}[`\x27\"]?\s*", t))
for t in sorted(terms): print("(?<![A-Za-z])%ss?(?![a-z])|%ss?(?![a-z])" % (t, t[0].upper()+t[1:]))' "$RUN/glossary.tsv" > "$RUN/synonyms.txt"; echo "3: $(wc -l < "$RUN/synonyms.txt" | tr -d ' ') avoided terms from $(wc -l < "$RUN/glossary.tsv" | tr -d ' ') glossary rows"
if [ -s "$RUN/synonyms.txt" ]; then
  rg -n --pcre2 -f "$RUN/synonyms.txt" "${X[@]}" "${W[@]}" -g '!**/{locales,i18n,translations}/**' "${ROOTS[@]}" > "$RUN/syn-code.txt"; echo "rg 3a exit $? ($(wc -l < "$RUN/syn-code.txt" | tr -d ' ') lines)"
  rg -n --pcre2 '^\s*"[^"]*(?:'"$(paste -sd'|' "$RUN/synonyms.txt")"')[^"]*"\s*:' -g '**/{locales,i18n,translations}/**/*.json' "${X[@]}" "${ROOTS[@]}"; echo "rg 3b exit $? (keys only)"
elif [ -s "$RUN/glossary.tsv" ]; then echo "3: blocked (glossary rows found, no avoided term read: see the lines above)"
else echo "3: N/A (no glossary declared)"; fi
```

Read `names.ledger` first: one line per rule, `rule N1 (<oracle source>): matched N files · k candidates in f files · e exempt`, and `NOT RUN (vacuous: matched 0 files)` for a rule whose scope matched nothing. A vacuous rule proves nothing about its scope (§ 20, V399). A contested doc row makes no rule (it is AL-02). A doc rule that at least 80% of 5 or more matched files break prints `-> AL-04 candidate`: its rows come out as `advisory` (doc stale? § 18), never renames. One site broken the same way under several rules (the doc, check-file and ls-lint) is one row, the other rule ids in its note.

**Measured** (2026-10-18), whole script per fixture root; no ls-lint, ESLint or Ruff is installed in any of them, so those lanes printed `blocked` and `name-check.py` carried every class:

- `web-dashboard` (18 files, three T2 naming rules from `ai/conventions.md`): N1 "Component files are PascalCase and match the exported component name" matched 8 files → 2 candidate rows, both on one component file (case `flat`, and stem ≠ export): the fixture's naming seed, found. N2 hooks camelCase with `use` matched 3 → 0; N3 `src/lib/` kebab matched 2 → 0. § 4 skeleton 0 rows (no `ai/modules.md`). 2c printed 4 lines, none a row: no boolean rule is declared, and 3 of the 4 are `let cancelled = false` effect-cleanup locals. § 3 `N/A (no glossary declared)`.
- `convention-drift` (staged copy, 177 files listed, 16 rules from the doc, check-file, ls-lint and Ruff; re-run 2026-10-18): 14 rows, 0 false. 5 naming rows (one component file's case and its export, a PascalCase feature folder, an admin Vue file, a PascalCase Python function), 6 `advisory` AL-04 rows for the doc's `.store.ts` suffix that all 6 store files break, and 3 § 4 rows (`order-history/` absent, `__tests__/`, the `refunds` barrel). The first run printed 74 rows, 11 true: a doc subject dropped under "under `<dir>`", ls-lint's `camelCase | kebab-case` read as its first case, contested hook rows still emitted, and a check-file folder glob (`features/*/`) that matched 0 directories. Each is now a self-test case. The boolean prop `loading` in a card component is grep 2c's, not the script's. **9 of 9 seeds** after the glossary fix (re-run 2026-10-18): § 3 first printed `N/A (no glossary declared)` on the fixture's three-column `Term | Meaning | Not` glossary, because the synonym parser read column 2 (`Meaning`). It now reads the column the table header names: 11 avoided terms from 5 rows (`chargeback (that is …)` loses its parenthesis), 3a 48 lines, among them a route file (CD-AL18-a) and an events module (CD-AL18-b), most of the rest camel-case noise (`apiClient`, `QueryClient`, `http_client`, CD-DECOY-18 among them); 3b finds the `"clients"` keys in both catalogs. No decoy is a naming row.
- `quality-mix` (126 files): 0 naming rules declared (Ruff selects `E`, `F`, `I`; no `N`), so §1–§2 are `N/A (no naming rule declared)`; § 4 read `ai/architecture.md`'s layer table → 0 rows (its module paths are globs, which the skeleton check skips, and the plain ones such as `domain/` resolve tail-relative); 2c 5 lines, not rows.
- `a11y-states` (138 files) and `frontend-correctness` (113 files): no naming rule, no glossary, no module doc → §1–§4 `N/A`; 2c 3 and 0 lines. Their 48/48 and 41/41 PascalCase component files are a `convention-oracle` § 2 proposal, not a rule (§ 1).
- A real NestJS + React monorepo (read-only, re-measured 2026-10-18 after the fold-back fix): § 4 skeleton 0 rows → 1, `ai/modules.md:95` `features/placeholder/ absent` (the module the doc still lists; the fallback route moved). Its module catalog roots each section in the heading (`## apps/web (`apps/web/src/`)`) and writes table cells with no trailing slash, and the old reader needed both a path-only heading and a trailing slash, so it read nothing. A first cut printed 5 rows: a file stem cited as a module (`shared/errors` = `errors.ts`), a directory outside the scanned roots (`docs/decisions`) and a lint rule id (`<plugin>/platform-scope-justification`) now resolve. `convention-drift`: the same 3 § 4 rows.
- § 3 was exercised on a scratch tree (a glossary table `customer | client, buyer` plus `never purchase`): 3a matched `clientId`, `ClientCard`, `fetch_clients`, `purchaseTotal` and the event `order.removed`, and not `clientele`; 3b matched the key `"clients.title"` and not the value `"Our clients"`. A second scratch glossary (2026-10-18): a `Term | Avoid` table read column 2, a `Word | Meaning | Notes` table printed `no avoid column named in the table header; read it by hand` instead of a silent `N/A`, and the prose line ``Never say `purchase`.`` read `purchase` (the first parser read `say`).

## The 3,000-hit path

A repo that turns on a naming rule for the first time can return thousands of rows. Triage in this order and record every step in the coverage block:

1. **Intersect with the oracle.** Keep rows whose rule is T1 or T2 for that scope. A T2g rule collapses to **one** ratification line, however many files it touches.
2. **Group** by (rule, actual shape, directory). One decision covers a group: forty `*.Component.tsx` files under one folder are one rename policy, not forty findings.
3. **Rank** by newest files first (`ages.tsv`: new code is copied next), then exported names (they leak into imports), then churn.
4. **Read** the top 30 groups fully: the rule, two compliant siblings, the framework and wire-name checks.
5. **Ratchet the rest.** Turn the rule on at `error` with a bulk-suppression baseline (ESLint) or a shrink-only counter (`rg -c` per rule per file) and report `Live, ratcheted (k groups / n hits — <baseline file>)`; otherwise `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

| § | Class | Severity | Proof |
|---|---|---|---|
| 1 | AL-16 file or directory name against the declared case or pattern | Low | V402 |
| 2 | AL-17 identifier name against the declared convention | Low; Medium when exported | V402 |
| 3 | AL-18 synonym drift against a declared glossary | Low | V402 |
| 4 | AL-19 placement: declared module skeleton, test co-location, barrel policy | Low | V404 (V402 for the move) |

Convention classes are never Critical, and naming is never High.

### 1. File or directory name (AL-16)

```
BAD:   src/components/billing/invoicelist.tsx         rule: ai/conventions.md:8 "Component files are PascalCase and match the exported component name"
       features/OrderHistory/                          rule: .ls-lint.yml `.dir: kebab-case`
GOOD:  src/components/billing/InvoiceList.tsx         (exports InvoiceList)
       app/orders/[orderId]/page.tsx · src/routes/orders/$orderId.tsx · App.vue · __init__.py     (framework names, § 13)
```
**Read the code:** Which rule covers this path, and is it the **nearest** one (an ls-lint subtree key overrides its parents)? Is the name framework-mandated (`name-check.py` prints `exempt` rows with `--all`)? On unicorn ≥ 65, did the directory rows appear only after the bump? Then it is a rebaseline, not new drift (§ 3). Does anything import the path by a string the tooling cannot see (a dynamic `import()`, a route manifest, a Storybook glob)? On a case-insensitive file system, a case-only rename needs a two-step `git mv`. **Finding when** a declared T1/T2 rule covers the path, the name breaks it, and no exemption applies. **Proof:** V402 — `git mv`, then every reference resolves, `tsc --noEmit --incremental false` (no `.tsbuildinfo` written) and the build pass, and no generated or wire name changed.

### 2. Identifier name (AL-17)

```
BAD:   interface ButtonProps { loading: boolean }      rule: "Boolean props start with is/has/should" (naming-convention at error)
       def BuildDigest(request):                        rule: Ruff N802 at error
GOOD:  interface ButtonProps { isLoading: boolean }  ·  def build_digest(request):
       class OrderDto { @Expose({ name: 'created_at' }) createdAt }      (wire name fixed by contract, § 15)
```
**Read the code:** Is the identifier exported, or used across files (the rename is wider)? Is it bound by a wire contract (`@Expose`, `@JsonProperty`, `@SerializedName`, `alias=`, `db_column=`, `Field(alias=)`)? `name-check.py` never emits those, but a hand-read grep hit can. Is it a third-party callback name or a framework hook signature (`getServerSideProps`, `setUp`)? Does the typed selector need TS type information on a TS 7 repo? Then the lane is `NOT RUN (TS7, no programmatic API)` and only grep 2c stands, `Unconfirmed` until the rename compiles. A 2c line is never a row without a declared rule: on `web-dashboard`, 3 of 4 lines were `let cancelled = false` cleanup flags no rule covers. **Finding when** a declared rule names the pattern and the identifier breaks it outside a contract. **Severity:** Low; Medium when exported. **Proof:** V402 — rename through the language server or ts-morph (needs the TS 6 API), never a text replace; types and build pass; `oasdiff breaking` or a schema snapshot shows no serialised change when an API is near.

### 3. Synonym drift (AL-18)

```
BAD:   route /clients/:id · key "clients.title" · emit('order.removed')     glossary: customer (avoid: client) · deleted (avoid: removed)
GOOD:  /customers/:id · "customers.title" · emit('order.deleted')
       copy "Our clients love it" in en.json values                          (prose and catalog values are not identifiers)
```
**Read the code:** Is there a glossary at all (`ai/glossary.md`, a DDD ubiquitous-language doc)? Without one the class is `N/A`, and a felt synonym split is AL-02 at most. Does the term reach a **wire** (an event name a consumer subscribes to, a public route, a DB column)? Then renaming is a contract change: route it to `/refactor` with an ADR (§ 15) and report the internal sites only. Does the synonym belong to a third party's vocabulary (`clientId` in an OAuth config is the protocol's word)? **Finding when** an identifier, a route string, an internal event name or an i18n **key** uses the avoided term in live code. **Proof:** V402, plus the consumer side of every renamed key or event resolved in the same change.

### 4. Placement (AL-19)

```
BAD:   apps/web/src/__tests__/orders.test.tsx     rule: "Tests are co-located beside the file they test"
       features/refunds/ with no index.ts         rule: "Each feature under `features/<name>/` exposes an `index.ts`"
       `src/modules/billing/` named in ai/modules.md, absent on disk
GOOD:  apps/web/src/features/orders/orders.test.tsx · features/refunds/index.ts
```
**Read the code:** Is the module catalog written with paths relative to its section heading (`ai/modules.md` uses both forms)? `name-check.py` tries root-, heading- and tail-relative forms before printing `absent`; a heading roots its section when it is a path or carries one (`## apps/web (`apps/web/src/`)`), a cell with no trailing slash is still a module, and a file stem (`shared/errors` = `errors.ts`), a directory on disk outside the scanned roots, or a lint rule id that looks like a path is never `absent`. Is the directory generated or a framework routing directory (`app/`, `routes/`, `pages/`)? Is the missing module simply not built yet? Then it is `/roadmap`, not drift. Does the boundary tool (eslint-plugin-boundaries elements, depcruise) classify files by the same paths? A pattern that matches 0 files after a move makes every policy vacuous. **Finding when** the declared placement rule names the path and the tree breaks it. **Proof:** V404 — the repo's boundary tool green on every module, not only the moved one, with `matched N files` > 0 (V399); `git mv` keeps history.

## Proof

Oracles and variant lists: [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Align. **V402** (rename with serialised names unchanged) for §1–§3, **V404** (boundary whole-repo) for §4, **V399** (non-vacuous) for every rule a fix relies on, and **V391** (re-detect zero: the same `name-check.py` and lane commands return 0 at the ledger sites and 0 new sites in touched files) before a row closes.

## Output

```
naming-layout-scan — lanes: name-check.py (oracle T2 3 rules), eslint 10.13 check-file + unicorn 78 (dirs on); ls-lint, ruff absent
Gates: unicorn-dirs (v78 checks directories) · ts7-no-api (naming-convention typed selectors NOT RUN)

1. src/components/billing/invoicelist.tsx                             [report-with-fix]   low
   §1 AL-16 — stem `invoicelist` (flat) vs rule N1 ai/conventions.md:8 "Component files are PascalCase and match the
   exported component name exactly"; exports InvoiceList. 0 dynamic imports of the path. Proof: git mv → tsc + build green.
2. src/components/ui/Button.tsx:12 `loading: boolean`                  [report-flagged]    medium
   §2 AL-17 — rule naming-convention (eslint.config.mjs:31, prefix is/has/should) at error; typed lane NOT RUN (TS 7),
   found by grep 2c. Exported prop: 9 call sites. Settling probe: rename via the TS 6 alias, then tsc --noEmit.
3. apps/web/src/routes/clients.$id.tsx                                 [report-flagged]    low
   §3 AL-18 — `clients` vs ai/glossary.md:7 "customer | client, buyer"; the route is public (SEO links) → the URL is
   a contract (§ 15): internal identifiers only, route rename via /refactor + ADR.

Verification: 6 candidates → 1 finding · 2 unconfirmed · 1 hardening · 0 pre-existing · 2 refuted

Class coverage:
  §1  AL-16 files/dirs       checked (3 rules / 31 files → 1 finding; 4 exempt framework names)
  §2  AL-17 identifiers      blocked (TS7: typed selectors) · checked by grep 2c (4 lines → 1 unconfirmed)
  §3  AL-18 synonyms         checked (glossary 2 terms → 3a 5 lines, 3b 1 key → 1 unconfirmed)
  §4  AL-19 placement        N/A (no module catalog, no co-location or barrel rule declared)
```

`[report-with-fix]`: the rule is T1/T2 for this scope, no exemption applies, and the rename is proven by V402 or V404. `[report-flagged]`: a link is open (a typed lane not run, a T2g rule awaiting ratification, a name that may be a contract). The coverage block lists **all four** classes on every run: `checked (k → m)` only when the step ran on a declared rule; `N/A (<reason>)` only when no rule or glossary is declared for the class; `blocked (<reason>)` when a script, `rg` or tool failed; `Live, unreviewed` / `Live, ratcheted` for a partial review.

## False positives / precedents

The verifier reads [`precedents/align.md`](../../../../snippets/precedents/align.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10 (maintainability / conventions column: the oracle line quoted plus the site). The ones this skill meets most:

- **§ 13 Framework-mandated names** override every naming rule.
- **§ 15 Externally fixed names** are contract: a rename routes to `/refactor` with an ADR.
- **§ 11 Tests may import internals**, and **tests are in scope for naming and layout** unless § 11 or § 13 applies.
- **§ 16 Generated, vendored and frozen code** is out of scope.
- **§ 19 The formatter owns formatting**; a rename commit that also reformats is AL-34.
- **§ 1, § 28, § 29** a majority, a generated line and a contested category are not rules.
- **§ 20** a rule that matched 0 files, or a lane that did not run, is `NOT RUN`, never clean.

## When to run

- On any diff that adds or renames files or directories, adds exported identifiers, routes, events or i18n keys, or touches `.ls-lint.yml`, a naming rule, `ai/glossary.md` or `ai/modules.md`: the `align-detect` dispatch signal.
- On every whole-repo `/align-scan`, reporting all four classes.
- After a version bump of eslint-plugin-unicorn (≥ 65 checks directories) or eslint-plugin-boundaries (renamed rules): the counts move for reasons that are not new drift.

## Halt conditions

- Do not report a row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§ 10). Under `/align-scan` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any row without the site, the oracle row with its quote or rule id, and the expected and actual shape.
- Never rename by text replace, never rename a wire, DB, env or generated name under align, and never rename a framework-mandated file.
- Never report a name against a majority, a T2g line or a contested category as a Finding.
- Never print "names clean" without the coverage block. A lane whose tool is absent or whose typed rules need the TS 6 API is `blocked` / `NOT RUN`, never zero; a rule that matched 0 files is `NOT RUN (vacuous)`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `scripts/name-check.py` (this skill): the file, directory and identifier check (§1–§2), `--skeleton` (§4), `--census` (AL-02 input for `convention-oracle` §2), `--rule=<spec>` for a rule read by hand, `--self-test`. Stdlib only, `python3 -I` safe; it reads files and writes nothing into the root.
- `convention-oracle` builds the oracle map this skill reads and runs the AL-01 quote check over its rows. `convention-ratchet-scan` §1 owns suppressions of naming rules. `align-detect` dispatches this skill; `/align-scan` folds the coverage block into its class ledger; `find-and-align` closes rows with the `rename` verb and V402.
- `api-consistency-audit` (backend) owns API field and path casing; `i18n-scan` (frontend) owns key namespaces; `architectural-diagnosis` (code-quality) owns layer direction.
- [`precedents/align.md`](../../../../snippets/precedents/align.md) § 11, § 13, § 15–16, § 19–20; [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Align V391, V399, V402, V404.
