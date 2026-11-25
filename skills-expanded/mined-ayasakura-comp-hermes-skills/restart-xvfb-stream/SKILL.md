---
name: restart-xvfb-stream
description: 重啟、管理與健康檢查本機 Xvfb 即時螢幕串流與錄影服務（Xvfb Streaming）。當使用者要求「重啟 xvfb streaming」、「重啟 xvfb stream」、「重啟 xvfb 串流」、「restart xvfb stream service」、「重啟 gemma streaming」、「串流監看掛了」、Tailscale Funnel 502、或指令 /restart-xvfb-stream 時使用。會自動偵測 nodriver-browser 運行的 Xvfb DISPLAY 與 XAUTHORITY，重建 Docker 容器與 Tailscale sidecar，並驗證端對端串流健康狀態。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [xvfb, streaming, mjpeg, ffmpeg, docker, tailscale, funnel, restart]
---

# Restart Xvfb Stream Service

當本機 Xvfb 螢幕畫面串流服務需要重啟、修復連線、更新 DISPLAY，或使用者提出以下需求時使用：
- 口語觸發詞：`重啟 xvfb streaming`、`重啟 xvfb stream`、`重啟 xvfb 串流`、`restart xvfb stream service`、`重啟 gemma streaming`、`串流監看掛了`、`串流黑畫面`
- 快捷指令：`/restart-xvfb-stream`

---

## ⚡ 快速執行

### 1. 標準重啟（更新 Xvfb 並重建 Docker 與 Funnel）
```bash
bash ~/.hermes/skills/restart-xvfb-stream/scripts/restart.sh
# 或
bash ~/.hermes/skills/restart-service/scripts/restart-xvfb-streaming.sh
```

### 2. 檢查狀態
```bash
bash ~/.hermes/skills/restart-xvfb-stream/scripts/restart.sh status
```

### 3. 停止服務
```bash
bash ~/.hermes/skills/restart-xvfb-stream/scripts/restart.sh disable
```

---

## 🏗️ 服務架構

| 組件 | 說明 | 管理方式 |
| :--- | :--- | :--- |
| **Xvfb 虛擬桌面** | 瀏覽器背景工作者運行的 X11 display (如 `:100`) | nodriver-browser (`/home/chihmin/.pi/agent/extensions/nodriver-browser/`) |
| **Xvfb Streaming 後端** | FastAPI + FFmpeg (`x11grab` + `image2pipe` MJPEG) | Docker service `xvfb-streaming` (`/home/chihmin/src/xvfb-streaming/`) |
| **Tailscale Funnel** | 公開 HTTPS 串流端點與 Webhook 轉發 | Docker service `xvfb-stream-ts` (共享 `xvfb-streaming` network namespace) |

- **公開端點**：`https://xvfb-streaming.crayfish-monitor.ts.net/` (相容舊域名 `https://gemma-stream.crayfish-monitor.ts.net/`)
- **內部連接埠**：`127.0.0.1:8771` (Docker 內部) / `0.0.0.0:8765` (本機 systemd 模式)

---

## 🔍 重啟腳本執行流程

1. **偵測目前運行中的 nodriver-browser 工作程序**：
   自動取得工作程序的 `DISPLAY` 與 `XAUTHORITY` 路徑，避免手動指定錯誤的 display 編號。
2. **同步認證 Cookie**：
   更新專案 `.env` 中的 `DISPLAY_NUMBER`，容器內自動偵測並同步 `/host-tmp/xvfb-run.*/Xauthority`。
3. **重建與啟動容器**：
   執行 `docker compose build xvfb-streaming` 與 `docker compose up -d`。
4. **端對端健康驗證**：
   輪詢驗證容器 healthy 狀態、Tailscale 連線狀態以及 HTTP `/api/status` 取得有效畫面幀 (`state=live`)。

---

## 📡 HTTP & WebSocket API 參考

- `GET /` — 視覺化串流儀表板 (含畫面預覽、解析度／速率調整、遙測、MP4 錄影按鈕)
- `GET /api/health` — 程序健康檢查 (`{"status": "ok", "state": "live"}`)
- `GET /api/status` — 即時狀態與串流幀數統計 (`frame_id`, `capture_fps`, `viewers`)
- `GET /api/frame.jpg` — 最新單張 JPEG 快照
- `GET /stream.mjpg` — 即時 Multipart MJPEG 串流
- `WS /ws` — 即時 WebSocket 遙測廣播
- `POST /api/recording/start` & `POST /api/recording/stop` — MP4 錄影控制
