# 容晟科技客戶管理 SOP

## API 端點（rsun.me Worker）

| 動作 | 方法 | 路徑 | 認證 |
|------|------|------|------|
| 列出所有客戶 | GET | `/api/clients` | 無 |
| 查單一客戶 | GET | `/api/clients/:id` | 無 |
| 新增客戶 | POST | `/api/clients` | `X-Admin-Pin` |
| 更新客戶 | PUT | `/api/clients/:id` | `X-Admin-Pin` |
| 新增備注 | POST | `/api/clients/:id/notes` | `X-Admin-Pin` |

**環境變數**：`RSUN_ADMIN_PIN`（使用者自行 export，或在指令前加上）

---

## 操作指令 SOP

---

### 🟢 新增客戶（`新增客戶` / `建立客戶` / `add client`）

**步驟**：

1. 詢問並收集以下資訊（未提供者用預設值）：

   | 欄位 | 說明 | 預設值 |
   |------|------|--------|
   | `id` | 唯一識別，小寫英文+連字符（如 `apex-gold`） | 必填，無預設 |
   | `name` | 客戶全名（中文或英文） | 必填，無預設 |
   | `avatar` | 1–2 個 Emoji 代表產業（房產→🏠，金融→💰，科技→💡） | 依產業自動選 |
   | `industry` | 產業分類 | 必填 |
   | `market` | 服務市場（如「台灣/澳洲」） | `"待確認"` |
   | `status` | `active` / `prospect` / `completed` / `on-hold` | `"prospect"` |
   | `status_label` | 中文狀態說明（如「提案中」） | 依 status 自動選 |
   | `contact.name` | 窗口姓名 | 選填 |
   | `contact.email` | 窗口 Email | 選填 |
   | `contact.line` | LINE ID | 選填 |
   | `budget` | 預算範圍（如「NT$200,000–300,000」） | `"待定"` |
   | `current_phase` | 當前階段說明 | `"初步接洽"` |

   **status_label 預設對照**：
   - `active` → `"合作中"`
   - `prospect` → `"提案中"`
   - `completed` → `"已完成"`
   - `on-hold` → `"暫緩"` 

2. 確認後，執行：
   ```bash
   curl -s -X POST https://rsun.me/api/clients \
     -H "Content-Type: application/json" \
     -H "X-Admin-Pin: $RSUN_ADMIN_PIN" \
     -d '{
       "id": "<id>",
       "name": "<name>",
       "avatar": "<avatar>",
       "industry": "<industry>",
       "market": "<market>",
       "status": "<status>",
       "status_label": "<status_label>",
       "contact": { "name": "<contact.name>", "email": "<contact.email>", "line": "<contact.line>" },
       "budget": "<budget>",
       "current_phase": "<current_phase>"
     }'
   ```

3. 若收到 HTTP 201，輸出：
   ```
   ✅ 客戶已建立：<name>（<id>）
   🔗 Portal：https://rsun-tracker.pages.dev/clients/
   ```
   若 HTTP 409，提示客戶 ID 已存在，詢問是否改用 PUT 更新。

4. 詢問是否同步部署（Portal 刷新）：若是，執行部署 SOP。

---

### ✏️ 更新客戶（`更新客戶` / `改狀態` / `改階段` / `update client`）

**步驟**：

1. 確認要更新哪個客戶 ID。若不確定，先執行「列出客戶」。

2. 詢問要修改哪些欄位（可更新欄位）：
   - `status` / `status_label`
   - `current_phase`
   - `budget`
   - `contact`（name / email / line）
   - `market`

3. 執行：
   ```bash
   curl -s -X PUT https://rsun.me/api/clients/<id> \
     -H "Content-Type: application/json" \
     -H "X-Admin-Pin: $RSUN_ADMIN_PIN" \
     -d '{ <只帶要修改的欄位> }'
   ```

4. 若 HTTP 200：`✅ <id> 已更新，updated_at = <今天日期>`

---

### 📋 列出所有客戶（`客戶列表` / `所有客戶` / `list clients`）

執行：
```bash
curl -s https://rsun.me/api/clients | python3 -c "
import sys, json
data = json.load(sys.stdin)
clients = data if isinstance(data, list) else data.get('clients', [])
for c in clients:
    status = c.get('status_label') or c.get('status','?')
    updated = c.get('updated_at','?')
    phase = c.get('current_phase','?')
    print(f\"  {c.get('avatar','')} {c['name']} ({c['id']})  [{status}]  {phase}  更新:{updated}\")
"
```

