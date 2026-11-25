---
name: systems-memory
description: "Memory: stack versus heap, ownership models, allocation strategies (arenas, pools, reuse), fragmentation, leaks and how to find them, cache locality and data layout, false sharing and alignment, memory-mapped files and zero-copy, measuring heap versus resident memory, and garbage-collected runtimes' knobs. Read before optimising memory use or chasing a leak."
---

# Memory: where it lives, how long, what it costs

The default version allocates a fresh `Vec` or `std::string` per item in
the hot loop, keeps a cache that only grows, links objects with
`Rc<RefCell<_>>` or `shared_ptr` in both directions so the cycle never
frees, chases pointers through a linked list, puts two threads' counters
on one cache line, and "fixes" memory by guessing because nobody compared
RSS with the live heap. This skill gives the decisions and the tools:
where data lives, how to allocate less, how to find a leak, how layout
decides speed, and what to measure. Profiling in general is in
`performance-profiling`.

## 1. Where data lives and for how long

| Place | Lives | Cost | Limit |
|---|---|---|---|
| Stack | the function call | nothing (a pointer bump) | 8 MiB main thread on Linux and macOS, 1 MiB on Windows, 2 MiB per Rust-spawned thread, 512 KiB per secondary pthread on macOS |
| Heap | until freed or dropped | tens of ns for small blocks; far more when it goes to the OS or contends | RAM, the container limit |
| Static | the whole process | none | fixed at build time |
| Memory map | until unmapped | a page fault on first touch | address space, the file |

- Large buffers go on the heap: a 1 MiB array on a spawned thread's stack
  overflows it. In Rust, `vec![0u8; n].into_boxed_slice()`, not
  `Box::new([0u8; N])` (which may build the array on the stack first).
- Recursion over input depth overflows the stack: an explicit `Vec` stack
  or a depth cap (`systems-formats`). Bigger stacks where needed:
  `thread::Builder::new().stack_size(8 << 20)`, `pthread_attr_setstacksize`.

## 2. Ownership models

| Model | Where | Frees | Watch for |
|---|---|---|---|
| Single owner, borrowed views | Rust, C++ `unique_ptr`, C create/destroy pairs | at scope end, deterministically | views outliving the owner |
| Reference counting | `Arc`, `Rc`, `shared_ptr`, Swift, CPython | when the last reference goes | cycles leak; atomic counts cost under contention |
| Arena or region | bumpalo, `std::pmr`, per-request pools | all at once | nothing freed early; destructors may not run |
| Tracing GC | Go, JVM, .NET, JavaScript | when unreachable | pauses, heap sizing, references held by caches |

## 3. Allocate less in hot paths

Count first: allocations per operation from `dhat` (Rust), heaptrack
(Linux) or Instruments' Allocations (macOS). Then:

- Reuse: hoist buffers out of loops and `clear()` them (Rust `Vec` and
  `String`, C++ `std::vector` keep their capacity); pass `&mut Vec<T>`
  into hot functions instead of returning a new one.
- Size once: `with_capacity(n)` or `reserve(n)` when the size is known or
  bounded; `shrink_to_fit()` on long-lived collections after a burst.
- Stay inline: `SmallVec<[T; 8]>`, `arrayvec`, `compact_str` in Rust;
  C++ strings keep 15 (libstdc++, MSVC) or 22 (libc++) chars inline.
- Hidden allocations: `format!` and `to_string()` per item, `clone()` of
  `String` and `Vec`, `collect()` into a temporary, boxed closures, a
  `std::function` with large captures, strings built with `+` in a loop.
- Share instead of copy: `Arc<str>`, `bytes::Bytes` slices, interned
  identifiers.
- dhat behind a `dhat-heap` feature: `#[global_allocator] static ALLOC:
  dhat::Alloc = dhat::Alloc;` and `let _profiler =
  dhat::Profiler::new_heap();` first in `main` (writes `dhat-heap.json`).

## 4. Arenas and pools

An arena (bump allocation) suits data that dies together: per request,
per frame, per parse, per compiler pass. Allocation is a pointer bump;
freeing is one reset.

```rust
let mut arena = bumpalo::Bump::new();
for request in requests {
    {
        let doc = parse_in(&arena, request)?; // Document<'_> borrows the arena
        respond(&doc)?;
    }
    arena.reset(); // frees everything at once, keeps the largest chunk
}
```

- `bumpalo` does not run `Drop` for what it holds: store plain data and
  its own collections (feature `collections`), not a std `String`, `Vec`
  or file handle, whose heap memory or descriptor would leak. `typed-arena`
  runs destructors.
- Graphs by index: a `Vec<Node>` with `u32` ids, `slotmap` for keys that
  detect stale use, `slab` for a pool of same-type objects.
