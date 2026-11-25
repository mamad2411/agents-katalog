---
name: actual-setup
description: Set up Actual Computer (actual.inc) inference in Hermes.
version: 2.0.0
author: shl0ms + Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [actual, actual-inc, provider, local-inference, relay, gguf, setup]
    category: devops
---

# 实际计算机配置技能

该技能用于将[actual.inc](https://actual.inc)（Actual Computer）设置为Hermes推理提供者。Actual能够将用户的自有硬件转化为私有推理集群，并通过两种方式提供兼容OpenAI的API：一种是通过`https://api.actual.inc`提供的端到端加密托管中继服务（需使用`ac_`密钥进行身份验证）；另一种则是通过`http://127.0.0.1:8080`提供的本地设备守护进程服务（在本地回环连接下无需身份验证）。该技能不会自动为用户安装Actual守护进程——设备授权流程需要用户通过浏览器操作。

## 适用场景

- 用户希望将actual.inc作为推理提供者使用（无论是云端中继还是本地部署）。
- 用户拥有`ac_`密钥，希望让Hermes请求通过其Actual集群处理。
- 用户希望利用Actual守护进程实现完全在本地设备上进行的推理。
- 故障排查：遇到难以理解的400错误或空数据流问题时。

## 先决条件

- Hermes 提供了**一流的 `actual` 提供商支持**（提供商 ID 为 `actual`，别名包括 `actual-computer`、`actualcomputer`、`aci`）。请勿在当前版本的 Hermes 中将 Actual 配置为 `custom_providers` 或 `providers.actual.*` 类型的条目——内置的提供商已拥有该名称，并能自动处理基础 URL 的标准化、Responses 传输方式以及本地无认证功能。
- 中继模式：需要一个 Actual 账户，以及从 https://actual.inc/user/keys 获取的 `ac_` 格式的推理密钥。
- 本地模式：用户需先安装守护进程（执行命令 `curl -fsSL "https://actual.inc/install" | bash`），然后通过运行一次 `actual` 命令并打开浏览器中生成的 `https://actual.inc/device?code=...` 链接来完成设备授权。只需将该链接转发给用户并等待即可——绝不可伪造邮箱或代为授权。验证码有效期为 5 分钟，如需重新获取验证码，请再次运行 `actual` 命令。

## 运行方式

### 中继/API 模式

1. 将密钥放入 `.env` 文件中（仅存放敏感信息，切勿放入 config.yaml 文件）：
   在 `~/.hermes/.env` 文件末尾添加 `ACTUAL_API_KEY=ac_...`。
2. 使用 `terminal` 命令验证密钥并查找可用模型：
   ```bash
   curl -s https://api.actual.inc/v1/models -H "Authorization: Bearer $ACTUAL_API_KEY"
   ```
3. 选择提供商与模型：
   ```bash
   hermes config set model.provider actual
   hermes config set model.default "MODEL_ID_FROM_DISCOVERY"
   ```
4. 验证端到端流程：
   ```bash
   hermes chat -Q -q "Reply with exactly: ACTUAL_OK" --provider actual -m MODEL_ID
   ```

### 本地模式

1. 用户已安装并授权了守护进程（详见前提条件）。
2. 下载并加载模型（授权后只需执行一次该操作即可）。
   ```bash
   actual models search "qwen2.5 0.5b instruct gguf" --limit 8 --no-prompt
   # Downloads REQUIRE an explicit quantization (409 ambiguous_model_download otherwise):
   actual models download "Qwen/Qwen2.5-0.5B-Instruct-GGUF/Q4_K_M"
   actual models list        # note the INSTALLED name (differs from download id)
   actual models load "qwen2.5-0.5b-instruct-q4_k_m"   # load by installed name
   ```
3. 将 Hermes 指向该守护进程。若将 `ACTUAL_BASE_URL` 设置为回环主机地址，系统会自动将内置提供程序切换至本地无需认证的模式——无需任何密钥：只需在 `~/.hermes/.env` 文件中添加 `ACTUAL_BASE_URL=http://127.0.0.1:8080`，随后即可。
   ```bash
   hermes config set model.provider actual
   hermes config set model.default "INSTALLED_MODEL_NAME"
   ```
4. 验证（工具集已精简——详情参见下文的上下文窗口相关问题）：
   ```bash
   hermes chat -Q -q "Reply with exactly: LOCAL_OK" --provider actual -m INSTALLED_NAME -t file,web
   ```

## 快速参考

| 项目 | 值 |
|---|---|
| 托管中继 | `https://api.actual.inc/v1`（会自动从原始主机地址进行标准化处理） |
| 本地守护进程 | `http://127.0.0.1:8080/v1`（回环地址无需身份验证） |
| 密钥环境变量 | `ACTUAL_API_KEY`（格式为 `ac_...`） |
| 基础 URL 环境变量 | `ACTUAL_BASE_URL`（使用回环主机时即进入本地无认证模式） |
| 提供商 ID/别名 | `actual` / `actual-computer`、`actualcomputer`、`aci` |
| 传输方式 | 响应 API（`codex_responses`）——为内置功能，不可被覆盖 |
| 集群绑定 | 通过 config.yaml 中的 `providers.actual.extra_headers` 设置 `X-Cluster-ID` 请求头 |
| 模型大小参考 | 0.5B Q4_K_M 级模型大小约 470MB（小型模型），7-8B Q4_K_M 级模型大小约 4.5GB（常用模型），32B 级模型大小约 20GB |

## 常见问题

1. **推理难度设置陷阱（作为一级供应商，Hermes 已自动处理此问题。）**
   Actual 的 SGLang/vLLM 后端仅支持 `none/low/medium/high/max` 这些取值；
   若使用 `xhigh`/`ultra` 设置，将会返回含义不明的错误信息：
   `Expecting value: line 1 column 1 (char 0)`（实际上是封装后的 HTTP 400 错误）。内置供应商会在传输过程中将 `xhigh` 自动转换为 `high`，将 `ultra` 自动转换为 `max`。如果在旧版本的 Hermes 中仍会出现 400 错误，可在 config.yaml 中为特定模型设置上限，例如：`agent.reasoning_overrides.<model>: high`。
2. **小型本地模型中的上下文窗口溢出问题。** Hermes的默认工具集包含约26k个令牌的架构信息，以及约9k个令牌的系统提示词。当加载上下文长度为32k的模型时，会在第一轮对话之前就出现溢出现象，此时llama.cpp系列服务器仅会返回`data: [DONE]`这样的简单响应——而Hermes则会报告“Provider returned an empty stream with no finish_reason”。这并非SSE协议的缺陷。解决方案包括：限制可使用的工具类型（如使用`-t file,web`选项），为模型设置更大的`n_ctx`值，或选择上下文长度不低于64k的模型以支持完整工具集。相关问题追踪编号为#51448（请勿新建问题，可在该编号下附上相关证据）。另有类似但不同的问题编号为#65631（HTTP-200状态码下的SSE流却携带400错误），以及#56516（仅输出推理过程的流）。

3. **下载的模型标识与已安装名称不一致的问题。** `actual models download`功能在未指定量化格式时会尝试从`repo/QUANT`路径下载模型，从而导致409冲突错误；而`actual models load`功能则会根据“实际模型列表”中的已安装名称来加载模型。

4. **推理型模型返回空内容的问题。** GLM/Qwen系列的推理版本会将思考过程输出到单独的`reasoning`字段中，因此可能会将有限的`max_tokens`额度全部用于推理过程。在判定模型故障之前，建议先为这类模型设置较高的`max_tokens`值。

5. **请勿创建名为“actual”的自定义提供者。** 在早期版本的安装指南中（在Hermes正式支持此类配置之前），人们会使用`providers.actual.*`这样的配置块。但在当前版本的Hermes中，内置提供者的名称具有优先权，过时的自定义配置块要么会被忽略，要么会导致冲突。建议删除这些旧配置块，改用上述基于环境变量和`model.provider`的配置方式。

## 验证

```bash
# Relay:
hermes chat -Q -q "Reply with exactly: ACTUAL_OK" --provider actual -m MODEL
# Local (small model — reduced toolset):
hermes chat -Q -q "Reply with exactly: LOCAL_OK" --provider actual -m MODEL -t file,web
# Provider status (local no-auth shows key_source=local-offline):
hermes status
```

对于其他兼容 OpenAI 的客户端（例如 OpenCode），请参阅 `references/opencode.md`。
