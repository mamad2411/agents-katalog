---
name: doc-structure-scan
description: "Human docs vs docs: links, anchors, the docs gate, ADR graph, changelog grammar, translations, placeholders, nav."
kind: skill
pack: documentation
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: doc-structure-scan

## Premise

A doc set rots as a structure before any single page lies: a heading is renamed and twelve deep links from other pages, an alert's `runbook_url` and an error message now land on nothing; ADR 0003 says "Superseded by 0006" and 0006 never says it supersedes anything; the changelog lists 1.2.0 below 1.1.0; the Arabic setup page still tells readers to run a command the English page renamed; the nav points at a page that moved. And the docs CI is green throughout, because Docusaurus defaults `onBrokenAnchors` to `warn`, MkDocs leaves missing anchors at `info`, and `remark` without `--frail` exits 0 on warnings. Roughly 10% of links in code comments are dead (Hata et al., ICSE 2019).

This skill owns the **docs-against-docs** classes DL-1–DL-4, DK-3, DX-1–DX-3, DH-2, DI-1–DI-3, DF-1 and DF-2 (§1–§14). Docs against code and config is `doc-drift-scan`; samples and spec examples are `doc-sample-scan`.

**Every finding cites the doc line and the target it fails to reach (the file, the slug list of the target page, the reciprocal ADR, the source page of a translation, the gate config line), and the oracle that proves it.** An engine row is a candidate, never a finding. "Docs structure holds" is never printed without the class-coverage block (§ Output).

## The rule

A candidate becomes a finding only when all four hold:

1. **The doc is in scope.** A human doc, not a dated record (an ADR or changelog keeps only its doc-to-doc links, [precedents § 1](../../../../snippets/precedents/documentation.md)), tool config (§ 2), test data (§ 27), versioned docs (§ 12) or agent-facing knowledge (§ 28).
2. **The renderer was read.** Anchors are resolved with the slugger of the renderer that serves the page (GitHub, MkDocs `toc`, Docusaurus, Sphinx), detected from its config (§ 10); a gate is judged by the version and the options the repo pins.
3. **The target fails**: no file, no heading slug, no reciprocal line, a grammar rule broken, a translation that carries different code or links, a nav entry to nothing, a gate whose config cannot fail.
4. **No record makes it intentional**: an outdated banner under a declared lag policy (§ 11), a partial supersession (§ 30), a generated changelog's own grammar (§ 17).

## Boundaries

- An alert with no `runbook_url` → observability `alert-rule-lint`, when the observability pack is installed; §5 here takes a `runbook_url` that resolves to no file or anchor. Without that pack, the missing-URL half is out of scope and the coverage block says so.
- Accepted ADRs against the code → align `convention-oracle` AL-03/04 (when installed); this skill grades only ADR **metadata** (status, supersession, index, number) and never reads an ADR body as a claim. ADR coverage of decisions nobody recorded → `/setup-project-health` § 2 for Refract setups, else Hardening.
- The changelog version against the released version → devops `release-integrity-scan` RL-2 (when installed); breaking changes missing from the notes → `doc-drift-scan` §12.
- UI string catalogs → frontend `i18n-scan` (when installed); §10–§12 here are **doc pages**. TODO / FIXME debt in code → code-quality `debt-ledger`; §13 here is prose in published docs.
- Agent-facing knowledge (`ai/**` except runbooks and decisions, `CLAUDE.md`, `AGENTS.md`) → the learning pack's `knowledge-ref-scan`: the engine routes it, and a broken link inside it is learning's.
- Markdown style (MD040, heading increments, line length) is NIT unless the project configures and enforces the linter (§ 22).

## Lanes

The engine (`doc-drift-scan/scripts/doc-claims.py`, lanes `links`, `linksin`, `adr`, `changelog`, `i18n`, `placeholders`, `nav`, `gates`) always runs, offline. Tool lanes run only when the binary is installed in the repo (never `npx -y`), in a scratch copy where they write caches, with `CI=true DO_NOT_TRACK=1`; each prints `ran / NOT-RUN (<why>) / BLOCKED (exit n)` through its own exit map ([precedents § 32](../../../../snippets/precedents/documentation.md)).

