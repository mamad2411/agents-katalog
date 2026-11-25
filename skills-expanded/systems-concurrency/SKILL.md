---
name: systems-concurrency
description: "Concurrency without data races or deadlocks: choosing threads, message passing or async, shared state and its locks, lock ordering and contention, atomics and memory ordering, condition variables, thread pools, async runtimes with cancellation and backpressure, bounded queues, and testing with loom, TSan and stress tests. Read before writing code that runs things at the same time."
---

# Concurrency without races or deadlocks

The default version: a thread per request, one `Arc<Mutex<State>>` locked
around a network call, `sleep(100ms)` to "wait for the other thread", an
unbounded channel that grows until the process is killed, an `Ordering`
copied from a blog post, and a test that passed once. This skill is how to
choose the model, share state safely, bound every queue, stop cleanly and
prove it with tools. Rust detail in `systems-rust`, false sharing and
layout in `systems-memory`.

## 1. Choose the model

| Work | Model | Rust | C++ |
|---|---|---|---|
| CPU-bound, data-parallel | a fixed pool, one thread per core | rayon | a pool of `std::jthread`, TBB, OpenMP |
| Many waits on I/O (thousands of sockets) | an async runtime | tokio | Asio, C++20 coroutines |
| Stages that hand work along | threads or tasks joined by bounded queues | `crossbeam-channel`, `tokio::sync::mpsc` | a mutex, a deque and two condition variables |
| A few blocking calls inside async code | a separate blocking pool | `spawn_blocking` | a dedicated pool |
| Read-mostly shared data | an immutable snapshot swapped whole | `arc-swap` | `shared_ptr<const T>` swapped under a mutex |

Order of preference: transfer ownership through a channel; share
immutable data (`Arc<T>`, `const` after construction); share mutable data
behind a lock; atomics; lock-free structures last, from a library.

## 2. Data races and race conditions

- A data race is two threads touching the same memory without
  synchronisation, at least one writing: undefined behaviour in C, C++ and
  unsafe Rust, impossible in safe Rust.
- A race condition is a logic error in the order of events, and no
  language prevents it: check-then-act (`if !map.contains_key(k) {
  map.insert(k, v) }` across two lock scopes), read-modify-write split
  over two critical sections, a file checked and then opened (TOCTOU).
- Fix it by making the compound action one step: one lock scope, the
  map's `entry()` API, `compare_exchange`, `fetch_add`, `create_new` /
  `O_EXCL` for files.

## 3. Locks

- Hold a lock for the shortest time: compute outside, lock, mutate,
  unlock. Never hold one across I/O, a channel send that can block, a
  callback into unknown code, or an `.await`:

```rust
let batch = {
    let mut state = shared.lock().expect("state lock poisoned");
    std::mem::take(&mut state.pending)
}; // guard dropped here, before the slow part
send_all(&batch).await?;
```

- Lock ordering prevents deadlock: code that holds two locks takes them in
  one documented order (by level: `registry` before `session`; by id for
  two of the same kind). C++ `std::scoped_lock lock(a, b);` takes several
  without deadlock; Rust has no equivalent, so order them or restructure
  until one lock suffices.
- `RwLock` only when reads dominate and a measurement shows the mutex
  contends: an uncontended mutex is cheaper, and writers can starve
  (fairness varies by platform).
- A panic while holding a Rust std lock poisons it, and `expect` on the
  next `lock()` passes the failure on (`parking_lot` does not poison).
  Locking a non-recursive mutex twice on one thread deadlocks: restructure
  rather than reach for a recursive mutex.

## 4. Contention

Symptoms: time in `pthread_mutex_lock`, `futex` or `lock_slow` frames in
the profile; throughput that stops rising as threads are added.

- Shard: N locks over N partitions chosen by key hash (N a power of two,
  about 4 times the thread count), or a concurrent map (`dashmap`,
  `papaya`; never hold a `dashmap` reference while touching the same map).
