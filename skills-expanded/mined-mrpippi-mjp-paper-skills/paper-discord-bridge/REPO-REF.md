# Repo Ref
- source: https://github.com/mrpippi/mjp-paper-skills (path: .claude/skills/paper/paper-discord-bridge/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 只用 JDK 的 Discord 聊天橋接（不需 JDA／DiscordSRV）：遊戲 → Discord 以 webhook 佇列送出（429 照 Retry-After 重送一次、禁止 @提及、Markdown 跳脫），Discord → 遊戲以 Gateway WebSocket 狀態機（心跳、RESUME、致命關閉碼、退避）在單一執行緒接收後切回主執行緒；祕密不進 log / JDK-on
