+++
title = "Ascend Profiling Analysis Skill 设计深度解析"
date = 2026-05-28
draft = false
categories = ["Skills"]
tags = ["skills", "ascend", "profiling", "npu", "performance"]
+++

# Ascend Profiling Analysis Skill 设计深度解析

> 本文深度解析一个用于分析 Ascend NPU torch profiler 产出的 skill，涵盖其设计哲学、Pipeline 架构、昇腾核心知识体系和先验知识体系。

## 一、背景与动机

### 为什么需要 profiling 分析？

在昇腾 NPU 上运行 LLM 推理时，的性能调优需要回答几个关键问题：

- **Step 时间去哪了？** attention/FFN/MoE 各占多少？
- **瓶颈在哪？** Cube 计算还是 Vector 内存搬运？
- **EP/TP 负载均衡吗？** 有没有 rank 掉队？
- **通信是否拖后腿？** HCCL collective 是否慢于预期？

传统的分析手段面临几个问题：

| 工具 | 问题 |
|------|------|
| CANN Studio  Timeline | 只能看时序，无法聚合统计 |
| `trace_view.json` | 数据稀疏，难以关联到 kernel 语义 |
| `kernel_details.csv` | 数据量级 GB，需要专门解析逻辑 |

### 设计目标

这个 skill 的核心目标：**从原始 profiling 数据出发，产出带证据链的可追溯报告**。

- 每一条诊断结论都必须能追溯到原始 CSV 的行号
- 支持跨 rank 对齐和异常检测
- 输出 Markdown / Excel / HTML 三种格式

## 二、设计哲学：证据链优先

### 核心理念

> **每个 claim 必须能追溯到原始 row。**

```text
report claim
  → diagnosis finding (diagnosis_findings.json)
  → evidence id (evidence_index.csv)
  → source path + row range (raw_kernel_index.csv)
  → original kernel_details.csv
```

### 置信度分层

| 置信度 | 条件 | 处理方式 |
|--------|------|----------|
| high | 直接 row 证据 + 交叉验证一致 | 直接输出 |
| medium | 直接证据存在，但缺少一个佐证 | 标注后输出 |
| low | 模式可疑，但覆盖不完整 | 标注 limitation |

### 结构 Role vs 实现 Evidence

这是理解整个 skill 的关键：

- **结构 Role** = Paper 术语，表示"这是什么功能块"（MLA、DSA、CSA）
- **实现 Evidence** = Kernel 分类，表示"哪些 kernel 实现这个功能"

```yaml
# 结构 Role (attention_families.yaml)
- family: csa  # Compressed Sparse Attention
  must_have:
    - attention.kv_compressor      # KV 压缩
    - attention.lightning_indexer   # top-k 选择
    - attention.sparse_sharedkv    # 稀疏 KV 共享

# 实现 Evidence (kernel_signatures.yaml)
- profile_name: fusedinferattentionscore
  categories: [attention.flash_score]
  used_by_family: [mla, dsa, hca, gqa_or_mha]
```

**关键洞察**：同一个 kernel（如 `FusedInferAttentionScore`）可以服务多个 architecture。Family 由组合判断，非单个 kernel。

### 确定性优先

```python
# segment.py 开头的设计原则
The segmenter is intentionally deterministic.
It does not use duration percentiles, fuzzy similarity,
expected model layer counts, or "best score" candidate selection.
```

- 层数 = 观测结果，非假设
- 不写死模型名
- 宁可低置信度输出，不输出不可追溯结论

## 三、Pipeline 架构

### 阶段划分

```
normalize → segment → classify → summarize → cross_rank → diagnostics → report
    ↓          ↓         ↓          ↓           ↓           ↓          ↓
 原始CSV   Step切分   Block分解   聚合统计    跨Rank对齐    诊断发现    报告生成
```

### 阶段可复用

```bash
# 从某个阶段重跑，复用上游结果
python3 profile_analyze.py \
  --from-stage classify \
  --remote-output-dir /tmp/previous_run
```

### 远端执行策略

Profiling 数据可能几十 GB，绝不能全量拉回本地。

```bash
# 1. tar-over-ssh 只同步分析框架 (~10MB)
# 2. 远端容器内执行分析
# 3. 只拉回轻量产物 (report/, *manifest.json, *.csv)
```

### Artifact 契约

每个阶段的产出文件固定，其他阶段只依赖 `manifest.json` 校验。

