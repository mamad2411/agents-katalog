---
name: imagemagick
description: 图片缩放、裁切、拼接与格式转换。
disable-model-invocation: true
---

# ImageMagick

下面使用 ImageMagick 7 的 `magick` 命令；用 `magick -version` 确认已安装的版本。

## 常用五条

```bash
magick 原.png -resize 50% 出.png                                  # 按比例缩
magick 原.png -resize 256x256 出.png                              # 缩到框内，保持比例
magick 原.png -crop 100x80+10+10 +repage 出.png                   # 裁一块（+repage 必须加）
magick 原.png -background none -gravity center -extent 512x512 出.png  # 居中补透明边到固定尺寸
magick a.png b.png +append 横.png                                 # 横着拼（-append 是竖着拼）
magick 原.png 出.webp                                             # 转格式，看后缀
magick identify -format '%wx%h' 图.png                            # 查尺寸
```

## 坑

- ImageMagick 7 使用 `magick`，避免依赖旧版 `convert` 命令。
- **`-crop` 后面必须跟 `+repage`**，不然裁出来的图带着原图的偏移量，后面再处理会错位。
- `montage` 若报 `unable to read font`，指定当前可用字体；不需要文字的简单拼图可用 `+append` / `-append`。
- **参数顺序有意义**：`magick 输入 [操作] 输出`，操作写在输入后面、输出前面。写反了不报错，出来的图不对。
- 游戏素材从素材站搬回来尺寸经常不对，**统一尺寸用 `-extent` 补边，不要用 `-resize` 硬拉**（会变形）。
