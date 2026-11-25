---
name: oxygen-quickstart
description: Connect this kit to an OXYGEN workspace, inspect capabilities and complete a small hosted demonstration without paid execution.
---

# Start with OXYGEN

Read [the runtime contract](../../../docs/runtime-contract.md) and [function setup](../../../docs/oxygen-setup.md). Use `oxygen` unless the operator selected `oxygen-dev`; keep the selected environment throughout the session.

For this kit, run `npm run demo` first when the reader needs an example. It requires no account. For a hosted walkthrough:

1. Read `oxygen whoami --json` and resolve the intended workspace. If access is not entitled, inspect the returned billing-owner guidance before proposing resources.
2. Search `oxygen capabilities search "build a small prospect table" --json`, then hydrate the chosen command with `oxygen commands get "tables create" --json`.
3. Inspect existing resources before creating a small Table. Insert only the requested manual/synthetic rows using the returned schema.
4. Describe the Table, query the bounded rows and return its actual web_url.
5. Discover a provider operation with `oxygen tools search "company research" --json` and inspect its schema; discovery does not run it.

For the kit's 13 functions, use `npm run setup` to preview and `npm run setup -- --apply` within the requested installation scope. Setup is distinct from paid execution.

For broader onboarding, retrieve the current `oxygen-onboarding` procedure with `oxygen skills get oxygen-onboarding --json`; that optional live skill is not bundled here. Use existing company answers rather than restarting an interview.

Return the selected environment, inspected/created objects, relevant next skill and unconfigured dependencies. A first walkthrough does not start a provider run, purchase, send or publishing action.
