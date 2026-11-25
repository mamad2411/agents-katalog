---
name: knowledge-fact-scan
description: Knowledge claims vs lockfile and sources — wrong engine or ids, stale counts, derived copies, drifted citations.
kind: skill
pack: learning
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: knowledge-fact-scan

## Premise

The costliest knowledge defect is not a missing doc: it is a wrong fact multiplied by derivation. On a real NestJS + React monorepo one anchor bullet said "MikroORM (MySQL) with ULID PKs" and "testcontainers-MySQL e2e" in **177 installed artifacts** (49 agents, 57 commands, 71 skills). The lockfile resolved `@mikro-orm/postgresql` and `uuidv7`; the profile those bullets cite by line had been corrected to Postgres 16 and UUIDv7; the session digest said "Postgres 16, not MySQL". Every identifier in the stale bullet still resolved, so the setup audit's reference check passed it, and every agent loaded the wrong database into its context.

`scripts/knowledge-facts.py` (this skill) compares what the knowledge layer claims with what the repository can prove: §1 typed facts vs the manifest and lockfile (KN-07), §2 count and range claims (KN-08), §3 the module map vs the member directories (KN-09), §4 one key with two values across loaded files (KN-11), §5 a derived file vs its recomputed source (KN-13), §6 a citation whose cited line no longer carries the claim (KN-14). §7 (KN-12, one fact in N copies) is how every row is reported: identical claims collapse into **one finding with N sites**, and class 7 adds a normalised-paragraph hash (≥ 80 characters, generated files skipped) for a paragraph copied into two loaded files ([`precedents/learning.md`](../../../../snippets/precedents/learning.md) § 17).

**Every finding cites the knowledge `file:line` + the claim as written + the truth and where it was read (lockfile line, manifest, the cited line at HEAD, the tree) + the number of sites that carry the same claim + the fix (source wins: overwrite with the lockfile value, or regenerate the derived copy).** A word match is never a finding by itself, and "facts consistent" is never printed without the class-coverage block.

## The rule

A claim is a finding when all four hold:

1. **It is a live, typed claim.** An engine, an ORM driver, a framework or runtime major, an id scheme, a package manager, a count of a named set, an ADR range, or a `path:line` citation — in a live region (P-3, P-10, P-21) and not history-marked (§ 14: "not MySQL", "was X, now Y", an arrow, "any doc still saying ULID is stale").
2. **The truth is read, not remembered.** The lockfile (pnpm 6–9, npm 7+, yarn v1/berry, poetry, uv, go.mod, Gemfile.lock, composer.lock), the manifests, `.nvmrc`/`engines`/volta, compose `image:` lines, Prisma `provider`. A key with no truth source is UNREAD in the ledger, never "consistent".
3. **They disagree at the level that matters.** Engine and id scheme by identity, framework and runtime by MAJOR only (§ 12: `engines >=18` is satisfied by 22; "React 18+" by 19). A line naming several values for one key is a capability list or a correction, not a claim.
4. **The source wins.** The fix is the lockfile-derived value, or a regeneration of the derived copy from its source — never a hand edit of a generated block.

## Boundaries

- **A reference that does not resolve** → `knowledge-ref-scan` §1 (a cited file that is gone is its row; this skill only checks citations whose file resolves). **A citation inside a sink entry** → `memory-hygiene-scan` §1.
- **A convention claim the code majority contradicts** (KN-10) → align `convention-oracle` AL-04 when the align pack is installed; without it the row is `N/A (owner pack align not installed)` and `/detect-drift`'s fallback agent reads it.
- **Architecture diagrams** (KN-09 in a diagram) → documentation `diagram-sync` when the documentation pack is installed; §3 here reads the text map only.
- **Unmarked claims and approval stamps in the oracle** (KN-16, 18) → `/setup-project-health` checks 11 and 9; **a sampled oracle** (KN-17) → `audit-setup.sh` C2v. `/audit-knowledge` reads them, this skill does not re-grade them.
- **The decision index's ADR home** → `decision-record-scan` §0 detects it; §5 here checks the index's rows against it.

## Adapt to the codebase — the truth lanes

