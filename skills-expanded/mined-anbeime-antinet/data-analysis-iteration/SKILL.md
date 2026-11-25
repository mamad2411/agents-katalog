---
name: data-analysis-iteration
description: 知易智能知识管家。部署于Windows ARM64的端侧智能数据工作站，通过QNN SDK加速的Qwen2.0-7B/llama3系列实现自然语言驱动的数据分析与知识管理闭环。支持四色卡片生成（蓝/绿/黄/红）、批量处理、OCR识别、知识图谱关联、Agent记忆共享、向量检索、性能测试，基于8-Agent锦衣卫风格协作架构。支持NPU加速部署、模型量化（INT8/INT4）、多模型切换（Qwen2.0-7B-SSD/llama3.1-8b/llama3.2-3b）、并行推理。
dependency:
  python:
    - pandas>=1.5.0
    - openpyxl>=3.0.0
    - pytesseract>=0.3.0
    - Pillow>=9.0.0
    - fastapi>=0.104.0
    - uvicorn>=0.24.0
    - faiss-cpu>=1.7.4
    - sentence-transformers>=2.2.0
    - httpx>=0.25.0
    - python-multipart>=0.0.6
    - pydantic>=2.0.0
    - python-dotenv>=1.0.0
    - aiofiles>=23.0.0
  system:
    - echo "配置venv_arm64虚拟环境（Python 3.12+ ARM64 NPU优化）"
    - echo "设置QNN SDK环境变量：QNN_SDK_ROOT，PATH（如使用NPU加速）"
    - echo "配置GenieAPIService HTTP API（如使用NPU推理）"
    - echo "安装Tesseract OCR：apt-get install tesseract-ocr tesseract-ocr-chi-sim"
---

# 知易智能知识管家

## 任务目标
- 本技能用于：Windows ARM64端侧智能数据工作站，实现数据分析自动化与知识沉淀结构化
- 能力包含：
  1. 自然语言查询解析（如"分析上个月销售趋势"）
  2. 多格式数据读取（CSV/JSON/Excel/图像）
  3. 批量文件处理与自动分类
  4. 8-Agent协作分析（锦衣卫总指挥使/密卷房/通政司/监察院/太史阁/刑狱司/参谋司/驿传司）
  5. 四色卡片生成（蓝/绿/黄/红）
  6. OCR图像文本提取（支持NPU加速）
  7. 知识图谱关联（BGE-M3向量检索）
  8. 可视化报告生成
  9. Agent记忆共享与流转（SQLite数据库）
  10. 知识图谱引导应用
- 触发条件：用户上传数据文件或通过自然语言提出分析需求

## 核心目标

1. **数据分析自动化**：用户自然语言查询触发端侧处理流程
2. **知识沉淀结构化**：生成四色卡片（事实/解释/风险/行动），构建可检索知识图谱
3. **端侧安全与性能**：数据不出域，NPU推理延迟<500ms，本地向量检索响应<100ms

## 前置准备

### 环境配置

#### Python虚拟环境（venv_arm64）
```bash
# 创建ARM64 NPU优化的虚拟环境
python -m venv venv_arm64

# 激活虚拟环境（Windows）
venv_arm64\Scripts\activate.bat

# 验证Python版本
python --version  # 应显示 Python 3.12.10
```

#### QNN SDK环境配置（Windows ARM64）
```bash
# 设置QNN SDK环境变量
set QNN_SDK_ROOT=C:/path/to/qnn/sdk
set PATH=%QNN_SDK_ROOT%/bin;%PATH%
```

#### GenieAPIService配置
```python
# GenieAPIService HTTP API配置
GENIE_API_BASE_URL = "http://localhost:8910"
```