| Renderer | Anchors (§2) | Nav (§14) | Gate that can fail (§4) | Locales (§10–§12) |
|---|---|---|---|---|
| **GitHub / plain repo** | github-slugger: lowercase, punctuation dropped, Unicode kept, `-1` duplicates; `<a name>`, `id=` | — | a lychee or remark CI step | `docs/<lc>/`, `README.<lc>.md` |
| **MkDocs** 1.6 | `toc` slugify: ASCII unless `pymdownx.slugs`, `_1` duplicates; `attr_list` `{#id}` | `nav`, `not_in_nav` | `strict: true` or `mkdocs build --strict`, and `validation.links.anchors: warn` (default `info`) | mkdocs-static-i18n (`fallback_to_default: true` hides gaps) |
| **Docusaurus** 3.10 | github-slugger, `{#id}` | `sidebars.*` doc ids | `onBrokenLinks: throw` (default), `onBrokenAnchors` and `onBrokenMarkdownLinks` (default `warn`) → `throw` | `i18n.locales`, `i18n/<lc>/docusaurus-plugin-content-docs/current/` |
| **Sphinx** 9.1 | labels; MyST heading anchors → CHECK | toctree | `sphinx-build -W --keep-going`, `-n` when nitpicky is policy | `locale_dirs`, sphinx-intl (`stat` exit is not a gate) |
| **mdBook** 0.5 | mdBook ids (lowercase, `-1`) | `SUMMARY.md` | `[output.linkcheck] warning-policy = "error"` (default `warn`) | — |
| **VitePress / Hugo** | GitHub-like [K?] | sidebar config [K?] | the build's dead-link option [K?] | `locales` / `languages` |

| Tool | Command (offline) | Exit map | Trap |
|---|---|---|---|
| lychee 0.24 | `lychee --offline --include-fragments --no-progress --format json './**/*.md'` | 0 ok · **2 broken links** · 1 runtime / config error · 3 config file | reversed against every linter; fragments only on GET; JS anchors invisible |
| markdownlint-cli2 0.23 | `node_modules/.bin/markdownlint-cli2 "**/*.md" "#node_modules"`, only when the repo has a config | 0 · 1 errors · 2 the tool failed | MD051 is same-file only; no MD057 |
| rumdl 0.3 | `rumdl check .` (pinned, pre-1.0) | 0 · 1 violations · 2 tool error | `rumdl fmt` exits 0 with violations left |
| remark-validate-links 13 | `node_modules/.bin/remark --use remark-validate-links --frail --quiet .` | `--frail`: warnings exit 1 | without `--frail` every warning exits 0 |
| python-kacl 0.7 | `kacl-cli verify --json` | **exit = error count** | the PyPI package `kacl` is another project |
| site builds | `mkdocs build --strict` · `sphinx-build -W --keep-going -b dummy` · `docusaurus build`, in a scratch copy with the pinned toolchain | non-zero on failure | builds need the install; never in the audited tree |

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). `NETWORK=1` opts into the external-link lane (§3). Every grep ends in `ck`: exit 2 is a blocked class, never zero hits. `doc-claims exit 1` is candidates, not a failure; exit 2 is BLOCKED.

