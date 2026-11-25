---
name: architectural-diagnosis
description: "Project-wide architecture diagnosis, /optimize Phase 0: import-graph lanes per stack, cycles, layer and boundary violations against the declared architecture, coupling, god and bottleneck modules, churn × complexity hotspots, all ranked against the repo's own distribution."
kind: skill
pack: code-quality
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: architectural-diagnosis

## Purpose

Produce the module-level picture **before any optimisation fix lands**: the foundation fixes whose closure dissolves tactical findings. `/optimize` dispatches it first (Phase 0) and applies its findings in Phase 1. The graph comes from a **tool lane**, never from reading: a graph built by eye misses aliases, re-exports and type-only edges.

**A metric is never a finding** (`precedents/code-quality.md § 51`). Fan-in, fan-out, LOC, instability and complexity are triage inputs, cut at **this repo's own percentiles** unless the project configures a value (`THR-COMPLEXITY`, `THR-FN-LEN` in `templates/governance/thresholds.json`; the percentile cut-offs below — fan-in, fan-out and LOC at p99, churn at p95, complexity at p90, SDP ΔI 0.25 — are `THR-ARCH-RELATIVE`). The fixed cut-offs this skill used to print (in-degree ≥ 30, outward imports ≥ 30, ≥ 500 LOC) flagged 458 files on a real monorepo, mostly its shared kernel and composition roots. A finding needs impact evidence: a **declared** rule broken, a runtime cycle with init-order impact or across declared boundaries, a hotspot with fix history. Standard: the **ISO/IEC 5055:2021 maintainability measure**, weaknesses named in prose (the CWE entries behind it are Prohibited for mapping; never cite their ids).

**Every finding cites `<path:line>` + the number against the repo cut-off or the declared rule (`file:line`) + the impact evidence + the closure verb + the cascade.**

## The rule

A structural candidate is a finding when all four hold:

1. **It breaks something declared or measured:** a conformance config, an `ai/modules.md` boundary line, `ai/architecture.md`, an ADR, or a repo cut-off. A rule in prose only makes the row **Advisory**; its fix proposes the rule file.
2. **No running control owns it** (gate 4): a conformance tool at error in CI owns its class, and the finding, if any, is that the tool is off, at warn, unrun or wrong (trap 4).
3. **It has impact evidence** (per detector). Without it: Hardening.
4. **On a diff, it is worse than the merge-base on changed code**; otherwise **Pre-existing** (§ 61).

## Boundaries

- Clones, one rule implemented twice → `duplication-scan`; swallowed errors → `error-handling-scan`; dead modules → `dead-code-scan`; function-level fingerprints → `refactoring-sweep` (all this pack).
- Workspace design across packages → `@monorepo-architect` (this pack). Rendering the graph → `diagram-sync` (documentation pack, when installed; without it nothing renders the graph).
- `/setup-project --refine` uses the learning pack's `extract-architecture-deeply`: it maps, this grades.

## When to use

- `/optimize` Phase 0 every run (`--diagnose-only`: artifact only); `/audit`'s architecture axis; `/quality-audit`; a diff that adds a module, a cross-module import or a dependency on a hotspot.
- Not for per-feature work: `/add-feature` and `/fix-bug` own their scope.

## Inputs (precise contract)

| Input | Source | Required |
|---|---|---|
| Root, `PROJECT_KIND` | orchestrator · `_extracted-codebase.md § Gold standards` | YES |
| Declared layers and boundaries | conformance configs (step 0a) · `ai/modules.md` rule lines (0c) · `ai/architecture.md` · `_extracted-idioms.md § Layers` · ADRs | NO — without them §1 runs default rules as candidates, with a WARN |
| Modules | `ai/modules.md` catalog paths · else the deepest `modules/ features/ apps/ packages/ internal/ src/` segment | YES (auto) |
| `BASE`, scope | caller (`git merge-base origin/main HEAD`; `--scope=orders`) | diff runs / NO |

## Adapt to the codebase — the lanes

Run the project's own tool first. Versions: code-quality research catalog, 2026-10-05.

| Stack | Graph + cycles | Declared boundaries (§1) | Complexity (§9) |
|---|---|---|---|
| TS / JS | **dependency-cruiser 18.5.0** (`--metrics`: Ca / Ce / I; `moreUnstable` = SDP); madge 8.0.0 `--circular` (slow-moving); knip `--include cycles` | dep-cruiser `forbidden` (`--baseline-mode shrink-only`); eslint-plugin-boundaries 7.2.0 `boundaries/dependencies`; `no-restricted-imports` / import-x `no-restricted-paths`; `@nx/enforce-module-boundaries`; Sheriff; the module-boundaries hook | ESLint `complexity`; lizard |
| Python | Refract graph; `pydeps --show-cycles` | import-linter 2.15 `lint-imports` (`layers`, `forbidden`, `independence`); Tach 0.35.2 (maintenance unconfirmed: prefer import-linter) | Ruff `C901`; radon (stagnant, reporting only) |
| Go | `go list` (package cycles do not compile: §2 N/A) | go-arch-lint 1.19.0; depguard; `internal/` | `gocyclo -over`, `gocognit -over` |
| JVM · .NET | ArchUnit 1.5.1 `slices().should().beFreeOfCycles()`; jdeps · ArchUnitNET 0.13.4 | ArchUnit `layeredArchitecture()`, `FreezingArchRule`; Konsist · ArchUnitNET (NetArchTest is stagnant) | PMD 7.28; detekt · CA1502 / CA1506 |
| Ruby · PHP · Rust | packwerk 3.3.1 · deptrac 4.7.2 · `cargo modules dependencies --lib --acyclic` | `bin/packwerk check` · `deptrac analyse` · crate split | RuboCop `Metrics/*` · PHPMD 3.0.0 · clippy |
| any | — | — | **lizard 1.24.0** `--csv` (30+ languages) |

