---
name: dsh-internals
description: DSH (DeepSeek Harness) 內部機制地圖 — cordis 組合架構、套件佈局、AGENTS.md 指令系統、session log 格式、MCP/skills/memory 機制。當要研究 DSH 點運作、改 DSH 設定、或者想知某個機制喺邊度實作時使用。
whenToUse: 用戶問 DSH 內部原理、要 patch cordis.yml、要搵 DSH source code、或者研究 DSH 記憶/RAG/MCP/skills 機制。
---

# DSH Internals（DeepSeek Harness 內部機制地圖）

## 快速定位
- **Source code**：`~/.dsh/profiles/node_modules/@deepseek-ai/*`（全部套件都有 README.md 講機制）
- **用戶設定**：`~/.dsh/settings.yaml`（模型/provider，熱更新）
- **Profile patch**：`~/.dsh/profiles/web/cordis.patch.yml`（改 config 喺度改；**patch 會成個替換 row config，唔係 merge**）
- **憑證**：`~/.dsh/.credentials.yaml`（`OPENCODE_GO_API_KEY`）
- **Skills**：`~/.dsh/skills/<name>/SKILL.md`（watcher 自動發現）
- **Sessions**：`~/.dsh/sessions/<workspace-hash>/<session-id>/session.jsonl.zstd`

## 關鍵機制
1. **AGENTS.md 指令鏈**：`~/.dsh/AGENTS.md` 全域 + 專案 AGENTS.md/CLAUDE.md + AGENTS.local.md overlay。maxBytes 65536。冇 watcher，touch-driven。
2. **Skills**：frontmatter name(kebab-case) + description(必填)。模型按 description 觸發。
3. **MCP**：`@deepseek-ai/dsh-mcp-client`，stdio/streamable-http，工具名 `mcp__<server>__<tool>`，改 cordis.patch.yml 加 entry，HMR 自動重連。
4. **Session FTS**：`dsh-session-query-sqlite`，base 係 `openAt: never`（關）。要開就 patch。
5. **Web search**：`dsh-web-search-deepseek` 用 DEEPSEEK_API_KEY — **用戶冇呢個 key，唔好用**；用 web-research-fallback skill。
6. **Session log 格式**：JSONL + 串聯 zstd frames；Node `node:zlib` 有 zstdDecompressSync。Record types：user/message、assistant/message、tool/call、session/title...（詳見 knowledge/research/session-log-format.md）

## 常用操作
- 研究機制：讀對應套件 README（例如 `dsh-agent-instructions/README.md`）
- 改設定：edit `cordis.patch.yml`，跟 YAML array 格式，id 對應 row
- 睇 session：寫 node script 用 zstdDecompressSync 解壓
