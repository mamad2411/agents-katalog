---
name: rust-conventions
description:
  This skill should be used when working on Rust projects, writing Rust code, running Rust tests,
  managing Cargo dependencies, or reviewing Rust code.
version: 0.1.0
---

# Rust Coding Conventions and Idiomatic Patterns

This skill defines comprehensive conventions for writing idiomatic Rust code following community
best practices, the Rust API Guidelines, and clippy as the authoritative style guide.

## Ownership and Borrowing

### Prefer Borrowing Over Cloning

Functions should borrow data when they do not need ownership. Unnecessary clones are a code smell
that clippy will flag.

```rust
// CORRECT: Borrow the slice; caller retains ownership
fn sum(values: &[i32]) -> i32 {
    values.iter().sum()
}
```

```rust
// WRONG: Taking ownership when only a read is needed
fn sum(values: Vec<i32>) -> i32 {
    values.iter().sum()
}
```

### Accept the Most General Borrow

Use `&str` instead of `&String`, `&[T]` instead of `&Vec<T>`, and `&Path` instead of `&PathBuf` in
function parameters.

```rust
// CORRECT: Accepts &str, &String, String slices, etc.
fn greet(name: &str) {
    println!("Hello, {name}!");
}
```

```rust
// WRONG: Forces callers to have a String
fn greet(name: &String) {
    println!("Hello, {name}!");
}
```

### Use Into for Flexible Owned Parameters

When a function needs to own a String, use `impl Into<String>` to accept both `&str` and `String`.

```rust
// CORRECT: Caller can pass &str or String
fn set_name(&mut self, name: impl Into<String>) {
    self.name = name.into();
}
```

```rust
// WRONG: Forces allocation even when caller already has a String
fn set_name(&mut self, name: &str) {
    self.name = name.to_string();
}
```

### Return Owned Types from Constructors

Constructors and factory functions should return owned types, not references.

```rust
// CORRECT: Returns owned type
fn new(name: &str) -> Self {
    Self { name: name.to_string() }
}
```

```rust
// WRONG: Lifetime entanglement makes the returned value hard to use
fn new<'a>(name: &'a str) -> Self<'a> {
    Self { name }
}
```

## Error Handling

### Use thiserror for Library Errors

Library crates should define structured error enums with `thiserror`.

```rust
// CORRECT: Structured, typed errors with automatic Display/From
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ParseError {
    #[error("unexpected token '{token}' at position {position}")]
    UnexpectedToken { token: String, position: usize },

    #[error("unexpected end of input")]
    UnexpectedEof,

    #[error("invalid number: {0}")]
    InvalidNumber(#[from] std::num::ParseIntError),
}
```

```rust
// WRONG: Stringly-typed errors lose structure
fn parse(input: &str) -> Result<Ast, String> {
    Err(format!("unexpected token at position {}", pos))
}
```

### Use anyhow for Application Errors

Binary crates (applications, CLIs, services) should use `anyhow` for convenient error handling with
context.

```rust
// CORRECT: anyhow with context for application code
use anyhow::{Context, Result};

fn load_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.toml")
        .context("failed to read config.toml")?;
    let config: Config = toml::from_str(&content)
        .context("failed to parse config.toml")?;
    Ok(config)
}
```

```rust
// WRONG: Using anyhow in a library (callers cannot match on error types)
// Libraries should use thiserror instead
pub fn parse(input: &str) -> anyhow::Result<Ast> {
    // ...
}
```

### Never Use unwrap in Production Code

Use `unwrap` only in tests and examples. In production code, propagate errors with `?` or handle
them explicitly.

```rust
// CORRECT: Propagate errors
fn read_port() -> Result<u16, ConfigError> {
    let port_str = std::env::var("PORT")
        .map_err(|_| ConfigError::Missing("PORT"))?;
    port_str.parse().map_err(|_| ConfigError::InvalidPort(port_str))
}
```

```rust
// WRONG: Will panic in production if PORT is unset
fn read_port() -> u16 {
    std::env::var("PORT").unwrap().parse().unwrap()
}
```

### Use expect Only with Invariant Documentation

If a panic is truly impossible due to a preceding check, use `expect` with a message explaining why
the invariant holds.

```rust
// CORRECT: Invariant is documented and provably true
let first = non_empty_vec
    .first()
    .expect("vec is non-empty because we checked len > 0 above");
```

```rust
// WRONG: Lazy expect that will produce a confusing panic message
let first = items.first().expect("should work");
```

## Code Style

### Clippy Is the Style Guide

Clippy is the definitive Rust style guide. Do not fight it. If clippy warns about something, fix it
unless there is a compelling, documented reason to suppress.

```rust
// CORRECT: Follow clippy's suggestion to use if-let
if let Some(value) = optional {
    process(value);
}
```

```rust
// WRONG: clippy warns about this pattern (clippy::match_single_binding)
match optional {
    Some(value) => process(value),
    None => {},
}
```

### Lint Suppression Rules

When suppressing a clippy lint, use the specific lint name and add a comment explaining why.

