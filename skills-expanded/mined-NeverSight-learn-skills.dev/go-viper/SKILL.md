---
name: go-viper
description: Write, debug, and explain Go configuration code using github.com/spf13/viper. Use this skill whenever the user wants Viper-based config loading, config structs, file plus env plus flag precedence, Cobra or pflag integration, unmarshaling config into structs, env key replacers, or a clean application config bootstrap that follows Viper's README behavior.
source: local
license: MIT
---

Use this skill to produce a clean Viper setup that reads configuration from file, flags, and environment with Viper's normal precedence:

1. explicit `Set`
2. flags
3. environment variables
4. config file
5. remote key/value store
6. defaults

## Core approach

- Prefer `viper.New()` over the package global; build one configured instance and pass it where needed.
- Define a typed `Config` struct and unmarshal into it after all defaults, file paths, env bindings, and flag bindings are configured.
- Keep configuration bootstrap in one place such as `internal/config` or `pkg/config` with a `Load(...)` function.
- Treat the config file as optional only when the app design allows it; otherwise return a clear error.
- Bind flags and env explicitly for important keys, and use `AutomaticEnv()` plus an env key replacer for the general case.

## Clean Viper bootstrap

When writing a Viper-based loader, follow this order:

1. Create an instance with `v := viper.New()`.
2. Set config file name, type if needed, and search paths.
3. Set defaults with `SetDefault`.
4. Configure env loading with `SetEnvPrefix`, `SetEnvKeyReplacer`, `AutomaticEnv`, and `BindEnv` for special keys.
5. Define and parse `pflag` or Cobra flags, then bind them with `BindPFlag` or `BindPFlags`.
6. Call `ReadInConfig()`.
7. Handle `viper.ConfigFileNotFoundError` separately from parse errors when the file is optional.
8. Call `Unmarshal(&cfg)` into a typed struct.
9. Validate the resulting struct if the app has required fields or constraints.

## Implementation rules

- Use `mapstructure` tags on struct fields when file keys differ from Go field names.
- For nested keys that should map to env vars, use `strings.NewReplacer(".", "_", "-", "_")` with `SetEnvKeyReplacer`.
- Remember that env vars are case-sensitive and are read when accessed, not cached at bind time.
- Remember that Viper does not deep-merge complex values; later sources replace the whole value.
- Add all config paths before `ReadInConfig()` and before `WatchConfig()`.
- If the user uses Cobra, bind command flags directly from the command's flag set.
- If the user wants testable code, return both the typed config and the configured `*viper.Viper` only when the caller truly needs both; otherwise return just the typed config.

## Output expectations

- Give a small, production-leaning config package, not scattered snippets.
- Show how file, env, and flags work together in one example.
- Make precedence explicit in the explanation.
- Mention the exact env var names and flag names generated or bound.

## References

- Read `references/clean-config-pattern.md` for the recommended package shape, loader order, validation strategy, testing guidance, and common pitfalls.
- Read `references/file-env-flag-precedence.md` when the task is specifically about how file, env, and flags interact or why one source wins over another.
- Read `examples/clean_setup.go` for a compact end-to-end loader example.
