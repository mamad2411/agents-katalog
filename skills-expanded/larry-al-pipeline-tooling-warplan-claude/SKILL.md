# /warplan — warplan a hard project (Claude is the planner)

> **`$SETUP_DIR`** = the larry-setup repo on this machine. Resolve once, first that exists: `$SETUP_DIR` · `~/larry-setup` · `/mnt/rojaws/localDev/setup` (same chain `alw` uses).

Read and follow the canonical warplan instructions at
`$SETUP_DIR/tooling/warplan.md` (ignore its pi-specific `$@` placeholder and its
"run this in Claude" preamble — you ARE the strong model it wants).

The mission is:

$ARGUMENTS

Notes for this entry point:
- If the mission is empty, ask for it (one line) before starting the interview.
- Interactive session → run the recon interview as written. Non-interactive (`claude -p`, e.g.
  delegated from pi) → skip the interview, do the recon you can do yourself (read the repo, dig
  symbols), and put every unresolved question in `ledger.md` as a `(variable: …)` placeholder —
  never guess.
- Deliverables and hand-off are exactly as the canonical file specifies: `war-plans/<name>.md`,
  `success.md`, `ledger.md`, then print the `<tool> build` command and STOP — do not build.
