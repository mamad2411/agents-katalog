---
name: ray-train
description: Orquestração de treinamento distribuído em clusters. Escala PyTorch/TensorFlow/HuggingFace do laptop para milhares de nós. Ajuste de hiperparâmetros integrado com Ray Tune, tolerância a falhas, escalabilidade elástica. Use ao treinar modelos massivos em múltiplas máquinas ou executar varreduras distribuídas de hiperparâmetros.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Ray Train, Distributed Training, Orchestration, Ray, Hyperparameter Tuning, Fault Tolerance, Elastic Scaling, Multi-Node, PyTorch, TensorFlow]
dependencies: [ray[train], torch, transformers]
---

# Ray Train - Orquestração de Treinamento Distribuído

## Início rápido

Ray Train escala treinamento de aprendizado de máquina de GPU única para clusters multi-nó com alterações mínimas no código.

**Instalação**:
```bash
pip install -U "ray[train]"
```

**Treinamento básico com PyTorch** (nó único):

```python
import ray
from ray import train
from ray.train import ScalingConfig
from ray.train.torch import TorchTrainer
import torch
import torch.nn as nn

# Define função de treinamento
def train_func(config):
    # Seu código PyTorch normal
    model = nn.Linear(10, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    # Prepare para distribuído (Ray gerencia alocação de devices)
    model = train.torch.prepare_model(model)

    for epoch in range(10):
        # Seu loop de treinamento
        output = model(torch.randn(32, 10))
        loss = output.sum()
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # Report métricas (logged automaticamente)
        train.report({"loss": loss.item(), "epoch": epoch})

# Execute treinamento distribuído
trainer = TorchTrainer(
    train_func,
    scaling_config=ScalingConfig(
        num_workers=4,  # 4 GPUs/workers
        use_gpu=True
    )
)

result = trainer.fit()
print(f"Final loss: {result.metrics['loss']}")
```

**Pronto!** Ray gerencia:
- Coordenação distribuída
- Alocação de GPU
- Tolerância a falhas
- Checkpointing
- Agregação de métricas

## Fluxos de trabalho comuns

### Fluxo 1: Escale código PyTorch existente

**Código original com GPU única**:
```python
model = MyModel().cuda()
optimizer = torch.optim.Adam(model.parameters())

for epoch in range(epochs):
    for batch in dataloader:
        loss = model(batch)
        loss.backward()
        optimizer.step()
```

**Versão Ray Train** (escala para multi-GPU/multi-nó):
```python
from ray.train.torch import TorchTrainer
from ray import train

def train_func(config):
    model = MyModel()
    optimizer = torch.optim.Adam(model.parameters())

    # Prepare para distribuído (alocação de device automática)
    model = train.torch.prepare_model(model)
    dataloader = train.torch.prepare_data_loader(dataloader)

    for epoch in range(epochs):
        for batch in dataloader:
            loss = model(batch)
            loss.backward()
            optimizer.step()

            # Report métricas
            train.report({"loss": loss.item()})

# Escale para 8 GPUs
trainer = TorchTrainer(
    train_func,
    scaling_config=ScalingConfig(num_workers=8, use_gpu=True)
)
trainer.fit()
```

**Benefícios**: Mesmo código roda em 1 GPU ou 1000 GPUs

### Fluxo 2: Integração com Transformers HuggingFace

```python
from ray.train.huggingface import TransformersTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments

def train_func(config):
    # Carregue modelo e tokenizer
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")

    # Argumentos de treinamento (API HuggingFace)
    training_args = TrainingArguments(
        output_dir="./output",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        learning_rate=2e-5,
    )

    # Ray gerencia automaticamente o treinamento distribuído
    from transformers import Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
    )

    trainer.train()

# Escale para multi-nó (2 nós × 8 GPUs = 16 workers)
trainer = TransformersTrainer(
    train_func,
    scaling_config=ScalingConfig(
        num_workers=16,
        use_gpu=True,
        resources_per_worker={"GPU": 1}
    )
)

result = trainer.fit()
```

### Fluxo 3: Ajuste de hiperparâmetros com Ray Tune

```python
from ray import tune
from ray.train.torch import TorchTrainer
from ray.tune.schedulers import ASHAScheduler

def train_func(config):
    # Use hiperparâmetros do config
    lr = config["lr"]
    batch_size = config["batch_size"]

    model = MyModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    model = train.torch.prepare_model(model)

    for epoch in range(10):
        # Loop de treinamento
        loss = train_epoch(model, optimizer, batch_size)
        train.report({"loss": loss, "epoch": epoch})

# Defina espaço de busca
param_space = {
    "lr": tune.loguniform(1e-5, 1e-2),
    "batch_size": tune.choice([16, 32, 64, 128])
}

# Execute 20 trials com parada antecipada
tuner = tune.Tuner(
    TorchTrainer(
        train_func,
        scaling_config=ScalingConfig(num_workers=4, use_gpu=True)
    ),
    param_space=param_space,
    tune_config=tune.TuneConfig(
        num_samples=20,
        scheduler=ASHAScheduler(metric="loss", mode="min")
    )
)

results = tuner.fit()
best = results.get_best_result(metric="loss", mode="min")
print(f"Best hyperparameters: {best.config}")
```

**Resultado**: Busca distribuída de hiperparâmetros no cluster

### Fluxo 4: Checkpointing e tolerância a falhas

