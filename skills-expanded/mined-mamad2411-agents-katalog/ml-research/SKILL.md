---
name: ml-research
version: 1.0.0
description: 机器学习研究全流程支持，涵盖 PyTorch/scikit-learn 流水线、模型架构实现、超参数调优与实验追踪
author: tzukwan
---

# ML Research — 机器学习研究技能

## 描述

ML Research 技能为机器学习研究者提供从数据预处理到论文就绪的完整研究支持。深度集成 PyTorch 和 scikit-learn 生态，提供模型架构实现辅助、自动化超参数调优、实验追踪与比较，以及研究级别的代码质量保证。LLM 在整个流程中充当高级研究助手，帮助理解最新进展、诊断训练问题、解读实验结果。

## 功能列表

- **PyTorch Pipeline 构建**：数据集类、DataLoader、训练循环、混合精度训练、分布式训练模板
- **scikit-learn Pipeline**：特征工程流水线、交叉验证、模型评估、Pipeline 对象构建
- **模型架构实现辅助**：基于论文描述或伪代码，辅助实现自定义神经网络架构
- **超参数调优**：支持 Grid Search、Random Search、Bayesian Optimization（Optuna）、Population-Based Training
- **实验追踪**：集成 MLflow、Weights & Biases、TensorBoard，统一日志接口
- **训练诊断**：损失曲线分析、梯度监控、过拟合/欠拟合诊断、梯度消失/爆炸检测
- **模型解释**：SHAP 值计算、注意力可视化、特征重要性分析、Grad-CAM
- **基准测试**：自动与 Papers with Code 上的 SOTA 结果对比，报告相对性能差距

## 命令

- `pipeline`
- `implement`
- `tune`
- `track`
- `diagnose`

## 支持的框架与生态

### PyTorch 生态

| 组件 | 支持库 | 典型用途 |
|------|--------|----------|
| 核心框架 | PyTorch ≥2.0 | 模型定义、训练、推理 |
| 闪电框架 | PyTorch Lightning | 快速研究原型，减少样板代码 |
| 视觉 | torchvision | 图像分类/检测/分割 |
| 文本 | Hugging Face Transformers | NLP 任务，预训练模型微调 |
| 图 | PyTorch Geometric (PyG) | 图神经网络 |
| 优化 | Optuna, Ray Tune | 超参数搜索 |
| 追踪 | MLflow, W&B, TensorBoard | 实验管理 |
| 加速 | torch.compile, FSDP, DeepSpeed | 大模型训练优化 |

### scikit-learn 生态

| 组件 | 支持库 | 典型用途 |
|------|--------|----------|
| 核心 | scikit-learn ≥1.3 | 传统 ML 算法全套 |
| 扩展 | imbalanced-learn | 不均衡数据处理 |
| 解释 | SHAP, LIME | 模型可解释性 |
| 特征 | feature-engine | 特征工程自动化 |
| 优化 | scikit-optimize | 贝叶斯超参数搜索 |

## 使用示例

```bash
# 为一个图像分类任务构建完整 PyTorch pipeline
tzukwan ml-research pipeline build \
  --task image-classification \
  --framework pytorch \
  --model resnet50 \
  --dataset imagenet \
  --output ./experiments/image_cls/

# 基于论文描述实现一个自定义注意力机制
tzukwan ml-research implement \
  --description "Multi-head cross-attention with relative positional encoding as described in section 3.2" \
  --framework pytorch \
  --output ./models/cross_attention.py

# 使用 Optuna 对 BERT 微调进行超参数搜索
tzukwan ml-research tune \
  --script train.py \
  --config config.yaml \
  --method optuna \
  --trials 50 \
  --metric val_f1 \
  --direction maximize \
  --params "lr:1e-5,5e-5 batch_size:16,32 dropout:0.1,0.3"

# 启动实验追踪（集成 W&B）
tzukwan ml-research track init \
  --backend wandb \
  --project my-nlp-research \
  --entity my-team

# 诊断训练问题
tzukwan ml-research diagnose \
  --log-dir ./experiments/run_001/logs/ \
  --metrics loss,accuracy,gradient_norm

# 与 Papers with Code SOTA 对比
tzukwan ml-research benchmark \
  --task "text-classification" \
  --dataset "SST-2" \
  --your-result "accuracy=94.2"
```

### 对话触发示例

```
用户：帮我用 PyTorch 实现一个 Transformer 分类模型
用户：我的训练 loss 不收敛，帮我诊断一下
用户：帮我做超参数搜索，使用贝叶斯优化
用户：生成一个带有实验追踪的完整训练脚本
用户：我的结果和 SOTA 差多少？帮我对比一下
用户：帮我实现这篇论文中描述的注意力机制
用户：生成一个 scikit-learn Pipeline，包含特征工程和模型选择
```

