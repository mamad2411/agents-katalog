---
name: mlflow
description: Rastreie experimentos de ML, gerencie registro de modelos com versionamento, implante modelos em produção e reproduza experimentos com MLflow - plataforma agnóstica a frameworks para ciclo de vida de ML
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [MLOps, MLflow, Experiment Tracking, Model Registry, ML Lifecycle, Deployment, Model Versioning, PyTorch, TensorFlow, Scikit-Learn, HuggingFace]
dependencies: [mlflow, sqlalchemy, boto3]
---

# MLflow: Plataforma de Gerenciamento do Ciclo de Vida de ML

## Quando Usar Esta Skill

Use MLflow quando precisar:
- **Rastrear experimentos de ML** com parâmetros, métricas e artefatos
- **Gerenciar registro de modelos** com versionamento e transições de estágio
- **Implantar modelos** em várias plataformas (local, nuvem, serving)
- **Reproduzir experimentos** com configurações de projeto
- **Comparar versões de modelos** e métricas de desempenho
- **Colaborar** em projetos de ML com workflows de equipe
- **Integrar** com qualquer framework de ML (agnóstico a frameworks)

**Usuários**: 20.000+ organizações | **GitHub Stars**: 23k+ | **Licença**: Apache 2.0

## Instalação

```bash
# Instalar MLflow
pip install mlflow

# Instalar com extras
pip install mlflow[extras]  # Inclui SQLAlchemy, boto3, etc.

# Iniciar interface MLflow
mlflow ui

# Acessar em http://localhost:5000
```

## Início Rápido

### Rastreamento Básico

```python
import mlflow

# Iniciar um run
with mlflow.start_run():
    # Registrar parâmetros
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("batch_size", 32)

    # Seu código de treinamento
    model = train_model()

    # Registrar métricas
    mlflow.log_metric("train_loss", 0.15)
    mlflow.log_metric("val_accuracy", 0.92)

    # Registrar modelo
    mlflow.sklearn.log_model(model, "model")
```

### Autologging (Rastreamento Automático)

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier

# Ativar autologging
mlflow.autolog()

# Treinar (automaticamente registrado)
model = RandomForestClassifier(n_estimators=100, max_depth=5)
model.fit(X_train, y_train)

# Métricas, parâmetros e modelo registrados automaticamente!
```

## Conceitos Principais

### 1. Experimentos e Runs

**Experiment**: Contêiner lógico para runs relacionados
**Run**: Execução única de código de ML (parâmetros, métricas, artefatos)

```python
import mlflow

# Criar/definir experimento
mlflow.set_experiment("my-experiment")

# Iniciar um run
with mlflow.start_run(run_name="baseline-model"):
    # Registrar params
    mlflow.log_param("model", "ResNet50")
    mlflow.log_param("epochs", 10)

    # Treinar
    model = train()

    # Registrar métricas
    mlflow.log_metric("accuracy", 0.95)

    # Registrar modelo
    mlflow.pytorch.log_model(model, "model")

# O ID do run é gerado automaticamente
print(f"Run ID: {mlflow.active_run().info.run_id}")
```

### 2. Registrando Parâmetros

```python
with mlflow.start_run():
    # Parâmetro único
    mlflow.log_param("learning_rate", 0.001)

    # Múltiplos parâmetros
    mlflow.log_params({
        "batch_size": 32,
        "epochs": 50,
        "optimizer": "Adam",
        "dropout": 0.2
    })

    # Parâmetros aninhados (como dict)
    config = {
        "model": {
            "architecture": "ResNet50",
            "pretrained": True
        },
        "training": {
            "lr": 0.001,
            "weight_decay": 1e-4
        }
    }

    # Registrar como string JSON ou params individuais
    for key, value in config.items():
        mlflow.log_param(key, str(value))
