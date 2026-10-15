---
name: zephyr-kernel-datapassing
description: Enhances the knowledge of an AI agent with all kernel objects and subsystems used to pass data between threads and ISRs in Zephyr OS. Use this skill when you need to implement, explain, or debug data passing mechanisms (FIFO, LIFO, Stack, Message Queue, Mailbox, Pipe, ZBus, Ring Buffer).
---

# Zephyr Kernel Data Passing

## Overview

This skill provides expert knowledge on Zephyr kernel objects and subsystems used for data passing. It helps in selecting the right mechanism for the task and provides implementation details.

## Workflow

### 1. Selection Strategy
To choose the correct data passing mechanism, first determine the requirements:
*   **Participants**: Thread-to-Thread? ISR-to-Thread? One-to-Many?
*   **Data Size**: Fixed small structure? Arbitrary size? Byte stream?
*   **Behavior**: FIFO? LIFO? Synchronous? Pub/Sub?
*   **Coupling**: Tight (direct reference) or loose (decoupled)?

**Step 1:** Read [references/comparison.md](references/comparison.md) to see the features, pros, cons, and a decision flowchart.

### 2. Implementation
Once the mechanism is selected, use the implementation guide to write the code.

**Step 2:** Read the appropriate reference:
*   **Kernel Objects**: [references/data_passing.md](references/data_passing.md) for FIFO, LIFO, Stack, Message Queue, Mailbox, Pipe.
*   **ZBus (Pub/Sub)**: [references/zbus.md](references/zbus.md) for publish-subscribe communication.
*   **Ring Buffer**: [references/ring_buffer.md](references/ring_buffer.md) for low-level byte stream buffering.

### 3. API & Configuration
For API signatures, Kconfig options, and sample locations.

**Step 3:** Read [references/api.md](references/api.md) for:
*   Complete API function signatures.
*   Kconfig options for each mechanism.
*   Header file and sample locations.

### 4. Troubleshooting
If debugging data passing issues, refer to the **Common Pitfalls** section at the end of [references/data_passing.md](references/data_passing.md).

## Source Locations

| Description | Path |
| :--- | :--- |
| **Data Passing Docs** | `<zephyr-ws-dir>/zephyr/doc/kernel/services/data_passing` |
| **ZBus Docs** | `<zephyr-ws-dir>/zephyr/doc/services/zbus/` |
| **Kernel Header** | `<zephyr-ws-dir>/zephyr/include/zephyr/kernel.h` |
| **ZBus Header** | `<zephyr-ws-dir>/zephyr/include/zephyr/zbus/zbus.h` |
| **Ring Buffer Header** | `<zephyr-ws-dir>/zephyr/include/zephyr/sys/ring_buffer.h` |
| **MsgQ Sample** | `<zephyr-ws-dir>/zephyr/samples/kernel/msg_queue` |
| **ZBus Samples** | `<zephyr-ws-dir>/zephyr/samples/subsys/zbus/` |
| **Philosophers Sample** | `<zephyr-ws-dir>/zephyr/samples/philosophers` |
