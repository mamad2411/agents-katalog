# TrafficLab AI 指示文件

本檔案是給在這個 repository 裡工作的 AI coding agent 看的操作細節；README 保持面向使用者、簡潔扼要。

## 工作原則

除非明確override，否則這些規則適用於此專案中的每一項任務。
原則：在非小事的工作上，謹慎優先於速度。小事則依判斷行事。

### 規則 1 — 動手前先思考
明確說明假設。若不確定，應提問而非用猜的。
當存在歧義時，提出多種可能的解讀。
若有更簡單的做法，應提出來討論。
感到困惑時就停下來，並具體指出不清楚的地方。

### 規則 2 — 遵循該程式碼庫的慣例，即使你不認同
在程式碼庫裡，「一致性」優先於「個人品味」。
如果你真心認為某個慣例有害，就提出來討論，不要私自另起爐灶。

### 規則 3 — 手術式修改
只動你必須動的地方。只清理自己造成的髒亂。
不要「順便改善」旁邊的程式碼、註解或格式。
不要重構沒壞的東西。match現有的風格。

### 規則 4 — 以目標為導向的執行
先定義成功標準，反覆執行直到驗證通過。
不要只是照步驟做，要定義「成功」是什麼並反覆迭代。
明確的成功標準能讓你獨立地反覆執行。

### 規則 5 — 出問題要大聲說出來
如果任何東西被悄悄跳過，那「已完成」這個說法就是錯的。
如果任何測試被跳過，那「測試通過」這個說法就是錯的。
預設要主動揭露不確定性，而不是隱藏它。

### 規則 6 — 只在需要判斷力時才用到我（模型）
可以用我做：分類、草擬、摘要、擷取資訊。
不要用我做：routing、重試、確定性的轉換。
如果程式碼能處理，就交給程式碼處理。

### 規則 7 — 衝突要攤開來講，不要折衷處理它們或混合使用
若兩種模式互相矛盾，選一個（較新的／較經過驗證的）。
說明理由，並標記另一個待清理。
不要把互相衝突的模式混在一起用。

### 規則 8 — 先讀再寫
在新增程式碼之前，先讀過相關的 exports、直接呼叫方、共用的 utilities。
「看起來無關」是很危險的想法。若不確定程式碼為何這樣設計，就提問。

### 規則 9 — 測試要驗證意圖，不只是驗證行為
測試必須表達出「為什麼這個行為重要」，不能只是「做了什麼」。
如果商業邏輯改變了，測試卻不會失敗，那這個測試就是錯的。

### 規則 10 — 每完成一個重要步驟就checkpoint一次
摘要已完成的事、已驗證的事，以及還剩下什麼。
不要從一個你無法複述清楚的狀態繼續做下去。
如果你失去脈絡，就停下來重新整理狀態。

## Repository 用途

本專案把車禍影片重建成地圖上的 2D 行車軌跡。以資深貢獻者的標準工作：精準、有效率、重視可維護性與清晰度。

## Repository 結構

```text
TrafficLab-3D/
├── main.py                     # GUI 進入點
├── trafficlab/
│   ├── gui/                    # PyQt5 GUI 實作
│   ├── inference/               # GUI 與 CLI 共用的推論 pipeline
│   ├── projection/              # G-projection 與 SVG projection 的輔助工具
│   ├── visualization/           # replay 載入與渲染
│   ├── io/                      # replay/config I/O 輔助工具
│   ├── motion/                  # 運動學（kinematics）工具
│   └── trajectory/              # 推論後的軌跡靜態繪圖工具
├── scripts/                     # CLI 輔助工具與維護用工具
├── location/<location_code>/    # 校正資產、衛星／CCTV 影像、投影檔案與影片素材
├── output/                      # 產生出來的 model/tracker/config/location replay 輸出結果
└── models/                      # 本地端的 detector/tracker checkpoint
```

- h-aware / OpenPifPaf：邏輯在 `trafficlab/motion/keypoints_openpifpaf.py`，CLI 入口在 `scripts/run_keypoints_openpifpaf.py`。

## 指令規則

- 所有 Python 指令都要先啟動 `trafficlab` conda 環境、並從 repository root 執行：

```bash
source /opt/anaconda3/bin/activate trafficlab
```

