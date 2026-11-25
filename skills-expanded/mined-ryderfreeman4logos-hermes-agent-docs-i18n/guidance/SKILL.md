---
name: guidance
description: Constrain LLM output with grammars; guarantee valid JSON.
version: 1.0.1
author: Orchestra Research
license: MIT
dependencies: [guidance, transformers]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Prompt Engineering, Guidance, Constrained Generation, Structured Output, JSON Validation, Grammar, Microsoft Research, Format Enforcement, Multi-Step Workflows]

---

# 指导功能：受限型大语言模型生成

## 何时使用此功能

当您需要实现以下目标时，可使用指导功能：
- 使用正则表达式或语法规则**控制大语言模型的输出格式**
- **确保生成有效的 JSON/XML/代码内容**
- 相较于传统提示方式，**降低响应延迟**
- **强制采用结构化格式**（日期、电子邮件地址、编号等）
- 基于 Python 风格的流程控制来**构建多步骤工作流**
- 通过语法约束**避免无效输出**

**GitHub 星标数**：18,000+ | **来源**：微软研究院

## 安装指南

```bash
# Base installation
pip install guidance

# With specific backends
pip install guidance[transformers]  # Hugging Face models
pip install guidance[llama_cpp]     # llama.cpp models
```

## 快速入门

### 基本示例：结构化生成

```python
from guidance import models, gen

# Load model (supports OpenAI, Transformers, llama.cpp)
lm = models.OpenAI("gpt-4")

# Generate with constraints
result = lm + "The capital of France is " + gen("capital", max_tokens=5)

print(result["capital"])  # "Paris"
```

### 与本地模型的聊天模式

> **要实现约束功能，必须能够访问本地模型。** 正则表达式、`select()`函数以及基于语法的约束生成功能仅支持本地后端（如`Transformers`、`LlamaCpp`）。而远程API后端（如`OpenAI`及Azure相关版本）仅支持无约束的`gen()`/聊天功能——它们无法实施基于token级别的约束。guidance 0.3.x版本中不存在`models.Anthropic`类。

```python
from guidance import models, gen, system, user, assistant

# Local model (supports constrained generation)
lm = models.Transformers("microsoft/Phi-4-mini-instruct")

# Use context managers for chat format
with system():
    lm += "You are a helpful assistant."

with user():
    lm += "What is the capital of France?"

with assistant():
    lm += gen(max_tokens=20)
```

## 核心概念

### 1. 上下文管理器

该指南采用符合 Python 风格的上下文管理器来实现类似对话式的交互。

```python
from guidance import system, user, assistant, gen

lm = models.Transformers("microsoft/Phi-4-mini-instruct")

# System message
with system():
    lm += "You are a JSON generation expert."

# User message
with user():
    lm += "Generate a person object with name and age."

# Assistant response
with assistant():
    lm += gen("response", max_tokens=100)

print(lm["response"])
```

**优势：**  
- 自然的对话流程  
- 清晰的角色分工  
- 易于阅读与维护  

### 2. 约束生成  

通过规则引导，利用正则表达式或语法确保输出符合指定模式。  

#### 正则表达式约束

```python
from guidance import models, gen

lm = models.Transformers("microsoft/Phi-4-mini-instruct")

# Constrain to valid email format
lm += "Email: " + gen("email", regex=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Constrain to date format (YYYY-MM-DD)
lm += "Date: " + gen("date", regex=r"\d{4}-\d{2}-\d{2}")

# Constrain to phone number
lm += "Phone: " + gen("phone", regex=r"\d{3}-\d{3}-\d{4}")

print(lm["email"])  # Guaranteed valid email
print(lm["date"])   # Guaranteed YYYY-MM-DD format
```

**工作原理：**
- 正则表达式在分词层面被转换为语法结构
- 生成过程中会过滤掉无效的分词
- 模型仅能输出符合规则的响应

#### 选择约束条件

