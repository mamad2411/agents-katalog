---
name: restart-service
description: 重啟、修復與健康檢查本機所有背景服務（包含 taigi、stock、fuji、piweb、power-monitor、webtop、ComfyUI、4get、qwen MTP、Strata、gemma、komorebi、claude-discord 與 xvfb streaming）。當使用者要求重啟服務或回報服務掛掉、連不上、502 時使用。
version: 1.5.5
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [systemd, docker, tailscale, funnel, restart, services, taigi, stock, fuji, power-monitor, piweb, webtop, 4get, qwen, strata, gemma, komorebi, claude, xvfb, streaming]
---

# Local Services Management & Restart Hub

當使用者要求重啟特定服務、切換模型服務、或回報服務斷線／502 時，直接執行對應的專屬重啟與驗證腳本：

---

## 🛠️ 服務重啟路由表 (Service Router)

| 服務項目 | 口語觸發詞 | 執行腳本 / 指令 | 驗證標準 |
| :--- | :--- | :--- | :--- |
| **Singing RMVPE** | `singing-rmvpe`、`歌唱 RMVPE` | `systemctl --user start singing-rmvpe.service` / `systemctl --user stop singing-rmvpe.service` / `systemctl --user restart singing-rmvpe.service` / `systemctl --user status singing-rmvpe.service` | 僅此 CPU unit；127.0.0.1:8791 `/singing/api/capabilities` protocol=rmvpe-pair-v1；合成音訊同源同意 POST、RuntimeDirectory 清空。禁止重啟 shared/GPU/Funnel 或修改既有 root；路由依 `/home/chihmin/singing-practice-web/RMVPE-DEPLOY.md` 單一路徑操作。 |
| **Taigi / Breeze ASR** | `重啟 taigi`、`台語掛了`、`翻譯連不上` | `bash ~/.hermes/skills/restart-service/scripts/restart-taigi.sh` | 重啟 Breeze supervisor + OmniVoice TTS + WebSocket 測試 |
| **HayAegis Stock** | `重啟 stock`、`重啟 assetsentry`、`股票掛了` | `bash ~/.hermes/skills/restart-service/scripts/restart-stock.sh` | 重建 FastAPI + React + Tailscale Funnel |
| **Fuji Camera** | `重啟 fuji`、`相機 app 掛了`、`底片相機` | `bash ~/.hermes/skills/restart-service/scripts/restart-fuji.sh` | 重啟 GPU gen + Docker stack + Tailscale HTTPS |
| **Power Monitor** | `重啟 power-monitor`、`電量監控`、`電費異常` | `bash ~/.hermes/skills/restart-service/scripts/restart-power-monitor.sh` | 重建 FastAPI 後端 + WebSocket 測試 |
| **Piweb** | `重啟 piweb`、`網頁版卡住`、`worker 沒回` | `bash ~/.hermes/skills/restart-service/scripts/restart-piweb.sh` | 依序重啟 gateway + worker + Docker web + Tailscale |
| **Piscord** | `重啟 piscord`、`Discord bot 掛了`、`pi-agent 沒回` | `bash ~/.hermes/skills/restart-service/scripts/restart-piscord.sh` | 檢查 user systemd、實際 entrypoint 與 Discord 連線完成日誌 |
| **Webtop AMD** | `重啟 webtop`、`桌面連不上` | `bash ~/.hermes/skills/restart-service/scripts/restart-webtop.sh` | 重啟 host backend + Docker frontend |
| **ComfyUI** | `重啟 comfyui`、`ComfyUI 掛了`、`8188 連不上` | `bash ~/.hermes/skills/restart-service/scripts/restart-comfyui.sh` | 重啟 user systemd unit 並檢查 `/system_stats` |
| **OmniParser** | `重啟 omniparser`、`OmniParser 掛了`、`8012 連不上` | `bash ~/.hermes/skills/restart-service/scripts/restart-omniparser.sh` | 重啟 CPU detector API 並檢查 `/health` |
| **Pi browser (nodriver worker)** | `browser 連不上`、`browser_intent 逾時`、`瀏覽器開不起來` | `systemctl --user stop "pi-nodriver-browser-*"` 然後 `python3 ~/.pi/agent/extensions/nodriver-browser/ops/browser-agent-watchdog.py check` | worker 會自己偵測卡死的 Chrome（頁面層探測）並重開；只有 worker 程序本身掛掉才需要這步。重啟會關掉所有瀏覽器分頁。舊的 laya-intent router 已停用（2026-11-04 改寫後 browser_intent 不再需要它）。 |
| **4get 搜尋代理** | `重啟 4get`、`搜尋代理壞了` | `docker restart 4get 2>/dev/null \|\| true` | 檢查 `http://localhost:8081` 返回 200 |
| **EmbeddingGemma 2 Q8_0 CPU 影音測試** | `embeddinggemma CPU Q8`、`CPU 5秒影音 benchmark` | `bash ~/.hermes/skills/restart-service/scripts/restart-embeddinggemma2-gguf-cpu.sh [start\|restart\|stop\|status]` | 獨立 CPU-only build，:8798；8 threads，main 與 mmproj 均禁 GPU；health ok 且 PID 無 GPU backend mapping。僅 source40–45秒，不動既有 GPU／Qwen／Strata。 |
| **EmbeddingGemma 2 llama.cpp Q4_0／Q8_0 hosts** | `embeddinggemma GGUF`、`量化影音 embedding host` | `bash ~/.hermes/skills/restart-service/scripts/restart-embeddinggemma2-gguf.sh [start\|restart\|stop\|status] [Q4_0\|Q8_0\|Q8_FLASH\|all]` | 僅操作 user `embeddinggemma2-gguf@Q4_0/Q8_0.service` 或測試專用 `embeddinggemma2-gguf-flash.service`；:8796/:8797（Flash :8799）`/health` status=ok，unit active；影音 `/v1/embeddings` 必須驗證 media ablation，禁止文字／字幕 fallback。不動 Qwen／Strata／PyTorch :8795 或 Tailscale。 |
| **EmbeddingGemma 2 GPU 固定 5 秒樣本** | `embeddinggemma2 GPU`、`影音向量常駐服務` | `bash ~/.hermes/skills/restart-service/scripts/restart-embeddinggemma2-gpu.sh [start\|restart\|stop\|status]` | 僅操作 user `embeddinggemma2-gpu.service`；:8795 `/health` ready/resident、GPU、PID 與 unit 一致。固定原影片 40–45s，非通用上傳 API；不動 CPU :8794、Qwen／Strata／其他 GPU 服务或 Tailscale。 |
| **Qwen MTP 模型** | `重啟 qwen`、`重啟 llama` | `sudo systemctl restart qwen-mtp` | 檢查 `http://localhost:8001/health` (自動載入 FlashHead Draft + 2 Slot np2 最佳化) |
| **Strata (Qwen3.8-Flash-Next)** | `啟動 strata`、`重啟 strata`、`切換 strata`、`enable strata` | 見下方「🚀 Strata (Qwen3.8-Flash-Next)」專節；**啟動前必須先停 qwen-mtp** | 檢查 `http://localhost:8090/health` 與 `/v1/models`（model_name `qwen3.8-flash`） |
| **Gemma 4 模型服務** | `啟動 gemma`、`重啟 gemma`、`切換 gemma` | `bash ~/.hermes/skills/restart-service/scripts/start-gemma.sh [e2b|12b|26b|31b|status]` | 檢查對應 port (8002/8004/8005/8003) `/health` |
| **Komorebi Voice + Gemma GPU／CPU／NPU dependencies + Breeze ASR** | `啟動 komorebi`、`重啟 komorebi`、`停用 komorebi`、`關閉 komorebi` | `bash ~/.hermes/skills/restart-service/scripts/restart-komorebi.sh [start\|restart\|stop\|status]` | CPU Gemma (`gemma-cpu.service`, :8031) 與 NPU Gemma (`flm-serve.service`, :52625) 均為整套服務依賴，與 GPU :8002、Breeze ASR :8025 一起啟停；檢查 app :8792 及所有後端，不可僅重啟 Docker |
| **Xvfb Streaming** | `重啟 xvfb streaming`、`重啟 xvfb stream`、`重啟 xvfb 串流`、`restart xvfb stream service`、`重啟 gemma streaming`、`串流監看掛了` | `bash ~/.hermes/skills/restart-service/scripts/restart-xvfb-streaming.sh [restart\|disable\|status]` | `restart` 更新 Xvfb 並重建 Docker/Funnel；`disable` 停止串流容器；`status` 顯示容器狀態與串流 API |
| **LINE (Wine/Bottles 桌面版)** | `重啟 line`、`line 掛了`、`LINE 要重新登入`、`line QR` | `bash ~/.hermes/skills/restart-service/scripts/restart-line.sh [start\|restart\|stop\|status]` | user units `line-xvfb.service`（Xvfb :121）+ `line-wine.service`（Restart=always）；退出碼 0=已登入、2=停在登入畫面（需 QR：`python3 -W ignore ~/line-wine-test/line_qr.py`）、1=未執行。QR 登入不會保留自動登入，restart 後通常要重掃；只停 Line 容器程序（以 WINEPREFIX 辨識），不動其他 Bottles 容器。程式在 `~/line-wine-test/` |
| **Claude Code (Discord)** | `重啟 claude`、`啟動 claude` | `bash ~/.hermes/skills/restart-service/scripts/restart-claude.sh` | 檢查 tmux session `claude-discord` 是否存活 |
| **Tailscale Funnel** | `funnel 掛了`、`沒開 VPN 連不上`、`外面連不進來` | `bash ~/.hermes/skills/restart-service/scripts/restart-funnel.sh [status\|<節點>...]` | 從 3 個公開 DNS resolver 驗證紀錄存在，缺的自動重啟該 sidecar |

