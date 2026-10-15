---
name: dasel
description: >
  Use dasel v3 CLI to query, modify, and transform structured data (JSON, YAML, TOML, XML, CSV, HCL, INI).
  Load this skill whenever the user wants to: read/write/convert data files with dasel, write dasel query expressions,
  filter/map/transform structured data on the command line, edit config files in place using dasel, pipe data through dasel in shell scripts,
  or asks about dasel syntax, functions, or CLI flags. Even if they just say "use dasel to..." or "dasel query for...", load this skill.
---

# Dasel v3

Dasel (Data-Select) is a CLI tool for querying, modifying, and converting structured data files using a consistent query syntax across formats.

> Docs are bundled in `references/`. Read them when you need deeper detail on a topic.

---

## CLI basics

```bash
# Read from stdin, specify input format
echo '{"name":"Tom"}' | dasel -i json 'name'
# => "Tom"

# Read from a file via stdin redirection
dasel -i yaml 'database.host' < config.yaml

# Convert formats: read JSON, output YAML
cat data.json | dasel -i json -o yaml

# Output the whole document (needed when modifying)
echo '{"a":1}' | dasel -i json --root 'a = 2'
# => {"a": 2}
```

**Key flags:**

| Flag | Short | Purpose |
|------|-------|---------|
| `--in FORMAT` | `-i` | Input format (json, yaml, toml, xml, csv, hcl, ini) |
| `--out FORMAT` | `-o` | Output format |
| `--root` | | Output the full document, not just the selected value |
| `--var name=fmt:file:path` | | Pass a file as a named variable |
| `--read-flag key=val` | | Parser-specific read options |
| `--write-flag key=val` | | Parser-specific write options |
| `--config PATH` | `-c` | Path to dasel config file (default: `~/dasel.yaml`) |
| `--unstable` | | Enable unstable/experimental features |

---

## Query syntax

Queries are dot-chained **accessors** and **function calls**, terminated with `;` when using multiple statements.

```
# Access nested fields
user.address.city

# Array index (zero-based)
users[0].name

# Range slice
users[0:4]

# Assign (modifies the value in the document)
user.name = "Alice"

# Variables - $root is stdin, $this is current element
$root.users.filter(active == true).map(name)
```

**Multi-statement queries** (use `;` to separate, last statement is the output):
```
$active = $root.users.filter(active == true);
$active.map(name)
```

### Environment variables
```bash
GREETING=hello NAME=tom dasel '$GREETING + " " + $NAME'
# => "hello tom"
```

---

## Common patterns

### Read a value
```bash
echo '{"foo":{"bar":"baz"}}' | dasel -i json 'foo.bar'
# => "baz"
```

### Modify a value (output full document)
```bash
echo '{"foo":"old"}' | dasel -i json --root 'foo = "new"'
# => {"foo": "new"}
```

### Edit a file in place
```bash
dasel -i yaml --root 'server.port = 9090' < config.yaml > config.yaml.tmp \
  && mv config.yaml.tmp config.yaml
```
> Note: there is no `-f` flag for data files in v3. Always use stdin (`< file` or `cat file |`).
> Note: always go via a temp file — bash truncates the target before dasel reads it.

### Filter an array
```bash
echo '{"users":[{"name":"Alice","active":true},{"name":"Bob","active":false}]}' \
  | dasel -i json 'users.filter(active == true).map(name)'
# => ["Alice"]
```

### Map / transform
```bash
echo '[1,2,3]' | dasel -i json 'map($this * 2)'
# => [2, 4, 6]
```

### Modify elements in place with `each`
```bash
echo '[1,2,3]' | dasel -i json 'each($this = $this + 1)'
# => [2, 3, 4]
```

### Default / coalesce
```bash
# Fall back to a default if path missing
dasel -f config.yaml 'server.timeout ?? 30'
```

### Conditional
```bash
dasel -f data.json 'if(count > 5) { "many" } else { "few" }'
```

