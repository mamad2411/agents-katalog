---
name: tooling-jq
description: Use when processing JSON on the command line with jq — filtering, mapping, group_by, select, recursive descent, and the one-liners that come up daily.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: tooling
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [tooling-shell-fish, tooling-ripgrep, tooling-fzf, tooling-git-advanced]
---

# jq — JSON Processing on the Command Line

`jq` is a small functional language for filtering, projecting, and transforming JSON streams. Every API in the world returns JSON; `jq` is how you make it useful from a pipe.

**Core principle:** filters are functions from a value to a stream of values. `.foo` is a function that, given an object, emits the value of `foo`. Compose with `|`. That's the whole model.

## The five filters you'll use 80% of the time

```sh
echo '{"name": "alice", "age": 30}' | jq '.name'
# "alice"

echo '[1,2,3,4,5]' | jq '.[]'
# 1 2 3 4 5 (one per line — a stream)

echo '[{"n":1},{"n":2}]' | jq '.[] | .n'
# 1 2

echo '[1,2,3]' | jq 'map(. * 2)'
# [2, 4, 6]

echo '[{"n":1},{"n":2},{"n":3}]' | jq '.[] | select(.n > 1)'
# {"n":2} {"n":3}
```

`.foo` / `.["foo"]` / `.[0]` access. `.foo?` suppresses errors on missing keys. `[]` iterates (yields a stream of elements).

## Filtering — `select` is your `WHERE`

```sh
# Status-filtered API response
curl ... | jq '.items[] | select(.status == "active")'

# Multiple conditions
jq '.[] | select(.age > 18 and .country == "US")'

# Regex
jq '.[] | select(.email | test("@example\\.com$"))'

# Negation
jq '.[] | select(.deleted_at == null)'
```

`select` is a filter that passes its input through if the expression is truthy, otherwise drops it. Combine with `|` upstream and downstream like any other filter.

## Projection — `map` and object construction

```sh
# Map over a list
jq 'map({id, name})'                                  # shorthand: pulls these keys
jq 'map({id: .id, display: (.first + " " + .last)})'  # explicit

# Project from a stream (no enclosing array)
jq '.items[] | {id, name}'

# Wrap a stream back into an array
jq '[.items[] | {id, name}]'
```

`{key}` shorthand pulls `key` from the input. `{key: expr}` builds it from an expression. `map(f)` is sugar for `[.[] | f]`.

## Grouping and aggregation

```sh
# Group orders by user, sum amounts per user
jq 'group_by(.user_id) | map({user_id: .[0].user_id, total: map(.amount) | add})'

# Count by status
jq 'group_by(.status) | map({(.[0].status): length}) | add'

# Sort by a field
jq 'sort_by(.created_at)'
jq 'sort_by(-.amount)'                                # descending via negation — NUMBERS only; strings → null sort keys
jq 'sort_by(.name) | reverse'                         # descending for strings/dates: sort, then reverse
```

`group_by(f)` returns a list of lists, sorted by `f`, grouped where `f` is equal. `add` sums numbers (or concatenates strings/arrays). `length` is universal — strings, arrays, objects, null.

## Recursive descent — `..` finds anything anywhere

```sh
# Every email anywhere in the document
jq '.. | .email? // empty' input.json

# Every "url" key
jq '[.. | .url? // empty] | unique'

# Strings only
jq '[.. | strings]'

# Objects of a particular shape
jq '[.. | objects | select(.type == "user")]'
```

`..` emits every value in the tree recursively. Filter with `select` or type guards (`strings`, `numbers`, `objects`, `arrays`, `booleans`, `nulls`). `// empty` swallows nulls so the stream stays clean.

## The flags you should know

