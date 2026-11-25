---
name: riscos-re
description: Reconstruct functionality, interfaces, and state machines from RISC OS module binaries. Use when you need to understand how an existing RISC OS module works or reimplement it in C.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-dump:*) Bash(riscos-dumpi:*)
---

# RISC OS Reverse Engineering (riscos-re)

A guide for analyzing RISC OS module binaries and reconstructing their functionality, interfaces, and internal state machines.

## Initial Reconnaissance

### 1. Identify the Module Header
Every RISC OS module starts with a fixed-format header. Use `riscos-dump --words <file>` to inspect the first 10 words:
*   **Offset &00:** Initialisation code offset.
*   **Offset &04:** Finalisation code offset.
*   **Offset &08:** Service call handler offset.
*   **Offset &0C:** Title string offset (usually followed by the title itself).
*   **Offset &10:** Help string offset (contains version and date).
*   **Offset &14:** Command table offset.
*   **Offset &18:** SWI chunk base (e.g., `&58000`).
*   **Offset &1C:** SWI handler offset.
*   **Offset &20:** SWI name table offset.

### 2. Extract the Interface (SWIs and Commands)
*   **SWI Names:** Look at the offset from `&20`. The first string is the prefix (e.g., `ESocket`), followed by function names (e.g., `ConnectToHost`).
*   **Commands:** Inspect the table at offset `&14`. Each entry typically defines the command name, min/max arguments, and a help string.

## Disassembly Analysis

### 1. Identify named functions
Use `riscos-dumpi --function-map <file>` to locate the named functions within the binary. Absolute files will have an offset of 0x8000 added to their addresses. These named functions may help to identify the necessary functionality and the intended behaviour. Retaining the same names may help with the conversion to C.

### 2. Mapping the SWI Dispatcher
Use `riscos-dumpi <file>` to find the SWI handler. Look for a branch table (a series of `B` instructions) near the start of the handler. This maps SWI offsets (`0, 1, 2...`) to internal function addresses.

### 3. Identifying System Interactions
Search the disassembly for `SWI` calls to understand how the module interacts with the OS:
*   **Socket/Internet:** `XSocket_Creat`, `XSocket_Ioctl`, `XResolver_GetHost`.
*   **Memory:** `OS_Module 6` (Claim), `OS_Module 7` (Free).
*   **Events:** `OS_Claim` for `EventV` (16). Look for `OS_Byte 14` to enable specific events like `Internet` (19).
*   **Filters:** `Wimp_RegisterFilter` indicates the module is trapping Wimp messages (like `TaskWindow_Input`).

### 4. Reconstructing State Structures
Identify the "Private Word" (R12) usage. In C, this maps to your global workspace. 
*   Look for patterns like `LDR R0, [R11, #8]`. If R11 is a validated handle, `#8` is a field in the handle's struct.
*   **Magic Numbers:** Modules often use magic words (e.g., `&FEEF1EF0`) at fixed offsets in allocated blocks to validate pointers passed from userspace.

## Reimplementation Strategy

### 1. Handle Safety
Original assembly often trusts user-provided pointers. In C, implement a validation function that:
1. Checks the pointer is not NULL.
2. Checks for a Magic Number at a known offset.
3. (Preferably) Iterates through a known list of active handles to ensure the pointer is actually one managed by the module.

### 2. Buffering and Non-blocking I/O
RISC OS modules must not block the machine. 
*   Use `ioctl(s, FIONBIO, &on)` to ensure all sockets are non-blocking.
*   Implement internal buffers for read operations to handle partial data arriving over multiple polls.

### 3. Task-Aware Cleanup
If the module is used by multitasking applications, it must handle `Service_WimpCloseDown` (&53).
*   Store the `task_handle` (usually from `Wimp_ReadSysInfo`) in your socket structures.
*   When the service call fires, close only the sockets and free resources belonging to the task handle in `R0`.

## Documentation Synthesis
Combine findings from the binary with any available documentation.
*   **States:** Map return codes (1, 2, 3, 4) to semantic states (Lookup, Connecting, Listening, Connected).
*   **Flags:** Deconstruct register bitfields (e.g., `R2` in `SendLine`) to provide clear C defines.