#### 模型配置
```python
# 模型路径配置
MODEL_PATHS = {
    "qwen2.0-7b-ssd": "models/Qwen2.0-7B-SSD-8380-2.34",  # 通用推荐 ⭐️ (~450ms)
    "llama3.1-8b": "models/llama3.1-8b",                    # 更强推理 (~520ms)
    "llama3.2-3b": "models/llama3.2-3b",                     # 最快响应 (~280ms)
    "crnn-int8": "models/crnn-int8",                        # NPU OCR模型 (~50ms)
}

# 使用NPUModelLoader切换模型
from scripts.model_loader import NPUModelLoader

# 使用更小模型（更快）
loader = NPUModelLoader(model_key="llama3.2-3b")
model = loader.load()

# 使用NPU OCR
from scripts.ocr_npu import NPUCREngine
ocr_engine = NPUCREngine(model_path="models/crnn-int8")
result = ocr_engine.extract_text_from_image(image_path)
```

#### NPU OCR配置（新增）⭐
```python
# NPU OCR引擎配置
from scripts.easy_ocr_npu import EasyOCRNPU

# 初始化EasyOCR NPU引擎（推荐）
ocr_engine = EasyOCRNPU(use_mock=False)  # 真实NPU模式

# 单张图像OCR
result = ocr_engine.ocr_single_image(
    image_path="./image.jpg",
    languages=["ch_sim", "eng"]
)

# 批量OCR
batch_result = ocr_engine.ocr_batch(
    image_paths=["./image1.jpg", "./image2.jpg"],
    languages=["ch_sim", "eng"]
)

# 获取引擎信息
info = ocr_engine.get_engine_info()
```

### 依赖说明
```
pandas>=1.5.0
openpyxl>=3.0.0
pytesseract>=0.3.0
Pillow>=9.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
faiss-cpu>=1.7.4
sentence-transformers>=2.2.0
httpx>=0.25.0
python-multipart>=0.0.6
pydantic>=2.0.0
python-dotenv>=1.0.0
aiofiles>=23.0.0
```

### OCR环境配置
```bash
# 安装Tesseract OCR引擎
apt-get install tesseract-ocr tesseract-ocr-chi-sim
```

### 数据目录准备
```bash
# 创建用户数据目录
mkdir -p ./user-data/
mkdir -p ./knowledge-graph/
```

### NPU部署准备（关键）
```bash
# 1. 从高通模型广场下载预转换的QNN格式模型
# 2. 使用QAI AppBuilder将微调模型转换为INT8/INT4精度的QNN格式
# 3. 配置多进程架构，支持四色卡片生成器在独立NPU进程中并行推理
```

## 8-Agent协作架构（锦衣卫风格）

### Agent分工（ARM64 NPU优化版本）

```
用户查询 (U)
    ↓
锦衣卫总指挥使 (Orchestrator) - NPU核心（Qwen2.0-7B-SSD或llama3.1-8b）
    ↓
    ├─── 密卷房 (Preprocessor) - CPU辅助（规则引擎）
    ├─── 查询构建与执行 (Query Builder) - 本地代码（Python + DuckDB）
    ├─── 卡片生成与分类 (Card Classifier) - NPU路由器（超轻量分类模型）
    └─── 四色卡片生成器家族（并行NPU推理）：
         ├─── 通政司 (Fact Generator) - NPU，Qwen2-1.5B-INT4
         ├─── 监察院 (Interpreter) - NPU，LoRA微调+量化Qwen2-7B
         ├─── 刑狱司 (Risk Detector) - NPU，规则引擎+Phi-3-mini
         └─── 参谋司 (Action Advisor) - NPU，CoT提示技术
    ↓
太史阁 (Memory) - 本地数据库+CPU向量检索（BGE-M3 + FAISS/Chroma）
    ↓
驿传司 (Reporter) - 前端 + NPU超轻量模型（100M参数）优化报告语言
    ↓
报告输出
```

### 详细Agent说明（ARM64 NPU优化版）

**1. 锦衣卫总指挥使 (Orchestrator)**
- 定位：8智能体体系的最高调度核心，统筹全流程、分配任务、处理异常
- 部署位置：Windows ARM64 + QNN SDK + NPU，运行Qwen2.0-7B-SSD或llama3.1-8b模型
- 核心能力：需求拆解、任务调度、进度监控、异常处置、结果聚合
- 模型选择：
  - Qwen2.0-7B-SSD (~450ms) - 通用推荐，平衡性能与速度
  - llama3.1-8b (~520ms) - 更强推理能力，适合复杂任务
  - llama3.2-3b (~280ms) - 最快响应速度，适合简单任务
