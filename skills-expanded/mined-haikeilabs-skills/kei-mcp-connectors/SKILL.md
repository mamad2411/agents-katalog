---
name: kei-mcp-connectors
description: "Use when an organization admin or an agent helping one needs to set up a remote MCP connector in Kei end to end: prepare the CLI, create and activate the connector, connect an account, create and approve its tool manifest, sync a harness, or troubleshoot setup errors."
---

# Set up a remote MCP connector in Kei

This skill covers the ordered setup path for a **remote MCP server** using
per-user OAuth, then the errors that can block that path. It is written for an
organization admin or an agent working with one. Keep the admin in control of
production changes.

## Follow this order

1. Upgrade to `kei` 0.2.3 or later and run `kei login` as a workspace admin.
2. Create the MCP connector and activate it in the console.
3. Use the workspace **NAME** with `--workspace <name>`; workspace UUIDs
   are not accepted.
4. Connect as a workspace admin with
   `kei connectors connect <connector-id> --workspace <workspace-name>`.
5. From the connected account, make the first tool-list call from a harness
   (`tools/list` or list tools); that call creates the candidate manifest.
   Review it, then approve it with `kei connectors manifests approve`.
6. Run `kei harness sync`; follow its notes, including Codex `/hooks` trust.

Older connectors may need an `admins` group permit added by an admin. For
`no_matching_policy`, state explicitly: production policy changes are the
admin's decision, and an older connector may need the `admins` group permit
added by an admin. Say plainly: "Production policy changes are the admin's
decision. An older connector may need an `admins` group permit added by an
admin." The admin decides whether to add it. Never create or widen a policy
yourself. Use the
workspace name, not its UUID, for `--workspace`. For
`connector_has_no_tools`, connect first as a workspace admin, then make the
first harness tool-list call to create the manifest. This reason means the
connector has no available tools; a policy change is not its remedy.
Have the user complete per-user OAuth in the browser. For organization OAuth
registration errors, ask the platform owner to arrange registration. Never ask
for, accept, print, or store OAuth tokens, client secrets, or other credentials.

Use the [kei-cli skill](../kei-cli/SKILL.md) for exact CLI syntax beyond the
commands shown here, including connector creation options and policy commands.
Use [kei-harness-setup](../kei-harness-setup/SKILL.md) for harness installation
and configuration, [kei-harness-policy](../kei-harness-policy/SKILL.md) for
policy behavior, [kei-proxy](../kei-proxy/SKILL.md) for connector invocation,
and the matching provider connector skill (for example,
[linear-connector](../linear-connector/SKILL.md)) for provider-specific API
behavior. Do not restate those references here.

## Ordered setup

Complete these steps in order. A connector becomes callable only after the
user connection, tool manifest review, and harness setup are complete.

1. **Check the CLI and sign in.** Use `kei` version 0.2.3 or later. Upgrade
   with `kei upgrade`, then authenticate the admin with `kei login`. If the
   CLI reports `not logged in` or an HTTP 401, repeat `kei login` and retry;
   login tokens expire. Never ask the user to reveal a token.
2. **Choose the workspace by name.** `--workspace` takes the workspace name,
   not its UUID. Use `kei workspaces list` to find the name. A UUID returns a
   workspace-not-found error. Connector slugs must match
   `^[a-z][a-z0-9_]{1,47}$`; choose one at creation because it cannot be
   changed later.
3. **Create the MCP connector.** Use an MCP template from the catalog and
   provide its server URL if the template has no URL of its own. For example:

   ```sh
   kei connectors create --workspace Main --template <mcp-template-id> \
     --kind mcp --label "Linear" --slug linear_mcp \
     --mcp-url https://mcp.example.com/mcp
   ```

   The exact template ID and whether `--mcp-url` is needed depend on the
   catalog entry. Do not assume a local template-list command exists. The
   creator receives the `admins` group permit by default for newly created
   connectors. Older connectors may not have that permit; an admin must add
   the appropriate group permit. Review the scope before allowing a group.
4. **Activate the connector.** In the Kei console, open Connections, select
   the connector, and activate it. The console's ordered checklist is:
   **Connect your account**, **Make the first tools/list call to create the
   manifest**, then **Approve tools**. The CLI create operation and activation
   are separate steps; the next three steps explain the checklist actions.
5. **Connect the admin's account.** From the CLI, run:

   ```sh
   kei connectors connect <connector-id> --workspace Main
   ```

   This opens the per-user OAuth flow for the admin running the command. An
   admin can connect even before the MCP server has tools listed. State that
   OAuth auto-registration is version-dependent and depends on the deployed
   bridge. Before the bridge auto-registration change (HAI-804) is deployed,
   the platform owner must arrange the organization OAuth registration
   required by the older deployment. If the CLI says `no OAuth registration
   in this organization is for the resource's authorization server`, use
   that same owner path. Never request or accept an OAuth client secret.
6. **Make the first tool-list call from a harness.** Ask the connected harness
   to list the server's tools. That first tool-list call causes the runtime to
   submit a candidate tool manifest. Running `kei connectors connect` alone
   does not create the manifest.
7. **Review and approve the manifest.** List candidates, inspect the newest
   one, and approve its ID:

   ```sh
   kei connectors manifests list <connector-id> --workspace Main
   kei connectors manifests show <connector-id> --workspace Main
   kei connectors manifests approve <connector-id> <manifest-id> --workspace Main
   ```

   Review names, descriptions, schemas, and changes before approval. Treat
   tools that write, delete, or change state with particular care. Approval
   replaces the current approved manifest; do not approve a candidate you have
   not reviewed.
8. **Sync the harness.** Run `kei harness sync` in the environment where the
   target harness is configured. Read its notes and warnings: a successful
   sync installs the relevant harness configuration, but it does not widen
   policies scoped to a different harness. Ask the admin before changing
   policy scope. If sync suggests sharing a policy with this harness, its
   suggested command may show a workspace UUID; replace that value with the
   workspace name before running it. For Codex, open Codex and run `/hooks` to
   trust the Kei hooks.

## Troubleshoot setup

Use the message or reason code to find the next step in the
[troubleshooting reference](references/troubleshooting.md). In particular,
distinguish a missing tool manifest from an access-policy denial: those have
different fixes.

## Safety and ownership

- Never print, request, accept, or store OAuth tokens, client secrets, or
  other credentials in chat. The user completes OAuth in the browser.
- Never create or widen a policy without explicit approval from the admin.
  Older-connector access repair and harness-scope changes affect production
  permissions and belong to the admin.
- Review tool manifests before approval. An approved MCP manifest defines the
  tools exposed to harness users.

## Validation commands

The admin can verify the setup using the documented CLI commands:

```sh
kei --version
kei connectors get <connector-id> --workspace <workspace-name>
kei connectors manifests list <connector-id> --workspace <workspace-name>
kei harness sync
```

Confirm that the connector is active, the expected manifest is approved, and
the harness sync output has no unresolved setup warnings. See the [kei-cli
skill](../kei-cli/SKILL.md) for command options and status output.

## Realistic usage boundaries

This skill covers remote MCP setup and its setup errors. It does not document
provider API behavior, arbitrary connector invocation, tool-adapter design,
or general harness installation; follow the linked skills for those tasks.
The bridge's OAuth auto-registration depends on the deployed version. If the
registration error appears, the platform owner must confirm which deployment
path is available. Connector and policy changes in production remain the
admin's responsibility.
