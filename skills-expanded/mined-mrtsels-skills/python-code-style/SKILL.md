---
name: python-code-style
description: "Write Python code that reads like a human wrote it — concise, no AI-verbose comments, no numbered section labels, no self-evident docstrings."
category: software-development
---

# Python Code Style: Anti-AI-Verbose

> 本技能为 Python 代码风格类技能的伞,已吸收 `python-code-conventions`(2026-08 合并)。
> 完整原文见 `references/absorbed-*.md`。


Rules for writing Python code that doesn't sound AI-generated. Apply these to all Python files.

## 1. No numbered / labeled section comments

Bad:
```python
# A) Query the endpoint to get a list of sectors
_sectors = requests.get(...).json()

# B) Given a sector, return list of EBITDAs
def get_ebitdas(sector):
    ...

# C) Multi-select component
multi_select = dmc.MultiSelect(...)
```

Good:
```python
_sectors = requests.get(f"{API_BASE}/Sector").json()

def get_ebitdas(sector: str) -> list[int]:
    resp = requests.get(f"{API_BASE}/EBITDA", params={"Sector": sector})
    resp.raise_for_status()
    return resp.json()

multi_select = dmc.MultiSelect(
    id="sector-select",
    label="Select Sectors",
    data=[{"value": s, "label": s} for s in _sectors],
    ...
)
```

## 2. No self-evident comments

Bad: `# import pandas` before `import pandas`
Bad: `# Load the CSV file` before `pd.read_csv("data.csv")`

**If the code itself says it, don't comment it.**

## 3. No AI tutorial tone

Bad:
```python
# First, we create a function that takes a list of numbers and returns their sum
def calculate_total(values):
    # Initialize the sum variable
    total = 0
    # Loop through each value
    for v in values:
        # Add the current value to the running total
        total += v
    # Return the final sum
    return total
```

Good:
```python
def calculate_total(values):
    return sum(values)
```

## 4. No numbered list / outline structures in comments

Bad:
```python
# 1. Parse input
# 2. Transform data
# 3. Return result
```

Good — either no comment, or a single-line intent description if genuinely unclear.

## 5. Keep import blocks clean

No `# External imports` / `# Standard library` / `# Third-party` dividers unless the file genuinely has 15+ imports and grouping helps readability. For normal files (3-10 imports), just list them.

## 6. No docstrings in task scripts

For scripts that implement a task (ingest, API, benchmark, backtest, etc.): **zero docstrings**. No file-level docstring, no function docstring, no class docstring. The code and its context (filename, function name, type hints) IS the documentation.

Bad:
```python
"""Ingest intraday data into DuckDB and MongoDB."""
import duckdb
...

def ingest_duckdb():
    """Load all CSV.zip files into DuckDB."""
    ...
```

Good:
```python
import duckdb
...

def ingest_duck():
    ...
```

Exception: a reusable library/module (`lib.py`, `utils.py`, `helpers.py`) that will be imported by others may have a one-line docstring if the purpose isn't obvious from the name. Task scripts (`main.py`, `api.py`, `benchmark.py`) get zero.

## 7. Functions: label by name, not by comment

The function name IS the documentation. Short names are better — `files()` over `get_ticker_files()`, `ticker()` over `normalize_ticker()`. Prefer 5-12 char names. Avoid `get_`/`set_` prefixes unless the language convention requires it. A docstring that just restates the function name is worse than no docstring — delete it.

**Clarity over brevity in abbreviations.** Domain abbreviations are fine (`idx` for index, `cfg` for config) but never shorten to the point of ambiguity. `ts` → write `timestamp`, `cb` → `callback`. If a reader would pause to decode it, write it out. When a user asks "what is X", that's a clear signal the abbreviation is too aggressive — fix it immediately and remember the rule.

## 8. Short-circuit early, avoid else

Prefer guard clauses over nested if-else.

## 9. `if __name__` block

Keep it minimal — just `main()` call, no surrounding commentary.

## 10. Language: English only

Every comment, docstring, print statement, and error message must be in English. No Chinese or mixed-language comments even if the user is conversing in Chinese. English-only keeps the codebase consistent.

Bad:
```python
# ADF 显著性
ALPHA = 0.05
print(f"共 {len(stocks)} 只")
```

Good:
```python
ALPHA = 0.05
print(f"{len(stocks)} stocks")
```

File-level docstrings: single line in English describing what the script does. No multi-line headers like `"""Subtask A — 相关性矩阵"""`.

