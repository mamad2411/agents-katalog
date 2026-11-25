---
name: legalgraph
description: "Turn legal documents, policies, contracts, compliance rules, and regulatory text into a queryable knowledge graph. Extracts clauses, obligations, prohibitions, permissions, cross-references, and detects conflicts. Answers questions like 'What does policy X say about Y?', 'Find all obligations for role Z', 'Are these two clauses contradictory?'"
---

# /legalgraph

Build a navigable knowledge graph from legal and policy documents with clause-level extraction, cross-references, conflict detection, and compliance tracing.

## Usage

```
/legalgraph                                          # full pipeline on current directory
/legalgraph <path>                                   # full pipeline on specific path
/legalgraph <path> --mode deep                        # thorough extraction, finer clause granularity
/legalgraph <path> --update                           # incremental - re-extract only new/changed files
/legalgraph <path> --no-viz                           # skip visualization, just report + JSON
/legalgraph <path> --conflicts-only                   # only extract and report clause conflicts
/legalgraph query "<question>"                        # query the graph (BFS traversal)
/legalgraph path "Clause 3.2" "Section 7.1"           # relationship path between two clauses
/legalgraph obligations "<role/department>"            # find all obligations for a role
/legalgraph conflicts --domain GDPR                  # check for conflicts within a regulatory domain
/legalgraph explain "Data Retention Policy"           # plain-language explanation of a clause/concept
```

## What legalgraph is for

Drop a folder of legal documents, policies, contracts, or regulatory text into legalgraph and get a structured graph of every clause, obligation, prohibition, permission, and cross-reference. Detect contradictory provisions, trace compliance chains, and answer natural-language questions about your legal corpus.

## What You Must Do When Invoked

If the user invoked `/legalgraph --help` or `/legalgraph -h` (with no other arguments), print the contents of the `## Usage` section above verbatim and stop.

**Fast path — existing graph:** Before doing anything else, check whether `legalgraph-out/graph.json` exists relative to the current working directory. If it exists AND the user's request is a natural-language question about the documents and NOT an explicit rebuild command (`--update`, `--conflicts-only`, or a bare path): **skip Steps 1-4 and jump straight to `## For /legalgraph query`.**

If no path was given, use `.` (current directory). Do not ask the user for a path.

Follow these steps in order. Do not skip steps.

### Step 1 - Ensure legalgraph is installed

```bash
# Detect Python interpreter
PYTHON=""
LEGALGRAPH_BIN=$(which legalgraph 2>/dev/null)
if [ -z "$PYTHON" ] && command -v uv >/dev/null 2>&1; then
    _UV_PY=$(uv tool run legalgraph python -c "import sys; print(sys.executable)" 2>/dev/null)
    if [ -n "$_UV_PY" ]; then PYTHON="$_UV_PY"; fi
fi
if [ -z "$PYTHON" ] && [ -n "$LEGALGRAPH_BIN" ]; then
    _SHEBANG=$(head -1 "$LEGALGRAPH_BIN" | tr -d '#!')
    case "$_SHEBANG" in
        *[!a-zA-Z0-9/_.-]*) ;;
        *) "$_SHEBANG" -c "import legalgraph" 2>/dev/null && PYTHON="$_SHEBANG" ;;
    esac
fi
if [ -z "$PYTHON" ]; then PYTHON="python3"; fi
if ! "$PYTHON" -c "import legalgraph" 2>/dev/null; then
    if command -v uv >/dev/null 2>&1; then
        uv tool install --upgrade legalgraph -q 2>&1 | tail -3
        _UV_PY=$(uv tool run legalgraph python -c "import sys; print(sys.executable)" 2>/dev/null)
        if [ -n "$_UV_PY" ]; then PYTHON="$_UV_PY"; fi
    else
        "$PYTHON" -m pip install legalgraph -q 2>/dev/null \
          || "$PYTHON" -m pip install legalgraph -q --break-system-packages 2>&1 | tail -3
    fi
fi
mkdir -p legalgraph-out
"$PYTHON" -c "import sys; open('legalgraph-out/.legalgraph_python', 'w', encoding='utf-8').write(sys.executable)"
echo "$(cd INPUT_PATH && pwd)" > legalgraph-out/.legalgraph_root
```

