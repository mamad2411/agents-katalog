---
name: tech-tencentcloud-expert-team
description: 面向腾讯云资源治理、应用上线、域名访问、云存储、文件交付、图片文字识别和音频转写等场景，按业务目标、异常现象和预期交付物选择合适能力：可巡检服务器、证书、权限和监控，处理
  CloudBase、Web、微信小程序和轻量服务器部署，修复 DNSPod 解析问题，管理 COS 对象存储与专属云盘文件，调用 OCR/ASR 完成文字识别和音频转写。交付部署地址、解析记录、文件链接、识别文本、转写稿、问题定位结论、待确认事项或明确失败原因。
---

# 腾讯云专家

Use this skill as the routing entry point for Tencent Cloud work. It coordinates the companion Tencent Cloud skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request by business goal, current blocker, and expected deliverable.
2. Choose the smallest relevant companion skill set from the guide. For multi-step work, sequence investigation before mutation and implementation before deployment verification.
3. Before resource changes, deployments, deletions, overwrites, DNS updates, paid API calls, credential setup, or service restarts, inspect current state and ask for confirmation when the action may affect running resources or cost.
4. Execute through the selected companion skill instructions and bundled scripts. Do not invent cloud state; return real command/API output, verified URLs, records, links, transcription text, OCR text, or explicit blocker reasons.
5. Summarize the triggered skill, completed result, verification evidence, required confirmations, and unresolved blockers.

## Companion Skills

- `$tencentcloud-infra`: 腾讯云资源巡检与跨产品排障
- `$tencentcloud-lighthouse-skill`: 轻量服务器运维与应用部署
- `$tencentcloud-dnspod-skill`: DNSPod 域名解析管理
- `$cloudbase`: CloudBase 项目上线与排障
- `$tencent-cos-skill`: COS 对象存储与媒体处理
- `$tencent-agent-storage`: 专属云盘文件交付与管理
- `$tencentcloud-ocr-general`: 腾讯云图片文字识别
- `$tencentcloud-asr`: 腾讯云音频转写与字幕生成
- `$web-development`: Web 应用实现与验证
- `$miniprogram-development`: 微信小程序开发与发布

## Output

Return only the artifacts relevant to the matched scenario: deployment address, DNS record, file link, OCR text, ASR transcript, resource inspection result, risk list, pending confirmation, or failure cause.
