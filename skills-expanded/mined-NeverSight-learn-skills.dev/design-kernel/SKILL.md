---
name: design-kernel
description: >
    Shared kernel design workflow across all supported languages and DSLs. Provides language
    selection table, naming conventions, versioning rules, KernelPlan structure, composition
    patterns, clone workflow, implementation workflow, devlog template, and designer output
    contract. Use when: (1) choosing which language-specific kernel design skill to load,
    (2) the intended implementation language is not fixed yet, (3) you need naming or
    versioning guidance before selecting a DSL, (4) you are implementing any kernel regardless
    of DSL, (5) you are updating docs that refer to kernel design skills.
---

# Kernel Design — Shared Workflow

This skill contains everything that is common across all supported DSLs. Once the implementation language is known, **also** load the matching language-specific design skill for DSL-specific runtime patterns, pitfalls, and API guidance.

## Language Selection

| Language key | Python package path | Design skill | API reference skill | Use when |
|--------------|---------------------|--------------|---------------------|----------|
| `cutile-dsl` | `cutile` | `/design-cutile-dsl-kernel` | `/cutile-dsl-ref` | Block-level control, tiling, CTA remapping, compiler hints are sufficient |
| `cute-dsl` | `cute_python` | `/design-cute-dsl-kernel` | `/cute-dsl-ref` | Explicit thread/warp scheduling, TMA pipelines, shared memory control needed |

---

## Naming Conventions

- Public-facing names, docs, skills, and knowledge-base entries use **kebab-case** language keys (e.g., `cute-dsl`).
- Python packages use **underscores** where required (e.g., `cute_python`).
- Kernel package nesting: `src/mla_var3/kernel/<lang_pkg>/mla/<design>/...`.
- The shortcut CLI `python -m mla_var3.kernel <kernel> [<version>]` is the preferred user-facing entry point.

## Kernel Structure and Versioning

We use a nested structure for kernel packages inside the `kernel` sub-package:

1. **Language level**: which DSL the kernel is implemented in (e.g., `kernel.cutile`, `kernel.cute_python`).
2. **Layer level**: which model layer the kernel targets (e.g., `kernel.cutile.mla`).
3. **Design level**: the kernel design (e.g., `kernel.cutile.mla.flash_mla`).
4. **Version level**: the kernel version (e.g., `kernel.cutile.mla.flash_mla.flash_mla_v2`). The first version has no suffix and is called the "base version".
5. **Entry module**: inside the version package, a module named after the version's full name (e.g., `flash_mla_v2.py`) must contain the `KernelPlan` subclass.

### Package Nesting Pattern

```
kernel.<lang_pkg>.mla.<design>.<design>[_v<N>].<design>[_v<N>].py
```

### Rules

- Base version: `<design>/<design>/` (no suffix, aliased as v0)
- Version N: `<design>/<design>_vN/`
- Kernel entry function name MUST match the module filename
- Each version is a sibling package under the design package

### CLI Usage

```bash
# Full path
python -m mla_var3.kernel.<lang_pkg>.mla.<design> [<version>] [args]
# Shortcut (discovers across all languages)
python -m mla_var3.kernel <design> [<version>] [args]

# Examples
python -m mla_var3.kernel.cutile.mla.mla_var6_plus v4 --b=32 --s=16 --t=4096
python -m mla_var3.kernel mla_var6_plus v4 --b=32 --s=16 --t=4096
```

---

## Version Creation Checklist

1. Clone the previous version:
    ```bash
    source .venv/bin/activate
    python ./scripts/clone-kernel.py <kernel_full_name> <new_suffix>
    ```
2. The script rewrites versioned symbols automatically:
    - Python module filenames
    - Decorated kernel function names (`@ct.kernel`, `@cute.kernel`, `@cute.jit`)
    - `KernelPlan` subclass names
    - `Tiling` subclass names
    - Intra-package imports
    - Quoted forward references and embedded package-name string literals
3. Modify the cloned files to implement the new optimization.
4. Manual fallback if the script is unavailable:
    - Copy the latest version directory
    - Rename the versioned module files
    - Update class names, function names, imports, and pipeline name strings by hand
5. Verify correctness:
    ```bash
    source .venv/bin/activate
    python -m mla_var3.kernel.<lang_pkg>.mla.<design> <version> --prof_type=disabled --check
    ```
