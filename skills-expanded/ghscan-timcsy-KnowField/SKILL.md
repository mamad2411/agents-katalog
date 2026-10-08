---
name: ship-knowfield
description: 把做完的一刀真正送上線——反流知識庫、推送、等 CI 出映像、部署 k3s、核對 pod 的實際 digest。當一個 spec 實作完成、測試綠、要出貨時使用。
---

# 出貨收工（KnowField）

**為什麼存在**：這條流程在 2026-08-21 一天內手動跑了三次，步驟完全相同，
而其中兩步**漏掉會造成災難且不會報錯**：

- `helm upgrade` 忘了 `--reuse-values` → PG 密碼與 `existingSecret` 掉回預設 → **站掛掉**（`history/089`）
- 不核對 digest → push 靜默失敗時 rollout 照樣說「成功」，你在**驗舊版**（`experience.md「部署要核對「pod 實際 digest」」`）

第三次還撞到權限被擋。這些都寫在我的私人記憶裡過——但那不是專案的小腦，
**Codex／Gemini 看不到**，換一台機器也沒有。所以它該在這裡。

## 判準：出貨不是 push，是「線上跑的是這一版」

`git push` 成功、CI 綠、`rollout` 成功，三個都不證明線上跑的是你剛寫的東西。
**唯一算數的證據是 pod 的 `imageID` digest 等於 ghcr 上那個 tag 的 digest。**
沒核對這一條，這個 skill 沒有做完。

## 步驟

### 1. 出貨前的門檻（任一條沒過就別往下）

```bash
uv run pytest -q                      # 後端全綠
cd frontend && npm run build          # ⚠️ 用 npm run build（tsc -b），不是 npx tsc --noEmit
cd frontend && npm run test -- --run  # 前端有測試才跑
git status --short                    # 沒有沒意料到的改動
```

⚠️ `npx tsc --noEmit` 與 `npm run build` **不是同一條管線**，本地綠、CI 紅已經發生過。

### 2. knowie 反流（**這一步最容易被跳過，而跳過不會有人發現**）

一刀做完要留下的東西——不是全部都要，用判準挑：

| 產出 | 何時寫 |
|---|---|
| `history/NNN` | 有 **pivot**（舊決定被推翻／假設被改）。⚠️ 只是「做完了」不算轉移 |
| `experience` 教訓 | 它會改變**某條判準**怎麼寫；有來源可 grep |
| `vision` 打勾 ＋ 里程碑索引補列 | 階段出貨了 |
| draft 標記已兌現 | 設計源已落地 |

⚠️ **`vision` 打勾最常漏**：階段 35 出貨後三天路線圖還說它沒做（2026-08-22 才發現）。
判準是 `experience.md「死的知識不是靜止的知識，是沒有任何消費者會發現它錯掉的知識」`「如果它錯了，誰會發現」——沒有人會，所以要在這裡當成步驟。

### 3. 推送並等映像

```bash
git push
SHA=$(git rev-parse HEAD)
RUN=$(gh run list --limit 5 --json databaseId,headSha -q "map(select(.headSha==\"$SHA\"))[0].databaseId")
gh run watch $RUN --exit-status
```

⚠️ **不要用 `gh run list --limit 1`**：GitHub 註冊 run 有延遲，push 完立刻查會抓到**上一次**的 run，
然後它回你「已經完成，success」——你以為 CI 綠了，其實它根本還沒開始。
2026-08-25 就這樣過了一次假的綠燈。**一定要用 `headSha` 挑，不是用時間挑。**
（`$RUN` 是空的就代表 run 還沒註冊，等幾秒重查——空值比抓錯的好。）

### 4. 部署（⚠️ 兩個旗標都不能少）

```bash
SHA=$(git rev-parse --short HEAD)
helm upgrade knowfield deploy/helm/knowfield -n knowfield --reuse-values --set image.tag=$SHA
```

- ⚠️ `--reuse-values`：PG 密碼與 `existingSecret: knowfield-env` 都在 release values 裡。**不帶會把站弄掛。**
- ⚠️ **不要用 `kubectl set image` 繞過 helm**——會造成 release 漂移，
  下次任何人 `helm upgrade` 都把站退回舊版（2026-08-21 就是這樣從 `988cdd2` 漂到 `40a8f25`）。

### 5. 核對 digest（沒做這步就沒出貨）

