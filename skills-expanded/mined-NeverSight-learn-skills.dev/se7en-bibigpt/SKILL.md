---
name: se7en-bibigpt
description: |
  通过 BibiGPT API 自动总结视频内容并提取口播逐字稿。
  当用户发送一个视频链接（YouTube、Bilibili、抖音、小红书、播客等）并要求总结、提取逐字稿或字幕时，使用此技能。
  触发关键词：总结视频、逐字稿、提取字幕、视频摘要、summarize video、transcript。
  也适用于用户只发送视频链接而没有其他明确指令的情况——默认执行总结+逐字稿提取。
  支持所有 BibiGPT 支持的平台。
version: "1.0.0"
user_invocable: true
---

# BibiGPT 视频总结 & 逐字稿提取

通过 BibiGPT API 获取视频的 AI 总结和完整口播逐字稿。

## 前置配置

### 获取 API Token

1. 前往 [BibiGPT](https://bibigpt.co) 注册账号
2. 在 [集成页面](https://bibigpt.co/user/integration) 获取 API Token
3. 在 [商店](https://bibigpt.co/shop) 购买时长额度

### 配置 Token

**方式一：环境变量（推荐）**

```bash
export BIBIGPT_TOKEN="your_token_here"
```

**方式二：修改脚本**

编辑 `scripts/bibigpt_fetch.py`，将 `API_TOKEN` 变量替换为你的 token。

---

## 工作流程

### 第一步：清理 URL

从用户消息中提取视频链接，去除追踪参数：
- Bilibili: 只保留 `https://www.bilibili.com/video/BVXXXXXX/`
- YouTube: 只保留 `https://www.youtube.com/watch?v=VIDEO_ID`

### 第二步：调用 API

使用本技能目录下的 `scripts/bibigpt_fetch.py` 脚本：

```bash
python3 /path/to/bibigpt_fetch.py "<视频URL>"
```

脚本会自动：
1. 先尝试 POST API（含详情）
2. 失败则降级到 GET API
3. 提取标题、总结、逐字稿
4. 输出 JSON 到 stdout

### 第三步：保存结果

将结果保存为 Markdown 文件：

```markdown
---
source: <视频URL>
platform: <平台>
author: <作者>
duration: <时长秒>
created: <YYYY-MM-DD>
tags: [bibigpt, transcript]
---

## 总结

<summary 内容>

## 口播逐字稿

<transcript 内容>
```

保存路径由用户指定，默认保存到当前工作目录。

### 第四步：报告

向用户展示：
- 视频标题和作者
- 总结摘要（前几百字）
- 逐字稿字数
- 文件保存路径

---

## API 参考

### 端点一览

| 端点 | 方法 | 用途 | 消耗时长 |
|------|------|------|----------|
| `/api/v1/summarizeWithConfig` | POST | 总结 + 详情（推荐） | 是 |
| `/api/v1/summarize` | GET | 基本总结 | 是 |
| `/api/v1/getSubtitle` | GET | 仅字幕（快） | 较少 |
| `/api/v1/express` | GET | AI 文案改写 | 是 |
| `/api/v1/getPolishedText` | GET | 字幕润色 | 是 |

### 响应结构（summarize / summarizeWithConfig）

```json
{
  "success": true,
  "id": "BV1FW6TBHErd",
  "service": "bilibili",
  "sourceUrl": "https://...",
  "htmlUrl": "https://bibigpt.co/...",
  "summary": "## 总结 Markdown 内容...",
  "costDuration": 600,
  "remainingTime": 3000,
  "detail": {
    "title": "视频标题",
    "author": "作者名",
    "duration": 1200,
    "cover": "封面URL",
    "type": "bilibili",
    "subtitlesArray": [
      {"startTime": 0.5, "text": "第一句话"},
      {"startTime": 3.2, "text": "第二句话"}
    ]
  }
}
```

注意：`summary` 和 `detail` 在顶级，不是嵌套在 `data` 里。
当 `includeDetail: true` 时才返回 `detail` 对象。

### 错误响应

```json
{
  "success": false,
  "code": "PAYMENT_REQUIRED",
  "message": "余额不足啦，请升级会员或购买时长哦！"
}
```

常见错误码：`PAYMENT_REQUIRED`（余额不足）、`INVALID_URL`、`TIMEOUT`。

### 仅获取字幕（不消耗 LLM 时长）

如果用户只要逐字稿不要总结，用 getSubtitle 端点更省额度。

### promptConfig 参数（可选）

POST 请求支持 promptConfig 自定义总结风格：

```json
{
  "url": "<视频URL>",
  "includeDetail": true,
  "promptConfig": {
    "showEmoji": true,
    "showTimestamp": false,
    "outlineLevel": 1,
    "sentenceNumber": 5,
    "detailLevel": 700,
    "outputLanguage": "zh-CN",
    "customPrompt": "自定义提示词",
    "isRefresh": true
  }
}
```

`isRefresh: true` 时忽略缓存，`customPrompt` 才会生效。
