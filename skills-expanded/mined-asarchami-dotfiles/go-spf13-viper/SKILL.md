---
name: go-spf13-viper
description: "viper config resolution — layered precedence (flag > env > file > KV > default), env binding triple, BindPFlag, graceful ConfigFileNotFoundError, mapstructure unmarshal, Sub, hot reload, and test isolation. Use when adopting viper, wiring flags or env to config values, or debugging why a key resolves to the wrong source layer."
license: MIT
---

# spf13/viper

**Leading word: config.** Viper answers one question — "what is the value of key X right now?" — by walking a fixed precedence pipeline (flag beats env beats file beats KV beats default). The discipline: know which layer every key comes from, bind each key once so all reachable layers stay visible, and treat a missing config file as a normal state, not a crash.

## Steps

1. **Walk the precedence pipeline before writing code.** Resolve each key's source layers in order: explicit `Set()`, bound flag, env var, config file, KV remote, default. A key that "should" come from a file may be shadowed by an env var or a flag default.
   *Done when: for every key, you can name the highest-priority layer that may set it and the shadowing it must survive.*

2. **Wire the env binding triple together.** Set `SetEnvPrefix("MYAPP")` to prevent collisions, `SetEnvKeyReplacer(strings.NewReplacer(".", "_"))` so `database.host` maps to `MYAPP_DATABASE_HOST`, and `AutomaticEnv()`. Missing any one breaks nested key resolution silently.
   *Done when: every nested config key resolves from its env var with dots translated to underscores.*

3. **Read the config file gracefully.** Use `errors.As(err, &notFound)` on `viper.ConfigFileNotFoundError` and propagate only real errors — a missing file must not crash a run that works on flags and env alone.
   *Done when: a run with no config file starts cleanly, while genuinely corrupt files still fail loudly.*

4. **Bind flags before `Execute()`.** Call `viper.BindPFlag` / `BindPFlags` in `init()` or `PersistentPreRunE` — binding in `RunE` is too late because cobra parses flags before it runs.
   *Done when: every cobra flag the CLI exposes is bound to a viper key before command execution.*

5. **Unmarshal into structs with `mapstructure` tags.** Tag every field (`mapstructure:"max_conn"`); implicit mapping silently misses nested and underscore-named fields. Prefer `UnmarshalKey("database", &dbCfg)` over `Sub("database").Unmarshal` — it avoids the nil-check `Sub` requires when the key is missing.
   *Done when: every config struct field carries an explicit tag and no `Sub` result is used without a nil check.*

6. **Isolate tests with `viper.New()`.** Never use the global viper in tests — its state leaks across test cases and causes flaky ordering.
   *Done when: every test configures its own `*viper.Viper` instance.*

7. **Handle hot reload with fsnotify's limits.** `WatchConfig` + `OnConfigChange` watch inodes; editors that save via atomic rename (vim, neovim) replace the inode and the callback may not fire.
   *Done when: the reload path is verified with `echo >> config.yaml`, not editor saves.*

## Reference

### The precedence pipeline

```
1. explicit Set()      — viper.Set("key", val)    highest priority
2. flag                — bound pflag.Flag
3. env var             — BindEnv / AutomaticEnv
4. config file         — ReadInConfig / MergeInConfig
5. KV remote           — etcd / Consul
6. default             — viper.SetDefault("key", val)   lowest priority
```

The pipeline is fixed and cannot be reordered.

### Reading a config file

```go
viper.SetConfigName("config")
viper.AddConfigPath("$HOME/.myapp")
if err := viper.ReadInConfig(); err != nil {
    var notFound *viper.ConfigFileNotFoundError
    if !errors.As(err, &notFound) {
        return fmt.Errorf("reading config: %w", err)
    }
}
```

### Env binding triple

```go
viper.SetEnvPrefix("MYAPP")                             // PORT → MYAPP_PORT
viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))  // database.host → MYAPP_DATABASE_HOST
viper.AutomaticEnv()
```

Without `SetEnvKeyReplacer`, viper looks for `MYAPP_DATABASE.HOST` (dot preserved) and never matches.

### Flag binding (the cobra seam)

```go
func init() {
    rootCmd.PersistentFlags().Int("port", 8080, "listen port")
    viper.BindPFlag("port", rootCmd.PersistentFlags().Lookup("port"))
    // viper.BindPFlags(cmd.Flags()) — bind an entire FlagSet at once
}
```

### Unmarshaling

```go
type Config struct {
    Port     int `mapstructure:"port"`
    Database struct {
        MaxConn int `mapstructure:"max_conn"`
    } `mapstructure:"database"`
}
var cfg Config
viper.Unmarshal(&cfg)
```

### Hot reload

```go
viper.WatchConfig()
viper.OnConfigChange(func(e fsnotify.Event) { /* re-apply changed values */ })
```

### Resources

- [pkg.go.dev/github.com/spf13/viper](https://pkg.go.dev/github.com/spf13/viper) · [github.com/spf13/viper](https://github.com/spf13/viper)
- Install: `go get github.com/spf13/viper@latest`

### Deep references

- **[sources-and-formats.md](./references/sources-and-formats.md)** — supported formats, multi-path search, `MergeInConfig`, remote KV (etcd/Consul)
- **[binding-and-env.md](./references/binding-and-env.md)** — `BindEnv`, `AutomaticEnv`, `SetEnvPrefix`, `SetEnvKeyReplacer`, `AllowEmptyEnv`, timing rules
- **[unmarshal.md](./references/unmarshal.md)** — `Unmarshal`, `UnmarshalKey`, mapstructure tags, custom `DecodeHook`s (Duration, IP, slice)
- **[watch-and-reload.md](./references/watch-and-reload.md)** — `WatchConfig`, `OnConfigChange`, fsnotify caveats, atomic-rename trap, race-safe patterns
- **[testing-and-isolation.md](./references/testing-and-isolation.md)** — `viper.New()` per test, `t.Setenv` interactions, `Reset()` limitations, snapshot/restore

## Watch for

| Mistake | Fix |
| --- | --- |
| `AutomaticEnv` without `SetEnvKeyReplacer` | Add `SetEnvKeyReplacer(strings.NewReplacer(".", "_"))` before `AutomaticEnv` |
| No `mapstructure` tags on struct fields | Add `mapstructure:"key_name"` to every field |
| Using global viper in tests | Create `viper.New()` per test |
| Missing `ConfigFileNotFoundError` check | `errors.As(err, &notFound)` — propagate only non-not-found errors |
| Binding flags in `RunE` | Bind in `init()` or `PersistentPreRunE`, before cobra parses |

## Cross-references

- → See `go-spf13-cobra` for the cobra side — flag definition and binding
- → See `go-cli` for general CLI architecture — project layout, exit codes, signal handling
- → See `go-testing` for general Go testing patterns
