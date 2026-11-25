---
name: sglang
description: Geração estruturada rápida e serving para LLMs com RadixAttention para cache de prefixos. Use para saídas JSON/regex, decodificação restrita, workflows com agentes que fazem chamadas de ferramentas, ou quando você precisa de 5× mais rápido que vLLM com compartilhamento de prefixos. Alimenta 300.000+ GPUs na xAI, AMD, NVIDIA e LinkedIn.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Inference Serving, SGLang, Structured Generation, RadixAttention, Prefix Caching, Constrained Decoding, Agents, JSON Output, Fast Inference, Production Scale]
dependencies: [sglang, torch, transformers]
---

# SGLang

Framework de serving de alto desempenho para LLMs e VLMs com RadixAttention para cache automático de prefixos.

## Quando usar SGLang

**Use SGLang quando:**
- Precisa de saídas estruturadas (JSON, regex, gramática)
- Construindo agentes com prefixos repetidos (prompts de sistema, ferramentas)
- Workflows com agentes e chamadas de funções
- Conversas com múltiplos turnos e contexto compartilhado
- Precisa de decodificação JSON mais rápida (3× vs padrão)

**Use vLLM em vez disso quando:**
- Geração de texto simples sem estrutura
- Não precisa de cache de prefixos
- Quer um sistema de produção maduro e amplamente testado

**Use TensorRT-LLM em vez disso quando:**
- Latência máxima de requisição única (sem batching necessário)
- Deploy apenas em NVIDIA
- Precisa de quantização FP8/INT4 em H100

## Início rápido

### Instalação

```bash
# pip install (recomendado)
pip install "sglang[all]"

# Com FlashInfer (mais rápido, CUDA 11.8/12.1)
pip install sglang[all] flashinfer -i https://flashinfer.ai/whl/cu121/torch2.4/

# Desde a fonte
git clone https://github.com/sgl-project/sglang.git
cd sglang
pip install -e "python[all]"
```

### Inicie o servidor

```bash
# Servidor básico (Llama 3-8B)
python -m sglang.launch_server \
    --model-path meta-llama/Meta-Llama-3-8B-Instruct \
    --port 30000

# Com RadixAttention (cache automático de prefixos)
python -m sglang.launch_server \
    --model-path meta-llama/Meta-Llama-3-8B-Instruct \
    --port 30000 \
    --enable-radix-cache  # Padrão: habilitado

# Multi-GPU (tensor parallelism)
python -m sglang.launch_server \
    --model-path meta-llama/Meta-Llama-3-70B-Instruct \
    --tp 4 \
    --port 30000
```

### Inferência básica

```python
import sglang as sgl

# Defina backend
sgl.set_default_backend(sgl.OpenAI("http://localhost:30000/v1"))

# Geração simples
@sgl.function
def simple_gen(s, question):
    s += "Q: " + question + "\n"
    s += "A:" + sgl.gen("answer", max_tokens=100)

# Execute
state = simple_gen.run(question="What is the capital of France?")
print(state["answer"])
# Output: "The capital of France is Paris."
```

### Saída JSON estruturada

```python
import sglang as sgl

@sgl.function
def extract_person(s, text):
    s += f"Extract person information from: {text}\n"
    s += "Output JSON:\n"

    # Geração JSON restrita
    s += sgl.gen(
        "json_output",
        max_tokens=200,
        regex=r'\{"name": "[^"]+", "age": \d+, "occupation": "[^"]+"\}'
    )

# Execute
state = extract_person.run(
    text="John Smith is a 35-year-old software engineer."
)
print(state["json_output"])
# Output: {"name": "John Smith", "age": 35, "occupation": "software engineer"}
```

## RadixAttention (Inovação Principal)

**O que faz**: Automaticamente faz cache e reutiliza prefixos comuns entre requisições.

**Desempenho**:
- **5× mais rápido** para workloads com agentes e prompts de sistema compartilhados
- **10× mais rápido** para few-shot prompting com exemplos repetidos
- **Zero configuração** - funciona automaticamente

**Como funciona**:
1. Constrói árvore radix de todos os tokens processados
2. Detecta automaticamente prefixos compartilhados
3. Reutiliza cache KV para prefixos correspondentes
4. Computa apenas novos tokens

