---
name: yq
description: >-
  Safely parse, edit, merge, and transform YAML files using yq,
  providing robust command-line examples for extraction and in-place modifications.
  You MUST load this skill when using the yq tool.
license: MIT
---

# yq

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

Safely parse, edit, merge, and transform YAML files using yq, providing robust command-line examples for extraction and in-place modifications.

## WHEN TO USE

- Automating modifications to YAML configuration files in CI/CD pipelines.
- Extracting specific values from complex or deeply nested YAML structures.
- Merging multiple YAML files programmatically.
- Converting between JSON and YAML formats in shell scripts.

## WHEN NOT TO USE

- When writing full-fledged Python or Node.js scripts (use native YAML parsing libraries instead).
- When dealing with malformed or non-compliant YAML files (fix the files first).
- Simple string replacements where the YAML structure is flat and strictly controlled (though `yq` is still safer).
- Simple text files that are not YAML (use `sed` instead).
- JSON files where `jq` is preferred (though `yq` works).
- Writing complex logic better suited for `python`.

## Core Principles

- **Use yq**: Rely on `yq` (mikefarah/yq) for robust, correct YAML parsing rather than fragile tools like `grep` or `sed` to avoid breaking structure or indentation.
- **In-Place Modification**: Use the `-i` flag for editing YAML files in-place cleanly, which preserves comments and structure where supported.
- **Robust Selectors**: Use precise selectors and filters to retrieve values safely, even with deeply nested or optional fields.
- **Conversion Options**: Leverage `yq` to easily convert between JSON and YAML formats without custom scripting.

## Commands / Usage Patterns

- **Extracting a value**:
  `yq '.path.to.key' config.yaml`
- **Modifying a value in-place**:
  `yq -i '.path.to.key = "new_value"' config.yaml`
- **Adding a new array item**:
  `yq -i '.my_array += ["new_item"]' config.yaml`
- **Deleting a key**:
  `yq -i 'del(.path.to.key)' config.yaml`
- **Filtering an array of objects**:
  `yq '.items[] | select(.name == "target_name")' config.yaml`
- **Converting YAML to JSON**:
  `yq -o=json '.' config.yaml`
- **Converting JSON to YAML**:
  `yq -P '.' config.json`
- **Merging two YAML files (mikefarah/yq)**:
  `yq eval-all 'select(fileIndex == 0) * select(fileIndex == 1)' file1.yaml file2.yaml`

## What to Avoid

- Using `sed`, `awk`, or `grep` to modify YAML structures, as these tools are not schema-aware and often break indentation.
- Hardcoding complex bash string manipulation for YAML extraction.

## Common Pitfalls

- **Syntax Confusion**: Mixing `kislyuk/yq` (Python) syntax with `mikefarah/yq` (Go) syntax. They are different tools; this skill assumes `mikefarah/yq`.
- **Losing Comments**: Depending on the version and flags used, in-place edits might strip comments or reformat the file unexpectedly. Always test non-destructively first.
- **Quoting Issues**: Failing to properly escape quotes in shell wrappers around `yq` commands, leading to syntax errors.

## Limitations

- Ensure you are using the Go version of `yq` (`mikefarah/yq`) rather than the Python wrapper (`kislyuk/yq`), as the CLI syntax and capabilities differ significantly.
