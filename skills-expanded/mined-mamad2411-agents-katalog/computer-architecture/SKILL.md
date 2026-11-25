-----

## name: computer-architecture
description: >
  Expert computer architecture assistant for hardware engineers and system designers. Use this skill whenever the user needs:
  help with CPU design, memory hierarchy, instruction set architecture, performance optimization, or understanding
  modern processor implementations. Includes both theoretical foundations and practical design guidance.
trigger: Any computer architecture problem - from ISA design to microarchitecture to performance analysis.
license: MIT
compatibility: opencode
metadata:
  audience: engineers
  category: computer-science

# Computer Architecture — Processors, Memory, and Performance

Covers: **Instruction Sets · Microarchitecture · Pipelining · Memory Systems · Performance · Parallelism**

-----

## Instruction Set Architecture (ISA)

### What is an ISA?

The ISA defines the interface between software and hardware:
- Instruction format and encoding
- Registers and addressing modes
- Data types and sizes
- Memory model and alignment
- Exception/interrupt handling

### RISC vs. CISC

| Characteristic | RISC | CISC |
|---------------|------|------|
| Instruction size | Fixed (32-bit) | Variable |
| Instructions/cycle | Simple, few | Complex, many |
| Memory operations | Load/store only | Direct memory access |
| Registers | Many (32+) | Few |
| Microcode | Minimal | Extensive |
| Examples | ARM, RISC-V, MIPS | x86, VAX |

### Register File Design

**Number of registers**: Balance between encoding space and register pressure.
**Read/write ports**: Affects issue width and pipeline depth.
**Physical vs. Logical**: Rename table maps logical to physical.

### Addressing Modes

| Mode | Example | Meaning |
|------|---------|---------|
| Immediate | addi $t0, $t1, 42 | Constant value |
| Register | add $t0, $t1, $t2 | Register contents |
| Base+offset | lw $t0, 0($t1) | Memory at address |
| PC-relative | beq $t0, $t1, label | Branch offset |
| Register indirect | lw $t0, 0($t1) | Address in register |

### Instruction Categories

- **Data transfer**: lw, sw, mov
- **Arithmetic/logical**: add, sub, and, or, xor
- **Control flow**: beq, j, jal, jr
- **Floating-point**: add.s, mul.d
- **SIMD**: vadd, vmul (vector instructions)

### Endianness

- **Little-endian**: Least significant byte at lowest address (x86, ARM)
- **Big-endian**: Most significant byte at lowest address (network order)

### Alignment Requirements

- Word-aligned: addresses multiple of 4
- Cache line alignment: typically 64 bytes
- Unaligned access may be slower or illegal

### Common ISAs

| ISA | Vendor | Use |
|-----|--------|-----|
| x86-64 | Intel, AMD | Desktop, server |
| ARM64 (AArch64) | Apple, Qualcomm | Mobile, Apple Silicon |
| RISC-V | Open | Research, embedded |
| MIPS | Deprecated | Historical |

-----

## Microarchitecture

### Single-Cycle Datapath

All operations complete in one cycle:
- Simple control unit
- Long cycle time
- Low clock frequency

### Multi-Cycle Implementation

Break instruction into steps:
- IF, ID, EX, MEM, WB
- Higher clock frequency
- More complex control

### Pipelining Basics

Overlap instruction execution stages:
- Throughput increases
- Latency unchanged
- Must handle hazards

### Classic 5-Stage Pipeline (MIPS)

| Stage | Function |
|-------|----------|
| IF | Instruction fetch |
| ID | Instruction decode + register read |
| EX | Execute / ALU operation |
| MEM | Memory access |
| WB | Write back to register |

### Pipeline Hazards

**Structural hazards**: Hardware cannot support all combinations.
- Solution: Duplicate resources, stall

**Data hazards**: Instruction depends on previous.
- RAW (read after write) — true dependence
- WAR (write after read) — anti-dependence
- WAW (write after write) — output dependence
- Solution: Forwarding, stall, scheduling

**Control hazards**: Branch outcome unknown.
- Solution: Branch prediction, delay slots

### Branch Prediction

| Type | Description |
|------|-------------|
| Static | Always taken or not |
| 1-bit | Toggle on mispredict |
| 2-bit | Two-bit saturating counter |
| Two-level | History + pattern table |
| BTB | Branch target buffer |
| Return address stack | Predict return addresses |

### Branch Target Buffer (BTB)

Cache of recent branch addresses and targets:
- Index by PC
- Store predicted PC
- Update on mispredict

