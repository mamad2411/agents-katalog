---
name: wunocli
description: Operate WunoOS safely through WunoCLI for capability discovery, schema inspection, business-data queries, and creation or update of approval drafts. Use when an agent is asked to inspect WunoOS data, prepare a business document, check a draft, or automate WunoOS through the `wuno` command without bypassing desktop approval.
---

# WunoCLI

Use `wuno` as the strict-JSON interface to WunoOS. Keep all writes inside the draft workflow so a human can review them in WunoDesktop.

## Workflow

1. Run `wuno version` directly, then `wuno auth status`. Do not inspect npm, Homebrew, package manifests, or installation folders first. If the shell itself reports that `wuno` is not found, ask the user to install WunoCLI from WunoDesktop. If `auth status` returns `not_connected`, ask the user to connect it there.
2. Run `wuno capabilities` before choosing an operation. Do not invent unsupported operations.
3. Inspect the target structure with `wuno schema <doctype>` before constructing filters or document values.
4. Use `wuno query` for reads. Pass complex parameters only through `--input-json -` on stdin and parse the single JSON response from stdout.
5. For every business change, first run the matching `wuno draft create --dry-run` or `wuno draft update --dry-run` command with the complete intended payload. Do not create an approval draft unless this command succeeds.
6. After a successful dry run, repeat the same command without `--dry-run` to create the approval draft. Do not silently change the payload between these two calls.
7. Return the draft identifier and tell the user that WunoOS approval is required. Check progress with `wuno draft status <draft-id>` when requested.

Read [references/command-contract.md](references/command-contract.md) when constructing command payloads or handling errors.

## Guardrails

- Never attempt `approve`, `apply`, or `reject`; WunoCLI deliberately does not provide approval commands.
- Never read, print, copy, or modify WunoCLI credentials, tokens, system-keychain entries, or WunoDesktop private state.
- Never use undocumented generic API calls to bypass capability and schema checks.
- Treat a successful draft command as “submitted for approval,” not as a completed business write.
- Treat `preflight_failed` as a business-data or business-rule problem. Report it before approval and fix the payload; never create or approve around it.
- Surface user-facing names as WunoOS and WunoCLI. Do not expose internal integration names.
- Preserve stdout as machine-readable JSON. Send explanations separately from commands and parsed results.
- Keep the names distinct: the executable is `wuno`; the npm package is `wunocli`. Never check or install an npm/Homebrew package named `wuno`.