**Traps, measured 2026-10-05.** (1) dependency-cruiser 18.5.0 refuses Node 23 (`^22||^24||>=26`): the script then prints §2 `blocked` for that root, never `0 cycles`, and lists the Refract graph's strongly connected components as candidates. (2) `--ts-config apps/x/tsconfig.json` from the repo root cannot read its `extends` (TS5083): run from the tsconfig's directory. (3) `dependencyTypesNot: ['type-only']` on `to` alone still reported 4 cycles closing through an `import type`; adding `viaOnly` with the same filter gave 0. (4) One specifier imported as a value **and** re-exported as a type gives two entries: an edge is type-only only when every entry is. A home-grown cycle gate that erased by specifier text missed a 12-file runtime cycle that dependency-cruiser reported. (5) The Refract graph (`~/.claude/scripts/build-graph.py --corpus=project`, built by `rank-source-files.py`) reads every tsconfig's `paths`/`baseUrl` scoped to its own directory, each workspace package's `exports` mapped back to source through its outDir → rootDir, and labels every edge value / `type` / `dynamic` per statement (an edge is type-only only when every statement behind it is). Measured 2026-10-15 on a real NestJS + React monorepo: 0 → 1 alias rule and 3 workspace packages read, 21,101 → 8,543 unresolved (8,221 external packages, 204 assets, 118 local: template strings in a scaffold script and test-only targets), 1 → 2,007 edges into the contracts package; 0 value cycles and 28 type-only SCCs (largest 40), as a hand-built value-edge checker found. Its cycles are value cycles over **resolved** edges; it still cannot read JS-declared aliases (it names the file) and has no `moreUnstable`, so it stays the fallback lane for TS/JS. (6) **Read-only target** (an audit that must not write the checkout): the build-graph cache defaults to `<repo>/.claude/_graph.json`, so the pre-flight passes `--no-cache`; set `RO=1` and dependency-cruiser runs from `$D` against a wrapper `rank-source-files.py --ts-wrapper <root>` prints (absolute `baseUrl` and `paths`, workspace packages mapped to source, no `extends`). A wrapper that only `extends` the app's tsconfig resolved 0 of 10,314 aliased imports; the absolute one gave 7,240 files and 39,313 edges (2026-10-15).

## Pre-flight (one script)

Run from the repository root (shell state does not survive between calls). Step **N** feeds §**N**; step 0 is context. Every `rg` names its path: given none, `rg` reads stdin when stdin is a pipe, a silent zero-hit run. A `blocked` line is `blocked` in the coverage block, never zero. `RULES='domain:infrastructure;…'` replaces the default layer rules with the declared ones.