If the import succeeds, print nothing and move to Step 2.

**In every subsequent bash block, use `$(cat legalgraph-out/.legalgraph_python)` instead of `python3`.**

### Step 2 - Detect files

```bash
$(cat legalgraph-out/.legalgraph_python) -c "
import json
from legalgraph.detect import detect
from pathlib import Path
result = detect(Path('INPUT_PATH'))
print(json.dumps(result, ensure_ascii=False))
" > legalgraph-out/.legalgraph_detect.json
```

Replace INPUT_PATH with the actual path. Read the JSON silently and present:

```
Corpus: X files · ~Y words
  contracts:    N files (.pdf .docx .txt with contract patterns)
  policies:     N files (.md .txt policy documents)
  regulations:  N files (.pdf .html regulatory text)
  general:      N files (other doc types)
```

Omit categories with 0 files. Then:
- If `total_files` is 0: stop with "No supported files found in [path]."
- If `total_words` > 1,000,000 OR `total_files` > 300: show top 5 subdirectories by file count, ask user to narrow scope
- Otherwise: proceed to Step 3

### Step 3 - Extract clauses and relationships

This step has two parts: **structural extraction** (section parsing, heading hierarchy) and **semantic extraction** (LLM-based clause analysis).

**Run Part A and Part B in parallel.**

#### Part A - Structural extraction

Parse document structure, heading hierarchy, section numbering, and cross-reference patterns:

```bash
$(cat legalgraph-out/.legalgraph_python) -c "
import json
from legalgraph.extract import structural_extract
from pathlib import Path

detect = json.loads(Path('legalgraph-out/.legalgraph_detect.json').read_text(encoding='utf-8'))
all_files = [f for files in detect['files'].values() for f in files]

result = structural_extract(all_files)
Path('legalgraph-out/.legalgraph_structural.json').write_text(
    json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Structural: {len(result[\"nodes\"])} nodes, {len(result[\"edges\"])} edges')
"
```

#### Part B - Semantic extraction (LLM subagents)

**MANDATORY: Use the Agent tool. Processing files one-by-one is forbidden.**

Before dispatching, check for Gemini API key:
> Tip: Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` to use Gemini for semantic extraction (`pip install 'legalgraph[gemini]'`).

If set, use `legalgraph.llm.extract_corpus_parallel(files, backend="gemini")`. Otherwise dispatch Claude subagents.

**Step B0 - Check extraction cache**

```bash
$(cat legalgraph-out/.legalgraph_python) -c "
import json
from legalgraph.cache import check_semantic_cache
from pathlib import Path

detect = json.loads(Path('legalgraph-out/.legalgraph_detect.json').read_text(encoding='utf-8'))
all_files = [f for files in detect['files'].values() for f in files]

cached_nodes, cached_edges, uncached = check_semantic_cache(all_files)

if cached_nodes or cached_edges:
    Path('legalgraph-out/.legalgraph_cached.json').write_text(
        json.dumps({'nodes': cached_nodes, 'edges': cached_edges}, ensure_ascii=False), encoding='utf-8')
Path('legalgraph-out/.legalgraph_uncached.txt').write_text('\n'.join(uncached), encoding='utf-8')
print(f'Cache: {len(all_files)-len(uncached)} files hit, {len(uncached)} files need extraction')
"
```

**Step B1 - Split into chunks**

Load from `legalgraph-out/.legalgraph_uncached.txt`. Split into chunks of 15-20 files. Group files from the same directory and same document type together.

**Step B2 - Dispatch ALL subagents in one message**

Use `subagent_type="general-purpose"`. One call per chunk, all in the same response.

Each subagent receives the prompt from `references/extraction-spec.md` with FILE_LIST, CHUNK_NUM, TOTAL_CHUNKS, DEEP_MODE, and CHUNK_PATH substituted.

CHUNK_PATH must be absolute:
```bash
PROJECT_ROOT=$(cat legalgraph-out/.legalgraph_root)
CHUNK_PATH="${PROJECT_ROOT}/legalgraph-out/.legalgraph_chunk_0N.json"
```

**Step B3 - Collect, cache, merge**

Wait for all subagents. For each:
- Verify `legalgraph-out/.legalgraph_chunk_NN.json` exists
- If missing, warn: "chunk N missing — subagent may have been read-only. Re-run with general-purpose agent."
- If invalid JSON, warn and skip

**More than half failed?** Stop and tell the user.

Read real token counts from Agent `usage` field, write back to chunk JSON, then merge:

```bash
$(cat legalgraph-out/.legalgraph_python) -c "
import json, glob
from pathlib import Path

