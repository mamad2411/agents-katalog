---
name: outlines
description: Garanta estrutura válida de JSON/XML/código durante a geração, use modelos Pydantic para outputs type-safe, suporte modelos locais (Transformers, vLLM) e maximize velocidade de inferência com Outlines - biblioteca de geração estruturada da dottxt.ai
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Prompt Engineering, Outlines, Structured Generation, JSON Schema, Pydantic, Local Models, Grammar-Based Generation, vLLM, Transformers, Type Safety]
dependencies: [outlines, transformers, vllm, pydantic]
---

# Outlines: Geração Estruturada de Texto

## Quando Usar Esta Skill

Use Outlines quando você precisa:
- **Garantir estrutura válida de JSON/XML/código** durante a geração
- **Usar modelos Pydantic** para outputs type-safe
- **Suportar modelos locais** (Transformers, llama.cpp, vLLM)
- **Maximizar velocidade de inferência** com geração estruturada sem overhead
- **Gerar contra JSON schemas** automaticamente
- **Controlar sampling de tokens** no nível de gramática

**Estrelas GitHub**: 8.000+ | **De**: dottxt.ai (antigo .txt)

## Instalação

```bash
# Instalação base
pip install outlines

# Com backends específicos
pip install outlines transformers  # Modelos Hugging Face
pip install outlines llama-cpp-python  # llama.cpp
pip install outlines vllm  # vLLM para alto throughput
```

## Início Rápido

### Exemplo Básico: Classificação

```python
import outlines
from typing import Literal

# Carregue o modelo
model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

# Gere com restrição de tipo
prompt = "Sentimento de 'This product is amazing!': "
generator = outlines.generate.choice(model, ["positive", "negative", "neutral"])
sentiment = generator(prompt)

print(sentiment)  # "positive" (garantido uma destas opções)
```

### Com Modelos Pydantic

```python
from pydantic import BaseModel
import outlines

class User(BaseModel):
    name: str
    age: int
    email: str

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

# Gere output estruturado
prompt = "Extract user: John Doe, 30 years old, john@example.com"
generator = outlines.generate.json(model, User)
user = generator(prompt)

print(user.name)   # "John Doe"
print(user.age)    # 30
print(user.email)  # "john@example.com"
```

## Conceitos Principais

### 1. Amostragem Constreita de Tokens

Outlines usa Máquinas de Estado Finito (FSM) para constranger a geração de tokens no nível de logit.

**Como funciona:**
1. Converta schema (JSON/Pydantic/regex) para gramática livre de contexto (CFG)
2. Transforme CFG em Máquina de Estado Finito (FSM)
3. Filtre tokens inválidos em cada passo durante a geração
4. Avance rapidamente quando apenas um token válido existe

**Benefícios:**
- **Sem overhead**: Filtragem acontece no nível de token
- **Melhoria de velocidade**: Avance rapidamente através de caminhos determinísticos
- **Validade garantida**: Outputs inválidos impossíveis

```python
import outlines

# Modelo Pydantic -> JSON schema -> CFG -> FSM
class Person(BaseModel):
    name: str
    age: int

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

# Nos bastidores:
# 1. Person -> JSON schema
# 2. JSON schema -> CFG
# 3. CFG -> FSM
# 4. FSM filtra tokens durante a geração

generator = outlines.generate.json(model, Person)
result = generator("Generate person: Alice, 25")
```

### 2. Geradores Estruturados

Outlines oferece geradores especializados para diferentes tipos de output.

#### Gerador de Escolha

```python
# Seleção de múltipla escolha
generator = outlines.generate.choice(
    model,
    ["positive", "negative", "neutral"]
)

sentiment = generator("Review: This is great!")
# Resultado: Uma das três opções
```

#### Gerador JSON

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

# Gere JSON válido correspondente ao schema
generator = outlines.generate.json(model, Product)
product = generator("Extract: iPhone 15, $999, available")

