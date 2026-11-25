---
name: esp32-memory-and-heap
description: Use when an ESP32 runs out of memory, fragments over days, cannot allocate a DMA buffer, or a task crashes with a stack overflow. Covers internal RAM versus PSRAM, heap capabilities, stack sizing and what DMA can actually reach.
license: MIT
---

# Memory and heap on ESP32

"Out of memory" on ESP32 usually means "no contiguous block of the right kind",
which is a different problem from "not enough bytes".

## The two memories are not interchangeable

| | Internal SRAM | PSRAM (external) |
|---|---|---|
| Size | a few hundred KB, shared with the stack and DMA | 2-8 MB on modules that have it |
| Speed | fast, on-die | slower, through the cache |
| DMA | reachable | **not reachable on the classic ESP32** |
| Use for | stacks, DMA buffers, ISR data | big buffers, images, JSON documents |

A `malloc()` for a 200 KB buffer fails on a board with 4 MB of PSRAM unless the
allocation asks for it. And a DMA descriptor allocated in PSRAM fails at runtime
even though the allocation succeeded - the peripheral cannot read that memory.

## Ask for the kind of memory you need

```c
void *buf = heap_caps_malloc(len, MALLOC_CAP_SPIRAM);   // PSRAM, no DMA
void *dma = heap_caps_malloc(len, MALLOC_CAP_DMA);      // internal, DMA-safe
```

`MALLOC_CAP_DMA` is the one people forget. On the classic ESP32 it forces an
internal allocation, which is why a Wi-Fi + camera + TLS design can pass every
size check and still fail at the first transmit.

## Total free heap is the wrong number

```c
heap_caps_get_free_size(MALLOC_CAP_8BIT);        // total
heap_caps_get_largest_free_block(MALLOC_CAP_8BIT); // what a single malloc can get
```

A heap with 80 KB free and a largest block of 4 KB cannot allocate 8 KB. Watch the
largest block over time; that is the number that predicts the next failure.

Fragmentation comes from mixing allocation sizes. Fixed-size pools for
frequently-created objects remove most of it.

## Stack sizing

- `xTaskCreate()` takes **bytes** on ESP-IDF, **words** on vanilla FreeRTOS. A
  value copied from an example can be a quarter of what you meant.
- `uxTaskGetStackHighWaterMark()` tells you the real headroom. Log it once under
  load; a task sitting at 40 bytes of margin will overflow on a different input.
- Deep call chains (JSON parsing, printf with floats) need more than the code
  suggests.

## Rules for the agent

- Never increase a buffer size to "fix" an allocation failure without checking
  which heap it came from.
- When a crash is a `LoadProhibited` inside a task and the same code works in
  `loop()`, suspect the stack before the pointer.
- If the design needs a big buffer and the board has PSRAM, say so explicitly in
  the code - a silent `malloc()` that lands in internal RAM is a bug waiting for
  a busy day.
