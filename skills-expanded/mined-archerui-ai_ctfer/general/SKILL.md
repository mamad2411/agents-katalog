---
name: general
description: "CTF 通用工作流：附件检查、证据记录、最小验证与有界同步执行。"
metadata:
  category: "general"
  keywords: "[\"CTF\",\"triage\",\"附件\",\"证据\",\"验证\",\"remote\",\"工作流\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/general.md\",\"section\":\"# General CTF Skill\",\"start_line\":1,\"end_line\":94,\"sha256\":\"22cc3e43853b1b4ea10e3e8dfa2f13ae8bf49ea7871133bcc9a50150944ee6f7\"}"
  resources: "[\"references/checklist.md\"]"
---

# 通用 CTF 工作流

## 适用前提
开始新题、重新规划，或尚未得到稳定解题路线时使用。先以题目元数据和附件为依据；旧案例中的目标、凭据、flag 和运行结果都不是当前题目的事实。

## 工作流
1. 用 `list_files`、`read_file` 和 `search_files` 列附件、读题面与 README；需要识别格式时再调用 `run_command` 中的 `file`、`xxd`、`strings`。压缩包先列目录再解压。
2. 每次明确一个假设和所需证据，运行一个可解释的检查；输出过长时查看已保存 artifact 的相关范围，不反复打印整份源码。
3. 将可复用逻辑写到 `/work/solve.py` 或 `/work/helper.py`，打印有标签的中间结果，提取文件放到命名目录，保留原始附件。
4. 从 remote 文本推断 HTTP/TCP、host 和 port，做一次最小探测。HTTP 保留 cookie；交互协议用确定性脚本记录原始收发内容，prompt/ACK 后继续接收异步消息。
5. 用 `LOCAL_TEST_VALUE` 作为本地占位，避免污染候选检测。对候选执行小型验证再提交，保留网页上的被动发现及其上下文。
6. 两次无新证据的失败后回看题面、已排除假设及类别线索，转到 `unknown` 或相应专项 Skill。

## 执行器约束
当前每条命令运行于独立的临时 Docker 容器。不要跨工具调用使用后台 PID、常驻进程或 TCP 会话；需要同一连接的交互必须放进一次有超时的同步脚本。旧来源第 20–22 行的后台任务建议已在此修正，尚未实现后台任务工具。

## 验证与失败处理
保存输入、精确命令、stdout/stderr artifact 和验证依据。脚本退出成功仅表示脚本执行完成；不能单凭成功状态或模型判断认定 flag 已验证。依赖缺失时检查现有工具并给出明确限制；远程状态变化后重新获取环境相关证据。

## 按需参考
`references/checklist.md` 保留旧文其他检查项，包括编码、文件纪律、PoW 和远程服务处理。仅在当前任务需要细节时加载。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/general.md` 的 1–94 行（# General CTF Skill）。完整原文件 SHA-256：`22cc3e43853b1b4ea10e3e8dfa2f13ae8bf49ea7871133bcc9a50150944ee6f7`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