格式化輸出：
```
🏠 Apex Gold (apex-gold)  [提案中]  v3 提案已送出  更新:2026-04-20
🌿 先見明 Horizen (horizen)  [合作中]  開發中  更新:2026-04-18
...
```

---

### 🔍 查客戶（`查客戶` / `看客戶資料` / `client detail` / `查 <客戶名稱>`）

執行：
```bash
curl -s https://rsun.me/api/clients/<id> | python3 -c "
import sys, json
c = json.load(sys.stdin)
print(json.dumps(c, ensure_ascii=False, indent=2))
"
```

整理後輸出關鍵資訊：
- 基本資料（名稱、產業、市場、狀態、階段）
- 聯絡窗口（姓名、Email、LINE）
- 預算
- 文件清單（id、標題、版本、建立/更新日期）
- 最新備注（最多 3 條）

---

### 📝 加備注（`加備注` / `客戶備注` / `add note` / `記錄一下`）

**步驟**：

1. 確認客戶 ID 和備注內容。

2. 執行：
   ```bash
   curl -s -X POST https://rsun.me/api/clients/<id>/notes \
     -H "Content-Type: application/json" \
     -H "X-Admin-Pin: $RSUN_ADMIN_PIN" \
     -d '{ "text": "<備注內容>" }'
   ```

3. HTTP 200：`✅ 備注已加入 <id>`

---

### 📄 新增文件到客戶（`新增文件` / `加文件` / `add doc` / `登記文件`）

**步驟**：

1. 確認客戶 ID 與文件資訊：

   | 欄位 | 說明 |
   |------|------|
   | `doc_id` | 文件 slug（如 `proposal-v3`、`requirements-form`） |
   | `title` | 文件標題（中英文皆可） |
   | `url` | 相對路徑（如 `/clients/apex-gold/proposal`） |
   | `version` | 版本號（如 `v3`）|
   | `description` | 一行說明（選填） |
   | `created` | 建立日期（預設今天）|
   | `updated` | 更新日期（預設今天）|

2. 先 GET 現有文件清單，將新文件附加到 `documents[]`，再 PUT 回去：
   ```bash
   # 取得現有資料
   CURRENT=$(curl -s https://rsun.me/api/clients/<id>)
   # 手動確認現有 documents[]，加入新項目，執行 PUT
   curl -s -X PUT https://rsun.me/api/clients/<id> \
     -H "Content-Type: application/json" \
     -H "X-Admin-Pin: $RSUN_ADMIN_PIN" \
     -d '{ "documents": [ <現有 documents + 新項目> ] }'
   ```

3. HTTP 200：`✅ 文件 <doc_id> 已加入 <id>`

---

### 🚀 同步部署（`同步部署` / `deploy tracker` / `部署客戶文件` / `更新 portal`）

**步驟**：

1. 確認 `RSUN_ADMIN_PIN` 已設定：
   ```bash
   echo "RSUN_ADMIN_PIN=${RSUN_ADMIN_PIN:-(未設定)}"
   ```
   若未設定，提示：`export RSUN_ADMIN_PIN=你的PIN`

2. 執行 sync-and-deploy：
   ```bash
   cd ~/Projects/TRACKER && RSUN_ADMIN_PIN=$RSUN_ADMIN_PIN ./scripts/sync-and-deploy.sh
   ```

3. 腳本會：
   - 掃描 last commit 中 `clients/*` 的變更
   - PUT 受影響客戶的 `updated_at` 到 registry
   - `npx wrangler pages deploy` 到 Cloudflare Pages

4. 完成後：
   ```
   ✨ 部署完成
   Portal：https://rsun-tracker.pages.dev/clients/
   ```

---

## 注意事項

- **RSUN_ADMIN_PIN 不要寫死在指令裡**，從環境變數讀取
- **客戶 ID 一旦建立不可修改**（KV key），若打錯只能刪除重建（目前無 DELETE 端點，需手動清 KV）
- **documents[] 更新是全量覆蓋**，PUT 時必須帶完整陣列，否則會清空現有文件
- **備注是 prepend**（最新在前），最多保留 50 條（Worker 端自動截斷）
