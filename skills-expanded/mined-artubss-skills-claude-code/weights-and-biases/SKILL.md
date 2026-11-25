---
name: weights-and-biases
description: Rastreie experimentos de ML com logging automático, visualize treinamento em tempo real, otimize hiperparâmetros com sweeps e gerencie registro de modelos com W&B - plataforma colaborativa de MLOps
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [MLOps, Weights And Biases, WandB, Experiment Tracking, Hyperparameter Tuning, Model Registry, Collaboration, Real-Time Visualization, PyTorch, TensorFlow, HuggingFace]
dependencies: [wandb]
---

# Weights & Biases: Rastreamento de Experimentos de ML & MLOps

## Quando Usar Esta Skill

Use Weights & Biases (W&B) quando você precisar:
- **Rastrear experimentos de ML** com logging automático de métricas
- **Visualizar treinamento** em dashboards em tempo real
- **Comparar execuções** entre hiperparâmetros e configurações
- **Otimizar hiperparâmetros** com sweeps automatizados
- **Gerenciar registro de modelos** com versionamento e linhagem
- **Colaborar em projetos de ML** com workspaces de equipe
- **Rastrear artefatos** (datasets, modelos, código) com linhagem

**Usuários**: 200.000+ praticantes de ML | **GitHub Stars**: 10.5k+ | **Integrações**: 100+

## Instalação

```bash
# Instalar W&B
pip install wandb

# Fazer login (cria chave de API)
wandb login

# Ou definir chave de API programaticamente
export WANDB_API_KEY=your_api_key_here
```

## Início Rápido

### Rastreamento Básico de Experimentos

```python
import wandb

# Inicializar uma execução
run = wandb.init(
    project="my-project",
    config={
        "learning_rate": 0.001,
        "epochs": 10,
        "batch_size": 32,
        "architecture": "ResNet50"
    }
)

# Loop de treinamento
for epoch in range(run.config.epochs):
    # Seu código de treinamento
    train_loss = train_epoch()
    val_loss = validate()

    # Registrar métricas
    wandb.log({
        "epoch": epoch,
        "train/loss": train_loss,
        "val/loss": val_loss,
        "train/accuracy": train_acc,
        "val/accuracy": val_acc
    })

# Finalizar a execução
wandb.finish()
```

### Com PyTorch

```python
import torch
import wandb

# Inicializar
wandb.init(project="pytorch-demo", config={
    "lr": 0.001,
    "epochs": 10
})

# Acessar config
config = wandb.config

# Loop de treinamento
for epoch in range(config.epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        # Forward pass
        output = model(data)
        loss = criterion(output, target)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Registrar a cada 100 batches
        if batch_idx % 100 == 0:
            wandb.log({
                "loss": loss.item(),
                "epoch": epoch,
                "batch": batch_idx
            })

# Salvar modelo
torch.save(model.state_dict(), "model.pth")
wandb.save("model.pth")  # Upload para W&B

wandb.finish()
```

## Conceitos Principais

### 1. Projetos e Execuções

**Projeto**: Coleção de experimentos relacionados
**Execução**: Execução única do seu script de treinamento

```python
# Criar/usar projeto
run = wandb.init(
    project="image-classification",
    name="resnet50-experiment-1",  # Nome opcional da execução
    tags=["baseline", "resnet"],    # Organizar com tags
    notes="First baseline run"      # Adicionar notas
)

# Cada execução tem ID único
print(f"Run ID: {run.id}")
print(f"Run URL: {run.url}")
```

### 2. Rastreamento de Configuração

Rastreie hiperparâmetros automaticamente:

```python
config = {
    # Arquitetura do modelo
    "model": "ResNet50",
    "pretrained": True,

    # Parâmetros de treinamento
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 50,
    "optimizer": "Adam",

    # Parâmetros de dados
    "dataset": "ImageNet",
    "augmentation": "standard"
}

wandb.init(project="my-project", config=config)

# Acessar config durante treinamento
lr = wandb.config.learning_rate
batch_size = wandb.config.batch_size
```

### 3. Logging de Métricas

```python
# Registrar escalares
wandb.log({"loss": 0.5, "accuracy": 0.92})

# Registrar múltiplas métricas
wandb.log({
    "train/loss": train_loss,
    "train/accuracy": train_acc,
    "val/loss": val_loss,
    "val/accuracy": val_acc,
    "learning_rate": current_lr,
    "epoch": epoch
})

# Registrar com eixo x customizado
wandb.log({"loss": loss}, step=global_step)

# Registrar mídia (imagens, áudio, vídeo)
wandb.log({"examples": [wandb.Image(img) for img in images]})

# Registrar histogramas
wandb.log({"gradients": wandb.Histogram(gradients)})

# Registrar tabelas
table = wandb.Table(columns=["id", "prediction", "ground_truth"])
wandb.log({"predictions": table})
```

