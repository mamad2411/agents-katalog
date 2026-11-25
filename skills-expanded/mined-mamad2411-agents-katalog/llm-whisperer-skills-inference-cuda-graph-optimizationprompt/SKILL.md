# CUDA Graph Optimization for LLM Inference

## Overview

CUDA Graphs capture a sequence of GPU operations (kernel launches, memory copies, synchronization points) into a reusable graph structure that can be replayed with minimal CPU overhead. In standard CUDA execution, each kernel launch requires a CPU-to-GPU round trip through the CUDA driver, adding 5-15 microseconds of latency per launch. For LLM inference with dozens of kernel launches per layer, this overhead accumulates to hundreds of microseconds per token — significant when the target latency is single-digit milliseconds.

For LLM autoregressive generation, where the same computation pattern repeats for each new token with only the input changing, CUDA Graphs eliminate the per-kernel launch overhead entirely. The graph is captured once during a warmup phase and then replayed for each generation step. This can reduce decode latency by 20-40% for small batch sizes where kernel launch overhead is a significant fraction of total execution time.

Modern serving frameworks like vLLM implement CUDA Graphs with piecewise capture (capturing graphs for different batch sizes and sequence lengths) and automatic fallback to eager execution when graph capture isn't possible. The main limitation is that CUDA Graphs require fixed tensor shapes and memory addresses, which conflicts with dynamic batching and PagedAttention's variable memory layouts. Production systems solve this by maintaining a pool of pre-captured graphs for common configurations.

## Key Concepts

- **CUDA Graph**: A reusable representation of GPU operations that eliminates per-launch CPU overhead
- **Graph Capture**: Recording GPU operations into a graph during a warmup phase
- **Graph Replay**: Executing a captured graph with updated input/output pointers
- **Piecewise Capture**: Capturing separate graphs for different batch sizes and configurations
- **Memory Pinning**: CUDA Graphs require fixed memory addresses for input/output tensors
- **Warmup Phase**: Initial runs that capture graphs before production serving
- **Graph Pool**: Collection of pre-captured graphs for different configurations
- **torch.compile**: PyTorch's compiler that can automatically generate CUDA Graphs
- **Kernel Fusion**: Combining multiple small kernels into one larger kernel
- **CPU Overhead**: Latency from CPU-side operations between GPU kernel launches
- **Static Shapes**: CUDA Graphs require fixed tensor dimensions
- **Graph Invalidation**: When shape changes require re-capturing the graph

## Implementation Patterns

### Basic CUDA Graph Capture and Replay

```python
import torch

class CUDAGraphWrapper:
    """Wrapper for CUDA graph capture and replay."""

    def __init__(self, model, max_batch_size: int = 1, max_seq_len: int = 2048):
        self.model = model
        self.max_batch_size = max_batch_size
        self.max_seq_len = max_seq_len
        self.graphs = {}
        self.static_inputs = {}
        self.static_outputs = {}

    def warmup(self, batch_sizes: list = None, seq_lens: list = None):
        """Capture CUDA graphs for common configurations."""
        if batch_sizes is None:
            batch_sizes = [1, 2, 4, 8, 16]
        if seq_lens is None:
            seq_lens = [1, 128, 512, 1024]

        self.model.eval()

        with torch.no_grad():
            for bs in batch_sizes:
                for sl in seq_lens:
                    if bs > self.max_batch_size or sl > self.max_seq_len:
                        continue

                    config_key = (bs, sl)
                    self._capture_graph(config_key, bs, sl)

        print(f"Captured {len(self.graphs)} CUDA graphs")

    def _capture_graph(self, config_key: tuple, batch_size: int, seq_len: int):
        """Capture a CUDA graph for a specific configuration."""
        device = next(self.model.parameters()).device

        # Create static input tensor
        static_input = torch.zeros(
            (batch_size, seq_len), dtype=torch.long, device=device
        )

        # Warmup runs (required before capture)
        for _ in range(3):
            self.model(static_input)

        # Capture the graph
        graph = torch.cuda.CUDAGraph()
        with torch.cuda.graph(graph):
            static_output = self.model(static_input)

        self.graphs[config_key] = graph
        self.static_inputs[config_key] = static_input
        self.static_outputs[config_key] = static_output

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Forward pass using CUDA graph replay."""
        batch_size, seq_len = input_ids.shape
        config_key = (batch_size, seq_len)

        if config_key in self.graphs:
            # Copy input to static buffer
            self.static_inputs[config_key].copy_(input_ids)
            # Replay the graph
            self.graphs[config_key].replay()
            return self.static_outputs[config_key].clone()
        else:
            # Fallback to eager execution
            return self.model(input_ids)
```

### Piecewise CUDA Graph for Transformer Layer