### Out-of-Order Execution

Execute instructions when operands ready:
- Scoreboard tracks dependencies
- Register renaming eliminates WAR/WAW
- Reorder buffer (ROB) maintains in-order commit

### Register Renaming

Map logical registers to physical:
- Avoids WAR/WAW hazards
- Enables out-of-order
- Map table maintained dynamically

### Superscalar

Multiple instructions per cycle:
- Issue width: number of instructions
- Execution units duplicated
- Complexity increases exponentially

### Very Long Instruction Word (VLIW)

Compiler schedules instructions:
- Explicit parallelism
- Hardware simpler
- Compiler complexity

### SIMD Extensions

Single instruction, multiple data:
- SSE/AVX (x86): 128/256/512-bit vectors
- NEON (ARM): 128-bit vectors
- Operate on arrays of data

-----

## Memory Hierarchy

### Memory Technology

| Type | Access Time | Size | Volatile |
|------|-------------|------|----------|
| SRAM | ~1 ns | MB | Yes |
| DRAM | ~100 ns | GB | Yes |
| Flash | ~μs | GB | No |
| Disk | ~ms | TB | No |

### Cache Organization

**Associativity**: Number of ways
- Direct-mapped: 1-way
- Set-associative: 2, 4, 8, 16-way
- Fully-associative: all ways

### Cache Performance

```
AMAT = Hit time + Miss rate × Miss penalty
```

### Cache Miss Types

| Type | Cause | Solution |
|------|-------|----------|
| Compulsory | First access | Prefetching |
| Capacity | Working set > cache | Increase size |
| Conflict | Too many to same set | Increase associativity |

### Write Policies

**Write-through**: Update memory on every write.
- Simple, coherent
- Slow writes

**Write-back**: Update memory on eviction.
- Fast writes
- Complex coherence

### Write Miss Policies

**Allocate on write miss**: Load block first.
**No-allocate**: Write directly to memory.

### Cache Coherence

**MESI Protocol** states:
- Modified: Exclusive, dirty
- Exclusive: Clean, only in this cache
- Shared: Clean, possibly elsewhere
- Invalid: Not present

### Virtual Memory

Process gets virtual address space:
- Page table maps VA to PA
- TLB caches recent translations
- Page fault if not resident

### Translation Lookaside Buffer (TLB)

Cache of page table entries:
- Fully-associative or set-associative
- Typically 32-512 entries
- Miss penalty: page table walk

### Page Table

Hierarchical or inverted:
- Multi-level page table common
- Each level adds lookup time

### Memory Management Unit (MMU)

Hardware that performs address translation:
- Walks page table
- Updates TLB
- Handles protection

-----

## Performance Analysis

### Amdahl's Law

Speedup limited by serial portion:
```
S = 1 / [(1 - f) + f/k]
```

f = parallel fraction, k = number of processors

### CPI Equation

```
CPI = Σ (CPI_i × Frequency_i)
```

### Execution Time

```
Time = Instruction count × CPI × Clock cycle time
```

### Speedup Calculation

```
Speedup = Old time / New time
```

### Benchmarks

| Type | Description | Examples |
|------|-------------|----------|
| Micro | Individual operations | Dhrystone |
| Kernel | Critical loops | Livermore loops |
| Synthetic | Mix of operations | Whetstone |
| Full | Real applications | SPEC CPU |

### SPEC Benchmark

Standard Performance Evaluation Corporation:
- SPEC CPU2006, CPU2017: CPU-intensive
- SPEC power: Power consumption
- SPEC viewperf: Graphics

### Roofline Model

Performance bound by memory bandwidth or compute:
```
Performance = min(Peak FLOPS, Peak I/O × Arithmetic intensity)
```

### Performance Counters

Hardware counters measure:
- Cache misses
- Branch mispredictions
- Pipeline stalls
- Cache hits

### Profiling

- Hardware events sampled
- Attribution to code
- Hotspot identification

### Optimization Priorities

1. Algorithm choice
2. Data structures
3. Memory layout
4. Compiler flags
5. Intrinsics/assembly

-----

## Parallel Processing

### Flynn's Taxonomy

| Category | Single/Multiple | Instruction/Data |
|----------|-----------------|------------------|
| SISD | Single | Single |
| SIMD | Single | Multiple |
| MISD | Multiple | Single |
| MIMD | Multiple | Multiple |

### Multicore