# Instância Product válida garantida
print(type(product))  # <class '__main__.Product'>
```

#### Gerador Regex

```python
# Gere texto correspondente a regex
generator = outlines.generate.regex(
    model,
    r"[0-9]{3}-[0-9]{3}-[0-9]{4}"  # Padrão de número telefônico
)

phone = generator("Generate phone number:")
# Resultado: "555-123-4567" (garantido corresponder ao padrão)
```

#### Geradores Inteiro/Float

```python
# Gere tipos numéricos específicos
int_generator = outlines.generate.integer(model)
age = int_generator("Person's age:")  # Inteiro garantido

float_generator = outlines.generate.float(model)
price = float_generator("Product price:")  # Float garantido
```

### 3. Backends de Modelo

Outlines suporta múltiplos backends locais e baseados em API.

#### Transformers (Hugging Face)

```python
import outlines

# Carregue do Hugging Face
model = outlines.models.transformers(
    "microsoft/Phi-3-mini-4k-instruct",
    device="cuda"  # Ou "cpu"
)

# Use com qualquer gerador
generator = outlines.generate.json(model, YourModel)
```

#### llama.cpp

```python
# Carregue modelo GGUF
model = outlines.models.llamacpp(
    "./models/llama-3.1-8b-instruct.Q4_K_M.gguf",
    n_gpu_layers=35
)

generator = outlines.generate.json(model, YourModel)
```

#### vLLM (Alto Throughput)

```python
# Para deployments em produção
model = outlines.models.vllm(
    "meta-llama/Llama-3.1-8B-Instruct",
    tensor_parallel_size=2  # Multi-GPU
)

generator = outlines.generate.json(model, YourModel)
```

#### OpenAI (Suporte Limitado)

```python
# Suporte básico OpenAI
model = outlines.models.openai(
    "gpt-4o-mini",
    api_key="your-api-key"
)

# Nota: Alguns recursos limitados com modelos de API
generator = outlines.generate.json(model, YourModel)
```

### 4. Integração Pydantic

Outlines tem suporte de primeira classe a Pydantic com tradução automática de schema.

#### Modelos Básicos

```python
from pydantic import BaseModel, Field

class Article(BaseModel):
    title: str = Field(description="Título do artigo")
    author: str = Field(description="Nome do autor")
    word_count: int = Field(description="Número de palavras", gt=0)
    tags: list[str] = Field(description="Lista de tags")

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, Article)

article = generator("Generate article about AI")
print(article.title)
print(article.word_count)  # Garantido > 0
```

#### Modelos Aninhados

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class Person(BaseModel):
    name: str
    age: int
    address: Address  # Modelo aninhado

generator = outlines.generate.json(model, Person)
person = generator("Generate person in New York")

print(person.address.city)  # "New York"
```

#### Enums e Literals

```python
from enum import Enum
from typing import Literal

class Status(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Application(BaseModel):
    applicant: str
    status: Status  # Deve ser um dos valores de enum
    priority: Literal["low", "medium", "high"]  # Deve ser um dos literals

generator = outlines.generate.json(model, Application)
app = generator("Generate application")

print(app.status)  # Status.PENDING (ou APPROVED/REJECTED)
```

## Padrões Comuns

### Padrão 1: Extração de Dados

```python
from pydantic import BaseModel
import outlines

class CompanyInfo(BaseModel):
    name: str
    founded_year: int
    industry: str
    employees: int

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, CompanyInfo)

text = """
Apple Inc. was founded in 1976 in the technology industry.
The company employs approximately 164,000 people worldwide.
"""

prompt = f"Extract company information:\n{text}\n\nCompany:"
company = generator(prompt)

print(f"Name: {company.name}")
print(f"Founded: {company.founded_year}")
print(f"Industry: {company.industry}")
print(f"Employees: {company.employees}")
```

### Padrão 2: Classificação

