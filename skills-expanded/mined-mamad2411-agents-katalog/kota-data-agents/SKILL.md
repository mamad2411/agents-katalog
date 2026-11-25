# Data

This directory holds mutable project data that is not source code.

- Keep rough captures, normalized work, and external-resource monitoring as
  separate concerns. Their local files own the exact storage shape.
- Keep quick captures lightweight.
- Keep normalized work specs in the task queue.
- Keep watchlist entries minimal.
- Watchlist coverage should span evolving peer runtimes, vendor research,
  and research series relevant to autonomy, memory, orchestration, and evaluation.
  Each entry's notes explain what development merits revisiting. Prefer release
  surfaces, engineering blogs, and maintained research projects over overlapping
  documentation pages. Settled papers and one-off articles remain citations in
  their existing task or decision records, not recurring monitors.
- Do not add aggregator indexes, "awesome-*" lists, or arXiv category pages as
  watchlist entries — they inflate coverage without adding durable signal.
- Record unreachable entries honestly with `status: inaccessible` rather than
  silently dropping them.