- Batch (lock once per batch, not per item); keep per-thread state and
  merge at the end (thread-local counters, rayon's `fold` then `reduce`).
- Read-copy-update for read-mostly data: readers load an `Arc` snapshot,
  a writer builds a new version and swaps it in.
- Pad per-thread hot counters to 128 bytes to stop false sharing
  (`CachePadded`, `systems-memory`).

## 5. Atomics and memory ordering

| Ordering | Guarantees | Use for |
|---|---|---|
| `Relaxed` | atomicity only, no ordering with other memory | statistics counters, unique ids from `fetch_add` |
| `Release` store, `Acquire` load | writes before the release are visible after an acquire that reads it | publishing data behind a flag or pointer |
| `AcqRel` | both, on a read-modify-write | `compare_exchange` or `fetch_sub` that consumes and publishes |
| `SeqCst` | one total order over all `SeqCst` operations | several flags every thread must see in the same order; the default when unsure |

```rust
static VALUE: AtomicU64 = AtomicU64::new(0);
static READY: AtomicBool = AtomicBool::new(false);

// Writer
VALUE.store(42, Ordering::Relaxed);
READY.store(true, Ordering::Release); // publishes the store above
// Reader
if READY.load(Ordering::Acquire) {
    assert_eq!(VALUE.load(Ordering::Relaxed), 42); // guaranteed by the pair
}
```

- `SeqCst` does not fix a wrong algorithm. Anything weaker needs its proof
  in a comment, and x86 hides ordering bugs that Arm shows: test on Arm
  (Apple silicon, Graviton) and under loom.
- A flag and a separate value are two atomics: a reader can see one new
  and one old unless the ordering links them. Pack them into one word or
  use a lock.
- Do not write your own lock-free queue, stack or reference count: ABA,
  memory reclamation (epochs, hazard pointers) and ordering make them hard
  to get right. Use `crossbeam`, `Arc`, or a lock, and measure first.
- C++ `std::atomic<T>` with `std::memory_order_*` has the same semantics;
  C11 has `<stdatomic.h>`. `volatile` is not synchronisation in any of them.

## 6. Condition variables

Wait on a predicate (spurious wake-ups happen), with the predicate's state
under the same mutex; change the state, then notify.

```rust
let (lock, cvar) = &*shared; // Arc<(Mutex<State>, Condvar)>
let mut state = cvar
    .wait_while(lock.lock().expect("queue poisoned"), |s| s.items.is_empty() && !s.closed)
    .expect("queue poisoned");
let job = state.items.pop_front(); // None: closed and drained
```

```cpp
std::unique_lock lock(mutex_);
cv_.wait(lock, [&] { return !queue_.empty() || closed_; });
```

`notify_one` per item, `notify_all` for shutdown; a bounded queue needs
two conditions (not empty, not full). A channel is usually the better tool.

## 7. Threads and pools

- CPU-bound pools sized to the cores available:
  `std::thread::available_parallelism()` (on Linux it honours affinity
  and cgroup CPU quotas), `std::thread::hardware_concurrency()` in C++.
  More threads than cores only adds switching.
- Blocking I/O gets its own, larger pool (tens to hundreds) so it never
  starves the CPU pool; tokio's blocking pool caps at 512 threads.
- No thread per request without a bound. Every thread is joined or owned
  by a scope (`std::thread::scope`; C++ `std::jthread` joins in its
  destructor); a detached thread is a leak and an unobserved panic. Name
  threads (`thread::Builder::new().name("wal-writer".into())`) for dumps.

## 8. Async: cooperative, cancellable, bounded

- Tasks yield only at `.await`. A task that computes for more than about
  100 microseconds between awaits, or calls anything blocking (`std::fs`,
  `thread::sleep`, a synchronous client, a long-held blocking lock), stalls
  every task on its worker: move that work to `spawn_blocking` or a CPU
  pool.
- Cancellation happens at any `.await`: the future is dropped and the
  rest never runs. Keep state consistent at every await point and use
  cancel-safe operations in `select!` (`systems-rust`, section 6).
- Structured concurrency: every task has an owner that awaits or cancels
  it (`JoinSet`, `TaskTracker`, Go's `errgroup`, Kotlin scopes); shutdown
  cancels the tree through one token and waits with a deadline.
- Backpressure is a decision per queue: when full, block the producer
  (`send().await` on `mpsc::channel(1024)`), drop the oldest, or reject
  (`try_send`, answered with HTTP 429 or 503). A `Semaphore` caps use of a
  resource; `buffer_unordered(16)` caps a stream's concurrency.
- A timeout on every external call, and on waiting for a lock or permit
  that another component controls.

## 9. Deadlock, livelock, starvation

- Deadlock: threads wait on each other forever. Dump every thread's stack
  and look for two holding what the other wants:

```sh
gdb -p <pid> -batch -ex 'thread apply all bt'   # Linux
lldb -p <pid> --batch -o 'bt all'                # macOS
jstack <pid>                                     # JVM
kill -QUIT <pid>                                 # Go prints every goroutine and exits
```

- `parking_lot`'s `deadlock_detection` feature reports lock cycles;
  tokio-console (`console-subscriber`, `RUSTFLAGS="--cfg tokio_unstable"`)
  shows tasks that never wake.
- Livelock: threads retry and back off in step (two `try_lock` loops):
  jitter the backoff or order the locks. Starvation: a writer that never
  gets an `RwLock`, a task that never runs, one hot shard: fair locks,
  bounded batches, wait times measured.

## 10. Write down who owns what

- For each shared structure: which lock guards which fields, which thread
  owns which resource, the lock order, and what may block. In Rust the
  type says it (`Mutex<Inner>` wraps exactly the guarded fields).
- C and C++: Clang's thread-safety analysis checks the comments. Annotate
  with `GUARDED_BY(mu)`, `REQUIRES(mu)`, `ACQUIRE()` (or Abseil's
  `ABSL_GUARDED_BY`) and build with `-Wthread-safety`.

## 11. Test it

loom runs a small model under every interleaving it can reach, with many
weak-memory outcomes (it treats `SeqCst` as `AcqRel`). Swap the types in
by cfg, keep models to two or three threads:

```rust
// src/sync.rs: the library imports these, so loom can replace them.
#[cfg(loom)]
pub(crate) use loom::sync::{atomic::{AtomicUsize, Ordering}, Arc};
#[cfg(not(loom))]
pub(crate) use std::sync::{atomic::{AtomicUsize, Ordering}, Arc};

#[cfg(loom)]
#[test]
fn counter_is_exact() {
    loom::model(|| {
        let n = Arc::new(AtomicUsize::new(0));
        let a = { let n = n.clone(); loom::thread::spawn(move || n.fetch_add(1, Ordering::Relaxed)) };
        let b = { let n = n.clone(); loom::thread::spawn(move || n.fetch_add(1, Ordering::Relaxed)) };
        a.join().unwrap();
        b.join().unwrap();
        assert_eq!(n.load(Ordering::Relaxed), 2);
    });
}
```

```sh
RUSTFLAGS="--cfg loom" cargo test --release --lib counter_is_exact
LOOM_MAX_PREEMPTIONS=3 RUSTFLAGS="--cfg loom" cargo test --release   # bound big models
```

loom goes under `[target.'cfg(loom)'.dependencies]`; `unexpected_cfgs =
{ level = "warn", check-cfg = ["cfg(loom)"] }` in `[lints.rust]` declares
the cfg.

- ThreadSanitizer: `-fsanitize=thread` in C and C++; Rust nightly
  `RUSTFLAGS="-Zsanitizer=thread" cargo +nightly test -Zbuild-std --target
  x86_64-unknown-linux-gnu`; Go `go test -race`. It sees only the
  interleavings that happen, so pair it with stress: the test thousands
  of times, more threads than cores, on Arm and x86
  (`for i in $(seq 500); do cargo test -q concurrent || break; done`).
- Randomised and deterministic schedulers: `shuttle` for programs too big
  for loom; `turmoil` or `madsim` to simulate networked async code with a
  seed that replays a failure.
- Never order events in a test with `sleep`: use a barrier, a channel or
  a latch.

## 12. Other languages, briefly

- Go: goroutines and channels, `context.Context` deadlines on every call,
  `errgroup.WithContext`, `go test -race` in CI; since Go 1.25 GOMAXPROCS
  follows the container's CPU limit.
- Java: sized `ExecutorService` pools, virtual threads (21+) for blocking
  I/O at scale, `java.util.concurrent`, jcstress for memory-model tests.
- C++20: `std::jthread` with `std::stop_token`, `std::latch`,
  `std::barrier`, `std::counting_semaphore`; Asio or coroutines for I/O.

## Check it

- The design is written down: threads or tasks, owners, lock order,
  queue bounds and what happens when full, the shutdown path and its
  deadline.
- `bash`: loom models, a TSan build and a stress loop pass; where TSan
  cannot run here (Rust TSan needs nightly), say so and run the stress loop.
- A shutdown test: start, load, signal, and assert everything stopped
  inside the deadline with no lost or duplicated work.
- Under load, the profile shows no lock in the top frames, or the one
  there is accepted and explained.

## Avoid

A thread per request; locks held across I/O, callbacks or `.await`; two
locks taken in different orders; `RwLock` by reflex; check-then-act across
two lock scopes; hand-written lock-free structures; orderings weaker than
`SeqCst` without a written proof; `volatile` as synchronisation; unbounded
channels and queues; blocking calls on an async runtime; tasks and threads
nobody owns or joins; `sleep` as synchronisation in code or tests;
concurrency tested once on x86 and called done.
