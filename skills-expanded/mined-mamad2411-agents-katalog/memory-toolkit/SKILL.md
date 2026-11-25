---
name: memory-toolkit
description: Consolidated toolkit for memory. Covers memory-safety-patterns, memory-forensics, memory-systems
---
# Memory Toolkit

## Use this skill when
- Choosing between languages for safety
- Debugging memory issues
- Implementing RAII patterns
- Managing resources (files, sockets, memory)
- Needing guidance, best practices, or checklists for memory forensics
- Preventing use-after-free and leaks
- Working on memory forensics tasks or workflows
- Writing memory-safe systems code

## Do not use this skill when
- The task is unrelated to memory forensics
- The task is unrelated to memory safety patterns
- You need a different domain or tool outside this scope

## Core Capabilities
# Memory Toolkit

# Memory Safety Patterns

Cross-language patterns for memory-safe programming including RAII, ownership, smart pointers, and resource management.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

---

# Memory Forensics

Comprehensive techniques for acquiring, analyzing, and extracting artifacts from memory dumps for incident response and malware analysis.

## Memory Acquisition

### Live Acquisition Tools

#### Windows
```powershell
# WinPmem (Recommended)
winpmem_mini_x64.exe memory.raw

# DumpIt
DumpIt.exe

# Belkasoft RAM Capturer
# GUI-based, outputs raw format

# Magnet RAM Capture
# GUI-based, outputs raw format
```

#### Linux
```bash
# LiME (Linux Memory Extractor)
sudo insmod lime.ko "path=/tmp/memory.lime format=lime"

# /dev/mem (limited, requires permissions)
sudo dd if=/dev/mem of=memory.raw bs=1M

# /proc/kcore (ELF format)
sudo cp /proc/kcore memory.elf
```

#### macOS
```bash
# osxpmem
sudo ./osxpmem -o memory.raw

# MacQuisition (commercial)
```

### Virtual Machine Memory

```bash
# VMware: .vmem file is raw memory
cp vm.vmem memory.raw

# VirtualBox: Use debug console
vboxmanage debugvm "VMName" dumpvmcore --filename memory.elf

# QEMU
virsh dump <domain> memory.raw --memory-only

# Hyper-V
# Checkpoint contains memory state
```

## Volatility 3 Framework

### Installation and Setup

```bash
# Install Volatility 3
pip install volatility3

# Install symbol tables (Windows)
# Download from https://downloads.volatilityfoundation.org/volatility3/symbols/

# Basic usage
vol -f memory.raw <plugin>

# With symbol path
vol -f memory.raw -s /path/to/symbols windows.pslist
```

### Essential Plugins

#### Process Analysis
```bash
# List processes
vol -f memory.raw windows.pslist

# Process tree (parent-child relationships)
vol -f memory.raw windows.pstree

# Hidden process detection
vol -f memory.raw windows.psscan

# Process memory dumps
vol -f memory.raw windows.memmap --pid <PID> --dump

# Process environment variables
vol -f memory.raw windows.envars --pid <PID>

# Command line arguments
vol -f memory.raw windows.cmdline
```

#### Network Analysis
```bash
# Network connections
vol -f memory.raw windows.netscan

# Network connection state
vol -f memory.raw windows.netstat
```

#### DLL and Module Analysis
```bash
# Loaded DLLs per process
vol -f memory.raw windows.dlllist --pid <PID>

# Find hidden/injected DLLs
vol -f memory.raw windows.ldrmodules

# Kernel modules
vol -f memory.raw windows.modules

# Module dumps
vol -f memory.raw windows.moddump --pid <PID>
```

#### Memory Injection Detection
```bash
# Detect code injection
vol -f memory.raw windows.malfind

# VAD (Virtual Address Descriptor) analysis
vol -f memory.raw windows.vadinfo --pid <PID>

# Dump suspicious memory regions
vol -f memory.raw windows.vadyarascan --yara-rules rules.yar
```

