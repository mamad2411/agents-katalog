---
name: convention-oracle
description: Tiered oracle map for align; drops rows citing no oracle, reports splits, unenforced rules and stale docs (AL-01–04).
kind: skill
pack: align
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: convention-oracle

## Premise

Align enforces conventions the project **already declares**. Every align row therefore depends on one question asked before any site is read: *where is this convention declared, and how strongly?* A rule at `error` in the flat config that CI lints is law. The same sentence inside `<!-- refine-enriched -->` markers is a sampled majority a setup run wrote down. A category under `## Unsettled conventions` is a live split. A grep sees three identical sentences.

This skill answers that question once per run and owns the four classes that are about the convention itself, not about a site:

- **§ 0** builds the oracle map with `scripts/oracle-map.py`: every declared rule, tagged by tier and provenance, with its scope, CI coverage, version gates and inline exceptions. Every other align detector (`wrapper-adoption-scan`, `naming-layout-scan`, `convention-ratchet-scan`) and every dispatched owner row reads it.
- **§ 1 AL-01, invented convention.** A meta-check on every candidate row from every detector: a row whose `oracle:` does not resolve is dropped and counted.
- **§ 2 AL-02, split with no declared winner.** A report, never a ledger row.
- **§ 3 AL-03, declared but unenforced.** The doc says X; no rule at `error` that CI runs says it.
- **§ 4 AL-04, doc–code contradiction.** The written rule is stale and the current code consistently does the other thing. Advisory, routed to a doc update.

**Every row this skill emits cites the oracle `path:line` with its quote (or the rule id and config file), the tier, and the count that justifies the class.** A majority is never a Finding ([`precedents/align.md`](../../../../snippets/precedents/align.md) § 1). "Oracle clean" is never printed without the class-coverage block (§ Output).

## The rule

The tier decides what a declaration can produce ([`precedents/align.md`](../../../../snippets/precedents/align.md), the claim restated and the tier table):

| Tier (`oracle-map.py` tag) | Source | Produces |
|---|---|---|
| **T1 enforced** (`enforced`) | a rule at `error` in the static-parsed config for that scope, in a package CI lints (or no CI file exists: `ci=unknown`): ESLint flat config, stylelint, ls-lint, depcruise `forbidden`, eslint-plugin-boundaries, import-linter, Ruff `select` and `banned-api`, tsconfig flags, `.editorconfig` IDE1006, Spectral, golangci depguard | a Finding at a site (§ 2) |
| **T1-warn / T1-noci** (`written`) | the same rule at `warn`, or at `error` in a scope no CI job lints | an oracle, plus AL-03 against itself |
| **T2 written** (`written`) | `ai/conventions.md`, `ai/architecture.md`, `ai/modules.md` **outside** `refine-enriched` markers; accepted ADRs; CONTRIBUTING; design-system docs; `ai/glossary.md` | a Finding, plus AL-03 when no T1 rule backs it |
| **T2g generated** (`generated`) | lines inside `refine-enriched` markers; `[inferred:]`, `[unconfirmed]`, `[SAMPLED` facts; every line of `.claude/codebase-profile.md`, `_extracted-*.md`, `_refine-extract.md` | a proposal: **Unconfirmed** behind one ratification probe per rule (§ 28) |
| **contested** | `[CONTESTED: A n/N, B m/N]` rows; every row under `## Unsettled conventions`; a T2g row naming a contested category | AL-02 only, even when a doc elsewhere names a side (§ 29) |
| `off`, `inactive` | a rule at `off`; an ADR that is proposed, rejected, superseded or deprecated | no convention (an `off` row feeds AL-31 in `convention-ratchet-scan` §3) |

A row is kept by § 1 only when its oracle resolves: the quote is found in the cited file (whitespace-normalised), or the rule id is a `rules.tsv` row that is not `off`. Everything else is dropped and counted.

## Boundaries

- **Every site-level class** is another detector's: wrappers, imports and helpers (AL-11/13/14/15/22) → `wrapper-adoption-scan`; names and placement (AL-16–19) → `naming-layout-scan`; suppressions, ratchets, per-package drift and migration residue (AL-29–32) → `convention-ratchet-scan`. This skill hands them the oracle map and runs § 1 over their output.
- **Per-package config drift** (a package that does not extend the shared config, or turns a convention rule `off`) is AL-31 in `convention-ratchet-scan` §3. A rule whose **whole** scope CI never lints, or that sits at `warn`, is AL-03 here; a package left out while its siblings are linted (`ci=partial`) is AL-31 there.
- **Owner classes** (tokens AL-05–10/12 → ui-ux `design-token-audit`; layering AL-20/21 → code-quality `architectural-diagnosis`; API contract AL-23–25 → backend; i18n AL-26/27 and a11y AL-28 → frontend) still pass § 1: a dispatched owner row that cites a convention must cite one that resolves. The owner grades the row; this skill only checks the citation. Without the owner pack the class prints `N/A (owner pack <x> not installed)` in the align ledger.
- **Writing the winner of a split** into `ai/conventions.md` is a human ratification through `/setup-project --refine`, never this skill. **Introducing** a convention the project does not have is `/polish`.
- **Rule-versus-reality as learning's `/detect-drift` reports it** is the same question asked read-only; when the align pack is installed, it should dispatch this skill (integrator item IR-4 of the batch-6 eval).

## Adapt to the codebase — oracle sources and lanes

`oracle-map.py` reads configs statically and executes nothing from the repo. The resolved configuration is the truth when the project's own tool is installed, so each lane names its resolution command. Versions come from `versions.tsv` (lockfile > manifest range), never from memory.

