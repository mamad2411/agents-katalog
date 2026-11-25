---
name: phone-playwright
description: Use when controlling, inspecting, automating, or building AI agents for Android or iOS mobile devices — using Playwright-style lazy locators, viewport-aware semantic distillation, auto-waiting actionability state machines, warm-cache fast dispatch, scroll_into_view, Chinese clipboard typing, or MCP stdio JSON-RPC mobile servers. Triggers: 手机自动化, phone playwright, 手机UI自动化, adb 控制, 手机点击, 手机无障碍, 手机 agent, mobile playwright, 手机端自动化, 移动端自动化.
---

# Phone-Playwright: 移动端 AI 原生无障碍感知与确定性交互框架

Phone-Playwright 是一个专为 AI Agent 与自动化开发者打造的“手机版 Playwright”。它将现代化 Web 自动化的核心范式（**惰性定位器 Locator**、**可用性自动等待 Actionability Auto-Waiting**、**视口感知语义蒸馏 Semantic Pruning**）深度移植至移动端（Android ADB / iOS WDA），彻底解决了移动端 UI 自动化中“元素动态漂移”、“渲染动画抖动丢失点击”、“Token 消耗巨大”与“Wi-Fi ADB 端口动态改变”等生产难题。

---

## 1. 核心架构与创新指标

- 🚀 **极速首击优化 (Warm-Cache Fast Dispatch)**：针对 AI 决策流中 `snapshot() -> click()` 模式，通过 1.0s TTL 快照温热缓存，跳过冗余 Dump 与稳定度循环，**将首击物理动作耗时从 7640ms 降至 141ms（提升 54 倍）**！
- 📉 **视口感知语义蒸馏 (O(N) DFS Pruning)**：物理屏幕视口几何相交裁剪、空无交互容器折叠、后代标签向父卡片提升，将上万字符的冗长 XML 压缩为极简的 `@1, @2, ...` Markdown 元素表，**Token 消耗降低 ≥90%**。
- 🛡️ **严格 5 阶段动作守卫 (Actionability State Machine)**：`Attached -> Visible in Viewport -> Stable [jitter < ε] -> Enabled -> Dispatch`，杜绝页面转场过程中的幽灵点击。
- 🔍 **无界视口事后诊断与动态滚动**：长列表深层元素超时失败时，通过百万像素无界视口精确识别 `OffscreenElementError` 与 `SelectorNotFoundError`；搭配 `.scroll_into_view()` 自动滑动居中可视。
- 🌐 **双通道混合感知 (Hybrid Perception)**：以 80ms 零 GPU 开销的无障碍树为主，在极端精简或 Webview 容器下自动无缝接入本地极轻量 ONNX OCR 兜底。
- 🔌 **生产级跨平台 MCP Server**：原生支持 Claude / ZCode 的 STDIO JSON-RPC 2.0 协议，采用异步线程池隔离技术彻底免疫 Windows IOCP 管道崩溃。

---

## 2. 目录与自包含组件

本 Skill 经过严格工程化解耦，完全**自包含（Self-Contained）**：

```text
phone-playwright/
├── SKILL.md                          # 本文档：架构概述、快速上手与使用规范
├── pyproject.toml                    # 独立依赖与打包构建规范 (仅需 pydantic)
├── src/                              # 核心源码包 (可独立 pip install)
│   └── phone_playwright/
│       ├── api/                      # 异步/同步高层 SDK (PhonePage, PhoneLocator)
│       ├── core/                     # 状态机、语义蒸馏器、选择器解析器
│       ├── drivers/                  # 硬件驱动桥接 (Android ADB, iOS WDA)
│       ├── fleet/                    # 多设备管理、看门狗探针、mDNS 服务发现
│       ├── mcp/                      # 标准 MCP STDIO JSON-RPC 2.0 服务端
│       └── models/                   # 几何数据结构、动作结果与异常模型
├── scripts/                          # 开箱即用便捷脚本
│   ├── cli.py                        # 全功能 CLI 交互式与单步命令工具 (含 REPL/MCP)
│   └── inspect_ui.py                 # 快速 UI 视口元素检查与截图导出工具
├── docs/                             # v2 进阶系统与子系统详细工程规格书
│   ├── README.md                     # 规格书体系导航与开发原则
│   └── specs/                        # 输入子系统/SoM视觉/手势/CDP/断言/Trace 规格
├── references/                       # 生产架构与深度手册
│   ├── architecture.md               # 完整分层架构、状态机模型与优化算法剖析
│   ├── api-reference.md              # Async / Sync Page & Locator API 全量字典
│   └── pitfalls.md                   # 生产实战硬核避坑手册 (Dump延时/端口漂移/中文输入)
└── tests/                            # 自动化单元测试与类型守卫套件 (42 项全绿)
```

