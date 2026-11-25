---
name: instructor
description: Extraia dados estruturados de respostas de LLM com validação Pydantic, tente novamente automaticamente extrações que falharem, analise JSON complexo com segurança de tipo e transmita resultados parciais com Instructor - biblioteca de saída estruturada testada em batalha
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Prompt Engineering, Instructor, Structured Output, Pydantic, Data Extraction, JSON Parsing, Type Safety, Validation, Streaming, OpenAI, Anthropic]
dependencies: [instructor, pydantic, openai, anthropic]
---

# Instructor: Saídas Estruturadas de LLM

## Quando Usar Esta Skill

Use Instructor quando você precisar:
- **Extrair dados estruturados** de respostas de LLM de forma confiável
- **Validar saídas** contra schemas Pydantic automaticamente
- **Tentar novamente extrações que falharem** com tratamento automático de erros
- **Analisar JSON complexo** com segurança de tipo e validação
- **Transmitir resultados parciais** para processamento em tempo real
- **Suportar múltiplos provedores de LLM** com API consistente

**Estrelas do GitHub**: 15.000+ | **Testado em batalha**: 100.000+ desenvolvedores

## Instalação

```bash
# Instalação base
pip install instructor

# Com provedores específicos
pip install "instructor[anthropic]"  # Anthropic Claude
pip install "instructor[openai]"     # OpenAI
pip install "instructor[all]"        # Todos os provedores
```

## Início Rápido

### Exemplo Básico: Extrair Dados de Usuário

```python
import instructor
from pydantic import BaseModel
from anthropic import Anthropic

# Defina a estrutura de saída
class User(BaseModel):
    name: str
    age: int
    email: str

# Crie um cliente instructor
client = instructor.from_anthropic(Anthropic())

# Extraia dados estruturados
user = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "John Doe is 30 years old. His email is john@example.com"
    }],
    response_model=User
)

print(user.name)   # "John Doe"
print(user.age)    # 30
print(user.email)  # "john@example.com"
```

### Com OpenAI

```python
from openai import OpenAI

client = instructor.from_openai(OpenAI())

user = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=User,
    messages=[{"role": "user", "content": "Extract: Alice, 25, alice@email.com"}]
)
```

## Conceitos Fundamentais

### 1. Response Models (Pydantic)

Response models definem a estrutura e as regras de validação para saídas de LLM.

#### Modelo Básico

```python
from pydantic import BaseModel, Field

class Article(BaseModel):
    title: str = Field(description="Article title")
    author: str = Field(description="Author name")
    word_count: int = Field(description="Number of words", gt=0)
    tags: list[str] = Field(description="List of relevant tags")

article = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Analyze this article: [article text]"
    }],
    response_model=Article
)
```

**Benefícios:**
- Segurança de tipo com type hints do Python
- Validação automática (word_count > 0)
- Auto-documentado com descrições de Field
- Suporte a autocomplete do IDE

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

person = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "John lives at 123 Main St, Boston, USA"
    }],
    response_model=Person
)

print(person.address.city)  # "Boston"
```

#### Campos Opcionais

```python
from typing import Optional

class Product(BaseModel):
    name: str
    price: float
    discount: Optional[float] = None  # Opcional
    description: str = Field(default="No description")  # Valor padrão

# LLM não precisa fornecer discount ou description
```

#### Enums para Restrições

```python
from enum import Enum

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class Review(BaseModel):
    text: str
    sentiment: Sentiment  # Apenas estes 3 valores permitidos

review = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "This product is amazing!"
    }],
    response_model=Review
)

print(review.sentiment)  # Sentiment.POSITIVE
```

### 2. Validação

Pydantic valida saídas de LLM automaticamente. Se a validação falhar, Instructor tenta novamente.

#### Validadores Integrados

```python
from pydantic import Field, EmailStr, HttpUrl

class Contact(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=0, le=120)  # 0 <= age <= 120
    email: EmailStr  # Valida formato de email
    website: HttpUrl  # Valida formato de URL

# Se LLM fornecer dados inválidos, Instructor tenta novamente automaticamente
```

#### Validadores Customizados

```python
from pydantic import field_validator

class Event(BaseModel):
    name: str
    date: str
    attendees: int

    @field_validator('date')
    def validate_date(cls, v):
        """Assegure que a data está no formato YYYY-MM-DD."""
        import re
        if not re.match(r'\d{4}-\d{2}-\d{2}', v):
            raise ValueError('Date must be YYYY-MM-DD format')
        return v

    @field_validator('attendees')
    def validate_attendees(cls, v):
        """Assegure participantes positivos."""
        if v < 1:
            raise ValueError('Must have at least 1 attendee')
        return v
```

#### Validação em Nível de Modelo

```python
from pydantic import model_validator

