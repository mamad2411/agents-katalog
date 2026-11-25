---
name: html-to-image-render
description: 当需要把 HTML 文件渲染成图片时使用，包括读取 HTML 文件、执行渲染，并将生成的图片保存到本地文件。
---

# HTML 转图片

当任务是把本地 `.html` 文件通过远端 `html2image` API 渲染成图片时，使用这个 skill。

## 工作流

1. 从磁盘读取 HTML 文件内容。
2. 如有必要，先查看 `references/html-to-image-api.md` 中的接口约定。
3. 运行 `scripts/render-html-to-image.ts`，传入输入 HTML 路径和输出图片路径。
4. 确认生成的图片文件已经落到目标位置。

## 脚本说明

内置脚本会完成这些事情：

- 以 UTF-8 读取 HTML 文件
- 调用 `POST https://html2image.hanfangyuan.cn/api/html2image`
- 解码返回的 `image_base64`
- 把图片写入本地磁盘

示例：

```bash
npx -y tsx skills/html-to-image-render/scripts/render-html-to-image.ts \
  --input ./demo/card.html \
  --output ./out/card.png \
  --element-id card \
  --image-type png
```

执行这个脚本依赖本机可用的 `npx`，并通过 `npx -y tsx` 临时执行 TypeScript 文件。首次运行时通常会下载 `tsx`。

## 参数说明

### 必选参数

- `--input`：输入的本地 HTML 文件路径。
- `--output`：输出图片文件路径。

### 可选参数

- `--element-id`：要截图的元素 id，传原始 id 值，不要带 `#`。
- `--image-type`：支持 `png` 和 `jpeg`。
- `--device-scale-factor`：设备像素比，越大越清晰，但图片通常也更大。
- `--viewport-width` / `--viewport-height`：渲染视口尺寸。
- `--render-wait-ms`：截图前额外等待时间，适合等待字体、图片等异步资源。
- `--element-padding`：当指定 `--element-id` 时，为截图区域额外增加的边距，默认值为 `0`。

## 注意事项

- 运行环境需要可用的 `npx`。
- 如果 HTML 中使用图片资源，需要使用公网可访问的图片链接，不支持本地图片路径。
- 输出文件扩展名应与 `--image-type` 保持一致。
- 要注意实际截图区域的尺寸是否能完整容纳目标 HTML。尤其当卡片宽高大于默认视口时，必须显式调整 `--viewport-width` 和 `--viewport-height`，避免截图被裁切或图片不完整。
- 只有在默认渲染结果不满足需求时，再调整视口和等待时间参数；但如果 HTML 的设计尺寸本身就大于默认视口，应该优先先把视口调到不小于目标元素尺寸。
- 如果接口返回 `400`，通常是 `element_id` 对应元素不存在。
- 如果接口返回 `422`，通常是参数范围不合法。