- 優先直接啟動環境，不要用 `conda run -n trafficlab ...`（sandbox 裡可能因暫存檔寫入權限失敗，除非直接啟動行不通才用）。
- 從 repo root 執行時 `import trafficlab` 會正常解析；若指令必須在 repo root 以外執行，設定 `PYTHONPATH=<repo_root>`（例如 `PYTHONPATH=$(pwd)`，在 repo root 下執行時）。`scripts/run_inference.py` 是例外，即使在 repo root 也不會自動加進 `sys.path`，一律要明確帶 `PYTHONPATH`（見下方「YOLO 框定位」）。
- 只有跑 YOLO 模型時，才需要在 Apple Silicon 上加 `PYTORCH_ENABLE_MPS_FALLBACK=1`（GUI 若可能牽涉到推論也算）；`device: mps` 時不要假設 `half: true` 一定安全。
- 不要依賴系統的 `python` binary；缺 dependency 時先確認 `trafficlab` 環境已啟動再下結論。

## 常用指令

### 1. 開啟 GUI

```bash
source /opt/anaconda3/bin/activate trafficlab && PYTORCH_ENABLE_MPS_FALLBACK=1 python main.py
```

### 2. YOLO 框定位

透過 `scripts/run_inference.py`（`trafficlab.inference.pipeline.InferencePipeline`）執行 YOLO 偵測＋追蹤＋bbox 投影，是 TrafficLab 原生的定位方法，不使用關鍵點。這是兩種定位方法之一（另一種是下方的「keypoints-openpifpaf」）— 依情境挑選合適的方法，不要把它當成預設要跑的方法。

```bash
source /opt/anaconda3/bin/activate trafficlab && PYTHONPATH=$(pwd) PYTORCH_ENABLE_MPS_FALLBACK=1 python scripts/run_inference.py --config-name <config_name> <selector>
```

- `--all-pending`：處理所有待處理影片
- `--location <location_code>`：處理單一 location
- `--mp4 <video_path>`：處理單一 mp4
- 加 `--force`：即使輸出已存在也強制重跑
- `<config_name>`：YAML（預設 `inference_config.yaml`，可用 `--config-path` 換）裡定義的 config key，不填則用檔案裡第一個 config

Config 的 `model` 區塊預設是偵測模型（regression box 直接拿去投影）。設定 `model.type: "seg"` 可以改用 segmentation checkpoint（如 `models/yolo11m-seg.pt`）：box 來源改成從分割 mask 的最大 contour 算出的 tight box，其餘流程（追蹤、投影、kinematics）不變。seg 模式下 `model.classes` 為必填，是 COCO 類別名稱 → 專案內部類別名稱的對照表（例如 `{car: car, motorcycle: two_wheeler}`）；分割模型偵測到的每個物件都會算 tight box，但只有在這張表裡的類別會被定位、寫進輸出，其餘（如 `person`）算完 box 後就跳過。seg 模式的輸出固定寫到 `output/yolobox-seg/model-<model_name>_<tracker_type>/<config_name>/<location_code>/`，忽略一般模式用的 `output/` 輸出根目錄。

Config 可加 `projection` 區塊來覆寫接地點推算方式：`projection.ref_method`（`center_bottom_side` / `center_box`）與 `projection.proj_method`（`down_h` 全車高視差修正 / `down_h_2` 半車高 / 其他值一律不修正，慣例寫 `match`）。解析順序是 config `projection` → G_projection JSON 的同名欄位 → 內建預設（`center_bottom_side` / `down_h`），實際採用值會印在 log。用途：同一份 `G_projection_<code>.json` 可讓不同 config 走不同投影行為 —— 例如 seg tight-box 的底邊已接近接地面，適合設 `proj_method: match` 避免對已接地的點再套 `down_h` 重複修正。

### 3. keypoints-openpifpaf

在每一幀上執行 OpenPifPaf Apollo-24 偵測，並透過 height-aware 關鍵點模板比對來定位每輛車。輸出是標準的 TrafficLab replay JSON，可以在 GUI 中載入（衛星座標位置、車頭朝向、車輛外框，以及 CCTV 關鍵點疊圖）。`--method` 是必填參數，用來選擇兩種互斥的逐幀策略之一 — 只有被選中策略自己的 flag 才會生效。

```bash
source /opt/anaconda3/bin/activate trafficlab && \
PYTORCH_ENABLE_MPS_FALLBACK=1 python scripts/run_keypoints_openpifpaf.py \
  --video <video_path> \
  --g-proj <g_proj_path> \
  --method <geometric|segmentation>
```

輸出：`output/haware/<location_code>/<video_stem>.json.gz` — 但 `--localizer wheel_pair` 例外，會寫到 `output/wheel_pair/<location_code>/<video_stem>.json.gz`（獨立資料夾，避免跟同一支影片的 `procrustes`/`reprojection` 輸出互相覆蓋）。