class DateRange(BaseModel):
    start_date: str
    end_date: str

    @model_validator(mode='after')
    def check_dates(self):
        """Assegure que end_date é depois de start_date."""
        from datetime import datetime
        start = datetime.strptime(self.start_date, '%Y-%m-%d')
        end = datetime.strptime(self.end_date, '%Y-%m-%d')

        if end < start:
            raise ValueError('end_date must be after start_date')
        return self
```

### 3. Tentativa Automática

Instructor tenta novamente automaticamente quando a validação falha, fornecendo feedback de erro ao LLM.

```python
# Tenta novamente até 3 vezes se a validação falhar
user = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Extract user from: John, age unknown"
    }],
    response_model=User,
    max_retries=3  # Padrão é 3
)

# Se a idade não puder ser extraída, Instructor diz ao LLM:
# "Validation error: age - field required"
# LLM tenta novamente com melhor extração
```

**Como funciona:**
1. LLM gera saída
2. Pydantic valida
3. Se inválido: Mensagem de erro enviada de volta ao LLM
4. LLM tenta novamente com feedback de erro
5. Repete até max_retries

### 4. Transmissão

Transmita resultados parciais para processamento em tempo real.

#### Transmitindo Objetos Parciais

```python
from instructor import Partial

class Story(BaseModel):
    title: str
    content: str
    tags: list[str]

# Transmita atualizações parciais enquanto o LLM gera
for partial_story in client.messages.create_partial(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Write a short sci-fi story"
    }],
    response_model=Story
):
    print(f"Title: {partial_story.title}")
    print(f"Content so far: {partial_story.content[:100]}...")
    # Atualize UI em tempo real
```

#### Transmitindo Iteráveis

```python
class Task(BaseModel):
    title: str
    priority: str

# Transmita itens da lista enquanto são gerados
tasks = client.messages.create_iterable(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Generate 10 project tasks"
    }],
    response_model=Task
)

for task in tasks:
    print(f"- {task.title} ({task.priority})")
    # Processe cada tarefa conforme chega
```

## Configuração de Provedor

### Anthropic Claude

```python
import instructor
from anthropic import Anthropic

client = instructor.from_anthropic(
    Anthropic(api_key="your-api-key")
)

# Use com modelos Claude
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[...],
    response_model=YourModel
)
```

### OpenAI

```python
from openai import OpenAI

client = instructor.from_openai(
    OpenAI(api_key="your-api-key")
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=YourModel,
    messages=[...]
)
```

### Modelos Locais (Ollama)

```python
from openai import OpenAI

# Aponte para servidor Ollama local
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"  # Requerido mas ignorado
    ),
    mode=instructor.Mode.JSON
)

response = client.chat.completions.create(
    model="llama3.1",
    response_model=YourModel,
    messages=[...]
)
```

## Padrões Comuns

### Padrão 1: Extração de Dados de Texto

```python
class CompanyInfo(BaseModel):
    name: str
    founded_year: int
    industry: str
    employees: int
    headquarters: str

text = """
Tesla, Inc. was founded in 2003. It operates in the automotive and energy
industry with approximately 140,000 employees. The company is headquartered
in Austin, Texas.
"""

company = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"Extract company information from: {text}"
    }],
    response_model=CompanyInfo
)
```

### Padrão 2: Classificação

```python
class Category(str, Enum):
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    OTHER = "other"

class ArticleClassification(BaseModel):
    category: Category
    confidence: float = Field(ge=0.0, le=1.0)
    keywords: list[str]

classification = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Classify this article: [article text]"
    }],
    response_model=ArticleClassification
)
```

### Padrão 3: Extração de Múltiplas Entidades

```python
class Person(BaseModel):
    name: str
    role: str

class Organization(BaseModel):
    name: str
    industry: str

class Entities(BaseModel):
    people: list[Person]
    organizations: list[Organization]
    locations: list[str]

text = "Tim Cook, CEO of Apple, announced at the event in Cupertino..."

entities = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"Extract all entities from: {text}"
    }],
    response_model=Entities
)

for person in entities.people:
    print(f"{person.name} - {person.role}")
```

### Padrão 4: Análise Estruturada

```python
class SentimentAnalysis(BaseModel):
    overall_sentiment: Sentiment
    positive_aspects: list[str]
    negative_aspects: list[str]
    suggestions: list[str]
    score: float = Field(ge=-1.0, le=1.0)

review = "The product works well but setup was confusing..."

analysis = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"Analyze this review: {review}"
    }],
    response_model=SentimentAnalysis
)
```

### Padrão 5: Processamento em Lote

```python
def extract_person(text: str) -> Person:
    return client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Extract person from: {text}"
        }],
        response_model=Person
    )

texts = [
    "John Doe is a 30-year-old engineer",
    "Jane Smith, 25, works in marketing",
    "Bob Johnson, age 40, software developer"
]

people = [extract_person(text) for text in texts]
```

## Recursos Avançados

### Tipos Union

```python
from typing import Union

class TextContent(BaseModel):
    type: str = "text"
    content: str