- C++ `std::pmr::monotonic_buffer_resource` with `std::pmr::vector`; in C,
  a bump arena over `malloc`ed blocks.
- Object pools only when a profile blames allocation of that type: modern
  allocators already cache small blocks per thread, and a pool hides
  use-after-release from ASan and holds its peak forever. Cap it.

## 5. Allocators and fragmentation

- Fragmentation shows as RSS high or growing while the live heap is flat:
  free memory scattered between live blocks cannot return to the OS.
  Typical of long-running, multi-threaded servers with mixed sizes.
- glibc malloc makes up to 8 arenas per core for threads;
  `MALLOC_ARENA_MAX=2` is a quick test of whether that is the cause, and
  `malloc_trim(0)` hands free pages back.
- jemalloc (`tikv-jemallocator`) and mimalloc (`mimalloc` crate) fragment
  less and scale better with threads; musl's allocator is slow under
  threads. Switch only with before and after numbers (RSS and throughput
  on the real workload):

```rust
#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;
```

- Short-lived data in an arena, long-lived data on the heap: mixing both
  in one heap is a common cause of fragmentation.

## 6. Leaks, and how to find them

Usual causes: reference cycles (make the back-pointer `Weak` or
`weak_ptr`); caches and maps without a bound or expiry (`lru`, or `moka`
with a capacity); unbounded channels and queues; listeners and callbacks
registered and never removed; tasks or threads that never finish and hold
their captures; `Box::leak` or `mem::forget` as shortcuts; a C `*_free`
missed on one error path; `Vec` capacity kept after a burst.

| Tool | Platform | Finds | Run |
|---|---|---|---|
| LeakSanitizer | Linux, with ASan | unreachable blocks at exit | `-fsanitize=address`, on by default |
| Valgrind memcheck | Linux | leaks, invalid access (20 to 50 times slower) | `valgrind --leak-check=full ./app` |
| heaptrack | Linux | allocations by stack over time, peak, leaks | `heaptrack ./app`, then `heaptrack_gui` or `heaptrack_print` |
| dhat | Rust, any OS | allocation counts, peak, short-lived blocks | the `dhat` crate, `dhat-heap.json` in DHAT's viewer |
| leaks, Instruments | macOS | leaks, allocations by stack | `leaks --atExit -- ./app`; Allocations and Leaks |
| Heap profiles | jemalloc `prof`, Go pprof, JVM heap dumps | growth between two points | diff two snapshots minutes apart |

A server's leak rarely shows at exit: the memory is still reachable (a
map that grows). Take two heap profiles under steady load and compare
what grew.

## 7. Cache locality and data layout

Rough costs: an L1 hit about 1ns, L2 about 4ns, L3 10 to 40ns, main memory
80 to 120ns. A loop is fast when its next data is already in cache.

- Contiguous beats linked: `Vec<T>` over `LinkedList<T>` and over
  `Vec<Box<T>>`; indices over pointers; a sorted `Vec` with binary search
  over a tree for read-mostly sets. A linear scan of a few dozen elements
  beats a hash map.
- Struct of arrays for hot loops that read one or two fields of many
  records (`xs: Vec<f32>, ys: Vec<f32>` instead of `Vec<Particle>` with
  ten fields): the loop loads only the bytes it uses, and vectorises.
- Split hot from cold: fields the loop touches in one struct, rarely used
  ones behind a `Box` or in a side table.
- Walk memory in order (row-major for `[row][col]`); block large matrix
  work into tiles that fit in cache.

## 8. Size, alignment and padding

- Rust reorders fields of default-repr structs to cut padding;
  `#[repr(C)]`, C and C++ keep declaration order, so order fields from the
  largest alignment down. Pin sizes that matter:

```rust
const _: () = assert!(std::mem::size_of::<Entry>() == 16);
```

```c
_Static_assert(sizeof(struct entry) == 16, "entry must stay 16 bytes");
```

- Inspect with `pahole -C entry ./binary` (holes and padding from DWARF)
  or `cargo +nightly rustc -- -Zprint-type-sizes`.
- An enum is as big as its largest variant: box a rare large one (clippy
  `large_enum_variant`). `Option<Box<T>>`, `Option<&T>` and
  `Option<NonZeroU32>` cost nothing extra (niche).
- `u32` indices instead of `usize` or pointers halve index-heavy
  structures on 64-bit targets.

## 9. False sharing

Two threads writing different variables on one cache line make the line
bounce between cores; every write becomes a miss. Pad per-thread or
per-shard hot data to its own line: 128 bytes on x86-64 (the adjacent-line
prefetcher pulls pairs of 64-byte lines) and on big Arm cores such as
Apple silicon, 64 elsewhere.

```rust
struct Stats { per_worker: Vec<crossbeam_utils::CachePadded<AtomicU64>> }
```