```rust
// CORRECT: Specific lint, documented reason
#[allow(clippy::cast_possible_truncation)]
// Port numbers are validated to be in 0..=65535 before this point
let port = raw_port as u16;
```

```rust
// WRONG: Blanket suppression hides real issues
#[allow(clippy::all)]
fn messy_function() {
    // ...
}
```

```rust
// WRONG: Suppression without explanation
#[allow(clippy::cast_possible_truncation)]
let port = raw_port as u16;
```

### Use Standard Derive Order

Derive macros should follow a consistent order: Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord,
Hash, Default, Serialize, Deserialize.

```rust
// CORRECT: Consistent derive order
#[derive(Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize)]
pub struct Config {
    pub name: String,
    pub port: u16,
}
```

```rust
// WRONG: Random ordering makes it hard to scan
#[derive(Serialize, Hash, Clone, Default, Debug, Deserialize, Eq, PartialEq)]
pub struct Config {
    pub name: String,
    pub port: u16,
}
```

### Naming Conventions

Follow Rust naming conventions strictly:

- Types and traits: `UpperCamelCase` (e.g., `UserService`, `IntoIterator`)
- Functions and methods: `snake_case` (e.g., `get_user`, `into_inner`)
- Constants and statics: `SCREAMING_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- Modules: `snake_case` (e.g., `user_service`)
- Lifetimes: short lowercase (e.g., `'a`, `'ctx`)
- Type parameters: short uppercase (e.g., `T`, `K`, `V`) or descriptive (e.g., `Item`, `Error`)

### Method Naming Conventions

Follow the standard library's naming patterns for methods:

```rust
// CORRECT: Standard method name prefixes
impl MyType {
    fn new() -> Self { /* constructor */ }
    fn with_capacity(cap: usize) -> Self { /* constructor variant */ }
    fn is_empty(&self) -> bool { /* boolean query */ }
    fn has_value(&self) -> bool { /* boolean query */ }
    fn as_str(&self) -> &str { /* cheap reference conversion */ }
    fn to_string(&self) -> String { /* expensive conversion */ }
    fn into_inner(self) -> T { /* consuming conversion */ }
    fn len(&self) -> usize { /* collection length */ }
}
```

```rust
// WRONG: Non-standard naming
impl MyType {
    fn create() -> Self { /* should be new() */ }
    fn empty(&self) -> bool { /* should be is_empty() */ }
    fn get_string(&self) -> String { /* should be to_string() or as_str() */ }
    fn count(&self) -> usize { /* should be len() for collections */ }
}
```

## Unsafe Code Rules

### Minimize Unsafe Scope

Keep `unsafe` blocks as small as possible, wrapping only the specific operation that requires it.

```rust
// CORRECT: Minimal unsafe scope
let value = {
    // SAFETY: We verified the pointer is valid and aligned in the check above.
    unsafe { ptr.read() }
};
process(value);
```

```rust
// WRONG: Overly broad unsafe block
unsafe {
    let value = ptr.read();
    process(value); // process() is safe; it does not belong in unsafe
    log_result(&value); // also safe
}
```

### SAFETY Comments Are Mandatory

Every `unsafe` block must have a `// SAFETY:` comment immediately before it explaining why the
invariants are upheld.

```rust
// CORRECT: SAFETY comment explains the invariant
// SAFETY: `index` was bounds-checked against `self.len` on line 42.
unsafe { *self.ptr.add(index) }
```

```rust
// WRONG: No SAFETY comment
unsafe { *self.ptr.add(index) }
```

### Prefer Safe Abstractions

If you find yourself writing `unsafe`, first check if there is a safe alternative in the standard
library, a well-audited crate (e.g., `bytemuck`, `zerocopy`), or a different design.

```rust
// CORRECT: Use bytemuck for safe zero-copy casts
use bytemuck::cast_slice;
let floats: &[f32] = cast_slice(bytes);
```

```rust
// WRONG: Manual unsafe cast when bytemuck handles it safely
// SAFETY: (even with this comment, prefer the safe alternative)
let floats: &[f32] = unsafe {
    std::slice::from_raw_parts(bytes.as_ptr().cast(), bytes.len() / 4)
};
```

## Macro Rules

### Prefer Functions Over Macros

Use macros only when functions cannot express the pattern (e.g., variadic arguments, compile-time
code generation, or syntax extensions).

```rust
// CORRECT: A function suffices here
fn max(a: i32, b: i32) -> i32 {
    if a > b { a } else { b }
}
```

```rust
// WRONG: Using a macro where a generic function would work
macro_rules! max {
    ($a:expr, $b:expr) => {
        if $a > $b { $a } else { $b }
    };
}
```

### Export Macros with Full Paths

When macros reference other items, use full paths (`$crate::`) to avoid hygiene issues.

```rust
// CORRECT: Uses $crate:: for unambiguous resolution
#[macro_export]
macro_rules! create_error {
    ($msg:expr) => {
        $crate::error::AppError::new($msg)
    };
}
```

