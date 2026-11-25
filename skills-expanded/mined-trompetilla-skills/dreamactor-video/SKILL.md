---
name: dreamactor-video
description: 使用 Dreamactor V2 进行动作迁移，将视频中的动作、表情和口型迁移到图片角色上。当用户想要动作迁移、表情驱动、口型同步、或提到 dreamactor 时使用此 skill。
category: video
tags: [motion-transfer, dreamactor, video-to-video]
featured: false
---

# Dreamactor V2 动作迁移

字节跳动 Dreamactor V2 动作迁移模型。输入一张参考图片和一个驱动视频，将视频中的动作、表情和口型迁移到图片中的角色上，同时保持角色和背景特征不变。

**特色**：
- 支持真人、动画、宠物等多种角色类型
- 对非人类和多角色有出色表现
- 支持全脸和全身驱动
- 最大驱动视频时长 30 秒

## 可用模型

| 模型 ID | 功能 | 说明 |
|--------|------|------|
| `fal-ai/bytedance/dreamactor/v2` | 动作迁移 | 图片+视频→动作迁移视频，按秒计费 |

## 工作流

### 1. 调用 submit_task

使用 MCP 工具 `submit_task` 提交任务：

```json
{
  "model_id": "fal-ai/bytedance/dreamactor/v2",
  "parameters": {
    "image_url": "参考图片 URL",
    "video_url": "驱动视频 URL",
    "trim_first_second": true
  }
}
```

### 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| image_url | string | **是** | - | 参考图片 URL。支持真人/动画/宠物。jpeg/jpg/png，最大 4.7MB |
| video_url | string | **是** | - | 驱动视频 URL。提供动作/表情/口型参考。最大 30 秒，mp4/mov/webm |
| trim_first_second | boolean | 否 | true | 是否裁剪输出视频第一秒过渡画面 |

### 输入要求

**图片要求**：
- 格式：jpeg、jpg、png
- 最大大小：4.7 MB
- 分辨率：480x480 至 1920x1080（超大图片会按比例缩小）
- 角色应清晰可见

**视频要求**：
- 格式：mp4、mov、webm
- 最大时长：30 秒
- 分辨率：200x200 至 2048x1440
- 支持全脸和全身驱动

## 查询任务状态

提交任务后会返回 `task_id`，使用 `get_task` 查询结果：

```json
{
  "task_id": "返回的任务ID"
}
```

任务状态：
- `pending` - 排队中
- `processing` - 处理中
- `completed` - 完成，结果在 `result` 中
- `failed` - 失败，查看 `error` 字段

## 完整示例

**用户请求**：把这张人物图片用这个舞蹈视频来驱动

**执行步骤**：

1. 调用 `submit_task`：
```json
{
  "model_id": "fal-ai/bytedance/dreamactor/v2",
  "parameters": {
    "image_url": "https://v3b.fal.media/files/b/0a8d6292/E9WNRJh8K8DF9lSV0bkXs_image.png",
    "video_url": "https://v3b.fal.media/files/b/0a8d633f/u5Ye7jXL0Cfo0ijz5M6YY_input_example_dreamactor.mp4",
    "trim_first_second": true
  }
}
```

2. 获取 `task_id` 后调用 `get_task` 查询结果

## 计费说明

- **计费方式**：按驱动视频秒数计费
- **单价**：20 积分/秒（约 $0.05/秒）
- **最低计费**：3 秒
- **最大时长**：30 秒

| 视频时长 | 费用（积分） |
|---------|-------------|
| 5 秒 | 100 |
| 10 秒 | 200 |
| 15 秒 | 300 |
| 30 秒 | 600 |

## 使用技巧

1. **图片质量**：使用高质量、角色清晰的图片效果更好
2. **视频选择**：驱动视频中的动作越清晰，迁移效果越好
3. **多角色支持**：Dreamactor V2 对多角色场景有出色表现
4. **非人类角色**：支持动画角色、宠物等非真人角色
5. **过渡裁剪**：建议保持 `trim_first_second: true` 以获得更流畅的开头
