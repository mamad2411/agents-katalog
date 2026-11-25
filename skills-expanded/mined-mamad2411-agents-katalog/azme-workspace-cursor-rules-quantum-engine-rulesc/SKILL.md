# Quantum Engine Development Rules

## Quantum-Specific Development Guidelines

### P-ADIC PROCESSOR RULES
- All p-adic operations must validate numerical stability
- Implement bounds checking for all quantum state operations
- Use secure random generators for quantum key distribution
- Validate tensor dimensions before quantum operations
- Protect quantum memory from overflow and corruption

### FRACTAL STORAGE RULES
- Implement proper memory management for fractal storage
- Validate access patterns to prevent memory leaks
- Use efficient algorithms for fractal storage operations
- Monitor memory usage during fractal operations
- Implement cleanup routines for fractal storage

### LHA3 ADAPTIVE ENGINE RULES
- Validate quantum state integrity before LHA3 operations
- Implement proper state transitions in LHA3 memory
- Monitor LHA3 memory usage and performance
- Handle LHA3 memory errors gracefully
- Optimize LHA3 operations for GPU acceleration

### QUANTUM STATE VALIDATION
- Always validate quantum states before operations
- Check quantum state normalization
- Verify quantum circuit integrity
- Validate quantum measurement operations
- Protect against quantum state corruption

### GPU QUANTUM OPERATIONS
- All quantum tensor operations must run on GPU
- Never offload quantum computations to CPU
- Monitor GPU memory usage during quantum operations
- Optimize quantum algorithms for GPU parallelization
- Handle GPU errors gracefully in quantum operations

## Quantum Algorithm Implementation

### QUANTUM CIRCUIT DESIGN
- Validate quantum circuit before execution
- Check quantum gate compatibility
- Verify quantum circuit depth and width
- Implement quantum error correction where needed
- Monitor quantum circuit performance

### QUANTUM MEASUREMENT
- Implement proper quantum measurement protocols
- Validate measurement outcomes
- Handle quantum measurement errors
- Optimize measurement operations for GPU
- Document quantum measurement procedures

### QUANTUM ENTANGLEMENT
- Implement quantum entanglement protocols
- Validate entanglement state integrity
- Monitor entanglement operations
- Handle entanglement errors gracefully
- Optimize entanglement for quantum processing

## Performance Optimization

### QUANTUM MEMORY MANAGEMENT
- Monitor quantum memory usage
- Implement efficient quantum memory allocation
- Clean up quantum memory after operations
- Optimize quantum memory access patterns
- Handle quantum memory errors

### QUANTUM COMPUTATION OPTIMIZATION
- Optimize quantum algorithms for GPU
- Implement parallel quantum operations
- Monitor quantum computation performance
- Optimize quantum circuit compilation
- Handle quantum computation errors

## Error Handling for Quantum Systems

### QUANTUM ERROR DETECTION
- Implement quantum error detection algorithms
- Validate quantum error correction codes
- Monitor quantum error rates
- Handle quantum errors gracefully
- Document quantum error handling procedures

### QUANTUM STATE RECOVERY
- Implement quantum state recovery mechanisms
- Validate quantum state recovery procedures
- Monitor quantum state recovery performance
- Handle quantum state recovery errors
- Document quantum state recovery processes
description:
globs:
alwaysApply: false
---
