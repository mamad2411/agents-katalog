# Master's Thesis Repository Instructions

This repository contains research, implementations, infrastructure,
experiments, data-analysis tooling, and thesis materials for the master's thesis:

**Analiza porównawcza wydajności technologii WebAssembly, konteneryzacji i wirtualizacji w realizacji funkcji sieciowych**

**Comparative analysis of the performance of WebAssembly, containerization, and virtualization technologies in implementing network functions**

## Primary objective

The objective of the project is to experimentally compare three execution technologies:

1. WebAssembly
2. containers
3. virtual machines

in the implementation of selected network functions.

The initial network functions are:

- stateless Layer 4 virtual firewall (`vFW`)
- simple round-robin Layer 4 virtual load balancer (`vLB`)

The primary metrics are:

- latency
- throughput
- CPU utilization
- memory utilization
- startup time
- scalability

## Repository knowledge

Before making significant architectural, experimental, or implementation changes,
read the relevant documentation.

Before implementing a major subsystem, check `docs/decisions.md` and the relevant
design documents. Proposed decisions must not be silently promoted to accepted decisions.

Important files:

- `docs/thesis.md` — thesis overview and motivation
- `docs/scope.md` — project boundaries
- `docs/research.md` — research questions and hypotheses
- `docs/architecture.md` — experimental environment architecture
- `docs/methodology.md` — benchmarking and experimental methodology
- `docs/experimental-framework.md` — automation and orchestration design
- `docs/decisions.md` — important project and research decisions
- `docs/literature.md` — literature notes and source tracking
- `docs/glossary.md` — terminology used in the project

## General rules

### Research integrity

Treat this as an academic research repository.

Never:

- fabricate citations,
- fabricate benchmark results,
- invent experimental data,
- present assumptions as measured results,
- silently remove unsuccessful experiments,
- alter raw benchmark data manually.

Clearly distinguish between:

- measured facts,
- literature findings,
- assumptions,
- hypotheses,
- interpretations.

### Reproducibility

Reproducibility is a primary requirement.

Whenever experiments are introduced, they should eventually record enough information
to reproduce a run, including where applicable:

- Git commit,
- timestamp,
- hardware,
- operating system,
- kernel version,
- runtime version,
- compiler version,
- implementation version,
- benchmark configuration,
- traffic parameters,
- measurement duration,
- warm-up duration,
- number of repetitions.

Experiment execution must be fully automated by `mt`. Record cooldown, repetition,
traffic profile, resource allocation, and experiment order as well. Use active readiness
probes and identical traffic definitions across execution environments. Record the Git
commit for every campaign/run; a clean-working-tree requirement for final measurements
is proposed. Raw data must remain immutable.

### Scope discipline

Do not expand the thesis scope without explicitly documenting the proposal.

Before introducing major technologies or research dimensions such as:

- Kubernetes,
- distributed orchestration,
- service mesh,
- eBPF,
- DPDK,
- multiple WebAssembly runtimes,
- multiple programming languages,
- public cloud deployments,
- multi-node clusters,

check `docs/scope.md` and `docs/decisions.md`. The accepted Rust VNF and Clojure
orchestrator/backend roles are intentional; additional VNF languages remain optional.

If something is outside the current scope, propose it first instead of implementing it immediately.

### Experimental fairness

The comparison between WebAssembly, containers, and virtual machines must be as fair as possible.

The implementations should aim to provide equivalent network-function behavior.

Avoid introducing unnecessary differences between variants.

When equivalence cannot be achieved, document the difference and explain its likely impact.

### Raw data

Once benchmark data is introduced:

- raw measurement files must be immutable,
- processed data must be stored separately,
- plots and statistics must be generated from scripts,
- manual editing of measurements is not allowed.

### Documentation

Important design or methodology decisions should be recorded in:

`docs/decisions.md`

Do not allow important decisions to exist only in source code or chat history.

### Citations

Never invent bibliographic information.

When a source has not been verified, mark it as:

`TODO: verify source`

instead of constructing a citation from memory.

### Language

Repository technical documentation should normally be written in English.

The final thesis itself may be written in Polish.

Use precise technical terminology.

Prefer the terms:

- WebAssembly technology
- WebAssembly runtime
- container
- virtual machine
- network function

Avoid calling WebAssembly itself a virtual machine unless discussing a specific runtime architecture.

## Accepted implementation and architecture baseline

- Rust is the VNF reference language; share function logic between WebAssembly and native
  x86_64 builds where technically feasible. Rust is selected for fairness, portability,
  low runtime overhead, and mature tooling, not universal language performance superiority.
- Wasmtime is the baseline WebAssembly runtime.
- Docker Engine on Linux runs the native Rust VNF.
- QEMU/KVM/libvirt with a Linux guest and virtio networking runs the same native executable
  or an equivalent build from the same source tree.
- All three technologies are benchmarked on the same bare-metal x86 DUT: Intel Core
  i7-6700K, 16 GB RAM, SSD. Ubuntu Server 24.04 LTS is the accepted preferred DUT OS;
  installation and exact versions still need verification.
- MacBook M4 Max generates traffic, runs the orchestrator, and collects final artifacts.
  MacBook M1 Pro runs backends/receivers. Neither Mac is a primary DUT.
- Layer 4 / socket-based networking is the initial preferred abstraction.
- Clojure is used for `mt` (master-thesis); EDN defines experiment scenarios.
- Ansible configures/provisions hosts. `mt deploy` deploys applications/artifacts;
  `mt run` manages experiment lifecycles. Ansible is not the per-benchmark engine.
- Backend services may be written in Clojure on the M1 Pro. The primary vLB scenario
  uses a configurable service in `minimal` mode, outside the DUT.
- Final measurements use the controlled bare-metal DUT. AWS/EC2 is auxiliary only
  unless evidence and an explicit decision justify changing this baseline.

Experimental fairness and reproducibility take priority over implementation convenience.
Document unavoidable networking, build, and measurement differences. Account for total
VM/environment overhead where appropriate, rather than only guest VNF process RSS.

## Proposals and open methodology

A second DUT NIC, TRex, exact packet/payload sizes and load levels, approximately 30
repetitions, exact CPU/memory allocations, statistical tests, and a clean-working-tree
check remain proposals. A second NIC is not known to exist. Wasmtime vs WasmEdge and
Rust vs C/C++ vs TinyGo are optional secondary experiments, not core requirements.
Do not infer acceptance from illustrative configuration examples.

## Current project state

Documentation and planning only. No VNF, backend, `mt`, Ansible, or infrastructure
implementation has been authorized by this planning update.

Before implementation is requested, resolve networking feasibility, remaining architecture
and methodology questions, and version/resource controls in the relevant documents.
Do not install dependencies, configure hosts, build images, create VMs, or run benchmarks
as part of a documentation-only task.