```
segment_manifest.json      # 切分段数、层数、hard_errors
classify_manifest.json   # block 统计、companion_layers
summary_manifest.json    # pipeline 覆盖率
```

## 四、昇腾核心知识体系

### AICore vs AIVector 解耦架构

Atlas A2/A3 的关键架构特征：**Cube 和 Vector 是两个独立的执行单元**。

```
┌─────────────────────────────────────────────────────┐
│                    NPU Die                           │
│  ┌──────────────┐      ┌──────────────┐           │
│  │   AI Core    │      │  AI Vector  │           │
│  │   (Cube)    │      │  (Vector)   │           │
│  │              │      │              │           │
│  │  ┌────────┐ │      │  ┌────────┐ │           │
│  │  │  MAC   │ │      │  │  ALU   │ │           │
│  │  │(矩阵乘) │ │      │  │(向量运算)│ │           │
│  │  └────────┘ │      │  └────────┘ │           │
│  └──────────────┘      └──────────────┘           │
│         ↑                      ↑                    │
│         └────────┴────────────┘                    │
│              解耦执行，互不阻塞                      │
└─────────────────────────────────────────────────┘
```

### Pipeline 时间字段映射

`kernel_details.csv` 暴露了 11 个 pipeline 时间字段（单位 μs）：

| Pipeline | Stage | CSV Column | 含义 |
|----------|-------|------------|------|
| AIC | matmul | `aic_mac_time` | Cube 矩阵乘 |
| AIC | fixpipe | `aic_fixpipe_time` | 写回/量化 |
| AIC | mte1 | `aic_mte1_time` | GM → L0 |
| AIC | mte2 | `aic_mte2_time` | GM → L0A/B |
| AIC | scalar | `aic_scalar_time` | AIC 标量指令 |
| AIV | vec | `aiv_vec_time` | Vector ALU |
| AIV | mte2 | `aiv_mte2_time` | GM → UB |
| AIV | mte3 | `aiv_mte3_time` | UB → GM |
| AIV | scalar | `aiv_scalar_time` | AIV 标量指令 |

### 为什么 AIC mte2 ≠ AIV mte2

两者走的是**完全不同的内存路径**：

```python
# 正确做法：分开统计
aic_mte_total = aic_mte1_time + aic_mte2_time  # AIC 侧
aiv_mte_total = aiv_mte2_time + aiv_mte3_time   # AIV 侧

# 错误做法：合并掩盖真相
# merged_mte = aic_mte2 + aiv_mte2  # 混淆两种路径
```

如果一个算子受困于 AIV 的 GM→UB 压力，错误合并会被误诊断为 Cube 侧 mte2 问题。

### op_type 分类体系

基于 `Accelerator Core` 列和 kernel name 的粗粒度分类：

| op_type | 触发条件 | 含义 |
|---------|----------|------|
| `aic` | Core = AI_CORE | 纯 Cube 算子 |
| `aiv` | Core = AI_VECTOR_CORE | 纯 Vector 算子 |
| `mix_cv` | Core = MIX_AIC/MIX_AIV | Cube+Vector 同时运行（FlashAttention、GroupedMatmul）|
| `mix_comm_aiv` | Core = COMMUNICATION 且 AIV > 0 | 通信+AIV 融合（DispatchFFNCombine）|
| `communication` | Core = COMMUNICATION 且 AIV = 0 | 纯 HCCL 集合通信 |
| `aicpu` | Core = AI_CPU | Host 侧算子 |

**`mix_comm_aiv` 的设计意图**：当 CANN 报告 `DispatchFFNCombine` 时，`Accelerator Core = COMMUNICATION`。但实际上有一半运行时在 AIV 上跑。我们检查非零 AIV 时间并重新标记，让报告能单独归因 AIV 负担。

## 五、Step / Layer / Block 分解

### Step 切分

基于 **selection/sampling kernel** 定位 step boundary：

```python
# segment.py
if "argmax" in text or "applytopktopp" in text:
    role = "selection"
    primary_roles.add("selection")
```

Step 切分的结果：

```
Step 0: [head] → [layer_0, layer_1, ..., layer_N] → [tail]
         ↑                             ↑                    ↑
       启动开销                  主计算                 采样/输出
```

每个 step 分解为四个时间桶：

| 时间桶 | 计算方式 | 含义 |
|--------|----------|------|
| head | step.start → layer[0].start | 启动/调度开销 |
| main | layer[0].start → layer[-1].end | 主计算 |
| tail | layer[-1].end → step.end | 后处理 |
| bubble | wall - busy | 设备空闲时间 |

