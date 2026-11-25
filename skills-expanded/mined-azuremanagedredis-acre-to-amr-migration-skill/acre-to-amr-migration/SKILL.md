---
name: acre-to-amr-migration-skill
description: >
  ACRE (Azure Cache for Redis Enterprise) to AMR (Azure Managed Redis) migration expert.
  Get a tailored checklist of changes for your ARM templates, Bicep, Azure CLI, PowerShell, or Terraform
  scripts. Discover your ACRE caches and migrate them step-by-step with confirmation gates. Understand
  breaking changes, SKU mappings, Private Endpoint / Private Link migration, and DNS zone updates.
  Use for: ACRE to AMR migration, Azure Managed Redis migration, convert ACRE script, review deployment
  script, migration checklist, Enterprise_E10, Enterprise_E20, EnterpriseFlash, geo-replicated caches,
  Private Endpoints, Private Link, SKU mapping, breaking changes, check my ARM template, update my Bicep
  template, Terraform, azurerm_redis_enterprise_cluster, azurerm_managed_redis, geo-replication database
  config parity, eviction policy matching, ACRE resource cleanup, post-migration cleanup script,
  delete old ACRE caches, or what changes do I need for AMR.
license: MIT
metadata:
  author: azure-redis-team
  version: "1.0"
---

# ACRE to AMR Migration & Automation Script Update Guide

This skill provides **three modes** of assistance for ACRE → AMR migration:

1. **Automation Script Update** — Analyzes existing ACRE automation scripts (ARM, Bicep, CLI, PowerShell) and produces a tailored checklist of required changes with before/after examples. Does NOT modify files directly.
2. **Interactive Cache Migration** — Discovers ACRE caches in the user's subscription, determines the migration path for each (in-place for standalone caches, create-new-and-swap for geo-replicated caches), and walks the user through each step interactively with confirmation gates.
3. **Generic Migration Guide** — Presents a recommended step-by-step migration process (for both standalone and geo-replicated caches) without executing any commands or accessing the user's Azure subscription. Use this mode when the user asks for general guidance, a flowchart, or a process overview rather than requesting hands-on migration of specific caches.

---

## Quick Reference Index

Navigate to the relevant reference document based on your task:

| Reference | Description | When to Use |
|-----------|-------------|-------------|
| [Breaking Changes](references/breaking-changes.md) | Property changes, DNS updates, API versions, PE migration strategies | Understanding what changes between ACRE and AMR |
| [Script Analysis](references/script-analysis.md) | Detection patterns, companion parameter files, ACRE indicators, validation checklist | Detecting script type, reading params, validating before checklist |
| [SKU Resolution](references/sku-resolution.md) | `listSkusForScaling` procedure + fallback mapping table + AMR SKU families | Determining the target AMR SKU |
| [Per-Script Checklists](references/checklists.md) | Numbered checklists for ARM, Bicep, Azure CLI, Azure PowerShell | Producing the tailored migration checklist for a script |
| [Before/After Examples](references/examples/README.md) | [Routing index](references/examples/README.md) linking to per-type example files | Showing the user exact code transformations. Load **only** the file matching the detected script type: [ARM](references/examples/arm.md), [Bicep](references/examples/bicep.md), [CLI](references/examples/cli.md), [PowerShell](references/examples/powershell.md), [Connection Strings](references/examples/connection-strings.md) |
| [Generic Migration Guide](references/migration-guide.md) | Step-by-step process overview, flowchart, Path A and Path B summaries | Presenting the recommended migration process without executing commands |
| [Interactive Migration](references/interactive-migration.md) | Discovery, in-place migration steps, geo-replicated migration steps, DB config parity, post-migration ACRE cleanup | Hands-on migration with cache discovery and confirmation gates. Includes geo-replication config matching (Step 3) and cleanup commands/scripts (Step 8) |
| [Terraform Checklist & Examples](references/terraform.md) | Terraform checklist, `azurerm` resource examples (before/after) | Producing the tailored migration checklist for Terraform configs |
| [Troubleshooting & FAQ](references/troubleshooting.md) | Common pitfalls, error messages, interactive Q&A patterns | Answering follow-up questions and debugging deployment failures |
| [Poll-MigrationStatus.ps1](scripts/Poll-MigrationStatus.ps1) | Reusable PowerShell polling script for migration/creation status | Use instead of inline polling loops in interactive migration (PowerShell / pwsh) |
| [poll-migration-status.sh](scripts/poll-migration-status.sh) | Reusable Bash polling script for migration/creation status | Use instead of inline polling loops in interactive migration (Bash on Linux/macOS) |
---

