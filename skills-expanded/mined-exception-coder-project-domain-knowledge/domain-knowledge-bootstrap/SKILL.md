---
name: domain-knowledge-bootstrap
description: 一次性初始化某项目的「预初始化知识图谱」。当用户说"初始化业务知识图谱"、"bootstrap 知识库"、"分析某项目并生成业务真理"、"一气呵成生成所有模块业务真理"、"预初始化知识图谱"、"补齐 domain knowledge"、"看知识库还缺什么"、"更新项目模块"、"同步模块清单"、"重新解析模块"、"modules.json 对齐代码目录"时触发。两阶段一体：阶段A 产出/更新目标项目的项目画像入口（Claude Code 用 CLAUDE.md，Codex/Cursor 用 AGENTS.md，多工具项目双写同步；实现侧，不入业务库）；阶段B 优先使用项目 Graphify 定位并定向核对源码→人判定边界→生成 draft 业务真理骨架→人填口径→校验。脚本只做机械脚手架（scan/gaps/new/check），绝不自动抽内容入库。仅在 project-domain-knowledge 仓库内使用，受众是知识库 owner。
---

# 知识图谱初始化 Skill（两阶段一体）

一次调用,把某个目标项目(如 yoooni)初始化成「**预初始化知识图谱**」:
- **阶段 A · 项目画像**——技术栈/分层/编码/启动方式 → 落到目标项目的 Agent 入口文件（`CLAUDE.md` / `AGENTS.md`，实现侧，**不**进业务真理库）。
- **阶段 B · 业务真理候选**——Graphify 导航与模块内源码核验 → 人判定边界 → 生成 `draft` 骨架 → 人填业务口径 → 校验。落到 **`project-domain-knowledge` 业务区**。

> 两阶段分流是硬约束:实现事实(怎么实现/目录/类名)归项目 Agent 入口文件与 `impl/`;只有「重写也成立的业务真理」进业务区(见 [_taxonomy.md](../../../knowledge/_taxonomy.md) §0)。脚本永远只产 `draft` 候选,owner 评审后才升 `stable`。

## 红线(不可越)

- ❌ 不把代码/SQL/`/init`/目录结构等**实现事实**写进业务区。
- ❌ 不自动抽业务内容入库——`scan` 只列**类名结构线索**,业务口径(公式数字、状态条件)由人填。
- ❌ 不替业务 owner 拍板对不对。AI 可起草,人判定+评审。

## 触发条件

