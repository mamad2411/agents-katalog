---
name: "distributed-training-patterns"
description: "Distributed training patterns with code: a PyTorch DDP loop, FSDP with a transformer auto-wrap policy, DeepSpeed ZeRO-3 configuration, AMP with GradScaler, gradient checkpointing, and data loading across ranks. Use when scaling training past one GPU."
---

# Distributed Training Patterns

Expert patterns for DDP, FSDP, DeepSpeed, and mixed precision training across multiple GPUs.

## Pattern 1: PyTorch DDP Training Loop

Standard DDP setup with torchrun launcher, DistributedSampler, and proper cleanup.

```python
# train_ddp.py
import os
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler

def setup(rank: int, world_size: int):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'
    dist.init_process_group(backend="nccl", rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)

def cleanup():
    dist.destroy_process_group()

def train(rank: int, world_size: int, model_cls, dataset, epochs: int = 10):
    setup(rank, world_size)

    # Model
    model = model_cls().to(rank)
    ddp_model = DDP(model, device_ids=[rank])

    # Data: each rank sees a disjoint shard
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank, shuffle=True)
    loader = DataLoader(dataset, batch_size=32, sampler=sampler, num_workers=4, pin_memory=True)

    optimizer = torch.optim.AdamW(ddp_model.parameters(), lr=3e-4)
    criterion = torch.nn.CrossEntropyLoss()

    for epoch in range(epochs):
        sampler.set_epoch(epoch)  # critical: re-shuffle each epoch
        ddp_model.train()

        for batch_idx, (x, y) in enumerate(loader):
            x, y = x.to(rank, non_blocking=True), y.to(rank, non_blocking=True)
            optimizer.zero_grad()
            logits = ddp_model(x)
            loss = criterion(logits, y)
            loss.backward()  # all-reduce gradients across ranks
            torch.nn.utils.clip_grad_norm_(ddp_model.parameters(), max_norm=1.0)
            optimizer.step()

        # Log only from rank 0
        if rank == 0:
            print(f"Epoch {epoch}: loss={loss.item():.4f}")

    # Save checkpoint from rank 0 only
    if rank == 0:
        torch.save(ddp_model.module.state_dict(), "model.pt")

    cleanup()

if __name__ == "__main__":
    # torchrun handles rank assignment via environment variables
    rank = int(os.environ["LOCAL_RANK"])
    world_size = int(os.environ["WORLD_SIZE"])
    train(rank, world_size, MyModel, my_dataset)
```

```bash
# Launch on single node with 4 GPUs
torchrun --nproc_per_node=4 --nnodes=1 train_ddp.py

# Launch on 2 nodes, 8 GPUs each (from node 0)
torchrun --nproc_per_node=8 --nnodes=2 \
  --node_rank=0 --master_addr="10.0.0.1" --master_port=12355 \
  train_ddp.py
```

## Pattern 2: FSDP with Transformer Auto-Wrap Policy

Use FSDP for models that don't fit on a single GPU, wrapping at transformer block granularity.

```python
import torch
from torch.distributed.fsdp import (
    FullyShardedDataParallel as FSDP,
    MixedPrecision,
    ShardingStrategy,
    CPUOffload,
    FullStateDictConfig,
    StateDictType,
)
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
from transformers import LlamaForCausalLM, LlamaConfig
from transformers.models.llama.modeling_llama import LlamaDecoderLayer
import functools

def build_fsdp_model(rank: int):
    # Mixed precision: BF16 params/activations, FP32 for reductions
    bf16_policy = MixedPrecision(
        param_dtype=torch.bfloat16,
        reduce_dtype=torch.float32,
        buffer_dtype=torch.bfloat16,
    )

    # Wrap each LlamaDecoderLayer independently
    wrap_policy = functools.partial(
        transformer_auto_wrap_policy,
        transformer_layer_cls={LlamaDecoderLayer}
    )

    model = LlamaForCausalLM(LlamaConfig())

    fsdp_model = FSDP(
        model,
        auto_wrap_policy=wrap_policy,
        mixed_precision=bf16_policy,
        sharding_strategy=ShardingStrategy.FULL_SHARD,  # ZeRO-3 equivalent
        device_id=rank,
        use_orig_params=True,  # required for torch.compile compatibility
    )
    return fsdp_model

def save_fsdp_checkpoint(model: FSDP, path: str, rank: int):
    """Save full state dict from rank 0."""
    save_policy = FullStateDictConfig(offload_to_cpu=True, rank0_only=True)
    with FSDP.state_dict_type(model, StateDictType.FULL_STATE_DICT, save_policy):
        state_dict = model.state_dict()
    if rank == 0:
        torch.save(state_dict, path)
```

## Pattern 3: DeepSpeed ZeRO-3 Configuration

DeepSpeed config JSON for ZeRO Stage 3 with BF16 and gradient checkpointing.

```json
{
  "train_batch_size": 256,
  "gradient_accumulation_steps": 8,
  "train_micro_batch_size_per_gpu": 4,
  "bf16": {
    "enabled": true
  },
  "gradient_clipping": 1.0,
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {
      "device": "none"
    },
    "offload_param": {
      "device": "none"
    },
    "overlap_comm": true,
    "contiguous_gradients": true,
    "sub_group_size": 1e9,
    "reduce_bucket_size": "auto",
    "stage3_prefetch_bucket_size": "auto",
    "stage3_param_persistence_threshold": "auto",
    "stage3_max_live_parameters": 1e9,
    "stage3_max_reuse_distance": 1e9,
    "gather_16bit_weights_on_model_save": true
  },
  "activation_checkpointing": {
    "partition_activations": true,
    "cpu_checkpointing": false,
    "contiguous_memory_optimization": true,
    "synchronize_checkpoint_boundary": false
  }
}
```