```bash
DC="${DC:-.claude/skills/doc-drift-scan/scripts/doc-claims.py}"; NETWORK="${NETWORK:-}"
OUT="$(mktemp -d "${TMPDIR:-/tmp}/doc-structure.XXXXXX")"; export GIT_OPTIONAL_LOCKS=0 CI=true DO_NOT_TRACK=1; : > "$OUT/stamp"
ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
python3 -I "$DC" . --lanes=links,linksin,adr,changelog,i18n,placeholders,nav,gates --out="$OUT/run" > "$OUT/claims.tsv" 2> "$OUT/ledger.txt"
echo "doc-claims exit $? — 0 clean · 1 candidates (not a failure) · 2 BLOCKED: read the ledger's last line"; cat "$OUT/ledger.txt"
cut -f2,3 "$OUT/claims.tsv" | sort | uniq -c | sort -rn
X=(-g '!**/node_modules/**' -g '!**/{dist,build,vendor,.venv,target,site,_build}/**' -g '!ai/**' -g '!.claude/**' -g '!**/{test,tests,fixtures,testdata}/**')
# S1. Every docs gate and its silencing option (§4), in CI, scripts and site configs only: the lines read before believing a green docs job.
#     --hidden: CI lives under .github/ and rg skips dot-directories without it (0 hits that read as "no gate").
G=(-g '.github/workflows/*.{yml,yaml}' -g '.gitlab-ci.yml' -g '.circleci/*.yml' -g '**/package.json' -g 'docusaurus.config.*' -g 'mkdocs.{yml,yaml}' -g 'book.toml' -g '**/conf.py' -g '**/Makefile' -g 'justfile' -g '.pre-commit-config.yaml' -g 'typedoc.json' -g 'lefthook.yml')
rg -n --hidden --pcre2 'onBroken(?:Links|Anchors|MarkdownLinks)\s*:|^strict\s*:|^\s+anchors\s*:\s*\w+|warning-policy|lychee|markdown-link-check|markdownlint|rumdl|\bremark\s+[-.\x27"]|remark-validate-links|sphinx-build|SPHINXOPTS|mkdocs\s+build|mdbook\s+(?:build|test)|treat(?:Validation)?WarningsAsErrors|oasdiff|openapi-diff|spectral\s+lint|fail\s*:\s*false|continue-on-error\s*:\s*true' "${G[@]}" -g '!**/node_modules/**' .; ck S1 $?
# S2. Links into the docs from code, alerts and config (§5): runbook_url and doc paths in strings.
rg -n --pcre2 'runbook_url\s*:|["\x27`](?:\./)?(?:docs?|runbooks?)/[\w./-]+\.mdx?(?:#[\w-]+)?["\x27`]|/blob/[^/\s"\x27]+/(?:docs?|runbooks?)/' -g '!**/{migrations,migrate,seeds}/**' -g '!*.{md,mdx,lock}' "${X[@]}" .; ck S2 $?
# S3. Declared locales and translation markers (§10–§12).
rg -n --pcre2 '\blocales\s*:|defaultLocale|^\s*-\s*locale\s*:|locale_dirs|fallback_to_default|source[-_ ]?commit\s*:|translated_from_sha' -g '*.{js,ts,mjs,yml,yaml,py,toml,md,mdx}' "${X[@]}" .; ck S3 $?
# Tool lanes: lychee offline (exit 2 = broken links, 1/3 = lychee failed), then the online lane only with NETWORK=1.
if command -v lychee >/dev/null; then lychee --offline --include-fragments --no-progress --format json --output "$OUT/lychee.json" './**/*.md' './**/*.mdx' >/dev/null 2>&1
  r=$?; case $r in 0) echo "lychee offline ran: 0 broken";; 2) echo "lychee offline ran: broken links in $OUT/lychee.json";; *) echo "lychee BLOCKED (exit $r: tool or config error)";; esac
  if [ -n "$NETWORK" ]; then lychee --include-fragments --no-progress --accept '200..=299,403,429' --format json --output "$OUT/lychee-net.json" './**/*.md' >/dev/null 2>&1; echo "lychee online exit $? (DL-3: no --cache here, it writes .lycheecache into the tree; rerun failures once before reporting)"; else echo "§3 N/A (offline by default; NETWORK=1 runs it)"; fi
