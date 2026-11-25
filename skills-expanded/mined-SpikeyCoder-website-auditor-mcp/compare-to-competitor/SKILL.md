---
name: compare-to-competitor
description: Compare the user's website against a named competitor in AI assistant answers — where the rival gets named and they don't. Use when the user asks how they stack up against a competitor or why AI assistants recommend a rival instead of them.
---

1. Make sure you have both domains — the user's own website and the
   competitor's. Ask for whichever is missing.
2. Call `compare_competitors` with the user's site as the domain and the rival
   as the competitor.
3. Report where the competitor gets named and the user's site does not, and
   what is different about how each one is described.

If no API key is configured, call `get_sample_audit` instead so the user sees
exactly what the real check returns, and tell them what it would take to run it
for real.
