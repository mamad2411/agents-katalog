---
name: generate-test-docs
description: 自主学习型测试文档生成器。从需求文档（PDF/Word/Markdown）生成测试文档，支持持久化记忆和持续学习。当用户提到"生成测试用例"、"测试计划"、"测试报告"或"根据需求生成测试"时触发。
allowed-tools: Write Read Glob Bash AskUserQuestion
compatibility: Requires Python 3, openpyxl, PyMuPDF, python-docx
---

# 自主学习型测试文档生成器

从需求文档自动生成专业测试文档，具备项目感知、持续学习和专业测试设计方法能力。

## 核心能力

- **专业测试设计方法**：等价类划分、边界值分析、场景法、错误推测法
- **需求追溯矩阵**：自动生成需求-用例追溯关系，计算覆盖率
- **优先级管理**：P0-P3 优先级分类，支持冒烟/核心/全量回归测试集
- **自主学习**：学习项目模板、领域术语、命名规范
- **交互式确认**：关键节点询问用户，支持快速/专家双模式

## 交互模式

详见 [INTERACTION-PATTERNS.md](references/INTERACTION-PATTERNS.md)

### 模式定义

| 模式 | 名称 | 适用场景 | 确认方式 |
|------|------|---------|---------|
| `quick` | 快速模式 | 日常生成、熟悉流程 | 回车继续，仅问题时询问 |
| `expert` | 专家模式 | 首次使用、精细控制 | 每阶段确认，完整预览 |

### 交互检查点

| 检查点 | 阶段 | Quick 模式 | Expert 模式 |
|--------|------|-----------|-------------|
| 解析确认 | Phase 2.5 | 摘要 + 有问题时询问 | 完整列表 + 等待确认 |
| 歧义处理 | Phase 2.6 | 仅关键歧义 | 所有歧义 |
| 生成预览 | Phase 2.8 | 统计数据 | 统计 + 样例 + 可调整 |
| 输出选择 | Phase 2.9 | 确认默认配置 | 完整格式选择 |

### 模式切换

- **首次运行**：询问用户选择模式
- **命令切换**：`切换模式` / `快速模式` / `专家模式`
- **偏好存储**：`.memory/user-preferences.json`

## 首次使用

检测或询问用户项目结构：
- 模板文件夹路径（默认: `./templates`）
- 需求文档路径（默认: `./requirements`）
- 创建 `.memory` 文件夹用于存储学习数据

**安装依赖**：
```bash
pip install openpyxl PyMuPDF python-docx
```

## 测试设计方法

详见 [TEST-DESIGN-METHODS.md](references/TEST-DESIGN-METHODS.md)

### 方法选择指南

| 需求特征 | 推荐方法 |
|---------|---------|
| 有明确输入范围/格式要求 | 等价类划分 + 边界值分析 |
| 涉及业务流程/多步骤操作 | 场景法 |
| 历史缺陷多/高风险模块 | 错误推测法 |

### 核心4种方法

1. **等价类划分法 (EP)**
   - 划分有效/无效等价类
   - 一条用例覆盖多个有效类，每个无效类单独覆盖

2. **边界值分析法 (BVA)**
   - 测试边界点：上点、离点、内点
   - 对闭区间 [a,b]：测试 a-1, a, b, b+1

3. **场景法 (ST)**
   - 识别基本流、备选流、异常流
   - 每条路径生成对应用例

4. **错误推测法 (EG)**
   - 基于经验推测常见错误
   - 补充特殊字符、极端值、并发等测试

### 用例设计流程

```
1. 等价类划分 → 识别所有输入的有效/无效等价类
       ↓
2. 边界值分析 → 对每个等价类的边界进行测试
       ↓
3. 场景法     → 覆盖主要业务流程（基本流+备选流+异常流）
       ↓
4. 错误推测   → 补充经验性测试用例
```

## 需求追溯与覆盖率

详见 [TRACEABILITY.md](references/TRACEABILITY.md)

### 追溯矩阵

生成用例时自动关联需求ID，输出包含：
- **正向追溯**：需求ID → 关联用例列表
- **反向追溯**：用例 → 来源需求
- **覆盖率统计**：需求覆盖率、覆盖深度

### 需求ID提取规则

自动识别需求文档中的ID模式：
- `REQ_001`、`REQ-123`
- `F1.2`、`F-3.1.2`
- `US_042`
- JIRA格式：`PROJ-123`

若无明确ID，自动生成：`MOD_{模块缩写}_{序号}`

## 优先级与回归分类

详见 [TEST-PRIORITY.md](references/TEST-PRIORITY.md)

### 优先级定义

| 级别 | 定义 | 来源 |
|------|------|------|
| P0 | 核心功能，不可用则系统无法使用 | 基本流用例 |
| P1 | 主要功能，影响核心业务流程 | 备选流 + 边界值 |
| P2 | 次要功能，不影响主流程 | 异常流 + 错误推测 |
| P3 | 体验优化，边缘场景 | 边缘错误推测 |

### 回归测试集