---

## 🎙️ Komorebi Voice 主控服務與後端連動 (Komorebi Master Service)

- **主控服務**：`komorebi.service`（系統級 systemd unit）
  - 管理 Docker 容器 stack（`komorebi-app` 網頁服務 :8792 + `komorebi-ts` 私有 Tailscale HTTPS Serve）。
  - **依賴清單**：`gemma-mtp.service`（GPU）、`gemma-cpu.service`（CPU Gemma）、`flm-serve.service`（NPU Gemma）、`breeze-asr.service` 與 `breeze-asr.socket`。
  - 現有 `/etc/systemd/system/komorebi.service` 使用 `Wants=` 加入依賴，並由 `ExecStartPre=systemctl start ...` 在啟動 Docker stack 前拉起所有依賴；不是 `Requires=`，也不代表模型 API 已完成載入。
  - 停止主控時，`ExecStopPost=systemctl stop ...` 停止上述依賴；模型 units 的 `PartOf=komorebi.service` 連動停止／重啟。CPU／NPU 即使先前因省 RAM 被停止，整套 start／restart 仍會重新拉起。
  - 預設全套模式不可省略 CPU／NPU dependencies，也不可只重啟 `komorebi-app` 而忽略模型服務。使用者明確要求 NPU-only 時，改用下述獨立暫時 profile，不啟動 GPU／CPU／Breeze。