```

### 3. Registrando Métricas

```python
with mlflow.start_run():
    # Loop de treinamento
    for epoch in range(NUM_EPOCHS):
        train_loss = train_epoch()
        val_loss = validate()

        # Registrar métricas a cada passo
        mlflow.log_metric("train_loss", train_loss, step=epoch)
        mlflow.log_metric("val_loss", val_loss, step=epoch)

        # Registrar múltiplas métricas
        mlflow.log_metrics({
            "train_accuracy": train_acc,
            "val_accuracy": val_acc
        }, step=epoch)

    # Registrar métricas finais (sem passo)
    mlflow.log_metric("final_accuracy", final_acc)
```

### 4. Registrando Artefatos

```python
with mlflow.start_run():
    # Registrar arquivo
    model.save('model.pkl')
    mlflow.log_artifact('model.pkl')

    # Registrar diretório
    os.makedirs('plots', exist_ok=True)
    plt.savefig('plots/loss_curve.png')
    mlflow.log_artifacts('plots')

    # Registrar texto
    with open('config.txt', 'w') as f:
        f.write(str(config))
    mlflow.log_artifact('config.txt')

    # Registrar dict como JSON
    mlflow.log_dict({'config': config}, 'config.json')
```

### 5. Registrando Modelos

```python
# PyTorch
import mlflow.pytorch

with mlflow.start_run():
    model = train_pytorch_model()
    mlflow.pytorch.log_model(model, "model")

# Scikit-learn
import mlflow.sklearn

with mlflow.start_run():
    model = train_sklearn_model()
    mlflow.sklearn.log_model(model, "model")

# Keras/TensorFlow
import mlflow.keras

with mlflow.start_run():
    model = train_keras_model()
    mlflow.keras.log_model(model, "model")

# HuggingFace Transformers
import mlflow.transformers

with mlflow.start_run():
    mlflow.transformers.log_model(
        transformers_model={
            "model": model,
            "tokenizer": tokenizer
        },
        artifact_path="model"
    )
```

## Autologging

Registre automaticamente métricas, parâmetros e modelos para frameworks populares.

### Ativar Autologging

```python
import mlflow

# Ativar para todos os frameworks suportados
mlflow.autolog()

# Ou ativar para framework específico
mlflow.sklearn.autolog()
mlflow.pytorch.autolog()
mlflow.keras.autolog()
mlflow.xgboost.autolog()
```

### Autologging com Scikit-learn

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Ativar autologging
mlflow.sklearn.autolog()

# Dividir dados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Treinar (registra automaticamente params, métricas, modelo)
with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    # Métricas como accuracy, f1_score registradas automaticamente
    # Modelo registrado automaticamente
    # Duração do treinamento registrada
```

### Autologging com PyTorch Lightning

```python
import mlflow
import pytorch_lightning as pl

# Ativar autologging
mlflow.pytorch.autolog()

# Treinar
with mlflow.start_run():
    trainer = pl.Trainer(max_epochs=10)
    trainer.fit(model, datamodule=dm)

    # Hiperparâmetros registrados
    # Métricas de treinamento registradas
    # Melhor checkpoint do modelo registrado
```

## Registro de Modelos

Gerencie o ciclo de vida do modelo com versionamento e transições de estágio.

### Registrar Modelo

```python
import mlflow

# Registrar e registrar modelo
with mlflow.start_run():
    model = train_model()

    # Registrar modelo
    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name="my-classifier"  # Registrar imediatamente
    )

# Ou registrar depois
run_id = "abc123"
model_uri = f"runs:/{run_id}/model"
mlflow.register_model(model_uri, "my-classifier")
```

### Estágios de Modelo

Transicionar modelos entre estágios: **None** → **Staging** → **Production** → **Archived**

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Promover para staging
client.transition_model_version_stage(
    name="my-classifier",
    version=3,
    stage="Staging"
)

# Promover para produção
client.transition_model_version_stage(
    name="my-classifier",
    version=3,
    stage="Production",
    archive_existing_versions=True  # Arquivar versões antigas de produção
)

# Arquivar modelo
client.transition_model_version_stage(
    name="my-classifier",
    version=2,
    stage="Archived"
)
```

### Carregar Modelo do Registro

```python
import mlflow.pyfunc

# Carregar modelo de produção mais recente
model = mlflow.pyfunc.load_model("models:/my-classifier/Production")

# Carregar versão específica
model = mlflow.pyfunc.load_model("models:/my-classifier/3")

