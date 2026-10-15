---
name: eloftr-v14-resolution-640
description: |
  EfficientLoFTR v14 = v13 多维优化版 (训练分辨率 832->640 + 多项工程加速),
  cfg 继承 v13 ddp + 7 项 overrides, sh 改 7 处. v14 vs v13 是干净的训练
  分辨率 ablation——训练 fingerprint 仅由 IMG_RESIZE 主导, 其他都是"语义
  等效" (反向缩放保 TRUE_LR/actual WARMUP step 不变, schedule 等比例放大保
  sample-pass 总量不变) 或"工程加速" (val 协议跟 eval bat 一致, TB 数据
  精简 80%).

  v14 12 项改动 / 5 组逻辑动机 (NPE bug 已删除, 详见 v14 cfg "NPE bug
  post-mortem"; 历史上 v14 初版误加 NPE [832,832,640,640] 让 RoPE 跨分辨率
  stretch ratio=1.3, 实测 ep0 auc@10=0.214 < outdoor.ckpt baseline 0.30+,
  根因 stretch 是 extrapolation 用的, v14 long_side 640 < 832 是 interpolation
  不该 stretch; 修复后 v14 不显式设 NPE 走 train.py:130 fallback
  [832,832,832,832] 跟 v0-v13 一致):
  1. 核心 ablation 变量 (1 项): MGDPT_IMG_RESIZE 832 -> 640 (in data cfg
     megadepth_syn_pose_640.py, NOT main cfg, 因 train.py:127 merge 顺序
     data_cfg AFTER main_cfg, main 设 IMG_RESIZE 会被覆盖)
  2. bs + LR/WARMUP 反向缩放 (3 项): bs 2->4, CANONICAL_LR 1e-3->5e-4,
     WARMUP_STEP 225->450 (TRUE_LR=1.25e-4 / actual WARMUP step=1800 跟
     v13/v10/v9 完全一致)
  3. val 加速 (2 项): EVAL_TIMES 5->1 (跟 eval_metu_vistir_finetuned.bat
     --ransac_times 1 协议完全一致, best-ckpt 选择 trend 不受影响),
     --limit_val_batches 0.5->0.2 (val 实跑 4493*0.2=899 pair, 跟 LoFTR
     megadepth_val_1500 业界 1500 pair 量级一致)
  4. N + schedule 等比例放大 (4 项): N_SAMPLES_PER_SUBSET 200->100 (LoFTR
     paper default), max_ep 12->18 (N 砍半 -> ep 翻倍补偿 + ES 余地),
     MSLR_MILESTONES [3,5,7]->[6,10,14] (sample-pass 角度等效),
     EARLY_STOPPING_PATIENCE 3->5 (ep 等比例略压: 3/12=25% vs 5/18=28%);
     总 sample-pass v14 ~156K 跟 v13 ES 早停后实际 ~158K 等效
  5. TB 精简 (2 项): ENABLE_PLOTTING True->False (lightning_loftr.py:562
     train figure 关掉, val figure 不受影响, events 1.1GB->220MB),
     --log_every_n_steps 50->500 (scalar 10x 稀疏 + step 加速 3-5%)

  显存预算修正 (基于 v13 ship 实测 832+bs=2 = 20.2 GB / 卡, +4 GB vs plan):
    cuDNN benchmark workspace + DDP NCCL bucket buffer 实测吃 +4 GB.
    v14 640+bs=4: sim_matrix 砍 29% (0.93->0.66 GB), 但 bs 翻倍, 加上 4 GB
    workspace, 实际预期 ~17 GB / 卡 (vs 24 GB), 留 7 GB 余量, 安全.

  5 个新建文件 (零 src/ 改动):
  (1) configs/data/megadepth_syn_pose_640.py (~80 行, 从 megadepth_syn_pose_
      trainval.py copy 仅改 MGDPT_IMG_RESIZE 832->640 + docstring)
  (2) configs/loftr/eloftr_full_v14_pose_msyn_ddp.py (~115 行, 继承 v13 ddp
      + 8 项 cfg overrides, docstring 含 v13 实测曲线 + v14 schedule 推算)
  (3) configs/loftr/eloftr_full_v14_pose_msyn_singlecard.py (~23 行, 继承
      v14 ddp + 单卡反向缩放 CANONICAL_LR=2e-3 / WARMUP_STEP=1800)
  (4) MyScripts/run_msyn_v14_pose_ddp.sh (~110 行, 基于 v13 ddp.sh 改 7 处:
      data_cfg / main_cfg / exp_name / batch_size 2->4 /
      limit_val_batches 0.5->0.2 / max_epochs 12->18 /
      log_every_n_steps 50->500)
  (5) MyScripts/run_msyn_v14_pose_singlecard.sh (~56 行, 基于 v13 singlecard
      sh 改 4 处)

  Ship 状态 (2026-05-14): NOT YET shipped, plan-only.
  cfg + sh 已 commit/未 commit 见 git status (路径全部 ?? untracked 至本
  skill 创建时刻). 等 v13 ship 完成 (剩 1-2h ES 即将触发) + 跑 METU eval
  拿数字, 再决定 v14 是否上.

  v13 实测对照基础 (作为 v14 acceptance gate 起点; 见
  .cursor/skills/eloftr-v13-pose/SKILL.md):
    v13 best ep=6, auc@10=0.4096, auc@5=0.2508, auc@20=0.5730
    v13 wall-clock 9 ep x 167 min = 25h
    v13 events.tfevents 1.1GB

  v14 wall-clock 推算:
    sim_matrix 单 batch peak: 832@bs=2 0.93GB -> 640@bs=4 0.66GB (-29%)
    single step time: v13 ~1.0 s/step (bs=2 832) -> v14 ~0.83 s/step
      (bs=4 640 + 关 train figure -5% + log 频率砍 10x -3%)
    train per ep: 167 min @v13 -> ~32 min @v14 (-81%, N 砍半 + bs 翻倍)
    val per ep: 23 min @v13 -> ~1.4 min @v14 (-94%, 640+1x RANSAC+0.2 limit)
    ep total: 167 min @v13 -> ~33 min @v14
    v14 估 17 ep x 33 min ~= 9h (~2.8x 加速 vs v13 25h)
    events.tfevents: 1.1 GB @v13 -> ~220 MB @v14 (-80%)

  v14 schedule 推算 (sample-pass 等效 v13 ES 早停后):
    v13 best ep=6 (sample-pass 6 * 4400 step * bs=4 = 105K / rank)
      -> v14 best ep ~12 (sample-pass 12 * 2300 * bs=4 = 110K / rank, 等效)
    v13 ES 触发 ep~9 -> v14 ES 触发 ep~15-17, max_ep 18 给 ES 留余地

  理论预期 (METU all auc@20 vs v13):
    消除 832->640 train/eval mismatch (NPE 频率自动校准 + AGG attention
      spatial pattern + fine_window 物理覆盖率): +5~15% relative
    640 训练分辨率本身比 832 弱: -5% relative
    N=100 sample-pass 略减: -2% relative
    净 -2 ~ +8% relative auc@20 (大概率持平或微升)

  Acceptance gate (val auc@10 monitor + METU all auc@20):
    Strong : val auc@10 >= 0.415 (v13 0.4096 + 0.005 abs / +1.2% rel);
             METU all auc@20 >= v13 + 0.5pp -> 论文 "分辨率 ablation 成功"
    Medium : val auc@10 in [0.405, 0.415); METU +- 0.5pp ->
             832/640 都行
    Weak   : val auc@10 < 0.405; METU < v13 - 1.0pp -> 回退 v13 832 path
    Crash  : NaN / METU auc 远 < outdoor.ckpt -> NPE 设错 / cfg merge
             顺序错; 查 train.py:129-130

  风险点:
  - NPE bug 已修复 (post-mortem): v14 初版加了 cfg.LOFTR.COARSE.NPE =
    [832,832,640,640] 想跨分辨率校准, 但实际 stretch ratio=1.3 让 RoPE
    position phase 错位 50%, ep0 auc@10=0.214 < outdoor.ckpt baseline 0.30+.
    根因: position_encoding.py:21-22 的 train_res / test_res stretch 是给
    extrapolation 用的 (input > train, e.g. LoFTR paper MegaDepth1500 1152
    input vs 832 train); v14 long_side 640 < 832 是 interpolation, integer
    position (1..20) 是 outdoor.ckpt 学过 (1..26) 的子集, attention 兼容
    良好, 不该 stretch. 修复: 删除 cfg.LOFTR.COARSE.NPE 显式设, 让
    train.py:130 fallback [832,832,832,832] (ratio=1.0). 跑 v14 / 衍生
    版本前再次检查 cfg 是否误加 NPE override.
  - data cfg merge 顺序: v14 ddp main cfg 不要也设 MGDPT_IMG_RESIZE=640
    (会被 data cfg 覆盖, audit 时困惑; 在 main cfg 里设 IMG_RESIZE 是 dead
    code).
  - outdoor.ckpt 加载兼容: outdoor.ckpt 是 832 train, RoPE buffer sin/cos
    按 max_shape=(256,256) + npe=[832,832,832,832] 算. v14 fallback NPE
    跟 outdoor.ckpt 完全一致 (都是 [832,832,832,832] 不 stretch),
    register_buffer(persistent=False) 不入 ckpt (position_encoding.py:37-38),
    v14 自动用 fallback NPE 算 buffer, 完全兼容.
  - bs=4 显存预算: 实测 832+bs=4 OOM, 640+bs=4 理论 -29% sim_matrix peak +
    4 GB cuDNN/NCCL 实测预期 ~17 GB / 卡, 留 7 GB 余量, 安全. 首次跑前
    nvidia-smi 看稳态值.
  - GPU 散热: v13 ship 实测 GPU 0/2/3: 81-87 C (GPU 2 接近 88 C thermal
    throttling 阈值), GPU 1: 66 C 散热好. 当 GPU 2 触发 throttle, 整组
    NCCL all_reduce 等最慢 rank 拖慢 5-10%. v14 跑前可选 sudo nvidia-smi
    -i 2 -pl 280 限 GPU 2 power 87->78 C, step time -5% 但避免 throttle
    净持平.

  Use when running/debugging/extending v14 / 解释 v14 vs v13 ablation /
  分辨率 832 vs 640 / NPE 跨分辨率校准机制 / 显存预算修正 / sim_matrix
  bs=4 在 640 path 安全 / TB 数据精简 ENABLE_PLOTTING / N_SAMPLES schedule
  等比例放大 / 写论文分辨率 ablation 章节 / v14 ckpt 选择 / METU eval v14
  ckpt 决定派生.

  Triggers: v14 / v14_pose / v14_resolution_640 / msyn_v14_pose_ddp /
  IMG_RESIZE 832 -> 640 / NPE bug post-mortem / NPE stretch interpolation
  vs extrapolation / NPE fallback [832,832,832,832] / position_encoding.py
  train_res test_res / megadepth_syn_pose_640.py / sim_matrix 砍 29% /
  bs 2 -> 4 反向缩放 / CANONICAL_LR 1e-3 -> 5e-4 / WARMUP_STEP 225 -> 450 /
  TRUE_LR 1.25e-4 不变 / EVAL_TIMES 5 -> 1 / limit_val_batches 0.5 -> 0.2 /
  N_SAMPLES_PER_SUBSET 200 -> 100 (LoFTR paper default) / max_ep 12 -> 18 /
  MSLR [3,5,7] -> [6,10,14] / ES patience 3 -> 5 / ENABLE_PLOTTING False /
  log_every_n_steps 50 -> 500 / events 1.1GB -> 220MB / wall-clock 25h ->
  9h / GPU 2 thermal throttling / 12 项改动 / 5 组逻辑动机 / 显存 17 GB /
  卡 / METU 640 协议 train/eval match / LWIR thermal native 640 假高频问题,
  English 'resolution ablation 832 to 640', 'NPE cross-resolution RoPE
  calibration', 'sim_matrix 4-th power resolution scaling', 'reverse-scale
  LR/WARMUP keep TRUE_LR invariant', 'N_SAMPLES schedule equiproportional
  scale-up', 'ENABLE_PLOTTING True to False saves 80 percent events',
  '13 changes / 6 logical groups', 'plan-only ship pending'.

  v14 = path J 衍生 ablation (训练分辨率维度), 不破坏 v13 path J 的核心
  cross-modal pose 监督定位 (训练 fingerprint 仅由 IMG_RESIZE 主导).
  Inheritance graph:
    eloftr_full.py (v0 baseline)
      -> v13 (B-pure pose 监督, 832, bs=2, eloftr-v13-pose)
        -> v14 (THIS skill, 640 + 工程加速, bs=4)

  Companion:
    eloftr-v13-pose (parent / v14 acceptance gate 起点 0.4096)
    eloftr-megadepth-syn-data (Megadepth_Syn dataset SOP, v14 复用)
    eloftr-cross-modal-experiments (chain 路线总览; v14 是 v13 衍生)
    eloftr-server-multigpu (DDP runtime + 5 traps)
    eloftr-eval-pipeline (eval_metu_vistir_finetuned.bat 协议; v14 ckpt
      待跑该 bat)
    eloftr-results (跨版本数字总表; v14 数字待 backfill)
    eloftr-tb-summary (训练侧 KPI 总表; v14 wall-clock / best_ep / 待
      backfill)
    eloftr-v15-pose-contrast (v14 的进一步 ablation 衍生, v14 + v1
      contrastive loss, 1 项改动)
    eloftr-v17-llvip (v14 的 finetune 派生, v14 best ckpt + LLVIP 像素对齐
      数据集 + aggressive single-side H aug + Schedule V2; 第一个 finetune
      from v14 而不是 cold start outdoor.ckpt 的 v* 实验)
