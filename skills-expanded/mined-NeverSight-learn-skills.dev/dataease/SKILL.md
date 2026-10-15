---
name: dataease
description: DataEase V2 全能技能 - 创建图表看板、查询数据集、管理组织、导出截图/PDF。支持柱状图、折线图、饼图、明细表，部署后自动截图展示。
environment:
  required:
    - DATAEASE_ACCESS_KEY
    - DATAEASE_SECRET_KEY
    - DATAEASE_BASE_URL
security:
  requiresSecrets: true
  sensitiveEnvironment: true
  externalNetworkAccess: true
---

# DataEase V2 全能技能

一站式 DataEase 自动化解决方案，融合图表部署与资源管理能力。

## 🎯 核心功能

| 功能模块 | 命令 | 说明 |
|---------|------|------|
| 📊 数据探索 | `inspect_data.py` | 查询数据集列表、字段信息 |
| 📈 图表部署 | `deploy.py` | 创建单图表并自动截图 |
| 📋 多图看板 | `multi_deploy.py` | 创建多图表仪表板并自动截图 |
| 🏢 组织管理 | `capture_dashboard.py list-orgs/switch-org` | 查询/切换组织 |
| 📑 资源列表 | `capture_dashboard.py list-resources` | 列出仪表板/大屏 |
| 📸 截图导出 | `capture_dashboard.py capture` | 导出仪表板截图或PDF |

## 🎭 沟通风格 (Persona)

作为 DataEase 自动化专家：
1. **执行优先**: 直接运行工具，不预先展示代码
2. **结果导向**: 优先展示截图，再说明逻辑
3. **单次往复**: 一次完成从探索到部署的全过程

## 🚀 环境配置

### 1. 配置凭据

复制 `.env.example` 为 `.env`，填写：

```bash
DATAEASE_BASE_URL=https://your-dataease.example.com
DATAEASE_ACCESS_KEY=your_access_key
DATAEASE_SECRET_KEY=your_secret_key
DATAEASE_USERNAME=admin          # 可选，用于密码登录
DATAEASE_PASSWORD=your_password  # 可选
DATAEASE_LOGIN_ORIGIN=0          # 登录源

# 截图输出目录（必须在 OpenClaw workspace 内才能用 MEDIA: 展示,不输入默认直接在 OpenClaw workspace 内创建）
DATAEASE_OUTPUT_DIR=/Users/username/.openclaw/workspace/dataease-output
```

### 2. 安装截图依赖

首次使用需安装 Playwright 浏览器：

```bash
cd {baseDir}
npm install
npx playwright install chromium
```

### 3. 验证连接

```bash
python3 scripts/inspect_data.py --list-datasets
```

---

## 📊 数据探索

### 查询所有数据集
```bash
python3 scripts/inspect_data.py --list-datasets
```

### 查询特定数据集字段
```bash
python3 scripts/inspect_data.py --dataset "<数据集名称或ID>"
```

**返回示例**：
```json
[
  {"name": "产品", "type": 0, "id": "..."},
  {"name": "销售额", "type": 2, "id": "..."}
]
```

字段类型：`0`=文本, `1`=日期, `2`=指标, `3`=数值

---

## 📈 图表部署

### 单图表部署（自动截图）
```bash
python3 scripts/deploy.py <type> <title> <dataset> <x_fields> <y_fields>
```

**参数说明**：
- `type`: `bar`(柱状图), `line`(折线图), `pie`(饼图), `table_info`(明细表)
- `title`: 图表标题
- `dataset`: 数据集名称或ID
- `x_fields`: 维度字段（逗号分隔）
- `y_fields`: 指标字段（逗号分隔）

**示例**：
```bash
python3 scripts/deploy.py bar '各产品销售额' '销售数据' '产品' '实际销售'
python3 scripts/deploy.py bar '销售对比' '销售数据' '公司' '期望销售,实际销售'
python3 scripts/deploy.py pie '产品占比' '销售数据' '产品类别' '实际销售'
```

**可选参数**：
- `--no-screenshot`: 跳过截图，仅返回链接

**输出**：
- 自动截图并返回 JSON 结果（包含 `screenshot` 路径）
- Agent 应使用 `MEDIA:<screenshot_path>` 展示截图

### 多图表看板部署
```bash
python3 scripts/multi_deploy.py <dashboard_title> '<charts_json>'
```

**JSON 结构**：
```json
[
  {
    "type": "bar",
    "title": "图表标题",
    "dataset_name": "数据集名",
    "x_axis": ["维度字段"],
    "y_axis": ["指标1", "指标2"]
  }
]
```

**示例**：
```bash
python3 scripts/multi_deploy.py '销售分析看板' '[
  {"type":"bar","title":"各产品销售","dataset_name":"销售数据","x_axis":["产品"],"y_axis":["实际销售"]},
  {"type":"pie","title":"类别占比","dataset_name":"销售数据","x_axis":["产品类别"],"y_axis":["实际销售"]}
]'
```

---

## 🏢 组织管理

### 查询组织列表
```bash
python3 scripts/capture_dashboard.py list-orgs
```

**返回**：所有可用组织及其 ID

