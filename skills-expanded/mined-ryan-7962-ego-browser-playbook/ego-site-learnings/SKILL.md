---
name: ego-site-learnings
description: 浏览器自动化的站点踩坑知识库。自动化任何站点前先读对应 learnings；调试出新坑后必须回写。触发词：站点踩坑、learnings、页面改版、自动化知识库。
---

# ego-site-learnings：站点经验包（官方 learnings 格式）

## 知识库位置

```
~/.workbuddy/skills/egobrowser/agent-workspace/learnings/<site-id>/
├── manifest.json     # { id, name, domains[], notes[], browserTools{} }
├── notes/            # overview.md（站点地图/额度模型）+ pitfalls.md（坑与解法）
└── browser-tools/    # 可选：页面侧 JS 提取函数
```

## 使用规则（双向）

### 自动化前（读）

用 ego-browser 自动化以下站点时，**必须先读对应 learnings**：
- `item.taobao.com` / `detail.tmall.com`（淘宝/天猫）→ `learnings/taobao/notes/overview.md` + `notes/pitfalls.md`
- `app.qian-gua.com`（千瓜）→ `learnings/qian-gua/notes/overview.md` + `notes/pitfalls.md`

命中以下任一情况，说明你正在踩已知的坑，先查 pitfalls 再动手：
- 选择器匹配不到（日期面板/分栏表格/按钮标签）
- 下载事件收不到
- 弹窗表单填不进值
- 发送/提交类操作计数异常

### 调试后（写，append-only）

自动化过程中发现**新的坑**并找到解法后：
1. 在对应站点 `notes/pitfalls.md` 追加一条（现象→根因→解法→验证日期），不改旧条目
2. 站点级新事实（新页面路由、额度变化）更新 `notes/overview.md`
3. 若发现稳定可复用的页面提取函数 → 写成 `browser-tools/*.js` 并登记进 manifest.json 的 browserTools

### 新站点初始化

首次自动化新站点且预期会复用时，初始化包结构：
```bash
mkdir -p ~/.workbuddy/skills/egobrowser/agent-workspace/learnings/<site-id>/{notes,browser-tools}
```
manifest.json 参照 qian-gua 的格式；site-id 用主域名（如 `qian-gua`、`taobao`、`douyin-compass`）。店透视插件寄生在淘宝/天猫详情页上，其经验归入 `taobao` 包，不单独建 site-id。

## 运行时接入（向前兼容）

- 目录按官方格式（github.com/citrolabs/ego-lite `skills/ego-browser/learnings/`）摆放
- 当 Ego Lite 运行时暴露 `runSiteTool`/`learnContext` 助手后，设置环境变量即可自动接入：
  `EGO_BROWSER_AGENT_WORKSPACE=~/.workbuddy/skills/egobrowser/agent-workspace`
- 当前安装版（0.6.0.16+）未暴露这些助手，learnings 以 Agent 可读文档方式生效（本 skill 即入口）
