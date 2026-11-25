---
name: web-perf-audit
description: >
  审计并优化网页/站点的加载性能与交互响应性（Core Web Vitals: LCP/CLS/INP/TBT）。
  当用户提到"网站慢""首屏优化""Lighthouse 分数低""性能审计""图片/字体/JS 优化"
  或粘贴了一个网址想知道"为什么加载慢"时，都应主动使用本技能，即使用户没有明说
  "性能优化"四个字。
---

# Web Performance Audit Skill

基于 web.dev《Learn Performance》知识体系的全自动 Web 性能审计技能包。
多阶段流水线：SCAN → ANALYZE → SCORE → REPORT。
结果落盘为 JSON + Markdown，支持增量对比和 CI 集成。

## Pipeline Overview

```
SCAN                      ANALYZE                     SCORE              REPORT
─────                    ─────────                   ─────              ──────
fetch_metrics.py    ┌→ analyze_critical_path.py ┐
(Lighthouse/PSI)    ├→ check_resource_hints.py  ├→ score_and_report.py → audit-report.json
                    ├→ audit_images.py          │                       report.md
                    ├→ audit_fonts.py           │                       dashboard.html
                    └→ audit_js_bundles.js      ┘
                                                       diff_report.py
                                                       (CI/PR 对比)
```

## Prerequisites

在首次使用前，确认以下依赖可用：

```bash
# Node.js 依赖（Lighthouse + Puppeteer）
npm install -g lighthouse
npm install puppeteer  # 或在技能目录下 npm install

# Python 依赖（仅标准库 + urllib，无需额外安装）
# Python 3.8+ 即可
```

## Stage 1: SCAN — 抓取页面原始数据

**目标：** 获取 Core Web Vitals 原始指标和 Lighthouse 审计结果。

使用 `scripts/fetch_metrics.py`：

```bash
# 默认使用本地 Lighthouse CLI（推荐，无需 API Key）
python scripts/fetch_metrics.py <URL> --output-dir .web-perf

# 可选：使用 PageSpeed Insights API（获取 CrUX 真实用户数据）
python scripts/fetch_metrics.py <URL> --output-dir .web-perf --psi-key <YOUR_API_KEY>

# 桌面端策略
python scripts/fetch_metrics.py <URL> --output-dir .web-perf --strategy desktop
```

**输出文件：**
- `.web-perf/metrics.json` — 包含所有 CWV 指标和优化机会的原始数据

**关键指令：**
- 如果用户只提供了域名（如 `example.com`），自动补全为 `https://example.com`
- 如果 Lighthouse 未安装，提示用户运行 `npm install -g lighthouse`
- 如果目标 URL 是本地开发服务器（localhost），用 `--extra-lighthouse-flags` 跳过 TLS 检查

## Stage 2: ANALYZE — 分类审计

**目标：** 对页面进行 5 个维度的独立审计。可以并行运行。

### 2.1 关键渲染路径分析

```bash
python scripts/analyze_critical_path.py .web-perf/metrics.json -o .web-perf/critical-path.json
```

**检测内容：** 渲染阻塞 CSS/JS、关键请求链深度、DOM 大小、资源分布。

### 2.2 Resource Hints 审计

```bash
python scripts/check_resource_hints.py <URL> -o .web-perf/resource-hints.json
```

**检测内容：** preload/prefetch/preconnect/dns-prefetch 的使用是否合理、同步脚本、缺少维度的图片。

### 2.3 图片性能审计

```bash
python scripts/audit_images.py <URL> -o .web-perf/images.json
```

**检测内容：** 图片格式（WebP/AVIF）、srcset/sizes、懒加载、显式宽高、LCP 候选图片。

### 2.4 字体性能审计

```bash
python scripts/audit_fonts.py <URL> -o .web-perf/fonts.json
```

**检测内容：** font-display 设置、woff2 格式、字体 preload、字重数量、系统字体栈。

### 2.5 JS Bundle 审计

```bash
node scripts/audit_js_bundles.js <URL> --output .web-perf/js-bundles.json
```

**检测内容：** Coverage 数据（未使用 JS）、长任务、第三方脚本体积。

**并行执行：** 2.2-2.5 可以同时运行，互不依赖。

## Stage 3: SCORE — 加权评分

```bash
python scripts/score_and_report.py <URL> \
  --output-dir .web-perf \
  --metrics-file .web-perf/metrics.json \
  --critical-path-file .web-perf/critical-path.json \
  --resource-hints-file .web-perf/resource-hints.json \
  --images-file .web-perf/images.json \
  --fonts-file .web-perf/fonts.json \
  --js-file .web-perf/js-bundles.json \
  --audience dev \
  --format all
```

**评分权重：**

| 类别 | 权重 | 影响的主要 CWV |
|------|:----:|---------------|
| Metrics (Lighthouse Score) | 25% | 综合 |
| Critical Path | 20% | LCP, FCP |
| JS Bundles | 20% | TBT, INP |
| Images | 15% | LCP, CLS |
| Resource Hints | 10% | LCP, FCP |
| Fonts | 5% | LCP, CLS |
| Third Party | 5% | TBT |

**优先级排序规则：** Issue 按 CWV 影响面打分 (1-30)，映射为 P0 (≥20)、P1 (≥10)、P2 (<10)，不是按发现顺序。