6. Update devlog with "What changed" section.

---

## KernelPlan Structure

Every kernel version must implement a `KernelPlan` subclass. The `plan()` method returns a DSL-specific runtime wrapper (see the language-specific skill for the concrete type).

```python
@dataclass
class MyKernel(KernelPlan):
    b: int = 64; s: int = 1; t: int = 4096  # problem dimensions
    tiling: MyTiling = field(default_factory=MyTiling)

    def prepare_inputs(self, device) -> tuple:
        # Allocate and return input tensors

    def reference_fn(self, *inputs) -> tuple:
        # Reference implementation for --check

    def _autotune_configs(self) -> list[MyTiling]:
        # Candidate tiling configs for autotuner search

    def _algorithmic_flops_bytes(self, tiling) -> tuple[int, int]:
        # Analytical (FLOPs, bytes) for roofline

    def plan(self, *inputs) -> BenchmarkFn:
        # Build executable runtime object (DSL-specific)

    def plan_empty(self, peak_tflops, peak_gbps) -> BenchmarkFn:
        # Roofline-only prediction (no real tensors)
```

## Tiling Dataclass

```python
@dataclass
class MyTiling(Tiling):
    # DSL-specific fields — see the language-specific skill for examples

    def validate(self, pd: "MyKernel") -> bool:
        # Return True if this tiling is valid for the given problem dimensions
        ...
```

## Composition Patterns

### Sequential pipeline

```python
def plan(self, *inputs) -> KernelPipeline:
    stage1 = stage1_plan.plan(...)
    stage2 = stage2_plan.plan(...)
    return KernelPipeline(_name="my_pipeline", stages=[stage1, stage2])
```

### Concurrent stages + sequential combine

```python
def plan(self, *inputs) -> KernelPipeline:
    a = plan_a.plan(...)
    b = plan_b.plan(...)
    concurrent = ConcurrentKernels(
        _name="overlap_group", concurrent_kernels=[a, b],
        validate_joint_tiling_fn=validate_fn,
    )
    combine = combine_plan.plan(...)
    return KernelPipeline(_name="pipeline", stages=[concurrent, combine])
```

---

## Implementation Workflow

1. **Read current kernel source** — understand the existing implementation
2. **Read optimization instructions** from orchestrator (specific optimizations to apply)
3. **Load the DSL API reference skill** — do not hallucinate APIs
4. **Check the DSL suitability gate** (in the language-specific skill) before implementing
5. **Clone the current version** with `python ./scripts/clone-kernel.py`
6. **Read optimization detail files** from `docs/knowledge/` for implementation patterns
7. **Implement changes** in the new version files
8. **Test correctness**: `--prof_type=disabled --check`
9. **Update devlog** with "What changed" and "High-level description"
10. **If committing**, use a Conventional Commits message

---

## Knowledge Base Links

- Put reusable algorithmic/device/hardware findings in `docs/knowledge/optimizations/` or `docs/knowledge/anti-patterns/`.
- Put DSL-specific implementation findings in `docs/knowledge/languages/<language>/...`.
- Use the language-specific optimization catalog skill together with the language-specific design skill.

## Development Log Entry Template

Add to `docs/kernels/<kernel>.md` under `## Development log`:

```markdown
### V<N>: [Brief Description]

**Location**: `src/mla_var3/kernel/<lang_pkg>/mla/<kernel>/<kernel>_v<N>/`

**What changed**:
- [Bullet list of changes]

**High-level description of main code changes**:
- [Description of optimizations and how they relate to profiling insights]
```

Performance metrics, bottleneck analysis, issues, and insights are filled by the profiler agent after profiling.

## Designer Output Contract

Return results to the orchestrator in this format:

```markdown
## New Version: [kernel] [version]

### Changes Applied
1. [change + rationale]

### Files
- Created: [paths]
- Modified: [paths]

### Correctness: [PASS/FAIL]

### Devlog Entry Written: [path]
```

## References

- **Optimization patterns**: `docs/knowledge/optimizations/`
- **Anti-patterns**: `docs/knowledge/anti-patterns/`
- **Kernel devlogs**: `docs/kernels/<kernel>.md`