---

## 3. 快速上手

### 方式一：便捷命令行 (CLI & REPL)

无需编写任何脚本，直接使用自带 CLI 即可调试手机：

```bash
# 查看当前屏幕的紧凑语义元素表 (设备 ID 缺省时自动探测 adb devices 中的唯一在线设备)
python scripts/cli.py --device 192.168.1.3:43037 snapshot

# 点击元素 (支持 text=, @index, resource-id= 等选择器)
python scripts/cli.py --device 192.168.1.3:43037 click "text=设置"

# 安全输入文本 (中文/Emoji/空格全兼容；剪贴板通道失败时显式报错而非注入乱码)
python scripts/cli.py --device 192.168.1.3:43037 fill "resource-id=search_src_text" "无线局域网"

# 自动滚动长列表直到目标可见
python scripts/cli.py --device 192.168.1.3:43037 scroll "text=关于本机"

# 启动交互式 REPL 控制台
python scripts/cli.py --device 192.168.1.3:43037 repl
```

### 方式二：Python 异步代码调用 (Async SDK)

```python
import asyncio
from phone_playwright.api.async_api import AsyncPhonePlaywright

async def main():
    async with AsyncPhonePlaywright() as pw:
        # 1. 连接设备 (支持无线 ADB IP:端口，或 USB 设备序列号)
        page = await pw.connect("192.168.1.3:43037")

        # 2. 获取紧凑快照 (同时温热 1.0s 执行缓存)
        snapshot = await page.snapshot()
        print(f"当前 Activity: {snapshot.activity_name}")
        print(snapshot.summary_markdown)

        # 3. 极速响应点击 (利用快照缓存，~140ms 极速下发)
        await page.locator("text=无线网络").click()

        # 4. 深层长列表滚动与链式交互
        await page.get_by_text("高级设置").scroll_into_view().click()

        # 5. 安全中文输入
        await page.locator("role=Input").fill("办公专用WiFi")

asyncio.run(main())
```

### 方式三：Python 同步脚本 (Sync SDK)

```python
from phone_playwright.api.sync_api import SyncPhonePlaywright

with SyncPhonePlaywright() as pw:
    page = pw.connect("192.168.1.3:43037")
    page.locator("text=蓝牙").click()
    page.press_back()
```

### 方式四：启动 MCP STDIO 服务供 Agent 驱动

在 AI 客户端配置中加入该 MCP 服务器：

```json
{
  "mcpServers": {
    "phone-playwright": {
      "command": "python",
      "args": ["<path-to-skill>/scripts/cli.py", "--device", "192.168.1.3:43037", "mcp"]
    }
  }
}
```

---

## 4. 选择器语法速查表

| 选择器类型 | 示例语法 | 匹配行为 |
|---|---|---|
| **紧凑数字引用** | `@1`, `@5`, `@12` | 匹配最新快照列表中指定索引号的元素 |
| **文本内容** | `text=设置`, `text=确定` | 模糊匹配节点的 `text` 或 `content-desc` 属性 |
| **控件标识符** | `resource-id=com.android.settings:id/search` | 匹配 Android `resource-id` |
| **语义角色** | `role=Button`, `role=Input` | 匹配标准 UI 角色类型 |
| **复合过滤** | `role=Button[name='取消']` | 组合角色与显示文本属性进行精确过滤 |

---

## 5. 深入阅读

- 架构设计与理论推导：[`references/architecture.md`](references/architecture.md)
- 完整 API 接口字典：[`references/api-reference.md`](references/api-reference.md)
- 真实设备踩坑指南：[`references/pitfalls.md`](references/pitfalls.md)