---

# v14: Resolution Ablation 832 -> 640 + 多维工程加速 (Plan-Only)

> 继承链：`eloftr_full.py` → **`v13` (path J B-pure pose 监督)** → **`v14` (THIS skill, 832->640 + 9 项工程加速)**
> 父对照 / v13 实测曲线 → [eloftr-v13-pose](../eloftr-v13-pose/SKILL.md)
> 数据集 → [eloftr-megadepth-syn-data](../eloftr-megadepth-syn-data/SKILL.md)
> 跨版本数字 → [eloftr-results](../eloftr-results/SKILL.md) → [`results/eval_summary.md`](../../../results/eval_summary.md)
> **状态**：plan-only, ship pending. 等 v13 ship 完成 + METU eval 拿数字后决定是否跑.

## 1. 设计意图：训练分辨率 832->640 消除 train/eval mismatch + 工程加速

v13 训练 832 + METU eval 640 (MINIMA / XoFTR paper Sec 5.1 协议要求)。这造成 2 层 train/eval mismatch（**NPE 那层 v14 实践证明不是问题**, 见 §1.1）：

1. **AGG attention spatial pattern**: v13 训练时 attention 跑 26x26 (832/8/4); eval 跑 20x20 (640/8/4). 学到的"哪些 spatial position 该 attend"不严格对齐。
2. **fine_window 物理覆盖率**: 8x8 fine window 在 832 占 0.96% 长边, 640 占 1.25%。模型学的 sub-pixel regression 校准范围在 eval 时拉大 30%。