```python
import deepspeed

def init_deepspeed(model, optimizer, ds_config_path: str):
    engine, optimizer, _, lr_scheduler = deepspeed.initialize(
        model=model,
        optimizer=optimizer,
        config=ds_config_path,
    )
    return engine, optimizer, lr_scheduler

# Training loop with DeepSpeed engine
def train_step(engine, batch):
    x, y = batch
    logits = engine(x)
    loss = criterion(logits, y)
    engine.backward(loss)   # handles gradient scaling
    engine.step()           # handles optimizer step + gradient sync
    return loss.item()
```

## Pattern 4: Mixed Precision with AMP + GradScaler

FP16 training with loss scaling for models on non-Ampere GPUs (no native BF16).

```python
import torch
from torch.cuda.amp import autocast, GradScaler

def train_amp(model, loader, optimizer, epochs: int):
    scaler = GradScaler()

    for epoch in range(epochs):
        for x, y in loader:
            x, y = x.cuda(), y.cuda()
            optimizer.zero_grad()

            # Forward pass in FP16
            with autocast(dtype=torch.float16):
                logits = model(x)
                loss = criterion(logits, y)

            # Backward with scaled loss (prevents FP16 underflow)
            scaler.scale(loss).backward()

            # Unscale before clipping
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

            # Step and update scale factor
            scaler.step(optimizer)
            scaler.update()

# Memory savings: FP16 activations ~2x less memory than FP32
# Watch for: loss going NaN (lower lr), scale factor dropping (unstable training)
```

## Pattern 5: Gradient Checkpointing for Memory

Trade compute for memory by recomputing activations in backward pass instead of storing them.

```python
from torch.utils.checkpoint import checkpoint

class MemoryEfficientTransformer(torch.nn.Module):
    def __init__(self, num_layers: int, d_model: int):
        super().__init__()
        self.layers = torch.nn.ModuleList([
            TransformerBlock(d_model) for _ in range(num_layers)
        ])

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for layer in self.layers:
            # Use gradient checkpointing every block
            # Saves activation memory at cost of ~33% extra compute
            x = checkpoint(layer, x, use_reentrant=False)
        return x

# Memory math (approximate):
# Without checkpointing: activations = batch_size × seq_len × d_model × num_layers × 2 bytes
# With checkpointing: activations = batch_size × seq_len × d_model × 2 bytes (only last layer)
# For 24-layer model: ~24x activation memory reduction

# In HuggingFace:
model.gradient_checkpointing_enable()
```

## Pattern 6: Efficient Data Loading Across Ranks

Prevent CPU data loading from bottlenecking GPU training.

```python
from torch.utils.data import DataLoader, DistributedSampler, Dataset
import torch

class ShardedDataset(Dataset):
    """Pre-shard data to disk per rank to avoid redundant reads."""
    def __init__(self, data_path: str, rank: int, world_size: int, transform=None):
        import pyarrow.parquet as pq
        # Read only this rank's shard
        self.data = pq.read_table(f"{data_path}/shard_{rank:04d}.parquet").to_pandas()
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        x = torch.tensor(row['features'], dtype=torch.float32)
        y = torch.tensor(row['label'], dtype=torch.long)
        if self.transform:
            x = self.transform(x)
        return x, y

def build_dataloader(dataset, world_size: int, rank: int, batch_size: int):
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    return DataLoader(
        dataset,
        batch_size=batch_size,
        sampler=sampler,
        num_workers=4,          # 4 workers per GPU is usually optimal
        pin_memory=True,        # enables async CPU→GPU transfer
        prefetch_factor=2,      # prefetch 2 batches per worker
        persistent_workers=True # keep workers alive between epochs
    )
```

## Anti-Patterns

### Anti-Pattern 1: Not Calling sampler.set_epoch(epoch)
Without this, `DistributedSampler` uses the same shuffle each epoch. Every GPU sees the same sequence of examples across epochs, destroying regularization benefit of shuffling.

### Anti-Pattern 2: Saving Checkpoint from All Ranks
Every rank saving the full checkpoint wastes storage and causes I/O contention. Only rank 0 saves. For FSDP use `FullStateDictConfig(rank0_only=True)`.

### Anti-Pattern 3: ZeRO-3 Without Understanding Communication Cost
ZeRO-3 all-gathers parameters before every forward pass. For small models, communication overhead exceeds memory savings. Profile before adopting ZeRO-3; ZeRO-2 is often sufficient and faster.

### Anti-Pattern 4: Large Batch Size Without LR Scaling
Linear scaling rule: if you increase batch size k×, increase learning rate k× and use a linear warmup. Ignoring this causes slower convergence or training instability at large scale.

### Anti-Pattern 5: FP16 with LLMs on A100
A100 and H100 have native BF16 support. BF16 has the same dynamic range as FP32 (8 exponent bits vs 5 for FP16), making it far more stable for large model training. Always use BF16 on Ampere/Hopper, FP16 on Volta/Turing.
