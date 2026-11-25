---
name: idalib-cli
description: Analyse binaries with IDA Pro's IDALib through the stateless `idalib-cli` tool - inspect segments, functions, CFG, disassembly, Hex-Rays pseudo-code, strings, xrefs, and edit IDB state (comments, bookmarks). Every command takes -d/--db and returns JSON.
---

# idalib-cli

Agent-first CLI for the IDA Pro IDALib. **Stateless**: every command takes
`-d/--db <PATH>` — an IDB file (`.i64`) or a binary (an IDB is created next to
it on first use). All state lives in the IDB file; every command prints one
JSON document on stdout (errors on stderr, non-zero exit).

## When to use

Reverse-engineering, triage, or deep inspection of any binary; decompiling
functions; finding xrefs/strings; annotating an IDB; bulk-analysing many
samples concurrently.

## Core model

```sh
idalib-cli -d <bin-or-i64> <command> [args]   # → one JSON document
```

- Pass a **binary** → IDB auto-created next to it (`<bin>.i64`), then opened.
- Pass an **.i64** → reopened directly, all prior state intact.
- Omitted `-a <ea>` addresses accept `0x401000` or `401000`.

## Setup check (once per environment)

```sh
idalib-cli info        # → { idalib_cli, idalib_rs, ida_version, license, ... }
```

If it errors, the tool isn't built/installed — see the repo README (needs
`IDADIR` + absolute `IDASDKDIR`, then `cargo install --path .`).

## Command map

| Goal | Command |
| --- | --- |
| DB paths / size / state | `-d <db> db info` |
| Filetype, compiler, bitness | `-d <db> meta` |
| Processor | `-d <db> processor` |
| All segments / one segment | `-d <db> segments` / `segments-by-range -a <ea>` |
| Function list (skip lib/thunk) | `-d <db> functions [-u]` |
| One function: CFG, blocks, xrefs | `-d <db> function -a <ea>` |
| Disassemble N instructions | `-d <db> disasm -a <ea> [-n N]` |
| Hex-Rays pseudo-code | `-d <db> decompile -a <ea>` |
| Single instruction | `-d <db> insn -a <ea>` |
| Strings / names / entries | `-d <db> strings` / `names` / `entries` |
| Xrefs to / from an address | `-d <db> xrefs [-a <ea>] [--all] [--from]` |
| Search text / immediate / bytes | `-d <db> find --text S` / `--imm 0xV` / `--pattern 4889e5` |
| Raw bytes / integers | `-d <db> bytes -a <ea> [-n N] [--width byte\|word\|dword\|qword]` |
| Rename a function / label | `-d <db> rename -a <ea> -n <name>` |
| Apply a C type (prototype / data) | `-d <db> set-type -a <ea> -t "int f(int, char *);"` |
| Comments (get/set/append/remove) | `-d <db> comments <verb> -a <ea> [-c "text"]` |
| Bookmarks (list/add/get/remove) | `-d <db> bookmarks <verb> -a <ea> [-d "desc"]` |
| FLIRT signatures | `-d <db> signatures --make` |
| Many ops, IDB opened once | `-d <db> batch -- "op1" "op2" ...` |
| One op, many DBs, concurrent | `parallel -d <list\|glob> [--jobs N] -- "op"` |

## Recommended workflow

**1. Triage** — what is this thing?

```sh
idalib-cli -d ./sample meta
idalib-cli -d ./sample segments
idalib-cli -d ./sample strings
idalib-cli -d ./sample functions -u        # user code only
```

**2. Focus** — read the interesting parts.

```sh
idalib-cli -d ./sample decompile -a 0x401000     # pseudo-code (best readability)
idalib-cli -d ./sample function -a 0x401000      # CFG + blocks + xrefs
idalib-cli -d ./sample disasm -a 0x401000 -n 20  # raw instructions
```

**3. Follow the data** — who references what / what does it reference?

```sh
idalib-cli -d ./sample xrefs -a 0x401000 --all        # incoming
idalib-cli -d ./sample xrefs -a 0x401000 --from --all # outgoing (calls)
idalib-cli -d ./sample find --text "MAGIC"            # locate a string
idalib-cli -d ./sample find --imm 0x1337              # locate a magic constant
idalib-cli -d ./sample bytes -a 0x401000 -n 32        # raw bytes
```

**4. Name & annotate** — persist findings for future turns/agents.

```sh
idalib-cli -d ./sample rename -a 0x401000 -n parse_config
idalib-cli -d ./sample set-type -a 0x401000 -t "int parse_config(const char *);"
idalib-cli -d ./sample comments set -a 0x401000 -c "parses config, see 0x402100"
idalib-cli -d ./sample bookmarks add -a 0x401000 -d "entry point"
```

## Batch & parallel (efficiency)

- `batch` — several facts about **one** binary, IDB opened once:
  ```sh
  idalib-cli -d ./sample batch -- "meta" "segments" "decompile -a 0x401000"
  ```
- `parallel` — one op across **many** binaries, one subprocess each
  (IDALib is not thread-safe; isolation is by process):
  ```sh
  idalib-cli parallel -d "./samples/*.i64" --jobs 8 -- "functions -u"
  idalib-cli parallel -d "./a.i64,./b.i64" -- "decompile -a 0x401000"
  ```
- Compose them for bulk work:
  ```sh
  idalib-cli parallel -d "./samples/*.bin" -- "batch -- meta functions -u"
  ```

## Tips for agents

- JSON contract: parse stdout; treat `error: ...` on stderr as failure.
- Prefer `batch` over several separate invocations — it avoids reopening the
  IDB repeatedly (large IDBs cost seconds per open).
- `decompile` needs the Hex-Rays decompiler; without it the command fails
  cleanly — fall back to `disasm` + `function`.
- Only one process may use an IDB at a time. `parallel` respects this; for
  manual multi-agent work, give each agent its own `-d` target.
- Annotate as you go — comments/bookmarks persist in the IDB and are visible
  to later turns and other agents.
- Statelessness means "session" = the IDB path. To resume earlier work, just
  pass the same `-d` path again.