- 提示词设计：见 [references/8-agent-architecture.md](references/8-agent-architecture.md)

**2. 密卷房 (Preprocessor)**
- 定位：数据加工智能体，专注原始数据的清洗、格式转换、特征提取
- 部署位置：CPU辅助，运行规则引擎或小模型
- 核心能力：数据清洗、格式转换、特征提取、质量核验
- 提示词设计：见 [references/8-agent-architecture.md](references/8-agent-architecture.md)

**3. 查询构建与执行 Agent (Query Builder)** ⭐新增
- 定位：根据结构化条件生成可执行的查询语句（SQL、API调用），从本地数据库获取数据
- 部署位置：本地代码（Python），不依赖AI模型，连接本地SQLite/DuckDB
- 核心能力：
  - 接收来自Orchestrator的JSON查询条件
  - 映射到本地数据库的表和字段
  - 生成优化的SQL查询
  - 执行查询，将结果集（DataFrame）返回给Orchestrator
- 技术特点：确定性程序，确保SQL生成的安全性和效率
- 代码位置：见 [agents/query_builder.py](agents/query_builder.py)

**4. 卡片生成与分类 Agent (Card Classifier)** ⭐新增
- 定位：分析数据结果，决定需要生成哪几类卡片，并触发对应的卡片生成器
- 部署位置：骁龙NPU，与Orchestrator共享模型或使用超轻量分类模型
- 核心能力：
  - 基于数据摘要和用户原始问题，判断需要生成哪些类型的分析卡片（四选一或组合）
  - 路由到对应的卡片生成器
- 四色卡片规则：
  - 🔵事实卡片：必须生成，总结核心数据事实
  - 🟢解释卡片：当数据有显著变化、模式或对比差异时生成
  - 🟡风险卡片：当数据触及预设阈值（如增长率< -5%）、发现异常点或潜在问题时生成
  - 🔴行动卡片：当问题本身要求建议，或识别出明确风险和机会时生成
- 代码位置：见 [agents/card_classifier.py](agents/card_classifier.py)

**5. 通政司 (Fact Generator) - 四色卡片生成器之一**
- 定位：事实生成智能体，从预处理数据中提取核心事实，验证事实真实性
- 部署位置：NPU，使用量化后的Qwen2-1.5B-INT4模型
- 核心能力：事实提取、事实验证、事实结构化、事实反馈
- 提示词设计：专注于客观描述，禁止任何推断
- 并行推理：在独立NPU进程中与其他三个卡片生成器并行推理
- 提示词设计：见 [references/8-agent-architecture.md](references/8-agent-architecture.md)

**6. 监察院 (Interpreter) - 四色卡片生成器之一**
- 定位：解释生成智能体，为事实结论生成可解释的逻辑说明
- 部署位置：NPU，用业务分析语料对Qwen2-7B进行LoRA微调后量化
- 核心能力：逻辑推导、解释可视化、异常解释、解释校验
- 提示词设计：引导"寻找相关性、季节性、外部因素"
- 并行推理：在独立NPU进程中与其他三个卡片生成器并行推理
- 提示词设计：见 [references/8-agent-architecture.md](references/8-agent-architecture.md)

**7. 太史阁 (Memory)**
- 定位：数据存储智能体，统一数据仓库，支持权限管控与版本回溯；提供知识图谱引导应用服务
- 部署位置：CPU辅助，SQLite + BGE-M3模型 + FAISS/Chroma
- 核心能力：全量存储、权限调取、版本管理、向量检索、关联分析、知识图谱引导
- 知识图谱引导应用：见 [references/knowledge-graph-application.md](references/knowledge-graph-application.md)
- 详细说明：见 [references/knowledge-graph.md](references/knowledge-graph.md)

**8. 刑狱司 (Risk Detector) - 四色卡片生成器之一**
- 定位：风险检测智能体，基于事实结论检测潜在风险点，评估风险等级
- 部署位置：NPU，结合规则引擎与轻量模型
  - 规则引擎：首先用规则（阈值、同比环比）过滤
  - 轻量模型：再用Phi-3-mini量化版描述风险性质和可能影响
