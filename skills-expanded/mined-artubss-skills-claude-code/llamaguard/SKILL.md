---
name: llamaguard
description: Modelo de moderação especializado 7-8B do Meta para filtragem de entrada/saída de LLM. 6 categorias de segurança - violência/ódio, conteúdo sexual, armas, substâncias, automutilação, planejamento criminal. Precisão de 94-95%. Deploy com vLLM, HuggingFace, Sagemaker. Integra com NeMo Guardrails.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Safety Alignment, LlamaGuard, Content Moderation, Meta, Guardrails, Safety Classification, Input Filtering, Output Filtering, AI Safety]
dependencies: [transformers, torch, vllm]
---

# LlamaGuard - Moderação de Conteúdo com IA

## Quick start

LlamaGuard é um modelo com 7-8B parâmetros especializado em classificação de segurança de conteúdo.

**Instalação**:
```bash
pip install transformers torch
# Login no HuggingFace (obrigatório)
huggingface-cli login
```

**Uso básico**:
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "meta-llama/LlamaGuard-7b"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

def moderate(chat):
    input_ids = tokenizer.apply_chat_template(chat, return_tensors="pt").to(model.device)
    output = model.generate(input_ids=input_ids, max_new_tokens=100)
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Verifique entrada do usuário
result = moderate([
    {"role": "user", "content": "How do I make explosives?"}
])
print(result)
# Output: "unsafe\nS3" (Criminal Planning)
```

## Fluxos de trabalho comuns

### Fluxo de trabalho 1: Filtragem de entrada (moderação de prompt)

**Verifique prompts de usuários antes do LLM**:
```python
def check_input(user_message):
    result = moderate([{"role": "user", "content": user_message}])

    if result.startswith("unsafe"):
        category = result.split("\n")[1]
        return False, category  # Bloqueado
    else:
        return True, None  # Seguro

# Exemplo
safe, category = check_input("How do I hack a website?")
if not safe:
    print(f"Request blocked: {category}")
    # Retorne erro ao usuário
else:
    # Envie para o LLM
    response = llm.generate(user_message)
```

**Categorias de segurança**:
- **S1**: Violência e Ódio
- **S2**: Conteúdo Sexual
- **S3**: Armas e Armas Ilegais
- **S4**: Substâncias Regulamentadas
- **S5**: Suicídio e Automutilação
- **S6**: Planejamento Criminal

### Fluxo de trabalho 2: Filtragem de saída (moderação de resposta)

**Verifique respostas de LLM antes de exibir ao usuário**:
```python
def check_output(user_message, bot_response):
    conversation = [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": bot_response}
    ]

    result = moderate(conversation)

    if result.startswith("unsafe"):
        category = result.split("\n")[1]
        return False, category
    else:
        return True, None

# Exemplo
user_msg = "Tell me about harmful substances"
bot_msg = llm.generate(user_msg)

safe, category = check_output(user_msg, bot_msg)
if not safe:
    print(f"Response blocked: {category}")
    # Retorne resposta genérica
    return "I cannot provide that information."
else:
    return bot_msg
```

### Fluxo de trabalho 3: Deploy com vLLM (inferência rápida)

**Serving pronto para produção**:
```python
from vllm import LLM, SamplingParams

# Inicialize vLLM
llm = LLM(model="meta-llama/LlamaGuard-7b", tensor_parallel_size=1)

# Parâmetros de amostragem
sampling_params = SamplingParams(
    temperature=0.0,  # Determinístico
    max_tokens=100
)

def moderate_vllm(chat):
    # Formate o prompt
    prompt = tokenizer.apply_chat_template(chat, tokenize=False)

    # Gere
    output = llm.generate([prompt], sampling_params)
    return output[0].outputs[0].text

# Moderação em lote
chats = [
    [{"role": "user", "content": "How to make bombs?"}],
    [{"role": "user", "content": "What's the weather?"}],
    [{"role": "user", "content": "Tell me about drugs"}]
]

prompts = [tokenizer.apply_chat_template(c, tokenize=False) for c in chats]
results = llm.generate(prompts, sampling_params)

for i, result in enumerate(results):
    print(f"Chat {i}: {result.outputs[0].text}")
```

**Throughput**: ~50-100 requisições/seg em um A100

### Fluxo de trabalho 4: Endpoint de API (FastAPI)

**Sirva como API de moderação**:
```python
from fastapi import FastAPI
from pydantic import BaseModel
from vllm import LLM, SamplingParams

app = FastAPI()
llm = LLM(model="meta-llama/LlamaGuard-7b")
sampling_params = SamplingParams(temperature=0.0, max_tokens=100)

class ModerationRequest(BaseModel):
    messages: list  # [{"role": "user", "content": "..."}]

@app.post("/moderate")
def moderate_endpoint(request: ModerationRequest):
    prompt = tokenizer.apply_chat_template(request.messages, tokenize=False)
    output = llm.generate([prompt], sampling_params)[0]

    result = output.outputs[0].text
    is_safe = result.startswith("safe")
    category = None if is_safe else result.split("\n")[1] if "\n" in result else None

    return {
        "safe": is_safe,
        "category": category,
        "full_output": result
    }