```python
from typing import Literal
import outlines

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

# Classificação binária
generator = outlines.generate.choice(model, ["spam", "not_spam"])
result = generator("Email: Buy now! 50% off!")

# Classificação multiclasse
categories = ["technology", "business", "sports", "entertainment"]
category_gen = outlines.generate.choice(model, categories)
category = category_gen("Article: Apple announces new iPhone...")

# Com confiança
class Classification(BaseModel):
    label: Literal["positive", "negative", "neutral"]
    confidence: float

classifier = outlines.generate.json(model, Classification)
result = classifier("Review: This product is okay, nothing special")
```

### Padrão 3: Formulários Estruturados

```python
class UserProfile(BaseModel):
    full_name: str
    age: int
    email: str
    phone: str
    country: str
    interests: list[str]

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, UserProfile)

prompt = """
Extract user profile from:
Name: Alice Johnson
Age: 28
Email: alice@example.com
Phone: 555-0123
Country: USA
Interests: hiking, photography, cooking
"""

profile = generator(prompt)
print(profile.full_name)
print(profile.interests)  # ["hiking", "photography", "cooking"]
```

### Padrão 4: Extração Multi-Entidade

```python
class Entity(BaseModel):
    name: str
    type: Literal["PERSON", "ORGANIZATION", "LOCATION"]

class DocumentEntities(BaseModel):
    entities: list[Entity]

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, DocumentEntities)

text = "Tim Cook met with Satya Nadella at Microsoft headquarters in Redmond."
prompt = f"Extract entities from: {text}"

result = generator(prompt)
for entity in result.entities:
    print(f"{entity.name} ({entity.type})")
```

### Padrão 5: Geração de Código

```python
class PythonFunction(BaseModel):
    function_name: str
    parameters: list[str]
    docstring: str
    body: str

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, PythonFunction)

prompt = "Generate a Python function to calculate factorial"
func = generator(prompt)

print(f"def {func.function_name}({', '.join(func.parameters)}):")
print(f'    """{func.docstring}"""')
print(f"    {func.body}")
```

### Padrão 6: Processamento em Lote

```python
def batch_extract(texts: list[str], schema: type[BaseModel]):
    """Extraia dados estruturados de múltiplos textos."""
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
    generator = outlines.generate.json(model, schema)

    results = []
    for text in texts:
        result = generator(f"Extract from: {text}")
        results.append(result)

    return results

class Person(BaseModel):
    name: str
    age: int

texts = [
    "John is 30 years old",
    "Alice is 25 years old",
    "Bob is 40 years old"
]

people = batch_extract(texts, Person)
for person in people:
    print(f"{person.name}: {person.age}")
```

## Configuração de Backend

### Transformers

```python
import outlines

# Uso básico
model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

# Configuração GPU
model = outlines.models.transformers(
    "microsoft/Phi-3-mini-4k-instruct",
    device="cuda",
    model_kwargs={"torch_dtype": "float16"}
)

# Modelos populares
model = outlines.models.transformers("meta-llama/Llama-3.1-8B-Instruct")
model = outlines.models.transformers("mistralai/Mistral-7B-Instruct-v0.3")
model = outlines.models.transformers("Qwen/Qwen2.5-7B-Instruct")
```

### llama.cpp

```python
# Carregue modelo GGUF
model = outlines.models.llamacpp(
    "./models/llama-3.1-8b.Q4_K_M.gguf",
    n_ctx=4096,         # Janela de contexto
    n_gpu_layers=35,    # Camadas GPU
    n_threads=8         # Threads CPU
)

# Offload total para GPU
model = outlines.models.llamacpp(
    "./models/model.gguf",
    n_gpu_layers=-1  # Todas as camadas na GPU
)
```

### vLLM (Produção)

```python
# Single GPU
model = outlines.models.vllm("meta-llama/Llama-3.1-8B-Instruct")

# Multi-GPU
model = outlines.models.vllm(
    "meta-llama/Llama-3.1-70B-Instruct",
    tensor_parallel_size=4  # 4 GPUs
)

# Com quantização
model = outlines.models.vllm(
    "meta-llama/Llama-3.1-8B-Instruct",
    quantization="awq"  # Ou "gptq"
)
```

## Melhores Práticas

### 1. Use Tipos Específicos

