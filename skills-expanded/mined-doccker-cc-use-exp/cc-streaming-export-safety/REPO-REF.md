# Repo Ref
- source: https://github.com/doccker/cc-use-exp (path: .codex/skills/cc-streaming-export-safety/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: 当实现用户驱动的大文件导出或批量序列化（Excel/CSV/JSON/JSONL/PDF，数据量未知或超过 1 万行/10 MB）时触发；普通小文件下载、静态资源下载、非导出 Writer/Report 类不触发。防止 OOM、临时文件残留、同步导出阻塞 HTTP 线程和表格公式注入。
