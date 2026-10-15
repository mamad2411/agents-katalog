---
name: rust-gpu-parallelism
description: >
  Use this skill when writing Rust code involving wgpu, WGSL compute shaders,
  Tokio async pipelines, GPU buffer management, SAM/ReBAR memory strategy,
  RDNA2/RDNA3 hardware constraints, or any architecture where Rust async and
  GPU compute must be reasoned about together. Triggers include: wgpu pipeline
  layout, WGSL workgroup design, buffer staging strategy, GPU-resident data
  architecture, Tokio task topology for hardware ingestion, crossbeam channel
  design for real-time pipelines, and any question about why Tokio is not
  C++ threading.
---

# Rust GPU Parallelism Skill

This skill encodes hard-won architectural knowledge for systems that combine
Rust async (Tokio) with wgpu GPU compute. It covers two distinct parallelism
models that must coexist without fighting each other, and the precise patterns
that make them cooperate.

---

## The Two Parallelism Models

### 1. Tokio — OS-Cooperative Async (CPU side)

Tokio is not a thread pool with a queue in front of it. It is a cooperative
scheduler that multiplexes many tasks onto a small number of OS threads using
`async/await` as the yield mechanism. The OS handles preemption at the task
boundary. The programmer handles cooperation at the `.await` point.

**What this means in practice:**
- An `.await` is a voluntary yield. The current task suspends, the scheduler
  runs something else, the task resumes when its future is ready.
- A blocking call inside an async task starves every other task on that thread.
  `std::thread::sleep`, synchronous file I/O, and synchronous USB reads are
  all blocking calls. They must be wrapped in `tokio::task::spawn_blocking`.
- Channel sends that never block (crossbeam `try_send`, `tokio::sync::mpsc`)
  are the right primitive for the ingestion hot path. A blocking channel
  send in a real-time callback is a latency spike.
- This is categorically different from C++ threading, where you manage thread
  lifetimes, mutexes, and condition variables manually. In Tokio you describe
  *what depends on what*, and the scheduler figures out *when*. The OS is
  the concurrency engine. You are not.

**The correct Tokio task topology for hardware ingestion:**

```
[Hardware interrupt / USB packet] → OS driver buffer
        │
        ▼  (cpal callback, runs on dedicated audio thread — not Tokio)
[crossbeam::channel::bounded] ← lock-free, never blocks the callback
        │
        ▼  (Tokio task: ingestion dispatcher)
[tokio::select! over all hardware channels]
        │ drains samples, forms RawIQPoint structs
        ▼
[wgpu queue.write_buffer()] ← SAM write, CPU → VRAM via PCIe 4.0
        │
        ▼  (Tokio task: GPU dispatch)
[wgpu::Queue::submit()] ← async, non-blocking from CPU perspective
```

Key: the cpal audio callback runs on a real-time thread managed by cpal,
NOT on Tokio. The boundary between cpal and Tokio is the crossbeam channel.
`crossbeam::channel::bounded` is the correct bridge — it is lock-free on
the send side when the channel has capacity, which is what the audio callback
requires. `tokio::sync::mpsc` is not appropriate here because it is not
safe to call from a non-Tokio thread without `try_send`.

**The three Tokio task categories in this system:**

```rust
// Category 1: Hardware ingesters — one per device
tokio::spawn(async move { ingest_rtlsdr(rx_channel).await });
tokio::spawn(async move { ingest_pluto(rx_channel).await });
tokio::spawn(async move { ingest_pico(rx_channel).await });

// Category 2: GPU dispatch — one, owns the wgpu Device
tokio::spawn(async move { gpu_dispatch_loop(device, queue, rx).await });

// Category 3: Corpus writer — one, append-only, fsync
tokio::spawn(async move { corpus_writer(rx).await });
```

Never share `wgpu::Device` across tasks without `Arc`. Never share
`wgpu::Queue` across tasks — it is internally synchronized but
concurrent submits from multiple tasks produce undefined ordering.
One task owns the queue. Others send work to it via channel.

