---
name: file-placement
description: "[治理] 决定任何文件该放哪时使用。触发条件：创建/下载/产出任何文件前；项目内建子目录时；归类轻量会话产出时；判断是否该提醒新建项目时。包含文件类型→路径映射、项目内多级分层、轻量任务归档、新建项目触发阈值，全部规则可程序化判断。"
---

# 文件存放分层标准（AOS 2.0 完整版）

## 0. 判定顺序（对任何文件依次过三道闸）

```
闸1 归属判定：属于某个项目？ → 是 → 进 §2 项目内分层
                      → 否 → 进 §1 顶层路由
闸2 寿命判定：临时（<90天/可再生）？ → 是 → 05_CACHE 体系
                         → 否 → 永久区（项目/导出/参考/归档）
闸3 副本判定：是否唯一副本？ → 是 → 禁止进 05_CACHE，必须永久区+备份
```

## 1. 顶层路由表（非项目文件）

| 内容 | 去向 | 分层 |
|---|---|---|
| 交付物/输出 | `07_EXPORTS/{project}/` | 项目名/（无项目主题用 `07_EXPORTS/quicktasks/`，见 §4） |
| Agent 中间产物 | `05_CACHE/{project|quicktask}/{YYYYMMDD}/` | 两级强制 |
| 重量级外部输入 | `08_INBOX/{YYYYMMDD}/` | 中转区，处理完迁 §1/§2 归宿并留指针 |
| 知识（长期有效） | `09_REFERENCE/{domain}/{topic}.md` + `_index.md` 钩子 | 按领域 |
| 用户/项目状态 | `04_MEMORY/`（user/project + INDEX） | — |
| 运行日志/历史 | `06_LOGS/{project}/` | 追加 |
| 废弃但不可删 | `99_ARCHIVE/{批次名}/` | 只增 |

## 2. 项目内部分层（01_PROJECTS/{name}/）

> 依据：社区"浅层可预测结构"共识 + Go/Rust 社区"按需生长"共识 + "by-feature 优于顶层 by-layer"强共识（来源见文末）。**本节规则只治理非代码产物的落位；代码内部分层遵循语言生态惯例，不由本表强制**。

### 2.1 标准骨架（两层强制，其余按需生长）

```
{name}/
├── AGENTS.md            ← 根层只允许：两件套 + .gitignore + CHANGELOG.md
│                          【agent 友好共识】AGENTS.md 必须列出 build/test/run 各一条命令
├── README.md
├── docs/                ← 一切项目文档
│   ├── design/          设计文档、架构决策（ADR）
│   ├── reports/         调研报告、验证报告
│   ├── archive/         过期文档（含迁移收编的 STATUS/PROGRESS）
│   └── media/           文档配图（截图等）
│   （对外产品文档可另立 Diátaxis 四象限：tutorials/how-to/reference/explanation）
├── src/                 ← 源代码（单一项目）；项目集放子项目
│   ├── 代码内部分层遵循生态惯例：Python 库用 src-layout；应用层项目
│   ├── by-feature（feature 内薄分层，禁止顶层 by-layer 大杂烩——强共识反模式）；
│   ├── Go 小项目平铺按需生长；Rust 由 Cargo 强制；JS monorepo 用 apps/+packages/
│   └── （本表不为代码指定内部结构）
├── scripts/             ← 项目脚本
│   ├── dev/  deploy/  verify/
├── config/              ← 配置文件（模板与实例；密钥只引用 credentials.json id）
├── assets/              ← 静态资源（被读取不修改）
│   ├── images/  fonts/  audio/  models/
│   └── data/
│       ├── 数据科学项目按 Cookiecutter 惯例细分 raw/ interim/ processed/
├── tests/               ← 测试与夹具（生态另有惯例时从惯例，如 Rust tests/）
├── tools/               ← 项目专用工具（可执行/工具链）
└── backup/              ← 项目内备份（唯一备份禁放 05_CACHE）
```

