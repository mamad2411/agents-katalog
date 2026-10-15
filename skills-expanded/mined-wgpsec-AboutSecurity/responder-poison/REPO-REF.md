# Repo Ref
- source: https://github.com/wgpsec/AboutSecurity (path: skills/tool/responder-poison/SKILL.md, branch: master)
- mined: 2026-10-14
- desc: 使用 Responder 进行 LLMNR/NBT-NS/MDNS 投毒和 NTLMv2 哈希捕获。当处于 Windows 域网络中、需要被动捕获凭据或进行中间人攻击时使用。Responder 监听网络中的名称解析广播请求（LLMNR/NBT-NS/MDNS），伪造响应诱使目标发送 NTLMv2 认证哈希。抓到的哈希可用 hashcat 离线破解或通过 ntlmrelayx 中继到其他服务。涉及 