- 核心能力：风险规则加载、风险识别、风险评级、风险预警
- 并行推理：在独立NPU进程中与其他三个卡片生成器并行推理
- 提示词设计：见 [references/8-agent-architecture.md](references/8-agent-architecture.md)

**9. 参谋司 (Action Advisor) - 四色卡片生成器之一**
- 定位：行动建议智能体，基于风险结果和解释结论生成可落地的行动建议
- 部署位置：NPU，使用思维链（CoT）提示技术
- 核心能力：建议生成、建议优先级、建议验证、建议优化
- 提示词设计：要求模型按"问题->根因->可选行动->推荐行动"的步骤推理
- 并行推理：在独立NPU进程中与其他三个卡片生成器并行推理
- 提示词设计：见 [references/8-agent-architecture.md](references/8-agent-architecture.md)

**10. 驿传司 (Reporter)** ⭐调整定位
- 定位：报告合成与呈现智能体，将零散卡片整合为结构化的、用户友好的最终报告，并驱动前端界面更新
- 部署位置：前端 (React) 与 端侧轻量模型（100M参数级别）结合
- 工作流程：
  - 接收来自Orchestrator的所有卡片（JSON格式）
  - 调用前端组件，按照"总览 -> 事实 -> 解释 -> 风险 -> 行动"的逻辑顺序进行排版
  - 调用运行在骁龙NPU上的超轻量文本润色模型，对报告的语言进行流畅性优化
  - 生成交互式数据看板，支持用户点击卡片钻取详情
- 提示词设计：见 [references/8-agent-architecture.md](references/8-agent-architecture.md)

详细架构说明：见 [references/8-agent-architecture.md](references/8-agent-architecture.md)

### NPU部署策略（关键创新点）

**1. 模型量化**
- 使用QAI AppBuilder，将微调后的模型转换为INT8/INT4精度的QNN格式
- 在NPU上获得最佳能效比

**2. 并行执行**
- 利用QAI AppBuilder的多进程架构
- 让四个卡片生成器（通政司/监察院/刑狱司/参谋司）在独立的NPU进程中并行推理
- 大幅提升处理速度

**3. 模型选择策略**
- 根据任务复杂度动态选择模型：
  - 简单任务：llama3.2-3b (~280ms)
  - 通用任务：Qwen2.0-7B-SSD (~450ms)
  - 复杂推理：llama3.1-8b (~520ms)
- 通过NPUModelLoader灵活切换

详细部署指南：见 [references/npu-deployment.md](references/npu-deployment.md)

## 操作步骤

### 标准流程

1. **批量数据加载**
   - 支持用户拖拽文件夹或选择目录
   - 调用 `scripts/batch_process.py --dir <目录路径>` 批量处理
   - 自动识别文件类型（CSV/JSON/Excel/图像）
   - 对图像文件执行OCR提取文本

2. **任务触发与分解**
   - 用户自然语言查询（如"分析上个月销售趋势"）
   - **锦衣卫总指挥使**解析意图，拆解为原子任务：
     * 密卷房数据加工→查询构建与执行→卡片生成与分类→四色卡片并行生成→太史阁知识检索→驿传司报告合成

3. **数据预处理**
   - **密卷房**接收数据加工任务
   - 数据感知：对接多源数据（数据库/API/文件）
   - 数据清洗：处理缺失值、异常值、重复值
   - 格式转换：统一转换为结构化JSON格式
   - 特征提取：提取核心分析特征
   - 输出"预处理数据+质量报告"至总指挥使

4. **查询构建与执行**
   - **查询构建与执行 Agent**接收查询条件
   - 接收来自Orchestrator的JSON查询条件
   - 映射到本地数据库的表和字段
   - 生成优化的SQL查询
   - 执行查询（使用DuckDB），将结果集（DataFrame）返回给Orchestrator
   - 输出"查询结果+数据摘要"至总指挥使