---

### 2. wgpu + WGSL — Data Parallelism (GPU side)

The GPU executes thousands of threads simultaneously on independent data.
There are no yield points. There is no scheduler. A thread runs to
completion or it does not run.

**RDNA2/RDNA3 hardware constraint — the Wave64 mandate:**

```wgsl
@workgroup_size(64, 1, 1)
```

This is not a style choice. RDNA2 executes exactly 64-thread wavefronts.
A workgroup of 32 wastes half the execution width. A workgroup of 128
executes as two sequential wavefronts. 64 maps one workgroup to one
wavefront: maximum SIMD utilization, minimum scheduling overhead.

Every compute shader in this codebase uses `@workgroup_size(64, 1, 1)`.
No exceptions.

**Analytical phase computation — the pattern that eliminates inter-thread dependencies:**

```wgsl
// WRONG: sequential dependency — thread N needs thread N-1's output
var phase = initial_phase;
for (var i = 0u; i < frame_count; i++) {
    phase = (phase + phase_inc) % TAU;
    output[i] = amplitude * sin(phase);
}

// RIGHT: each thread computes its frame independently from frame_idx
@compute @workgroup_size(64, 1, 1)
fn synthesize(@builtin(global_invocation_id) gid: vec3<u32>) {
    let frame_idx = gid.x;
    let phase = (params.initial_phase + f32(frame_idx) * params.phase_inc) % TAU;
    output[frame_idx] = params.amplitude * sin(phase);
}
```

The key insight: if you can express the computation as a pure function of
the thread index, you have zero inter-thread dependencies and the GPU can
execute all threads simultaneously. This applies to synthesis, to the
freq_to_hue color operator, to particle attribute computation, and to
the anomaly score normalization pass.

**The 128-byte struct law — why it maps to hardware:**

RDNA2's Infinity Cache works on 128-byte cache lines. A struct that is
exactly 128 bytes guaranteed to be `align(128)` occupies exactly one cache
line. When the GPU fetches it, it fetches the entire struct in a single
transaction. A struct that straddles two cache lines requires two fetches.
At 100k+ particles per frame, that is 100k+ wasted memory transactions.

```rust
#[repr(C, align(128))]
pub struct FieldParticle { /* fields totaling exactly 128 bytes */ }
const _: () = assert!(std::mem::size_of::<FieldParticle>() == 128);
const _: () = assert!(std::mem::align_of::<FieldParticle>() == 128);
```

Every byte that is not a named field is a named reservation for a future
field. Anonymous padding (`_pad: [u8; 3]`) is forbidden. The name of
every byte is a contract.

**Structure of Arrays vs Array of Structures:**

For buffers with >10k elements:

```rust
// WRONG — Array of Structures: GPU reads full struct to get one field
// Cache thrashes when the shader only needs `energy` from each particle
struct ParticleBuffer { particles: array<FieldParticle> }

// RIGHT — Structure of Arrays: GPU reads only the fields it needs
// Energy pass reads a contiguous stream of f32 values
struct EnergyBuffer   { values: array<f32> }
struct FreqBuffer     { values: array<f32> }
struct PhaseBuffer    { values: array<f32> }
```

The exception: when a compute pass needs MOST fields of each struct,
AoS is appropriate. FieldParticle uses AoS because the render pass
reads almost every field. The sparse Laplacian pass uses SoA because
it reads only position and timestamp.

---

## The CPU→GPU Boundary — SAM and the Single-Cross Rule

Smart Access Memory (ReBAR) exposes the full GDDR6 address space to the
CPU via BAR registers on PCIe 4.0. The CPU can write directly into VRAM
without a staging buffer bounce.

```
Without SAM: CPU → DDR4 staging buffer → PCIe → GDDR6
With SAM:    CPU → PCIe → GDDR6 directly (~32 GB/s on PCIe 4.0 x16)
```

