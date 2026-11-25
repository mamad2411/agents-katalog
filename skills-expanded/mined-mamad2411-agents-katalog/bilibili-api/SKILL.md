---
name: bilibili_api
description: Bilibili 平台 API 的调用规范与 WBI 签名处理
---

# Bilibili API 技能 (Bilibili API)

## 接口范围
- **视频信息**: `/x/web-interface/view` (Web), `/x/v2/view` (App)
- **播放地址**:
  - `/x/player/wbi/playurl` (Web Wbi 签名)
  - `/pgc/player/web/v2/playurl` (PGC/番剧)
  - `api.snm0516.aisee.tv/x/tv/playurl` (TV 端接口)
- **互动视频**: 通过 `player.so` 接口获取互动图谱，并解析 `stein/edgeinfo_v2`

## 关键流程: WBI 签名
1. 获取 `img_key` 和 `sub_key` (通常由 `nav` 接口返回)。
2. 对参数进行排序并根据算法生成 `wts` 和 `w_rid`。
3. **注意**: WBI 签名具有时效性，需在调用前动态生成。

## 高级特性
- **画质解锁**: TV 接口支持获取更多高画质流。
- **杜比/无损**: DASH 响应中需特别处理 `dolby` 和 `flac` (Hi-Res) 节点。

## 代码规范
- 所有的 API 调用应封装在 `internal/biliapi` 目录下。
- 使用强类型的 Struct 来解析 JSON 响应。
- 必须包含错误处理，特别是针对 403 Forbidden 和 API 速率限制。