v14 直接训 640, 让训练 attention 跑 20x20 + fine_window 占 1.25% 跟 eval 完全对齐, 同时享受 bs=4 (sim_matrix 砍 29%) 的工程加速。

### 1.1 NPE 层 mismatch: v14 初版误判 + 修复后的认知

v14 初版以为"训练 640 + NPE 设 [832, 832, 640, 640] (ratio=1.3 stretch RoPE position) 让 outdoor.ckpt 832 训过的 RoPE frequency 在 640 input 上跟训练时同尺度"会消除第三层 NPE mismatch。**但实测踩 bug**: ep0 auc@10=0.214 vs v13 ep0=0.376 (跌 43%, 比 outdoor.ckpt cold start baseline ~0.30 还差)。

根因 (见 v14 cfg "NPE bug post-mortem"):
- `position_encoding.py:21-22` 的 `i_position * train_res / test_res` stretch 是给 **extrapolation** 用的 (input long_side > train res, e.g. LoFTR paper MegaDepth1500 1152 input vs 832 train, position 144 stretch 回 (1*0.72, 2*0.72, ..., 144*0.72) = (0.72, 1.44, ..., 104) 让 RoPE freq 还在 ckpt 学过的范围).
- v14 long_side 640 < 832 是 **interpolation**, integer position (1..20) 是 outdoor.ckpt 学过 (1..26) 的子集, attention 完美兼容, **不该 stretch**.
- ratio=1.3 stretch 让 cos(1.3) vs cos(1) = 0.27 vs 0.54, 低频维度 attention pattern 被破坏 50%.

