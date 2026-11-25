# Gradient Checkpointing for Memory Efficiency

## Overview

Gradient checkpointing (also called activation checkpointing or rematerialization) trades computation for memory by discarding intermediate activations during the forward pass and recomputing them during the backward pass. This technique can reduce activation memory by 60-80% at the cost of approximately 30% more compute, enabling training of much larger models or using larger batch sizes on the same hardware. This skill covers implementing gradient checkpointing, configuring checkpoint granularity, and optimizing the memory-compute tradeoff.

Without gradient checkpointing, all intermediate activations from every layer must be stored in GPU memory for the backward pass. For a 7B parameter model with sequence length 4096, this can consume 40-60 GB of memory just for activations. Checkpointing reduces this to storing activations at selected boundaries, recomputing the rest on demand.

## Key Concepts

- **Activation Memory**: The GPU memory consumed by storing intermediate layer outputs for gradient computation
- **Checkpoint Boundaries**: Points in the computation graph where activations are saved instead of recomputed
- **Recomputation Cost**: The additional forward computation needed to regenerate discarded activations
- **Selective Checkpointing**: Checkpointing only the most memory-intensive layers (attention, FFN) while keeping others
- **Granularity Control**: Choosing whether to checkpoint at the layer, sublayer, or operation level
- **Unsloth Checkpointing**: Optimized checkpointing that fuses operations for lower overhead
- **CPU Offloading**: Moving activations to CPU memory instead of recomputing them
- **Memory-Compute Tradeoff**: The fundamental balance between memory savings and computation overhead

## Implementation Patterns

```python
import torch
import torch.nn as nn
from typing import Callable, Any

class CheckpointedModule(nn.Module):
    """Wrapper that applies gradient checkpointing to a module."""
    def __init__(self, module: nn.Module, use_reentrant: bool = False):
        super().__init__()
        self.module = module
        self.use_reentrant = use_reentrant

    def forward(self, *args, **kwargs):
        return torch.utils.checkpoint.checkpoint(
            self.module,
            *args,
            use_reentrant=self.use_reentrant,
            **kwargs,
        )


def apply_checkpointing(model: nn.Module, layer_class: type,
                        use_reentrant: bool = False) -> nn.Module:
    """Apply gradient checkpointing to specific layer types."""
    for name, module in model.named_modules():
        if isinstance(module, layer_class):
            parent_name = ".".join(name.split(".")[:-1])
            child_name = name.split(".")[-1]
            parent = dict(model.named_modules()).get(parent_name)
            if parent:
                setattr(parent, child_name, CheckpointedModule(module, use_reentrant))
    return model


def selective_checkpointing(module: nn.Module, checkpoint_attention: bool = True,
                           checkpoint_ffn: bool = True) -> nn.Module:
    """Apply checkpointing selectively to attention and/or FFN layers."""
    from transformers.models.llama.modeling_llama import LlamaAttention, LlamaMLP

    for name, child in module.named_children():
        if checkpoint_attention and isinstance(child, LlamaAttention):
            setattr(module, name, CheckpointedModule(child))
        elif checkpoint_ffn and isinstance(child, LlamaMLP):
            setattr(module, name, CheckpointedModule(child))
        else:
            selective_checkpointing(child, checkpoint_attention, checkpoint_ffn)
    return module


def estimate_memory_savings(model_params_b: float, seq_len: int = 4096,
                           batch_size: int = 2, num_layers: int = 32,
                           checkpoint: bool = True) -> dict:
    """Estimate memory savings from gradient checkpointing."""
    hidden_dim = int((model_params_b * 1e9 / num_layers / 12) ** 0.5)

    # Activation memory per layer (rough estimate)
    # Attention: O(seq_len^2), FFN: O(seq_len * hidden_dim)
    attn_mem = batch_size * seq_len * seq_len * 4  # bytes
    ffn_mem = batch_size * seq_len * hidden_dim * 8  # 2 linear layers
    per_layer = attn_mem + ffn_mem
    total_activation = per_layer * num_layers

    if checkpoint:
        # Only store one layer's activations at a time
        checkpointed = per_layer  # one layer
        recomputation = total_activation * 0.3  # 30% overhead
        total_memory = checkpointed + recomputation
    else:
        total_memory = total_activation

    return {
        "without_checkpoint_gb": round(total_activation / (1024**3), 2),
        "with_checkpoint_gb": round(total_memory / (1024**3), 2),
        "savings_gb": round((total_activation - total_memory) / (1024**3), 2),
        "savings_percent": round((1 - total_memory / total_activation) * 100, 1),
        "compute_overhead_percent": 30 if checkpoint else 0,
    }


class GradientCheckpointingConfig:
    def __init__(self, enabled: bool = True, granularity: str = "layer",
                 use_reentrant: bool = False, selective: bool = False):
        self.enabled = enabled
        self.granularity = granularity  # "layer", "sublayer", "attention_only"
        self.use_reentrant = use_reentrant
        self.selective = selective

    def apply(self, model: nn.Module) -> nn.Module:
        if not self.enabled:
            return model

        if hasattr(model, "gradient_checkpointing_enable"):
            model.gradient_checkpointing_enable(
                gradient_checkpointing_kwargs={"use_reentrant": self.use_reentrant}
            )
            return model

        if self.granularity == "layer":
            from transformers.models.llama.modeling_llama import LlamaDecoderLayer
            return apply_checkpointing(model, LlamaDecoderLayer, self.use_reentrant)
        elif self.selective:
            return selective_checkpointing(model)

        return model
```

## Best Practices

1. **Always enable for models > 3B** — Activation memory dominates GPU usage for large models; checkpointing is essential
2. **Use `use_reentrant=False`** — The non-reentrant implementation is more compatible with autograd and distributed training
3. **Start with layer-level checkpointing** — Checkpointing entire transformer layers is simple and effective
4. **Consider selective checkpointing** — Checkpoint attention (most memory) while keeping FFN activations for less overhead
5. **Combine with Flash Attention** — Flash Attention already reduces attention memory; checkpointing handles the rest
6. **Profile memory usage** — Use `torch.cuda.memory_summary()` to verify checkpointing is working as expected
7. **Account for 30% compute overhead** — Budget for ~30% longer training time when enabling checkpointing
8. **Use with gradient accumulation** — Checkpointing + gradient accumulation maximizes batch size on limited memory
9. **Test backward pass correctness** — Verify that gradients match between checkpointed and non-checkpointed training
10. **Consider CPU offloading for extreme cases** — For very large models, offload activations to CPU instead of recomputing

## Common Pitfalls

- **Using use_reentrant=True**: The reentrant implementation has compatibility issues with some autograd operations
- **Not accounting for compute overhead**: 30% more compute means 30% longer training; plan accordingly
- **Checkpointing everything**: Some small layers don't save much memory when checkpointed but still incur overhead
- **Forgetting to enable for evaluation**: Checkpointing should be disabled during evaluation (no backward pass needed)
- **Memory fragmentation**: Checkpointing can cause GPU memory fragmentation; use `torch.cuda.empty_cache()` periodically
- **Not combining with other techniques**: Checkpointing alone may not be enough; combine with gradient accumulation and mixed precision

## References

- [Training Deep Nets with Sublinear Memory Cost](https://arxiv.org/abs/1604.06174) — Original gradient checkpointing paper
- [Gradient Checkpointing in PyTorch](https://pytorch.org/docs/stable/checkpoint.html) — Official documentation
- [Torch.utils.checkpoint](https://pytorch.org/docs/stable/checkpoint.html) — API reference
