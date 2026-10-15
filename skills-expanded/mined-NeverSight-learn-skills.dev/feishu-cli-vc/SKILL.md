---
name: feishu-cli-vc
description: >-
  飞书视频会议与妙记操作。搜索历史会议记录、获取会议纪要和逐字稿、查看妙记信息。
  当用户请求"搜索会议"、"会议记录"、"会议纪要"、"逐字稿"、"妙记"、"meeting"、
  "vc search"、"minutes"、"查看最近的会议"时使用。
  也适用于：用户想了解某次会议的内容、获取会议总结、下载会议逐字稿等场景。
user-invocable: true
allowed-tools: Bash, Read
---

# 飞书视频会议与妙记

搜索历史会议记录、获取会议纪要和逐字稿、查看妙记基础信息。

> **feishu-cli**：如尚未安装，请前往 [riba2534/feishu-cli](https://github.com/riba2534/feishu-cli) 获取安装方式。

## 前置条件

- **认证**：需要有效的 App Access Token（环境变量 `FEISHU_APP_ID` + `FEISHU_APP_SECRET`，或 `~/.feishu-cli/config.yaml`）
- **权限**：应用需开通 `vc:room:readonly`（会议室只读）、`vc:meeting:readonly`（会议记录只读）、`minutes:minutes:readonly`（妙记只读）
- **验证**：`feishu-cli auth status` 确认认证状态正常

## 命令速查

### 搜索历史会议

搜索飞书视频会议的历史记录，支持按时间范围、会议号、会议状态过滤。

```bash
feishu-cli vc search [选项]
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `--start` | string | 起始时间（Unix 秒级时间戳） |
| `--end` | string | 结束时间（Unix 秒级时间戳） |
| `--meeting-no` | string | 会议号精确匹配 |
| `--meeting-status` | int | 会议状态（1=进行中，2=已结束） |
| `--page-size` | int | 每页数量（默认 20） |
| `--page-token` | string | 分页 token（上一页返回） |
| `-o json` | string | JSON 格式输出 |

### 获取会议纪要

获取指定会议的纪要内容（包含结构化摘要和逐字稿）。`--meeting-id` 和 `--minute-token` 二选一，互斥。

```bash
feishu-cli vc notes [选项]
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `--meeting-id` | string | 通过会议 ID 获取纪要（与 `--minute-token` 互斥） |
| `--minute-token` | string | 通过妙记 token 获取纪要（与 `--meeting-id` 互斥） |
| `-o json` | string | JSON 格式输出 |

### 获取妙记基础信息

获取妙记的元数据（标题、创建时间、时长、参与者等）。

```bash
feishu-cli minutes get <minute_token> [选项]
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `<minute_token>` | string | 妙记 token（必填，位置参数） |
| `-o json` | string | JSON 格式输出 |

## 使用示例

```bash
# 搜索最近一周的会议（假设当前时间戳为 1711584000）
feishu-cli vc search --start 1710979200 --end 1711584000

# 搜索已结束的会议
feishu-cli vc search --meeting-status 2

# 按会议号精确查找
feishu-cli vc search --meeting-no "123456789"

# 分页获取更多会议记录
feishu-cli vc search --page-size 50

# 通过会议 ID 获取会议纪要
feishu-cli vc notes --meeting-id "6911xxxxx"

# 通过妙记 token 获取纪要
feishu-cli vc notes --minute-token "obcnxxxxx"

# 获取妙记基础信息
feishu-cli minutes get obcnxxxxx

# JSON 格式输出（便于程序解析）
feishu-cli vc search --meeting-status 2 -o json
feishu-cli minutes get obcnxxxxx -o json
```

## 典型工作流

### 查找某次会议并获取纪要

```bash
# 1. 搜索时间范围内的会议
feishu-cli vc search --start 1710979200 --end 1711584000 -o json
# → 找到目标会议的 meeting_id

# 2. 获取会议纪要
feishu-cli vc notes --meeting-id "<meeting_id>"
# → 输出会议摘要和逐字稿

# 3. 如果有妙记 token，也可以查看妙记详情
feishu-cli minutes get <minute_token>
```

## 权限要求

| 功能 | 所需权限 |
|------|---------|
| 搜索会议记录 | `vc:meeting:readonly` |
| 会议室信息 | `vc:room:readonly` |
| 获取妙记信息 | `minutes:minutes:readonly` |

## 注意事项

- **时间参数**：`--start` 和 `--end` 使用 **Unix 秒级时间戳**（非毫秒），可通过 `date +%s` 获取当前时间戳
- **meeting-id vs minute-token**：`vc notes` 的两个参数互斥，不能同时使用；meeting-id 来自 `vc search` 的结果，minute-token 来自妙记 URL 或 `minutes get` 返回
- **妙记 token 来源**：飞书妙记 URL 格式为 `https://xxx.feishu.cn/minutes/<minute_token>`，从 URL 中提取即可
- **数据时效**：会议记录和妙记需要会议结束后一段时间才能查询到，实时会议无法获取纪要
- **权限申请**：`vc:meeting:readonly` 和 `minutes:minutes:readonly` 需要在飞书开放平台单独申请开通
