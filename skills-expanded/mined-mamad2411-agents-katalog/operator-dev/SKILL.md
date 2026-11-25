---
name: operator-dev
description: Structured workflow for SIPU operator development in torch_sipu. Use when implementing, modifying, fixing, or refactoring operators, for infrastructure changes that affect operator behavior, or for addressing MR review feedback from colleagues.
---

# torch_sipu Operator Development Workflow

You are working in the torch_sipu repository — a PyTorch device backend extension for SIPU hardware. When the user asks you to add, modify, or refactor an operator or its underlying infrastructure, you MUST follow the steps below in order. Do not skip steps.

---

## Entry: Detect Scenario

Before doing anything, classify the user's request into one of two scenarios and **state it explicitly**:

### Scenario A — New / Ongoing Development
User wants to implement, refactor, or modify an operator from scratch (or continue in-progress work).

**Signals:** "implement X", "refactor X", "add dtype support for X", "fix bug in X kernel", no MR mentioned.

**Action:**

1. **Branch Guard (MANDATORY):** Follow the Branch Guard from the **dev-workflow** skill — check current branch and create a feature branch if needed. Do NOT proceed until on a feature branch.
2. Proceed to **Step 0**.

### Scenario B — Handling MR Review Feedback
User has already submitted an MR and received review comments from a colleague that need to be addressed.

**Signals:** "reviewer said", "MR rejected", "MR comment", "CR feedback", "review feedback", "colleague said", paste of review comments.

**Action:** **Skip Step 0 entirely. Jump directly to Step 8.** (Branch already exists.)

---

## Step 0: Determine Change Scope

> **Prerequisite:** You MUST already be on a feature branch (enforced by Entry Branch Guard above).

### 0.1 Create JIRA Ticket (If Needed)

Before starting development, check if a JIRA ticket exists. If not, **ask the user** whether to create one.

> **Reference:** Read `.codex/skills/operator-dev/refs/jira-mr-automation.md` §1 for the JIRA ticket creation script.

### 0.2 Classify the Change

| Change Type | Scope | CI Label |
|---|---|---|
| **New Triton op** | Python kernel + registration + tests | `triton` |
| **New C++ op** | `.su`/`.cpp` + YAML + tests | `sikernel` |
| **New op (both backends)** | Triton + C++ + tests | `sikernel` or `triton` |
| **Refactor `.cpp` → `.su`** | Replace `.cpp` with `.su`, update YAML | `sikernel` |
| **Bug fix (kernel)** | Modify existing kernel + add regression test | `sikernel` or `triton` |
| **Bug fix (registration)** | Fix YAML or dispatcher registration | `aten` |
| **Infrastructure change** | Headers (`.suh`), utilities, build | `sikernel` |

### 0.3 Understand the Op

Before writing any code:

1. **Read the PyTorch documentation** for the op (if it exists in upstream ATen).
2. **Read the upstream CUDA implementation** to understand the algorithm.
3. **Check if the op is `CompositeImplicitAutograd`** — if it auto-decomposes, do NOT register it unless you have a performance reason for a fused kernel:
   ```bash
   python -c "import torch; print(torch._C._dispatch_dump('aten::<op>'))"
   ```

---

## Step 1: Locate Files and Understand Architecture

### 1.0 Identify the Correct Dispatch Mechanism

- **DispatchStub** (`REGISTER_PRIVATEUSE1_DISPATCH`) — for TensorIterator-based ops
- **Structured Kernel** (`TORCH_SIPU_IMPL_FUNC`) — for complex ops needing custom shape setup
- **use_native_impl: True** — for metadata-only ops (view, reshape)

### 1.1 Locate Source Files

```bash
find torch_sipu/csrc/aten/native/sipu/ -name "*<Op>*"
find torch_sipu/backends/sipu_triton_kernels/ops/ -name "*<op>*"
grep -r "<op>" torch_sipu/csrc/aten/native/native_functions.yaml
grep -r "<op>" torch_sipu/backends/sipu_triton_kernels/__init__.py
```

> **Reference:** Read `.codex/skills/operator-dev/refs/dispatch-guide.md` for the complete dispatch mechanism decision tree, stub header reference, YAML entry patterns, and operator category quick reference.

### 1.2 Present the File List

Before making any edits, output a table of files to modify and files NOT modified. **Rule: if a file is not in this table, do not touch it.**

---

## Step 2: Enforce Minimal Modification Principle

- [ ] Every file in the change list has a clear reason tied to the operator task.
- [ ] No formatting-only changes to lines you did not otherwise modify.
- [ ] No drive-by refactors, comment additions, or import reordering in unrelated code.
- [ ] No new abstractions or helper functions unless the op genuinely requires them.
- [ ] If modifying an existing op, the diff should touch only the lines relevant to the change.

