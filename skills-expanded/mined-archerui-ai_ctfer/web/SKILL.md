---
name: web
description: "HTTP/API Web CTF triage：路由、会话、输入、上传、模板和浏览器线索的最小检查。"
metadata:
  category: "web"
  keywords: "[\"web\",\"HTTP\",\"API\",\"网站\",\"SSRF\",\"SQL\",\"SSTI\",\"XSS\",\"cookie\",\"upload\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/web.md\",\"section\":\"# Web Skill\",\"start_line\":1,\"end_line\":76,\"sha256\":\"14dbad768b78dbb6a7be3f059c00682a786781b35d1e106e52e0fa6093119f87\"}"
  resources: "[\"references/checklist.md\"]"
---

# Web 题目入口与证据检查

## 适用前提
题目入口是 HTTP、API、前端代码、身份逻辑、模板、文件上传或描述明确的 admin bot。

## 工作流
1. 请求题面指明的入口，保存响应头、状态码和少量正文；用 cookie jar 或 `requests.Session()` 保留会话。
2. 从 HTML 表单、JS fetch、链接、源码和 API 文档整理已知端点，保存正常请求的基线，识别框架与处理参数的路径。
3. 身份、cookie 或 JWT 是关键线索时加载 `web-session`。其他分支按证据选择 SQL/NoSQL、文件路径/上传、模板/代码、SSRF 或客户端处理检查。
4. 使用参考中的针对性检查项，先复现一种输入与响应差异；将请求、会话状态、解析和最终读取写成可重放脚本。
5. 对题目指定的服务交互。遇到网站只提供二进制/pcap 时先下载并路由到对应类别。

## 验证与失败处理
比较同一会话中的正常与测试响应，保留响应内容及环境信息。页面中出现 flag 样式文本不等于已验证；需说明它来自哪个端点及触发条件。失败后回到源代码/请求差异，不无目的扩大扫描范围。

## 按需参考
`references/checklist.md` 保留原文 Web 分支，身份会话细节拆至 `web-session`。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/web.md` 的 1–76 行（# Web Skill）。完整原文件 SHA-256：`14dbad768b78dbb6a7be3f059c00682a786781b35d1e106e52e0fa6093119f87`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

