# MM-Rec Architecture - Cursor Rules

## Project Overview
MM-Rec (Multi-Memory Recurrence) is a novel LLM architecture that overcomes Transformer limitations using:
- Associative Scan with exponential product (Log-Sum-Exp pattern)
- Hierarchical Dynamic Memory System (HDS) with dual memory (short-term h_t and long-term M)
- Memory Decay/Integration (MDI) mechanism
- Core recurrence formula: h_t = z_t ⊙ σ(W_g h_{t-1}) + γ ⊙ h_{t-1}

## Workspace Hygiene (avoid clutter)
- Place new Markdown docs under `docs/` in the appropriate folder (architecture/performance/training/testing/install/cpp/integration/plans/status/analysis/mlops/misc); do not leave new .md files in the repo root.
- Put scripts/utilities under `scripts/`; installation scripts belong in `scripts/install/`.
- Keep temporary outputs/experimental notes in `tmp/` or other `.gitignore`d locations; avoid committing artifacts.
- If doc paths change, update README or other references that point to them.
- Before committing, ensure `git status` is clean; if adding new root-level files, align them with these rules first.

## Critical Architecture Requirements

### Core Formula (Efficiency Kernel)
- Formula: `h_t = z_t ⊙ σ(W_g h_{t-1}) + γ ⊙ h_{t-1}`
- Must use Log-Sum-Exp for cumulative product ∏ᵢ γᵢ
- Log-space clamping: [-50.0, 0.0] for numerical stability
- FP32 accumulation for log operations, BF16 for storage

### Associative Scan (Exponential Product)
- Operator: Cumulative exponential product (NOT sum): Y_t = ∏_{i=1}^t γ_i
- Implementation: Log-Sum-Exp pattern (log-space cumulative sum, then exp)
- Algorithm: Work-efficient parallel scan (Blelloch algorithm)
- Block size: 512-1024 for seq_len >= 1024, 256 for seq_len >= 256
- Block-to-block carry-over: CRITICAL for sequences > block_size

### HDS (Hierarchical Data Structure)
- Dual memory system:
  - Short-term: h_t [batch, seq_len, hidden_dim]
  - Long-term: M [batch, num_memories, M, mem_dim] where M << seq_len
- Access cost: O(M), not O(N) where N is sequence length
- Hierarchy levels: Level 0 (token), Level 1 (block), Level 2 (global), Level 3 (long-term M)

### MDI (Memory Decay/Integration)
- Learnable decay coefficients: γ (per memory bank)
- Context-dependent modulation: σ(W_modulation context)
- Gated integration: gate * new_mem + (1 - gate) * old_mem + residual

## Model Configuration (7B Model - REQUIRED)
- hidden_dim: 4096 (D_hidden, REQUIRED)
- num_layers: 24 (L_layer, REQUIRED)
- max_seq_len: >= 32768 (N_sequence ≥ 32K, REQUIRED)
- memory_size_M: 1024 (long-term memory size, M << seq_len)
- use_log_sum_exp: True (CRITICAL)
- log_clamp_min: -50.0, log_clamp_max: 0.0

## Context Window / Sequence Length Awareness

### CRITICAL: Long Context Support (32K+)
- MM-Rec is designed for VERY LONG sequences (32K+ tokens)
- This is a KEY differentiator from Transformer architectures
- All implementations MUST scale to 32K+ without quadratic complexity
- Memory complexity MUST be O(M) not O(N) where N is sequence length

### Sequence Length Handling
- **Short sequences** (< 256): Use small blocks (128), simple processing
- **Medium sequences** (256-1024): Use medium blocks (256), standard processing
- **Long sequences** (1024-32768): Use large blocks (512-1024), block-to-block carry-over REQUIRED
- **Very long sequences** (> 32768): Use maximum blocks (1024), optimize carry-over

### Block Size Selection (Context-Aware)
```python
if seq_len >= 1024:
    BLOCK_SIZE = 1024  # Large blocks for long context
elif seq_len >= 512:
    BLOCK_SIZE = 512   # Medium blocks
elif seq_len >= 256:
    BLOCK_SIZE = 256   # Small blocks
else:
    BLOCK_SIZE = 128   # Minimal blocks
```

### Memory Efficiency for Long Context
- NEVER allocate O(N²) memory (e.g., full attention matrices)
- ALWAYS use O(M) or O(N) memory where M << N
- Long-term memory M is fixed size (1024), independent of sequence length
- Short-term memory h_t scales linearly but can be checkpointed

### Context Window Testing
- ALWAYS test with target context window (32K+)
- Test scalability: 128, 1024, 8192, 32768, 65536 tokens
- Verify memory usage doesn't grow quadratically
- Profile with long sequences to catch performance regressions

## Code Standards

