---
name: terminal-explainer
description: Use when asked for an illustrated terminal walkthrough, a visual review of a change or PR in tmux, or a terminal explainer that gathers feedback.
license: MIT
---

# Terminal Explainer

Build a walkthrough around something the reader needs to understand or decide. For a review, inspect the actual change and its tests. Pick the behavior with the biggest consequence for the reader. Trace one concrete example through it. Show where the evidence runs out.

Use a picture to answer a question: what moved, which actor owns the write, where a retry branches, or what the user sees before and after a change. Screenshots, generated illustrations and annotated diagrams all work. Figures get about 15 terminal rows, and terminals without an image protocol show them as coarse colored half-blocks, so generated diagrams need wide compositions, bold silhouettes on a flat dark background, and no embedded text. Place exact identifiers and numbers in the terminal caption so they stay readable. Open and inspect each image before using it. Treat a diagram as an explanation and the captured source or diff as evidence. A request for an illustrated review warrants a real visual.

## Author and present

Requires macOS or Linux and `uv`. Let `EXPLAIN` be the absolute path to `scripts/explain.py` beside this skill. Use `uv run --script "$EXPLAIN"` for commands. The first run installs its declared Python dependencies.

1. Read `config` for the user's renderer, image style and generator. See [configuration and illustration jobs](references/configuration.md) and [the example brief](examples/brief.txt) when generating images or changing settings. Start slow illustration jobs first so they render while you verify line numbers and write the spec. Use available generation tools when the command is empty. Reuse an accurate existing picture when it already answers the question.
2. Write a JSON spec and keep its image assets beside it in a temporary or scratch folder outside the repository so the checkout stays clean. See [the walkthrough format](references/authoring.md) and [the runnable example](examples/walkthrough.json). For code reviews attach exact line ranges or a file diff (or a list of them when comparing implementation and tests) to each claim.
3. Run `uv run --script "$EXPLAIN" open walkthrough.json --root "$PROJECT"`. This snapshots the evidence into a private run. Inside tmux it splits a new pane from yours, zooms it to fill the window, focuses it and returns the run and pane. The reader works entirely from the keyboard and shows its keys at the bottom. Outside tmux, a human can run `open` directly in a terminal. If the agent shell has neither tmux nor a human-visible TTY, use `prepare` with the same spec and root, then give the reader the exact `view "<run>"` command for their terminal.
4. When collecting feedback, run `uv run --script "$EXPLAIN" wait "<run>" --timeout 60` and keep polling that same command with a timeout shorter than your shell tool limit. Exit 0 returns the submitted answers, 2 means the reader closed the tour, and 3 means the wait timed out. A later wait reads the saved response. For a preview-only request, hand over the open tour without waiting. Treat the response as feedback on this walkthrough.
5. The reader's pane closes when they submit or close, and tmux returns to your pane. If `wait` reports that the reader stopped, read its error with `tmux capture-pane -p -t <pane>`, then close it with `tmux kill-pane -t <pane>`. The snapshot and response stay in the run directory.

To try the included walkthrough, run `uv run --script "$EXPLAIN" demo`.