| Lane | Declarations read (static) | Resolved truth (project-local binary only) | Version gate (`gates.tsv`) | Without the tool |
|---|---|---|---|---|
| **JS / TS** — React, Vue, Svelte, Angular, Node | `eslint.config.{js,mjs,cjs,ts}` `rules` / `files` / `ignores`, `no-restricted-imports` paths and patterns, boundaries elements; `.stylelintrc*` / `stylelint.config.*`; `.ls-lint.yml`; `.dependency-cruiser.*` `forbidden`; `tsconfig*.json`; `package.json` `exports` | `node_modules/.bin/eslint --print-config <file>` (one sample file per config scope); `stylelint --print-config <file>` | ESLint ≥ 10 reads flat config only (10.0.0, 2026-02-06), so an `.eslintrc*` beside a flat config is dead (AL-31); TS 7 with no `@typescript/typescript6` alias = typed rules `NOT RUN`; jsx-a11y / import / react plugins still peer ESLint ≤ 9 (name the `-x` forks); boundaries v6 `dependencies`, v7 `policies` | static parse stands; every `static!=resolved` gate row (spread, imported preset, computed value) stays open and caps § 3 at `Unconfirmed` |
| **Python** | `pyproject.toml` / `ruff.toml` `select`, `extend-ignore`, `per-file-ignores`, `flake8-tidy-imports.banned-api`; `.importlinter` contracts | `ruff check --show-settings <file>` (add `--no-cache`: Ruff writes a cache directory into the project otherwise) | Ruff 0.17 | static parse |
| **Go** | `.golangci.yml` depguard | `golangci-lint config` (GPL-3.0: run, never vendor) | v2 schema | static parse |
| **Java / Kotlin** | ArchUnit / Konsist tests, detekt and Checkstyle configs | the project's test or lint task | ArchUnit `FreezingArchRule` store present | read the rule source |
| **.NET** | `.editorconfig` naming, `BannedSymbols.txt` | the .NET build (`dotnet build`) with `EnforceCodeStyleInBuild` (only the IDE1006 diagnostic severity is enforced at build, never a per-naming-rule severity) | — | static parse |
| **Ruby / PHP** | `.rubocop.yml`, packwerk `package.yml`; `deptrac.yaml`, `phpstan.neon` | `rubocop --show-cops`; `vendor/bin/deptrac` | packwerk `strict` | static parse |
| **Docs (all stacks)** | `ai/*.md`, `ai/_convention-cheatsheet.md`, `ai/core/invariants.md`, ADRs (`docs/adr`, `doc/adr`, `ai/decisions`, …), CONTRIBUTING, DS docs, glossary; the MUST / never lines of `CLAUDE.md` and `ai/patterns/*.md`; provenance markers | — | ADR status and date (`adr=<status>@<date>`, `frozen-until=`) | — |
| **CI** | GitHub, GitLab, Azure, Circle, Bitbucket `run:` / `script:` steps and their block scalars; `npm run lint` resolved through `package.json` scripts; `turbo run x`, `pnpm -r x`, `nx run-many -t x`, `lerna run x` and `--filter <pkg>` expanded to each package's own script in its directory | — | — | no CI file → `ci=unknown`, and T1 needs no CI proof |
| **Structural specs** | `specs.tsv`: a test that reads the source tree and asserts a shape (`*-only-falls.spec.ts`, a layout spec, ArchUnit / Konsist); `ratchet` when it holds a count that may only fall | the project's test task | — | a spec CI never runs (`ci=no`) enforces nothing |

Offline by default: never `npx -y` (network plus a `$HOME` cache). Before any CLI: `DO_NOT_TRACK=1 CI=true`. A missing binary prints `blocked (<tool> not installed)`; `--online` installs only into `$RUN/tools`.

## Pre-flight

Run as **one** bash script from the repo root (shell state does not survive between tool calls), and run it with `bash`: `${PIPESTATUS[…]}` and the `X` / `T` arrays are bash-only, so under zsh (the macOS login shell an agent's tool may use) every `exit` line printed blank. The first line refuses any other shell. Step **N** feeds detector **§N**. Every `rg` names its path; any `rg` exit 2 is a failed search, never zero hits. Exclusions are root-relative globs (`**/…`): an exclusion matched against an absolute path silently drops every file under a directory such as `benchmarks/fixtures/` (§ 20). `name-check.py` (naming-layout-scan's script) takes its file list only through `--files=-` on a pipe or `--files=<list>`, and never reads stdin implicitly: under an agent shell an open stdin hung the earlier read-when-not-a-terminal rule (measured 2026-10-18: a `--census` call with no pipe ran until the 120 s timeout).