`--method` 選項：

| Method | 何時選它 | 相關 flag |
|--------|---------------|-----------------|
| `geometric` | 沒有明顯 PifPaf instance-splitting 時，用 bbox IoU 把關鍵點對到 YOLO track id | `--yolo` / `--yolo-conf` / `--yolo-classes` / `--iou-threshold` / `--yolo-boxes-json` / `--yolo-boxes-class` |
| `segmentation` | PifPaf 把同一台車拆成兩塊多關鍵點碎片、`geometric` 修不了時用 — 詳見 `docs/keypoints-openpifpaf-segmentation-matching.md` | `--seg-model` / `--seg-conf` / `--seg-device` |

例外：搭配 `--localizer wheel_pair` 時，`--method` 一律用 `segmentation`（不分機器）—— 實測 segmentation 的關鍵點比對在 wheel_pair 下結果最好。若同一支影片已有 `record_car_masks.py` 的輸出，帶 `--seg-masks-json` 重用它，不必再跑一次 car-segmenter。

共用選項：

| Flag | 預設值 | 說明 |
|------|---------|-------|
| `--checkpoint` | `models/shufflenetv2k16-apollo-24.pkl`（不存在時退回名稱 `shufflenetv2k16-apollo-24`，由 openpifpaf 從 torch.hub 下載到 `~/.cache/torch`） | PifPaf model |
| `--cad-template` | `--localizer wheel_pair` 時預設為已入庫的 `cad_models/nissan_juke_nismo/keypoint_template_nissan_juke_nismo.json`（帶真實輪轂高度）；其他 localizer 為 *(無)* | 指向 `scripts/build_cad_keypoint_template.py` 產出的車型專屬 24 點模板 JSON；設定時直接套用這個模板，取代 `build_car_template(dims)`，`prior_dimensions.json` 會被忽略。載入時會檢查模板的 `kp_names` 是否跟目前的 `KP_NAMES` 順序一致，不一致就報錯要求重新產生 — 完整流程見 `docs/cad-keypoint-template-pipeline.md`。要在 wheel_pair 下改回 `build_car_template`，明確傳 `--cad-template ""` |
| `--kp-conf` | `0.2` | 關鍵點信心度閾值 |
| `--frames` | `-1`（全部） | 限制幀數以便快速測試 |
| `--start-frame` | `0` | 開始處理的第一幀；在此之前的幀會被讀取後丟棄，而不是用 seek |
| `--localizer` | `procrustes` | `procrustes`（closed-form 擬合，一般情況）、`reprojection`（非線性最小平方，對 PifPaf 像素位置擬合），或 `wheel_pair`（只用同側前後輪關鍵點，適合僅輪胎清楚可見時；會把 `--cad-template` 預設為 nissan_juke_nismo 模板 —— 見上 — 詳見 `docs/keypoints-openpifpaf-wheel-pair-localizer.md`） |
| `--out` | 自動 | 覆寫輸出路徑 |

`--method geometric` 選項：

| Flag | 預設值 | 說明 |
|------|---------|-------|
| `--yolo` | `models/best.pt` | 用於 track-ID 比對的 YOLO model（ByteTrack）；傳入 `--yolo ""` 可停用並讓 `tracked_id=None` |
| `--yolo-conf` | `0.25` | YOLO 偵測信心度閾值 |
| `--yolo-classes` | *(全部)* | 要保留的 YOLO class index，以逗號分隔 — 依 model 而異，請檢查 `--yolo` 所指 model 的 `.names` |
| `--iou-threshold` | `0.3` | 接受 PifPaf↔YOLO 比對所需的最小 bbox IoU |
| `--yolo-boxes-json` | *(無)* | 使用預先算好的 replay JSON（例如 `pipeline.py` 的輸出）作為 YOLO box 來源，而不是即時跑 model；設定時優先於 `--yolo` |
| `--yolo-boxes-class` | `car` | `--yolo-boxes-json` 中要視為汽車的 `class` 值 |

`--method segmentation` 選項：

