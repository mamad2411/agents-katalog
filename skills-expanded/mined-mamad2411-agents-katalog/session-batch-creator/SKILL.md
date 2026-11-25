---
name: session-batch-creator
description: 批量创建 Codex 侧边栏会话（task/聊天/会话）。当用户要求「创建/新建 N 个会话」「创建五个」「网站开发 创建三个」「批量添加会话」「多开几个会话」「加几个侧边栏项目」等时使用。按标题批量生成新会话，并完整注册到本机 Codex 存储（sessions rollout 文件、session_index.jsonl、state_5.sqlite、.codex-global-state.json、config.toml），适配本机 Codex 桌面端。Use when the user wants to quickly create multiple new Codex threads/sessions in the sidebar with a given name and count.
metadata:
  short-description: 批量创建侧边栏会话
x-alice-class: assist
---# Session Batch Creator（批量创建侧边栏会话）

按标题批量创建 Codex 侧边栏会话，并像真实会话一样注册到本机存储的 5 个位置：
rollout 会话文件、`session_index.jsonl`、`state_5.sqlite`（threads 表）、`.codex-global-state.json`（桌面端 UI 状态）、`config.toml`（`[projects.'<id>'] trust_level = "trusted"` 登记）。

## 使用步骤

1. **解析用户输入**：提取「标题」和「数量」。
   - 示例：`网站开发 创建五个` → 标题 `网站开发`，数量 `5`
   - 示例：`创建三个 测试` → 标题 `测试`，数量 `3`
   - 示例：`10个 小红书` → 标题 `小红书`，数量 `10`
   - 中文数字（一~十、两、十五、二十等）和阿拉伯数字都支持。

2. **运行脚本**（用 `python` 执行）：
   ```powershell
   python "C:\Users\Administrator\.codex\skills\session-batch-creator\scripts\create_sessions.py" --from "网站开发 创建五个"
   ```
   或显式传参：
   ```powershell
   python "C:\Users\Administrator\.codex\skills\session-batch-creator\scripts\create_sessions.py" --title "网站开发" --count 5
   ```

3. **克隆已有会话（可选）**：把某个已有会话的完整对话复制成 N 份（带 `parent_thread_id` 派生关系）：
   ```powershell
   python "C:\Users\Administrator\.codex\skills\session-batch-creator\scripts\create_sessions.py" --title "你会什么" --count 5 --clone-from 01a04e4c-83e6-7273-a271-e6a83d9e6398
   ```

4. **删除会话（可选）**：清理之前批量创建的会话（会同时移除 5 个位置的登记）：
   ```powershell
   python "C:\Users\Administrator\.codex\skills\session-batch-creator\scripts\create_sessions.py" --delete <session_id> [<session_id> ...]
   ```

## 参数说明

- `--title <名称>`：会话标题，如 `网站开发`
- `--count <数量>`：创建个数
- `--from <自然语言>`：自动解析标题和数量（推荐）
- `--clone-from <会话id>`：克隆已有会话内容
- `--cwd <路径>`：会话工作目录（默认 `C:\Users\Administrator\Documents\openclaw`）
- `--no-config`：不写 config.toml（默认会写，和用户要求一致）
- `--dry-run`：只预览不写入
- `--delete <id>...`：删除会话

## 命名规则

新会话命名为 `{标题} 副本{序号}`（例如 `网站开发 副本1`），序号从 1 开始。

## 注意事项
- `.codex-global-state.json` 可能被运行中的桌面端覆盖重写；若侧边栏未显示新会话，重启桌面端即可（权威索引是 `state_5.sqlite` + `session_index.jsonl`，这两处才是侧边栏真正读取的来源）。

- 脚本会自动备份被修改的文件到 `~/.codex/backups/`。
- 创建完成后，若侧边栏未立即显示，提醒用户**重启 Codex 桌面端**。
- 新会话默认是「空会话」（只有 session_meta），打开后可正常对话；`--clone-from` 模式会复制完整对话历史。
- 写 `config.toml` 的 `[projects.'<session_id>']` 只是登记记录；实际项目信任看 `[projects.'<工作目录>']`。