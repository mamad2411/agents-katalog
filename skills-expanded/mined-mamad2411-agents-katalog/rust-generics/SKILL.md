---
name: rust-generics
description: "When to activate: Rust generics, trait bounds, associated types, GATs, where clauses, PhantomData, higher-ranked trait bounds, type system"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: rust
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Rust Generics and Type System

## Generic Functions and Structs

```rust
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in list {
        if item > largest { largest = item; }
    }
    largest
}

struct Pair<T> { first: T, second: T }

impl<T: std::fmt::Display + PartialOrd> Pair<T> {
    fn new(first: T, second: T) -> Self { Self { first, second } }

    fn cmp_display(&self) {
        if self.first >= self.second {
            println!("largest is first: {}", self.first);
        } else {
            println!("largest is second: {}", self.second);
        }
    }
}
```

## Trait Bounds

```rust
// Multiple bounds
fn print_debug<T: std::fmt::Display + std::fmt::Debug>(val: T) {
    println!("Display: {val}  Debug: {val:?}");
}

// where clause for readability
fn complex<T, U>(t: T, u: U) -> String
where
    T: std::fmt::Display + Clone,
    U: std::fmt::Debug + PartialOrd,
{
    format!("{t} {:?}", u)
}

// impl Trait in argument position
fn notify(item: &impl std::fmt::Display) { println!("{item}"); }

// impl Trait in return position (opaque type)
fn make_adder(x: i32) -> impl Fn(i32) -> i32 {
    move |y| x + y
}
```

## Associated Types

```rust
trait Transform {
    type Output;
    type Error;

    fn transform(&self, input: &str) -> Result<Self::Output, Self::Error>;
}

struct JsonParser;

impl Transform for JsonParser {
    type Output = serde_json::Value;
    type Error = serde_json::Error;

    fn transform(&self, input: &str) -> Result<Self::Output, Self::Error> {
        serde_json::from_str(input)
    }
}
```

## Generic Associated Types (GATs)

```rust
trait Container {
    type Item<'a> where Self: 'a;
    fn get(&self, idx: usize) -> Option<Self::Item<'_>>;
}

struct VecContainer<T>(Vec<T>);

impl<T> Container for VecContainer<T> {
    type Item<'a> = &'a T where Self: 'a;
    fn get(&self, idx: usize) -> Option<&T> { self.0.get(idx) }
}
```

## PhantomData for Type Safety

```rust
use std::marker::PhantomData;

struct Meters;
struct Feet;

struct Length<Unit> { value: f64, _unit: PhantomData<Unit> }

impl<Unit> Length<Unit> {
    fn new(value: f64) -> Self { Self { value, _unit: PhantomData } }
    fn value(&self) -> f64 { self.value }
}

impl Length<Meters> {
    fn to_feet(&self) -> Length<Feet> { Length::new(self.value * 3.28084) }
}
// Cannot add Length<Meters> + Length<Feet> — type error at compile time
```

## Higher-Ranked Trait Bounds (HRTB)

```rust
fn apply_to_str<F>(f: F) -> String
where
    F: for<'a> Fn(&'a str) -> &'a str,
{
    f("hello world").to_string()
}
```

## Default Type Parameters

```rust
use std::ops::Add;

struct Point { x: f64, y: f64 }

impl Add for Point {
    type Output = Point;
    fn add(self, other: Point) -> Point {
        Point { x: self.x + other.x, y: self.y + other.y }
    }
}

impl Add<f64> for Point {
    type Output = Point;
    fn add(self, scalar: f64) -> Point {
        Point { x: self.x + scalar, y: self.y + scalar }
    }
}
```

## Blanket Implementations

```rust
trait Printable: std::fmt::Display {
    fn print(&self) { println!("{self}"); }
}

// Every Display type gets Printable for free
impl<T: std::fmt::Display> Printable for T {}

42i32.print();
"hello".print();
```

## Common Anti-Patterns

- **Over-genericizing** — if there's only one realistic `T`, use a concrete type
- **Bounds on the struct definition** — put bounds on `impl<T: Bound>`, not `struct Foo<T: Bound>`, unless the struct itself requires it
- **`dyn Trait` when generics suffice** — generics are zero-cost; `dyn` adds vtable indirection
- **Trait objects for non-object-safe traits** — `Clone`/`Sized` cannot be used as `dyn`; use generics
- **Complex bounds inline** — use `where` clauses for readability