### Layer 切分

按 **anchor**（attention / MoE / matmul / block_head）构建 layer observations：

```python
# segment.py
def anchor_kind(event):
    if has_attention_role(event):
        return primary_attention_category(event)  # attention.flash_score, etc.
    if has_moe_role(event):
        return primary_moe_category(event)  # moe.dispatch, etc.
    if has_matmul(event) and not is_collective(event):
        return "compute.matmul"
    if is_block_head(event):
        return "block_head"
```

**关键设计**：层数是观测结果，不是先验假设。观测到什么就是什么。

### Block 分解

每个 layer 最多切分为 2 个 block：

```text
标准 transformer layer:
  dense layer    → [attention block] + [ffn block]
  MoE layer      → [attention block] + [moe block]
  companion layer → [moe block] (无 attention)
```

Block 边界由 **row 中点** 决定，而非时间中点：

```python
# block_taxonomy.md
# Both present: split at the midpoint between last attention row
# and first MoE row.
# Why row-midpoint instead of time-midpoint:
# row order matches on-device sequencing and is independent of stream skew
```

## 六、Bound 分类

### 11 个 pipeline 字段 → 5 个 family

```python
# pipeline_taxonomy.md
FAMILY_MAPPING = {
    "cube": ["aic_mac_time", "aic_fixpipe_time"],
    "vector": ["aiv_vec_time"],
    "aic_mte": ["aic_mte1_time", "aic_mte2_time"],
    "aiv_mte": ["aiv_mte2_time", "aiv_mte3_time"],
    "scalar": ["aic_scalar_time", "aiv_scalar_time"],
}
```

### Dominant Core vs Bound Stage

```python
# 关键区分
dominant_core = AIC 侧时间 > AIV 侧时间 ? "aic" : "aiv"
# 而 bound_stage 是 9 个 sub-stage 中累计耗时最大的
```

```python
# bound_classification.md
# 计算每个子 stage 的累计时间，返回最大的
def bound_stage(pipeline_us):
    stages = {
        "mac": pipeline_us.get("aic_mac_time", 0),
        "mte1": pipeline_us.get("aic_mte1_time", 0),
        # ...
    }
    return max(stages, key=stages.get)
```

## 七、Class 分组：Shape-strict Equality

### 设计原则

> **Shape 必须完全一样才可以。跨 DP 的话可能存在两个 step 一个 shape 为 (3, 4)，另一个 shape 为 (4, 3)，这种情况也视为两种不同的 step。**

```python
# step_class_grouping.md
# 1. 顺序敏感的 tuple
pairs = [(name1, shape1), (name2, shape2)]  # 3×4 ≠ 4×3

# 2. 缺失 shape 不合并
if not pairs:
    return f"{prefix}_unknown_shape_{digest}"

# 3. BLAKE2b 哈希确保确定性
payload = json.dumps([structure, scope_label, pairs])
digest = blake2b(payload.encode(), digest_size=8).hexdigest()
```

### Aggregate 计算策略

```python
# step_class_grouping.md
# wall_ms_mean: 算术平均
# wall_ms_sum: 总贡献 = Σ(member_count × wall_mean)
# bound_family: 在 pipeline 聚合上重新计算
```

## 八、先验知识体系

这是 skill 最核心的创新：通过 YAML 声明式地管理模型架构知识。

### 三层架构

```
┌─────────────────────────────────────────────────────────┐
│  Layer 3: model_architectures.yaml                      │
│  HF arch → (attention_family, ffn_family, block_pattern)│
│  用于诊断异常，不驱动切分                              │
├─────────────────────────────────────────────────────────┤
│  Layer 2: attention_families.yaml                     │
│  kernel category 组合 → paper-aligned family name        │
│  CSA/HCA/DSA/MLA/linear/GQA_MHA                     │
├─────────────────────────────────────────────────────────┤
│  Layer 1: kernel_signatures.yaml                     │
│  profile kernel name → categories + roles               │
│  100+ 条映射，覆盖所有见过的 kernel                   │
└─────────────────────────────────────────────────────────┘
```

### Attention Family 检测（7 种）

```yaml
# attention_families.yaml 决策顺序
decision_order:
  1. CSA: kv_compressor + lightning_indexer + sparse_sharedkv
  2. HCA: kv_compressor + flash_score (无 indexer/sparse)
  3. DSA: lightning_indexer + sparse_sharedkv (无 compressor)
  4. MLA: mlaprolog / kvrmsnormropecache 等
  5. linear: causalconv / mamba 等
  6. gqa_or_mha: flash_score (无架构特定伴随)
  7. attn: 未知
```

