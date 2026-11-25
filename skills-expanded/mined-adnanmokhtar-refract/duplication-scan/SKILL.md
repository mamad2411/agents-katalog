---
name: duplication-scan
description: Find copies that drifted — clone pairs where a fix reached one copy only, one business rule implemented twice, new clones a change adds — each proved by a divergence test or a new-clones-only run against the merge-base.
kind: skill
pack: code-quality
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: duplication-scan

## Premise

A copy is cheap to make and expensive to keep in step. Juergens, Deissenboeck, Hummel and Wagner
(*Do Code Clones Matter?*, ICSE 2009) studied five systems. In 52 % of the clone groups, the copies
had been changed inconsistently, and 28 % of those inconsistencies were unintentional. Developers
confirmed 107 faults among them: about one in every two or three unintentional inconsistent changes
was a fault. The harm is not the copy. It is the fix that reached one copy and not the other: the
rounding corrected in the API and not in the worker, the limit added to the web form and not to the
import.

So **clone count, clone size and duplication % are triage inputs, never findings**
(`precedents/code-quality.md § 51`). Most clones are harmless (§ 58). Two similar blocks that are
not one rule are the right design, and a shared helper with flag parameters is often worse than the
copy. This skill hunts three things: the **divergent copy** (§1), **one business rule implemented
twice** (§2), and, on a diff, **the clones the change added** (§3). Measured on a real monorepo
(2026-10-05): 1,623 clone pairs. 77 were near-miss pairs and 10 of those had a fix on one side only.
Reading 3 of them found 0 defects: the read step is what makes a finding.

**Every finding cites both copies `<file:start-end>` + the lines that differ + the commit that
changed one side + the input that difference decides + the entry point that reaches the unfixed
copy + the proof + the fix.** "No duplication problems" is never printed without the
class-coverage block (§ Output).

