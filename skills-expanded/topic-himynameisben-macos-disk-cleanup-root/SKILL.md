---
name: macos-disk-cleanup
description: 診斷並清理 macOS 磁碟空間，特別是「系統資料 / System Data」這類看不出內容的用量。涵蓋開發者工具殘骸（Xcode iOS DeviceSupport、Simulator runtime、DerivedData）、套件管理器快取（Homebrew、pnpm、pip、npm、cargo、go、uv）、容器與 VM 磁碟（Docker、podman、lima）、瀏覽器 profile、以及已移除 app 的孤兒 container。使用時機：(1) 使用者說磁碟快滿了、System Data 佔太多、想清空間 (2) 詢問某個資料夾或快取能不能刪 (3) 移除 app 後想清乾淨殘留檔案、完整解除安裝 (4) 想知道 Docker.raw、Group Containers、Library/Caches 這些是什麼、佔了多少。Also triggers in English — disk full, startup disk almost full, free up disk space, clean up Mac storage, what is System Data on my Mac, what is taking up space, safe to delete this cache, uninstall app leftovers, reclaim disk space, Docker.raw huge, Xcode taking too much space
---

# macOS 磁碟清理

## 核心原則

**刪除不可逆。** 每一次刪除前都要能回答：這是自動重建的快取，還是使用者唯一的副本？答不出來就先看內容，再問使用者。

分三級處理：

| 等級 | 判準 | 動作 |
|---|---|---|
| **SAFE** | 自動重建、不含使用者資料 | 合併成一個選項提案，確認後刪 |
| **CONFIRM** | 可重新下載但代價高（GB 級），或改變 app 行為 | 列出大小與後果，問過再刪 |
| **DANGER** | 含使用者資料（文件、聊天記錄、憑證、書籤） | **先列出實際內容**，逐項確認 |

分類對照表在 `references/locations.md`。

## 流程

### 1. 掃描

```bash
scripts/disk_scan.sh          # 標準掃描，約 40 秒
scripts/disk_scan.sh --deep   # 追加各語言套件管理器快取
```

唯讀，不刪任何東西。輸出含：磁碟總量、`~/Library` 各層排名、Xcode/Simulator 用量、**稀疏 VM 磁碟的實佔 vs 宣告值**、以及**孤兒 container**（app 已不在但 container 還佔著空間）。

### 2. 分類與呈現

對照 `references/locations.md` 把發現分成上述三級，用表格呈現「項目 / 大小 / 是什麼 / 刪掉的後果」。

要點出使用者自己看不出來的東西，例如：`Docker.raw` 是整台 Linux VM 的虛擬硬碟、`iOS DeviceSupport` 每個 iOS 小版本各存一份 5 G。

### 3. 確認

把所有待刪項目整理成一則提問，一次問完，並把預估回收量寫進每個選項。不要每刪一項問一次。有結構化提問工具（例如 AskUserQuestion）就用，沒有就用一則清楚的條列訊息。

SAFE 等級可以合併成單一選項（「套件快取共 N G」），但**仍然要出現在選項裡**。重抓數十 GB 對計量網路、即將離線、或正在趕工的人是實質代價，這個取捨屬於使用者，不該由 skill 代為決定。

### 4. 執行

**進 DANGER 等級的 container 之前，一定先跑：**

```bash
ls -la ~/Library/Containers/<bundleid>/Data/
```

`Downloads`、`Desktop`、`Movies`、`Music`、`Pictures` 是**指向真實家目錄的 symlink**。`du -sh Data/*/*` 會穿過它們，把使用者的 `~/Downloads` 列成 app 資料——照著刪就是災難。細節見 `references/gotchas.md` 第 1 節。

執行時：

- 每個階段刪完立刻跑 `df -h /System/Volumes/Data`，用前後差值歸因
- 刪除腳本**不要用 `set -e`**（`rm -rf` 遇到權限錯誤會回傳非 0 而中止後續指令）
- 靠重新量測驗證，不要靠 exit code

### 5. 驗證與回報

回報實際的前後數字和每項的貢獻。踩到已知的預期性失敗（container 空殼、simctl 非同步）時，說明那是正常的，不要當成錯誤回報。

## 開工前必讀

`references/gotchas.md` —— 十個會造成**誤判或資料損失**的陷阱。至少掌握這四個：

1. **Container symlink**：`du -sh Data/*/*` 會穿過 symlink，把家目錄算成 app 資料
2. **稀疏檔**：`ls -lh` 顯示宣告上限（Docker.raw 看起來 60G，實際 5.4G），**一律用 `du`**
3. **`Operation not permitted`**：被 `.com.apple.containermanagerd.metadata.plist` 擋住的 container 空殼刪不掉，這是**預期行為**，sudo 也無效，別當失敗回報
4. **`simctl runtime delete` 靜默且非同步**：跑完沒輸出、`list` 還看得到是正常的。用 sudo 重跑會回報「找不到」，那是假失敗

## 需要 sudo 時

Agent 執行指令的 shell 沒有 tty，`sudo` 必定失敗（`a terminal is required to read the password`）。先用 `sudo -n true` 測試免密碼；不行就把指令交給使用者，請他們自己在終端機執行：

```
sudo rm -f /Library/LaunchDaemons/com.example.plist
```

**把所有需要 sudo 的操作合併成一到兩行**再交出去，不要讓使用者分五次貼指令。

某些環境可以讓使用者把指令送回對話（例如 Claude Code 在輸入框用 `!` 前綴執行，輸出會直接回到上下文）。有這種機制就善用，沒有就請使用者把輸出貼回來。

## 用 Finder 開啟資料夾

`open` 在沙箱下會失敗（`kLSApplicationNotFoundErr`），改用：

```bash
osascript -e 'tell application "Finder" to open POSIX file "/absolute/path"'
```

## 完整移除 app 的殘留

除了 `/Applications/<App>.app` 之外，掃這些位置：

```
~/Library/Containers/<bundleid>
~/Library/Group Containers/<TEAMID>.<bundleid>
~/Library/Application Support/<App>
~/Library/Caches/<bundleid>
~/Library/Preferences/<bundleid>.plist
~/Library/Application Scripts/<bundleid>
~/Library/Saved Application State/<bundleid>.savedState
~/Library/HTTPStorages/<bundleid>
~/Library/LaunchAgents/<bundleid>.plist
/Library/LaunchDaemons/<bundleid>.plist          # sudo
/Library/PrivilegedHelperTools/<helper>          # sudo
```

Docker 這類有 watchdog 的，**先刪 app bundle 再 kill 程序**，否則會被重生。各 app 的細節在 `references/locations.md` 的「App 專屬知識」。
