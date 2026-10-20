---
mode: agent
description: Explain how to use the Azure Cleanup Skill safely.
---

# Azure Cleanup Help

Read the full contract at `@.github/skills/azure-cleanup/SKILL.md` before using the skill.

Run the skill with `/azure-cleanup`. It discovers first and is read-only by default.

## Options

- `-All -SiteName "name"` targets the project's `rg-<SiteName>` resource group.
- `-Resource "name" -RG "name"` targets one exact resource.
- `-ResourceGroup "name"` targets a named resource group.
- `-Commercial` selects Azure Commercial.
- `-Gov` selects Azure Government.
- No cloud parameter uses `.azure/environment.json`; when no saved profile exists, Azure Commercial is the default.
- The recorded cloud, subscription, and authentication method are selected automatically. If login is required, the skill starts that flow directly.
- `-WhatIf` lists targets and findings without deleting anything.
- `-Apply` enables deletion only after review and explicit `DELETE` confirmation.

The skill displays subscription, cloud, resource group, exact resources, and findings before any mutation. It reports all errors and post-cleanup results. It never stores credentials or deletes resources based only on a name match.