#### Registry Analysis
```bash
# List registry hives
vol -f memory.raw windows.registry.hivelist

# Print registry key
vol -f memory.raw windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"

# Dump registry hive
vol -f memory.raw windows.registry.hivescan --dump
```

#### File System Artifacts
```bash
# Scan for file objects
vol -f memory.raw windows.filescan

# Dump files from memory
vol -f memory.raw windows.dumpfiles --pid <PID>

# MFT analysis
vol -f memory.raw windows.mftscan
```

### Linux Analysis

```bash
# Process listing
vol -f memory.raw linux.pslist

# Process tree
vol -f memory.raw linux.pstree

# Bash history
vol -f memory.raw linux.bash

# Network connections
vol -f memory.raw linux.sockstat

# Loaded kernel modules
vol -f memory.raw linux.lsmod

# Mount points
vol -f memory.raw linux.mount

# Environment variables
vol -f memory.raw linux.envars
```

### macOS Analysis

```bash
# Process listing
vol -f memory.raw mac.pslist

# Process tree
vol -f memory.raw mac.pstree

# Network connections
vol -f memory.raw mac.netstat

# Kernel extensions
vol -f memory.raw mac.lsmod
```

## Analysis Workflows

### Malware Analysis Workflow

```bash
# 1. Initial process survey
vol -f memory.raw windows.pstree > processes.txt
vol -f memory.raw windows.pslist > pslist.txt

# 2. Network connections
vol -f memory.raw windows.netscan > network.txt

# 3. Detect injection
vol -f memory.raw windows.malfind > malfind.txt

# 4. Analyze suspicious processes
vol -f memory.raw windows.dlllist --pid <PID>
vol -f memory.raw windows.handles --pid <PID>

# 5. Dump suspicious executables
vol -f memory.raw windows.pslist --pid <PID> --dump

# 6. Extract strings from dumps
strings -a pid.<PID>.exe > strings.txt

# 7. YARA scanning
vol -f memory.raw windows.yarascan --yara-rules malware.yar
```

### Incident Response Workflow

```bash
# 1. Timeline of events
vol -f memory.raw windows.timeliner > timeline.csv

# 2. User activity
vol -f memory.raw windows.cmdline
vol -f memory.raw windows.consoles

# 3. Persistence mechanisms
vol -f memory.raw windows.registry.printkey \
    --key "Software\Microsoft\Windows\CurrentVersion\Run"

# 4. Services
vol -f memory.raw windows.svcscan

# 5. Scheduled tasks
vol -f memory.raw windows.scheduled_tasks

# 6. Recent files
vol -f memory.raw windows.filescan | grep -i "recent"
```

## Data Structures

### Windows Process Structures

```c
// EPROCESS (Executive Process)
typedef struct _EPROCESS {
    KPROCESS Pcb;                    // Kernel process block
    EX_PUSH_LOCK ProcessLock;
    LARGE_INTEGER CreateTime;
    LARGE_INTEGER ExitTime;
    // ...
    LIST_ENTRY ActiveProcessLinks;   // Doubly-linked list
    ULONG_PTR UniqueProcessId;       // PID
    // ...
    PEB* Peb;                        // Process Environment Block
    // ...
} EPROCESS;

// PEB (Process Environment Block)
typedef struct _PEB {
    BOOLEAN InheritedAddressSpace;
    BOOLEAN ReadImageFileExecOptions;
    BOOLEAN BeingDebugged;           // Anti-debug check
    // ...
    PVOID ImageBaseAddress;          // Base address of executable
    PPEB_LDR_DATA Ldr;              // Loader data (DLL list)
    PRTL_USER_PROCESS_PARAMETERS ProcessParameters;
    // ...
} PEB;
```

### VAD (Virtual Address Descriptor)

