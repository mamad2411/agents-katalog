---
name: lambda-labs
description: On-demand GPU cloud instances for ML training.
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [lambda-cloud-client>=1.0.0]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Infrastructure, GPU Cloud, Training, Inference, Lambda Labs]

---

# Lambda Labs GPU 云平台

本指南介绍如何使用 Lambda Labs GPU 云平台上的按需实例及一键集群功能来运行机器学习工作负载。

## 何时选择 Lambda Labs

**以下情况适合使用 Lambda Labs：**
- 需要具备完整 SSH 访问权限的专用 GPU 实例
- 需要运行耗时较长的训练任务（数小时至数天）
- 希望享受无数据输出费用且定价简单的服务
- 需要在不同会话之间保持数据持久化
- 需要高性能的多节点集群（16–512 个 GPU）
- 希望使用预安装的机器学习套件（包含 PyTorch、CUDA、NCCL 的 Lambda Stack）

**主要功能：**
- **多种 GPU 选择**：B200、H100、GH200、A100、A10、A6000、V100
- **Lambda Stack**：预安装了 PyTorch、TensorFlow、CUDA、cuDNN、NCCL
- **持久化文件系统**：确保数据在实例重启后依然保留
- **一键集群功能**：支持配备 InfiniBand 的 16–512 个 GPU Slurm 集群
- **简单透明的定价**：按分钟计费，无数据输出费用
- **全球多区域部署**：覆盖全球 12 个以上地区

**如需其他替代方案，请考虑：**
- **Modal**：适用于无服务器及自动扩展型工作负载
- **SkyPilot**：用于多云资源编排与成本优化
- **RunPod**：提供更便宜的按需实例及无服务器端点
- **Vast.ai**：拥有价格最低的 GPU 市场平台

## 快速入门

### 账户创建

1. 访问 https://lambda.ai 创建账户
2. 添加支付方式
3. 通过控制面板生成 API 密钥
4. 添加 SSH 密钥（启动实例前必需）

### 通过控制台启动实例

1. 访问 https://cloud.lambda.ai/instances  
2. 点击“启动实例”  
3. 选择GPU类型与区域  
4. 选定SSH密钥  
5. 如有需要，可附加文件系统  
6. 启动实例并等待3至15分钟  

### 通过SSH连接

```bash
# Get instance IP from console
ssh ubuntu@<INSTANCE-IP>

# Or with specific key
ssh -i ~/.ssh/lambda_key ubuntu@<INSTANCE-IP>
```

## GPU实例

### 可用GPU型号

| GPU | 显存容量 | 每小时价格 | 最佳适用场景 |
|-----|----------|--------------|------------|
| B200 SXM6 | 180 GB | $4.99 | 大型模型训练，追求最快训练速度 |
| H100 SXM | 80 GB | $2.99-3.29 | 大型模型训练 |
| H100 PCIe | 80 GB | $2.49 | 性价比高的H100方案 |
| GH200 | 96 GB | $1.49 | 单GPU驱动的大型模型训练 |
| A100 80GB | 80 GB | $1.79 | 生产环境训练 |
| A100 40GB | 40 GB | $1.29 | 标准训练任务 |
| A10 | 24 GB | $0.75 | 推理及模型微调 |
| A6000 | 48 GB | $0.80 | 显存容量与价格比优异 |
| V100 | 16 GB | $0.55 | 预算有限的训练场景 |

### 实例配置选项

```
8x GPU: Best for distributed training (DDP, FSDP)
4x GPU: Large models, multi-GPU training
2x GPU: Medium workloads
1x GPU: Fine-tuning, inference, development
```

### 启动时间

- 单 GPU：3-5 分钟
- 多 GPU：10-15 分钟

## Lambda Stack

所有实例均预装了 Lambda Stack：

```bash
# Included software
- Ubuntu 22.04 LTS
- NVIDIA drivers (latest)
- CUDA 12.x
- cuDNN 8.x
- NCCL (for multi-GPU)
- PyTorch (latest)
- TensorFlow (latest)
- JAX
- JupyterLab
```

### 验证安装情况

```bash
# Check GPU
nvidia-smi

# Check PyTorch
python -c "import torch; print(torch.cuda.is_available())"

# Check CUDA version
nvcc --version
```

## Python API

### 安装指南

```bash
pip install lambda-cloud-client
```

### 认证

```python
import os
import lambda_cloud_client

# Configure with API key
configuration = lambda_cloud_client.Configuration(
    host="https://cloud.lambdalabs.com/api/v1",
    access_token=os.environ["LAMBDA_API_KEY"]
)
```

### 列出可用实例

```python
with lambda_cloud_client.ApiClient(configuration) as api_client:
    api = lambda_cloud_client.DefaultApi(api_client)

    # Get available instance types
    types = api.instance_types()
    for name, info in types.data.items():
        print(f"{name}: {info.instance_type.description}")
```

