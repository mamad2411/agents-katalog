---
name: turnstile-prov-views
description: Show derived views over the turnstile decision-provenance ledger — origin labels for stated prompts (instruction, pipeline chatter, waiver-carried), the chatter noise rate, and taste-drift aggregates over denials and overrides — via the turnstile CLI. Use when the user asks about decision patterns, taste drift, chatter rate, or the origin of stated prompts. Distinct from turnstile-prov, which reports the raw ledger rows themselves.
---

# Turnstile prov-views

Show what the decision record reveals about how decisions were made.
Read-only — never modify config or journals from this skill.

## Steps

1. Detect context: inside the turnstile repo use
   `node bin/cli.mjs prov-views`; elsewhere
   `npx opencode-turnstile prov-views`. Views are derived at read time
   from the same `prov:*` rows `prov` reports; nothing is written and
   no derived value feeds gates or capture.
2. Scope: with no sessionID the views cover every session. When the
   user asks about a specific session, pass the sessionID as the first
   argument. If the user names options (`--json`, `--tail <n>`),
   forward them verbatim to the invocation; if the CLI rejects one,
   surface the usage error verbatim — never retry blind, never drop
   the flag. Use `--json` when the user wants machine-readable output.
3. Report the three views in plain terms:
   - Origin labels — how many stated prompts were instruction, pipeline
     chatter ("continue", bare acknowledgements), or waiver-carried.
   - Chatter noise rate — the share of stated prompts that are pure
     pipeline chatter.
   - Taste-drift aggregates — patterns across denials and overrides
     (what kinds the human refuses or waves through).
4. Summarize what the aggregate view shows about judgment in the loop,
   but do not editorialize beyond what the views report. The rows are
   already secret-redacted at capture; never attempt to un-redact or
   infer redacted content.