| 测试集 | 包含用例 | 执行时机 |
|--------|---------|---------|
| 冒烟测试 | 所有 P0 | 每次构建 |
| 核心回归 | P0 + P1 | 每日/提测 |
| 全量回归 | 所有 | 发版前 |

## 项目感知

### 识别项目结构
1. 扫描项目根目录
2. 查找 `templates/`、`requirements/`、`docs/` 等目录
3. 识别模板文件和需求文档
4. 将识别结果存入 `.memory/project-context.json`

### 支持的文档格式

| 格式 | 扩展名 | 提取脚本 |
|------|--------|---------|
| PDF | .pdf | `scripts/extract_document.py --format pdf` |
| Word | .docx | `scripts/extract_document.py --format docx` |
| Markdown | .md | 直接读取 |
| 富文本 | .rtf | `scripts/extract_document.py --format rtf` |

## .memory 记忆系统

Skill 在项目中创建 `.memory/` 文件夹，存储学习数据：

### project-context.json
```json
{
  "project_name": "电商平台",
  "detected_at": "2024-01-15",
  "template_dir": "./templates",
  "requirements_dir": "./requirements",
  "output_dir": "./test-docs"
}
```

### template-schemas.json
```json
{
  "test_case": {
    "source": "./templates/测试用例模板.xlsx",
    "columns": ["用例编号", "模块名称", "用例标题", "优先级", "关联需求ID", "设计方法", "前置条件", "测试步骤", "预期结果", "实际结果", "是否通过", "回归类型", "备注"],
    "id_format": "TC_{module}_{seq:03d}",
    "learned_at": "2024-01-15"
  }
}
```

### terminology.json
```json
{
  "domain_terms": {
    "SKU": "库存单位",
    "GMV": "商品交易总额"
  },
  "module_abbreviations": {
    "用户登录": "LOGIN",
    "购物车": "CART"
  }
}
```

### generation-history.json
```json
{
  "generations": [
    {
      "date": "2024-01-15",
      "type": "test_case",
      "source": "PRD-v1.0.pdf",
      "output": "登录模块_测试用例_v1.xlsx",
      "case_count": 25,
      "coverage_rate": "95%"
    }
  ]
}
```

## Workflow

### Phase 0: 项目初始化（首次运行）
1. 询问或检测项目结构
2. **询问交互模式**：Quick（快速）或 Expert（专家）
3. 创建 `.memory/` 文件夹
4. 学习模板结构，存入 `template-schemas.json`
5. 提取领域术语，存入 `terminology.json`
6. 保存用户偏好到 `user-preferences.json`

### Phase 1: 读取需求
1. 用户指定需求文档或文件夹
2. 调用 `scripts/extract_document.py` 提取文本
3. 返回结构化内容

### Phase 2: 解析需求
1. 读取 `.memory/terminology.json` 理解领域术语
2. **提取需求ID**：识别或生成需求唯一标识
3. **结构识别**：功能模块、验收条件、业务规则
4. **等价类划分**：识别输入的有效/无效等价类
5. **边界值提取**：识别数值、长度、时间边界
6. **场景流识别**：识别基本流、备选流、异常流
7. **错误推测补充**：根据输入类型和模块类型触发
8. **歧义检测**：识别不明确的需求描述
9. 参考 [PARSING-RULES.md](references/PARSING-RULES.md)

### Phase 2.5: 【检查点1】解析确认
使用 **AskUserQuestion** 确认解析结果：

**Expert 模式**：
```markdown
显示完整解析结果表格：
- 识别的模块列表（名称、需求数、缩写）
- 提取的需求ID列表（ID、名称、验收条件数）
- 识别的业务规则
- 识别的边界条件

等待用户确认：确认 / 修改 / 重新解析
```

**Quick 模式**：
```markdown
显示摘要：已识别 X 个模块，Y 条需求，Z 条规则

仅在发现警告时询问用户
无警告则自动继续
```

### Phase 2.6: 歧义处理
对检测到的歧义需求逐一询问：

```markdown
需求原文：{text}
歧义类型：边界不明确 / 规则冲突 / 条件缺失
我的理解：{interpretation}

请选择：
1. 接受我的理解
2. 提供不同解释
3. 跳过此需求
4. 标记为待确认
```

- **Expert 模式**：询问所有歧义
- **Quick 模式**：仅询问影响 P0/P1 的关键歧义

### Phase 2.8: 【检查点2】生成预览
使用 **AskUserQuestion** 预览生成方案：

**Expert 模式**：
```markdown
显示优先级分布：P0/P1/P2/P3 数量和占比
显示设计方法分布：EP/BVA/ST/EG
显示样例用例：每个优先级展示1条

可选操作：
- 调整优先级分布
- 增加/减少特定类型用例
- 预览特定模块
```

**Quick 模式**：
```markdown
显示统计：将生成 X 条用例，P0:X | P1:X | P2:X | P3:X

仅在分布异常时询问（如 P0 > 20%）
正常则回车继续
```

### Phase 2.9: 【检查点3】输出选择
使用 **AskUserQuestion** 选择输出格式：

