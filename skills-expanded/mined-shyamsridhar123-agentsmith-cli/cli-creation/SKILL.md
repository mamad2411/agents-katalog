---
name: cli-creation
description: Build professional command-line interface (CLI) applications following industry best practices. Covers argument parsing, help text, output formatting, error handling, subcommands, configuration, and distribution across multiple languages.
---

# CLI Creation

Build professional, delightful command-line applications that follow established conventions and modern best practices.

## When to Use This Skill

- Creating new CLI tools or utilities
- Adding command-line interfaces to existing applications
- Refactoring CLI programs for better usability
- User asks to "build a CLI", "create a command-line tool", or "add CLI commands"

---

## Core Philosophy

### Human-First Design
Design for humans first, machines second. The CLI is a text-based UI, not just a scripting interface.

### Simple Parts That Work Together
Follow UNIX philosophy: small programs with clean interfaces that compose via pipes and standard I/O.

### Consistency
Follow existing patterns. Terminal conventions are muscle memory—don't break expectations.

### Ease of Discovery
Help users learn. Provide comprehensive help, examples, and suggestions.

### Robustness
Handle errors gracefully. Be responsive. Show progress for long operations.

---

## Project Structure

```
mycli/
├── src/
│   ├── main.{ts,py,go,rs}    # Entry point
│   ├── commands/              # Subcommands
│   │   ├── init.{ts,py,go,rs}
│   │   └── run.{ts,py,go,rs}
│   ├── utils/
│   │   ├── output.{ts,py,go,rs}  # Colors, formatting
│   │   └── config.{ts,py,go,rs}  # Configuration handling
│   └── types.{ts,py,go,rs}
├── tests/
├── README.md
└── package.json / pyproject.toml / go.mod / Cargo.toml
```

---

## Recommended Libraries

