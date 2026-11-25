---
name: performance-memory
description: "Memory problems: finding leaks with heap snapshots and growth over time, reducing allocations, streaming instead of loading whole files or result sets, choosing data structures, pools and their costs, container memory limits and OOM kills, runtime settings for Node, the JVM, Go, Python and .NET, and measuring resident versus heap memory. Read when memory grows, a process is killed for memory, or memory use must shrink."
---

# Memory: growth, leaks and limits

The default response to memory trouble treats the symptom: the limit raised
until the OOM kills stop, a nightly restart, `gc()` called by hand,
`heapUsed` watched while buffers outside the heap grow, a fix shipped
without comparing two snapshots, a 2 GB export built in a list before the
first byte is sent. This skill reads the symptom, measures the right
number, finds what holds the memory, and sets the runtime and the container
so the process lives inside its limit. Allocators, data layout and cache
locality are in `systems-memory`.

## 1. Read the symptom

| Pattern under steady load | Usual meaning |
|---|---|
| Rises, then plateaus | warm-up: caches, JIT code, pools, allocator arenas; fine if the plateau fits |
| Sawtooth with a flat floor | healthy GC; high peaks mean a high allocation rate or a small heap |
| Sawtooth with a rising floor | a leak under GC: each collection frees less |
| Straight climb, never levels | a leak or an unbounded cache |
| Steps at certain requests or times | a request, report or job loading everything at once |
| RSS grows while the heap is flat | native memory: buffers, fragmentation, native libraries, thread stacks |
| Killed, exit code 137, `OOMKilled` | the container or cgroup limit was hit (SIGKILL, 128 + 9) |
| p99 spikes lined up with GC | allocation pressure, or a heap too close to its limit |

Watch long enough before calling growth a leak: a soak test of hours
(`performance-load`) separates a slow warm-up from a leak.

## 2. Measure the right number

- **RSS** (resident set size) is what the process holds in RAM, close to
  what a container limit counts. **Heap** is what the runtime manages. The
  gap is native memory: buffers, thread stacks, JIT code, and memory the
  allocator keeps after the heap freed it.
- A container limit counts the cgroup: anonymous memory plus page cache
  (reclaimed before a kill). Kubernetes uses the working set (usage minus
  inactive file cache) for `kubectl top` and eviction.
- **Peak** decides whether it fits; **steady state** decides how many
  instances fit on a node. Measure over a window that includes the
  heaviest job.
- **Allocation per operation** (bytes and objects per request) drives GC
  time: benchmarks report it (`performance-benchmarks`), and allocation
  profiles show where it comes from.

```bash
ps -o pid,rss,vsz,command -p <pid>              # RSS in KB
grep -E 'VmRSS|VmHWM' /proc/<pid>/status        # current and peak RSS (Linux)
/usr/bin/time -v ./job                          # Maximum resident set size (GNU time, Linux)
/usr/bin/time -l ./job                          # maximum resident set size in bytes (macOS)
cat /sys/fs/cgroup/memory.current /sys/fs/cgroup/memory.peak   # cgroup v2; peak needs kernel 5.19+
docker stats --no-stream                        # or kubectl top pod
```

| Runtime | Heap and memory outside it |
|---|---|
| Node | `process.memoryUsage()`: `rss`, `heapUsed`, `heapTotal`, `external`, `arrayBuffers` (Buffers live outside the V8 heap) |
| JVM | `jcmd <pid> GC.heap_info`, `jstat -gcutil <pid> 1000`; native: `-XX:NativeMemoryTracking=summary`, then `jcmd <pid> VM.native_memory summary` |
| Go | `runtime/metrics` (heap, stacks, GC CPU) and the pprof heap profile |
| Python | `tracemalloc.get_traced_memory()` (current, peak); `resource.getrusage(resource.RUSAGE_SELF).ru_maxrss` (KB on Linux, bytes on macOS) |
| .NET | `dotnet-counters monitor -p <pid>`: GC heap size, allocation rate, gen 0, 1 and 2 counts |

## 3. Find the leak

The method is the same in every runtime:

1. Reproduce with a repeatable workload: the same request or operation in
   a loop.
