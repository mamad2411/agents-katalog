---
name: evaluating-code-models
description: Avalia modelos de geração de código em HumanEval, MBPP, MultiPL-E e 15+ benchmarks com métricas pass@k. Use ao comparar modelos de código, avaliar capacidades de codificação, testar suporte multilíngue ou medir qualidade de geração de código. Padrão da indústria do BigCode Project usado pelos leaderboards do HuggingFace.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Evaluation, Code Generation, HumanEval, MBPP, MultiPL-E, Pass@k, BigCode, Benchmarking, Code Models]
dependencies: [bigcode-evaluation-harness, transformers>=4.25.1, accelerate>=0.13.2, datasets>=2.6.1]
---

# BigCode Evaluation Harness - Benchmarking de Modelos de Código

## Primeiros Passos

BigCode Evaluation Harness avalia modelos de geração de código em 15+ benchmarks incluindo HumanEval, MBPP e MultiPL-E (18 idiomas).

**Instalação**:
```bash
git clone https://github.com/bigcode-project/bigcode-evaluation-harness.git
cd bigcode-evaluation-harness
pip install -e .
accelerate config
```

**Avalie em HumanEval**:
```bash
accelerate launch main.py \
  --model bigcode/starcoder2-7b \
  --tasks humaneval \
  --max_length_generation 512 \
  --temperature 0.2 \
  --n_samples 20 \
  --batch_size 10 \
  --allow_code_execution \
  --save_generations
```

**Visualize tarefas disponíveis**:
```bash
python -c "from bigcode_eval.tasks import ALL_TASKS; print(ALL_TASKS)"
```

## Fluxos de Trabalho Comuns

### Fluxo de Trabalho 1: Avaliação de Benchmark de Código Padrão

Avalie o modelo em benchmarks de código principais (HumanEval, MBPP, HumanEval+).

**Checklist**:
```
Avaliação de Benchmark de Código:
- [ ] Etapa 1: Escolha a suite de benchmark
- [ ] Etapa 2: Configure o modelo e geração
- [ ] Etapa 3: Execute avaliação com execução de código
- [ ] Etapa 4: Analise resultados pass@k
```

**Etapa 1: Escolha a suite de benchmark**

**Geração de código Python** (mais comum):
- **HumanEval**: 164 problemas manuscritos, preenchimento de função
- **HumanEval+**: Os mesmos 164 problemas com 80× mais testes (mais rigoroso)
- **MBPP**: 500 problemas crowdsourced, dificuldade de entrada
- **MBPP+**: 399 problemas curados com 35× mais testes

**Multilíngue** (18 idiomas):
- **MultiPL-E**: HumanEval/MBPP traduzido para C++, Java, JavaScript, Go, Rust, etc.

**Avançado**:
- **APPS**: 10.000 problemas (introdutório/entrevista/competição)
- **DS-1000**: 1.000 problemas de ciência de dados em 7 bibliotecas

**Etapa 2: Configure o modelo e geração**

```bash
# Modelo HuggingFace padrão
accelerate launch main.py \
  --model bigcode/starcoder2-7b \
  --tasks humaneval \
  --max_length_generation 512 \
  --temperature 0.2 \
  --do_sample True \
  --n_samples 200 \
  --batch_size 50 \
  --allow_code_execution

# Modelo quantizado (4-bit)
accelerate launch main.py \
  --model codellama/CodeLlama-34b-hf \
  --tasks humaneval \
  --load_in_4bit \
  --max_length_generation 512 \
  --allow_code_execution

# Modelo personalizado/privado
accelerate launch main.py \
  --model /path/to/my-code-model \
  --tasks humaneval \
  --trust_remote_code \
  --use_auth_token \
  --allow_code_execution
```

**Etapa 3: Execute avaliação**

```bash
# Avaliação completa com estimativa pass@k (k=1,10,100)
accelerate launch main.py \
  --model bigcode/starcoder2-7b \
  --tasks humaneval \
  --temperature 0.8 \
  --n_samples 200 \
  --batch_size 50 \
  --allow_code_execution \
  --save_generations \
  --metric_output_path results/starcoder2-humaneval.json
```

**Etapa 4: Analise resultados**

Resultados em `results/starcoder2-humaneval.json`:
```json
{
  "humaneval": {
    "pass@1": 0.354,
    "pass@10": 0.521,
    "pass@100": 0.689
  },
  "config": {
    "model": "bigcode/starcoder2-7b",
    "temperature": 0.8,
    "n_samples": 200
  }
}
```

### Fluxo de Trabalho 2: Avaliação Multilíngue (MultiPL-E)

Avalie geração de código em 18 linguagens de programação.

**Checklist**:
```
Avaliação Multilíngue:
- [ ] Etapa 1: Gere soluções (máquina host)
- [ ] Etapa 2: Execute avaliação em Docker (execução segura)
- [ ] Etapa 3: Compare entre idiomas
```

