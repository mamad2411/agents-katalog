---
name: reduced-aes-integral
description: "针对源码确认的四轮 AES、末轮无 MixColumns、同会话选择明文的 delta-set 积分恢复与重加密验证。"
metadata:
  category: "crypto"
  keywords: "[\"AES\",\"four round\",\"4-round\",\"四轮\",\"Square\",\"integral\",\"积分\",\"delta set\",\"S_inv\",\"MixColumns\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/crypto.md\",\"section\":\"Reduced-round AES / Square-style integral puzzles:\",\"start_line\":80,\"end_line\":104,\"sha256\":\"5071cdb2ea828c613f46c3482fd48fe4087a0a7959b6d42a5b7458308833d777\"}"
  resources: "[\"references/checklist.md\"]"
---

# 四轮 AES 积分检查

## 适用前提
源码确认是适合此性质的四轮 AES 结构，末轮没有 MixColumns，并允许同一会话密钥下的选择明文查询。不能仅凭“少于五轮”就假设下面的具体字节测试成立。

## 工作流
1. 在单个 `solve.py` 中组织本地随机密钥自检、一次会话内的查询和最终验证；复制题目中的字节/矩阵转换、逆 S-box 与密钥扩展规则。
2. 构造 256 个分组的 delta set：改变一个字节的全部取值，其他字节固定；保存该会话的加密 flag 和查询密文。
3. 对每个密文字节与末轮密钥字节候选 g，检查该集合的 `xor(S_inv[c_byte ^ g]) == 0`。
4. 使用不同固定模式的更多 delta sets 取候选交集，直到每个字节唯一。不要反复查询相同集合来处理歧义。
5. 恢复末轮密钥、按题目实现逆推密钥扩展，解密并处理 padding。

## 验证与失败处理
先让本地随机密钥自检通过，再进行远程查询；最终重加密 padded plaintext 与原密文比较。结果异常优先核对轮结构、字节布局、逆表和会话是否换 key。此库记录方法模板，未包含真实题目密钥或已验证结果。

## 按需参考
`references/checklist.md` 保留现有四轮 AES 段落。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/crypto.md` 的 80–104 行（Reduced-round AES / Square-style integral puzzles:）。完整原文件 SHA-256：`5071cdb2ea828c613f46c3482fd48fe4087a0a7959b6d42a5b7458308833d777`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