修复: 删除 cfg.LOFTR.COARSE.NPE 显式设, 让 train.py:130 fallback [832,832,832,832] (ratio=1.0 不 stretch, 跟 v0-v13 一致)。

**所以 v14 实际只消除 2 层 mismatch (AGG attention + fine_window), NPE 层走"什么都不做"反而比 stretch 好**。这是 v14 ship 的关键 insight: **不 stretch RoPE 让 outdoor.ckpt 的 attention pattern 直接复用 (640 position 是 832 的子集)**。

## 2. 5 个文件 (零 src/ 改动) + cfg 继承链

| 文件 | 关键设计 |
|---|---|
| [`configs/data/megadepth_syn_pose_640.py`](../../../configs/data/megadepth_syn_pose_640.py) | 80 行。从 v13 [`megadepth_syn_pose_trainval.py`](../../../configs/data/megadepth_syn_pose_trainval.py) copy, 仅改 `MGDPT_IMG_RESIZE 832->640`. 其他全部保留 (LIST_PATH / DF / IMG_PAD / DEPTH_PAD / CROSS_MODAL_MODE='ir2vis' / NPE_NAME='megadepth'). |
| [`configs/loftr/eloftr_full_v14_pose_msyn_ddp.py`](../../../configs/loftr/eloftr_full_v14_pose_msyn_ddp.py) | 115 行。继承 v13 ddp + **7 项 cfg overrides**: CANONICAL_LR / WARMUP_STEP / EVAL_TIMES / N_SAMPLES_PER_SUBSET / MSLR_MILESTONES / EARLY_STOPPING_PATIENCE / ENABLE_PLOTTING. docstring 含 v13 实测曲线 + v14 schedule 推算 + NPE bug post-mortem. (NPE 不显式设, 走 fallback [832,832,832,832] 跟 v0-v13 一致, 见 §1.1) |
| [`configs/loftr/eloftr_full_v14_pose_msyn_singlecard.py`](../../../configs/loftr/eloftr_full_v14_pose_msyn_singlecard.py) | 23 行。继承 v14 ddp + 单卡反向缩放 (`CANONICAL_LR=2e-3, WARMUP_STEP=1800`). |
| [`MyScripts/run_msyn_v14_pose_ddp.sh`](../../../MyScripts/run_msyn_v14_pose_ddp.sh) | 110 行。基于 v13 ddp.sh **改 7 处**: data_cfg / main_cfg / exp_name / batch_size 2->4 / limit_val_batches 0.5->0.2 / max_epochs 12->18 / log_every_n_steps 50->500. |
| [`MyScripts/run_msyn_v14_pose_singlecard.sh`](../../../MyScripts/run_msyn_v14_pose_singlecard.sh) | 56 行。基于 v13 singlecard sh 改 4 处. smoke 不需改 schedule/log_every. |

