---
name: code-writer
description: "Delegate boilerplate code generation to a cheap worker model. Use for tests, config, docstrings, type stubs, or any generation where >80% is predictable from reference files."
---

```bash
# Generate and write directly to target file
"${extensionPath:-$HOME/.gemini/extensions/shunt}/plugins/shunt/scripts/code-write" --spec "<what to generate>" --reference <reference-file> --target <output-path>

# Output to stdout instead (omit --target)
"${extensionPath:-$HOME/.gemini/extensions/shunt}/plugins/shunt/scripts/code-write" --spec "<what to generate>" --reference <reference-file>
```

Each call is independent. To build on what was just generated, pass that file as the
`--reference` for the next call.

Review the output and make surgical edits for the ~5-20% that needs your own judgment.