**Etapa 1: Gere soluções no host**

```bash
# Gere sem execução (seguro)
accelerate launch main.py \
  --model bigcode/starcoder2-7b \
  --tasks multiple-py,multiple-js,multiple-java,multiple-cpp \
  --max_length_generation 650 \
  --temperature 0.8 \
  --n_samples 50 \
  --batch_size 50 \
  --generation_only \
  --save_generations \
  --save_generations_path generations_multi.json
```

**Etapa 2: Avalie em container Docker**

```bash
# Extraia a imagem Docker MultiPL-E
docker pull ghcr.io/bigcode-project/evaluation-harness-multiple

# Execute avaliação dentro do container
docker run -v $(pwd)/generations_multi.json:/app/generations.json:ro \
  -it evaluation-harness-multiple python3 main.py \
  --model bigcode/starcoder2-7b \
  --tasks multiple-py,multiple-js,multiple-java,multiple-cpp \
  --load_generations_path /app/generations.json \
  --allow_code_execution \
  --n_samples 50
```

**Idiomas suportados**: Python, JavaScript, Java, C++, Go, Rust, TypeScript, C#, PHP, Ruby, Swift, Kotlin, Scala, Perl, Julia, Lua, R, Racket

### Fluxo de Trabalho 3: Avaliação de Modelo com Instruções

Avalie modelos chat/instruções com formatação apropriada.

**Checklist**:
```
Avaliação de Modelo com Instruções:
- [ ] Etapa 1: Use tarefas com instruções
- [ ] Etapa 2: Configure tokens de instrução
- [ ] Etapa 3: Execute avaliação
```

**Etapa 1: Escolha tarefas com instruções**

- **instruct-humaneval**: HumanEval com prompts de instrução
- **humanevalsynthesize-{lang}**: Tarefas de síntese HumanEvalPack

**Etapa 2: Configure tokens de instrução**

```bash
# Para modelos com templates de chat (ex: CodeLlama-Instruct)
accelerate launch main.py \
  --model codellama/CodeLlama-7b-Instruct-hf \
  --tasks instruct-humaneval \
  --instruction_tokens "<s>[INST],</s>,[/INST]" \
  --max_length_generation 512 \
  --allow_code_execution
```

**Etapa 3: HumanEvalPack para modelos com instruções**

```bash
# Teste síntese de código em 6 idiomas
accelerate launch main.py \
  --model codellama/CodeLlama-7b-Instruct-hf \
  --tasks humanevalsynthesize-python,humanevalsynthesize-js \
  --prompt instruct \
  --max_length_generation 512 \
  --allow_code_execution
```

### Fluxo de Trabalho 4: Compare Múltiplos Modelos

Suite de benchmarking para comparação de modelos.

**Etapa 1: Crie script de avaliação**

```bash
#!/bin/bash
# eval_models.sh

MODELS=(
  "bigcode/starcoder2-7b"
  "codellama/CodeLlama-7b-hf"
  "deepseek-ai/deepseek-coder-6.7b-base"
)
TASKS="humaneval,mbpp"

for model in "${MODELS[@]}"; do
  model_name=$(echo $model | tr '/' '-')
  echo "Avaliando $model"

  accelerate launch main.py \
    --model $model \
    --tasks $TASKS \
    --temperature 0.2 \
    --n_samples 20 \
    --batch_size 20 \
    --allow_code_execution \
    --metric_output_path results/${model_name}.json
done
```

**Etapa 2: Gere tabela de comparação**

```python
import json
import pandas as pd

models = ["bigcode-starcoder2-7b", "codellama-CodeLlama-7b-hf", "deepseek-ai-deepseek-coder-6.7b-base"]
results = []

for model in models:
    with open(f"results/{model}.json") as f:
        data = json.load(f)
        results.append({
            "Model": model,
            "HumanEval pass@1": f"{data['humaneval']['pass@1']:.3f}",
            "MBPP pass@1": f"{data['mbpp']['pass@1']:.3f}"
        })

df = pd.DataFrame(results)
print(df.to_markdown(index=False))
```

## Quando Usar vs Alternativas

**Use BigCode Evaluation Harness quando:**
- Avaliar modelos de **geração de código** especificamente
- Precisar de avaliação **multilíngue** (18 idiomas via MultiPL-E)
- Testar **correção funcional** com testes unitários (pass@k)
- Fazer benchmarking para **BigCode/HuggingFace leaderboards**
- Avaliar capacidades **fill-in-the-middle** (FIM)

**Use alternativas em vez disso:**
- **lm-evaluation-harness**: Benchmarks gerais de LLM (MMLU, GSM8K, HellaSwag)
- **EvalPlus**: HumanEval+/MBPP+ mais rigorosos com mais casos de teste
- **SWE-bench**: Resolução de problemas reais do GitHub
- **LiveCodeBench**: Problemas sem contaminação, continuamente atualizados
- **CodeXGLUE**: Tarefas de compreensão de código (detecção de clone, previsão de defeito)

