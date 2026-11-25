---
name: clawshire-data-query
description: ClawShire 公告数据查询技能 - A 股上市公司公告提取结果查询，支持按日期范围、证券代码、公告原文链接检索结构化提取数据
---

# ClawShire 公告数据查询技能

A 股上市公司公告提取结果查询服务。支持按日期范围、证券代码、公告原文链接检索结构化提取数据。

**服务地址：** `https://api.clawshire.cn`

---

## 前置检查

在执行任何 API 调用前，必须检查 `CLAWSHIRE_API_KEY` 环境变量是否存在。
- 只判断是否存在，**不得**在输出中明文显示 key 内容
- 若不存在，引导用户注册获取：`https://api.clawshire.cn/docs`

---

## 认证方式

若接口需要认证，所有请求头携带：

```
Authorization: Bearer $CLAWSHIRE_API_KEY
```

公告查询接口（`/api/v1/announcements`、`/api/v1/stock/{sec_code}/announcements`、`/api/v1/met_link`）**无需认证**即可调用。

---

## 工作流

### 工作流 1：按日期查询公告

适用场景：用户想获取某天或某段时间内的所有公告提取结果。

**步骤：**
1. 确认日期范围（`start_date`、`end_date`，格式 `YYYY-MM-DD`）
2. 可选：用户是否指定公告类别（`infotype`，如 `董事会决议`）
3. 调用 `GET /api/v1/announcements`
4. 展示结果：公告总数、公司名、公告类型、日期、结构化提取内容

**默认行为：**
- 未指定数量时，默认展示前 20 条（`page_size=20`）
- 结果包含 `extracted_info` 字段时，完整展示提取内容

---

### 工作流 2：按证券代码查询公告

适用场景：用户关注特定上市公司的公告。

**步骤：**
1. 确认证券代码（6 位数字，如 `000001`）
2. 可选：日期范围（默认当天）、公告类别筛选
3. 调用 `GET /api/v1/stock/{sec_code}/announcements`
4. 展示该公司的公告列表及提取结果

---

### 工作流 3：按公告链接查询

适用场景：用户有公告原文链接，想获取结构化提取结果。

**步骤：**
1. 获取用户提供的公告原文链接（`met_link`）
2. 调用 `GET /api/v1/met_link?met_link=<url_encoded_link>`
3. 展示该公告的完整提取结果

---

### 工作流 4：获取 API Key

适用场景：用户需要获取 API Key。

**步骤：**
1. 引导用户登录控制台：`https://clawshire.cn`
2. 在控制台完成登录认证后，手动创建 API Key
3. 将控制台生成的 `api_key` 设置为环境变量：
   ```bash
   export CLAWSHIRE_API_KEY="sk-xxxxxxxx"
   ```

> API Key 必须在控制台登录后手动创建，不支持通过 API 接口注册或获取。

---

## 结果展示规范

每条公告结果必须包含：
- **公司**：`{sec_name}（{sec_code}）`
- **类型**：`infotype`
- **日期**：`doc_date`
- **原文链接**：`met_link`
- **提取内容**：`extracted_info` 的完整 JSON（若存在）

---

## 调用限制

- **免费账户**：每个 API Key 共 100 次调用额度，请合理规划使用
- 每次查询日期范围建议不超过 30 天，避免结果过多
- `page_size` 最大 100，超出需分页获取
- 若用户未指定数量，默认 `page_size=20`
- 建议优先用宽日期范围 + 类别筛选一次性取完，减少不必要的翻页请求

---

## 错误处理

| 错误码 | 含义 | 处理方式 |
|:------:|------|----------|
| 400 | 参数错误 | 检查日期格式（YYYY-MM-DD）和必填字段 |
| 401 | API Key 无效 | 提示用户检查 `CLAWSHIRE_API_KEY` 环境变量 |
| 404 | 资源不存在 | 确认证券代码或链接是否正确 |
| 500 | 服务器错误 | 稍后重试，或访问 https://clawshire.cn 查看服务状态 |
