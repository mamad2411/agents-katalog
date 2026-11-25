---
name: guidance
description: Controle saída de LLM com regex e gramáticas, garanta geração válida de JSON/XML/código, aplique formatos estruturados e construa fluxos de trabalho multi-etapas com Guidance - framework de geração restrita da Microsoft Research
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Prompt Engineering, Guidance, Constrained Generation, Structured Output, JSON Validation, Grammar, Microsoft Research, Format Enforcement, Multi-Step Workflows]
dependencies: [guidance, transformers]
---

# Guidance: Geração de LLM Restrita

## Quando Usar Esta Skill

Use Guidance quando você precisar:
- **Controlar a sintaxe da saída do LLM** com regex ou gramáticas
- **Garantir geração válida de JSON/XML/código**
- **Reduzir latência** em comparação com abordagens de prompting tradicional
- **Aplicar formatos estruturados** (datas, emails, IDs, etc.)
- **Construir fluxos de trabalho multi-etapas** com controle de fluxo Pythônico
- **Prevenir saídas inválidas** através de restrições gramaticais

**GitHub Stars**: 18.000+ | **De**: Microsoft Research

## Instalação

```bash
# Instalação base
pip install guidance

# Com backends específicos
pip install guidance[transformers]  # Modelos Hugging Face
pip install guidance[llama_cpp]     # Modelos llama.cpp
```

## Início Rápido

### Exemplo Básico: Geração Estruturada

```python
from guidance import models, gen

# Carrega modelo (suporta OpenAI, Transformers, llama.cpp)
lm = models.OpenAI("gpt-4")

# Gera com restrições
result = lm + "The capital of France is " + gen("capital", max_tokens=5)

print(result["capital"])  # "Paris"
```

### Com Anthropic Claude

```python
from guidance import models, gen, system, user, assistant

# Configura Claude
lm = models.Anthropic("claude-sonnet-4-5-20250929")

# Usa context managers para formato de chat
with system():
    lm += "You are a helpful assistant."

with user():
    lm += "What is the capital of France?"

with assistant():
    lm += gen(max_tokens=20)
```

## Conceitos Principais

### 1. Context Managers

Guidance usa context managers Pythônicos para interações em estilo chat.

```python
from guidance import system, user, assistant, gen

lm = models.Anthropic("claude-sonnet-4-5-20250929")

# Mensagem de sistema
with system():
    lm += "You are a JSON generation expert."

# Mensagem do usuário
with user():
    lm += "Generate a person object with name and age."

# Resposta do assistente
with assistant():
    lm += gen("response", max_tokens=100)

print(lm["response"])
```

**Benefícios:**
- Fluxo de chat natural
- Separação clara de papéis
- Fácil de ler e manter

### 2. Geração Restrita

Guidance garante que as saídas correspondam a padrões especificados usando regex ou gramáticas.

#### Restrições com Regex

```python
from guidance import models, gen

lm = models.Anthropic("claude-sonnet-4-5-20250929")

# Restringe para formato de email válido
lm += "Email: " + gen("email", regex=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Restringe para formato de data (YYYY-MM-DD)
lm += "Date: " + gen("date", regex=r"\d{4}-\d{2}-\d{2}")

# Restringe para número de telefone
lm += "Phone: " + gen("phone", regex=r"\d{3}-\d{3}-\d{4}")

print(lm["email"])  # Email válido garantido
print(lm["date"])   # Formato YYYY-MM-DD garantido
```

**Como funciona:**
- Regex convertido para gramática no nível de token
- Tokens inválidos filtrados durante geração
- Modelo pode produzir apenas saídas correspondentes

#### Restrições de Seleção

```python
from guidance import models, gen, select

lm = models.Anthropic("claude-sonnet-4-5-20250929")

# Restringe a escolhas específicas
lm += "Sentiment: " + select(["positive", "negative", "neutral"], name="sentiment")

# Seleção de múltipla escolha
lm += "Best answer: " + select(
    ["A) Paris", "B) London", "C) Berlin", "D) Madrid"],
    name="answer"
)

print(lm["sentiment"])  # Uma de: positive, negative, neutral
print(lm["answer"])     # Uma de: A, B, C ou D
```