2. Warm up, take snapshot A; run the operation N times (1,000 is plenty),
   snapshot B; N more, snapshot C. Tools collect garbage first.
3. Compare: objects whose count grows by about N (or a multiple) between
   each pair are the leak. Ignore one-off growth between A and B.
4. Follow the **retainers**, the chain of references from a GC root to the
   leaked object. The fix is the link that should have been removed, not
   the object.

Sort by **retained size** (what would be freed if the object went), not
shallow size (the object alone): a small `Map` retaining 800 MB of entries
is the finding.

- **Node and browsers**: DevTools Memory panel, heap snapshots in the
  Comparison view sorted by size delta, with the Retainers pane; the
  allocation timeline shows allocations still alive. In production:
  `node --heapsnapshot-signal=SIGUSR2`, `v8.writeHeapSnapshot()`, or
  `--heapsnapshot-near-heap-limit=1` to capture the heap just before an
  OOM. For pages, look for detached DOM nodes.
- **Python**: `tracemalloc` snapshots compared by traceback; memray for
  Python and native allocations.

  ```python
  import tracemalloc
  tracemalloc.start(25)                      # keep 25 frames per allocation
  before = tracemalloc.take_snapshot()
  run_workload(1000)
  after = tracemalloc.take_snapshot()
  for stat in after.compare_to(before, "traceback")[:10]:
      print(stat)
      print("\n".join(stat.traceback.format()[-6:]))
  ```

  `memray run -o out.bin app.py`, then `memray flamegraph --leaks out.bin`
  (run with `PYTHONMALLOC=malloc` for leak reports); `memray attach <pid>`
  for a live process.
- **Go**: compare two heap profiles, `go tool pprof -base heap1.pb.gz
  heap2.pb.gz` (`-sample_index=inuse_space`). A goroutine count that only
  grows (`/debug/pprof/goroutine?debug=1`) is goroutines blocked forever;
  go.uber.org/goleak catches them in tests.
- **JVM**: `jcmd <pid> GC.heap_dump /tmp/app.hprof`, opened in Eclipse MAT
  (Leak Suspects, the dominator tree, retained sizes). In production run
  with `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/dumps`.
- **.NET**: `dotnet-gcdump collect -p <pid>` twice and compare by type;
  `dotnet-dump analyze` with `dumpheap -stat` and `gcroot` for retainers.
- **Native**: heaptrack, Valgrind `--leak-check=full`, LeakSanitizer
  (`-fsanitize=address`), the `dhat` crate for Rust, Instruments or
  `leaks <pid>` on macOS (`systems-memory`).

Heap dumps pause the process, can need as much memory again, and contain
secrets and personal data: take them from an instance out of rotation, keep
them private, delete them afterwards.

Usual causes, roughly in the order they turn up:

- Caches and maps with no bound: a `Map` keyed by user, session or request
  id; `@lru_cache(maxsize=None)` or `@cache` on a function called with
  ever-new arguments.
- Listeners, subscriptions, timers and intervals added per request or per
  mount and never removed (Node warns past 10 listeners on one emitter;
  React effects without a cleanup).
- Closures that capture a large object (the request, a buffer) and are
  stored somewhere long-lived.
- Registries that only grow: metrics labelled with user ids or raw URLs,
  in-memory queues nobody drains, lists of recent items without a cap.
- Resources never closed: response bodies (Go), streams, files, cursors,
  connections; goroutines or tasks waiting on a channel nobody writes to.
- Thread-locals in pooled threads, class loaders kept across redeploys
  (JVM), detached DOM nodes still referenced from JavaScript.

## 4. Use less memory

- **Stream instead of loading.** Read files, uploads and bodies in chunks
  or lines; parse big JSON with a streaming parser (`json.Decoder` in Go,
  ijson in Python, NDJSON line by line); write exports as a stream to the
  response or object storage. Memory stays flat at any size and the first
  byte leaves early. A file loaded whole costs its size plus its parsed
  objects, often several times more.
