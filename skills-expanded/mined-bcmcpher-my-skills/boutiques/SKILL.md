---
name: boutiques
description: >
  Generate a Boutiques schema-version 0.5 JSON descriptor for a CLI tool.
  Invoke when the user asks to create, generate, or write a boutiques descriptor
  or boutiques .json for any command-line tool or program. Accepts a command
  name or a command + subcommand pair (e.g. /boutiques bet or /boutiques git commit).
  Use this skill any time the user mentions "boutiques descriptor", "boutiques json",
  or wants to describe a CLI tool in the Boutiques format.
argument-hint: <command> [subcommand]
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash, Write
---

# Skill: boutiques

Generate a Boutiques schema-version 0.5 JSON descriptor for a CLI tool by inspecting
its help output. Load `references/boutiques-schema.md` at the start of Step 5 when the
tool has more than 10 flags or any ambiguous types; otherwise load it when uncertain
about a field's valid values.

## Steps

### 1. Parse arguments

Extract the command and optional subcommand from $ARGUMENTS.
If $ARGUMENTS is empty, ask the user which command to describe before continuing.

### 2. Get the tool version

```bash
<command> --version 2>&1
```

If that fails or returns nothing, try `-version` or `--version` as a subcommand.
Record the version string. Use `"unknown"` if it cannot be determined.

### 3. Fetch help text

```bash
<command> [subcommand] --help 2>&1
```

If that returns an error or empty output, retry with `-h`. If still unhelpful, try
running with no arguments (`<command> [subcommand] 2>&1`). If the tool requires a TTY
to display help (output is empty or contains "not a terminal"), inform the user and ask
them to paste the help text manually. Capture the full output — you will parse it in step 5.

### 4. Ask for the output path

Before writing anything, ask the user where to save the descriptor.
Suggest a default filename in the current working directory using this pattern:
- Version found: `<command>[-<subcommand>]-<version>.json` (e.g. `flirt-6.0.json`, `git-commit-2.43.0.json`)
- No version: `<command>[-<subcommand>].json`

Convert the version string to kebab-case (replace spaces, underscores, and other
non-alphanumeric characters except `.` with `-`; strip any leading `v`).
Wait for the user's confirmation or a different path.
If the suggested file already exists (`Bash: test -f <path> && echo exists`), warn the
user before overwriting.

### 5. Parse the help text

Extract from the captured help output:

- **Description** — the first paragraph or sentence before the Usage/Options sections.
  If none is obvious, use the tool name and subcommand as the description.
- **Usage pattern** — the `Usage:` line(s). Use this to determine the order and names
  of positional arguments, which must appear in the command-line template in that order.
- **Options/flags** — each entry in the Options, Arguments, or Flags section.
  For each, record: short flag (e.g. `-f`), long flag (e.g. `--file`), metavar
  (e.g. `FILE`), and description text.

### 6. Map each argument to a Boutiques input

For each positional argument and option, determine its type using this table:

| Pattern | Boutiques type | Notes |
|---|---|---|
| No value (bare `-v`, `--verbose`) | `Flag` | Boolean; present or absent |
| Metavar contains `FILE`, `PATH`, `DIR`, `IMAGE`, `INPUT`, `OUTPUT` | `File` | |
| Metavar is `N`, `NUM`, `INT`, `COUNT` | `Number` | Set `"integer": true` |
| Metavar is `FLOAT`, `VALUE`, `RATE`, `THRESH`, `SIZE` | `Number` | |
| Metavar exists but does not match the above | `String` | Safe default |

When ambiguous, prefer `String` over `Number`, and `File` if the description
mentions file, path, image, or directory.

For each input, build an object containing at minimum:

```json
{
  "id": "snake_case_from_long_flag_or_positional_name",
  "name": "Human Readable Name",
  "type": "File | String | Number | Flag",
  "value-key": "[UPPER_CASE_ID]",
  "command-line-flag": "--flag-name",
  "description": "Copied from help text.",
  "optional": true
}
```

