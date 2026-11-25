---
name: lambda-labs-gpu-cloud
description: Instâncias GPU em nuvem reservadas e sob demanda para treinamento e inferência de ML. Use quando você precisar de instâncias GPU dedicadas com acesso SSH simples, sistemas de arquivos persistentes ou clusters multi-node de alto desempenho para treinamento em larga escala.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Infrastructure, GPU Cloud, Training, Inference, Lambda Labs]
dependencies: [lambda-cloud-client>=1.0.0]
---

# Lambda Labs GPU Cloud

Guia abrangente para executar cargas de trabalho de ML em GPU cloud da Lambda Labs com instâncias sob demanda e Clusters 1-Click.

## Quando usar Lambda Labs

**Use Lambda Labs quando:**
- Você precisa de instâncias GPU dedicadas com acesso SSH completo
- Executando trabalhos de treinamento longos (horas a dias)
- Quer preços simples sem taxas de saída
- Precisa de armazenamento persistente entre sessões
- Requer clusters multi-node de alto desempenho (16-512 GPUs)
- Quer stack ML pré-instalado (Lambda Stack com PyTorch, CUDA, NCCL)

**Características principais:**
- **Variedade de GPUs**: B200, H100, GH200, A100, A10, A6000, V100
- **Lambda Stack**: PyTorch, TensorFlow, CUDA, cuDNN, NCCL pré-instalados
- **Sistemas de arquivos persistentes**: Mantenha dados entre reinicializações de instância
- **Clusters 1-Click**: Clusters Slurm de 16-512 GPUs com InfiniBand
- **Preços simples**: Pague por minuto, sem taxas de saída
- **Regiões globais**: 12+ regiões em todo o mundo

**Use alternativas:**
- **Modal**: Para cargas de trabalho serverless e auto-scaling
- **SkyPilot**: Para orquestração multi-cloud e otimização de custos
- **RunPod**: Para instâncias spot mais baratas e endpoints serverless
- **Vast.ai**: Para marketplace de GPU com preços mais baixos

## Quick start

### Configuração de conta

1. Crie conta em https://lambda.ai
2. Adicione método de pagamento
3. Gere chave API do dashboard
4. Adicione chave SSH (obrigatório antes de iniciar instâncias)

### Iniciar via console

1. Vá para https://cloud.lambda.ai/instances
2. Clique em "Launch instance"
3. Selecione tipo de GPU e região
4. Escolha chave SSH
5. Opcionalmente anexe filesystem
6. Inicie e aguarde 3-15 minutos

### Conectar via SSH

```bash
# Obtenha IP da instância do console
ssh ubuntu@<INSTANCE-IP>

# Ou com chave específica
ssh -i ~/.ssh/lambda_key ubuntu@<INSTANCE-IP>
```

## Instâncias GPU

### GPUs disponíveis

| GPU | VRAM | Preço/GPU/hr | Melhor Para |
|-----|------|--------------|----------|
| B200 SXM6 | 180 GB | $4.99 | Maiores modelos, treinamento mais rápido |
| H100 SXM | 80 GB | $2.99-3.29 | Treinamento de modelos grandes |
| H100 PCIe | 80 GB | $2.49 | H100 com melhor custo-benefício |
| GH200 | 96 GB | $1.49 | Modelos grandes com uma GPU |
| A100 80GB | 80 GB | $1.79 | Treinamento em produção |
| A100 40GB | 40 GB | $1.29 | Treinamento padrão |
| A10 | 24 GB | $0.75 | Inferência, fine-tuning |
| A6000 | 48 GB | $0.80 | Bom ratio VRAM/preço |
| V100 | 16 GB | $0.55 | Treinamento com orçamento limitado |

### Configurações de instância

```
8x GPU: Melhor para treinamento distribuído (DDP, FSDP)
4x GPU: Modelos grandes, treinamento multi-GPU
2x GPU: Cargas de trabalho médias
1x GPU: Fine-tuning, inferência, desenvolvimento
```

### Tempos de inicialização

- Single-GPU: 3-5 minutos
- Multi-GPU: 10-15 minutos

## Lambda Stack

Todas as instâncias vêm com Lambda Stack pré-instalado:

```bash
# Software incluído
- Ubuntu 22.04 LTS
- NVIDIA drivers (versão mais recente)
- CUDA 12.x
- cuDNN 8.x
- NCCL (para multi-GPU)
- PyTorch (versão mais recente)
- TensorFlow (versão mais recente)
- JAX
- JupyterLab
```

### Verificar instalação

```bash
# Verificar GPU
nvidia-smi

# Verificar PyTorch
python -c "import torch; print(torch.cuda.is_available())"

# Verificar versão CUDA
nvcc --version
```

## Python API

### Instalação

```bash
pip install lambda-cloud-client
```