```python
from ray import train
from ray.train import Checkpoint

def train_func(config):
    model = MyModel()
    optimizer = torch.optim.Adam(model.parameters())

    # Tente retomar de checkpoint
    checkpoint = train.get_checkpoint()
    if checkpoint:
        with checkpoint.as_directory() as checkpoint_dir:
            state = torch.load(f"{checkpoint_dir}/model.pt")
            model.load_state_dict(state["model"])
            optimizer.load_state_dict(state["optimizer"])
            start_epoch = state["epoch"]
    else:
        start_epoch = 0

    model = train.torch.prepare_model(model)

    for epoch in range(start_epoch, 100):
        loss = train_epoch(model, optimizer)

        # Salve checkpoint a cada 10 epochs
        if epoch % 10 == 0:
            checkpoint = Checkpoint.from_directory(
                train.get_context().get_trial_dir()
            )
            torch.save({
                "model": model.state_dict(),
                "optimizer": optimizer.state_dict(),
                "epoch": epoch
            }, checkpoint.path / "model.pt")

            train.report({"loss": loss}, checkpoint=checkpoint)

trainer = TorchTrainer(
    train_func,
    scaling_config=ScalingConfig(num_workers=8, use_gpu=True)
)

# Retoma automaticamente de checkpoint se o treinamento falhar
result = trainer.fit()
```

### Fluxo 5: Treinamento multi-nó

```python
from ray.train import ScalingConfig

# Conecte ao cluster Ray
ray.init(address="auto")  # Or ray.init("ray://head-node:10001")

# Treine em 4 nós × 8 GPUs = 32 workers
trainer = TorchTrainer(
    train_func,
    scaling_config=ScalingConfig(
        num_workers=32,
        use_gpu=True,
        resources_per_worker={"GPU": 1, "CPU": 4},
        placement_strategy="SPREAD"  # Distribua entre nós
    )
)

result = trainer.fit()
```

**Inicie cluster Ray**:
```bash
# No nó head
ray start --head --port=6379

# Nos nós worker
ray start --address=<head-node-ip>:6379
```

## Quando usar vs alternativas

**Use Ray Train quando**:
- Treinar em múltiplas máquinas (multi-nó)
- Precisar de ajuste de hiperparâmetros em escala
- Quiser tolerância a falhas (reinicialização automática de workers)
- Escalabilidade elástica (adicionar/remover nós durante treinamento)
- Framework unificado (mesmo código para PyTorch/TF/HF)

**Principais vantagens**:
- **Orquestração multi-nó**: Configuração multi-nó mais fácil
- **Integração Ray Tune**: Ajuste de hiperparâmetros da melhor categoria
- **Tolerância a falhas**: Recuperação automática de falhas
- **Elástico**: Adicione/remova nós sem reiniciar
- **Agnóstico a framework**: PyTorch, TensorFlow, HuggingFace, XGBoost

**Use alternativas em vez disso**:
- **Accelerate**: Multi-GPU em nó único, mais simples
- **PyTorch Lightning**: Abstrações de alto nível, callbacks
- **DeepSpeed**: Máxima performance, setup complexo
- **DDP bruto**: Máximo controle, overhead mínimo

## Problemas comuns

**Problema: Cluster Ray não conectando**

Verifique status de ray:
```bash
ray status

# Deve mostrar:
# - Nodes: 4
# - GPUs: 32
# - Workers: Ready
```

Se não conectado:
```bash
# Reinicie nó head
ray stop
ray start --head --port=6379 --dashboard-host=0.0.0.0

# Reinicie nós worker
ray stop
ray start --address=<head-ip>:6379
```

**Problema: Memória insuficiente**

Reduza workers ou use gradient accumulation:
```python
scaling_config=ScalingConfig(
    num_workers=4,  # Reduza de 8
    use_gpu=True
)

# Em train_func, acumule gradientes
for i, batch in enumerate(dataloader):
    loss = model(batch) / accumulation_steps
    loss.backward()

    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

**Problema: Treinamento lento**

Verifique se carregamento de dados é gargalo:
```python
import time

def train_func(config):
    for epoch in range(epochs):
        start = time.time()
        for batch in dataloader:
            data_time = time.time() - start
            # Train...
            start = time.time()
            print(f"Data loading: {data_time:.3f}s")
```

Se carregamento de dados é lento, aumente workers:
```python
dataloader = DataLoader(dataset, num_workers=8)
```

## Tópicos avançados

**Setup multi-nó**: Veja [references/multi-node.md](references/multi-node.md) para deployment de cluster Ray em AWS, GCP, Kubernetes e SLURM.

**Ajuste de hiperparâmetros**: Veja [references/hyperparameter-tuning.md](references/hyperparameter-tuning.md) para integração Ray Tune, algoritmos de busca (Optuna, HyperOpt) e population-based training.

**Loops de treinamento customizados**: Veja [references/custom-loops.md](references/custom-loops.md) para uso avançado de Ray Train, backends customizados e integração com outros frameworks.

## Requisitos de hardware

- **Nó único**: 1+ GPUs (ou CPUs)
- **Multi-nó**: 2+ máquinas com conectividade de rede
- **Cloud**: AWS, GCP, Azure (autoscaling de Ray)
- **On-prem**: Kubernetes, clusters SLURM

**Aceleradores suportados**:
- NVIDIA GPUs (CUDA)
- AMD GPUs (ROCm)
- TPUs (Google Cloud)
- CPUs

## Recursos

- Docs: https://docs.ray.io/en/latest/train/train.html
- GitHub: https://github.com/ray-project/ray ⭐ 36,000+
- Versão: 2.40.0+
- Exemplos: https://docs.ray.io/en/latest/train/examples.html
- Slack: https://forms.gle/9TSdDYUgxYs8SA9e8
- Usado por: OpenAI, Uber, Spotify, Shopify, Instacart