### 2.2 按需目录启用规则（防过度建目录）
- 三人以下小项目最少只需：`docs/` + `src/`（+两件套）。config/scripts/assets/tests/tools/backup **有对应文件才建**
- 单文件不建目录：1 个脚本直接放 `scripts/`，不为它建 `scripts/dev/`

### 2.3 文件类型 → 路径映射（可自动化）

| 类型 | 特征（扩展名/模式） | 路径 |
|---|---|---|
| 文档 | `*.md`（非两件套/CHANGELOG） | `docs/{design|reports}/`（设计→design，报告→reports） |
| 代码 | `*.py *.ts *.js *.go *.rs *.java *.cs *.cpp` … | `src/`；**内部组织遵循生态惯例（src-layout/by-feature/Cargo/apps-packages），本表不强制代码内部结构** |
| 脚本 | `*.ps1 *.sh *.bat` 或 `check_* verify_* deploy_* fix_*` | `scripts/{dev|deploy|verify}/` |
| 配置 | `*.json *.yaml *.yml *.toml *.ini *.env*`（项目级） | `config/` |
| 图片 | `*.png *.jpg *.webp *.svg *.ico *.gif` | 文档配图→`docs/media/`；资源图→`assets/images/` |
| 字体/音视频/模型 | `*.ttf/otf` `*.mp3/wav/ogg` `*.mp4/webm` `*.glb/onnx/pt` | `assets/{fonts,audio,models}/` |
| 数据集 | `*.csv *.parquet *.jsonl *.db *.sqlite`（被读取不修改） | `assets/data/`；会变的运行时数据→项目运行目录（如 `data/`，遵循项目自身约定） |
| 压缩包 | `*.zip *.7z *.tar.gz` | 解压后的内容按本表归位；压缩包本身→`backup/` 或删 |
| 可执行/工具链 | `*.exe *.dll` 或大型工具目录 | `tools/` |
| 测试 | `test_*.py *.spec.ts *_test.go` conftest | `tests/` |
| 日志 | `*.log` | `06_LOGS/{project}/`（禁止留在项目根/src） |
| 临时输出 | 生成即弃、可再生 | `05_CACHE/{project}/{YYYYMMDD}/`（不进项目） |

### 2.4 禁止事项（自动化巡检可 grep）
- 项目根层堆放 ≥3 个非两件套文件 → 违规
- `src/` 内出现 `*.log`、截图、压缩包 → 违规
- 同一目录混放 ≥4 种类型（按 §2.3 分类数）→ 违规
- 深度 >4 级仍未到文件（无谓空层级）→ 违规
- 日期命名一律 `YYYYMMDD`，禁止 `final/最终版/新建文件夹`；日期只作事务性分层键，主题 slug 必须并列（`YYYYMMDD_{slug}`）——纯日期轴被共识视为查找灾难

## 3. 轻量会话/一次性任务归档（quicktask 体系）

**判定**：任务无部署物、无独立 repo、产出 <10 文件且预计单会话完成 → quicktask，不建项目。

| 产出 | 去向 |
|---|---|
| 有交付物（报告/脚本/图） | `07_EXPORTS/quicktasks/{YYYYMMDD}_{主题slug}/`（主题 ≤3 词，kebab-case） |
| 仅中间过程文件 | `05_CACHE/quicktasks/{YYYYMMDD}_{主题slug}/` |
| 结论有长期价值（知识） | 提炼进 `09_REFERENCE/{domain}/`，quicktask 目录留指针 |
| 纯问答、无文件 | 不归档（会话日志由 harness 承载）；值得记的偏好→user_profile，事实→04_MEMORY |
| 后续追问同主题 | 已有 quicktask 目录则续用；跨 ≥2 次会话回到同主题 → 触发 §4 提醒 |

## 4. 新建项目触发判定（未手动指令时自动提醒）

**硬触发（任一命中即提醒）**：
1. 同一主题 quicktask 目录累计 ≥3 个（`07_EXPORTS/quicktasks/` 与 `05_CACHE/quicktasks/` 合计，按主题 slug 前缀匹配）
2. 单任务产出 ≥10 个文件 或 总量 >50MB
3. 任务需要独立部署物/运行时（建服务、注册域名、开 repo、装依赖树）