class ImageContent(BaseModel):
    type: str = "image"
    url: HttpUrl
    caption: str

class Post(BaseModel):
    title: str
    content: Union[TextContent, ImageContent]  # Um ou outro tipo

# LLM escolhe tipo apropriado baseado no conteúdo
```

### Modelos Dinâmicos

```python
from pydantic import create_model

# Crie modelo em tempo de execução
DynamicUser = create_model(
    'User',
    name=(str, ...),
    age=(int, Field(ge=0)),
    email=(EmailStr, ...)
)

user = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[...],
    response_model=DynamicUser
)
```

### Modos Customizados

```python
# Para provedores sem saídas estruturadas nativas
client = instructor.from_anthropic(
    Anthropic(),
    mode=instructor.Mode.JSON  # Modo JSON
)

# Modos disponíveis:
# - Mode.ANTHROPIC_TOOLS (recomendado para Claude)
# - Mode.JSON (fallback)
# - Mode.TOOLS (OpenAI tools)
```

### Gerenciamento de Contexto

```python
# Cliente de uso único
with instructor.from_anthropic(Anthropic()) as client:
    result = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[...],
        response_model=YourModel
    )
    # Cliente fechado automaticamente
```

## Tratamento de Erros

### Tratando Erros de Validação

```python
from pydantic import ValidationError

try:
    user = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[...],
        response_model=User,
        max_retries=3
    )
except ValidationError as e:
    print(f"Failed after retries: {e}")
    # Trate graciosamente

except Exception as e:
    print(f"API error: {e}")
```

### Mensagens de Erro Customizadas

```python
class ValidatedUser(BaseModel):
    name: str = Field(description="Full name, 2-100 characters")
    age: int = Field(description="Age between 0 and 120", ge=0, le=120)
    email: EmailStr = Field(description="Valid email address")

    class Config:
        # Mensagens de erro customizadas
        json_schema_extra = {
            "examples": [
                {
                    "name": "John Doe",
                    "age": 30,
                    "email": "john@example.com"
                }
            ]
        }
```

## Melhores Práticas

### 1. Descrições de Campo Claras

```python
# ❌ Ruim: Vago
class Product(BaseModel):
    name: str
    price: float

# ✅ Bom: Descritivo
class Product(BaseModel):
    name: str = Field(description="Product name from the text")
    price: float = Field(description="Price in USD, without currency symbol")
```

### 2. Use Validação Apropriada

```python
# ✅ Bom: Restrinja valores
class Rating(BaseModel):
    score: int = Field(ge=1, le=5, description="Rating from 1 to 5 stars")
    review: str = Field(min_length=10, description="Review text, at least 10 chars")
```

### 3. Forneça Exemplos nos Prompts

```python
messages = [{
    "role": "user",
    "content": """Extract person info from: "John, 30, engineer"

Example format:
{
  "name": "John Doe",
  "age": 30,
  "occupation": "engineer"
}"""
}]
```

### 4. Use Enums para Categorias Fixas

```python
# ✅ Bom: Enum garante valores válidos
class Status(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Application(BaseModel):
    status: Status  # LLM deve escolher do enum
```

### 5. Trate Dados Faltantes Graciosamente

```python
class PartialData(BaseModel):
    required_field: str
    optional_field: Optional[str] = None
    default_field: str = "default_value"

# LLM só precisa fornecer required_field
```

## Comparação com Alternativas

| Recurso | Instructor | JSON Manual | LangChain | DSPy |
|---------|------------|------------|-----------|------|
| Segurança de Tipo | ✅ Sim | ❌ Não | ⚠️ Parcial | ✅ Sim |
| Validação Automática | ✅ Sim | ❌ Não | ❌ Não | ⚠️ Limitado |
| Tentativa Automática | ✅ Sim | ❌ Não | ❌ Não | ✅ Sim |
| Transmissão | ✅ Sim | ❌ Não | ✅ Sim | ❌ Não |
| Multi-Provedor | ✅ Sim | ⚠️ Manual | ✅ Sim | ✅ Sim |
| Curva de Aprendizado | Baixa | Baixa | Média | Alta |

**Quando escolher Instructor:**
- Precisa de saídas estruturadas e validadas
- Quer segurança de tipo e suporte a IDE
- Requer tentativas automáticas
- Construindo sistemas de extração de dados

**Quando escolher alternativas:**
- DSPy: Precisa otimizar prompts
- LangChain: Construindo chains complexas
- Manual: Extrações simples e únicas

## Recursos

- **Documentação**: https://python.useinstructor.com
- **GitHub**: https://github.com/jxnl/instructor (15k+ stars)
- **Cookbook**: https://python.useinstructor.com/examples
- **Discord**: Suporte da comunidade disponível

## Veja Também

- `references/validation.md` - Padrões avançados de validação
- `references/providers.md` - Configuração específica de provedor
- `references/examples.md` - Casos de uso do mundo real