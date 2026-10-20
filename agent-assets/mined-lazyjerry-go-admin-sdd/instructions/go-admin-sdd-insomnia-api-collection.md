---
applyTo: "docs/insomnia/**/*.yaml"
description: "Insomnia 5.0 格式 API 集合檔案生成規範"
---

# Insomnia API 集合檔案生成指令

供 AI 代理在建立或更新 API 測試集合時遵循 Insomnia 5.0 格式規範。

---

## 指令

當需要建立或更新 API 測試集合時，應在 `docs/insomnia/` 目錄中建立符合 Insomnia 5.0 格式的 YAML 檔案。

---

## 目標

- 建立標準化的 API 測試集合
- 確保與 Insomnia REST Client 完全相容
- 提供完整的 CRUD 操作測試覆蓋
- 包含錯誤處理和驗證測試案例
- 支援環境變數配置

---

## Insomnia 5.0 格式規範

### 基本結構

```yaml
type: collection.insomnia.rest/5.0
name: [集合名稱]
meta:
  id: [唯一識別碼]
  created: [Unix 時間戳]
  modified: [Unix 時間戳]
  description: "[集合描述]"
collection:
  - [請求物件列表]
environments:
  - [環境設定列表]
```

### 請求物件格式

```yaml
- url: "{{ _.base_url }}/api/endpoint"
  name: "[請求名稱]"
  meta:
    id: [請求唯一識別碼]
    created: [Unix 時間戳]
    modified: [Unix 時間戳]
    isPrivate: false
    description: "[請求描述]"
    sortKey: [排序鍵值]
  method: [HTTP方法]
  body:
    mimeType: application/json
    text: |
      {JSON 請求內容}
  headers:
    - name: Accept
      value: application/json
    - name: Content-Type
      value: application/json
  settings:
    renderRequestBody: true
    encodeUrl: true
    followRedirects: global
    cookies:
      send: true
      store: true
    rebuildPath: true
```

### 環境變數格式

```yaml
environments:
  - name: "Local Development"
    meta:
      id: env_local_dev
      created: [Unix 時間戳]
      modified: [Unix 時間戳]
    data:
      base_url: "http://localhost:80"

  - name: "Production"
    meta:
      id: env_production
      created: [Unix 時間戳]
      modified: [Unix 時間戳]
    data:
      base_url: "https://api.production.com"
```

---

## 必要請求類型

### CRUD 操作

1. **GET** - 列表查詢（支援分頁、篩選）
2. **POST** - 建立新資源
3. **GET** - 單一資源查詢
4. **PUT** - 完整資源更新
5. **PATCH** - 部分資源更新
6. **DELETE** - 資源刪除

### 系統測試

1. **Health Check** - 系統健康檢查
2. **Authentication** - 身份驗證測試（如適用）

### 錯誤處理測試

1. **Validation Errors** - 輸入驗證錯誤（422）
2. **Not Found** - 資源不存在錯誤（404）
3. **Server Errors** - 伺服器錯誤處理（500）

---

## 命名規範

### 檔案命名

- 格式：`{service-name}-api-collection.yaml`
- 範例：`todo-api-collection.yaml`

### 請求命名

- 中文描述，清楚表達功能
- 範例：
  - "獲取所有任務"
  - "建立新任務"
  - "更新任務狀態"
  - "刪除指定任務"

### ID 命名規範

- Collection ID：`wrk_{service}_{type}_collection`
- Request ID：`req_{action}_{resource}`
- Environment ID：`env_{environment_name}`

---

## 請求內容規範

### Headers 設定

所有請求必須包含：

```yaml
headers:
  - name: Accept
    value: application/json
  - name: Content-Type
    value: application/json
```

### Body 範例資料

- 使用真實但通用的測試資料
- 避免敏感或個人資訊
- 包含各種資料類型（字串、數字、布林值、陣列、物件）

### URL 參數化

- 使用環境變數：`{{ _.base_url }}`
- 支援動態參數：`{{ _.todo_id }}`

---

## 測試案例覆蓋

### 正常流程測試

1. 建立資源 → 查詢列表 → 查詢單一 → 更新 → 刪除
2. 每個步驟驗證回應格式和狀態碼

### 異常流程測試

1. 無效輸入驗證
2. 不存在資源處理
3. 權限驗證（如適用）
4. 伺服器錯誤處理

### 邊界條件測試

1. 空資料處理
2. 最大長度限制
3. 特殊字符處理
4. 數據類型驗證

---

## 文檔要求

### 集合描述

- 包含 API 版本資訊
- 說明主要功能和用途
- 列出支援的操作類型

### 請求描述

- 清楚說明請求目的
- 標註預期的回應格式
- 說明必要參數和可選參數

### 使用說明

- 提供匯入步驟
- 說明環境變數設定
- 包含測試執行順序建議

---

## 品質檢查清單

- [ ] 格式符合 Insomnia 5.0 規範
- [ ] 所有 CRUD 操作都有對應請求
- [ ] 包含完整的錯誤處理測試
- [ ] 使用環境變數進行 URL 參數化
- [ ] 請求命名清楚且符合規範
- [ ] 包含真實的測試資料
- [ ] 提供完整的使用文檔
- [ ] 支援多環境配置
- [ ] 包含系統健康檢查
- [ ] 所有請求都有適當的描述

---

## 範例檔案結構

```
docs/insomnia/
├── {service}-api-collection.yaml    # 主要集合檔案
├── README.md                       # 使用說明文檔
└── environments/                   # 環境配置檔案（可選）
    ├── local.yaml
    ├── staging.yaml
    └── production.yaml
```

---

## 注意事項

1. **時間戳格式**：使用 Unix 毫秒時間戳
2. **字符編碼**：確保 UTF-8 編碼支援中文
3. **YAML 語法**：注意縮排和特殊字符轉義
4. **版本控制**：修改時更新 modified 時間戳
5. **敏感資訊**：避免在集合中包含敏感資料
6. **向下相容**：確保與舊版 Insomnia 相容性

---

_此指令模板遵循 Insomnia 5.0 API 集合格式標準，確保生成的檔案完全相容於 Insomnia REST Client。_
