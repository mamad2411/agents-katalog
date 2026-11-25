---
name: astrale-services
description: Use the Services domain to turn existing code or requirements into a deployed Cloudflare-backed Service with SDK-declared Functions, verify calls end to end, inspect it, manage write-only secrets, configure schedules, tail logs, delete it, or open its view.
---

# Astrale Services

Use `services.astrale.ai` as the provider control plane for deployed Services. `CloudflareWorker` is
the current concrete backend. A Service may publish an Astrale Application, but Services never
installs or uninstalls that Application on a consumer Kernel.

## Intent router

- Deploy a plain background Service or cron that calls an installed Domain under its own registered
  account: read [references/service-account-cron.md](references/service-account-cron.md). Do not
  scaffold an Application or install a Domain merely to deploy this caller.
- Build or adopt code, deploy it as a Service with published Functions, deliberately install it on
  the selected consumer Kernel, verify it end to end, and hand back exact calls: read
  [references/deployer-agent.md](references/deployer-agent.md).
- Deploy artifacts, operate a service, manage secrets/schedules/logs, delete, or open the GUI: read [references/workflows.md](references/workflows.md).
- Understand the Service class, deploy payload, and result shape: read
  [references/schema.md](references/schema.md).
