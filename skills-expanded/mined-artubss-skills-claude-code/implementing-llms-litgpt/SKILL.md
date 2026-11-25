---
name: implementing-llms-litgpt
description: Implementa e treina LLMs usando LitGPT da Lightning AI com 20+ arquiteturas pré-treinadas (Llama, Gemma, Phi, Qwen, Mistral). Use quando precisar de implementações limpas de modelos, entendimento educacional de arquiteturas ou fine-tuning de produção com LoRA/QLoRA. Implementações em arquivo único, sem camadas de abstração.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Model Architecture, LitGPT, Lightning AI, LLM Implementation, LoRA, QLoRA, Fine-Tuning, Llama, Gemma, Phi, Mistral, Educational]
dependencies: [litgpt, torch, transformers]
---

# LitGPT - Implementações Limpas de LLM

## Início rápido

LitGPT fornece 20+ implementações de LLM pré-treinados com código limpo, legível e workflows de treinamento prontos para produção.

**Instalação**:
```bash
pip install 'litgpt[extra]'
```

**Carregue e use qualquer modelo**:
```python
from litgpt import LLM

# Carregue modelo pré-treinado
llm = LLM.load("microsoft/phi-2")

# Gere texto
result = llm.generate(
    "What is the capital of France?",
    max_new_tokens=50,
    temperature=0.7
)
print(result)
```

**Liste modelos disponíveis**:
```bash
litgpt download list
```

## Workflows comuns

### Workflow 1: Fine-tune em dataset customizado

Copie este checklist:

```
Fine-Tuning Setup:
- [ ] Step 1: Download pretrained model
- [ ] Step 2: Prepare dataset
- [ ] Step 3: Configure training
- [ ] Step 4: Run fine-tuning
```

**Passo 1: Faça download do modelo pré-treinado**

```bash
# Baixe Llama 3 8B
litgpt download meta-llama/Meta-Llama-3-8B

# Baixe Phi-2 (menor, mais rápido)
litgpt download microsoft/phi-2

# Baixe Gemma 2B
litgpt download google/gemma-2b
```

Os modelos são salvos no diretório `checkpoints/`.

**Passo 2: Prepare o dataset**

LitGPT suporta múltiplos formatos:

**Formato Alpaca** (instruction-response):
```json
[
  {
    "instruction": "What is the capital of France?",
    "input": "",
    "output": "The capital of France is Paris."
  },
  {
    "instruction": "Translate to Spanish: Hello, how are you?",
    "input": "",
    "output": "Hola, ¿cómo estás?"
  }
]
```

Salve como `data/my_dataset.json`.

**Passo 3: Configure o treinamento**

```bash
# Fine-tuning completo (requer GPU 40GB+ para modelos 7B)
litgpt finetune \
  meta-llama/Meta-Llama-3-8B \
  --data JSON \
  --data.json_path data/my_dataset.json \
  --train.max_steps 1000 \
  --train.learning_rate 2e-5 \
  --train.micro_batch_size 1 \
  --train.global_batch_size 16

# Fine-tuning LoRA (eficiente, GPU 16GB)
litgpt finetune_lora \
  microsoft/phi-2 \
  --data JSON \
  --data.json_path data/my_dataset.json \
  --lora_r 16 \
  --lora_alpha 32 \
  --lora_dropout 0.05 \
  --train.max_steps 1000 \
  --train.learning_rate 1e-4
```

**Passo 4: Execute o fine-tuning**

O treinamento salva checkpoints em `out/finetune/` automaticamente.

Monitore o treinamento:
```bash
# Visualize logs
tail -f out/finetune/logs.txt

# TensorBoard (se usar --train.logger_name tensorboard)
tensorboard --logdir out/finetune/lightning_logs
```

### Workflow 2: Fine-tuning LoRA em GPU única

Opção mais eficiente em memória.

```
LoRA Training:
- [ ] Step 1: Choose base model
- [ ] Step 2: Configure LoRA parameters
- [ ] Step 3: Train with LoRA
- [ ] Step 4: Merge LoRA weights (optional)
```

**Passo 1: Escolha o modelo base**

Para GPU com memória limitada (12-16GB):
- **Phi-2** (2.7B) - Melhor relação qualidade/tamanho
- **Llama 3 1B** - Menor, mais rápido
- **Gemma 2B** - Bom raciocínio

**Passo 2: Configure os parâmetros LoRA**

