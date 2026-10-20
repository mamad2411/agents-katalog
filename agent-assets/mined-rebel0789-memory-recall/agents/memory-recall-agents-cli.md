# CLI Agent Rules

Commands are local and scriptable, use stable exit codes, write machine output to stdout and diagnostics to stderr, and never silently enable network or writes.

`recall map` is an explicit read-only developer report. It delegates once to
`buildRecallMap`, accepts only bounded local map options, and must keep source
bodies, absolute workspace paths, model/network calls, and workspace mutations
out of every rendering. Return `0` for a safe report and `2` for invalid
arguments; setup may print the map command but must never run it implicitly.