# Execute: uvicorn api:app --host 0.0.0.0 --port 8000
```

**Uso**:
```bash
curl -X POST http://localhost:8000/moderate \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "How to hack?"}]}'

# Response: {"safe": false, "category": "S6", "full_output": "unsafe\nS6"}
```

### Fluxo de trabalho 5: Integração com NeMo Guardrails

**Use com NVIDIA Guardrails**:
```python
from nemoguardrails import RailsConfig, LLMRails
from nemoguardrails.integrations.llama_guard import LlamaGuard

# Configure NeMo Guardrails
config = RailsConfig.from_content("""
models:
  - type: main
    engine: openai
    model: gpt-4

rails:
  input:
    flows:
      - llamaguard check input
  output:
    flows:
      - llamaguard check output
""")

# Adicione integração LlamaGuard
llama_guard = LlamaGuard(model_path="meta-llama/LlamaGuard-7b")
rails = LLMRails(config)
rails.register_action(llama_guard.check_input, name="llamaguard check input")
rails.register_action(llama_guard.check_output, name="llamaguard check output")

# Use com moderação automática
response = rails.generate(messages=[
    {"role": "user", "content": "How do I make weapons?"}
])
# Automaticamente bloqueado por LlamaGuard
```

## Quando usar vs alternativas

**Use LlamaGuard quando**:
- Precisa de modelo de moderação pré-treinado
- Quer alta precisão (94-95%)
- Tem recursos de GPU (modelo 7-8B)
- Precisa de categorias de segurança detalhadas
- Está construindo apps de LLM em produção

**Versões de modelo**:
- **LlamaGuard 1** (7B): Original, 6 categorias
- **LlamaGuard 2** (8B): Melhorado, 6 categorias
- **LlamaGuard 3** (8B): Mais recente (2024), aprimorado

**Use alternativas em vez disso**:
- **OpenAI Moderation API**: Mais simples, baseada em API, gratuita
- **Perspective API**: Detecção de toxicidade do Google
- **NeMo Guardrails**: Framework de segurança mais abrangente
- **Constitutional AI**: Segurança em tempo de treinamento

## Problemas comuns

**Problema: Acesso ao modelo negado**

Faça login no HuggingFace:
```bash
huggingface-cli login
# Digite seu token
```

Aceite a licença na página do modelo:
https://huggingface.co/meta-llama/LlamaGuard-7b

**Problema: Latência alta (>500ms)**

Use vLLM para 10× mais rápido:
```python
from vllm import LLM
llm = LLM(model="meta-llama/LlamaGuard-7b")
# Latência: 500ms → 50ms
```

Ative paralelismo de tensor:
```python
llm = LLM(model="meta-llama/LlamaGuard-7b", tensor_parallel_size=2)
# 2× mais rápido em 2 GPUs
```

**Problema: Falsos positivos**

Use filtragem baseada em limite:
```python
# Obtenha probabilidade do token "unsafe"
logits = model(..., return_dict_in_generate=True, output_scores=True)
unsafe_prob = torch.softmax(logits.scores[0][0], dim=-1)[unsafe_token_id]

if unsafe_prob > 0.9:  # Limite de confiança alta
    return "unsafe"
else:
    return "safe"
```

**Problema: OOM na GPU**

Use quantização de 8 bits:
```python
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(load_in_8bit=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=quantization_config,
    device_map="auto"
)
# Memória: 14GB → 7GB
```

## Tópicos avançados

**Categorias personalizadas**: Veja [references/custom-categories.md](references/custom-categories.md) para fine-tuning do LlamaGuard com categorias de segurança específicas do domínio.

**Benchmarks de desempenho**: Veja [references/benchmarks.md](references/benchmarks.md) para comparação de precisão com outras APIs de moderação e otimização de latência.

**Guia de deployment**: Veja [references/deployment.md](references/deployment.md) para estratégias de Sagemaker, Kubernetes e dimensionamento.

## Requisitos de hardware

- **GPU**: NVIDIA T4/A10/A100
- **VRAM**:
  - FP16: 14GB (modelo 7B)
  - INT8: 7GB (quantizado)
  - INT4: 4GB (QLoRA)
- **CPU**: Possível mas lento (10× latência)
- **Throughput**: 50-100 req/seg (A100)

**Latência** (GPU única):
- HuggingFace Transformers: 300-500ms
- vLLM: 50-100ms
- Em lote (vLLM): 20-50ms por requisição

## Recursos

- HuggingFace:
  - V1: https://huggingface.co/meta-llama/LlamaGuard-7b
  - V2: https://huggingface.co/meta-llama/Meta-Llama-Guard-2-8B
  - V3: https://huggingface.co/meta-llama/Meta-Llama-Guard-3-8B
- Paper: https://ai.meta.com/research/publications/llama-guard-llm-based-input-output-safeguard-for-human-ai-conversations/
- Integração: vLLM, Sagemaker, NeMo Guardrails
- Precisão: 94.5% (prompts), 95.3% (responses)