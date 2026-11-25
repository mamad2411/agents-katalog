---
name: esp32-modbus-security-and-mapping
description: Use when implementing Modbus RTU/TCP register maps, scaling, access control, exception handling or multi-vendor interoperability.
license: MIT
---

# Modbus Security And Mapping

A Modbus register map is an application contract, not a universal schema. Address notation, data representation, permissions and timing vary by vendor.

## Addressing and functions

Separate protocol reference numbers (such as 30001/40001 notation) from zero-based PDU offsets. Record function code, table, offset, quantity, access mode and device-specific limits. Do not blindly subtract 40001 unless the vendor map explicitly uses that convention. Validate legal quantities and avoid crossing undocumented register boundaries.

## Data representation

Specify signedness, word order, byte order, scaling, engineering units, invalid sentinels and update rate for every multi-register value. Test IEEE-754 floats and 32/64-bit integers with known byte patterns. Preserve raw register values alongside converted values so field diagnostics can distinguish transport from scaling errors.

## Security and robustness

Treat Modbus as unauthenticated unless protected by a separate trusted network/security layer. Segment control networks, restrict write-capable clients and use allowlists for writable ranges. Validate unit ID, function code, quantity and payload length. Rate-limit expensive operations and never expose arbitrary register writes to an internet-facing endpoint.

## Interoperability tests

| Test | Expected result |
|---|---|
| Unknown unit ID | Defined timeout/ignore policy |
| Illegal address | Correct exception response |
| Read-only write | Rejected and logged |
| Swapped word order | Detected by known-pattern test |
| Maximum register quantity | Boundary validated |
| Duplicate request | Idempotent read; safe write policy |

## Agent rules

Keep a machine-readable register map with source document revision. Never infer units or scaling from register numbers. Use explicit conversion functions and test vectors. Record vendor-specific deviations and gateway behavior.

## Field evidence to capture

- Record the exact ESP32 SoC, module, board revision and schematic revision.
- Record framework, compiler, driver version and relevant configuration flags.
- Preserve raw measurements and error codes before applying filters or retries.
- Separate a suspected cause from a reproduced root cause and a verified fix.
- Link the test result to a reproducible fixture or documented manual procedure.

## Version and safety boundary

Check the selected target's datasheet, errata and framework release notes before choosing APIs or pin capabilities. Electrical protection, isolation, overcurrent limits and safe outputs must be designed independently of firmware. A passing host test is not evidence of electrical compliance or field reliability.