## Benchmarks Suportados

| Benchmark | Problemas | Idiomas | Métrica | Caso de Uso |
|-----------|-----------|---------|---------|------------|
| HumanEval | 164 | Python | pass@k | Conclusão de código padrão |
| HumanEval+ | 164 | Python | pass@k | Avaliação mais rigorosa (80× testes) |
| MBPP | 500 | Python | pass@k | Problemas de nível introdutório |
| MBPP+ | 399 | Python | pass@k | Avaliação mais rigorosa (35× testes) |
| MultiPL-E | 164×18 | 18 idiomas | pass@k | Avaliação multilíngue |
| APPS | 10.000 | Python | pass@k | Nível competição |
| DS-1000 | 1.000 | Python | pass@k | Ciência de dados (pandas, numpy, etc.) |
| HumanEvalPack | 164×3×6 | 6 idiomas | pass@k | Síntese/correção/explicação |
| Mercury | 1.889 | Python | Eficiência | Eficiência computacional |

## Problemas Comuns

**Problema: Resultados diferentes dos relatados em artigos**

Verifique estes fatores:
```bash
# 1. Verifique n_samples (necessário 200 para pass@k preciso)
--n_samples 200

# 2. Verifique temperatura (0.2 para algo próximo a greedy, 0.8 para sampling)
--temperature 0.8

# 3. Verifique que o nome da tarefa corresponde exatamente
--tasks humaneval  # Não "human_eval" ou "HumanEval"

# 4. Verifique max_length_generation
--max_length_generation 512  # Aumente para problemas mais longos
```

**Problema: Memória CUDA insuficiente**

```bash
# Use quantização
--load_in_8bit
# OU
--load_in_4bit

# Reduza o tamanho do batch
--batch_size 1

# Defina limite de memória
--max_memory_per_gpu "20GiB"
```

**Problema: Execução de código trava ou atinge timeout**

Use Docker para execução segura:
```bash
# Gere no host (sem execução)
--generation_only --save_generations

# Avalie em Docker
docker run ... --allow_code_execution --load_generations_path ...
```

**Problema: Pontuações baixas em modelos com instruções**

Garanta formatação correta de instruções:
```bash
# Use tarefas específicas de instruções
--tasks instruct-humaneval

# Defina tokens de instrução para seu modelo
--instruction_tokens "<s>[INST],</s>,[/INST]"
```

**Problema: Falhas em idiomas MultiPL-E**

Use a imagem Docker dedicada:
```bash
docker pull ghcr.io/bigcode-project/evaluation-harness-multiple
```

## Referência de Comandos

| Argumento | Padrão | Descrição |
|-----------|--------|----------|
| `--model` | - | ID de modelo HuggingFace ou caminho local |
| `--tasks` | - | Nomes de tarefas separados por vírgula |
| `--n_samples` | 1 | Amostras por problema (200 para pass@k) |
| `--temperature` | 0.2 | Temperatura de sampling |
| `--max_length_generation` | 512 | Máximo de tokens (prompt + geração) |
| `--batch_size` | 1 | Tamanho do batch por GPU |
| `--allow_code_execution` | False | Habilite execução de código (obrigatório) |
| `--generation_only` | False | Gere sem avaliação |
| `--load_generations_path` | - | Carregue soluções pré-geradas |
| `--save_generations` | False | Salve código gerado |
| `--metric_output_path` | results.json | Arquivo de saída para métricas |
| `--load_in_8bit` | False | Quantização de 8-bit |
| `--load_in_4bit` | False | Quantização de 4-bit |
| `--trust_remote_code` | False | Permita código de modelo personalizado |
| `--precision` | fp32 | Precisão do modelo (fp32/fp16/bf16) |

## Requisitos de Hardware

| Tamanho do Modelo | VRAM (fp16) | VRAM (4-bit) | Tempo (HumanEval, n=200) |
|-------------------|-------------|--------------|-------------------------|
| 7B | 14GB | 6GB | ~30 min (A100) |
| 13B | 26GB | 10GB | ~1 hora (A100) |
| 34B | 68GB | 20GB | ~2 horas (A100) |

## Recursos

- **GitHub**: https://github.com/bigcode-project/bigcode-evaluation-harness
- **Documentação**: https://github.com/bigcode-project/bigcode-evaluation-harness/tree/main/docs
- **BigCode Leaderboard**: https://huggingface.co/spaces/bigcode/bigcode-models-leaderboard
- **HumanEval Dataset**: https://huggingface.co/datasets/openai/openai_humaneval
- **MultiPL-E**: https://github.com/nuprl/MultiPL-E