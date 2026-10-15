---
name: mindsdb-mcp-skill
description: MindsDB MCP服务器交互技能，采用三模块架构（db_connector、workflow_rag_build、workflow_rag_analysis），支持通过自然语言查询和操作200+企业级数据源，提供RAG知识库构建、NLP2SQL转换、智能数据分析和元数据自动提取能力。
version: 2.1.0
author: yejinlei
---

# MindsDB MCP Skill | MindsDB MCP Skill

基于 MindsDB MCP 协议的通用数据库交互技能，采用**三模块架构**设计，支持自然语言操作各类数据源，自动适配本地/远程 MindsDB 部署，无需修改技能代码即可兼容所有 MindsDB 支持的数据库。

**v2.1.0 新增功能**：元数据自动提取与智能查询，支持自动理解数据库结构，实现零配置智能问答。

A universal database interaction skill based on the MindsDB MCP protocol, featuring a **three-module architecture**, supporting natural language operations on various data sources, automatically adapting to local/remote MindsDB deployments, and compatible with all MindsDB-supported databases without modifying skill code.

## 架构设计 | Architecture Design

本技能采用**三模块架构**，职责分离清晰，便于维护和扩展：

### 模块1：db_connector（公共数据库连接模块）
- **职责**：统一管理数据库连接，封装MCP请求
- **功能**：
  - MindsDB服务自动检测、安装和启动
  - 数据库连接管理（DuckDB、MySQL、TDengine等）
  - 统一MCP请求发送和响应处理
  - 连接信息缓存

### 模块2：workflow_rag_build（本地RAG构建与管理工作流）
- **职责**：构建和维护本地RAG知识库
- **功能**：
  - 本地RAG系统初始化（ChromaDB + all-MiniLM-L6-v2）
  - 知识库管理（创建、列表、删除）
  - 数据字典管理（获取、搜索、刷新）
  - **元数据自动提取**（新增）：自动从数据库提取表结构、列信息、业务含义
  - 数据持久化管理

### 模块3：workflow_rag_analysis（基于RAG的NLP2SQL和数据分析工作流）
- **职责**：利用RAG进行智能数据分析和查询
- **功能**：
  - 自然语言到SQL转换（NLP2SQL）
  - **智能查询引擎**（新增）：基于元数据理解用户意图，自动生成SQL
  - 智能数据分析
  - 知识库智能问答
  - AI模型创建与预测

## 新增功能 | New Features (v2.1.0)

### 1. 元数据自动提取 (metadata_extractor.py)

**功能说明**：
- 自动从DuckDB数据库提取完整的元数据信息
- 智能推断表和列的业务含义
- 自动检测表之间的关系（外键关联）
- 推断业务域并分组

**提取内容**：
| 元数据类型 | 包含信息 |
|-----------|---------|
| 表级元数据 | 表名、行数、业务含义、标签、样本数据 |
| 列级元数据 | 列名、数据类型、业务含义、主外键、样本值 |
| 关系元数据 | 表间关联关系、外键检测 |
| 业务域元数据 | 按业务主题分组的表集合 |

**使用示例**：
```python
from scripts.metadata_extractor import extract_metadata_from_duckdb

# 一键提取元数据
data_dict, stats = extract_metadata_from_duckdb(
    db_path="path/to/database.duckdb",
    save_path="path/to/metadata.json"
)

# 查看提取结果
print(data_dict.generate_summary())
```

### 2. 智能查询引擎 (intelligent_query.py)

**功能说明**：
- 基于元数据理解用户自然语言问题
- 自动识别查询意图（计数、列表、统计、详情）
- 智能匹配相关表和字段
- 自动生成并执行SQL查询

**工作流程**：
```
用户问题 → 意图识别 → 关键词提取 → 表/字段匹配 → SQL生成 → 执行查询 → 返回结果
```

**使用示例**：
```python
from scripts.intelligent_query import IntelligentQueryEngine

# 初始化引擎
engine = IntelligentQueryEngine(db_path)

# 自然语言查询
result = engine.query("总共几个部门")
# 自动输出：意图(count) → 匹配表(odw_department) → SQL(SELECT COUNT(*)) → 结果(168)
```