| Flag | 預設值 | 說明 |
|------|---------|-------|
| `--seg-model` | `models/yolo11m-seg.pt` | car-segmenter 用的 Ultralytics `*-seg` checkpoint；若本地端沒有，首次使用時會自動下載到該路徑 |
| `--seg-conf` | `0.3` | car-segmenter 偵測信心度閾值 |
| `--seg-device` | *(自動)* | `cuda` / `mps` / `cpu`，或不設定讓 ultralytics 自行選擇 |
| `--seg-masks-json` | *(無)* | 指向 `record_car_masks.py` 輸出檔案的路徑，提供逐幀的汽車 instance（tracker_id/bbox/mask polygon），用它取代即時執行 car-segmenter。設定此參數時，`--seg-model`/`--seg-conf`/`--seg-device` 會被忽略，car-segmenter 也完全不會被載入。 |

在標準 14 個欄位之外，每個物件會新增的欄位：`kp_cctv`（GUI 疊圖用的原始 `[x, y, conf] × 24`）、`n_keypoints`、`status`（`ok` / `ambiguous_heading` / `failed_insufficient_kp`）。

#### 一次錄製 car-segmenter mask 供重複使用

`--method segmentation` 通常每次執行都會即時跑一次 car-segmenter。如果同一支影片需要同時跑 `--localizer procrustes` 和 `--localizer reprojection` 兩個 pass，就會對相同的輸出跑兩次 YOLO11-seg，改成只錄製一次、兩個 pass 共用：

1. 錄製一次：

```bash
python scripts/record_car_masks.py --video <video_path>
```

輸出：`output/car_masks/<location_code>/seg-mask_<video_stem>.json.gz`（純影像空間的紀錄 — 沒有 G-projection，也沒有 PifPaf）。

2. 兩個 pass 都指向同一份 mask 檔：

```bash
python scripts/run_keypoints_openpifpaf.py --video <video_path> \
  --g-proj <g_proj_path> --method segmentation \
  --seg-masks-json <mask_json_path> --localizer procrustes

python scripts/run_keypoints_openpifpaf.py --video <video_path> \
  --g-proj <g_proj_path> --method segmentation \
  --seg-masks-json <mask_json_path> --localizer reprojection
```

### 4. 重投影關鍵點視覺化

把 replay JSON 裡單一 frame 的逐車輛 `kp_sat`/`sat_coords` 重投影結果畫到衛星影像上，用於檢查重投影結果。

```bash
source /opt/anaconda3/bin/activate trafficlab && \
python scripts/plot_reprojection_keypoints.py \
  <replay_json_path> \
  --frame-index <N>
```

選項：

| Flag | 預設值 | 說明 |
|------|---------|-------|
| `--frame-index` | 自動 | 要繪製的 frame；預設會自動挑選有效關鍵點最多的那一幀 |
| `--ids` | *(全部)* | 要納入的 `tracked_id` 值，以逗號分隔 |
| `--location-code` | 自動推斷 | 覆寫推斷出的 location code |
| `--sat-image` | 自動推斷 | 覆寫衛星影像路徑 |
| `-o` / `--out` | 與輸入檔同層 | 輸出 PNG 路徑 |
| `--dpi` | `200` | 輸出解析度 |

輸出：預設把 PNG 存在輸入 JSON 旁邊（`<stem>.keypoints_frame<N>.png`）。

### 5. CCTV + SAT 合成輸出

把整份 replay JSON 批次渲染成 PNG：預設每幀左 CCTV、右 SAT 疊圖，並排輸出。

```bash
QT_QPA_PLATFORM=offscreen python scripts/export_cctv_sat_composite.py \
  --replay <replay_json_path> \
  --out-dir <out_dir>
```

選項：