5. **卡片生成与分类**
   - **卡片生成与分类 Agent**接收数据摘要和用户原始问题
   - 基于数据摘要和用户原始问题，判断需要生成哪些类型的分析卡片
   - 四色卡片规则：
     * 🔵事实卡片：必须生成，总结核心数据事实
     * 🟢解释卡片：当数据有显著变化、模式或对比差异时生成
     * 🟡风险卡片：当数据触及预设阈值（如增长率< -5%）、发现异常点或潜在问题时生成
     * 🔴行动卡片：当问题本身要求建议，或识别出明确风险和机会时生成
   - 输出"需要生成的卡片类型列表"至总指挥使

6. **四色卡片并行生成** ⭐关键创新
   - **四色卡片生成器家族**（通政司/监察院/刑狱司/参谋司）并行接收生成任务
   - 每个生成器在独立NPU进程中运行，实现并行推理
   - **通政司**（事实卡片生成器）：使用Qwen2-1.5B-INT4，专注于客观描述
   - **监察院**（解释卡片生成器）：使用LoRA微调+量化Qwen2-7B，引导寻找相关性、季节性、外部因素
   - **刑狱司**（风险卡片生成器）：结合规则引擎（阈值、同比环比）+ Phi-3-mini量化版，描述风险性质和可能影响
   - **参谋司**（行动卡片生成器）：使用CoT提示技术，按"问题->根因->可选行动->推荐行动"步骤推理
   - 输出四色卡片至总指挥使

7. **知识沉淀与关联**
   - **太史阁**存储新卡片元数据到SQLite
   - 使用BGE-M3模型将卡片内容向量化
   - 存入FAISS/Chroma本地库
   - 根据当前查询语义检索相关历史卡片
   - 应用四色卡片关联维度：
     * 蓝色卡片（事实层）：时间/地点/人物/事件/数字指标
     * 绿色卡片（分析层）：因果关系/对比关系/趋势变化/关联规则
     * 黄色卡片（创意层）：跨领域类比/潜在机会/创新方向
     * 红色卡片（风险层）：潜在问题/负面因素/冲突矛盾
   - 支持自定义关联规则：
     * 显性规则：直接描述关联逻辑（"将销售额>100万的地区与营销策略关联"）
     * 隐性规则：通过示例学习关联模式
     * 规则优先级：指定不同规则的权重和执行顺序
   - 跨色卡片引用机制：
     * 直接引用：任意卡片可引用其他颜色卡片
     * 规则映射：通过自定义规则实现跨色关联
     * 动态更新：引用关系随原始节点变化自动更新
     * 引用限制：循环引用检测、权限控制、引用标记
   - 详细说明：见 [references/knowledge-graph.md](references/knowledge-graph.md) 和 [references/card-specification.md](references/card-specification.md)

8. **报告合成与呈现** ⭐调整
   - **驿传司（Reporter）**接收所有四色卡片
   - 调用前端组件，按照"总览 -> 事实 -> 解释 -> 风险 -> 行动"的逻辑顺序进行排版
   - 调用运行在骁龙NPU上的超轻量文本润色模型（100M参数级别），对报告的语言进行流畅性优化
   - 生成交互式数据看板，支持用户点击卡片钻取详情
   - 输出格式：见 [assets/data-analysis-report-template.md](assets/data-analysis-report-template.md)

### 端到端分析示例

**场景：销售数据分析（用户查询："分析上个月销售趋势"）**

1. **任务触发**
   - 锦衣卫总指挥使解析意图为"趋势分析"，启动标准流程

2. **数据预处理**
   - 密卷房输出预处理数据：
     ```json
     {
       "preprocessed_data": {
         "data": [
           {"date": "2024-12-01", "sales": 50000},
           {"date": "2024-12-31", "sales": 42500}
         ]
       },
       "quality_report": {
         "completeness": 0.98,
         "accuracy": 0.99
       }
     }
     ```

3. **事实生成**
   - 通政司输出事实结论：
     ```json
     {
       "fact_card": {
         "card_type": "blue",
         "title": "12月销售数据统计",
         "content": {
           "dimensions": ["时间"],
           "metrics": {
             "sales": {"value": 1200000, "unit": "元"},
             "growth_rate": {"value": "-15%", "comparison": "环比"}
           }
         }
       }
     }
     ```

