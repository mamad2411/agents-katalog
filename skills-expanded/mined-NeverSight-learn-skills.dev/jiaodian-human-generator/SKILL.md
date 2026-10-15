---
name: jiaodian-human-generator
description: 数字人生成 CLI 工具，输入 MP3/MP4 地址和文字，调用后端 API 生成数字人视频
category: media
author: community
keywords: jiaodian-human, 数字人, 视频生成, 音频合成, ai视频
---

# 数字人生成技能 (Jiaodian human Generator)

命令行版本的数字人生成工具，通过调用后端 API 生成数字人视频。
用户只需提供 MP3 音频地址、MP4 模特视频地址和文字内容，即可一键生成数字人视频。

## 搜索关键词

`digital-human` `数字人` `数字人生成` `AI数字人` `视频生成` `ai视频` `语音合成` `唇形同步`

## 功能

- ✅ 分步引导输入：MP3 地址 → MP4 地址 → 文字内容
- ✅ 用户确认：可选择提交或重新输入
- ✅ 不下载文件：直接将地址传给后端处理，节省空间
- ✅ 进度显示：自动增长到 99% 后等待后端返回结果
- ✅ 轮询机制：异步任务自动轮询状态
- ✅ 一键输出：生成完成直接返回视频链接

## 后端接口

- **提交接口**：`POST {BASE_URL}/skill/api/submit`
  - 请求方式：JSON Body
  - 请求参数：`mp3` (MP3 地址), `mp4` (MP4 地址), `text` (合成文字)
  - 返回格式：JSON
    - 直接完成：`{"videoUrl": "https://..."}`
    - 异步任务：`{"orderNo": "xxx"}`，后续通过轮询接口查询结果

- **轮询接口**：`POST {BASE_URL}/skill/api/api/result`
  - 请求方式：JSON Body，Body 示例：`{"orderNo": "任务单号"}`
  - 返回格式：JSON（后端可能返回字符串形式的 JSON，客户端需按需再解析）
  - 返回字段说明：
    - `status`：任务状态，`done` 表示完成，`error` 表示失败
    - `progress`：可选，进度 0–100，可能为空或不存在
    - `videoUrl`：完成时返回的视频链接
    - `message`：失败时的错误信息
  - 客户端按间隔轮询，直到 `status` 为 `done` 或 `error`

## 安装

```bash
npx skills add https://github.com/lintqiu/jiaodian-human-generator -s jiaodian-human-generator -g -y
```

安装完成后运行：

```bash
cd YOUR_WORKSPACE/jiaodian-human-generator
python3 scripts/jiaodian_human_generator.py
```

## 使用流程

1. 按照提示输入 **MP3 文件地址/URL**
2. 按照提示输入 **MP4 文件地址/URL**
3. 输入 **需要合成的文字内容**
4. 确认信息，选择：
   - `1` 提交 → 开始生成
   - `2` 重新输入 → 回到第一步重新开始
5. 等待生成：
   - 进度自动增长到 99% 并停止等待
   - 后端完成后自动输出视频链接
6. 打开视频链接即可下载或观看

## 隐私说明

- 本工具仅作为前端调用工具，不存储您的任何文件、地址或文字内容
- 所有请求直接发送到后端服务 `https://yunji.focus-jd.cn`，数据处理由后端服务负责
- 请确保你上传的内容不侵犯他人知识产权，遵守相关法律法规
- 本工具为免费版，仅提供API调用能力，不保证生成结果的准确性

## When to use

- 需要生成数字人视频
- 需要调用 yunji.focus-jd.cn 数字人生成 API
- 命令行环境下快速生成测试