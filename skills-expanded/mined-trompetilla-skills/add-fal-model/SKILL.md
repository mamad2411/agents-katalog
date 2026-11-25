---
name: add-fal-model
description: 为 V3 API 添加新的 Fal AI 模型。当用户要添加 fal 模型、配置新模型、或提供 fal.ai 模型文档链接时使用此 skill。
---

# 添加 Fal 模型到 V3

## 概述

本 skill 指导如何将新的 Fal AI 模型集成到 V3 API 系统中。

### 架构说明

V3 系统支持两个入口访问同一套模型：

```
┌─────────────┐     ┌─────────────┐
│   API 入口   │     │   MCP 入口   │
│ /api/v3/tasks│     │ submit_task │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └───────┬───────────┘
               ▼
       ┌───────────────┐
       │ TaskServiceV3 │
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │   Executor    │  ← 统一执行器
       │ (get_price)   │  ← 统一价格（3种模式）
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │  Fal API 调用  │
       └───────────────┘
```

**关键点**：
- 模型只需注册一次，API 和 MCP 两个入口自动可用
- 执行器中的 `SUPPORTED_CHANNELS` 控制支持的通道
- 价格配置在执行器中统一管理（支持 3 种定价模式：固定/按秒/按时长选项）
- 添加完成后需分别测试两个入口确保正常工作

## 前置输入

需要用户提供 **fal 模型文档链接**（如 `https://fal.ai/models/fal-ai/xxx`），从中提取：
- 模型 ID（如 `fal-ai/flux/schnell`）
- **输入媒体类型**：TEXT / IMAGE / VIDEO / AUDIO（根据必填参数判断）
- **输出媒体类型**：IMAGE / VIDEO / AUDIO
- 输入参数（必填/可选、类型、范围、默认值、**示例值**）
- **输出格式及示例**（来自 Output Schema）
- **定价信息及计费方式**（从 fal Playground 页面底部获取）

### 定价类型判断（关键！）

Fal 模型有不同的计费方式，**必须先判断计费类型再实现执行器**：

| 计费方式 | Fal 页面显示 | 系统实现 | 适用场景 | 执行器参考 |
|---------|------------|---------|---------|-----------|
| **固定每次** | `$0.025 per request` | `PRICE_MAP` | 图像生成、简单处理 | `seedream_executor.py` |
| **按秒计费** | `$0.05 per second` | `PRICE_PER_SECOND` | 视频驱动/动作迁移/音频驱动 | `omnihuman_executor.py`、`dreamactor_executor.py` |
| **按时长选项** | `$0.05 for 5s, $0.10 for 10s` | `PRICE_MAP` (嵌套) | 视频生成（用户选时长） | `wan_executor.py`、`sora_executor.py` |

**如何判断**：
- 打开 fal 模型的 **Playground 页面**，页面底部会显示 `Your request will cost $X.XX per second` 或 `$X.XX per request`
- 如果是 "per second" → 使用 **按秒计费** 模式
- 如果是固定价格但有 duration 参数 → 使用 **按时长选项** 模式
- 如果是固定价格且无 duration 参数 → 使用 **固定每次** 模式

## 添加流程

### 步骤 1：模型注册表

**文件**: `translate_api/app/api/v3/transports/mcp/model_registry.py`

