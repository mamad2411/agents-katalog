---
name: zephyr-kconfig
description: "Comprehensive Zephyr Kconfig expertise for build-time configuration. Use this skill when you need to: (1) Create or edit Kconfig files to define new configuration symbols, (2) Configure applications via prj.conf, boards/*.conf, or overlay configs, (3) Debug 'unmet dependencies', 'symbol not visible', or 'unknown symbol' errors, (4) Use menuconfig/guiconfig interactively, (5) Integrate Kconfig with external modules or out-of-tree drivers, (6) Use Kconfig functions with devicetree (dt_chosen_enabled, etc.), (7) Understand symbol visibility, hidden configs, or select/imply behavior."
---

# Zephyr Kconfig Skill

Expert guidance on Zephyr's Kconfig system for build-time configuration, symbol definition, and dependency management.

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Common Workflows](#common-workflows)
3. [Configuration Files](#configuration-files)
4. [Advanced Topics](#advanced-topics)
5. [Troubleshooting](#troubleshooting)

---

## Core Concepts

### Define vs. Configure (CRITICAL)

| Action | File | Syntax |
|--------|------|--------|
| **Define** symbol | `Kconfig` | `config MY_FEAT` (NO prefix) |
| **Configure** value | `prj.conf` | `CONFIG_MY_FEAT=y` (WITH prefix) |

### Symbol Types

- **bool**: `y` or `n`
- **int**: Integer value
- **hex**: Hexadecimal value
- **string**: Quoted text

### Key Files After Build
- `build/zephyr/.config` — Final resolved configuration
- `build/zephyr/kconfig/Kconfig.modules` — Auto-generated module Kconfigs

---

## Common Workflows

### 1. Defining Symbols in Kconfig
Create new configuration options for drivers, modules, or apps.

- **Syntax (types, menus, choices, conditionals)**: See [syntax.md](references/syntax.md)
- **Best practices (naming, placement, dependencies)**: See [best_practices.md](references/best_practices.md)

**Quick Example:**
```kconfig
config MY_DRIVER_ENABLE
    bool "Enable My Driver"
    depends on I2C
    help
      Enable support for My Driver over I2C.
```

### 2. Configuring Applications
Set values in `prj.conf` or board-specific overlays.

| Type | Example |
|------|---------|
| Boolean | `CONFIG_LOG=y` |
| Integer | `CONFIG_MAIN_STACK_SIZE=2048` |
| String | `CONFIG_BT_DEVICE_NAME="MyDevice"` |
| Hex | `CONFIG_FLASH_BASE_ADDRESS=0x08000000` |

### 3. Using Menuconfig
Interactive configuration exploration and modification.

- **Launch and navigate menuconfig**: See [menuconfig.md](references/menuconfig.md)

```bash
west build -t menuconfig
```

### 4. Writing Module Kconfig
Integrate external modules with Zephyr's build system.

- **Module integration details**: See [best_practices.md](references/best_practices.md#modules--drivers)

---

## Configuration Files

### Application Level
| File | Purpose |
|------|---------|
| `prj.conf` | Main app configuration |
| `boards/<board>.conf` | Board-specific overrides |
| `app.overlay` | Devicetree + Kconfig overlay |

### Module/Driver Level
| File | Purpose |
|------|---------|
| `Kconfig` | Symbol definitions |
| `zephyr/module.yml` | Module metadata pointing to Kconfig |

---

## Advanced Topics

### Kconfig Functions
Integrate Kconfig with devicetree at build time.

- **Functions reference (dt_chosen_enabled, dt_nodelabel_enabled, etc.)**: See [functions.md](references/functions.md)

### Practical Examples
Complete Kconfig patterns for common scenarios.

- **Driver, subsystem, choice examples**: See [examples.md](references/examples.md)

---

## Troubleshooting

For common errors and debugging techniques:
- See [debugging.md](references/debugging.md)

### Quick Reference

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| "X" has unmet dependencies | Missing `depends on` | Enable required dependency first |
| Symbol not visible | `depends on` condition false | Check what it depends on |
| Unknown symbol "X" | Typo or Kconfig not sourced | Verify spelling, check module.yml |
| warning: Y selected by X but not visible | `select` bypassing `depends on` | Use `imply` or fix dependencies |

---

## References

- [syntax.md](references/syntax.md) — Types, menus, choices, conditionals, sourcing
- [best_practices.md](references/best_practices.md) — Naming, organization, modules, dependency safety
- [menuconfig.md](references/menuconfig.md) — Interactive configuration workflow
- [functions.md](references/functions.md) — Kconfig functions for devicetree integration
- [examples.md](references/examples.md) — Complete Kconfig patterns
- [debugging.md](references/debugging.md) — Error resolution and debugging techniques