```bash
[ -n "${BASH_VERSION:-}" ] || { echo "pre-flight: run it with bash (save it, then bash <file>): PIPESTATUS and arrays are bash-only, and under zsh every exit prints blank"; exit 2; }
ROOTS=(.)   # code roots; in a monorepo name them: ROOTS=(apps/web apps/api packages). Config and docs are always read from .
CO="${CO:-.claude/skills/convention-oracle/scripts}"; NL="${NL:-.claude/skills/naming-layout-scan/scripts}"
RUN="${RUN:-$(mktemp -d "${TMPDIR:-/tmp}/align.XXXXXX")}"; mkdir -p "$RUN"; echo "RUN=$RUN"
export GIT_OPTIONAL_LOCKS=0 DO_NOT_TRACK=1 CI=true
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/third_party/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**'
   -g '!**/.venv/**' -g '!**/__generated__/**' -g '!**/*.gen.*' -g '!**/*.min.*' -g '!**/*.{lock,map,snap}')
T=(-g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,migrations,locales,i18n}/**'
   -g '!**/*.{spec,test,stories,story,test-data,fixture,fixtures,doc}.*' -g '!**/*.md' -g '!ai/**' -g '!docs/**')

# 0. The oracle map: every align detector reads $RUN/oracle (rules, docs, wrappers, exports, versions, gates, ci, exceptions, ages).
python3 -I "$CO/oracle-map.py" . --out="$RUN/oracle" --age-buckets; echo "oracle-map exit $? (0 ran, 2 usage)"
#    0b. CI lint steps, read with --hidden: rg skips dot-directories, so .github/ is invisible without it.
rg --hidden -n --pcre2 '\b(?:eslint|stylelint|ls-lint|lint-imports|depcruise|ruff|golangci-lint|spectral|biome|oxlint)\b|\b(?:npm|pnpm|yarn|bun)\s+(?:run\s+)?lint\b' -g '.github/workflows/*.{yml,yaml}' -g '.gitlab-ci.yml' -g '.circleci/*.yml' -g 'azure-pipelines.yml' -g 'bitbucket-pipelines.yml' -g '!.git/**' .; echo "rg 0b exit $? (1 = no CI lint step)"
#    0c. The resolved ESLint config, one sample file per rule scope, with the project's own binary (never npx).
if [ -x node_modules/.bin/eslint ]; then
  awk -F'\t' '$2=="eslint" && $9+0>0 {print $7}' "$RUN/oracle/rules.tsv" | sort -u | while read -r g; do
    f=$(rg --files -g "$g" "${X[@]}" . 2>/dev/null | head -1); [ -n "$f" ] || continue
    node_modules/.bin/eslint --print-config "$f" > "$RUN/resolved.$(printf '%s' "$f" | tr '/.' '__').json"; echo "print-config $f exit $?"
  done
else echo "0c: blocked (eslint not installed) — rules.tsv is the static parse; every static!=resolved gate stays open"; fi

# 1. AL-01: every candidate row from every align detector and dispatched owner, as TSV `id site oracle` in $RUN/candidates.tsv.
[ -s "$RUN/candidates.tsv" ] && { python3 -I "$CO/oracle-map.py" . quotes --candidates="$RUN/candidates.tsv" --oracle="$RUN/oracle" > "$RUN/quotes.tsv"; echo "quotes exit $? (1 = rows dropped, 2 usage)"; tail -1 "$RUN/quotes.tsv"; }

# 2. AL-02: contested rows first, then a census of shapes per concern, then the floor test (0 ledger rows either way).
awk -F'\t' '$2=="contested"' "$RUN/oracle/docs.tsv"
rg --files "${ROOTS[@]}" "${X[@]}" | python3 -I "$NL/name-check.py" . --census --files=- > "$RUN/census.tsv"; echo "census exit ${PIPESTATUS[1]}"
#    2b. One rg per code-shape concern; `-o -r '$1'` prints the shape. Example: props declared as interface vs type.
rg -n -o -r '$1' --pcre2 '^\s*(?:export\s+)?(interface|type)\s+\w*Props\b' -g '*.{ts,tsx,vue}' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | awk -F: '{print "props-declaration\t"$3"\t"$1":"$2}' >> "$RUN/census.tsv"; echo "rg 2b exit ${PIPESTATUS[0]}"
#    2c. Two call shapes for one job. Example: user-facing error feedback, a toast library's `.error()` vs the design system's
#        notify call with an error kind. The wrapper's own implementation prints too (it calls the library): drop it at the read.
rg -n --pcre2 '\b(?:toast|message|notification|snackbar)\.error\s*\(' -g '*.{ts,tsx,js,jsx,vue,svelte}' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | awk -F: '{print "error-feedback\tlibrary .error()\t"$1":"$2}' >> "$RUN/census.tsv"; echo "rg 2c exit ${PIPESTATUS[0]}"
rg -n --pcre2 '\b(?:notify|showToast|addToast|showNotification|enqueueSnackbar)\s*\(\s*\{[^}\n]*\b(?:kind|type|variant|severity)\s*:\s*["\x27]error["\x27]' -g '*.{ts,tsx,js,jsx,vue,svelte}' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | awk -F: '{print "error-feedback\tnotify({kind: error})\t"$1":"$2}' >> "$RUN/census.tsv"; echo "rg 2c' exit ${PIPESTATUS[0]}"
#    2c''. The project's OWN error helper, read from wrapper-adoption-scan's tables when they are filled: a toast library a
#        T2 row routes through a wrapper file -> the error-named functions that file exports (`notifyError`), plus such names
#        in helpers.tsv. Without them the census sees only the library's shape and "proposes" it (measured 2026-10-18).
WN=$(python3 -I - "$RUN/wa" <<'PY'
import os, re, sys
wa, names = sys.argv[1], set()
rows = lambda n: [l.rstrip('\n').split('\t') for l in open(os.path.join(wa, n), encoding='utf-8')] if os.path.exists(os.path.join(wa, n)) else []
for c in rows('wrappers-t2.tsv'):
    if len(c) > 1 and not c[0].startswith('#') and re.search(r'toast|sonner|notif|snack|message|alert', c[0], re.I) and os.path.isfile(c[1]):
        names |= set(re.findall(r'export\s+(?:async\s+)?(?:function\s*\*?\s*|const\s+|let\s+)(\w*(?:Error|Fail)\w*)', open(c[1], encoding='utf-8', errors='replace').read()))
for c in rows('helpers.tsv'):
    if c and not c[0].startswith('#') and re.search(r'(?:notif|toast|snack|alert)\w*(?:error|fail)', c[0], re.I): names.add(c[0])
print('|'.join(sorted(names)))
PY
)
if [ -n "$WN" ]; then rg -n --pcre2 '\b(?:'"$WN"')\s*\(' -g '*.{ts,tsx,js,jsx,vue,svelte}' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | rg -v --pcre2 '^[^:]+:\d+:\s*(?:export\b|//|/?\*)' | awk -F: -v w="$WN" '{print "error-feedback\tproject helper ("w")\t"$1":"$2}' >> "$RUN/census.tsv"; echo "rg 2c'' exit ${PIPESTATUS[0]} (wrapper: $WN)"
else echo "2c'': no project error helper read (fill \$RUN/wa/wrappers-t2.tsv or helpers.tsv first: wrapper-adoption-scan)"; fi
python3 -I "$CO/oracle-map.py" . propose --sites="$RUN/census.tsv" --oracle="$RUN/oracle" < /dev/null

# 3. AL-03: config rules declared but not enforced (warn, or a scope no CI job lints), then T2 doc rules to match against them.
awk -F'\t' '$6=="T1-warn" || $6=="T1-noci" {print $1"\t"$6"\t"$2"\t"$3"\t"$7"\tci="$10"\t"$12}' "$RUN/oracle/rules.tsv" > "$RUN/al03.tsv"; cat "$RUN/al03.tsv"
awk -F'\t' '$2=="written" && $3=="T2" {print $1"\t"$4"\t"$7"\t"substr($8,1,110)}' "$RUN/oracle/docs.tsv"
#    3b. V390 where the tool is installed: the rule at error over its declared scope, counted. Never --fix, never a cache.
while IFS=$'\t' read -r id tier tool rule scope ci src; do
  case "$tool" in
    eslint) [ -x node_modules/.bin/eslint ] || { echo "V390 $id: blocked (eslint not installed)"; continue; }
      node_modules/.bin/eslint -f json --rule "{\"$rule\": \"error\"}" "${ROOTS[@]}" > "$RUN/v390.$id.json"; echo "V390 $id eslint exit $? (2 = config error, not a count)"
      python3 -I -c 'import json,sys; print(sum(1 for f in json.load(open(sys.argv[1])) for m in f["messages"] if m.get("ruleId")==sys.argv[2]), "violations at error")' "$RUN/v390.$id.json" "$rule" ;;
    depcruise) [ -x node_modules/.bin/depcruise ] || { echo "V390 $id: blocked (depcruise not installed)"; continue; }
      cfg="${src%%:*}"; (cd "$(dirname "$cfg")" && "$OLDPWD/node_modules/.bin/depcruise" . --config "$(basename "$cfg")" --output-type json) > "$RUN/v390.$id.json"; echo "V390 $id depcruise exit $?" ;;
    ruff) RUFF=$(command -v .venv/bin/ruff || command -v ruff) || { echo "V390 $id: blocked (ruff not installed)"; continue; }
      "$RUFF" check --no-cache --select "$rule" --output-format concise "${scope%%/\*\*}"; echo "V390 $id ruff exit $? (1 = violations)" ;;
    *) echo "V390 $id: $tool — run it at error by hand from a scratch config under \$RUN that extends the project's" ;;
  esac
done < "$RUN/al03.tsv"

# 4. AL-04: per declared rule, the share of its scope that follows the other shape (name-check's ledger; other detectors' counts).
rg --files "${ROOTS[@]}" "${X[@]}" | python3 -I "$NL/name-check.py" . --files=- --oracle="$RUN/oracle" > "$RUN/names.tsv" 2> "$RUN/names.ledger"; echo "name-check exit ${PIPESTATUS[1]} (1 = candidates)"
#    the ratio is DISTINCT FILES over matched files (one file can carry two rows: its case and its export name)
sed -nE 's/^ *rule (N[0-9]+) \(([^,]+),.*matched ([0-9]+) files · [0-9]+ candidates in ([0-9]+) files.*/\1 \2 \3 \4/p' "$RUN/names.ledger" | awk '$3>0 {printf "%s %s %d/%d files = %.2f%s\n", $1, $2, $4, $3, $4/$3, ($4/$3>=0.8 ? "  AL-04 candidate: read the newest files" : "")}'
#    4b. A doc literal the code contradicts: each backticked literal with a number in a T2 doc row (`/api/v1`, `node 20`) is
#        generalised (each digit run -> \d+) and counted in code per concrete value. The doc's value in under 20% of >= 3 files,
#        with another value holding the rest, prints an AL-04 candidate. Read the code (a route prefix, a base URL) before a row.
#    Skipped as noise (measured 2026-10-18, 8 of 8 candidates on a real monorepo): a literal with an 8+ digit run (a migration
#    timestamp names ONE file), one the sentence contrasts ("against a `varchar(26)`", "not", "instead of"), a row of a
#    ratchet table (it lists what the code is moving AWAY from), a hex colour (design-token-audit's), and ai/patterns/ or
#    CLAUDE.md lines (worked examples such as `/v2/orders`, not the project's values).
awk -F'\t' '$2=="written" && $3=="T2" {print $7"\t"$5"\t"$8}' "$RUN/oracle/docs.tsv" > "$RUN/doc-literals.tsv"
python3 -I - "$RUN/doc-literals.tsv" "${X[@]}" "${T[@]}" -- "${ROOTS[@]}" <<'PY'
import re, subprocess, sys
rest = sys.argv[2:]; i = rest.index('--'); globs, roots = rest[:i], rest[i + 1:]; seen, n, skip = set(), 0, 0
CONTRA = re.compile(r'(?i)\b(?:against|instead of|rather than|not|never|no longer|vs\.?|versus|was|were|replaced?|replaces|old|legacy|formerly|deprecated)\b[^.;`]{0,24}$')
for l in open(sys.argv[1], encoding='utf-8'):
    where, sec, quote = (l.rstrip('\n').split('\t', 2) + ['', ''])[:3]
    if re.search(r'(?i)ratchet', sec) or re.match(r'(?:ai/patterns/|CLAUDE\.md)', where): continue   # pattern docs show examples
    for mm in re.finditer(r'`([^`\s]{2,40})`', quote):
        lit = mm.group(1)
        if not re.search(r'\d', lit) or re.fullmatch(r'[\d.:/-]+', lit) or lit in seen: continue   # a bare number or date is no literal
        if re.search(r'\d{8,}', lit) or re.fullmatch(r'#[0-9a-fA-F]{3,8}', lit) or CONTRA.search(quote[max(0, mm.start() - 40):mm.start()]): skip += 1; continue
        seen.add(lit); n += 1
        rx = ''.join(r'\d+' if s.isdigit() else re.escape(s) for s in re.split(r'(\d+)', lit))
        rx = ('(?<![\w])' if re.match(r'\w', lit) else '') + rx + '(?!\d)'
        p = subprocess.run(['rg', '-o', '-n', '--no-heading', '--pcre2', rx] + globs + roots, capture_output=True, text=True)
        if p.returncode == 2: print('4b %s `%s`: blocked (rg exit 2)' % (where, lit)); continue
        vals = {}
        for h in p.stdout.splitlines(): vals.setdefault(h.split(':', 2)[2], set()).add(h.split(':', 1)[0])
        tot = sum(len(v) for v in vals.values()); mine = len(vals.get(lit, ()))
        if tot >= 3 and mine < 0.2 * tot and len(vals) > (lit in vals):
            print('AL-04 candidate\t%s `%s`\tcode: %s' % (where, lit, ' · '.join('%s in %d files' % (k, len(v)) for k, v in sorted(vals.items(), key=lambda kv: -len(kv[1])))))