4. **解释生成**
   - 监察院输出解释说明：
     ```json
     {
       "interpretation_card": {
         "card_type": "green",
         "title": "销售下滑原因分析",
         "content": {
           "logic_chain": [
             {"step": 1, "description": "竞品于12月中旬推出满减促销活动"},
             {"step": 2, "description": "核心客户群体被分流"},
             {"step": 3, "description": "销量环比下降15%"}
           ]
         }
       }
     }
     ```

5. **风险检测**
   - 刑狱司输出风险结果：
     ```json
     {
       "risk_card": {
         "card_type": "yellow",
         "title": "库存积压预警",
         "content": {
           "risk_type": "库存积压",
           "risk_level": "一级",
           "details": {
             "current_stock": 5000,
             "expected_demand": 2000,
             "excess_ratio": "150%"
           }
         }
       }
     }
     ```

6. **行动建议**
   - 参谋司输出行动建议：
     ```json
     {
       "action_card": {
         "card_type": "red",
         "title": "库存清理行动建议",
         "content": {
           "actions": [
             {
               "step": 1,
               "action": "推出限时折扣清理库存",
               "priority": "立即执行",
               "expected_effect": "库存周转率提升30%"
             }
           ]
         }
       }
     }
     ```

7. **信息衔接与知识检索**
   - 驿传司转发所有模块间信息
   - 检索太史阁历史"竞品动态"卡片，提供上下文

8. **报告输出**
   - 锦衣卫总指挥使整合所有结果
   - 生成交互式报告，包含折线图、风险预警、行动建议

### 可选分支

- **当数据质量不足时**：密卷房标注质量问题，报告至总指挥使，触发人工介入
- **当用户意图不明确时**：锦衣卫总指挥使主动沟通澄清需求，或提供多个可选分析方向
- **当检测到高风险时**：刑狱司推送特级/一级风险至总指挥使，触发应急处置
- **当需要人工介入时**：驿传司转发至人工系统，请求人工确认或补充信息
- **当历史知识可用时**：太史阁检索相关历史卡片，提供给各智能体参考
- **当模型切换需求时**：根据任务复杂度动态切换模型（llama3.2-3b/Qwen2.0-7B-SSD/llama3.1-8b）

## 前端对接

### 技术栈
- React 18 + TypeScript + Vite + Tailwind CSS
- Framer Motion（动画）
- Recharts（数据可视化）
- Lucide React（图标）

### 对接规范
- 后端提供RESTful API，前端通过HTTP请求对接
- 后端接口使用GenieAPIService（HTTP API）实现NPU推理调用
- 支持动态模型切换（llama3.2-3b/Qwen2.0-7B-SSD/llama3.1-8b）
- 前端状态管理建议使用Zustand或React Context API
- 核心组件包括：
  - 知识概览（KnowledgeOverview）
  - 知识图谱可视化（KnowledgeGraph）
  - 规则配置（RuleConfig）
  - 卡片生成（CardGeneration）
  - 报告看板（ReportDashboard）
  - 模型选择器（ModelSelector）⭐新增
- 详见 [references/frontend-integration.md](references/frontend-integration.md)

## 资源索引

### 必要脚本
- [scripts/read_data.py](scripts/read_data.py)
  - 用途：读取 CSV/JSON/Excel 格式数据文件
  - 参数：`--file` 文件路径，`--format` 文件格式

- [scripts/batch_process.py](scripts/batch_process.py)
  - 用途：批量处理文件夹中的文件，自动识别类型并分类
  - 参数：`--dir` 目录路径，`--output` 输出目录

- [scripts/ocr_process.py](scripts/ocr_process.py)
  - 用途：对图像文件执行OCR文本提取（CPU版本，pytesseract）
  - 参数：`--file` 图像文件路径，`--language` 语言（chi_sim/eng）

- [scripts/ocr_npu.py](scripts/ocr_npu.py)
  - 用途：NPU加速的OCR图像文本提取（使用高通AI Engine SDK）
  - 参数：`--file` 图像文件路径，`--language` 语言
  - 性能：NPU加速，推理延迟~50ms（比CPU快4倍）
  - 使用方式：
    ```python
    from scripts.ocr_npu import NPUCREngine

    # 初始化NPU OCR引擎
    ocr_engine = NPUCREngine(model_path="models/crnn-int8")

    # 单张图像OCR
    result = ocr_engine.extract_text_from_image(
        image_path=Path("./image.jpg"),
        language='chi_sim+eng'
    )

    # 批量OCR
    batch_result = ocr_engine.batch_extract_text(
        image_paths=[Path("./image1.jpg"), Path("./image2.jpg")],
        language='chi_sim+eng'
    )
    ```

