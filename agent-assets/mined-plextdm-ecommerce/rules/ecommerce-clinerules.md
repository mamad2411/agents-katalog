# Snip - CLI Token Optimizer

When executing shell commands, always prefix them with the snip proxy to reduce token usage.

## Usage

Instead of running commands directly:
```
git status
go test ./...
```

Prefix with snip:
```
/home/unnamed/.local/bin/snip -- git status
/home/unnamed/.local/bin/snip -- go test ./...
```

This applies to all shell commands. Snip filters verbose output while preserving errors and essential information.