| Flag | 預設值 | 說明 |
|------|---------|-------|
| `--replay` | *(必填)* | replay `.json`/`.json.gz` 的路徑 |
| `--out-dir` | *(必填)* | 逐幀 PNG 的輸出目錄 |
| `--ids` | *(全部)* | 要納入的 `tracked_id` 值，以逗號分隔；某一幀若沒有符合的物件就整幀跳過 |
| `--cctv-video` | replay 裡的 `mp4_path` | 覆寫影片路徑 |
| `--sat-image` | `location/<code>/sat_<code>.png` | 覆寫 SAT 背景圖路徑 |
| `--kp-conf` | `0.2` | 僅在缺少 `bbox_2d` 時，用來推導 2D box 的關鍵點信心度閾值；`--right-panel parallax` 時也用來判斷 `kp_cctv`/`kp_sat` 配對是否有效 |
| `--sat-only` | 關閉 | 完全跳過 CCTV 面板與水平拼接 — 只輸出 SAT 疊圖，也因為不需要而跳過開啟影片檔 |
| `--right-panel` | `sat` | `sat`：現有 SAT 疊圖（box/arrow/coords dot/label/keypoints）；`parallax`：改畫 parallax-correction 前後對比 — 每個 `kp_sat`（彩色點+label，已校正）與其未校正的 h=0 apparent point（灰點）連線，逐幀比照 `trafficlab/projection/parallax_reprojection.py` 的畫面。需要能解析出 G_projection config（見 `--g-proj`） |
| `--g-proj` | `location/<code>/G_projection_<code>.json` | 僅 `--right-panel parallax` 使用；覆寫 G_projection config 路徑 |
| `--kp-color-mode` | `track` | 僅 `--right-panel sat` 有效：`track` 依每輛車的 track 顏色來上色（預設，與 GUI 一致）；`part` 改為依車輛部位上色（wheel/light/plate/door/corner/bumper/glass），同部位跨車輛使用相同顏色。`--right-panel parallax` 一律依部位上色，不受此 flag 影響 |
| `--no-sat-keypoints` | 關閉 | SAT 面板不畫關鍵點（box/arrow/coords dot/label 不受影響）；只能搭配 `--right-panel sat` |
| `--zoom-to-ids` | 關閉 | 把 SAT 面板裁切成單一固定視窗，涵蓋 `--ids` 所指 track 在其出現過的每一幀裡的 `sat_coords`（`--right-panel parallax` 時則涵蓋校正前後兩組關鍵點），所有輸出幀共用同一視窗（畫面不跳動），取代顯示完整 SAT 影像；必須搭配 `--ids` |
| `--zoom-margin` | `200` | `--zoom-to-ids` 裁切框周圍的 padding，單位為 SAT 影像像素（與 `trajectory_tools.py` 的 `--zoom-margin` 預設值一致） |

輸出：`--out-dir` 裡每幀一張 `frame_<NNNN>.png`。要把這些幀轉成影片：

```bash
ffmpeg -framerate 25 -i <out_dir>/frame_%04d.png \
  -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -pix_fmt yuv420p \
  <out_dir>/composite.mp4
```

（只有在合成出來的寬／高是奇數、`libx264` 不接受時，才需要 `pad` filter。）

### 6. 軌跡繪圖

涵蓋 `plot`（整條軌跡所有點畫一張圖）與 `frames`（對選定 id 用同一個固定裁切窗口逐幀輸出 PNG，適合接 ffmpeg 轉影片、畫面不跳動）：

```bash
source /opt/anaconda3/bin/activate trafficlab && python scripts/trajectory_tools.py <plot|frames> <replay_json_path> [flags]
```

| Flag | 適用 | 說明 |
|---|---|---|
| `--location-code` / `--sat-image` | 兩者皆可 | replay 缺 `location_code` metadata 時擇一必填；否則預設找 `location/<location_code>/sat_<location_code>.png` |
| `--ids` | 兩者皆可 | 篩選 `tracked_id`，逗號分隔 |
| `--zoom-margin`（`plot` 需搭配 `--zoom-to-fit`） | 兩者皆可 | 預設 `200`，衛星影像像素；裁切窗口是對軌跡 bounding box 加 padding 算出來的，會視需要放大到跟原圖同比例避免 `imshow` 變形 |
| `--show-heading-arrows` / `--show-keypoints`（`frames` 預設顯示，用 `--hide-heading-arrows`/`--hide-keypoints` 關閉） | 兩者皆可 | `--show-keypoints` 依部位（wheel/light/plate/door/corner/bumper/glass）上色，跟「CCTV + SAT 合成輸出」`--kp-color-mode part` 同一套配色 |
| `--keypoint-trajectories` | 僅 `plot` | 逗號分隔的 `kp_sat` 關鍵點名稱（見 `trafficlab/motion/keypoints_openpifpaf.py` 的 `KP_NAMES`，連字號／底線皆可），把每個指定關鍵點畫成逐 track 連線軌跡，跟一般的 `sat_coords` 軌跡疊在同一張圖上，各關鍵點固定配色（跟 `--show-keypoints` 的部位配色是不同套） |
| `--show-id-labels` | 僅 `plot` | 可見軌跡旁渲染同色 `tracked_id` 標籤 |
| `--min-points` | 僅 `plot` | 預設跳過少於 5 點的 track |
| `--include-out-of-bounds` | 僅 `plot` | 預設跳過完全在衛星影像外的 track |
| `--out-dir` | 僅 `frames` | 逐幀 PNG 輸出目錄（必填） |

`plot` 跟 `frames` 差別一句話：`plot` 把整條軌跡所有點畫在同一張圖；`frames` 用同一個固定裁切窗口，對選定 id 出現過的每一幀各輸出一張 PNG。