- **後端硬體與語音服務**：
  - **GPU 模型後端**：`gemma-mtp.service`（ROCm 7.2.2 llama-server，port 8002，alias `gemma-4-e2b-qat-q4-mtp`）
  - **CPU Gemma dependency**：`gemma-cpu.service`（目前 E4B Q4_K_M，CPU-only llama.cpp 16-thread，port 8031，alias `gemma-4-e4b-cpu`；`--gpu-layers 0 --no-mmproj-offload`，CPU unit 隱藏 GPU 裝置）。`/etc/systemd/system/gemma-cpu.service.d/model-e4b.conf` 將 ExecStart 改為 `/home/chihmin/bin/start-gemma4-e4b-cpu.sh`；獨立 GGUF 與 F16 projector 位於 `/home/chihmin/models/gemma-4-e4b/`。保留原 E2B base unit／launcher，若使用者要求回 E2B，僅移除此 model drop-in、daemon-reload 後 restart CPU unit。正式網頁已用獨立 UI-only 映像修補 E4B 選項／路由標籤／頂部 badge，`komorebi-voice:pre-cpu-e4b-labels` 保留原映像。既有 server 仍可能傳入舊 alias，應以 CPU `/v1/models` 與實際 process model path 判定；不得部署未驗證 working tree。回 E2B 時需同步更新 UI 標籤或回原 UI 映像。
  - **NPU Gemma dependency**：`flm-serve.service`（FastFlowLM XDNA2，port 52625，model `gemma4-it:e4b`；配置 `LimitMEMLOCK=infinity`）
  - **ASR 語音辨識**：`breeze-asr.service` / `breeze-asr.socket`（Breeze-ASR-26 on ROCm GPU，port 8025，支援 socket activation 與閒置 60s 自動釋放顯存）