**支持的查询类型**：
| 查询类型 | 示例问题 | 自动生成的SQL |
|---------|---------|--------------|
| 计数查询 | "总共几个部门" | `SELECT COUNT(*) FROM odw_department` |
| 列表查询 | "有哪些项目" | `SELECT DISTINCT project_name FROM odw_project` |
| 统计查询 | "各部门人数分布" | `SELECT dept, COUNT(*) FROM ... GROUP BY ...` |
| 详情查询 | "项目进度如何" | `SELECT * FROM odw_project LIMIT 10` |

## 技能用途 | Skill Purpose

### 主要用途 | Main Purposes

- **自然语言到SQL转换**：将用户的自然语言查询自动转换为可执行的SQL语句，无需用户编写SQL
- **元数据自动提取**：自动理解数据库结构，无需手动配置即可进行智能查询
- **多数据源管理**：统一管理和操作200+企业级数据源，包括SQL数据库、NoSQL数据库、时序数据库、文件型数据源等
- **RAG知识库构建与查询**：基于数据库数据构建知识库，支持智能问答和文档检索，提升数据分析能力
- **本地RAG备用方案**：当MindsDB未配置embedding model时，自动切换到本地RAG（ChromaDB + all-MiniLM-L6-v2）
- **AI模型训练与预测**：基于数据源创建AI预测模型，进行数据预测和分析
- **跨源数据分析**：支持多数据源联动查询与分析，提供统一的结果格式
- **Agent系统集成**：可直接集成到各类Agent系统，为Agent提供数据库操作能力

### 应用场景 | Application Scenarios

- **智能数据查询**：用户通过自然语言查询数据库，无需了解SQL语法
- **零配置数据分析**：自动提取元数据，无需预先配置即可进行智能分析
- **知识库构建**：基于企业数据构建智能知识库，支持员工快速获取信息
- **数据分析与报表**：通过自然语言驱动的数据分析，自动生成报表和insights
- **工业设备监控**：连接时序数据库，监控设备运行状态，预测设备故障
- **业务决策支持**：基于多源数据的分析，为业务决策提供数据支持

## 如何使用 | How to Use

### 环境准备 | Environment Preparation

安装技能包所需依赖：

```bash
pip install requests
```

#### 元数据提取依赖 | Metadata Extraction Dependencies

元数据自动提取功能需要以下依赖：
```bash
pip install duckdb
```

#### MindsDB自动安装与启动 | MindsDB Automatic Installation and Startup

本技能支持自动检测、安装和启动MindsDB服务，无需手动操作：

- **自动检测**：首次使用时会检查MindsDB是否已安装
- **自动安装**：如果未安装，自动执行 `pip install mindsdb`
- **自动启动**：自动启动MindsDB服务（默认端口47334）
- **服务验证**：验证MindsDB服务是否正常运行

#### 手动安装选项 | Manual Installation Option

如果您希望手动安装和配置MindsDB：

```bash
# 安装MindsDB
pip install mindsdb

# 启动MindsDB服务
python -m mindsdb
```

确保MindsDB服务在默认端口47334上运行。

#### 本地RAG依赖 | Local RAG Dependencies

当MindsDB RAG不可用时，技能会自动安装以下依赖：
- **chromadb**：轻量级向量数据库
- **sentence-transformers**：提供all-MiniLM-L6-v2嵌入模型

### 快速开始 | Quick Start

#### 方式1：使用元数据提取模块 | Method 1: Use Metadata Extraction Module

```python
from scripts.metadata_extractor import extract_metadata_from_duckdb

# 提取DuckDB数据库元数据
data_dict, stats = extract_metadata_from_duckdb(
    db_path="data/weekly_report_warehouse.duckdb",
    save_path="data/metadata.json"
)

# 查看提取统计
print(f"表数量: {stats['tables_extracted']}")
print(f"列数量: {stats['columns_extracted']}")
print(f"关系数量: {stats['relationships_detected']}")

# 查看数据字典摘要
print(data_dict.generate_summary())
```

#### 方式2：使用智能查询引擎 | Method 2: Use Intelligent Query Engine