print('4b: %d doc literals compared with the code (%d skipped: timestamps, contrasted, ratchet tables)' % (n, skip))
PY
```

`--rule '{"<id>": "error"}'` is merged with the project's configuration files (ESLint CLI reference, `--rule`, read 2026-10-18), so the rule keeps the scope its config gives it. When `rules.tsv` shows options for it, pass them in the same JSON: `{"<id>": ["error", <options>]}`. A file can carry two candidate rows (its case and its export name), so the `name-check.py` ledger prints both counts per rule, `k candidates in f files`, and the § 4 ratio above divides the **distinct files** `f` by the files the rule matched. It is still a triage cut-off: read the newest files before a row is written.

**Measured** (2026-10-18), whole script per fixture root, no tool installed in any of them (so 0c and every 3b lane printed `blocked`):

- `web-dashboard`: oracle `T1 0 · T2 14 · T2g 4 (unratified) · contested 0`, no CI file (`ci=unknown`); 0b exit 1. § 1 on a 4-row probe file: 1 kept (`ai/conventions.md:26`), 1 Unconfirmed (a quote from `.claude/codebase-profile.md:9`, T2g), 2 dropped (a paraphrased quote, an undeclared rule id) → `AL-01: 2 candidate rows dropped (of 4)`. § 2: 4 concerns from the census plus 1 `interface` from 2b, all `undetermined — ask` (the largest is 7 sites, under the 30-site floor). § 3: 0 config rules; all 14 T2 lines lack a T1 rule. By our reading, 12 are expressible by a tool the stack can run (3 naming → check-file or ls-lint, 2 layering → `no-restricted-imports`, 2 tokens → stylelint strict-value, 3 a11y and 1 i18n → lint rules, 1 permission gate → an ast-grep rule), and 2 are semantic (the catch rule and the hook triple) and stay agent-checked. § 4: rule N1 2 rows / 8 files (one file, `orderstable.tsx`, the WEB-NAME-01 seed), N2 0/3, N3 0/2: no AL-04.
- `quality-mix`: oracle `T1 7 · T1-warn 1 · T1-noci 2 · T2 9`, three CI lint steps, four `static!=resolved` gates (presets and a spread not expanded). § 3: the two depcruise `forbidden` rules for `api/src/domain` are `T1-noci` and `no-circular` is `T1-warn`. That is the answer key's statement that `api/.dependency-cruiser.cjs` declares rules no CI job runs. § 2: 6 concerns, all `undetermined — ask`; `file-case:other/*.ts` is a 3/3 kebab-vs-camel split, under the floor. § 4: no naming rule declared.
- `a11y-states`: oracle `T1 2` (tsconfig `strict` only), no docs, no CI; § 2 `file-case:components/*.tsx` 48/48 pascal → `proposed canonical: pascal … — ratify?` with 0 ledger rows; § 3 and § 4 have nothing to read.
- `frontend-correctness`: oracle `T1 2 · T2g 1`; § 2 `components/*.tsx` 41/41 → `proposed canonical: pascal`; the rest under the floor.
- `convention-drift` (staged copy, 188 files, one commit; no tool installed, so 0c and every 3b lane printed `blocked` or `run it at error by hand`): oracle `T1 15 · T1-warn 1 · T1-noci 19 · T2 53 · T2g 1 (unratified) · contested 2 · off 3`, 56 doc rows, 0 vacuous. § 1 on a candidate file seeded with invented quotes: `AL-01: 2 candidate rows dropped (of 6)`. § 2: 16 concerns, 0 ledger rows — `hook-file-case` 14 camel / 3 kebab `contested — ask` (CD-AL02-b), `props-declaration` 36 / 42 `proposed canonical: type … — ratify?` (CD-AL02-c), 14 `undetermined`. § 3: 20 AL-03 rows, 19 `T1-noci` and 1 `T1-warn` (the stylelint strict-value rule, CD-AL03-a; the row cites the rule key at `stylelint.config.mjs:6`, the severity sits at `:10`), plus 0b's `ci.yml:19`, the one lint step, over `apps/web` only (CD-AL03-b). § 4: rule N1 6/6 = 1.00 → AL-04 candidate (CD-AL04-a). **7 of 7 seeds** (re-run 2026-10-18 after adding 2c and 4b): 2c's `error-feedback: n=12 · library .error() 7 · notify({kind: error}) 5 → undetermined — ask` (CD-AL02-a; the 7th `.error()` is the design system's own `notify.ts:7`, which the read drops: the fixture's split is 6 / 5), and 4b's AL-04 candidate for `ai/conventions.md:86` (the doc's `/api/v1` in 0 files, `/api/v2` in 9; CD-AL04-b; 5 doc literals compared, 1 candidate). Before them both seeds were agent reads. No decoy printed.

- A real NestJS + React monorepo (pnpm + turbo, ESLint 10 flat config with a local plugin, no `node_modules`; read-only, re-measured 2026-10-18 after the fold-back fixes; before → after):
  - § 0: `oracle-map.py` crashed on a `message:` that names a const (`TypeError`, exit 1, no map) → the map builds; a const the file defines resolves (`group: FEATURE_IMPORTS`, the ADR message strings) and one it imports prints `<NAME>` with a `static!=resolved` row. Tiers `T1 4 · T1-noci 31` (with a patched copy) → `T1 29 · T1-noci 0`: CI's `pnpm run lint` is `turbo run lint`, now expanded to each package's `eslint "src/**/*.ts" "test/**/*.ts"` (25 CI steps read), and the 6 rows read from the local plugin's rule map are gone. T2 664 → 2,029 rows (CLAUDE.md 23, the cheatsheet 33, invariants 73, `ai/patterns/` 1,237 normative lines); `specs.tsv` 361 structural specs (23 ratchets), all run by CI. History `dated` → `history-blind (13255 of 13617 files first-added on one day: an import or squash)`, so § 2 is whole-tree only.
  - § 1: the three `eslint:no-restricted-imports` candidates resolved to the first block with that id (`shared/**`, T1-noci) → the block whose scope holds each site (the pages wall, the domain wall, the features wall), T1.
  - § 2: `error-feedback: n=240 · library .error() 240 → proposed canonical` → `n=746 · project helper (notifyError) 506 · library .error() 240 → undetermined — ask` (2c'' reads the wrapper file `wrappers-t2.tsv` names).
  - § 4b: 8 AL-04 candidates, all noise (6 migration timestamps, a `varchar(26)` the sentence contrasts, a ratchet-table example) → 0 (43 literals compared, 7 skipped; `ai/patterns/` examples are not compared). Inline exceptions 187 → 486: 5 config-comment lines that only NAME a directive are gone (2 were the only "reasonless" rows), 304 rows from CI-linted test trees are in, and all 68 `-- see above` reasons resolve to the comment above or the last reason given (before, 42 of 47 sat in P-26 "clusters" of the bare words `see above`).