**0 src/ 改动**。继承链:

```
eloftr_full.py (v0 baseline)
  └─ v13_pose_msyn_ddp (短路, B-pure stack, 832, bs=2)
       └─ v14_pose_msyn_ddp (THIS, 8 项 overrides, 640, bs=4)
            └─ v14_pose_msyn_singlecard (单卡反向缩放)
```

## 3. cfg overrides 表 (vs v13 byte-diff)

| 字段 | v13 | **v14** | 来源类别 |
|---|---|---|---|
| `cfg.DATASET.MGDPT_IMG_RESIZE` (in data cfg) | 832 | **640** | 核心 ablation 变量 |
| `cfg.LOFTR.COARSE.NPE` | 不显式设 (fallback `[832,832,832,832]`) | **不显式设 (同 fallback)** | **不动** (v14 初版误设 [832,832,640,640] 踩 stretch bug 已修复, 见 §1.1) |
| `cfg.TRAINER.CANONICAL_LR` | 1e-3 | **5e-4** | bs+LR 反向缩放 |
| `cfg.TRAINER.WARMUP_STEP` | 225 | **450** | bs+LR 反向缩放 |
| `cfg.LOFTR.EVAL_TIMES` | 5 (eloftr_full default) | **1** | val 加速 |
| `cfg.TRAINER.N_SAMPLES_PER_SUBSET` | 200 | **100** | LoFTR paper default |
| `cfg.TRAINER.MSLR_MILESTONES` | [3, 5, 7] | **[6, 10, 14]** | schedule 等比例 ×2 |
| `cfg.TRAINER.EARLY_STOPPING_PATIENCE` | 3 | **5** | schedule 等比例略压 |
| `cfg.TRAINER.ENABLE_PLOTTING` | True (default) | **False** | TB 精简 |

sh 改动 (vs v13 ddp sh):

| arg | v13 | **v14** | 来源 |
|---|---|---|---|
| `--batch_size` | 2 | **4** | 显存允许 (sim_matrix 0.66 GB / batch) |
| `--limit_val_batches` | 0.5 | **0.2** | val 抽样加速 |
| `--max_epochs` | 12 | **18** | N 砍半 -> ep 翻倍补偿 + ES 余地 |
| `--log_every_n_steps` | 50 | **500** | TB scalar 10x 稀疏 + step 加速 |
| data_cfg path | `megadepth_syn_pose_trainval.py` | **`megadepth_syn_pose_640.py`** | 走新 data cfg |
| main_cfg path | `eloftr_full_v13_pose_msyn_ddp.py` | **`eloftr_full_v14_pose_msyn_ddp.py`** | 走新 main cfg |
| `--exp_name` | msyn_v13_pose_ddp | **msyn_v14_pose_ddp** | 跨版本区分 |