- **Page through large result sets.** Server-side cursors or batches of
  1,000 to 5,000 rows: Django `.iterator(chunk_size=2000)`, SQLAlchemy
  `yield_per`, Laravel `lazyById()` or `chunkById()`, Rails `find_each`,
  keyset pagination by hand (`database-queries`).
- **No intermediate collections.** Generators in Python, one loop instead
  of `.map().filter().map()` over a large array in JavaScript, lazy
  iterators in Rust, `strings.Builder` or `"".join()` instead of
  concatenation in a loop.
- **Preallocate when the size is known** (`make([]T, 0, n)`,
  `Vec::with_capacity(n)`, a sized `StringBuilder`) and reuse buffers
  across iterations of a hot loop.
- **Compact representations.** A Python `int` is 28 bytes plus an 8-byte
  pointer in a list: a million ints take about 36 MB as a list and 8 MB as
  `array('q')` or a NumPy array. `__slots__` drops the per-instance dict of
  a Python class; typed arrays in JavaScript; primitive arrays instead of
  `List<Integer>` in Java; enums or small ints instead of repeated
  strings; Arrow or Parquet for columns of analytics data.
- **Bound every cache** by entries or bytes, with a TTL where data goes
  stale: lru-cache (`max`, `maxSize`) in Node, `lru_cache(maxsize=1024)`
  in Python, Caffeine (`maximumSize`, `maximumWeight`) on the JVM, moka in
  Rust. Keys and invalidation are in `backend-caching`.
- **Pools only when measured.** Modern allocators and collectors make
  short-lived small objects cheap. A pool keeps its peak forever, can hand
  one user's data to the next if not reset, and adds contention. It pays
  for large buffers reused at a high rate (`sync.Pool` in Go,
  `ArrayPool<T>` in .NET), after a profile shows the allocation cost. In
  .NET, arrays of 85,000 bytes or more land on the Large Object Heap,
  collected only with gen 2 and prone to fragmentation: rent them.
- **Big one-off jobs in a process that ends.** CPython and glibc seldom
  give freed memory back to the OS, so a worker that once built a 2 GB
  report keeps a high RSS. Run such jobs in a subprocess or a job worker
  that exits or is recycled after them.

## 5. Containers and OOM kills

- The memory **limit** is a hard cap: crossing it gets the process
  SIGKILLed with no chance to log. The **request** is what the scheduler
  reserves. For memory, set the request equal to the limit so a node never
  overcommits it.
- Diagnose a kill: `kubectl describe pod` (Last State: Terminated, Reason:
  OOMKilled, Exit Code: 137), `kubectl get events`, the cgroup's
  `memory.events` (`oom_kill`), `dmesg` on the node, or
  `docker inspect --format '{{.State.OOMKilled}}' <container>`. A 137
  without OOMKilled is another SIGKILL, such as a failed liveness probe.
- An out-of-memory error inside the runtime names the area that ran out:

  | Message | Area | First move |
  |---|---|---|
  | `JavaScript heap out of memory` (Node) | the V8 heap at `--max-old-space-size` | find the leak; raise the limit only for a live set that is legitimately larger |
  | `OutOfMemoryError: Java heap space` | the JVM heap | a heap dump in MAT |
  | `OutOfMemoryError: Metaspace` | class metadata | a class loader leak, generated classes |
  | `OutOfMemoryError: Direct buffer memory` | off-heap NIO buffers | buffers never released, `-XX:MaxDirectMemorySize` |
  | `unable to create native thread` | threads or a process limit | a thread pool without a bound |
  | `MemoryError` (Python), `runtime: out of memory` (Go) | the process could not allocate | peak RSS, streaming (section 4) |

- On the JVM add `-XX:+ExitOnOutOfMemoryError`, so a process that ran out
  exits and is restarted instead of limping on with broken threads.
- The heap is not the whole process. Set a heap-only limit (Node, the
  JVM) to about 60 to 75% of the container limit, leaving the rest for
  native memory, thread stacks, buffers and page cache. `GOMEMLIMIT`
  covers all memory the Go runtime manages, so it can sit at 80 to 90%.
- The runtime must know the limit. The JVM and .NET size their heaps from
  the cgroup limit; for Node and Go set it explicitly (section 7) rather
  than trust defaults; Python has no heap limit, so watch its RSS. Before
  Go 1.25, `GOMAXPROCS` also ignored CPU limits (automaxprocs fixed that).