顯示完整說明：

```bash
source /opt/anaconda3/bin/activate trafficlab && python scripts/trajectory_tools.py --help
```

### 7. 對 script 做語法檢查

```bash
source /opt/anaconda3/bin/activate trafficlab && python -m py_compile scripts/run_inference.py
```

### 8. 車輛模板 GCP 校正工具

獨立的 GUI 工具，把「方向 4：車輛模板作為 PnP GCP」跟「方向 7：多參考物最小二乘法」接在一起：在 CCTV 畫面上點 2 個輪胎接地點，工具用既有 ground homography 把車輛 CAD 模板（24 個關鍵點）套上正確的 sat 位置、朝向與大小，再跟該幀 replay JSON 的 `kp_cctv` 配對，產生多組「頭點像素＋腳點真實位置＋真實高度」參考點，餵給跟方向 7 完全共用的 `trafficlab.projection.reference_point_calibration.calibrate()` 解出 `cam_sat_xy`/`z_cam_meters`。完整使用步驟（5 個分頁）、設計細節與常見問題見 `docs/car-template-calibration-tool-guide.md`。

```bash
source /opt/anaconda3/bin/activate trafficlab
python scripts/car_template_calibration_tool.py \
  --replay-json <replay_json_path> \
  --g-proj <g_proj_path>
```

不帶參數執行會用預設值（`output/wheel_pair/test21/test21-4.json.gz` 與 `location/test21/G_projection_test21.json`，若存在）。

| Flag | 說明 |
|------|------|
| `--replay-json` | 已跑過 `run_keypoints_openpifpaf.py`、帶 `kp_cctv` 欄位的 replay JSON；`location_code`／對應影片路徑會自動推斷，不用另外指定影片 |
| `--g-proj` | 既有 `G_projection_<code>.json`，若給了優先於 `--location-code` |
| `--location-code` | `--g-proj` 的替代寫法，自動找 `location/<code>/G_projection_<code>.json` |

一定要有既有的 `G_projection_<code>.json` 才能運作；預設不會覆寫它，結果另存到 `output/car_template_calibration/<location_code>/`，需要在「結果」tab 另外按「套用到 G_projection」才會覆寫（無法復原）。

核心程式碼：`trafficlab/projection/car_template_placement.py`（模板數學，純 numpy）、`trafficlab/gui/tools/car_template_calibration_tool.py`（GUI 本體）；共用 `trafficlab/projection/reference_point_calibration.py` 的 `calibrate()`，以及「5. 驗證」tab 用到的 `trafficlab/projection/parallax_reprojection.py`。

### 9. 多參考物最小二乘校正工具

獨立的 GUI 工具，實作方向 7（多參考物最小二乘法）：蒐集 N 個（N ≥ 2）已知真實高度的參考物件的頭／腳像素座標，套用非線性最小二乘同時解出相機的 sat 平面位置（`cam_sat_xy`）與高度（`z_cam_meters`）——是現有 `pars_stage.py` 兩物件手動標定法的推廣，參考物件數量從固定 2 個放寬到任意多個，數學模型相同。完整使用步驟（4 個分頁）與常見問題見 `docs/reference-point-calibration-tool-guide.md`。

```bash
source /opt/anaconda3/bin/activate trafficlab
python scripts/reference_point_calibration_tool.py \
  --video <video_path> \
  --g-proj <g_proj_path>
```

不帶參數執行會用預設值（`location/test21/footage/test21-4.mp4` 與 `location/test21/G_projection_test21.json`）。

| Flag | 說明 |
|------|------|
| `--video` | 開啟時直接載入這支影片，預設 `location/test21/footage/test21-4.mp4` |
| `--g-proj` | 既有 `G_projection_<code>.json`（提供 undistort + homography），若給了優先於 `--location-code` |
| `--location-code` | `--g-proj` 的替代寫法，自動找 `location/<code>/G_projection_<code>.json`，預設 `test21` |

一定要有既有的 `G_projection_<code>.json` 才能運作；預設不會覆寫它，結果另存到 `output/reference_point_calibration/<location_code>/`，需要在「結果」tab 另外按「套用到 G_projection」才會覆寫（無法復原）。

核心程式碼：`trafficlab/projection/reference_point_calibration.py`（`ReferencePoint`、`calibrate()`，純 numpy/scipy）、`trafficlab/gui/tools/reference_point_calibration_tool.py`（GUI 本體）；「4. 驗證」tab 共用 `trafficlab/projection/parallax_reprojection.py`（跟 `car_template_calibration_tool` 的「5. 驗證」tab 同一套邏輯）。