```python
register_model(ModelInfo(
    id="fal-ai/xxx/model-name",           # 模型唯一标识
    name="模型显示名称",                    # 用户可见名称
    category=ModelCategory.IMAGE,          # IMAGE / VIDEO / AUDIO
    task_type=TaskType.TEXT_TO_IMAGE,     # t2i / i2i / t2v / i2v / v2v / t2a
    description="模型描述",
    fal_model="fal-ai/xxx/real-path",     # 可选：实际 API 路径（如果与 id 不同）
    input_media=[MediaType.TEXT, MediaType.IMAGE],  # 输入媒体类型
    output_media=MediaType.VIDEO,                    # 输出媒体类型
    output_example={                                 # 输出示例（来自 Fal 文档 Output Schema）
        "video": {
            "content_type": "video/mp4",
            "url": "https://example.fal.media/output.mp4"
        },
        "seed": 123456
    },
    parameters=[
        ModelParameter(
            name="prompt", 
            type="string", 
            required=True, 
            description="提示词",
            examples=["Fal 文档中的示例提示词"]  # 使用 Fal 文档中的真实示例
        ),
        ModelParameter(
            name="image_url",
            type="string",
            required=True,
            description="输入图片 URL",
            examples=["https://v3b.fal.media/files/xxx.png"]  # 使用 Fal 文档中的真实示例链接
        ),
        # 根据文档添加其他参数...
    ]
))
```

**重要**：
- **参数 examples 必须使用 Fal 文档中的真实示例链接**，不要使用 `example.com` 等占位符
- **output_example 必须来自 Fal 文档的 Output Schema 示例**

**媒体类型**（`MediaType` 枚举）：
- `MediaType.TEXT` - 文本输入
- `MediaType.IMAGE` - 图像输入/输出
- `MediaType.VIDEO` - 视频输入/输出
- `MediaType.AUDIO` - 音频输入/输出

**参数类型**: `string` / `integer` / `number` / `boolean` / `array`

**通用参数可复用**:
- `IMAGE_SIZE_PARAM` - 图像尺寸
- `NUM_IMAGES_PARAM` - 图像数量
- `DURATION_PARAM` - 视频时长
- `ASPECT_RATIO_PARAM` - 视频宽高比

### 步骤 2：执行器

**目录**: `translate_api/app/api/v3/executors/`
- 图像模型: `image/`
- 视频模型: `video/`

**选择策略**:
- **同系列模型** → 更新现有执行器的 `SUPPORTED_MODELS` 列表
- **新系列模型** → 创建新执行器文件

**执行器需实现**:

| 属性/方法 | 说明 |
|----------|------|
| `SUPPORTED_MODELS` | 支持的模型列表（支持 `*` 通配符） |
| `SUPPORTED_CHANNELS` | 支持的通道 `[Channel.API]` |
| `validate_params()` | 参数验证 |
| `transform_params()` | 用户输入 → API 格式 |
| `transform_result()` | API 返回 → 统一格式 |
| `get_endpoint()` | 获取 API 端点 |
| `get_params_schema()` | JSON Schema 参数定义 |
| `get_price()` | 计算价格（积分） |

**基类选择**:
- 图像: `BaseExecutor, ImageExecutorMixin`
- 视频: `BaseExecutor, VideoExecutorMixin`

**价格换算规则**:

```
┌─────────────────────────────────────────────────┐
│  1 美元 = 400 积分  │  1 积分 = 0.0025 美元    │
└─────────────────────────────────────────────────┘
```

**换算示例**:
| Fal 定价（美元） | 系统价格（积分） | 计算公式 |
|-----------------|-----------------|---------|
| $0.003 | 1 | 0.003 × 400 ≈ 1（向上取整） |
| $0.01 | 4 | 0.01 × 400 = 4 |
| $0.025 | 10 | 0.025 × 400 = 10 |
| $0.05 | 20 | 0.05 × 400 = 20 |
| $0.10 | 40 | 0.10 × 400 = 40 |
| $0.50 | 200 | 0.50 × 400 = 200 |
| $1.00 | 400 | 1.00 × 400 = 400 |

#### 定价模式 A：固定每次计费（PRICE_MAP）

适用于：图像生成、简单视频处理等按次收费的模型。

```python
# 执行器属性
PRICE_MAP = {
    "fal-ai/xxx/model-name": 10,  # $0.025 × 400 = 10 积分/次
}

# get_price 实现
def get_price(self, model: str, params: Dict[str, Any]) -> float:
    return self.PRICE_MAP.get(model, 10)
```

**参考**: `seedream_executor.py`、`flux2_executor.py`

