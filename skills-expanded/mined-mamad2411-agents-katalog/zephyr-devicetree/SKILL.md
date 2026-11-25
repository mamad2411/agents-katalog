---
name: zephyr-devicetree
description: "Comprehensive Zephyr Devicetree expertise including overlays, bindings, C API macros, pin control, clocks, interrupts, DMA, and address translation. Use this skill when you need to: (1) Understand or create .dts/.dtsi/.overlay files, (2) Write or debug devicetree bindings (.yaml), (3) Use DT_* macros in C/C++ code, (4) Configure pin control, clocks, interrupts, or DMA in devicetree, (5) Resolve devicetree-related build errors, (6) Understand address translation and memory regions."
---

# Zephyr Devicetree Skill

Expert guidance on Zephyr's devicetree system for hardware description, driver integration, and build-time code generation.

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Common Workflows](#common-workflows)
3. [Hardware Configuration](#hardware-configuration)
4. [Advanced Topics](#advanced-topics)
5. [Troubleshooting](#troubleshooting)

---

## Core Concepts

### Understanding Devicetree Structure
Devicetree is a tree of nodes and properties. Zephyr uses **bindings** to validate nodes and generate C macros.

- **Basic syntax, nodes, properties**: See [syntax.md](references/syntax.md)
- **Bindings and compatible matching**: See [bindings.md](references/bindings.md)
- **Address translation (#address-cells, #size-cells, ranges)**: See [address-translation.md](references/address-translation.md)

### Key Files in a Build
After building, check these for debugging:
- `build/zephyr/zephyr.dts` — Final merged devicetree
- `build/zephyr/include/generated/devicetree_generated.h` — Generated macros

---

## Common Workflows

### 1. Modifying Hardware via Overlays
Overlays customize hardware without modifying base Zephyr files.

- **Override properties, add nodes, enable/disable devices**: See [overlays.md](references/overlays.md)

### 2. Writing Custom Bindings
Bindings define the schema for devicetree nodes.

- **Basic binding structure**: See [bindings.md](references/bindings.md)
- **Advanced features (child-binding, enums, specifier-cells)**: See [advanced-bindings.md](references/advanced-bindings.md)

### 3. Accessing Devicetree from C Code
Zephyr provides compile-time macros to access devicetree data.

- **Basic macros (node IDs, properties, registers)**: See [macros.md](references/macros.md)
- **Advanced macros (iteration, strings, bus helpers)**: See [advanced-macros.md](references/advanced-macros.md)

---

## Hardware Configuration

### Pin Control (Pinctrl)
Configure pin multiplexing and electrical properties.
- See [pinctrl.md](references/pinctrl.md)

### Clocks
Configure clock providers and consumers.
- See [clocks.md](references/clocks.md)

### Interrupts
Configure interrupt controllers and consumers with multi-level support.
- See [interrupts.md](references/interrupts.md)

### DMA
Configure DMA controllers and channel assignments.
- See [dma.md](references/dma.md)

---

## Advanced Topics

### Address Translation
Understanding `#address-cells`, `#size-cells`, and `ranges` for complex SoC hierarchies.
- See [address-translation.md](references/address-translation.md)

### Advanced Binding Features
Child bindings, enums, const, specifier-cells, and binding inheritance.
- See [advanced-bindings.md](references/advanced-bindings.md)

### Advanced C Macros
Iteration macros, string helpers, and bus-specific conveniences.
- See [advanced-macros.md](references/advanced-macros.md)

---

## Troubleshooting

For common errors and debugging techniques:
- See [debugging.md](references/debugging.md)

### Quick Reference

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| "binding for ... not found" | Missing or mismatched `compatible` | Check binding exists and `compatible` matches |
| `DEVICE_DT_GET()` returns NULL | Node disabled | Add `status = "okay";` |
| `__device_dts_ord_N` linker error | Driver not enabled | Enable driver in Kconfig |
| Property type mismatch | Binding expects different type | Check binding's `type:` field |

---

## Practical Examples

See [examples.md](references/examples.md) for complete working examples:
- GPIO LED (Blinky)
- I2C Sensor
- SPI Flash with Partitions
- PWM Buzzer
- UART with Pin Control
- ADC Channel Configuration
- CAN Bus Setup
- Timer/Counter Configuration
