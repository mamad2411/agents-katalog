---
name: cr-doctor
description: 检查尽调的运行环境：本机有没有上游 Company Research Agent 服务、有没有 Python，决定走轨 A 还是轨 B。开始一次尽调前，或用户问环境、配置、模型时读这份。
---

# 检查环境

## 配置

`app/config.json` 可能不存在，不存在时按默认值：

```json
{ "mode": "auto", "apiBase": "http://127.0.0.1:8000" }
```

`mode` 是 `auto`（默认）、`a`（只用本机服务）或 `b`（只用兼容模式）。用户说“以后都用兼容模式”或者告诉你服务的地址时，改这个文件。`apiBase` 只能是本机地址。

## 检查

1. 看有没有 Python：依次试 `python3 --version`、`python --version`、`py -3 --version`，记下能用的那个。都不行就是没有 Python。
2. 有 Python 时探测上游服务：

   ```bash
   python3 "$HOME/skills/cr-research/scripts/upstream.py" probe --api <apiBase>
   ```

   没有 Python 时不用探测：轨 A 的脚本要用 Python，只能走轨 B。

3. 决定走哪条路：

| `mode` | 服务可达且有 Python | 否则 |
| --- | --- | --- |
| `auto` | 轨 A | 轨 B |
| `a` | 轨 A | 任务 `failed`，告诉用户下面的启动说明 |
| `b` | 轨 B | 轨 B |

4. 把结果写进 `app/state.json` 的 `runtime`：`mode`、`track`、`python`、`apiReachable`、`checkedAt`。探测到服务时再写 `openrouter`、`openai`、`defaultModel`。

## 只报告查得到的

上游的 `/config` 只告诉我们 OpenRouter 和 OpenAI 有没有配置，以及默认模型。Tavily 和 Gemini 的情况查不到，不要猜，也不要去读 .env 文件。上游缺 Key 时任务会失败，把它返回的错误告诉用户。

轨 B 不需要任何 Key：搜索用 `web_search` 和 `web_fetch`。用户想用 Tavily，就到 App 的设置里选搜索接口，选好后 `web_search` 会自动走它。

## 用户问有哪些模型

- 轨 A 且配了 OpenRouter：`curl -s --max-time 10 <apiBase>/models`，Windows 上用 `curl.exe`，列出前几个。
- 其他情况：模型在 App 的机器人设置里选。

## 启动本机服务的说明

用户想用轨 A 时给出这些步骤。你不要代为安装，也不要代为配置 Key：

1. 克隆 `https://github.com/guy-hartstein/company-research-agent`。
2. 在目录里安装依赖：`pip install -r requirements.txt`。
3. 按项目的 README 配好 Tavily 和模型的 Key。
4. 启动：`uvicorn application:app --host 127.0.0.1 --port 8000`。

没有启动也不影响使用，这个 Bot 会用兼容模式跑同样的流程。
