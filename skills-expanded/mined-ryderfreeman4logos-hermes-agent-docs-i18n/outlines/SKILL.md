---
name: outlines
description: "Outlines: structured JSON/regex/Pydantic LLM generation."
version: 1.0.1
author: Orchestra Research
license: MIT
dependencies: [outlines, transformers, vllm, pydantic]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Prompt Engineering, Outlines, Structured Generation, JSON Schema, Pydantic, Local Models, Grammar-Based Generation, vLLM, Transformers, Type Safety]

---

# 大纲生成：结构化文本生成

## 何时使用此技能

当您需要以下功能时，可使用大纲生成技能：
- 在生成过程中**确保输出为有效的 JSON/XML/代码结构**
- 使用 **Pydantic 模型**实现类型安全的输出
- **支持本地模型**（如 Transformers、llama.cpp、vLLM）
- 通过无开销的结构化生成方式**最大化推理速度**
- **自动依据 JSON 架构进行生成**
- 在语法层面**控制令牌采样过程**

**GitHub 星标数**：12,000+ | **来源**：dottxt.ai（前身为 .txt）

> **API 说明（Outlines 1.x 版）**：该技能针对当前 v1 API 设计。
> 1.0 版之前的辅助函数（如 `outlines.models.transformers(...)`,
> `outlines.generate.json/choice/regex/...`）已**被移除**。在 v1 版中，您需要先使用 `outlines.from_transformers(...)`（或 `from_vllm`、`from_llamacpp`、`from_openai`）创建模型，然后再通过指定输出类型**直接调用该模型**：`model(prompt, output_type)`。JSON/Pydantic 格式的输出将以**JSON 字符串**形式返回——建议使用 `YourModel.model_validate_json(result)` 进行验证。

## 安装指南

```bash
# Base installation
pip install outlines

# With specific backends
pip install outlines transformers  # Hugging Face models
pip install outlines llama-cpp-python  # llama.cpp
pip install outlines vllm  # vLLM for high-throughput
```

## 快速入门

### 基本示例：分类任务

```python
import outlines
from typing import Literal
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

# v1: wrap a Transformers model + tokenizer
model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto"),
    AutoTokenizer.from_pretrained(MODEL_NAME),
)

# Call the model directly with an output type
prompt = "Sentiment of 'This product is amazing!': "
sentiment = model(prompt, Literal["positive", "negative", "neutral"])

print(sentiment)  # "positive" (guaranteed one of these)
```

### 使用 Pydantic 模型

```python
from pydantic import BaseModel
import outlines
from transformers import AutoModelForCausalLM, AutoTokenizer

class User(BaseModel):
    name: str
    age: int
    email: str

MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto"),
    AutoTokenizer.from_pretrained(MODEL_NAME),
)

# Generate structured output (returns a JSON string)
prompt = "Extract user: John Doe, 30 years old, john@example.com"
result = model(prompt, User, max_new_tokens=200)

user = User.model_validate_json(result)  # parse into the Pydantic model
print(user.name)   # "John Doe"
print(user.age)    # 30
print(user.email)  # "john@example.com"
```

## 核心概念

### 1. 受限令牌采样

该机制通过基于输出类型生成的编译后自动机，在逻辑层面对令牌生成过程进行约束。

**工作原理：**
1. 将输出类型（JSON/Pydantic/正则表达式/`Literal`）转换为模式/语法结构
2. 将该语法结构编译为令牌级自动机
3. 在生成过程中的每一步过滤无效令牌
4. 当仅存在一个有效令牌时直接跳过后续处理

**优势：**
- **零额外开销**：过滤操作在令牌层面直接执行
- **提升速度**：可通过确定性路径快速推进
- **保证有效性**：彻底杜绝无效输出的产生

```python
import outlines
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

class Person(BaseModel):
    name: str
    age: int

model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-4k-instruct", device_map="auto"),
    AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct"),
)

result = model("Generate person: Alice, 25", Person)
person = Person.model_validate_json(result)
```

### 2. 输出类型

在 v1 版本中，您需要直接将所需的**输出类型**作为第二个参数传入。

#### 多项选择（`Literal`）