```bash
D="${TMPDIR:-/tmp}/arch-diag"; rm -rf "$D"; mkdir -p "$D"
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,target,.next,.venv,coverage}/**' -g '!**/*.{min.js,d.ts}'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,testdata,stories,migrations,seeds,generated,__generated__,locales,i18n,scripts}/**'
   -g '!**/*.{spec,test,e2e-spec,mock,stories,test-data,fixture,fixtures}.*' -g '!**/{*_test,test_*,conftest}.*' -g '!docs/**' -g '!ai/**')
for t in ts js py go java kotlin cs php ruby rust dart; do printf '%-6s %s\n' "$t" "$(rg --files -t "$t" "${X[@]}" . | wc -l)"; done   # 0 = lane absent
# 0a. The declared architecture and what already enforces it (gate 4). A rule file here is §1's oracle.
rg --files --hidden -g '{.dependency-cruiser.*,.importlinter,tach.toml,.go-arch-lint.y*ml,deptrac.y*ml,sheriff.config.*,archunit.properties,package.yml,thresholds.local.json,architecture.md,modules.md}' -g '!**/{node_modules,vendor}/**' .
rg -n --pcre2 'boundaries/(?:dependencies|element-types)|no-restricted-(?:imports|paths)|enforce-module-boundaries|import(?:-x)?/no-cycle|\[tool\.importlinter\]|\b(?:depguard|cyclop|gocognit|gocyclo|mccabe|C901|complexity|CognitiveComplexity)\b' -g '{eslint.config.*,.eslintrc*,pyproject.toml,setup.cfg,.golangci.y*ml,detekt.yml,.rubocop.yml,nx.json,project.json,phpmd.xml}' -g '!**/node_modules/**' .
# 0b. Architecture tests and home-grown cycle gates: a control only once their verdict agrees with the tool lane (trap 4).
rg -l --pcre2 '\b(?:layeredArchitecture|beFreeOfCycles|ArchRuleDefinition|ArchUnitNET|NetArchTest|Konsist|findImportCycles)\b|(?:no-)?import-cycles\.|architecture-rules\.' -g '*.{ts,tsx,js,cjs,mjs,py,java,kt,cs,go,rb,php}' -g '!**/{node_modules,vendor,migrations}/**' -g '!{ai,docs}/**' .
# 0c. The repo-baseline module-boundaries hook: each rule line is an executable boundary for §1.
[ -f ai/modules.md ] && rg -n '^- `[^`]+` (?:MUST NOT import from|MAY import from) `' ai/modules.md; [ -d .claude ] && rg --files -g 'module-boundaries.sh' .claude
# 1b. A framework, ORM or web package imported inside a domain folder: the graph drops node_modules edges, so §1 sees these only here.
rg -n --pcre2 '^\s*(?:import\b[^\n]*\bfrom\s+|import\s+|from\s+)["\x27]?(?:@prisma/client|typeorm|@mikro-orm/|@nestjs/|express|fastify|sequelize|mongoose|knex|drizzle-orm|django|sqlalchemy|flask|fastapi|gorm\.io|github\.com/gin-gonic|org\.springframework|jakarta\.persistence|javax\.persistence)' -g '**/domain/**' "${X[@]}" .
# 1–4. The graph. JS/TS: dependency-cruiser per tsconfig root, run FROM that root (trap 2); cycles on value edges only (trap 3).
cat > "$D/dc.cjs" <<'JS'
module.exports = { forbidden: [{ name: 'no-circular', severity: 'error', from: {},
    to: { circular: true, dependencyTypesNot: ['type-only'], viaOnly: { dependencyTypesNot: ['type-only'] } } }],
  options: { doNotFollow: { path: 'node_modules' }, tsPreCompilationDeps: true,
    exclude: { path: '(^|/)(test|tests|__tests__|spec|e2e|__mocks__|mocks|fixtures|stories|migrations|seeds|generated)/|\\.(spec|test|e2e-spec|stories)\\.' } } };
JS
RK="$HOME/.claude/scripts/rank-source-files.py"; HERE=$PWD
n=0; for c in $(rg --files -g 'tsconfig.json' -g '!**/node_modules/**' .); do r=$(dirname "$c"); [ -d "$r/src" ] || continue; n=$((n+1)); echo "$r" > "$D/dc.$n.root"
  B=""; for b in "$HERE/$r/node_modules/.bin/depcruise" "$HERE/node_modules/.bin/depcruise" "$(command -v depcruise)"; do [ -x "$b" ] && { B="$b"; break; }; done   # installed only — an audit never downloads
  [ -n "$B" ] || { echo "graph NOT-RUN in $r (dependency-cruiser not installed — to enable: npm i -D dependency-cruiser@18) → build-graph.py lane"; continue; }
  if [ -n "${RO:-}" ] && [ -f "$RK" ]; then   # read-only target (trap 6): cwd and tsconfig in $D, never in the checkout
    python3 "$RK" . --ts-wrapper "$r" > "$D/tsc.$n.json" && python3 -c 'import os,sys; print(os.path.relpath(sys.argv[1]))' "$D" > "$D/dc.$n.root"
    (cd "$D" && "$B" "$HERE/$r/src" --config "$D/dc.cjs" --ts-config "$D/tsc.$n.json" --metrics --output-type json)
  else (cd "$r" && "$B" src --config "$D/dc.cjs" --ts-config tsconfig.json --metrics --output-type json); fi > "$D/dc.$n.json" 2> "$D/dc.$n.err" \
    || { echo "graph blocked in $r — $(rg -m1 -i 'error|node version' "$D/dc.$n.err")"; rm -f "$D/dc.$n.json"; }; done
# Python, Vue/Svelte, Dart (and TS/JS when the lane above is blocked): the Refract graph, value edges only (type-only and import()-only erased per statement, trap 5). --no-cache: writes nothing into the repo (trap 6).
[ -f "$HOME/.claude/scripts/build-graph.py" ] && python3 "$HOME/.claude/scripts/build-graph.py" --corpus=project --repo=. --no-cache --json > "$D/graph.json" 2> "$D/graph.err"
[ -f go.mod ] && go list -f '{{.ImportPath}}{{range .Imports}} {{.}}{{end}}' ./... > "$D/go.txt"   # package edges; Go package cycles do not compile
python3 - "$D" <<'PY'
import json,glob,os,re,sys,collections as C
D=sys.argv[1]; E=set(); VAL=set(); FB=set(); lane=[]; pc=lambda v,q: sorted(v)[int(q*(len(v)-1))] if v else 0
TEST=re.compile(r'(^|/)(test|tests|__tests__|spec|e2e|__mocks__|mocks|fixtures|testdata|stories|migrations|seeds|generated|scripts|docs|ai|node_modules|vendor|dist|build)/|\.(spec|test|e2e-spec|stories|test-data|fixtures?|d)\.|(^|/)(test_[^/]*|[^/]*_test)\.\w+$')
for p in sorted(glob.glob(D+'/dc.*.json')):
    r=open(p[:-4]+'root').read().strip(); J=lambda s: os.path.normpath(os.path.join(r,s)); lane.append('dependency-cruiser '+r)
    for m in json.load(open(p))['modules']:
        for d in m['dependencies']:
            if d.get('couldNotResolve') or d.get('coreModule') or 'node_modules' in d['resolved']: continue
            e=(J(m['source']),J(d['resolved'])); E.add(e); VAL.update([e] if 'type-only' not in d['dependencyTypes'] else [])   # type-only only if EVERY entry is (trap 4)
done={a.split('/src/')[0] for a,_ in E}
if os.path.exists(D+'/graph.json'):
    g=json.load(open(D+'/graph.json')); lane.append('refract graph ('+g['gates']['code']['detail']+')')
    GA=[x for x in g['edges'] if x['from'].split('/src/')[0] not in done]; GV={(x['from'],x['to']) for x in GA if not x.get('label')}   # label '' = value edge
    E|={(x['from'],x['to']) for x in GA}; VAL|=GV; FB|=GV
if os.path.exists(D+'/go.txt'):
    mp=open('go.mod').read().split()[1]; lane.append('go list'); G0={(a,b) for l in open(D+'/go.txt') for a,*bs in [l.split()] for b in bs if b.startswith(mp)}; E|=G0; VAL|=G0
NS=re.compile(r'\.(?:json|ya?ml|ttf|otf|woff2?|eot|css|scss|sass|less|svg|png|jpe?g|gif|webp|ico|md|mdx|txt|html|wasm|mp[34]|webm)$')   # assets and data files are not modules (§4 read 15 of 113 as fonts and i18n json)
E={e for e in E if not TEST.search(e[0]) and not TEST.search(e[1]) and not NS.search(e[0]) and not NS.search(e[1]) and e[0]!=e[1]}; V=E&VAL
cat=sorted({t.strip('/') for l in (open('ai/modules.md') if os.path.exists('ai/modules.md') else []) if l.startswith('|') for t in re.findall(r'`([\w@.\-/]+)`','|'.join(l.split('|')[1:3])) if '/' in t},key=len,reverse=True)
KEYS={'modules','features','domains','contexts','slices','internal','pkg','packages','apps','libs','services','src'}
def mod(f):   # the ai/modules.md catalog wins; else the deepest <container>/<name> segment
    for c in cat:
        i=('/'+f+'/').find('/'+c+'/')
        if i>=0: return f[:i+len(c)]
    s=f.split('/'); ix=[i for i,x in enumerate(s[:-1]) if x in KEYS]
    return '/'.join(s[:ix[-1]+(2 if ix[-1]+2<len(s) else 1)]) if ix else s[0]
HEX={'interface':'interface','presentation':'interface','controllers':'interface','application':'application','domain':'domain','infrastructure':'infrastructure','adapters':'infrastructure'}; FSD=['app','pages','widgets','features','entities','shared']
def lay(f):
    s=f.split('/'); h=[HEX[x] for x in s if x in HEX]; i=s.index('src')+1 if 'src' in s else 0
    return h[0] if h else (s[i] if 0<i<len(s)-1 and s[i] in FSD else '-')
R=os.environ.get('RULES') or ';'.join(['domain:application,interface,infrastructure','application:interface,infrastructure','interface:infrastructure']+[f'{a}:'+','.join(FSD[:i]) for i,a in enumerate(FSD) if i])
RU={(a,b) for r in R.split(';') for a,bs in [r.split(':')] for b in bs.split(',')}
F=sorted({x for e in E for x in e}); fi=C.defaultdict(set); fo=C.Counter(); M={f:mod(f) for f in F}
for a,b in E: fi[b].add(M[a]); fo[a]+=1
loc={f:sum(1 for _ in open(f,errors='ignore')) for f in F if os.path.isfile(f)}
print('lanes:',' · '.join(lane) or 'none — graph blocked'); print(f'files {len(F)} · edges {len(E)} ({len(E-V)} type-only) · modules {len(set(M.values()))} · layer rules: {"RULES" if "RULES" in os.environ else "default — the declared architecture wins"}')
json.dump([{'from':a,'to':b,'layer_from':lay(a),'layer_to':lay(b)} for a,b in sorted(E)],open(D+'/_dep-graph.json','w'))
print('§0 layer matrix:',dict(C.Counter((lay(a),lay(b)) for a,b in V if '-' not in (lay(a),lay(b)))))
bad=[(a,b) for a,b in V if (lay(a),lay(b)) in RU]; print(f'§1 forbidden-layer edges {len(bad)}'); [print('  ',a,'->',b) for a,b in bad[:10]]
PUB=re.compile(r'(^|/)(index|__init__|mod|api|public|contracts?|ports?)\.\w+$'); KER={'shared','common','core','kernel','lib','libs','utils','types','config','src'}
ri=C.Counter((M[a],M[b]) for a,b in V if M[a]!=M[b] and M[b].split('/')[-1] not in KER and M[a].split('/')[-1]!='src' and not M[a].startswith(M[b]+'/') and not PUB.search(b) and b.count('/')>M[b].count('/')+1)
print(f'§1 cross-module reach-ins {sum(ri.values())} across {len(ri)} module pairs'); [print(f'   {n:4d} {a} -> {b}') for (a,b),n in ri.most_common(8)]
cy=[]   # dependency-cruiser's own no-circular rows (value edges only), merged into groups
for p in glob.glob(D+'/dc.*.json'):
    r=open(p[:-4]+'root').read().strip()
    for x in json.load(open(p))['summary']['violations']:
        if x['rule']['name']=='no-circular': cy.append({os.path.normpath(os.path.join(r,y if isinstance(y,str) else y['name'])) for y in [x['from']]+x['cycle']})
grp=[]
for c in cy: hit=[g for g in grp if g&c]; grp=[g for g in grp if not g&c]+[set().union(c,*hit)]
BL=[open(r).read().strip() for r in glob.glob(D+'/dc.*.root') if not os.path.exists(r[:-4]+'json')]   # a root whose dependency-cruiser run failed or was not installed
FB={e for e in FB if e in E}; adj=C.defaultdict(list); [adj[a].append(b) for a,b in FB]; ix={}; low={}; st=[]; on=set(); scc=[]; k=0
for v0 in list(adj):   # iterative Tarjan over the fallback graph: SCCs are cycle CANDIDATES (no type-only flag, trap 5)
    if v0 in ix: continue
    work=[(v0,0)]
    while work:
        v,i=work.pop()
        if i==0: ix[v]=low[v]=k; k+=1; st.append(v); on.add(v)
        if i<len(adj[v]):
            work.append((v,i+1)); w=adj[v][i]
            if w not in ix: work.append((w,0))
            elif w in on: low[v]=min(low[v],ix[w])
            continue
        for w in adj[v]:
            if w in on: low[v]=min(low[v],low[w])
        if low[v]==ix[v]:
            c=set()
            while True:
                x=st.pop(); on.discard(x); c.add(x)
                if x==v: break
            if len(c)>1: scc.append(c)
if BL: print(f'§2 blocked (dependency-cruiser did not run in {", ".join(BL)} — see the "graph blocked" or "graph NOT-RUN" line above; never "0 cycles" there)')
if glob.glob(D+'/dc.*.json'): print(f'§2 runtime cycles {len(grp)} (dependency-cruiser, {len(cy)} reported paths, value edges only)'); [print(f'   {len(g)} files / {len({M[x] for x in g if x in M})} modules:',' '.join(sorted(g)[:4])) for g in sorted(grp,key=len,reverse=True)[:5]]
elif not FB and not BL: print('§2 blocked (no lane computed cycles: no dependency-cruiser run, no Refract graph; Go package cycles do not compile)')
if FB: print(f'§2 value cycles from the Refract graph {len(scc)} (type-only and import()-only erased per statement; resolved edges only — read each, trap 5)'); [print(f'   {len(c)} files:',' '.join(sorted(c)[:4])) for c in sorted(scc,key=len,reverse=True)[:5]]
Ca=C.defaultdict(set); Ce=C.defaultdict(set); MS=set(M.values()); root=lambda m: m.split('/')[-1]=='src' or '/' not in m
for a,b in V:
    if M[a]!=M[b]: Ce[M[a]].add(M[b]); Ca[M[b]].add(M[a])
I={m:len(Ce[m])/((len(Ca[m])+len(Ce[m])) or 1) for m in MS}
sdp=sorted({(a,b) for a in MS for b in Ce[a] if not root(a) and not root(b) and len(Ca[a])>=2 and I[a]+0.25<I[b]},key=lambda e:I[e[0]]-I[e[1]])
v=[len(fi[f]) for f in F]; c99=pc(v,.99); print(f'§3 fan-in (importing modules) p50 {pc(v,.5)} p90 {pc(v,.9)} p99 {c99} max {max(v or [0])} · above p99:'); [print(f'   {len(fi[f]):4d} {f}') for f in sorted(F,key=lambda f:-len(fi[f]))[:6] if len(fi[f])>c99]
print(f'§3 SDP edges (stable module -> markedly less stable) {len(sdp)}'); [print(f'   {a} (I {I[a]:.2f}) -> {b} (I {I[b]:.2f})') for a,b in sdp[:5]]
CR=re.compile(r'(^|/)(main|index|app|server|wire|Program|Startup)\.\w+$|\.module\.\w+$|(^|/)(entities|providers|routes?|registry)\.\w+$')
f99,l99=pc([fo[f] for f in F],.99),pc(list(loc.values()),.99); print(f'§4 fan-out p99 {f99} · LOC p99 {l99} · above either (composition roots tagged, § 57):')
[print(f'   out {fo[f]:4d} loc {loc.get(f,0):5d}{"  [composition root?]" if CR.search(f) else ""} {f}') for f in sorted(F,key=lambda f:-(fo[f]/max(f99,1)+loc.get(f,0)/max(l99,1)))[:8] if fo[f]>f99 or loc.get(f,0)>l99]
PY
# 6. Data access in the transport / view layer (also §1 presentation-imports-data): read each against the declared layers.
rg -n --pcre2 '\b(?:em|entityManager|prisma|knex|dataSource|queryRunner|db)\.(?:find|get|query|execute|create|persist|insert|update|delete|transaction)\w*\(|\.objects\.(?:filter|get|create|update)\(|\bsession\.(?:query|execute)\(|\b(?:DB|Model)::(?:table|query)\(' -g '**/{interface,controllers,presentation,handlers,routes,views,components,pages,ui}/**' "${X[@]}" .
# 7. Cross-cutting concerns rolled by hand (catch-and-log, inline auth check): files per directory; ≥ 5 directories → read.
rg -c -U --pcre2 'catch\s*\(\s*\w+(?:\s*:\s*\w+)?\s*\)\s*\{\s*(?:console|this\.logger|logger|log)\.(?:error|warn)\(|\bif\s*\(\s*!\s*(?:req\.)?(?:user|session|currentUser)\b[^\n]*\)\s*(?:\{\s*)?(?:throw|return\s+res\.status\(\s*40[13])' "${X[@]}" . | sed -E 's#^\./##; s#/[^/]+:[0-9]+$##' | sort | uniq -c | sort -rn | awk 'NR<=10 {print} END {print NR" directories"}'
# 8. Hand-rolled retry and pagination loops (one primitive missing at ≥ 3 sites, THR-DRY); clones across modules: duplication-scan step 1.
rg -n --pcre2 '\bfor\s*\(\s*let\s+(?:attempt|retry|tries)\b|\bwhile\s*\(\s*(?:attempt|retries|tries)\s*<|\bfor\s*\(\s*let\s+\w+\s*=\s*\d+\s*;\s*\w+\s*<=?\s*(?:\w+\.)?\w*(?:ATTEMPT|Attempt|RETR|Retr|TRIES|Tries)\w*|\b(?:offset|skip)\s*[+]=\s*(?:limit|take|pageSize|PAGE_SIZE)\b' "${X[@]}" .
# 9. Hotspots: 12-month churn (commits touching > 30 files dropped) × summed cyclomatic complexity × the share of fix commits.
git log --since=12.months --no-merges --format='%x00%H%x09%s' --name-only -- . ':!*.lock' ':!**/CHANGELOG*' > "$D/log.txt"
{ git rev-parse --is-shallow-repository; git log --max-parents=0 --format=%cs HEAD | sort | head -1; } > "$D/hist.txt"   # re-rooted / squashed / shallow history
rg --files -g '*{complexity,function-size}*baseline*.json' -g '!**/node_modules/**' . > "$D/cx-baselines.txt"   # a committed ESLint complexity baseline: the §9 fallback lane
python3 - "$D" <<'PY'
import re,sys,os,csv,json,shutil,datetime,subprocess,collections as C
D=sys.argv[1]; sh,*rt=open(D+'/hist.txt').read().split(); age=(datetime.date.today()-datetime.date.fromisoformat(rt[0])).days if rt else 0
if sh=='true' or age<90: sys.exit(f'§9 blocked (history {rt[0] if rt else "none"}: {"shallow clone" if sh=="true" else f"root commit {age} days ago"}; churn needs ≥ 90 days of history — re-rooted or squashed history is not a calm repo)')
FIX=re.compile(r'^(?:fix|hotfix|bugfix|revert)\b|\b(?:fixes|closes|resolves)\s+#\d+',re.I); pc=lambda v,q: sorted(v)[int(q*(len(v)-1))] if v else 0
SRC=re.compile(r'\.(?:ts|tsx|js|jsx|mjs|py|go|java|kt|cs|rb|php|rs|swift|dart|vue|svelte)$'); SKIP=re.compile(r'(^|/)(test|tests|__tests__|spec|e2e|__mocks__|mocks|fixtures|testdata|migrations|seeds|generated|locales|i18n|scripts|docs|ai|vendor|dist|build)/|\.(spec|test|e2e-spec|stories|d)\.|(^|/)(test_[^/]*|[^/]*_test)\.\w+$')
ch=C.Counter(); fx=C.Counter(); n=m=0
for b in open(D+'/log.txt').read().split('\0')[1:]:
    h,*fs=[x for x in b.split('\n') if x]; n+=1
    if len(fs)>30: m+=1; continue
    for f in fs:
        if SRC.search(f) and not SKIP.search(f) and os.path.isfile(f): ch[f]+=1; fx[f]+=bool(FIX.search(h.split('\t',1)[1]))
print(f'§9 commits {n} ({m} mass dropped) · files {len(ch)} · repo fix share {sum(fx.values())/max(sum(ch.values()),1):.2f}')
s=C.Counter(); mx={}; part=''
if shutil.which('lizard'):
    open(D+'/churn.txt','w').write('\n'.join(ch))
    for r in csv.reader(subprocess.run(['lizard','--csv','-f',D+'/churn.txt'],capture_output=True,text=True).stdout.splitlines()):
        s[r[6]]+=int(r[1]); mx[r[6]]=max(mx.get(r[6],(0,)),(int(r[1]),r[7],r[9],r[10]))
else:   # fallback: the project's committed complexity baseline (ESLint `complexity` over its limit): only over-limit functions are visible
    def walk(o,f=None,k=False):
        if isinstance(o,dict): [walk(v,(x if SRC.search(x) else f),k or 'complex' in x.lower()) for x,v in o.items()]
        elif isinstance(o,list): [walk(v,f,k) for v in o]
        elif k and f and isinstance(o,(int,float)) and not isinstance(o,bool): s[f]=max(s[f],int(o)); mx[f]=max(mx.get(f,(0,)),(int(o),'(baseline)','?','?'))
    B=[l.strip()[2:] if l.startswith('./') else l.strip() for l in open(D+'/cx-baselines.txt') if l.strip()]
    for b in B: walk(json.load(open(b)))
    if not s: sys.exit('§9 complexity lane blocked — lizard absent and no committed complexity baseline (pipx install lizard==1.24.0, or a stack lane from the table)')
    part=f' · partial: complexity from {", ".join(B)} (only functions over its limit), lizard absent'
F=[f for f in ch if f in s]; cc,kc=pc([ch[f] for f in (ch if part else F)],.95),(1 if part else pc([s[f] for f in F],.90)); base=sum(fx[f] for f in F)/max(sum(ch[f] for f in F),1)
H=sorted([f for f in F if ch[f]>=cc and s[f]>=kc],key=lambda f:-fx[f]/ch[f])
print(f'§9 hotspots {len(H)} (churn ≥ p95 {cc} commits AND summed CCN ≥ p90 {kc}) · fix share ≥ repo {base:.2f}: {sum(fx[f]/ch[f]>=base for f in H)}{part}')
[print(f'   {ch[f]:3d} commits {fx[f]:3d} fix · CCN sum {s[f]:4d} max {mx[f][0]:3d} {mx[f][1]} · {f}:{mx[f][2]}-{mx[f][3]}') for f in H[:12]]
PY
```

A candidate is an output line **plus** the code read at both ends **plus** the declared rule or the impact evidence. Blind spots: DI by token, dynamic `import()`, reflection, event buses and file-based routing produce no edge (read each composition root); the module unit is a guess until `ai/modules.md` names it; squash merges and fixes filed as `chore:` starve §9's fix share (read the top hotspots' commit subjects).

