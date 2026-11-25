---
name: mebular-assistant-integration
description: Mebular「连接 AI 助手」接入契约。凡涉及助手检测/接入/验证/卡片展示/新增助手（含自定义 descriptor、三态判定、验证器、连接页交互、桌面向导第②步）都必须遵守。Use when working on assistant detection/integration/verification, the connect page, client descriptors, or adding an assistant integration (built-in or custom).
license: MIT（与仓库一致）
---

# Mebular 助手接入契约

本文件是「连接 AI 助手」链路的**单一契约**，与 `mebular-console-design`（视觉）并列。
适用范围：助手注册表（内置 + 自定义）、`/admin/api/clients`、连接页、桌面向导第②步、
接入后验证。规格文档：[`docs/design/config-journey-v1.md`](../../../docs/design/config-journey-v1.md)。
内置条目的落面/写入/验证值以 **F-EXP-1 勘察事实**为准（§2.1/§2.2），实现不得自行发明。

---

## 一、核心理念：助手是数据，不是代码

新增一家助手 = 新增一条 **descriptor（数据条目）**，**不改检测/接入代码**。
长尾助手由用户在前端「新增助手」流程自助登记（选配置文件 / 粘贴片段），**零发布**。

## 二、Descriptor schema（六要素，缺一不可）

```jsonc
{
  "id": "openchamber",                 // 稳定小写 id（kebab-case）
  "name": "OpenChamber",               // 展示名
  "probe": {                           // ① 探测（多信号取并集，逐信号可证伪）
    "signals": [
      { "kind": "config-path", "paths": ["~/.config/opencode/opencode.json"] },
      { "kind": "cli", "command": "opencode --version", "timeoutMs": 1500 },
      { "kind": "app-bundle", "paths": ["/Applications/OpenChamber.app"] },
      { "kind": "process", "pattern": "opencode serve --service" }
    ]
  },
  "landing": {                         // ② 落面（读写面 + 格式适配器）
    "primaryPath": "~/.config/opencode/opencode.json",
    "keyPath": "mcp.servers.mebular",  // 目标键位（见 §2.3 schema 缺陷注记）
    "forbiddenPaths": ["~/.config/openchamber/opencode.managed.json"],
    "format": "opencode-json",         // 格式适配器 id（注册表内置：opencode-json / hermes-yaml / json-mcpServers / toml / yaml / generic-snippet）
    "snippet": { /* 该格式下 mebular 条目的形状 */ }
  },
  "writer": {                          // ③ 写入（命令/策略/备份要求）
    "strategy": "merge-key",           // merge-key（原子合并单键）| cli-set（经该助手官方 CLI 写入）| manual（只给片段）
    "command": null,                   // cli-set 必填，如 hermes config set --force mcp_servers.mebular.url <value>
    "backup": "byte-level",            // merge-key/cli-set 必须 byte-level（字节级备份 + 失败回滚）；manual 为 n/a
    "atomic": true                     // merge-key 必须 true（临时文件 + rename）
  },
  "verify": {                          // ④ 验证（命令 + 判据）
    "cli": { "command": "opencode mcp list", "expect": "mebular", "timeoutMs": 4000 },
    "configReadback": true             // 兜底：回读确认条目存在且原配置无损
  },
  "activation": {                      // ⑤ 生效/重启语义（决定是否需要「重启清单」步）
    "kind": "user-reload",             // user-reload（用户在助手侧重载/重启）| hot（免重启，新会话即用）
    "note": "OpenChamber：由用户在 App 侧重载/重启生效；产品不得发 opencode reload 干扰运行服务"
  },
  "risks": [                           // ⑥ 风险注记（如实写，UI 可展示）
    "opencode.managed.json 为 App 所有且会被重写，禁写",
    "opencode mcp list 经运行服务回答，只读但勿频繁调用"
  ]
}
```

硬规则：

- `probe.signals` 至少一条；每条信号必须能**独立证伪**（见红线二）。「配置文件能否读到」
  只是信号之一，**不得**作为「装了没」的唯一判据。
- `writer.strategy: "manual"` 的条目在 UI 上是「手动合并」流（给片段 + 步骤），
  **不得**给「接入」自动写按钮。