- **無 Fallback 原生執行原則**：
  - 前後端均已移除靜默 fallback，切換至指定後端（GPU/CPU/NPU）即由該硬體原生處理，錯誤時直接明確回傳。
- **常用操作**：
  - 重啟／啟動：`bash ~/.hermes/skills/restart-service/scripts/restart-komorebi.sh [start|restart]`
  - 關閉全套服務：`bash ~/.hermes/skills/restart-service/scripts/restart-komorebi.sh stop`
  - 檢查全套狀態：`bash ~/.hermes/skills/restart-service/scripts/restart-komorebi.sh status`
  - 僅更新已獨立驗證的正式 UI 映像：確認原 compose 配置未變、預期模型服務仍健康後，將驗證映像 tag 為 `komorebi-voice:local`，再 `bash ~/.hermes/skills/restart-service/scripts/restart-komorebi.sh reload-app`。此命令要求主控已 active，自動保留 NPU profile，使用 `up -d --no-build --no-deps app`；不重啟模型或 Tailscale、不重建 working tree、不修改私人資料，也不替代整套 startup／repair 的依賴驗證。
  - 使用者只要求額外開 CPU／切 CPU 模型時：`sudo -n systemctl start gemma-cpu.service`／`sudo -n systemctl restart gemma-cpu.service`，等待 :8031 `/health` 並測 Komorebi 明確 backend=cpu 的推論；不要啟動全套主控、GPU 或 Breeze，也不要停止既有 NPU。單獨加開的 CPU 仍屬獨立 unit，NPU-only 主控停止不會自動停止它。
- **明確指定 NPU-only（暫時 profile）**：
  - 使用 hub 內 `scripts/komorebi-npu.service`，安裝至 `/run/systemd/system/komorebi-npu.service`（先確認沒有其他同名 unit，再 `sudo -n install -m644 <模板> <目的地>` 與 `sudo -n systemctl daemon-reload`）。不覆寫 `/etc/systemd/system/komorebi.service`，不 enable；重開機後此 runtime unit 不保留。
  - 啟動：`KOMOREBI_UNIT=komorebi-npu.service bash ~/.hermes/skills/restart-service/scripts/restart-komorebi.sh start`。
  - 此 profile 只依賴 Docker 與 `flm-serve.service`；與全套 `komorebi.service` 互斥。使用 `scripts/komorebi-npu-only.compose.yaml` 將 app 預設設為 NPU，`up --no-build` 沿用正式映像，禁止將未驗證 working tree 重建部署。
  - GPU Gemma、CPU Gemma、Breeze service/socket 必須保持 inactive；若為其他服務共用且正在使用，先告知使用者，不可擅自停止共用服務。不得觸碰 Qwen／Strata。
  - `stop`／`status` 未提供 `KOMOREBI_UNIT` 時會自動辨識 active NPU profile；一般 `start`／`restart` 仍選全套主控。指定 unit 僅允許 `komorebi.service` 或 `komorebi-npu.service`。
  - NPU profile 啟動需 app `/api/config` 與 NPU `/v1/models` 同時成功；再確認 default_backend=npu、實際 NPU 推論完成及其餘後端 inactive。現有瀏覽器偏好仍可能選 CPU／GPU，應切回 NPU；不新增 fallback。
