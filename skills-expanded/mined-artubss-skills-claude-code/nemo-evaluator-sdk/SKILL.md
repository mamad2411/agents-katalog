---
name: nemo-evaluator-sdk
description: Avalia LLMs em 100+ benchmarks de 18+ harnesses (MMLU, HumanEval, GSM8K, segurança, VLM) com execução multi-backend. Use quando precisar de avaliação escalável em Docker local, HPC Slurm ou plataformas cloud. Plataforma enterprise-grade da NVIDIA com arquitetura container-first para benchmarking reproduzível.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Evaluation, NeMo, NVIDIA, Benchmarking, MMLU, HumanEval, Multi-Backend, Slurm, Docker, Reproducible, Enterprise]
dependencies: [nemo-evaluator-launcher>=0.1.25, docker]
---

# NeMo Evaluator SDK - Benchmarking Enterprise para LLM

## Início Rápido

NeMo Evaluator SDK avalia LLMs em 100+ benchmarks de 18+ harnesses usando avaliação containerizada e reproduzível com execução multi-backend (Docker local, HPC Slurm, cloud Lepton).

**Instalação**:
```bash
pip install nemo-evaluator-launcher
```

**Defina chave de API e execute avaliação**:
```bash
export NGC_API_KEY=nvapi-your-key-here

# Crie config mínima
cat > config.yaml << 'EOF'
defaults:
  - execution: local
  - deployment: none
  - _self_

execution:
  output_dir: ./results

target:
  api_endpoint:
    model_id: meta/llama-3.1-8b-instruct
    url: https://integrate.api.nvidia.com/v1/chat/completions
    api_key_name: NGC_API_KEY

evaluation:
  tasks:
    - name: ifeval
EOF

# Execute avaliação
nemo-evaluator-launcher run --config-dir . --config-name config
```

**Veja tarefas disponíveis**:
```bash
nemo-evaluator-launcher ls tasks
```

## Fluxos de Trabalho Comuns

### Fluxo 1: Avaliar Modelo em Benchmarks Padrão

Execute benchmarks acadêmicos principais (MMLU, GSM8K, IFEval) em qualquer endpoint compatível com OpenAI.

**Checklist**:
```
Avaliação Padrão:
- [ ] Etapa 1: Configurar endpoint de API
- [ ] Etapa 2: Selecionar benchmarks
- [ ] Etapa 3: Executar avaliação
- [ ] Etapa 4: Verificar resultados
```

**Etapa 1: Configurar endpoint de API**

```yaml
# config.yaml
defaults:
  - execution: local
  - deployment: none
  - _self_

execution:
  output_dir: ./results

target:
  api_endpoint:
    model_id: meta/llama-3.1-8b-instruct
    url: https://integrate.api.nvidia.com/v1/chat/completions
    api_key_name: NGC_API_KEY
```

Para endpoints auto-hospedados (vLLM, TRT-LLM):
```yaml
target:
  api_endpoint:
    model_id: my-model
    url: http://localhost:8000/v1/chat/completions
    api_key_name: ""  # Sem chave necessária para local
```

**Etapa 2: Selecionar benchmarks**

Adicione tarefas à sua config:
```yaml
evaluation:
  tasks:
    - name: ifeval           # Seguimento de instruções
    - name: gpqa_diamond     # QA nível graduado
      env_vars:
        HF_TOKEN: HF_TOKEN   # Algumas tarefas precisam de token HF
    - name: gsm8k_cot_instruct  # Raciocínio matemático
    - name: humaneval        # Geração de código
```

**Etapa 3: Executar avaliação**

```bash
# Execute com arquivo de config
nemo-evaluator-launcher run \
  --config-dir . \
  --config-name config

# Substitua diretório de saída
nemo-evaluator-launcher run \
  --config-dir . \
  --config-name config \
  -o execution.output_dir=./my_results

# Limite amostras para teste rápido
nemo-evaluator-launcher run \
  --config-dir . \
  --config-name config \
  -o +evaluation.nemo_evaluator_config.config.params.limit_samples=10
```

**Etapa 4: Verificar resultados**

```bash
# Verifique status do job
nemo-evaluator-launcher status <invocation_id>

# Liste todas as execuções
nemo-evaluator-launcher ls runs

# Veja resultados
cat results/<invocation_id>/<task>/artifacts/results.yml
```

### Fluxo 2: Executar Avaliação em Cluster HPC Slurm

Execute avaliação em larga escala em infraestrutura HPC.

**Checklist**:
```
Avaliação Slurm:
- [ ] Etapa 1: Configurar definições Slurm
- [ ] Etapa 2: Configurar deployment do modelo
- [ ] Etapa 3: Lançar avaliação
- [ ] Etapa 4: Monitorar status do job
```

**Etapa 1: Configurar definições Slurm**

```yaml
# slurm_config.yaml
defaults:
  - execution: slurm
  - deployment: vllm
  - _self_

execution:
  hostname: cluster.example.com
  account: my_slurm_account
  partition: gpu
  output_dir: /shared/results
  walltime: "04:00:00"
  nodes: 1
  gpus_per_node: 8
```

