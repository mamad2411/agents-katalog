---
name: hermes-profile-evolution
description: Route proposed Team Mimir profile behavior changes into target-owned Hermes dialogue after producer-owned custody classification.
---

# Hermes Profile Evolution

Use this skill when a requested Team Mimir edit may change a profile's repo-safe behavior. The
named profile retains autonomy: this path sends a proposal for dialogue and does not authorize or
perform a profile mutation.

## Workflow

1. Put the intended repository-relative paths, plain-language intent, and sanitized evidence
   references in one bounded JSON object. Do not include credentials, secrets, transcripts, logs,
   databases, host addresses, provider/model overrides, system prompts, or tool definitions.
2. Pipe that object to the bundled adapter. Run the command from this skill directory so the
   repository's proven skill-relative install layout resolves the bundled script:

   ```bash
   printf '%s' '{"schema_version":1,"intent":"Consider clarifying your review preference.","paths":["profiles/brokkr/SOUL.md"],"evidence_references":["docs/team/README.md"]}' \
     | python3 ../../scripts/profile_request.py suggest brokkr
   ```

3. If Team Mimir classifies every path as ordinary repository work, continue through normal review;
   Hermes is not contacted.
4. If the result starts Hermes dialogue, retain the returned proposal and continuity data in the
   chat. Continue interactively with `reply` or `resume`; do not turn the exchange into an offline
   queue.
5. Treat an adapter error as a stop. Fix only the request shape or unavailable producer/service
   boundary named by the error. Never bypass classification by recreating its policy locally.

## Continuation

`reply` and `resume` accept bounded JSON on standard input. A reply object has exactly
`schema_version`, `proposal`, and `message`; a resume object has exactly `schema_version` and
`proposal`. The proposal is the canonical envelope previously sent to Hermes.

## Supported boundary

The Codex hook covers recognized edits through `apply_patch`, `Edit`, and `Write`. It is advisory
beyond those supported tool calls and does not claim to prevent shell commands, external editors,
disabled hooks, untrusted hooks, or same-user/root activity. Hook trust is an operator decision.
