---
name: oss-upload
description: >-
  【OSS上传skill】阿里云 OSS 存图与 Cloud Agent 跨境上传排障。涵盖 oss-upload.sh、封面永久链、
  签名 URL、上传超时根因（美西 Agent → 北京 Bucket）与正确重试策略。
  当用户说 OSS 慢/上传失败/超时、发图上传、oss-upload、封面入库时必须参考本 skill。
---

# OSS 上传 Skill（Cloud Agent 必读）

本仓库图片/成片对象一律经 `bash scripts/oss-upload.sh` 上传。风水竖版成片对用户只发实验室 / **HTTPS** 预览链（`https://39.106.179.17.sslip.io/`；勿发 HTTP 裸 IP），**不要**只丢 OSS 裸链、**不要**聊天塞视频附件。约定见 `docs/cloud-hosting.md`、`.cursor/rules/image-preview-delivery.mdc`。图文 / tuwen 出图已废弃。


## 0. 基本用法

```bash
# 普通图 → 私有 + 12h 签名 URL（stdout；勿贴进对话框预览）
bash scripts/oss-upload.sh <local.png>

# 封面 / 入库长期图 → __cover_keep__ + public-read 永久 URL
bash scripts/oss-upload.sh --cover <cover.png>
bash scripts/oss-upload.sh --cover <graphic-page-01.png>   # 社媒 image_previews 也常用永久链

# 预览 HTML / 临时公开对象（非封面；可被 14h 清理或用户确认后删除）
bash scripts/oss-upload.sh --public <preview.html>

# 非社媒预览页（推荐）：生成 HTML 并上传，stdout 仅 HTML URL
node scripts/make-oss-preview-html.mjs --title "预览" --image a.png --image b.png

# 跳过上传前 14h 清理（批量连传时建议）
OSS_SKIP_CLEANUP=1 bash scripts/oss-upload.sh --cover <file>
```

对用户预览：**禁止**只丢 OSS 裸链；风水成片发实验室/HTTPS；HTML 预览页仅强烈要求或非社媒例外（见 `.cursor/rules/image-preview-delivery.mdc`）。


禁止绕过脚本直接 `ossutil cp`（会漏清理、封面标记、超时/stat 兜底）。

## 0. 全新 VM：ossutil 自动安装

新的 Cloud Agent VM 不带 `ossutil`。`oss-upload.sh` 发现缺失时会自己下载安装到 `~/.local/bin/ossutil`（可用 `OSSUTIL_VERSION` 指定版本、`OSSUTIL` 指定路径），无需手工准备。

**注意**：`oss-upload.sh` 正在跑时**不要编辑它**。bash 按字节偏移增量读脚本，改动会让后续调用跳到错误分支（实测报 `local_dir: unbound variable`，且 URL 已打印、退出码却非 0，容易误判上传失败并留下孤儿对象）。要改脚本先等批量上传结束。

## 1. Cloud Agent 上传慢：根因（已实测）

| 项 | 事实 |
| --- | --- |
| Agent 出口 | AWS **us-west-2（Oregon）** |
| Bucket | **oss-cn-beijing**（华北2） |
| 路径 | 美西 → 北京公网，跨境高延迟 |
| 有效吞吐 | 约 **20–40 KiB/s**（含等响应）；2.7MB PNG 单次成功约 **150s** |
| 1KB | ~1s 成功 |
| 128KB / 512KB | 约 7s / 16s 可成功 |
| ~3MB 默认参数 | 易 `read tcp … i/o timeout` |

### 为何「进度 100%」却仍卡数分钟？

1. `ossutil` 进度里的 `100%` + `done:(0 objects)` 只表示**本地侧字节已投递**，不等于服务端 ACK。
2. 默认 **`--read-timeout 20`**、**`--retry-times 10`**：单次等响应最多 ~20s 就超时，再重试最多 10 次 → 墙钟常到 **3–5 分钟**。
3. 3MB 按 ~30KiB/s 需要 **~90s+** 才能跑完一轮；默认 20s 读超时**单次根本不够**，只能靠多次重试碰运气。
4. 传输加速 `oss-accelerate`：**当前 Bucket 未开通**（会报 `Transfer Acceleration is not configured`）。
5. 偶发：某次重试其实已写入成功，客户端仍报 timeout → **必须 `stat` 确认**，不能只看退出码。

### 正确策略（脚本已内建，Agent 也要遵守）

1. 使用加长的 `read-timeout` / 合理 `retry-times`（见 `scripts/oss-upload.sh`）。
2. `cp` 非 0 时：对目标 key 做 `stat`；`Content-Length` 与本地文件一致则视为成功并继续签 URL / 回永久链。
3. 多张连传：`OSS_SKIP_CLEANUP=1`，清理只做一次或放批量末尾。
4. 不要并行狂打 PutObject 而不做失败兜底；优先串行 + stat。
5. 长期方案（需人工改云配置，Agent 不可自作主张开通）：Bucket 开 **传输加速**，或把常用素材放到离 Agent 更近的区域（产品决策）。

## 2. 与图文交付相关的易混坑

- **「第二张下半截没了」**：先查社媒预览条容器比例。预览条为一行两列 `aspect-[9/16]` + `object-cover`（格内宽撑满、高度超出裁切）；若误用 `aspect-[3/4]` 会裁掉 9:16 下半截。不要先假定导出缺页。
- **封面正文像黑体**：Cloud Agent 环境常无系统宋体；用本地 `NotoSerifSC-*.ttf` + `ensure-noto-serif-sc.sh`，导出失败勿静默回退。
- **改 markdown 后高亮全丢**：blockId 会变；需按正文 remap 或重新 `era_apply_highlights(replace: true)`。

## 3. 自检命令

```bash
# 出口地域
curl -s https://ipinfo.io/json | head

# 单次大图（应在 ~3 分钟内成功，勿用默认 20s 读超时）
OSS_SKIP_CLEANUP=1 bash scripts/oss-upload.sh --cover /path/to/2-3mb.png

# timeout 后确认是否已落盘
~/.local/bin/ossutil stat oss://agent-17718139319/era/assets/<key>
```