**Exemplo** (Agente com prompt de sistema):

```
Requisição 1: [SYSTEM_PROMPT] + "What's the weather?"
→ Computa prompt completo (1000 tokens)

Requisição 2: [SAME_SYSTEM_PROMPT] + "Book a flight"
→ Reutiliza cache KV do prompt de sistema (998 tokens)
→ Computa apenas 2 novos tokens
→ 5× mais rápido!
```

## Padrões de geração estruturada

### JSON com schema

```python
@sgl.function
def structured_extraction(s, article):
    s += f"Article: {article}\n\n"
    s += "Extract key information as JSON:\n"

    # Constraint de schema JSON
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "author": {"type": "string"},
            "summary": {"type": "string"},
            "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]}
        },
        "required": ["title", "author", "summary", "sentiment"]
    }

    s += sgl.gen("info", max_tokens=300, json_schema=schema)

state = structured_extraction.run(article="...")
print(state["info"])
# Output: JSON válido correspondendo ao schema
```

### Geração restrita por regex

```python
@sgl.function
def extract_email(s, text):
    s += f"Extract email from: {text}\n"
    s += "Email: "

    # Padrão regex de email
    s += sgl.gen(
        "email",
        max_tokens=50,
        regex=r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    )

state = extract_email.run(text="Contact john.doe@example.com for details")
print(state["email"])
# Output: "john.doe@example.com"
```

### Geração baseada em gramática

```python
@sgl.function
def generate_code(s, description):
    s += f"Generate Python code for: {description}\n"
    s += "```python\n"

    # Gramática EBNF para Python
    python_grammar = """
    ?start: function_def
    function_def: "def" NAME "(" [parameters] "):" suite
    parameters: parameter ("," parameter)*
    parameter: NAME
    suite: simple_stmt | NEWLINE INDENT stmt+ DEDENT
    """

    s += sgl.gen("code", max_tokens=200, grammar=python_grammar)
    s += "\n```"
```

## Workflows com agentes e chamadas de funções

```python
import sglang as sgl

# Defina ferramentas
tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        }
    },
    {
        "name": "book_flight",
        "description": "Book a flight",
        "parameters": {
            "type": "object",
            "properties": {
                "from": {"type": "string"},
                "to": {"type": "string"},
                "date": {"type": "string"}
            }
        }
    }
]

@sgl.function
def agent_workflow(s, user_query, tools):
    # Prompt de sistema (cacheado com RadixAttention)
    s += "You are a helpful assistant with access to tools.\n"
    s += f"Available tools: {tools}\n\n"

    # Consulta do usuário
    s += f"User: {user_query}\n"
    s += "Assistant: "

    # Gere com function calling
    s += sgl.gen(
        "response",
        max_tokens=200,
        tools=tools,  # SGLang manipula o formato de chamadas de função
        stop=["User:", "\n\n"]
    )

# Múltiplas consultas reutilizam prompt de sistema
state1 = agent_workflow.run(
    user_query="What's the weather in NYC?",
    tools=tools
)
# Primeira chamada: Computa prompt de sistema completo

state2 = agent_workflow.run(
    user_query="Book a flight to LA",
    tools=tools
)
# Segunda chamada: Reutiliza prompt de sistema (5× mais rápido)
```

## Benchmarks de desempenho

### Speedup do RadixAttention

**Few-shot prompting** (10 exemplos no prompt):
- vLLM: 2.5 seg/requisição
- SGLang: **0.25 seg/requisição** (10× mais rápido)
- Throughput: 4× maior

**Workflows com agentes** (prompt de sistema com 1000 tokens):
- vLLM: 1.8 seg/requisição
- SGLang: **0.35 seg/requisição** (5× mais rápido)

**Decodificação JSON**:
- Padrão: 45 tok/s
- SGLang: **135 tok/s** (3× mais rápido)

### Throughput (Llama 3-8B, A100)

| Workload | vLLM | SGLang | Speedup |
|----------|------|--------|---------|
| Geração simples | 2500 tok/s | 2800 tok/s | 1.12× |
| Few-shot (10 exemplos) | 500 tok/s | 5000 tok/s | 10× |
| Agente (chamadas de ferramentas) | 800 tok/s | 4000 tok/s | 5× |
| Saída JSON | 600 tok/s | 2400 tok/s | 4× |

## Conversas com múltiplos turnos

```python
@sgl.function
def multi_turn_chat(s, history, new_message):
    # Prompt de sistema (sempre cacheado)
    s += "You are a helpful AI assistant.\n\n"

    # Histórico de conversa (cacheado conforme cresce)
    for msg in history:
        s += f"{msg['role']}: {msg['content']}\n"

    # Nova mensagem do usuário (apenas a nova parte)
    s += f"User: {new_message}\n"
    s += "Assistant: "
    s += sgl.gen("response", max_tokens=200)

