---
name: follow-create-nushell-plugin
description: Build NuShell plugins in Rust per the official contributor guide
argument-hint: "[plugin-name]"
related:
  - follow-create-plugins
  - ship

---

## Goal

Build a working NuShell plugin in Rust that follows the official NuShell contributor guide's standards

## Scope

Use for creating a new NuShell plugin in Rust with the `nu-plugin` and `nu-protocol` crates

## Execute

### 1. Setup Project

> Goal: scaffold the project structure for a NuShell plugin

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest NuShell/nu-plugin versions, per the conventions in `/update-devin-global-skills` — `nu-plugin`/`nu-protocol` must match the installed NuShell version
2. Create the project with `cargo new nu_plugin_<name>`
3. Edit `Cargo.toml` to add the dependencies: `nu-plugin` + `nu-protocol` (same version as the installed NuShell — not pinned in this skill)
3. Set `edition = "2024"` and match the version to the installed NuShell
4. Create `src/main.rs` as the plugin entry point

### 2. Implement Plugin Trait

> Goal: create a struct that implements the `Plugin` trait

1. Create a unit struct for the plugin (e.g. `LenPlugin`)
2. Implement the `Plugin` trait:
   - `fn version(&self) -> String` using `env!("CARGO_PKG_VERSION").into()`
   - `fn commands(&self) -> Vec<Box<dyn PluginCommand<Plugin = Self>>>` returning the list of commands
3. You may keep plugin state in this struct when needed

### 3. Implement Command

> Goal: create commands with `SimplePluginCommand` or `PluginCommand`

1. Create a unit struct for each command (e.g. `Len`)
2. Implement `SimplePluginCommand` (or `PluginCommand` if you must handle streams):
   - `fn name(&self) -> &str`
   - `fn description(&self) -> &str`
   - `fn signature(&self) -> Signature` declaring input/output types
   - `fn run(...)` processes the input and returns a `Value` or `LabeledError`
3. Use `EvaluatedCall` for arguments and `call.head` for the error span
4. Use `PluginCommand` instead when the command must accept or emit streams

### 4. Wire Main Entry Point

> Goal: connect to the NuShell plugin runtime

1. In `main()`, call `serve_plugin(&YourPlugin, JsonSerializer)` or `MsgPackSerializer`
2. Use `MsgPackSerializer` in production because it is faster
3. Use `JsonSerializer` for debugging or protocol testing

### 5. Build And Register Plugin

> Goal: install and register the plugin with NuShell

1. Build a release with `cargo install --path . --locked`
2. In NuShell, register the plugin with `plugin add <path/to/nu_plugin_name>` (append `.exe` on Windows)
3. Load the plugin immediately with `plugin use <command_name>` or restart NuShell
4. Verify with `plugin list`

### 6. Development Workflow

> Goal: develop and test the plugin

1. Use `cargo build` and `cargo run` during development
2. Use `cargo clippy` and `cargo fmt` for code quality
3. Test the command in NuShell after `plugin use <command_name>`
4. Make `Signature` declare the correct input/output types so type checking works

### 7. Ship

> Goal: deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Naming And Version

- Always name the project `nu_plugin_<name>`
- `nu-plugin` and `nu-protocol` versions must match the installed NuShell version
- Don't hardcode versions; take them from `env!("CARGO_PKG_VERSION")`

### 2. Command Type

- Use `SimplePluginCommand` for commands that don't handle streams
- Use `PluginCommand` for commands that must handle streams

### 3. Error Handling

- Return errors with `LabeledError` including the `call.head` span so NuShell underlines the failing command

### 4. Serialization

- Use `MsgPackSerializer` in production
- Use `JsonSerializer` for debugging or protocol testing

- Use /follow-create-biome-plugin if needed
- Use /follow-create-bun-plugin if needed
- Use /follow-create-devin-plugin if needed
- Use /follow-create-plugins if needed


## Expected Outcome

- A NuShell plugin that builds and registers successfully
- Commands appear in NuShell with help and type signatures
- The plugin behaves per its declared `Signature`
- Code passes `cargo clippy` and `cargo fmt`

## Examples

### Cargo.toml

```toml
[package]
name = "nu_plugin_len"
version = "0.1.0"
edition = "2024"

[dependencies]
nu-plugin = "0.104.0"
nu-protocol = "0.104.0"
```

### `src/main.rs`

```rust
use nu_plugin::{
    EngineInterface, EvaluatedCall, JsonSerializer, Plugin, PluginCommand, SimplePluginCommand,
    serve_plugin,
};
use nu_protocol::{LabeledError, Signature, Type, Value};

struct LenPlugin;

impl Plugin for LenPlugin {
    fn version(&self) -> String {
        env!("CARGO_PKG_VERSION").into()
    }

    fn commands(&self) -> Vec<Box<dyn PluginCommand<Plugin = Self>>> {
        vec![Box::new(Len)]
    }
}

struct Len;

impl SimplePluginCommand for Len {
    type Plugin = LenPlugin;

    fn name(&self) -> &str {
        "len"
    }

    fn description(&self) -> &str {
        "calculates the length of its input"
    }

    fn signature(&self) -> Signature {
        Signature::build(PluginCommand::name(self))
            .input_output_type(Type::String, Type::Int)
    }

    fn run(
        &self,
        _plugin: &LenPlugin,
        _engine: &EngineInterface,
        call: &EvaluatedCall,
        input: &Value,
    ) -> Result<Value, LabeledError> {
        let span = input.span();
        match input {
            Value::String { val, .. } => Ok(Value::int(val.len() as i64, span)),
            _ => Err(
                LabeledError::new("Expected String input from pipeline")
                    .with_label(
                        format!("requires string input; got {}", input.get_type()),
                        call.head,
                    )
            ),
        }
    }
}

fn main() {
    serve_plugin(&LenPlugin, JsonSerializer);
}
```

### Register And Use

```nu
# build and install (from project root)
cargo install --path . --locked

# register in NuShell
plugin add ~/.cargo/bin/nu_plugin_len   # add .exe on Windows

# load and test
plugin use len
"hello" | len    # => 5
```

## Guide

- [NuShell Plugins Guide](https://www.nushell.sh/contributor-book/plugins.html#creating-a-plugin-in-rust)
- [nu-plugin crate docs](https://docs.rs/nu-plugin)
- [nu-protocol crate docs](https://docs.rs/nu-protocol)