Function docstrings: delete when redundant. A docstring like `"""计算对数收益率相关系数矩阵"""` on `compute_correlation()` is worse than none — the function name is the documentation. Keep docstrings only when the logic is genuinely non-obvious, and even then prefer a single line.

## 11. Remove comments that just name the next operation

If the next line of code makes it obvious what's happening, don't comment it.

Bad:
```python
# Convert correlation to distance
dist = squareform(1 - corr)
# Rolling std
if t < lookback:
```

Good:
```python
dist = squareform(1 - corr)
if t < lookback:
```

Comments that explain WHY are valuable. Comments that repeat WHAT the code is already saying are noise.

## 12. No shebang line

Do NOT add `#!/usr/bin/env python3` to `.py` files. Users on Windows cannot use shebangs, and `/usr/bin/env` paths are not portable. Python files should start directly with the docstring or import block.

Bad:
```python
#!/usr/bin/env python3
"""My script."""
```

Good:
```python
"""My script."""
```

## 13. No decorative output banners in scripts

Bad — AI-generated decorative separators:
```python
print("=== DuckDB (time-series columnar) ===")
print("\\n=== MongoDB (NoSQL document) ===")
print(f"{'='*50}")
print("-" * 80)
```

Good — label data directly, no visual dividers:
```python
print(f"duckdb: {n:,} rows")
print(f"mongodb: {n:,} rows")
print(f"ratio: duck {r1}ms  mongo {r2}ms  {r2/r1:.1f}x")
```

Decorative banners (`===`, `---`, `****`, horizontal rules) are an AI-generated formatting pattern. They add noise. Print the data with inline labels — `key: value` is enough to distinguish lines.

## 14. Print messages in English only

All `print()`, logging, and user-facing output must be in English. Even if the user converses in Chinese, script output stays English for consistency with codebases and CI logs.

## 14. Human style applies to all languages, not just Python

The same principle applies to C++, Rust, JavaScript, Makefiles, CMake, shell scripts — any code. Short comments (or none), no Doxygen/JSDoc templates, no decorative section dividers. A C++ `// 行优先矩阵` is better than `// Matrix data structure (row-major storage)`.

## 15. Reports and docs: same rule

No formal report structure (sections/subsection numbering, "Verdict" tables, "Overall: PASS ✅" conclusions, bullet-point conclusions). Write like a dev jotting notes: short sections, raw data, one-line takeaways. If it reads like a template, rewrite it.

## 16. Reports: wrap math in proper LaTeX

When a README or report contains mathematical notation (especially doc/README that may be rendered by a LaTeX-aware viewer), wrap it in `$...$` delimiters:

- `A^T A` → `$A^T A$`
- `σ = sqrt(λ)` → `$\sigma = \sqrt{\lambda}$`
- `A -= σ * u ⊗ v^T` → `$A \leftarrow A - \sigma \cdot u \otimes v^T$`

Raw unicode math (`λ`, `σ`, `v²`, `A^T`) looks unprofessional in a rendered doc. If the doc contains any math at all, all of it should be wrapped.

In code comments, raw unicode math is fine — `// A^T A` is clearer than `// $A^T A$` in a source file.

## 17. Language follows project convention

Check AGENTS.md / CLAUDE.md in the project root for language convention. Some projects use Chinese comments and docs (quant-academy, yuecai). Others require English-only. Follow the project's established convention — rule #10 ("English only") applies per-project, not universally.

## 18. "Still too AI" means cut more — iteratively

If the user says "still has AI vibes" after you trimmed, you didn't trim enough. They will probably say it again after the second pass too. The human threshold is lower than you think.

Cut comments to single words where possible. Remove docstrings entirely from task scripts. Replace structured documentation with raw data and one-liners. The bar is "looks like a tired dev wrote this at 2am" — not "looks like a tired dev who still cares about formatting".

Signs you still have AI traces:
- Section dividers (`---`, `====`, `////`) in code comments
- Every function has a comment (humans leave most functions undocumented)
- Reports have numbered sections, verdict tables, or "Overall: PASS ✅" conclusions
- Docstrings that restate the function name
- Explanatory text between code blocks in README (humans write `## Usage` then just the code)
- Table headers are lowercase (human inconsistency shows; English convention requires Title Case headers)

When the user says "还是 AI 味", the fix is always less: fewer words, fewer comments, less structure, less explanation. Never add more.

## When to use this skill

Load for any session where you're writing, editing, or reviewing code — Python, C++, or any language — especially when the user has previously corrected your comment style or verbosity. If the user says "去AI味", "human style", "写得太AI了", or "too verbose", this skill applies. Pair with the project's AGENTS.md for language and formatting conventions.
