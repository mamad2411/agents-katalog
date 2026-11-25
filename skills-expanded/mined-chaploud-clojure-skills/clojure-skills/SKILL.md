---
name: clojure-skills
description: >-
  Clojure/ClojureScript/ClojureDart development skill. Activates when
  working with .clj, .cljs, .cljc, .cljd, .edn, .bb, .lpy files. Provides
  structural search and editing of S-expressions, nREPL evaluation,
  runtime queries via cider-nrepl, and static navigation via clojure-lsp.
compatibility: >-
  Every command is a shell command, so any agent with shell access can use
  them. The optional automatic paren-repair hooks are Claude Code specific.
license: EPL-2.0
paths:
  - "**/*.clj"
  - "**/*.cljs"
  - "**/*.cljc"
  - "**/*.cljd"
  - "**/*.edn"
  - "**/*.bb"
  - "**/*.lpy"
user-invocable: false
---

# Clojure Development Skill

All commands live under a single binary, `clj-skill`.
Line and column numbers are **1-based everywhere**, matching editors and ripgrep.

## Check the environment first

!`command -v clj-skill >/dev/null && clj-skill doctor || echo "clj-skill NOT INSTALLED — git clone https://github.com/chaploud/clojure-skills.git ~/clojure-skills && cd ~/clojure-skills && bb install"`

The report above says which command groups work here. Do not attempt a group it
reports as unavailable — use the alternative named below instead.

## Which command to reach for

| Goal | Command | Needs |
|---|---|---|
| Map a large file before reading it | `clj-skill outline FILE` | nothing |
| Find code by its *shape* | `clj-skill find PATTERN [PATH…]` | nothing |
| Rewrite a whole top-level form | `clj-skill replace FILE PATTERN` | nothing |
| Find code by its *text* | `rg` | ripgrep |
| Balance delimiters / format | `clj-skill repair FILE…` | nothing |
| Evaluate code | `clj-skill repl eval` | nREPL |
| Callers of a function | `clj-skill cider refs SYM` | cider-nrepl |
| Where a symbol is defined | `clj-skill cider info SYM` | cider-nrepl |
| Run tests | `clj-skill cider test [NS…]` | cider-nrepl |
| Explain the last exception | `clj-skill cider stacktrace` | cider-nrepl |
| Look inside a huge value | `clj-skill cider inspect CODE` | cider-nrepl |
| References / definition / hover | `clj-skill lsp …` | clojure-lsp |
| Project diagnostics | `clj-skill lsp diagnostics` | clojure-lsp |

`cider` answers about **what is loaded right now**; `lsp` answers from a
**static index** and works on code that was never evaluated. When both are
available, prefer `lsp` for navigation and `cider` for behaviour — tests,
exceptions and values.

## Structural commands (always available)

### outline — read a big file cheaply

```bash
clj-skill outline src/my/ns.clj
```

Prints `path:START-END: <first line of the form>` for every top-level form. Use
it before reading a file over a few hundred lines, then read only the range you
need with `sed -n 'START,ENDp' FILE`.

### find — search by shape, not by text

```bash
clj-skill find '(defmethod &)' src
clj-skill find '(rf/reg-event-fx _ &)' src/app --limit 100
```

A pattern is a Clojure form in which:

- `_` matches any single form
- `&` matches the rest of a sequence, and must be its last element

Everything else matches exactly as written:

- collection type counts — `(a b)` does not match `[a b]`; a list pattern also
  matches `#(...)`, so `(assoc _ :id &)` finds `#(assoc % :id 1)`
- arity is exact without a trailing `&` — `(inc _)` matches `(inc 1)`, not `(inc 1 2)`
- collections match in written order — `{:a 1 :b 2}` does not match `{:b 2 :a 1}`
- `'x` and `(quote x)` are different forms and do not match each other
- metadata is seen through — `(defn foo &)` matches `(defn ^:private foo [] 1)`
- `#_` forms are skipped; `(comment …)` blocks are searched

Prints `path:line:col: <first line of the match>`. Stops after 50 matches
(`--limit N`) without reading later files. A keyword pattern works as is
(`find :status src`); a pattern starting with `-` needs `--` before it.

Directories are walked by extension, plus extensionless `bb` scripts. Skipped
below the directory you name: `node_modules target build out .git .cpcache
.shadow-cljs .lsp .clj-kondo .dart_tool .cljd`, and any directory with its own
`.git` (a worktree or submodule) — name it explicitly to search it.

Use `rg` when you are looking for a name or a string. Use `find` when the
*shape* is the question and no substring identifies it:

```bash
clj-skill find '(defn _ [_ _] &)' src        # every two-argument defn
clj-skill find '(defn _ _ {:status _} &)' src # a handler taking a status map
clj-skill find '(assoc _ :id &)' src          # calls that set :id
clj-skill find '(defmethod _ [::a ::b] &)' src # one multimethod dispatch value
clj-skill find '{:status status}' src         # an argument destructured this way
```

That last one is the case `rg` cannot narrow: `:status` appears everywhere, but
`{:status status}` as a *form* appears only where it is destructured.

### replace — edit a whole form

```bash
clj-skill replace src/my/ns.clj '(defn my-fn &)' <<'EOF'
(defn my-fn [x]
  (inc x))
EOF
```

