---
name: skypilot-multi-cloud-orchestration
description: Orquestração multi-nuvem para workloads de ML com otimização automática de custos. Use quando precisar executar treinamento ou jobs em lote em múltiplas nuvens, aproveitar instâncias spot com auto-recuperação ou otimizar custos de GPU entre provedores.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Infrastructure, Multi-Cloud, Orchestration, GPU, Cost Optimization, SkyPilot]
dependencies: [skypilot>=0.7.0]
---

# SkyPilot Multi-Cloud Orchestration

Guia abrangente para executar workloads de ML entre nuvens com otimização automática de custos usando SkyPilot.

## Quando usar SkyPilot

**Use SkyPilot quando:**
- Executar workloads de ML em múltiplas nuvens (AWS, GCP, Azure, etc.)
- Precisar de otimização de custos com seleção automática de nuvem/região
- Executar jobs longos em instâncias spot com auto-recuperação
- Gerenciar treinamento distribuído multi-nó
- Quiser interface unificada para 20+ provedores de nuvem
- Precisar evitar vendor lock-in

**Principais características:**
- **Multi-nuvem**: AWS, GCP, Azure, Kubernetes, Lambda, RunPod, 20+ provedores
- **Otimização de custos**: Seleção automática da nuvem/região mais barata
- **Instâncias spot**: Economia de 3-6x com recuperação automática
- **Treinamento distribuído**: Jobs multi-nó com gang scheduling
- **Jobs gerenciados**: Auto-recuperação, checkpointing, tolerância a falhas
- **Sky Serve**: Serving de modelos com autoscaling

**Use alternativas em vez disso:**
- **Modal**: Para serverless GPU mais simples com API nativa em Python
- **RunPod**: Para pods persistentes em nuvem única
- **Kubernetes**: Para infraestrutura K8s existente
- **Ray**: Para orquestração pura baseada em Ray

## Quick start

### Installation

```bash
pip install "skypilot[aws,gcp,azure,kubernetes]"

# Verificar credenciais de nuvem
sky check
```

### Hello World

Crie `hello.yaml`:
```yaml
resources:
  accelerators: T4:1

run: |
  nvidia-smi
  echo "Hello from SkyPilot!"
```

Inicie:
```bash
sky launch -c hello hello.yaml

# SSH para o cluster
ssh hello

# Terminar
sky down hello
```

## Conceitos principais

### Estrutura de Task YAML

```yaml
# Nome da task (opcional)
name: my-task

# Requisitos de recurso
resources:
  cloud: aws              # Opcional: auto-selecionar se omitido
  region: us-west-2       # Opcional: auto-selecionar se omitido
  accelerators: A100:4    # Tipo e quantidade de GPU
  cpus: 8+                # Mínimo de CPUs
  memory: 32+             # Memória mínima (GB)
  use_spot: true          # Usar instâncias spot
  disk_size: 256          # Tamanho do disco (GB)

# Número de nós para treinamento distribuído
num_nodes: 2

# Diretório de trabalho (sincronizado para ~/sky_workdir)
workdir: .

# Comandos de setup (executados uma vez)
setup: |
  pip install -r requirements.txt

# Comandos de execução
run: |
  python train.py
```

### Comandos principais

| Comando | Propósito |
|---------|-----------|
| `sky launch` | Iniciar cluster e executar task |
| `sky exec` | Executar task em cluster existente |
| `sky status` | Mostrar status do cluster |
| `sky stop` | Parar cluster (preservar estado) |
| `sky down` | Terminar cluster |
| `sky logs` | Visualizar logs da task |
| `sky queue` | Mostrar fila de jobs |
| `sky jobs launch` | Iniciar job gerenciado |
| `sky serve up` | Implantar endpoint de serving |

## Configuração de GPU

### Aceleradores disponíveis

```yaml
# NVIDIA GPUs
accelerators: T4:1
accelerators: L4:1
accelerators: A10G:1
accelerators: L40S:1
accelerators: A100:4
accelerators: A100-80GB:8
accelerators: H100:8

# Cloud-específico
accelerators: V100:4         # AWS/GCP
accelerators: TPU-v4-8       # GCP TPUs
```