**Etapa 2: Configurar deployment do modelo**

```yaml
deployment:
  checkpoint_path: /shared/models/llama-3.1-8b
  tensor_parallel_size: 2
  data_parallel_size: 4
  max_model_len: 4096

target:
  api_endpoint:
    model_id: llama-3.1-8b
    # URL auto-gerada pelo deployment
```

**Etapa 3: Lançar avaliação**

```bash
nemo-evaluator-launcher run \
  --config-dir . \
  --config-name slurm_config
```

**Etapa 4: Monitorar status do job**

```bash
# Verifique status (consulta sacct)
nemo-evaluator-launcher status <invocation_id>

# Veja informações detalhadas
nemo-evaluator-launcher info <invocation_id>

# Termine se necessário
nemo-evaluator-launcher kill <invocation_id>
```

### Fluxo 3: Comparar Múltiplos Modelos

Compare múltiplos modelos nas mesmas tarefas.

**Checklist**:
```
Comparação de Modelos:
- [ ] Etapa 1: Criar config base
- [ ] Etapa 2: Executar avaliações com overrides
- [ ] Etapa 3: Exportar e comparar resultados
```

**Etapa 1: Criar config base**

```yaml
# base_eval.yaml
defaults:
  - execution: local
  - deployment: none
  - _self_

execution:
  output_dir: ./comparison_results

evaluation:
  nemo_evaluator_config:
    config:
      params:
        temperature: 0.01
        parallelism: 4
  tasks:
    - name: mmlu_pro
    - name: gsm8k_cot_instruct
    - name: ifeval
```

**Etapa 2: Executar avaliações com overrides de modelo**

```bash
# Avalie Llama 3.1 8B
nemo-evaluator-launcher run \
  --config-dir . \
  --config-name base_eval \
  -o target.api_endpoint.model_id=meta/llama-3.1-8b-instruct \
  -o target.api_endpoint.url=https://integrate.api.nvidia.com/v1/chat/completions

# Avalie Mistral 7B
nemo-evaluator-launcher run \
  --config-dir . \
  --config-name base_eval \
  -o target.api_endpoint.model_id=mistralai/mistral-7b-instruct-v0.3 \
  -o target.api_endpoint.url=https://integrate.api.nvidia.com/v1/chat/completions
```

**Etapa 3: Exportar e comparar**

```bash
# Exporte para MLflow
nemo-evaluator-launcher export <invocation_id_1> --dest mlflow
nemo-evaluator-launcher export <invocation_id_2> --dest mlflow

# Exporte para JSON local
nemo-evaluator-launcher export <invocation_id> --dest local --format json

# Exporte para Weights & Biases
nemo-evaluator-launcher export <invocation_id> --dest wandb
```

### Fluxo 4: Avaliação de Segurança e Visão-Linguagem

Avalie modelos em benchmarks de segurança e tarefas VLM.

**Checklist**:
```
Avaliação Segurança/VLM:
- [ ] Etapa 1: Configurar tarefas de segurança
- [ ] Etapa 2: Configurar tarefas VLM (se aplicável)
- [ ] Etapa 3: Executar avaliação
```

**Etapa 1: Configurar tarefas de segurança**

```yaml
evaluation:
  tasks:
    - name: aegis              # Harness de segurança
    - name: wildguard          # Classificação de segurança
    - name: garak              # Sondagem de segurança
```

**Etapa 2: Configurar tarefas VLM**

```yaml
# Para modelos visão-linguagem
target:
  api_endpoint:
    type: vlm  # Endpoint visão-linguagem
    model_id: nvidia/llama-3.2-90b-vision-instruct
    url: https://integrate.api.nvidia.com/v1/chat/completions

evaluation:
  tasks:
    - name: ocrbench           # Avaliação OCR
    - name: chartqa            # Compreensão de gráficos
    - name: mmmu               # Compreensão multimodal
```

## Quando Usar vs Alternativas

**Use NeMo Evaluator quando:**
- Precisar de **100+ benchmarks** de 18+ harnesses em uma plataforma
- Executar avaliações em **clusters HPC Slurm** ou cloud
- Exigir avaliação containerizada **reproduzível**
- Avaliar contra **APIs compatíveis com OpenAI** (vLLM, TRT-LLM, NIMs)
- Precisar de avaliação **enterprise-grade** com exportação de resultados (MLflow, W&B)

**Use alternativas em vez disso:**
- **lm-evaluation-harness**: Setup mais simples para avaliação local rápida
- **bigcode-evaluation-harness**: Focada apenas em benchmarks de código
- **HELM**: Avaliação mais ampla de Stanford (equidade, eficiência)
- **Scripts customizados**: Avaliação de domínio altamente especializada

## Harnesses e Tarefas Suportadas