```cpp
struct alignas(128) PerThread { std::atomic<std::uint64_t> count{0}; };
```

Find it with `perf c2c record` then `perf c2c report` on Linux, or by a
counter whose throughput falls as threads are added.

## 10. Memory-mapped files

- For large, read-mostly files with random access (indexes, lookup
  tables, databases): the page cache backs them and processes share it.
  For one sequential pass, buffered reads with a 64 KiB to 1 MiB buffer
  are as fast and simpler.
- The map is only as stable as the file: another process truncating it
  turns an access into SIGBUS, and its writes change bytes under your
  `&[u8]`. Map files you own; validate before trusting.

```rust
let file = std::fs::File::open(&path)?;
// SAFETY: the file lives in our data directory, is opened read-only, and
// is never truncated or written while mapped (single-writer rule, store.rs).
let map = unsafe { memmap2::Mmap::map(&file)? };
map.advise(memmap2::Advice::Random)?; // Unix only
```

- Writable maps need `flush()` (msync) to be durable, like `fsync`
  (`systems-os`). 32-bit targets run out of address space at a few GiB;
  on Windows a mapped file cannot be deleted or truncated.

## 11. Zero-copy

- Parse into borrowed views (`&'a [u8]`, `&'a str`, `Cow<'a, str>` with
  `#[serde(borrow)]`) when the buffer outlives the parsed value
  (`systems-formats`).
- `bytes::Bytes`: reference-counted, `split_to` and `slice` hand out parts
  of one buffer without copying; `BytesMut::freeze` after filling.
- Kernel copies: `std::io::copy` between files and sockets uses
  `copy_file_range`, `sendfile` or `splice` on Linux where it can.
- A copy of under a few KiB often costs less than the lifetime plumbing,
  and than a small borrowed slice that keeps a large buffer alive.

## 12. Measure the right number

| Number | Means | Read it |
|---|---|---|
| VSZ | address space reserved; says little | `ps -o vsz= -p <pid>` |
| RSS | pages in RAM now, with shared libraries and mapped files | `ps -o rss= -p <pid>`, VmRSS in `/proc/<pid>/status` |
| Peak RSS | the high-water mark | `/usr/bin/time -v` (Linux), `/usr/bin/time -l` (macOS), VmHWM |
| PSS | shared pages split among the processes sharing them | `/proc/<pid>/smaps_rollup`, `smem` |
| Live heap | allocated and not yet freed | heaptrack, dhat, allocator stats, GC metrics |
| Footprint (macOS) | what the OS charges the process | `footprint <pid>`, `vmmap -summary <pid>` |

RSS far above the live heap: fragmentation, allocator caching or mapped
files. The live heap growing under steady load: a leak or an unbounded
structure. Report steady state after warm-up and peak under the largest
input separately, with the workload.

## 13. Containers and garbage-collected runtimes

- The container limit is the ceiling (cgroup v2 `memory.max`, use in
  `memory.current`, detail in `memory.stat`; page cache counts but is
  reclaimed first). Crossing it gets SIGKILL: exit code 137, `OOMKilled`,
  a line in `dmesg`, no destructors or final log. Size caches from the
  limit, not the host's RAM, and keep peak under about 80% of it.
- Go: `GOMEMLIMIT` at about 90% of the limit with `GOGC` (default 100);
  heap profiles via `pprof`.
- JVM: `-XX:MaxRAMPercentage=75` in containers instead of a fixed `-Xmx`;
  G1 by default, ZGC (`-XX:+UseZGC`) for short pauses on large heaps,
  Parallel for batch throughput; `-Xlog:gc*` to see pauses.
- Node: `--max-old-space-size=<MiB>` at about 75% of the limit. .NET:
  Server GC for services (`DOTNET_gcServer=1`), `DOTNET_GCHeapHardLimit`,
  `dotnet-counters` and `dotnet-gcdump`. A GC frees only what nothing
  references: bounded caches and removed listeners matter there too.

## Check it

- Before and after numbers on the same workload: allocations per
  operation, steady and peak RSS, throughput. A memory change without
  them is a guess.
- `bash`: the ASan or Valgrind run reports no leaks; dhat or heaptrack
  shows the hot-path allocation gone; the size assertions compile.
- A long run under load: RSS sampled every minute for 30 minutes or more
  is flat after warm-up.
- Say which tools could not run here (Valgrind and heaptrack need Linux).

## Avoid

Allocating per item in hot loops; caches, maps and queues without bounds;
`Rc` or `shared_ptr` cycles; pools added without a measurement; large
arrays on the stack; linked structures for data that is iterated; hot
per-thread data sharing a cache line; mapping files others may truncate;
judging memory by VSZ, or by RSS alone; switching allocators or GC flags
without numbers; sizing from the host's RAM inside a container.
