---
name: path-aware
description: "需要判斷 CLI 是否存在，或準備回報工具缺失時，先驗證 PATH。"
when_to_use: "只在工具存在性或 PATH 是目前決策的一部分時觸發。"
tags: [path, shell, tooling, environment]
effort: low
shell: optional
runtime-scope: shared-core
alwaysApply: false
---

# 環境感知 -- 工具存在性驗證

Sandbox 的 shell 繼承了使用者完整的 PATH（透過 zsh profile）。
大多數工具**已經安裝**，只是你不確定而已。

## 硬規則

1. **禁止未驗證就說「工具未安裝」或「找不到指令」**
   - 在聲稱任何 CLI 工具不存在之前，必須先用 Bash 跑 `command -v <tool>` 驗證
   - 如果 `command -v` 找不到，再試 `which <tool>` 和常見安裝路徑

2. **遇到 "command not found" 錯誤時，嘗試定位而非放棄**
   - 檢查 homebrew: `/opt/homebrew/bin/<tool>`
   - 檢查 cargo: `~/.cargo/bin/<tool>`
   - 檢查 go: `~/go/bin/<tool>`
   - 檢查 npm/pnpm global: 用 `pnpm bin -g` 或 `npm bin -g` 查詢
   - 檢查 pip/pipx: `~/.local/bin/<tool>`
   - 檢查 bun: `~/.bun/bin/<tool>`

3. **善用 `brew list` 和 `brew --prefix` 定位 homebrew 安裝的工具**
   - `brew --prefix <formula>` 可以找到安裝路徑
   - `brew list <formula>` 可以列出所有檔案

4. **版本管理器的工具需要特別處理**
   - Node: 透過 nvm，檢查 `~/.nvm/versions/node/*/bin/`
   - Python: 透過 pyenv，檢查 `~/.pyenv/shims/` 和 `~/.pyenv/versions/*/bin/`
   - Go: 檢查 `GOROOT/bin` 和 `GOPATH/bin`

## 流程

```text
需要使用工具 X
  -> command -v X
  -> 找到? 直接用
  -> 找不到? 搜尋常見路徑
  -> 搜尋到? 用完整路徑執行
  -> 都找不到? 才告知使用者，並建議安裝方式
```

## 反模式（Anti-patterns）

- 不要在沒跑 `command -v` 的情況下說「請先安裝 X」
- 不要因為上一個 session 找不到就假設這次也找不到
- 不要建議使用者手動設定 PATH -- sandbox 已經繼承完整環境