```python
from guidance import models, gen, select

lm = models.Transformers("microsoft/Phi-4-mini-instruct")

# Constrain to specific choices
lm += "Sentiment: " + select(["positive", "negative", "neutral"], name="sentiment")

# Multiple-choice selection
lm += "Best answer: " + select(
    ["A) Paris", "B) London", "C) Berlin", "D) Madrid"],
    name="answer"
)

print(lm["sentiment"])  # One of: positive, negative, neutral
print(lm["answer"])     # One of: A, B, C, or D
```

### 3. 令牌修复功能

该功能可自动“修复”提示词与生成内容之间的令牌边界问题。

**问题：** 令牌化处理会生成不自然的边界。

```python
# Without token healing
prompt = "The capital of France is "
# Last token: " is "
# First generated token might be " Par" (with leading space)
# Result: "The capital of France is  Paris" (double space!)
```

**解决方案：** Guidance功能会备份一个令牌并重新生成。

```python
from guidance import models, gen

lm = models.Transformers("microsoft/Phi-4-mini-instruct")

# Token healing enabled by default
lm += "The capital of France is " + gen("capital", max_tokens=5)
# Result: "The capital of France is Paris" (correct spacing)
```

**优势：**  
- 自然的文本分界  
- 无尴尬的间距问题  
- 更佳的模型性能（能够识别自然的标记序列）  

### 4. 基于语法的生成  

通过组合语法函数来定义复杂结构。当前的指南中并未涉及 `grammar=` 格式的模板字符串——建议通过可组合的函数来构建语法，或使用 `guidance.json()` 来处理 JSON 格式的内容。

```python
from guidance import models, gen
from guidance import json as gen_json
from pydantic import BaseModel, Field

lm = models.Transformers("microsoft/Phi-4-mini-instruct")

# JSON via a Pydantic schema (guidance.json compiles the schema to a grammar)
class Person(BaseModel):
    name: str = Field(pattern=r"[A-Za-z ]+")
    age: int
    email: str = Field(pattern=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

lm += gen_json(name="person", schema=Person)

print(lm["person"])  # Guaranteed valid JSON matching the schema

# Or compose grammar functions directly:
grammar = "name=" + gen("name", regex=r"[A-Za-z ]+") + " age=" + gen("age", regex=r"[0-9]+")
lm += grammar
```

**应用场景：**
- 复杂的结构化输出
- 嵌套的数据结构
- 编程语言语法
- 领域专用语言

### 5. 指导函数

通过 `@guidance` 装饰器创建可复用的生成模式。

```python
from guidance import guidance, gen, models

@guidance
def generate_person(lm):
    """Generate a person with name and age."""
    lm += "Name: " + gen("name", max_tokens=20, stop="\n")
    lm += "\nAge: " + gen("age", regex=r"[0-9]+", max_tokens=3)
    return lm

# Use the function
lm = models.Transformers("microsoft/Phi-4-mini-instruct")
lm = generate_person(lm)

print(lm["name"])
print(lm["age"])
```

**有状态函数：**

```python
@guidance(stateless=False)
def react_agent(lm, question, tools, max_rounds=5):
    """ReAct agent with tool use."""
    lm += f"Question: {question}\n\n"

    for i in range(max_rounds):
        # Thought
        lm += f"Thought {i+1}: " + gen("thought", stop="\n")

        # Action
        lm += "\nAction: " + select(list(tools.keys()), name="action")

        # Execute tool
        tool_result = tools[lm["action"]]()
        lm += f"\nObservation: {tool_result}\n\n"

        # Check if done
        lm += "Done? " + select(["Yes", "No"], name="done")
        if lm["done"] == "Yes":
            break

    # Final answer
    lm += "\nFinal Answer: " + gen("answer", max_tokens=100)
    return lm
```

## 后端配置

### OpenAI（远程——仅支持无限制模式）

> 远程 API 后端不支持受限生成功能（如正则表达式/选择项/语法限制）；
> 仅适用于普通聊天或 `gen()` 功能。如需实现约束条件，应使用本地后端。

```python
from guidance import models

lm = models.OpenAI(
    model="gpt-4o-mini",
    api_key="your-api-key"  # Or set OPENAI_API_KEY env var
)
```

### 本地模型（Transformer）