- `convention-drift` re-run 2026-10-18 after the same fixes: tier line, AL-01, § 2, § 3 and § 4 output identical; 2c'' prints `no project error helper read` (no wa tables), 4b compares the same 5 literals (0 skipped). **7 of 7 seeds** still print.

Every root printed `history-blind` (one commit, or one add date for every file), so § 2 used whole-tree counts and no AL-04 row could be dated. The prototype lesson the eval recorded still holds: exclusions written against `/fixtures/` returned 0 on every fixture, because the fixture roots sit under `benchmarks/fixtures/` (§ 20).

## The 3,000-hit path

A large repo yields hundreds of doc lines and thousands of candidate rows. Triage in this order and record every step in the coverage block:

1. **Intersect with the oracle.** Only T1 and T2 rows can make Findings. All T2g rows collapse to **one** ratification line per rule (`confirm ai/conventions.md:41`), never N rows.
2. **Group.** Candidate rows group by (oracle row, normalised before-shape). One quote check (§ 1) settles a whole group, and the group key is the one `align-sweep-gate.py consistency` checks later.
3. **Rank** newest files first (new code is copied next), then by churn, then by user-visible surface.
4. **Read** the top 30 groups fully: the oracle line, two compliant sites, two violating ones.
5. **Ratchet the rest.** Where the owning rule can run at `error`, turn it on with a bulk-suppression baseline and report `Live, ratcheted (k groups / n hits — eslint-suppressions.json)`; otherwise `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

| § | Class | Severity | Proof |
|---|---|---|---|
| 0 | Oracle map (context for every align detector) | — | `oracle-map.py --self-test` |
| 1 | AL-01 invented convention | n/a: the row is dropped and counted | V389 |
| 2 | AL-02 split, no declared winner | advisory: 0 ledger rows | none (a report) |
| 3 | AL-03 declared but unenforced | Low; Medium when the declaration is an ADR | V390 |
| 4 | AL-04 doc–code contradiction | advisory → doc update | none (a report) |

Convention classes are never Critical, and none of these four is ever High.

### 0. The oracle map

Run once per run; every align detector reads `$RUN/oracle`. **Read the code:** Does the summary line's tier count match what the docs say they declare? Is any `gates.tsv` row `static!=resolved` (a preset, a spread, a const imported from another file, a `parser error`)? Then the rule set is incomplete until `--print-config` (0c) resolves it. Which `ci` value does each T1 row carry (`yes`, `partial`, `no`, `unknown`)? Is any rule `vacuous` (matched 0 files, § 20)? Then it proves nothing about its scope. Was the history dated, or `history-blind (<reason>)`? A history where ≥ 90% of the files share one first-add date is an import or a squash, and is blind: "the newest 20 files" would be one day's import. **Halt** the run, not the class, when `oracle-map exit` is 2: the map was not built (an internal error prints its traceback; it never exits 1, which `quotes` reserves for dropped rows).

### 1. Invented convention (AL-01)

```
BAD:   site: src/hooks/useOrders.ts:3   oracle: "hooks should return objects"          (cited from nowhere)
       site: src/x.ts:1                 oracle: eslint:no-restricted-imports           (rule not in any config)
