---
name: clawshire-financial-analysis
description: ClawShire 财务风险分析技能 - 上传上市公司年报 PDF，调用 25+ 条分析规则输出整体风险评级（低/中/高）及各规则详细结论
---

# ClawShire 财务风险分析技能

对上市公司年度报告 PDF 进行深度财务风险评估。上传 PDF 后，系统自动解析、提取、分析，输出整体风险评级（低/中/高）和各规则详细结论。

**服务地址：** `https://api.clawshire.cn`

---

## 前置检查

在执行任何 API 调用前，必须检查 `CLAWSHIRE_API_KEY` 环境变量是否存在。

- 只判断是否存在，**不得**在输出中明文显示 key 内容
- 若不存在，引导用户登录控制台创建：`https://clawshire.cn`

---

## 认证方式

所有请求头携带：

```http
Authorization: Bearer $CLAWSHIRE_API_KEY
```

---

## 工作流

### 工作流 1：分析年报 PDF

适用场景：用户有年报 PDF 文件，需要快速获取财务风险评估结论。

**步骤：**

1. 确认 PDF 文件路径（本地文件，最大 100MB）
2. 调用 `POST /api/v1/financial-analysis/jobs` 上传 PDF
3. 用返回的 `job_id` 轮询 `GET /api/v1/financial-analysis/jobs/{job_id}`，直到 `status` 为 `completed`
4. 展示分析结果：整体风险评级 + 高/中风险规则列表

**注意：**

- 分析通常耗时 2～8 分钟，请耐心等待
- 轮询建议间隔 5 秒

**示例：**

```text
上传 PDF
→ POST /api/v1/financial-analysis/jobs
  Content-Type: multipart/form-data
  file=年报.pdf, language=zh

← {"id": "job_xxxxx", "status": "pending", ...}

轮询结果
→ GET /api/v1/financial-analysis/jobs/job_xxxxx
← {
    "status": "completed",
    "overall_risk_level": "medium",
    "rule_results": [
      {"display_name_zh": "收入真实性", "risk_level": "high", ...},
      ...
    ]
  }
```

**使用脚本：**

```bash
# 终端输出风险摘要
python skills/clawshire-financial-analysis/scripts/financial_analysis_client.py analyze path/to/年报.pdf

# 导出 HTML 报告（自动命名，保存到同目录）
python skills/clawshire-financial-analysis/scripts/financial_analysis_client.py analyze path/to/年报.pdf --output html

# 英文报告
python skills/clawshire-financial-analysis/scripts/financial_analysis_client.py analyze path/to/report.pdf --lang en --output html
```

---

### 工作流 2：查看所有分析规则

适用场景：用户想了解系统支持哪些风险分析维度。

**步骤：**

1. 调用 `GET /api/v1/financial-analysis/rules`
2. 展示规则列表：规则名称、分类、描述

**使用脚本：**

```bash
python skills/clawshire-financial-analysis/scripts/financial_analysis_client.py rules
```

---

### 工作流 3：获取 API Key

**步骤：**

1. 引导用户登录控制台：`https://clawshire.cn`
2. 在控制台创建 API Key，并开通财务分析权限
3. 设置环境变量：

```bash
export CLAWSHIRE_API_KEY="sk-xxxxxxxx"
```

---

## 结果展示规范

分析完成后必须展示：

- **整体风险评级**：低风险 / 中风险 / 高风险
- **高风险项**：列出所有 `risk_level = "high"` 的规则名称和结论
- **中风险项**：列出所有 `risk_level = "medium"` 的规则名称和结论
- **规则统计**：共分析 N 条规则，高/中/低/不适用各几条
- **分析耗时**：从提交到完成的时间

若无高/中风险项，明确告知「未发现高风险或中风险项」。

---

## 接口说明

### 上传分析任务

```http
POST /api/v1/financial-analysis/jobs
Authorization: Bearer {api_key}
Content-Type: multipart/form-data

file: <PDF 文件>
language: zh | en  （默认 zh）
```

响应：

```json
{
  "id": "job_xxxxx",
  "status": "pending",
  "created_at": "2026-03-20T10:00:00Z"
}
```

### 查询任务状态

```http
GET /api/v1/financial-analysis/jobs/{job_id}
Authorization: Bearer {api_key}
```

响应（完成时）：

```json
{
  "id": "job_xxxxx",
  "status": "completed",
  "overall_risk_level": "medium",
  "rule_results": [
    {
      "rule_id": "revenue_authenticity",
      "display_name_zh": "收入真实性",
      "display_name_en": "Revenue Authenticity",
      "rule_category": "收入质量",
      "risk_level": "high",
      "conclusion_zh": "...",
      "evidence": ["..."]
    }
  ]
}
```

`status` 取值：`pending` → `parsing` → `chunking` → `extracting` → `analyzing` → `completed` / `failed`

### 查询规则列表

```http
GET /api/v1/financial-analysis/rules
Authorization: Bearer {api_key}
```

---

## 调用限制

- **免费账户**：每个 API Key 共 100 次调用额度
- 每次上传 PDF 消耗 1 次额度
- PDF 文件最大 100MB
- 分析耗时 2～8 分钟，超时请重试

---

## 错误处理

| 错误码 | 含义 | 处理方式 |
| --- | --- | --- |
| 400 | 参数错误或非 PDF 文件 | 检查文件格式和请求参数 |
| 401 | API Key 无效或未开通权限 | 检查 `CLAWSHIRE_API_KEY`，并在控制台开通财务分析权限 |
| 413 | 文件过大 | PDF 不超过 100MB |
| 500 | 服务器错误 | 稍后重试，或访问 [clawshire.cn](https://clawshire.cn) 查看服务状态 |