else echo "lychee NOT-RUN (not installed) — the engine's links lane is the oracle"; fi
if [ -x node_modules/.bin/markdownlint-cli2 ] && ls .markdownlint* >/dev/null 2>&1; then node_modules/.bin/markdownlint-cli2 "**/*.md" "#node_modules" > "$OUT/mdl.txt" 2>&1; r=$?; [ $r -ge 2 ] && echo "markdownlint BLOCKED (exit $r)" || echo "markdownlint ran: exit $r (only MD042/MD051/MD052 rows feed §1–§2; style is NIT)"; else echo "markdownlint NOT-RUN (no config or binary)"; fi
if command -v kacl-cli >/dev/null && [ -f CHANGELOG.md ]; then kacl-cli verify --json > "$OUT/kacl.json" 2>&1; echo "kacl-cli exit $? = error count (0 valid)"; else echo "kacl-cli NOT-RUN — the engine's changelog lane is the oracle"; fi
find . -newer "$OUT/stamp" -type f -not -path './node_modules/*' -not -path './.git/*' | head -3; echo "write check done (empty = nothing written)"
```

A site build (`mkdocs build --strict`, `sphinx-build -W`, `docusaurus build`) is the strongest oracle for §1, §2 and §14 when the toolchain is pinned: run it in `git archive HEAD | tar -x -C "$OUT/site"` after a scratch install, never in the tree; without the install it is `NOT-RUN (no install)`, and the engine stands.

## Measured

Measured 2026-10-19 (`doc-claims 1.0`, self-test 46/46).

- **A real NestJS + React monorepo** (read-only, write check empty): 107 human docs in scope, plain GitHub rendering (no docs site). DL-1 277 links → 0 (6 broken links the eval found live in installed `ai/patterns`, now routed `-> learning`), DL-2 45 fragments → 0, DL-3 1 external link counted, offline. DK-3 63 → 60 links into docs after migration files are skipped as history (one migration comment pointed at a deleted doc), → 0. ADRs 40 + an index: DX-1 2 supersessions → 0 (the one partial "Supersedes: the chrome clause of [0016]" no longer flips 0016, § 30), DX-2 41 → 1 (a "retired 2026-10-09" status outside the installed template's vocabulary), DX-3 0. DH-2: 1 changelog, 0. DI, DF-2, DL-4: N/A (no doc locales, no site nav, no docs gate). Greps: S1 0 (no docs gate in CI, scripts or a site config) · S2 42 (30 alert `runbook_url`s into `ai/runbooks/`, all resolving) · S3 31 (UI-catalog `locales:` keys of the web app: frontend `i18n-scan`'s, not doc locales). S1 first matched `remark` as a code identifier and `strict: true` in a TypeScript config (300+ lines); it now reads CI, scripts and site configs only.
- **Fixtures**: `backend-defects` DL-4 2 (`oasdiff breaking` with no `--fail-on` in a workflow and a package script: the backend seed, seen from the gate side); `infra-ops` DX-2 1 (an ADR with no status); `mobile-defects` DF-1 1 (a `TODO` in prose). Greps: S1 1 (`backend-defects`), S2 26 on `obs-defects` (its alert rules), ≤ 2 elsewhere, S3 ≤ 2. Every other fixture prints 0 structure rows: they carry no docs site, ADR set or translation, so the seeded corpus is the engine's `--self-test` until a doc fixture lands (integrator request).
- **The `doc-drift` fixture** (2026-10-19, history staged): the pre-flight printed **28 candidates, two per class for every engine §** (DL-1 3: the third is the DI-3 seed's Arabic link, one root cause; DL-4 3: the CI `mkdocs build` and `mkdocs.yml` `strict` rows are one finding), all 26 engine-detectable doc-structure-scan seeds; DL-3 `N/A (offline)` with 10 external links counted. 0 of 22 decoys printed as a candidate (the `#L42` anchor, the banner page § 11 and `docs/v1/` § 12 printed as skips). DI-2 needs the history script: on the one-commit copy every pair compares a commit with itself and prints `checked (6 claims -> 0)`, which reads as clean (engine gap; integrator). **S1 printed 0 workflow lines on its first run**: rg skips `.github/` without `--hidden`, so a lychee step with `fail: false` was invisible; S1 now passes `--hidden` and prints 5 lines here, and on the other fixtures 7 on `backend-defects`, 2 on `ci-defects`, 1 on `brittle-suite`, 0 elsewhere. S2 7 (4 alert `runbook_url`s, 3 error-message doc URLs), S3 3; lychee, markdownlint and kacl-cli NOT-RUN (not installed).

## The 3,000-row path

1. **Scope and renderer first.** A ledger with a wrong renderer (MkDocs slugs read as GitHub ones) turns every non-ASCII anchor into a row; fix the detection before reading any. An area over 30% of the rows is checked against precedents § 1, § 2, § 12, § 28.
2. **Group by target, not by line.** One renamed heading is **one finding with N inbound links**: `cut -f3,7 claims.tsv | sed 's/#.*//' | sort | uniq -c`. One deleted page: one finding.
3. **Read in this order:** primary surface (README, quickstart, runbooks), DK-3 inbound links from code and alerts, the gate (§4), ADR and changelog metadata, translations, hygiene.
4. **Close a group with one checked reason** (`40 DI-1 rows under docs/ar/: lag policy declared in docs/translations.md:4, § 11`).
5. **Ledger the rest** as `Live, unreviewed (k groups / n rows)` with the `--class` command that continues it.

