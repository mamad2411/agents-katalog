---
name: test-suite-maintainer
description: 在项目迭代上线前维护和执行全量测试用例集。当用户提到"上线前测试"、"更新测试用例"、"全量测试"、"跑用例"、"维护测试集"、"测试覆盖"、"检测代码变更需要更新哪些测试"时触发此skill。也适用于用户指定功能模块需要添加或更新测试的场景。
---

<SUBAGENT-STOP>
如果你是作为子代理被派发执行特定任务，跳过此skill。
</SUBAGENT-STOP>

# 测试用例集维护

这个skill帮助你维护一份项目全量测试用例与自动化测试脚本，确保迭代过程中测试始终与代码同步。

## 核心概念

**测试清单（test-manifest.yaml）** 是整个skill的核心。它记录：
- 所有功能模块及其测试用例
- 每个用例的状态（active/skip/pending）
- 用例与代码路径的关联关系
- 用例优先级和分类

通过这份清单，你可以：
1. 快速了解项目测试覆盖全貌
2. 检测代码变更后确定哪些测试需要更新
3. 上线前执行全量测试并验证覆盖

## 推荐技术栈

| 项目类型 | 测试框架 | 说明 |
|---------|---------|------|
| Python | pytest | fixture机制强大，插件生态丰富，按模块组织测试 |
| NextJS | Vitest | 与Vite原生集成，速度快，支持项目分隔 |

## 目录结构

测试用例集维护在 `workplace/test/` 目录下：

```
workplace/test/
├── test-manifest.yaml      # 全量用例清单（核心文件）
├── python/                  # Python项目测试
│   ├── conftest.py          # 共享fixtures和配置
│   ├── pytest.ini           # pytest配置（可选）
│   ├── auth/                # 功能模块：认证
│   │   ├── test_login.py    # 登录测试
│   │   └── test_register.py # 注册测试
│   ├── payment/             # 功能模块：支付
│   │   ├── test_checkout.py
│   │   └── test_refund.py
│   └── ...
├── nextjs/                  # NextJS项目测试
│   ├── vitest.config.ts     # Vitest配置
│   ├── setup.ts             # 测试setup文件
│   ├── auth/
│   │   ├── login.test.ts
│   │   ├── register.test.ts
│   ├── payment/
│   │   ├── checkout.test.ts
│   │   └── refund.test.ts
│   └── ...
```

## test-manifest.yaml 格式

```yaml
version: "1.0"
project:
  name: "项目名称"
  python_root: "src/"        # Python代码根目录（相对项目根）
  nextjs_root: "app/"        # NextJS代码根目录

modules:
  auth:                      # 功能模块名
    description: "用户认证模块"
    code_paths:              # 关联的代码路径（用于变更检测）
      - "src/auth/"
      - "app/api/auth/"
    priority: high           # 模块优先级: high/medium/low
    cases:
      - name: "用户登录"
        id: "auth-login-001"
        status: active       # active/skip/pending
        type: unit           # unit/integration/e2e
        script: "python/auth/test_login.py::test_login_success"
        coverage:
          - "src/auth/login.py"
          - "app/api/auth/login/route.ts"
        last_run: "2026-04-15"
        notes: "验证正常登录流程"

      - name: "登录失败处理"
        id: "auth-login-002"
        status: active
        type: unit
        script: "python/auth/test_login.py::test_login_failure"
        coverage: ["src/auth/login.py"]
        last_run: "2026-04-15"
        notes: "验证错误密码、账户锁定等场景"

  payment:
    description: "支付处理模块"
    code_paths: ["src/payment/", "app/api/payment/"]
    priority: high
    cases:
      - name: "支付流程"
        id: "payment-checkout-001"
        status: active
        type: integration
        script: "nextjs/payment/checkout.test.ts"
        coverage: ["src/payment/checkout.py", "app/api/payment/route.ts"]
        last_run: "2026-04-10"
        notes: "完整支付流程测试，需mock支付网关"
```

## 工作流程

### 场景一：迭代上线前执行测试

1. **读取清单** - 从 `workplace/test/test-manifest.yaml` 加载全量用例
2. **筛选执行** - 只执行 `status: active` 的用例
3. **优先级排序** - high > medium > low
4. **运行测试** - 使用对应框架执行
5. **生成报告** - 记录执行结果，更新 `last_run` 字段