```python
from guidance.models import Transformers

lm = Transformers(
    "microsoft/Phi-4-mini-instruct",
    device="cuda"  # Or "cpu"
)
```

### 本地模型（llama.cpp）

```python
from guidance.models import LlamaCpp

lm = LlamaCpp(
    model_path="/path/to/model.gguf",
    n_ctx=4096,
    n_gpu_layers=35
)
```

## 常见模式

### 模式 1：JSON 生成

```python
from guidance import models, gen, system, user, assistant

lm = models.Transformers("microsoft/Phi-4-mini-instruct")

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

print(lm)  # Valid JSON guaranteed
```

### 模式2：分类任务

```python
from guidance import models, gen, select

lm = models.Transformers("microsoft/Phi-4-mini-instruct")

text = "This product is amazing! I love it."

lm += f"Text: {text}\n"
lm += "Sentiment: " + select(["positive", "negative", "neutral"], name="sentiment")
lm += "\nConfidence: " + gen("confidence", regex=r"[0-9]+", max_tokens=3) + "%"

print(f"Sentiment: {lm['sentiment']}")
print(f"Confidence: {lm['confidence']}%")
```

### 模式 3：多步骤推理

```python
from guidance import models, gen, guidance

@guidance
def chain_of_thought(lm, question):
    """Generate answer with step-by-step reasoning."""
    lm += f"Question: {question}\n\n"

    # Generate multiple reasoning steps
    for i in range(3):
        lm += f"Step {i+1}: " + gen(f"step_{i+1}", stop="\n", max_tokens=100) + "\n"

    # Final answer
    lm += "\nTherefore, the answer is: " + gen("answer", max_tokens=50)

    return lm

lm = models.Transformers("microsoft/Phi-4-mini-instruct")
lm = chain_of_thought(lm, "What is 15% of 200?")

print(lm["answer"])
```

### 模式 4：ReAct 智能体

```python
from guidance import models, gen, select, guidance

@guidance(stateless=False)
def react_agent(lm, question):
    """ReAct agent with tool use."""
    tools = {
        "calculator": lambda expr: eval(expr),
        "search": lambda query: f"Search results for: {query}",
    }

    lm += f"Question: {question}\n\n"

    for round in range(5):
        # Thought
        lm += f"Thought: " + gen("thought", stop="\n") + "\n"

        # Action selection
        lm += "Action: " + select(["calculator", "search", "answer"], name="action")

        if lm["action"] == "answer":
            lm += "\nFinal Answer: " + gen("answer", max_tokens=100)
            break

        # Action input
        lm += "\nAction Input: " + gen("action_input", stop="\n") + "\n"

        # Execute tool
        if lm["action"] in tools:
            result = tools[lm["action"]](lm["action_input"])
            lm += f"Observation: {result}\n\n"

    return lm

lm = models.Transformers("microsoft/Phi-4-mini-instruct")
lm = react_agent(lm, "What is 25 * 4 + 10?")
print(lm["answer"])
```

### 模式 5：数据提取

```python
from guidance import models, gen, guidance

@guidance
def extract_entities(lm, text):
    """Extract structured entities from text."""
    lm += f"Text: {text}\n\n"

    # Extract person
    lm += "Person: " + gen("person", stop="\n", max_tokens=30) + "\n"

    # Extract organization
    lm += "Organization: " + gen("organization", stop="\n", max_tokens=30) + "\n"

    # Extract date
    lm += "Date: " + gen("date", regex=r"\d{4}-\d{2}-\d{2}", max_tokens=10) + "\n"

    # Extract location
    lm += "Location: " + gen("location", stop="\n", max_tokens=30) + "\n"

    return lm

text = "Tim Cook announced at Apple Park on 2024-09-15 in Cupertino."

lm = models.Transformers("microsoft/Phi-4-mini-instruct")
lm = extract_entities(lm, text)

print(f"Person: {lm['person']}")
print(f"Organization: {lm['organization']}")
print(f"Date: {lm['date']}")
print(f"Location: {lm['location']}")
```

## 最佳实践

### 1. 使用正则表达式进行格式验证

