---
name: performance-evaluation
description: (project - Skill) 团队绩效评分自动化处理。整合TAPD缺陷查询、Excel处理和智能体团队协作，实现月度绩效考核的自动化计算。使用场景：(1) 处理前端组绩效Excel表格 (2) 查询TAPD缺陷数据生成评分链接 (3) 计算绩效系数 (4) 更新汇总表。Triggers: "绩效", "考核", "评分", "绩效表", "coefficient"
---

# 绩效评分技能 (Performance Evaluation)

自动化处理团队月度绩效考核Excel文件，整合TAPD缺陷查询、Excel处理和智能体团队协作。

## Agent 团队配置

使用 Agent 工具创建智能体团队，并行处理不同任务：

| 角色 | 模型 | 职责 |
|------|------|------|
| 数据处理员 | glm-5 | Excel读写、表格格式化、数据合并 |
| tapd操作员 | MiniMax-M2.5 | TAPD API调用、缺陷查询、URL生成 |
| 绩效评估员 | kimi-k2.5 | 评分计算、系数计算、汇总表更新 |

## 快速启动

```bash
# 合并个人表格到工作簿（推荐）
python3 scripts/merge_sheets.py --input-dir "bech/3m/" --month 3 --year 2026

# 仅修复现有工作簿中的标题和日期
python3 scripts/merge_sheets.py --file "绩效表格.xlsx" --month 3 --fix-only

# 预览模式（不保存文件）
python3 scripts/merge_sheets.py --input-dir "bech/3m/" --month 3 --dry-run
```

## 工作流程

### Phase 1: 表格合并与格式化

1. 合并成员表格到工作簿
2. 修复标题: "[月份]绩效考核表"
3. 设置考核周期: "YYYY.M.D-YYYY.M.D"
4. 移除空白行列

### Phase 2: 绩效评分

1. 检查上级评分，若为空则填入自评分
2. 查询TAPD缺陷数据
   - 生产质量: 开发人员=姓名, version_report=线上版本, 排除closed|rejected
   - 测试质量: 开发人员=姓名, version_report=测试版本, 排除closed|rejected
3. 参考"评分等级"列计算上级评分
4. 填入TAPD URL链接

### Phase 3: 汇总表更新

1. 提取成员上级评分
2. 计算绩效系数（见 coefficient_rules.md）
3. 更新或新增汇总记录

## 环境配置

```bash
# TAPD API 凭证（用于查询缺陷数据）
export TAPD_ACCESS_TOKEN="你的个人访问令牌"  # 推荐
# 或
export TAPD_API_USER="API账号"
export TAPD_API_PASSWORD="API密钥"

# 项目配置
export TAPD_WORKSPACE_ID="50372234"  # 聚宝赞项目
```

## Excel 单元格结构

### 成员工作表

| 单元格 | 内容 |
|--------|------|
| A1 | 标题 (如 "2月绩效考核表") |
| J2 | 考核周期 (如 "2026.2.1-2026.2.28") |
| J9 | 生产质量上级评分 |
| J10 | 测试质量上级评分 |
| K9 | 生产质量TAPD URL |
| K10 | 测试质量TAPD URL |

**特殊情况**：
- 陈方杰、刘奕君的上级评分在K列（第11列）

### 汇总工作表

| 列 | 内容 |
|----|------|
| A | 序号 |
| B | 部门 (合并单元格) |
| C | 岗位 |
| D | 姓名 |
| E | 绩效分数 |
| F | 绩效系数 |

## 绩效系数规则

| 分数范围 | 绩效系数 |
|----------|----------|
| >116 | 1.2 |
| 106-115 | 1.1 |
| 91-105 | 1.0 |
| 81-90 | 0.9 |
| ≤80 | 0.8 |

## 与 tapd-idle 技能集成

本技能依赖 `tapd-idle` 技能提供的 TAPDClient 类：

```python
# 从 tapd-idle 导入 TAPD 客户端
import sys
sys.path.insert(0, '/path/to/.agents/skills/tapd-idle/scripts')
from tapd_client import TAPDClient

client = TAPDClient()
# API参数: de = 开发人员（不是 developer）
bugs = client.get_bug({'workspace_id': '50372234', 'de': '姓名'})
```

**API参数对照**：
| 查询字段 | API参数 | 说明 |
|---------|---------|------|
| 开发人员 | `de` | 缺陷的开发人员 |
| 处理人 | `current_owner` | 缺陷的处理人 |
| 发现版本 | `version_report` | 缺陷发现的版本 |
| 创建时间 | `created` | 创建时间范围 |

**注意**：TAPD前端URL使用 `queryToken` 机制保存筛选条件，无法通过简单URL参数生成可分享的链接。需要在浏览器中手动设置筛选条件后使用"保存筛选"功能。

## 文件结构

