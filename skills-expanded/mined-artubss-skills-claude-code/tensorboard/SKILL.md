---
name: tensorboard
description: Visualize métricas de treinamento, depure modelos com histogramas, compare experimentos, visualize grafos de modelos e perfil de desempenho com TensorBoard - kit de visualização de ML do Google
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [MLOps, TensorBoard, Visualization, Training Metrics, Model Debugging, PyTorch, TensorFlow, Experiment Tracking, Performance Profiling]
dependencies: [tensorboard, torch, tensorflow]
---

# TensorBoard: Kit de Visualização para ML

## Quando Usar Esta Skill

Use TensorBoard quando você precisa:
- **Visualizar métricas de treinamento** como perda e acurácia ao longo do tempo
- **Depurar modelos** com histogramas e distribuições
- **Comparar experimentos** em múltiplas execuções
- **Visualizar grafos e arquitetura de modelos**
- **Projetar embeddings** em dimensões inferiores (t-SNE, PCA)
- **Rastrear experimentos de hiperparâmetros**
- **Fazer perfil de desempenho** e identificar gargalos
- **Visualizar imagens e texto** durante o treinamento

**Usuários**: 20M+ downloads/ano | **GitHub Stars**: 27k+ | **Licença**: Apache 2.0

## Instalação

```bash
# Instalar TensorBoard
pip install tensorboard

# Integração PyTorch
pip install torch torchvision tensorboard

# Integração TensorFlow (TensorBoard incluído)
pip install tensorflow

# Iniciar TensorBoard
tensorboard --logdir=runs
# Acesse em http://localhost:6006
```

## Quick Start

### PyTorch

```python
from torch.utils.tensorboard import SummaryWriter

# Criar writer
writer = SummaryWriter('runs/experiment_1')

# Loop de treinamento
for epoch in range(10):
    train_loss = train_epoch()
    val_acc = validate()

    # Registrar métricas
    writer.add_scalar('Loss/train', train_loss, epoch)
    writer.add_scalar('Accuracy/val', val_acc, epoch)

# Fechar writer
writer.close()

# Iniciar: tensorboard --logdir=runs
```

### TensorFlow/Keras

```python
import tensorflow as tf

# Criar callback
tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir='logs/fit',
    histogram_freq=1
)

# Treinar modelo
model.fit(
    x_train, y_train,
    epochs=10,
    validation_data=(x_val, y_val),
    callbacks=[tensorboard_callback]
)

# Iniciar: tensorboard --logdir=logs
```

## Conceitos Principais

### 1. SummaryWriter (PyTorch)

```python
from torch.utils.tensorboard import SummaryWriter

# Diretório padrão: runs/CURRENT_DATETIME
writer = SummaryWriter()

# Diretório personalizado
writer = SummaryWriter('runs/experiment_1')

# Comentário personalizado (anexado ao diretório padrão)
writer = SummaryWriter(comment='baseline')

# Registrar dados
writer.add_scalar('Loss/train', 0.5, step=0)
writer.add_scalar('Loss/train', 0.3, step=1)

# Descarregar e fechar
writer.flush()
writer.close()
```

### 2. Logging de Escalares

```python
# PyTorch
from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter()

for epoch in range(100):
    train_loss = train()
    val_loss = validate()

    # Registrar métricas individuais
    writer.add_scalar('Loss/train', train_loss, epoch)
    writer.add_scalar('Loss/val', val_loss, epoch)
    writer.add_scalar('Accuracy/train', train_acc, epoch)
    writer.add_scalar('Accuracy/val', val_acc, epoch)

    # Taxa de aprendizado
    lr = optimizer.param_groups[0]['lr']
    writer.add_scalar('Learning_rate', lr, epoch)

writer.close()
```

```python
# TensorFlow
import tensorflow as tf

train_summary_writer = tf.summary.create_file_writer('logs/train')
val_summary_writer = tf.summary.create_file_writer('logs/val')

for epoch in range(100):
    with train_summary_writer.as_default():
        tf.summary.scalar('loss', train_loss, step=epoch)
        tf.summary.scalar('accuracy', train_acc, step=epoch)

    with val_summary_writer.as_default():
        tf.summary.scalar('loss', val_loss, step=epoch)
        tf.summary.scalar('accuracy', val_acc, step=epoch)
```