## Scans for

| § | Class | Lane | Finding when | Default (primary) | Oracle |
|---|---|---|---|---|---|
| 1 | DL-1 relative link to a missing file | links | no file after the doc dir, the site root and the renderer's route forms | MEDIUM | V430 |
| 2 | DL-2 anchor missing | links | no slug of the target page under its renderer | MEDIUM | V430 |
| 3 | DL-3 external URL dead | lychee online (`NETWORK=1`) | 404 / 410 / DNS twice, with a token | LOW; MEDIUM in a quickstart | V431 |
| 4 | DL-4 the docs gate cannot fail | gates | a config or CI line silences the gate, or the gate checks nothing | MEDIUM | V432 |
| 5 | DK-3 link into the docs resolves to nothing | linksin | a `runbook_url`, doc path in code or blob URL of this repo with no file or anchor | MEDIUM; HIGH for an alert's runbook | V430 |
| 6 | DX-1 supersession one-way or target missing | adr | the target is absent, or the superseded ADR still reads Accepted | MEDIUM | V447 |
| 7 | DX-2 status vocabulary and index | adr | a status outside the template's vocabulary, or the index disagrees with or misses the file | LOW | V447 |
| 8 | DX-3 duplicate or colliding number | adr | two files share a number, or the title number ≠ the file number | LOW | V447 |
| 9 | DH-2 changelog structure | changelog | order, duplicates, non-ISO dates, compare links, `[Unreleased]` placement | LOW | V445 |
| 10 | DI-1 translation missing | i18n | a declared locale lacks the page, with no lag policy | LOW | V448 |
| 11 | DI-2 translation stale | i18n | commits touched the source after the translation's marker, with no outdated banner | LOW; MEDIUM on a setup page | V448 |
| 12 | DI-3 translation diverges | i18n | the translation carries a code block or link target the source does not | MEDIUM | V448 |
| 13 | DF-1 placeholder in published prose | placeholders | `TBD`, `TODO`, `FIXME`, `lorem ipsum`, `<insert …>` outside fences | LOW | V449 |
| 14 | DF-2 orphan page or nav to nothing | nav | a nav entry to a missing page, or a page in no nav and linked from nowhere | LOW | V449 |

### 1. Relative link to a missing file (DL-1)

```
BAD:   README.md   [Deploy guide](docs/deploy.md)          (moved to docs/operations/deploy.md)
GOOD:  [Deploy guide](docs/operations/deploy.md)            · and every other doc that links the old path
```
**Read the docs:** Did the engine try the renderer's forms (extensionless routes, `index.md`, `/README.md`, `.html` → `.md`)? Is the target gitignored or generated at build (§ 4)? A case-only mismatch prints CHECK: it works on macOS and breaks on Linux CI. What does the rename lookup say (`renamed -> …`)? **Finding when** no form resolves. **Proof:** V430; lychee offline exit 0 and `--claim=<target>` prints no row.

### 2. Anchor missing (DL-2)

```
BAD:   docs/setup.md#install-steps        (heading is "## Installing", slug `installing`)
GOOD:  docs/setup.md#installing   ·   or `## Install steps {#install-steps}` where the renderer honours custom ids
```
**Read the docs:** Which renderer serves the target (the ledger names it)? MkDocs strips non-ASCII unless `pymdownx.slugs`; duplicates are `_1` there and `-1` on GitHub. Is the anchor from an HTML `id=`, an MDX component, or a plugin (mkdocstrings) the engine cannot see (CHECK)? `#L42` and `#top` are fine (§ 10). **Finding when** no slug or id matches under the renderer in use. **Proof:** V430 (lychee `--include-fragments`, or the strict site build).

### 3. External URL dead (DL-3)