### Autenticação

```python
import os
import lambda_cloud_client

# Configure com chave API
configuration = lambda_cloud_client.Configuration(
    host="https://cloud.lambdalabs.com/api/v1",
    access_token=os.environ["LAMBDA_API_KEY"]
)
```

### Listar instâncias disponíveis

```python
with lambda_cloud_client.ApiClient(configuration) as api_client:
    api = lambda_cloud_client.DefaultApi(api_client)

    # Obtenha tipos de instância disponíveis
    types = api.instance_types()
    for name, info in types.data.items():
        print(f"{name}: {info.instance_type.description}")
```

### Iniciar instância

```python
from lambda_cloud_client.models import LaunchInstanceRequest

request = LaunchInstanceRequest(
    region_name="us-west-1",
    instance_type_name="gpu_1x_h100_sxm5",
    ssh_key_names=["my-ssh-key"],
    file_system_names=["my-filesystem"],  # Opcional
    name="training-job"
)

response = api.launch_instance(request)
instance_id = response.data.instance_ids[0]
print(f"Launched: {instance_id}")
```

### Listar instâncias em execução

```python
instances = api.list_instances()
for instance in instances.data:
    print(f"{instance.name}: {instance.ip} ({instance.status})")
```

### Encerrar instância

```python
from lambda_cloud_client.models import TerminateInstanceRequest

request = TerminateInstanceRequest(
    instance_ids=[instance_id]
)
api.terminate_instance(request)
```

### Gerenciamento de chaves SSH

```python
from lambda_cloud_client.models import AddSshKeyRequest

# Adicionar chave SSH
request = AddSshKeyRequest(
    name="my-key",
    public_key="ssh-rsa AAAA..."
)
api.add_ssh_key(request)

# Listar chaves
keys = api.list_ssh_keys()

# Deletar chave
api.delete_ssh_key(key_id)
```

## CLI com curl

### Listar tipos de instância

```bash
curl -u $LAMBDA_API_KEY: \
  https://cloud.lambdalabs.com/api/v1/instance-types | jq
```

### Iniciar instância

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

### Encerrar instância

```bash
curl -u $LAMBDA_API_KEY: \
  -X POST https://cloud.lambdalabs.com/api/v1/instance-operations/terminate \
  -H "Content-Type: application/json" \
  -d '{"instance_ids": ["<INSTANCE-ID>"]}' | jq
```

## Armazenamento persistente

### Filesystems

Filesystems persistem dados entre reinicializações de instância:

```bash
# Local de montagem
/lambda/nfs/<FILESYSTEM_NAME>

# Exemplo: salvar checkpoints
python train.py --checkpoint-dir /lambda/nfs/my-storage/checkpoints
```

### Criar filesystem

1. Vá para Storage no console Lambda
2. Clique em "Create filesystem"
3. Selecione região (deve corresponder à região da instância)
4. Nomeie e crie

### Anexar à instância

Filesystems devem ser anexados no tempo de inicialização da instância:
- Via console: Selecione filesystem ao iniciar
- Via API: Inclua `file_system_names` na solicitação de inicialização

### Melhores práticas

```bash
# Armazenar em filesystem (persiste)
/lambda/nfs/storage/
  ├── datasets/
  ├── checkpoints/
  ├── models/
  └── outputs/

# SSD local (mais rápido, efêmero)
/home/ubuntu/
  └── working/  # Arquivos temporários
```

## Configuração SSH

### Adicionar chave SSH

```bash
# Gere chave localmente
ssh-keygen -t ed25519 -f ~/.ssh/lambda_key

# Adicione chave pública ao console Lambda
# Ou via API
```

### Múltiplas chaves

```bash
# Na instância, adicione mais chaves
echo 'ssh-rsa AAAA...' >> ~/.ssh/authorized_keys
```

### Importar do GitHub

```bash
# Na instância
ssh-import-id gh:username
```

### SSH tunneling

```bash
# Encaminhar Jupyter
ssh -L 8888:localhost:8888 ubuntu@<IP>

# Encaminhar TensorBoard
ssh -L 6006:localhost:6006 ubuntu@<IP>

# Múltiplas portas
ssh -L 8888:localhost:8888 -L 6006:localhost:6006 ubuntu@<IP>
```

## JupyterLab

### Iniciar do console

1. Vá para a página Instances
2. Clique em "Launch" na coluna Cloud IDE
3. JupyterLab abre no navegador

### Acesso manual

```bash
# Na instância
jupyter lab --ip=0.0.0.0 --port=8888

# Da máquina local com tunnel
ssh -L 8888:localhost:8888 ubuntu@<IP>
# Abra http://localhost:8888
```

## Workflows de treinamento

### Treinamento com uma GPU

