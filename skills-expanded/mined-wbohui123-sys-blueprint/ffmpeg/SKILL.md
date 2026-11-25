---
name: ffmpeg
description: 音视频转换、剪切、抽帧与信息读取。
disable-model-invocation: true
---

# ffmpeg

需已安装 FFmpeg；用 `ffmpeg -version` 和 `ffprobe -version` 确认当前命令可用。

## 常用五条

```bash
ffprobe -v error -show_entries format=duration,size -of csv=p=0 片.mp4   # 取时长和大小
ffmpeg -i 片.mp4 -ss 1 -t 10 -c copy 出.mp4                              # 从第1秒剪10秒，不重编码，秒出
ffmpeg -i 片.mp4 -vcodec libx264 -crf 30 小.mp4                          # 压缩，crf 越大越小越糊（18~30）
ffmpeg -i 片.mp4 -ss 3 -vframes 1 帧.png                                 # 抽第3秒那一帧
ffmpeg -i 片.mp4 -vf "fps=12,scale=640:-1" 出.gif                        # 转 GIF，给用户看演示用这个
```

## 坑

- **`-version` 一个杠，不是 `--version`。** 写两个杠会报错。
- **`-ss` 放 `-i` 前面 = 快但可能差几帧；放后面 = 准但慢。** 剪片子用上面那种（放后面）。
- **`-c copy` 只能在切边正好是关键帧时精确。** 要精确切就别加 `-c copy`，让它重编码。
- **`-y` 覆盖、`-n` 不覆盖。** 都不写会卡在问你要不要覆盖，那一轮就废了。
- **GIF 别贪大**：`fps=12,scale=640:-1` 是个好起点；原分辨率直接转 GIF 会几十兆。
- 若报 `Library not loaded`，检查安装来源与缺失的动态库；Homebrew 安装的版本可用 `brew reinstall ffmpeg` 修复。
