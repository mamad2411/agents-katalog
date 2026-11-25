---
name: rlm
description: Recursive Language Model loop for large-context tasks. Searches Willow KB first via willow_knowledge_search, then chunks file context and dispatches rlm-subcall (Haiku) per chunk if the KB doesn't fully answer. Use when a query spans more context than fits in the session — corpus archaeology, MIGR1 atoms, large log files, Grove history digests.
---

# RLM — Recursive Language Model Workflow

## Arguments (from $ARGUMENTS)

| Arg | Required | Default | Purpose |
|-----|----------|---------|---------|
| `query=<question>` | yes | — | What to answer |
| `context=<path>` | no | — | Path to large context file |
| `limit=<int>` | no | 10 | Max KB atoms to retrieve |
| `chunk_chars=<int>` | no | 200000 | Characters per chunk |

If arguments are missing, ask for `query` and optionally `context` before proceeding.

## Procedure

### Step 1 — KB retrieval

Call `willow_knowledge_search` with the query and limit. Collect the returned atoms.

Assess coverage: do the atoms answer the query fully?

- **Yes** → synthesize from atoms and stop. Do not proceed to file chunking.
- **No, and no `context` path given** → surface what's missing. Ask the user for a context file path. Stop here until they provide one.
- **No, and `context` path given** → proceed to Step 2.

### Step 2 — Chunk the context file

Write chunk files to `.claude/rlm_state/chunks/`. Create the directory if it doesn't exist.

Run this inline Python to chunk the file:

```bash
python3 - <<'PYEOF'
import sys, os, pathlib

context_path = "<CONTEXT_PATH>"   # substitute $ARGUMENTS[context]
chunk_chars = <CHUNK_CHARS>       # substitute with integer, no quotes (e.g. 200000)
import subprocess
repo_root = pathlib.Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip())
out_dir = repo_root / ".claude/rlm_state/chunks"
out_dir.mkdir(parents=True, exist_ok=True)

# Remove any previous chunks
for f in out_dir.glob("chunk_*.txt"):
    f.unlink()

content = pathlib.Path(context_path).read_text(encoding="utf-8", errors="replace")
total = len(content)
i = 0
start = 0
while start < total:
    end = min(start + chunk_chars, total)
    chunk_path = out_dir / f"chunk_{i:04d}.txt"
    chunk_path.write_text(content[start:end], encoding="utf-8")
    print(f"chunk_{i:04d}.txt: {end - start} chars")
    start = end
    i += 1
print(f"Total: {i} chunks from {total} chars")
PYEOF
```

Substitute the actual values before running. Note the chunk count printed.

### Step 3 — Dispatch rlm-subcall per chunk

For each chunk file (`.claude/rlm_state/chunks/chunk_NNNN.txt`), dispatch the `rlm-subcall` subagent with:

- The user query (verbatim)
- The chunk file path
- Instruction to return compact JSON only

**Do not paste chunk content into the main session.** The subagent reads the file itself via the Read tool.

Collect each subagent's JSON result. Append to a results list.

### Step 4 — Synthesize

Combine:
- KB atoms from Step 1 (cite by title/id)
- `relevant` entries from each chunk result (cite evidence verbatim, ≤25 words)
- `answer_if_complete` fields where non-null

Produce a final answer. Quote only what you cite. If chunks contain conflicting evidence, note it.

### Step 5 — Clean up

After synthesis:

```bash
rm -rf .claude/rlm_state/chunks/
```

## Guards

- Never load raw chunk content into the main session context.
- Subagents cannot spawn further subagents (Claude Code depth limit).
- If a chunk's `relevant` list is empty and `answer_if_complete` is null, skip it — don't quote its `missing` list as evidence.
- Verify `.claude/rlm_state/` is in `.gitignore` before proceeding; add it if missing. Do not commit chunk files.