```sh
jq -r '.name'              # raw output (strings without quotes — pipe-friendly)
jq -c '.'                  # compact (one object per line — for ndjson)
jq -s '.'                  # slurp (reads all input into a single array)
jq -n '{ts: now}'          # null input (compute from scratch)
jq -e '.[0]'               # error exit if filter produces null/false (script-friendly)
jq --arg name "alice" '.users[] | select(.name == $name)'   # inject shell var safely
jq --argjson n 5 '.[] | select(.count > $n)'                # inject as JSON number
jq --slurpfile cfg config.json '. + $cfg[0]'                # load file as variable
```

`--arg` is **always** how you inject shell values. Building filter strings via shell interpolation invites injection bugs and quoting nightmares.

**Filter strings MUST be static — never user-controlled.** `jq "$USER_FILTER" data.json` is a code-injection primitive: an attacker passes `$ENV` as the filter and dumps every environment variable (`AWS_SECRET_ACCESS_KEY`, `DATABASE_URL`, every secret in the process env), or pipes through `@sh` to construct shell payloads. The hardcoded filter is the trust boundary; `--arg` / `--argjson` / `--slurpfile` carry untrusted DATA. Wrappers exposing arbitrary filter strings to web users or other untrusted sources are equivalent to `eval`.

## ndjson — line-delimited JSON

Logs/streaming APIs emit one JSON object per line; `jq` handles this natively:

```sh
jq 'select(.level == "error") | .msg' app.ndjson    # filter ndjson
jq -c '.items[]' input.json > items.ndjson          # convert to ndjson (-c = compact)
jq -s '.' items.ndjson                              # slurp ndjson into an array
```

## Updating values — `|=`

```sh
jq '.users |= map(. + {active: true})'                # add active:true to every user
jq '(.users[] | select(.id == "u1")).name = "Alice"'  # mutate one element
jq 'del(.password)'                                   # delete a key
jq 'del(.. | .password?)'                             # delete anywhere
```

`f |= g` updates the value at path `f` using filter `g`. `del(path)` removes a path.

## Multiple files and `--slurp`

```sh
# Concat arrays from many files
jq -s 'add' a.json b.json c.json

# Index a list by key into an object
jq 'INDEX(.id)' users.json
# {"u1": {...}, "u2": {...}}

# Reverse: object to list
jq '[.[]]'
```

`INDEX(.id)` is the one-liner version of "build a lookup by ID."

## Common one-liners

```sh
# All unique values of a field
jq -r '.[] | .country' data.json | sort -u

# Pretty-print a single curl response
curl -s ... | jq .

# Extract specific fields as TSV
jq -r '.[] | [.id, .name, .email] | @tsv'

# Count items
jq 'length'              # array/object/string length
jq '[.items[]] | length' # count after filtering

# Diff two JSON files structurally
diff <(jq -S . a.json) <(jq -S . b.json)    # -S sorts keys for stable diff
```

## Gotchas

- `null` vs missing key: `.missing` returns `null`, `.[]` over `null` errors. Use `.missing?` or `// empty`.
- `-r` only affects top-level strings; nested structures still serialize as JSON.
- `--arg` is always a string; use `--argjson` for numbers/booleans/pre-parsed JSON.
- Streams vs arrays: `.items[]` is a stream; `[.items[]]` is an array. Sorting is by JSON order — `sort_by(.field)` for deterministic results.

## Anti-patterns

- Building filter strings via shell interpolation (`"${var}"`) — use `--arg`; user-controlled filter strings are eval
- Parsing JSON with grep/sed/awk because "jq isn't installed" — install it
- `jq '.foo' | jq '.bar'` in a pipeline — combine: `jq '.foo, .bar'` or `jq '{foo, bar}'`
- Forgetting `-r` and getting `"value"` instead of `value` into a shell variable; `cat file | jq ...` when `jq ... file` works
- `jq` against a 10GB file when you want a streaming parser — see `jq --stream` or `gron`

## Hand-off

Shell-side variable handling complementing `--arg`: `Skill(tooling-shell-fish)`. Finding files: `Skill(tooling-ripgrep)`. Interactive selection: `Skill(tooling-fzf)`. Git porcelain JSON: `Skill(tooling-git-advanced)`.
