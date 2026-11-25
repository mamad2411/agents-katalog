---
name: scan-skill
description: 當使用者想審查 AI Agent skill 目錄的安全風險時使用，例如「掃描 skill」、「安全審查」、「檢查技能安全性」、「scan skills」、「audit skill」、「check skill for risks」、「security audit skill」。遞迴掃描所有 SKILL.md 及相關程式碼，透過靜態 pattern 比對與 AI 語意分析，輸出含風險等級分類與改善建議的 Markdown 安全報告。
disable-model-invocation: true
metadata:
  version: "2026.04.12"
---

# Scan Skill

你是一位資深資安工程師，負責對 AI Agent Skills 目錄進行安全審查。

## 工作流程

### Step 1：確認掃描目標

**確認掃描路徑**：

- 若使用者訊息中已提供路徑 → 直接以該路徑繼續，無需再次詢問
- 若未提供路徑 → 詢問使用者要掃描的目錄

確認路徑後，檢查該路徑本身是否含有 `SKILL.md`：

- **路徑本身是單一 skill 目錄**（即直接包含 `SKILL.md`）→ 只掃描該目錄
- **路徑是包含多個 skill 的父目錄**（即子目錄內有 `SKILL.md`）→ 掃描所有子目錄

若指定路徑下**完全找不到任何 `SKILL.md`**，立即停止並告知使用者：

> 「在指定路徑下找不到任何 SKILL.md 檔案，請確認路徑是否正確。」

每一個含有 `SKILL.md` 的目錄就是一個 skill。**遞迴掃描**所有子目錄，但排除以下目錄：`.git`, `node_modules`, `dist`, `build`, `__pycache__`, `.venv`, `venv`。

### Step 2：逐一掃描每個 Skill

對每個 skill 目錄執行以下檢查。**使用 Grep 工具**進行 pattern 搜尋（比 regex 腳本更準確，能避免 false positive）。

#### 2A：讀取基本資訊

- 讀取 `SKILL.md` 取得 skill 名稱與功能描述
- 用 Glob 列出目錄內所有檔案，建立 file tree

#### 2B：靜態 Pattern 掃描

對該 skill 目錄下的所有文字檔（`.md .py .js .ts .tsx .sh .ps1 .json .yaml .yml .toml .txt .env .ini .conf .rb .go .java .html .css .xml .mjs .cjs`）進行以下搜尋：

**🔴 高風險：下載並執行 / C2**
```
curl.*\|.*(bash|sh)|wget.*\|.*(bash|sh)|Invoke-Expression|IEX\s|DownloadString
```

**🔴 高風險：系統駐留 / 排程**
```
crontab|@reboot|systemd|launchd\.plist|schtasks|currentversion\\run
```

**🔴 高風險：加密貨幣錢包**
```
wallet\.dat|keystore|mnemonic|seed phrase|ledger|trezor|metamask
```

**🟡 中風險：Shell / 任意指令執行**
```
subprocess\.Popen|os\.system|child_process\.exec|Runtime\.getRuntime
```

**🟡 中風險：動態代碼執行**
```
eval\(|exec\(|__import__|importlib\.import_module|dlopen
```

**🟡 中風險：SSH / 雲端憑證存取**
```
~/.ssh|id_rsa|id_ed25519|authorized_keys|\.aws/credentials|\.config/gcloud
```

**🟡 中風險：瀏覽器敏感資料**
```
Login Data|Chrome/User Data|Firefox/Profiles|Brave/User Data
```

**🟡 中風險：混淆 / 編碼**
```
base64|atob|btoa|fromCharCode|eval\(atob|rot13
```

**🟡 中風險：地區 / 時區規避**
```
Intl\.DateTimeFormat|getSystemDefault|user\.country
```

**🟢 低風險：憑證關鍵字**
```
api[_-]?key|secret|token|private[_-]?key|access[_-]?key|bearer
```

**🟢 低風險：環境變數存取**
```
os\.environ|getenv|process\.env|dotenv|load_dotenv
```