Multiple processor cores on chip:
- Share cache (L3) or private
- Coherence maintained
- Amdahl's law applies

### Symmetric Multiprocessing (SMP)

Shared memory, multiple CPUs:
- All CPUs equal
- Cache coherent
- Bus or interconnect

### Non-Uniform Memory Access (NUMA)

Memory access time depends on location:
- Multi-socket systems
- Local vs. remote memory
- Data locality important

### Graphics Processing Units (GPUs)

Massive parallelism:
- Thousands of small cores
- SIMT: single instruction multiple thread
- High memory bandwidth
- Good for data parallel

### Heterogeneous Computing

Combine different processor types:
- CPU + GPU
- CPU + FPGA
- CPU + ASIC

### Interconnects

| Type | Bandwidth | Latency |
|------|-----------|---------|
| PCIe | ~32 GB/s | ~μs |
| QPI/UPI | ~20 GB/s | ~100 ns |
| Ethernet | ~100 Gb/s | ~μs |
| Infiniband | ~200 Gb/s | ~μs |

### Synchronization

**Locks**: Mutual exclusion
**Barriers**: Wait for all threads
**Atomics**: Lock-free operations

### Memory Consistency

- Sequential consistency: default, slow
- Release consistency: better performance
- Weak ordering: most efficient

-----

## ISA Examples

### x86-64

Complex CISC with variable length:
- 1-15 bytes per instruction
- Legacy complexity
- Extensions: SSE, AVX, AVX-512

### ARM64 (AArch64)

Clean 64-bit RISC:
- Fixed 32-bit instructions
- 31 general-purpose registers
- SIMD: NEON, SVE

### RISC-V

Open source ISA:
- Base + extensions
- 32-bit and 64-bit
- RV32GC, RV64GC

### Vector Extensions

| ISA | Vector Width |
|-----|-------------|
| AVX-512 | 512-bit |
| SVE | Variable (up to 2048) |
| RVV | Variable |

-----

## Low-Power Design

### Power Consumption

```
P = P_static + P_dynamic
P_dynamic = CV²f + P_shorting
```

### Dynamic Voltage and Frequency Scaling (DVFS)

Reduce V and f to save power:
- Power ∝ V² × f
- Slow down when idle

### Clock Gating

Disable clock to unused logic:
- Reduces dynamic power
- No switching

### Power Gating

Turn off power to unused blocks:
- Eliminates static power
- State may be lost

### Dark Silicon

Cannot power all transistors simultaneously:
- Partition chip into regions
- Time-share active areas

### Near-Threshold Computing

Operate at low V (near V_t):
- Energy efficient
- Slower, more variation

### Approximate Computing

Relax accuracy requirements:
- Error-tolerant applications
- Energy savings

-----

## Hardware Security

### Side Channels

Exploit physical emanations:
- Power analysis
- Timing analysis
- Electromagnetic analysis

### Spectre/Meltdown

Speculative execution leaks data:
- Branch prediction + cache
- Fixed with microcode, software

### Speculation Control

- Indirect branch prediction hardening
- Retpoline
- Hardware fixes

### Secure Enclaves

Isolated execution regions:
- Intel SGX, ARM TrustZone
- Encrypted memory

### Hardware Roots of Trust

Secure boot, measured boot:
- TPM, secure bootrom
- Immutable

-----

## Emerging Architectures

### Domain-Specific Architectures

Customize for workload:
- DNN accelerators
- Network processors
- Crypto ASICs

### In-Memory Computing

Process near memory:
- Reduce data movement
- New memory technologies

### Neuromorphic Computing

Brain-inspired:
- Spiking neural networks
- Event-driven

### Quantum Computing

Quantum bits (qubits):
- Superposition, entanglement
- Algorithm-specific speedups

### Chiplets

Multiple dies in package:
- Heterogeneous integration
- Flexible, cost-effective

-----

## Common Errors to Avoid

- Confusing ISA with microarchitecture
- Ignoring memory hierarchy effects
- Underestimating branch misprediction cost
- Not considering data alignment
- Misapplying Amdahl's law
- Ignoring cache coherency overhead
- Confusing throughput and latency
- Forgetting memory consistency issues
- Not accounting for off-chip bandwidth
- Underestimating power/thermal limits

-----

## Key References

- **Computer Organization and Design** by Patterson & Hennessy — Classic text
- **Computer Architecture: A Quantitative Approach** — Advanced
- **Modern Processor Design** — Microarchitecture
- **Digital Design and Computer Architecture** — RTL to layout

