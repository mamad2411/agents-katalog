---
name: luma-vision
description: 多模型视觉理解能力。通过 /skill luma-vision 激活时，执行 vision.js 脚本调用外部视觉模型分析图片。
---

# Luma Vision Skill — 多模型视觉理解

## 说明

所有模型要发送图片都必须在 `config.toml` 中声明 `image_in` 能力，否则前端会拦截图片提交。
但纯文本模型即使声明了 `image_in` 也无法真正理解图片内容。

**本 skill 只在用户主动通过 `/skill luma-vision` 命令发送图片时激活。**
如果用户直接粘贴图片（没有 `/skill`），不要执行本 skill 的逻辑。

## 何时触发

- **仅限** 用户当前消息以 `/skill luma-vision` 开头并附带图片
- 历史消息中的 `Attached image file:` 内容**不触发**本 skill

## 何时不触发

- 用户直接粘贴图片发送（没有 `/skill` 前缀）
- 多模态模型收到图片时，直接用原生看图能力，不要走脚本

## 行为

直接执行 vision.js 脚本，不要用 `ReadMediaFile`：

```bash
node "<skill_dir>/scripts/vision.js" "<图片来源>" "<问题描述>"
```

## 支持的图片来源

脚本兼容三种来源，适配不同 agent 的传图方式：

| 类型 | 示例 | 适用场景 |
|------|------|----------|
| 本地路径 | `./image.png`、`D:\photos\photo.jpg` | Kimi Code skill 传的缓存路径 |
| HTTP(S) URL | `https://example.com/image.png` | 网页图片 |
| Data URI | `data:image/png;base64,...` | Claude Code 等直接内联传入 |
| `@` 前缀路径 | `@clipboard.png` | 自动剥离 `@` 后按本地路径处理 |

## 环境变量

在系统环境变量中配置，脚本会自动读取：

| 变量 | 说明 |
|------|------|
| `CUSTOM_BASE_URL` | API 地址 |
| `CUSTOM_MODEL_NAME` | 模型名称 |
| `CUSTOM_API_KEY` | API Key |

## 注意事项

- 脚本路径：`<skill_dir>/scripts/vision.js`
- 不要用 `ReadMediaFile` 代替