### 10. CCTV 影格選取工具

獨立的 GUI 工具，用來從 location 的 footage 裡挑一幀存成 `location/<location_code>/cctv_<location_code>.png`。下拉選單先選 location（只列出 `footage/` 底下有 `.mp4` 的 location），再選該 location 的某支影片；可播放／暫停、上一幀／下一幀，或拖曳 slider／輸入 spinbox 跳到指定幀。輸出圖片維持原影片的寬高，不做任何縮放。

```bash
source /opt/anaconda3/bin/activate trafficlab
python scripts/cctv_frame_picker_tool.py
```

| Flag | 說明 |
|------|------|
| `--location-code` | 開啟時預先選取的 location（預設：`location/` 底下第一個符合條件的） |
| `--video` | 開啟時預先選取的影片路徑（預設：所選 location 的第一支影片） |

按「存成 CCTV 圖片」會寫到 `location/<location_code>/cctv_<location_code>.png`；若檔案已存在會先跳出確認覆寫對話框（無法復原，除非該檔案本身有版本控制）。

核心程式碼：`trafficlab/gui/tools/cctv_frame_picker_tool.py`（GUI 本體，共用 `trafficlab/visualization/video_player.py` 的 `VideoPlayer` 與 `undistort_stage.py` 的 `ImageViewer`）；跳幀時沿用 `reference_point_calibration_tool.py` 的 seek-with-sequential-fallback 邏輯，因為部分 AV1 編碼的素材直接 seek 會靜默失敗。

### 11. seg yolobox + wheel pair 修正工具

獨立的 GUI 工具，把「seg tight-box 定位」到「wheel_pair 修正」串成一條三分頁的流程。使用者唯一要選的是 location，其餘（影片、config、G_projection）都自動解析。

```bash
source /opt/anaconda3/bin/activate trafficlab
python scripts/seg_wheelpair_tool.py
```

| 分頁 | 內容 |
|------|------|
| `1. 推論` | 選 location（只列出同時有 `footage/*.mp4` 與 `G_projection_*.json` 的），按「執行 seg yolobox 推論」跑 `InferencePipeline`，完成後自動跳到分頁 2 |
| `2. seg yolobox 結果` | 顯示 seg replay 的軌跡圖，下方「執行 wheel pair 修正」按鈕，完成後自動跳到分頁 3 |
| `3. 修正前後對照` | 左右並排顯示修正前／後的軌跡圖，下方是逐 track 的修正報告 |

| Flag | 說明 |
|------|------|
| `--location-code` | 開啟時預先選取的 location（預設：第一個可用的） |
| `--config-name` | seg 推論要用的 config key（預設 `yolo_seg_tight_box_cpu`；不用 `seg_default` 是因為它綁 `device: mps`） |

**分頁 2 的「執行 wheel pair 修正」實際做三件事**：

1. 用 `trafficlab/trajectory/seg_mask_adapter.py` 把 seg replay 自己的 `mask_contour` 轉成 `record_car_masks.py` 的檔案格式，寫到 `output/car_masks/<code>/seg-mask_<stem>.from-replay.json.gz`
2. 跑 `run_keypoints_openpifpaf.py --method segmentation --seg-masks-json <上面那份> --localizer wheel_pair`（不傳 `--cad-template`，沿用 wheel_pair 的預設 nissan_juke_nismo 模板），輸出到 `output/wheel_pair/<code>/<stem>.from-seg-masks.json.gz` —— **因此 segmentation 模型整條流程只跑一次**（在步驟 1 的 seg 推論裡），log 會出現 `car-segmenter not loaded` 佐證。檔名帶 `.from-seg-masks` 是為了不覆蓋手動跑 `run_keypoints_openpifpaf.py` 產生在同一個資料夾的 `<stem>.json.gz`
3. 呼叫 `correct_replay()`，輸出 `<stem>.wheelpair_corrected.json.gz`（放在 target replay 旁邊，不覆蓋原檔）

工具全程不覆蓋任何既有檔案，唯一的例外是各 replay 旁邊的 `<stem>.trajectories.png` 軌跡圖（沿用 `trajectory_tools.py` 的預設輸出路徑，重跑會更新）。