⚠️ **先等 rollout，再讀 digest**——沒等的話，`.items[0]` 會挑到還沒起來的新 pod
（或正在終止的舊 pod），`imageID` 是**空字串**，而輸出長這樣：

```
  ready=false
```

那看起來像「digest 對不上」，實際上是「還沒有 digest 可讀」。⇒ 空的結果有兩個原因。

```bash
kubectl -n knowfield rollout status deploy/knowfield-knowfield --timeout=180s
POD=$(kubectl -n knowfield get pod -l app.kubernetes.io/component=app \
  --field-selector=status.phase=Running -o jsonpath='{.items[0].status.containerStatuses[0].imageID}')
GHCR=$(gh api "/user/packages/container/knowfield/versions" \
  --jq ".[] | select(.metadata.container.tags[]? == \"$SHA\") | .name")
[ -n "$POD" ] && [ -n "$GHCR" ] || { echo "❌ 有一邊是空的——不是不符，是沒讀到"; }
echo "pod=${POD#*@}"; echo "ghcr=$GHCR"
```

兩個 `sha256:` **必須逐字相同**。不同就是拉到舊映像，回頭查 push。
⚠️ **任何一邊是空的都不算通過**——空的和不符是兩件事，而 `[ "$a" = "$b" ]` 只認得一件。

ⓘ `deploy` 的名字是 `knowfield-knowfield`（release 名 ＋ chart 名）。
`kubectl rollout status deploy -l app.kubernetes.io/component=app` **選不到它**
——那個 label 在 **pod** 上，不在 Deployment 上，而 kubectl 只會說 `No resources found`。

⚠️ **不要自己寫「等到有 pod ready」的迴圈**（2026-08-27，rev 58 就這樣誤報過一次）。
滾動更新期間**舊 pod 一直是 ready**，⇒ 那個條件永遠先為真，你會讀到上一版的 digest
而以為出貨了。要等就把**目標 digest 寫進條件裡**：

```bash
WANT=$(gh api "/user/packages/container/knowfield/versions" \
  --jq ".[] | select(.metadata.container.tags[]? == \"$SHA\") | .name")
for i in $(seq 1 40); do
  kubectl -n knowfield get pod -l app.kubernetes.io/component=app \
    -o jsonpath='{range .items[*]}{.status.containerStatuses[0].imageID}{" ready="}{.status.containerStatuses[0].ready}{"\n"}{end}' \
    | grep "$WANT ready=true" && break
  sleep 6
done
```

迴圈跑完什麼都沒印 ＝ **沒出貨**。
⇒ 判準：**等待條件裡必須出現「我要的那個版本」**——
「有一個健康的東西在跑」在滾動更新期間永遠為真，它測不到你要問的事。

### 5.5 有加欄時：確認正式庫真的長出來了（⚠️ migration 是**懶跑**的）

`init_db`（含 `_ensure_columns`）在 **`Repository()` 被建出來時**才跑，不是行程啟動就跑。
`/healthz` 不建 repo ⇒ **部署完、pod ready、digest 對，正式庫的 schema 可能還是舊的**。

```bash
APP=$(kubectl -n knowfield get pod -l app.kubernetes.io/component=app -o jsonpath='{.items[0].metadata.name}')
kubectl -n knowfield exec $APP -- python -c "from knowfield.store.repository import Repository; Repository().close()"
kubectl -n knowfield exec knowfield-knowfield-postgres-0 -- bash -lc \
  'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT table_name||'"'"'.'"'"'||column_name FROM information_schema.columns WHERE table_name='"'"'<表>'"'"'"'
```

那行 `Repository()` 跟使用者下一個請求做的事**完全相同**（純加法 schema，不動資料）。
不跑它也會自己好——但**你就不知道它好了沒**，而 migration 失敗會發生在使用者的請求裡。

### 6. 收工

```bash
git log --oneline origin/main..HEAD | wc -l   # 應為 0
pkill -f "uvicorn knowfield.web.app"; pkill -f vite   # 本機開發伺服器（若有起）
```

## 權限

部署使用者已長期授權（2026-08-21 明講），可直接執行。
**授權涵蓋部署，不涵蓋**改正式環境設定、動 DB 資料、或設 `KNOWFIELD_AUTH_DISABLED`（那只給本機）。
若 helm 指令被工具層擋下，把完整指令交給使用者跑，不要改用繞過 helm 的方式。
