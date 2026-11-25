---
name: terminology-consistency-check
description: 检查文档中的术语一致性，包括：同一术语的多种表达方式（如 AppID/App Id/APPID）、中英文混用问题、大小写不一致、专业术语的统一性检查。当审核文档质量、检查术语使用规范或优化文档表达时使用此技能。
---

# 术语一致性检查

## 审核流程

### 步骤 1：收集文档术语

通读文档，列出所有发现的技术术语及其不同表达方式。重点关注：
- 产品相关术语（AppID、Token、AppSign 等）
- 平台相关术语（iOS、Android、macOS 等）
- 功能相关术语（Room/房间、Stream/流 等）

### 步骤 2：对照标准术语规范

将收集的术语与workspace下的[术语说明](general/zh/docs_glossary_zh/Term Explanation.mdx)内容对照，识别不一致之处。

### 步骤 3：执行一致性检查

按照检查维度逐项检查，记录问题位置和具体内容。

### 步骤 4：输出检查结果

按照输出格式模板，整理并输出检查结果。

## 检查维度

### 1. 术语表达一致性

检查同一概念是否有多种表达方式。

**常见需要统一的术语**：

| 标准表达 | 错误/不一致表达 |
|---------|----------------|
| AppID | App Id、APPID、appid、app ID |
| AppSign | App Sign、APPSIGN、appsign |
| Token | token、TOKEN |
| SDK | sdk、Sdk |
| API | api、Api |
| iOS | ios、IOS |
| Android | android、ANDROID |
| macOS | Mac OS、MacOS |
| Windows | windows、WINDOWS |
| 用户端 | 用户客户端、用户侧 |
| 服务端 | 服务器、Server、服务端 |

### 2. 中英文混用检查

检查是否存在不必要的句中英文混用，影响阅读体验。

**允许的情况**：
- 专有名词（SDK、API、AppID 等）
- 代码相关内容（函数名、参数名等）
- 已广泛使用的缩写（HTTP、HTTPS、JSON 等）

**不建议的情况**：
- "请先 login 再操作" → 应为 "请先登录再操作"
- "点击 confirm 按钮" → 应为 "点击确认按钮"

### 3. 大小写一致性

检查同一术语在不同位置的大小写是否一致。

## 输出格式

```markdown
## 术语一致性检查结果

### ✅ 术语检查通过
未发现术语一致性问题。

### ❌ 术语表达不一致

1. **AppID 相关**
   - 标准表达：AppID
   - 发现的其他表达：
     - 第 X 行：App Id
     - 第 Y 行：appid
     - 第 Z 行：APPID

2. **SDK 相关**
   - 标准表达：SDK
   - 发现的其他表达：
     - 第 X 行：sdk
     - 第 Y 行：Sdk

### ⚠️ 中英文混用问题

1. 第 X 行："请先 login 再操作"
   建议：改为"请先登录再操作"

2. 第 Y 行："点击 confirm 按钮确认"
   建议：改为"点击确认按钮确认"
```