### 关键洞察：Kernel Category 中性设计

```python
# common.py categories_and_roles
# FusedInferAttentionScore 支持 MHA/GQA/MLA
if "fusedinferattentionscore" in text:
    categories.add("attention.flash_score")
    # 不加 mha/gqa/mla——同一 kernel 可以服务多个架构

# Family 由 block 内的 category 组合决定
def resolve_attention_family(categories):
    if "kv_compressor" in cats and "lightning_indexer" in cats:
        return "csa"
    # ...
```

### 代码片段：categories_and_roles 结构

```python
# common.py (约 350 行)
def categories_and_roles(name, task_type, accelerator_core):
    """Classify one kernel into op_categories + op_roles.

    Rule order and signatures mirror kernel_signatures.yaml.
    """
    text = fold_text(f"{name} {task_type} {accelerator_core}")
    categories = set()
    roles = set()

    # --- Communication ---
    if any(token in text for token in ("hccl", "hcom", "allreduce", ...)):
        categories.add("communication.collective")
        roles.add("communication")

    # --- Attention: sparse-attention building blocks ---
    # CSA 和 DSA 共用这些 kernel
    if "sparseattnsharedkv" in text:
        if "metadata" in text:
            categories.add("attention.sparse_sharedkv.metadata")
        else:
            categories.add("attention.sparse_sharedkv")

    # --- Attention: MLA (DeepSeek V2/V3) ---
    if "mlapreprocess" in text or "mlaprolog" in text:
        categories.add("attention.mla.preprocess")
        categories.add("attention.mla")

    # --- MoE ---
    if "dispatchffncombine" in text:
        categories.add("moe.dispatch_expert_compute")

    # ...
    return (tuple(sorted(categories)), tuple(sorted(roles)))
```

### 代码片段：resolve_attention_family 决策流程

```python
# common.py
def resolve_attention_family(categories):
    cats = set(categories)

    has_compressor = "attention.kv_compressor" in cats
    has_indexer = "attention.lightning_indexer" in cats
    has_sparse_sharedkv = "attention.sparse_sharedkv" in cats
    has_flash_score = "attention.flash_score" in cats
    has_mla_marker = bool(_MLA_CATEGORIES & cats)

    if has_compressor and has_indexer and has_sparse_sharedkv:
        return "csa"  # Compressed Sparse Attention
    elif has_compressor and has_flash_score and not has_indexer:
        return "hca"  # Heavily Compressed Attention
    elif has_indexer and has_sparse_sharedkv and not has_compressor:
        return "dsa"  # DeepSeek Sparse Attention
    elif has_mla_marker and not (has_compressor or has_indexer):
        return "mla"  # Multi-head Latent Attention
    elif "attention.linear_or_mamba" in cats:
        return "linear"
    elif has_flash_score:
        return "gqa_or_mha"  # 伞形，需要 shape 细化
    else:
        return "attn"
```

### KVComp Overlay

```yaml
# 如果存在 Hamming-distance KV 剪枝，叠加 +kvc 后缀
if "attention.kvcomp.topk" in categories:
    base = f"{base}+kvc"  # mla+kvc, dsa+kvc, etc.
```

### 扩展新 Kernel 的流程

```yaml
# 1. kernel_signatures.yaml 添加映射
- profile_name: newkernel
  categories: [attention.new_category]
  roles: [attention]
  evidence:
    - "vllm-ascend/path/to/kernel:123"

# 2. attention_families.yaml 更新 must_have 组合

# 3. semantic_conventions.yaml 添加新 enum 值

# 4. Python 测试确保不破坏现有逻辑
```

## 九、通信诊断

### HCCL 两层事件

| Layer | 出现位置 | 代表含义 |
|-------|----------|----------|
| Op-level | `kernel_details.csv` 的 COMMUNICATION 行 | 用户发起的集合通信 |
| Task-level | `communication.json` (level 1) | 集合内部的任务分解 |

### Op-kind Taxonomy

```python
hccl_op_kind_map = {
    "HCOM_ALLREDUCE_*": "allreduce",
    "HCOM_ALLGATHER_*": "allgather",
    "HCOM_REDUCESCATTER_*": "reducescatter",
    "HCOM_ALLTOALLV_*": "alltoallv",
    "DispatchFFNCombine": "comm_aiv_fused",  # 特殊：混合 AIV
}
```

