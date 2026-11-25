---
title: "EasyImage Upload"
type: skill
tags: [easyimage, image-host, upload, api, curl, python, thumb.php, resize]
created: 2026-10-22
updated: 2026-10-22
author: scriptsmay
status: active
---

# EasyImage Upload

通过 API 向自建 EasyImage 图床上传图片并取回直链的标准流程：接口契约、curl / Python 两种调用方式、用 `thumb.php` 按需派生展示尺寸、错误码对照与凭据安全约定，供脚本与自动化任务（包括 AI agent）直接复用。

Upload images to a self-hosted EasyImage instance via its API and get back a direct URL: the exact request contract, curl and Python recipes, on-demand derived sizes via `thumb.php`, an error-code map, and credential-handling rules for scripts and AI agents.

## 为什么需要这个技能 / Why

EasyImage 的上传接口有三处与常见图床 API 的直觉相反，凭经验猜参数必踩坑（均经实测）：

1. 文件字段名是 `image`，不是更常见的 `file` —— 猜错直接返回「没有选择上传的文件」
2. token 走 `multipart/form-data` 表单字段，不走 `Authorization` 请求头 —— 放请求头返回 `Token Error`
3. 图床设了最小图片尺寸阈值，1×1 之类的测试图会被拒 —— 联调时容易误判成接口故障

The API contradicts common assumptions in three places — the file field is `image` (not `file`), the token is a form field (not an `Authorization` header), and tiny test images are rejected by a minimum-size rule. Guessing any of these wastes a debugging round.

## 关键结论 / Key Facts

| 项目 | 值 |
| :--- | :--- |
| 接口地址 | `https://<YOUR_EASYIMAGE_HOST>/api/index.php` |
| 请求方法 | `POST`，`multipart/form-data` |
| 文件字段名 | `image`（**不是** `file`） |
| 认证字段 | `token` 作为**表单字段**传递（**不是** `Authorization` 请求头） |
| 成功判定 | `result == "success"` 且 `code == 200`，直链取返回 JSON 的 `url` 字段 |
| 派生展示尺寸 | `GET /app/thumb.php?img=<原图路径>&w=<宽>[&h=<高>]&q=<质量>`（见步骤 5） |
| 适用版本 | EasyImage 2.x（上传契约实测 2.8.5，派生尺寸实测 2.8.6） |

## 前置条件 / Prerequisites

- 一台已部署的 EasyImage 2.x 实例，且管理员已在后台开启 API 并生成 token（token 在图床管理后台查看/重置）
- 待上传图片为图床允许的格式与大小，且尺寸不低于图床的最小宽高阈值（见故障排查）
- 调用方能访问图床域名（自建实例常配合反向代理/内网访问，按自己的部署调整）

## 变量 / Variables

| 占位符 / 环境变量 | 含义 | 说明 |
|---|---|---|
| `<YOUR_EASYIMAGE_HOST>` / `EASYIMAGE_BASE_URL` | 图床根地址，如 `https://img.example.com` | 接口路径固定为 `/api/index.php`，根地址不要带尾随路径 |
| `<EASYIMAGE_TOKEN>` / `EASYIMAGE_TOKEN` | API token | 只放环境变量或权限 600 的本地文件，**不进仓库、不进日志** |
| `EASYIMAGE_TOKEN_FILE` | token 文件路径（可选） | 文件内容为单行 token；读取时必须去掉尾随换行（见避坑 4） |

## 给 Agent 的执行约定 / Agent Guide

AI agent 或自动化脚本调用本技能时，按以下顺序执行，不要跳步：

1. **先备齐变量再发请求**：从环境变量 `EASYIMAGE_BASE_URL` / `EASYIMAGE_TOKEN`（或 `EASYIMAGE_TOKEN_FILE` 指向的文件）解析图床地址与 token。缺任何一项就停下来向用户索取，不要猜地址、不要用示例域名发真实请求。
2. **全程不回显凭据**：token 不打印、不写日志、不拼进可分享的命令记录；返回结果里的 `del`（删除链接）同等对待——默认丢弃，只有用户明确要求且通道私密时才可给出。
3. **上传前自检**：确认文件存在、非空、格式受支持、尺寸不是 1×1 之类的占位图。联调要用测试图时，用 ≥200×200 的真实图片。
4. **优先用参考脚本**：`references/easyimage_upload.py` 已处理字段名、token 去换行、成功判定与 `del` 脱敏；手写 curl 时逐字对照下文示例，不要凭记忆改字段名。
5. **严格判定成功**：只有 `result == "success"` 且 `code == 200` 才算成功，再取 `url` 作为产物；其余一律按故障排查表处理，不要把失败响应当成功继续后续步骤。
6. **失败先查表再重试**：对照错误码定位是参数问题（改参数）还是网络问题（可重试 1 次）；参数错误重试多少次都不会成功，不要盲目循环重试。
7. **交付只给直链**：向用户汇报时给出 `url`（需要时附 `thumb`），不附 `del`、不附 token、不用真实域名/token 回填本文档示例。