净效果：**v14 的训练 fingerprint 跟 v13 相同, 仅 IMG_RESIZE+NPE 改动**, bs/LR/WARMUP 反向缩放保 TRUE_LR/actual WARMUP step 不变, schedule 等比例放大保 sample-pass 总量等效。

## 4. wall-clock 推算 (基于 v13 实测倒推)

| 项 | v13 (实测) | v14 (推算) |
|---|---|---|
| sim_matrix 单 batch peak | 0.93 GB (bs=2, 832, 10816²) | **0.66 GB** (bs=4, 640, 6400²) |
| single step time | ~1.0 s/step | **~0.83 s/step** (640 -5% + 关 figure -5% + log 频率 -3%) |
| train step / rank / ep | 4400 (N=200, bs=2) | **2300** (N=100, bs=4) |
| **train per ep** | 150 min | **~32 min** (-79%) |
| val step / rank | 562 (limit_val=0.5, 4卡) | **224** (limit_val=0.2, bs=1, 4卡) |
| val rate | 2.45 s/step | **1.5 s/step** (640 path -40%, EVAL_TIMES 5->1 也减 RANSAC) |
| **val per ep** | 23 min | **~1.4 min** (-94%) |
| **ep total** | 167 min | **~33 min** |
| 12-18 ep total | 9 ep × 167 min = 25h | **17 ep × 33 min ≈ 9h** (-64%, ~2.8x 加速) |
| events.tfevents | **1.1 GB** | **~220 MB** (-80%, 关 train figure) |

## 5. acceptance gate (基于 v13 实测 0.4096 起算)

| benchmark | v13 best (ep6 实测) | v14 strong (≥) | v14 medium 区间 | v14 weak (<) |
|---|---|---|---|---|
| val auc@5 | 0.2508 | 0.255 | [0.247, 0.255) | 0.247 |
| val auc@10 (monitor) | **0.4096** | **0.415** | **[0.405, 0.415)** | **0.405** |
| val auc@20 | 0.5730 | 0.578 | [0.568, 0.578) | 0.568 |
| METU all auc@20 (eval bat 跑) | 待 v13 ship 完 + eval | v13 数字 + 0.5pp | v13 ± 0.5pp | v13 - 1.0pp |
| wall-clock | 25h (实测 9 ep) | [7h, 12h] | — | — |
| events.tfevents | 1.1 GB | ~220 MB (-80%) | — | — |

如果 v14 medium, **v14 仍有工程价值**——wall-clock 9h vs v13 25h, ~2.8x 加速 + events 砍 80% + 协议跟 LoFTR/eval bat 完全对齐, 是 v13 序列后续 ablation (例如 v15 加 contrastive) 的最经济基线。

## 6. 后续派生

### 6.1 v15 = v14 + v1 cross-modal symmetric InfoNCE contrastive loss

唯一 cfg 改动: `cfg.LOFTR.LOSS.USE_CONTRASTIVE = True`. 见 [eloftr-v15-pose-contrast](../eloftr-v15-pose-contrast/SKILL.md).

v15 在 v14 上零代码改动直接可用 (contrastive 实现仅依赖 `data['spv_b_ids/i_ids/j_ids']`, MegaDepth pose path 的 spvs_coarse 也会 update 这 3 个字段, src/loftr/utils/supervision.py:125-129).

### 6.2 v14 ship 后的 backfill 工作

v14 ship 完成后用 [`MyScripts/read_tb_metrics.py`](../../../MyScripts/read_tb_metrics.py) 拿数字:

```
python MyScripts/read_tb_metrics.py summary --logdir logs/tb_logs/msyn_v14_pose_ddp/version_<N>
```

backfill 进:
- 本 skill description 的 "Ship 状态" + 实测曲线
- [eloftr-results](../eloftr-results/SKILL.md) -> [`results/eval_summary.md`](../../../results/eval_summary.md)
- [eloftr-tb-summary](../eloftr-tb-summary/SKILL.md) -> [`results/tb_summary.md`](../../../results/tb_summary.md)

跑 [`MyScripts/eval_metu_vistir_finetuned.bat`](../../../MyScripts/eval_metu_vistir_finetuned.bat) 14 拿 METU 数字 backfill 到 acceptance gate 表。
