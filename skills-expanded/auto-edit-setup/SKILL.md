---
name: auto-edit-setup
description: 檢測並安裝這個工作區要用的工具（git、Node.js 22、ffmpeg／ffprobe、whisper-cli、auto-editor、根目錄 npm install 的 HyperFrames、hyperframes 與 auto-editor 兩組外部 Skill、9 支 auto-edit Skill），最後探測生圖能力。當使用者說「幫我檢測環境」「檢測環境」「安裝環境」「裝工具」「Skills 看不到 auto-edit」時使用。已經在剪片、只是某個剪片指令出錯時不要用（看那個階段 Skill 的退路表）。
version: 0.1.0
---
# 環境準備

規則在 AGENTS.md；本檔只寫這一階段的指令、判準、停點、退路。
衝突時：使用者當下的話 > AGENTS.md > shared/style.md > USAGE.md > USAGE-reference.md > 本 Skill；派工時派工訊息 > 本 Skill。

| 輸入 | 指令 | 產出 | 完成判準 | 停點 |
|---|---|---|---|---|
| — | `bash setup/check.sh`（Mac）、`setup\check.ps1`（Windows） | 每一步的進度行、總表、能力表 | 檢測 JSON 的 `all_ok` 是 `true` | 沒有（安裝清單問一次同意） |

手冊是 `setup/README.md`（步驟代號 M＝`setup/mac.md`、W＝`setup/windows.md`、S＝共用步驟）；本檔不抄手冊，只指路、補完成判準。進度回報格式照 `setup/README.md`「進度回報格式」原文。

## 開始前

| 條件（看得到的事實） | 做法 |
|---|---|
| 這一輪還沒讀過 `setup/README.md` | 先讀全文 |
| 使用者只說「Skills 看不到 auto-edit」 | 只做 S4（`node setup/install-skills.mjs`），再跑一次檢測 |
| 檢測顯示 `restart` | 照 `setup/README.md` 步驟 2：先加 PATH 前綴把 S1–S4 做完（前綴照手冊步驟 3 那一行），再請使用者重開 MiniMax Code（Mac `M8`、Windows `W9`），這一輪到這裡結束。重開後還是 `restart`，就整輪加前綴做，總表最後註明「之後的指令要加 PATH 前綴」 |
| 檢測 JSON 的 `all_ok` 是 `true` | 不用列清單、不用問同意，直接從步驟 3 的 S5 做 |

## 步驟

**0. 檢測**

```
Mac：bash setup/check.sh
Windows（PowerShell）：[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; powershell -NoProfile -ExecutionPolicy Bypass -File setup\check.ps1
```