### 切换组织
```bash
python3 scripts/capture_dashboard.py switch-org --org-id <组织ID>
```

切换后，后续操作将在新组织上下文中执行。

---

## 📑 资源列表

### 列出仪表板
```bash
python3 scripts/capture_dashboard.py list-resources --busi-type dashboard
```

### 列出数据大屏
```bash
python3 scripts/capture_dashboard.py list-resources --busi-type dataV
```

### 指定组织查询
```bash
python3 scripts/capture_dashboard.py list-resources --org-id <组织ID> --busi-type dashboard
```

---

## 📸 截图导出

### 导出仪表板截图
```bash
python3 scripts/capture_dashboard.py capture \
  --resource-id <仪表板ID> \
  --busi-type dashboard \
  --output-dir <输出目录>
```

### 导出数据大屏
```bash
python3 scripts/capture_dashboard.py capture \
  --resource-id <大屏ID> \
  --busi-type dataV \
  --output-dir <输出目录>
```

### 导出 PDF
```bash
python3 scripts/capture_dashboard.py capture \
  --resource-id <ID> \
  --busi-type dashboard \
  --result-format 1 \
  --output-dir <输出目录>
```

### 按名称匹配导出
```bash
python3 scripts/capture_dashboard.py capture \
  --resource-name "销售总览" \
  --busi-type dashboard
```

### 高级参数
- `--pixel`: 分辨率，默认 `1920*1080`，可用 `2560*1440`
- `--ext-wait-time`: 额外等待时间（秒），用于复杂图表
- `--org-id`: 指定组织 ID

### ⚠️ 导出结果处理

**重要：导出的图片和 PDF 必须直接发送到对话中展示！**

截图或 PDF 导出成功后，返回的 JSON 中包含 `saved_file` 字段：
```json
{
  "ok": true,
  "saved_file": "/path/to/file.jpg"  // 或 .pdf
}
```

**Agent 必须执行：**
1. 读取 `saved_file` 路径
2. 使用 `MEDIA:<saved_file>` 语法直接发送到对话中

**示例：**
```
MEDIA:/path/to/output/仪表板名_123456.jpg
MEDIA:/path/to/output/仪表板名_123456.pdf
```

**不要只返回文件路径，必须使用 MEDIA: 发送文件！**

---

## 🛠 参数规范

### 图表类型
| 类型 | 说明 | 适用场景 |
|-----|------|---------|
| `bar` | 柱状图 | 分类对比、排名 |
| `line` | 折线图 | 趋势分析、时序数据 |
| `pie` | 饼图 | 占比分析、构成分布 |
| `table_info` | 明细表 | 数据明细展示 |

### 维度与指标
- **维度 (x_axis)**: 类别、日期等分组字段
- **指标 (y_axis)**: 数值、金额等聚合字段
- 明细表的 `y_axis` 传空，`x_axis` 列出所有展示字段

### 业务类型
- `dashboard`: 仪表板
- `dataV`: 数据大屏

---

## 📸 结果处理

### 图表部署结果

部署成功后输出 JSON：
```json
{
  "ok": true,
  "dashboard_id": "1243929230048366592",
  "url": "https://...",
  "screenshot": "/path/to/screenshot.jpg",
  "title": "图表标题"
}
```

**Agent 处理流程**：
1. 读取 `screenshot` 路径图片
2. 使用 `MEDIA:<screenshot_path>` 展示
3. 同时提供访问链接

### 截图导出结果

```json
{
  "ok": true,
  "resource_id": "...",
  "resource_name": "...",
  "saved_file": "/path/to/file.jpg",
  "pixel": "1920*1080",
  "capture_engine": "local_playwright"
}
```

---

## ⚠️ 常见问题

### SSL 证书错误
macOS 上 Python 可能缺少系统证书，运行：
```bash
/Applications/Python\ 3.13/Install\ Certificates.command
```

### Playwright 浏览器未安装
```bash
npx playwright install chromium
```

### 截图超时
使用 `--ext-wait-time` 增加等待时间：
```bash
python3 scripts/capture_dashboard.py capture --resource-id <ID> --ext-wait-time 5 --busi-type dashboard
```

### 资源名称匹配失败
使用 `--resource-id` 精确指定，或查看 `candidates` 字段获取候选列表。

---

## 📁 文件结构

```
skills/dataease-chart-skill/
├── SKILL.md              # 本文档
├── .env                  # 环境配置
├── .env.example          # 配置模板
├── package.json          # Node 依赖
├── scripts/
│   ├── inspect_data.py   # 数据探索
│   ├── deploy.py         # 单图表部署
│   ├── multi_deploy.py   # 多图表部署
│   ├── engine.py         # 图表引擎
│   ├── multi_engine.py   # 多图表引擎
│   ├── client.py         # API 客户端
│   ├── capture_dashboard.py  # 截图/资源管理
│   └── browser_capture.mjs   # 浏览器截图
├── templates/            # 图表模板
│   ├── chart_bar/
│   ├── chart_line/
│   ├── chart_pie/
│   └── chart_table_info/
├── references/           # 参考文档
│   ├── api.md
│   └── resource_aliases.json
├── agents/
│   └── openai.yaml
└── output/               # 截图输出目录
```
