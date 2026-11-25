---
name: cua-browser-github-oauth
description: Complete GitHub OAuth/Device Code Flow via Cua Driver browser automation — bypasses Chrome URL bar search issue when authenticating from headless agents
version: 2.0
triggers:
  - cua github
  - github oauth
  - gh auth login
  - device code flow
---

# Cua Browser GitHub OAuth 流程

## 適用場景
需要用 browser 完成 GitHub OAuth（device code flow、create token、授權 gh CLI），但 Cua 嘅 `type_text` + Enter 喺 Chrome URL bar 會觸發 Google Search 而唔係 navigate。

## 核心問題
Chrome URL bar 嘅預設行為係：打 `github.com/xxx` → Google Search，唔係直接 navigate。呢個令到用 Cua 嘅 `type_text()` → `press_key('enter')` 去 navigate 唔 work。

## 重要前提：用戶角色判斷

Device code flow 有幾種用戶場景，做法大不同：

**場景 A：用戶正用電腦打字（標準）**
→ 用 terminal 開 `gh auth login`，用戶自己輸入 code 最直接。

**場景 B：用戶喺手機上（如 Telegram），電腦冇人操作**
→ gh CLI timeout（~120s）係主要問題，用戶手機操作嘅 timing 難以配合。
→ **解決：** 叫用戶手機開 browser 去 https://github.com/login/device 自己貼 code，佢填完授權就得。agent 喺 terminal 等住 `gh auth status`。

**場景 C：用戶想 agent 喺電腦上全自動搞**
→ 先確定 Safari/Chrome 嘅 AX tree 深度。Safari 可以深達 2000+ nodes，Cua 嘅 `get_window_state` 會被截斷。
→ 如果 vision mode 截圖唔 work（background app screenshot limitation），需要用 AppleScript。

## 可靠方法

### 方法 A：用 `open` command（最 reliable）
```bash
open -a "Google Chrome" "https://github.com/login/device"
# 或者用 skip_account_picker 跳過 Google account picker
open -a "Safari" "https://github.com/login/device?skip_account_picker=1"
```
呢個會直接開新 tab/window navigate 去目標 URL。然後用 Cua 嘅 `list_windows` 睇新開嘅 window。

### 方法 B：Cua hotkey + URL（次選）
```python
# Cmd+L focus URL bar
cua_call('hotkey', {'pid': chrome_pid, 'window_id': wid, 'keys': ['command', 'l']})
# 必須用完整 https:// 開頭（但依然可能被 search）
cua_call('type_text', {'pid': chrome_pid, 'window_id': wid, 'text': 'https://github.com/login/device'})
cua_call('press_key', {'pid': chrome_pid, 'window_id': wid, 'key': 'enter'})
```

### 方法 C：AppleScript（最直接，需事前 Enable 設定）

**Step 0：確保 Safari Developer 設定已開**
Safari > Settings > Developer > 「Allow JavaScript from Apple Events」
可以一開機就叫用戶開咗佢，之後永久可用。

**Step 1：Terminal 開 gh auth login 攞 code**
```bash
gh auth login --git-protocol https --web
```
輸出：`! First copy your one-time code: XXXX-XXXX`

**Step 2：用 open command 開 Safari 去 device login page**
```bash
open -a "Safari" "https://github.com/login/device?skip_account_picker=1"
```
用 `?skip_account_picker=1` 可以跳過 Google account picker，直接去 code input page。

**Step 3：AppleScript 檢查當前 URL + 填 code**
```bash
# Check which page we're on
osascript -e 'tell app "Safari" to return URL of current tab of window 1'

# If on account picker page, click the desired account
osascript -e '
tell application "Safari"
    do JavaScript "..." in current tab of window 1
end tell'

# Fill device code into inputs
osascript -e '
tell application "Safari"
    do JavaScript "
        document.getElementById(\"otp_0\").value = \"B\";
        document.getElementById(\"otp_1\").value = \"C\";
        ...
    " in current tab of window 1
end tell'
```

**Step 4：授權確認頁面處理**
填完 code 後，GitHub 會顯示 account name 同「Continue」button。
```bash
osascript -e '
tell application "Safari"
    do JavaScript "
        document.querySelector(\"button\").click();
    " in current tab of window 1
end tell'
```

**Step 5：Terminal check**
```bash
gh auth status
# 成功: Logged in as <username>
```