### Fallbacks de GPU

```yaml
resources:
  accelerators:
    H100: 8
    A100-80GB: 8
    A100: 8
  any_of:
    - cloud: gcp
    - cloud: aws
    - cloud: azure
```

### Instâncias spot

```yaml
resources:
  accelerators: A100:8
  use_spot: true
  spot_recovery: FAILOVER  # Auto-recuperar em preempção
```

## Gerenciamento de cluster

### Iniciar e executar

```bash
# Iniciar novo cluster
sky launch -c mycluster task.yaml

# Executar em cluster existente (pular setup)
sky exec mycluster another_task.yaml

# SSH interativo
ssh mycluster

# Stream de logs
sky logs mycluster
```

### Autostop

```yaml
resources:
  accelerators: A100:4
  autostop:
    idle_minutes: 30
    down: true  # Terminar em vez de parar
```

```bash
# Definir autostop via CLI
sky autostop mycluster -i 30 --down
```

### Status do cluster

```bash
# Todos os clusters
sky status

# Visualização detalhada
sky status -a
```

## Treinamento distribuído

### Configuração multi-nó

```yaml
resources:
  accelerators: A100:8

num_nodes: 4  # 4 nós × 8 GPUs = 32 GPUs total

setup: |
  pip install torch torchvision

run: |
  torchrun \
    --nnodes=$SKYPILOT_NUM_NODES \
    --nproc_per_node=$SKYPILOT_NUM_GPUS_PER_NODE \
    --node_rank=$SKYPILOT_NODE_RANK \
    --master_addr=$(echo "$SKYPILOT_NODE_IPS" | head -n1) \
    --master_port=12355 \
    train.py
```

### Variáveis de ambiente

| Variável | Descrição |
|----------|-----------|
| `SKYPILOT_NODE_RANK` | Índice do nó (0 a num_nodes-1) |
| `SKYPILOT_NODE_IPS` | Endereços IP separados por quebra de linha |
| `SKYPILOT_NUM_NODES` | Número total de nós |
| `SKYPILOT_NUM_GPUS_PER_NODE` | GPUs por nó |

### Execução somente no nó head

```bash
run: |
  if [ "${SKYPILOT_NODE_RANK}" == "0" ]; then
    python orchestrate.py
  fi
```

## Jobs gerenciados

### Recuperação de spot

```bash
# Iniciar job gerenciado com recuperação de spot
sky jobs launch -n my-job train.yaml
```

### Checkpointing

```yaml
name: training-job

file_mounts:
  /checkpoints:
    name: my-checkpoints
    store: s3
    mode: MOUNT

resources:
  accelerators: A100:8
  use_spot: true

run: |
  python train.py \
    --checkpoint-dir /checkpoints \
    --resume-from-latest
```

### Gerenciamento de jobs

```bash
# Listar jobs
sky jobs queue

# Visualizar logs
sky jobs logs my-job

# Cancelar job
sky jobs cancel my-job
```

## File mounts e armazenamento

### Sincronização de arquivo local

```yaml
workdir: ./my-project  # Sincronizado para ~/sky_workdir

file_mounts:
  /data/config.yaml: ./config.yaml
  ~/.vimrc: ~/.vimrc
```

### Armazenamento em nuvem

```yaml
file_mounts:
  # Montar bucket S3
  /datasets:
    source: s3://my-bucket/datasets
    mode: MOUNT  # Transmitir do S3

  # Copiar bucket GCS
  /models:
    source: gs://my-bucket/models
    mode: COPY  # Pré-buscar para disco

  # Cache mount (escritas rápidas)
  /outputs:
    name: my-outputs
    store: s3
    mode: MOUNT_CACHED
```

### Modos de armazenamento