```
performance-evaluation/
├── SKILL.md                 # 技能主文件
├── package.json             # 版本信息
├── .cursorrules             # Cursor规则
├── scripts/
│   ├── requirements.txt     # openpyxl>=3.1.0, requests>=2.25.0
│   ├── process_performance.py  # 主处理脚本
│   └── tapd_helper.py       # TAPD查询辅助函数
└── references/
    ├── excel_structure.md   # Excel单元格位置定义
    └── coefficient_rules.md # 绩效系数计算规则
```

## 命令详解

### process_performance.py

```bash
python3 scripts/process_performance.py [选项]

选项:
  --file PATH       绩效表格路径 (必需)
  --month MONTH     月份 (1-12)
  --year YEAR       年份 (默认当前年)
  --fix-format      仅修复格式
  --calculate-scores 仅计算评分
  --update-summary  仅更新汇总表
  --dry-run         预览变更不执行
  --output PATH     输出文件路径 (默认覆盖原文件)
```

### tapd_helper.py

```bash
# 查询缺陷
python3 scripts/tapd_helper.py query-bugs --developer "姓名" --version "线上版本" --created "2026-02-01~2026-02-28"

# 生成TAPD URL
python3 scripts/tapd_helper.py build-url --developer "姓名" --version "线上版本" --created "2026-02-01~2026-02-28"

# 统计缺陷数量
python3 scripts/tapd_helper.py count-bugs --developer "姓名" --version "线上版本" --created "2026-02-01~2026-02-28"
```

### merge_sheets.py

```bash
python3 scripts/merge_sheets.py [选项]

选项:
  --input-dir DIR   个人表格所在目录（合并模式）
  --file PATH       现有工作簿路径（仅修复模式）
  --output PATH     输出文件路径（合并模式，可选）
  --month MONTH     月份 (1-12, 必需)
  --year YEAR       年份（默认当前年）
  --dry-run         预览模式，不保存文件
```

**功能说明**:

1. **合并模式** (`--input-dir`):
   - 扫描目录下所有 `.xlsx` 文件（排除汇总文件）
   - 合并到指定工作簿，替换同名工作表
   - 自动修复标题月份和考核周期

2. **仅修复模式** (`--file`):
   - 修复现有工作簿中的标题和日期错误
   - 不合并新文件

**自动修复规则**:

| 问题 | 修复规则 |
|------|----------|
| 标题 "x月" | 替换为指定月份 |
| 标题月份错误 | 替换为正确月份 |
| 年份 2025 | 替换为 2026 |
| 月份错误 | 替换为正确月份 |
| 汇总表月份 | 更新为指定月份 |
| 姓名字段错误 | 更新为工作表名称 |

**文件名姓名提取**:

支持从包含额外信息的文件名中提取姓名：

| 文件名格式 | 提取结果 |
|------------|----------|
| `周树梧.xlsx` | 周树梧 |
| `前端组_周树梧.xlsx` | 周树梧 |
| `2026年3月_周树梧.xlsx` | 周树梧 |
| `周树梧_绩效.xlsx` | 周树梧 |
| `3月_周树梧_前端.xlsx` | 周树梧 |

提取规则：
1. 纯姓名文件名（2-4个中文字符）直接返回
2. 下划线分割时，查找2-4个中文字符的部分
3. 排除包含年、月、组、部门等关键词的部分
4. 无法提取时返回原文件名（去掉后缀）
## 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| TAPD连接失败 | 跳过URL填充，继续处理其他任务 |
| 单元格为空 | 保留原值或填入默认值 |
| 工作表不存在 | 打印警告，跳过该成员 |
| 环境变量未设置 | 提示用户配置TAPD凭证 |

## 示例使用场景

### 场景1: 完整处理流程

```bash
python3 scripts/process_performance.py \
    --file "bech/2m/研发中心-2月份-前端组绩效.xlsx" \
    --month 2 --year 2026
```

输出:
```
=== 绩效考核表处理开始 ===

加载文件: bech/2m/研发中心-2月份-前端组绩效.xlsx

1. 修复标题月份错误:
  [吴铝] 标题: '1月绩效考核表' -> '2月绩效考核表'
  [李金涛] 标题: '1月绩效考核表' -> '2月绩效考核表'

2. 修复考核周期错误:
  [吴铝] 考核周期: '2026.1.1-2026.1.31' -> '2026.2.1-2026.2.28'

3. 查询TAPD bug数据:
  [吴铝] 生产质量: 3条, 测试质量: 2条
  [文武] 生产质量: 1条, 测试质量: 0条

4. 更新汇总表:
  吴铝: 95 -> 95, 系数=1.0
  文武: 88 -> 88, 系数=0.9

=== 处理完成 ===
```

### 场景2: 仅查询TAPD数据

```bash
python3 scripts/tapd_helper.py query-bugs \
    --developer "吴铝" \
    --version "线上版本" \
    --created "2026-02-01~2026-02-28"
```

## 参考文档

- `references/excel_structure.md` - Excel单元格详细位置
- `references/coefficient_rules.md` - 绩效系数计算规则
- `../tapd-idle/SKILL.md` - TAPD技能使用指南