### 4. Salvamento de Pontos de Verificação de Modelo

```python
import torch
import wandb

# Salvar checkpoint do modelo
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}

torch.save(checkpoint, 'checkpoint.pth')

# Upload para W&B
wandb.save('checkpoint.pth')

# Ou usar Artifacts (recomendado)
artifact = wandb.Artifact('model', type='model')
artifact.add_file('checkpoint.pth')
wandb.log_artifact(artifact)
```

## Sweeps de Hiperparâmetros

Pesquise automaticamente por hiperparâmetros ideais.

### Definir Configuração de Sweep

```python
sweep_config = {
    'method': 'bayes',  # ou 'grid', 'random'
    'metric': {
        'name': 'val/accuracy',
        'goal': 'maximize'
    },
    'parameters': {
        'learning_rate': {
            'distribution': 'log_uniform',
            'min': 1e-5,
            'max': 1e-1
        },
        'batch_size': {
            'values': [16, 32, 64, 128]
        },
        'optimizer': {
            'values': ['adam', 'sgd', 'rmsprop']
        },
        'dropout': {
            'distribution': 'uniform',
            'min': 0.1,
            'max': 0.5
        }
    }
}

# Inicializar sweep
sweep_id = wandb.sweep(sweep_config, project="my-project")
```

### Definir Função de Treinamento

```python
def train():
    # Inicializar execução
    run = wandb.init()

    # Acessar parâmetros do sweep
    lr = wandb.config.learning_rate
    batch_size = wandb.config.batch_size
    optimizer_name = wandb.config.optimizer

    # Construir modelo com configuração do sweep
    model = build_model(wandb.config)
    optimizer = get_optimizer(optimizer_name, lr)

    # Loop de treinamento
    for epoch in range(NUM_EPOCHS):
        train_loss = train_epoch(model, optimizer, batch_size)
        val_acc = validate(model)

        # Registrar métricas
        wandb.log({
            "train/loss": train_loss,
            "val/accuracy": val_acc
        })

# Executar sweep
wandb.agent(sweep_id, function=train, count=50)  # Executar 50 testes
```

### Estratégias de Sweep

```python
# Busca em grade - exaustiva
sweep_config = {
    'method': 'grid',
    'parameters': {
        'lr': {'values': [0.001, 0.01, 0.1]},
        'batch_size': {'values': [16, 32, 64]}
    }
}

# Busca aleatória
sweep_config = {
    'method': 'random',
    'parameters': {
        'lr': {'distribution': 'uniform', 'min': 0.0001, 'max': 0.1},
        'dropout': {'distribution': 'uniform', 'min': 0.1, 'max': 0.5}
    }
}

# Otimização Bayesiana (recomendado)
sweep_config = {
    'method': 'bayes',
    'metric': {'name': 'val/loss', 'goal': 'minimize'},
    'parameters': {
        'lr': {'distribution': 'log_uniform', 'min': 1e-5, 'max': 1e-1}
    }
}
```

## Artifacts

Rastreie datasets, modelos e outros arquivos com linhagem.

### Registrar Artifacts

```python
# Criar artifact
artifact = wandb.Artifact(
    name='training-dataset',
    type='dataset',
    description='ImageNet training split',
    metadata={'size': '1.2M images', 'split': 'train'}
)

# Adicionar arquivos
artifact.add_file('data/train.csv')
artifact.add_dir('data/images/')

# Registrar artifact
wandb.log_artifact(artifact)
```

### Usar Artifacts

```python
# Baixar e usar artifact
run = wandb.init(project="my-project")

# Baixar artifact
artifact = run.use_artifact('training-dataset:latest')
artifact_dir = artifact.download()

# Usar os dados
data = load_data(f"{artifact_dir}/train.csv")
```

### Registro de Modelos

```python
# Registrar modelo como artifact
model_artifact = wandb.Artifact(
    name='resnet50-model',
    type='model',
    metadata={'architecture': 'ResNet50', 'accuracy': 0.95}
)

model_artifact.add_file('model.pth')
wandb.log_artifact(model_artifact, aliases=['best', 'production'])

# Vincular ao registro de modelos
run.link_artifact(model_artifact, 'model-registry/production-models')
```

## Exemplos de Integração

### HuggingFace Transformers