**Two kinds of proof.** A divergent copy or a doubled rule (§1, §2) is a **correctness** claim. The
proof is **divergence**: the input the one-sided fix addressed, run through the unfixed copy, gives
the old wrong answer. Or a differential property test feeds both copies the same generated inputs
with a fixed seed, and the first input where they disagree is the witness. The fix changes
behaviour, so it goes to `/quality-fix`, failing-first. An identical clone (§3) is
**maintainability**. On a diff, the proof is the **new-clones-only run** against the merge-base. A
clone that was there at the base is **Pre-existing** (§ 61). The fix is behaviour-preserving and
goes to `/simplify` or `/refactor`. Both oracles are in
[`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Code quality (*Divergence*,
*Metric ratchet*; variants V85, V86).

## The rule

A divergent copy is a finding when all four hold:

1. **One rule.** Both copies implement the same business rule, which must change together: the same
   inputs, the same purpose, the same spec. Two blocks that only look alike are not one rule (§ 58).
2. **They disagree on an input.** The differing lines change the output for some value. A difference
   in naming, logging, formatting or messages does not count.
3. **The lagging copy is live.** A real entry point reaches it: not a mock, a script or a test
   (gate 1).
4. **The lagging copy is wrong.** The expected answer comes from the fix commit's test, a spec, or a
   documented rule. "They differ" alone is not wrong: a deliberate per-case difference (an exchange
   validates what a cash return does not) is the design.

**On a diff.** When the change fixes one copy and leaves its sibling, the finding belongs to the
diff: that is the sibling sweep every fix owes (the `N_found == N_fixed + N_explained + N_followup` ledger of
[`fix-bug-core.md`](../../../../snippets/fix-bug-core.md)). A new clone is a §3 finding of the diff
only when at least one of its ends is in a changed file. Everything else is Pre-existing.

## Boundaries

- **Every instance of one surface type** (tables, forms, headers, tabs, filters, buttons, the
  validation pipeline) behind one shared implementation → `/unify-surfaces`. A copy that reinvents
  a wrapper or idiom the project already names → `/align`. This skill reports the copy that
  diverged; it does not consolidate surfaces.
- **A copy that nothing reaches** → `dead-code-scan` (this pack); delete it, do not merge it.
- **Copy-paste slips inside one function**: `a.x == b.x && a.y == b.x`, a duplicate `case`, an
  unrenamed identifier in the last of a run of similar lines → `correctness-smell-scan` (this pack).
- **Contract drift between services** → backend `api-snapshot` and testing `contract-test`, when
  those packs are installed. Without them, report it here as a §2 candidate tagged
  `contract-class (owner pack not installed)`.
- **Duplication kept for measured performance** → the performance pack when it is installed (§ 63); without it, Hardening here with the benchmark cited. **Generated code**
  and **test duplication** are excluded (§ 54, § 55).

## Adapt to the codebase — the clone lanes

Read the clone tool the project already runs (grep 0) and its threshold first. The project's
minimum token count beats jscpd's default of 50.

| Lane | Command | Clone types | Traps |
|---|---|---|---|
| **jscpd 5.4.0** (MIT; any of 224 formats; the cross-stack default; installed only — `node_modules/.bin` or PATH, never a download) | `jscpd --max-gap-lines 3 --ignore "<globs>" --fail-on-empty -r json -o <dir> .`; diff lane `--baseline-from-ref <base> --fail-on-new-clones`; type-2 `--ignore-identifiers --ignore-literals`; JS/TS AST near-miss `--similarity 0.85` | exact; `similar` (gap or AST); `renamed` | see the five traps below |
| **PMD CPD 7.28.0** (JVM, C#, Go, Python, Ruby, PHP, Swift…) | `pmd cpd --minimum-tokens 100 --dir src --language java --format xml` (`--ignore-identifiers`, `--ignore-literals`) | exact, renamed | the PMD 7 CLI is `pmd cpd`; PMD 6's `run.sh` is gone |
| **Go** | `dupl -t 100 ./...`; golangci-lint `dupl` (threshold 150) | AST | `if err != nil` boilerplate: raise the threshold, never report it |
| **Python** | pylint 4.1.2: `pylint --disable=all --enable=duplicate-code --min-similarity-lines=6 <pkg>` (R0801) | exact | Ruff has no R0801 |
| **Ruby** | flay 2.14.4: `flay --mass 32 app lib` | AST, near-miss | — |
| **PHP** | jscpd or PMD CPD | — | phpcpd is archived |
| **Offline fallback** (`scripts/clones.py`, this skill; no download) | `CLONES=fallback` in step 1, or automatic when jscpd is not installed or fails; `--self-test` | exact; `similar` (gap ≤ 3 lines) | type-1 only (no renamed copies); boilerplate windows shared by > 40 places are skipped and counted |
| **Type-4 (semantic)** | jscpd `--semantic` (experimental; downloads a 548 MB model, or calls an embeddings API you name) | semantic | a candidate generator for §2 only, never a required lane |

The jscpd traps, measured on 5.4.0 on 2026-10-05:

1. **An empty scan exits 0** and prints a clean report, unless `--fail-on-empty` is set.
2. **`-a` (absolute paths) makes `--ignore` match the whole path.** A checkout under any folder named
   like an ignore entry (`fixtures/`, `build/`, `test/`) scans 0 files. `--fail-on-empty` catches it.
3. **The `--baseline-from-ref` scan sees the base tree's full paths.** Run from the repository
   root. From a subfolder whose ancestors match an ignore entry, the base scan is empty and every
   clone reads as new. The `neither` count of grep 3 is the tell.
4. **`--ignore` is one comma-separated list**, so a `{a,b}` brace glob breaks it. Give one glob per
   entry.
5. **jscpd 4 config keys differ.** Review an old `.jscpd.json` before trusting it. The base scan
   needs the full history in CI (`fetch-depth: 0`).

Versions are from the code-quality research catalog (2026-10-05). The jscpd flags and traps were
run against 5.4.0 on that date. A lane that errors is `blocked`, never a quiet lane.

## Pre-flight greps

Run as **one** script from the **repository root** (shell state does not survive between tool
calls). Step **N** feeds detector **§N**; step 0 is context. Every `rg` names its path (`.`): `rg`
given no path reads stdin whenever stdin is a pipe, and under an agent's shell that is a silent
zero-hit run. Any `rg` error on stderr (exit 2) is a failed grep, never zero hits. Set `BASE` for a
diff run. On a whole-repo run with no merge-base, step 3 prints `N/A`.

```bash
D="${TMPDIR:-/tmp}/duplication-scan"; rm -rf "$D"; mkdir -p "$D"
BASE="${BASE:-$(git merge-base origin/main HEAD 2>/dev/null)}"   # empty on a whole-repo run with no remote: §3 diff lane is N/A
# jscpd's --ignore is one comma-separated list, so no {a,b} braces: one glob per entry.
IGN='**/node_modules/**,**/vendor/**,**/dist/**,**/build/**,**/.next/**,**/target/**,**/.venv/**,**/*.min.*,**/*.d.ts,**/test/**,**/tests/**,**/__tests__/**,**/spec/**,**/e2e/**,**/__mocks__/**,**/mocks/**,**/fixtures/**,**/testdata/**,**/stories/**,**/migrations/**,**/seeds/**,**/generated/**,**/__generated__/**,**/locales/**,**/i18n/**,**/*.spec.*,**/*.test.*,**/*.test-data.*,**/*.fixture.*,**/*.e2e-spec.*,**/*.stories.*,**/*_test.*,**/test_*.py,**/scripts/**,**/docs/**,**/ai/**,**/*.md,**/*.json,**/*.lock,**/*.yml,**/*.yaml,**/*.sql,**/*.svg,**/*.html'
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/*.d.ts' -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,testdata,stories,migrations,seeds,generated,__generated__,locales,i18n,scripts}/**'
   -g '!**/*.{spec,test,e2e-spec,mock,stories,test-data,fixture,fixtures}.*' -g '!**/{*_test,test_*,conftest}.*' -g '!docs/**' -g '!ai/**')
for t in ts js py go java kotlin cs rust php ruby; do printf '%-7s %s\n' "$t" "$(rg --files -t "$t" "${X[@]}" . | wc -l)"; done   # 0 = lane absent
# 0. Context: a clone tool the project already runs (it owns §3 at its own threshold, which beats jscpd's 50-token default).
rg --files -g '{.jscpd.json,.jscpd.yml,cpd.xml}' -g '!**/node_modules/**' . ; rg -n --pcre2 '\bjscpd\b|\bpmd\s+cpd\b|\bdupl\b|duplicate-code|\bR0801\b|\bflay\b' -g '{package.json,pyproject.toml,setup.cfg,.pylintrc,pylintrc,.golangci.y*ml,Makefile,*.gradle*,pom.xml,Gemfile}' -g '!**/node_modules/**' .
# 1. Every clone pair, exact and near-miss (--max-gap-lines 3 merges copies that differ by up to 3 lines: kind "similar").
#    --fail-on-empty makes a mis-globbed scan exit 1 instead of printing a clean report. Never add -a: with absolute paths
#    jscpd 5.4 matches --ignore against the whole path, and a checkout under any folder named fixtures/ or build/ scans 0 files.
#    jscpd runs only when already installed (the project's node_modules/.bin, then PATH) — an audit never downloads it.
#    Not installed, CLONES=fallback, or jscpd failed: the shipped token-window finder writes the same report shape
#    (type-1 only: renamed copies are not found). It is a lane, so its line is printed.
CL=.claude/skills/duplication-scan/scripts/clones.py; [ -f "$CL" ] || CL="$HOME/.claude/skills/duplication-scan/scripts/clones.py"; mkdir -p "$D/all"
JSCPD="$( { [ -x node_modules/.bin/jscpd ] && echo node_modules/.bin/jscpd; } || command -v jscpd || true)"
[ -n "$JSCPD" ] || { echo "§1 jscpd NOT-RUN (jscpd not installed — to enable: npm i -D jscpd@5)"; CLONES="${CLONES:-not installed}"; }
{ [ -z "${CLONES:-}" ] && "$JSCPD" --max-gap-lines 3 --ignore "$IGN" --fail-on-empty -r json -o "$D/all" --no-colors . > "$D/all.log" 2>&1; } \
  || { echo "§1 jscpd ${CLONES:-blocked — $(tail -1 "$D/all.log" 2>/dev/null)} → clones.py"; rg --files -t ts -t js -t py -t go -t java -t kotlin -t cs -t php -t ruby "${X[@]}" . > "$D/files.txt"
       [ -f "$CL" ] && python3 -B "$CL" . "$D/files.txt" "$D/all/jscpd-report.json" || echo "§1 blocked — jscpd unavailable and clones.py absent"; }
# 1b. Divergence: a near-miss pair where one copy took a fix commit the other never got. The commit counts when its subject
#     is a fix (conventional type or "fixes #n"), it is newer than the other copy, and it touched <= 30 files (not a sweep).
#     Exact pairs are skipped: copies identical today have not diverged inside the matched range. A one-sided fix wider than
#     30 files is printed WIDE? (a sweep, or the only real fix), never dropped. A copy whose line history starts at the repo's
#     root commit is history-blind: a re-rooted, squashed or shallow history hides every fix made before it.
[ -f "$D/all/jscpd-report.json" ] && python3 - "$D/all/jscpd-report.json" <<'PY'
import json,os,re,subprocess,sys,collections
d=json.load(open(sys.argv[1]))['duplicates']
FIX=re.compile(r'^(?:fix|hotfix|bugfix|revert)\b|\b(?:fixes|closes|resolves)\s+#\d+',re.I)
git=lambda *a: subprocess.run(['git',*a],capture_output=True,text=True).stdout
width=lambda h: len(git('show','--format=','--name-only',h).split())
ROOTS=set(git('rev-list','--max-parents=0','HEAD').split()); RD=git('log','-1','--format=%cs',*sorted(ROOTS)[:1]).strip() if ROOTS else '?'
def hist(f,s,e): return [l.split('\t',2) for l in git('log','--no-patch','--format=%H\t%ct\t%s','-L',f'{s},{e}:{f}').splitlines() if l.count('\t')>=2 and len(l.split('\t')[0])==40]
def only(h,o): born=min(int(c[1]) for c in o); oh={c[0] for c in o}; return [c for c in h if c[0] not in oh and FIX.search(c[2]) and int(c[1])>born]
print('pairs',len(d),dict(collections.Counter(x['kind'] for x in d)),'cross-file',sum(x['firstFile']['name']!=x['secondFile']['name'] for x in d))
n=blind=0
for x in d:
    if x['kind']=='exact': continue
    a,b=[(os.path.normpath(y['name']),y['start'],y['end']) for y in (x['firstFile'],x['secondFile'])]
    ha,hb=hist(*a),hist(*b); n+=1
    if (ha and ha[-1][0] in ROOTS) or (hb and hb[-1][0] in ROOTS): blind+=1
    if not ha or not hb: continue
    fa,fb=only(ha,hb),only(hb,ha)
    if bool(fa)!=bool(fb):
        fx,(p,q)=(fa,(a,b)) if fa else (fb,(b,a)); nar=[c for c in fx if width(c[0])<=30]; c=(nar or fx)[0]
        print(f"{'DIVERGENT?' if nar else 'WIDE?'} {p[0]}:{p[1]}-{p[2]} fixed by {c[0][:9]} \"{c[2][:90]}\"{'' if nar else f' ({width(c[0])} files: a sweep, or the only fix — read it)'} | not in {q[0]}:{q[1]}-{q[2]} (similarity {x.get('similarity')})")
print(f'history-blind {blind}/{n} near-miss pairs (a copy reaching back to the root commit, {RD})')
if n and 2*blind>n: print(f'§1 partial — history-blind {blind}/{n}: 1b cannot see fixes before {RD}; read every near-miss pair side by side (pair diff), never report "0 divergent"')
PY
# 2. One business rule implemented twice: a domain-verb function defined under the same name in two top-level areas
#    (server and client, two services). Read both bodies.
V='(?:[a-z]\w*)?(?:[Cc]alc|[Cc]ompute|[Pp]rice|[Pp]ricing|[Rr]ound|[Pp]rorat|[Tt]ax|[Ff]ee|[Cc]ommission|[Dd]iscount|[Tt]otal|[Aa]mount|[Bb]alance|[Rr]efund|[Cc]harge|[Cc]onvert|[Nn]ormali[sz]e|[Vv]alidate|[Ee]ligib|[Ss]ettle|[Pp]ayout|[Qq]uota|[Ll]imit|[Bb]ucket|[Tt]ransition|[Ss]core|[Cc]losed|[Aa]llowed|[Ss]tatusOf|[Cc]ountKey|[Ee]ffective)\w*'
#    Stop-list: a bare verb or noun (`validate`, `settle`, `price`, `round1`, `invalidate`, `statusOf`) is a homonym, not a rule (9 of 16 names on a real monorepo).
rg -n -o --pcre2 '^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?(?:function\s*\*?\s+|def\s+|func\s+(?:\([^)]*\)\s*)?)\K'"$V"'(?=\s*[(<\[])|^\s*(?:export\s+)?const\s+\K'"$V"'(?=\s*(?::[^=\n]+)?=\s*(?:async\s*)?(?:\([^)\n]*\)|\w+)\s*(?::[^=\n]+)?=>)|^\s+(?:(?:public|private|protected|static|async|override|internal)\s+)*\K'"$V"'(?=\s*\([^)\n]*\)\s*(?::\s*[^{\n]+)?\{\s*$)' -t ts -t js -t py -t go -t java -t kotlin -t cs -t php -t ruby "${X[@]}" . \
 | awk -F: '{ n=split($1,p,"/"); area=p[2]"/"p[3]; k=$3; if (tolower(k) ~ /^(in)?(calc|calculate|compute|price[ds]?|pricing|round[0-9]*|tax|fee|commission|discount|total|amount|balance|refund|charge|convert|normali[sz]e|validate|eligib[a-z]*|settled?|payout|quota|limit|bucket|transition|score|closed|allowed|effective)s?$|^(amount|status|price|total|count)of$/) next; if (!((k,area) in seen)) { seen[k,area]=1; c[k]++; at[k]=at[k]" "$1":"$2 } } END { for (k in c) if (c[k]>1) print c[k], k, at[k] }' | sort -rn
# 2b. A rule copied as a WHOLE FILE escapes grep 2's names: one file stem (`perf-scoring`, `settlement-day.rules` ~ `settlement-day`) in two
#     top-level areas (apps/api vs apps/web, server vs client). Glue files (`x.api.ts`, `x.schema.ts`, `x.controller.ts`) and generic stems are
#     skipped: only a plain stem or a rule-ish suffix pairs. Read both files; agreeing copies are Hardening (they will drift), not findings.
rg --files -t ts -t js -t py -t go -t java -t kotlin -t cs -t php -t ruby "${X[@]}" . | awk -F/ '{ f=$NF; sub(/\.[^.]*$/,"",f); k=split(f,q,"."); g=q[1]; x=(k>1?q[2]:""); area=$2"/"$3
  if (k>2 || (x!="" && x !~ /^(rules?|polic(y|ies)|logic|calc|utils?|helpers?|domain|model|vocab|machine|mappers?|assemblers?|format)$/)) next
  if (tolower(g) ~ /^(mainactivity|mainapplication|appdelegate|gradle|index|main|app|types?|utils?|helpers?|constants?|config|schemas?|errors?|api|client|server|module|routes?|router|registry|hooks?|store|service|controller|models?|mappers?|contracts?|dto|entit(y|ies)|enums?|common|shared|lib|csv|money|logger|http|quer(y|ies)|keys|i18n|setup|env|vocab|phone|format|labels?|columns|fixtures?|mocks?)$/) next
  if (!((g,area) in s)) { s[g,area]=1; c[g]++; at[g]=at[g]" "$0 } } END { for (g in c) if (c[g]>1) print c[g], g, at[g] }' | sort -rn
# 3. Diff lane: clones the change added (absent from the merge-base tree), and how many of their ends the diff touched.
#    Exit 1 from --fail-on-new-clones is the signal; "analyzed no files" in the log is a blocked scan.
if [ -n "$BASE" ] && [ -z "$JSCPD" ]; then echo "§3 diff lane NOT-RUN (jscpd not installed — to enable: npm i -D jscpd@5)"
elif [ -n "$BASE" ]; then
  "$JSCPD" --ignore "$IGN" --baseline-from-ref "$BASE" --fail-on-new-clones --fail-on-empty -r json -o "$D/new" --no-colors . > "$D/new.log" 2>&1
  rg -q 'analyzed no files' "$D/new.log" && echo "§3 blocked — $(tail -1 "$D/new.log")"
  git diff --name-only --diff-filter=AMR "$BASE"...HEAD > "$D/changed.txt"
  [ -f "$D/new/jscpd-report.json" ] && python3 - "$D/new/jscpd-report.json" "$D/changed.txt" <<'PY'
import json,os,sys
ch={l.strip() for l in open(sys.argv[2])}; new=[x for x in json.load(open(sys.argv[1]))['duplicates'] if x.get('isNew')]
ends=lambda x: sum(os.path.normpath(x[k]['name']) in ch for k in ('firstFile','secondFile'))
print('new clones',len(new),'both ends in diff',sum(ends(x)==2 for x in new),'one end',sum(ends(x)==1 for x in new),'neither',sum(ends(x)==0 for x in new))
for x in new: print('NEW', x['tokens'], f"{os.path.normpath(x['firstFile']['name'])}:{x['firstFile']['start']}", f"{os.path.normpath(x['secondFile']['name'])}:{x['secondFile']['start']}")
PY
else echo "§3 diff lane: N/A (no merge-base; whole-repo run)"; fi
```

A candidate is a hit **plus** both copies read side by side **plus** the history of each **plus**
the hops to an entry point. Three blind spots are structural:

- **A fix that broke the match.** When one copy's fix rewrote more than 3 lines, jscpd reports two
  shorter exact clones around it, or none at all. For a pair you suspect, re-run with
  `--max-gap-lines 10` on those two files, and use `git log -S '<the fixed token>' --oneline -- <both paths>`.
- **A fix whose subject does not say so.** Squash merges, `chore:` or `refactor:` commits that
  change behaviour, and repos without a commit convention all escape 1b's filter. On such a repo,
  read every near-miss pair whose two sides have different last commits.
- **The same rule under two names** (`prorate` / `proRata`, `fee` / `commission`) escapes grep 2.
  Read the domain glossary (`ai/` docs, the money and quota modules). jscpd `--similarity 0.85`
  (JS / TS function AST) or `--semantic` will propose pairs; read each one. A rule copied as a
  whole file under the same stem is step 2b's.
- **A history that starts recently.** A re-rooted, squashed or shallow history puts every copy's
  birth at one commit, and 1b then sees no one-sided fix at all. 1b prints `history-blind k/n`;
  above half, §1 is `partial` (§ 91) and every near-miss pair is read side by side
  (`diff <(sed -n a,bp f1) <(sed -n c,dp f2)`), never reported as "0 divergent".
- **Gate 1 shortcut.** A project that commits an export-liveness ledger (a JSON of exports only
  tests import, such as an `every-export-is-imported.json` with a `testOnly` list, enforced by a
  test) already answers "is the lagging copy live?": read it before walking callers.

**Measured** (2026-10-05). On a real NestJS-on-Fastify + MikroORM + React monorepo (about 14,200
tracked files; the script runs in about 5 s without step 3), step 1 found 1,623 pairs: 1,546 exact
and 77 near-miss, 1,181 of them across files. Step 1b returned 10 candidates. A naive version that
kept exact pairs and any commit whose subject contained "fix" returned 311; exact copies that are
identical today cannot have diverged inside the range, which is why 1b skips them. 3 of the 10 were
read, and none was a defect. Two billing ports looked alike but read different totals for different
purposes (§ 58). An exchange and a cash-return use case differ on deliberate per-case validation.
Two order queries: the sibling had taken the same fix in another form. Step 2 returned 13 names
defined in both the API and the web app. 3 were read. A client import validator mirrors the
server's, with a test that asserts both agree (§ 46). A settlement-closure rule **has diverged**:
the server closes a cancelled order and treats a partial delivery like a rejection, and the client
copy does neither. But the client copy is imported only by a mock and its test, so gate 1 fails:
Hardening, plus a `dead-code-scan` item. The rest are name collisions (`validate`, `settle`,
`price`). Step 3, on a scratch clone 40 commits back (232 changed files), found 20 new clones: 15
with both ends in the diff, 5 with one, 0 with neither. Fixtures: `web-dashboard` 3 exact pairs and
`review-decoys` 2 (its base and change snapshots of one file); every other fixture has 0. Step 3 run
from inside a fixture folder reported every clone as new, with `neither` equal to the total: trap 3.
**Re-measured 2026-10-15** on the same monorepo, read-only and offline (`CLONES=fallback`, about
15 s): `clones.py` 1,214 pairs (1,178 exact, 36 similar), 2.94 % duplicated lines; 1b printed
`history-blind 35/36` (the history had been re-rooted three days earlier, so §1 is `partial`) and
one `WIDE?` row, a 172-file fix that reached the web copy of a carrier problem-code table and not
the API's — the old 30-file filter had dropped the only one-sided fix. Step 2 16 → 10 names after
the stop-list and the `*.test-data.*` exclusion, with the settlement-closure and import-row pairs
kept. Step 2b 24 stem pairs, among them a permission tree copied whole into the web app and live
there, and four rule files the late reader confirmed as copies (scoring, rescue rules, settlement
day, module access). Fixtures with the fallback: `quality-mix` step 2 lists both seeded rules
(`prorate`, `computeTax`) and one decoy; `web-dashboard` 3 exact pairs, `review-decoys` 3.

## The 3,000-hit path

A large repo has thousands of exact pairs. They are §3 material, and §3 on a whole repo is
Hardening. Never read them one by one:

1. **Exact pairs on a whole repo** go to one Hardening line with the count and the duplicated-lines
   %. On a diff, only step 3's new clones with an end in the diff are read.
2. **Near-miss pairs** (`similar`) are the divergence pool: usually tens. Run 1b on all of them.
3. **Rank 1b's candidates by risk surface**: money, authorization, tenancy, quota, persisted data,
   external contracts first, from the context map.
4. **Read the top 30** with §1's questions. Read all of step 2's names on money and validation
   paths.
5. **Prefer the differential test as the bulk oracle** for a group of copies of one rule: one
   property test over every copy settles the whole group.
6. **Ledger the rest** as `Live, unreviewed (k groups / n pairs)` with the command that continues
   them. Never `checked`.

## Scans for

| § | Class | Default severity |
|---|---|---|
| 1 | Divergent copies: a fix reached one copy only | medium; high when the lagging copy is on a money, authorization, tenancy or data-write path and the divergence test fails |
| 2 | One business rule implemented twice (server and client, API and worker, two services) | medium when the differential test disagrees on a live path; high on money; Hardening when the copies agree or one copy is unreachable |
| 3 | Clones a change added (identical or renamed) | low on a diff when a new clone has an end in a changed file, medium past 3 copies; Pre-existing otherwise; whole repo: Hardening with the count |

### 1. Divergent copies

```
BAD:   orders/pricing.ts:40-58        rounds half-even since "fix: invoice totals off by a cent" (a1b2c3d)
       worker/invoice-batch.ts:12-30  the same block, still Math.round — nightly invoices keep the old cent
GOOD:  one rounding function both call; or the fix applied to both, with the fix commit's test run against each
```
**Read the code:** Put the two ranges side by side (`diff <(sed -n 40,58p a) <(sed -n 12,30p b)`).
Which lines differ, and does each difference change an output? Read the fix commit (`git show
<sha>`): what input did it address, and what test did it add? Is the lagging copy the same rule:
the same inputs, purpose and spec? Or is it a different case on purpose? Does a real entry point
reach the lagging copy? Did the sibling take the same fix in another form (a bound, a guard, a
shared helper called elsewhere)? **Finding when** the input the fix addressed still produces the
old answer through the lagging copy, on a live path. **Proof:** divergence — the fix commit's test,
or its input, pointed at the lagging copy's entry point fails. Or a property test over both copies
with a fixed seed, where the first differing input is the witness.

### 2. One business rule implemented twice

```
BAD:   api/settlement.rules.ts   isClosed: cancelled → true; partial delivery → supplied && returned
       web/settlement.ts         isClosed: rejected → returned && supplied; else supplied   // the board shows "closed" early
GOOD:  one implementation the client receives (from the API, or a shared package both import);
       or both copies generated from one schema, or a test asserting they agree (§ 46)
```
**Read the code:** Is it really one rule, the same name and the same domain meaning? Or a name
collision (`validate`, `settle`, `price`)? Is one copy generated from the other, or held to it by
an agreement test (§ 46)? Is each copy reachable: not only a mock, a story or a test (a copy only its own test imports is
`dead-code-scan`'s, § 90)? Which copy
is right? Use the spec, the domain docs, or the copy the data actually flows through. **Finding
when** the differential test disagrees on an input the live path receives. **Proof:** divergence —
a property test feeding both copies the same generated inputs (`fc.assert(fc.property(arb, x =>
expect(apiRule(x)).toEqual(webRule(x))), { seed: 42, numRuns: 1000 })`) fails, with the witness
recorded.

### 3. Clones a change added

```
BAD:   the diff pastes a 70-token query builder from wallets/queries.ts into orders/finance.port.ts
GOOD:  the diff calls the existing builder, or extracts it once both callers are in the diff
```
**Read the code:** Does step 3 report the clone as new, with an end in a changed file? Is it the
same rule, which will need the same next change (a finding), or two similar blocks that will evolve
apart (§ 58)? Is it test, generated or migration code (§ 54, § 55)? Is a canonical helper already
in the repo? Then `/align` owns the fix. **Finding when** the change added a clone of one rule on
changed code. **Proof:** the new-clones-only run — `jscpd --baseline-from-ref "$BASE"
--fail-on-new-clones` exits 1 with the clone listed, and it exits 0 after the fix with the
duplicated-lines % no higher than at the base (V86). Nothing is gamed: no ignore glob added and no
threshold raised (*Metric ratchet*).

## Proof

The oracles, the shapes and the variants are in
[`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Code quality (*Divergence*,
*Metric ratchet*; V85, V86). §1 and §2 fixes change behaviour on purpose: one copy now answers
differently. So they are failing-first through `/quality-fix`: the divergence test fails, then the
copies are reconciled (one implementation, or the fix applied to each), then every copy passes V85.
§3 fixes are behaviour-preserving: pin first (`test-shield`, this pack), extract or reuse, then
the new-clones run exits 0. **Never a fix:** merging two copies that are different rules behind a
flag parameter (§ 58), adding the clone to an ignore list or a baseline file, or raising
`--min-tokens`.

## Output

```
duplication-scan — lanes: jscpd 5.4.0 (ts, tsx, js; --max-gap-lines 3; project min-tokens none → default 50); pmd cpd, dupl, pylint, flay absent
Context: no clone tool in CI · BASE = merge-base origin/main (232 changed files)

Findings: 1 · Unconfirmed: 1

1. worker/src/invoices/batch-totals.ts:12-30  ↔  api/src/orders/pricing.ts:40-58     [report-with-fix]   high
   §1 divergent copy — a1b2c3d "fix: invoice totals off by a cent" moved pricing.ts to half-even;
   the worker copy still uses Math.round. Proof: test/invoices/batch-rounding.spec.ts — 10.125 → 10.13
   from the worker, 10.12 from the API (fails). Fix (/quality-fix): the worker calls roundMinor().

2. web/src/reports/settlement.ts:160  ↔  api/src/reports/settlement.rules.ts:168      [report-flagged]    medium
   §2 rule twice — the copies disagree on cancelled and partial orders. Unproven link: whether a live
   screen reads the web copy (only a mock imports it). Settling step: dead-code-scan §1 on the web copy.

Verification: 23 candidates → 1 finding · 1 unconfirmed · 1 hardening · 0 pre-existing · 20 refuted

Class coverage:
  §1  divergent copies        checked (77 near-miss pairs → 10 one-sided fixes → 1 finding) · Live, unreviewed (6 candidates — continue with step 1b's list from line 5)
  §2  rule implemented twice  checked (13 names → 1 unconfirmed; 2 agree by test (§ 46); 10 name collisions)
  §3  clones a change added   checked (20 new clones; 15 both ends, 5 one end → 0 findings: two-block copies (§ 58)) · whole repo: Hardening (1,546 exact pairs, 2.9 % duplicated lines)
```

`[report-with-fix]`: both copies cited, the fix commit read, the divergence test failed, and the
fix reconciles the copies. `[report-flagged]`: one link is unproven, such as reachability, which
copy is right, or a missing harness. It is named with the settling step. The coverage block lists
**all three** classes on every run: `checked (k → m findings)` only when the lane ran;
`N/A (<reason>)` only when the repo has no such surface (no merge-base for §3 on a whole-repo run);
`blocked (<reason>)` when jscpd scanned no files or a grep failed. A partial review reads
`Live, unreviewed (k groups / n pairs)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/code-quality.md`](../../../../snippets/precedents/code-quality.md)
(maintainability § 51–70; client and server validation § 46) and
[`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4, § 5, § 6 and § 10.
The ones this skill meets most:

- **Two similar blocks that are not one rule** (§ 58): bounded contexts evolve apart on purpose.
  Rule of three: two copies are not yet a §3 finding unless they are one rule.
- **Client and server validation** generated from one schema, or held by an agreement test (§ 46).
- **Generated code** (§ 54) and **DAMP tests** (§ 55) are excluded. A copy-pasted stale assertion is
  still a correctness candidate for the testing pack.
- **Table-driven code** (§ 53) and **duplication kept for measured performance** (§ 63).
- **A metric alone** (§ 51): a duplicated-lines % or a clone size is never a finding.

## When to run

- On any diff that fixes a bug: the sibling sweep. Run step 1b and step 2 for the fixed function's
  name, and step 3 for what the diff pasted. This is the `/review-changes` and `/quality-audit` signal,
  and backend's `/fix-bug` sibling sweep when that pack is installed.
- On every whole-repo `/quality-audit`, reporting all three classes.
- When an incident is "it was fixed, but it still happens from the other screen, worker or
  service".

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/quality-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any §1 or §2 finding without both copies cited, the differing lines named, the input that decides them, and the divergence proof or its settling test.
- Do not report a clone count, a clone size or a duplication % as a finding. On a diff, do not report a clone the merge-base already had: that is Pre-existing.
- Do not print a clean verdict from a scan that analyzed no files, or from step 3 when `neither` equals the total (trap 3). Both are `blocked`.
- Do not propose merging copies that are different rules behind a flag parameter, or silencing a clone with an ignore glob, a baseline entry or a higher `--min-tokens`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `/quality-audit` dispatches this skill and folds its coverage block into the class ledger; `/quality-fix` reconciles §1 and §2 failing-first; `/simplify` and `/refactor` remove §3 clones, pinned first.
- `dead-code-scan` (this pack) owns copies nothing reaches; `correctness-smell-scan` (this pack) owns copy-paste slips inside one function; `/align` owns copies of an idiom the project already names; `/unify-surfaces` owns surface-type consolidation.
- `rules/engineering-principles.md` (this pack) states "extend over duplicate": a fork needs a named invariant that split the two cases. §1 and §2 are its executor, and that invariant is what clears a pair under § 58.

Tool versions and traps come from the code-quality research catalog for this pack (2026-10-05) and from runs of jscpd 5.4.0 on that date. Juergens et al. (ICSE 2009, arXiv 1701.05472): numbers only, read from the full text for that catalog.