- "初始化/预初始化 XX 项目的知识图谱"、"一气呵成生成所有模块业务真理"
- "分析某项目并 bootstrap 业务真理"、"补齐 domain knowledge"
- "看知识库还缺什么 / 覆盖度"
- "更新项目模块 / 同步模块清单 / 重新解析模块 / modules.json 对齐代码目录"（走 [sync-modules](#更新模块清单sync-modulesdiff--确认--落盘)：diff 预览 → 确认 → 只新增落盘）

## 前置

在 `project-domain-knowledge` 仓库根、已 build;且能访问目标项目代码根:

```powershell
node --version            # ≥18
npm install ; npm run build
```

需要两个路径:本库根(运行脚本处) + **目标项目根**(`--project-root`,如 `D:\yoooni\yoooniCodeSpace\yoooni`)。

---

## 阶段 A — 项目画像 + Agent 入口文件（实现侧）

目的:让 AI 在目标项目里编码时少踩坑。**产物落在目标项目根,不进本库。**

1. 摸技术栈/分层/编码/规模(读目标项目顶层 + `src` 包 + 配置)。
2. 先检查目标项目根已有的 `CLAUDE.md` 与 `AGENTS.md`，再按下方「入口文件选择与同步规则」写入；至少含:技术栈与版本、分层约定(注意 yoooni 业务逻辑层叫 **`manage` 不是 service**)、编码分区(`src`=GBK / `WebRoot`=UTF-8)、启动方式、常见坑。
3. 顺手提示该清的 `.gitignore`(运行时垃圾:`out/`、`hs_err_pid*.log`、`replay_*.log`、崩溃转储 zip)。

### 入口文件选择与同步规则

| 使用场景 | 必须维护的入口 |
|---|---|
| Claude Code | `CLAUDE.md` |
| Codex / Cursor | `AGENTS.md` |
| 明确为多工具团队、无法可靠判断当前 Agent、或两份入口任一已存在 | `CLAUDE.md` + `AGENTS.md` |

- 两份都不存在：默认按多工具项目处理，同时创建两份；共享同一份项目画像正文，仅文件开头说明各自适用入口。
- 仅存在一份：先完整读取并保留人工规则，再创建缺失入口；共享事实与约束保持一致，不把已有文件整份覆盖。
- 两份都存在：同步更新共享的技术栈、分层、编码、启动和常见坑；保留各自 Agent 专属指令。发现冲突时停止合并并请 owner 决定，不擅自选边。
- `AGENTS.md` 不得只写“请阅读 CLAUDE.md”的空壳链接；Codex/Cursor 必须从入口文件本身获得可执行约束。
- 不使用软链接代替入口文件，避免 Windows、Git 和不同 Agent 的链接处理差异。
- 阶段 A 的幂等判据从“是否已有 `CLAUDE.md`”改为“本次适用的入口是否齐全且共享画像已同步”。

> 这步等价于一次"对业务库友好的 /init",但内容留在目标项目的 Agent 入口文件;**绝不**把它倒进业务区。

---

## 阶段 A2 — DDL 基线（DB 项目必产,写 SQL 前必读）

目的:凡目标项目有数据库(SQL / DAO / Mapper / ORM),**必须**先把真实 schema dump 成 `knowledge/{project}/impl/ddl-baseline.md`,作为写 SQL、核对表/字段的权威源。缺它 AI 只能按框架习惯**猜表名**——真实教训:SRM 无基线 → 把芋道新版 `system_menu` 猜成旧版 `sys_menu`,`Table doesn't exist`。本步与 team-standards `backend-evidence` 的 DDL 基线规则同源,这里是 onboarding 里的执行位(yoooni 已产、SRM 曾漏)。

1. 按 DB 引擎 dump(**从真实库/权威 schema,不靠 ORM 实体或记忆反推**):
   - MySQL:`mysqldump --no-data --skip-add-drop-table --compact <db> > schema.sql`
   - PostgreSQL:`pg_dump --schema-only --no-owner --no-privileges <db>`
   - Oracle:JDBC + `DBMS_METADATA.GET_DDL`(见 `knowledge/yoooni/impl/ddl-baseline.md` 文末维护脚本)
   - 无本地 DB 客户端时:owner 在能连库的机器 dump 后回传;或用只读 MCP 查 `information_schema` 逐页重建(近似,能挡"猜表名"但 DEFAULT/CHECK 等可能不全)。
2. 落 `knowledge/{project}/impl/ddl-baseline.md`:表头(数据源 + dump 方式 + 表数 + 日期,**口令不落盘**)+ 全局字段约定 + 每表 `CREATE TABLE`(按业务域分节)+ 文末维护脚本。**单文件,不拆**。
3. schema 迁移后重跑维护脚本刷新。

> 这份是 impl(实现事实),不是业务真理——放 `impl/`、不进业务区。hook `check-sql-ddl-readiness.js` 会在写 SQL 前兜底提醒先读它。

---

## 阶段 B — 全模块业务真理（业务侧,逐模块循环）

### B0. 先看全局缺口

```powershell
node scripts/bootstrap.mjs gaps yoooni
```

得到每模块已有几条、缺哪些 type、哪些空。据此排优先级:**龙头/高密度模块先行**(sale 销售全链路、allcost 订单成本、produce 生产),flow/state/formula 三类骨干优先,concept/term 随后。

### B1. 项目图谱导航与候选证据

先运行 `node scripts/bootstrap.mjs draft-all --project <project> --project-root <root>` 预览，已授权初始化时加 `--apply`。适配器读取项目 `graphify-out/graph.json`，候选保留节点、关系、覆盖缺口和源码指纹。图谱不可用则登记路径扫描降级，路径存在不等于图谱新鲜。旧 `scan` 命令仅用于定向补查。

核对使用 `scripts/evidence-check.mjs`；格式、命令和限制见 [README.md](../../../README.md#项目图谱到候选知识的闭环)。日常代码任务先查 MCP，不自动执行全模块初始化；stale 只要求核对映射，不撤销业务成熟度。

### B1.1 定向源码补查

```powershell
node scripts/bootstrap.mjs scan --project-root D:\yoooni\yoooniCodeSpace\yoooni --module produce
```

列出该模块 Action/Model/Constant/Manage 类名(靠 `modules.json` 的 codePath 定位)。**只是线索**:Action 名→可能的 flow;Constant/状态字段→state;价/费/分摊→formula;校验/授权/额度→rule;实体含义→concept。

### B2. 过边界判据(人判定,关键,不可跳)

对每条候选逐条问:
1. **是业务真理吗?**(重写也成立?) 否 → 不进库(分流项目 Agent 入口文件/impl/topology/profiles)。
2. **属哪模块?**(对齐 modules.json key) → 目录。
3. **哪类?** formula/flow/state/rule/concept/term → `type`。

AI 可读对应代码 + 用户给的新人文档**起草**草案,但"算不算真理/口径对不对"由人点头。**宁可不收,不可错收。**

### B3. 生成 draft 骨架(机械)

```powershell
node scripts/bootstrap.mjs new `
  --project yoooni --module produce --type state `
  --id yoooni-artorder-state `
  --title "制造单状态机" `
  --tags 制造单,状态,生产 `
  --related yoooni-manufacturing-flow
```

生成 `knowledge/yoooni/produce/yoooni-artorder-state.md`(frontmatter 合法、`stability: draft`、按 type 给骨架)。随后**人工填业务定义**(变量含义+规则/mermaid),**不贴实现代码**,口径来源指向新人文档/owner。

### B4. 收尾(每批一起做)

```powershell
node scripts/bootstrap.mjs check    # id 唯一/type 合法/模块在清单内
node scripts/bootstrap.mjs check-paths --project <P> --backend-root <后端根> [--frontend-root <前端根>]
                                     # 校验 modules.json 的 codePath/webPaths 真实存在(前端 webPaths 最易填错)
npm run catalog                     # 刷新 _catalog.md
```

> ⚠️ `check-paths` 必跑:`modules.json` 的前端 `webPaths` 全靠人工填、最易写错(写了不存在的目录、或漏了真实业务目录)。一个后端模块的前端常散在多个目录,故 `webPaths` 用数组列全;填完务必用 `check-paths` 对照真实目录验证。

MCP 端运行时调 `reload_knowledge` 生效。最后 **PR → owner 评审 → 升 stable**。

---

## 更新模块清单（sync-modules，diff → 确认 → 落盘）

当项目代码新增/重构了业务目录，`modules.json` 会滞后。用 `sync-modules` **按目录结构重新解析模块**，与现有清单出差异，**owner 确认后再写盘（只新增、绝不删除）**。

```powershell
# 1) 预览（默认，不写盘）：打印「新增候选 / 目录已消失」两类 diff
node scripts/bootstrap.mjs sync-modules --project yoooni --project-root D:\yoooni\yoooniCodeSpace\yoooni

# 2) 确认无误后落盘：把新增目录追加为骨架条目（name/webPath 留空待人填），已有条目原样不动
node scripts/bootstrap.mjs sync-modules --project yoooni --project-root D:\yoooni\yoooniCodeSpace\yoooni --apply
```

- **基准目录**：默认从现有 `codePath` 的父目录自动推导（yoooni 即 `application`、`application/erp`、`application/crm`）；也可 `--code-base a,b`（逗号分隔，相对项目根）显式指定。首次无 `modules.json` 时必须给 `--code-base`。
- **只新增，不删除**：diff 里「目录已消失」只告警，不会动清单——避免误删人工填的 `name`/`summary`/`webPath`；确需删除请手动改 `modules.json`。
- **候选是线索不是真理**：扫到的目录含技术目录（`common`/`excel`/`timetask` 等）与容器目录，`--apply` 前**由 owner 剔除非业务目录**（预览里挑，别照单全收）；容器目录（某模块的父目录）已自动跳过。
- **key 冲突**：新目录名与现有 key 相同（如两处都叫 `flow`）会在 `--apply` 时跳过并告警，需手动改名后再加。
- **落盘后**：填 `name`（中文业务名）+ `webPath`/`webPaths`（前端目录）→ 跑 `check-paths` 校验路径 → `npm run catalog` → MCP `reload_knowledge`。

> 与 `scan` 的分工：`sync-modules` 维护**模块清单本身**（有哪些模块、代码目录在哪）；`scan` 是在清单已就绪后 dump 某模块的类名线索供起草业务真理。先 `sync-modules` 对齐清单，再 `scan` 逐模块深入。

---

## 「一气呵成」的执行编排(skill 被触发时怎么跑)

用户说"分析 XX 项目、一次生成所有模块业务真理"时,按此自动编排,但**保留人判定关卡**:

1. **阶段 A**:摸画像 → 按入口选择规则写/同步目标项目 `CLAUDE.md` 与 `AGENTS.md` → 报告该清的 `.gitignore`。
2. **阶段 A2**(DB 项目):产 `impl/ddl-baseline.md`(见上);无本地 DB 客户端则请 owner dump 回传。**先于任何写 SQL / scan**——防"猜表名"。
3. **B0**:跑 `gaps`,产出按优先级排好的模块清单,**念给用户,确认范围/顺序**。
4. **逐模块循环**(B1→B2→B3):每模块先 `scan`,AI 读代码起草候选并**逐条标注**"建议 type + 是否像业务真理 + 口径来源",**整理成清单交用户一次性判定**(批量过关卡,不必每条卡死),通过的 `new` 落盘 + AI 填入起草内容(全部 `draft`)。
5. **B4**:全部跑完 `check` + `catalog`,汇总"本次生成 N 条 draft,覆盖 M 个模块",提示 PR + owner 评审。

> "一气呵成"指**流程不停顿地跑完脚手架**,不是"跳过人判定全自动入库"。所有产物是 `draft` 候选,真理性由 owner 评审兜底。遇到拿不准的认知,标 `draft` + 在正文写 `⚠️ 待 owner 核实`,不阻塞整体。

## 拒绝项

任何"把代码/`/init`/分析结果直接当业务知识入库"的诉求 → 按 §0 拒绝,改为:实现事实进项目 Agent 入口文件/`impl/`,跨项目进 cross-topology,编码约定进 project-coding-profiles。