```python
from typing import Literal

sentiment = model("Review: This is great!", Literal["positive", "negative", "neutral"])
# Result: one of the three choices
```

#### 通过 Pydantic 处理 JSON 数据

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

result = model("Extract: iPhone 15, $999, available", Product)
product = Product.model_validate_json(result)  # valid Product instance
```

#### 正则表达式（传入正则表达式字符串）

```python
# Generate text matching a regex pattern
phone = model("Generate phone number:", r"[0-9]{3}-[0-9]{3}-[0-9]{4}")
# Result: "555-123-4567" (guaranteed to match the pattern)
```

#### 数值类型

```python
# Pass the Python type directly
age = model("Person's age:", int)      # guaranteed integer
price = model("Product price:", float)  # guaranteed float
```

### 3. 模型后端

Outlines 支持通过 `from_*` 工厂函数使用多种本地及基于 API 的后端。

#### Transformers（Hugging Face）

```python
import outlines
from transformers import AutoModelForCausalLM, AutoTokenizer

model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-4k-instruct", device_map="auto"),
    AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct"),
)

result = model(prompt, YourModel)
```

#### llama.cpp

```python
import outlines
from llama_cpp import Llama

llm = Llama("./models/llama-3.1-8b-instruct.Q4_K_M.gguf", n_gpu_layers=35, n_ctx=4096)
model = outlines.from_llamacpp(llm)

result = model(prompt, YourModel)
```

#### vLLM（高吞吐模式）

```python
import outlines
from vllm import LLM

llm = LLM("meta-llama/Llama-3.1-8B-Instruct", tensor_parallel_size=2)
model = outlines.from_vllm(llm)

result = model(prompt, YourModel)
```

#### OpenAI（服务器端受限 JSON 格式）

```python
import outlines
from openai import OpenAI

client = OpenAI()
model = outlines.from_openai(client, "gpt-4o-mini")

# API backends support JSON-schema style structured output
result = model(prompt, YourModel)
```

### 4. Pydantic 集成

Outlines 提供一流的 Pydantic 支持，可实现自动模式转换。
生成结果为 JSON 字符串；可通过调用 `model_validate_json` 函数来获取对应实例。

#### 基本模型

```python
from pydantic import BaseModel, Field

class Article(BaseModel):
    title: str = Field(description="Article title")
    author: str = Field(description="Author name")
    word_count: int = Field(description="Number of words", gt=0)
    tags: list[str] = Field(description="List of tags")

result = model("Generate article about AI", Article, max_new_tokens=300)
article = Article.model_validate_json(result)
print(article.title)
print(article.word_count)  # Guaranteed > 0
```

#### 嵌套模型

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class Person(BaseModel):
    name: str
    age: int
    address: Address  # Nested model

result = model("Generate person in New York", Person)
person = Person.model_validate_json(result)
print(person.address.city)  # "New York"
```

#### 枚举与字面量

```python
from enum import Enum
from typing import Literal

class Status(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Application(BaseModel):
    applicant: str
    status: Status  # Must be one of enum values
    priority: Literal["low", "medium", "high"]  # Must be one of literals

result = model("Generate application", Application)
app = Application.model_validate_json(result)
print(app.status)  # Status.PENDING (or APPROVED/REJECTED)
```

## 常见模式

### 模式 1：数据提取

```python
from pydantic import BaseModel
import outlines
from transformers import AutoModelForCausalLM, AutoTokenizer

class CompanyInfo(BaseModel):
    name: str
    founded_year: int
    industry: str
    employees: int

model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-4k-instruct", device_map="auto"),
    AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct"),
)

text = """
Apple Inc. was founded in 1976 in the technology industry.
The company employs approximately 164,000 people worldwide.
"""

prompt = f"Extract company information:\n{text}\n\nCompany:"
company = CompanyInfo.model_validate_json(model(prompt, CompanyInfo, max_new_tokens=200))

print(f"Name: {company.name}")
print(f"Founded: {company.founded_year}")
print(f"Industry: {company.industry}")
print(f"Employees: {company.employees}")
```

### 模式2：分类任务

