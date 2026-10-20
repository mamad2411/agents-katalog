---
description: Spawn ClawTeam parallel workers for the current development phase
argument-hint: Optional phase override (foundation, algorithms, advanced, finetune)
---

# Spawn Team

Spawn a team of parallel ClawTeam workers, each in an isolated git worktree, to work on independent modules simultaneously.

## Steps

### Step 1: Determine current phase

Run `bash score.sh --quick` and read `.score` to determine the phase.

If user specified a phase ($ARGUMENTS), use that instead.

### Step 2: Spawn workers based on phase

Execute the appropriate clawteam commands:

#### Phase: foundation (score < 0.05)
Do NOT spawn workers. Tell the user: "Foundation phase should be done with `/develop foundation` (single agent). The project needs CMakeLists.txt, headers, and type definitions before parallel work can begin."

#### Phase: algorithms (score 0.05 ~ 0.30)
```bash
clawteam team spawn-team tq-alg -d "quant.cpp core algorithms"

clawteam spawn --team tq-alg --agent-name polar --workspace --repo . \
  --task "Implement PolarQuant algorithm. Read CLAUDE.md for full context. Read refs/PolarQuant/models/modeling_llama_polar.py lines 135-157 and refs/PolarQuant/models/kernel4group.py lines 14-81 for the algorithm. Create src/core/tq_polar.c with tq_polar_quantize_ref(), tq_polar_dequantize_ref(), tq_polar_attention_ref(). Create tests/test_polar.cpp with Google Test. Run bash score.sh --quick to verify. ONLY modify: src/core/tq_polar.*, tests/test_polar.*"

clawteam spawn --team tq-alg --agent-name qjl --workspace --repo . \
  --task "Implement QJL algorithm. Read CLAUDE.md for full context. Read refs/QJL/models/llama2_utils_qjl.py lines 7-185 for the algorithm. Create src/core/tq_qjl.c with tq_qjl_init_projection(), tq_qjl_quantize_ref(), tq_qjl_detect_outliers(), tq_qjl_attention_ref(). Create tests/test_qjl.cpp with Google Test. Run bash score.sh --quick to verify. ONLY modify: src/core/tq_qjl.*, tests/test_qjl.*"

clawteam spawn --team tq-alg --agent-name uniform --workspace --repo . \
  --task "Implement uniform baseline and value quantization. Read CLAUDE.md for full context. Create src/core/tq_uniform.c (min-max 2/4-bit), src/core/tq_value_quant.c (value cache quantization). Create tests/test_uniform.cpp and tests/test_value.cpp. Run bash score.sh --quick to verify. ONLY modify: src/core/tq_uniform.*, src/core/tq_value_quant.*, tests/test_uniform.*, tests/test_value.*"
```

#### Phase: advanced (score 0.30 ~ 0.60)
```bash
clawteam team spawn-team tq-adv -d "quant.cpp advanced features"

clawteam spawn --team tq-adv --agent-name turbo --workspace --repo . \
  --task "Implement quant.cpp composite (PolarQuant + QJL). Read CLAUDE.md. Create src/core/tq_turbo.c combining polar stage 1 + qjl residual stage 2. Create tests/test_turbo.cpp. ONLY modify: src/core/tq_turbo.*, tests/test_turbo.*"

clawteam spawn --team tq-adv --agent-name cache --workspace --repo . \
  --task "Implement paged cache and progressive compression. Read CLAUDE.md. Read refs/vllm/csrc/cache_kernels.cu for patterns. Create src/cache/tq_paged_cache.c and src/cache/tq_progressive.c with tests. ONLY modify: src/cache/**, tests/test_paged_cache.*, tests/test_progressive.*"

clawteam spawn --team tq-adv --agent-name simd --workspace --repo . \
  --task "Implement NEON and AVX2 optimized kernels. Read CLAUDE.md. Read refs/llama.cpp/ggml/src/ggml-cpu/arch/arm/quants.c for NEON patterns. Create src/backend/cpu/tq_generic.c, tq_neon.c, tq_avx2.c, tq_cpu_dispatch.c. ONLY modify: src/backend/cpu/**"

clawteam spawn --team tq-adv --agent-name bench --workspace --repo . \
  --task "Create benchmarks and specs. Read CLAUDE.md. Create bench/tq_bench.cpp (output: quantize_throughput=N, attention_throughput=N, compression_ratio=N, simd_speedup=N). Create bench/tq_quality.cpp (output: roundtrip_mse=N, attention_cosine=N, cross_platform=pass/fail). Create spec/tq_format_v1.md and spec/tq_operators_v1.md. ONLY modify: bench/**, spec/**"
```

#### Phase: finetune (score > 0.60)
Do NOT spawn workers. Tell the user: "Fine-tuning phase is best done with `/develop` (single agent) for precision. Focus on the lowest-scoring dimension."

### Step 3: Monitor

Tell the user how to monitor:
```bash
clawteam board attach <team-name>     # Live tmux view
clawteam task list <team-name>         # Task status
watch -n 30 bash score.sh --quick      # Score tracking
```

### Step 4: After workers complete

Tell the user to run the merge gate:
```bash
# Wait for completion
clawteam task wait <team-name> --timeout 1800

# Then merge each worker's branch one-by-one:
# git merge clawteam/<team>/<worker> --no-edit
# bash score.sh --quick
# If score dropped: git reset --hard HEAD~1
```

Or suggest running `/harness` which automates the merge gate.