- `verify.cli` 可缺省；缺省时 `configReadback` 必须 true 且 UI 明示「仅配置级验证」。
- `activation.kind: "hot"` 的条目**跳过**重启清单步（验证通过即完成）；`user-reload`
  才展示「我已重启/重载，重新验证」清单。

### 2.1 内置条目 · OpenChamber（opencode 宿主）— F-EXP-1 实测

- **落面 = global `~/.config/opencode/opencode.json` 的 `mcp.servers.mebular`**。
  `OPENCODE_CONFIG` 是**合并、非取代**：`opencode debug config` 来源列表同时含真实
  global（index 0）与 managed（index 2）→ global 会被读取。
- remote 条目固定 `{"type":"remote","url":…,"oauth":false,"codemode":false}`：
  `oauth:false` 防止宿主对本地 Mebular 发起 OAuth；`codemode:false` 让工具保持直连，
  不被 OpenCode 2 Code Mode 的目录折叠隐藏。
- 已有 mebular 条目只覆盖 `type/url/oauth/codemode`；`headers`、`timeout`、`protocol`
  等用户字段保留，其他配置键文本不变（原子写 + 字节级备份 + 失败回滚 + 幂等）。
- **禁止**写 `~/.config/openchamber/opencode.managed.json` **及**
  `~/.config/openchamber/run/instances/*/opencode.managed.json`（App 所有、会被重写）。
- 生效：写完由**用户在 App 侧重载/重启**（产品不得发 `opencode reload` 干扰运行服务）。
- 验证钩子（只读、经运行服务回答、**勿频繁**）：`opencode mcp list`（应出现 mebular）、
  `opencode debug config`（来源 0 的 keys 含 `mcp`）。
- 探测证据：`/Applications/OpenChamber.app`（+ 运行进程 `serve --service`）。

### 2.2 内置条目 · Hermes — F-EXP-1 实测

- **落面：`~/.hermes/config.yaml` 的 `mcp_servers.mebular`**；
  stdio = `{command,args[],env{},enabled}`；remote = `{url}`。
- **写入必须用 `hermes config set --force mcp_servers.mebular.<field> <value>`**
  （ruamel 保注释；未知子键必须 `--force`；结构化值支持 JSON 字面量）。
  **Hermes 无法 env 沙箱**（`HERMES_CONFIG_PATH` 被剥离）→ **写前字节级备份 + 失败回滚**是硬要求。
- 生效：**免重启**——新会话即用，或已开会话 `/reload-mcp`（`activation.kind = "hot"`）。
- **验证钩子（黄金样例）**：`hermes mcp test mebular` → rc=0 且 `✓ Connected` +
  `✓ Tools discovered: N≥1`；辅以 `hermes mcp list`（`✓ enabled`）。
- 探测证据：`~/.local/bin/hermes` → `~/.hermes/hermes-agent`。

### 2.3 疑似 schema 缺陷（实现注意）

现有写入产出 `mcp.<name>` 形状，而正确 schema 可能是 **`mcp.servers.<name>`**
（以 `opencode mcp add` 产出为真源）——这是「接了不生效」的头号嫌疑。
实现轮**必须**在沙箱对照 `opencode mcp list` 验证并修正后，才允许宣布接入完成。

### 2.4 OpenChamber 原生 memory 共存（只读守卫）

- 只读探测三件事：env `OPENCHAMBER_MEMORY_ENABLE`、`settings.json` 的
  `agentMemoryToolEnabled`、`memory.json` 是否存在（global `~/.config/openchamber/memory.json`
  与 `projects/*/memory.json`）。**不读取 entries、不写、不导入、不替换、不双写**，
  也不注册 `openchamber_memory` 工具。
- 原生 memory 开启时，Mebular 沉浸式默认 **tool-only**，必须由用户显式 opt-in；
  轻量 MCP 不受影响。
- 状态/描述必须如实给出三路证据与 `tool-only / 需显式 opt-in` 口径；不得声称已接管、
  已迁移或已同步原生 memory。

## 三、三态诚实（判据与动作分离）

| 态 | 判据（全部来自 descriptor，如实上报来源） | 卡片主按钮 | 次级 |
|---|---|---|---|
| **未安装** | 所有 probe 信号均阴性 | 「怎么装」（展开安装指引/官网链接） | 重新检测 · 手动登记为已装 |
| **已装·未接入** | ≥1 信号阳性 ∧ 落面无 mebular 条目 | 「接入」（merge-key / cli-set）或「查看片段」（manual） | 查看改动 · 重新检测 |
| **已接入** | 落面有 mebular 条目 ∧ 回读校验通过 | 无（收编为「已接入 ✓」态标） | 验证 · 回滚（二次确认）· 查看改动 |

