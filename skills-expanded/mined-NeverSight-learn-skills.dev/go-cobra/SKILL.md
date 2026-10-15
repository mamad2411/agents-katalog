---
name: go-cobra
description: Write, scaffold, and debug Go CLI applications using the spf13/cobra library. Use this skill whenever the user wants to build a command-line interface in Go, add commands/subcommands, work with flags (persistent, local, required), implement shell completions, generate documentation, or asks anything about cobra-based CLI development.
source: local
license: MIT
---

# Cobra CLI Framework Skill

Write, scaffold, and debug Go CLI applications using the spf13/cobra library. Use this skill whenever the user wants to build a command-line interface in Go, add commands/subcommands to a CLI, work with flags (persistent, local, required), implement shell completions, generate documentation, or asks anything about cobra-based CLI development -- even if they just say "I want to build a CLI tool" or "how do I add commands to my Go app".

---

## Quick Start

### Installation

```bash
go get -u github.com/spf13/cobra@latest
```

For the CLI generator (optional but recommended for scaffolding):
```bash
go install github.com/spf13/cobra-cli@latest
```

### Project Structure

```
myapp/
  cmd/
    root.go       # Root command and Execute()
    version.go    # Additional commands
    serve.go
  main.go         # Just calls cmd.Execute()
```

### Minimal main.go

```go
package main

import "myapp/cmd"

func main() {
    cmd.Execute()
}
```

### Minimal root.go

```go
package cmd

import (
    "fmt"
    "os"
    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "A brief description of your application",
    Long:  `A longer description that spans multiple lines.`,
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Println("Hello from myapp!")
    },
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}
```

---

## Core Concepts

**Commands** represent actions. **Args** are things. **Flags** modify behavior.

Pattern: `APPNAME COMMAND ARG --FLAG`

Examples:
- `hugo server --port=1313` — "server" is command, "port" is flag
- `git clone URL --bare` — "clone" is command, "URL" is arg, "bare" is flag

---

## Command Structure

### Creating Commands

```go
var serveCmd = &cobra.Command{
    Use:   "serve",                           // How to call it
    Short: "Start the server",                // One-line help
    Long:  `Detailed description here...`,   // Full help text
    Example: `  myapp serve --port 8080`,    // Usage examples
    Run: func(cmd *cobra.Command, args []string) {
        // Command logic here
    },
}

func init() {
    rootCmd.AddCommand(serveCmd)
}
```

### Key Command Fields

| Field | Purpose |
|-------|---------|
| `Use` | Usage pattern: `"command [args]"` |
| `Aliases` | Alternative names: `[]string{"s", "srv"}` |
| `Short` | Brief description for help listings |
| `Long` | Full description for `--help` |
| `Example` | Usage examples (indent with 2 spaces) |
| `Run` | The actual command logic |
| `RunE` | Same as Run but returns error |
| `Args` | Positional argument validation |
| `ValidArgs` | Static list for shell completion |
| `ValidArgsFunction` | Dynamic completion function |
| `Hidden` | Hide from help output |
| `Deprecated` | Mark as deprecated with message |
| `Version` | Version string (enables --version) |

### Run vs RunE

Use `RunE` when you need to return errors to the caller:

```go
var tryCmd = &cobra.Command{
    Use:   "try",
    Short: "Try something",
    RunE: func(cmd *cobra.Command, args []string) error {
        if err := doSomething(); err != nil {
            return err  // Error handled by Cobra
        }
        return nil
    },
}
```

---

## Flags

### Flag Types

**Persistent Flags** — Available to this command AND all subcommands:
```go
rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file path")
rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")
```

**Local Flags** — Only for this specific command:
```go
serveCmd.Flags().IntVarP(&port, "port", "p", 8080, "port to listen on")
serveCmd.Flags().StringVar(&host, "host", "localhost", "host address")
```

### Flag Methods

| Method | Example |
|--------|---------|
| `StringVar` | `--name value` |
| `StringVarP` | `--name value` or `-n value` |
| `BoolVar` | `--verbose` (true) or `--verbose=false` |
| `IntVar` | `--count 5` |
| `StringSliceVar` | `--tag a --tag b` or `--tag a,b` |
| `StringArrayVar` | `--tag a --tag b` (no comma splitting) |
| `CountVarP` | `-v` (1), `-vv` (2), `-vvv` (3) |

### Required Flags

```go
cmd.Flags().StringVarP(&region, "region", "r", "", "AWS region")
cmd.MarkFlagRequired("region")

// For persistent flags
cmd.MarkPersistentFlagRequired("config")
```

### Flag Groups