- [scripts/easy_ocr_npu.py](scripts/easy_ocr_npu.py)
  - 用途：EasyOCR NPU引擎封装，推荐的OCR解决方案
  - 使用方式：
    ```python
    from scripts.easy_ocr_npu import EasyOCRNPU

    ocr_engine = EasyOCRNPU(use_mock=False)  # 真实NPU模式
    result = ocr_engine.ocr_single_image(image_path="./image.jpg", languages=["ch_sim", "eng"])
    ```

- [scripts/model_loader.py](scripts/model_loader.py)
  - 用途：NPU模型加载器，支持多模型切换（llama3.2-3b/Qwen2.0-7B-SSD/llama3.1-8b）
  - 参数：`--model_key` 模型标识符
  - 示例：
    ```python
    from scripts.model_loader import NPUModelLoader

    # 使用更小模型（更快）
    loader = NPUModelLoader(model_key="llama3.2-3b")
    model = loader.load()
    ```

- [scripts/vector_retrieval.py](scripts/vector_retrieval.py)
  - 用途：向量检索模块，使用BGE-M3模型和FAISS进行语义搜索
  - 使用方式：`vr = VectorRetrieval(); vr.search(query, top_k=10)`

- [scripts/agent_memory_db.py](scripts/agent_memory_db.py)
  - 用途：Agent记忆数据库访问类，封装所有CRUD操作
  - 使用方式：`db = AgentMemoryDB("./agent_memory.db")`

- [scripts/init_memory_db.py](scripts/init_memory_db.py)
  - 用途：初始化Agent记忆数据库，创建表结构和索引
  - 参数：`--db-path` 数据库路径（默认：./agent_memory.db）

### Agent模块
- [agents/orchestrator.py](agents/orchestrator.py) - 锦衣卫总指挥使，8-Agent体系最高调度核心
- [agents/preprocessor.py](agents/preprocessor.py) - 密卷房，数据清洗与格式转换
- [agents/query_builder.py](agents/query_builder.py) - 查询构建与执行Agent
- [agents/card_classifier.py](agents/card_classifier.py) - 卡片生成与分类Agent
- [agents/fact_generator.py](agents/fact_generator.py) - 通政司，事实卡片生成器
- [agents/interpreter.py](agents/interpreter.py) - 监察院，解释卡片生成器
- [agents/risk_detector.py](agents/risk_detector.py) - 刑狱司，风险卡片生成器
- [agents/action_advisor.py](agents/action_advisor.py) - 参谋司，行动卡片生成器
- [agents/memory.py](agents/memory.py) - 太史阁，知识存储与检索
- [agents/messenger.py](agents/messenger.py) - 驿传司，报告合成与呈现
- [agents/canmousi.py](agents/canmousi.py) - 蚕眸司，视觉分析Agent
- [agents/jianchayuan.py](agents/jianchayuan.py) - 监察院（扩展），数据分析
- [agents/mijuanfang.py](agents/mijuanfang.py) - 密卷房（扩展），文档处理
- [agents/taishige.py](agents/taishige.py) - 太史阁（扩展），知识管理
- [agents/tongzhengsi.py](agents/tongzhengsi.py) - 通政司（扩展），信息传递
- [agents/xingyusi.py](agents/xingyusi.py) - 行移司，流程调度
- [agents/yichuansi.py](agents/yichuansi.py) - 驿传司（扩展），报告输出

### 领域参考
- [references/8-agent-architecture.md](references/8-agent-architecture.md)
  - 何时读取：设计Agent协作流程、理解Agent角色职责、实现提示词设计

- [references/7-agent-architecture.md](references/7-agent-architecture.md)
  - 何时读取：7-Agent架构参考，对比8-Agent设计