## GitHub Token Copy 問題
經典 token create 後，GH 嘅 UI 用 CSS `text-overflow: ellipsis` truncate 顯示。Cua 嘅 Accessibility API 同 clipboard 都只拎到 truncated version（例如 `ghp_go...Pyjy`）。

**解決方法：** 直接用 `open` command 開 token 頁面，叫用戶手動 copy token，或者用 device code flow 代替。

## 經典 Token Create（備用方案）

如果 device code flow 持續失敗，可以用 classic token：

1. `open -a "Google Chrome" "https://github.com/settings/tokens/new"`
2. Cua fill Note + 揀 repo scope + workflow
3. Scroll down + click "產生令牌"
4. Success page 出現。**Token value truncated** — 需要用戶手動 copy

## Device Code Flow vs Token 對比

| 方法 | 適合場景 | 風險 |
|---|---|---|
| Device code flow（手機授權） | 用戶喺手機/另一部機操作 | gh CLI timeout 問題；用戶手機 browser 可能 redirect 到主頁而非 /login/device |
| Token method（PAT） | 用戶肯俾 token 時 | Token 用完要 delete；agent 唔應該儲存 token 在任何地方 |
| Cua Driver 自動填 code | 電腦 Chrome/Safari 可用 | Safari AX 2000+ nodes 易截斷；Chrome 相對穩定 |

## Token method 安全操作 SOP

1. **只用一次**：agent 收完 token 後，用 `gh auth login --with-token` login，唔好 save 落任何檔案
2. **用完即棄**：叫用戶去 https://github.com/settings/tokens delete 個 token。gh CLI 喺 macOS 會自動轉用 Keychain credential，唔再依賴 token
3. **Keychain 自動接管**：login 成功後 macOS Keychain 會存 credential。如果後續 delete token，gh CLI 會顯示 invalid token error，要 `gh auth logout` 再重新 login
4. **Fine-grained token vs Classic token**：Fine-grained 嘅 scopes 比 Classic 精準，但兩者都只暴露 GitHub account 本身，唔會洩漏 iMac/system info
5. **唔好將 token 寫入任何 config file**：gh CLI 嘅 hosts.yml 只存 username，token 喺 keychain

## 手機操作嘅死循環陷阱

用戶手機成功喺 browser 授權後，gh CLI session 已 timeout：
1. Agent 再開新 code → 用戶手機 browser 直接 redirect 到 GitHub 主頁（因為已授權）
2. 用戶永遠去唔到 `/login/device` 重新輸入 — 手機 browser（尤其係內置 browser）可能 cache 咗 redirect，之後永遠 show 404
3. **解決：** logout 先 (`gh auth logout`) 再重新開 flow，或者直接轉用 Token method

## macOS 環境下的 GitHub CLI 認證路徑

### macOS Keychain token 失效後的處理

當用戶 delete 咗 PAT token 後，gh CLI 嘅 keyring 入面仍然存有舊 token 記錄，顯示：
```
X Failed to log in to github.com account (keyring)
- The token in keyring is invalid.
```

**必須先 logout 再重新 login，唔可以直接再 `gh auth login`：**
```bash
gh auth logout -h github.com -u <username>   # 先清除舊記錄
gh auth login --hostname github.com --git-protocol https --web   # 再重新 login
```

### 多種認證方式嘅優先級策略

| 嘗試順序 | 方法 | 時機 |
|---|---|---|
| 1 | Device code flow（手機） | 用戶容易操作時先試 |
| 2 | Cua Driver + Chrome 自動填 code | 用戶想全自動、Chrome 可用時 |
| 3 | Fine-grained PAT token（使用一次） | 1-2 次 device flow 失敗後立即轉用 |
| 4 | AppleScript + Safari（需預先 enable JS） | Safari 用戶、需自動化時 |

**實戰建議：** 如果 device code flow 試咗 2 次都唔得，直接 skip 去 Token method。每次 device flow 大約要 3-5 分鐘來回溝通，仲未計 troubleshooting。

### Cua 實戰 Chrome 完整操作流程（2026-06-22 實測有效）