### 3. Logging de Múltiplos Escalares

```python
# PyTorch: Agrupar métricas relacionadas
writer.add_scalars('Loss', {
    'train': train_loss,
    'validation': val_loss,
    'test': test_loss
}, epoch)

writer.add_scalars('Metrics', {
    'accuracy': accuracy,
    'precision': precision,
    'recall': recall,
    'f1': f1_score
}, epoch)
```

### 4. Logging de Imagens

```python
# PyTorch
import torch
from torchvision.utils import make_grid

# Imagem única
writer.add_image('Input/sample', img_tensor, epoch)

# Múltiplas imagens em grade
img_grid = make_grid(images[:64], nrow=8)
writer.add_image('Batch/inputs', img_grid, epoch)

# Visualização de predições
pred_grid = make_grid(predictions[:16], nrow=4)
writer.add_image('Predictions', pred_grid, epoch)
```

```python
# TensorFlow
import tensorflow as tf

with file_writer.as_default():
    # Codificar imagens como PNG
    tf.summary.image('Training samples', images, step=epoch, max_outputs=25)
```

### 5. Logging de Histogramas

```python
# PyTorch: Rastrear distribuições de pesos
for name, param in model.named_parameters():
    writer.add_histogram(name, param, epoch)

    # Rastrear gradientes
    if param.grad is not None:
        writer.add_histogram(f'{name}.grad', param.grad, epoch)

# Rastrear ativações
writer.add_histogram('Activations/relu1', activations, epoch)
```

```python
# TensorFlow
with file_writer.as_default():
    tf.summary.histogram('weights/layer1', layer1.kernel, step=epoch)
    tf.summary.histogram('activations/relu1', activations, step=epoch)
```

### 6. Logging de Grafo de Modelo

```python
# PyTorch
import torch

model = MyModel()
dummy_input = torch.randn(1, 3, 224, 224)

writer.add_graph(model, dummy_input)
writer.close()
```

```python
# TensorFlow (automático com Keras)
tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir='logs',
    write_graph=True
)

model.fit(x, y, callbacks=[tensorboard_callback])
```

## Recursos Avançados

### Embedding Projector

Visualize dados de alta dimensionalidade (embeddings, features) em 2D/3D.

```python
import torch
from torch.utils.tensorboard import SummaryWriter

# Obter embeddings (ex: embeddings de palavras, features de imagem)
embeddings = model.get_embeddings(data)  # Shape: (N, embedding_dim)

# Metadados (rótulos para cada ponto)
metadata = ['class_1', 'class_2', 'class_1', ...]

# Imagens (opcional, para embeddings de imagem)
label_images = torch.stack([img1, img2, img3, ...])

# Registrar em TensorBoard
writer.add_embedding(
    embeddings,
    metadata=metadata,
    label_img=label_images,
    global_step=epoch
)
```

**Em TensorBoard:**
- Navegue até a aba "Projector"
- Escolha visualização PCA, t-SNE ou UMAP
- Pesquise, filtre e explore clusters

### Ajuste de Hiperparâmetros

```python
from torch.utils.tensorboard import SummaryWriter

# Experimentar diferentes hiperparâmetros
for lr in [0.001, 0.01, 0.1]:
    for batch_size in [16, 32, 64]:
        # Criar diretório de execução único
        writer = SummaryWriter(f'runs/lr{lr}_bs{batch_size}')

        # Registrar hiperparâmetros
        writer.add_hparams(
            {'lr': lr, 'batch_size': batch_size},
            {'hparam/accuracy': final_acc, 'hparam/loss': final_loss}
        )

        # Treinar e registrar
        for epoch in range(10):
            loss = train(lr, batch_size)
            writer.add_scalar('Loss/train', loss, epoch)

        writer.close()

# Comparar na aba "HParams" do TensorBoard
```

### Logging de Texto

