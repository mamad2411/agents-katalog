---
name: switch-qwen-model
description: 切換本機互斥的 Qwen 模型服務（Qwen 3.6 35B qwen-mtp :8001 ↔ Qwen 3.8 Flash Strata :8090），並同步修改 pi agent 的 defaultProvider/defaultModel 與 piscord（pi-discord-gateway）的 PI_MODEL。當使用者說 /switch-qwen-model、「切換 qwen 模型」、「切到 3.6」、「切到 3.8」、「換回 3.6」、「switch to 3.8 flash」或要求更換 pi／piscord 預設本地模型時使用。
---

# Switch Qwen Model (3.6 ↔ 3.8 Flash)

本機兩個 Qwen 引擎**互斥**（同時運行必定 OOM），切換時必須「停一個、開另一個」，
並同步更新 pi 與 piscord 的預設模型設定。

| 目標 | 服務 | Port | pi provider | pi model id | piscord `PI_MODEL` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **3.6** | `qwen-mtp.service`（system systemd） | 8001 | `local-llama` | `qwen3.6-35b-q4` | `local-llama/qwen3.6-35b-q4` |
| **3.8** | `strata.service`（**user** systemd） | 8090 | `local-strata` | `qwen3.8-flash` | `local-strata/qwen3.8-flash` |

## 操作方式

一律使用技能內腳本（具備健康檢查與 settings.json 自動備份）：

```bash
bash ~/.pi/agent/skills/switch-qwen-model/scripts/switch-qwen-model.sh 3.6     # 切到 Qwen 3.6
bash ~/.pi/agent/skills/switch-qwen-model/scripts/switch-qwen-model.sh 3.8     # 切到 Qwen 3.8 Flash (Strata)
bash ~/.pi/agent/skills/switch-qwen-model/scripts/switch-qwen-model.sh status  # 查看目前狀態
```

腳本流程：停止對方服務 → 啟動目標服務 → 等待 `/health`（最長 3 分鐘，Strata 載入需數十秒）
→ 備份並更新 `~/.pi/agent/settings.json` 的 `defaultProvider`/`defaultModel`
→ 備份並更新 `~/.config/pi-discord-gateway/config.env` 的 `PI_MODEL`，若 `pi-discord-gateway.service`
正在運行則 `systemctl --user restart` 讓新模型生效（未運行則下次啟動自動生效）。

3.8 的 health 判斷是 Strata `/health` 的 `"loaded": true`，不是只看 wrapper 有回應：
Strata 的 wrapper 在 engine 死掉（例如 exit -9）或被 unload 時仍會回 `/health` 200、
service 也仍是 active，只有下一個請求才會重新載入 engine（一兩分鐘，再加上冷的 prompt 讀取）。
腳本在 engine 沒載入時會呼叫 Strata 的 `POST /load` 先載好，切換完成時第一個請求就不會卡住。

**piweb 不需要重啟。** piweb worker 每次執行時都會重新讀 `~/.pi/agent/settings.json`
的預設模型：沒有指定模型的對話會用新的預設模型重新啟動 pi（`--model <預設>`），
不會沿用 pi session 檔裡存的舊模型；已經常駐的閒置 pi 程序也會在下一則訊息時自動換掉。
有手動選過模型（override）的對話則維持原本的選擇，若選的是已停止的那個本地模型，
需在該對話用模型選單改選。切換後不要跑 restart-piweb（會重建網頁容器，
把熱部署的前端檔案還原掉），也不要重啟 piweb-worker。

piscord 只有在 `PI_MODEL` 原本就是這兩個 Qwen 之一時才會跟著切；使用者另外指定的模型
（例如 2026-10-31 起的 `lfm3-rocm/lfm3-1.7b`）腳本會保留不動、也不重啟 gateway。

記憶體（2026-11-07 起 A3：`STRATA_COMPLEMENT_MAX_GIB=0`，Strata 從 ~70 GiB 降到 ~60 GiB，切換後 MemAvailable 約多 10 GiB；詳見 restart-service 的 Strata 專節；A3 寫在 `strata-iq3_s.json` 裡，切到 3.8 會自動套用，腳本切 3.8 和 `status` 都會印 `strata A3: on`，若 Strata 的 setup/update 把 `exe` 改回原版會印 WARNING）。以下為 A3 之前的紀錄：3.8 開好時（262K context + GPU 圖片 encoder，其他常駐服務照常跑）MemAvailable 只剩約 4 GB，
earlyoom 在 3 GB 會開始 SIGTERM 其他程式（strata 是 OOMScoreAdjust -500，不會先被砍）。
2026-10-31 開好兩分鐘內就掉到 2.4 GB，earlyoom 砍了 11 個 headless Chrome 分頁；停掉閒置的 `lfm3-xdna`
（`systemctl --user stop`，約 5 GB；earlyoom 不會砍 llama-server）後回到 7.5 GB。切 3.8 前先空出約 5 GB。

KV 快取（2026-11-07 起）：prefix-tree KV 快取**內建在 Strata 裡**（`serve/trie_kv.py`，drop-in `trie-front.conf` 的 ExecStart 帶 `--trie-kv`），
Strata 直接聽 **0.0.0.0:8090**。所有 client（pi/piweb/piscord 的 `local-strata` `http://localhost:8090/v1`、HayAegis 的 `host.docker.internal:8090`）
都會經過它，client 不用設定。舊的 `strata-trie-kv.service` proxy（:8090 → Strata :8089）已 **disabled**，`~/src/strata-trie-kv` 只留著回滾用
（步驟寫在 drop-in 註解）。決策 log 還是 `~/.cache/llama-slots/trie-kv.jsonl`；`python3 ~/src/Strata/serve/trie_kv.py --tree` 看樹。
namespace 改成看 engine 參數＋模型檔，改 env 或換 engine binary（例如 A3）不會再讓快取作廢。3.6（qwen-mtp, local-llama）沒有 KV manager。

注意：piscord 各頻道若有 per-channel session 記住的模型，切換後該頻道可能仍沿用舊模型，
需在該頻道用 `/model` 重選或開新 session。

## 規範

- **禁止** `kill`/`pkill`/`killall` 引擎 process（qwen-mtp 與 strata 均為受保護服務）；只能透過 `systemctl` / `systemctl --user` 操作。
- qwen-mtp 用 system systemd（`sudo systemctl`）；strata 用 user systemd（`systemctl --user`），不要混用。
- 若切換後 health check 逾時：3.8 查 `journalctl --user -u strata -n 50`（或 `/home/chihmin/src/Strata/strata-iq3_s.log`）；3.6 查 `journalctl -u qwen-mtp -n 50`。
- 第一個請求慢不代表 piweb 壞了：先跑 `status`，看 3.8 是否顯示 `engine loaded`。
- 若使用者只要查狀態不要切換，跑 `status` 即可，不要動服務。
- 3.8 的圖片：`status` 會顯示 `images: true|false`（Strata `/health` 的 `images`）；切到 3.8 時腳本會把 pi `models.json` 的 local-strata `input` 同步成 Strata 實際能力（有 encoder → `[text,image]`）。圖片要能用，`strata-iq3_s.json` 需同時有 `"vision"` 段落**和** engine args 的 `--vision`（缺後者會回 400 `this engine was started without --vision`）。
- 切換完成後向使用者回報：哪個服務 active、health 結果（3.8 要是 engine loaded，並附 images 狀態）、pi 預設模型新值、piscord PI_MODEL 新值與 gateway 是否已重啟。
