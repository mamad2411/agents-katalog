# Repo Ref
- source: https://github.com/stargazed-dreamer/localagent-public (path: .agents/skills/daily/windows-recycle-and-space-reclaim/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 在本机 Windows 上安全删除文件/目录并真正回收磁盘空间 —— 走项目既有的 ctypes 回收站工具（因 Add-Type 被安全策略拦死），并解决「进了回收站却不释放空间」这个核心陷阱。含回收站条目审计与按身份核对后永久清理两个脚本；**也含反向能力：从回收站把已删内容（整目录）捞回来**。当用户说"把这个目录删掉 / 清理 temp / 太占存储了 / 帮我回收空间 / 磁盘满了 / 