---

## Step 2.5: Optimization Strategy Selection (MANDATORY)

Before writing any code, use the hardware optimization decision engine to determine the implementation strategy.

> **Reference:** Read `.codex/skills/operator-dev/refs/hardware-optimization-guide.md` for the complete decision engine, hardware architecture summary, implementation pattern library, and similar-op reference matching.

### 2.5.1 Classify the Operator

| Category | Examples | Typical Path |
|----------|----------|--------------|
| **E1: Unary element-wise** | neg, sigmoid, silu, rsqrt | PATH-A: TensorIterator + Tile→RVV→Scalar |
| **E2: Binary element-wise** | add, mul, sub, div | PATH-A: with `*_with_scalars*` variants |
| **C: Comparison** | eq, ne, gt, ge | PATH-A: with CompareVec |
| **R1: Simple reduction** | sum, prod, any, all | PATH-A-REDUCE: Reduce.suh |
| **R2: Compound reduction** | softmax, layernorm, rmsnorm | PATH-B: parallel_for + VectorizedM1 |
| **M: Matrix** | mm, bmm, attention | PATH-C or Triton |
| **S: Structural** | cat, topk, sort | PATH-B or PATH-C |
| **X: Custom SIPU** | mm_t2t, flash_attention | PATH-C: sikernel library |

### 2.5.2 State the Strategy

Output the selected strategy before proceeding:

```
Op category: E1 (unary element-wise)
Execution path: PATH-A — TensorIterator + Tile→RVV→Scalar cascade
Precision: Standard M1→M2 widening for bf16/fp16
Reference impl: silu in UnaryOpsKernel.su (most similar)
```

> **Vec library reference:** When implementing the vectorized path, consult `.codex/skills/operator-dev/refs/vec-library-guide.md` for the complete API reference.

---

## Step 3: Implement the Operator

### 3.0 License Header (New Files Only)

Every **new** source file MUST start with the Apache v2.0 license header. Use the file's creation year and the correct comment syntax. Full template is in CLAUDE.md.

### 3.1 Triton Backend Implementation

> **Reference:** Read `.codex/skills/operator-dev/refs/triton-template.md` for the complete Triton template, decorator stack, preprocessing configs, and registration guide.

Key: Create `ops/<op>.py` → export in `ops/__init__.py` → register in `__init__.py` with `_sipu_lib_aten.impl()`.

### 3.2 C++ Kernel Implementation

> **Reference:** Read `.codex/skills/operator-dev/refs/cpp-template.md` for Option A (DispatchStub `.su`), Option B (Structured kernel `.su`), and Option C (host-only `.cpp`).

Key points:
- **Option A** (element-wise/reduction): Tile → RVV → Scalar cascade + `REGISTER_PRIVATEUSE1_DISPATCH`
- **Option B** (complex ops): `TORCH_SIPU_IMPL_FUNC` + `parallel_for` + `VectorizedM1`
- **Option C** (sikernel calls): host-only `.cpp`

### 3.3 Forward/Backward & AutogradPrivateUse1

> **Inference Backend:** Do NOT implement backward. Register `AutogradPrivateUse1` ONLY for metadata ops (`to.dtype`, `type_as`) or in-place ops conflicting with autograd (`_index_put_impl_`).

### 3.4 Refactoring from `.cpp` to `.su`

> **Reference:** Read `.codex/skills/operator-dev/refs/cpp-to-su-migration.md` for the migration workflow and SoftMax example.

---

## Step 4: Build

Triton-only changes (Python files) do NOT require a rebuild.

```bash
conda activate pytorch
source setup_sipu_sdk_env.sh
make install-dev           # Extension only
# OR
make install-all-dev       # Full rebuild (if third_party/sikernel changed)
```

Common failures: `CMAKE_SIPU_COMPILER not found` → forgot SDK env. `clang++ not found` → forgot conda. Stale build → `rm -rf build/`.

---

## Step 5: Performance Review (MANDATORY for C++ Kernels)

> **Reference:** Read `.codex/skills/operator-dev/refs/performance-guide.md` for the performance checklist and anti-patterns. Also consult `.codex/skills/operator-dev/refs/hardware-optimization-guide.md` §5 for the deterministic validation checklist.

Key checks:
1. **Option A ops**: Full Tile → RVV → Scalar cascade?
2. **Option B ops**: `VectorizedM1` in hot loop with scalar tail?
3. **Precision**: bf16/fp16 accumulation in float32?
4. **Numerically-sensitive ops**: ALL intermediates in float32?

State the performance level after review.

---

