---
name: web-session
description: "从 cookie、JWT、角色字段和用户标识验证 CTF Web 身份/会话处理假设，维护可重放的会话基线。"
metadata:
  category: "web"
  keywords: "[\"web\",\"session\",\"会话\",\"身份\",\"JWT\",\"cookie\",\"HMAC\",\"role\",\"IDOR\",\"认证\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/web.md\",\"section\":\"Auth/session:\",\"start_line\":23,\"end_line\":29,\"sha256\":\"14dbad768b78dbb6a7be3f059c00682a786781b35d1e106e52e0fa6093119f87\"}"
  resources: "[\"references/checklist.md\"]"
---

# Web 身份与会话差异检查

## 适用前提
已找到具体 Web 入口及正常请求，存在 cookie/JWT、角色、用户标识或登录/重置流程的线索。

## 工作流
1. 离线解读 cookie 或 JWT 的结构，用 `requests.Session()` 或 curl cookie jar 保存正常会话和响应基线。
2. 依据应用实际实现选择检查：JWT 算法/验签、弱 HMAC secret、key confusion 或受支持的 kid/JKU 处理；签名 cookie 的密钥来源。
3. 结合路由/源码和正常响应检查 role、user ID、批量字段赋值、重置 token、对象访问与 host-header 信任。
4. 每次仅改变一个相关字段，记录请求、响应和身份上下文；将有效路径整理为可重复的会话脚本。

## 验证与失败处理
字段能被修改或 token 能被解码都不等于服务信任它。必须用目标操作的服务端响应证明影响，并与基线比较。若限制实际来自加密构造则交由 Crypto；无相应处理路径时停止套用检查项。

## 按需参考
`references/checklist.md` 保存原 Auth/session 段落；请求基线和端点映射见 `web`。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/web.md` 的 23–29 行（Auth/session:）。完整原文件 SHA-256：`14dbad768b78dbb6a7be3f059c00682a786781b35d1e106e52e0fa6093119f87`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

