---
name: pytorch-lightning
description: "Framework de deep learning (PyTorch Lightning). Organize código PyTorch em LightningModules, configure Trainers para multi-GPU/TPU, implemente data pipelines, callbacks, logging (W&B, TensorBoard), distributed training (DDP, FSDP, DeepSpeed), para treinamento escalável de redes neurais."
---

# PyTorch Lightning

## Visão Geral

PyTorch Lightning é um framework de deep learning que organiza código PyTorch para eliminar boilerplate mantendo total flexibilidade. Automatize workflows de treinamento, orquestração multi-device e implemente boas práticas para treinamento e scaling de redes neurais em múltiplas GPUs/TPUs.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Construir, treinar ou fazer deploy de redes neurais usando PyTorch Lightning
- Organizar código PyTorch em LightningModules
- Configurar Trainers para treinamento multi-GPU/TPU
- Implementar data pipelines com LightningDataModules
- Trabalhar com callbacks, logging e estratégias de distributed training (DDP, FSDP, DeepSpeed)
- Estruturar projetos de deep learning profissionalmente

## Capacidades Principais

### 1. LightningModule - Definição de Modelo

Organize modelos PyTorch em seis seções lógicas:

1. **Inicialização** - `__init__()` e `setup()`
2. **Training Loop** - `training_step(batch, batch_idx)`
3. **Validation Loop** - `validation_step(batch, batch_idx)`
4. **Test Loop** - `test_step(batch, batch_idx)`
5. **Prediction** - `predict_step(batch, batch_idx)`
6. **Optimizer Configuration** - `configure_optimizers()`

**Referência de template rápido:** Veja `scripts/template_lightning_module.py` para boilerplate completo.

**Documentação detalhada:** Leia `references/lightning_module.md` para documentação abrangente de métodos, hooks, propriedades e boas práticas.

### 2. Trainer - Automação de Treinamento

O Trainer automatiza o loop de treinamento, gerenciamento de devices, operações de gradiente e callbacks. Recursos principais:

- Suporte multi-GPU/TPU com seleção de strategy (DDP, FSDP, DeepSpeed)
- Treinamento com precisão mista automática
- Gradient accumulation e clipping
- Checkpointing e early stopping
- Barras de progresso e logging

**Referência de setup rápido:** Veja `scripts/quick_trainer_setup.py` para configurações comuns de Trainer.

**Documentação detalhada:** Leia `references/trainer.md` para todos os parâmetros, métodos e opções de configuração.

### 3. LightningDataModule - Organização de Data Pipeline

Encapsule todos os passos de processamento de dados em uma classe reutilizável:

1. `prepare_data()` - Download e processe dados (single-process)
2. `setup()` - Crie datasets e aplique transforms (per-GPU)
3. `train_dataloader()` - Retorne training DataLoader
4. `val_dataloader()` - Retorne validation DataLoader
5. `test_dataloader()` - Retorne test DataLoader

**Referência de template rápido:** Veja `scripts/template_datamodule.py` para boilerplate completo.

**Documentação detalhada:** Leia `references/data_module.md` para detalhes de métodos e padrões de uso.

### 4. Callbacks - Lógica de Treinamento Extensível

Adicione funcionalidade customizada em hooks específicos de treinamento sem modificar seu LightningModule. Callbacks built-in incluem:

- **ModelCheckpoint** - Salve modelos melhores/mais recentes
- **EarlyStopping** - Pare quando métricas platô
- **LearningRateMonitor** - Rastreie mudanças do LR scheduler
- **BatchSizeFinder** - Determine automaticamente batch size ótimo

**Documentação detalhada:** Leia `references/callbacks.md` para callbacks built-in e criação de callbacks customizados.

### 5. Logging - Rastreamento de Experimentos

Integre com múltiplas plataformas de logging:

- TensorBoard (padrão)
- Weights & Biases (WandbLogger)
- MLflow (MLFlowLogger)
- Neptune (NeptuneLogger)
- Comet (CometLogger)
- CSV (CSVLogger)

Log de métricas usando `self.log("metric_name", value)` em qualquer método de LightningModule.

**Documentação detalhada:** Leia `references/logging.md` para setup de loggers e configuração.

### 6. Distributed Training - Escale para Múltiplos Devices

Escolha a strategy correta baseada no tamanho do modelo:

- **DDP** - Para modelos <500M parâmetros (ResNet, transformers menores)
- **FSDP** - Para modelos 500M+ parâmetros (transformers grandes, recomendado para usuários Lightning)
- **DeepSpeed** - Para recursos de ponta e controle fine-grained

Configure com: `Trainer(strategy="ddp", accelerator="gpu", devices=4)`

**Documentação detalhada:** Leia `references/distributed_training.md` para comparação de strategies e configuração.

### 7. Boas Práticas

- Código device agnostic - Use `self.device` ao invés de `.cuda()`
- Salvamento de hiperparâmetros - Use `self.save_hyperparameters()` em `__init__()`
- Logging de métricas - Use `self.log()` para agregação automática entre devices
- Reproducibilidade - Use `seed_everything()` e `Trainer(deterministic=True)`
- Debugging - Use `Trainer(fast_dev_run=True)` para testar com 1 batch

**Documentação detalhada:** Leia `references/best_practices.md` para padrões comuns e armadilhas.

## Workflow Rápido

1. **Defina o modelo:**
   ```python
   class MyModel(L.LightningModule):
       def __init__(self):
           super().__init__()
           self.save_hyperparameters()
           self.model = YourNetwork()

       def training_step(self, batch, batch_idx):
           x, y = batch
           loss = F.cross_entropy(self.model(x), y)
           self.log("train_loss", loss)
           return loss

       def configure_optimizers(self):
           return torch.optim.Adam(self.parameters())
   ```

2. **Prepare dados:**
   ```python
   # Option 1: DataLoaders diretos
   train_loader = DataLoader(train_dataset, batch_size=32)

   # Option 2: LightningDataModule (recomendado para reusabilidade)
   dm = MyDataModule(batch_size=32)
   ```

3. **Treine:**
   ```python
   trainer = L.Trainer(max_epochs=10, accelerator="gpu", devices=2)
   trainer.fit(model, train_loader)  # ou trainer.fit(model, datamodule=dm)
   ```

## Recursos

### scripts/
Templates Python executáveis para padrões comuns de PyTorch Lightning:

- `template_lightning_module.py` - Boilerplate completo de LightningModule
- `template_datamodule.py` - Boilerplate completo de LightningDataModule
- `quick_trainer_setup.py` - Exemplos de configuração comum de Trainer

### references/
Documentação detalhada para cada componente de PyTorch Lightning:

- `lightning_module.md` - Guia abrangente de LightningModule (métodos, hooks, propriedades)
- `trainer.md` - Configuração de Trainer e parâmetros
- `data_module.md` - Padrões e métodos de LightningDataModule
- `callbacks.md` - Callbacks built-in e customizados
- `logging.md` - Integrações de loggers e uso
- `distributed_training.md` - Comparação de DDP, FSDP, DeepSpeed e setup
- `best_practices.md` - Padrões comuns, dicas e armadilhas