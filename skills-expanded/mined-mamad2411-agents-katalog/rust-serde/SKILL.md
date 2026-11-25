---
name: rust-serde
description: "When to activate: Rust serde, JSON, serialization, deserialization, custom serialize, rename, flatten, skip, default, serde_json, toml, bincode"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: rust
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Rust Serde Patterns

## Basic Derive

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct User {
    id: u64,
    name: String,
    email: String,
}

let user = User { id: 1, name: "Alice".into(), email: "alice@example.com".into() };
let json = serde_json::to_string(&user)?;
let back: User = serde_json::from_str(&json)?;
```

## Field Attributes

```rust
#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct ApiUser {
    #[serde(rename = "user_id")]
    id: u64,

    display_name: String,   // serialized as "displayName"

    #[serde(skip_serializing_if = "Option::is_none")]
    avatar_url: Option<String>,

    #[serde(default)]
    is_active: bool,

    #[serde(skip)]
    internal_cache: String,

    #[serde(with = "chrono::serde::ts_seconds")]
    created_at: chrono::DateTime<chrono::Utc>,
}
```

## Enum Serialization

```rust
// Internally tagged with content field
#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "type", content = "data")]
enum Event {
    UserCreated { user_id: u64, email: String },
    OrderPlaced { order_id: u64, total: f64 },
}
// {"type":"UserCreated","data":{"user_id":1,"email":"..."}}

// Untagged — tries each variant
#[derive(Debug, Serialize, Deserialize)]
#[serde(untagged)]
enum StringOrInt {
    String(String),
    Int(i64),
}

// Rename variants
#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
enum Status { Active, Inactive, PendingReview }
```

## Flattening Nested Structs

```rust
#[derive(Debug, Serialize, Deserialize)]
struct Address { street: String, city: String, country: String }

#[derive(Debug, Serialize, Deserialize)]
struct Person {
    name: String,
    #[serde(flatten)]
    address: Address,
}
// {"name":"Alice","street":"123 Main St","city":"NYC","country":"US"}
```

## Custom Serialize/Deserialize

```rust
use serde::{Deserializer, Serializer, de};

fn serialize_hex<S: Serializer>(val: &u64, s: S) -> Result<S::Ok, S::Error> {
    s.serialize_str(&format!("{val:#010x}"))
}

fn deserialize_hex<'de, D: Deserializer<'de>>(d: D) -> Result<u64, D::Error> {
    let s = String::deserialize(d)?;
    u64::from_str_radix(s.trim_start_matches("0x"), 16).map_err(de::Error::custom)
}

#[derive(Serialize, Deserialize)]
struct Token {
    #[serde(serialize_with = "serialize_hex", deserialize_with = "deserialize_hex")]
    value: u64,
}
```

## Multiple Formats

```toml
[dependencies]
toml = "0.8"
bincode = "1"
```

```rust
// TOML config files
let config: Config = toml::from_str(&std::fs::read_to_string("config.toml")?)?;
let serialized = toml::to_string_pretty(&config)?;

// Bincode (binary, fast, compact)
let encoded: Vec<u8> = bincode::serialize(&data)?;
let decoded: MyData = bincode::deserialize(&encoded)?;
```

## Dynamic JSON with Value

```rust
use serde_json::{json, Value};

let payload = json!({
    "user": { "id": 42, "name": "Alice" },
    "version": 1
});

let name = payload["user"]["name"].as_str().unwrap_or("unknown");

// Merge two objects
fn merge(base: Value, overrides: Value) -> Value {
    match (base, overrides) {
        (Value::Object(mut a), Value::Object(b)) => {
            a.extend(b);
            Value::Object(a)
        }
        (_, b) => b,
    }
}
```

## Common Anti-Patterns

- **`Vec<u8>` when you want base64** — use `#[serde(with = "base64")]` or a newtype wrapper
- **`serde_json::Value` for known schemas** — use typed structs; `Value` only for truly dynamic data
- **Panicking on parse with `.unwrap()`** — always handle `Result` from serde operations
- **Mixing `rename_all` and per-field `rename` carelessly** — `rename_all` applies first, `rename` overrides
- **Deserializing untrusted input without size limits** — add bounds to prevent DoS via huge payloads
