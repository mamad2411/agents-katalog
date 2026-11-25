---
name: gjensidige-azure-login
description: Sign in to the Gjensidige Azure tenant through Microsoft Edge so Intune device claims satisfy Conditional Access. Use when Azure CLI authentication is missing, expired, or fails with AADSTS530003 outside the office.
disable-model-invocation: true
---

# Gjensidige Azure Login

Use normal browser authentication in Microsoft Edge. Brave and device-code login can omit the managed-device claim required by Gjensidige Conditional Access.

## Login

1. If the user only needs a valid session, check it first:

   ```bash
   az account get-access-token --resource https://management.azure.com/ --query expires_on -o tsv
   ```

   Stop when this succeeds. If the user explicitly asks to log in again, continue regardless.

2. Run the bundled script in a TTY and wait for the user to finish authentication in Edge:

   ```bash
   bash ~/.agents/skills/gjensidige-azure-login/scripts/login.sh
   ```

   Pass a subscription name or ID as the first argument when the user names one. Otherwise, accept the starred default by pressing Enter at the subscription prompt.

3. Verify both account selection and token issuance:

   ```bash
   az account show --query '{subscription:name, tenantId:tenantId, user:user.name, state:state}' -o table
   az account get-access-token --resource https://management.azure.com/ --query expires_on -o tsv
   ```

Completion requires an enabled account and a successful access-token command.

## AADSTS530003

If Edge still reports that Gjensidige must manage the device:

1. Check enrollment with `profiles status -type enrollment`.
2. Ask the user to open Company Portal and refresh the device status.
3. Retry the normal Edge browser flow. Do not switch to `--use-device-code`.
4. Read the newest `~/.azure/commands/*.login.*.log` and report its timestamp, trace ID, and correlation ID for the Gjensidige Identity team.

When Cisco VPN is connected outside the office, Azure traffic may still leave through the local network because the VPN uses split tunneling. Office success can therefore come from a trusted network location while home login still requires a valid Intune device claim.
