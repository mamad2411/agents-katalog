---
name: cgagentharness-verify
description: Verify changed Harness CLI, research, browser or desktop behavior with scoped checks and isolated fixtures.
---

# Verify the harness

Read `AGENTS.md`, affected invariants, CI and fixture assertions. Record the
checkout, SHA, dirty state, binary and architecture. Preserve operator homes.

Choose checks by the changed contract:
- Runtime: run the changed command or route; inspect output and side effects.
  Select tests from `cgagentharness-invariant-guard`. Use actual Seatbelt or
  bubblewrap for claims about that backend.
- Research: select the affected PDF input or goal/loop path. Check extracted
  text, source citations and refusals as well as successful completion.
- Browser: `scripts/chat-browser-acceptance.mjs` drives the console;
  `scripts/browser-use-eval.sh` needs a debug `test-support` build, prepared
  Chrome/Playwright and local Ollama for its Qwen fixture. Exercise `/browse`
  itself when its route or UI changes.
- Desktop: use `cgagentharness-release` for packaged identity. Drive fresh
  WKWebView and browser UIs when both ship, following `AGENTS.md`.
- Models: record live tag and allocation. Keep fixtures and live models distinct.
- Prose: run `invariant_guard::markdown_stays_on_the_docs_budget`. Rebuild the
  self-manual when its inputs change; if bytes change, run
  `self_manual::every_chunk_is_clean_under_the_configured_scanner`.

For live checks, use an owned temporary home and unique listener. Verify the
running binary and assets; exercise benign chat and the changed behavior. Stop
only owned processes. Report commands, exits, artifact hashes and gaps;
zero selected tests means NOT RUN. Compare the baseline when attribution is unclear.