```c
typedef struct _MMVAD {
    MMVAD_SHORT Core;
    union {
        ULONG LongFlags;
        MMVAD_FLAGS VadFlags;
    } u;
    // ...
    PVOID FirstPrototypePte;
    PVOID LastContiguousPte;
    // ...
    PFILE_OBJECT FileObject;
} MMVAD;

// Memory protection flags
#define PAGE_EXECUTE           0x10
#define PAGE_EXECUTE_READ      0x20
#define PAGE_EXECUTE_READWRITE 0x40
#define PAGE_EXECUTE_WRITECOPY 0x80
```

## Detection Patterns

### Process Injection Indicators

```python
# Malfind indicators
# - PAGE_EXECUTE_READWRITE protection (suspicious)
# - MZ header in non-image VAD region
# - Shellcode patterns at allocation start

# Common injection techniques
# 1. Classic DLL Injection
#    - VirtualAllocEx + WriteProcessMemory + CreateRemoteThread

# 2. Process Hollowing
#    - CreateProcess (SUSPENDED) + NtUnmapViewOfSection + WriteProcessMemory

# 3. APC Injection
#    - QueueUserAPC targeting alertable threads

# 4. Thread Execution Hijacking
#    - SuspendThread + SetThreadContext + ResumeThread
```

### Rootkit Detection

```bash
# Compare process lists
vol -f memory.raw windows.pslist > pslist.txt
vol -f memory.raw windows.psscan > psscan.txt
diff pslist.txt psscan.txt  # Hidden processes

# Check for DKOM (Direct Kernel Object Manipulation)
vol -f memory.raw windows.callbacks

# Detect hooked functions
vol -f memory.raw windows.ssdt  # System Service Descriptor Table

# Driver analysis
vol -f memory.raw windows.driverscan
vol -f memory.raw windows.driverirp
```

### Credential Extraction

```bash
# Dump hashes (requires hivelist first)
vol -f memory.raw windows.hashdump

# LSA secrets
vol -f memory.raw windows.lsadump

# Cached domain credentials
vol -f memory.raw windows.cachedump

# Mimikatz-style extraction
# Requires specific plugins/tools
```

## YARA Integration

### Writing Memory YARA Rules

```yara
rule Suspicious_Injection
{
    meta:
        description = "Detects common injection shellcode"

    strings:
        // Common shellcode patterns
        $mz = { 4D 5A }
        $shellcode1 = { 55 8B EC 83 EC }  // Function prologue
        $api_hash = { 68 ?? ?? ?? ?? 68 ?? ?? ?? ?? E8 }  // Push hash, call

    condition:
        $mz at 0 or any of ($shellcode*)
}

rule Cobalt_Strike_Beacon
{
    meta:
        description = "Detects Cobalt Strike beacon in memory"

    strings:
        $config = { 00 01 00 01 00 02 }
        $sleep = "sleeptime"
        $beacon = "%s (admin)" wide

    condition:
        2 of them
}
```

### Scanning Memory

```bash
# Scan all process memory
vol -f memory.raw windows.yarascan --yara-rules rules.yar

# Scan specific process
vol -f memory.raw windows.yarascan --yara-rules rules.yar --pid 1234

# Scan kernel memory
vol -f memory.raw windows.yarascan --yara-rules rules.yar --kernel
```

## String Analysis

### Extracting Strings

```bash
# Basic string extraction
strings -a memory.raw > all_strings.txt

# Unicode strings
strings -el memory.raw >> all_strings.txt

# Targeted extraction from process dump
vol -f memory.raw windows.memmap --pid 1234 --dump
strings -a pid.1234.dmp > process_strings.txt

# Pattern matching
grep -E "(https?://|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})" all_strings.txt
```

### FLOSS for Obfuscated Strings

```bash
# FLOSS extracts obfuscated strings
floss malware.exe > floss_output.txt

# From memory dump
floss pid.1234.dmp
```

## Best Practices

### Acquisition Best Practices

