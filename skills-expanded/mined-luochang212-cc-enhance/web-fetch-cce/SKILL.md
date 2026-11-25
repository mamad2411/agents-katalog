---
name: web-fetch-cce
description: 网页内容提取策略。当需要读取网页内容、爬取页面、提取文章正文、处理JS渲染页面、或绕过反爬限制时，必须使用此技能。三层工具选择：WebFetch（内置）→ Crawl4AI（JS渲染/反爬）→ 原生 Playwright（兜底降级）。
---

> 来自 [cc-enhance](https://github.com/luochang212/cc-enhance)。`-cce` 后缀表示此技能由 cc-enhance 项目安装，避免与本地同名技能冲突。

# Web Fetch

搜索拿到 URL 之后，把页面内容提取为 Claude 可读的格式。

## 工具选择

| 工具 | 适用场景 | 格式 |
|------|----------|------|
| `WebFetch` | 静态页面、文档、博客 | HTML → Markdown |
| Crawl4AI | JS 渲染、反爬、结构化提取 | Playwright → Markdown / JSON |
| 原生 Playwright | Crawl4AI 超时/被检测时的降级 | `inner_text` 纯文本 |

## 策略

1. **优先 `WebFetch`**。内置、<1s、零依赖。覆盖 90% 的页面。
2. **Crawl4AI 处理 JS 重/反爬页**。Markdown 质量好，`magic=True` 解微信。
3. **原生 Playwright 兜底**。当 Crawl4AI 超时（阮一峰）或被检测时，手动控制 `wait_until` 策略。

## 对比

| | WebFetch | Crawl4AI | 原生 Playwright |
|------|------|------|------|
| 速度 | <1s | 2-4s | 1-5s |
| JS 渲染 | 否 | 是 | 是 |
| 输出质量 | 可用 | 丰富 Markdown | 纯文本 |
| 反爬 | 否 | magic/undetected | 手动注入 |
| 灵活性 | 无 | 中 | 高（wait_until、stealth） |
| 适合 | 90% 日常 | JS 重/反爬页 | Crawl4AI 搞不定时 |

## 参考


- [references/crawl4ai.md](references/crawl4ai.md) — Crawl4AI 部署与使用、中国站点实测矩阵
- [references/playwright.md](references/playwright.md) — 原生 Playwright 降级方案

## 环境依赖

| 依赖 | 用途 | 安装方式 | 磁盘 | 必需 |
|------|------|----------|------|------|
| Python 环境 + Crawl4AI | JS 渲染、反爬绕过 | 见下方「Python 环境检测」 | ~300MB | 否 |
| 无（WebFetch 内置） | 静态页面首选，零依赖 | — | 0 | 否 |

### Python 环境检测

按以下顺序检查，任一项满足即可跳过安装：

1. `conda --version` → 已有 conda，直接用 conda 创建环境
2. `uv --version` → 已有 uv，用 `uv venv && uv pip install`
3. `python3 --version` → 已有 python3，用 `venv + pip`

若都没有，按优先级推荐安装：

- **首选**：[Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install/overview) — 跨平台、环境隔离好
- **备选**：[uv](https://github.com/astral-sh/uv) — 轻量快速、pip 兼容

安装后执行：

中国大陆使用镜像加速（腾讯云 / 阿里云二选一）：

```bash
# conda
conda create -n crawl4ai python=3.13 -y && conda activate crawl4ai
pip install -i https://mirrors.cloud.tencent.com/pypi/simple/ crawl4ai  # 腾讯云
pip install -i https://mirrors.aliyun.com/pypi/simple/ crawl4ai          # 阿里云
playwright install chromium

# uv
uv venv && source .venv/bin/activate
uv pip install -i https://mirrors.cloud.tencent.com/pypi/simple/ crawl4ai  # 腾讯云
uv pip install -i https://mirrors.aliyun.com/pypi/simple/ crawl4ai          # 阿里云
playwright install chromium

# venv
python3 -m venv venv && source venv/bin/activate
pip install -i https://mirrors.cloud.tencent.com/pypi/simple/ crawl4ai  # 腾讯云
pip install -i https://mirrors.aliyun.com/pypi/simple/ crawl4ai          # 阿里云
playwright install chromium
```