**Expert 模式**：
```markdown
多选输出格式：
- Excel 测试用例
- Markdown 测试用例
- 测试计划文档
- 测试报告模板

单选追溯矩阵：
- 包含在Excel中
- 单独生成文件
- 不生成
```

**Quick 模式**：
```markdown
确认默认配置（基于上次选择或默认）：
- ✅ Excel 测试用例（含追溯矩阵）
- ✅ 覆盖率统计

回车确认，或输入"更多"选择其他格式
```

### Phase 3: 生成文档
1. 读取 `.memory/template-schemas.json` 获取模板结构
2. **分配优先级**：根据用例类型自动判断 P0-P3
3. **设置回归类型**：根据优先级映射冒烟/核心/全量
4. **标记设计方法**：EP/BVA/ST/EG
5. **关联需求ID**：每个用例记录来源需求
6. 调用 `scripts/generate_excel.py` 生成 Excel（含追溯矩阵）

### Phase 4: 更新记忆
1. 记录本次生成到 `generation-history.json`
2. 如有新术语，更新 `terminology.json`
3. **保存用户偏好**到 `user-preferences.json`
4. 如用户反馈，调整学习数据

## 输出格式

### 测试用例 Excel

**默认列**：
| 列名 | 说明 |
|------|------|
| 用例编号 | TC_{MODULE}_{SEQ:03d} |
| 模块名称 | 功能模块 |
| 用例标题 | 测试点简述 |
| 优先级 | P0/P1/P2/P3（下拉选择，带颜色） |
| 关联需求ID | REQ_XXX（支持多个，逗号分隔） |
| 设计方法 | EP/BVA/ST/EG |
| 前置条件 | 执行前提 |
| 测试步骤 | 详细操作步骤 |
| 预期结果 | 期望行为 |
| 实际结果 | 执行时填写 |
| 是否通过 | 通过/未通过/阻塞/未执行 |
| 回归类型 | 冒烟/核心/全量 |
| 备注 | 补充说明 |

**额外 Sheet**（启用追溯时）：
- **需求追溯矩阵**：需求ID、关联用例、覆盖状态
- **覆盖率统计**：总需求数、覆盖率、优先级分布

### 测试计划 Markdown

固定8章节结构：
1. 测试目标
2. 测试范围
3. 测试策略
4. 测试环境
5. 测试资源
6. 测试进度
7. 风险与应对
8. 交付物

### 测试报告 Markdown

固定5章节结构：
1. 执行概述
2. 测试统计
3. 缺陷分析
4. 覆盖率报告
5. 结论与建议

## 脚本调用

### 提取文档
```bash
python3 "${SKILL_ROOT}/scripts/extract_document.py" \
  --input "/path/to/PRD.pdf" \
  --format pdf \
  --output "/tmp/prd-content.json"
```

### 生成 Excel（带追溯矩阵）
```bash
python3 "${SKILL_ROOT}/scripts/generate_excel.py" \
  --output "测试用例.xlsx" \
  --data '[{"用例编号":"TC_LOGIN_001", "优先级":"P0", "关联需求ID":"REQ_001", ...}]' \
  --traceability \
  --requirements '[{"id":"REQ_001", "name":"用户登录"}]'
```

### 管理记忆
```bash
python3 "${SKILL_ROOT}/scripts/memory_manager.py" \
  --action init \
  --project "/path/to/project"
```

## 学习能力

### 自动学习
- 首次使用时学习模板结构
- 从需求文档积累领域术语
- 识别命名规范并保持一致

### 用户反馈学习
- 用户修正后，询问是否记住
- 将反馈存入记忆供后续使用

### 记忆更新命令
```
"更新术语表"    → 重新扫描并更新 terminology.json
"重新学习模板"  → 重新解析模板结构
"清除记忆"      → 删除 .memory 文件夹
```

## 约束

- **需求追溯**：所有用例必须关联需求ID
- **方法标记**：所有用例必须标记设计方法
- **优先级覆盖**：P0 占比 10-15%，P1 占比 30-40%
- **交互确认**：Expert 模式下每个检查点必须等待用户确认
- **歧义处理**：发现不明确需求时必须询问用户（可配置）
- **模式记忆**：用户模式偏好存入 `.memory/user-preferences.json`
- 遵循项目已有的命名规范
- 不凭空编造需求中不存在的场景
- 默认输出中文，除非项目配置为其他语言
- `.memory` 文件夹应加入 .gitignore（可选）

## 参考文档

- [INTERACTION-PATTERNS.md](references/INTERACTION-PATTERNS.md) - 交互模式与问题模板
- [TEST-DESIGN-METHODS.md](references/TEST-DESIGN-METHODS.md) - 核心4种测试设计方法详解
- [TRACEABILITY.md](references/TRACEABILITY.md) - 需求追溯矩阵规范
- [TEST-PRIORITY.md](references/TEST-PRIORITY.md) - 优先级与回归分类
- [PARSING-RULES.md](references/PARSING-RULES.md) - 需求解析规则
- [MEMORY-SCHEMA.md](references/MEMORY-SCHEMA.md) - 记忆文件结构
- [LEARNING-RULES.md](references/LEARNING-RULES.md) - 学习规则