```python
from typing import Literal
from pydantic import BaseModel

# Binary classification
result = model("Email: Buy now! 50% off!", Literal["spam", "not_spam"])

# Multi-class classification
category = model(
    "Article: Apple announces new iPhone...",
    Literal["technology", "business", "sports", "entertainment"],
)

# With confidence
class Classification(BaseModel):
    label: Literal["positive", "negative", "neutral"]
    confidence: float

out = model("Review: This product is okay, nothing special", Classification)
result = Classification.model_validate_json(out)
```

### 模式 3：结构化表单

```python
class UserProfile(BaseModel):
    full_name: str
    age: int
    email: str
    phone: str
    country: str
    interests: list[str]

prompt = """
Extract user profile from:
Name: Alice Johnson
Age: 28
Email: alice@example.com
Phone: 555-0123
Country: USA
Interests: hiking, photography, cooking
"""

profile = UserProfile.model_validate_json(model(prompt, UserProfile, max_new_tokens=250))
print(profile.full_name)
print(profile.interests)  # ["hiking", "photography", "cooking"]
```

### 模式4：多实体提取

```python
from typing import Literal

class Entity(BaseModel):
    name: str
    type: Literal["PERSON", "ORGANIZATION", "LOCATION"]

class DocumentEntities(BaseModel):
    entities: list[Entity]

text = "Tim Cook met with Satya Nadella at Microsoft headquarters in Redmond."
prompt = f"Extract entities from: {text}"

result = DocumentEntities.model_validate_json(model(prompt, DocumentEntities, max_new_tokens=300))
for entity in result.entities:
    print(f"{entity.name} ({entity.type})")
```

### 模式 5：代码生成

```python
class PythonFunction(BaseModel):
    function_name: str
    parameters: list[str]
    docstring: str
    body: str

prompt = "Generate a Python function to calculate factorial"
func = PythonFunction.model_validate_json(model(prompt, PythonFunction, max_new_tokens=300))

print(f"def {func.function_name}({', '.join(func.parameters)}):")
print(f'    """{func.docstring}"""')
print(f"    {func.body}")
```

### 模式 6：批量处理

```python
import outlines
from transformers import AutoModelForCausalLM, AutoTokenizer
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-4k-instruct", device_map="auto"),
    AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct"),
)

texts = [
    "John is 30 years old",
    "Alice is 25 years old",
    "Bob is 40 years old",
]

# v1 accepts a list of prompts for batched generation
prompts = [f"Extract from: {t}" for t in texts]
outputs = model(prompts, Person, max_new_tokens=100)
people = [Person.model_validate_json(o) for o in outputs]
for person in people:
    print(f"{person.name}: {person.age}")
```

## 后端配置

### 转换器

```python
import outlines
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

# Basic usage
model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto"),
    AutoTokenizer.from_pretrained(MODEL_NAME),
)

# GPU + dtype configuration is set on the HF model itself
import torch
model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="cuda", torch_dtype=torch.float16),
    AutoTokenizer.from_pretrained(MODEL_NAME),
)

# Popular models
for name in [
    "meta-llama/Llama-3.1-8B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "Qwen/Qwen2.5-7B-Instruct",
]:
    model = outlines.from_transformers(
        AutoModelForCausalLM.from_pretrained(name, device_map="auto"),
        AutoTokenizer.from_pretrained(name),
    )
```

### llama.cpp

```python
import outlines
from llama_cpp import Llama

# Load GGUF model
llm = Llama(
    "./models/llama-3.1-8b.Q4_K_M.gguf",
    n_ctx=4096,       # Context window
    n_gpu_layers=35,  # GPU layers
    n_threads=8,      # CPU threads
)
model = outlines.from_llamacpp(llm)

# Full GPU offload: set n_gpu_layers=-1 on the Llama object
```

### vLLM（生产环境版）

```python
import outlines
from vllm import LLM

# Single GPU
model = outlines.from_vllm(LLM("meta-llama/Llama-3.1-8B-Instruct"))

# Multi-GPU
model = outlines.from_vllm(LLM("meta-llama/Llama-3.1-70B-Instruct", tensor_parallel_size=4))

# With quantization
model = outlines.from_vllm(LLM("meta-llama/Llama-3.1-8B-Instruct", quantization="awq"))
```

## 最佳实践

### 1. 使用特定类型