```
BAD:   docs/integrations.md   https://api.vendor.invalid/v1/docs      (DNS failure, twice)
GOOD:  the current URL, or the link removed with the integration
```
**Read the docs:** Offline by default: the coverage block prints `N/A (offline)`. Under `NETWORK=1`, is it 403, 429 or 999 (an auth wall or rate limit, § 15)? A GitHub URL needs `GITHUB_TOKEN`. **Finding when** 404, 410 or DNS failure reproduces twice. **Proof:** V431.

### 4. The docs gate cannot fail (DL-4)

```
BAD:   docusaurus.config.ts   (no onBrokenAnchors)          → default 'warn': a broken anchor ships green
       .github/workflows/docs.yml   uses: lycheeverse/lychee-action@v2  with: fail: false
       "lint:docs": "remark . --use remark-validate-links"   → no --frail: warnings exit 0
       oasdiff breaking a.yaml b.yaml                        → no --fail-on: exit 0 on a breaking diff
GOOD:  onBrokenAnchors: 'throw'  ·  fail: true  ·  remark --frail  ·  oasdiff breaking --fail-on ERR
```
**Read the docs and the config:** Does the gate run on PRs, or only on `main`? Is `continue-on-error: true` on the step or the job? For MkDocs, `strict: true` without `validation.links.anchors: warn` still passes missing anchors (§ 32). Spectral with no ruleset lints nothing. **Finding when** a planted defect would pass the gate as configured. **Proof:** V432, the mutation proof (plant a broken link and a broken anchor in a scratch copy, run the gate, assert non-zero through its exit map).

### 5. Link into the docs resolves to nothing (DK-3)

```
BAD:   deploy/alerts/api-alerts.yml   runbook_url: docs/runbooks/api-down.md#mitigate    (file renamed api-outage.md)
       src/errors.ts             'See docs/troubleshooting.md#tls'                   (heading renamed)
GOOD:  the URL repointed in the alert and the code string, in the same change as the rename
```
**Read the docs and the code:** Is the URL this repo's (relative, or a blob URL of the `origin` remote)? Templated (`{{ $labels.x }}`) is § 6. A migration comment is history (§ 1). **Finding when** the file or anchor is absent. **Proof:** V430. The alert with no `runbook_url` at all is observability's.

### 6. Supersession one-way or target missing (DX-1)

```
BAD:   0003-cache.md   Status: Superseded by [0006](0006-redis.md)      0006-redis.md: no "Supersedes"
       0007-auth.md    Status: Accepted · Supersedes [0004](0004-jwt.md) 0004-jwt.md: Status: Accepted
GOOD:  0006: "Supersedes [0003](0003-cache.md)" · 0004: "Status: Superseded by [0007](0007-auth.md)"
```
**Read the docs:** Are the ids from links or `ADR-n` tokens (a date is not an id, § 26)? Is the supersession partial ("the chrome clause of", "amends", § 30)? Did `adr-tools new -s` write both ends? **Finding when** a target is absent, or a whole supersession left the older ADR reading Accepted (readers follow a dead decision). **Proof:** V447.

### 7. Status vocabulary and index (DX-2)

```
BAD:   0012-x.md   (no status line)          docs/adr/README.md   | 0002 | … | Proposed |   (file: Accepted)
GOOD:  Status: Accepted in the file, and the index row the same
```
**Read the docs:** Where does the vocabulary come from: the project's ADR template or `adr-template.md` lifecycle (then out-of-vocabulary is WRONG), else MADR / Nygard, an open set (CHECK)? Free-text qualifiers after the first word ("Accepted · amended by …") are fine. Is the index generated (log4brains, adr-tools `toc`)? **Finding when** a status is missing or outside the declared vocabulary, or the index disagrees with or omits a file. **Proof:** V447.

### 8. Duplicate or colliding number (DX-3)

```
BAD:   docs/adr/0009-queue.md and docs/adr/0009-events.md     ·   0011-x.md titled "# 10. X"
GOOD:  0010-events.md, never reusing a number (Nygard)
```
**Read the docs:** A renumbered import with a redirect note is not a collision. **Finding when** two files share a number or a title contradicts its file. **Proof:** V447.

### 9. Changelog structure (DH-2)

