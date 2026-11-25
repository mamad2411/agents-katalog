---
name: "cli-help-patterns"
description: "CLI help conventions: POSIX usage lines, GNU long and short option naming, alignment, documenting defaults and required options, examples, environment variables, exit codes, subcommand help, and anti-patterns. Use when writing --help output or man pages."
---

# CLI Help Text Patterns

## POSIX Usage Line Conventions

The usage line is the most compact expression of a command's interface. Know the notation:

| Notation | Meaning | Example |
|----------|---------|---------|
| `[item]` | Optional | `[--verbose]` |
| `<item>` | Required placeholder | `<source>` |
| `item...` | Repeatable | `FILE...` |
| `a\|b` | Mutually exclusive | `--json\|--yaml` |
| `{a,b,c}` | One of these required | `{start,stop,status}` |

```
# Simple command
USAGE: compress [OPTIONS] FILE [OUTPUT]

# Subcommand pattern
USAGE: tool <command> [ARGS]...

# Mutually exclusive
USAGE: format [--json | --yaml | --csv] FILE

# Repeatable
USAGE: tag [--label KEY=VALUE]... IMAGE
```

## Option Naming Conventions

### GNU long option rules
- All lowercase, hyphen-separated: `--dry-run` not `--dryRun` or `--dry_run`
- Every short option should have a corresponding long option
- Boolean flags: `--verbose` (set), `--no-verbose` (unset)
- Options taking values: `--output FILE` or `--output=FILE` (both forms work)

### Short option letter conventions (POSIX tradition)
```
-v  verbose/version
-h  help
-o  output
-n  count/number/dry-run
-f  file/force
-r  recursive/reverse
-q  quiet
-d  debug/directory
-c  config/count
-e  expression/environment
-i  interactive/input
-l  list/long
-p  port/path/pretty
```

## Alignment and Formatting

### Option description alignment
Align all descriptions at a consistent column. The standard is 24-30 characters:

```
# Bad: misaligned
-v, --verbose   Verbose output
-o, --output FILE  Output path
-h, --help  Help

# Good: aligned at column 24
  -v, --verbose         Enable verbose output
  -o, --output FILE     Write output to this path
  -h, --help            Show this message and exit
```

### Documenting defaults
Every option with a default must show it:

```
# Bad: developer has to test to find the default
  --format TEXT   Output format

# Good: default visible in help text
  --format TEXT   Output format: json, yaml, or csv  [default: json]
  --timeout INT   Request timeout in seconds         [default: 30]
  --workers INT   Number of parallel workers         [default: CPU count]
```

### Required option marking
```
  --api-key TEXT  API authentication key  [required]
  --endpoint URL  Target API endpoint     [required]
```

## Examples Section Best Practices

The examples section is the highest-ROI part of help text. Most users jump here first.

```
# Bad examples: generic, don't show real use
EXAMPLES:
  mycli --option VALUE
  mycli --flag

# Good examples: real inputs, comments, common scenarios
EXAMPLES:
  # Process a single file with default settings
  mycli data.csv

  # Convert to JSON with custom output path
  mycli data.csv --format json --output result.json

  # Process multiple files in parallel (uses all CPU cores)
  mycli --workers 0 *.csv --output-dir ./processed/

  # Dry run to preview what would be processed
  mycli --dry-run data.csv
```

## Environment Variable Documentation

Document environment variables that affect behavior:

```
ENVIRONMENT VARIABLES:
  MYCLI_API_KEY    API key (overrides --api-key flag)
  MYCLI_ENDPOINT   API endpoint URL [default: https://api.example.com]
  MYCLI_LOG_LEVEL  Log verbosity: debug, info, warn, error [default: info]
  NO_COLOR         Disable ANSI color output when set (any value)
```

The `NO_COLOR` convention (no-color.org) should be respected by any terminal tool that outputs color.

## Exit Code Documentation

```
EXIT CODES:
  0    Success
  1    Runtime error (see stderr for details)
  2    Invalid arguments or missing required options
  3    Authentication failed
  4    Resource not found
  5    Permission denied
  130  Interrupted (Ctrl+C, SIGINT)
```

Exit code 130 = 128 + SIGINT(2). Tools that handle SIGINT should exit 130, not 1.

## Subcommand Help Pattern

Tools with subcommands should provide two layers of help:

```
# Top-level help
USAGE: mycli [OPTIONS] COMMAND [ARGS]...

  Development toolkit for the Acme platform.

OPTIONS:
  --config PATH   Config file path  [default: ~/.myclirc]
  --debug         Enable debug output
  -h, --help      Show this message and exit
  --version       Show version and exit

COMMANDS:
  deploy   Deploy to a target environment
  migrate  Run database migrations
  logs     Stream application logs
  status   Check deployment health

Run 'mycli COMMAND --help' for command-specific help.

# Subcommand help
USAGE: mycli deploy [OPTIONS] ENVIRONMENT

  Deploy the application to a target environment.
  ...
```

## Anti-Patterns

### Cryptic option names
```
# Bad
-m, --mtype TEXT    Message type

# Good
-t, --message-type TEXT   Message type: info, warn, error, debug
```

### Missing context for destructive operations
```
# Bad: no warning in help text
  -f, --force   Force operation

# Good: the danger is visible
  -f, --force   Skip confirmation and overwrite existing data (irreversible)
```

### No examples
A command with no `EXAMPLES` section makes every user figure out syntax independently. The developer who wrote the tool has already solved this problem for every user who reads an example.

### Truncated descriptions at 80 chars
```
# Bad: wraps at 80, misaligns on wider terminals
  --output-format TEXT   Output format for the report. Supported: json, yaml, csv, tsv, xml [def

# Good: use terminal width awareness or wrap with consistent indentation
  --output-format TEXT   Output format: json, yaml, csv, tsv, xml
                         [default: json]
```

### Undocumented config file precedence
Always document the precedence order when multiple sources can configure the same value:

```
CONFIGURATION (in order of precedence):
  1. Command-line flags
  2. Environment variables (MYCLI_*)
  3. Project config file (.myclirc in current directory)
  4. User config file (~/.config/mycli/config.yaml)
  5. Built-in defaults
```

## References
- [POSIX Utility Conventions](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)
- [GNU Coding Standards - Command-Line Interfaces](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)
- [BATS-core](https://bats-core.readthedocs.io/)
- [no-color.org](https://no-color.org/) - NO_COLOR convention
- [clig.dev](https://clig.dev/) - CLI guidelines
