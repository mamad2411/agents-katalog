---
name: myplugins
description: 在當前目錄按序號啟用或關閉全局未啟用的可選插件（如 frontend-design、chrome-devtools-mcp、skill-creator），預設寫入共享設定 .claude/settings.json，也可寫本地個人設定，並增刪可選插件清單。
when_to_use: 使用者輸入 /myplugins，或說「列出可選插件」「啟用插件 3」「這個專案開 frontend-design」「關掉插件」「把 xxx 加入／移出插件清單」時。安裝場景配置包用 myconfig；修改權限、環境變數等其他設定用 update-config。
argument-hint: "[序號… | all | off 序號… | add 名稱@市場 說明 | remove 序號 | sync] [--local|-c] [--dry-run|-t|--test]"
allowed-tools: Bash(python3 ~/.claude/skills/myplugins/scripts/myplugins *)
---

# 可選插件管理

所有動作交給腳本，不自己編輯 settings 檔。命令照字面單獨執行：寫 `~/.claude/...`，不展開成絕對路徑、不加引號、不串接、不重導向（沙箱排除與權限規則按命令文字比對，2026-11-04 實測）：

```sh
python3 ~/.claude/skills/myplugins/scripts/myplugins <子命令> [參數]
```

| 使用者輸入 | 執行 |
|---|---|
| 沒有內容，或要求列出 | `list` |
| 序號、插件名稱或 `all`（如 `3`、`1 4 6`） | `enable <選擇>` |
| `off <選擇>` | `off <選擇>` |
| `add`、`remove`、`sync`，或帶 `--dry-run`／`-t`／`--test` | 先讀 `references/details.md` 再執行 |

- 預設寫共享層 `.claude/settings.json`，直接執行。使用者帶 `--local`／`-c`，或說「只給自己」「本地」「不進版控」時加 `--local`。
- 自然語言描述（如「這個專案開前端插件」）：先 `list` 找序號，說明要執行的命令再執行；對應不明確先問。
- 腳本有寫入時，提醒使用者輸入 `/reload-plugins`（或重開 Claude）才生效，你無法代為執行。
- 腳本輸出「注意：」的行要轉告（如未安裝時的安裝命令），不自行安裝或 `sync`。
- 腳本報錯（如「無法寫入…sandbox.excludedCommands」），或使用者問 `/plugin` 為何把插件列在 User 分組時，讀 `references/details.md`。

## 列出後的回覆

工具輸出已是完整清單，不要再轉成表格或重抄清單。回覆只含：

1. 照抄腳本的「已啟用：」一行；有「注意：」的行一併照抄。
2. 下面的用法：

```
/myplugins 3            啟用第 3 個（寫入 .claude/settings.json，會進版控）
/myplugins 1 4 6        批量啟用；all 全部啟用
/myplugins 3 --local    只寫本地個人設定 .claude/settings.local.json（同 -c）
/myplugins 3 --test     預演，確認後才寫入（同 -t、--dry-run）
/myplugins off 3        關閉，回到下一層的值
/myplugins add 名稱@市場 說明 | remove 3 | sync    維護清單
```