```python
from scripts.intelligent_query import IntelligentQueryEngine

# 初始化引擎（自动加载或提取元数据）
engine = IntelligentQueryEngine(
    db_path="data/weekly_report_warehouse.duckdb"
)

# 自然语言查询
result = engine.query("总共几个部门")
print(f"SQL: {result['sql']}")
print(f"结果: {result['data']}")

# 关闭连接
engine.close()
```

#### 方式3：使用公共数据库连接模块 | Method 3: Use Database Connector Module

```python
from scripts.db_connector import get_db_connector

# 获取数据库连接器
db = get_db_connector()

# 连接DuckDB数据库
result = db.connect_database(
    db_type="duckdb",
    db_path="data/weekly_report_warehouse.duckdb",
    database="warehouse_db"
)
print(result)

# 执行SQL查询
result = db.execute_sql("SELECT * FROM warehouse_db.odw_project LIMIT 5")
print(result)
```

#### 方式4：使用RAG构建工作流 | Method 4: Use RAG Build Workflow

```python
from scripts.workflow_rag_build import rag_build_workflow_entry

# 创建RAG知识库（自动包含元数据）
params = {
    "action": "create_kb",
    "kb_name": "weekly_report_kb",
    "database": "warehouse_db",
    "extract_metadata": True  # 新增：自动提取元数据
}
result = rag_build_workflow_entry(params)
print(result)

# 获取数据字典摘要
params = {
    "action": "get_data_dict_summary"
}
result = rag_build_workflow_entry(params)
print(result)
```

#### 方式5：使用RAG分析工作流 | Method 5: Use RAG Analysis Workflow

```python
from scripts.workflow_rag_analysis import rag_analysis_workflow_entry

# 自然语言查询（NLP2SQL）
params = {
    "action": "nl_query",
    "database": "warehouse_db",
    "nl_text": "查询所有项目的状态"
}
result = rag_analysis_workflow_entry(params)
print(result)

# 知识库智能问答
params = {
    "action": "query_kb",
    "kb_name": "weekly_report_kb",
    "nl_text": "项目进度如何"
}
result = rag_analysis_workflow_entry(params)
print(result)
```

### RAG知识库全流程 | RAG Knowledge Base Full Process

```python
from scripts.workflow_rag_build import rag_build_workflow_entry
from scripts.workflow_rag_analysis import rag_analysis_workflow_entry
import json

# 1. 创建RAG知识库（工作流1）- 自动提取元数据
create_kb = {
    "action": "create_kb",
    "kb_name": "test_rag_kb",
    "database": "warehouse_db",
    "extract_metadata": True
}
create_result = rag_build_workflow_entry(create_kb)
print("创建知识库结果:", create_result)

# 2. 知识库智能问答（工作流2）
query_kb = {
    "action": "query_kb",
    "kb_name": "test_rag_kb",
    "nl_text": "查询核心数据信息"
}
query_result = rag_analysis_workflow_entry(query_kb)
print("知识库查询结果:", query_result)
```

## 核心功能 | Core Functions

### 模块1：db_connector（公共数据库连接模块）

| 方法 | 必传参数 | 功能说明 |
|------|---------|----------|
| connect_database | db_type | 连接指定类型的数据源 |
| list_databases | 无 | 列出所有已连接的数据源 |
| show_tables | database | 查看指定数据库的所有表 |
| describe_table | database, table | 查看指定表的结构 |
| execute_sql | sql | 执行自定义SQL语句 |

### 模块2：workflow_rag_build（RAG构建工作流）

| 动作 | 必传参数 | 功能说明 |
|------|---------|----------|
| create_kb | kb_name | 创建RAG知识库，自动提取数据库元数据 |
| list_kb | 无 | 列出所有已创建的RAG知识库 |
| delete_kb | kb_name | 删除指定名称的RAG知识库 |
| get_data_dict_summary | 无 | 获取数据字典摘要信息 |
| search_data_dict | keyword | 搜索数据字典中的元数据 |
| refresh_data_dict | database | 刷新指定数据库的数据字典 |
| extract_metadata | database | 提取指定数据库的元数据（新增） |

### 模块3：workflow_rag_analysis（RAG分析工作流）