- A restart schedule or gunicorn's `--max-requests` hides a leak. Use one
  only as a stopgap while the leak is found, and say so.

## 6. GC time and pauses

- Look at the collector first: `node --trace-gc` (a line per scavenge and
  mark-compact), `GODEBUG=gctrace=1` (heap sizes and GC CPU per cycle),
  JVM `-Xlog:gc*` or JFR, `dotnet-counters` (`% Time in GC`), Python's
  `gc.callbacks` for pauses of the cyclic collector.
- More than about 5 to 10% of CPU in GC, or pauses visible at p99, is
  worth fixing. The cause is nearly always the allocation rate or a heap
  too close to its limit, seldom the collector itself.
- Cut the allocation rate first (section 4): fewer temporary objects per
  request means fewer collections of every kind.
- Give the heap room: a live set near the limit makes the collector run
  back to back, so CPU climbs and throughput falls before the process
  dies. A heap of 2 to 4 times the live set (what survives a full
  collection) is a common starting point.
- Pauses: G1 aims at `-XX:MaxGCPauseMillis` (200ms by default); ZGC keeps
  pauses under a millisecond; Go's pauses are sub-millisecond by design,
  so its cost shows as CPU and allocation assists instead. On G1,
  leave the young generation to the pause target; in Node,
  `--max-semi-space-size` (MB) can cut scavenges in allocation-heavy
  services.

## 7. Runtime settings

| Runtime | Setting | Default and advice |
|---|---|---|
| Node | `--max-old-space-size=<MB>`, or in `NODE_OPTIONS` | set it in containers, about 75% of the limit (1536 for 2 GiB); Buffers sit outside it |
| JVM | `-XX:MaxRAMPercentage=75` | the default is 25% of the container's memory, which wastes most of it |
| JVM | the collector | G1 (default) for most services; ZGC (`-XX:+UseZGC`, generational by default since JDK 23) for sub-millisecond pauses on large heaps; Parallel for batch throughput |
| Go | `GOMEMLIMIT` (1.19+) | a soft limit at 80 to 90% of the container limit, such as `GOMEMLIMIT=900MiB` for 1 GiB |
| Go | `GOGC` (default 100) | higher trades memory for less GC CPU; `GOGC=off` with `GOMEMLIMIT` only for batch jobs allowed to fill the limit |
| Python (glibc) | `MALLOC_ARENA_MAX=2` | glibc allows up to 8 arenas per core in threaded processes; fewer often cut RSS markedly |
| Python | jemalloc through `LD_PRELOAD` | when fragmentation keeps RSS high after objects are freed |
| Python | `gc.freeze()` before forking workers | keeps copy-on-write pages shared in pre-fork servers |
| .NET | Server GC (default in ASP.NET Core) | adapts its heap count since .NET 9 (DATAS); the default heap limit is 75% of a container limit; `DOTNET_GCHeapHardLimitPercent` (hexadecimal) changes it; `System.GC.ConserveMemory` (0 to 9) trades CPU for less fragmentation |

Change one setting at a time and measure peak RSS, GC time and p99 latency
before and after (`performance`).

## Check it

- The same workload and measurement that showed the problem: the memory
  curve over a long run is flat, the snapshot comparison no longer grows
  by N, and peak RSS stays under the limit with headroom.
- Where it is cheap, a test guards it: goleak in Go tests, or a loop of
  10,000 operations asserting heap growth under a bound after a forced
  GC, with a margin generous enough not to flake.
- The report gives peak and steady-state RSS before and after, with the
  workload and its duration; the tests pass.

## Avoid

Raising the limit or scheduling restarts instead of finding the leak;
calling the GC by hand; watching the heap while buffers and native memory
grow; a heap limit equal to the container limit; the JVM's 25% default in a
container; unbounded maps, caches and label sets; listeners and timers
never removed; whole files or tables loaded into memory; object pools
without a measurement; heap dumps shared, kept or taken from the only
instance; a leak declared fixed without the same measurement.
