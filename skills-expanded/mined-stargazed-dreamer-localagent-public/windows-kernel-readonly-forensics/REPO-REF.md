# Repo Ref
- source: https://github.com/stargazed-dreamer/localagent-public (path: .agents/skills/dev/windows-kernel-readonly-forensics/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 在 Windows 上做**只读**内核级取证：用 LiveKd 起内核调试会话读活内存（对象引用计数、EPROCESS 字段、通知回调表、对象回调链），用 GFlags **runtime** Object Reference Tracing（`!obtrace`，**不必重启**）打出每一次引用/解引用的调用栈，并把内核地址确定性地点名到模块。用于排查「进程退出后内核对象不回收 / 内存只涨不
