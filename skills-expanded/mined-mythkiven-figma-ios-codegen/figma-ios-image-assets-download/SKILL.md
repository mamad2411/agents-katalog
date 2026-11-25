---
name: figma-ios-image-assets-download
description: >-
  Reference iOS image assets that figma-ios-preload-data pre-downloaded into the data package.
  Covers two cases: (1) local imagesets (copy + UIImage(named:)), and
  (2) server-side images (avatars / covers / category icons / any RECTANGLE filled with IMAGE
  that has no local imageset) — these MUST use the data package's mock.default_image_url via
  sd_setImage, never fabricated asset names. Use when wiring any UIImage reference or
  generating mock data for image fields.
---

# Figma 图片资源引用规范（消费数据包）

切图下载已由 `figma-ios-preload-data` 阶段 1 完成，阶段 2 只负责"拷贝 + 引用"。

## 数据来源

| 文件 | 用途 |
|---|---|
| `{data_dir}/assets/ios/manifest.json` | `node_id → asset_name` 映射 + 文件路径 |
| `{data_dir}/assets/ios/img_xxxxx_*.imageset/` | iOS 标准 imageset（Contents.json + @2x.png + @3x.png）|

## manifest.json 结构

```json
{
  "schema_version": "1.0.0",
  "platform": "ios",
  "scale": 3,
  "download_failed_count": 0,
  "items": {
    "29:107": {
      "node_id": "29:107",
      "name": "去除图片文字 (9)",
      "asset_name": "img_231f7_background",
      "asset_id": "29-107",
      "imageset_path": "img_231f7_background.imageset",
      "files": [
        {"scale": 2.0, "path": "img_231f7_background.imageset/img_231f7_background@2x.png"},
        {"scale": 3.0, "path": "img_231f7_background.imageset/img_231f7_background@3x.png"}
      ]
    }
  }
}
```

> `imageset_path` 相对 `assets/ios/`；`files[].path` 也相对该平台目录。若 `download_failed: true` 出现在某 item 上，**禁止** `UIImage(named:)`，改走下方 mock URL，并在 README 记警告。

## 集成步骤

### Step 1：拷贝 imageset 到主工程

```bash
# 目标位置：主工程的 Assets.xcassets/<目标分组>/
cp -R {data_dir}/assets/ios/*.imageset <project>/Assets.xcassets/<group>/
```

### Step 2：代码中引用

```swift
// Figma node: 29:107
imageView.image = UIImage(named: "img_231f7_background")
```

> `UIImage(named:)` 的字符串 = `manifest.items[node_id].asset_name`，禁止臆造。

### Step 3：在生成的 README 中列出资源清单

```markdown
## 图片资源

需要将以下 imageset 拷贝到主工程 Assets.xcassets：

- img_231f7_background.imageset  ← Figma 节点 29:107 (去除图片文字 9)
- img_0642b_game_pubg.imageset   ← Figma 节点 29:108 (PUBG)
- ...
```

## 服务器下发图片场景（统一用默认 mock URL）

### 触发条件

节点表现为图片，但**本地没有切图可用**——任一即触发：

- `fills` 含 `IMAGE` 类型，但节点**没有** `export.settings`（设计师未点 export）→ `figma-ios-preload-data` 不下载本地副本
- 节点是 `RECTANGLE` / `ELLIPSE` 等被填充 image 的占位形状（头像、封面图、品类卡片背景图等业务图）
- 任何被识别为"图片表现但无 imageset 文件"的节点

> 业务上这一类几乎都是后端接口下发的真实图——发版时由业务接口注入，开发期需要 mock 演示。

### ✅ 统一规则：用数据包中的 `mock.default_image_url`

读 `{data_dir}/manifest.json` 的 **`mock.default_image_url`**（配置源是 `config.json` 的 `default_mock_image_url`，写入包时落在 `mock` 下）：

```jsonc
// manifest.json
{
  "mock": {
    "default_image_url": "https://picsum.photos/200"
  }
}
```

> 这是一个**真实可访问的 mock 图**（不是 Figma 临时 URL，不会过期），跑起来就能看到图。配置在 `figma-ios-preload-data/config.json` 的 `default_mock_image_url`（见 `config.example.json`），需要换图床就改那里，**不要在 Swift 代码里写死**。

### 推荐 Swift 写法

```swift
// MARK: - 服务器下发图片（Figma 节点 ID: 29:107）
// TODO(阶段3): 接入业务接口后替换为后端返回的真实图片 URL
private static let kMockImageURL = "https://picsum.photos/200"

// 使用：
imageView.sd_setImage(
    with: URL(string: Self.kMockImageURL),
    placeholderImage: nil
)
```

mock URL 统一用数据包 `manifest.json.mock.default_image_url`，不要编造宿主常量名。

### ⚠️ 严禁直接写 Figma S3 URL

Figma 渲染产生的临时 URL（`figma-alpha-api.s3.*`）**24 小时即失效**，写到生产代码就是定时炸弹。**任何场景下都不要把 Figma S3 URL 写进 Swift 文件**。

### ⚠️ 同样禁止：example.com / placeholder.com / 仿造的假 URL

旧版 skill 曾建议写 `https://example.com/REPLACE_WITH_BUSINESS_API.png` 之类的占位字符串。**已禁用**——这种 URL 跑起来只能看到失败占位，达不到 mock 演示效果。**一律用 `manifest.mock.default_image_url`**。

### 调试期想看设计稿真图

`figma-ios-preload-data` 在阶段 1 已经把节点导出为 `.imageset` 放到 `{data_dir}/assets/ios/`，**直接用 `UIImage(named: <asset_name>)` 即可**，不需要也**禁止**在阶段 2 再手动调 Figma images 接口或下载图片。

如需排查"为什么这张图没生成切图"，按下列顺序定位：

1. 看 `{data_dir}/assets/ios/manifest.json` 里有没有该 `node_id` 的 `asset_name` 条目
2. 没有则看 `{data_dir}/manifest.json.warnings` 有没有相关导出失败警告
3. 仍无解 → 回到 `figma-ios-preload-data/` 仓库提单（导出策略归数据包阶段管），不要在阶段 2 自行兜底

> 任何 `figma-alpha-api.s3.*` 临时 URL 都禁止出现在最终代码里。

## 命名规范（参考，由 figma-ios-preload-data 生成）

`img_<5位哈希>_<语义>`：
- 哈希：保证唯一
- 语义：英文 / 拼音，可追溯到 Figma 原节点名

例：`img_231f7_background`、`img_0642b_game_pubg`、`img_a11a6_game_lol`

## 自检清单

- [ ] 已读 `assets/ios/manifest.json`
- [ ] 所有 `UIImage(named:)` 字符串来源于 `manifest.items[].asset_name`
- [ ] 生成 README 已列出 imageset 拷贝清单
- [ ] 服务器下发图片**统一用** `{data_dir}/manifest.json` → `mock.default_image_url`，配 `sd_setImage` + TODO 注释
- [ ] **无 `example.com` / `placeholder.com` / 任何手编占位 URL**
- [ ] **无 `figma-alpha-api.s3.*` 临时 URL**
- [ ] 没有任何对 `download_figma_images.py` / `get_figma_image_url.py` 的调用