**Measured** (2026-10-05) on a real NestJS-on-Fastify + MikroORM + React monorepo (6,038 production files, 31,366 edges, 3,552 commits; about 22 s). §1: 0 edges against the declared hexagonal order in the API, which its ESLint rules hold at error; 108 default FSD hits in the web app, all inside the exemption those rules carry, so the declared tool wins. §2: 1 runtime cycle, 12 files across three feature slices through their barrels, missed by the project's own gate (trap 4). §3: every file above the fan-in p99 (19 importing modules) is shared kernel. §4: the eight largest fan-outs are composition roots (§ 57). §6: 0. §8: six hand-rolled unique-code retry loops in four modules. §9: 82 hotspots, 46 at or above the repo's 0.46 fix share; on the top one, a 426-line function with CCN 75, 20 of the 28 commits on its own lines were fixes. The most-churned file (90 commits) was a composition root the complexity cut removed. `benchmarks/fixtures/slow-marketplace`: §2 lists 3 ORM-entity cycles (§2 read). `quality-mix` on Node 23.8: 1b → the one seeded `@prisma/client` import in `api/src/domain` (the declared rule exists but no CI runs it); dependency-cruiser blocked in both roots, so §2 prints `blocked` and the Refract graph's value cycles: 1, the seeded `billing.events` ↔ `billing.service` (the `import type` pair it used to list is erased per statement since 2026-10-15). **Re-measured 2026-10-15** on the same monorepo, read-only and offline (Refract graph lane only, `--no-cache`, about 8 s): 7,046 files, 39,118 edges (9,110 type-only); §1 107 default FSD hits (the declared ESLint rules own them); §2 0 value cycles — the 12-file cycle is gone — and 28 type-only SCCs, the largest 40 files (§ 87); §4 the eight largest fan-outs are composition roots, and fonts and i18n JSON (15 of 113 rows) no longer enter it; §7 16 directories; §8 9 loops (the `n <= DERIVED_TRIES` shape was missed before); §9 `blocked (history 2026-10-12)` — the history had been re-rooted three days earlier, which the old script read as a calm repo of 136 commits; forced past that, the committed complexity baseline (lizard absent) gives 3 hotspots. `slow-marketplace`: the same 3 ORM-entity cycles.

