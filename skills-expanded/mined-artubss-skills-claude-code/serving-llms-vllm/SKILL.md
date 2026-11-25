---
name: serving-llms-vllm
description: Serve LLMs com alta throughput usando PagedAttention do vLLM e continuous batching. Use ao fazer deploy de APIs LLM em produção, otimizar latência/throughput de inferência, ou servir modelos com memória GPU limitada. Suporta endpoints compatíveis com OpenAI, quantização (GPTQ/AWQ/FP8) e tensor parallelism.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [vLLM, Inference Serving, PagedAttention, Continuous Batching, High Throughput, Production, OpenAI API, Quantization, Tensor Parallelism]
dependencies: [vllm, torch, transformers]
---

# vLLM - Serving LLM de Alto Desempenho

## Quick start

vLLM atinge 24x maior throughput que transformers padrão através de PagedAttention (KV cache baseado em blocos) e continuous batching (misturando requisições de prefill/decode).

**Instalação**:
```bash
pip install vllm
```

**Inferência offline básica**:
```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3-8B-Instruct")
sampling = SamplingParams(temperature=0.7, max_tokens=256)

outputs = llm.generate(["Explain quantum computing"], sampling)
print(outputs[0].outputs[0].text)
```

**Servidor compatível com OpenAI**:
```bash
vllm serve meta-llama/Llama-3-8B-Instruct

# Query com SDK OpenAI
python -c "
from openai import OpenAI
client = OpenAI(base_url='http://localhost:8000/v1', api_key='EMPTY')
print(client.chat.completions.create(
    model='meta-llama/Llama-3-8B-Instruct',
    messages=[{'role': 'user', 'content': 'Hello!'}]
).choices[0].message.content)
"
```

## Fluxos de trabalho comuns

### Workflow 1: Deploy de API em produção

Copie este checklist e acompanhe o progresso:

```
Progresso de Deploy:
- [ ] Etapa 1: Configurar settings do servidor
- [ ] Etapa 2: Testar com tráfego limitado
- [ ] Etapa 3: Ativar monitoramento
- [ ] Etapa 4: Deploy em produção
- [ ] Etapa 5: Verificar métricas de desempenho
```

**Etapa 1: Configurar settings do servidor**

Escolha configuração baseada no tamanho do modelo:

```bash
# Para modelos 7B-13B em GPU única
vllm serve meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --max-model-len 8192 \
  --port 8000

# Para modelos 30B-70B com tensor parallelism
vllm serve meta-llama/Llama-2-70b-hf \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.9 \
  --quantization awq \
  --port 8000

# Para produção com caching e métricas
vllm serve meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --enable-prefix-caching \
  --enable-metrics \
  --metrics-port 9090 \
  --port 8000 \
  --host 0.0.0.0
```

**Etapa 2: Testar com tráfego limitado**

Execute teste de carga antes de produção:

```bash
# Instalar ferramenta de load testing
pip install locust

# Criar test_load.py com requisições de amostra
# Executar: locust -f test_load.py --host http://localhost:8000
```

Verifique se TTFT (time to first token) < 500ms e throughput > 100 req/sec.

**Etapa 3: Ativar monitoramento**

vLLM expõe métricas Prometheus na porta 9090:

```bash
curl http://localhost:9090/metrics | grep vllm
```

Métricas-chave para monitorar:
- `vllm:time_to_first_token_seconds` - Latência
- `vllm:num_requests_running` - Requisições ativas
- `vllm:gpu_cache_usage_perc` - Utilização de KV cache

**Etapa 4: Deploy em produção**

Use Docker para deploy consistente:

```bash
# Executar vLLM em Docker
docker run --gpus all -p 8000:8000 \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --enable-prefix-caching
```

**Etapa 5: Verificar métricas de desempenho**

Confirme se o deploy atinge os objetivos:
- TTFT < 500ms (para prompts curtos)
- Throughput > target req/sec
- Utilização GPU > 80%
- Sem erros OOM nos logs

### Workflow 2: Inferência em lote offline

Para processar grandes conjuntos de dados sem overhead de servidor.

Copie este checklist:

```
Processamento em Lote:
- [ ] Etapa 1: Preparar dados de entrada
- [ ] Etapa 2: Configurar engine LLM
- [ ] Etapa 3: Executar inferência em lote
- [ ] Etapa 4: Processar resultados
```

**Etapa 1: Preparar dados de entrada**

```python
# Carregar prompts de arquivo
prompts = []
with open("prompts.txt") as f:
    prompts = [line.strip() for line in f]

print(f"Loaded {len(prompts)} prompts")
```

**Etapa 2: Configurar engine LLM**

```python
from vllm import LLM, SamplingParams

llm = LLM(
    model="meta-llama/Llama-3-8B-Instruct",
    tensor_parallel_size=2,  # Use 2 GPUs
    gpu_memory_utilization=0.9,
    max_model_len=4096
)

sampling = SamplingParams(
    temperature=0.7,
    top_p=0.95,
    max_tokens=512,
    stop=["</s>", "\n\n"]
)
```

**Etapa 3: Executar inferência em lote**

vLLM agrupa automaticamente requisições para eficiência:

```python
# Processar todos os prompts em uma chamada
outputs = llm.generate(prompts, sampling)

# vLLM lida com batching internamente
# Sem necessidade de chunking manual de prompts
```