Rules:
- `id`: snake_case of the long flag name (strip leading `--`). For positional args,
  use the metavar or positional name in snake_case. IDs must be unique.
- `value-key`: the `id` in `UPPER_CASE` wrapped in brackets: `[INPUT_FILE]`
- `command-line-flag`: include for named flags; omit for positional arguments
- `optional`: `false` for positional/required arguments, `true` for optional flags
- For `Number` inputs, add `"integer": true` when the metavar or description implies integers
- For `Number` inputs, add `"minimum"` / `"maximum"` if the help text states a valid range
- For `String` inputs with a fixed set of valid values, add `"value-choices": [...]`
- For flags the tool accepts multiple times (e.g., repeated `-i file1 -i file2`), add
  `"list": true` to the input object

### 6.5. Add input groups for mutually exclusive options

If the help text shows mutually exclusive options (e.g., "use `-T` or `-I` but not both"),
add an `input-groups` entry:

```json
{
  "id": "mode_group",
  "name": "Mode selection",
  "description": "Mutually exclusive mode flags.",
  "mutually-exclusive": true,
  "members": ["flag_t", "flag_i"]
}
```

Load `references/boutiques-schema.md` for `exclusive`, `all-or-none`, and
`one-is-required` group types before writing any `input-groups` entry — do not
invent the syntax from memory.

### 7. Identify output files

Scan the inputs for any whose `id`, flag name, or metavar suggests output
(e.g. `--output`, `--out`, `-o`, `OUTPUT_FILE`, `OUTPUT_IMAGE`).
For each, add an entry to `output-files`:

```json
{
  "id": "output_<name>",
  "name": "Output <Name>",
  "description": "Output file produced by the tool.",
  "path-template": "[OUTPUT_FILE]",
  "optional": false
}
```

### 8. Build the command-line template

Reconstruct the full command as a template string following the usage pattern:

- Start with `<command> [subcommand]`
- Positional args: insert their `value-key` at the position shown in the Usage line
- Named flags with values: `--flag [VALUE_KEY]`
- Flag (boolean) inputs: just `[FLAG_KEY]` — Boutiques substitutes the flag string
  when true and empty string when false
- Keep optional flags after required positionals

Example: `bet [INPUT_IMAGE] [OUTPUT_IMAGE] [FRACTIONAL_INTENSITY] [VERBOSE]`

Verify that every `value-key` in the template has exactly one matching input entry.

### 9. Assemble the descriptor and write

Construct the full JSON object. Required fields:

```json
{
  "name": "<command>[-<subcommand>]",
  "description": "<description from help>",
  "tool-version": "<version or unknown>",
  "schema-version": "0.5",
  "command-line": "<template string>",
  "inputs": [...],
  "output-files": [...]
}
```

Omit `output-files` if none were identified. Omit optional top-level fields
(`author`, `url`, `tags`, etc.) unless you can confidently populate them from
the help text.

Write the JSON to the path confirmed in step 4. Report the path when done and
note any arguments that were ambiguous or could not be fully parsed.

### 9.5. Suggest validation

After writing, tell the user they can validate the descriptor with:
```bash
bosh validate <path>
```
This requires the `boutiques` Python package (`pip install boutiques`). Optional but
recommended — it checks the descriptor against the Boutiques JSON schema.

## Constraints

- Never invent flags or options not present in the help output. If help is
  truncated or missing, tell the user what was captured and ask how to proceed.
- Always confirm the output path before writing. Never silently overwrite.
- Every `value-key` in `command-line` must have a corresponding input; every
  input must have its `value-key` appear in `command-line`.
- Keep `id` values unique. If two flags would produce the same id, append `_2`.
- Produce valid, pretty-printed JSON (2-space indent).
- If the help text is very long or the tool has many subcommands, focus on the
  subcommand specified in $ARGUMENTS and note that other subcommands are not covered.
- For `disables-inputs` / `requires-inputs` dependency relationships, load
  `references/boutiques-schema.md` — do not invent the syntax from memory.
