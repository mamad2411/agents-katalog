---
name: tdd
description: 测试驱动开发（TDD）流程助手。严格遵循红-绿-重构循环，包含会话状态管理、测试运行策略、Git 提交规范。用户提到 TDD、测试先行、红绿重构时使用。
user-invocable: true
---

# TDD 编程模式

> **快速反馈是 TDD 的核心**

严格遵循测试驱动开发（Test-Driven Development）流程：红 → 绿 → 重构。

---

## 1. TDD 循环

### 1.1 🔴 红 - 编写失败的测试

```bash
pytest tests/test_new_feature.py -v
```

**Git**：`git commit -m "test: 添加 xxx 功能的失败测试"`

### 1.2 🟢 绿 - 编写最少代码使测试通过

```bash
pytest tests/test_new_feature.py -v
```

**Git**：`git commit -m "feat: 实现使测试通过的 xxx 功能"`

### 1.3 ♻️ 重构 - 在测试保护下优化代码

```bash
pytest tests/test_module.py -v
```

**Git**：`git commit -m "refactor: 重构 xxx 功能代码"`

---

## 2. 测试运行策略

| 场景 | 命令 |
|------|------|
| 开发单个功能 | `pytest tests/test_xxx.py` |
| 调试特定测试 | `pytest -k "test_login"` |
| 重跑失败测试 | `pytest --lf` |
| 失败优先 | `pytest --ff` |
| 按类型运行 | `pytest -m unit` |

**提交前验证**：`pytest && uv run ruff check && uv run mypy .`

---

## 3. 测试规范

| 规范 | 要求 |
|------|------|
| **AAA 模式** | Arrange → Act → Assert |
| **命名规范** | `test_<功能>_<条件>_<期望>` |
| **单一职责** | 一个测试一个行为，≤20 行 |
| **测试金字塔** | 单元 70% / 集成 20% / E2E 10% |
| **覆盖率** | 核心 ≥80%，整体 ≥70% |

---

## 4. Git 提交规范

| 阶段 | 前缀 | 示例 |
|------|------|------|
| 红（测试） | `test:` | `test: 添加用户登录的失败测试` |
| 绿（实现） | `feat:` | `feat: 实现用户登录功能` |
| 重构 | `refactor:` | `refactor: 优化登录验证逻辑` |
| 修复 | `fix:` | `fix: 修复登录验证 bug` |

---

## 5. TDD 会话模式

运行 `/tdd` 时自动管理会话状态，保存在 `tmp/tdd-session-<timestamp>.json`。

会话信息包括：
- 当前阶段（红/绿/重构）
- 迭代次数
- 测试文件和结果
- Git commit 数量

```bash
# 查看会话状态
/tdd --status

# 取消会话
rm tmp/tdd-session-*.json
```

---

**快速反馈 → 快速迭代 → 高质量代码**
