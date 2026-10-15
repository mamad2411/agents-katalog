---
name: jo
description: >-
  Prefers `jo` (https://github.com/jpmens/jo) for constructing JSON in
  shell snippets over hand-written quoted JSON literals. Removes
  quote-escaping pitfalls, makes variable interpolation natural, and
  lets `jo` infer field types from values (with explicit coercion when
  needed).
when_to_use: >-
  Use whenever about to build a JSON payload inside a shell command or
  script — curl/HTTPie bodies, kubectl `--patch` / `--overrides` args,
  API smoke tests, config emission, jq inputs. Triggers: «собери json»,
  «json пейлоад», «curl с телом», «отправь json», «json в shell»,
  «build a json body», «POST with json», «inline json», «json payload»,
  «escape this json», «construct json in shell».
---

# jo

Build JSON in shell snippets with `jo`,
not by hand-typing a quoted JSON literal.
`jo` handles JSON quoting internally,
so shell variables interpolate cleanly
and you never juggle nested single/double quotes.

Authoritative documentation:
https://github.com/jpmens/jo
(README + `jo.md` man page).
Verify any non-trivial form against the manual before relying on it.

## Why

- Hand-written JSON in a shell string is a quote-escaping minefield.
  Inserting `$VAR` into `'{"user":"x"}'` either breaks the single quotes
  or forces an awkward `'"$VAR"'` pattern that is hard to read and easy
  to mistype.
- Typos in inline JSON (missing comma, stray quote, trailing comma)
  fail at the server,
  not at parse time —
  hard to spot in a long single-line payload.
- `jo` figures out types from the value:
  numbers, booleans, `null`, nested objects, and arrays are detected
  automatically;
  override with `-s`/`-n`/`-b` per word when the guess would be wrong
  (e.g. a numeric ID that must stay a string).
- `jo` composes:
  shell variables, command substitution, bracket-path shorthands,
  and nested `jo` calls all work without re-escaping.

## How `jo` types a value

Per the man page, the value pipeline is:

1. **Try to parse the value as JSON.**
   `5` → number,
   `true`/`false` → boolean,
   `null` → null,
   `{...}` / `[...]` → embedded object/array,
   strings that look numeric but aren't valid floats
   (e.g. `3.14159.26`) → string.
2. **If JSON parse fails,**
   check special value prefixes:
   `@file`, `%file`, `:file`
   (see *Reading from files* below).
3. **Otherwise** it's a literal string.

A missing/empty value (`k=`) becomes `null`.
Pass `-B` to disable detection of the literal strings `true`/`false`/`null`.
Globally,
`-n` drops keys with empty values
(not to be confused with the per-word `-n` coercion after `--`).

## Direct substitutions

| Don't                                  | Do                                                  |
| -------------------------------------- | --------------------------------------------------- |
| `'{"name":"alice"}'`                   | `"$(jo name=alice)"`                                |
| `'{"name":"'"$USER"'"}'`               | `"$(jo name="$USER")"`                              |
| `'{"count":5,"active":true}'`          | `"$(jo count=5 active=true)"`                       |
| `'{"value":null}'`                     | `"$(jo value=null)"` (or `"$(jo value=)"`)          |
| `'{"tags":["a","b","c"]}'`             | `"$(jo tags="$(jo -a a b c)")"`                     |
| `'{"point":[1,2]}'`                    | `"$(jo 'point[]=1' 'point[]=2')"`                   |
| `'{"geo":{"lat":10,"lon":20}}'`        | `"$(jo 'geo[lat]=10' 'geo[lon]=20')"`               |
| `'{"user":{"id":1,"name":"alice"}}'`   | `"$(jo user="$(jo id=1 name=alice)")"`              |
| `'{"code":"12345"}'` (string ID)       | `"$(jo -- -s code=12345)"`                          |

Bracket-path forms (`key[]=`, `key[sub]=`) are **one level deep only** —
`'a[b][c]=1'` silently drops `[c]` and produces `{"a":{"b":1}}`.
For deeper nesting,
use nested `jo` via command substitution.

## Syntax cheatsheet

### Value forms

- `k=v` —
  JSON-parsed then prefix-checked then literal string
  (see *How `jo` types a value*).
- `k@v` —
  boolean from a truthy value
  (`T`/`t` or non-zero numeric → `true`, else `false`);
  handy for `flag@$ENABLED`.
- `k=@file` —
  load `file` contents as a string value.
- `k=%file` —
  load `file` as base64-encoded string.
- `k=:file` —
  parse `file` as JSON and embed.
- `k:=file` or `k:=-` —
  same as `k=:file` but as an operator;
  `-` reads JSON from stdin.

To use a literal `@`, `%`, or `:` at the start of a string value,
escape it with `\`:
`twitter='\@jpmens'`,
`vimcmd='\:split'`,
`uri='\\%20'`.

### Bracket paths (one level)

- `'name[]=v1' 'name[]=v2'` —
  appends to the `name` array.
- `'obj[k]=v'` —
  creates `{"obj":{"k":v}}`.
- Combine `-d.`
  (path separator) for dot notation:
  `jo -d. geo.lat=10 geo.lon=20`
  is equivalent to `jo 'geo[lat]=10' 'geo[lon]=20'`.
- Always quote bracket forms —
  unquoted `[` / `]` get caught by zsh globbing
  (and bash too,
  if any expansion matches).

### Arrays

- `jo -a v1 v2 v3` —
  array of auto-typed values.
- `jo -a -- -s 123 hello -n "five"` —
  per-word coercion inside an array
  (here: `["123","hello",4]` —
  `-n` on a non-numeric string yields its length).

### Type coercion

- `jo -- -s k=v` —
  force string.
  Use for numeric IDs, version strings, phone numbers, ZIPs.
- `jo -- -n k=v` —
  force number
  (non-numeric strings become their *length*).
- `jo -- -b k=v` —
  force boolean
  (empty → `false`, anything else → `true`).
- `--` is mandatory before the word list whenever the first word starts
  with `-`;
  pass it always for consistency with the manual.

### Global options

The two most-used:

- `-p` —
  pretty-print
  (drop for production payloads).
- `-a` —
  emit an array instead of an object.

For the full option list
(`-B`, `-D`, `-n` global, `-d sep`, `-f file`, `-e`, `-o`, `-v`/`-V`,
plus per-word coercion semantics after `--`)
see `references/options.md`.

## Idioms

`curl` POST with a body:

```sh
curl -X POST https://api.example.com/v1/users \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$(jo name="$NAME" email="$EMAIL" active=true)"
```

Bracket shorthand for one-level nesting
(no nested `jo` substitution needed):

```sh
curl -X POST https://api.example.com/v1/orders \
    -H "Authorization: Bearer $TOKEN" \
    -d "$(jo \
        'customer[id]='"$CUSTOMER_ID" \
        'customer[name]='"$CUSTOMER_NAME" \
        'items[]='"$SKU_A" \
        'items[]='"$SKU_B")"
```

Nested deeper than one level —
build via command substitution
(or stash in a variable):

```sh
payload=$(jo \
    name="$NAME" \
    address="$(jo street="$STREET" city="$CITY")" \
    tags="$(jo -a admin user)")

curl -X POST -d "$payload" https://api.example.com/v1/users
```

`kubectl` patch:

```sh
kubectl patch deployment web \
    --type=merge \
    --patch "$(jo spec="$(jo replicas=3)")"
```

Numeric ID that must stay a string
(otherwise `jo` emits `"id":12345` as a number):

```sh
curl -X POST -d "$(jo -- -s id=12345 name="$NAME")" \
    https://api.example.com/v1/users
```

Modify an existing JSON document:

```sh
curl -sSL https://api.example.com/v1/config \
    | jo -f - updated_at="$(date -Iseconds)" version="$NEW_VERSION"
```

## When NOT to use `jo`

### Large, fixed JSON document

A heredoc with literal JSON is clearer than a long chain of `jo` calls,
and the JSON can be copy-pasted from API docs without translation:

```sh
curl -X POST -d @- https://api.example.com/v1/config <<'JSON'
{
  "feature_flags": {
    "alpha": true,
    "beta": false
  },
  "limits": {
    "rps": 100,
    "burst": 200
  }
}
JSON
```

### `jo` not available on the host

Some minimal CI images or locked-down servers lack it.
Fall back to a heredoc;
do **not** fall back to fragile inline quoted JSON.

## Installing `jo`

- macOS: `brew install jo` or `sudo port install jo`
- Debian/Ubuntu: `apt install jo`
- Fedora: `dnf install jo`
- Alpine: `apk add jo`
- Gentoo: `emerge jo`
- Arch: `pacman -S jo` (in `extra`)
- Snap: `snap install jo`
- Windows: `scoop install jo`
- Docker: `docker run --rm jpmens/jo ...`
- From source: https://github.com/jpmens/jo

`jo` is not in the default aqua/mise short-name registry;
on a mise-managed host install via the package manager
or via `ubi:jpmens/jo`.

## Scope

Applies anywhere a shell snippet emits JSON:

- `Bash` tool invocations.
- Snippets in `SKILL.md` / `README.md` / docs.
- Scripts under `scripts/`.
- Makefile recipes.
- CI configs.
- API smoke-test instructions.

If you encounter a hand-written inline JSON string while editing a file,
replace it with the equivalent `jo` form as part of the same edit.