## 步骤 / Steps

### 1. 准备 token

```bash
export EASYIMAGE_BASE_URL="https://<YOUR_EASYIMAGE_HOST>"
# 方式 A：直接放环境变量
export EASYIMAGE_TOKEN="<EASYIMAGE_TOKEN>"
# 方式 B：放 600 权限文件，读取时去掉尾随换行
TOKEN=$(tr -d '\n' < /path/to/easyimage-token)
```

### 2. 上传（curl）

```bash
curl -sS -m 20 -X POST "$EASYIMAGE_BASE_URL/api/index.php" \
  -F "image=@/path/to/image.png" \
  -F "token=$EASYIMAGE_TOKEN"
```

### 3. 上传（Python 参考脚本，标准库零依赖）

```bash
python3 references/easyimage_upload.py /path/to/image.png
# 成功时 stdout 只输出图片直链，可直接管道给后续步骤
# --json 输出完整响应 JSON（del 字段默认脱敏，加 --show-del 才显示）
```

脚本同样读取 `EASYIMAGE_BASE_URL` / `EASYIMAGE_TOKEN` / `EASYIMAGE_TOKEN_FILE`，逻辑与本文档契约一致：手写 multipart、token 去空白、严格成功判定、失败时退出码非 0 且错误信息只写 stderr。

### 4. 解析返回

成功返回 JSON（`url` 即图片直链）：

```json
{
  "result": "success",
  "code": 200,
  "url": "https://<YOUR_EASYIMAGE_HOST>/i/1/2026/01/01/example-1.png",
  "srcName": "example",
  "thumb": "https://<YOUR_EASYIMAGE_HOST>/app/thumb.php?img=/i/1/2026/01/01/example-1.png",
  "del": "https://<YOUR_EASYIMAGE_HOST>/app/del.php?hash=<DELETE_HASH>",
  "id": 1,
  "message": "success"
}
```

字段含义：

- `url` — 图片直链（主产物，可直接访问）
- `srcName` — 原始文件名（不含扩展名）
- `thumb` — 缩略图链接
- `del` — 删除链接（内含删除凭证，**等同密码，勿外泄、勿入公开文档/日志/仓库**）
- `id` — 图床侧的图片序号

### 5. 派生展示尺寸（推荐）

原图常是 2000–3000px、1 MB 以上，而卡片/列表往往只需要固定宽度。EasyImage 内置的 `thumb.php` 可以按需裁剪缩放：不用重新上传，也不用在本地跑图像处理，原图保留即可随时换尺寸。

**接口契约**

| 项目 | 值 |
| :--- | :--- |
| 接口地址 | `GET https://<YOUR_EASYIMAGE_HOST>/app/thumb.php` |
| `img` | 原图 `url` 的 pathname，必须以 `/i/` 开头（如 `/i/1/2026/01/01/example-1.jpg`），**不要**传完整域名 |
| `w` | 目标宽度（px）；只给 `w` 时高度按原比例 |
| `h` | 可选；与 `w` 同时给定时输出正好 `w×h`（裁剪填充，不保持原比例） |
| `q` | JPEG 质量 1–100，展示图建议 80–82 |
| 响应 | `image/jpg`，带 `Access-Control-Allow-Origin: *` 与 `cache-control: max-age=7200, must-revalidate` |

**常用档位（实测数据）**

| 用途 | 参数 | 输出 | 体积 |
| :--- | :--- | :--- | :--- |
| 卡片主图（1080×1440 画布） | `w=1080&q=82` | 1080×1440（3:4 源图） | ≈139 KB（源图 2268×3024 / 1.28 MB） |
| 列表缩略图（3:4） | `w=258&h=344&q=80` | 258×344 | ≈15 KB |
| 轻量展示 / 种子数据 | `w=900&q=80` | 900 宽等比 | ≈96 KB |

**派生 URL 生成（JS）**

```js
function buildDerivedUrls(originalUrl, baseUrl) {
  const { pathname } = new URL(originalUrl);
  if (!pathname.startsWith('/i/')) return null; // 非图床上传路径无法派生
  return {
    card: `${baseUrl}/app/thumb.php?img=${pathname}&w=1080&q=82`,
    thumb: `${baseUrl}/app/thumb.php?img=${pathname}&w=258&h=344&q=80`,
  };
}
```

**落库约定（素材/内容表）**

- `url` — 派生后的展示图（卡片用 1080 宽）
- `thumb_url` — 258×344 派生缩略图
- `source_url` — 上传返回的原图直链，**必须单独保留**：派生链接依赖原文件存在，换尺寸只改参数，不用重新上传