1. **Minimize footprint**: Use lightweight acquisition tools
2. **Document everything**: Record time, tool, and hash of capture
3. **Verify integrity**: Hash memory dump immediately after capture
4. **Chain of custody**: Maintain proper forensic handling

### Analysis Best Practices

1. **Start broad**: Get overview before deep diving
2. **Cross-reference**: Use multiple plugins for same data
3. **Timeline correlation**: Correlate memory findings with disk/network
4. **Document findings**: Keep detailed notes and screenshots
5. **Validate results**: Verify findings through multiple methods

### Common Pitfalls

- **Stale data**: Memory is volatile, analyze promptly
- **Incomplete dumps**: Verify dump size matches expected RAM
- **Symbol issues**: Ensure correct symbol files for OS version
- **Smear**: Memory may change during acquisition
- **Encryption**: Some data may be encrypted in memory

---

# Memory System Design

Memory provides the persistence layer that allows agents to maintain continuity across sessions and reason over accumulated knowledge. Simple agents rely entirely on context for memory, losing all state when sessions end. Sophisticated agents implement layered memory architectures that balance immediate context needs with long-term knowledge retention. The evolution from vector stores to knowledge graphs to temporal knowledge graphs represents increasing investment in structured memory for improved retrieval and reasoning.

## When to Activate

Activate this skill when:
- Building agents that must persist knowledge across sessions
- Choosing between memory frameworks (Mem0, Zep/Graphiti, Letta, LangMem, Cognee)
- Needing to maintain entity consistency across conversations
- Implementing reasoning over accumulated knowledge
- Designing memory architectures that scale in production
- Evaluating memory systems against benchmarks (LoCoMo, LongMemEval, DMR)
- Building dynamic memory with automatic entity/relationship extraction and self-improving(Cognee)

## Core Concepts

Memory spans a spectrum from volatile context window to persistent storage. Key insight from benchmarks: **tool complexity matters less than reliable retrieval** — Letta's filesystem agents scored 74% on LoCoMo using basic file operations, beating Mem0's specialized tools at 68.5%. Start simple, add structure (graphs, temporal validity) only when retrieval quality demands it.

## Detailed Topics

### Production Framework Landscape

| Framework | Architecture | Best For | Trade-off |
|-----------|-------------|----------|-----------|
| **Mem0** | Vector store + graph memory, pluggable backends | Multi-tenant systems, broad integrations | Less specialized for multi-agent |
| **Zep/Graphiti** | Temporal knowledge graph, bi-temporal model | Enterprise requiring relationship modeling + temporal reasoning | Advanced features cloud-locked |
| **Letta** | Self-editing memory with tiered storage (in-context/core/archival) | Full agent introspection, stateful services | Complexity for simple use cases |
| **Cognee** | Multi-layer semantic graph via customizable ECL pipeline with customizable Tasks | Evolving agent memory that adapts and learns; multi-hop reasoning | Heavier ingest-time processing |
| **LangMem** | Memory tools for LangGraph workflows | Teams already on LangGraph | Tightly coupled to LangGraph |
| **File-system** | Plain files with naming conventions | Simple agents, prototyping | No semantic search, no relationships |

Zep's Graphiti engine builds a three-tier knowledge graph (episode, semantic entity, community subgraphs) with a bi-temporal model tracking both when events occurred and when they were ingested. Mem0 offers the fastest path to production with managed infrastructure. Letta provides the deepest agent control through its Agent Development Environment. Cognee produces multi-layer semantic graphs — it layers text chunks and entity types as nodes with detailed relationship edges, building interconnected knowledge engine. Every core piece (ingestion, entity extraction, post-processing, retrieval) is customizable.

**Benchmark Performance Comparison**

