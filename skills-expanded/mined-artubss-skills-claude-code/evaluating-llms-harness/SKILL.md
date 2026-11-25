---
name: evaluating-llms-harness
description: Avalia LLMs em mais de 60 benchmarks acadêmicos (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Use quando benchmarking de qualidade de modelo, comparação de modelos, relatório de resultados acadêmicos ou rastreamento de progresso de treinamento. Padrão da indústria usado por EleutherAI, HuggingFace e laboratórios principais. Suporta HuggingFace, vLLM, APIs.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Evaluation, LM Evaluation Harness, Benchmarking, MMLU, HumanEval, GSM8K, EleutherAI, Model Quality, Academic Benchmarks, Industry Standard]
dependencies: [lm-eval, transformers, vllm]
---

# lm-evaluation-harness - Benchmarking de LLM

## Início rápido

lm-evaluation-harness avalia LLMs em mais de 60 benchmarks acadêmicos usando prompts e métricas padronizadas.

**Instalação**:
```bash
pip install lm-eval
```

**Avalie qualquer modelo HuggingFace**:
```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag \
  --device cuda:0 \
  --batch_size 8
```

**Veja tarefas disponíveis**:
```bash
lm_eval --tasks list
```

## Fluxos de trabalho comuns

### Fluxo de trabalho 1: Avaliação de benchmark padrão

Avalie o modelo em benchmarks principais (MMLU, GSM8K, HumanEval).

Copie esta lista de verificação:

```
Avaliação de Benchmark:
- [ ] Etapa 1: Escolha a suite de benchmark
- [ ] Etapa 2: Configure o modelo
- [ ] Etapa 3: Execute a avaliação
- [ ] Etapa 4: Analise os resultados
```

**Etapa 1: Escolha a suite de benchmark**

**Benchmarks principais de raciocínio**:
- **MMLU** (Massive Multitask Language Understanding) - 57 disciplinas, múltipla escolha
- **GSM8K** - Problemas de matemática de escola primária
- **HellaSwag** - Raciocínio de senso comum
- **TruthfulQA** - Veracidade e factualidade
- **ARC** (AI2 Reasoning Challenge) - Perguntas de ciência

**Benchmarks de código**:
- **HumanEval** - Geração de código Python (164 problemas)
- **MBPP** (Mostly Basic Python Problems) - Codificação Python

**Suite padrão** (recomendado para lançamentos de modelo):
```bash
--tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge
```

**Etapa 2: Configure o modelo**

**Modelo HuggingFace**:
```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,dtype=bfloat16 \
  --tasks mmlu \
  --device cuda:0 \
  --batch_size auto  # Detecta automaticamente o tamanho de lote ideal
```

**Modelo quantizado (4-bit/8-bit)**:
```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,load_in_4bit=True \
  --tasks mmlu \
  --device cuda:0
```

**Checkpoint customizado**:
```bash
lm_eval --model hf \
  --model_args pretrained=/path/to/my-model,tokenizer=/path/to/tokenizer \
  --tasks mmlu \
  --device cuda:0
```

**Etapa 3: Execute a avaliação**

```bash
# Avaliação completa de MMLU (57 disciplinas)
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu \
  --num_fewshot 5 \  # Avaliação 5-shot (padrão)
  --batch_size 8 \
  --output_path results/ \
  --log_samples  # Salva predições individuais

# Múltiplos benchmarks de uma vez
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge \
  --num_fewshot 5 \
  --batch_size 8 \
  --output_path results/llama2-7b-eval.json
```

**Etapa 4: Analise os resultados**

Resultados salvos em `results/llama2-7b-eval.json`:

```json
{
  "results": {
    "mmlu": {
      "acc": 0.459,
      "acc_stderr": 0.004
    },
    "gsm8k": {
      "exact_match": 0.142,
      "exact_match_stderr": 0.006
    },
    "hellaswag": {
      "acc_norm": 0.765,
      "acc_norm_stderr": 0.004
    }
  },
  "config": {
    "model": "hf",
    "model_args": "pretrained=meta-llama/Llama-2-7b-hf",
    "num_fewshot": 5
  }
}
```

### Fluxo de trabalho 2: Rastreie o progresso do treinamento

Avalie checkpoints durante o treinamento.

```
Rastreamento de Progresso de Treinamento:
- [ ] Etapa 1: Configure avaliação periódica
- [ ] Etapa 2: Escolha benchmarks rápidos
- [ ] Etapa 3: Automatize a avaliação
- [ ] Etapa 4: Plote curvas de aprendizado
```

**Etapa 1: Configure avaliação periódica**

Avalie a cada N etapas de treinamento:

```bash
#!/bin/bash
# eval_checkpoint.sh

CHECKPOINT_DIR=$1
STEP=$2

lm_eval --model hf \
  --model_args pretrained=$CHECKPOINT_DIR/checkpoint-$STEP \
  --tasks gsm8k,hellaswag \
  --num_fewshot 0 \  # 0-shot para velocidade
  --batch_size 16 \
  --output_path results/step-$STEP.json
```

**Etapa 2: Escolha benchmarks rápidos**

Benchmarks rápidos para avaliação frequente:
- **HellaSwag**: ~10 minutos em 1 GPU
- **GSM8K**: ~5 minutos
- **PIQA**: ~2 minutos

Evite para avaliação frequente (muito lento):
- **MMLU**: ~2 horas (57 disciplinas)
- **HumanEval**: Requer execução de código

**Etapa 3: Automatize a avaliação**

Integre com script de treinamento:

```python
# No loop de treinamento
if step % eval_interval == 0:
    model.save_pretrained(f"checkpoints/step-{step}")

    # Execute avaliação
    os.system(f"./eval_checkpoint.sh checkpoints step-{step}")
```

Ou use callbacks do PyTorch Lightning:

```python
from pytorch_lightning import Callback

class EvalHarnessCallback(Callback):
    def on_validation_epoch_end(self, trainer, pl_module):
        step = trainer.global_step
        checkpoint_path = f"checkpoints/step-{step}"

        # Salve checkpoint
        trainer.save_checkpoint(checkpoint_path)

        # Execute lm-eval
        os.system(f"lm_eval --model hf --model_args pretrained={checkpoint_path} ...")
```

**Etapa 4: Plote curvas de aprendizado**

```python
import json
import matplotlib.pyplot as plt

# Carregue todos os resultados
steps = []
mmlu_scores = []

for file in sorted(glob.glob("results/step-*.json")):
    with open(file) as f:
        data = json.load(f)
        step = int(file.split("-")[1].split(".")[0])
        steps.append(step)
        mmlu_scores.append(data["results"]["mmlu"]["acc"])

# Plote
plt.plot(steps, mmlu_scores)
plt.xlabel("Training Step")
plt.ylabel("MMLU Accuracy")
plt.title("Training Progress")
plt.savefig("training_curve.png")
```

### Fluxo de trabalho 3: Compare múltiplos modelos

Suite de benchmark para comparação de modelos.

```
Comparação de Modelos:
- [ ] Etapa 1: Defina a lista de modelos
- [ ] Etapa 2: Execute avaliações
- [ ] Etapa 3: Gere tabela de comparação
```

**Etapa 1: Defina a lista de modelos**

```bash
# models.txt
meta-llama/Llama-2-7b-hf
meta-llama/Llama-2-13b-hf
mistralai/Mistral-7B-v0.1
microsoft/phi-2
```

**Etapa 2: Execute avaliações**

```bash
#!/bin/bash
# eval_all_models.sh

TASKS="mmlu,gsm8k,hellaswag,truthfulqa"

while read model; do
    echo "Evaluating $model"

    # Extraia nome do modelo para arquivo de saída
    model_name=$(echo $model | sed 's/\//-/g')

    lm_eval --model hf \
      --model_args pretrained=$model,dtype=bfloat16 \
      --tasks $TASKS \
      --num_fewshot 5 \
      --batch_size auto \
      --output_path results/$model_name.json

done < models.txt
```

**Etapa 3: Gere tabela de comparação**

```python
import json
import pandas as pd

models = [
    "meta-llama-Llama-2-7b-hf",
    "meta-llama-Llama-2-13b-hf",
    "mistralai-Mistral-7B-v0.1",
    "microsoft-phi-2"
]

tasks = ["mmlu", "gsm8k", "hellaswag", "truthfulqa"]

results = []
for model in models:
    with open(f"results/{model}.json") as f:
        data = json.load(f)
        row = {"Model": model.replace("-", "/")}
        for task in tasks:
            # Obtenha métrica primária para cada tarefa
            metrics = data["results"][task]
            if "acc" in metrics:
                row[task.upper()] = f"{metrics['acc']:.3f}"
            elif "exact_match" in metrics:
                row[task.upper()] = f"{metrics['exact_match']:.3f}"
        results.append(row)

df = pd.DataFrame(results)
print(df.to_markdown(index=False))
```

Saída:
```
| Model                  | MMLU  | GSM8K | HELLASWAG | TRUTHFULQA |
|------------------------|-------|-------|-----------|------------|
| meta-llama/Llama-2-7b  | 0.459 | 0.142 | 0.765     | 0.391      |
| meta-llama/Llama-2-13b | 0.549 | 0.287 | 0.801     | 0.430      |
| mistralai/Mistral-7B   | 0.626 | 0.395 | 0.812     | 0.428      |
| microsoft/phi-2        | 0.560 | 0.613 | 0.682     | 0.447      |
```