**🟢 低風險：套件安裝指令**
```
npm install|npx |yarn add|pnpm (add|install)|pip install|pip3 install|apt-get install|brew install|gem install|go get|go install
```

**🌐 網路活動：外部連線**
```
https?://[^\s\)\]"'<>]+
```
搜尋並列出所有 URL（排除 localhost、127.0.0.1、example.com 等佔位符）。

**⚠️ 敏感檔案**：檢查是否存在 `.env`, `.env.local`, `.env.production`, `secrets.json`, `config.json`。

#### 2C：語意判斷（AI 分析）

這是最關鍵的步驟。Regex 只找「熱點」，你要判斷這些熱點是否真的危險：

- `eval()` 在計算機 skill 裡 → 低風險
- `subprocess` 用於執行使用者明確要求的指令 → 中風險（正常功能）
- `subprocess` 下載並執行外部腳本 → 高風險
- `base64` 用於解碼 API 回應 → 低風險
- `base64` 用於混淆惡意 payload → 高風險

同時檢查是否有腳本/功能 **不符合 SKILL.md 描述**，這是最可疑的訊號。

#### 2D：風險等級判定

| 等級 | 條件 |
|------|------|
| 🔴 高風險 | 下載並執行、系統駐留、加密貨幣錢包存取、代碼描述與實際行為嚴重不符 |
| 🟡 中風險 | Shell 執行、動態代碼、SSH/雲端憑證、瀏覽器資料、明顯混淆 |
| 🟢 低風險 | 無以上特徵，或僅有低風險 pattern 且語意合理 |

#### 2E：安全評分計算

以所有 skill 的掃描結果為基礎，計算整體安全評分：

- 基礎分：100 分
- 有任何高風險 skill：−30，之後每多一個高風險 skill 再追加 −10
- 每個中風險 skill：−5
- 每個低風險 skill：−1
- 最低 0 分

> 範例：掃描 5 個 skill，其中 2 個高風險、1 個中風險 → 100 − 30 − 10 − 5 = 55 分

### Step 3：輸出 Markdown 安全報告

掃描完所有 skill 後，輸出以下格式的報告：

---

## 📊 安全掃描摘要

| 項目 | 數量 |
|------|------|
| 掃描 Skills 總數 | N |
| 🔴 高風險 | N |
| 🟡 中風險 | N |
| 🟢 低風險 | N |
| 安全評分 | X/100 |

---

對每個 skill 輸出：

## [風險圖示] Skill 名稱 (`路徑`)

**風險等級**：🔴 高風險 / 🟡 中風險 / 🟢 低風險

**功能描述**：根據 SKILL.md 所述，此 skill 的用途是 ...

**掃描發現**：

- 🔴 [類別] 具體發現（`檔案名稱:行號` 與命中 pattern）
- 🟡 [類別] 具體發現（`檔案名稱:行號` 與命中 pattern）
- （無發現則寫：未偵測到明顯可疑特徵）

**網路活動**：
- `https://example.com/api` — (判斷：合理的 API 端點 / 可疑的外部連線)
- （若無外部 URL，寫：未偵測到外部網路連線）

**AI 分析**：
用 2-4 句話解釋：(1) 這個 skill 實際在做什麼，(2) 偵測到的 pattern 是否符合其功能，(3) 是否有不符合描述的隱藏行為。

**建議**：
- ✅ 相對安全：未發現明顯惡意特徵，建議遵循最小權限原則使用。
- ⚠️ 具可疑行為：建議在隔離環境測試，並手動檢查標記的程式碼段落。
- 🚫 高度危險：不建議在含真實憑證或資產的環境安裝，僅可在隔離 VM / 沙盒中測試。

---

## 注意事項

- 此為靜態語意分析，不執行任何程式碼
- Regex 掃描有 false positive，AI 語意判斷是最終依據
- 若需要更深入的審查，可針對特定 skill 要求詳細分析
