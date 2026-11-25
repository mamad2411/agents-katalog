---
name: godot
description: 制作和修改 Godot 2D／3D 游戏与实时场景工程，检查、运行、录影并导出作品；改一处只验碰到的那一项，导出、开包、录片这类整套验收一轮跑一次。
disable-model-invocation: true
---

# Godot

目标是交付可运行、可继续修改的 Godot 游戏或实时场景。已有工程沿用其结构，目标平台决定运行和导出方式。

需已安装 Godot，命令是 `godot`；用 `godot --version` 确认版本。下文标注 4.7.2 的实测经验按当前版本核对。

## 脚本检查

```bash
godot --headless --path <项目目录> --check-only --script <脚本.gd>   # 查脚本有没有错，不开窗
```

取得实际运行和画面证据，同时让用户的桌面保持可用。检查、导入和导出用 `--headless`；它没有渲染器，不能代替画面验证。Blueprint 项目命令中的 `godot` 默认隐藏窗口、不抢焦点且静音，仍保留 GPU 渲染。用能把画面存成 PNG 的场景或录影，再用 `read_image` 查看。

## 改一处验一项，一轮验一整套

后台跑一次 Godot 要几十秒到几分钟。改一处就把导出、开包、录片整套跑一遍，一遍五六分钟，一轮里大半时间都在等。

- 改一处：只跑碰到的那一项。脚本用上面的 `--check-only`；场景和逻辑用下面「后台运行」那条跑几百帧，看 stderr 有没有新报错。
- 一轮做完、交东西之前：再跑一次整套，导出、打开导出的包、录片、量帧率。
- 拷一份工程去验（临时快照），连 `.godot/` 一起拷。不带它，所有资源要重新导入；带上，只重导改过的（4.7.2 实测）。一个带 65 米巨像和 4k 贴图的工程，重导一次用了 4 分多钟。
- 退出时打的 `ObjectDB instances were leaked at exit`、`resources still in use at exit`：用 `--quit-after` 强退时常见，查下来是退出那一刻播放实例、节点没来得及释放，不影响运行。记一笔，不当失败，也不必追；运行过程中报的错才要查。
- 量帧率前看一眼有没有别的 Godot、Blender 在跑（`pgrep -x Godot; pgrep -x Blender`）。几个渲染挤在一台机器上，读数不可信。帧率在装好的成品里量一次就够。

## 导出

导出模板装了才能导网页版和安装包。没装时可用本机 Godot 验证工程；确需导出时说明缺少的匹配模板，不自动打开编辑器。
按当前 Godot 版本检查匹配的导出模板，不沿用开发机的安装状态。

## 实测命令

命令中的项目目录、应用名与可执行文件名，按当前项目实际产物填写。

### 后台运行 / 截图（保留渲染）
- 后台运行：`godot --path "<项目目录>" --quit-after 120`（跑 120 帧自退；检查 stderr 和退出状态）
- 录影取帧（不依赖系统截图权限），在同一次 bash 调用中执行：
  ```bash
  recording_dir="$(mktemp -d "$TMPDIR/godot-recording.XXXXXX")"
  godot --path "<项目目录>" --write-movie "$recording_dir/t.avi" --fixed-fps 60 --quit-after 120
  ffmpeg -y -i "$recording_dir/t.avi" -vf "select=eq(n\,60)" -frames:v 1 f.png
  ```
- 若用户数据或缓存写入被拒绝，根据具体错误为该功能配置项目内可写位置；不要沿用固定的开发机临时目录。

### 导出（macOS，实测通过）
- `godot --headless --path "<项目目录>" --export-release "macOS" "<导出目录>/<应用名>.app"`（目标目录须先存在）
- 工程须开 `rendering/textures/vram_compression/import_etc2_astc=true`（否则报「停用 ETC2 ASTC 无法导出 arm64/Universal」）
- 4.7.2 模板封包只含 `godot_macos_release.universal`（macos.zip 内）→ 预设 `binary_format/architecture` 只能选 `universal`（含 arm64）
- Code Signing = Built-in (ad-hoc only)、Notarization = Disabled 可本机直接跑

### 导出包（.app）验证
- 用项目的后台启动环境运行 Godot；导出包内的自定义可执行文件名用 `DYLD_INSERT_LIBRARIES="$BLUEPRINT_BACKGROUND_WINDOW_LIBRARY" "<app>/Contents/MacOS/<可执行文件名>" --quit-after 300` 加载同一窗口保护。检查正常退出、渲染器日志与实际画面，不以桌面弹窗作为成功证据。
- 需要用户试玩时交回安装包或预览入口，由用户打开。
- 录影出画面：`--write-movie "$TMPDIR/<本次唯一文件名>.avi" --fixed-fps 60 --quit-after 300`（非实时录制）＋ ffmpeg 抽帧

### 校验脚本
- `godot --headless --path "<项目目录>" --check-only --script res://x.gd` —— **退出码恒为 0，要 grep stderr 文本判绿**
- 首次先跑 `godot --headless --path "<项目目录>" --import`

### 录影 → mp4
- `godot --path "<项目目录>" --disable-vsync --write-movie "$TMPDIR/<本次唯一文件名>.avi" --fixed-fps 60 --resolution 1280x720 --quit-after 600`
  → 等正常退出 → `ffmpeg -y -i "$TMPDIR/<本次唯一文件名>.avi" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac "<项目内输出路径>.mp4"`
- 铁律：`--write-movie` 一律绝对路径（相对路径按项目目录解析）；让进程正常退出（直接杀会缺时长）；AVI 大、录完即转；建议 `--disable-vsync`（官方文档：加速 movie 写入）

### 声音导入（4.7.2 实测）
- WAV 默认导成有损 QOA（`.import` 里 `compress/mode=2`）；音乐和要保住低频、峰值的音效改 0。循环文件 `edit/loop_mode=2`。
- ffmpeg 写的 24 位 WAV 是扩展头，导入报 not PCM；用 16 位 PCM。`--headless` 时音频驱动是 Dummy，听不到。
- 做声音、量声音见 audio 技能。

### 校验脚本的坑（4.7.2 实测）
- **引用 autoload 的脚本用 `--check-only` 会误报** `Identifier not found: <Autoload>`（check 时不注册 autoload）——这类脚本要跑项目看 stderr 判绿；不引用 autoload 的脚本 check-only 正常。

### 录影的坑：MovieWriter 捕获冻结
- 曾在开窗环境下遇到 `--write-movie`「帧照写、画面定格」；Metal 与 opengl3 均出现过，需检查当前产物。
- 可靠替代：游戏内每 N 帧 `get_viewport().get_texture().get_image().save_png()` 存 PNG 序列 → `ffmpeg -framerate 60/N -i seq_%05d.png -c:v libx264 -crf 18 -pix_fmt yuv420p out.mp4`。
- 录完务必冻检：相邻整秒抽帧 md5，连续 ≥2 秒同帧＝疑似冻结。
