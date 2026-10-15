---
name: live-broadcast
version: 0.1.16
description: 直播预报——NBA/世界杯/中国男女足比赛赛程与转播源。用户问比赛，直接跑 cyeam tv 命令返回结果，不要分析不要缓存。【重要】必须先读 skill 原文获取正确命令格式，禁止瞎猜。
---

# 直播预报

## 规则

**用户问比赛 → 跑 cyeam tv → 返回结果。不要预加载、不要缓存、不要分析。一次一个命令。**

```
用户: "今天有什么比赛？"          →  cyeam tv today
用户: "最近 NBA 赛程"            →  cyeam tv list --league nba --days 7
用户: "湖人下一场什么时候？"     →  cyeam tv next --team 湖人
用户: "世界杯赛程"               →  cyeam tv list --league worldcup
```

## 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--league` | nba, worldcup, cn-football | `--league nba,worldcup` |
| `--days` | 未来 N 天，默认 3，最大 14 | `--days 7` |
| `--from`/`--to` | 日期范围 | `--from 2026-06-15 --to 2026-06-20` |
| `--team` | 球队名 | `--team 湖人` |
| `--source` | 转播源 | `--source CCTV5` |

## 输出要点

- 球队名、联赛阶段名（Finals/Playoffs 等）**必须翻译成中文并加国旗 emoji**
- 转播源渲染为可点击链接
- 不需要登录

## 不做的事

- 不抓直播流、不解 m3u8/flv
- 不绕过会员或地区限制
- 不推送实时比分或赛后集锦
- 不覆盖 NBA/世界杯/中国男女足以外的赛事