- **依賴驗證**：
  - GPU :8002 與 CPU :8031 檢查 `/health`；NPU :52625 檢查 `/v1/models`；Breeze :8025 檢查 `/health` 並辨識 socket activation 狀態；app :8792 檢查 `/api/config`。
  - 預設全套 start／restart 以 app readiness 決定退出碼，再輸出所有後端狀態；退出碼 0 或 app healthy **不等於所有模型都 healthy**。CPU／NPU unavailable 時應明確回報，不可宣稱整套成功或靜默 fallback。明確 NPU-only 時，CPU／GPU／Breeze down 是預期狀態，不是要自動修復／拉起的故障。
  - 僅更新此 skill 的依賴說明不需要執行 restart、stop 或 daemon-reload；實際啟停需依使用者要求操作。

---

## 🧠 模型引擎被 OOM 殺掉（earlyoom / exit code -15）

本機是 128 GB RAM、**原本 0 swap** 的 Strix Halo 機器；GPU VRAM 由系統 RAM 劃走
（Strata 常駐 ~58 GB、ComfyUI ~6 GB、gemma GPU ~5 GB），記憶體一吃緊 earlyoom
就會 SIGTERM 掉正在服務中的引擎，Discord/piweb 會看到
`the engine stopped unexpectedly (exit code -15); the next request restarts it`。

- **判定**：`journalctl --since "-6h" | grep earlyoom`（看 `sending SIGTERM to ... "strata"`）
  ＋ `free -m`（MemAvailable < 3 GiB 就是危險區）＋ `rocm-smi --showpids`（誰吃掉 VRAM）。
- **已裝的防護（2026-10-06）**：
  - `/swapfile` 16 G（fstab `sw,pri=10`）＋ `/etc/sysctl.d/99-llm-swap.conf` `vm.swappiness=1`；
    earlyoom 有可用 swap 時不會再亂殺。
  - `~/.config/systemd/user/strata.service.d/oom.conf` → `OOMScoreAdjust=-500`（引擎變最後犧牲者）。
  - `/etc/default/earlyoom` 已 `--ignore '^llama-server$'`（qwen MTP 永不當victim）。
- **省 RAM 順序**（要空間時先動這些，都還留 GPU 語音後端 :8002）：
  `sudo systemctl stop flm-serve.service`（NPU，~9 GB）→
  `sudo systemctl stop gemma-cpu.service`（CPU，~2 GB）→
  清 `tmux ls` 裡過期的 `piweb-cc-*` Claude Code 殘留 session（每個 ~300 MB）。
  注意：重啟 `komorebi.service` 會把 CPU/NPU 後端全部拉回來（再吃 ~11 GB）。
- `qwen-mtp.service`（:8001）與 `strata.service`（:8090）**互斥**，同時開必定 OOM。

---

## 🚀 Strata (Qwen3.8-Flash-Next) 服務管理

- **Unit**：`strata.service`（**user** systemd，`~/.config/systemd/user/strata.service`），`ExecStart=%h/src/Strata/run-iq3_s.sh` → `.venv/bin/python serve/server.py --engine strata --config strata-iq3_s.json --port 8090`。
- **Enable（開機自啟）**：`systemctl --user enable strata.service`（目前為 disabled；enable 後搭配既有 `Restart=on-failure` 與 drop-in `strata.service.d/oom.conf` 的 `OOMScoreAdjust=-500`）。
- **啟動 / 重啟 / 停止 / 狀態**：
  ```bash
  sudo systemctl stop qwen-mtp            # ⚠️ 必要前置：qwen-mtp (:8001) 與 strata (:8090) 互斥，同時開必定 OOM
  systemctl --user start strata.service   # 或 restart / stop / status
  ```