## Diff runs — worse than the merge-base, or Pre-existing

Run the same script on the merge-base in a detached worktree (never `stash`, `reset` or `checkout` in a shared tree), then keep what the diff made worse:

```bash
BASE=$(git merge-base origin/main HEAD); W="${TMPDIR:-/tmp}/arch-diag-base"; git worktree add -q --detach "$W" "$BASE"
# run the pre-flight inside "$W" with TMPDIR="$W.tmp", then:
git diff --name-only --diff-filter=AMR "$BASE"...HEAD > "${TMPDIR:-/tmp}/arch-diag/changed.txt"
python3 -c 'import json,sys;h,b=({(r["from"],r["to"]) for r in json.load(open(p))} for p in sys.argv[1:3]);c=set(open(sys.argv[3]).read().split());n=sorted(e for e in h-b if e[0] in c);print(len(n),"new edges from changed files");[print("  ",*e) for e in n]' "${TMPDIR:-/tmp}/arch-diag/_dep-graph.json" "$W.tmp/arch-diag/_dep-graph.json" "${TMPDIR:-/tmp}/arch-diag/changed.txt"
git worktree remove --force "$W"
```

A diff finding is a new edge breaking a declared rule, a cycle at head absent at the base, a changed file whose fan-out, LOC or complexity grew past the cut-off (*Metric ratchet*, [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Code quality), or a new dependency on a known hotspot or god module (§ 61 flips back). The rest is **Pre-existing**, one line each. Measured: a 60-commit range (349 changed files) gave 193 new edges in about 45 s.

## The 3,000-hit path

1. **The declared tool's violations first**; default rules only fill a gap.
2. **Group** by module pair (§1), cycle (§2), module (§3–§5), directory (§6–§8), file (§9).
3. **Rank** money, authorization, tenancy and write paths first, then hotspots (a candidate inside one rises a step). **Read the top 30 groups.**
4. **Bulk oracles:** the conformance tool over the tree, `smoke-verify`'s boot, the base-vs-head run.
5. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the continuing command.

## Detectors (the 8 architectural smells, plus §9 hotspots)

Maintainability is **never critical**. One step up on a hotspot or a money / auth / tenant path.

| § | Class | ISO/IEC 5055 maintainability weakness | Default |
|---|---|---|---|
| 1 | layer-violation (incl. cross-module reach-in) | layer-skipping, hierarchy-breaking call | high when domain / core imports infrastructure, UI or a framework against a declared rule; else medium; Advisory when prose only |
| 2 | cyclic-dependency | circular dependency | medium; high with a boot failure or in core; type-only or inside one module: Hardening |
| 3 | bottleneck-module (fan-in, instability, SDP) | excessive coupling | low; medium with change coupling |
| 4 | god-module | excessive outward calls, oversized unit | medium; high when a hotspot |
| 5 | anemic-module | — | low / Advisory; medium under a declared rich domain |
| 6 | wrong-level-responsibility | hierarchy-breaking call | medium |
| 7 | cross-cutting-duplication | redundant code | medium when a copy diverged; else Hardening |
| 8 | missing-abstraction | redundant code | low; medium at ≥ 3 sites that change together (`THR-DRY`) |
| 9 | hotspot (churn × complexity × fix share) | excessive cyclomatic complexity | ranks the others; medium alone only with fix density or an untested hot branch |

### 1. layer-violation

```
BAD:   modules/billing/domain/invoice.ts imports '@mikro-orm/core'            // declared: domain is framework-free (ARCH-2)
       features/orders/list/Page.tsx imports features/delivery/review/components/Panel   // past the slice's index (ARCH-3)
GOOD:  the domain owns a port, infrastructure implements it · cross-module access through the public surface
```
**Read the code:** Which declared rule does the edge break (cite `file:line`)? Is the importer a composition root (§ 57), a test or a type-only import? Is the target the public surface (`index`, `api`, `ports`)? Does a running tool already report it at error? Under Active Record (§ 66) a model in a controller is the design. **Finding when** a value edge breaks a declared rule no running tool owns. **Proof:** the conformance tool (or the module-boundaries rule replayed) prints it at `<path:line>`; on a diff, the edge is absent at the base.

### 2. cyclic-dependency

**Read the code:** Is every edge a value edge (traps 3, 4)? Does a module-level statement use an imported binding during evaluation (TDZ `undefined`; Python "partially initialized module")? ORM entities linked by `() => Entity` thunks resolve late, but `emitDecoratorMetadata` on a property typed with the other class reads it at definition (`Rel<T>` / `Ref<T>` avoid it). Does it cross declared boundaries? Does a home-grown gate (step 0b) agree? **Finding when** a runtime cycle crosses declared boundaries or has init-order impact; else Hardening (a type-only or thunk-only cycle: § 87). **Proof:** *Boot* (`smoke-verify`) fails, or the tool lists it; on a diff, absent at the base. Closure: `decouple-cycle` (move the shared piece down a layer, or import the leaf instead of the barrel).

### 3. bottleneck-module

**Read the code:** Is the fan-in a shared kernel by design (errors, ids, UI primitives; § 86)? Is the SDP edge (stable module → markedly less stable) a real direction, or a type the stable side should own? Do its changes ripple (`git log --format=%H -- <file>` co-changing with ≥ 5 modules in 12 months)?
**Finding when** an SDP edge or above-p99 fan-in carries change coupling the design does not intend. **Proof:** `depcruise --metrics` Ca / Ce / I and the co-change count.

### 4. god-module

**Read the code:** Composition root (§ 57), registry, generated client (§ 54) or framework shape (§ 56)? Cluster its exports by responsibility and name each. **Finding when** fan-out or LOC is above the repo p99 **and** it mixes named responsibilities **and** it is a hotspot or its callers' changes keep touching it. **Proof:** the numbers against the percentiles, the clusters, the hotspot row.

### 5. anemic-module

**Read the code:** From the responsibility map: a data-only module whose single consumer holds all its behaviour? DTOs, contracts, messages and ports are data by design. **Finding when** a declared rich-domain rule is broken and the entity's invariants are enforced elsewhere (ARCH-5). **Proof:** the rule cited and the invariant's enforcement site.

### 6. wrong-level-responsibility

**Read the code:** A controller, view or handler that queries, decides a business rule or formats for another layer: a read through an allowed port, or the decision itself? **Finding when** the declared layer map puts it elsewhere and the code bypasses that layer. **Proof:** the rule and the second site that does it in the right layer.

### 7. cross-cutting-duplication

**Read the code:** Do ≥ 5 directories roll one concern (inline auth check, catch-and-log, retry) while a middleware, filter, interceptor or decorator exists or should? **Finding when** `duplication-scan` §1 or `error-handling-scan` proves a copy wrong, or the central primitive exists and is bypassed. **Proof:** that skill's oracle.

### 8. missing-abstraction

**Read the code:** Do ≥ 3 sites (`THR-DRY`) implement one primitive (paging, retries, unique codes, an error envelope) that must change together, not two similar blocks (§ 58)? **Finding when** one site already drifted, or a pending change touches them all. **Proof:** the sites cited with the line that differs; `duplication-scan` step 1 for clones.

### 9. hotspot

```
HOT:   ledger/application/commands/ledger.shared.ts:480-905   31 commits (p95 = 9) · CCN 75 · 20 fixes on its own lines
COLD:  orders/orders.module.ts   90 commits, CCN ≤ 2 per factory   // composition root: churn without complexity
```
**Read the code:** `git log --no-patch --format=%s -L<start>,<end>:<file>` on the hottest function: how many commits are fixes, to the same branch? Is that branch covered (`test-shield`, this pack, or `coverage-gap` when the testing pack is installed)? **Finding when** the fix share on the function's own lines is at or above the repo's with at least two fixes, or the hot branch is untested; else it only ranks. **Proof:** the `git log -L` count and the coverage line. The fix goes to `refactoring-sweep` (Phase 2), pinned first; §9 has no architectural closure verb.

## Procedure (step-by-step — what the skill executes)

1. **Pin** `git rev-parse HEAD` in the header.
2. **Run the pre-flight**; record lanes and `blocked` lines; copy `$TMPDIR/arch-diag/_dep-graph.json` (rows `{from, to, layer_from, layer_to}`) to `ai/optimize/_dep-graph.json`.
3. **Responsibility map**: per module, exports and a one-line responsibility → `ai/optimize/_responsibility-map.md`.
4. **Run the 9 detectors** through § The rule (diffs: § Diff runs).
5. **Verify** through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10 with [`precedents/code-quality.md`](../../../../snippets/precedents/code-quality.md).
6. **Per finding:** `<path:line>`, closure verb, cascade (tactical findings it dissolves), net lines, risk.
7. **Order foundations** by cascade, dependencies first (introduce the abstraction before the split that uses it).
8. **Write** `ai/optimize/_architecture-decisions.md`; apply nothing.

Closure verbs (the closed set `/optimize` Phase 1 applies): `move-responsibility`, `fix-layering`, `decouple-cycle`, `split-god-module`, `merge-anemic-module`, `centralize-cross-cutting`, `introduce-abstraction`.

## Outputs (precise contract)

`ai/optimize/_architecture-decisions.md`, read by `/optimize` Phase 1 and checked by `scripts/validate-optimize-artifacts.sh` (four Phase 0 blocks, `Modules scanned: ≥ 1`, a `<path:line>` in every `### F-A-` section, no hand-waves):

```markdown
# Architecture decisions — generated <iso>
> Commit <sha> · PROJECT_KIND <kind> · lanes: dependency-cruiser 18.5.0 (apps/api, apps/web), lizard 1.24.0
> Layer rules: eslint.config.mjs:393-480 (declared) · ai/modules.md: 0 boundary lines · BASE: none (whole repo)

### F-A-001 — cyclic-dependency [P1]   [report-flagged]
- **Class**: §2 · ISO/IEC 5055 maintainability (circular dependency) · runtime, through barrels
- **Evidence**: `src/features/orders/scanner/lib/export.ts:1` imports the delivery/review barrel; closes at `src/features/delivery/review/components/ReviewPanel.tsx:24` (12 files, 3 slices)
- **Measured**: dependency-cruiser no-circular, value edges only; the project's gate reports 0 (trap 4)
- **Impact**: crosses declared slice boundaries · unproven link: boot order — settling step `smoke-verify` with that route first
- **Closure verb**: decouple-cycle (the summary helper moves to the delivery core) · **Cascade**: 0 · **Net lines**: ±0 · **Risk**: low

## Class coverage
  §1 layer-violation      checked (declared: ESLint at error → tool-owned; 108 default hits, all exempted)
  §2 cyclic-dependency    checked (1 runtime cycle → 1 flagged)
  §3 bottleneck-module    checked (6 above p99, all shared kernel → Hardening) · Live, unreviewed (21 SDP edges)
  §4 god-module           checked (8 above p99, all composition roots, § 57)
  §5 anemic-module        checked (no rich-domain ADR → 0)
  §6 wrong-level          checked (0 hits)
  §7 cross-cutting dup    checked (20 directories, ≤ 2 files each)
  §8 missing-abstraction  checked (6 retry loops / 4 modules → 1 Advisory)
  §9 hotspot              checked (82 → 46 at fix share ≥ repo → 1 finding) · Live, unreviewed (45 rows)
```

Then `## Decision summary` and `## Application order (foundation phase)`. **All nine** classes are listed on every run: `checked (k → m findings)` only when the lane ran; `N/A (<reason>)` only for an absent surface (Go package cycles; no history); `blocked (<reason>)` when a lane failed. `[report-with-fix]` rows carry the proof; `[report-flagged]` rows name the unproven link and its settling step.

## Mandatory Phase-0 evidence emission

The artifact MUST contain machine-verifiable evidence. Without it, `validate-optimize-artifacts.sh § check_phase_0_blocks_nonempty` halts the run. Required shape:

```
## Phase 0 — Dependency map evidence
Source files walked: <count>   (the pre-flight's "files" line)
Import statements parsed: <count>   (its "edges" line; type-only counted separately)
Sample (first 20 rows; full graph at ai/optimize/_dep-graph.json):
  <module-A> → <module-B>  (via <import-statement-path:line>)

## Phase 0 — Responsibility map evidence
Source: ai/optimize/_responsibility-map.md
Sample (first 20 modules):
  <module-path>: owns <responsibility>; exports <symbol-count> symbols at <path:lines>

## Phase 0 — Layer attribution evidence
Layer rules read from: <the declared rule file:line, ai/architecture.md, or "default — candidates only">
Modules attributed (per layer):
  <layer>: [<module-paths>]

## Phase 0 — Detector run evidence
For EACH of the 9 detectors, paste:
  Detector: <detector-name>
  Modules scanned: <count>
  Fingerprint matches: <count>   (and the repo cut-off it was measured against)
  Sample matches (first 10):
    - <path:line> — <fingerprint-excerpt>
  No-match modules: <count>
```

Without these blocks the validator halts with: "Phase 0 evidence missing in <file>; architectural diagnosis cannot be trusted."

## Halt #A1 — Phase 0 must be auditable

A Phase 0 run that outputs only architecture-decisions.md without the four evidence blocks above is a "summary diagnosis" — flagged equivalent to the F039 anti-Trusted-Summary recurrence. The validator refuses to advance /optimize past Phase 0 without visible evidence.

## Hard rules

- Every finding cites `<path:line>` and the rule or cut-off it was measured against. A graph comes from a tool lane; a `blocked` lane is never a clean result.
- No fixed numeric threshold is a finding. Closure verbs are the closed set above; no novel architectural move is invented at fix time.
- A high-risk finding (multi-PR cycle, a split that changes a public API) goes to the user. The artifact is internal; `/optimize` summarises each fix in one or two lines.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/optimize`, `/audit` or `/quality-audit` that happens in their verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on a finding without `<path:line>`, the measured number or declared rule, and the impact evidence. Do not print "architecturally clean" without the coverage block, or from a `blocked` graph lane.
- Do not report a diff finding the merge-base already had: it is Pre-existing.
- No declared layers → WARN, §1 default rules as candidates only. Five or fewer modules → "skip — small project", no foundations. A cycle across four or more modules → a user decision with a multi-PR plan.

## Verify (postconditions)

Contract: [`templates/snippets/postcondition-check.md`](../../../../snippets/postcondition-check.md). **Preconditions are not verification** — this skill guards its entry and must also check its exit. Every entry under `## Failure modes` that this skill's own write could cause becomes a check here, observed rather than assumed, reported when it passes as well as when it fails, and `NOT RUN` with a reason where no signal is available. Here: `validate-optimize-artifacts.sh` passes its Phase 0 checks, and `ai/optimize/_dep-graph.json` holds the pinned commit's rows.

## Failure modes

- **No findings** → "Codebase already architecturally clean; tactical sweep proceeds directly", with the coverage block.
- **All findings high-risk** → halt /optimize; list them with one-line risk reasons; the user picks.
- **Declared rules contradict the layout** → WARN, prefer the declared rules, report the drift as its own row.
- **A home-grown gate disagrees with the tool lane** → the gate's blind spot is the finding (trap 4).

## False positives / precedents

The verifier reads [`precedents/code-quality.md`](../../../../snippets/precedents/code-quality.md) (§ 51–70, § 86–87, § 91) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4, § 5, § 10. Most met here: a metric alone (§ 51), composition roots (§ 57), generated code and framework shapes (§ 54, § 56), two similar blocks (§ 58), untouched breaches (§ 61), Active Record (§ 66), structural co-change (§ 68). A **shared kernel** has high fan-in by design (§ 86), and a **type-only or lazy ORM-entity cycle** does not exist at runtime (§ 87; Hardening at most).

## References

- `/optimize` Phase 0–1, `/audit`, `/quality-audit`; [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Code quality (*Metric ratchet*, *Boot*, V86).
- This pack: `smoke-verify`, `test-shield`, `duplication-scan`, `error-handling-scan`, `dead-code-scan`, `refactoring-sweep`, `debt-ledger` (an acknowledged finding may become a dated, owned ledger item), `ai-patterns/module-boundaries.md`, `rules/engineering-principles.md`; `align-discipline.md` (closure verbs); `migration-discipline.md` (dead-module axes).
- Sources: the code-quality research catalog and maintainability notes (2026-10-05: tool versions; Nagappan & Ball, ICSE 2005, relative churn; Alves et al., ICSM 2010, percentile thresholds; McCabe 1976); runs of dependency-cruiser 18.5.0 and lizard 1.24.0 that day.
