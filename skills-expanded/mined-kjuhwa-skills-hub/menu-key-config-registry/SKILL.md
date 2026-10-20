---
name: menu-key-config-registry
description: Centralize sidebar/drawer menu keys as a union type + config object per domain, so menu rendering, drawer view switches, and default-expand state all reference the same source of truth. Eliminates string-key drift across the three places a menu key appears.
category: frontend
tags: [react, menu, drawer, registry, typescript, union-type, configuration]
triggers: ["menu key drift", "Drawer case switch", "selectedSubMenu", "DetailMenuList", "sidebar menu config"]
source_project: lucida-ui
version: 0.1.0-draft
---

# Menu Key Config Registry

One union type + one config object per menu domain. Menu items, drawer content switch, and default-expanded state all read from it.

See `content.md`.
