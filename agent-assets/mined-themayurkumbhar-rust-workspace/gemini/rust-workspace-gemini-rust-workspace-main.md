# GEMINI.md: Project Context

## Project Overview

This is a Rust learning workspace, as indicated by the `README.md` and the project structure. The repository is organized into directories named `day1`, `day2`, etc., with each directory containing small, standalone Rust programs that explore a specific language feature.

The `Cargo.toml` file is configured to define multiple binary targets. Each `.rs` file is treated as a separate executable application. This setup is tailored for learning and allows each example to be built and run independently.

## Building and Running

Because this project contains multiple applications, you need to specify which one you want to run.

### Building

To build all the example programs at once, run:

```bash
cargo build
```

This will compile all binaries into the `target/debug/` directory.

### Running a Specific Program

To run a specific program, use the `cargo run --bin <binary_name>` command. The binary name is defined by the `name` field in the `[[bin]]` section of the `Cargo.toml` file.

For example:
*   To run `greetings.rs` from day 1:
    ```bash
    cargo run --bin greetings
    ```
*   To run `scope.rs` from day 2:
    ```bash
    cargo run --bin scope
    ```
*   To run `shadowing.rs` from day 3:
    ```bash
    cargo run --bin shadowing
    ```

### Testing

While there are currently no tests, you can run tests for the workspace using the standard command:

```bash
cargo test
```

## Development Conventions

*   **Structure**: Each concept or lesson is contained within its own `.rs` file and is defined as a separate `[[bin]]` target in `Cargo.toml`.
*   **Self-Contained Examples**: Each file is a small, self-contained program with a `main` function, designed to demonstrate a specific Rust concept clearly and concisely.
*   **Focus**: The code focuses on fundamental Rust features like variable bindings, scope, shadowing, and basic types.
