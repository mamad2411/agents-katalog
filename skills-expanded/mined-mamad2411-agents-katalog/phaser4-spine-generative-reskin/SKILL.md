---
name: phaser4-spine-generative-reskin
description: 对 Phaser 4 Spine Atlas/纹理图集的全部 Region/Cell 逐项生成替换图、断点续作、重建全新纹理或验证无旧纹理回退时使用；要求保留 Skeleton、Attachment 与 Mesh UV，并能在任何 Cell 失败时安全恢复。
---

# Phaser 4 Spine 生成式换皮

## 全局控制接入

控制面边界：可提议、可审查、可在已建立且任务授权有效的 Work Item 范围内修改，且必须回到 `$phaser4-game-workflow-control` 审计和状态迁移；仅实际 A4-A6 操作请求批准。

Spine 换皮是资源生产域，不得旁路全局控制。只在已建立且任务授权有效的 Work Item、冻结 Implementation Package、A 等级和 Atlas/输出路径内修改；每次恢复、生成、重建与验证都按 [`phaser4-game-workflow-control`](../phaser4-game-workflow-control/SKILL.md) 提交证据和状态，仅实际 A4-A6 操作请求批准。

先将 `<skill-dir>` 解析为本 `SKILL.md` 所在的 Skill 根目录；以下所有工具命令都使用 `node <skill-dir>/scripts/spine_reskin_progress.mjs`，不依赖当前工作目录。复制安装器会在该 Skill 目录安装 Sharp，不会修改目标游戏项目的依赖清单。

按以下顺序完成整套换皮。任何一个 Cell 未完成、校验失败或状态不明，都不得宣称交付完成。

## 1. 审计输入并建立候选目录

1. 找到 `.atlas`、所有 Page 图片和配套 Skeleton JSON/Binary；记录 Phaser 4、Spine runtime 版本、纹理加载器、PMA 约定和运行入口。
2. 运行 `node <skill-dir>/scripts/spine_reskin_progress.mjs init --atlas <source.atlas> --output <candidate>/progress.json`。默认把候选写入新目录，禁止覆盖原 Atlas、Page 或 Skeleton；需要源 Cell 参考时增加 `--reference-dir <candidate>/source-cells`。
3. 审核清单中的每一页尺寸、格式、filter、repeat、pma、scale，以及每个 Region 的 `xy/size/orig/offset/index/rotate` 或 `bounds/offsets`。发现重复 ID、缺页、越界或字段无法解析时立即停止。
4. 用清单列出全部 Cell，不以 Attachment 数量、首个 Page 或可见角色数量代替总数。记录源 Atlas、全部 Page 和配套 Skeleton 文件的 SHA-256，确保后续不会误用旧候选。

详细的多 Page、trim/offset/UV、padding/extrusion、PMA 和透明空白页规则见 [references/atlas-rebuild.md](references/atlas-rebuild.md)。

## 2. 冻结全局风格与结构参考

1. 在清单中登记全局角色/材质/光照/色彩/轮廓参考和排除项；每个 Cell 同时传入原 Cell 参考图与同一份全局参考。
2. 原 Cell 只能用于结构、比例、透明轮廓、裁剪边界和 Mesh 语义参考，或作为生成模型的蒙版。禁止复制原图 RGB、抠取原图像素、以原 Page 作为输出底图或在失败时回退到原纹理。
3. 对每个 Cell 标注是否为刚体、可变形 Mesh、附件点缀、阴影/高光或透明特效。不要改变 Attachment 名称、Skeleton 绑定、Mesh 顶点顺序或 UV 语义。

## 3. 逐 Cell 生成并持久化

1. 先把 Cell 标为 `generating`：
   `node <skill-dir>/scripts/spine_reskin_progress.mjs mark --manifest <candidate>/progress.json --cell <cell-id> --status generating`。
2. 使用当前可用的图片生成能力逐 Cell 生图。每次请求都传入该 Cell 的原图参考、全局风格/角色参考和清单中的 `orig`/`size`/`rotate` 约束；保持同一角色跨 Cell 的脸、材质、光向、颜色和透明边缘一致。不要在初始化 Skill 时实际生图。
3. 让输出图符合清单的结构契约：可提供未裁剪的 `orig` 尺寸（工具会按 `offset`/`size` 提取），或直接提供正向的裁剪 `size` 尺寸；旋转 Cell 必须按正向尺寸提供，再由打包器旋回 Atlas 方向。保留真实透明度，不用纯色背景填充。
4. 生成后立即写入不可变候选路径并标记：
   `node <skill-dir>/scripts/spine_reskin_progress.mjs mark --manifest <candidate>/progress.json --cell <cell-id> --status generated --image <candidate>/generated/<file>.png`。
   工具会记录 SHA-256、尝试次数和状态历史；不要手改 JSON。失败则用 `--status failed --error <原因>`，修复后从 `failed` 重新进入 `generating`。