### Triton Kernel Development
- Always use Log-Sum-Exp pattern: `max(a, b) + log1p(exp(-abs(a - b)))`
- Clamp log values to [-50, 0] range
- Use FP32 for log-space operations, convert to BF16 at boundaries
- Implement block-to-block carry-over for sequences > block_size
- Use work-efficient parallel scan (Blelloch algorithm)

### Numerical Stability
- All log/exp operations in FP32
- Use stable exponential: `exp(log_sum - max) * exp(max)`
- Add epsilon (1e-8) before log operations
- Clamp decay coefficients to [1e-6, 1-1e-6]

### Testing Requirements
- Always include CPU fallback for development/testing
- Test with both FP32 and BF16 dtypes
- Verify against sequential reference implementation
- Gradient tests using finite difference
- Tolerance: 1e-3 for forward, 1e-2 for gradients

### File Structure
- Core components: `mm_rec/core/`
- Blocks: `mm_rec/blocks/`
- CUDA kernels: `mm_rec/cuda/`
- Tests: `tests/`
- Documentation: Markdown files in root and subdirectories

## Implementation Guidelines

### When Adding New Components
1. Check if it requires custom CUDA/Triton kernel (if standard PyTorch insufficient)
2. Use Log-Sum-Exp pattern for any exponential products
3. Support both CPU fallback and GPU acceleration
4. Add comprehensive tests
5. Document numerical stability considerations

### When Modifying Associative Scan
- NEVER remove Log-Sum-Exp pattern
- NEVER remove log-space clamping
- ALWAYS maintain block-to-block carry-over mechanism
- ALWAYS test with 32K+ sequence lengths
- ALWAYS consider context window size when choosing block size
- NEVER assume sequences are short (< 1K) - design for 32K+

### When Working with Memory States
- Remember dual memory system (h_t and M)
- O(M) access cost, not O(N)
- Update both short-term and long-term memory
- Handle memory state serialization for checkpoints

## Common Patterns

### Log-Sum-Exp Implementation
```python
def stable_log_sum_exp(a, b):
    max_val = max(a, b)
    diff = abs(a - b)
    diff_clamped = min(diff, 20.0)  # exp(-20) ≈ 0
    return max_val + log1p(exp(-diff_clamped))
```

### Cumulative Product in Log-Space
```python
# Convert to log-space
log_gamma = clamp(log(gamma + 1e-8), min=-50.0, max=0.0)
# Cumulative sum in log-space
log_cumsum = associative_scan(log_gamma, operator='add')
# Convert back with stability
max_log = max(log_cumsum)
stable_exp = exp(log_cumsum - max_log) * exp(max_log)
```

### Block-to-Block Carry-Over
```python
carry_in = zeros([batch, heads, dim])  # Previous block prefix
for block_idx in range(num_blocks):
    # Process block with carry_in
    # Compute block_prefix for next block
    carry_in = block_prefix  # Propagate to next block
```

## Documentation Standards
- All public APIs must have docstrings
- Include mathematical formulas in docstrings where relevant
- Document numerical stability considerations
- Include usage examples
- Specify tensor shapes: [BATCH, HEADS, SEQ_LEN, D_HEAD]

## Testing Standards
- Every new component needs unit tests
- Compare against reference implementation (sequential)
- Test with various sequence lengths (128, 1024, 32768, 65536)
- Test gradient correctness with finite difference
- Include CPU fallback tests
- **CRITICAL**: Always test with target context window (32K+)
- Verify memory usage scales linearly, not quadratically with sequence length

## Performance Considerations
- Use kernel fusion where possible
- Optimize memory access patterns (coalesced reads)
- Support gradient checkpointing for memory efficiency
- Profile with NVIDIA Nsight for GPU kernels

## Error Handling
- Validate input tensor shapes and dtypes
- Check for NaN/Inf in critical operations
- Provide clear error messages
- Fallback gracefully (CPU fallback, sequential implementation)

## Dependencies
- PyTorch 2.0+
- Triton 2.0+ (optional, for GPU acceleration)
- CUDA 11.8+ (optional, for GPU)

## Key Files Reference
- Core implementation: `mm_rec/core/associative_scan_triton.py`
- Algorithm explanation: `mm_rec/core/ALGORITHM_EXPLANATION.md`
- Technical requirements: `TECHNICAL_REQUIREMENTS.md`
- Implementation spec: `IMPLEMENTATION_SPEC.md`
- Core formula: `CORE_FORMULA_SPEC.md`

## Important Notes
- NEVER use direct multiplication for cumulative products (use Log-Sum-Exp)
- NEVER skip block-to-block carry-over for long sequences
- ALWAYS use FP32 for log-space operations
- ALWAYS clamp log values to prevent overflow/underflow
- ALWAYS test with 32K+ sequence lengths for scalability
- NEVER assume short context windows - MM-Rec is designed for 32K+ tokens
- ALWAYS consider context window size in memory allocations and algorithm choices
- REMEMBER: O(M) memory access, not O(N²) - this is the key advantage over Transformers

