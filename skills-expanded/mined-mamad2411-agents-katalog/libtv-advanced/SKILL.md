---
name: libtv-advanced
description: LibTV (LibLib.tv) 高级视频工作流技能，支持一键完成 AI 视频生成、自动下载、智能剪辑（含转场、字幕、BGM）。Use when the user wants to create AI videos or short films using LibTV, especially when they need automatic video editing with transitions, subtitles, or background music.
license: MIT
---

# LibTV 高级视频工作流

完整的 AI 视频制作流水线：生成素材 → 自动下载 → 智能剪辑成片。

## 核心原则（必读）

**Agent 是"信使"，不是"导演"。** 调用 LibTV 生成素材时，必须遵守以下规则：

1. **原样转发用户请求** — 把用户的描述直接作为 message 发送给 LibTV 后端 Agent，不要自行拆解、改写或"优化" prompt
2. **不要分解任务** — 不要把一个请求拆成多个分镜单独生成，LibTV 后端 Agent 会自行规划分镜和生成策略
3. **不要添加创意发挥** — 不要在用户 prompt 基础上擅自增加细节描述，保持原意
4. **信任后端能力** — LibTV 后端 Agent 具备完整的多模型调度、分镜规划、角色一致性等能力，前端 Agent 只需做好传话和结果处理

错误示范：用户说"生成猫咪看风景的视频"，Agent 自行拆成 4 个分镜分别描述并调用 4 次 API
正确示范：用户说"生成猫咪看风景的视频"，Agent 直接把这句话作为 message 发送，让后端 Agent 规划

## 前置要求

```bash
# 安装 moviepy（仅剪辑功能需要）
pip3 install moviepy

# 安装 FFmpeg（Mac）
brew install ffmpeg

# 或下载: https://ffmpeg.org/download.html
```

## 环境变量

```bash
export LIBTV_ACCESS_KEY="your-access-key"
```

## 快速开始

### 1. 一键完整工作流

生成 + 下载 + 剪辑一条龙：

```bash
python3 scripts/libtv_workflow.py "生成一个可口可乐1分钟宣传片"
```

带配置文件（字幕、BGM、转场）：

```bash
python3 scripts/libtv_workflow.py "生成古风武侠短片" --config scripts/config_example.json
```

### 2. 上传参考素材后生成

```bash
# 先上传参考图片
python3 scripts/upload_file.py ./reference.jpg

# 然后在 prompt 中引用上传的 URL
python3 scripts/libtv_workflow.py "参考这张图片的风格，生成一个类似的视频"
```

### 3. 单独剪辑（已有素材）

```bash
python3 scripts/libtv_workflow.py "--" --skip-generate --video-dir ./my_videos --config my_config.json
```

### 4. 高级剪辑（精细控制）

```bash
python3 scripts/video_editor.py scene1.mp4 scene2.mp4 scene3.mp4 \
  --transition fade \
  --bgm ./music.mp3 \
  --bgm-volume 0.3 \
  --style cinematic \
  -o final.mp4
```

## Scripts

### scripts/libtv_client.py
LibTV API 完整客户端，覆盖全部 4 个端点。

```bash
# 创建会话
python3 scripts/libtv_client.py create "生成一个短视频"

# 查询会话
python3 scripts/libtv_client.py query <session-id> --after-seq 0

# 上传文件
python3 scripts/libtv_client.py upload ./image.png

# 切换项目
python3 scripts/libtv_client.py change-project
```

### scripts/libtv_workflow.py
完整工作流脚本，串联全部步骤。

```bash
# 基础用法
python3 scripts/libtv_workflow.py "生成短剧视频"

# 完整参数
python3 scripts/libtv_workflow.py "生成短剧" \
  --config config.json \
  --wait-timeout 600 \
  --output my_video.mp4
```

### scripts/video_editor.py
专业视频剪辑工具。

```bash
python3 scripts/video_editor.py video1.mp4 video2.mp4 \
  --transition fade \
  --transition-duration 1.5 \
  --bgm music.mp3 \
  --bgm-volume 0.25 \
  --style cinematic \
  -o output.mp4
```

### scripts/config_example.json
配置文件模板：

```json
{
  "transition": "fade",
  "transition_duration": 1.5,
  "style": "cinematic",
  "bgm": "./assets/music.mp3",
  "bgm_volume": 0.25,
  "subtitles": [
    {
      "text": "第一章",
      "start": 0,
      "duration": 3,
      "position": "center",
      "fontsize": 80,
      "color": "white"
    }
  ]
}
```

## 功能特性

| 功能 | 说明 |
|------|------|
| AI 生成 | 调用 LibTV 生成图片和视频素材 |
| 文件上传 | 上传参考图片/视频供生成时引用 |
| 自动下载 | 并行批量下载生成的所有素材 |
| 转场效果 | fade(淡入淡出)、slide(滑动) |
| 字幕支持 | 自定义位置、大小、颜色、描边 |
| 背景音乐 | 自动循环、音量调节、淡入淡出 |
| 调色风格 | normal、warm、cool、cinematic |

## 典型工作流

```
用户: "帮我做一个古风武侠短片"

Agent:
  1. 原样转发: create_session("帮我做一个古风武侠短片")
     → 后端 Agent 自行规划分镜并生成

  2. 轮询等待: query_session(session_id, after_seq)
     → 每 8 秒查询一次，检测完成状态

  3. 自动下载所有素材（并行下载）

  4. 调用 video_editor 拼接
     → 加转场、加字幕、加 BGM

  5. 返回: final_video.mp4
```

## 轮询策略

- 轮询间隔：8 秒
- 使用 `after_seq` 增量获取新消息，避免重复拉取
- 超时时间：默认 5 分钟（视频生成可能需要 3-10 分钟）
- 完成判断：检查消息中是否包含生成结果（`task_result`）或完成标记

## 注意事项

1. **信使原则**：不要改写用户 prompt，直接转发给 LibTV 后端
2. **生成需要时间**：短剧可能需要 5-10 分钟，耐心等待
3. **剪辑需要 FFmpeg**：确保已安装
4. **字幕需要字体**：macOS 默认使用 PingFang SC，可自定义
5. **BGM 版权**：使用自己的音乐文件，注意版权