# Carregar do staging
model = mlflow.pyfunc.load_model("models:/my-classifier/Staging")

# Usar modelo
predictions = model.predict(X_test)
```

### Versionamento de Modelos

```python
client = MlflowClient()

# Listar todas as versões
versions = client.search_model_versions("name='my-classifier'")

for v in versions:
    print(f"Version {v.version}: {v.current_stage}")

# Obter versão mais recente por estágio
latest_prod = client.get_latest_versions("my-classifier", stages=["Production"])
latest_staging = client.get_latest_versions("my-classifier", stages=["Staging"])

# Obter detalhes da versão do modelo
version_info = client.get_model_version(name="my-classifier", version="3")
print(f"Run ID: {version_info.run_id}")
print(f"Stage: {version_info.current_stage}")
print(f"Tags: {version_info.tags}")
```

### Anotações de Modelo

```python
client = MlflowClient()

# Adicionar descrição
client.update_model_version(
    name="my-classifier",
    version="3",
    description="Classificador ResNet50 treinado em 1M de imagens com 95% de acurácia"
)

# Adicionar tags
client.set_model_version_tag(
    name="my-classifier",
    version="3",
    key="validation_status",
    value="approved"
)

client.set_model_version_tag(
    name="my-classifier",
    version="3",
    key="deployed_date",
    value="2025-01-15"
)
```

## Buscando Runs

Encontre runs programaticamente.

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Buscar todos os runs no experimento
experiment_id = client.get_experiment_by_name("my-experiment").experiment_id
runs = client.search_runs(
    experiment_ids=[experiment_id],
    filter_string="metrics.accuracy > 0.9",
    order_by=["metrics.accuracy DESC"],
    max_results=10
)

for run in runs:
    print(f"Run ID: {run.info.run_id}")
    print(f"Accuracy: {run.data.metrics['accuracy']}")
    print(f"Params: {run.data.params}")

# Buscar com filtros complexos
runs = client.search_runs(
    experiment_ids=[experiment_id],
    filter_string="""
        metrics.accuracy > 0.9 AND
        params.model = 'ResNet50' AND
        tags.dataset = 'ImageNet'
    """,
    order_by=["metrics.f1_score DESC"]
)
```

## Exemplos de Integração

### PyTorch

```python
import mlflow
import torch
import torch.nn as nn

# Ativar autologging
mlflow.pytorch.autolog()

with mlflow.start_run():
    # Registrar config
    config = {
        "lr": 0.001,
        "epochs": 10,
        "batch_size": 32
    }
    mlflow.log_params(config)

    # Treinar
    model = create_model()
    optimizer = torch.optim.Adam(model.parameters(), lr=config["lr"])

    for epoch in range(config["epochs"]):
        train_loss = train_epoch(model, optimizer, train_loader)
        val_loss, val_acc = validate(model, val_loader)

        # Registrar métricas
        mlflow.log_metrics({
            "train_loss": train_loss,
            "val_loss": val_loss,
            "val_accuracy": val_acc
        }, step=epoch)

    # Registrar modelo
    mlflow.pytorch.log_model(model, "model")
```

### HuggingFace Transformers

```python
import mlflow
from transformers import Trainer, TrainingArguments

# Ativar autologging
mlflow.transformers.autolog()

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True
)

# Iniciar run MLflow
with mlflow.start_run():
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset
    )

    # Treinar (automaticamente registrado)
    trainer.train()

    # Registrar modelo final no registry
    mlflow.transformers.log_model(
        transformers_model={
            "model": trainer.model,
            "tokenizer": tokenizer
        },
        artifact_path="model",
        registered_model_name="hf-classifier"
    )
```

### XGBoost

```python
import mlflow
import xgboost as xgb

# Ativar autologging
mlflow.xgboost.autolog()

with mlflow.start_run():
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)

    params = {
        'max_depth': 6,
        'learning_rate': 0.1,
        'objective': 'binary:logistic',
        'eval_metric': ['logloss', 'auc']
    }

    # Treinar (automaticamente registrado)
    model = xgb.train(
        params,
        dtrain,
        num_boost_round=100,
        evals=[(dtrain, 'train'), (dval, 'val')],
        early_stopping_rounds=10
    )

    # Modelo e métricas registrados automaticamente
```