### Notify Wait 诊断

```yaml
# communication_taxonomy.md
# Task-level 的 Notify Wait 是暴露 peer 等待的关键
- 症状: one rank's Notify Wait > 50% of collective wall
- 含义: 该 rank 在等待更慢的 peer
```

### 诊断发现类型

```yaml
finding_type:
  - communication_collective_slow      # rank 间 duration skew > 30%
  - ep_load_imbalance_suspected        # EP 路由不均
  - slow_rank_suspected                # 某个 rank 掉队
  - dp_workload_imbalance              # DP 负载不均
  - reduced_work_or_dummy_rank         # 陪跑/dummy rank
```

## 十、报告结构

### 章节布局

1. **Executive Summary** — 关键指标一览
2. **Capture And Segmentation** — 采集和切分统计
3. **Macro Step Timeline** — per-rank step 时长分位数
4. **Pipeline Coverage** — AIC/AIV 各 stage 占比
5. **Step Class View** — top step classes 按 wall 贡献排序
6. **Layer And Block View** — block_kind 分解
7. **Operator View** — top 算子 + HCCL 汇总
8. **Cross-Rank Anomaly** — 跨 rank 异常
9. **Evidence Chain** — 证据索引

### HTML 报告特性

- 单文件零依赖
- Single-step Inspector（点击 step 查看详情）
- Bubble tracing axis
- 可缩放多流时间轴
- 46 字段算子卡（带 raw kernel_details row 追溯）

## 十一、Skill 的优势与限制

### 优势

1. **证据链可追溯** — 每条结论都能追溯到原始 CSV 行
2. **Kernel category 中性** — 易于扩展新 kernel
3. **Paper 术语与实现解耦** — `csa`/`dsa`/`mla` vs `kv_compressor`/`lightning_indexer`
4. **远端执行** — 避免大文件传输
5. **确定性切分** — 不依赖模糊匹配

### 限制

1. **不读 HF config.json** — 无法直接确认 model arch
   - 原因：skill 只看到 `ascend_pt/` 输出，无 config 访问权限
   - 影响：`block_pattern_unexpected` 诊断无法自动关联到 HF arch

2. **Shape 可能缺失** — acl-graph compile 会擦除 `Input Shapes`
   - 影响：GQA/MHA/MQA 细化可能失败，保持伞形 `gqa_or_mha`

3. **HCA 检测是 heuristic** — 缺少确认样本
   - 误报可能：V3.2 + KV 压缩在非 CSA 层

4. **Task-level 通信数据需要 level 1 profiling**
   - Level 0 只有 op-level，`Notify Wait` 等诊断不可用

### 可改进点

| 改进项 | 当前状态 | 目标 |
|--------|----------|------|
| YAML-driven matcher | Python 代码镜射 YAML | 直接读 YAML |
| Shape 缺失 graceful degradation | 直接失败 | 多级 fallback |
| 诊断规则 YAML 化 | Python 内联 | `diagnosis_rules.yaml` |
| HF config 集成 | 不可达 | serving 侧传递 config |
| 层结构指纹库 | 人工阅读 YAML | 自动匹配已知架构 |

## 十二、关键设计原则总结

1. **层数 = 观测结果，非假设**
   - 不写死 24/27/36/40 层

2. **不写死模型名 / 层数**
   - "layer_17" 只是个 hash，不是 "attention_layer_17"

3. **宁可低置信度输出，不输出不可追溯结论**

4. **kernel category 中性**
   - 同一 kernel 可服务多个 architecture

5. **Paper 术语与实现解耦**
   - `csa`/`dsa`/`mla` 是架构名
   - `kv_compressor`/`lightning_indexer` 是 kernel category

6. **AIV mte2 与 AIC mte2 必须分开**
   - 两者走不同内存路径

7. **Shape 缺失不合并**
   - 保守策略：宁可 under-cluster

---

## 参考资料

- [Ascend Profiling Analysis Skill](https://github.com/your-org/ascend-profiling-analysis)
- [CANN HCCL 用户指南](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/API/hccl/)
- [DeepSeek-V4 Paper](https://arxiv.org/abs/xxxx)
- [DeepSeek-V3.2 (DSA)](https://arxiv.org/abs/2512.02556)

[^1]: 本文的分析基于 Ascend Atlas A2/A3 架构。不同硬件版本可能有细微差异。
