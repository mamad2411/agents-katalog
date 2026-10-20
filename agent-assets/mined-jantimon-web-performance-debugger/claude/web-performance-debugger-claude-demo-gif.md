# CLAUDE.md — `examples/demo-gif/`

The README hero GIF. `demo.tape` is the source of truth (a [VHS](https://github.com/charmbracelet/vhs)
script running the `--target node` CPU lane over `examples/ssr-demo`); the rendered `demo.gif` is
git-ignored and hosted via a GitHub user-attachments URL, so it never enters the npm tarball. Render
and publish steps, and what the GIF shows, live in `README.md` here.

Before you touch `demo.tape`, the load-bearing gotchas:

- **Keep it runnable from a clean checkout.** `ssr-demo` is JSX-free (no build step) and `npm install`s
  itself from the tape. A demo that leans on a prebuilt bundle rots unnoticed until the GIF shows a
  flag that no longer exists.
- **`NODE_ENV=production` is load-bearing** (hidden in the tape). Without it React resolves to its dev
  build: `react` outranks `react-dom` and the profile shows a cost nobody ships.
- **`--iterations 250`** buys sampling stability; the top rows only settle at a high count.
- **`Sleep` must outlast the process** — VHS fires the next keystroke after the Sleep, not on exit.
- **Color is automatic** — VHS records in a real PTY, so `--color auto` colorizes with no flag.