### Recursive descent — find all values by key
```bash
# All values with key "name" at any depth
dasel -f data.json '..name'

# All values at any depth
dasel -f data.json '..*'
```

### Predicate-based deep search
```bash
dasel -f data.json 'search(has("id") && has("name"))'
```

### Format conversion
```bash
cat file.json | dasel -i json -o yaml
cat file.yaml | dasel -i yaml -o toml
```

### Build a new object
```bash
echo '{"first":"Tom","last":"Wright"}' \
  | dasel -i json '{"fullName": first + " " + last}'
```

### Spread operator
```bash
# Merge objects
echo '{"a":1}' | dasel -i json '{$this..., "b": 2}'
# => {"a":1,"b":2}

# Append to array
echo '[1,2,3]' | dasel -i json '[$this..., 4, 5]'
# => [1,2,3,4,5]
```

---

## Supported formats

| Format | Read | Write | Notes |
|--------|------|-------|-------|
| json   | ✓    | ✓     | |
| yaml   | ✓    | ✓     | |
| xml    | ✓    | ✓     | See `--read-flag xml-mode=structured` |
| csv    | ✓    | ✓     | All values as strings; `--read-flag csv-delimiter=;` |
| hcl    | ✓    | ✓     | `--read-flag hcl-block-format=array` |
| toml   | ✓    | ✓     | Generally working; unsorted maps |
| ini    | ✓    | ✓     | Basic sections + key values only |

---

## Key functions

| Function | Description | Example |
|----------|-------------|---------|
| `filter(pred)` | Filter array by predicate | `arr.filter($this > 1)` |
| `map(expr)` | Transform each element | `arr.map($this * 2)` |
| `each(expr)` | Iterate and modify in place | `arr.each($this = $this+1)` |
| `search(pred)` | Recursive predicate search | `search(has("key"))` |
| `has(key)` | Check key/index exists | `has("name")` |
| `len(x)` | Length of array/string | `len($root.items)` |
| `keys(obj)` | Keys of a map | `keys($root.config)` |
| `add(a,b)` | Add / concatenate | `add(1, 2)` |
| `join(arr, sep)` | Join array to string | `join(tags, ",")` |
| `replace(str,old,new)` | String replace | `replace(name,"_"," ")` |
| `sortBy(key)` | Sort array of objects | `users.sortBy(name)` |
| `reverse(arr)` | Reverse array | `reverse(items)` |
| `min(arr)` / `max(arr)` | Min/max of numbers | `min(scores)` |
| `sum(arr)` | Sum numbers | `sum(prices)` |
| `toString(x)` | Convert to string | `toString(id)` |
| `toInt(x)` | Convert to int | `toInt(count)` |
| `typeOf(x)` | Type name | `typeOf(value)` |
| `parse(fmt, str)` | Parse a string as a format | `parse("json", raw)` |
| `readFile(path)` | Read a file | `readFile("x.json")` |
| `base64e(str)` | Base64 encode | `base64e(token)` |
| `base64d(str)` | Base64 decode | `base64d(encoded)` |

> For full function signatures and examples, see `references/functions.md`.

---

## Reference files

| File | When to read |
|------|-------------|
| `references/syntax.md` | Deep dive: types, arrays, objects, conditionals, spread, coalesce, branches, regex, recursive descent |
| `references/functions.md` | All function signatures with examples |
| `references/input-output.md` | Stdin/stdout, file editing, variables, format flags |

---

## Tips

- Always use `--root` when modifying data and wanting the full document back.
- Use `;` to write multi-statement queries for clarity.
- `$root` is the stdin document; `$this` is the current element inside functions.
- For in-place file edits, always redirect to a `.tmp` file first, then `mv`.
- The ternary operator (`? :`) is not yet implemented — use `if/else` form instead.
- `branch` is unstable — requires `--unstable` flag.