| Language | Library | Notes |
|----------|---------|-------|
| **Node.js** | [oclif](https://oclif.io/), [Commander](https://github.com/tj/commander.js) | oclif for complex CLIs, Commander for simple |
| **Python** | [Typer](https://github.com/tiangolo/typer), [Click](https://click.palletsprojects.com/) | Typer uses type hints, Click is battle-tested |
| **Go** | [Cobra](https://github.com/spf13/cobra), [urfave/cli](https://github.com/urfave/cli) | Cobra powers kubectl, Hugo, GitHub CLI |
| **Rust** | [clap](https://docs.rs/clap) | Derive macros for type-safe parsing |
| **Deno** | [parseArgs](https://jsr.io/@std/cli/doc/parse-args) | Built-in standard library |

---

## Arguments and Flags

### Terminology
- **Arguments (args)**: Positional parameters (`cp source dest`)
- **Flags**: Named parameters (`--verbose`, `-f file.txt`)

### Best Practices

```bash
# Prefer flags over positional args for clarity
mycli --input file.txt --output result.json  # ✅ Clear
mycli file.txt result.json                    # ❌ Ambiguous

# Have full-length versions of all flags
mycli -v          # Short form
mycli --verbose   # Long form (prefer in scripts)

# Use standard flag names
-h, --help       # Help
-v, --version    # Version (or use for verbose, pick one)
-q, --quiet      # Suppress output
-f, --force      # Force operation
-n, --dry-run    # Preview without executing
-o, --output     # Output file/path
--json           # JSON output format
--no-color       # Disable colors
```

### Flag Conventions

```typescript
// TypeScript with Commander
import { Command } from 'commander';

const program = new Command()
  .name('mycli')
  .description('A delightful CLI tool')
  .version('1.0.0')
  .option('-v, --verbose', 'Enable verbose output')
  .option('-c, --config <path>', 'Config file path')
  .option('--dry-run', 'Preview changes without applying');
```

```python
# Python with Typer
import typer

app = typer.Typer()

@app.command()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    config: str = typer.Option(None, "--config", "-c", help="Config file path"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Preview changes"),
):
    """A delightful CLI tool."""
    pass
```

```go
// Go with Cobra
var rootCmd = &cobra.Command{
    Use:   "mycli",
    Short: "A delightful CLI tool",
}

func init() {
    rootCmd.PersistentFlags().BoolP("verbose", "v", false, "Enable verbose output")
    rootCmd.PersistentFlags().StringP("config", "c", "", "Config file path")
    rootCmd.Flags().Bool("dry-run", false, "Preview changes")
}
```

---

## Help Text

### Display Help When Asked
Respond to `-h`, `--help`, and `help` subcommand:

```
$ mycli --help
A delightful CLI tool for managing widgets

Usage: mycli [command] [options]

Commands:
  init        Initialize a new project
  build       Build the project
  deploy      Deploy to production

Options:
  -v, --verbose    Enable verbose output
  -c, --config     Path to config file
  -h, --help       Show this help
  --version        Show version

Examples:
  $ mycli init my-project
  $ mycli build --verbose
  $ mycli deploy --dry-run

Run 'mycli <command> --help' for more information on a command.
```

### Help Text Principles

1. **Lead with examples** - Users learn from examples first
2. **Show common flags first** - Most-used options at the top
3. **Be concise by default** - Full help on `--help`, brief on no args
4. **Suggest next steps** - Tell users what to run next
5. **Link to documentation** - Include URLs to web docs

---

## Output

### Human-Readable by Default

```bash
# Check if stdout is a TTY
if [ -t 1 ]; then
  # Interactive terminal - use colors, formatting
else
  # Piped/redirected - plain output
fi
```

### Machine-Readable with `--json`

```bash
$ mycli status
✓ Connected to server
✓ 3 widgets deployed
✓ Last sync: 2 minutes ago

$ mycli status --json
{"connected": true, "widgets": 3, "lastSync": "2025-01-24T10:30:00Z"}
```

### Color Guidelines

```typescript
// Use color with intention
import chalk from 'chalk';

console.log(chalk.green('✓'), 'Success: Widget deployed');
console.log(chalk.yellow('⚠'), 'Warning: Deprecated API');
console.log(chalk.red('✗'), 'Error: Connection failed');

// Respect NO_COLOR environment variable
if (process.env.NO_COLOR || !process.stdout.isTTY) {
  chalk.level = 0;
}
```

### Progress Indicators

```python
from tqdm import tqdm
import time

# Show progress for long operations
for item in tqdm(items, desc="Processing"):
    process(item)
```

---

## Errors

### Write Errors for Humans

```bash
# Bad - cryptic error
Error: ENOENT

# Good - helpful error with suggestion
✗ Error: Cannot find config file 'widget.yaml'
  
  The file doesn't exist at the expected location.
  
  To fix this, either:
    • Run 'mycli init' to create a new config
    • Specify a path with --config <path>
```

### Error Handling Pattern

```typescript
try {
  await deploy();
} catch (error) {
  if (error.code === 'ENOENT') {
    console.error(chalk.red('✗'), `File not found: ${error.path}`);
    console.error('\n  Run "mycli init" to create the required files.\n');
    process.exit(1);
  }
  
  if (error.code === 'ECONNREFUSED') {
    console.error(chalk.red('✗'), 'Cannot connect to server');
    console.error(`\n  Check that the server is running at ${serverUrl}\n`);
    process.exit(1);
  }
  
  // Unexpected error - show debug info
  console.error(chalk.red('✗'), 'Unexpected error:', error.message);
  console.error('\n  Please report this issue:');
  console.error('  https://github.com/org/mycli/issues\n');
  if (process.env.DEBUG) {
    console.error(error.stack);
  }
  process.exit(1);
}
```

---

## Subcommands

### Git-Style Subcommands

```bash
mycli <command> [subcommand] [options]

# Examples
mycli config get theme
mycli config set theme dark
mycli widget list
mycli widget create --name "My Widget"
```

### Subcommand Consistency

```typescript
// Be consistent: noun-verb or verb-noun across all commands
// Noun-verb (recommended for complex CLIs)
mycli config get
mycli config set
mycli widget list
mycli widget create

// Verb-noun
mycli get config
mycli list widgets
```

---

## Configuration

### Configuration Precedence (highest to lowest)

1. Command-line flags
2. Environment variables
3. Project-level config (`.myclirc`, `mycli.config.js`)
4. User-level config (`~/.config/mycli/config.yaml`)
5. System-wide config (`/etc/mycli/config.yaml`)

### XDG Base Directory Spec

```typescript
import os from 'os';
import path from 'path';

const configDir = process.env.XDG_CONFIG_HOME 
  || path.join(os.homedir(), '.config');
const configPath = path.join(configDir, 'mycli', 'config.yaml');
```

### Environment Variables

```bash
# Use MYCLI_ prefix for your app's env vars
MYCLI_API_KEY=xxx
MYCLI_DEBUG=1
MYCLI_NO_COLOR=1

# Check standard env vars
NO_COLOR          # Disable colors
DEBUG             # Enable debug output
EDITOR            # User's preferred editor
```

---

## Interactivity

### Only Prompt in TTY

```typescript
import { stdin, stdout } from 'process';

if (stdin.isTTY && stdout.isTTY) {
  // Interactive mode - can prompt
  const answer = await prompt('Continue? [y/N]');
} else {
  // Non-interactive (script/pipe) - require flags
  if (!options.force) {
    console.error('Use --force to confirm in non-interactive mode');
    process.exit(1);
  }
}
```

### Confirm Dangerous Operations

```typescript
// Mild danger: simple confirmation
const confirm = await prompt('Delete file.txt? [y/N]');

// Moderate danger: require explicit yes
const confirm = await prompt('Delete 47 files? Type "yes" to confirm:');
if (confirm !== 'yes') process.exit(1);

// Severe danger: type the resource name
const confirm = await prompt('Delete production database? Type "prod-db" to confirm:');
if (confirm !== 'prod-db') process.exit(1);

// Always allow --force for scripting
if (options.force) {
  // Skip confirmation
}
```

---

## Signals and Exit Codes

### Exit Codes

```typescript
process.exit(0);  // Success
process.exit(1);  // General error
process.exit(2);  // Misuse of command (bad args)
```

### Handle Ctrl-C Gracefully

```typescript
process.on('SIGINT', async () => {
  console.log('\n\nInterrupted. Cleaning up...');
  await cleanup();
  process.exit(130);  // 128 + signal number
});

// For long cleanup, allow second Ctrl-C to force quit
let interrupted = false;
process.on('SIGINT', () => {
  if (interrupted) {
    console.log('\nForce quitting...');
    process.exit(1);
  }
  interrupted = true;
  console.log('\nGracefully stopping... (press Ctrl+C again to force)');
  gracefulShutdown();
});
```

---

## Distribution

### Single Binary is Best

- **Go**: Compiles to single binary by default
- **Rust**: Compiles to single binary by default
- **Node.js**: Use [pkg](https://github.com/vercel/pkg) or [nexe](https://github.com/nexe/nexe)
- **Python**: Use [PyInstaller](https://www.pyinstaller.org/) or [shiv](https://github.com/linkedin/shiv)

### Package Managers

```bash
# npm (Node.js)
npm install -g mycli

# Homebrew (macOS/Linux)
brew install mycli

# pip (Python)
pip install mycli

# Go
go install github.com/org/mycli@latest
```

### Make Uninstall Easy

Document how to remove your tool at the bottom of install instructions.

---

## Checklist

### Essential (Must Have)

- [ ] Use argument parsing library (don't roll your own)
- [ ] Return exit code 0 on success, non-zero on failure
- [ ] Send output to stdout, errors/logs to stderr
- [ ] Support `-h` and `--help` flags
- [ ] Support `--version` flag
- [ ] Handle Ctrl-C gracefully

### Recommended (Should Have)

- [ ] Provide examples in help text
- [ ] Use colors (respect NO_COLOR)
- [ ] Show progress for long operations
- [ ] Support `--json` for machine-readable output
- [ ] Support `--quiet` to suppress non-essential output
- [ ] Validate input early with helpful errors
- [ ] Suggest corrections for typos

### Nice to Have

- [ ] Shell completions (bash, zsh, fish)
- [ ] Man pages
- [ ] Configuration file support
- [ ] Auto-update mechanism
- [ ] Telemetry (opt-in only!)

---

## Anti-Patterns to Avoid

```bash
# ❌ Don't require specific argument order for flags
mycli --flag subcommand    # This should work
mycli subcommand --flag    # This should also work

# ❌ Don't hide errors in silent failure
mycli dostuff              # *hangs forever with no output*

# ❌ Don't use ambiguous subcommands
mycli update               # Update what?
mycli upgrade              # How is this different?

# ❌ Don't break existing interfaces without warning
mycli --old-flag           # Deprecation warning first, then remove

# ❌ Don't read secrets from command line flags
mycli --password=secret    # Visible in ps, shell history

# ✅ Do read secrets from files or stdin
mycli --password-file=/path/to/secret
echo "secret" | mycli --password-stdin
```

---

## Resources

- [Command Line Interface Guidelines](https://clig.dev/) - Comprehensive CLI design guide
- [12 Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46) - Best practices
- [GNU Coding Standards - CLI](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)
- [Heroku CLI Style Guide](https://devcenter.heroku.com/articles/cli-style-guide)