#### 定价模式 B：按秒计费（PRICE_PER_SECOND）⭐

适用于：输入视频/音频驱动类模型（如动作迁移、音频驱动视频），费用由输入媒体时长决定。

**特征**：Fal Playground 页面显示 `$X.XX per second`

```python
# 执行器属性
PRICE_PER_SECOND = 20   # $0.05/秒 × 400 = 20 积分/秒
MIN_SECONDS = 3          # 最低计费秒数
MAX_DURATION = 30        # 最大时长（秒）
DEFAULT_ESTIMATED_DURATION = 10  # 获取时长失败时的估算值

# get_price 实现 — 尝试探测输入媒体时长
def get_price(self, model: str, params: Dict[str, Any]) -> float:
    video_url = params.get("video_url", "")  # 或 audio_url
    duration = None

    if video_url:
        try:
            from app.utils.video_utils import get_video_duration_sync
            duration = get_video_duration_sync(video_url, timeout=8.0)
        except Exception:
            pass

    if duration is None:
        duration = self.DEFAULT_ESTIMATED_DURATION  # 降级估算

    import math
    billable = math.ceil(min(max(duration, self.MIN_SECONDS), self.MAX_DURATION))
    return billable * self.PRICE_PER_SECOND
```

> **重要**: 系统会自动根据 `PRICE_PER_SECOND`、`MIN_SECONDS`、`MAX_DURATION` 属性生成正确的定价展示信息（`/docs` 接口），无需额外配置。

**参考**: `omnihuman_executor.py`、`dreamactor_executor.py`、`kling_executor.py`（Motion Control 部分）

#### 定价模式 C：按时长选项计费（PRICE_MAP 嵌套）

适用于：用户可选择视频时长/分辨率的视频生成模型。

```python
# 按模型+分辨率嵌套
PRICE_MAP = {
    "wan/v2.6/image-to-video": {"720p": 20, "1080p": 30},  # 积分/秒
}

# 或按版本+时长嵌套
PRICE_MAP = {
    "master": {"5": 50, "10": 100},
    "pro": {"5": 30, "10": 60},
    "standard": {"5": 15, "10": 30},
}

# get_price 实现
def get_price(self, model: str, params: Dict[str, Any]) -> float:
    duration = int(params.get("duration", 5))
    resolution = params.get("resolution", "720p")
    price_per_second = self.PRICE_MAP.get(model, {}).get(resolution, 20)
    return duration * price_per_second
```

**参考**: `wan_executor.py`、`sora_executor.py`、`seedance_executor.py`

### 步骤 3：注册执行器

**文件**: `translate_api/app/api/v3/executors/factory.py`

```python
def _init_executors(self):
    from .image.new_model_executor import NewModelExecutor  # 添加导入
    
    self._executor_classes = [
        FluxExecutor,
        SeedreamExecutor,
        KlingExecutor,
        NewModelExecutor,  # 添加到列表
    ]
```

### 步骤 4（可选）：传输层

**文件**: `translate_api/app/api/v3/transports/api/fal_transport.py`

仅当模型前缀不在已支持列表（`fal-ai/`、`st-ai/`）时需要修改。

### 步骤 5：创建模型 Skill 文件

为新模型创建专用的 Skill 文件，方便 AI 助手理解如何调用。

**目录**: `.cursor/skills/{skill-name}/SKILL.md`

**创建步骤**:

```bash
# 1. 创建 skill 目录
mkdir -p .cursor/skills/{skill-name}

# 2. 创建 SKILL.md 文件
```

> **注意**: Skills 开发目录为 `.cursor/skills/`，运行 `python upload_skills_zip.py` 会自动同步到 `translate_api/app/api/v3/skills/` 并上传到云端。

**SKILL.md 模板**:

```markdown
---
name: {skill-name}
description: 使用 {模型显示名} 生成图像/视频。当用户想要{功能描述}时使用此 skill。
---

# {模型显示名}

{模型简介}

## 可用模型

| 模型 ID | 功能 | 说明 |
|--------|------|------|
| `{model-id}` | {功能} | {说明} |

## 工作流

### 1. 调用 submit_task

使用 MCP 工具 `submit_task` 提交任务：

\`\`\`json
{
  "model_id": "{model-id}",
  "parameters": {
    "prompt": "用户的提示词",
    // 其他参数...
  }
}
\`\`\`

### 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| prompt | string | **是** | - | 提示词 |
| {param} | {type} | {是/否} | {default} | {说明} |

## 查询任务状态

提交任务后会返回 `task_id`，使用 `get_task` 查询结果：

\`\`\`json
{
  "task_id": "返回的任务ID"
}
\`\`\`

任务状态：
- `pending` - 排队中
- `processing` - 处理中
- `completed` - 完成，结果在 `result` 中
- `failed` - 失败，查看 `error` 字段

## 完整示例

**用户请求**：{示例请求}

**执行步骤**：

1. 调用 `submit_task`：
\`\`\`json
{完整参数示例}
\`\`\`

2. 获取 `task_id` 后调用 `get_task` 查询结果

## 提示词技巧

1. {技巧1}
2. {技巧2}
```

**参考示例**: `.cursor/skills/sora-2/SKILL.md`

### 步骤 6：更新模型-Skill 映射

**文件**: `.cursor/skills/__init__.py`

在 `MODEL_SKILL_MAPPING` 中添加模型与 Skill 的对应关系：

```python
MODEL_SKILL_MAPPING: Dict[str, List[str]] = {
    # ... 现有映射 ...
    
    # 新模型映射（一个模型可对应多个 Skills）
    "fal-ai/xxx/model-name": ["skill-name"],
    
    # 如果多个模型共用同一个 Skill
    "fal-ai/xxx/model-v1": ["skill-name"],
    "fal-ai/xxx/model-v2": ["skill-name"],
    
    # 如果一个模型需要多个 Skills
    "fal-ai/xxx/complex-model": ["skill-basic", "skill-advanced", "skill-tips"],
}
```

## 步骤 7：测试验证

模型添加完成后，必须验证 **模型信息**、**API 入口**、**MCP 入口** 和 **扣费逻辑** 都正确工作。

### 7.1 获取模型信息验证

首先验证模型信息是否正确注册，参数定义是否完整。

#### API 获取模型信息

**端点**: `GET /api/v3/models/{model_id}`

```python
import requests

BASE_URL = "http://127.0.0.1:8002"
MODEL_ID = "fal-ai/xxx/model-name"

response = requests.get(f"{BASE_URL}/api/v3/models/{MODEL_ID}")
data = response.json()

print("模型信息:")
print(f"  名称: {data['data']['name']}")
print(f"  执行器: {data['data']['executor']}")
print(f"  支持通道: {data['data']['channels']}")
print(f"  参数 Schema: {data['data']['params_schema']}")
```

#### MCP 获取模型信息

**工具**: `get_model_info`

```json
{
  "tool": "get_model_info",
  "arguments": {
    "model_id": "fal-ai/xxx/model-name"
  }
}
```

**预期返回**:
```json
{
  "success": true,
  "model": {
    "id": "fal-ai/xxx/model-name",
    "name": "模型显示名称",
    "category": "image",
    "task_type": "text_to_image",
    "description": "模型描述",
    "parameters": {
      "type": "object",
      "properties": {
        "prompt": {
          "type": "string",
          "description": "提示词"
        }
      },
      "required": ["prompt"]
    }
  }
}
```

#### 验证检查项