```
BAD:   ## [1.1.0] - 2026-02-01   above   ## [1.2.0] - 2026-03-01     ·   ## [1.0.0] - 01/01/2026
       [Unreleased]: …/compare/v1.1.0...HEAD   while the latest release is 1.2.0
GOOD:  descending versions, ISO dates, one link reference per version, [Unreleased] first and comparing from the latest
```
**Read the docs:** Which generator writes it (release-please, changesets, git-cliff, semantic-release, § 17)? Fix at the generator. Changesets has no dates; release-please puts them in parentheses. Per-package changelogs version independently (§ 18). **Finding when** the grammar the file follows is broken. **Proof:** V445 (`kacl-cli verify`, exit = error count, or the engine lane).

### 10. Translation missing (DI-1)

```
BAD:   docusaurus i18n.locales: [en, ar]      i18n/ar/docusaurus-plugin-content-docs/current/setup.md  absent
GOOD:  the page translated, or a declared policy naming the minimum content per locale
```
**Read the docs:** Is the locale declared in config (MISS) or inferred from a `docs/<lc>/` folder? Does a doc declare a lag or minimum-content policy (§ 11)? mkdocs-static-i18n `fallback_to_default: true` renders the source page instead and hides the gap. **Finding when** a declared locale lacks a page and no policy allows it. **Proof:** V448.

### 11. Translation stale (DI-2)

```
BAD:   docs/de/setup.md   <!-- source-commit: 1a2b3c4 -->      git log 1a2b3c4..HEAD -- docs/setup.md: 3 commits
GOOD:  re-translated and the marker moved, or an outdated banner under the declared policy
```
**Read the docs:** With a marker, the engine counts commits since it; without one it compares commit times (CHECK). A shallow clone breaks both (use full history). **Finding when** the source changed after the marker and no banner says so. **Proof:** V448.

### 12. Translation diverges (DI-3)

```
BAD:   docs/de/setup.md   ```bash pnpm dev:all ```       docs/setup.md   ```bash pnpm dev ```
GOOD:  the translated page carries the source's commands, code and link targets; only prose is localised
```
**Read the docs:** Strings and comments inside code are normalised away (localised example values are fine); what differs is a command, a statement or a link target. **Finding when** the translation carries a code block or link the source no longer has: its reader runs an old command. **Proof:** V448.

### 13. Placeholder in published prose (DF-1)

```
BAD:   docs/billing.md   "Refunds: TBD."   ·   "<insert the webhook URL here>"
GOOD:  the content, or the page kept out of the nav until it exists
```
**Read the docs:** A placeholder inside a config fence (`<your-api-key>`) is § 6; a roadmap or TODO file is its own content. A proposed ADR with open questions is normal. **Finding when** published prose ships the placeholder. **Proof:** V449.

### 14. Orphan page or nav to nothing (DF-2)

```
BAD:   mkdocs.yml   nav: - Billing: billing/overview.md      (file moved)      docs/old-login.md: in no nav, linked from nowhere
GOOD:  nav repointed; the orphan linked, listed in not_in_nav, or deleted
```
**Read the docs:** Is the page reachable through another page's link (by design)? `not_in_nav` patterns? Autogenerated sidebars have no orphans. **Finding when** a nav entry resolves to no page, or a page is reachable from nothing. **Proof:** V449 (the strict site build, or the engine lane).

## Output