## 触发词

- `machine learning`
- `机器学习`
- `deep learning`
- `深度学习`
- `PyTorch`
- `pytorch`
- `neural network`
- `神经网络`
- `训练模型`
- `超参数`
- `hyperparameter`
- `fine-tuning`
- `微调`
- `实验追踪`
- `experiment tracking`
- `模型实现`
- `SHAP`
- `Optuna`

## 数据源/API 依赖

| 依赖 | 用途 | 安装 |
|------|------|------|
| PyTorch ≥2.0 | 深度学习核心框架 | `pip install torch torchvision` |
| Transformers ≥4.35 | 预训练模型库 | `pip install transformers` |
| scikit-learn ≥1.3 | 传统 ML 算法 | `pip install scikit-learn` |
| Optuna ≥3.4 | 超参数优化框架 | `pip install optuna` |
| MLflow ≥2.8 | 实验追踪（本地） | `pip install mlflow` |
| wandb ≥0.16 | 实验追踪（云端） | `pip install wandb` |
| SHAP ≥0.44 | 模型解释 | `pip install shap` |
| Papers with Code API | SOTA 对比 | HTTP API（无需安装） |

## 输出格式

### 生成的 PyTorch Pipeline 结构

```
experiments/image_cls/
├── config.yaml               # 超参数与训练配置
├── train.py                  # 主训练脚本
├── evaluate.py               # 评估脚本
├── predict.py                # 推理脚本
├── model/
│   ├── __init__.py
│   └── resnet_classifier.py  # 模型定义（含注释）
├── data/
│   ├── __init__.py
│   ├── dataset.py            # Dataset 类
│   └── transforms.py         # 数据增强变换
├── utils/
│   ├── metrics.py            # 自定义评估指标
│   ├── logger.py             # 统一日志接口（支持 MLflow/W&B）
│   └── checkpoint.py         # 模型保存与恢复
├── requirements.txt
└── README.md                 # 复现说明
```

### 超参数调优报告

```markdown
## 超参数搜索报告

**搜索方法：** Optuna (TPE Sampler)
**总试验数：** 50
**最佳结果：** val_f1 = 0.8924
**搜索耗时：** 3h 24min

### 最佳超参数配置

| 参数 | 最佳值 | 搜索范围 |
|------|--------|----------|
| learning_rate | 2.8e-5 | [1e-5, 5e-5] |
| batch_size | 32 | {16, 32, 64} |
| warmup_ratio | 0.12 | [0.05, 0.2] |
| dropout | 0.15 | [0.05, 0.4] |
| weight_decay | 0.012 | [0.0, 0.1] |

### 参数重要性分析（SHAP 值）

1. learning_rate — 重要性：0.41
2. warmup_ratio  — 重要性：0.24
3. batch_size    — 重要性：0.18
4. dropout       — 重要性：0.12
5. weight_decay  — 重要性：0.05

### 性能分布图

（见 hyperparameter_report.html 中的交互式图表）
```

### 训练诊断报告

```markdown
## 训练诊断报告

**状态：** 检测到 2 个问题

### 问题 1：梯度消失 [严重]
- **位置：** 第 1–3 层 Transformer block
- **症状：** gradient_norm < 1e-6（连续 20 epoch）
- **建议：**
  1. 使用梯度裁剪（`torch.nn.utils.clip_grad_norm_`，阈值 1.0）
  2. 检查权重初始化（推荐 Xavier 或 Kaiming）
  3. 考虑添加残差连接

### 问题 2：过拟合 [中等]
- **症状：** train_loss=0.12 vs val_loss=0.45（gap=0.33）
- **建议：**
  1. 增加 dropout（当前 0.1 → 建议 0.2–0.3）
  2. 添加 weight_decay（当前 0 → 建议 1e-4）
  3. 减少训练 epoch（Early Stopping patience=5）
  4. 数据增强（当前数据集偏小）
```

### SOTA 对比报告

```markdown
## SOTA 对比：SST-2 文本分类

**你的结果：** Accuracy = 94.2%
**数据来源：** Papers with Code (2024-01)

| 排名 | 方法 | Accuracy | 论文 |
|------|------|----------|------|
| 1 | DeBERTa-v3-large (fine-tuned) | 97.2% | He et al., 2021 |
| 2 | RoBERTa-large | 96.4% | Liu et al., 2019 |
| 3 | BERT-large | 94.9% | Devlin et al., 2019 |
| — | **你的方法** | **94.2%** | — |
| 4 | BERT-base | 93.5% | Devlin et al., 2019 |

**分析：** 你的方法超过 BERT-large 基线 0.7%，比 SOTA 低 3.0%。
建议参考 DeBERTa-v3 的 disentangled attention 设计进一步提升。
```