```rust
// WRONG: Depends on caller having `error` module in scope
#[macro_export]
macro_rules! create_error {
    ($msg:expr) => {
        error::AppError::new($msg)
    };
}
```

### Include Trailing Comma Support

Declarative macros should accept an optional trailing comma for consistency with Rust syntax.

```rust
// CORRECT: Handles trailing comma
macro_rules! vec_of_strings {
    ($($s:expr),* $(,)?) => {
        vec![$($s.to_string()),*]
    };
}

// Both work:
// vec_of_strings!["a", "b", "c"]
// vec_of_strings!["a", "b", "c",]
```

```rust
// WRONG: No trailing comma support causes surprising compile errors
macro_rules! vec_of_strings {
    ($($s:expr),*) => {
        vec![$($s.to_string()),*]
    };
}
```

## Iterator and Combinator Patterns

### Prefer Iterators Over Manual Loops

Rust iterators are zero-cost abstractions. Prefer them over index-based or manual loops.

```rust
// CORRECT: Iterator chain - clear, composable, and optimized
let total: f64 = orders
    .iter()
    .filter(|o| o.status == Status::Completed)
    .map(|o| o.total)
    .sum();
```

```rust
// WRONG: Manual loop with mutable accumulator
let mut total = 0.0;
for i in 0..orders.len() {
    if orders[i].status == Status::Completed {
        total += orders[i].total;
    }
}
```

### Use collect with Turbofish for Type Clarity

When the return type of `collect()` is not obvious from context, use the turbofish syntax.

```rust
// CORRECT: Type is clear from turbofish
let names: Vec<&str> = users.iter().map(|u| u.name.as_str()).collect();

// Also correct: turbofish on collect
let names = users.iter().map(|u| u.name.as_str()).collect::<Vec<_>>();
```

```rust
// WRONG: Ambiguous without type annotation
let names = users.iter().map(|u| u.name.as_str()).collect(); // Error: cannot infer type
```

## Struct and Enum Design

### Use Enums to Represent States

Use enums instead of boolean flags or stringly-typed state fields.

```rust
// CORRECT: States are explicit and exhaustive
enum ConnectionState {
    Disconnected,
    Connecting { attempt: u32 },
    Connected { since: Instant },
    Failed { error: String },
}
```

```rust
// WRONG: Boolean flags create invalid state combinations
struct Connection {
    is_connected: bool,
    is_connecting: bool,
    error: Option<String>,
    connected_since: Option<Instant>,
}
```

### Implement Default for Configuration Types

Types used for configuration should implement `Default` so users can customize only what they need.

```rust
// CORRECT: Default provides sensible values
#[derive(Debug, Clone)]
pub struct ServerConfig {
    pub host: String,
    pub port: u16,
    pub max_connections: usize,
    pub timeout_secs: u64,
}

impl Default for ServerConfig {
    fn default() -> Self {
        Self {
            host: "0.0.0.0".into(),
            port: 8080,
            max_connections: 1000,
            timeout_secs: 30,
        }
    }
}

// Usage: override only what you need
let config = ServerConfig {
    port: 3000,
    ..Default::default()
};
```

## Module Organization

### Keep Modules Focused

Each module should have a single, clear responsibility. If a module file grows beyond 500 lines,
consider splitting it.

```text
src/
├── lib.rs          # Public API re-exports
├── config.rs       # Configuration loading
├── error.rs        # Error types
├── service.rs      # Business logic
├── repository.rs   # Data access
└── models/         # Domain types
    ├── mod.rs
    ├── user.rs
    └── order.rs
```

### Re-Export Public API from lib.rs

The public API should be re-exported from `lib.rs` so consumers do not need to know your internal
module structure.

```rust
// CORRECT: Clean public API
// lib.rs
pub mod error;
mod service;
mod repository;

pub use error::AppError;
pub use service::UserService;
```

```rust
// WRONG: Exposing internal module paths
// lib.rs
pub mod internal;
pub mod service;
pub mod repository;
// Forces users to write: my_crate::service::user::UserService
```

## Documentation Rules

### Document All Public Items

Every public function, struct, enum, trait, and module should have a doc comment.

````rust
// CORRECT: Doc comment with examples
/// Parses a duration string like "5s", "100ms", or "2m30s".
///
/// # Errors
///
/// Returns `ParseError` if the input is empty or contains invalid units.
///
/// # Examples
///
/// ```rust
/// use my_crate::parse_duration;
///
/// let d = parse_duration("5s").unwrap();
/// assert_eq!(d.as_secs(), 5);
/// ```
pub fn parse_duration(input: &str) -> Result<Duration, ParseError> {
    // ...
}
````

```rust
// WRONG: No documentation on public function
pub fn parse_duration(input: &str) -> Result<Duration, ParseError> {
    // ...
}
```

### Use Standard Doc Sections

Use these standard sections in doc comments, in this order:

1. Summary line (first paragraph)
2. Extended description (optional)
3. `# Errors` (for fallible functions)
4. `# Panics` (for functions that can panic)
5. `# Safety` (for unsafe functions)
6. `# Examples`