5. 每批生成后运行 `status`，需要审阅完整字段时运行 `read`；进程中断时运行 `recover`，把 `generating/validating/packing` 安全退回 `pending`，再继续，禁止把旧图冒充新图。

## 4. 逐 Cell 透明度、形状和 Mesh 语义检查

1. 对照原 Cell 参考检查可见轮廓、透明边缘、锚点、方向、阴影层级和可读性；检查生成图的 alpha 是否有意外背景、孔洞或裁切。
2. 对 Mesh/九宫格/变形附件，确认关键形状、透明区域和局部细节仍落在原 `orig`/`offset` 语义内；不要通过改 Atlas 坐标“修图”。
3. 将 Cell 标为 `validating`；不通过就标为 `failed` 并记录原因。只有所有 Cell 都通过，才允许进入 `packing`。

## 5. 从透明空白 Page 重建

1. 使用 `node <skill-dir>/scripts/spine_reskin_progress.mjs pack --manifest <candidate>/progress.json --output-dir <candidate>/atlas`。工具会为每个原 Page 创建全透明 RGBA 空白页，只将已生成图按原 `xy/size` 放回；不会读取源 Page 像素。
2. 保留原 Region 名称、Page 顺序、坐标、trim/orig/offset、rotate、index、filter、repeat、scale 和 Skeleton 所需字段。按原旋转方向写回；根据 Page 的 `pma` 将生成图做 straight-alpha 到 premultiplied-alpha 转换。
3. 按项目约定设置 `--padding` 与 `--extrusion`；填充和边缘扩展只能来自当前生成图，且必须落在原 Region 矩形内，不能改变 UV 坐标。多 Page 必须逐页输出并在新 Atlas 中保持对应 Page 引用。
4. 任一 Cell 缺图、尺寸不符、旋转/裁剪越界、Sharp 不可用或写盘失败，都保持候选不完成，记录 `failed`，修复后重试。不要发布部分 Page。

## 6. 完成门与 Phaser 运行态验证

1. 打包成功后工具将 Cell 标为 `completed` 并记录候选 Page/Atlas 哈希。运行 `node <skill-dir>/scripts/spine_reskin_progress.mjs verify --manifest <candidate>/progress.json`；未完成、哈希不匹配或产物缺失必须返回非零。
2. 在隔离的 Phaser 4 候选场景加载新 Atlas 与原 Skeleton，逐一播放待测动画、Attachment 和 Mesh 变形；检查无缺图、错位、翻转、PMA 黑边、透明底色、UV 断裂和跨 Page 问题。至少保留整体预览截图/录屏和控制台日志。
3. 运行态验证失败时保留失败候选，创建新的进度清单并从受影响 Cell 重新生成、验证和打包；禁止修改已 `completed` 的清单或把失败状态覆盖掉。不得只改运行时代码或宣称“视觉上差不多”。手工比较原 Skeleton 文件 SHA-256 及 Skeleton/Attachment/Mesh UV 是否保持不变；工具 `verify` 不自动校验 Skeleton。只有新清单全 Cell `completed`、验证证据绑定当前候选哈希且手工比较通过，才可交付。

## 7. 最终工件与恢复

交付新 `.atlas`、全部新 Page PNG、进度清单、生成图/参考图索引、全局参考、哈希清单、整体预览和 Phaser 运行态验证记录。保留原 Atlas 与原 Page 只作回滚对照；任何 Cell 失败都公开报告 ID、原因、重试次数和下一步，不得静默跳过。

进度状态和字段约束见 [references/progress-state.md](references/progress-state.md)。

## 工具命令

在仓库根目录运行：

```powershell
node <skill-dir>/scripts/spine_reskin_progress.mjs --help
node --test <skill-dir>/scripts/spine_reskin_progress.test.mjs
```

工具缺少 Sharp 时会由 Node.js 给出依赖解析错误并返回非零；通过官方复制安装器安装时依赖会放在 Skill 自身目录。