## Step 6: Write Tests (MANDATORY — Never Skip)

> **Reference:** Read `.codex/skills/operator-dev/refs/test-template.md` for the complete test template and tolerance guidelines.

### Hard Rules

1. **SIPU results MUST match CPU reference** — CPU is the golden implementation.
2. **Use `torch.testing.assert_close`** — never `torch.equal` for floating-point.
3. **Test at least `torch.float32` and `torch.bfloat16`.**
4. **If new dtype support is added, test EVERY new dtype.**
5. **Do NOT test backward gradients** — this is an inference backend.

```bash
CUDA_VISIBLE_DEVICES= PYTORCH_TESTING_DEVICE_ONLY_FOR=sipu pytest test/test_<op>.py -v
TRITON_KERNEL_VERIFY=1 python examples/run_<op>.py    # Triton only
```

---

## Step 7: Output Deliverables

### 7.1 Change Summary

List every file changed with a one-line description.

### 7.2 How to Verify

Provide exact test commands (single file + full suite).

### 7.3 Risk Assessment

Call out: dtype gaps, shape limitations, tolerance concerns, regression risk.

### 7.4 Commit, Lint, Push & Create MR

Follow the **dev-workflow** skill (Steps 3–6) for lint, commit, squash, push, and MR creation. Key points:

1. **Lint**: `make lint` → `lintrunner -a --all-files` to auto-fix.
2. **Commit**: `<type>(<scope>): jira#S1SW-XXXX <description>`. Ask user for Jira number if not provided.
3. **Self-review**: Before pushing, invoke `/pr-review <commit_hash>` to catch issues early.
4. **Squash, rebase & push**: One commit per branch. Rebase onto develop before push.
5. **Create MR**: Use the MR creation script from `.codex/skills/operator-dev/refs/jira-mr-automation.md` §2.

---

## Step 8: Handle MR Review Feedback

> **Reference:** Read `.codex/skills/operator-dev/refs/mr-feedback-guide.md` for the complete review feedback handling workflow (comment classification, fix ordering, commit format, reviewer reply, CI re-trigger).

**Quick summary:** Classify comments → fix in order (bugs → tests → performance → style → design) → fixup commit → reply to reviewer → push → comment `test CI`.

---

## Reference: Key File Paths

```
# Triton backend ops (one file per op)
torch_sipu/backends/sipu_triton_kernels/ops/*.py
torch_sipu/backends/sipu_triton_kernels/ops/__init__.py      # exports
torch_sipu/backends/sipu_triton_kernels/__init__.py           # dispatcher registration

# AI backend ops
torch_sipu/backends/AI/ops/*.py
torch_sipu/backends/AI/__init__.py                            # dispatcher registration

# C++ kernel ops — joint compilation (.su) and host-only (.cpp)
torch_sipu/csrc/aten/native/sipu/*.su                         # joint compilation kernels (modern)
torch_sipu/csrc/aten/native/sipu/*.cpp                        # host-only C++ kernels
torch_sipu/csrc/aten/native/native_functions.yaml             # C++ dispatch registration
torch_sipu/csrc/aten/native/ext_native_functions.yaml         # extension ops (custom ops not in ATen)

# C++ infrastructure headers (.suh) — shared by many ops
torch_sipu/csrc/aten/native/sipu/Loops.suh                    # scalar element-wise loops (sipu_kernel)
torch_sipu/csrc/aten/native/sipu/VecLoops.suh                 # vectorized loops (sipu_kernel_vec)
torch_sipu/csrc/aten/native/sipu/TileLoops.suh                # tiled loops (sipu_kernel_tile)
torch_sipu/csrc/aten/native/sipu/Reduce.suh                   # reduction utilities (vectorized_reduction)
torch_sipu/csrc/aten/native/sipu/Parallel.suh                 # parallel execution (parallel_for, invoke_parallel)
torch_sipu/csrc/aten/native/sipu/Vec.suh                      # vector type utilities
torch_sipu/csrc/aten/native/sipu/Tile.suh                     # tile type utilities

# Triton op utilities
torch_sipu/backends/sipu_triton_kernels/ops/utils.py          # cpu_fallback, precheck_supported_dtypes, request_fallback
torch_sipu/backends/sipu_triton_kernels/ops/verify_decorator.py  # @sipu_verify
torch_sipu/backends/sipu_triton_kernels/ops/preprocessing_framework.py  # @triton_preprocess, *_OP_CONFIG

# Test utilities
torch_sipu/testing/_internal/triton_utils.py                  # skipIfUseSipuTritonKernels, onlySipuTritonKernels
torch_sipu/testing/_internal/common_utils.py

# Tests
test/test_*.py

# Examples
examples/run_*.py
```