chunks = sorted(glob.glob('legalgraph-out/.legalgraph_chunk_*.json'))
all_nodes, all_edges, all_hyperedges = [], [], []
total_in, total_out = 0, 0
for c in chunks:
    d = json.loads(Path(c).read_text(encoding='utf-8'))
    all_nodes += d.get('nodes', [])
    all_edges += d.get('edges', [])
    all_hyperedges += d.get('hyperedges', [])
    total_in += d.get('input_tokens', 0)
    total_out += d.get('output_tokens', 0)
Path('legalgraph-out/.legalgraph_semantic_new.json').write_text(json.dumps({
    'nodes': all_nodes, 'edges': all_edges, 'hyperedges': all_hyperedges,
    'input_tokens': total_in, 'output_tokens': total_out,
}, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Merged {len(chunks)} chunks: {total_in:,} in / {total_out:,} out tokens')
"
```

Save to cache:

```bash
$(cat legalgraph-out/.legalgraph_python) -c "
import json
from legalgraph.cache import save_semantic_cache
from pathlib import Path

new = json.loads(Path('legalgraph-out/.legalgraph_semantic_new.json').read_text(encoding='utf-8')) if Path('legalgraph-out/.legalgraph_semantic_new.json').exists() else {'nodes':[],'edges':[],'hyperedges':[]}
saved = save_semantic_cache(new.get('nodes', []), new.get('edges', []), new.get('hyperedges', []))
print(f'Cached {saved} files')
"
```

Merge cached + new:

```bash
$(cat legalgraph-out/.legalgraph_python) -c "
import json
from pathlib import Path

cached = json.loads(Path('legalgraph-out/.legalgraph_cached.json').read_text(encoding='utf-8')) if Path('legalgraph-out/.legalgraph_cached.json').exists() else {'nodes':[],'edges':[]}
new = json.loads(Path('legalgraph-out/.legalgraph_semantic_new.json').read_text(encoding='utf-8')) if Path('legalgraph-out/.legalgraph_semantic_new.json').exists() else {'nodes':[],'edges':[],'hyperedges':[]}

all_nodes = cached['nodes'] + new.get('nodes', [])
all_edges = cached['edges'] + new.get('edges', [])
all_hyperedges = new.get('hyperedges', [])
seen = set()
deduped = []
for n in all_nodes:
    if n['id'] not in seen:
        seen.add(n['id'])
        deduped.append(n)

merged = {
    'nodes': deduped,
    'edges': all_edges,
    'hyperedges': all_hyperedges,
    'input_tokens': new.get('input_tokens', 0),
    'output_tokens': new.get('output_tokens', 0),
}
Path('legalgraph-out/.legalgraph_semantic.json').write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Extraction: {len(deduped)} nodes, {len(all_edges)} edges ({len(cached[\"nodes\"])} from cache, {len(new.get(\"nodes\",[]))} new)')
"
```

Clean up: `rm -f legalgraph-out/.legalgraph_cached.json legalgraph-out/.legalgraph_uncached.txt legalgraph-out/.legalgraph_semantic_new.json`

#### Part C - Merge structural + semantic

```bash
$(cat legalgraph-out/.legalgraph_python) -c "
import json
from pathlib import Path

struct = json.loads(Path('legalgraph-out/.legalgraph_structural.json').read_text(encoding='utf-8'))
sem = json.loads(Path('legalgraph-out/.legalgraph_semantic.json').read_text(encoding='utf-8'))

seen = {n['id'] for n in struct['nodes']}
merged_nodes = list(struct['nodes'])
for n in sem['nodes']:
    if n['id'] not in seen:
        merged_nodes.append(n)
        seen.add(n['id'])

merged = {
    'nodes': merged_nodes,
    'edges': struct['edges'] + sem['edges'],
    'hyperedges': sem.get('hyperedges', []),
    'input_tokens': sem.get('input_tokens', 0),
    'output_tokens': sem.get('output_tokens', 0),
}
Path('legalgraph-out/.legalgraph_extract.json').write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Merged: {len(merged_nodes)} nodes, {len(merged[\"edges\"])} edges ({len(struct[\"nodes\"])} structural + {len(sem[\"nodes\"])} semantic)')
"
```

### Step 4 - Build graph, detect conflicts, analyze, generate outputs

```bash
mkdir -p legalgraph-out
$(cat legalgraph-out/.legalgraph_python) -c "
import json
from legalgraph.build import build_from_json
from legalgraph.conflict import find_conflicts, find_gaps
from legalgraph.analyze import key_clauses, compliance_paths, suggest_questions
from legalgraph.report import generate
from legalgraph.export import to_json
from pathlib import Path

extraction = json.loads(Path('legalgraph-out/.legalgraph_extract.json').read_text(encoding='utf-8'))
detection = json.loads(Path('legalgraph-out/.legalgraph_detect.json').read_text(encoding='utf-8'))

G = build_from_json(extraction)
conflicts = find_conflicts(G)
gaps = find_gaps(G)
keys = key_clauses(G)
compliance = compliance_paths(G)
questions = suggest_questions(G, conflicts, gaps)
labels = legalgraph.analyze.label_domains(G)

tokens = {'input': extraction.get('input_tokens', 0), 'output': extraction.get('output_tokens', 0)}
report = generate(G, labels, conflicts, gaps, keys, compliance, detection, tokens, '.')
Path('legalgraph-out/LEGAL_REPORT.md').write_text(report, encoding='utf-8')
to_json(G, labels, 'legalgraph-out/graph.json')

analysis = {
    'domains': {str(k): v for k, v in labels.items()},
    'conflicts': conflicts,
    'gaps': gaps,
    'keys': keys,
    'compliance': compliance,
    'questions': questions,
}
Path('legalgraph-out/.legalgraph_analysis.json').write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding='utf-8')
if G.number_of_nodes() == 0:
    print('ERROR: Graph is empty - extraction produced no nodes.')
    raise SystemExit(1)
print(f'Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {len(labels)} domains, {len(conflicts)} conflicts')
"
```

If `ERROR: Graph is empty`, stop.

### Step 5 - Label domains and refine report

Read `legalgraph-out/.legalgraph_analysis.json`. For each domain key, write a 2-5 word label (e.g. "Data Privacy", "Employment", "Intellectual Property").

Regenerate:

```bash
$(cat legalgraph-out/.legalgraph_python) -c "
import json
from legalgraph.build import build_from_json
from legalgraph.analyze import suggest_questions, label_domains
from legalgraph.report import generate
from pathlib import Path

extraction = json.loads(Path('legalgraph-out/.legalgraph_extract.json').read_text(encoding='utf-8'))
detection = json.loads(Path('legalgraph-out/.legalgraph_detect.json').read_text(encoding='utf-8'))
analysis = json.loads(Path('legalgraph-out/.legalgraph_analysis.json').read_text(encoding='utf-8'))

G = build_from_json(extraction)
tokens = {'input': extraction.get('input_tokens', 0), 'output': extraction.get('output_tokens', 0)}

# LABELS - replace with the domain names you chose
labels = LABELS_DICT

questions = suggest_questions(G, analysis['conflicts'], analysis['gaps'])
report = generate(G, labels, analysis['conflicts'], analysis['gaps'], analysis['keys'], analysis['compliance'], detection, tokens, '.', suggested_questions=questions)
Path('legalgraph-out/LEGAL_REPORT.md').write_text(report, encoding='utf-8')
Path('legalgraph-out/.legalgraph_labels.json').write_text(json.dumps({str(k): v for k, v in labels.items()}, ensure_ascii=False), encoding='utf-8')
print('Report updated with domain labels')
"
```

Replace `LABELS_DICT` with your constructed dict.

### Step 6 - Generate HTML visualization (unless --no-viz)

```bash
legalgraph export html
```

### Step 7 - Save manifest, update cost tracker, clean up

```bash
$(cat legalgraph-out/.legalgraph_python) -c "
import json
from pathlib import Path
from datetime import datetime, timezone
from legalgraph.detect import save_manifest

detect = json.loads(Path('legalgraph-out/.legalgraph_detect.json').read_text(encoding='utf-8'))
save_manifest(detect.get('all_files') or detect['files'])

extract = json.loads(Path('legalgraph-out/.legalgraph_extract.json').read_text(encoding='utf-8'))
input_tok = extract.get('input_tokens', 0)
output_tok = extract.get('output_tokens', 0)

cost_path = Path('legalgraph-out/cost.json')
if cost_path.exists():
    cost = json.loads(cost_path.read_text(encoding='utf-8'))
else:
    cost = {'runs': [], 'total_input_tokens': 0, 'total_output_tokens': 0}

cost['runs'].append({
    'date': datetime.now(timezone.utc).isoformat(),
    'input_tokens': input_tok,
    'output_tokens': output_tok,
    'files': detect.get('total_files', 0),
})
cost['total_input_tokens'] += input_tok
cost['total_output_tokens'] += output_tok
cost_path.write_text(json.dumps(cost, indent=2, ensure_ascii=False), encoding='utf-8')

print(f'This run: {input_tok:,} in, {output_tok:,} out tokens')
print(f'All time: {cost[\"total_input_tokens\"]:,} in, {cost[\"total_output_tokens\"]:,} out ({len(cost[\"runs\"])} runs)')
"
rm -f legalgraph-out/.legalgraph_detect.json legalgraph-out/.legalgraph_extract.json legalgraph-out/.legalgraph_structural.json legalgraph-out/.legalgraph_semantic.json legalgraph-out/.legalgraph_analysis.json
find legalgraph-out -maxdepth 1 -name '.legalgraph_chunk_*.json' -delete 2>/dev/null
```

Report to user:
```
Legal graph complete. Outputs in PATH_TO_DIR/legalgraph-out/

  legal.html            - interactive graph visualization
  LEGAL_REPORT.md       - analysis report
  graph.json            - raw graph data
```

Then paste these sections from LEGAL_REPORT.md into the chat:
- Key Clauses
- Detected Conflicts
- Compliance Gaps
- Suggested Questions

Do NOT paste the full report. Keep it concise.

Offer to explore: pick the most interesting conflict or gap and ask:

> "The most critical finding: **[conflict/gap]**. Want me to trace the clauses involved?"

If yes, run `/legalgraph query "[description]"` and walk them through the answer.

---

## Interpreter guard for subcommands

Before running any subcommand (`--update`, `query`, `path`, `obligations`, `conflicts`, `explain`), check that `.legalgraph_python` exists:

```bash
if [ ! -f legalgraph-out/.legalgraph_python ]; then
    PYTHON="python3"
    LEGALGRAPH_BIN=$(which legalgraph 2>/dev/null)
    if [ -n "$LEGALGRAPH_BIN" ]; then
        PYTHON=$(head -1 "$LEGALGRAPH_BIN" | tr -d '#!')
        case "$PYTHON" in *[!a-zA-Z0-9/_.-]*) PYTHON="python3" ;; esac
    fi
    mkdir -p legalgraph-out
    "$PYTHON" -c "import sys; open('legalgraph-out/.legalgraph_python', 'w', encoding='utf-8').write(sys.executable)"
fi
```

## For --update

Re-extracts only new or changed files. See `references/update.md`.

## For --conflicts-only

Skip full extraction, load existing graph, run conflict detection:

```bash
legalgraph analyze conflicts
# or scoped: legalgraph analyze conflicts --domain GDPR
```

---

## For /legalgraph query

When `legalgraph-out/graph.json` exists and the user asks a legal question:

```bash
legalgraph query "<question>"
```

## For /legalgraph obligations

Find all obligations, permissions, and prohibitions for a given role or department:

```bash
legalgraph query "obligations for <role>" --dfs --budget 2000
```

## For /legalgraph path

Trace the relationship chain between two clauses:

```bash
legalgraph path "Clause A" "Clause B"
```

## For /legalgraph conflicts

Check for contradictory provisions:

```bash
legalgraph analyze conflicts
# Domain-scoped: legalgraph analyze conflicts --domain <domain>
```

## For /legalgraph explain

Plain-language explanation of a clause or concept:

```bash
legalgraph explain "<clause name or topic>"
```