### 启动实例

```python
from lambda_cloud_client.models import LaunchInstanceRequest

request = LaunchInstanceRequest(
    region_name="us-west-1",
    instance_type_name="gpu_1x_h100_sxm5",
    ssh_key_names=["my-ssh-key"],
    file_system_names=["my-filesystem"],  # Optional
    name="training-job"
)

response = api.launch_instance(request)
instance_id = response.data.instance_ids[0]
print(f"Launched: {instance_id}")
```

### 列出正在运行的实例

```python
instances = api.list_instances()
for instance in instances.data:
    print(f"{instance.name}: {instance.ip} ({instance.status})")
```

### 终止实例

```python
from lambda_cloud_client.models import TerminateInstanceRequest

request = TerminateInstanceRequest(
    instance_ids=[instance_id]
)
api.terminate_instance(request)
```

### SSH密钥管理

```python
from lambda_cloud_client.models import AddSshKeyRequest

# Add SSH key
request = AddSshKeyRequest(
    name="my-key",
    public_key="ssh-rsa AAAA..."
)
api.add_ssh_key(request)

# List keys
keys = api.list_ssh_keys()

# Delete key
api.delete_ssh_key(key_id)
```

## 使用 curl 的 CLI

### 列出实例类型

```bash
curl -u $LAMBDA_API_KEY: \
  https://cloud.lambdalabs.com/api/v1/instance-types | jq
```

### 启动实例

```bash
curl -u $LAMBDA_API_KEY: \
  -X POST https://cloud.lambdalabs.com/api/v1/instance-operations/launch \
  -H "Content-Type: application/json" \
  -d '{
    "region_name": "us-west-1",
    "instance_type_name": "gpu_1x_h100_sxm5",
    "ssh_key_names": ["my-key"]
  }' | jq
```

### 终止实例

```bash
curl -u $LAMBDA_API_KEY: \
  -X POST https://cloud.lambdalabs.com/api/v1/instance-operations/terminate \
  -H "Content-Type: application/json" \
  -d '{"instance_ids": ["<INSTANCE-ID>"]}' | jq
```

## 持久存储

### 文件系统

文件系统能够在实例重启后依然保留数据：

```bash
# Mount location
/lambda/nfs/<FILESYSTEM_NAME>

# Example: save checkpoints
python train.py --checkpoint-dir /lambda/nfs/my-storage/checkpoints
```

### 创建文件系统

1. 进入 Lambda 控制台的存储管理页面。
2. 点击“创建文件系统”。
3. 选择区域（必须与实例所在区域一致）。
4. 命名并创建。

### 连接到实例

文件系统必须在实例启动时进行关联：
- 通过控制台操作：在启动实例时选择相应的文件系统。
- 通过 API 操作：在启动请求中包含 `file_system_names` 参数。

### 最佳实践

```bash
# Store on filesystem (persists)
/lambda/nfs/storage/
  ├── datasets/
  ├── checkpoints/
  ├── models/
  └── outputs/

# Local SSD (faster, ephemeral)
~/ (instance home)
  └── working/  # Temporary files
```

## SSH 配置

### 添加 SSH 密钥

```bash
# Generate key locally
ssh-keygen -t ed25519 -f ~/.ssh/lambda_key

# Add public key to Lambda console
# Or via API
```

### 多个密钥

```bash
# On instance, add more keys
echo 'ssh-rsa AAAA...' >> ~/.ssh/authorized_keys
```

### 从 GitHub 导入

```bash
# On instance
ssh-import-id gh:username
```

### SSH 隧道传输

```bash
# Forward Jupyter
ssh -L 8888:localhost:8888 ubuntu@<IP>

# Forward TensorBoard
ssh -L 6006:localhost:6006 ubuntu@<IP>

# Multiple ports
ssh -L 8888:localhost:8888 -L 6006:localhost:6006 ubuntu@<IP>
```

## JupyterLab

### 通过控制台启动

1. 进入“实例”页面
2. 点击“云 IDE”列中的“启动”按钮
3. JupyterLab即会在浏览器中打开

### 手动访问

```bash
# On instance
jupyter lab --ip=0.0.0.0 --port=8888

# From local machine with tunnel
ssh -L 8888:localhost:8888 ubuntu@<IP>
# Open http://localhost:8888
```

## 训练工作流

### 单 GPU 训练

```bash
# SSH to instance
ssh ubuntu@<IP>

# Clone repo
git clone https://github.com/user/project
cd project

# Install dependencies
pip install -r requirements.txt

# Train
python train.py --epochs 100 --checkpoint-dir /lambda/nfs/storage/checkpoints
```

### 多 GPU 训练（单节点）

