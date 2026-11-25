---
name: managed-toml-block-idempotent
description: Inject a daemon-managed block into a user-owned TOML file with BEGIN/END markers, top-level dotted-key syntax, and idempotent rewrite at the top of the file.
category: agents
version: 1.0.0
tags: [toml, config, managed-block, idempotent, rewrite]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- A daemon/tool needs to write settings into a config file the user also edits.
- You can't own the whole file (user has their own config) but you must guarantee specific keys take precedence.
- TOML format specifically — the same pattern works for ini-style configs with slightly different delimiters.

## Steps

1. Use clearly-delimited markers that include a "do not edit" hint:
   ```go
   const (
     BeginMarker = "# BEGIN myapp-managed (do not edit; regenerated automatically)"
     EndMarker   = "# END myapp-managed"
   )
   ```
2. Generate the managed block using top-level dotted-key assignments — never `[section]` headers:
   ```toml
   # BEGIN myapp-managed (do not edit; regenerated automatically)
   sandbox_mode = "workspace-write"
   sandbox_workspace_write.network_access = true
   # END myapp-managed
   ```
   Why no `[section]`: a section header would reparent subsequent user content into that section. And if the managed block is appended after a file that ends inside a user `[table]`, a bare `sandbox_mode = ...` would be parsed as a child of that preceding table and silently ignored.
3. Always place the managed block at the top of the file, above any user content:
   ```go
   func upsertManaged(path string, policy Policy) error {
     content, _ := os.ReadFile(path)
     withoutBlock := stripBetween(content, BeginMarker, EndMarker)
     managed := renderBlock(policy)
     out := managed + "\n" + strings.TrimLeft(string(withoutBlock), "\n")
     return os.WriteFile(path, []byte(out), 0644)
   }
   ```
4. Strip function is a simple state machine: pass through, drop lines from BeginMarker through EndMarker inclusive, pass through.
5. Run this on every task spawn (or on config change). Re-running is idempotent: stripping-then-rewriting yields the same file if nothing changed.

## Example

Decision-matrix-driven rendering for a platform-specific policy:

```go
func renderBlock(policy Policy) string {
  var b strings.Builder
  b.WriteString(BeginMarker + "\n")
  b.WriteString(fmt.Sprintf("sandbox_mode = %q\n", policy.Mode))
  if policy.Mode == "workspace-write" {
    b.WriteString(fmt.Sprintf("sandbox_workspace_write.network_access = %t\n", policy.NetworkAccess))
  }
  b.WriteString(EndMarker + "\n")
  return b.String()
}
```

Users can add their own `[tables]` and keys anywhere outside the markers and the daemon leaves them alone.

## Caveats

- Keep the managed-block keys to a minimum — each added key is something the user might legitimately want to override, creating a "why doesn't my setting apply?" report.
- If a user deletes the markers by hand, the daemon will inject a fresh block on next run; that's OK, the previous block is just gone.
- Document the pattern in a user-facing doc (e.g. "Troubleshooting") so users who see the markers know what they are.