### Fluxo de trabalho 4: Avalie com vLLM (inferência mais rápida)

Use backend vLLM para avaliação 5-10x mais rápida.

```
Avaliação com vLLM:
- [ ] Etapa 1: Instale vLLM
- [ ] Etapa 2: Configure backend vLLM
- [ ] Etapa 3: Execute avaliação
```

**Etapa 1: Instale vLLM**

```bash
pip install vllm
```

**Etapa 2: Configure backend vLLM**

```bash
lm_eval --model vllm \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8 \
  --tasks mmlu \
  --batch_size auto
```

**Etapa 3: Execute avaliação**

vLLM é 5-10× mais rápido que HuggingFace padrão:

```bash
# HF padrão: ~2 horas para MMLU em modelo 7B
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu \
  --batch_size 8

# vLLM: ~15-20 minutos para MMLU em modelo 7B
lm_eval --model vllm \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=2 \
  --tasks mmlu \
  --batch_size auto
```

## Quando usar vs alternativas

**Use lm-evaluation-harness quando:**
- Benchmarking de modelos para artigos acadêmicos
- Comparação de qualidade de modelo em tarefas padrão
- Rastreamento de progresso de treinamento
- Relatório de métricas padronizadas (todos usam os mesmos prompts)
- Necessidade de avaliação reproduzível

**Use alternativas em vez disso:**
- **HELM** (Stanford): Avaliação mais ampla (fairness, eficiência, calibração)
- **AlpacaEval**: Avaliação de seguimento de instruções com juízes LLM
- **MT-Bench**: Avaliação multi-turno conversacional
- **Scripts customizados**: Avaliação específica de domínio

## Problemas comuns

**Problema: Avaliação muito lenta**

Use backend vLLM:
```bash
lm_eval --model vllm \
  --model_args pretrained=model-name,tensor_parallel_size=2
```

Ou reduza exemplos fewshot:
```bash
--num_fewshot 0  # Em vez de 5
```

Ou avalie subconjunto de MMLU:
```bash
--tasks mmlu_stem  # Apenas disciplinas STEM
```

**Problema: Sem memória disponível**

Reduza tamanho do lote:
```bash
--batch_size 1  # Ou --batch_size auto
```

Use quantização:
```bash
--model_args pretrained=model-name,load_in_8bit=True
```

Ative offloading de CPU:
```bash
--model_args pretrained=model-name,device_map=auto,offload_folder=offload
```

**Problema: Resultados diferentes dos relatados**

Verifique contagem de fewshot:
```bash
--num_fewshot 5  # A maioria dos artigos usa 5-shot
```

Verifique nome exato da tarefa:
```bash
--tasks mmlu  # Não mmlu_direct ou mmlu_fewshot
```

Verifique correspondência de modelo e tokenizador:
```bash
--model_args pretrained=model-name,tokenizer=same-model-name
```

**Problema: HumanEval não executa código**

Instale dependências de execução:
```bash
pip install human-eval
```

Ative execução de código:
```bash
lm_eval --model hf \
  --model_args pretrained=model-name \
  --tasks humaneval \
  --allow_code_execution  # Necessário para HumanEval
```

## Tópicos avançados

**Descrições de benchmarks**: Veja [references/benchmark-guide.md](references/benchmark-guide.md) para descrição detalhada de todas as 60+ tarefas, o que medem e interpretação.

**Tarefas customizadas**: Veja [references/custom-tasks.md](references/custom-tasks.md) para criar tarefas de avaliação específicas de domínio.

**Avaliação de API**: Veja [references/api-evaluation.md](references/api-evaluation.md) para avaliar modelos OpenAI, Anthropic e outras APIs.

**Estratégias multi-GPU**: Veja [references/distributed-eval.md](references/distributed-eval.md) para avaliação data parallel e tensor parallel.

## Requisitos de hardware

- **GPU**: NVIDIA (CUDA 11.8+), funciona em CPU (muito lento)
- **VRAM**:
  - Modelo 7B: 16GB (bf16) ou 8GB (8-bit)
  - Modelo 13B: 28GB (bf16) ou 14GB (8-bit)
  - Modelo 70B: Requer multi-GPU ou quantização
- **Tempo** (modelo 7B, single A100):
  - HellaSwag: 10 minutos
  - GSM8K: 5 minutos
  - MMLU (completo): 2 horas
  - HumanEval: 20 minutos

## Recursos

- GitHub: https://github.com/EleutherAI/lm-evaluation-harness
- Documentação: https://github.com/EleutherAI/lm-evaluation-harness/tree/main/docs
- Biblioteca de tarefas: 60+ tarefas incluindo MMLU, GSM8K, HumanEval, TruthfulQA, HellaSwag, ARC, WinoGrande, etc.
- Leaderboard: https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard (usa este harness)