```python
# train_ddp.py
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def main():
    dist.init_process_group("nccl")
    rank = dist.get_rank()
    device = rank % torch.cuda.device_count()

    model = MyModel().to(device)
    model = DDP(model, device_ids=[device])

    # Training loop...

if __name__ == "__main__":
    main()
```

```bash
# Launch with torchrun (8 GPUs)
torchrun --nproc_per_node=8 train_ddp.py
```

### 将检查点保存至文件系统

```python
import os

checkpoint_dir = "/lambda/nfs/my-storage/checkpoints"
os.makedirs(checkpoint_dir, exist_ok=True)

# Save checkpoint
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, f"{checkpoint_dir}/checkpoint_{epoch}.pt")
```

## 一键式集群

### 概述

高性能 Slurm 集群，具备以下配置：
- 16–512 块 NVIDIA H100 或 B200 GPU
- NVIDIA Quantum-2 400 Gb/s InfiniBand 网络
- 3200 Gb/s 的 GPUDirect RDMA 技术
- 预装好的分布式机器学习框架栈

### 包含的软件

- Ubuntu 22.04 LTS 操作系统 + Lambda Stack 框架
- NCCL、Open MPI 工具
- 支持 DDP 和 FSDP 模式的 PyTorch
- TensorFlow 框架
- OFED 驱动程序

### 存储方案

- 每个计算节点配备 24 TB NVMe 存储（临时数据存储）
- 使用 Lambda 文件系统用于持久化数据存储

### 多节点训练功能

```bash
# On Slurm cluster
srun --nodes=4 --ntasks-per-node=8 --gpus-per-node=8 \
  torchrun --nnodes=4 --nproc_per_node=8 \
  --rdzv_backend=c10d --rdzv_endpoint=$MASTER_ADDR:29500 \
  train.py
```

## 网络连接

### 带宽

- 实例间（同一区域）：最高可达 200 Gbps
- 接入互联网的出站带宽：最高为 20 Gbps

### 防火墙

- 默认设置：仅开放端口 22（SSH）
- 可在 Lambda 控制台配置其他端口
- 默认允许 ICMP 流量

### 私有 IP 地址

```bash
# Find private IP
ip addr show | grep 'inet '
```

## 常见工作流程

### 工作流程 1：大语言模型微调

```bash
# 1. Launch 8x H100 instance with filesystem

# 2. SSH and setup
ssh ubuntu@<IP>
pip install transformers accelerate peft

# 3. Download model to filesystem
python -c "
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained('meta-llama/Llama-2-7b-hf')
model.save_pretrained('/lambda/nfs/storage/models/llama-2-7b')
"

# 4. Fine-tune with checkpoints on filesystem
accelerate launch --num_processes 8 train.py \
  --model_path /lambda/nfs/storage/models/llama-2-7b \
  --output_dir /lambda/nfs/storage/outputs \
  --checkpoint_dir /lambda/nfs/storage/checkpoints
```

### 工作流 2：批量推理

```bash
# 1. Launch A10 instance (cost-effective for inference)

# 2. Run inference
python inference.py \
  --model /lambda/nfs/storage/models/fine-tuned \
  --input /lambda/nfs/storage/data/inputs.jsonl \
  --output /lambda/nfs/storage/data/outputs.jsonl
```

## 成本优化

### 选择合适的 GPU

| 任务 | 推荐 GPU |
|------|----------|
| LLM 微调（70亿参数） | A100 40GB |
| LLM 微调（700亿参数） | 8台 H100 |
| 推理任务 | A10、A6000 |
| 开发测试 | V100、A10 |
| 最高性能需求 | B200 |

### 降低成本

1. **使用文件系统**：避免重复下载数据
2. **频繁保存检查点**：便于从中断处继续训练
3. **合理配置资源**：避免过度分配 GPU 资源
4. **手动终止空闲实例**：不设置自动停止功能，需手动操作

### 监控使用情况

- 控制面板可实时显示 GPU 使用率
- 提供 API 用于程序化监控

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 实例无法启动 | 检查所在区域是否可用，尝试更换其他 GPU |
| SSH 连接被拒绝 | 等待实例完成初始化（需3-15分钟） |
| 终止实例后数据丢失 | 使用持久化文件系统 |
| 数据传输速度慢 | 使用同一区域的文件系统 |
| 无法检测到 GPU | 重启实例，检查驱动程序 |

## 参考资料

- **[高级用法](references/advanced-usage.md)** - 多节点训练、API 自动化
- **[故障排除](references/troubleshooting.md)** - 常见问题及解决方案

## 资源链接

- **文档**：https://docs.lambda.ai
- **控制台**：https://cloud.lambda.ai
- **价格信息**：https://lambda.ai/instances
- **技术支持**：https://support.lambdalabs.com
- **博客**：https://lambda.ai/blog
