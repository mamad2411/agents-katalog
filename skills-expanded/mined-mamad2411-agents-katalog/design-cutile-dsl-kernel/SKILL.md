---
name: design-cutile-dsl-kernel
description: >
  cuTile Python DSL kernel implementation patterns, CtKernel runtime wrapper, suitability gate,
  and cuTile-specific pitfalls. Use when: (1) creating or modifying a cuTile Python DSL kernel
  version, (2) implementing an optimization that still fits within cuTile's exposed control
  surface, (3) deciding whether cuTile is still the right DSL, (4) reviewing cuTile-specific
  runtime patterns. Always also load /design-kernel for shared naming, versioning, and workflow.
---

# cuTile Python DSL — Language-Specific Guidance

**Prerequisite**: Load `/design-kernel` for shared naming, versioning, KernelPlan structure, composition patterns, clone workflow, devlog template, and designer output contract. This skill covers only cuTile-specific runtime patterns and constraints.

## When To Use cuTile Python DSL

Stay in cuTile Python DSL (`cutile-dsl`) when the next optimization is still expressible through:

- tile sizes and tensor layout choices,
- CTA remapping and work partitioning via `ct.bid()` / `ct.num_blocks()`,
- occupancy and cluster-size hints (`num_ctas`, `occupancy`),
- compiler guidance such as `latency` / `allow_tma` hints,
- multi-stage composition through `KernelPipeline` / `ConcurrentKernels`.

## Suitability Gate

Do not expect cuTile to express explicit intra-CTA scheduling. The public execution model does not expose thread, warp, or warpgroup identity, and does not allow explicit synchronization or communication within a block. Likewise, `num_ctas` does not give you a public cluster programming model: there is no exposed cluster rank, cluster barrier, DSM primitive, or cluster memory scope.

This becomes a hard design constraint when profiling shows the kernel is pinned to one CTA per SM. In that regime, the usual recovery path in state-of-the-art kernels is explicit scheduling inside the CTA: warpgroup seesaw schedules, producer/consumer pipelines, barrier choreography, or cluster-cooperative overlap. If the optimization you need falls in that category, **stop iterating inside cuTile and switch to CuTe DSL** (`/design-cute-dsl-kernel`).

The FlashMLA devlog (`docs/kernels/flash-mla.md`) is the concrete example: the official FlashMLA design remains productive at one resident block per SM because it uses explicit scheduling; cuTile FlashMLA versions cannot reproduce that behavior.

## Naming And Layout

- Public language key: `cutile-dsl`
- Python package path: `cutile`
- Kernel layout: `src/mla_var3/kernel/cutile/<layer>/<design>/<design>[_vN]/`
- Module file: `<design>[_vN].py`
- Main runtime wrapper: `CtKernel`

## CtKernel Runtime Pattern

`CtKernel(Kernel)` wraps cuTile kernels with `grid_fn` and `args_fn` callables:

```python
from mla_var3.runtime import CtKernel, KernelPlan, Tiling, ConstInt, ConstBool

@ct.kernel
def my_kernel(Tensor, ..., Bm: ConstInt, Bn: ConstInt, EVEN_N: ConstBool):
  bid_x = ct.bid(0)
  # block-level operations: ct.load, ct.mma, ct.store, ct.reshape, ...

@dataclass
class CtMyKernel(KernelPlan):
  b: int = 64; s: int = 1; t: int = 4096
  tiling: MyTiling = field(default_factory=MyTiling)

  def plan(self, *inputs) -> CtKernel:
    Out = torch.empty_like(inputs[0])

    def grid_fn(cfg):
      return (math.ceil(s / cfg.Bm), math.ceil(h / cfg.Bh), b)

    def args_fn(cfg):
      return (inputs[0], Out, cfg.Bm, cfg.Bn, (t % cfg.Bn) == 0)

    return CtKernel(
      input_tensors=inputs,
      output_tensors=(Out,),
      kernel_fn=my_kernel,
      grid_fn=grid_fn,
      args_fn=args_fn,
      tiling=self.tiling,
      autotune_configs=self._autotune_configs(),
      algorithmic_flops_bytes_fn=self._algorithmic_flops_bytes,
    )
```