**软触发（两项同时命中提醒）**：
4. 跨 ≥3 个会话仍在继续的同主题
5. 产出含 ≥3 份设计/调研文档（docs 级内容）

提醒话术模板：`"{主题} 已满足新建项目条件（命中规则 {n}），是否创建 01_PROJECTS/{slug}/？（project-init skill 两件套 3 分钟就绪）"`——**只提醒，不代建**；用户确认后走 project-init。

## 5. 组件存放边界（自研 vs 第三方）

**原则：AOS 的能力边界 ≠ AOS 的文件夹边界。** harness 预装/用户安装的插件与第三方 skills 在 AOS 会话中照常可用（发现机制全局扫描），文件不在 AOS 目录内是设计而非例外。

| 组件类型 | 存放位置 | 判定 |
|---|---|---|
| 自研 skills（承载 AOS 治理语义：file-placement、dual-machine 等） | `{AOS_ROOT}/.dsh/skills/`（项目级） | 换一个工作区即失去意义 → 入 AOS，随仓库版本化 |
| 第三方 skills（通用能力） | `~/.agents/skills/`（用户级）或 `~/.dsh/skills/` | 换任何工作区都有用 → 用户级，更新走 git/市场 |
| 第三方插件 | harness profile 路径，插件市场管理 | AOS 只声明依赖（如多机协同依赖 SSH 插件），不复制文件 |

**环境对齐**：所有外部依赖（插件/用户级 skill）登记于 `.dsh/skill-manifest.json`（唯一事实源）；新环境部署后跑 `python scripts/align_environment.py`（加 `--apply` 自动补装缺失项）；安装后补录 pin（commit hash）供多端对齐。

gotcha：多端可携带场景（多套 harness 并用）下第三方 skills 放项目级 `.agents/skills` 是合法权衡（随仓库走），代价是仓库膨胀与上游脱钩——单端运行不建议（多端并用评估结论）。

## gotchas

- **SKILL.md frontmatter 是 YAML，三条铁律**（三连事故实证）：①description 以 `[` 开头必须加引号，否则被解析为数组→技能整包下架 ②双引号串内禁英文双引号（用「」）③含反斜杠路径（`C:\Tools`）必须用**单引号**串（双引号下 `\T` 是非法转义）
- quicktask slug 一旦定名不可改（跨会话匹配靠它）
- 本标准是巡检项：inspection skill 抽查 §2.4 四条禁令
- 项目自身生态有更强约定时（如 pnpm workspace、Cargo），生态约定优先于本表，冲突记入项目 AGENTS.md
- 结构校验不依赖通用工具（Repolinter 已归档停维护）：非代码落位靠本 skill + inspection grep；代码结构靠语言原生强制（cargo/ruff/eslint-plugin-boundaries 进 CI）——"工具强制优于文档约定"是社区强共识
- **设计规范前先查外部共识**：本地先例 ≠ 社区共识，规范类产出必须先过调研再落笔

## 依据来源（2026-09 调研；原始调研档案存于内部 09_REFERENCE，发布包未随附，结论摘要如下）

- agent 友好结构（浅层可预测/唯一命令/一致命名）：Anthropic Claude Code Best Practices、agents.md 标准（6 万+项目采用）
- by-feature > 顶层 by-layer、过度结构化警告：Go 官方与社区（golang-standards 非官方且被警告勿套用）、Rust Cargo 文档
- 文档四象限：Diátaxis（diataxis.fr）；数据项目：Cookiecutter Data Science（data raw/interim/processed）
- monorepo：monorepo.tools（apps/packages）；结构约束工具：eslint-plugin-boundaries
- 个人组织体系对照：PARA（知名度高但 Areas/Resources 边界受批评）、Johnny Decimal（小众高忠诚）；AOS 的 INBOX 中转+指针模式与 agent 整理工作流趋势同构