The single-cross rule: data crosses the CPU→GPU boundary exactly once.
After `queue.write_buffer()`, the data lives in GDDR6. It does not come
back to CPU RAM until a corpus write or a readback for debugging. Every
algorithm that touches the data runs on the GPU. The CPU submits compute
passes and moves on.

```rust
// The entire ingestion-to-GPU path:
let raw_points: Vec<RawIQPoint> = drain_channel(&rx);
let bytes = bytemuck::cast_slice(&raw_points);
queue.write_buffer(&gpu_input_buffer, 0, bytes); // SAM write — one cross
// raw_points is dropped here. The data now lives in VRAM.
queue.submit([encoder.finish()]);
// GPU now runs the Laplacian, Mamba, and particle formation passes
// entirely in VRAM at 384 GB/s internal bandwidth.
```

**Buffer sizing:** pre-allocate the maximum expected burst. Do not
reallocate GPU buffers on the hot path. `wgpu::BufferDescriptor` with
`mapped_at_creation: false` and `usage: BufferUsages::STORAGE | BufferUsages::COPY_DST`
is the standard pattern for GPU-resident signal buffers.

---

## wgpu v28 API Reference (Windows 11 / RDNA2)

These are the current correct patterns. Prior versions had different APIs;
do not restore removed fields.

```rust
// Instance
let instance = wgpu::Instance::new(&wgpu::InstanceDescriptor {  // & required
    backends: wgpu::Backends::VULKAN,
    ..Default::default()
});

// Device — no `experimental_features`, no `trace` field
let (device, queue) = adapter.request_device(
    &wgpu::DeviceDescriptor {
        label: Some("synesthesia"),
        required_features: wgpu::Features::empty(), // COMPUTE_SHADER removed
        required_limits: wgpu::Limits::default(),
        memory_hints: wgpu::MemoryHints::Performance,
    },
    None,
).await?;

// Pipeline layout — no `push_constant_ranges` field
let layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
    label: Some("laplacian"),
    bind_group_layouts: &[&bgl],
    // push_constant_ranges field does not exist in wgpu 28
});

// Poll — Maintain::Wait is the correct variant
device.poll(wgpu::Maintain::Wait);
// panic_on_timeout() does not exist in wgpu 28 — remove all calls
```

---

## WGSL Sparse Matrix Patterns (Space-Time Laplacian)

The Laplacian eigenvector computation uses CSR-format sparse matrices.
This is the correct storage layout for GPU SpMV (sparse matrix-vector
multiply):

```wgsl
// Bindings
@group(0) @binding(0) var<storage, read>       row_ptr:  array<u32>;   // n+1 entries
@group(0) @binding(1) var<storage, read>       col_idx:  array<u32>;   // nnz entries
@group(0) @binding(2) var<storage, read>       values:   array<f32>;   // nnz entries
@group(0) @binding(3) var<storage, read>       x_vec:    array<f32>;   // n entries
@group(0) @binding(4) var<storage, read_write> y_vec:    array<f32>;   // n entries

// SpMV kernel — one thread per row
@compute @workgroup_size(64, 1, 1)
fn spmv(@builtin(global_invocation_id) gid: vec3<u32>) {
    let row = gid.x;
    if row >= arrayLength(&row_ptr) - 1u { return; }

    let start = row_ptr[row];
    let end   = row_ptr[row + 1u];
    var sum   = 0.0f;
    for (var j = start; j < end; j++) {
        sum += values[j] * x_vec[col_idx[j]];
    }
    y_vec[row] = sum;
}
```

Power iteration for eigenvalue extraction (10 steps is sufficient for
4 eigenvectors per SI-Mamba ablation data):