1. **確定 Chrome 嘅 window_id**：`list_windows(pid=chrome_pid)` → 揀 on_screen=true 嘅 window
2. **用 `open -a "Google Chrome" "https://github.com/login/device?skip_account_picker=1"` navigate**
3. **攞 code**：`gh auth login --git-protocol https --web`（呢邊開住先唔等）
4. **快啲填 code**：用 AX tree 嘅 element_index
   - 使用者代碼 0-3：`[21]`-`[24]` → click + type_text 逐格填
   - element `[25]` 係 dash，skip
   - 使用者代碼 5-8：`[26]`-`[29]` → click + type_text 逐格填
5. **Click 「繼續」**：`click(element_index=30, pid, window_id)`
6. **等待 confirmation page load** → URL 變 `github.com/login/device/confirmation`
7. **Click 「授權 GitHub」**：喺新 AX tree 搵 `AXButton "授權 GitHub"`（通常 element [37] 或 [436] — Chrome 有 duplicate tree）
8. **Check**：`gh auth status`

**重要 timing note：** 填 code 同 click 授權嘅動作要快，因為 `gh auth login` 嘅 session 只有 ~120s 有效期。如果中間 vision_analyze 或 AX query 花太多時間，可能未 click 完授權就已經 timeout。

**Chrome AX tree duplicate 問題：** Chrome 經常有 2 個 AXWindow（一個 active、一個 stale），同樣嘅 button 會出現喺兩個位置。click 邊個都得，效果一樣。

## GitHub Primer React 組件自動化（2026-07-04 實戰發現）

GitHub 使用 Primer React Components，輸入組件需要特殊處理：

### Create Repository 頁面 (`/new`)

- **Repository name input**: `id="repository-name-input"` (input type="text")
- **Description input**: `id="_r_d_"` (input，React controlled)
- **Create repository button**: `document.querySelectorAll('button')[21]` — text "Create repository"

**可靠填寫方法：`execCommand('insertText')`**

```javascript
// 填 repo name
var el = document.querySelector('#repository-name-input');
el.focus();
document.execCommand('insertText', false, 'cocos-creator-debug-skills');

// 填 description
var desc = document.querySelector('#_r_d_');
desc.focus();
document.execCommand('insertText', false, '17 executable AI agent skills...');

// Click Create repository
document.querySelectorAll('button')[21].click();
```

**注意：** 使用 `nativeSetter + inputEvent dispatch` 會 fail（React Primer 組件 reject programmatic value set）。`execCommand('insertText')` 係唯一成功方法。使用前要先 `focus()` + `click()` 確保 element 已被 React focus。

### Create Token 頁面 (`/settings/tokens/new`)

- **Token note input**: `id="token_description"`
- **Scopes checkboxes**: 用 `input[value="repo"]` selector
- **同樣可以用 `execCommand('insertText')` 填 note**

### 已知元素位置

| 頁面 | 元素 | Selector | 方法 |
|------|------|----------|------|
| `/new` | Repo name | `#repository-name-input` | execCommand('insertText') |
| `/new` | Description | `#_r_d_` | execCommand('insertText') |
| `/new` | Create button | `button:contains("Create repository")` | .click() |
| `/settings/tokens/new` | Token note | `#token_description` | execCommand('insertText') |
| `/settings/tokens/new` | repo scope | `input[value="repo"]` | .click() |

## 實戰發現：GitHub Sudo Mode & 2FA（2026-07-04 更新）

### Sudo Mode 觸發條件

- ✅ **唔會觸發**：`/settings/tokens` (token list page)、`/settings/emails`、`/new`
- ❌ **會觸發**：`/settings/tokens/N` (individual token page)、`/settings/tokens/new` (new token page)、any settings page that needs confirmation

### Sudo Mode 頁面結構

GitHub Sudo Mode 用 `<sudo-credential-options>` web component，有兩個選項：

**Option 1: GitHub Mobile（優先）**

```html
<button class="...">Use GitHub Mobile</button>
```

Click 後 GitHub send push notification 到手機 GitHub App。同時頁面顯示一組**驗證數字**：

```
We sent you a verification request on your GitHub Mobile app.
Enter the digits shown below to enter sudo mode.

42
```

你唔需要入呢個 code — GitHub Mobile app 會 show 呢個 code，你喺 app 入面確認就得。

**Option 2: Send a code via email**

呢個係一個 `<button>` 包喺 `<li>` 入面（唔係 `<a>` link）：

```html
<li><button><span>Send a code via email</span></button></li>
```

