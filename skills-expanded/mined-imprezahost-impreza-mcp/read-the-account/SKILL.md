---
name: read-the-account
description: Read what an Impreza Host account already has. Use when someone asks which servers, apps or deployments exist. Do not order, pay, register or transfer.
---

# Read the account

This plugin only lists. The tools that spend money are not in `allowed_tools`.

1. `impreza_list_servers` shows the account's machines.
2. `impreza_list_apps` shows the catalog. It does not install.
3. `impreza_list_deployments` shows what was already requested and its state.
4. `impreza_list_invoices` and `impreza_topup_status` only read. They do not pay or charge.

If the person asks to buy, pay or register a domain, say that this plugin does not do that and that the step is the
portal.