## Stage 4: REPORT — 生成报告

**输出文件：**
1. `.web-perf/audit-report.json` — 结构化数据，供程序读取/CI 集成
2. `.web-perf/report.md` — 人类可读报告，按 P0→P1→P2 列出问题 + 修复代码
3. `.web-perf/dashboard.html` — 可视化仪表盘 (Chart.js)
4. `.web-perf/fingerprint.txt` — 内容指纹，供增量分析用

### --audience 模式

| 模式 | 特性 |
|------|------|
| `dev` | 完整报告 + 可复制粘贴的代码修复片段 + 技术引用路径 |
| `pm` | 摘要报告 + 评分 + 优先级排序 + 预计收益（无代码） |

## 增量分析机制

### 指纹缓存

每次审计会生成基于 CWV 值 + 资源摘要的 SHA256 指纹，保存到 `.web-perf/fingerprint.txt`。

二次审计时：
1. 如果指纹未变 → 跳过全流程，直接输出 "No significant changes detected"
2. 如果指纹变化 → 运行全流程，并在报告中附加 "与上次对比" 部分

### diff_report.py（CI/PR 场景）

```bash
python scripts/diff_report.py \
  .web-perf/before/audit-report.json \
  .web-perf/after/audit-report.json \
  --format both \
  -o .web-perf/diff-report.json
```

**CI 集成示例（GitHub Actions）：**

```yaml
- name: Performance Audit (PR)
  run: |
    # 在 PR 的 base 分支和 head 分支分别审计
    git checkout ${{ github.base_ref }}
    python scripts/fetch_metrics.py $URL -o .web-perf/before/
    git checkout ${{ github.head_ref }}
    python scripts/fetch_metrics.py $URL -o .web-perf/after/
    python scripts/diff_report.py .web-perf/before/audit-report.json .web-perf/after/audit-report.json
```

## .webperfignore

在项目根目录放置 `.webperfignore` 可以排除不可控资源：

```
# 排除第三方统计脚本
google-analytics.com
googletagmanager.com
facebook.net
doubleclick.net
hotjar.com
newrelic.com

# 排除 CDN 域名
cdnjs.cloudflare.com
unpkg.com

# 排除特定文件
*.min.js
*.min.css
```

## 参考知识库 (references/)

每个主题一个 md 文件，遵循统一结构：问题现象 → 检测方式 → 修复代码 → 预期收益。报告中的 issue 会引用对应的 reference 文件，确保每个建议都能追溯到 web.dev 的原理说明。

| 文件 | 覆盖主题 | 相关 Lighthouse 审计 |
|------|---------|---------------------|
| `references/critical-path.md` | 关键渲染路径、CSS/JS 阻塞 | render-blocking-resources, critical-request-chains, dom-size |
| `references/html-loading.md` | HTML 解析策略、script 属性、资源顺序 | — |
| `references/resource-hints.md` | preload/prefetch/preconnect/dns-prefetch | uses-rel-preconnect, uses-rel-preload |
| `references/image-performance.md` | 格式、响应式、懒加载、LCP 图片 | modern-image-formats, uses-responsive-images, offscreen-images |
| `references/video-performance.md` | 编码、poster、preload、GIF 替代 | efficient-animated-content |
| `references/font-performance.md` | font-display、子集化、预加载 | font-display |
| `references/js-performance.md` | 代码分割、长任务、Web Worker | unused-javascript, legacy-javascript, duplicated-javascript |
| `references/predictive-loading.md` | prefetch/prerender/SW precaching | — |

## 快速开始（一键全流程）

```bash
# 设置 URL
URL="https://example.com"
OUTDIR=".web-perf"

# Stage 1: SCAN
python scripts/fetch_metrics.py "$URL" --output-dir "$OUTDIR"

# Stage 2: ANALYZE（并行）
python scripts/analyze_critical_path.py "$OUTDIR/metrics.json" -o "$OUTDIR/critical-path.json" &
python scripts/check_resource_hints.py "$URL" -o "$OUTDIR/resource-hints.json" &
python scripts/audit_images.py "$URL" -o "$OUTDIR/images.json" &
python scripts/audit_fonts.py "$URL" -o "$OUTDIR/fonts.json" &
node scripts/audit_js_bundles.js "$URL" --output "$OUTDIR/js-bundles.json" &
wait

# Stage 3 & 4: SCORE + REPORT
python scripts/score_and_report.py "$URL" --output-dir "$OUTDIR" --format all
```

## 故障处理

| 问题 | 解决方案 |
|------|---------|
| Lighthouse CLI 超时 | 增加 `--extra-lighthouse-flags --max-wait-for-load=60000` |
| Puppeteer 无法启动 | 尝试 `npx puppeteer browsers install chrome` |
| 目标网站需要登录 | 先用浏览器登录，导出 cookies，传给 Lighthouse: `--extra-lighthouse-flags --extra-headers="Cookie: ..."` |
| Python 脚本报编码错误 | Windows 下设置 `$Env:PYTHONUTF8=1` 或 `export PYTHONUTF8=1` |
| 某些第三方脚本拖慢审计 | 在 `.webperfignore` 中添加对应域名，审计时会跳过 |
