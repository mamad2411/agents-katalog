---
name: imagex-knowledge
description: 当在服务端开发中需要接入 veImageX 图片服务、使用 veImageX 服务端 SDK、调用图片处理 API、或实现图片上传/管理功能时使用。
user-invocable: false
---

# veImageX 图片服务平台

veImageX（简称 ImageX）是字节跳动提供的一站式云端一体图像综合处理解决方案。该平台主要服务于字节集团内部业务，同时面向火山引擎企业客户，为图像处理全生命周期提供高效支撑。veImageX 提供高可靠的素材存储托管、高可用的素材分发、业界领先的自研图形图像压缩算法，以及丰富的可扩展可编程 AI 富媒体处理能力。

## SDK 接入

veImageX 提供了配套的服务端 SDK，支持多种编程语言（Golang、Java、Python、PHP 等），帮助开发者更方便地调用 API。服务端 SDK 主要覆盖以下功能场景：

**核心使用场景**：
- 图片资源管理（上传文件获取、删除、更新、预热、刷新缓存等）
- 图像算法处理（OCR、画质评估、超分辨率等）
- 创意魔方的图片合成
- 离线图片转码和画质评估
- 智能审核任务处理
- 多文件压缩异步任务管理

**注意事项**：
- 基础图像处理（裁剪、缩放、加水印等）建议通过控制台模板配置，通过访问图片 URL 获取处理结果
- 图像格式转换（如 JPEG 转 HEIC）使用方式同上
- 图片 URL 签发请参考专门的接入指南

[sdk-usage-guide.md](./sdk-usage-guide.md) - veImageX 服务端 SDK 使用指南
[api-categories.md](./api-categories.md) - veImageX API 分类与接口说明
[error-handling.md](./error-handling.md) - veImageX 错误码处理指南

