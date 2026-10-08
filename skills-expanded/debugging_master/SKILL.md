---
name: debugging-master
description: Systematic debugging techniques and root cause analysis for complex issues.
---

# Debugging Master

Systematic approach to finding and fixing bugs.

## Debugging Methodology

### 1. Reproduce
- Identify exact steps to reproduce
- Note environment (OS, versions, config)
- Minimize the reproduction case
- Check if it reproduces consistently

### 2. Isolate
- Bisect: When did the bug start? (git bisect)
- Reduce: What's the minimal input that triggers it?
- Vary: Change one variable at a time
- Compare: Does it work in a different environment?

### 3. Diagnose
- **Logs**: Add structured logging, trace execution
- **Debugger**: Breakpoints, watch expressions, call stack
- **Profiler**: CPU/memory profiling for performance bugs
- **Network**: Capture traffic, inspect headers/payloads
- **State**: Dump relevant state at failure point

### 4. Fix
- Fix the root cause, not the symptom
- Verify the fix resolves the reproduction case
- Check for similar issues elsewhere (same pattern)
- Add a regression test
- Document the bug and fix for future reference

## Common Bug Categories

### Memory Bugs
- Leaks: growing memory over time
- Use-after-free: accessing freed memory
- Buffer overflow: out-of-bounds access
- Double-free: deallocating twice

### Concurrency Bugs
- Race conditions: shared state without synchronization
- Deadlocks: circular lock dependencies
- Livelocks: busy-waiting without progress
- Starvation: thread never gets resources

### Logic Bugs
- Off-by-one: boundary errors in loops/indexing
- Type coercion: unexpected type conversions
- Floating point: precision and rounding errors
- Null/undefined: missing null checks

### Integration Bugs
- API contract mismatch: different field names/types
- Version incompatibility: breaking changes
- Environment differences: dev vs prod
- Timing issues: race between services

## Debug Tools
- **Chrome DevTools**: Frontend debugging, network, performance
- **gdb/lldb**: Native code debugging
- **pdb/delv/pydbg**: Language-specific debuggers
- **strace/dtrace**: System call tracing
- **tcpdump/Wireshark**: Network packet analysis
- **valgrind**: Memory debugging (C/C++)