```python
# PyTorch: Registrar texto (ex: predições de modelo, resumos)
writer.add_text('Predictions', f'Epoch {epoch}: {predictions}', epoch)
writer.add_text('Config', str(config), 0)

# Registrar tabelas markdown
markdown_table = """
| Metric | Value |
|--------|-------|
| Accuracy | 0.95 |
| F1 Score | 0.93 |
"""
writer.add_text('Results', markdown_table, epoch)
```

### Curvas PR

Curvas de Precisão-Recall para classificação.

```python
from torch.utils.tensorboard import SummaryWriter

# Obter predições e rótulos
predictions = model(test_data)  # Shape: (N, num_classes)
labels = test_labels  # Shape: (N,)

# Registrar curva PR para cada classe
for i in range(num_classes):
    writer.add_pr_curve(
        f'PR_curve/class_{i}',
        labels == i,
        predictions[:, i],
        global_step=epoch
    )
```

## Exemplos de Integração

### Loop de Treinamento PyTorch

```python
import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter

# Setup
writer = SummaryWriter('runs/resnet_experiment')
model = ResNet50()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Registrar grafo do modelo
dummy_input = torch.randn(1, 3, 224, 224)
writer.add_graph(model, dummy_input)

# Loop de treinamento
for epoch in range(50):
    model.train()
    train_loss = 0.0
    train_correct = 0

    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        pred = output.argmax(dim=1)
        train_correct += pred.eq(target).sum().item()

        # Registrar métricas de batch (a cada 100 batches)
        if batch_idx % 100 == 0:
            global_step = epoch * len(train_loader) + batch_idx
            writer.add_scalar('Loss/train_batch', loss.item(), global_step)

    # Métricas de epoch
    train_loss /= len(train_loader)
    train_acc = train_correct / len(train_loader.dataset)

    # Validação
    model.eval()
    val_loss = 0.0
    val_correct = 0

    with torch.no_grad():
        for data, target in val_loader:
            output = model(data)
            val_loss += criterion(output, target).item()
            pred = output.argmax(dim=1)
            val_correct += pred.eq(target).sum().item()

    val_loss /= len(val_loader)
    val_acc = val_correct / len(val_loader.dataset)

    # Registrar métricas de epoch
    writer.add_scalars('Loss', {'train': train_loss, 'val': val_loss}, epoch)
    writer.add_scalars('Accuracy', {'train': train_acc, 'val': val_acc}, epoch)

    # Registrar taxa de aprendizado
    writer.add_scalar('Learning_rate', optimizer.param_groups[0]['lr'], epoch)

    # Registrar histogramas (a cada 5 epochs)
    if epoch % 5 == 0:
        for name, param in model.named_parameters():
            writer.add_histogram(name, param, epoch)

    # Registrar predições de amostra
    if epoch % 10 == 0:
        sample_images = data[:8]
        writer.add_image('Sample_inputs', make_grid(sample_images), epoch)

writer.close()
```

### Treinamento TensorFlow/Keras

```python
import tensorflow as tf

# Definir modelo
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Callback do TensorBoard
tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir='logs/fit',
    histogram_freq=1,          # Registrar histogramas a cada epoch
    write_graph=True,          # Visualizar grafo do modelo
    write_images=True,         # Visualizar pesos como imagens
    update_freq='epoch',       # Registrar métricas a cada epoch
    profile_batch='500,520',   # Fazer perfil dos batches 500-520
    embeddings_freq=1          # Registrar embeddings a cada epoch
)

# Treinar
model.fit(
    x_train, y_train,
    epochs=10,
    validation_data=(x_val, y_val),
    callbacks=[tensorboard_callback]
)
```

## Comparando Experimentos

### Múltiplas Execuções

```bash
# Executar experimentos com diferentes configs
python train.py --lr 0.001 --logdir runs/exp1
python train.py --lr 0.01 --logdir runs/exp2
python train.py --lr 0.1 --logdir runs/exp3

# Visualizar todas as execuções junto
tensorboard --logdir=runs
```

**Em TensorBoard:**
- Todas as execuções aparecem no mesmo dashboard
- Ativar/desativar execuções para comparação
- Usar regex para filtrar nomes de execução
- Sobrepor gráficos para comparar métricas