**注意**

- 只有 `/i/` 路径能走 `thumb.php`；外部直链无法派生，回落到原图。
- 源图缺失时 `thumb.php` 不返回 404，而是 **HTTP 200 + PNG 占位图**（实测 274×141）；批量生成后要抽查 `content-type` 与实际尺寸。
- 同一路径替换原图后派生 URL 不变，可能命中 2 小时缓存；需要立即生效请换文件名/路径。

## 故障排查 / Troubleshooting

| 现象 / 返回 | 原因 | 处理 |
|---|---|---|
| `{"result":"failed","code":204,"message":"没有选择上传的文件"}` | 文件字段名用成了 `file` | 改为 `image` |
| `{"result":"failed","code":202,"message":"Token Error"}` | token 放进了 `Authorization` 头，或 token 本身不对/带了换行 | token 改走表单字段 `token`；从文件读取时 `tr -d '\n'`；仍失败去后台核对 token |
| `{"result":"failed","code":400,"message":"图片高度太小。"}` | 图片尺寸低于图床最小阈值（如 1×1 测试图） | 换 ≥200×200 的真实图片；或在图床后台调整最小尺寸设置 |
| 超时 / 连接失败 | 图床不可达、反向代理或网络问题 | 先单独 `curl -I $EASYIMAGE_BASE_URL` 确认站点可达，再重试 1 次 |
| 返回非 JSON | 打到了错误路径或被代理拦截页替换 | 确认路径为 `/api/index.php` 且根地址无多余前缀 |
| `thumb.php` 返回 200，但图片是 274×141 的 PNG 占位图 | `img` 指向的源图不存在或已被删除 | 用原图直链核对路径；确认原图未删，派生图只是视图，不能替代原图 |

## 避坑 / Pitfalls（均经实测踩出）

1. **文件字段名是 `image`，不是 `file`**：用 `file` 返回 code 204。
2. **token 走表单字段，不走 Authorization 头**：用请求头返回 code 202 `Token Error`。
3. **图片尺寸不能太小**：1×1 像素图返回 code 400；200×200 正常通过。
4. **token 尾随换行必须去除**：token 文件末尾的换行拼进表单会带上多余字符导致校验异常，读取时 `tr -d '\n'`（或在代码里 `.strip()`）。
5. **删除链接是敏感凭据**：`del` 字段内的 hash 可直接删除对应图片，不要写入公开文档、日志或代码仓。
6. **派生图依赖原图存在**：`thumb.php` 只是视图，原图删了派生链接就变成占位图；落库时把原图单独存到 `source_url`，不要只留派生 URL。
7. **派生图不能只看 HTTP 状态码**：源图缺失也返回 200，必须校验 `content-type` 和实际像素尺寸。
8. **同路径换图有缓存**：派生响应缓存 2 小时，替换原图后想立即生效就换文件名/路径。

## 检查清单 / Checklist

- [ ] 图床地址与 token 来自环境变量/本地凭据文件，文档与代码里只有占位符？
- [ ] 文件字段名用 `image`，token 用表单字段 `token` 传递？
- [ ] 从文件读 token 时已去尾随换行？
- [ ] 上传图片尺寸满足最小阈值（联调不用 1×1 测试图）？
- [ ] 以 `result == "success"` 且 `code == 200` 判定成功，再从 `url` 取直链？
- [ ] `del` 删除链接未写入公开位置、未随结果转发？
- [ ] 展示图用 `/app/thumb.php` 派生（`w` / `h` / `q`），原图直链另存 `source_url`？
- [ ] 派生图只从 `/i/` 路径生成，并抽查过实际尺寸（防 200 占位图）？

## 参考实现 / Reference

`references/easyimage_upload.py` — 通用上传脚本（Python 标准库零依赖）：从环境变量读地址与 token，输出直链，失败映射错误信息，`del` 默认脱敏。

## 实测记录 / Field Notes

- 2026-10-22（EasyImage 2.8.5）：按本文档契约完成 curl 与 Python 两条路径的上传验证，返回 `url` 可直接访问；上文 204 / 202 / 400 三个错误码均为同日实测踩出后定位，非文档转述。
- 2026-10-22（EasyImage 2.8.6）：`/app/thumb.php` 派生尺寸实测——源图 2268×3024 / 1.28 MB → `w=1080&q=82` 得 1080×1440 / 139 KB，`w=258&h=344&q=80` 得 258×344 / 15 KB，`w=258&h=258` 得 258×258（确认 `w+h` 为裁剪填充）；源图缺失返回 200 + 274×141 PNG 占位图；`/i/` 与 `/app/thumb.php` 均带 `Access-Control-Allow-Origin: *`（canvas 可直接取图）。