Key fields on `CtKernel`:

| Field | Type | Purpose |
|-------|------|---------|
| `kernel_fn` | `@ct.kernel` function | The cuTile kernel function |
| `grid_fn` | `Callable[[Tiling], tuple]` | Maps tiling config to 3D grid dimensions |
| `args_fn` | `Callable[[Tiling], tuple]` | Maps tiling config to kernel arguments |
| `input_tensors` | `tuple[torch.Tensor]` | For autotuning cache key |
| `output_tensors` | `tuple[torch.Tensor]` | Returned by `__call__` |
| `tiling` | `Tiling` | Current tiling config |
| `autotune_configs` | `list[Tiling]` | Search space for autotuning |
| `algorithmic_flops_bytes_fn` | `Callable` | For roofline analysis |

### Autotuning

`CtKernel` autotuning uses `autotune_launch()` from `cuda.tile_experimental`, which handles occupancy/num_ctas hints automatically. The `_apply_hints()` method re-applies hints after tuning.

### Compilation

`CtKernel.compile()` uses `compile_tile()` to emit `.bytecode` and optionally translates to `.mlir` via `cuda-tile-translate`.

## Tiling Dataclass

cuTile tilings typically include tile dimensions plus optional compiler hints:

```python
@dataclass
class MyTiling(Tiling):
  Bm: int = 16       # query tile size
  Bn: int = 64       # KV tile size
  Bh: int = 8        # heads per block
  num_ctas: int = None   # CGA size (None = auto)
  occupancy: int = None  # occupancy hint (None = auto)

  def validate(self, pd: "CtMyKernel") -> bool:
    return self.Bm <= pd.s and self.Bn <= pd.t and self.Bh <= pd.h
```

## cuTile Constant Types

```python
from mla_var3.runtime import ConstInt, ConstBool, ConstFloat, INV_LOG_2
```

- `ConstInt = ct.Constant[int]` — compile-time integer
- `ConstBool = ct.Constant[bool]` — compile-time boolean
- `ConstFloat = ct.Constant[float]` — compile-time float

## Common Pitfalls

- Never hallucinate cuTile APIs — always verify with `/cutile-dsl-ref` or the official docs
- `@ct.kernel` function name MUST match the module filename
- Register budget: 255 max/thread, aim <128 for good occupancy (validate against the active device's SM limits via `docs/devices/` and `src/mla_var3/conf/devices.json`)
- Shared memory: 48KB/block default, 99KB opt-in, 100KB/SM total
- When reducing tile sizes for occupancy, verify compute efficiency doesn't degrade
- Do not assume `num_ctas` unlocks explicit cluster-cooperative algorithms; in cuTile it is a hint, not a cluster programming interface
- If NCU shows one CTA per SM, low eligible warps, and the missing fix is explicit warpgroup or barrier scheduling, further cuTile-only tuning is unlikely to close the gap

## Knowledge Links

- Shared optimization knowledge: `docs/knowledge/optimizations/`
- Shared anti-patterns: `docs/knowledge/anti-patterns/`
- cuTile-specific optimization overlays: `docs/knowledge/languages/cutile-dsl/`
- cuTile-specific optimization catalog: load `/optimization-catalog-cutile-dsl`

## References

- **Runtime API details**: See the `/design-kernel` skill's runtime-api reference for the complete CtKernel API documentation
- **Kernel templates**: See the `/design-kernel` skill's kernel-templates reference for copyable template code
- **FlashMLA scheduling limit**: See `docs/kernels/flash-mla.md` for the diagnosis comparing cuTile FlashMLA with the official explicitly scheduled implementation