## Scope Boundary — READ FIRST

> **This skill applies ONLY to ACRE → AMR migration.**
>
> - **ACRE** = Azure Cache for Redis Enterprise: SKUs starting with `Enterprise_` or `EnterpriseFlash_`
> - **AMR** = Azure Managed Redis: SKUs starting with `Balanced_`, `MemoryOptimized_`, `ComputeOptimized_`, or `FlashOptimized_`
>
> Both ACRE and AMR use the **same ARM resource type**: `Microsoft.Cache/redisEnterprise`

### Out of Scope — ACR Resources

This skill does **NOT** cover migration from **Azure Cache for Redis (ACR)** Basic/Standard/Premium SKUs to AMR. That is a fundamentally different migration path.

**ACR indicators** (any of these signals an ACR resource):
- Resource type `Microsoft.Cache/redis` (note: no "Enterprise" suffix)
- SKU names: `Basic`, `Standard`, `Premium`, `C0`–`C6`, `P1`–`P5`
- CLI commands: `az redis` (not `az redisenterprise`)
- PowerShell cmdlets: `New-AzRedisCache`, `Get-AzRedisCache` (not `*-AzRedisEnterprise*`)

**If the script contains ONLY ACR resources (no ACRE resources)**, respond:
> "Your script targets Azure Cache for Redis (ACR) with resource type `Microsoft.Cache/redis`, not Azure Cache for Redis Enterprise (ACRE) with resource type `Microsoft.Cache/redisEnterprise`. This skill covers ACRE-to-AMR migration only. ACR-to-AMR is a different migration path — please use the appropriate ACR migration skill or consult the Azure Cache for Redis migration documentation."

**If the script contains BOTH ACR and ACRE resources**, inform the user that the ACR resources are out of scope and proceed with analyzing only the ACRE resources:
> "Your script contains both ACR resources (`Microsoft.Cache/redis`) and ACRE resources (`Microsoft.Cache/redisEnterprise`). This skill only covers ACRE → AMR migration. I will analyze the ACRE resources and produce a migration checklist for those. For the ACR resources, please use the appropriate ACR migration skill or consult the Azure Cache for Redis migration documentation."

---

## Mode Detection — How to Choose the Right Mode

Before proceeding, determine which mode to use based on the user's request:

| User Intent | Mode | What the Agent Does |
|-------------|------|---------------------|
| User shares a script/template (ARM, Bicep, CLI, PowerShell, **Terraform**) and asks what needs to change for AMR | **Automation Script Update** | Analyze the script, produce a tailored checklist with before/after examples |
| User asks to migrate their caches, discover caches, or execute migration steps | **Interactive Cache Migration** | Log in, discover caches, walk through migration step-by-step |
| User asks for a step-by-step guide, recommended process, flowchart, or general migration overview — **without** referencing specific caches or asking to execute migration | **Generic Migration Guide** | Present the recommended migration process as documentation — no commands executed, no subscription access required |

**Detection signals for Generic Migration Guide mode** (use this mode if ANY of these match):
- User says "step by step process", "step-by-step guide", "migration steps", "how to migrate", "what is the process", "recommended process", "migration flowchart", "walkthrough", or "overview"
- User does NOT mention specific cache names, resource groups, or subscription IDs
- User does NOT say "migrate my caches", "migrate our caches", or "help me migrate" (these imply hands-on interactive migration)
- User asks a general knowledge question about the migration process rather than requesting execution

**Tie-breaker for ambiguous prompts**: If the user mentions *their* caches or subscription but asks a process question (e.g., "How do I migrate my ACRE cache?"), **default to Generic Migration Guide mode** and offer to switch to Interactive mode. The key signal for Interactive mode is an explicit request to *execute* steps (e.g., "migrate my caches", "discover my caches", "run the migration"). For example: *"Here is the recommended step-by-step migration process. If you'd like me to discover your actual ACRE caches and walk you through the migration interactively, just let me know."*
---

## Agent Behavior Rules

When this skill is invoked, you MUST follow these rules:

### MUST — General