```bash
litgpt finetune_lora \
  microsoft/phi-2 \
  --data JSON \
  --data.json_path data/my_dataset.json \
  --lora_r 16 \          # LoRA rank (8-64, maior=mais capacidade)
  --lora_alpha 32 \      # LoRA scaling (tipicamente 2×r)
  --lora_dropout 0.05 \  # Prevenir overfitting
  --lora_query true \    # Aplique LoRA à projeção de query
  --lora_key false \     # Geralmente não necessário
  --lora_value true \    # Aplique LoRA à projeção de value
  --lora_projection true \  # Aplique LoRA à projeção de saída
  --lora_mlp false \     # Geralmente não necessário
  --lora_head false      # Geralmente não necessário
```

Guia de rank LoRA:
- `r=8`: Leve, adapters de 2-4MB
- `r=16`: Padrão, boa qualidade
- `r=32`: Capacidade alta, use para tarefas complexas
- `r=64`: Qualidade máxima, adapters 4× maiores

**Passo 3: Treine com LoRA**

```bash
litgpt finetune_lora \
  microsoft/phi-2 \
  --data JSON \
  --data.json_path data/my_dataset.json \
  --lora_r 16 \
  --train.epochs 3 \
  --train.learning_rate 1e-4 \
  --train.micro_batch_size 4 \
  --train.global_batch_size 32 \
  --out_dir out/phi2-lora

# Uso de memória: ~8-12GB para Phi-2 com LoRA
```

**Passo 4: Mescle os pesos LoRA** (opcional)

Mescle adapters LoRA no modelo base para deployment:

```bash
litgpt merge_lora \
  out/phi2-lora/final \
  --out_dir out/phi2-merged
```

Agora use o modelo mesclado:
```python
from litgpt import LLM
llm = LLM.load("out/phi2-merged")
```

### Workflow 3: Pré-treinar do zero

Treine um novo modelo em seus dados de domínio.

```
Pretraining:
- [ ] Step 1: Prepare pretraining dataset
- [ ] Step 2: Configure model architecture
- [ ] Step 3: Set up multi-GPU training
- [ ] Step 4: Launch pretraining
```

**Passo 1: Prepare o dataset de pré-treinamento**

LitGPT espera dados tokenizados. Use `prepare_dataset.py`:

```bash
python scripts/prepare_dataset.py \
  --source_path data/my_corpus.txt \
  --checkpoint_dir checkpoints/tokenizer \
  --destination_path data/pretrain \
  --split train,val
```

**Passo 2: Configure a arquitetura do modelo**

Edite o arquivo de config ou use um existente:

```python
# config/pythia-160m.yaml
model_name: pythia-160m
block_size: 2048
vocab_size: 50304
n_layer: 12
n_head: 12
n_embd: 768
rotary_percentage: 0.25
parallel_residual: true
bias: true
```

**Passo 3: Configure o treinamento multi-GPU**

```bash
# GPU única
litgpt pretrain \
  --config config/pythia-160m.yaml \
  --data.data_dir data/pretrain \
  --train.max_tokens 10_000_000_000

# Multi-GPU com FSDP
litgpt pretrain \
  --config config/pythia-1b.yaml \
  --data.data_dir data/pretrain \
  --devices 8 \
  --train.max_tokens 100_000_000_000
```

**Passo 4: Lance o pré-treinamento**

Para pré-treinamento em larga escala em cluster:

```bash
# Usando SLURM
sbatch --nodes=8 --gpus-per-node=8 \
  pretrain_script.sh

# pretrain_script.sh content:
litgpt pretrain \
  --config config/pythia-1b.yaml \
  --data.data_dir /shared/data/pretrain \
  --devices 8 \
  --num_nodes 8 \
  --train.global_batch_size 512 \
  --train.max_tokens 300_000_000_000
```

### Workflow 4: Converta e faça deploy do modelo

Exporte modelos LitGPT para produção.

```
Model Deployment:
- [ ] Step 1: Test inference locally
- [ ] Step 2: Quantize model (optional)
- [ ] Step 3: Convert to GGUF (for llama.cpp)
- [ ] Step 4: Deploy with API
```

**Passo 1: Teste a inferência localmente**

```python
from litgpt import LLM

llm = LLM.load("out/phi2-lora/final")

# Geração única
print(llm.generate("What is machine learning?"))

# Streaming
for token in llm.generate("Explain quantum computing", stream=True):
    print(token, end="", flush=True)

# Inferência em batch
prompts = ["Hello", "Goodbye", "Thank you"]
results = [llm.generate(p) for p in prompts]
```

**Passo 2: Quantize o modelo** (opcional)

Reduza o tamanho do modelo com perda mínima de qualidade:

```bash
# Quantização 8-bit (redução de 50% de tamanho)
litgpt convert_lit_checkpoint \
  out/phi2-lora/final \
  --dtype bfloat16 \
  --quantize bnb.nf4

# Quantização 4-bit (redução de 75% de tamanho)
litgpt convert_lit_checkpoint \
  out/phi2-lora/final \
  --quantize bnb.nf4-dq  # Double quantization
```

**Passo 3: Converta para GGUF** (para llama.cpp)

```bash
python scripts/convert_lit_checkpoint.py \
  --checkpoint_path out/phi2-lora/final \
  --output_path models/phi2.gguf \
  --model_name microsoft/phi-2
```

**Passo 4: Faça deploy com API**

```python
from fastapi import FastAPI
from litgpt import LLM

app = FastAPI()
llm = LLM.load("out/phi2-lora/final")

@app.post("/generate")
def generate(prompt: str, max_tokens: int = 100):
    result = llm.generate(
        prompt,
        max_new_tokens=max_tokens,
        temperature=0.7
    )
    return {"response": result}

# Execute: uvicorn api:app --host 0.0.0.0 --port 8000
```

## Quando usar vs alternativas

**Use LitGPT quando:**
- Quiser entender arquiteturas de LLM (código limpo e legível)
- Precisar de receitas de treinamento prontas para produção
- Fins educacionais ou pesquisa
- Prototipagem de ideias de novos modelos
- Usuário do ecossistema Lightning

**Use alternativas no lugar:**
- **Axolotl/TRL**: Mais features de fine-tuning, configs YAML
- **Megatron-Core**: Desempenho máximo para modelos >70B
- **HuggingFace Transformers**: Suporte mais amplo de modelos
- **vLLM**: Apenas inferência (sem treinamento)

## Problemas comuns

**Problema: Falta de memória durante fine-tuning**

Use LoRA em vez de fine-tuning completo:
```bash
# Em vez de litgpt finetune (requer 40GB+)
litgpt finetune_lora  # Requer apenas 12-16GB
```

Ou ative gradient checkpointing:
```bash
litgpt finetune_lora \
  ... \
  --train.gradient_accumulation_iters 4  # Acumule gradientes
```

**Problema: Treinamento muito lento**

Ative Flash Attention (built-in, automático em hardware compatível):
```python
# Já ativado por padrão em GPUs Ampere+ (A100, série RTX 30/40)
# Nenhuma configuração necessária
```

Use micro-batch menor e acumule:
```bash
--train.micro_batch_size 1 \
--train.global_batch_size 32 \
--train.gradient_accumulation_iters 32  # Batch efetivo=32
```

**Problema: Modelo não carrega**

Verifique o nome do modelo:
```bash
# Liste todos os modelos disponíveis
litgpt download list

# Baixe se não existir
litgpt download meta-llama/Meta-Llama-3-8B
```

Verifique o diretório de checkpoints:
```bash
ls checkpoints/
# Deve mostrar: meta-llama/Meta-Llama-3-8B/
```

**Problema: Adapters LoRA muito grandes**

Reduza o rank LoRA:
```bash
--lora_r 8  # Em vez de 16 ou 32
```

Aplique LoRA a menos camadas:
```bash
--lora_query true \
--lora_value true \
--lora_projection false \  # Desative isso
--lora_mlp false  # E isso
```

## Tópicos avançados

**Arquiteturas suportadas**: Veja [references/supported-models.md](references/supported-models.md) para lista completa de 20+ famílias de modelos com tamanhos e capacidades.

**Receitas de treinamento**: Veja [references/training-recipes.md](references/training-recipes.md) para configurações de hiperparâmetros comprovadas para pré-treinamento e fine-tuning.

**Configuração FSDP**: Veja [references/distributed-training.md](references/distributed-training.md) para treinamento multi-GPU com Fully Sharded Data Parallel.

**Arquiteturas customizadas**: Veja [references/custom-models.md](references/custom-models.md) para implementar novas arquiteturas de modelos no estilo LitGPT.

## Requisitos de hardware

- **GPU**: NVIDIA (CUDA 11.8+), AMD (ROCm), Apple Silicon (MPS)
- **Memória**:
  - Inferência (Phi-2): 6GB
  - Fine-tuning LoRA (7B): 16GB
  - Fine-tuning completo (7B): 40GB+
  - Pré-treinamento (1B): 24GB
- **Armazenamento**: 5-50GB por modelo (depende do tamanho)

## Recursos

- GitHub: https://github.com/Lightning-AI/litgpt
- Docs: https://lightning.ai/docs/litgpt
- Tutorials: https://lightning.ai/docs/litgpt/tutorials
- Model zoo: 20+ arquiteturas pré-treinadas (Llama, Gemma, Phi, Qwen, Mistral, Mixtral, Falcon, etc.)