执行命令：
```bash
# Python测试
pytest workplace/test/python/ -v --tb=short

# NextJS测试
vitest run --config workplace/test/nextjs/vitest.config.ts

# 指定模块
pytest workplace/test/python/auth/ -v
vitest run --config workplace/test/nextjs/vitest.config.ts auth/
```

### 场景二：代码变更后更新测试

1. **检测变更** - 使用 `git diff` 获取变更文件
2. **关联分析** - 遍历manifest，匹配 `code_paths` 和 `coverage`
3. **识别影响** - 列出所有受影响的测试用例
4. **用户确认** - 展示需要更新的列表，让用户确认范围
5. **更新测试** - 根据代码变更更新对应测试脚本
6. **同步清单** - 更新manifest中的用例描述、状态等

变更检测命令：
```bash
git diff HEAD~5 --name-only          # 最近5次提交
git diff main...feature-branch --name-only  # 分支差异
git diff --cached --name-only        # 暂存区变更
```

### 场景三：新增功能添加测试

1. **确认模块** - 判断新功能属于哪个模块
2. **设计用例** - 分析功能点，设计测试用例列表
3. **编写脚本** - 创建测试文件，实现自动化测试
4. **注册清单** - 在manifest中添加用例记录

## Skill 执行步骤

### Step 1: 理解用户意图

确认用户要做什么：
- **执行测试** - "上线前跑测试"、"执行全量用例"
- **更新测试** - "代码变了，更新相关测试"
- **添加测试** - "新功能完成，添加测试用例"
- **查看覆盖** - "看看测试覆盖情况"

意图不明确时询问澄清。

### Step 2: 读取测试清单

读取 `workplace/test/test-manifest.yaml`：
- 不存在 → 初始化测试集（Step 5）
- 存在 → 解析内容继续

### Step 3: 执行对应操作

**执行测试：**
1. 筛选active用例
2. 按优先级执行
3. 收集结果更新last_run
4. 生成报告

**更新测试：**
1. git diff或用户指定变更范围
2. 匹配manifest关联
3. 列出受影响用例
4. 用户确认后更新脚本和manifest

**添加测试：**
1. 分析功能测试点
2. 创建测试文件
3. manifest注册用例

**查看覆盖：**
1. 统计manifest信息
2. 展示模块覆盖
3. 指出缺失/pending用例

### Step 4: 更新测试清单

任何操作后更新 `test-manifest.yaml`：last_run、状态、新用例、notes

### Step 5: 初始化测试集（如需要）

清单不存在时：
1. 分析项目结构，识别功能模块
2. 设计目录结构
3. 创建manifest骨架
4. 扫描现有测试文件
5. 迁移或创建测试

## 测试脚本编写指南

### Python (pytest)

```python
# workplace/test/python/auth/test_login.py
import pytest

def test_login_success():
    """测试正常登录"""
    # 实现测试

def test_login_failure_wrong_password():
    """测试密码错误"""
    # 实现测试

@pytest.fixture
def mock_user():
    return {"username": "testuser", "password": "testpass"}
```

### NextJS (Vitest)

```typescript
// workplace/test/nextjs/auth/login.test.ts
import { describe, it, expect, beforeEach } from 'vitest'

describe('Login', () => {
  it('should login successfully', async () => {
    // 实现测试
  })

  it('should handle wrong password', async () => {
    // 实现测试
  })
})
```

## 报告格式

执行完成后生成：

```markdown
# 测试执行报告

**执行时间**: 2026-04-20 14:30
**项目**: 项目名称

## 执行统计

| 指标 | 数值 |
|-----|-----|
| 总用例数 | 45 |
| 执行用例 | 42 |
| 通过 | 40 |
| 失败 | 2 |
| 耗时 | 5m32s |

## 模块覆盖

| 模块 | 用例数 | 通过 | 失败 | 覆盖率 |
|-----|-------|-----|-----|-------|
| auth | 12 | 12 | 0 | 100% |
| payment | 8 | 6 | 2 | 75% |

## 失败详情

1. **payment-checkout-001**: 支付流程
   - 错误: Mock支付网关超时
   - 路径: nextjs/payment/checkout.test.ts

## 建议

- 修复payment模块失败用例后可上线
```

## 最佳实践

1. **保持同步** - 代码变更时检查manifest
2. **优先级管理** - 核心模块标记high
3. **状态管理** - 过时用例标记skip而非删除
4. **关联准确** - code_paths和coverage要准确
5. **定期清理** - 清理skip无用用例