完成判準：最後一行 `JSON:` 解析成功，讀到 `todo` 與每一項的 `status`、`step`。
常見錯誤：Windows 的 shell 是 Git Bash → 改用 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File setup/check.ps1`。

**1. 列清單、問一次同意**（AGENTS.md 規則 3：整份清單問一次）

```
（不用指令：照 setup/README.md 步驟 1 的範例，每步寫用途和指令）
```

完成判準：回覆最後一行是 `❓ 請回：「可以開始」或要拿掉的步驟編號`。
常見錯誤：一項一項問 → 整份清單只問一次。

**2. 系統工具**

```
（照 setup/mac.md 或 setup/windows.md，只做 todo 對到的 M／W 步驟，順序照文件）
```

完成判準：再跑一次步驟 0，`todo` 裡那幾項不見了。
常見錯誤：要輸入電腦密碼的步驟（Mac 的 Homebrew）→ 請使用者自己在終端機做，等他說「好了」再驗證。Windows 的 winget 由你執行，執行前先提醒使用者跳出視窗要按「是」。都不要改用系統管理員權限執行。

**3. 共用步驟 S1–S9**（`setup/README.md` 步驟 3）

```
npx -y skills add heygen-com/hyperframes -a minimax-code -g -y
npx -y skills add https://github.com/wyattblue/auto-editor --skill auto-editor -a minimax-code -g -y
npm install
node setup/install-skills.mjs
node shared/template/tools/look.mjs ensure
npx -y hyperframes doctor
auto-editor --version
```

依序是 S1、S2、S3（在工作區根目錄）、S4、S5、S6、S7；S8 列素材、S9 最後檢測照手冊原文。每一步先看檢測 JSON，那一項是 `ok` 就跳過（手冊每一步括號裡的條件）。手冊裡的 `npx` 一律加 `-y`，才不會停在 `Ok to proceed?`。
完成判準：S3 之後 `node_modules/hyperframes/package.json` 的 version 和根目錄 `package.json` 釘的一樣；S4 最後一行 `✔ 完成：9 支 × 2 個位置…`；S5 最後一行 `✔ 4 個檔都對`（✖ 不擋其他步驟，照手冊 S5 處理）；S9 的 `all_ok` 是 `true`。
常見錯誤：`npm install` 在 `setup/` 裡跑 → 一定在工作區根目錄（有 `package.json` 的那層）；S4 印 `✖ 衝突` → 退路表第 3 列。

**4. 能力探測**（只讀，不裝、不登入）

```
node shared/template/tools/caps.mjs
```

完成判準：能力表貼在總表下面。
常見錯誤：結束碼 1（Chrome、ffmpeg／ffprobe、HyperFrames 有一項不可用）→ 回 S3／S6 補；codex、mmx 不可用不影響。

**5. 講者資料**（只讀）

```
node shared/template/tools/brand.mjs speaker
```

印 `⚠ 還沒設定講者` → 總表下面加一行請使用者給姓名與頭銜（或說「不要講者介紹」），收到後照 `auto-edit-style` 步驟 8 設定；不擋「環境準備完成」。
完成判準：總表下面有「講者：<姓名>」或「講者：還沒設定」一行。
常見錯誤：印 `✖ shared/講者.json：…` → 檔案被手改壞了，照它印的 → 重新設定（不要刪 `講者.json` 以外的檔）。

## 自我核對

- [ ] 安裝清單只問一次
- [ ] 沒有用系統管理員權限執行、沒幫使用者輸入密碼（`setup/README.md` 原則 5）
- [ ] 只裝「要裝的東西」表裡的
- [ ] 每一步都照「驗證」確認過
- [ ] `npm install` 在工作區根目錄跑
- [ ] `install-skills.mjs` 結束碼 0
- [ ] 最後 `all_ok` 是 `true`，或總表標題是【環境準備未完成】

## 退路表

| 症狀（工具原文） | 做法 | 第二次還失敗 |
|---|---|---|
| `npm ERR! code EACCES` | 不要改用系統管理員權限；確認在工作區根目錄、不是系統資料夾 | 停下來回報：指令、錯誤原文、已經試過什麼（`setup/README.md` 原則 8） |
| `npm ERR! network`、`ETIMEDOUT` | 等 1 分鐘重跑一次 | 停下來回報 |
| `✖ 衝突 … 這個資料夾不是 install-skills 裝的` | 把那個路徑貼給使用者，問要不要改名或移走；不要自己刪 | — |
| 檢測項目 `restart` | 照本檔「開始前」的 `restart` 那一列 | — |
| 其他症狀 | 查 `setup/troubleshooting.md` | 停下來回報 |

## 工具呼叫預算

同一步失敗 2 次就停（`setup/README.md` 原則 8）。

## 回報格式

每做完一步一行，照 `setup/README.md`「進度回報格式」（例：`【環境準備 3/11】Node.js ✅ v24.16.0（需要 22 以上）`）。最後是總表（必要項目一項一列），下面接能力表：

```
【環境準備完成】
| 項目 | 狀態 | 版本或位置 |
|---|---|---|
| Node.js | ✅ | v24.16.0 |
| 9 支 auto-edit Skill | ✅ | .claude/skills/、~/.minimax/skills/ |
（其他項目）
能力表：<caps.mjs 的表>
講者：<brand.mjs speaker 印的姓名｜還沒設定，請給我姓名與頭銜（或說「不要講者介紹」）>
可以貼第二個提示詞了。
```