| System | DMR Accuracy | LoCoMo | HotPotQA (multi-hop) | Latency |
|--------|-------------|--------|---------------------|---------|
| Cognee | — | — | Highest on EM, F1, Correctness | Variable |
| Zep (Temporal KG) | 94.8% | — | Mid-range across metrics | 2.58s |
| Letta (filesystem) | — | 74.0% | — | — |
| Mem0 | — | 68.5% | Lowest across metrics | — |
| MemGPT | 93.4% | — | — | Variable |
| GraphRAG | ~75-85% | — | — | Variable |
| Vector RAG baseline | ~60-70% | — | — | Fast |

Zep achieves up to 18.5% accuracy improvement on LongMemEval while reducing latency by 90%. Cognee outperformed Mem0, Graphiti, and LightRAG on HotPotQA multi-hop reasoning benchmarks across Exact Match, F1, and human-like correctness metrics. Letta's filesystem-based agents achieved 74% on LoCoMo using basic file operations, outperforming specialized memory tools — tool complexity matters less than reliable retrieval. No single benchmark is definitive; treat these as signals for specific retrieval dimensions rather than rankings.

### Memory Layers (Decision Points)

| Layer | Persistence | Implementation | When to Use |
|-------|------------|----------------|-------------|
| **Working** | Context window only | Scratchpad in system prompt | Always — optimize with attention-favored positions |
| **Short-term** | Session-scoped | File-system, in-memory cache | Intermediate tool results, conversation state |
| **Long-term** | Cross-session | Key-value store → graph DB | User preferences, domain knowledge, entity registries |
| **Entity** | Cross-session | Entity registry + properties | Maintaining identity ("John Doe" = same person across conversations) |
| **Temporal KG** | Cross-session + history | Graph with validity intervals | Facts that change over time, time-travel queries, preventing context clash |

### Retrieval Strategies

| Strategy | Use When | Limitation |
|----------|----------|------------|
| **Semantic** (embedding similarity) | Direct factual queries | Degrades on multi-hop reasoning |
| **Entity-based** (graph traversal) | "Tell me everything about X" | Requires graph structure |
| **Temporal** (validity filter) | Facts change over time | Requires validity metadata |
| **Hybrid** (semantic + keyword + graph) | Best overall accuracy | Most infrastructure |

Zep's hybrid approach achieves 90% latency reduction (2.58s vs 28.9s) by retrieving only relevant subgraphs. Cognee implements hybrid retrieval through its 14 search modes — each mode combines different strategies from its three-store architecture (graph, vector, relational), letting agents select the retrieval strategy that fits the query type rather than using a one-size-fits-all approach.

### Memory Consolidation

Consolidate periodically to prevent unbounded growth. **Invalidate but don't discard** — preserving history matters for temporal queries. Trigger on memory count thresholds, degraded retrieval quality, or scheduled intervals. See [implementation reference](./references/implementation.md) for working consolidation code.

## Practical Guidance

### Choosing a Memory Architecture

**Start simple, add complexity only when retrieval fails.** Most agents don't need a temporal knowledge graph on day one.

1. **Prototype**: File-system memory. Store facts as structured JSON with timestamps. Good enough to validate agent behavior.
2. **Scale**: Move to Mem0 or vector store with metadata when you need semantic search and multi-tenant isolation.
3. **Complex reasoning**: Add Zep/Graphiti when you need relationship traversal, temporal validity, or cross-session synthesis. Graphiti uses structured ties with generic relations, keeping graphs simple and easy to reason about; Cognee builds denser multi-layer semantic graphs with detailed relationship edges — choose based on whether you need temporal bi-modeling (Graphiti) or richer interconnected knowledge structures (Cognee).
4. **Full control**: Use Letta or Cognee when you need agent self-management of memory with deep introspection.

### Integration with Context

Memories must integrate with context systems to be useful. Use just-in-time memory loading to retrieve relevant memories when needed. Use strategic injection to place memories in attention-favored positions (beginning/end of context).

### Error Recovery