### 3. Token Healing

Guidance "corrige" automaticamente os limites de token entre o prompt e a geração.

**Problema:** Tokenização cria limites não naturais.

```python
# Sem token healing
prompt = "The capital of France is "
# Último token: " is "
# Primeiro token gerado pode ser " Par" (com espaço inicial)
# Resultado: "The capital of France is  Paris" (espaço duplo!)
```

**Solução:** Guidance volta um token e regenera.

```python
from guidance import models, gen

lm = models.Anthropic("claude-sonnet-4-5-20250929")

# Token healing ativado por padrão
lm += "The capital of France is " + gen("capital", max_tokens=5)
# Resultado: "The capital of France is Paris" (espaçamento correto)
```

**Benefícios:**
- Limites de texto naturais
- Sem problemas de espaçamento estranho
- Melhor desempenho do modelo (vê sequências de token naturais)

### 4. Geração Baseada em Gramática

Define estruturas complexas usando gramáticas livres de contexto.

```python
from guidance import models, gen

lm = models.Anthropic("claude-sonnet-4-5-20250929")

# Gramática JSON (simplificada)
json_grammar = """
{
    "name": <gen name regex="[A-Za-z ]+" max_tokens=20>,
    "age": <gen age regex="[0-9]+" max_tokens=3>,
    "email": <gen email regex="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}" max_tokens=50>
}
"""

# Gera JSON válido
lm += gen("person", grammar=json_grammar)

print(lm["person"])  # Estrutura JSON válida garantida
```

**Casos de uso:**
- Saídas estruturadas complexas
- Estruturas de dados aninhadas
- Sintaxe de linguagem de programação
- Linguagens específicas de domínio

### 5. Funções Guidance

Crie padrões de geração reutilizáveis com o decorador `@guidance`.

```python
from guidance import guidance, gen, models

@guidance
def generate_person(lm):
    """Gera uma pessoa com nome e idade."""
    lm += "Name: " + gen("name", max_tokens=20, stop="\n")
    lm += "\nAge: " + gen("age", regex=r"[0-9]+", max_tokens=3)
    return lm

# Usa a função
lm = models.Anthropic("claude-sonnet-4-5-20250929")
lm = generate_person(lm)

print(lm["name"])
print(lm["age"])
```

**Funções Stateful:**

```python
@guidance(stateless=False)
def react_agent(lm, question, tools, max_rounds=5):
    """Agente ReAct com uso de ferramentas."""
    lm += f"Question: {question}\n\n"

    for i in range(max_rounds):
        # Pensamento
        lm += f"Thought {i+1}: " + gen("thought", stop="\n")

        # Ação
        lm += "\nAction: " + select(list(tools.keys()), name="action")

        # Executa ferramenta
        tool_result = tools[lm["action"]]()
        lm += f"\nObservation: {tool_result}\n\n"

        # Verifica se concluído
        lm += "Done? " + select(["Yes", "No"], name="done")
        if lm["done"] == "Yes":
            break

    # Resposta final
    lm += "\nFinal Answer: " + gen("answer", max_tokens=100)
    return lm
```

## Configuração de Backend

### Anthropic Claude

```python
from guidance import models

lm = models.Anthropic(
    model="claude-sonnet-4-5-20250929",
    api_key="your-api-key"  # Ou defina a variável de ambiente ANTHROPIC_API_KEY
)
```

### OpenAI

```python
lm = models.OpenAI(
    model="gpt-4o-mini",
    api_key="your-api-key"  # Ou defina a variável de ambiente OPENAI_API_KEY
)
```

### Modelos Locais (Transformers)

```python
from guidance.models import Transformers

lm = Transformers(
    "microsoft/Phi-4-mini-instruct",
    device="cuda"  # Ou "cpu"
)
```

### Modelos Locais (llama.cpp)

```python
from guidance.models import LlamaCpp

lm = LlamaCpp(
    model_path="/path/to/model.gguf",
    n_ctx=4096,
    n_gpu_layers=35
)
```

## Padrões Comuns

### Padrão 1: Geração de JSON