```go
// Must be used together
cmd.MarkFlagsRequiredTogether("username", "password")

// Cannot be used together
cmd.MarkFlagsMutuallyExclusive("json", "yaml")

// At least one required
cmd.MarkFlagsOneRequired("json", "yaml")

// Exactly one required (combine both)
cmd.MarkFlagsOneRequired("json", "yaml")
cmd.MarkFlagsMutuallyExclusive("json", "yaml")
```

### Count Flags (Verbosity Pattern)

```go
var verbose int

func init() {
    rootCmd.PersistentFlags().CountVarP(&verbose, "verbose", "v", "verbosity (-v, -vv, -vvv)")
}

// Usage:
// myapp -v     → verbose = 1
// myapp -vv    → verbose = 2
// myapp -vvv   → verbose = 3
```

---

## Positional Arguments

### Built-in Validators

```go
cmd.Args = cobra.NoArgs              // No args allowed
cmd.Args = cobra.ArbitraryArgs       // Any args (default)
cmd.Args = cobra.MinimumNArgs(1)     // At least N
cmd.Args = cobra.MaximumNArgs(3)     // At most N
cmd.Args = cobra.ExactArgs(2)        // Exactly N
cmd.Args = cobra.RangeArgs(1, 3)     // Between min and max
cmd.Args = cobra.OnlyValidArgs       // Only from ValidArgs list
```

### Combining Validators

```go
cmd.Args = cobra.MatchAll(cobra.ExactArgs(2), cobra.OnlyValidArgs)
```

### Custom Validator

```go
cmd.Args = func(cmd *cobra.Command, args []string) error {
    if len(args) < 1 {
        return fmt.Errorf("requires at least 1 arg")
    }
    if !isValidInput(args[0]) {
        return fmt.Errorf("invalid argument: %s", args[0])
    }
    return nil
}
```

---

## Lifecycle Hooks

Hooks execute in this order:
1. `PersistentPreRun` (inherited by children)
2. `PreRun`
3. `Run`
4. `PostRun`
5. `PersistentPostRun` (inherited by children)

```go
var rootCmd = &cobra.Command{
    Use: "app",
    PersistentPreRun: func(cmd *cobra.Command, args []string) {
        // Runs before every command (including subcommands)
        initLogging()
    },
    PersistentPostRun: func(cmd *cobra.Command, args []string) {
        // Runs after every command
        cleanup()
    },
}

var subCmd = &cobra.Command{
    Use: "sub",
    PreRun: func(cmd *cobra.Command, args []string) {
        // Only for this command, before Run
    },
    Run: func(cmd *cobra.Command, args []string) {
        // Main logic
    },
}
```

Use `*RunE` variants to return errors:
```go
PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
    return initConfig()
}
```

---

## Viper Integration