| 检查项 | 说明 | 验证方法 |
|-------|------|---------|
| 模型存在 | 能通过 ID 获取到模型 | `success: true` |
| 基本信息 | id/name/category/task_type 正确 | 对比 `model_registry.py` 配置 |
| 参数完整 | 所有参数都有定义 | 对比 fal 文档 |
| 必填参数 | `required` 数组正确 | 必填参数都在 required 中 |
| 参数类型 | type 正确（string/integer/number/boolean/array） | 对比 fal 文档 |
| 默认值 | default 值正确 | 对比 fal 文档 |
| 枚举值 | enum 选项正确（如 aspect_ratio） | 对比 fal 文档 |
| 范围限制 | minimum/maximum 正确 | 对比 fal 文档 |
| 描述信息 | description 清晰准确 | 可读性检查 |

#### 参数 Schema 示例验证

确保 `params_schema` 格式正确：

```python
# 验证脚本
expected_params = {
    "prompt": {"type": "string", "required": True},
    "image_size": {"type": "string", "enum": ["square_hd", "landscape_4_3", ...]},
    "num_images": {"type": "integer", "minimum": 1, "maximum": 4, "default": 1},
    # ... 其他参数
}

actual_schema = data['data']['params_schema']

for param_name, expected in expected_params.items():
    if param_name not in actual_schema.get('properties', {}):
        print(f"❌ 缺少参数: {param_name}")
        continue
    
    actual = actual_schema['properties'][param_name]
    
    # 检查类型
    if actual.get('type') != expected.get('type'):
        print(f"❌ {param_name} 类型错误: 预期 {expected.get('type')}, 实际 {actual.get('type')}")
    
    # 检查枚举值
    if 'enum' in expected and actual.get('enum') != expected['enum']:
        print(f"❌ {param_name} 枚举值不一致")
    
    # 检查必填
    required_list = actual_schema.get('required', [])
    is_required = param_name in required_list
    if is_required != expected.get('required', False):
        print(f"❌ {param_name} 必填设置错误")

print("✅ 参数验证完成")
```

### 7.2 API 任务测试

**端点**: `POST /api/v3/tasks`

```python
import requests

BASE_URL = "http://127.0.0.1:8002"  # 本地开发
API_KEY = "your-api-key"

# 提交任务
response = requests.post(
    f"{BASE_URL}/api/v3/tasks",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "fal-ai/xxx/model-name",
        "parameters": {
            "prompt": "测试提示词",
            # 其他参数...
        }
    }
)
result = response.json()
task_id = result.get("task_id")
price = result.get("price")  # 记录扣费金额
print(f"任务ID: {task_id}, 扣费: {price}")

# 查询任务
response = requests.get(
    f"{BASE_URL}/api/v3/tasks/{task_id}",
    headers={"Authorization": f"Bearer {API_KEY}"}
)
print(response.json())
```

### 7.2 MCP 测试

通过 MCP 工具调用测试：

**submit_task**:
```json
{
  "tool": "submit_task",
  "arguments": {
    "model_id": "fal-ai/xxx/model-name",
    "parameters": {
      "prompt": "测试提示词"
    }
  }
}
```

**get_task**:
```json
{
  "tool": "get_task", 
  "arguments": {
    "task_id": "返回的任务ID"
  }
}
```

**验证返回**:
- `task_id` - 任务 ID
- `price` - 扣费金额（积分）
- `balance` - 用户剩余余额

### 7.3 定价展示验证

**端点**: `GET /api/v3/models/{model_id}/docs`

定价展示由系统根据执行器属性自动生成，必须验证展示信息与实际扣费一致。

```bash
curl -s 'http://127.0.0.1:8002/api/v3/models/{MODEL_ID}/docs' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('data',{}).get('pricing',{}), indent=2, ensure_ascii=False))"
```

**按定价模式检查**:

| 定价模式 | 期望 `price_type` | 关键字段 | 说明 |
|---------|------------------|---------|------|
| 固定每次 (PRICE_MAP) | `quantity_based` 或 `fixed` | `base_price` = 积分数 | 展示每次调用价格 |
| 按秒计费 (PRICE_PER_SECOND) | `per_second` | `per_second` = 积分/秒 | 展示每秒价格、最低秒数、最大时长 |
| 按时长选项 (PRICE_MAP 嵌套) | `duration_price` | `examples` 含各时长/分辨率价格 | 展示不同参数组合价格 |

