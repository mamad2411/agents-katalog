---
name: json-deep-sort
description: Alphabetically sorts primitive JSON arrays and recursively applies sort_keys=True for unified dictionary ordering safely natively.
category: Data Processing
---

# JSON Deep Sort Skill

## 1. Scope Statement

This skill establishes the standard protocol for autonomously scanning, parsing, and deep-sorting JSON configuration
files natively via a pure Python script. It guarantees that any array composed purely of primitives (strings, ints,
booleans) is sorted alphabetically, while recursively applying `sort_keys=True` to guarantee identical alphabetic
sorting across all nested dictionaries internally.

It explicitly bypasses third-party npm packages (like `jq` or `prettier`), providing an industrial, ultra-lean
fallback mechanism relying exclusively on native Python structures.

***

## 2. Environment & Dependencies

Before execution, the agent MUST verify:

- **Python Verification**: Ensure python is available natively (`python --version` or `python3 --version`). Minimum
  required version is Python 3.7 (which natively guarantees dictionary insertion order stability).
- **No External Packages**: This script executes entirely natively using standard built-in libraries (`json`, `sys`).
  No `pip install` required.

***

## 3. Command Syntax & Execution

To execute the global JSON Deep Sort, use the following Ultra-Lean inline script physically via `run_command`:

```bash
python -c '
import json
import sys

def sort_arrays(data):
    if isinstance(data, dict):
        return {k: sort_arrays(v) for k, v in data.items()}
    elif isinstance(data, list):
        if all(isinstance(x, (str, int, float, bool)) for x in data):
            try:
                return sorted(data, key=lambda x: str(x).lower() if isinstance(x, str) else x)
            except TypeError:
                return sorted(data)
        else:
            return [sort_arrays(x) for x in data]
    return data

for fp in sys.argv[1:]:
    with open(fp, "r") as f:
        data = json.load(f)
    print("Loaded", fp)
    data = sort_arrays(data)
    with open(fp, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)
        f.write("\n")
    print("Recursively sorted arrays and object keys. Saved", fp)
' "path/to/target1.json" "path/to/target2.json"
```

### 3.1 Deep Command Explanation Mandate

The exact semantic logic broken down block by block:

- `import json` / `import sys`: Invokes native system parsing capabilities bypassing external binaries.
- `sort_arrays(data)`: A recursive interceptor actively tracking the exact current datatype boundary natively.
- `if isinstance(data, dict)`: Dictates recursive drilling; immediately parses all sub-paths without mutating.
- `if isinstance(data, list)`: Validates that the list acts as a primitive holder (no deeply nested arbitrary
  objects) to prevent breaking syntax layouts unrecoverably.
- `sorted(data, key=lambda x: str(x).lower())`: Maps explicitly case-insensitive alphabetical bounds uniformly
  across arbitrary elements.
- `json.dump(..., sort_keys=True)`: Overrides standard output buffers explicitly enforcing immediate nested
  dictionary key sorting implicitly globally.

***

## 4. Execution Protocol

1. **Locate JSON Path(s)**: Identify correctly formatted JSON payloads. Check for block comments (`//`) which break
   native Python JSON parsers and fail execution.
2. **Execute Python Inline**: Run the target script referencing absolute boundaries structurally via `.argv`.
3. **Verify Standard Reformatting**: Read the resulting file back explicitly via `view_file` to guarantee standard
   indentions (4 spaces) match structural intent flawlessly.