- **Empty retrieval**: Fall back to broader search (remove entity filter, widen time range). If still empty, prompt user for clarification.
- **Stale results**: Check `valid_until` timestamps. If most results are expired, trigger consolidation before retrying.
- **Conflicting facts**: Prefer the fact with the most recent `valid_from`. Surface the conflict to the user if confidence is low.
- **Storage failure**: Queue writes for retry. Never block the agent's response on a memory write.

### Anti-Patterns

- **Stuffing everything into context**: Long inputs are expensive and degrade performance. Use just-in-time retrieval.
- **Ignoring temporal validity**: Facts go stale. Without validity tracking, outdated information poisons context.
- **Over-engineering early**: A filesystem agent can outperform complex memory tooling. Add sophistication when simple approaches fail.
- **No consolidation strategy**: Unbounded memory growth degrades retrieval quality over time.

## Examples

**Example 1: Mem0 Integration**
```python
from mem0 import Memory

m = Memory()
m.add("User prefers dark mode and Python 3.12", user_id="alice")
m.add("User switched to light mode", user_id="alice")

# Retrieves current preference (light mode), not outdated one
results = m.search("What theme does the user prefer?", user_id="alice")
```

**Example 2: Temporal Query**
```python
# Track entity with validity periods
graph.create_temporal_relationship(
    source_id=user_node,
    rel_type="LIVES_AT",
    target_id=address_node,
    valid_from=datetime(2024, 1, 15),
    valid_until=datetime(2024, 9, 1),  # moved out
)

# Query: Where did user live on March 1, 2024?
results = graph.query_at_time(
    {"type": "LIVES_AT", "source_label": "User"},
    query_time=datetime(2024, 3, 1)
)
```

**Example 3: Cognee Memory Ingestion and Search**
```python
import cognee
from cognee.modules.search.types import SearchType

# Ingest and build knowledge graph
await cognee.add("./docs/")
await cognee.add("any data")
await cognee.cognify()

# Enrich memory 
await cognee.memify()

# Agent retrieves relationship-aware context
results = await cognee.search(
    query_text="Any query for your memory",
    query_type=SearchType.GRAPH_COMPLETION,
)
```

## Guidelines

1. Start with file-system memory; add complexity only when retrieval quality demands it
2. Track temporal validity for any fact that can change over time
3. Use hybrid retrieval (semantic + keyword + graph) for best accuracy
4. Consolidate memories periodically — invalidate but don't discard
5. Design for retrieval failure: always have a fallback when memory lookup returns nothing
6. Consider privacy implications of persistent memory (retention policies, deletion rights)
7. Benchmark your memory system against LoCoMo or LongMemEval before and after changes
8. Monitor memory growth and retrieval latency in production

## Integration

This skill builds on context-fundamentals. It connects to:

- multi-agent-patterns - Shared memory across agents
- context-optimization - Memory-based context loading
- evaluation - Evaluating memory quality

## References

Internal references:
- [Implementation Reference](./references/implementation.md) - Detailed implementation patterns, production framework references (Mem0, Graphiti, Cognee)

Related skills in this collection:
- context-fundamentals - Context basics
- multi-agent-patterns - Cross-agent memory

External resources:
- Zep temporal knowledge graph paper (arXiv:2501.13956)
- Mem0 production architecture paper (arXiv:2504.19413)
- Cognee optimized knowledge graph + LLM reasoning paper	(arXiv:2505.24478)
- LoCoMo benchmark (Snap Research)
- MemBench evaluation framework (ACL 2025)
- Graphiti open-source temporal KG engine (github.com/getzep/graphiti)
- Cognee open-source knowledge graph memory (github.com/topoteretes/cognee)
- [Cognee comparison: Form vs Function](https://www.cognee.ai/blog/deep-dives/competition-comparison-form-vs-function) — graph structure comparison and HotPotQA benchmarks across Mem0, Graphiti, LightRAG, Cognee

---

## Skill Metadata

**Created**: 2025-12-20
**Last Updated**: 2026-02-26
**Author**: Agent Skills for Context Engineering Contributors
**Version**: 3.0.0

---
