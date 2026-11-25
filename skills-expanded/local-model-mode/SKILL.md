---
name: local-model-mode
description: 帮用户给 cccodroid 的「端侧小模型」配置自定义模式（~/.cccodroid/local-mode.json）：选工具、写系统提示、调 llama-server 参数，并在本机实测效果。用户说要配置/调教端侧模型、本地小模型自定义模式时使用。
---
<!-- cccodroid:managed —— 删掉这一行，应用升级时就不会覆盖你改过的版本 -->

# 端侧小模型的自定义模式

cccodroid 用 llama.cpp 在手机上跑 GGUF 小模型，内置只有「聊天」模式（不给工具，提示约 70 token）。
「自定义模式」是留给用户自己折腾的插口：网关每条消息都会现读下面这个文件。

## 配置文件

路径：`~/.cccodroid/local-mode.json`（`~` 是 cccodroid 的 home，即 `$HOME`）

```json
{
  "label": "命令执行",
  "tools": "Bash",
  "systemPrompt": "You are a command executor ...",
  "llamaArgs": ["--temp", "0.2"],
  "ctx": 8192
}
```

| 字段 | 含义 | 默认 |
|---|---|---|
| `label` | 设置页上显示的名字（≤40 字） | 自定义 |
| `tools` | 传给 `claude --tools`，逗号分隔，如 `"Bash"`、`"Bash,Read"`；空串 = 不给工具 | 空 |
| `systemPrompt` | 追加到系统提示末尾，**替换**内置那句身份说明（≤20000 字） | 内置身份句 |
| `llamaArgs` | 追加到 llama-server 命令行末尾，同名参数覆盖网关默认（不能改 `-m --host --port -np`） | 无 |
| `ctx` | 上下文长度（512–262144），覆盖网关按内存给的默认值 | 按内存 |

claude 始终以 `--bare` 运行（极简系统提示，不读 CLAUDE.md、不加载技能/MCP）。
上下文压缩线对端侧不生效。

## 生效与恢复

- 设置 → 模型服务 → 端侧小模型 → 模式选「自定义」，下一条消息生效。
- 文件写坏时设置页会显示错误，并自动回落聊天模式。
- 删掉文件 = 回到只有聊天。
- 换了 `llamaArgs` / `ctx`，网关会自动重启 llama-server。

## 网关默认的 llama-server 参数

```
-m <模型> --host 127.0.0.1 --port 8811 -c <按内存> -np 1 -t <大核数> --jinja --cache-reuse 256 --no-webui --api-key-file ~/.cache/llama-api-key
GPU 驱动装了：-ngl 99（全部层放 GPU）；没装：-dev none。想强制 CPU 就在 llamaArgs 里写 ["-dev", "none"]
```

常用可调：`--temp`、`--top-k`、`--top-p`、`--min-p`、`--repeat-penalty`、`-ub`（GPU 上崩时试 `-ub 128`）、`--chat-template-file`。

## 怎么测（不用开界面）

模型目录：`/sdcard/cccodroid/models/`（扩展页 llama-cpp 组件下能一键下载 26 个常见模型，也能贴 .gguf 直链）。先在设置页发一条消息让网关拉起服务（或自己另起一个端口），然后：（网关起的服务要密钥，在 `~/.cache/llama-api-key`；自己另起的没加 `--api-key` 就随便填）

```sh
cd 某个测试目录
env ANTHROPIC_BASE_URL=http://127.0.0.1:8811 ANTHROPIC_API_KEY="$(cat ~/.cache/llama-api-key)" \
  claude --model <模型 id> -p "统计一下这里有几个文件" \
  --bare --tools Bash --permission-mode bypassPermissions \
  --append-system-prompt "$(cat prompt.txt)" \
  --output-format stream-json --verbose | grep -o '"name":"Bash","input":{[^}]*'
```

看 stream-json 里有没有真正的 `tool_use`，而不只看最终文字——小模型最常见的失败是把命令**写成文字**而不是调用工具。
同一个问题至少跑 3 遍再下结论（采样有随机性）。

## 已知实测结论（Snapdragon 8+ Gen 1，Qwen2.5 Instruct Q4_K_M）

- 0.5B / 1.5B：基本撑不起工具调用；1.5B 只给 Bash 时 6 题里 5 题把命令写成文字，剩下一题对所有问题都回 `ls 文件名`。
- 3B：比 1.5B 稍好，但会对目录用 Read（EISDIR）、会选错命令；GPU 上可能 `vk::DeviceLostError`（网关只报错，不替你改；试 `-ub 128`、减少 `-ngl` 层数，或强制 CPU）。
- CPU 速度：3B 读提示约 14 token/s、生成约 10 token/s；1.5B 读提示约 28 token/s。带 Bash 工具时提示约 700 token，首字要等半分钟。
- 想让小模型干活，可以试：只给一个工具（`Bash`）、降温度（`--temp 0.2`）、在 systemPrompt 里写几组「问题 → 命令」示例、要求一句话回报结果。7B 以上模型效果会好很多，但手机内存和速度未必吃得消。

## 帮用户配置时

1. 先问清楚用途（聊天风格？翻译？跑命令？），再决定给不给工具。
2. 写好文件后，用上面的命令实测几遍，把结果（成功几次、耗时）告诉用户。
3. 提醒用户：在设置页把模式切到「自定义」。
