---
name: set-work-context
description: Read or update Opsphere provider and account context from Antigravity; not workspace selection or credential setup.
---

# Work context

Distinguish provider/account notes from the active Personal or external workspace. Use `ops_my_usage` to check the active workspace and `catalog_config_surface` / `work_context_editable_via_plugin`; read existing notes with `ops_get_work_context` when available.

If editing is allowed through MCP, ask for the user's projects, providers, environments and naming conventions without secrets. Confirm replacements before calling `ops_set_work_context` with the complete revised notes; preserve information the user did not ask to remove.

If the configuration surface is `admin_portal` or editing is not allowed, direct the user to the authorized admin at https://admin.opsphere.io. Do not try the write tool to bypass that restriction. Missing context should not block an unrelated task.

Do not put credentials in these notes or duplicate them into memory. For credentials use the installed `configure-integration` skill. Do not switch workspace to edit these notes without explicit consent.