```python
# ✅ Good: Regex ensures valid format
lm += "Email: " + gen("email", regex=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# ❌ Bad: Free generation may produce invalid emails
lm += "Email: " + gen("email", max_tokens=50)
```

### 2. 使用 select() 函数处理固定类别

```python
# ✅ Good: Guaranteed valid category
lm += "Status: " + select(["pending", "approved", "rejected"], name="status")

# ❌ Bad: May generate typos or invalid values
lm += "Status: " + gen("status", max_tokens=20)
```

### 3. 充分利用令牌修复功能

```python
# Token healing is enabled by default
# No special action needed - just concatenate naturally
lm += "The capital is " + gen("capital")  # Automatic healing
```

### 4. 使用停止序列

```python
# ✅ Good: Stop at newline for single-line outputs
lm += "Name: " + gen("name", stop="\n")

# ❌ Bad: May generate multiple lines
lm += "Name: " + gen("name", max_tokens=50)
```

### 5. 创建可复用函数

```python
# ✅ Good: Reusable pattern
@guidance
def generate_person(lm):
    lm += "Name: " + gen("name", stop="\n")
    lm += "\nAge: " + gen("age", regex=r"[0-9]+")
    return lm

# Use multiple times
lm = generate_person(lm)
lm += "\n\n"
lm = generate_person(lm)
```

### 6. 平衡约束条件

```python
# ✅ Good: Reasonable constraints
lm += gen("name", regex=r"[A-Za-z ]+", max_tokens=30)

# ❌ Too strict: May fail or be very slow
lm += gen("name", regex=r"^(John|Jane)$", max_tokens=10)
```

## 与其他方案的对比

| 功能特性 | Guidance | Instructor | Outlines | LMQL |
|---------|----------|------------|----------|------|
| 正则表达式限制 | ✅ 支持 | ❌ 不支持 | ✅ 支持 | ✅ 支持 |
| 语法支持 | ✅ 基于CFG | ❌ 不支持 | ✅ 基于CFG | ✅ 基于CFG |
| Pydantic验证 | ❌ 不支持 | ✅ 支持 | ✅ 支持 | ❌ 不支持 |
| 令牌修复功能 | ✅ 支持 | ❌ 不支持 | ✅ 支持 | ❌ 不支持 |
| 本地模型 | ✅ 支持 | ⚠️ 功能有限 | ✅ 支持 | ✅ 支持 |
| API模型 | ✅ 支持 | ✅ 支持 | ⚠️ 功能有限 | ✅ 支持 |
| Python风格语法 | ✅ 支持 | ✅ 支持 | ✅ 支持 | ❌ 类SQL语法 |
| 学习曲线 | 较低 | 较低 | 中等 | 较高 |

**何时选择 Guidance：**
- 需要正则表达式或语法限制
- 需要令牌修复功能
- 需要构建带有控制流的复杂工作流
- 使用本地模型（如Transformers、llama.cpp）
- 偏好Python风格的语法

**何时选择其他方案：**
- Instructor：需要具备自动重试功能的Pydantic验证
- Outlines：需要JSON模式验证
- LMQL：偏好声明式查询语法

## 性能特点

**延迟降低：**
- 对于有约束的输出，其速度比传统提示方式快30-50%
- 令牌修复功能可减少不必要的重新生成
- 语法限制能有效避免无效令牌的生成

**内存占用：**
- 相较于无约束生成方式，内存开销极低
- 语法规则会在首次使用后进行缓存
- 推理时能高效过滤令牌

**令牌效率：**
- 避免在无效输出上浪费令牌
- 无需重复尝试的循环
| 直接获得有效输出 |

## 资源链接

- **文档**：https://guidance.readthedocs.io  
- **GitHub 仓库**：https://github.com/guidance-ai/guidance（星标数超过 18,000 个）  
- **笔记本示例**：https://github.com/guidance-ai/guidance/tree/main/notebooks  
- **Discord 社区**：可获取社区支持  

## 相关内容

- `references/constraints.md` —— 详尽的正则表达式与语法模式说明  
- `references/backends.md` —— 各后端特有的配置指南  
- `references/examples.md` —— 可直接用于实际项目的示例代码


