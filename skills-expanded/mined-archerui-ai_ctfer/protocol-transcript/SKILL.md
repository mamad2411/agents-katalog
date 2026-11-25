---
name: protocol-transcript
description: "源码较多的异步密码协议服务：保存原始 transcript、检查 sender/nonce/channel 语义，并在一次连接中验证状态转换。"
metadata:
  category: "crypto"
  keywords: "[\"protocol\",\"协议\",\"transcript\",\"异步\",\"ACK\",\"MSGFROM\",\"Shamir\",\"Feldman\",\"committee\",\"nonce\",\"sender\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/crypto.md\",\"section\":\"Protocol crypto / source-heavy services:\",\"start_line\":128,\"end_line\":156,\"sha256\":\"5071cdb2ea828c613f46c3482fd48fe4087a0a7959b6d42a5b7458308833d777\"}"
  resources: "[\"references/checklist.md\"]"
---

# 有状态密码协议 transcript

## 适用前提
挑战使用有状态文本协议、消息通道、参与者角色或秘密共享，且源代码和服务交互共同决定语义。

## 工作流
1. 聚焦读取消息格式、状态机、sender 检查和最终成功条件，随后立即写 driver，不重复扫描全部源码。
2. 保存精确收发记录和 channel、user、nonce、identifier、参数、share、commitment、cookie、ACK；在 prompt 或 ACK 后继续读取异步消息。
3. 区分“命令已被接收”和“发送者具有权限”。一次检查暴露权限条件后，再根据源码检验身份、重连、状态转换或角色变化假设。
4. 包装器已创建连接时，直接驱动它的 stdin/stdout；只有源码证明可建立第二条外部连接才使用其他 client。
5. Shamir/Feldman/committee 场景先记录 identifier、q、g、commitments、participant list 和 own share，再聚焦 release/recommittee/recovery 的身份、key index、nonce 与 channel 检查。
6. 若最终输入是恢复出的 secret，将采集、状态转换、恢复/验证、退出命令和最后提交放在一个有界同步脚本中，保持连接生命周期连续。

## 验证与失败处理
以实际 transcript 和协议校验为证据，ACK 不等于已经授权或取得 secret。拒绝后不重复同一请求；保存拒绝条件，修正下一条假设。当前执行器不能跨工具调用恢复 TCP 会话。

## 按需参考
`references/checklist.md` 保留原协议段落；通用 remote/PoW 处理见 `general`。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/crypto.md` 的 128–156 行（Protocol crypto / source-heavy services:）。完整原文件 SHA-256：`5071cdb2ea828c613f46c3482fd48fe4087a0a7959b6d42a5b7458308833d777`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