Reads the new form from stdin and swaps it in, leaving every other byte of the
file — comments, blank lines, indentation of neighbouring forms — untouched.

It **refuses to write** unless the pattern matches exactly one top-level form,
and lists the candidates — or, when only nested forms match, where they are.
Prefer this over `Edit` for whole-function rewrites: it cannot mismatch on
whitespace and cannot unbalance the file. `--dry-run` reports which form would
change without writing.

### repair — fix delimiters

```bash
clj-skill repair src/my/ns.clj              # in place
echo '(defn f [x] (+ x 1' | clj-skill repair # as a filter
```

**Do not hand-count parentheses.** If a file has unbalanced delimiters, run
`clj-skill repair` on it. It infers missing closers from indentation, so re-read
the form it fixed. If it cannot balance the file, tell the user; do not guess.
It also formats the file, but only when a cljfmt config (`.cljfmt.edn` …)
applies to it — a project on another formatter is left alone.

For a codemod beyond `replace`, read `references/rewrite-clj-codemods.md` first.

## REPL

Pass code in a `<<'EOF'` heredoc, so no shell rewrites `!`, `$` or quotes in it.

```bash
clj-skill repl eval -p 7888 <<'EOF'
(require '[my.ns :as n] :reload)
(n/my-fn 42)
EOF
```

- `clj-skill repl ports` — nREPL servers on this machine, and which have cider-nrepl
- `--port` may be omitted when one server runs in this directory or a parent of
  it (the deepest wins); otherwise you are told to pass it
- One session per agent session and server, whatever the working directory:
  `*ns*`, `*1` and `*e` carry over between calls. Calls run one at a time, so
  parallel calls wait for each other. Use `:reload` for a namespace you just edited
- Exit 1 when any form throws, so `repl eval "(require 'x-test :reload)" && …`
  stops on a compile error. `-t MS` is a deadline for the whole eval (default
  2 min): it interrupts and exits 124; if the next eval times out too, `repl reset`
- Output is cut after 50000 characters (`--max-output 0` for all of it)
- Unbalanced code is repaired before it is sent, with a `;; delimiters repaired`
  note — check that it evaluated what you meant
- `clj-skill repl reset -p PORT` closes the session; vars already defined stay

A form that switches the evaluation environment — `(shadow/repl :build)`,
`:cljs/quit` — takes effect for the **next** call, not for the rest of the
heredoc: nREPL evaluates the heredoc as one request. Send the switch on its own:

```bash
clj-skill repl eval -p 7888 '(shadow/repl :app)'
clj-skill repl eval -p 7888 '(js/parseInt "42")'
```

## Runtime queries (cider-nrepl)

```bash
clj-skill cider deps my-fn --ns my.ns        # what it calls
clj-skill cider test my.ns-test              # failures only, with expected/actual
clj-skill cider test my.ns-test/one-test     # a single test var
clj-skill cider retest                       # only what failed last time
clj-skill cider ops                          # what this server supports
```

`--ns` defaults to the session's current namespace. `refs` and `deps` exit 1
when SYM does not resolve there, so `;; no callers` means it resolved and
nothing loaded calls it.

`test` runs only namespaces the REPL has loaded — require the test namespace
first. It exits 1 when a test fails or when no test ran at all.

`stacktrace` reads the last exception of the session — every cause, with its
ex-data — and prints project frames only; `--all` for the rest.

On babashka only part of cider is built in (no refs/deps/apropos/ns-vars);
`cider ops` says what is there.

## Static navigation (clojure-lsp)

```bash
clj-skill lsp diagnostics --file src/my/ns.clj
clj-skill lsp references --file src/my/ns.clj --line 10 --col 5
clj-skill lsp definition --file src/my/ns.clj --line 10 --col 5
clj-skill lsp hover      --file src/my/ns.clj --line 10 --col 5
```

- `--line`/`--col` must be on a symbol; a paren, a blank or a position past the
  line is an error, not an empty answer. The output starts with `;; symbol: X`
- Every query first re-reads files changed since the last one (`;; re-read N
  changed file(s)`). Past 400 changed files (a branch switch) it indexes again
  from scratch instead, which is faster. If re-reading cannot catch up in 20 s, or
  clojure-lsp fails on a file, it still answers, says the answer may be stale and
  why, and exits 1 — on every query until it is resolved
- An empty answer comes with the `rg` command that cross-checks it. Run that
  before deleting or renaming anything
- references/definition print `path:line:col: [definition] <source line>`. A
  location inside a dependency is `/abs/foo.jar:inner/ns.clj:LINE:COL`
- `diagnostics` starts with a count by severity and exits 1 only for errors.
  Without `--file` it covers the whole project
- The root is the nearest `deps.edn`/`project.clj`/`bb.edn`/`shadow-cljs.edn`
  above `--file`, or above the working directory; with none, pass `--project-root`

A bridge per project keeps clojure-lsp running between calls and turns, and
exits after 30 minutes without a query. The first query on a large project waits
for indexing (minutes when cold); `clj-skill lsp-bridge warm ROOT` does it ahead
of time. `lsp status` names the log to read when a query times out.

## Notes

- Non-zero exit means the command could not do its job — or, for `cider test`
  and `lsp diagnostics`, found a failure or an error. `;; no …` lines mean the
  search ran and found nothing
- Options go before positional arguments; a misspelled or misplaced option is
  an error
