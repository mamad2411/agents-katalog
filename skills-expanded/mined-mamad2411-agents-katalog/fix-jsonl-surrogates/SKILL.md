---
name: fix-jsonl-surrogates
description: "Diagnose and repair 'invalid high surrogate' API errors in Claude Code chat sessions. Use this skill when the user encounters API Error 400 with 'invalid high surrogate in string', 'not valid JSON', surrogate-related errors, or wants to fix/scan/repair a broken Claude Code JSONL chat file. Also use when a session refuses to resume due to JSON encoding errors, or when the user mentions request IDs (req_...) alongside JSON parse failures."
license: CC-BY-SA-4.0
compatibility: Works with any AI coding agent that can run Python 3.8+ scripts
metadata:
  author: Tebjan Halm
  version: "1.0"
---

# Fix JSONL Surrogates

Repairs Claude Code JSONL chat files that contain lone Unicode surrogates (U+D800-U+DFFF),
which cause the Anthropic API to reject requests with "invalid high surrogate in string".

## Background

Node.js internally uses UTF-16 strings. `JSON.stringify()` doesn't validate surrogate pairs,
so lone surrogates from file reads, terminal output, or web content can end up serialized
as `\uD8xx` without a matching low surrogate — producing invalid JSON that the API rejects.

Common triggers on Windows:
- Emoji in code comments or terminal output
- Box-drawing characters from build logs
- Web content with malformed UTF-16 encoding

Upstream issue: anthropics/claude-code#44230

## How to Use

### Quick diagnosis

If the user has a specific session or request ID, find the JSONL file:

```bash
grep -rl "req_XXXXX" ~/.claude/projects/*/
```

### Run the repair script

The bundled Python script handles scanning and fixing. It works on individual files,
session directories, or entire project trees.

```bash
# Scan a specific JSONL file + its session directory (subagents, tool-results)
python {SKILL_DIR}/scripts/fix_surrogates.py <path-to-file.jsonl>

# Dry run first to see what would change
python {SKILL_DIR}/scripts/fix_surrogates.py <path-to-file.jsonl> --dry-run --verbose

# Scan all sessions in a project directory
python {SKILL_DIR}/scripts/fix_surrogates.py ~/.claude/projects/<project-dir>/

# Scan everything recursively (includes subagent files)
python {SKILL_DIR}/scripts/fix_surrogates.py ~/.claude/projects/<project-dir>/ --recursive
```

The script:
1. Reads each file with `errors='surrogateescape'` to preserve bad characters for detection
2. Parses JSON and recursively checks all string values for surrogate code points
3. Replaces lone surrogates with U+FFFD (replacement character) via `str.encode('utf-8', 'surrogatepass').decode('utf-8', 'replace')`
4. Backs up originals as `.bak` before modifying
5. Reports a summary of what was found and fixed

### Important notes

- **Surrogates are often transient**: They may exist only in Node.js memory during request
  construction, not in the stored JSONL. If the script finds nothing, the error was transient
  and retrying the session should work.
- **Check all session artifacts**: The script automatically scans the main JSONL plus any
  subagent files and tool-result cache in the session directory.
- **Safe to re-run**: The script is idempotent. Running it on already-clean files is a no-op.

### Manual investigation

If the script finds nothing but the error persists, the surrogate may come from content
loaded at request time (CLAUDE.md, memory files, etc.). Scan those too:

```bash
python {SKILL_DIR}/scripts/fix_surrogates.py ~/.claude/ --recursive --dry-run
```

### What `{SKILL_DIR}` means

Replace `{SKILL_DIR}` with the actual path to this skill directory. When Claude invokes
this skill, it knows the skill's location and can substitute the correct path.
