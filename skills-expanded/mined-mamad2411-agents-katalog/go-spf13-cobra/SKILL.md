---
name: go-spf13-cobra
description: "cobra command trees — cobra.Command, RunE vs Run, the PreRunE/PostRunE hook chain, Args validators, persistent vs local flags, completions, doc generation, and testing with SetArgs/SetOut/SetErr. Use when building a CLI with spf13/cobra, adding subcommands or flags to an existing tree, or reviewing cobra usage."
license: MIT
---

# spf13/cobra

**Leading word: command.** A CLI is a command tree — a root named after the binary, with subcommands, flags, and validators. The discipline: design the user-facing surface first, then wire each behavior into the right hook, and always use the `*E` variants so errors flow back through cobra instead of `os.Exit`.

## Steps — build a command tree

1. **Design the tree from the root.** The root `Use` is the binary name; register subcommands with `AddCommand`. Add `SilenceUsage: true` and `SilenceErrors: true` on the root so you control error output.
   *Done when: every subcommand is reachable from the root and the help output shows a clean tree.*

2. **Label command groups before registering.** Call `AddGroup` before the `AddCommand` calls that reference them — cobra does not retroactively assign groups.
   *Done when: every group referenced by an `AddCommand` was registered earlier in source order.*

3. **Wire `RunE`, never `Run`.** Non-`E` hooks cannot return an error; the only escapes are `os.Exit` or panic, bypassing defers.
   *Done when: no command uses a non-`E` run hook.*

4. **Validate positional args with `Args`.** Declare `Args: cobra.ExactArgs(1)` etc. — `len(args)` checks inside `RunE` bypass cobra's standard error messages and arg tracking.
   *Done when: every command that takes positional args declares an `Args` validator.*

5. **Declare flags at the right scope.** `PersistentFlags()` inherit to every subcommand; `Flags()` are local. Use `MarkFlagRequired`, `MarkFlagsMutuallyExclusive`, and `MarkFlagsOneRequired` where the semantics demand it.
   *Done when: each flag lives on the command that owns it and required/exclusive flags are marked.*

6. **Wire the hook chain deliberately.** `PersistentPreRunE` on the root runs before every subcommand (config init, auth). A child `PersistentPreRunE` **replaces** the parent's — call the parent's hook explicitly when you need both.
   *Done when: every hook has a stated purpose and inheritance is explicit, not assumed.*

7. **Add completions for dynamic values.** Static `ValidArgs []string` for enumerable positionals, `ValidArgsFunction` for dynamic ones (return `ShellCompDirectiveNoFileComp` to suppress file fallback), `RegisterFlagCompletionFunc` for flag values.
   *Done when: every arg and flag value that has a bounded domain offers completion.*

8. **Test through the command object.** Use `SetOut`/`SetErr`/`SetArgs` and a fresh tree per test — cobra accumulates flag state across `Execute()` calls.
   *Done when: tests capture output via `OutOrStdout()`, build a new tree per test, and the suite passes.*

## Steps — extend a command tree

1. **Read the current tree first.** Map existing commands, groups, and flag scopes before changing anything.
   *Done when: you can name every existing subcommand, its flags, and its hooks.*

2. **Apply changes consistent with the structure.** Add the new subcommand to the intended parent, register any new group before it, use local flags for command-specific options, and extend `ValidArgsFunction` / completion functions for new dynamic values.
   *Done when: the new command appears in help under the right group, its flags don't leak into siblings, and completion covers its values.*

## Steps — review a command tree

1. **Check run-hook usage.** Every command uses `RunE`; `SilenceUsage`/`SilenceErrors` are set on the root. *Done when: no non-`E` hook and no `os.Exit`-based error escape remains.*
2. **Check output plumbing.** All writes go through `cmd.OutOrStdout()` / `cmd.ErrOrStderr()`, never `os.Stdout`. *Done when: every handler output is capturable by tests.*
3. **Check hook ordering and args validation.** `PersistentPreRunE` inheritance is explicit, and positional args are validated by `Args`. *Done when: the hook chain and validator set are correct and intentional.*
4. **Run the tests.** *Done when: command tests pass against freshly built trees.*

## Reference

### Cobra vs. viper

| Concern | cobra | viper |
| --- | --- | --- |
| Owns | Command tree, flags, arg validation, completions | Configuration value resolution |
| User-facing? | Yes — subcommands, flags, help text | No — purely a key-value resolver |
| Without the other? | Yes — a flag-only CLI needs only cobra | Yes — a daemon reading YAML + env needs only viper |
| Integration seam | Hands `pflag.Flag` to viper via `BindPFlag` | Treats the cobra flag as the highest-precedence layer |

Use cobra alone when the binary takes flags and args but no config; viper alone for a long-running service with no CLI; both when you need both — bind at `PersistentPreRunE` on the root. → See `go-spf13-viper`.

### Hook chain

```
PersistentPreRunE → PreRunE → RunE → PostRunE → PersistentPostRunE
```

- `PostRunE` runs only if `RunE` succeeded.
- A child `PersistentPreRunE` replaces the parent's entirely.

### Args validators

`NoArgs`, `ExactArgs(n)`, `MinimumNArgs(n)`, `MaximumNArgs(n)`, `RangeArgs(min,max)`, `OnlyValidArgs`, `ExactValidArgs(n)`, `MatchAll(v1, v2)`, or a custom `func(cmd *cobra.Command, args []string) error`.

### Flags primer

```go
rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file path")
serveCmd.Flags().IntVar(&port, "port", 8080, "listen port")
serveCmd.MarkFlagRequired("port")
serveCmd.MarkFlagsMutuallyExclusive("json", "yaml")
```

### Resources

- [pkg.go.dev/github.com/spf13/cobra](https://pkg.go.dev/github.com/spf13/cobra) · [github.com/spf13/cobra](https://github.com/spf13/cobra) · [cobra.dev](https://cobra.dev)
- Install: `go get github.com/spf13/cobra@latest`

### Deep references

- **[commands-and-args.md](./references/commands-and-args.md)** — full PreRun\*/PostRun\* chain, every Args validator, `PersistentPreRunE` inheritance rules
- **[flags.md](./references/flags.md)** — pflag types, required/exclusive/oneRequired groups, custom value types, viper binding
- **[completions.md](./references/completions.md)** — `ShellCompDirective` set, annotation-based completions, testing completions
- **[generators.md](./references/generators.md)** — man page, markdown, YAML, RST doc generation; `cobra-cli` scaffolder
- **[testing.md](./references/testing.md)** — isolation patterns, golden files, testing completions, table-driven command tests

## Watch for

| Mistake | Fix |
| --- | --- |
| Using `Run` instead of `RunE` | Use `RunE` and return the error — let cobra handle the exit |
| Writing `len(args)` checks in `RunE` | Declare `Args: cobra.ExactArgs(n)` on the command |
| Writing to `os.Stdout` directly | Use `cmd.OutOrStdout()` / `cmd.ErrOrStderr()` so tests can capture output |
| Child `PersistentPreRunE` silently drops the parent's | Call `parent.PersistentPreRunE(cmd, args)` from the child's hook |
| Reusing a root command across tests | Build a fresh command tree per test |

## Cross-references

- → See `go-cli` for general CLI architecture — project layout, exit codes, signal handling, I/O patterns
- → See `go-spf13-viper` for configuration layering (flag → env → file → default)
- → See `go-testing` for general Go testing patterns
