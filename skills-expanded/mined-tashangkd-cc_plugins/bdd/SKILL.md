---
name: bdd
description: 行为驱动开发（BDD）流程助手。用 Given-When-Then 描述验收标准，包含 Feature 文件管理、步骤定义实现。用户提到 BDD、验收测试、Gherkin 时使用。
user-invocable: true
---

# BDD 行为驱动开发

> **业务语言描述测试，连接需求与代码**

用自然语言描述验收标准，让业务、开发、测试达成共识。

---

## 快捷命令

```bash
/bdd                 # 交互式引导
/bdd feature         # 创建 Feature 文件
/bdd step            # 实现步骤定义
/bdd run             # 运行 BDD 测试
```

---

## 1. BDD 与 TDD 分层

```
┌─────────────────────────────────────────┐
│  BDD - 验收测试 (behave)                │
│  Feature: 用户登录                       │
│  Scenario: 错误密码登录                  │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  TDD - 单元测试 (pytest)                │
│  def test_login(): ...                  │
└─────────────────────────────────────────┘
```

| 层次 | 工具 | 关注点 |
|------|------|--------|
| **E2E/验收** | behave | 业务场景 |
| **集成** | pytest | 模块交互 |
| **单元** | pytest | 函数逻辑 |

---

## 2. Gherkin 语法

### 2.1 基本结构

```gherkin
Feature: [功能名称]

  Scenario: [场景名称]
    Given [前置条件]
    When [执行操作]
    Then [预期结果]
```

### 2.2 关键字

| 关键字 | 用途 | 示例 |
|--------|------|------|
| `Feature` | 功能描述 | `Feature: 用户登录` |
| `Scenario` | 具体场景 | `Scenario: 使用错误密码` |
| `Given` | 前置条件 | `Given 用户在登录页` |
| `When` | 执行动作 | `When 点击登录按钮` |
| `Then` | 验证结果 | `Then 显示错误提示` |
| `And` | 补充条件 | `And 输入用户名` |

---

## 3. 项目结构

```
project/
├── features/
│   ├── README.md              # Feature 索引（自动维护）
│   ├── login.feature          # Gherkin 场景
│   └── steps/
│       └── login_steps.py     # 步骤定义
└── environment.py             # 环境配置
```

---

## 4. 步骤定义

```python
from behave import given, when, then

@given('用户在登录页面')
def step_login_page(context):
    context.page = LoginPage()

@when('输入用户名 "{username}" 和密码 "{password}"')
def step_input_credentials(context, username, password):
    context.page.login(username, password)

@then('显示错误消息 "{message}"')
def step_check_error(context, message):
    assert context.page.error == message
```

---

## 5. 运行命令

| 场景 | 命令 |
|------|------|
| 运行全部 | `behave` |
| 特定文件 | `behave features/login.feature` |
| 特定场景 | `behave --name="错误密码"` |
| 跳过标签 | `behave --tags=~slow` |

---

## 6. Git 提交规范

| 阶段 | 前缀 | 示例 |
|------|------|------|
| 创建 Feature | `test:` | `test: 添加登录功能场景` |
| 实现步骤 | `test:` | `test: 实现登录步骤定义` |
| 修复场景 | `fix:` | `fix: 修复登录场景断言` |

---

**业务共识 → 可执行文档 → 自动化测试**