| Harness | Contagem de Tarefas | Categorias |
|---------|-----------|------------|
| `lm-evaluation-harness` | 60+ | MMLU, GSM8K, HellaSwag, ARC |
| `simple-evals` | 20+ | GPQA, MATH, AIME |
| `bigcode-evaluation-harness` | 25+ | HumanEval, MBPP, MultiPL-E |
| `safety-harness` | 3 | Aegis, WildGuard |
| `garak` | 1 | Sondagem de segurança |
| `vlmevalkit` | 6+ | OCRBench, ChartQA, MMMU |
| `bfcl` | 6 | Chamada de função v2/v3 |
| `mtbench` | 2 | Conversa multi-turno |
| `livecodebench` | 10+ | Avaliação de código ao vivo |
| `helm` | 15 | Domínio médico |
| `nemo-skills` | 8 | Matemática, ciência, agentic |

## Problemas Comuns

**Problema: Pull de container falha**

Certifique-se de que as credenciais NGC estão configuradas:
```bash
docker login nvcr.io -u '$oauthtoken' -p $NGC_API_KEY
```

**Problema: Tarefa requer variável de ambiente**

Algumas tarefas precisam de HF_TOKEN ou JUDGE_API_KEY:
```yaml
evaluation:
  tasks:
    - name: gpqa_diamond
      env_vars:
        HF_TOKEN: HF_TOKEN  # Mapeia nome de var env para var env
```

**Problema: Timeout de avaliação**

Aumente paralelismo ou reduza amostras:
```bash
-o +evaluation.nemo_evaluator_config.config.params.parallelism=8
-o +evaluation.nemo_evaluator_config.config.params.limit_samples=100
```

**Problema: Job Slurm não inicia**

Verifique conta e partição Slurm:
```yaml
execution:
  account: correct_account
  partition: gpu
  qos: normal  # Pode precisar de QOS específico
```

**Problema: Resultados diferentes do esperado**

Verifique se a configuração corresponde às definições reportadas:
```yaml
evaluation:
  nemo_evaluator_config:
    config:
      params:
        temperature: 0.0  # Determinístico
        num_fewshot: 5    # Verifique contagem de fewshot do paper
```

## Referência CLI

| Comando | Descrição |
|---------|-------------|
| `run` | Executar avaliação com config |
| `status <id>` | Verificar status do job |
| `info <id>` | Visualizar informações detalhadas do job |
| `ls tasks` | Listar benchmarks disponíveis |
| `ls runs` | Listar todas as invocações |
| `export <id>` | Exportar resultados (mlflow/wandb/local) |
| `kill <id>` | Terminar job em execução |

## Exemplos de Override de Configuração

```bash
# Substitua endpoint do modelo
-o target.api_endpoint.model_id=my-model
-o target.api_endpoint.url=http://localhost:8000/v1/chat/completions

# Adicione parâmetros de avaliação
-o +evaluation.nemo_evaluator_config.config.params.temperature=0.5
-o +evaluation.nemo_evaluator_config.config.params.parallelism=8
-o +evaluation.nemo_evaluator_config.config.params.limit_samples=50

# Altere definições de execução
-o execution.output_dir=/custom/path
-o execution.mode=parallel

# Defina tarefas dinamicamente
-o 'evaluation.tasks=[{name: ifeval}, {name: gsm8k}]'
```

## Uso da API Python

Para avaliação programática sem a CLI:

```python
from nemo_evaluator.core.evaluate import evaluate
from nemo_evaluator.api.api_dataclasses import (
    EvaluationConfig,
    EvaluationTarget,
    ApiEndpoint,
    EndpointType,
    ConfigParams
)

# Configure avaliação
eval_config = EvaluationConfig(
    type="mmlu_pro",
    output_dir="./results",
    params=ConfigParams(
        limit_samples=10,
        temperature=0.0,
        max_new_tokens=1024,
        parallelism=4
    )
)

# Configure endpoint alvo
target_config = EvaluationTarget(
    api_endpoint=ApiEndpoint(
        model_id="meta/llama-3.1-8b-instruct",
        url="https://integrate.api.nvidia.com/v1/chat/completions",
        type=EndpointType.CHAT,
        api_key="nvapi-your-key-here"
    )
)

# Execute avaliação
result = evaluate(eval_cfg=eval_config, target_cfg=target_config)
```

## Tópicos Avançados

**Execução multi-backend**: Veja [references/execution-backends.md](references/execution-backends.md)
**Aprofundamento em configuração**: Veja [references/configuration.md](references/configuration.md)
**Sistema de adaptador e interceptor**: Veja [references/adapter-system.md](references/adapter-system.md)
**Integração de benchmark customizado**: Veja [references/custom-benchmarks.md](references/custom-benchmarks.md)

## Requisitos

- **Python**: 3.10-3.13
- **Docker**: Necessário para execução local
- **Chave NGC API**: Para puxar containers e usar NVIDIA Build
- **HF_TOKEN**: Necessário para alguns benchmarks (GPQA, MMLU)

## Recursos

- **GitHub**: https://github.com/NVIDIA-NeMo/Evaluator
- **NGC Containers**: nvcr.io/nvidia/eval-factory/
- **NVIDIA Build**: https://build.nvidia.com (modelos hospedados gratuitamente)
- **Documentação**: https://github.com/NVIDIA-NeMo/Evaluator/tree/main/docs