Cobra integrates seamlessly with [Viper](https://github.com/spf13/viper) for configuration management. See **[references/viper-integration.md](references/viper-integration.md)** for complete documentation.

```go
import "github.com/spf13/viper"

func init() {
    cobra.OnInitialize(initConfig)
    
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file")
    rootCmd.PersistentFlags().String("author", "Me", "author name")
    
    // Bind flag to viper - priority: flag > env > config > default
    viper.BindPFlag("author", rootCmd.PersistentFlags().Lookup("author"))
}

func initConfig() {
    if cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        home, _ := os.UserHomeDir()
        viper.AddConfigPath(home)
        viper.SetConfigType("yaml")
        viper.SetConfigName(".myapp")
    }
    
    viper.AutomaticEnv()
    viper.ReadInConfig()
}

// IMPORTANT: Use viper.GetString("author"), not the flag variable
// Flag variables are NOT updated from config file values
```

---

## Help & Usage

### Automatic Features

- `--help` / `-h` flag added automatically
- `help` subcommand added when you have subcommands
- Typo suggestions: `myapp srever` → "Did you mean 'server'?"

### Customization

```go
// Custom help template
cmd.SetHelpTemplate(`Custom help: {{.Use}}`)

// Custom usage template
cmd.SetUsageTemplate(`Usage: {{.UseLine}}`)

// Custom help function
cmd.SetHelpFunc(func(cmd *cobra.Command, args []string) {
    fmt.Println("Custom help!")
})

// Disable suggestions
cmd.DisableSuggestions = true

// Adjust suggestion distance
cmd.SuggestionsMinimumDistance = 1
```

### Version Flag

```go
var rootCmd = &cobra.Command{
    Use:     "myapp",
    Version: "1.0.0",  // Enables --version flag
}

// Custom version template
cmd.SetVersionTemplate(`Version: {{.Version}}`)
```

### Grouping Commands

```go
rootCmd.AddGroup(&cobra.Group{ID: "core", Title: "Core Commands:"})
rootCmd.AddGroup(&cobra.Group{ID: "util", Title: "Utility Commands:"})

serveCmd.GroupID = "core"
versionCmd.GroupID = "util"
```

---

## Shell Completions

Cobra automatically provides a `completion` command. For detailed shell completion implementation, see `references/completions.md`.

Quick usage:
```bash
# Bash
source <(myapp completion bash)

# Zsh  
myapp completion zsh > "${fpath[1]}/_myapp"

# Fish
myapp completion fish > ~/.config/fish/completions/myapp.fish

# PowerShell
myapp completion powershell | Out-String | Invoke-Expression
```

### Dynamic Completions

```go
cmd.ValidArgsFunction = func(cmd *cobra.Command, args []string, toComplete string) ([]cobra.Completion, cobra.ShellCompDirective) {
    if len(args) != 0 {
        return nil, cobra.ShellCompDirectiveNoFileComp
    }
    return []cobra.Completion{"option1", "option2"}, cobra.ShellCompDirectiveNoFileComp
}
```

---

## Documentation Generation

Cobra can generate man pages, markdown, and more. See `references/docgen.md` for details.

Quick example:
```go
import "github.com/spf13/cobra/doc"

// Markdown
doc.GenMarkdownTree(rootCmd, "./docs")

// Man pages
header := &doc.GenManHeader{Title: "MYAPP", Section: "1"}
doc.GenManTree(rootCmd, header, "./man")
```

---

## Creating Plugins

For tools like kubectl that use plugins (`kubectl-myplugin` called as `kubectl myplugin`):

```go
rootCmd := &cobra.Command{
    Use: "kubectl-myplugin",
    Annotations: map[string]string{
        cobra.CommandDisplayNameAnnotation: "kubectl myplugin",
    },
}
```

---

## Global Settings

```go
// Enable case-insensitive command matching
cobra.EnableCaseInsensitive = true

// Enable prefix matching (dangerous for production)
cobra.EnablePrefixMatching = true

// Execute all parent hooks (not just first found)
cobra.EnableTraverseRunHooks = true

// Disable command sorting in help
cobra.EnableCommandSorting = false
```

---

## Testing Commands

```go
func TestServeCommand(t *testing.T) {
    cmd := rootCmd
    
    // Capture output
    buf := new(bytes.Buffer)
    cmd.SetOut(buf)
    cmd.SetErr(buf)
    
    // Set args
    cmd.SetArgs([]string{"serve", "--port", "9000"})
    
    // Execute
    err := cmd.Execute()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    
    // Check output
    if !strings.Contains(buf.String(), "expected") {
        t.Errorf("unexpected output: %s", buf.String())
    }
}
```

---

## Context Support

```go
var rootCmd = &cobra.Command{
    Use: "myapp",
    Run: func(cmd *cobra.Command, args []string) {
        ctx := cmd.Context()
        // Use context for cancellation, timeouts, etc.
    },
}

// Execute with context
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()
rootCmd.ExecuteContext(ctx)
```

---

## Common Patterns

### Subcommand Organization

For large apps, organize subcommands in separate packages:

```
cmd/
  root.go
  config/
    config.go      # Defines configCmd
    get.go         # config get
    set.go         # config set
```

```go
// cmd/config/config.go
var ConfigCmd = &cobra.Command{Use: "config", Short: "Manage configuration"}

func init() {
    ConfigCmd.AddCommand(getCmd)
    ConfigCmd.AddCommand(setCmd)
}

// cmd/root.go
import "myapp/cmd/config"

func init() {
    rootCmd.AddCommand(config.ConfigCmd)
}
```

### Error Handling

```go
func Execute() {
    if err := rootCmd.Execute(); err != nil {
        // Error already printed by Cobra
        os.Exit(1)
    }
}

// To silence automatic error printing:
rootCmd.SilenceErrors = true
rootCmd.SilenceUsage = true
```

### Silent/Quiet Mode

```go
var quiet bool

func init() {
    rootCmd.PersistentFlags().BoolVarP(&quiet, "quiet", "q", false, "suppress output")
}

func output(msg string) {
    if !quiet {
        fmt.Println(msg)
    }
}
```

---

## Reference Files

For more detailed information on specific topics:

- `references/completions.md` — Shell completion implementation details
- `references/docgen.md` — Documentation generation (man, markdown, yaml, rst)
- `references/advanced.md` — Advanced patterns and edge cases
