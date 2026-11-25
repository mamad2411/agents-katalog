---
name: mergeable-feature-dev
description: 在新模块开发或跨模块重构时，强制分离脚手架与交付件，保障"本地独立可运行"与"低成本可合并"同时成立。触发词：可直接合并、低成本交接、独立运行、脚手架、交付层、重构合并。
---

# Mergeable Feature Dev

用于解决以下矛盾：

- 本地研发需要独立可运行（快迭代）
- 主仓合并需要最小差异（低风险）

核心方法：**集成边界先行 + 双层目录隔离 + 单一职责 PR**。

---

## 何时使用

满足任一条件即使用：

1. 新建模块/子系统
2. 跨模块重构
3. 用户明确要求"可直接合并、低成本交接"
4. 你发现改动会同时涉及 online + training/scripts/demo

不用于：

- 单文件补丁
- 小范围 bugfix
- 纯文档任务

---

## 执行流程

### Step 1: 集成边界扫描（编码前）

扫描并输出 4 项：

1. **必须复用的现有抽象**
2. **禁止重写的能力**
3. **交付接口定义（对外暴露）**
4. **需要人类确认的边界项**

推荐扫描路径：

- `src/<project_repo>/component/`
- `src/<project_repo>/config/`
- `src/<project_repo>/vo/`
- 目标模块同级目录

搜索模板（项目级 + 模块内部重复检测）：

```bash
# 项目级：已有公共能力
rg "yaml.safe_load|get_texts_embedding_async|Logger\(__name__\)|Result\.(success|failed)" src

# 模块内部：检查新模块各文件是否有重复定义
rg "^def |^class " src/<project_repo>/service/intent/vector_intent/ --no-heading | sort -t: -k2 | uniq -d -f1
```

### Step 2: 双层目录初始化

```text
feature_module/
  ├── __init__.py
  ├── core_logic.py
  ├── config.py
  └── _standalone/
      ├── __init__.py
      ├── mock_xxx.py
      ├── demo_server.py
      └── test_local.py
```

硬约束：

- 交付层禁止 import `_standalone`
- 交付层禁止内联降级逻辑（`try: import X except: mock`）
- `_standalone/` 必须在 `.gitignore`
- 脚手架代码不进入首个合并 PR

### Step 3: 用依赖注入隔离本地能力

Python 模板：

```python
from typing import Any, Callable, Optional


class FeatureService:
    def __init__(
        self,
        storage: Optional[Any] = None,
        embed_fn: Optional[Callable[..., Any]] = None,
    ):
        self.storage = storage or existing_project_storage
        self.embed_fn = embed_fn or existing_project_embed_fn
```

本地脚手架仅在 `_standalone` 注入 mock：

```python
service = FeatureService(
    storage=LocalMockStorage(),
    embed_fn=local_mock_embed,
)
```

### Step 4: 提取共享核心消除重复分支

当两个方法仅在"数据来源"上不同时，提取共享核心：

**反面示例**（validator.py 实际情况：`validate` 和 `validate_on_collection` 各 ~60 行几乎相同）：

```python
# BAD: 60 行逻辑复制，仅 matcher 调用不同
async def validate(self, golden_path): ...
async def validate_on_collection(self, collection, golden_path): ...
```

**正面模板**：

```python
async def _run_validation(
    self, match_fn: Callable[[str], Awaitable[MatchResult]], golden_path: Path
) -> ValidationResult:
    """共享核心：遍历用例、聚合统计、返回结果。"""
    payload = self._load_cases(Path(golden_path))
    # ... 共享的遍历和统计逻辑 ...
    return ValidationResult(...)

async def validate(self, golden_path=config.GOLDEN_TEST_PATH):
    return await self._run_validation(self.matcher.match, golden_path)

async def validate_on_collection(self, collection, golden_path=config.GOLDEN_TEST_PATH):
    match_fn = lambda text: self.matcher.match_with_collection(text=text, collection=collection)
    return await self._run_validation(match_fn, golden_path)
```

### Step 5: PR 拆分决策树

```text
是否同时改 online + offline + scripts + docs ?
  是 -> 拆分 PR
       PR1: 在线热路径（可直接合并）
       PR2: 训练/校准链路
       PR3: 脚本与报告
       PR4: 文档与运营SOP
  否 -> 单 PR，但必须保持单一关注点
```

---

## 提交前检查（必须全部通过）

- [ ] 交付层无 `_standalone` 依赖
- [ ] 交付层无内联降级逻辑（`try: import X except: mock`）
- [ ] 无重复实现（YAML/embedding/logger/Result）
- [ ] 新模块内部无跨文件重复定义
- [ ] `FORCE_*` 默认值为 `False`
- [ ] 提交内容单一关注点
- [ ] diff 规模可审阅（建议净增 < 500 行）

---

## 常见陷阱

1. 为了本地跑通，直接在交付层写 mock/脚本
2. 同时提交在线逻辑和训练脚本，导致评审噪音
3. 重写项目已有工具（例如 yaml 加载、响应封装）
4. 把实验开关默认打开（`FORCE_* = True`）
5. 在交付层文件里写 `try: import private_sdk except: class FakeXxx` 降级——这等于把脚手架逻辑嵌入了交付代码
6. 新模块的两个文件各自定义同一个工具函数（如 `_normalize_vector`），造成模块内部冗余
7. 两个方法仅在"数据来源参数"不同就整段复制，不提取共享核心

---

## 输出要求

使用本 Skill 时，先给出：

1. 集成边界清单（四项）
2. PR 拆分建议（按关注点）
3. 交付件 vs 脚手架文件清单

然后再进入编码。