| Modo | Descrição | Melhor para |
|------|-----------|------------|
| `MOUNT` | Transmitir da nuvem | Datasets grandes, leitura intensiva |
| `COPY` | Pré-buscar para disco | Arquivos pequenos, acesso aleatório |
| `MOUNT_CACHED` | Cache com upload assíncrono | Checkpoints, outputs |

## Sky Serve (Model Serving)

### Serviço básico

```yaml
# service.yaml
service:
  readiness_probe: /health
  replica_policy:
    min_replicas: 1
    max_replicas: 10
    target_qps_per_replica: 2.0

resources:
  accelerators: A100:1

run: |
  python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-2-7b-chat-hf \
    --port 8000
```

```bash
# Implantar
sky serve up -n my-service service.yaml

# Verificar status
sky serve status

# Obter endpoint
sky serve status my-service
```

### Políticas de autoscaling

```yaml
service:
  replica_policy:
    min_replicas: 1
    max_replicas: 10
    target_qps_per_replica: 2.0
    upscale_delay_seconds: 60
    downscale_delay_seconds: 300
  load_balancing_policy: round_robin
```

## Otimização de custos

### Seleção automática de nuvem

```yaml
# SkyPilot encontra a opção mais barata
resources:
  accelerators: A100:8
  # Nenhuma nuvem especificada - auto-selecionar mais barata
```

```bash
# Mostrar decisão do otimizador
sky launch task.yaml --dryrun
```

### Preferências de nuvem

```yaml
resources:
  accelerators: A100:8
  any_of:
    - cloud: gcp
      region: us-central1
    - cloud: aws
      region: us-east-1
    - cloud: azure
```

### Variáveis de ambiente

```yaml
envs:
  HF_TOKEN: $HF_TOKEN  # Herdado do env local
  WANDB_API_KEY: $WANDB_API_KEY

# Ou usar secrets
secrets:
  - HF_TOKEN
  - WANDB_API_KEY
```

## Workflows comuns

### Workflow 1: Fine-tuning com checkpoints

```yaml
name: llm-finetune

file_mounts:
  /checkpoints:
    name: finetune-checkpoints
    store: s3
    mode: MOUNT_CACHED

resources:
  accelerators: A100:8
  use_spot: true

setup: |
  pip install transformers accelerate

run: |
  python train.py \
    --checkpoint-dir /checkpoints \
    --resume
```

### Workflow 2: Hyperparameter sweep

```yaml
name: hp-sweep-${RUN_ID}

envs:
  RUN_ID: 0
  LEARNING_RATE: 1e-4
  BATCH_SIZE: 32

resources:
  accelerators: A100:1
  use_spot: true

run: |
  python train.py \
    --lr $LEARNING_RATE \
    --batch-size $BATCH_SIZE \
    --run-id $RUN_ID
```

```bash
# Iniciar múltiplos jobs
for i in {1..10}; do
  sky jobs launch sweep.yaml \
    --env RUN_ID=$i \
    --env LEARNING_RATE=$(python -c "import random; print(10**random.uniform(-5,-3))")
done
```

## Debugging

```bash
# SSH para o cluster
ssh mycluster

# Visualizar logs
sky logs mycluster

# Verificar fila de jobs
sky queue mycluster

# Visualizar logs de job gerenciado
sky jobs logs my-job
```

## Problemas comuns

| Problema | Solução |
|----------|---------|
| Quota excedida | Solicitar aumento de quota, tentar região diferente |
| Preempção de spot | Usar `sky jobs launch` para auto-recuperação |
| Sincronização de arquivo lenta | Usar modo `MOUNT_CACHED` para outputs |
| GPU não disponível | Usar `any_of` para fallback de nuvens |

## Referências

- **[Advanced Usage](references/advanced-usage.md)** - Multi-nuvem, otimização, padrões de produção
- **[Troubleshooting](references/troubleshooting.md)** - Problemas comuns e soluções

## Recursos

- **Documentation**: https://docs.skypilot.co
- **GitHub**: https://github.com/skypilot-org/skypilot
- **Slack**: https://slack.skypilot.co
- **Examples**: https://github.com/skypilot-org/skypilot/tree/master/examples