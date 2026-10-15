---
name: vacuumtube-live-cam-tile
description: "VacuumTube を無音の複数インスタンス（例: 4台, CDP :9993-:9996）で並行起動し、渋谷/新宿/池袋/秋葉原などの YouTube TV ライブカメラを個別表示して、4K画面の右下 Full HD 領域を 2x2 に分割した位置へ KWin で正確にタイル配置する。複数ライブカメラを常時モニタしたいときに使う。"
---

# vacuumtube-live-cam-tile Skill

複数の無音 `VacuumTube` を使って、YouTube TV のライブカメラを同時表示し、デスクトップ右下に見やすく並べるためのスキルです。

このスキルは以下を扱います。

- 無音 `VacuumTube` を複数台（既定例: 4台）起動
- 各インスタンスを CDP ポートで個別制御
- チャンネル `streams` からライブカメラタイルを高速選択
- 4K画面の右下 `1920x1080` 領域を `2x2` に分割して配置
- `wmctrl` が効かない場合の KWin Scripting フォールバック

## 前提

- 既存スキル `vacuumtube-silent-live-cam` が使える状態
  - `.codex/skills/vacuumtube-silent-live-cam/scripts/start_silent_instance.sh`
  - `.codex/skills/vacuumtube-silent-live-cam/scripts/open_tv_channel_live_tile_fast.js`
- `VacuumTube` メインインスタンス（`vacuumtube-bg`, `:9992`）は維持したまま運用する前提
- KDE Plasma + KWin (X11)
- `tmux`, `curl`, `jq`, `node`, `pactl`, `lsof`, `wmctrl`, `xdotool`, `qdbus`, `xdpyinfo`

## 重要ルール / 注意点

- **同一 `user-data-dir` を同時共有しない**
  - 無音側は `~/.config/VacuumTube` の複製プロファイルを使う
- **`verify-regex` は広すぎないようにする**
  - 例: TBS は `TBS NEWS DIG` だけだと別動画が誤一致する場合がある
  - `新宿駅前|Shinjuku` のように目的タイトル寄りにする
- **KWin タイル状態では `wmctrl` / `xdotool` が no-op になりやすい**
  - その場合は KWin Scripting で `client.frameGeometry` を直接設定する
- **`wmctrl -lG` のサイズはクライアント領域**
  - タイトルバー分（例: 上端 28px）を差し引いた値が表示されることがある
- **最終確認は目視が必要**
  - 4画面の UX / 見え方は自動テストだけでは担保できない

## 基本ワークフロー（4台）

1. 無音 `VacuumTube` を `:9993`〜`:9996` で起動
2. 各ポートにライブカメラを割り当て（渋谷/新宿/池袋/秋葉原など）
3. KWin で右下 FHD 領域 `2x2` に配置
4. URL / ミュート状態 / 位置を確認
5. オーナーに目視確認を依頼

## 1) 無音 VacuumTube を複数台起動

既存の `start_silent_instance.sh` をポート/セッション/instance-dir を変えて複数回使う。

```bash
# 1台目（既存運用例）
.codex/skills/vacuumtube-silent-live-cam/scripts/start_silent_instance.sh \
  --session vacuumtube-bg-2 \
  --port 9993 \
  --sink vacuumtube_silent \
  --instance-dir ~/.cache/yuiclaw/vacuumtube-multi/instance2

# 2台目
.codex/skills/vacuumtube-silent-live-cam/scripts/start_silent_instance.sh \
  --session vacuumtube-bg-3 \
  --port 9994 \
  --sink vacuumtube_silent \
  --instance-dir ~/.cache/yuiclaw/vacuumtube-multi/instance3

# 3台目
.codex/skills/vacuumtube-silent-live-cam/scripts/start_silent_instance.sh \
  --session vacuumtube-bg-4 \
  --port 9995 \
  --sink vacuumtube_silent \
  --instance-dir ~/.cache/yuiclaw/vacuumtube-multi/instance4

# 4台目
.codex/skills/vacuumtube-silent-live-cam/scripts/start_silent_instance.sh \
  --session vacuumtube-bg-5 \
  --port 9996 \
  --sink vacuumtube_silent \
  --instance-dir ~/.cache/yuiclaw/vacuumtube-multi/instance5
```

確認:

```bash
for p in 9993 9994 9995 9996; do
  curl -fsS "http://127.0.0.1:$p/json/version" | jq -r '.Browser'
done
pactl get-sink-mute vacuumtube_silent
```

期待値:

- 4ポートすべて `Chrome/...`
- `vacuumtube_silent` は `Mute: yes`

## 2) 各ポートにライブカメラを割り当て（例: 東京4地点）

`open_tv_channel_live_tile_fast.js` を各ポートへ実行する。
`#/browse?c=<channelId>` を使い、`verify-regex` は目的動画に寄せる。

### 渋谷（FNN）

```bash
node .codex/skills/vacuumtube-silent-live-cam/scripts/open_tv_channel_live_tile_fast.js \
  --cdp-port 9993 \
  --browse-url 'https://www.youtube.com/tv/@FNNnewsCH/streams#/browse?c=UCoQBJMzcwmXrRSHBFAlTsIw' \
  --keyword 'いまの渋谷' \
  --verify-regex '渋谷|スクランブル交差点|Shibuya|FNN'
```

### 新宿（TBS NEWS DIG）

```bash
node .codex/skills/vacuumtube-silent-live-cam/scripts/open_tv_channel_live_tile_fast.js \
  --cdp-port 9994 \
  --browse-url 'https://www.youtube.com/tv/@tbsnewsdig/streams#/browse?c=UC6AG81pAkf6Lbi_1VC5NmPA' \
  --keyword '新宿駅前のライブカメラ' \
  --verify-regex '新宿駅前|Shinjuku'
```

### 池袋（サンシャイン60通り）

```bash
node .codex/skills/vacuumtube-silent-live-cam/scripts/open_tv_channel_live_tile_fast.js \
  --cdp-port 9995 \
  --browse-url 'https://www.youtube.com/tv/@%E3%82%B5%E3%83%B3%E3%82%B7%E3%83%A3%E3%82%A4%E3%83%B360%E9%80%9A%E3%82%8A%E3%83%A9%E3%82%A4%E3%83%96%E3%82%AB%E3%83%A1%E3%83%A9/streams#/browse?c=UCEloGRn_GCcr-I_6f5MYJPw' \
  --keyword 'サンシャイン60通りライブカメラ' \
  --verify-regex 'サンシャイン60通り|池袋|Sunshine|ikebukuro'
```

### 秋葉原（Cerevo）

```bash
node .codex/skills/vacuumtube-silent-live-cam/scripts/open_tv_channel_live_tile_fast.js \
  --cdp-port 9996 \
  --browse-url 'https://www.youtube.com/tv/@Cerevolivecamera/streams#/browse?c=UCrGS8VyrgCqYwaogH5bQpxQ' \
  --keyword '秋葉原ライブカメラ' \
  --verify-regex '秋葉原|Akihabara|Cerevo'
```

## 3) 右下 Full HD 領域を 2x2 に分割して配置

### レイアウトの考え方

- 画面全体: `SCREEN_W x SCREEN_H` (4096 x 2160)
- タスクバー高さを引いた有効領域: `4096 x 2116`
- 右下領域の左上:
  - `baseX = 2048`
  - `baseY = 1058`
- 4分割セルサイズ:
  - `cellW = 1024`
  - `cellH = 529`

配置先（frame geometry）:

- 左上: `(baseX, baseY, 1024, 529)`
- 右上: `(baseX+1024, baseY, 1024, 529)`
- 左下: `(baseX, baseY+529, 1024, 529)`
- 右下: `(baseX+1024, baseY+529, 1024, 529)`

実測例（DCI 4K `4096x2160` - Taskbar 44px）:

- `baseX=2048`, `baseY=1058`

### KWin Scripting による確実配置（推奨）

`wmctrl` / `xdotool` が効かない場合でも、KWin の `client.frameGeometry` は通りやすい。
以下は `:9993-:9996` の PID を `lsof` で引き、4台を配置する一時スクリプト例。