位置大約喺 (689, 352)（window-local coordinates）。可以用 Cua pixel click 觸發。

### 實戰策略

由於 Sudo Mode 需要用戶手機參與，以下係最有效率嘅做法：

1. **直接 navigate 到 `https://github.com/settings/tokens`**（list page，唔使 sudo）
2. 如果可以 regenerate existing token，呢個頁面冇 2FA block
3. 如果要 generate 新 token → 㩒「Generate new token」→ sudo mode → **通知用戶手機 approve**
4. 用戶 approve 後頁面自動 reload → agent 可以繼續填 form

### Key Insight：Token List Page ≠ Token Edit Page

Token list page (`/settings/tokens`) 完全唔使 sudo mode。但任何操作去 token detail 或 creation page 都需要。策略係：
- 如果可以 reuse existing token → 直接喺 list page 用已知 token ID 操作
- 如果一定要新 token → 用 GitHub Mobile 最快，email code 可能 delay

Generate PAT 時，GitHub 會卡一個「Confirm access」頁面要求手機 GitHub App 輸入驗證碼。Cua Driver 無法繞過呢個 macOS 安全邊界。

**協作模式：**
1. Cua 導航到 `https://github.com/settings/tokens/new` ✅
2. GitHub 彈出 sudo mode 頁面 → **需要 user 用手機 GitHub App 確認**
3. User 確認後返到 token 頁面 → Cua 可以繼續填 Note、tick scopes、Generate

**經驗教訓：**
- Cmd+L → type URL → Return 係最可靠嘅導航方法（AX path）
- Edge/Chromium 嘅 keyboard tab/return 有時會觸發 Google 搜尋而非 dropdown — 唔好用 tab 做 form 操作
- type_text 落 focused element 仍然可靠
- 如果頁面跳咗，重新 Cmd+L → type URL → Return 導航就得

## 已知 Pitfalls
- **gh CLI timeout ~120s** — 用戶喺手機操作一定唔夠快。最好係 agent 開 flow 先，唔好等 gh auth login 個 process 一路等，而係開咗 flow 就 let it background，等用戶搞掂先 check
- **手機操作嘅死循環**：用戶成功喺手機授權後，gh CLI session 已 timeout，再開新 code → 用戶手機 browser 被 redirect 到 GitHub 主頁 → 永遠去唔到 /login/device。**解決：** 唔好靠用戶手機做多次。改用電腦 Chrome 直接操作，或者用 Token method 一了百了
- **Cua 填 8 格 code input fields 可行**：Chrome 嘅 AX tree 對 `/login/device` 頁面支援良好，element_index [21]~[29] (使用者代碼 0-8) 可以用 `click` + `type_text` 逐格填。但記住中間 element [25] 係 dash（skip）。
- **授權確認頁面嘅「授權 GitHub」button**：填完 code 後嘅 `/login/device/confirmation` 頁面嘅「授權 GitHub」button 係 element [37]（AXButton）。click 完後 gh CLI 要見到先 sync 到
- **Cua 對同一 window 嘅 snapshot 有 2 個 duplicate tree**：Chrome 經常有 2 個 AXWindow（一個 active、一個 stale），同樣嘅 button 會出現喺兩個位置（e.g. [37] 同 [436]）。click 邊個都得
- **最穩陣係直接放棄 device code flow 改用 Token**：如果試咗 2-3 次 device flow 都搞唔掂，直接叫用戶開 github.com/settings/tokens generate fine-grained token 畀 agent，用 `gh auth login --with-token` 秒搞掂
- **Chrome 嘅 `open` command 會開新 tab，唔係新 window**：如果 Chrome 已經有 login session，新 tab 會自動跳過 account picker
- **Cua vision mode 對 background apps 唔一定 work** — 試到唔得就轉 method，唔好死試
- **Chrome URL bar 唔可以用嚟 navigate** — 一定用 `open` command
- **Safari AX tree 極深（2000+ nodes）** — query filter 都救唔到，AppleScript 係更可靠嘅路
- **AppleScript 需要事前 enable JS from Apple Events** — 呢個係一次性設定
- **Token copy truncated** — 唔好依賴 Cua copy token
- **Cua `hotkey` 用 array** — `keys: ['command', 'l']` 唔係 `key: 'l'` + `modifiers`