**Etapa 4: Processar resultados**

```python
# Extrair texto gerado
results = []
for output in outputs:
    prompt = output.prompt
    generated = output.outputs[0].text
    results.append({
        "prompt": prompt,
        "generated": generated,
        "tokens": len(output.outputs[0].token_ids)
    })

# Salvar em arquivo
import json
with open("results.jsonl", "w") as f:
    for result in results:
        f.write(json.dumps(result) + "\n")

print(f"Processed {len(results)} prompts")
```

### Workflow 3: Serving de modelo quantizado

Encaixar modelos grandes em memória GPU limitada.

```
Setup de Quantização:
- [ ] Etapa 1: Escolher método de quantização
- [ ] Etapa 2: Encontrar ou criar modelo quantizado
- [ ] Etapa 3: Lançar com flag de quantização
- [ ] Etapa 4: Verificar acurácia
```

**Etapa 1: Escolher método de quantização**

- **AWQ**: Melhor para modelos 70B, perda mínima de acurácia
- **GPTQ**: Amplo suporte a modelos, boa compressão
- **FP8**: Mais rápido em GPUs H100

**Etapa 2: Encontrar ou criar modelo quantizado**

Use modelos pré-quantizados do HuggingFace:

```bash
# Buscar modelos AWQ
# Exemplo: TheBloke/Llama-2-70B-AWQ
```

**Etapa 3: Lançar com flag de quantização**

```bash
# Usando modelo pré-quantizado
vllm serve TheBloke/Llama-2-70B-AWQ \
  --quantization awq \
  --tensor-parallel-size 1 \
  --gpu-memory-utilization 0.95

# Resultado: modelo 70B em ~40GB VRAM
```

**Etapa 4: Verificar acurácia**

Teste se saídas correspondem à qualidade esperada:

```python
# Comparar respostas quantizadas vs não-quantizadas
# Verificar desempenho específico da tarefa inalterado
```

## Quando usar vs alternativas

**Use vLLM quando:**
- Deployar APIs LLM em produção (100+ req/sec)
- Servir endpoints compatíveis com OpenAI
- Memória GPU limitada mas precisa de modelos grandes
- Aplicações multi-usuário (chatbots, assistentes)
- Precisar de baixa latência com alto throughput

**Use alternativas no lugar:**
- **llama.cpp**: Inferência em CPU/edge, single-user
- **HuggingFace transformers**: Pesquisa, prototipagem, geração pontual
- **TensorRT-LLM**: Apenas NVIDIA, precisa máximo absoluto de desempenho
- **Text-Generation-Inference**: Já está no ecossistema HuggingFace

## Problemas comuns

**Problema: Out of memory durante carregamento do modelo**

Reduza uso de memória:
```bash
vllm serve MODEL \
  --gpu-memory-utilization 0.7 \
  --max-model-len 4096
```

Ou use quantização:
```bash
vllm serve MODEL --quantization awq
```

**Problema: Primeiro token lento (TTFT > 1 segundo)**

Ative prefix caching para prompts repetidos:
```bash
vllm serve MODEL --enable-prefix-caching
```

Para prompts longos, ative chunked prefill:
```bash
vllm serve MODEL --enable-chunked-prefill
```

**Problema: Erro de modelo não encontrado**

Use `--trust-remote-code` para modelos customizados:
```bash
vllm serve MODEL --trust-remote-code
```

**Problema: Baixo throughput (<50 req/sec)**

Aumente sequências concorrentes:
```bash
vllm serve MODEL --max-num-seqs 512
```

Verifique utilização GPU com `nvidia-smi` - deve ser >80%.

**Problema: Inferência mais lenta do que esperado**

Verifique se tensor parallelism usa potência de 2 GPUs:
```bash
vllm serve MODEL --tensor-parallel-size 4  # Não 3
```

Ative speculative decoding para geração mais rápida:
```bash
vllm serve MODEL --speculative-model DRAFT_MODEL
```

## Tópicos avançados

**Padrões de deploy do servidor**: Veja [references/server-deployment.md](references/server-deployment.md) para configurações Docker, Kubernetes e load balancing.

**Otimização de desempenho**: Veja [references/optimization.md](references/optimization.md) para ajuste de PagedAttention, detalhes de continuous batching e resultados de benchmark.

**Guia de quantização**: Veja [references/quantization.md](references/quantization.md) para setup de AWQ/GPTQ/FP8, preparação de modelos e comparações de acurácia.

**Troubleshooting**: Veja [references/troubleshooting.md](references/troubleshooting.md) para mensagens de erro detalhadas, passos de debug e diagnósticos de desempenho.

## Requisitos de hardware

- **Modelos pequenos (7B-13B)**: 1x A10 (24GB) ou A100 (40GB)
- **Modelos médios (30B-40B)**: 2x A100 (40GB) com tensor parallelism
- **Modelos grandes (70B+)**: 4x A100 (40GB) ou 2x A100 (80GB), use AWQ/GPTQ

Plataformas suportadas: NVIDIA (primária), AMD ROCm, Intel GPUs, TPUs

## Recursos

- Documentação oficial: https://docs.vllm.ai
- GitHub: https://github.com/vllm-project/vllm
- Paper: "Efficient Memory Management for Large Language Model Serving with PagedAttention" (SOSP 2023)
- Comunidade: https://discuss.vllm.ai