```bash
# SSH para instância
ssh ubuntu@<IP>

# Clone repo
git clone https://github.com/user/project
cd project

# Instale dependências
pip install -r requirements.txt

# Treine
python train.py --epochs 100 --checkpoint-dir /lambda/nfs/storage/checkpoints
```

### Treinamento multi-GPU (nó único)

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
# Iniciar com torchrun (8 GPUs)
torchrun --nproc_per_node=8 train_ddp.py
```

### Checkpoint para filesystem

```python
import os

checkpoint_dir = "/lambda/nfs/my-storage/checkpoints"
os.makedirs(checkpoint_dir, exist_ok=True)

# Salve checkpoint
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, f"{checkpoint_dir}/checkpoint_{epoch}.pt")
```

## Clusters 1-Click

### Visão geral

Clusters Slurm de alto desempenho com:
- 16-512 GPUs NVIDIA H100 ou B200
- InfiniBand NVIDIA Quantum-2 400 Gb/s
- GPUDirect RDMA em 3200 Gb/s
- Stack ML distribuído pré-instalado

### Software incluído

- Ubuntu 22.04 LTS + Lambda Stack
- NCCL, Open MPI
- PyTorch com DDP e FSDP
- TensorFlow
- Drivers OFED

### Armazenamento

- 24 TB NVMe por nó de computação (efêmero)
- Filesystems Lambda para dados persistentes

### Treinamento multi-node

```bash
# Em cluster Slurm
srun --nodes=4 --ntasks-per-node=8 --gpus-per-node=8 \
  torchrun --nnodes=4 --nproc_per_node=8 \
  --rdzv_backend=c10d --rdzv_endpoint=$MASTER_ADDR:29500 \
  train.py
```

## Rede

### Largura de banda

- Inter-instância (mesma região): até 200 Gbps
- Saída de internet: máx. 20 Gbps

### Firewall

- Padrão: Apenas porta 22 (SSH) aberta
- Configure portas adicionais no console Lambda
- Tráfego ICMP permitido por padrão

### IPs privados

```bash
# Encontre IP privado
ip addr show | grep 'inet '
```

## Workflows comuns

### Workflow 1: Fine-tuning de LLM

```bash
# 1. Iniciar instância 8x H100 com filesystem

# 2. SSH e configuração
ssh ubuntu@<IP>
pip install transformers accelerate peft

# 3. Baixe modelo para filesystem
python -c "
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained('meta-llama/Llama-2-7b-hf')
model.save_pretrained('/lambda/nfs/storage/models/llama-2-7b')
"

# 4. Fine-tune com checkpoints em filesystem
accelerate launch --num_processes 8 train.py \
  --model_path /lambda/nfs/storage/models/llama-2-7b \
  --output_dir /lambda/nfs/storage/outputs \
  --checkpoint_dir /lambda/nfs/storage/checkpoints
```

### Workflow 2: Inferência em lote

```bash
# 1. Iniciar instância A10 (custo-efetivo para inferência)

# 2. Execute inferência
python inference.py \
  --model /lambda/nfs/storage/models/fine-tuned \
  --input /lambda/nfs/storage/data/inputs.jsonl \
  --output /lambda/nfs/storage/data/outputs.jsonl
```

## Otimização de custos

### Escolha a GPU certa

| Tarefa | GPU Recomendada |
|-------|-----------------|
| Fine-tuning de LLM (7B) | A100 40GB |
| Fine-tuning de LLM (70B) | 8x H100 |
| Inferência | A10, A6000 |
| Desenvolvimento | V100, A10 |
| Máximo desempenho | B200 |

### Reduza custos

1. **Use filesystems**: Evite re-download de dados
2. **Checkpoint frequentemente**: Retome treinamento interrompido
3. **Right-size**: Não sobre-provisione GPUs
4. **Encerre idle**: Sem auto-stop, termine manualmente

### Monitore uso

- Dashboard mostra utilização de GPU em tempo real
- API para monitoramento programático

## Problemas comuns

| Problema | Solução |
|----------|---------|
| Instância não inicia | Verifique disponibilidade de região, tente GPU diferente |
| Conexão SSH recusada | Aguarde inicialização da instância (3-15 min) |
| Dados perdidos após encerramento | Use filesystems persistentes |
| Transferência de dados lenta | Use filesystem na mesma região |
| GPU não detectada | Reinicie instância, verifique drivers |

## Referências

- **[Uso Avançado](references/advanced-usage.md)** - Treinamento multi-node, automação de API
- **[Solução de Problemas](references/troubleshooting.md)** - Problemas comuns e soluções

## Recursos

- **Documentação**: https://docs.lambda.ai
- **Console**: https://cloud.lambda.ai
- **Preços**: https://lambda.ai/instances
- **Suporte**: https://support.lambdalabs.com
- **Blog**: https://lambda.ai/blog