---
name: skill-system-debug
description: Debugging toolkit for AI agents. Diagnose symptoms via memory search + codebase grep, trace data flow, git-bisect bad commits, and compare output directories.
license: MIT
metadata:
  os: linux, macos, windows
---

# skill-system-debug

Debugging toolkit for AI agents: diagnose, trace, bisect, compare.

## Operations

### diagnose

Search memory (5-dimension diagnostic) + grep codebase to generate ranked hypotheses.

```bash
python3 scripts/debug_tool.py diagnose --symptom "alert file missing" --context "pipeline run"
```

### trace

Walk backward through data flow from an output file to its influencing inputs.

```bash
python3 scripts/debug_tool.py trace --output-file reports/profile.yaml --input-files data/train.csv
```

### bisect

Run `git bisect` to find the first bad commit given a test command.

```bash
python3 scripts/debug_tool.py bisect --good abc123 --bad def456 --test "pytest tests/ -q"
```

### compare

Compare two directories (senior reference vs current) and highlight key differences.

```bash
python3 scripts/debug_tool.py compare --senior reports/senior/ --current reports/current/ --format json
```

```skill-manifest
{
  "schema_version": "2.0",
  "id": "skill-system-debug",
  "version": "0.1.0",
  "capabilities": ["debug-diagnose", "debug-trace", "debug-bisect", "debug-compare"],
  "effects": ["proc.exec", "fs.read", "db.read"],
  "operations": {
    "diagnose": {
      "description": "Diagnose a symptom using 5-dimension memory search and codebase grep. Returns ranked hypotheses with confidence scores.",
      "input": {
        "symptom": { "type": "string", "required": true, "description": "Symptom description" },
        "context": { "type": "string", "required": false, "description": "Additional context" }
      },
      "output": {
        "description": "JSON with hypotheses list, memories_found count, code_matches count",
        "fields": { "hypotheses": "array", "memories_found": "integer", "code_matches": "integer" }
      },
      "entrypoints": {
        "unix": ["python3", "scripts/debug_tool.py", "diagnose", "--symptom", "{symptom}"],
        "windows": ["python3", "scripts/debug_tool.py", "diagnose", "--symptom", "{symptom}"]
      }
    },
    "trace": {
      "description": "Trace data flow from an output file back to influencing input files.",
      "input": {
        "output_file": { "type": "string", "required": true, "description": "Output file to trace from" },
        "input_files": { "type": "array", "required": false, "description": "Known input files" }
      },
      "output": {
        "description": "JSON with files list, transforms list, depth integer",
        "fields": { "files": "array", "transforms": "array", "depth": "integer" }
      },
      "entrypoints": {
        "unix": ["python3", "scripts/debug_tool.py", "trace", "--output-file", "{output_file}"],
        "windows": ["python3", "scripts/debug_tool.py", "trace", "--output-file", "{output_file}"]
      }
    },
    "bisect": {
      "description": "Run git bisect to find the first bad commit.",
      "input": {
        "good": { "type": "string", "required": true, "description": "Known good commit" },
        "bad": { "type": "string", "required": true, "description": "Known bad commit" },
        "test": { "type": "string", "required": true, "description": "Test command (exit 0=good, 1=bad)" }
      },
      "output": {
        "description": "JSON with commit, author, date, message, is_first_bad",
        "fields": { "commit": "string", "author": "string", "date": "string", "message": "string", "is_first_bad": "boolean" }
      },
      "entrypoints": {
        "unix": ["python3", "scripts/debug_tool.py", "bisect", "--good", "{good}", "--bad", "{bad}", "--test", "{test}"],
        "windows": ["python3", "scripts/debug_tool.py", "bisect", "--good", "{good}", "--bad", "{bad}", "--test", "{test}"]
      }
    },
    "compare": {
      "description": "Compare two directories and highlight key differences.",
      "input": {
        "senior": { "type": "string", "required": true, "description": "Senior/reference directory" },
        "current": { "type": "string", "required": true, "description": "Current directory" },
        "format": { "type": "string", "required": false, "default": "text", "description": "text | json | csv" }
      },
      "output": {
        "description": "JSON with key_diffs list and summary counts",
        "fields": { "key_diffs": "array", "summary": "object" }
      },
      "entrypoints": {
        "unix": ["python3", "scripts/debug_tool.py", "compare", "--senior", "{senior}", "--current", "{current}"],
        "windows": ["python3", "scripts/debug_tool.py", "compare", "--senior", "{senior}", "--current", "{current}"]
      }
    }
  }
}
```