```bash
export DISPLAY=:0
export XAUTHORITY="$HOME/.Xauthority"

PID_9993=$(lsof -nP -iTCP:9993 -sTCP:LISTEN -t | head -n1)
PID_9994=$(lsof -nP -iTCP:9994 -sTCP:LISTEN -t | head -n1)
PID_9995=$(lsof -nP -iTCP:9995 -sTCP:LISTEN -t | head -n1)
PID_9996=$(lsof -nP -iTCP:9996 -sTCP:LISTEN -t | head -n1)

cat > /tmp/codex_kwin_layout_4cams.js <<EOF
var baseX = 2048;
var baseY = 1058;
var cellW = 1024;
var cellH = 529;
var targets = [
  { pid: $PID_9993, x: baseX,         y: baseY,         w: cellW, h: cellH }, // Shibuya
  { pid: $PID_9994, x: baseX + cellW, y: baseY,         w: cellW, h: cellH }, // Shinjuku
  { pid: $PID_9995, x: baseX,         y: baseY + cellH, w: cellW, h: cellH }, // Ikebukuro
  { pid: $PID_9996, x: baseX + cellW, y: baseY + cellH, w: cellW, h: cellH }  // Akihabara
];
var clients = workspace.clientList();
for (var t = 0; t < targets.length; ++t) {
  var target = targets[t];
  for (var i = 0; i < clients.length; ++i) {
    var c = clients[i];
    if (c.pid !== target.pid) continue;
    try { c.fullScreen = false; } catch (e1) {}
    var g = c.frameGeometry;
    g.x = target.x; g.y = target.y; g.width = target.w; g.height = target.h;
    c.frameGeometry = g;
    break;
  }
}
EOF

PLUGIN=codex_kwin_layout_4cams
qdbus org.kde.KWin /Scripting org.kde.kwin.Scripting.loadScript /tmp/codex_kwin_layout_4cams.js "$PLUGIN" >/dev/null
qdbus org.kde.KWin /Scripting org.kde.kwin.Scripting.start >/dev/null
sleep 1
qdbus org.kde.KWin /Scripting org.kde.kwin.Scripting.unloadScript "$PLUGIN" >/dev/null || true
```

### `wmctrl` での確認

```bash
DISPLAY=:0 XAUTHORITY="$HOME/.Xauthority" wmctrl -lpG | rg 'VacuumTube'
```

注意:

- `wmctrl` はクライアント領域の高さを表示するため、タイトルバー分だけ `540` より小さく見える場合がある（例: `512`）
- 位置の `y` もタイトルバー分だけ `+28` されて見える場合がある

## 4) 一括確認コマンド

URL確認:

```bash
for p in 9993 9994 9995 9996; do
  printf '%s ' "$p"
  curl -fsS "http://127.0.0.1:$p/json" \
    | jq -r 'map(select(.type=="page" and (.url|contains("youtube.com/tv"))))[0].url'
done
```

ミュート確認:

```bash
pactl get-sink-mute vacuumtube_silent
```

期待値:

- 各ポートが目的の `#/watch?v=...` にいる
- `vacuumtube_silent` は `Mute: yes`

## 既知の東京4地点プリセット（実績）

- `:9993` 渋谷 / FNN / `dfVK7ld38Ys`
- `:9994` 新宿 / TBS NEWS DIG / `glJu8snzi78`
- `:9995` 池袋 / サンシャイン60通り / `TiDOEJxGtJI`
- `:9996` 秋葉原 / Cerevo / `Zq-D5z2n0EY`

## トラブルシュート

### TBS 新宿が別の TBS 動画に化ける

- `verify-regex` が広すぎる可能性が高い
- `新宿駅前|Shinjuku` のように絞る

### `wmctrl` / `xdotool` で位置が変わらない

- KWin タイル/制約で無視されている可能性が高い
- KWin Scripting（`workspace.clientList()` + `client.frameGeometry`）を使う

### TVチャンネルページが数秒で別状態に遷移する

- `open_tv_channel_live_tile_fast.js` を使う
- 手動遷移→手動選択はレースに負けやすい

### アカウント選択画面に落ちる（TBSで稀発）

- 既定フォーカスのアカウントに `Enter` で復帰できる場合がある
- 復帰後に再度 CDP で `#/watch?v=...` を指定する

## 手動確認（必須）

- 4台が右下 FHD 領域に `2x2` で収まっているか
- 各ウィンドウが意図した地域（渋谷/新宿/池袋/秋葉原）になっているか
- 音が出ていないか（`vacuumtube_silent`）

## 関連スキル

- `vacuumtube-silent-live-cam`（無音複数起動と TV ライブタイル選択の基盤）
- `desktop-windows-layout`（X11/KDE のウィンドウ配置・確認）
- `system-reboot-bringup`（再起動後の常駐群復旧）