**按秒计费模型的预期返回示例**:
```json
{
  "price_type": "per_second",
  "per_second": 20,
  "price_description": "按视频时长计费：20 积分/秒，最低 3 秒起（最长 30 秒）",
  "price_factors": ["video_url (视频时长)"],
  "examples": [
    {"description": "5秒视频", "price": 100},
    {"description": "10秒视频", "price": 200},
    {"description": "30秒视频", "price": 600}
  ]
}
```

> **自动生成规则**: 系统会自动检测执行器上的 `PRICE_PER_SECOND`、`MIN_SECONDS`、`MAX_DURATION` 属性来生成定价展示。如果这些属性正确配置，展示信息会自动正确。

### 7.4 扣费逻辑验证

**扣费流程**:
```
API/MCP 请求 → TaskServiceV3.create_task()
    └─> v3_pricing.calculate_and_deduct()
        └─> executor.get_price()  # 计算价格
            └─> deduct_user_money_by_id()  # 实际扣费
```

**验证点**:

| 检查项 | 说明 |
|-------|------|
| 执行器价格属性 | `PRICE_MAP` 或 `PRICE_PER_SECOND` 已正确配置 |
| 扣费金额单位 | 积分（1元=100积分），类型为 int |
| 扣费时机 | 任务创建时立即扣费 |
| 退款机制 | 任务失败时自动退款 |

**余额验证测试**:
```python
# 扣费前查询余额
balance_before = get_user_balance(user_id)

# 执行任务
result = submit_task(model_id, parameters)
deducted_price = result.get("price")

# 扣费后验证
balance_after = get_user_balance(user_id)
actual_deducted = balance_before - balance_after

assert actual_deducted == deducted_price, f"扣费不一致！预期: {deducted_price}, 实际: {actual_deducted}"
```

**数据库记录检查**:
- `FalTasks` 表：`money` 字段记录扣费金额
- `FinancialTransactions` 表：交易记录
- `PointsDetail` 表：积分明细

## 检查清单

```
添加 Fal 模型进度：

【模型注册】
- [ ] 获取 fal 模型文档链接
- [ ] 解析文档提取参数定义
- [ ] 在 model_registry.py 添加模型配置
- [ ] input_media: 输入媒体类型已设置（TEXT/IMAGE/VIDEO/AUDIO）
- [ ] output_media: 输出媒体类型已设置
- [ ] output_example: 输出示例已从 Fal 文档复制
- [ ] 参数 examples: 使用 Fal 文档中的真实示例链接（非 example.com）

【执行器 + 定价】
- [ ] 判断定价模式（固定/按秒/按时长选项）
- [ ] 创建/更新执行器
- [ ] 定价模式A（固定）: 配置 PRICE_MAP
- [ ] 定价模式B（按秒）: 配置 PRICE_PER_SECOND / MIN_SECONDS / MAX_DURATION
- [ ] 定价模式C（按时长）: 配置 PRICE_MAP 嵌套结构
- [ ] 实现 get_price() 方法
- [ ] 在 factory.py 注册执行器

【Skill 文件】
- [ ] 创建 Skill 文件（.cursor/skills/{skill-name}/SKILL.md）
- [ ] 更新 MODEL_SKILL_MAPPING（.cursor/skills/__init__.py）
- [ ] 运行 `python upload_skills_zip.py` 同步到部署目录

【模型信息验证】
- [ ] API: GET /api/v3/models/{model_id} 返回正确
- [ ] MCP: get_model_info 工具返回正确
- [ ] 基本信息: id/name/category/task_type 正确
- [ ] 输入输出: input_media/output_media 正确
- [ ] 输出示例: output_example 包含正确的示例
- [ ] 参数完整: 所有参数都已定义
- [ ] 必填参数: required 数组正确
- [ ] 参数类型: type 类型正确
- [ ] 默认值: default 值正确
- [ ] 枚举值: enum 选项正确
- [ ] 范围限制: minimum/maximum 正确
- [ ] 参数示例: examples 使用真实链接
- [ ] 描述信息: description 清晰准确

【API 任务测试】
- [ ] POST /api/v3/tasks 提交任务成功
- [ ] GET /api/v3/tasks/{id} 查询任务成功
- [ ] 任务执行完成，结果正确

【MCP 任务测试】
- [ ] submit_task 工具调用成功
- [ ] get_task 查询结果正确
- [ ] 返回 task_id、price、balance 信息

【定价展示验证】
- [ ] GET /api/v3/models/{model_id}/docs 定价信息正确
- [ ] price_type 与定价模式匹配（per_second / duration_price / quantity_based）
- [ ] price_description 描述准确（包含单价、最低秒数、最大时长等）
- [ ] examples 价格示例计算正确

【扣费验证】
- [ ] 扣费金额与执行器 get_price() 计算一致
- [ ] 扣费前后余额差值正确
- [ ] 任务失败时退款成功
```