| Lane | Truth for engine / driver | Truth for majors and runtime | Truth for id scheme | Trap |
|---|---|---|---|---|
| **Node / TS** | driver packages (`pg`, `mysql2`, `@mikro-orm/postgresql`, `better-sqlite3`, `mongoose`, `@prisma/adapter-pg`), Prisma `provider`, compose images | `pnpm-lock.yaml` / `package-lock.json` / `yarn.lock` resolved versions; `.nvmrc`, `.node-version`, `.tool-versions`, `engines.node`, volta | `ulid`/`ulidx`, `uuidv7`, `uuid` (does v4 and v7: never a contradiction), `@paralleldrive/cuid2`, `nanoid` | a range is not a pin; a monorepo may resolve two majors (any match passes) |
| **Python** | `psycopg`, `psycopg2`, `asyncpg`, `pymysql`, `mysqlclient`, `pymongo` | `poetry.lock`, `uv.lock`; `requires-python`, `.python-version` | `python-ulid`, `uuid6`, `uuid-utils` | `requirements.txt` without pins: UNREAD for majors |
| **Go** | `gorm.io/driver/*`, `github.com/jackc/pgx`, `github.com/go-sql-driver/mysql` | `go.mod` requires and the `go` line | `github.com/oklog/ulid/v2` | a module path is not a version: majors come from the `vN` suffix or the require line |
| **Ruby / PHP** | `pg`, `mysql2`, `sqlite3` gems; `doctrine/dbal` | `Gemfile.lock`, `composer.lock` | — | Laravel picks the driver from `.env`, which is not read: engine UNREAD unless compose names it |
| **Any** | `docker-compose*.yml` / `compose*.yaml` `image:` (postgres, mysql, mariadb, mongo) | — | — | an image for a sidecar (a test DB, an analytics store) adds an engine: both are true |

## Pre-flight

Run as **one** bash script from the repo root. Step **N** feeds detector **§N**. Every `rg` names its paths; any `rg` exit 2 is `blocked`. Includes first, exclusions last.

