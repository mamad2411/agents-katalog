---
name: chatgpt-browser-oracle
description: Legacy browser-artifact workflow only when the user explicitly names Oracle browser use and the owning policy permits it. Do not use for GitHub repository reviews, Issues/PRs, ChatGPT-Codex collaboration, generic Pro requests, or ordinary artifact generation.
---

# ChatGPT Browser Oracle

## Scope boundary

This is not the transport for GitHub collaboration. Follow the owning
repository's collaboration protocol and connected GitHub interface for reviews,
Issues, PRs and corrections. A request for a model or generated artifact does
not authorize authenticated browser automation.

The existing scripts remain preserved for separately approved legacy use; this
policy change does not start, stop, configure or retire any browser service.
Do not run them until the owner supplies and authorizes the actual project,
profile/service, model selection, input and output locations. Inspect applicable
local instructions and script defaults first; stale hardcoded defaults are not
permission to act. Stop when they conflict with the approved target.

## Authorized artifact workflow

For a separately authorized non-GitHub artifact task:

1. Verify the intended browser/project and allowed data before submission.
   Do not expose credentials, private source or sensitive payloads.
2. Verify the requested mode is actually selected before a costly run; do not
   infer model selection from old documentation or a worker's configuration.
3. Use the existing submission/download helpers only for the approved target.
   Keep the result in the exact approved durable destination.
4. Use `scripts/validate_generated_file.sh` on that final artifact, checking
   the requested type, name and required contents before claiming success.
5. Return the verified artifact reference and blocker, without duplicate report
   copies or an unrequested worker/browser handoff. Retain evidence under the
   owning acceptance/cleanup policy; no broad cleanup is authorized here.

Consult `references/oracle_chatgpt_notes.md` only for targeted legacy diagnosis.
Its historical environment details do not override this scope gate.