## 文件结构总览

```
translate_api/app/api/v3/
├── transports/
│   ├── mcp/
│   │   ├── model_registry.py  ← 步骤 1: 模型注册
│   │   └── tools.py           ← MCP 工具入口 (submit_task/get_task)
│   └── api/
│       └── fal_transport.py   ← 步骤 4: API 传输层
├── executors/
│   ├── factory.py             ← 步骤 3: 注册执行器
│   ├── image/
│   │   └── {model}_executor.py ← 步骤 2: 执行器 + PRICE_MAP
│   └── video/
│       └── {model}_executor.py
├── services/
│   ├── task_service.py        ← 任务创建 + 扣费入口
│   └── pricing_adapter.py     ← V3 计费适配器
└── skills/                    ← 由 upload_skills_zip.py 从 .cursor/skills/ 同步
    ├── __init__.py
    └── {skill-name}/
        └── SKILL.md

.cursor/skills/                ← 开发目录（步骤 5、6 在此目录操作）
├── __init__.py                ← 步骤 6: MODEL_SKILL_MAPPING
└── {skill-name}/
    └── SKILL.md               ← 步骤 5: Skill 文件
```

**入口对应关系**:
| 入口 | 文件 | 端点/工具 |
|-----|------|----------|
| API | `task_api.py` | `POST /api/v3/tasks` |
| MCP | `tools.py` | `submit_task` / `get_task` |

## 详细参考

- 固定计费执行器: 参考 `seedream_executor.py`、`flux2_executor.py`
- 按秒计费执行器: 参考 `omnihuman_executor.py`、`dreamactor_executor.py`
- 按时长选项执行器: 参考 `wan_executor.py`、`sora_executor.py`、`seedance_executor.py`
- 模型注册示例: 参考 `model_registry.py` 中现有模型
- Skill 示例: 参考 `.cursor/skills/sora-2/SKILL.md`

## 快速添加（同系列模型）

如果新模型与现有执行器同系列，只需：

1. 在 `model_registry.py` 添加 `register_model()` 配置
2. 在对应执行器的 `SUPPORTED_MODELS` 添加模型名
3. 在 `PRICE_MAP`（或 `PRICE_PER_SECOND` 等）添加价格
4. 在 `.cursor/skills/__init__.py` 的 `MODEL_SKILL_MAPPING` 添加映射（复用现有 Skill）
5. 运行 `python upload_skills_zip.py` 同步 skills 到部署目录
6. **测试验证**：
   - 模型信息: `GET /api/v3/models/{model_id}` 返回正确
   - 定价展示: `GET /api/v3/models/{model_id}/docs` 的 pricing 字段正确
   - 参数验证: 检查 params_schema 的类型、必填、枚举、默认值
   - API 任务: `POST /api/v3/tasks/create` 提交任务
   - 扣费验证: 金额与执行器 get_price() 计算一致

完成！