```bash
[ -n "${BASH_VERSION:-}" ] || { echo "pre-flight: run it with bash (arrays and PIPESTATUS are bash-only)"; exit 2; }
KS="${KS:-.claude/skills}"        # installed engines; in the Refract repo itself: templates/packs/learning/skills
RUN="${RUN:-$(mktemp -d "${TMPDIR:-/tmp}/knowledge.XXXXXX")}"; mkdir -p "$RUN"; echo "RUN=$RUN"
export GIT_OPTIONAL_LOCKS=0 DO_NOT_TRACK=1 CI=true
ROOTS=(); for p in CLAUDE.md CLAUDE.local.md AGENTS.md GEMINI.md ai .claude/rules .claude/agents .claude/commands .claude/skills \
  .claude/codebase-profile.md .cursor .github/copilot-instructions.md; do [ -e "$p" ] && ROOTS+=("$p"); done
[ ${#ROOTS[@]} -gt 0 ] || { echo "§1-§7 N/A: no knowledge layer"; exit 0; }
H=(-g '!**/ai/audits/**' -g '!**/ai/incidents/**' -g '!**/ai/runs/**' -g '!**/ai/migration/**' -g '!**/ai/dynamic/**' -g '!**/ai/failures/**'
   -g '!**/*_history.md' -g '!**/CHANGELOG*' -g '!**/node_modules/**')

# 1-7. The engine: typed claims (P-14 and capability lists filtered), lockfile truth, counts, module map,
#      cross-file keys, derived files, citation windows; identical claims grouped (KN-12).
python3 -I "$KS/knowledge-fact-scan/scripts/knowledge-facts.py" . > "$RUN/facts.tsv" 2> "$RUN/facts.ledger"
echo "knowledge-facts exit $? (0 clean · 1 rows · 2 blocked)"; cat "$RUN/facts.ledger"; cut -f1-9 "$RUN/facts.tsv"
python3 -I "$KS/knowledge-fact-scan/scripts/knowledge-facts.py" . --expand > "$RUN/facts-sites.tsv" 2>/dev/null   # one row per site

# Cross-checks: the truth the engine read, and the claims a plain search sees.
# 1a. Driver packages in every manifest (the engine's engine truth).
rg -n --pcre2 '"(?:pg|postgres|mysql2?|mariadb|@mikro-orm/(?:postgresql|mysql|mariadb|sqlite|mongodb)|better-sqlite3|sqlite3|mongoose|mongodb|@prisma/client|typeorm)"\s*:' \
  -g '**/package.json' -g '!**/node_modules/**' . ; echo "rg 1a exit $?"
# 1b. Engine and id-scheme words in the knowledge layer: the engine's row count must be explained against this.
rg -c --pcre2 '\b(?:MySQL|MariaDB|Postgre(?:SQL|s)|SQLite|Mongo(?:DB)?|ULIDs?|UUID\s?v?7)\b' -g '*.md' "${ROOTS[@]}" "${H[@]}" > "$RUN/g1b.txt"
echo "rg 1b exit $? ($(wc -l < "$RUN/g1b.txt" | tr -d ' ') files)"
# 6. Citations of the form path:line (§6 reads each one whose file resolves).
rg -o --pcre2 '`?(?:[\w@.-]+/)*[\w@.-]+\.[A-Za-z0-9]{1,6}:\d+' -g '*.md' "${ROOTS[@]}" "${H[@]}" > "$RUN/g6.txt"
echo "rg 6 exit $? ($(wc -l < "$RUN/g6.txt" | tr -d ' ') citations)"
```

Read the ledger first: the lockfiles read (or `UNREAD (no lockfile: majors not checked)`), the truth per key, and the claims per key. A key whose truth is UNREAD cannot produce a §1 row, and the coverage block says so.

**Measured** (2026-10-19), read-only on a real NestJS + React monorepo (13,620 tracked files, 478 knowledge files scanned, 9.4 s; 0 files written). Truth read from `pnpm-lock.yaml` (1,594 packages) and `.nvmrc`: engine postgres, ORM mikro-orm, id schemes cuid/nanoid/uuidv7, pnpm, Node 22 pinned, 13 framework majors. Claims: 966 engine, 410 id-scheme, 717 ORM, 44 framework-major, 18 package-manager, 17 scoped counts, 2,174 citations.
- §1: **3 groups × 177 sites** — the MySQL bullet (two lines per anchor) and the ULID bullet, grouped as KN-12; plus `ESLint 9` in the profile and `ai/conventions.md` against a lockfile that resolves ESLint 10. rg 1a confirms one driver: `@mikro-orm/postgresql` in `apps/api/package.json`; rg 1b lists 396 files with an engine or id-scheme word (196 mention MySQL) — beyond the anchors, history-marked corrections and capability lists the engine filters (P-14); rg 6 counts 2,887 `path:line` citations, of which the 2,174 whose file resolves reach §6.
- §2: 5 rows — "every file 0001–0033 has a row" against 0001–0040 on disk; "30 ADRs" in the digest (40 on disk); a stale "63 commands, 50 agents, 75 skills" table. The first cut also counted "168 rules" and "40 workspaces" (business rules, tenants) and "9 agents running" (concurrent processes): P-28 now requires the line to name the set.
- §3: 1 module directory with 9 tracked files not listed in `ai/modules.md`.
- §4: 3 keys with two values (engine, id scheme, ESLint major), each pointing at its §1 rows.
- §5: the decision index missing ADRs 0034–0040; **2 groups × 177 anchors** whose cited profile line now says Postgres/UUIDv7; 2 derivation shas with source commits since (Unconfirmed); 51 pattern anchors citing a profile line that carries neither id scheme while the claim agrees with the lockfile (Unconfirmed, P-27).
- §6: 52 citations past the end of the cited file (55 sites; code moved) and 34 aggregate citations where none of the named identifiers sits within ±3 lines (Unconfirmed, the R3 trap).
- On `benchmarks/fixtures/*` (24 trees): 0 rows — none carries typed claims against a lockfile. The self-test seeds 18 rows (3 anchors stale against the lockfile and against the cited line, React 18 vs 19, Node 18 vs `>=20`, npm vs pnpm, a range, a module count, a past-EOF citation, an unlisted module, an index missing 2 ADRs, a derivation sha behind its source, a second derived file at the same sha, a citation one past the last line, a port stated two ways, a paragraph copied into two files) and 11 decoys ("not MySQL", "about 30", an unscoped "168 rules", "~25 commands", "9 agents" with no `.claude/` near it, a supporting citation, a capability line in a generic body, Node 22 inside `>=20`, listed modules, environment-named ports, a generated Copilot copy).
- On `stale-knowledge` (the seeded fixture; truth from `pnpm-lock.yaml` and `.nvmrc`: postgres, uuidv7, mikro-orm, pnpm, Node 22): 33 files, 20 grouped rows (31 with `--expand`), all on seed sites — **15 seeds printed**: the stale Data access bullet as one KN-07 and one KN-13 group of 6 anchors (KN-12), MySQL in a deepened anchor, ULID in an always-loaded rule, React 18, a stale ADR range and module count, an unlisted 6-file module, npm vs pnpm, the index missing two ADRs, a cheatsheet and a digest derived before their sources changed (one row each: each file has its own sources), a rewritten citation (Unconfirmed), one past EOF, the API port stated as 4000 and 3000 (§4 `port:api`), and a verbatim tenancy paragraph in `CLAUDE.md` and `ai/architecture.md` (§7 paragraph hash, Unconfirmed; the generated Copilot file and the derived files are skipped). Decoys: 0 of 26.

## The 3,000-hit path

1. **Group by root cause** — already done: identical claim text collapses into one row with `sites=N` and a per-directory breakdown. 177 anchors are one finding: "anchors were never regenerated after the profile changed".
2. **Fix the source, then regenerate.** A derived copy (anchor, index, cheatsheet) closes when its source is right and the generator re-runs, never by editing N files.
3. **Rank by load**: anchors and files loaded every session first, then `ai/*` read by commands.
4. **Read the top 30 groups fully**, both ends: the claim and the truth line.
5. **Ledger the rest** as `Live, unreviewed (k groups / n sites)` with `knowledge-facts.py . --expand --classes=<n>`.

## Scans for

| § | Class | Default |
|---|---|---|
| 1 | KN-07 fact vs manifest or lockfile (engine, driver, ORM, id scheme, framework or runtime major, package manager) | M; H in a loaded file or an anchor |
| 2 | KN-08 count or range claim drift | L; M in a loaded file |
| 3 | KN-09 module map vs member directories (present, not listed) | M |
| 4 | KN-11 one key, two values across loaded files | H for engine and id scheme, else M |
| 5 | KN-13 derived file stale vs its source | M; H for an anchor set |
| 6 | KN-14 citation no longer supports the claim | M; L when the claim agrees with the lockfile |
| 7 | KN-12 one fact in N copies | the grouping of every row above |

### 1. Fact vs manifest or lockfile (KN-07)

```
BAD:   > - **Data access** (`.claude/codebase-profile.md:19`): MikroORM (MySQL) with ULID PKs     lockfile: @mikro-orm/postgresql, uuidv7
       CLAUDE.md: "pnpm monorepo on React 18"                                                   lockfile: react 19.2.0
GOOD:  "Postgres 16, not MySQL; UUIDv7, not ULID" (P-14) · "works with Postgres, MySQL or MongoDB" in a generic body (capability list, P-10)
       "Node 22" with `engines.node >=20` (a range is satisfied by a major inside it)
```
**Read the code:** Which lockfile did the ledger read, and does it resolve one major or several (a monorepo can hold two)? Is the engine a sidecar (an analytics DB beside the primary)? Is the line a correction or a migration plan (P-14, P-7)? Is the claim inside a generated block whose source is right (then it is §5 too)? **Finding when** a live claim names a value the truth source excludes. **Proof:** tier S + V494 — the claim quoted beside the lockfile line; after the fix the typed-fact diff for that site is empty (`--only=<file>:<line>` quiet).

### 2. Count or range claim (KN-08)

```
BAD:   "every file in `docs/decisions/` (0001–0033) has a row"       on disk: 0001–0040
       "`.claude/` — 63 commands, 50 agents, 75 skills"               on disk: 100, 63, 87
GOOD:  "about 30 modules" · "Last 6 decisions" · "as of 2026-09-01, 33 ADRs" · "168 rules" in a domain doc (P-28)
```
**Read the code:** Does the line name the set it counts (`.claude/`, `ADRs`, `src/modules`)? Is it dated or approximate? **Finding when** an exact count or range of a named set disagrees with the tree. **Proof:** tier S + V495 — the count recomputed from the tree; after the fix the engine recomputes the same number.

### 3. Module map (KN-09)

```
BAD:   apps/web/src/features/order-tracking/ (9 files) — not named anywhere in ai/modules.md or ai/architecture.md
GOOD:  a feature named in a summary row (`features/*`) · a directory under 5 files
```
**Read the code:** Is the directory a module or a helper folder? Does the map use logical names that differ from directory names? A listed module that is gone is `knowledge-ref-scan` §1. **Finding when** a member module with ≥ 5 tracked files is absent from the map. **Proof:** tier S + V498 — the directory listing beside the map; after the fix the engine is quiet.

### 4. One key, two values (KN-11)

```
BAD:   engine: postgres ×612 (profile, digest, rules) vs mysql ×354 (anchors) · ESLint 9 ×2 vs 10 ×1
GOOD:  ports named per environment (P-9) · the nearest AGENTS.md overriding the root (P-15) · Jest in the API and Vitest in the web app
```
**Read the code:** Which copy loads first for which task? Does a manifest decide it (then the off-truth sites are §1 rows)? **Finding when** two loaded files state different values for one key and neither is history-marked. **Proof:** tier S + V494 — both quotes; after the fix one value remains.

### 5. Derived file vs its source (KN-13)

```
BAD:   ai/_decision-index.md — missing ADR 0034–0040 (40 files in the home)
       177 anchors cite `.claude/codebase-profile.md:19` "MySQL/ULID"; that line now says Postgres/UUIDv7
       ai/_convention-cheatsheet.md "derived against main at 8c50776b" — ai/conventions.md changed in 1 commit since
GOOD:  a derived file whose declared sha has no source commit since · an mtime bump with no content change (P-13)
```
**Read the code:** What generates the file (`apply-anchors.sh`, the curator's index step, the cheatsheet step)? Did the source change after the declared derivation point? **Finding when** the recomputed projection of the source differs from the derived file. **Proof:** tier U + V496 — regenerate from the source twice; the second run is byte-identical (`cmp`, never mtime) and the engine is quiet.

### 6. Citation no longer supports the claim (KN-14)

```
BAD:   `apps/web/src/app/RootRoute.tsx:30` — the file has 24 lines · a cited doc line rewritten to a different engine
GOOD:  the same text two lines lower (±3 window) · a claim that aggregates several spans (R3 trap: Unconfirmed, never a Finding)
```
**Read the code:** Did the code move (repoint the line) or change (re-verify the claim)? Does the claim name typed facts the window contradicts, or only identifiers it does not repeat? **Finding when** the cited line is past the end of the file, or its ±3 window states a different value for a typed key the claim makes. **Proof:** tier S + V497 — the cited window quoted; after the fix it carries the claim.

## Proof

Oracles: [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Learning — V494 (typed-fact diff empty after the fix), V495 (count recomputed), V496 (derived file regenerated twice, byte-identical; 177 copies collapse to one regeneration), V497 (citation window carries the claim), V498 (module map). `knowledge-facts.py . --only=<file>:<line>` fires before the edit and is quiet after it.

## Output

```
knowledge-fact-scan — lockfiles: pnpm-lock.yaml · truth: postgres · mikro-orm · uuidv7/cuid/nanoid · pnpm · node 22 (.nvmrc)
Corpus 478 files (history and sinks excluded)

1. .claude/agents/accessibility-auditor.md:20 (+176 anchors: skills 71, commands 57, agents 49)   [report-with-fix]   high
   §1 KN-07 + §5 KN-13 — "MikroORM (MySQL) with ULID PKs" vs pnpm-lock.yaml @mikro-orm/postgresql 6.6.16, uuidv7 1.2.1;
   the cited `.claude/codebase-profile.md:19` now says Postgres 16 / UUIDv7. One root cause: anchors never regenerated.
   Fix: apply-anchors.sh re-run from the corrected profile (IR-1); regenerate twice, byte-identical. Proof: --only quiet.
2. ai/_decision-index.md:3                                                                       [report-with-fix]   medium
   §2 KN-08 + §5 KN-13 — "every file 0001–0033 has a row"; docs/decisions holds 0001–0040. Fix: regenerate the index.
3. ai/patterns/adr-template.md:36 (+50)                                                           [report-flagged]    low
   §5 KN-13 — cites `.claude/codebase-profile.md:7` for "UUIDv7"; the line carries neither scheme. Claim agrees with the lockfile.

Verification: 14 candidates → 9 findings · 4 unconfirmed · 0 hardening · 0 pre-existing · 1 refuted

Class coverage:
  §1  KN-07 fact vs lockfile     checked (2,155 typed claims → 5 groups, 533 sites)
  §2  KN-08 counts and ranges    checked (17 scoped counts, 1 range → 5)
  §3  KN-09 module map           checked (70 module dirs → 1)
  §4  KN-11 one key two values   checked (3 keys)
  §5  KN-13 derived vs source    checked (index, 177 anchors, 3 derivation points → 6 groups)
  §6  KN-14 citations            checked (2,174 → 52 past EOF, 34 unconfirmed) · Live, unreviewed (34 groups — --expand --classes=6)
  §7  KN-12 one fact, N copies   applied to every row
```

`[report-with-fix]`: both ends are cited and the fix is the lockfile value or a regeneration. `[report-flagged]`: the claim may be right and only the citation off, or the count's set is unclear. The coverage block lists **all seven** classes on every run: `checked (k → m)` when the class ran with a truth source; `N/A (<reason>)` (no lockfile for §1 majors, no module map for §3, no index for §5); `blocked (<reason>)` when the engine or an `rg` exited 2.

## False positives / precedents

The verifier reads [`precedents/learning.md`](../../../../snippets/precedents/learning.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. The ones this skill meets most: § 3 history, § 9 per-environment values, § 10 pack-generic capability lines, § 13 content not mtime, § 14 history-marked facts, § 15 nested precedence, § 17 one fact in N copies, § 27 a citation that resolves but does not support, § 28 counts need their set named.

## When to run

- On any diff that touches a manifest or lockfile, `.nvmrc`/`engines`, compose files, `ai/**`, `CLAUDE.md`, `AGENTS.md`, `.claude/codebase-profile.md`, an ADR, or adds or removes a member directory: the `/audit-knowledge` dispatch signal.
- On every whole-repo `/audit-knowledge`, reporting all seven classes.
- After a major upgrade (`/upgrade-dep`) or a database or id-scheme change: every copy of the old fact is a row.

## Halt conditions

- Do not report a row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§ 10, with [`precedents/learning.md`](../../../../snippets/precedents/learning.md)). Under `/audit-knowledge` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any row without the claim quoted, the truth source named, and the site count.
- Never state a version, engine or count from memory: if the ledger says UNREAD, the class is `N/A (no lockfile)` or `blocked`, never consistent.
- Never hand-edit N derived copies: fix the source and regenerate (tier U). Report one finding with N sites, not N findings.
- Never write into the scanned repository: the engine reads and runs read-only git; output goes under `$RUN`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `scripts/knowledge-facts.py` (this skill): §1–§7, `--only`, `--corpus`, `--expand`, `--classes`, `--self-test`; imports `kn_common.py` from the knowledge-ref-scan skill (its scripts directory) (lockfile readers, ADR home, corpus scope). Stdlib only, `python3 -I` safe; nothing is written under the scanned root.
- `knowledge-ref-scan` (references that do not resolve), `memory-hygiene-scan` (sink entries), `decision-record-scan` (the ADR home and lifecycle), `context-load-scan` (what loads and the oracle's age). `/audit-knowledge` dispatches all five; `/refresh-knowledge --from-audit` closes rows with source-wins edits and regenerations.
- align `convention-oracle` (when installed) owns convention claims; `/setup-project-health` owns provenance markers and approval stamps; `apply-anchors.sh` (Refract) is where the 177-copy class is fixed.