- 状态必须附带**判据说明**（哪条信号命中/未命中），悬停/展开可见；禁止只给一个词。
- 计数（向导 "n/m"、分组标题）只统计「已装」两态，分母 = 已装数（非注册表总数）。

## 四、验证器要求（接入后闭环）

接入写入成功后必须走完整闭环，缺一环就不许显示「完成」：

1. **回读校验**（必有）：重读落面，确认 mebular 条目存在 ∧ 原配置其余键无损。
2. **CLI 验证**（有 `verify.cli` 则必跑）：执行验证命令，命中 `expect` 才判「验证通过」。
   失败 → 明确「已写入但验证未过」态（黄），给出原始输出摘要。
3. **重启清单**（仅 `activation.kind = "user-reload"`）：展示 checklist（完全退出 →
   重开/重载 → 应能看到 mebular 工具），附「我已重载，重新验证」按钮。
   `hot` 条目跳过本步。
4. **重新验证**：用户点击后重跑 1+2；通过才翻「已接入 ✓ 已验证」。

「需重启未重启」是**一等状态**（不是一句提示）：卡片保持黄态，主按钮 = 「我已重载，重新验证」。

## 五、禁死卡片（交互完整性红线）

任何卡片、任何状态下，主按钮必须可达且有效：

- 未安装卡片**禁止**出现「接入」按钮（无落面可写 = 死交互）。
- 按钮无动作、动作必失败、动作结果无反馈，三者任一出现即视为缺陷。
- 空分组不渲染；注册表为空时连接页给「新增助手」引导而非空列表。

## 六、红线

**红线一 · 禁止假装检测**：探测信号必须真实执行（文件存在性 / CLI 探测 / Bundle /
进程），禁止硬编码「已安装」、禁止以「注册表里有这条」冒充「装了」。判据来源必须可展示。

**红线二 · 禁止假阴性/假阳性静默**：配置读不到 → 报「未检测到」（附各信号结果），
禁止报「未安装」以外的推断，更禁止报「已安装」。

**红线三 · 禁写死列表**：UI 枚举一律来自注册表（内置 + 用户自定义合并），
禁止在前端写死助手名单/数量（"n/7" 之类）。

**红线四 · 写入不失真**：merge-key/cli-set 只动 mebular 一条键；写前**字节级备份**、
失败回滚、原子写入（merge-key）、重复接入幂等；配置无法解析时**不写**，转手动流并给片段。

**红线五 · 自定义条目同权**：用户自定义 descriptor 与内置同 schema、同校验、
同三态判据；存储于 home（`assistants.custom.json`），内置条目不允许删除（只能自定义增删）。

**红线六 · 探针输出卫生**：任何探针/验证命令的**输出不得回显凭据值**（token、密钥、
证书）；只打印变量名/键名。日志、错误摘要、诊断包同此约束。

**红线七 · 禁写 App 私有面**：`landing.forbiddenPaths` 列出的路径（如
`~/.config/openchamber/opencode.managed.json`）一律禁写；落面以 F-EXP-1 实测为准，
禁止凭猜测写配置。

## 七、自定义条目（「新增助手」流程）规则

1. 入口：连接页「＋ 新增助手」一等按钮（与分组同级，不收在 overflow）。
2. 两种登记方式：**选配置文件**（推断格式适配器 + primaryPath）/ **粘贴配置片段**
   （生成 manual 策略条目）。名称/id 必填，id 冲突报错。
3. 可选：填验证命令（`verify.cli`）与生效语义（默认 `user-reload`）。
4. 登记后立即进入三态机：probe（用声明的路径/CLI）→ 未装 / 已装未接 / 已接。
5. manual 条目的「接入」= 展示片段 + 人话步骤 + 「我已手动合并，重新检测」。
6. 自定义条目可编辑/删除；删除不影响已写入目标配置的内容（另给「回滚」）。

## 八、验收锚点

实现与复核以规格文档「可判别验收断言清单」为准：
[`docs/design/config-journey-v1.md`](../../../docs/design/config-journey-v1.md) 第九节。