因為兩份 replay 的 `tracked_id` 都源自同一批 mask，修正預設用 **identity `track_id_map`**（只對應兩邊都有的 id）而不是 `sat_coords` 鄰近猜測。例外：若 target 出現 `tracked_id >= 500`，會跟 `run_keypoints_openpifpaf.py` 給未匹配 PifPaf 碎片的合成 id（per-frame index + 500）撞號，此時自動退回鄰近比對並在 log 標示。

核心程式碼：`trafficlab/gui/tools/seg_wheelpair_tool.py`（GUI 本體，重用 `trafficlab/gui/inference_session.py` 的 `InferenceSession` 與 `undistort_stage.py` 的 `ImageViewer`）、`trafficlab/trajectory/seg_mask_adapter.py`（純資料轉換，CLI 版是 `scripts/replay_to_seg_masks.py`）。

### 12. 把 seg replay 的 mask 轉成 car-segmenter 記錄

`seg_wheelpair_tool.py` 步驟 1 的 CLI 版，也可單獨使用：讓 `--seg-masks-json` 重用 `run_inference.py` 已經算好的 mask，不必再跑一次 segmentation 模型。

```bash
source /opt/anaconda3/bin/activate trafficlab && \
PYTHONPATH=$(pwd) python scripts/replay_to_seg_masks.py <seg_replay_json>
```

| Flag | 預設值 | 說明 |
|------|--------|------|
| `-o` / `--output` | 自動 | 預設 `output/car_masks/<code>/seg-mask_<stem>.from-replay.json.gz`（`.from-replay` 標記避免覆蓋真正的 `record_car_masks.py` 錄製檔） |
| `--car-classes` | `car` | 要輸出成 car instance 的 replay `class` 值，逗號分隔。預設只有 `car`，與 `CarMaskSource` 寫死的 `classes=('car',)` 一致 —— PifPaf 用的是汽車關鍵點模型，讓 `two_wheeler` 的 mask 去搶那些關鍵點只會配錯 |
| `--location-code` | 自動推斷 | 只影響輸出路徑 |

輸入 replay 必須帶 `mask_contour`（只有 `model.type: "seg"` 的推論會產生）；沒有的話會直接報錯，而不是安靜地輸出一份空的 instance 記錄。

## 推論相關注意事項

- GUI 的 inference 分頁與 `scripts/run_inference.py` 都使用 `trafficlab.inference.pipeline.InferencePipeline`。
- Location 的輸入應該放在 `location/<location_code>/footage/*.mp4` 底下。
- G-projection 檔案應該放在以下其中一個位置：
  - `location/<location_code>/G_projection_<location_code>.json`
  - `location/<location_code>/G_projection_svg_<location_code>.json`
- 輸出會寫到：

```text
output/model-<model_name>_tracker-<tracker_name>/<config_name>/<location_code>/*.json.gz
```

- 比較 GUI 與 CLI 的推論行為時，要用相同的 config name、mp4、環境與工作目錄。

## Replay JSON 格式預期

大部分推論後工具預期的是標準的 replay 格式：

```json
{
  "frames": [
    {
      "frame_index": 0,
      "objects": [
        {
          "tracked_id": 101,
          "class": "Car",
          "sat_coords": [1234.5, 678.9],
          "sat_center": [1234.5, 678.9]
        }
      ]
    }
  ]
}
```

- `tracked_id` 用來連接跨幀的同一個物件。
- `sat_coords` 是繪圖使用的標準衛星座標點。
- 當某個工具刻意移動衛星座標點時，`sat_center` 應該同步更新為 `sat_coords`。
- `class` 對繪圖來說是選填的，但對摘要與過濾很有用。
- `.json.gz` 是推論輸出的標準儲存格式；工具應該要保留 gzip 支援。

## 驗證檢查清單

對程式碼變更，執行範圍最小、但有效的檢查：

- 對改動過的 Python 檔案做語法檢查：

```bash
source /opt/anaconda3/bin/activate trafficlab && python -m py_compile path/to/file.py
```

- 對改動過的 script 檢查 CLI help：

```bash
source /opt/anaconda3/bin/activate trafficlab && python scripts/trajectory_tools.py --help
```

## 產生檔案與 Git 衛生守則

- 預設輸出放進 `output/`；只有純語法檢查／smoke-test 這類用後即丟的產出，才寫到 `/private/tmp`。驗證軌跡工具的改動時，省略 `-o`/`--output`，讓輸出留在預設路徑（輸入 JSON 旁邊）就好。
- 回報完成之前，先檢查 `git status --short`，把自己的變更和使用者原本就有的變更區分開來。
- 絕對不要還原使用者無關的變更。