```
doc-structure-scan — doc-claims 1.0 · renderer mkdocs (docs/) · 212 docs · locales ar (mkdocs-static-i18n) · lychee 0.24.2 offline

Findings: 3 · Unconfirmed: 1

1. docs/setup.md:14 ← 12 inbound links                         [report-with-fix]  MEDIUM · §2
   Heading "Install steps" renamed "Installing": 11 docs and deploy/alerts/api-alerts.yml:31 link #install-steps
   (mkdocs slugger). Fix: one rename across 12 sites, or {#install-steps} on the heading.
2. mkdocs.yml:1                                                 [report-with-fix]  MEDIUM · §4
   No strict and validation.links.anchors at info: a planted broken anchor builds green (mutation proof:
   mkdocs build exit 0). Fix: strict: true, validation.links.anchors: warn.
3. docs/de/setup.md:9                                           [report-with-fix]  MEDIUM · §12
   ```bash pnpm dev:all``` — the source page docs/setup.md:9 now runs `pnpm dev`.
4. docs/adr/0003-cache.md:3                                     [report-flagged]   MEDIUM · §6
   Superseded by 0006; 0006 never says Supersedes. Unproven link: is 0006 a whole replacement (§ 30)?

Verification: 31 candidates → 3 findings · 1 unconfirmed · 9 hardening · 0 pre-existing · 18 refuted

Class coverage:
  §1  missing file          checked (277 links → 0)
  §2  missing anchor        checked (45 fragments → 12 → 1 group)
  §3  external link         N/A (offline by default; NETWORK=1 runs lychee online)
  §4  gate cannot fail      checked (2 gates → 1; mutation proof recorded)
  §5  links into docs       checked (60 links → 1, folded into §2)
  §6  supersession          checked (3 pairs → 1 unconfirmed)
  §7  status / index        checked (41 statuses, 1 index → 0)
  §8  numbering             checked (40 files → 0)
  §9  changelog structure   checked (1 changelog, generator none → 0) · kacl-cli NOT-RUN
  §10 translation missing   checked (36 pages × ar → 0; lag policy docs/translations.md:4, § 11)
  §11 translation stale     checked (36 pairs → 4 CHECK → 0; banners present)
  §12 translation diverges  checked (36 pairs → 1)
  §13 placeholders          checked (212 docs → 0)
  §14 orphan / nav          checked (48 nav entries → 0)
  routed                    agent-facing docs → learning knowledge-ref-scan (329) · alerts without runbook_url → observability alert-rule-lint
```

`[report-with-fix]`: the target is cited, the oracle fired (engine, lychee, the build or the mutation), the fix is a docs edit. `[report-flagged]`: one link unproven (a renderer that may define the anchor, a partial supersession, a policy), named with its settling probe. Every run prints **all fourteen** §s as `checked (k → m)`, `N/A (<reason>)`, `blocked (<lane>: <reason>)`, `→ <owner> (k)` or `Live, unreviewed`; a tool lane prints `NOT-RUN (<why>)`, never PASS.

## Precedents

The verifier reads [`precedents/documentation.md`](../../../../snippets/precedents/documentation.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most: § 1 dated records keep only doc-to-doc links, § 10 renderer slugs, § 11 translation lag, § 12 versioned docs, § 15 external status codes, § 17 generated changelogs, § 22 style is not a gate, § 26 the ADR id parser, § 29 a gate is proven by failing, § 30 partial supersession, § 32 per-tool exit codes. The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Documentation, V430–V432, V445, V447–V449.

## When to run

- On every whole-repo `/doc-refresh --audit`, printing all fourteen §s.
- On a diff that renames or deletes a doc or a heading, edits a docs-site config, a nav or sidebar file, an ADR, the changelog or a translated page, or a CI step that runs a docs tool.
- Before relying on a green docs job: §4 with the mutation proof.

## Halt conditions

- Do not report a HIGH or BLOCKER row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md); under `/doc-refresh --audit` that is `@verifier` in refute mode. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and keep the rest Unconfirmed, Hardening or Refuted. Never drop them.
- Halt on any finding without the doc line, the target it fails to reach (file, slug list, reciprocal ADR, source page or gate line) and the V-number.
- Do not trust an exit code across tools: read each through its map (lychee 2 = broken links); a NOT-RUN tool lane is never PASS (§ 33).
- Do not grade a gate as working because the job is green: §4 needs the mutation proof (§ 29).
- Do not run a site build, lychee cache or linter cache inside the tree; scratch copies only, and the write check must print nothing.
- Do not report Markdown style as a finding unless the project enforces the linter (§ 22), and do not print "docs structure holds" without the class-coverage block.

## Related

- `doc-drift-scan` (this pack) owns the engine `scripts/doc-claims.py` and the docs-against-code classes; `doc-sample-scan` the fences and spec examples; `/doc-refresh --audit` runs all three and `--from-audit` closes the findings failing first.
- `/add-adr` writes ADRs with both supersession ends; `/add-runbook` writes runbooks this skill's §5 links must reach; `changelog-generate` writes the changelog §9 parses.
- Observability `alert-rule-lint`, devops `release-integrity-scan` RL-2, align `convention-oracle`, frontend `i18n-scan` and the learning pack's `knowledge-ref-scan`, each when its pack is installed.
