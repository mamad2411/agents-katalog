---
name: harmonyos-l1-query
description: "当需要快速精准检索鸿蒙应用开发相关的代码片段和概念时，使用此 Skill 进行 L1 RAG 查询。此 Skill 基于向量数据库和 BM25 混合检索，提供最常用的代码片段。注意：这是可选功能，需要配置 API Key 才能启用。"
---

# 鸿蒙应用 L1 RAG 查询 Skill

## 目的

获取最常用的代码片段和概念，通过 RAG（检索增强生成）快速定位相关知识点。

## ⚠️ 重要说明

**L1 RAG 是可选功能**：
- **启用条件**：需要在 `.opencode/skills/cangjie-dev-harmonyos/scripts/.env` 文件中将 `SILICONFLOW_API_KEY` 从默认值 `YOUR_API_KEY` 替换为有效的 API Key
- **禁用时**（默认）：保持 `SILICONFLOW_API_KEY=YOUR_API_KEY`，系统会直接跳过 L1 阶段，进入 L3 本地文档搜索
- **优势**：L1 可以提供语义搜索能力，但需要 API 调用成本
- **替代方案**：L3 本地文档搜索完全免费且包含完整官方文档

## 📋 L1 查询策略

### 基于需求分析结果进行查询

**操作**: 根据需求分析（L0）得出的核心API名称，分别进行精准查询。
**策略**: 使用纯英文API名称，让BM25关键词匹配发挥最大效果。

### 查询原则

- **纯英文关键词**: 直接使用英文API名称（如 "Button"），不添加中文后缀
- **单词精准**: 一个关键词（如 "Button"）可匹配该组件的所有相关信息
- **适度数量**: 控制在3-5个核心组件
- **结果展示**: **必须将L1查询结果贴出来供用户查看**，不要隐藏查询过程

## 🚀 执行方式

### 脚本路径

**L1 RAG 查询脚本**（位于 `.opencode/skills/cangjie-dev-harmonyos/scripts/`）：
- `ask_cangjie.py` - L1 阶段使用的 RAG 查询脚本（带自动初始化功能）
- `cangjie_retriever.py` - 混合检索器（向量 + BM25）
- `Database-Builder.py` - RAG 数据库构建脚本

### 调用方式

```bash
cd .opencode/skills/cangjie-dev-harmonyos/scripts
# 安装依赖（只需第一次）
python -m pip install -r requirements.txt

# 首次使用或确保 L3 文档已初始化（必须执行）
python ask_cangjie.py "test"

# 如果 L1 启用，可继续查询
python ask_cangjie.py "Button"
python ask_cangjie.py "List"
python ask_cangjie.py "TextInput"
```

### ⚠️ 初始化检查

**L3 文档初始化**（必须执行）：
- 检查 `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/` 目录是否存在
- 如果不存在，执行一次 `python ask_cangjie.py "test"` 来初始化

**L1 数据库初始化**（仅在 L1 启用时执行）：
- 检查 `.opencode/skills/cangjie-dev-harmonyos/scripts/chroma_db/` 目录是否存在
- 如果不存在，脚本会自动构建向量数据库

**⚠️ 用户提示说明**（必须执行）：

当检测到需要初始化时，必须先明确告知用户：

```
⚙️ 正在自动拉取文档和构建数据库，稍等1分钟...
```

### ⚠️ L1 功能启用检查（优先执行）

在执行 L1 查询前，脚本会自动检查：
1. **SILICONFLOW_API_KEY**（位于 `.opencode/skills/cangjie-dev-harmonyos/scripts/.env`）是否为默认值 `YOUR_API_KEY` 或空值

- **API Key 已配置且非默认值** → 继续 L1 初始化和查询
- **API Key 为默认值或空值** → 输出 `NO_RAG_RESULT`，提示直接使用 L3 搜索

## 🛑 L1 评估 (Self-Reflection)

- **L1 启用且有结果** -> 停止检索，开始编码
- **L1 启用但无相关结果** -> **进入 L3 本地文档搜索**（使用 `harmonyos-l3-query` skill）
- **L1 未启用** -> **已执行初始化脚本确保 L3 文档存在，直接进入 L3 本地文档搜索**（使用 `harmonyos-l3-query` skill）

## 📋 查询示例

### 示例 1: List 组件查询

```bash
python ask_cangjie.py "List"
```

**查询结果示例**:
```text
[原始问题]: List
[相关度]: 0.85
[来源]: 文档片段
[本地路径]: hm-docs/ui-dev/arkui-cj/cj-layout-development-create-list.md

[知识片段]:
List 组件是 ArkUI 中用于展示列表的基础组件，导入方式：
import kit.ArkUI

List 的基本使用需要导入 ArkUI 包，包含列表创建、滚动、数据绑定等功能...
```

### 示例 2: Button 组件查询

```bash
python ask_cangjie.py "Button"
```

### 示例 3: 线程创建查询

```bash
python ask_cangjie.py "spawn"
```

## ✅ L1 查询最佳实践

### 1. 分组执行
按组件分组，每个维度单独查询，提高 BM25 匹配精度

### 2. 精准关键词
- ✅ "Button" - 精准匹配相关内容
- ❌ "如何创建按钮" - 模糊描述，匹配度低

### 3. 结果展示
必须将查询结果完整展示给用户，包含原始问题和知识片段

### 4. 评估决策
根据查询结果决定下一步：
- ✅ 关键组件有完整代码 → 停止检索，开始编码
- ⚠️ 部分结果不完整 → 可选择性进入 L3 补充（使用 `harmonyos-l3-query` skill）
- ❌ 完全无结果 → 必须进入 L3（使用 `harmonyos-l3-query` skill）

## 工作流程

1. **需求分析**（已完成）- 使用 `harmonyos-requirement-analysis` skill
2. **使用 skill-B skills**（已完成）- 先使用 `.opencode/skills/` 中的仓颉语言 skills
3. **L1 查询**（本 Skill）- 如需进一步查询，使用本 Skill
4. **L3 查询** - 如需本地文档搜索，使用 `harmonyos-l3-query` skill
5. **构建** - 使用 `harmonyos-build` skill 进行项目构建
6. **迭代进化** - 使用 `harmonyos-evolution` skill 记录和解决问题

## 依赖要求

使用 L1 RAG 查询功能需要：

1. **Python 3.x**
2. **Python 包**:
   ```bash
   pip install langchain-chroma langchain-openai langchain-community jieba python-dotenv
   ```
3. **环境变量**: 
   - `SILICONFLOW_API_KEY` - SiliconFlow API 密钥（可选，用于启用 L1 RAG 功能）
   - 配置文件位置：`.opencode/skills/cangjie-dev-harmonyos/scripts/.env`
4. **RAG_Lite 数据源**: `.opencode/skills/cangjie-dev-harmonyos/scripts/RAG_Lite/` 目录（包含知识库 JSON 文件）

> **注意**: L1 RAG 功能是可选的。默认情况下 `SILICONFLOW_API_KEY=YOUR_API_KEY`，系统会自动跳过 L1 阶段，直接使用 L3 本地文档搜索。只有当你将 API Key 替换为有效值时，才会启用 L1 功能。