## Melhores Práticas

### 1. Organizar com Experimentos

```python
# ✅ Bom: Experimentos separados para diferentes tarefas
mlflow.set_experiment("sentiment-analysis")
mlflow.set_experiment("image-classification")
mlflow.set_experiment("recommendation-system")

# ❌ Ruim: Tudo em um experimento
mlflow.set_experiment("all-models")
```

### 2. Usar Nomes Descritivos para Runs

```python
# ✅ Bom: Nomes descritivos
with mlflow.start_run(run_name="resnet50-imagenet-lr0.001-bs32"):
    train()

# ❌ Ruim: Sem nome (UUID auto-gerado)
with mlflow.start_run():
    train()
```

### 3. Registrar Metadados Abrangentes

```python
with mlflow.start_run():
    # Registrar hiperparâmetros
    mlflow.log_params({
        "learning_rate": 0.001,
        "batch_size": 32,
        "epochs": 50
    })

    # Registrar info do sistema
    mlflow.set_tags({
        "dataset": "ImageNet",
        "framework": "PyTorch 2.0",
        "gpu": "A100",
        "git_commit": get_git_commit()
    })

    # Registrar info dos dados
    mlflow.log_param("train_samples", len(train_dataset))
    mlflow.log_param("val_samples", len(val_dataset))
```

### 4. Rastrear Linhagem de Modelo

```python
# Vincular runs para entender a linhagem
with mlflow.start_run(run_name="preprocessing"):
    data = preprocess()
    mlflow.log_artifact("data.csv")
    preprocessing_run_id = mlflow.active_run().info.run_id

with mlflow.start_run(run_name="training"):
    # Referenciar run pai
    mlflow.set_tag("preprocessing_run_id", preprocessing_run_id)
    model = train(data)
```

### 5. Usar Registro de Modelos para Implantação

```python
# ✅ Bom: Usar registry para produção
model_uri = "models:/my-classifier/Production"
model = mlflow.pyfunc.load_model(model_uri)

# ❌ Ruim: IDs de run hardcoded
model_uri = "runs:/abc123/model"
model = mlflow.pyfunc.load_model(model_uri)
```

## Implantação

### Servir Modelo Localmente

```bash
# Servir modelo registrado
mlflow models serve -m "models:/my-classifier/Production" -p 5001

# Servir de um run
mlflow models serve -m "runs:/<RUN_ID>/model" -p 5001

# Testar endpoint
curl http://127.0.0.1:5001/invocations -H 'Content-Type: application/json' -d '{
  "inputs": [[1.0, 2.0, 3.0, 4.0]]
}'
```

### Implantar em Nuvem

```bash
# Implantar em AWS SageMaker
mlflow sagemaker deploy -m "models:/my-classifier/Production" --region-name us-west-2

# Implantar em Azure ML
mlflow azureml deploy -m "models:/my-classifier/Production"
```

## Configuração

### Servidor de Rastreamento

```bash
# Iniciar servidor de rastreamento com backend store
mlflow server \
  --backend-store-uri postgresql://user:password@localhost/mlflow \
  --default-artifact-root s3://my-bucket/mlflow \
  --host 0.0.0.0 \
  --port 5000
```

### Configuração do Cliente

```python
import mlflow

# Definir URI de rastreamento
mlflow.set_tracking_uri("http://localhost:5000")

# Ou usar variável de ambiente
# export MLFLOW_TRACKING_URI=http://localhost:5000
```

## Recursos

- **Documentação**: https://mlflow.org/docs/latest
- **GitHub**: https://github.com/mlflow/mlflow (23k+ stars)
- **Exemplos**: https://github.com/mlflow/mlflow/tree/master/examples
- **Comunidade**: https://mlflow.org/community

## Veja Também

- `references/tracking.md` - Guia abrangente de rastreamento
- `references/model-registry.md` - Gerenciamento do ciclo de vida do modelo
- `references/deployment.md` - Padrões de implantação em produção