```python
from guidance import models, gen, system, user, assistant

lm = models.Anthropic("claude-sonnet-4-5-20250929")

with system():
    lm += "You generate valid JSON."

with user():
    lm += "Generate a user profile with name, age, and email."

with assistant():
    lm += """{
    "name": """ + gen("name", regex=r'"[A-Za-z ]+"', max_tokens=30) + """,
    "age": """ + gen("age", regex=r"[0-9]+", max_tokens=3) + """,
    "email": """ + gen("email", regex=r'"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"', max_tokens=50) + """
}"""

print(lm)  # JSON válido garantido
```

### Padrão 2: Classificação

```python
from guidance import models, gen, select

lm = models.Anthropic("claude-sonnet-4-5-20250929")

text = "This product is amazing! I love it."

lm += f"Text: {text}\n"
lm += "Sentiment: " + select(["positive", "negative", "neutral"], name="sentiment")
lm += "\nConfidence: " + gen("confidence", regex=r"[0-9]+", max_tokens=3) + "%"

print(f"Sentiment: {lm['sentiment']}")
print(f"Confidence: {lm['confidence']}%")
```

### Padrão 3: Raciocínio Multi-Etapas

```python
from guidance import models, gen, guidance

@guidance
def chain_of_thought(lm, question):
    """Gera resposta com raciocínio passo a passo."""
    lm += f"Question: {question}\n\n"

    # Gera múltiplas etapas de raciocínio
    for i in range(3):
        lm += f"Step {i+1}: " + gen(f"step_{i+1}", stop="\n", max_tokens=100) + "\n"

    # Resposta final
    lm += "\nTherefore, the answer is: " + gen("answer", max_tokens=50)

    return lm

lm = models.Anthropic("claude-sonnet-4-5-20250929")
lm = chain_of_thought(lm, "What is 15% of 200?")

print(lm["answer"])
```

### Padrão 4: Agente ReAct

```python
from guidance import models, gen, select, guidance

@guidance(stateless=False)
def react_agent(lm, question):
    """Agente ReAct com uso de ferramentas."""
    tools = {
        "calculator": lambda expr: eval(expr),
        "search": lambda query: f"Search results for: {query}",
    }

    lm += f"Question: {question}\n\n"

    for round in range(5):
        # Pensamento
        lm += f"Thought: " + gen("thought", stop="\n") + "\n"

        # Seleção de ação
        lm += "Action: " + select(["calculator", "search", "answer"], name="action")

        if lm["action"] == "answer":
            lm += "\nFinal Answer: " + gen("answer", max_tokens=100)
            break

        # Entrada de ação
        lm += "\nAction Input: " + gen("action_input", stop="\n") + "\n"

        # Executa ferramenta
        if lm["action"] in tools:
            result = tools[lm["action"]](lm["action_input"])
            lm += f"Observation: {result}\n\n"

    return lm

lm = models.Anthropic("claude-sonnet-4-5-20250929")
lm = react_agent(lm, "What is 25 * 4 + 10?")
print(lm["answer"])
```

### Padrão 5: Extração de Dados

```python
from guidance import models, gen, guidance

@guidance
def extract_entities(lm, text):
    """Extrai entidades estruturadas do texto."""
    lm += f"Text: {text}\n\n"

    # Extrai pessoa
    lm += "Person: " + gen("person", stop="\n", max_tokens=30) + "\n"

    # Extrai organização
    lm += "Organization: " + gen("organization", stop="\n", max_tokens=30) + "\n"

    # Extrai data
    lm += "Date: " + gen("date", regex=r"\d{4}-\d{2}-\d{2}", max_tokens=10) + "\n"

    # Extrai localização
    lm += "Location: " + gen("location", stop="\n", max_tokens=30) + "\n"

    return lm

text = "Tim Cook announced at Apple Park on 2024-09-15 in Cupertino."

lm = models.Anthropic("claude-sonnet-4-5-20250929")
lm = extract_entities(lm, text)

print(f"Person: {lm['person']}")
print(f"Organization: {lm['organization']}")
print(f"Date: {lm['date']}")
print(f"Location: {lm['location']}")
```

## Melhores Práticas

### 1. Use Regex para Validação de Formato

