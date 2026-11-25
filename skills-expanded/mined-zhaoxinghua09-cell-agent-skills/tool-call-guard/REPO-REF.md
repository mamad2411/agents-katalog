# Repo Ref
- source: https://github.com/zhaoxinghua09-cell/agent-skills (path: skills/tool-call-guard/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当用户说『agent乱调工具』『误删了文件』『不该发邮件却发了』『怎么给AI的工具加权限边界』，或在给 agent 接工具（文件/网络/数据库/消息/支付）想防危险动作时使用。把每次 tool call 当『需授权操作』：按 读/写/删/外发/支付 分级，危险动作先拦截+提示确认，低风险放行。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：工具调用安全、agent权限、tool call g