GOOD:  site: src/hooks/useOrders.ts:12  oracle: ai/conventions.md:26 "Every data hook exposes the full triple `{ data, loading, error }`"
```
**Read the code:** Is the quote **copied**, or paraphrased? A paraphrase does not resolve. Is the cited line inside `refine-enriched` markers or in `.claude/codebase-profile.md`? Then `quotes` returns `unconfirmed (generated — ratify <source>)`: keep the row as Unconfirmed behind the ratification probe (§ 28). Is the rule id at `warn`, or from another package's config? Then it is not enforced for this site (§ 2). Does the row's rule exist only in the reviewer's sense of style? Then nothing resolves it. **Finding when:** never: this is a filter. **Drop when** `quotes` prints `dropped`; count every drop on the `AL-01: k candidate rows dropped` line. **Proof:** V389 (the quote is found by `rg -n -F -- "<quote>" <file>`, or the rule id is at `error` in the resolved config of the site).

### 2. Split with no declared winner (AL-02)

```
BAD:   "Most hooks return tuples, so useOrders must return a tuple"        (95% majority, no oracle line: § 1)
       hook files: 6 kebab vs 5 camel, `## Unsettled conventions` lists the category, the generated block names camelCase
GOOD:  file-case:components/*.tsx: n=48 · pascal 48
         proposed canonical: pascal (k/n = 48/48 = 1.00, …) — ratify?         ledger_rows: 0
```
**Read the code:** Is the split a **context** split, not drift: server vs client components, tests vs production, a frozen package (§ 16, § 17)? Is the category contested anywhere (`docs.tsv` tag `contested`)? Then the verdict is `contested — ask (<source>)` whatever a T2g line says (§ 29). Is the history dated? Without it, the newest-files test is not computed and the line says `whole-tree only`. **Report** every concern: `proposed canonical` only at ≥ 30 sites **and** ≥ 0.75 share, sampled from the newest files when history allows; otherwise `undetermined — ask`. Both print `ledger_rows: 0` (§ 1). **Route:** a human ratifies the winner through `/setup-project --refine`, after which the sites become site-class Findings on the next run.

### 3. Declared but unenforced (AL-03)

```
BAD:   ai/conventions.md:31 "Never hardcode a hex colour …"      no stylelint rule at all
       api/.dependency-cruiser.cjs:5 forbidden: domain-is-framework-free   error, but no CI job runs depcruise
       stylelint.config.mjs: "scale-unlimited/declaration-strict-value" at warn while the doc says "never"
GOOD:  the rule at error over the declared scope, the CI job lints that scope, and 3b counts 0 (or a shrink-only baseline holds the rest)
```
**Read the code:** Can a tool the stack already runs express this rule (naming → check-file, ls-lint, unicorn `filename-case`; imports → `no-restricted-imports`, depcruise, Ruff `TID251`; tokens → stylelint `declaration-strict-value`; i18n → `i18next/no-literal-string`)? A semantic rule no tool can express is marked `agent-checked`, not unenforced. Does CI lint that package (`ci` column, cross-checked by 0b with `--hidden`)? Does a structural spec CI runs assert the rule (`specs.tsv`: its title or file name names it, e.g. `cross-module-imports-only-fall.spec.ts` for a layer-import rule)? Then the rule is enforced, not AL-03. Is the rule at `warn` with no zero-warning gate? A `warn` rule cannot take an ESLint bulk-suppression baseline, which covers `error` rules only (ESLint suppressions docs), so promoting it to `error` comes first. **Finding when** a T2 rule (or a T1-warn / T1-noci rule) has no T1 rule enforcing it over its scope; record the 3b count when the tool ran, else `blocked (<tool> not installed)` with the count left Unconfirmed. **Severity:** Low; Medium when the declaration is an ADR. **Proof:** V390. **Fix route:** ratchet enablement (the rule at `error` plus a baseline generated after the fixes, V395), or `ai/conventions.md` marks the rule `agent-checked`.

### 4. Doc–code contradiction (AL-04)

```
BAD:   ai/conventions.md "store files end in `.store.ts`"   — 9 of 9 store files end in `-store.ts`, newest 5 included
GOOD:  the doc and the newest files agree, or the newest files move toward the doc (a migration in progress: AL-32)
```
**Read the code:** Does the other shape hold at ≥ 80% of the rule's sites **and** in ≥ 90% of the files added in the last 6 months (`ages.tsv`)? Both are triage cut-offs, not standards (§ 18). Do the newest files follow the **doc**? Then code is migrating toward it: `convention-ratchet-scan` §4 (AL-32), not a stale doc. Is the rule contested? Then it is AL-02. **Report** `doc stale: <path:line>` with the counts and the newest 5 files; a human decides whether the doc or the code moves, and the code is not rewritten. Without history: `AL-04 candidate (history-blind)`. **Route:** a doc update by a human (`/setup-project --refine` for generated docs).

## Proof

Oracles and variant lists: [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Align. **V389** (oracle quote resolves) for every kept row from every detector. **V390** (rule at error count) for § 3, from a scratch config or the CLI `--rule` merge, never by editing the project's config. AL-02 and AL-04 have no V of their own: they produce `proposed canonical`, `undetermined`, `contested` or `doc stale` lines and 0 ledger rows. A T2g rule is a precondition the coverage block prints, one ratification probe per rule (`precedents/align.md` § 28).

## Output

```
convention-oracle — lanes: eslint 10.13 (flat; print-config ran on 4 scopes), ruff 0.17, depcruise 18.6; ls-lint, stylelint absent
Oracle: T1 41 · T1-warn 3 · T1-noci 2 · T2 12 · T2g 9 (unratified) · contested 2 · history dated (412 files)

AL-01: 7 candidate rows dropped (of 63)   (5 paraphrased quotes, 2 rule ids at warn cited as enforced)
Ratify first (T2g, 9 rules → 37 Unconfirmed site rows): confirm ai/conventions.md:41, :44, :52 …

1. ai/conventions.md:31 "Never hardcode a hex colour …"                    [report-with-fix]   low
   §3 AL-03 — no stylelint rule; tier T2. V390: declaration-strict-value at error over apps/web/src → 14 violations.
   Fix route: enable at error, with a shrink-only counter for any site left open (V395).
2. api/.dependency-cruiser.cjs:5 forbidden:domain-is-framework-free         [report-flagged]    medium
   §3 AL-03 — error, but .github/workflows/ci.yml runs no depcruise (ADR 0002 declares it). V390 blocked (depcruise
   not installed). Settling probe: node_modules/.bin/depcruise src --config .dependency-cruiser.cjs --output-type json.
3. hook file naming                                                        [report-flagged]    advisory
   §2 AL-02 — contested (.claude/_extracted-codebase.md:88 [CONTESTED: kebab 6/11, camel 5/11]); ledger_rows: 0.
4. ai/conventions.md:19 "store files end in `.store.ts`"                   [report-flagged]    advisory
   §4 AL-04 — 9/9 use `-store.ts`, newest 5/5 too → doc stale; route a doc update.

Verification: 11 candidates → 2 findings · 3 unconfirmed · 2 hardening · 0 pre-existing · 4 refuted

Class coverage:
  §0  oracle map             built (static; 4 static!=resolved resolved by print-config)
  §1  AL-01 invented         checked (63 rows → 7 dropped)
  §2  AL-02 split            checked (14 concerns → 1 proposed canonical, 11 undetermined, 2 contested; 0 rows)
  §3  AL-03 unenforced       checked (12 T2 + 5 T1-warn/noci → 2 findings, 1 unconfirmed; 3 agent-checked)
  §4  AL-04 stale doc        checked (6 rules → 1 doc stale)
```

`[report-with-fix]`: the oracle line, the tier and the V390 count are all in hand, and the closure is a ratchet enablement. `[report-flagged]`: a link is open (the tool is not installed, the history is blind, a human must ratify or choose). The coverage block lists **all five** rows on every run: `checked (k → m)` only when the step ran; `N/A (<reason>)` only when the repo has no such surface (no docs, no config); `blocked (<reason>)` when a script or tool failed; `Live, unreviewed (k groups / n hits)` or `Live, ratcheted (…)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/align.md`](../../../../snippets/precedents/align.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10, the maintainability / conventions column, whose gate 6 is the oracle line quoted plus the site. The ones this skill meets most:

- **§ 1 Majority is not an oracle**, even at 95%; the floor only picks `proposed canonical` over `undetermined`.
- **§ 2 The config is an oracle even without prose;** a rule at `warn` or in an unlinted package is AL-03, not a site Finding.
- **§ 18 A stale doc loses to a consistent, current codebase** (AL-04), and the code is not rewritten.
- **§ 20 A clean scan with a skipped step is not clean:** a vacuous rule, an rg exit 2, an absolute-path exclusion.
- **§ 28 A generated line is a proposal until a human ratifies it.**
- **§ 29 A contested category is AL-02** even when a doc elsewhere names a side.
- **§ 16, § 17** frozen packages and context splits are not splits.
- **§ 33** CI that lints through turbo / `pnpm -r` / nx still lints; **§ 34** a squashed history is blind; **§ 35** a structural spec CI runs is enforcement; **§ 36** `-- see above` is a reason.

## When to run

- First in every whole-repo `/align-scan` and every `/align` run: § 0 feeds every other align detector, and § 1 runs over their output before verification.
- On any diff that touches `ai/conventions.md`, `ai/architecture.md`, `ai/modules.md`, `ai/glossary.md`, an ADR, a lint, stylelint, ls-lint, depcruise or Ruff config, or a CI workflow.
- After `/setup-project --refine` writes a `refine-enriched` block: the T2g count and the ratification list change.
- When a user asks "half the files do X and half do Y": § 2 answers with counts and a proposal, never a winner.

## Halt conditions

- Do not report a row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§ 10, maintainability / conventions column). Under `/align-scan` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any row without its oracle `path:line` and quote (or rule id and config file), its tier, and its count.
- Never write a ledger row from § 2 or § 4, and never pick a winner by majority, at any share.
- Never enforce a T2g line as written: one ratification probe per rule, every site Unconfirmed.
- Never edit the project's config, docs or CI to make § 3 pass; V390 runs from a scratch config under `$RUN` or the CLI `--rule` merge.
- Never print "oracle clean" without the coverage block. A step whose script exited 2, whose `rg` exited 2, or whose tool is absent is `blocked`, never `checked`; a rule that matched 0 files is `NOT RUN (vacuous)`, never zero.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `scripts/oracle-map.py` (this skill): `build` (§ 0), `quotes` (§ 1), `propose` (§ 2), `--self-test`. Stdlib only, `python3 -I` safe; writes only under `--out`, which must sit outside the scanned root.
- `naming-layout-scan` (its `name-check.py --census`) feeds § 2 and § 4. `wrapper-adoption-scan`, `naming-layout-scan` and `convention-ratchet-scan` read `$RUN/oracle`. `align-detect` dispatches all four, `/align-scan` folds their coverage blocks into the AL-01…AL-34 ledger, and `find-and-align` re-checks the oracle quote (L0) before any fix.
- `align-sweep-gate.py` (under `find-and-align`) owns AL-33/AL-34 on the sweep, not the tree.
- [`precedents/align.md`](../../../../snippets/precedents/align.md) § 1–3, § 18, § 20, § 28–29; [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Align V389–V390.