```wgsl
// Rayleigh quotient iteration — converges in ~10 steps
// Run as separate compute pass after each SpMV
@compute @workgroup_size(64, 1, 1)
fn normalize(@builtin(global_invocation_id) gid: vec3<u32>) {
    // subgroup reduce for norm — requires subgroup ops extension
    // fallback: two-pass reduction with atomic add into shared memory
}
```

Gram-Schmidt orthogonalization runs after all 4 eigenvectors converge.
It is a separate compute pass, not part of the SpMV loop.

---

## AtomicF32 — The Only Correct Pattern

`std::sync::atomic::AtomicF32` does not exist in stable Rust.
The correct implementation via bit reinterpretation:

```rust
// src/utils/atomic.rs — only AtomicF32 in the codebase
use std::sync::atomic::{AtomicU32, Ordering};

pub struct AtomicF32(AtomicU32);

impl AtomicF32 {
    pub fn new(v: f32) -> Self {
        Self(AtomicU32::new(v.to_bits()))
    }
    pub fn load(&self, ord: Ordering) -> f32 {
        f32::from_bits(self.0.load(ord))
    }
    pub fn store(&self, v: f32, ord: Ordering) {
        self.0.store(v.to_bits(), ord)
    }
}
```

NaN bit patterns are preserved across the round-trip. This is intentional:
a NaN in a forensic field is a diagnostic signal, not an error to mask.

---

## Common Mistakes and Their Fixes

| Mistake | Why it's wrong | Fix |
|---------|---------------|-----|
| `@workgroup_size(32, 1, 1)` | Half-width wavefront on RDNA2 | `@workgroup_size(64, 1, 1)` |
| FFT at ingestion | Destroys information the model should learn | FFT only downstream of inference |
| `std::thread::sleep` in async task | Blocks the Tokio thread | `tokio::time::sleep` |
| Blocking channel send in cpal callback | Latency spike, possible dropout | `crossbeam::channel::try_send` |
| Anonymous `_pad` fields | Contract violation, build fails | Named reservations for future tracks |
| Sharing `wgpu::Queue` across tasks | Undefined submit ordering | One task owns the queue |
| `queue.write_buffer` in a loop | Multiple PCIe crossings | Batch into one write per dispatch |
| `clone()` on `FieldParticle` in hot path | 128-byte copy × particle_count | Pass references, use GPU-resident buffers |
| `push_constant_ranges` in wgpu 28 | Field removed from API | Delete the field |
| `wgpu::Features::COMPUTE_SHADER` | Feature removed, now default | Delete the reference |
| Restoring deleted types | Re-introduces dead architecture | Implement against current masterplan |

---

## Physical Constants (Never Learned Parameters)

```rust
pub const SPEED_OF_LIGHT_M_S:    f64 = 299_792_458.0;
pub const PLUTO_BASELINE_M:       f32 = 0.012;       // ~12mm — measure and confirm
pub const PICO_CLOCK_HZ:          u32 = 150_000_000;
pub const F_MIN_HZ:               f32 = 1.0;
pub const F_MAX_HZ:               f32 = 700e12;
pub const LOG_RANGE:              f32 = 33.18;        // log(F_MAX / F_MIN)
pub const POWERLINE_HZ:           f32 = 60.0;
pub const OV9281_FPS:             u32 = 120;
pub const OV9281_FRAME_PERIOD_MS: f32 = 8.333;
pub const REALTEK_ANTIALIAS_KHZ:  f32 = 85.0;        // approximate midpoint
pub const COIL_INDUCTANCE_KHZ:    f32 = 50.0;        // upper band limit
pub const KNN_K:                  usize = 20;         // SI-Mamba ablation optimum
pub const LAPLACIAN_EIGENVECS:    usize = 4;          // SI-Mamba ablation optimum
pub const PARTICLE_STRUCT_BYTES:  usize = 128;
pub const WAVEFRONT_WIDTH:        usize = 64;         // RDNA2/RDNA3 hardware
```

These are not configuration. They are physics and ruler measurements.
No model output overrides them.