# Turno 1
history = []
state = multi_turn_chat.run(history=history, new_message="Hi there!")
history.append({"role": "User", "content": "Hi there!"})
history.append({"role": "Assistant", "content": state["response"]})

# Turno 2 (reutiliza cache KV do Turno 1)
state = multi_turn_chat.run(history=history, new_message="What's 2+2?")
# Computa apenas a nova mensagem (muito mais rápido!)

# Turno 3 (reutiliza cache KV do Turno 1 + Turno 2)
state = multi_turn_chat.run(history=history, new_message="Tell me a joke")
# Progressivamente mais rápido conforme o histórico cresce
```

## Recursos avançados

### Decodificação especulativa

```bash
# Inicie com modelo draft (2-3× mais rápido)
python -m sglang.launch_server \
    --model-path meta-llama/Meta-Llama-3-70B-Instruct \
    --speculative-model meta-llama/Meta-Llama-3-8B-Instruct \
    --speculative-num-steps 5
```

### Multi-modal (modelos de visão)

```python
@sgl.function
def describe_image(s, image_path):
    s += sgl.image(image_path)
    s += "Describe this image in detail: "
    s += sgl.gen("description", max_tokens=200)

state = describe_image.run(image_path="photo.jpg")
print(state["description"])
```

### Batching e requisições paralelas

```python
# Batching automático (continuous batching)
states = sgl.run_batch(
    [
        simple_gen.bind(question="What is AI?"),
        simple_gen.bind(question="What is ML?"),
        simple_gen.bind(question="What is DL?"),
    ]
)

# Todos os 3 processados em um único batch (eficiente)
```

## API compatível com OpenAI

```bash
# Inicie servidor com API OpenAI
python -m sglang.launch_server \
    --model-path meta-llama/Meta-Llama-3-8B-Instruct \
    --port 30000

# Use com cliente OpenAI
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "default",
    "messages": [
      {"role": "system", "content": "You are helpful"},
      {"role": "user", "content": "Hello"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'

# Funciona com SDK Python do OpenAI
from openai import OpenAI
client = OpenAI(base_url="http://localhost:30000/v1", api_key="EMPTY")

response = client.chat.completions.create(
    model="default",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Modelos suportados

**Modelos de texto**:
- Llama 2, Llama 3, Llama 3.1, Llama 3.2
- Mistral, Mixtral
- Qwen, Qwen2, QwQ
- DeepSeek-V2, DeepSeek-V3
- Gemma, Phi-3

**Modelos de visão**:
- LLaVA, LLaVA-OneVision
- Phi-3-Vision
- Qwen2-VL

**100+ modelos** do HuggingFace

## Suporte a hardware

**NVIDIA**: A100, H100, L4, T4 (CUDA 11.8+)
**AMD**: MI300, MI250 (ROCm 6.0+)
**Intel**: Xeon com GPU (em breve)
**Apple**: M1/M2/M3 via MPS (experimental)

## Referências

- **[Guia de Geração Estruturada](references/structured-generation.md)** - Schemas JSON, regex, gramáticas, validação
- **[Mergulho Profundo em RadixAttention](references/radix-attention.md)** - Como funciona, otimização, benchmarks
- **[Deploy em Produção](references/deployment.md)** - Multi-GPU, monitoramento, autoscaling

## Recursos

- **GitHub**: https://github.com/sgl-project/sglang
- **Docs**: https://sgl-project.github.io/
- **Paper**: RadixAttention (arXiv:2312.07104)
- **Discord**: https://discord.gg/sglang