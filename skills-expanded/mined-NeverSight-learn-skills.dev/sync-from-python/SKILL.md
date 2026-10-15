---
name: sync-from-python
description: Forward-port one exoclaw Python package (core or plugin) into its exoclaw-go module. Trigger on "sync <package> from python", "forward-port <package>", "bring <module> up to date with python", or any request to update a Go module to track a newer Python release.
---

# Syncing a Python exoclaw package into exoclaw-go

exoclaw-go is a file-by-file port. Each Go module pins to one Python
package version (see `README.md` → "Source parity"). This skill walks
through the routine for forward-porting that pin one release at a time.

## Where the upstream Python lives

| Python package | Source path |
|---|---|
| `exoclaw` (core) | `~/dev/exoclaw/` |
| any `exoclaw-<plugin>` | `~/dev/exoclaw-plugins/packages/exoclaw-<plugin>/` |

If those checkouts are stale: `git -C <path> fetch && git -C <path>
checkout main && git -C <path> pull`.

## Step 1: read the pin from the README

Open `README.md` → "Source parity" table. Note the **currently-pinned
version** for the Go module you're updating.

## Step 2: get a focused diff of the Python changes

```bash
# In the Python repo:
git -C <python-path> log --oneline v<PINNED>..HEAD -- <package-subdir>
```

For core: `<python-path> = ~/dev/exoclaw`, `<package-subdir> = exoclaw`.
For plugins: `<python-path> = ~/dev/exoclaw-plugins`,
`<package-subdir> = packages/exoclaw-<plugin>`.

Then for the file-by-file plan:

```bash
git -C <python-path> diff v<PINNED>..HEAD -- <package-subdir> | less
```

If the pinned version isn't tagged, find the commit via `git -C
<python-path> log --grep='version = "<PINNED>"'` or by reading
`pyproject.toml` history.

## Step 3: mirror the diff file-by-file in the Go module

**This is non-negotiable: never do MVP slices or pick-and-choose.** The
discipline is a one-to-one source tree. Cherry-picking silently drops
edge cases.

For each changed Python file:

1. Find the corresponding Go file in the matching Go module. The
   naming is parallel: `exoclaw/agent/loop.py` →
   `exoclaw/agent/loop.go`. Subdirectories mirror exactly.
2. Apply the equivalent Go change.
3. Common translations:
   - Python `Protocol` / `Protocol[T]` → Go `interface`
   - Python `asyncio.Queue` → `chan` (usually buffered)
   - Python async generator → Go `chan T, chan error` pair (see
     `xhttp.Client.IterLines` for the shape)
   - Python `ContextVar` → values on `context.Context`
   - Python `@dataclass` with kwargs → Go struct + `Options{}` builder
   - Python `asyncio.gather` → `errgroup.WithContext`
4. If the upstream change adds a new file, add the corresponding `.go`
   file; if it removes one, remove it here too.

## Step 4: handle protocol surface changes

Watch for these — they ripple beyond the file being edited:

- New method on `LLMProvider` → every concrete provider needs it
- New `ChatParams` field → wire through `Chat()` to the request-body
  builder
- New `Tool` method → every tool impl plus `ToolBase` defaults
- New `Conversation` method → `DefaultConversation` plus any test stubs

## Step 5: build + test

Each module has its own test suite. From repo root:

```bash
go build ./...
go test ./...
```

If a sibling module references the one you changed (via `go.work`),
its tests pick up the new code automatically.

## Step 6: update the README pin + commit

In `README.md` → "Source parity" table, update the version cell for
this module. Also update the "Last sync" date at the bottom.

Commit with a focused message:

```
<module>: sync to <version>

Forward-port of <package> <PREV>..<NEW>. Summary of upstream changes:
- ...
- ...
```

## Downstream check (optional)

If `hey_lefty_service`'s `WorkerDeps` or `RegistryDeps` needs new
fields the new version introduced, that's a separate PR over there.
Don't fold downstream changes into the sync commit — keep the parity
diff readable.

## When in doubt

- Read `README.md` for the current pin and module layout
- The Python source is the source of truth; if there's a behavioural
  ambiguity, prefer matching Python verbatim and add a Go-idiomatic
  comment over the divergent line
