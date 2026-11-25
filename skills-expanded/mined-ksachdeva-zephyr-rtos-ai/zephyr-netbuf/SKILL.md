---
name: zephyr-netbuf
description: Expert guidance on Zephyr's Network Buffer (net_buf) subsystem for efficient data management. Use when the user asks about buffer pools, net_buf allocation, reference counting, data manipulation (add/push/pull/remove), buffer fragmentation, headroom/tailroom, or implementing protocol parsing/encoding in Zephyr applications (networking, Bluetooth, USB).
---

# Zephyr Network Buffers (net_buf)

## Overview

This skill provides expert knowledge on Zephyr's `net_buf` subsystem — a core memory management library used by networking, Bluetooth, and USB stacks. It covers pool creation, buffer lifecycle, data manipulation, and fragmentation patterns.

## Key Concepts

**Two Buffer Types:**
- `net_buf_simple` — Lightweight, no reference counting, stack-allocatable. Use for constrained scenarios.
- `net_buf` — Full-featured with reference counting, fragmentation, user data. Use for passing through kernel objects (FIFOs).

**Buffer Layout:**
```
[__buf start] <-- headroom --> [data] <-- len --> [tailroom] <-- [__buf end]
                                  ^
                               data pointer
```

## Workflow

### 1. Choose Buffer Type

| Scenario | Use |
|----------|-----|
| Temporary parsing, stack allocation | `net_buf_simple` + `NET_BUF_SIMPLE_DEFINE` |
| Pool-based allocation, ref counting | `net_buf` + `NET_BUF_POOL_DEFINE` |
| Large/fragmented packets | `net_buf` with fragment chains |

### 2. Pool Definition

For `net_buf`, define a pool at file scope:

```c
#include <zephyr/net_buf.h>

/* Fixed-size buffers (most common) */
NET_BUF_POOL_DEFINE(my_pool,
    10,    /* count: number of buffers */
    128,   /* size: max data per buffer */
    4,     /* user_data_size: metadata per buffer */
    NULL); /* destroy callback (optional) */
```

**Pool variants**: See [references/api.md](references/api.md) for `NET_BUF_POOL_VAR_DEFINE` (variable size) and `NET_BUF_POOL_HEAP_DEFINE` (heap-backed).

### 3. Allocation & Lifecycle

```c
/* Allocate (blocks until available or timeout) */
struct net_buf *buf = net_buf_alloc(&my_pool, K_FOREVER);

/* Reserve headroom for protocol headers */
net_buf_reserve(buf, HEADER_SIZE);

/* ... use buffer ... */

/* Release (returns to pool when refcount hits 0) */
net_buf_unref(buf);
```

**Reference counting:**
- `net_buf_alloc()` → refcount = 1
- `net_buf_ref(buf)` → increments refcount
- `net_buf_unref(buf)` → decrements; frees when 0

### 4. Data Manipulation

Four operation types — choose based on direction:

| Operation | Direction | Pointer | Length | Use Case |
|-----------|-----------|---------|--------|----------|
| **Add** | End ↓ | Unchanged | +len | Append payload |
| **Remove** | End ↑ | Unchanged | -len | Trim from tail |
| **Push** | Start ← | Moves back | +len | Prepend header |
| **Pull** | Start → | Moves forward | -len | Parse/consume header |

**Step 4:** Read [references/operations.md](references/operations.md) for:
- Endian-aware helpers (`_le16`, `_be32`, etc.)
- Byte-by-byte protocol parsing patterns
- Common encoding/decoding examples

### 5. Fragmentation (Advanced)

For packets larger than a single buffer:

```c
struct net_buf *head = net_buf_alloc(&pool, K_FOREVER);
struct net_buf *frag = net_buf_alloc(&pool, K_FOREVER);

/* Add fragment to chain */
net_buf_frag_add(head, frag);

/* Iterate fragments */
for (struct net_buf *f = head; f; f = f->frags) {
    /* process f->data, f->len */
}

/* Total length across all fragments */
size_t total = net_buf_frags_len(head);
```

See [references/fragmentation.md](references/fragmentation.md) for advanced patterns.

### 6. API & Configuration

**Step 6:** Read [references/api.md](references/api.md) for:
- Complete API function signatures
- Kconfig options (`CONFIG_NET_BUF_LOG`, `CONFIG_NET_BUF_POOL_USAGE`)
- Pool definition macro variants

## Common Pitfalls

- **Forgetting headroom**: Call `net_buf_reserve()` immediately after allocation if you need to prepend headers later.
- **Double unref**: Each `alloc` or `ref` needs exactly one `unref`. Track ownership carefully.
- **ISR allocation**: Use `K_NO_WAIT` in ISRs and handle NULL returns.
- **Blocking in destroy callback**: The destroy callback runs with a spinlock held — keep it fast.

## Source Locations

| Description | Path |
|:---|:---|
| **net_buf Header** | `<zephyr-ws>/deps/zephyr/include/zephyr/net_buf.h` |
| **net_buf Implementation** | `<zephyr-ws>/deps/zephyr/lib/net_buf/buf.c` |
| **Documentation** | `<zephyr-ws>/deps/zephyr/doc/services/net_buf/index.rst` |
| **UART Async Sample** | `<zephyr-ws>/deps/zephyr/samples/drivers/uart/async_api/` |
| **Bluetooth Samples** | `<zephyr-ws>/deps/zephyr/samples/bluetooth/` |