| 动作 | 必传参数 | 功能说明 |
|------|---------|----------|
| connect_db | db_type | 连接指定类型的数据源 |
| list_databases | 无 | 列出所有已连接的数据源 |
| show_table_schema | database | 查看指定数据源的所有数据表结构 |
| nl_query | database, nl_text | 通过自然语言查询数据（NLP2SQL） |
| exec_sql | database, sql | 执行自定义SQL语句 |
| analyze_data | database, nl_text | 对数据进行自然语言驱动的智能分析 |
| query_kb | kb_name, nl_text | 向知识库发送自然语言查询 |
| intelligent_query | database, nl_text | 智能查询（基于元数据）（新增） |
| create_model | model_name, predict_field | 创建AI预测模型 |

### 新增模块：metadata_extractor（元数据提取模块）

| 方法 | 必传参数 | 功能说明 |
|------|---------|----------|
| extract_from_duckdb | db_path | 从DuckDB提取完整元数据 |
| get_extraction_stats | 无 | 获取提取统计信息 |
| save_to_file | file_path | 保存数据字典到文件 |

### 新增模块：intelligent_query（智能查询模块）

| 方法 | 必传参数 | 功能说明 |
|------|---------|----------|
| query | question | 主查询接口，一站式智能查询 |
| understand_question | question | 理解用户问题，提取关键信息 |
| generate_sql | understanding | 根据理解结果生成SQL |
| execute_query | sql | 执行SQL查询 |

## 返回格式 | Return Format

所有操作的返回结果均为统一JSON格式：

```json
{
  "code": 0,
  "msg": "success",
  "data": {}
}
```

### 状态码说明 | Status Code Description

- **0**：操作成功
- **-1**：缺失必传参数action
- **-2**：不支持的action
- **-3**：缺失当前action的必传参数
- **-4**：MCP接口请求失败
- **-5**：MindsDB连接超时
- **-6**：MindsDB服务不可达
- **-7**：HTTP请求异常
- **-8**：未知异常
- **-9**：MindsDB服务未就绪
- **-10**：本地RAG初始化失败
- **-11**：元数据提取失败（新增）

## 注意事项 | Notes

- 创建RAG知识库前，建议先通过db_connector或workflow_rag_analysis连接数据源
- RAG知识库的名称（kb_name）需唯一，重复创建会返回错误
- 首次使用本地RAG时会自动下载all-MiniLM-L6-v2模型（约80MB），优先从国内源下载
- 本地RAG使用ChromaDB持久化存储，数据保存在`data/chromadb_persist`目录
- 数据字典自动持久化到`data/data_dictionary.json`文件
- **元数据自动提取**功能仅支持DuckDB数据库，其他数据库需要手动配置元数据
- **智能查询引擎**依赖元数据，首次使用会自动提取并缓存

## 项目结构 | Project Structure

```
mindsdb-mcp-skill/
├── scripts/
│   ├── db_connector.py           # 公共数据库连接模块
│   ├── workflow_rag_build.py     # 工作流1：本地RAG构建与管理
│   ├── workflow_rag_analysis.py  # 工作流2：基于RAG的NLP2SQL和数据分析
│   ├── data_dictionary.py        # 数据字典实现
│   ├── metadata_extractor.py     # 元数据自动提取模块（新增v2.1.0）
│   ├── intelligent_query.py      # 智能查询引擎（新增v2.1.0）
│   └── mindsdb_skill.py          # 原核心技能代码（保留兼容）
├── evals/
│   └── evals.json                # 测试用例
├── data/
│   ├── chromadb_persist/         # RAG向量数据持久化目录
│   └── data_dictionary.json      # 数据字典持久化文件
├── references/                   # 参考文档
├── README.md                     # 说明文档
├── SKILL.md                      # 技能定义文件
└── mcp.json                      # MCP配置文件
```

## 版本历史 | Version History

- **v2.1.0** (2026-03-19)：新增元数据自动提取与智能查询功能
  - 新增metadata_extractor模块，支持自动提取数据库元数据
  - 新增intelligent_query模块，支持基于元数据的智能查询
  - 优化RAG知识库构建流程，自动包含元数据
  
- **v2.0.0** (2026-03-19)：重构为三模块架构（db_connector、workflow_rag_build、workflow_rag_analysis）

- **v1.2.0**：原单模块架构版本