### Organizando Experimentos

```python
# Organização hierárquica
runs/
├── baseline/
│   ├── run_1/
│   └── run_2/
├── improved/
│   ├── run_1/
│   └── run_2/
└── final/
    └── run_1/

# Registrar com hierarquia
writer = SummaryWriter('runs/baseline/run_1')
```

## Melhores Práticas

### 1. Use Nomes Descritivos para Execuções

```python
# ✅ Bom: Nomes descritivos
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
writer = SummaryWriter(f'runs/resnet50_lr0.001_bs32_{timestamp}')

# ❌ Ruim: Nomes auto-gerados
writer = SummaryWriter()  # Cria runs/Jan01_12-34-56_hostname
```

### 2. Agrupar Métricas Relacionadas

```python
# ✅ Bom: Métricas agrupadas
writer.add_scalar('Loss/train', train_loss, step)
writer.add_scalar('Loss/val', val_loss, step)
writer.add_scalar('Accuracy/train', train_acc, step)
writer.add_scalar('Accuracy/val', val_acc, step)

# ❌ Ruim: Namespace plano
writer.add_scalar('train_loss', train_loss, step)
writer.add_scalar('val_loss', val_loss, step)
```

### 3. Registre Regularmente Mas Não Muito Frequentemente

```python
# ✅ Bom: Sempre registrar métricas de epoch, ocasionalmente de batch
for epoch in range(100):
    for batch_idx, (data, target) in enumerate(train_loader):
        loss = train_step(data, target)

        # Registrar a cada 100 batches
        if batch_idx % 100 == 0:
            writer.add_scalar('Loss/batch', loss, global_step)

    # Sempre registrar métricas de epoch
    writer.add_scalar('Loss/epoch', epoch_loss, epoch)

# ❌ Ruim: Registrar cada batch (cria arquivos de log enormes)
for batch in train_loader:
    writer.add_scalar('Loss', loss, step)  # Muito frequente
```

### 4. Feche o Writer Quando Terminar

```python
# ✅ Bom: Usar gerenciador de contexto
with SummaryWriter('runs/exp1') as writer:
    for epoch in range(10):
        writer.add_scalar('Loss', loss, epoch)
# Fecha automaticamente

# Ou manualmente
writer = SummaryWriter('runs/exp1')
# ... registrar ...
writer.close()
```

### 5. Use Writers Separados para Treinamento/Validação

```python
# ✅ Bom: Diretórios de log separados
train_writer = SummaryWriter('runs/exp1/train')
val_writer = SummaryWriter('runs/exp1/val')

train_writer.add_scalar('loss', train_loss, epoch)
val_writer.add_scalar('loss', val_loss, epoch)
```

## Perfil de Desempenho

### TensorFlow Profiler

```python
# Ativar profiling
tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir='logs',
    profile_batch='10,20'  # Fazer perfil dos batches 10-20
)

model.fit(x, y, callbacks=[tensorboard_callback])

# Visualizar na aba Profile do TensorBoard
# Mostra: utilização de GPU, estatísticas de kernel, uso de memória, gargalos
```

### PyTorch Profiler

```python
import torch.profiler as profiler

with profiler.profile(
    activities=[
        profiler.ProfilerActivity.CPU,
        profiler.ProfilerActivity.CUDA
    ],
    on_trace_ready=torch.profiler.tensorboard_trace_handler('./runs/profiler'),
    record_shapes=True,
    with_stack=True
) as prof:
    for batch in train_loader:
        loss = train_step(batch)
        prof.step()

# Visualizar na aba Profile do TensorBoard
```

## Recursos

- **Documentação**: https://www.tensorflow.org/tensorboard
- **Integração PyTorch**: https://pytorch.org/docs/stable/tensorboard.html
- **GitHub**: https://github.com/tensorflow/tensorboard (27k+ stars)
- **TensorBoard.dev**: https://tensorboard.dev (compartilhar experimentos publicamente)

## Veja Também

- `references/visualization.md` - Guia abrangente de visualização
- `references/profiling.md` - Padrões de perfil de desempenho
- `references/integrations.md` - Exemplos de integração específicos da framework