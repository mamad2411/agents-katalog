---
name: 锐捷-火山引擎视频生成
description: 使用火山引擎/UniAPI 进行 AI 视频生成时调用：支持文生视频、图生视频、Seedance 2.0 模型选择、duration/ratio 参数配置、异步任务提交与轮询，以及视频任务失败排查。
---

# 火山引擎 AI 视频生成

# 用途

使用火山引擎/UniAPI 提交 AI 视频生成任务，并用固定脚本轮询任务状态、下载结果视频和输出任务元数据。

适用场景：

- 文生视频
- 图生视频
- Seedance 2.0 / Seedance 2.0 Fast 模型选择
- 生成时长、画幅比例、分辨率等参数调优
- 异步任务提交、轮询、失败原因排查

## 执行检查清单

1. 确认输入模式：文生视频或图生视频。
2. 根据用户要求解析时长、画幅比例、分辨率和风格约束。
3. 使用固定脚本提交任务，并按有界轮询等待完成。
4. 返回最终视频 URL 或本地保存路径，同时保留 task id 和任务元数据。

## 执行方式

- 正常生成必须使用当前 skill 目录下的 `scripts/generate-video.mjs`。执行前把脚本路径解析成绝对路径。
- 不要为了生成视频临时手写 `curl`、`Invoke-RestMethod` 或内联 PowerShell。锐智只预授权固定 helper 命令，不预授权任意网络 shell。
- 认证读取顺序：`RUIZHI_API_KEY`、`RUIZHI_HOME` / `CODEX_HOME` 下的 `auth.json`、`OPENAI_API_KEY`。
- 默认 API base URL 读取 `RUIZHI_OPENAI_BASE_URL`，未设置时使用 `https://uniapi.ruijie.com.cn/v1`。
- 下载后的视频保存到当前工作区，默认建议使用 `output/video/`，除非用户指定路径。
- 不要打印 API key、`auth.json` 内容或任何认证头。

文生视频示例：

```powershell
node "<当前 skill 的绝对路径>/scripts/generate-video.mjs" --prompt "电影感产品亮相，柔和棚拍灯光，慢速推近镜头" --duration 10 --ratio 16:9 --out "output/video/result.mp4" --force
```

图生视频示例：

```powershell
node "<当前 skill 的绝对路径>/scripts/generate-video.mjs" --prompt "让产品缓慢旋转，镜头平稳推进，保持主体清晰" --image "C:/path/input.png" --duration 8 --ratio 16:9 --out "output/video/result.mp4" --force
```

如果用户没有指定输出文件，默认传入 `--out "output/video/<简短文件名>.mp4"` 并加 `--force`，避免只返回临时 URL。文件名应使用 ASCII、小写、连字符或时间戳。

## API 请求规则

### 参数被忽略的原因

火山引擎原生接口 `POST /contents/generations/tasks` 使用顶层参数 **`ratio`**（字符串，例如 `"16:9"`）和 **`duration`**（整数秒），而不是 `width` / `height`。UniAPI 的标准 `/v1/video/generations` 端点会映射到这些原生参数，但 `width` / `height` 到火山引擎 `ratio` 的映射不可靠，所以只传 `width` / `height` 时可能被静默忽略。

### 可用模型（UniAPI）

| 模型 ID | 说明 |
|---|---|
| `doubao-seedance-2-0-260128` | 默认模型，质量更高 |
| `doubao-seedance-2-0-fast-260128` | 速度更快，成本通常更低 |

除非用户明确要求“更快”或“更便宜”，默认使用 `doubao-seedance-2-0-260128`。

### 正确参数策略

参数解析优先级：**用户明确要求 > 默认值**。

- 用户指定时长时直接使用该值；默认值为 `10`。Seedance 2.0 支持 **4-15 秒**。
- 用户指定画幅比例时直接使用字符串；默认值为 `"16:9"`。
- 支持的 `ratio` 字符串：`"16:9"`、`"9:16"`、`"1:1"`、`"4:3"`、`"3:4"`、`"21:9"`、`"adaptive"`。

请求中必须同时包含顶层 `duration`、`width`、`height`，并在 `metadata` 中传入火山引擎原生命名的 `ratio` 和 `duration`，以最大化 UniAPI 正确转发参数的概率：

```json
{
  "model": "<model_id>",
  "prompt": "<prompt>",
  "image": "<url_or_base64_if_image_mode>",
  "duration": <resolved_duration>,
  "width": <resolved_width>,
  "height": <resolved_height>,
  "metadata": {
    "ratio": "<resolved_ratio_string>",
    "duration": <resolved_duration>,
    "resolution": "720p"
  }
}
```

画幅比例到顶层 `width` / `height` 的参考值：

- `"16:9"` -> 1920 x 1080
- `"9:16"` -> 1080 x 1920
- `"1:1"` -> 1080 x 1080
- `"4:3"` -> 1440 x 1080
- `"3:4"` -> 1080 x 1440
- `"21:9"` -> 2560 x 1080

## 可靠性规则

- 必须保留 task id，方便失败后重试或排查。
- 使用有界轮询间隔和超时时间，不要无限等待。
- 接口失败时直接暴露失败原因，并给出可执行的重试建议。
- 任务完成后检查响应里的 `metadata.duration`、`metadata.width`、`metadata.height` 是否符合请求；如果不一致，要提醒用户 UniAPI 可能没有透明转发这些参数。
- 如果用户要求真实生成，不能只 `--dry-run` 后假装完成。

## 参考资料

- `references/sources.md`
