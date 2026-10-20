# Agentic AI Instructions for Corvo

Welcome, AI Agent! You are contributing to the **Corvo** language, a modern scripting language written in Rust that compiles directly to standalone executables. When contributing to this repository or writing Corvo scripts, you must strictly adhere to the following rules:

## 1. Reference Material & Context
Always consult the following resources before generating or modifying code:
- **[README.md](README.md)**: For the core philosophy ("Write scripts like prose. Ship them like binaries. Trust them like Rust."), project setup, and high-level architecture.
- **[CHEATSHEET.md](CHEATSHEET.md)**: For the definitive list of all standard library functions, namespaces, built-in blocks (`browse`, `loop`, `http_listen`, `run_test`, etc.), and shorthands. **Do not hallucinate functions** that are not in this list.
- **[`examples/`](examples/)**: Review this directory for practical, working implementations of Corvo scripts covering various use cases. For complete CLI utility rewrites (coreutils), see the [`futils`](https://github.com/CorvoLang/futils) repository.

## 2. Implementing New Features (Rust Source)

The Corvo compiler, interpreter, and standard library are located in the `src/` directory. If you are adding a new feature, follow these established internal patterns:

### Adding a New Standard Library Function
1. **Implementation**: Add the function logic to the appropriate namespace file in `src/standard_lib/` (e.g., `sys.rs`, `fs.rs`). Functions typically take `(args: &[Value], named_args: &HashMap<String, Value>)` and return `CorvoResult<Value>`. Use `Value::as_string()`, `Value::as_number()`, etc., to safely extract types. Return errors using `CorvoError`.
2. **Registration**: Expose and route the function in the `call` match block inside `src/standard_lib/mod.rs`.
3. **Linting**: Add the full function name (e.g., `"fs.new_feature"`) to the `KNOWN_FUNCTIONS` array in `src/diagnostic.rs` so the static linter doesn't flag it as unknown.
4. **Documentation**: Update `CHEATSHEET.md` with the new function signature and description.
5. **Transpilation Macro**: Add a new `#[macro_export]` macro definition for the function in the corresponding implementation file (e.g., `src/standard_lib/fs.rs` for `fs.new_feature` or `src/type_system/type_methods.rs` for type methods) so that the transpiler can generate cleaner Rust code.
6. **Optional Cargo feature**: If the function pulls in a heavy or platform-specific dependency, gate it behind a `stdlib-*` feature in `Cargo.toml`, add it to `full-stdlib`, map the namespace in `src/compiler/usage_analyzer.rs` for Oxide lean builds, and document platform limits (see `pex.*` / `stdlib-pex` on Unix only).
7. **Stateful runtime handles**: If the API returns session handles (TCP listeners, PTY sessions, etc.), register them in a dedicated registry under `src/runtime/`, wire the field into `RuntimeState`, and add the function prefix to `function_needs_state` in `src/compiler/transpiler.rs` so transpiled code receives `RuntimeState`.

### Adding a New Syntax Block or Expression
Extending the language syntax itself (e.g., adding a new loop type or control flow) requires updates across the entire pipeline:
1. **Lexer**: Add any new keywords or tokens to `src/lexer/token.rs`.
2. **AST**: Add the new node variant to `src/ast/stmt.rs` or `src/ast/expr.rs`.
3. **Parser**: Implement the recursive descent parsing logic in `src/parser/recursive_descent.rs`.
4. **Linter**: Add static analysis handling for your new AST node in `src/diagnostic.rs` (`lint_stmt` or `lint_expr`).
5. **Interpreter**: Add runtime evaluation logic in `src/compiler/evaluator.rs`.
6. **Transpiler**: Ensure the AST can be converted to Rust by updating `src/compiler/transpiler.rs` and, if applicable, `src/compiler/builder.rs`.

## 3. Testing Requirements
Any new feature, standard library function, or `.corvo` script must be comprehensively tested. You must ensure:
1. **Unit Tests**: Rust logic must be covered by standard `#[test]` functions within the respective module.
2. **Interpreter Tests**: Ensure the code runs correctly via the interpreter (`corvo <file.corvo>`).
3. **Compiling Tests**: Ensure the code compiles to a standalone binary successfully (`corvo --compile <file.corvo>`).
4. **Transpiling Tests**: Ensure the AST can be successfully transpiled to a Rust project (`corvo --transpile <file.corvo>`).
5. **`run_test` blocks**: Interpreter-only integration tests (Unix + `stdlib-pex`); skipped in normal runs and stripped from transpiled output. Run with `corvo --run-test <file.corvo>`.

Your contributions will be rejected if tests are missing or if any of the pipeline steps fail.

## 4. Code Quality & Pre-Commit formatting
Before proposing any changes or committing files, you **MUST** run the following checks. Do not skip these steps:
- **Rust Code**: 
  - Run `cargo fmt` to ensure standard formatting.
  - Run `cargo clippy` to catch common mistakes and enforce idiomatic Rust. Ensure there are no warnings.
- **Corvo Scripts**: 
  - Run `corvo --lint <file.corvo>` on any modified or newly created `.corvo` files to catch syntax errors and unknown function calls statically.
- **Oxide Mode**:
  - Ensure any new standard library feature is correctly mapped in `src/compiler/usage_analyzer.rs`.
  - Verify that Oxide transpilation (`corvo --oxide <file>`) produces a lean project that compiles successfully.
  - Run `tests/oxide_transpilation_test.rs` for regressions in lean binary generation.
  - When merging into an existing Oxide output directory, `src/compiler/builder.rs` preserves prior `[[bin]]` entries and merges `corvo-lang` feature flags in `[dependencies]` only.
- **CI expectations** (`.github/workflows/ci.yml`): `cargo test --all-features`, `run_test_integration` and `oxide_transpilation_test` on Unix, `corvo --lint examples/*.corvo`, and Unix smoke of `pex_example.corvo` + `run_test_example.corvo`.