1. **Default: DO NOT directly edit, create, or modify any user files.** You are advisory only for automation script changes. However, if the user explicitly asks you to apply the changes to their files, you may do so — but you **MUST** inform the user afterwards: *"These changes were generated by AI. Please review all modifications thoroughly before committing or deploying them to ensure correctness and completeness."*
2. **Verify scope** before proceeding — if the script is for ACR (not ACRE), stop immediately and explain (see Scope Boundary above).
3. **Warn about access keys authentication** — the default for `accessKeysAuthentication` is `Disabled` in API version `2025-07-01`+. If the application uses access keys, it must be explicitly set to `Enabled`. See [breaking-changes.md](references/breaking-changes.md#properties-that-change) for details.
4. **Resolve the AMR SKU** by following the [SKU Resolution Procedure](references/sku-resolution.md). In **Automation Script Update** and **Interactive Cache Migration** modes, the agent MUST execute the `listSkusForScaling` API call itself (never just suggest it), MUST stop and ask the user for any missing parameters (subscription ID, resource group, cluster name) and WAIT before proceeding, and must only fall back to the [default mapping table](references/sku-resolution.md#default-migration-mapping-fallback) when the API call itself fails after execution. In **Generic Migration Guide** mode (where no commands are executed), present the SKU resolution procedure and mapping table as reference information only.

### MUST — Automation Script Update Mode

5. **Analyze** the user's script/template to detect the automation type (ARM JSON, Bicep, Azure CLI, Azure PowerShell, Terraform). See [Script Analysis](references/script-analysis.md). For Terraform configs, use the [Terraform Checklist & Examples](references/terraform.md) instead of the per-script checklists.
6. **Read companion parameter files** — For ARM templates, search the same directory (and the workspace) for associated `*.parameters.json` files. For Bicep templates, search for associated `.bicepparam` files. See [Script Analysis — Companion Parameter Files](references/script-analysis.md#companion-parameter-files).
7. **Validate the script** before producing the checklist. Follow the [Script Analysis — Validation Guardrails](references/script-analysis.md#step-4--validate-before-checklist).
8. **Produce a tailored, numbered checklist** of required changes specific to what you found in the user's script **and its parameter files**. Use the [Per-Script Checklists](references/checklists.md) as the template.
9. **Show before/after examples** inline for each checklist item so the user understands the exact transformation needed. See [Before/After Examples](references/examples/) — load only the file matching the detected script type (e.g., [arm.md](references/examples/arm.md) for ARM).
10. **DO NOT apply changes** to the user's files unless they explicitly ask (see Rule 1). If the user requests you to apply changes, do so, then remind them: *"These changes were generated by AI. Please review all modifications thoroughly before committing or deploying them to ensure correctness and completeness."*

### MUST — Interactive Cache Migration Mode

11. **Safe agent principles** — Interactive migration touches **production infrastructure**. The agent MUST:
    - **Get explicit user confirmation before every step** that modifies resources (create, update, delete, unlink).
    - **NEVER delete any resource directly.** For deletion steps (old ACRE cache, old Private Endpoint, old DNS zone), provide the exact command or portal guidance and instruct the user to execute it themselves.
    - **Present each step one at a time.** After presenting a step, **WAIT for the user to confirm** before proceeding. Do NOT batch multiple steps or skip ahead.
    - **Use the temp-file pattern for ALL `az rest --body` calls.** NEVER pass inline JSON with escaped quotes to `--body` — PowerShell mangles it. See [interactive-migration.md — Cross-Platform Command Reference](references/interactive-migration.md#cross-platform-command-reference) for the mandatory pattern and both PowerShell and Bash examples.
12. **Follow the Interactive Migration Procedure** in [references/interactive-migration.md](references/interactive-migration.md), which covers:
    - **Phase 1 — Discovery**: List caches, classify ACRE vs AMR, check geo-replication, detect Private Link, call `listSkusForScaling`, present migration plan, wait for user confirmation.
    - **Phase 2A — In-Place Migration**: For standalone (non-geo-replicated) caches.
    - **Phase 2B — Geo-Replicated Migration**: For geo-replicated caches (create new AMR cache, swap traffic, remove old ACRE — one member at a time).

### MUST — Geo-Replication Database Config Parity (Interactive Cache Migration — Phase 2B)

12a. **Match source database configuration exactly AND include geo-replication in one shot** when creating a new AMR database for geo-replicated migration (Phase 2B, Step 3). The agent MUST:
    - **Collect ALL required data BEFORE the PUT call**: (1) full source ACRE database properties (eviction policy, clustering policy, modules, TLS/clientProtocol, persistence), AND (2) the geo-replication group info (group nickname, all existing linked database IDs).
    - **Create the database with a single PUT request** that includes BOTH the database configuration AND the `geoReplication` block. Geo-replication **cannot** be added to an existing database — if you create the DB without it, you must delete and recreate.
    - **Always use PUT (`--method put`), NEVER PATCH for database resources.** The PATCH API on `databases/default` does not work reliably. PATCH works on the cluster resource for in-place migration, but all database operations must use PUT.
    - **Present the retrieved config to the user** (eviction policy, clustering policy, client protocol, modules, persistence, geo-replication group) and get confirmation.
    - **Copy every config property** from the source to the new database — do NOT use defaults or hardcoded values.
    - **Verify the new database config matches** after creation by running a side-by-side comparison.
    - **Warn about RediSearch + eviction policy**: If the source uses RediSearch, the eviction policy MUST be `NoEviction`.
    - See [Microsoft docs: Active geo-replication prerequisites](https://learn.microsoft.com/en-us/azure/redis/how-to-active-geo-replication#active-geo-replication-prerequisites) for the full list of properties that must match.

### MUST — Post-Migration ACRE Cleanup (Interactive Cache Migration — Phase 2B)

12b. **Generate cleanup scripts as FILES — NEVER execute deletions.** When it's time to clean up old ACRE resources (delete cache, delete PE, clean up DNS), the agent MUST:
    - **Generate a single cleanup script file** (`.sh` for Bash, `.ps1` for PowerShell) with all cleanup steps combined — cache deletion, PE deletion, DNS cleanup — using `az redisenterprise` CLI commands directly (NOT `az rest`). Force-unlinking is NOT required — you can directly delete old ACRE caches and Azure handles the geo-replication group update automatically.
    - **Write the script to disk** in the user's working directory (e.g., `cleanup-{cacheName}.sh` or `cleanup-{cacheName}.ps1`).
    - **Tell the user** where the script is and ask them to review every line before running it.
    - **NEVER execute any deletion command directly** — the user must run the script themselves.
    - **Warn about shared DNS zones** — do not suggest deleting `privatelink.redisenterprise.cache.azure.net` if other caches still depend on it.
    - See [interactive-migration.md — Step 6](references/interactive-migration.md#step-6--delete-old-acre-cache-and-clean-up-resources) and [Post-Migration ACRE Cleanup Script](references/interactive-migration.md#post-migration-acre-cleanup-script-geo-replication) for the detailed procedure and script templates.

### MUST — Cross-Platform Support (Interactive Migration)

12c. **Detect the user's shell environment** before generating any commands in Interactive Cache Migration mode. The skill's scripts and command patterns have both PowerShell and Bash variants — use the right one for the user's environment. Detection approach:
    - Check if the current session is PowerShell (e.g., `$PSVersionTable` exists, or the agent is running in a PowerShell terminal) → use **PowerShell** syntax: backtick line continuation, `$env:TEMP`, `ConvertTo-Json`, `Out-File`, and [Poll-MigrationStatus.ps1](scripts/Poll-MigrationStatus.ps1).
    - Otherwise (bash, zsh, or other POSIX shell on Linux/macOS) → use **Bash** syntax: backslash line continuation, `mktemp` / `$TMPDIR` / `/tmp`, `cat` heredocs or `echo` for JSON body files, and [poll-migration-status.sh](scripts/poll-migration-status.sh).
    - Plain `az` CLI commands (e.g., `az redisenterprise list`, `az rest --method get`) work identically on both platforms — only adapt line continuation characters and variable/temp-file syntax.
    - See [interactive-migration.md — Cross-Platform Command Reference](references/interactive-migration.md#cross-platform-command-reference) for side-by-side syntax patterns.

### MUST — Generic Migration Guide Mode

13. **Do NOT execute any commands or access the user's Azure subscription.** This mode is purely informational.
14. **Present the recommended migration process** from [references/migration-guide.md](references/migration-guide.md), covering both standalone and geo-replicated cache scenarios.
15. **Include key decision points** — help the user understand when to use in-place migration vs. create-new-and-swap, and what factors affect the choice.
16. **Reference the Breaking Changes table** — summarize the critical property changes from [references/breaking-changes.md](references/breaking-changes.md) so the user knows what to expect.
17. **Offer to switch modes** — At the end of the guide, offer to switch to Interactive Cache Migration mode if the user wants hands-on execution, or to Automation Script Update mode if they have scripts to update.

### SHOULD

18. **Answer follow-up questions** interactively about specific properties, SKU choices, DNS changes, or API version selection. See [Troubleshooting & FAQ](references/troubleshooting.md) for common Q&A patterns.
19. **Ask clarifying questions** if the target AMR SKU is unclear or if the script has ambiguous patterns (e.g., SKU name in a parameter/variable that you can't resolve).