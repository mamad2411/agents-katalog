---
name: Rust
description: Write idiomatic Rust avoiding ownership pitfalls, lifetime confusion, and common borrow checker battles.
metadata: {"clawdbot":{"emoji":"🦀","requires":{"bins":["rustc","cargo"]},"os":["linux","darwin","win32"]}}
---

## Ownership Traps
- Variable moved after use — clone explicitly or borrow with `&`
- `for item in vec` moves vec — use `&vec` or `.iter()` to borrow
- Struct field access moves field if not Copy — destructure or clone
- Closure captures by move with `move ||` — needed for threads and 'static
- `String` moved into function — pass `&str` for read-only access

## Borrowing Battles
- Can't have mutable and immutable borrow simultaneously — restructure code or use interior mutability
- Borrow lasts until last use (NLL) — not until scope end in modern Rust
- Returning reference to local fails — return owned value or use lifetime parameter
- Mutable borrow through `&mut self` blocks all other access — split struct or use `RefCell`

## Lifetime Gotchas
- Missing lifetime annotation — compiler usually infers, explicit when multiple references
- `'static` means "can live forever", not "lives forever" — `String` is 'static, `&str` may not be
- Struct holding reference needs lifetime parameter — `struct Foo<'a> { bar: &'a str }`
- Function returning reference must tie to input lifetime — `fn get<'a>(s: &'a str) -> &'a str`

## String Confusion
- `String` is owned, `&str` is borrowed slice — convert with `.as_str()` or `String::from()`
- Indexing `s[0]` fails — UTF-8 variable width, use `.chars().nth(0)` or `.bytes()`
- Concatenation: `s1 + &s2` moves s1 — use `format!("{}{}", s1, s2)` to keep both
- `.len()` returns bytes, not characters — use `.chars().count()` for char count

## Error Handling
- `unwrap()` panics on None/Err — use `?` operator or `match` in production
- `?` requires function returns Result/Option — can't use in main without `-> Result<()>`
- Converting errors: `map_err()` or `From` trait implementation
- `expect("msg")` better than `unwrap()` — shows context on panic
- `Option` and `Result` don't mix — use `.ok()` or `.ok_or()` to convert

## Pattern Matching
- Match must be exhaustive — use `_` wildcard for remaining cases
- `if let` for single pattern — avoids verbose match for one case
- Guard conditions: `match x { n if n > 0 => ... }` — guards don't create bindings
- `@` bindings: `Some(val @ 1..=5)` — binds matched value to name
- `ref` keyword in patterns to borrow — often unnecessary with match ergonomics

## Iterator Gotchas
- `.iter()` borrows, `.into_iter()` moves, `.iter_mut()` borrows mutably
- `.collect()` needs type annotation — `collect::<Vec<_>>()` or let binding with type
- Iterators are lazy — nothing happens until consumed
- `.map()` returns iterator, not collection — chain with `.collect()`
- Modifying while iterating impossible — collect indices first, then modify

## Type System
- Orphan rule: can't impl external trait on external type — newtype pattern workaround
- Trait objects `dyn Trait` have runtime cost — generics monomorphize for performance
- `Box<dyn Trait>` for heap-allocated trait object — `&dyn Trait` for borrowed
- Associated types vs generics: use associated when one impl per type
- `Self` vs `self`: type vs value — `Self::new()` vs `&self`

## Concurrency
- Data shared between threads needs `Send` and `Sync` — most types are, `Rc` is not
- Use `Arc` for shared ownership across threads — `Rc` is single-threaded only
- `Mutex<T>` for mutable shared state — lock returns guard, auto-unlocks on drop
- `RwLock` allows multiple readers or one writer — deadlock if reader tries to write
- Async functions return `Future` — must be awaited or spawned

## Memory Patterns
- `Box<T>` for heap allocation — also needed for recursive types
- `Rc<T>` for shared ownership (single-thread) — `Arc<T>` for multi-thread
- `RefCell<T>` for interior mutability — runtime borrow checking, panics on violation
- `Cell<T>` for Copy types interior mutability — no borrow, just get/set
- Avoid `Rc<RefCell<T>>` spaghetti — rethink ownership structure