```python
# ✅ Bom: Regex garante formato válido
lm += "Email: " + gen("email", regex=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# ❌ Ruim: Geração livre pode produzir emails inválidos
lm += "Email: " + gen("email", max_tokens=50)
```

### 2. Use select() para Categorias Fixas

```python
# ✅ Bom: Categoria válida garantida
lm += "Status: " + select(["pending", "approved", "rejected"], name="status")

# ❌ Ruim: Pode gerar erros de digitação ou valores inválidos
lm += "Status: " + gen("status", max_tokens=20)
```

### 3. Aproveite Token Healing

```python
# Token healing é ativado por padrão
# Nenhuma ação especial necessária - apenas concatene naturalmente
lm += "The capital is " + gen("capital")  # Correção automática
```

### 4. Use Sequências de Parada

```python
# ✅ Bom: Para na quebra de linha para saídas de uma linha
lm += "Name: " + gen("name", stop="\n")

# ❌ Ruim: Pode gerar múltiplas linhas
lm += "Name: " + gen("name", max_tokens=50)
```

### 5. Crie Funções Reutilizáveis

```python
# ✅ Bom: Padrão reutilizável
@guidance
def generate_person(lm):
    lm += "Name: " + gen("name", stop="\n")
    lm += "\nAge: " + gen("age", regex=r"[0-9]+")
    return lm

# Use múltiplas vezes
lm = generate_person(lm)
lm += "\n\n"
lm = generate_person(lm)
```

### 6. Equilibre Restrições

```python
# ✅ Bom: Restrições razoáveis
lm += gen("name", regex=r"[A-Za-z ]+", max_tokens=30)

# ❌ Muito rígido: Pode falhar ou ser muito lento
lm += gen("name", regex=r"^(John|Jane)$", max_tokens=10)
```

## Comparação com Alternativas

| Feature | Guidance | Instructor | Outlines | LMQL |
|---------|----------|------------|----------|------|
| Restrições com Regex | ✅ Sim | ❌ Não | ✅ Sim | ✅ Sim |
| Suporte a Gramática | ✅ CFG | ❌ Não | ✅ CFG | ✅ CFG |
| Validação Pydantic | ❌ Não | ✅ Sim | ✅ Sim | ❌ Não |
| Token Healing | ✅ Sim | ❌ Não | ✅ Sim | ❌ Não |
| Modelos Locais | ✅ Sim | ⚠️ Limitado | ✅ Sim | ✅ Sim |
| Modelos API | ✅ Sim | ✅ Sim | ⚠️ Limitado | ✅ Sim |
| Sintaxe Pythônica | ✅ Sim | ✅ Sim | ✅ Sim | ❌ Tipo SQL |
| Curva de Aprendizado | Baixa | Baixa | Média | Alta |

**Quando escolher Guidance:**
- Precisa de restrições com regex/gramática
- Quer token healing
- Construindo fluxos de trabalho complexos com controle de fluxo
- Usando modelos locais (Transformers, llama.cpp)
- Prefere sintaxe Pythônica

**Quando escolher alternativas:**
- Instructor: Precisa de validação Pydantic com retry automático
- Outlines: Precisa de validação com JSON schema
- LMQL: Prefere sintaxe declarativa de query

## Características de Desempenho

**Redução de Latência:**
- 30-50% mais rápido que prompting tradicional para saídas restritas
- Token healing reduz regeneração desnecessária
- Restrições de gramática previnem geração de token inválido

**Uso de Memória:**
- Overhead mínimo vs geração sem restrição
- Compilação de gramática em cache após primeiro uso
- Filtragem eficiente de token em tempo de inferência

**Eficiência de Token:**
- Previne desperdício de tokens em saídas inválidas
- Sem necessidade de loops de retry
- Caminho direto para saídas válidas

## Recursos

- **Documentação**: https://guidance.readthedocs.io
- **GitHub**: https://github.com/guidance-ai/guidance (18k+ stars)
- **Notebooks**: https://github.com/guidance-ai/guidance/tree/main/notebooks
- **Discord**: Suporte comunitário disponível

## Veja Também

- `references/constraints.md` - Padrões abrangentes de regex e gramática
- `references/backends.md` - Configuração específica de backend
- `references/examples.md` - Exemplos prontos para produção