```python
# ✅ Good: Specific types
class Product(BaseModel):
    name: str
    price: float  # Not str
    quantity: int  # Not str
    in_stock: bool  # Not str

# ❌ Bad: Everything as string
class Product(BaseModel):
    name: str
    price: str  # Should be float
    quantity: str  # Should be int
```

### 2. 添加约束条件

```python
from pydantic import Field

# ✅ Good: With constraints
class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=120)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

# ❌ Bad: No constraints
class User(BaseModel):
    name: str
    age: int
    email: str
```

### 3. 使用枚举类型定义分类

```python
# ✅ Good: Enum for fixed set
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str
    priority: Priority

# ❌ Bad: Free-form string
class Task(BaseModel):
    title: str
    priority: str  # Can be anything
```

### 4. 在提示词中提供上下文信息

```python
# ✅ Good: Clear context
prompt = """
Extract product information from the following text.
Text: iPhone 15 Pro costs $999 and is currently in stock.
Product:
"""

# ❌ Bad: Minimal context
prompt = "iPhone 15 Pro costs $999 and is currently in stock."
```

### 5. 处理可选字段

```python
from typing import Optional

# ✅ Good: Optional fields for incomplete data
class Article(BaseModel):
    title: str  # Required
    author: Optional[str] = None  # Optional
    date: Optional[str] = None  # Optional
    tags: list[str] = []  # Default empty list

# Can succeed even if author/date missing
```

### 6. 始终对 JSON 输出进行验证

```python
# v1 returns a JSON string for Pydantic/JSON output types.
result = model(prompt, Article)          # str
article = Article.model_validate_json(result)  # Article instance
```

## 与其他方案的对比

| 功能特性 | Outlines | Instructor | Guidance | LMQL |
|---------|----------|------------|----------|------|
| Pydantic 支持 | ✅ 原生支持 | ✅ 原生支持 | ✅ 支持 | ❌ 不支持 |
| JSON Schema 支持 | ✅ 支持 | ✅ 支持 | ✅ 支持 | ✅ 支持 |
| 正则表达式约束 | ✅ 支持 | ❌ 不支持 | ✅ 支持 | ✅ 支持 |
| 本地模型 | ✅ 完全支持 | ⚠️ 有限支持 | ✅ 完全支持 | ✅ 完全支持 |
| API 模型 | ✅ 支持 | ✅ 完全支持 | ✅ 支持 | ✅ 完全支持 |
| 零开销生成 | ✅ 支持 | ❌ 不支持 | ⚠️ 部分支持 | ✅ 支持 |
| 自动重试功能 | ❌ 不支持 | ✅ 支持 | ❌ 不支持 | ❌ 不支持 |
| 学习曲线 | 较低 | 较低 | 较低 | 较高 |

**何时选择 Outlines：**
- 使用本地模型（如 Transformers、llama.cpp、vLLM）
- 需要最高的推理速度
- 需要 Pydantic 模型支持
- 要求零开销的结构化生成
- 需要自行控制令牌采样过程

**何时选择其他方案：**
- Instructor：需要带有自动重试功能的 API 模型
- Guidance：需要令牌修复功能及复杂工作流支持
- LMQL：偏好声明式查询语法

## 性能特点

**速度：**
- **零开销**：结构化生成的效率与无约束生成相当
- **快进优化**：可跳过已确定的令牌
- 相比生成后的验证方式，速度提升 **1.2–2 倍**

**内存占用：**
- 每种输出类型仅编译一次自动机（并缓存结果）
- 运行时开销极低
- 结合 vLLM 使用时可实现高吞吐量处理

**准确性：**
- **100% 合法的输出结果**（由约束型自动机保证）
- 无需重复尝试
- 具有确定性的令牌过滤机制
## 资源

- **文档**：https://dottxt-ai.github.io/outlines/
- **GitHub 仓库**：https://github.com/dottxt-ai/outlines（拥有 12k 多个星标）
- **Discord 社群**：https://discord.gg/R9DSu34mGd
- **博客**：https://blog.dottxt.co

## 相关内容

- `references/json_generation.md` - 关于 JSON 与 Pydantic 的完整用法指南
- `references/backends.md` - 各后端特有的配置说明
- `references/examples.md` - 可直接用于生产环境的示例代码