- **A3 記憶體設定（2026-11-07 起）**：config `exe` 指向 `engine/strata-cap-d549940e`（`~/src/Strata-cap` branch `perf/complement-cap` 編的，多了 `STRATA_COMPLEMENT_MAX_GIB`），env `STRATA_COMPLEMENT_MAX_GIB=0` 拿掉 prompt path 那份 9.81 GiB 的 RAM 重複副本（改從 `experts.bin` 走 page cache）；A/B 實測 decode/prefill 無差、輸出 token 相同，MemAvailable +~10 GiB（報告 `/tmp/strata-offload-ab/REPORT.md`）。log 應見 `0 of the prompt path's 5141 lendable slots keep`。回滾：`cp strata-iq3_s.json.bak-pre-a3-20261107 strata-iq3_s.json` 後 `systemctl --user restart strata.service`。不要改用 `STRATA_RESIDENT_HEADROOM_GIB=1000` 代替（GPU 放不下全部 expert 時會退成純 mmap，變慢）。**Strata 的 `setup.sh`/`update.sh` 會重寫這份 config：env 會保留，但 `exe` 會被改回原版 `engine/strata`（不認這個 env）→ 默默回到 ~70 GiB**；跑完後用 `switch-qwen-model.sh status` 看 `strata A3: on`，off 就把 `exe` 指回 cap engine（或用新版 source 重編 cap patch）再重啟。
- **啟動時間**：載入需數十秒（expert cache 填充 24,576 experts / ~47 GiB VRAM；A3 後不再建 RAM 副本），log 在 `/home/chihmin/src/Strata/strata-iq3_s.log`，看到 `strata serve:` 開始收 request 才算 ready。
- **驗證**：`curl http://localhost:8090/health` ＋ `curl http://localhost:8090/v1/models`（應回 `qwen3.8-flash`）；OpenAI 相容 API 在 :8090。
- **切回 qwen-mtp**：`systemctl --user stop strata.service && sudo systemctl start qwen-mtp`。
- **Config 變體**（同目錄，改 `run-iq3_s.sh` 的 `--config` 即可切換）：`strata-iq3_s-base.json`（無 perf flags 對照組）、`strata-iq3_s-pfonly.json`、`strata-iq3_s-fast16k.json`、`strata-iq3_s-fastauto32k.json`（+ `--lookup-chain 3 --mtp-q4 all`）、`strata-unsloth-ud-iq4_xs.json`（UD-IQ4_XS，128k ctx，無 control vector）。
- **禁止**對 engine process 直接 `kill`/`pkill`（受保護服務）；一律透過 `systemctl --user` 操作。

---

## ⚠️ 重要規範
- 所有重啟腳本均具備冪等性（Idempotent），會自動完成服務重建與端對端 HTTP/WebSocket 健康檢查。
- 嚴禁未經腳本直接 `pkill python`，以免破壞正在運行的相依服務。

---

## 🌐 Tailscale Funnel 靜默失效

sidecar 可能本機顯示 `Funnel on`、`IngressEnabled=true`、憑證有效，但 control plane
其實已經把公開 DNS 紀錄撤掉了 —— 結果就是「有 VPN 正常、沒 VPN 完全連不上」，而且
**節點自己偵測不到**，因為失效發生在 control plane 那一側。

- 唯一可信的檢查是從外部查公開 DNS：`dig +short A <node>.crayfish-monitor.ts.net @8.8.8.8`
- **不要只查一個 resolver**：ts.net 的 SOA 有 300 秒 negative cache，剛修好的名字在
  曾經查過的 resolver 上還會 NXDOMAIN 好幾分鐘。`restart-funnel.sh` 用 3 個 resolver 取多數決。
- 驗證公網可達要用 `curl --resolve <fqdn>:443:<ingress-ip>`，直接 curl FQDN 會走 tailnet 不算數。
- 重啟 sidecar 容器對 app 一律安全（app 不會被動到）；反過來則不行 —— 重建
  `network_mode: container:<app>` 的 app 會炸掉 sidecar 的 network namespace（piweb 的老陷阱）。
- 重啟修不好時，通常不是這個故障模式，要另外查 tailnet ACL 的 `funnel` node attribute。