```python
class PiecewiseTransformerGraph:
    """Capture CUDA graphs for individual transformer components."""

    def __init__(self, attention_layer, mlp_layer, norm_layer):
        self.attention = attention_layer
        self.mlp = mlp_layer
        self.norm = norm_layer
        self.graphs = {}

    def capture_attention(self, config_key: tuple, hidden_states: torch.Tensor,
                           attention_mask: torch.Tensor):
        """Capture graph for attention computation."""
        graph = torch.cuda.CUDAGraph()

        # Warmup
        for _ in range(3):
            self.attention(hidden_states, attention_mask)

        # Capture
        with torch.cuda.graph(graph):
            output = self.attention(hidden_states, attention_mask)

        self.graphs[("attention", config_key)] = {
            "graph": graph,
            "static_input": hidden_states,
            "static_mask": attention_mask,
            "static_output": output,
        }

    def capture_mlp(self, config_key: tuple, hidden_states: torch.Tensor):
        """Capture graph for MLP computation."""
        graph = torch.cuda.CUDAGraph()

        for _ in range(3):
            self.mlp(hidden_states)

        with torch.cuda.graph(graph):
            output = self.mlp(hidden_states)

        self.graphs[("mlp", config_key)] = {
            "graph": graph,
            "static_input": hidden_states,
            "static_output": output,
        }

    def forward(self, hidden_states: torch.Tensor, attention_mask: torch.Tensor,
                config_key: tuple) -> torch.Tensor:
        """Forward pass using piecewise graph replay."""
        # Attention
        attn_key = ("attention", config_key)
        if attn_key in self.graphs:
            entry = self.graphs[attn_key]
            entry["static_input"].copy_(hidden_states)
            entry["static_mask"].copy_(attention_mask)
            entry["graph"].replay()
            attn_output = entry["static_output"].clone()
        else:
            attn_output = self.attention(hidden_states, attention_mask)

        # Residual + Norm
        hidden_states = hidden_states + attn_output
        hidden_states = self.norm(hidden_states)

        # MLP
        mlp_key = ("mlp", config_key)
        if mlp_key in self.graphs:
            entry = self.graphs[mlp_key]
            entry["static_input"].copy_(hidden_states)
            entry["graph"].replay()
            mlp_output = entry["static_output"].clone()
        else:
            mlp_output = self.mlp(hidden_states)

        return hidden_states + mlp_output
```

### torch.compile with CUDA Graphs

```python
import torch

def compile_model_with_cuda_graphs(model, mode: str = "max-autotune"):
    """
    Compile model with torch.compile for automatic CUDA graph optimization.

    Modes:
    - "default": Basic optimizations
    - "reduce-overhead": Focus on reducing CPU overhead (good for LLM decode)
    - "max-autotune": Maximum optimization including kernel fusion
    """
    compiled_model = torch.compile(
        model,
        mode=mode,
        fullgraph=True,        # Capture entire model as one graph
        dynamic=False,         # Static shapes for CUDA graph compatibility
    )

    return compiled_model

# Usage with vLLM-style serving
class CompiledModelWrapper:
    def __init__(self, model):
        self.model = model
        self.compiled_models = {}

    def get_compiled_model(self, batch_size: int, seq_len: int):
        """Get or create a compiled model for a specific configuration."""
        config_key = (batch_size, seq_len)
        if config_key not in self.compiled_models:
            # Create a copy and compile
            compiled = torch.compile(
                self.model,
                mode="reduce-overhead",
                dynamic=False,
            )
            self.compiled_models[config_key] = compiled
        return self.compiled_models[config_key]
```

### Graph Memory Management

```python
class GraphMemoryPool:
    """Manage memory for CUDA graph static tensors."""

    def __init__(self, device: str = "cuda"):
        self.device = device
        self.allocated_tensors = {}
        self.free_blocks = []

    def allocate(self, shape: tuple, dtype: torch.dtype, name: str) -> torch.Tensor:
        """Allocate a static tensor for CUDA graph use."""
        if name in self.allocated_tensors:
            existing = self.allocated_tensors[name]
            if existing.shape == shape and existing.dtype == dtype:
                return existing

        # Try to reuse a free block
        for i, (block_shape, block_dtype, block_tensor) in enumerate(self.free_blocks):
            if block_shape == shape and block_dtype == dtype:
                self.free_blocks.pop(i)
                self.allocated_tensors[name] = block_tensor
                return block_tensor

        # Allocate new tensor
        tensor = torch.zeros(shape, dtype=dtype, device=self.device)
        self.allocated_tensors[name] = tensor
        return tensor

    def release(self, name: str):
        """Release a tensor back to the free pool."""
        if name in self.allocated_tensors:
            tensor = self.allocated_tensors.pop(name)
            self.free_blocks.append((tensor.shape, tensor.dtype, tensor))

    def clear(self):
        """Release all allocated tensors."""
        self.allocated_tensors.clear()
        self.free_blocks.clear()
        torch.cuda.empty_cache()
```

## Best Practices

1. Capture CUDA graphs for all common batch sizes during a warmup phase before serving
2. Use piecewise capture for transformer layers to handle different configurations independently
3. Use `torch.compile(mode="reduce-overhead")` for automatic CUDA graph generation
4. Pin input/output tensors to fixed memory addresses for graph replay compatibility
5. Implement fallback to eager execution for configurations not covered by captured graphs
6. Monitor graph cache hit rates to identify missing configurations
7. Use static shapes wherever possible — dynamic shapes invalidate CUDA graphs
8. Profile the warmup time and include it in deployment startup metrics
9. Clear CUDA graph caches when switching models to avoid memory leaks
10. Test CUDA graph correctness by comparing outputs with eager execution

## Common Pitfalls

- Not running warmup captures before serving, causing first-request latency spikes
- Using dynamic shapes that invalidate captured graphs
- Not pinning tensor memory addresses, causing graph replay failures
- Capturing graphs with incorrect tensor values that affect autotuning decisions
- Not implementing fallback for uncaptured configurations
- Ignoring the memory overhead of storing multiple captured graphs
- Using CUDA graphs with operations that have data-dependent control flow
- Not testing graph replay correctness across different GPU architectures

## References

- NVIDIA CUDA Graphs documentation — https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#cuda-graphs
- PyTorch CUDA Graphs documentation — https://pytorch.org/docs/stable/notes/cuda.html
- torch.compile documentation — https://pytorch.org/docs/stable/torch.compiler.html
- vLLM CUDA Graph implementation — https://github.com/vllm-project/vllm
- Dao et al., "FlashAttention: Fast and Memory-Efficient Exact Attention" (NeurIPS 2022)