```python
# ✅ Bom: Tipos específicos
class Product(BaseModel):
    name: str
    price: float  # Não str
    quantity: int  # Não str
    in_stock: bool  # Não str

# ❌ Ruim: Tudo como string
class Product(BaseModel):
    name: str
    price: str  # Deveria ser float
    quantity: str  # Deveria ser int
```

### 2. Adicione Restrições

```python
from pydantic import Field

# ✅ Bom: Com restrições
class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=120)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

# ❌ Ruim: Sem restrições
class User(BaseModel):
    name: str
    age: int
    email: str
```

### 3. Use Enums para Categorias

```python
# ✅ Bom: Enum para conjunto fixo
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str
    priority: Priority

# ❌ Ruim: String livre
class Task(BaseModel):
    title: str
    priority: str  # Pode ser qualquer coisa
```

### 4. Forneça Contexto em Prompts

```python
# ✅ Bom: Contexto claro
prompt = """
Extract product information from the following text.
Text: iPhone 15 Pro costs $999 and is currently in stock.
Product:
"""

# ❌ Ruim: Contexto mínimo
prompt = "iPhone 15 Pro costs $999 and is currently in stock."
```

### 5. Trate Campos Opcionais

```python
from typing import Optional

# ✅ Bom: Campos opcionais para dados incompletos
class Article(BaseModel):
    title: str  # Obrigatório
    author: Optional[str] = None  # Opcional
    date: Optional[str] = None  # Opcional
    tags: list[str] = []  # Lista vazia padrão

# Pode ter sucesso mesmo se author/date ausentes
```

## Comparação com Alternativas

| Recurso | Outlines | Instructor | Guidance | LMQL |
|---------|----------|------------|----------|------|
| Suporte Pydantic | ✅ Nativo | ✅ Nativo | ❌ Não | ❌ Não |
| JSON Schema | ✅ Sim | ✅ Sim | ⚠️ Limitado | ✅ Sim |
| Restrições Regex | ✅ Sim | ❌ Não | ✅ Sim | ✅ Sim |
| Modelos Locais | ✅ Total | ⚠️ Limitado | ✅ Total | ✅ Total |
| Modelos de API | ⚠️ Limitado | ✅ Total | ✅ Total | ✅ Total |
| Sem Overhead | ✅ Sim | ❌ Não | ⚠️ Parcial | ✅ Sim |
| Retry Automático | ❌ Não | ✅ Sim | ❌ Não | ❌ Não |
| Curva de Aprendizado | Baixa | Baixa | Baixa | Alta |

**Quando escolher Outlines:**
- Usando modelos locais (Transformers, llama.cpp, vLLM)
- Precisa de velocidade máxima de inferência
- Quer suporte a modelo Pydantic
- Requer geração estruturada sem overhead
- Controle do processo de sampling de tokens

**Quando escolher alternativas:**
- Instructor: Precisa de modelos de API com retry automático
- Guidance: Precisa de token healing e workflows complexos
- LMQL: Prefere sintaxe de query declarativa

## Características de Performance

**Velocidade:**
- **Sem overhead**: Geração estruturada tão rápida quanto não constrita
- **Otimização de avanço rápido**: Pula tokens determinísticos
- **1.2-2x mais rápido** do que abordagens de validação pós-geração

**Memória:**
- FSM compilado uma vez por schema (cacheado)
- Overhead de runtime mínimo
- Eficiente com vLLM para alto throughput

**Precisão:**
- **100% de outputs válidos** (garantido por FSM)
- Nenhum loop de retry necessário
- Filtragem de token determinística

## Recursos

- **Documentação**: https://outlines-dev.github.io/outlines
- **GitHub**: https://github.com/outlines-dev/outlines (8k+ stars)
- **Discord**: https://discord.gg/R9DSu34mGd
- **Blog**: https://blog.dottxt.co

## Veja Também

- `references/json_generation.md` - Padrões abrangentes de JSON e Pydantic
- `references/backends.md` - Configuração específica de backend
- `references/examples.md` - Exemplos prontos para produção