```python
from transformers import Trainer, TrainingArguments
import wandb

# Inicializar W&B
wandb.init(project="hf-transformers")

# Argumentos de treinamento com W&B
training_args = TrainingArguments(
    output_dir="./results",
    report_to="wandb",  # Ativar logging de W&B
    run_name="bert-finetuning",
    logging_steps=100,
    save_steps=500
)

# Trainer registra automaticamente para W&B
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

trainer.train()
```

### PyTorch Lightning

```python
from pytorch_lightning import Trainer
from pytorch_lightning.loggers import WandbLogger
import wandb

# Criar logger W&B
wandb_logger = WandbLogger(
    project="lightning-demo",
    log_model=True  # Registrar checkpoints de modelo
)

# Usar com Trainer
trainer = Trainer(
    logger=wandb_logger,
    max_epochs=10
)

trainer.fit(model, datamodule=dm)
```

### Keras/TensorFlow

```python
import wandb
from wandb.keras import WandbCallback

# Inicializar
wandb.init(project="keras-demo")

# Adicionar callback
model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),
    epochs=10,
    callbacks=[WandbCallback()]  # Registra métricas automaticamente
)
```

## Visualização & Análise

### Gráficos Customizados

```python
# Registrar visualizações customizadas
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(x, y)
wandb.log({"custom_plot": wandb.Image(fig)})

# Registrar matriz de confusão
wandb.log({"conf_mat": wandb.plot.confusion_matrix(
    probs=None,
    y_true=ground_truth,
    preds=predictions,
    class_names=class_names
)})
```

### Relatórios

Crie relatórios compartilháveis na UI do W&B:
- Combine execuções, gráficos e texto
- Suporte a Markdown
- Visualizações incorporáveis
- Colaboração de equipe

## Melhores Práticas

### 1. Organizar com Tags e Grupos

```python
wandb.init(
    project="my-project",
    tags=["baseline", "resnet50", "imagenet"],
    group="resnet-experiments",  # Agrupar execuções relacionadas
    job_type="train"             # Tipo de job
)
```

### 2. Registrar Tudo Relevante

```python
# Registrar métricas de sistema
wandb.log({
    "gpu/util": gpu_utilization,
    "gpu/memory": gpu_memory_used,
    "cpu/util": cpu_utilization
})

# Registrar versão de código
wandb.log({"git_commit": git_commit_hash})

# Registrar divisões de dados
wandb.log({
    "data/train_size": len(train_dataset),
    "data/val_size": len(val_dataset)
})
```

### 3. Usar Nomes Descritivos

```python
# ✅ Bom: Nomes descritivos de execução
wandb.init(
    project="nlp-classification",
    name="bert-base-lr0.001-bs32-epoch10"
)

# ❌ Ruim: Nomes genéricos
wandb.init(project="nlp", name="run1")
```

### 4. Salvar Artifacts Importantes

```python
# Salvar modelo final
artifact = wandb.Artifact('final-model', type='model')
artifact.add_file('model.pth')
wandb.log_artifact(artifact)

# Salvar previsões para análise
predictions_table = wandb.Table(
    columns=["id", "input", "prediction", "ground_truth"],
    data=predictions_data
)
wandb.log({"predictions": predictions_table})
```

### 5. Usar Modo Offline para Conexões Instáveis

```python
import os

# Ativar modo offline
os.environ["WANDB_MODE"] = "offline"

wandb.init(project="my-project")
# ... seu código ...

# Sincronizar depois
# wandb sync <run_directory>
```

## Colaboração de Equipe

### Compartilhar Execuções

```python
# Execuções são automaticamente compartilháveis via URL
run = wandb.init(project="team-project")
print(f"Compartilhe esta URL: {run.url}")
```

### Projetos de Equipe

- Criar conta de equipe em wandb.ai
- Adicionar membros da equipe
- Definir visibilidade do projeto (privado/público)
- Usar artifacts e registro de modelos em nível de equipe

## Preços

- **Gratuito**: Projetos públicos ilimitados, 100GB armazenamento
- **Acadêmico**: Gratuito para estudantes/pesquisadores
- **Equipes**: R$ 250/assento/mês, projetos privados, armazenamento ilimitado
- **Enterprise**: Preço customizado, opções on-prem

## Recursos

- **Documentação**: https://docs.wandb.ai
- **GitHub**: https://github.com/wandb/wandb (10.5k+ stars)
- **Exemplos**: https://github.com/wandb/examples
- **Comunidade**: https://wandb.ai/community
- **Discord**: https://wandb.me/discord

## Veja Também

- `references/sweeps.md` - Guia abrangente de otimização de hiperparâmetros
- `references/artifacts.md` - Padrões de versionamento de dados e modelos
- `references/integrations.md` - Exemplos específicos de framework