- [references/npu-deployment.md](references/npu-deployment.md)
  - 何时读取：部署NPU加速功能、配置模型量化、实现并行推理

- [references/easyocr-npu-deployment.md](references/easyocr-npu-deployment.md)
  - 何时读取：EasyOCR NPU部署配置

- [references/model-selection.md](references/model-selection.md)
  - 何时读取：选择合适的模型、理解模型性能差异、配置模型切换策略

- [references/agent-prompts.md](references/agent-prompts.md)
  - 何时读取：配置和调试Agent时
  - 内容：所有Agent的详细提示词设计（锦衣卫风格）

- [references/knowledge-graph.md](references/knowledge-graph.md)
  - 何时读取：设计知识图谱结构、实现卡片关联、配置向量检索

- [references/agent-memory-database.md](references/agent-memory-database.md)
  - 何时读取：使用Agent记忆数据库、开发Agent协作功能
  - 数据库设计、API接口、使用示例、性能优化

- [references/knowledge-graph-application.md](references/knowledge-graph-application.md)
  - 何时读取：使用知识图谱引导应用时
  - 内容：SmartBot知识图谱引导应用完整工作流程

- [references/mock-summary.md](references/mock-summary.md)
  - 何时读取：准备替换Mock代码为真实AIPC NPU实现时
  - 内容：所有Mock代码的位置、替换说明、优先级

- [references/frontend-integration.md](references/frontend-integration.md)
  - 何时读取：对接前端组件、实现API接口、设计数据可视化

- [references/frontend-development.md](references/frontend-development.md)
  - 何时读取：前端开发规范、组件设计

- [references/card-specification.md](references/card-specification.md)
  - 何时读取：创建四色卡片、编写分析内容
  - 卡片结构、数据格式、约束条件

- [references/analysis-best-practices.md](references/analysis-best-practices.md)
  - 何时读取：数据分析最佳实践

- [references/backend-api.md](references/backend-api.md)
  - 何时读取：后端API设计、对接后端服务

- [references/data-classification.md](references/data-classification.md)
  - 何时读取：数据分类标准、处理规范

### 输出资产
- [assets/data-analysis-report-template.md](assets/data-analysis-report-template.md)
  - 用途：报告模板，定义标准报告结构

## 注意事项
- 所有数据不出域，本地AES-256加密存储
- NPU推理延迟<500ms，本地向量检索响应<100ms
- GenieAPIService作为标准HTTP API接口，支持RESTful调用
- 充分利用智能体的语言理解和生成能力，避免为简单任务编写脚本
- 按需读取参考，保持上下文简洁
- 前后端完全解耦，通过RESTful API对接

## 性能指标

- NPU推理延迟：<500ms（Qwen2.0-7B-INT8）
- CPU模式（INT4）：<2s
- 本地向量检索响应：<100ms（10万级数据）
- 批量处理速度：1000个文件/分钟（取决于文件大小和复杂度）
- OCR准确率：>95%（清晰图像）
- 前端响应时间：<200ms（知识概览页面加载）

## 部署环境

- **平台**：Windows ARM64（支持Linux/macOS）
- **后端**：FastAPI + Python 3.10+ + uvicorn
- **前端**：React 18 + TypeScript + Vite + Tailwind CSS
- **数据库**：SQLite（元数据）
- **向量检索**：BGE-M3 + FAISS
- **NPU SDK**：QNN SDK（可选，用于NPU加速）
- **服务接口**：FastAPI RESTful API + GenieAPIService（可选NPU推理）

## 架构说明

- **多Agent架构**：采用多Agent锦衣卫风格协作流
  - 核心Agent：orchestrator, preprocessor, query_builder, card_classifier
  - 卡片生成器：fact_generator, interpreter, risk_detector, action_advisor
  - 扩展Agent：canmousi, jianchayuan, mijuanfang, taishige, tongzhengsi, xingyusi, yichuansi
  - 基础设施：memory, messenger
- **前后端完全解耦**：通过RESTful API对接，前端通过HTTP请求调用后端服务
- **NPU加速支持**：可选集成GenieAPIService进行NPU推理
- **多模态扩展**：支持OCR识别图像文本，视频处理模块需后续迭代
