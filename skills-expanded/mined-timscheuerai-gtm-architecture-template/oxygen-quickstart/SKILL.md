---
name: oxygen-quickstart
description: Connect this kit to an OXYGEN workspace, inspect capabilities and complete a small hosted demonstration without paid execution, then hand over to onboarding or the consultant.
---

# Start with OXYGEN

Read [the runtime contract](../../../docs/runtime-contract.md) and [function setup](../../../docs/oxygen-setup.md). Use `oxygen` unless the operator selected another environment, and keep it throughout the session.

For "get me started", use [oxygen-onboarding](../oxygen-onboarding/SKILL.md); for a diagnosis of what already runs, use [oxygen-gtm-consultant](../oxygen-gtm-consultant/SKILL.md). Keep the walkthrough below for an explicit product tour.

For this kit, run `npm run demo` first when the reader needs an example. It requires no account. For a hosted walkthrough:

1. Read `oxygen whoami --json` and resolve the intended workspace.
2. Search `oxygen capabilities search "build a small prospect table" --json`, then hydrate the chosen command with `oxygen commands get "tables create" --json`.
3. Create a small Table and insert only synthetic rows using the returned schema; describe it and return its web_url.
4. `oxygen tools search --for-table <table> --json` answers what you could add and what each row would cost, without spending.
5. Find the next skill with `oxygen skills search "<next goal>" --json`.

For the kit's 13 functions, use `npm run setup` to preview and `npm run setup -- --apply` within the requested scope. Setup is distinct from paid execution. A first walkthrough does not start a provider run, purchase, send or publishing action.
