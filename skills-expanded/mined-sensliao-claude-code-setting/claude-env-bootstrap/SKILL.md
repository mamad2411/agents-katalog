---
name: claude-env-bootstrap
version: 2.2.0
status: stable
created_date: 2026-05-23
updated_date: 2026-06-22
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
description: >-
  Manually invoked project environment bootstrap (disable-model-invocation: true) — scans project signals into a signal_vector, asks high-leverage gap questions, then evaluates declarative selectors from catalog.json to compose a minimal-yet-complete `.claude/` environment. Manual-first because it writes files, copies skills and generates CLAUDE.md. Safe on EXISTING non-empty projects: copies are no-clobber with incremental modes --scan-only / --add / --adopt. On "init project / bootstrap / set up claude environment / configure claude / 装环境 / 初始化 .claude", RECOMMEND `/claude-env-bootstrap` but never auto-execute.
---

# claude-env-bootstrap v2.0.0 — Selector-Engine 智能装配

> **核心理念**:bootstrap 是**装配工**,不是包管理器。每个项目都不同 — bootstrap 不该是"挑预设 bundle",而是"扫描项目实情 + 推导信号向量 + 按 selector 智能匹配 → 实时编一份贴合此项目的 .claude/"。
>
> **v2.0.0 关键变化**:从 hardcode inclusion 表(v1.x)切换到 declarative selector engine。所有"装哪些 skill"的知识从 SKILL.md 迁移到 `catalog.json`,SKILL.md 只保留**引擎逻辑 + 工作流 + 反模式**。

---

## 1. 何时调用

✅ **应当调用**:
- 新项目装配 `.claude/`
- 已有项目但 `.claude/` 是空的 / 内容过时
- 团队成员需要"clone-and-run"的自包含项目仓库
- 全局 `~/.claude/` 更新了,想把新内容同步到项目(`--update` 模式)

❌ **不应调用**:
- 单文件改动 / 临时实验
- 已有完善 `.claude/` 且用户未要求重装

### 1.1 入口模式(v2.2 — 已有项目可用化)

| 模式 | 写盘? | 用途 |
|---|---|---|
| `/claude-env-bootstrap`(默认) | 写(**additive / no-clobber**) | 装配 `.claude/`。空目录=全量;非空=**只补缺、不覆盖任何已有文件**(EXECUTE 用 `cp -n`)|
| `--scan-only` | **零写** | 只读评估:扫项目 → 算该装啥 → 出清单,不写任何文件。任何项目(空/半配/全配)都安全(§3.0.6)|
| `--add <skill\|subsystem>` | 写(additive) | 给已有项目**增量装一个**能力 + 依赖(subsystem 包一层 SDK init),不全量重编(§7.7)|
| `--adopt` | 写(**仅新建 manifest,不碰其它**) | 已有 `.claude/` 但无 manifest → 扫现状生成描述性 v2 manifest,纳入管理(解死循环,§8.1)|
| `--update` | 写(merge) | 已 bootstrap 过的项目同步全局更新(§8)|
| `+ --force` | 写(**覆盖**) | 唯一会覆盖已有文件的开关;必须在 PROPOSE 显式确认 |

**默认即安全**:不加 `--force` 时 EXECUTE 永不覆盖你的文件——所以 v2.2 起非空项目**默认可直接跑**(不再一刀 BLOCK,见 §3.0.2)。

---

## 2. 六步工作流(严格顺序,不准跳)

```
Step 0 — PREFLIGHT  collision check: 项目 `.claude/` 是否已存在? 调用形式是否匹配? (§3.0)
Step 1 — SCAN       扫描项目状态,输出 signal_vector(25 raw + ~8 derived)
Step 2 — ASK        最多 4 题(合并成 1-2 个 AskUserQuestion),填补 SCAN 推不出的意图
Step 3 — COMPOSE    读 catalog.json,对每个 skill 跑 selector 评估;resolve 互斥 + handoff
Step 4 — PROPOSE    输出 dry-run 清单(skill + selector evidence + rules + templates + agents)
Step 5 — EXECUTE    用户确认后复制 + 生成 CLAUDE.md + 写 manifest.json(含 selector evidence)
Step 5b — VERIFY    post-EXECUTE 校验: files_written / manifest v2 / subsystem hooks registered (§7.5)
Step 5c — PROVISION per-project 工具备齐: 按选中 skill 跑 provision-tools.js — auto 自动装 / credential 报告待设 / ROE-time 攻击工具不装 / manual 给命令 (§7.6)
```

每步必经, Step 4 必须等用户确认才进 Step 5。Step 0 / Step 5b 是 hard gate, 不准跳, 不准 advisory。Step 5c (PROVISION) 是 report-only,绝不阻断 bootstrap(工具装不上 → 报告 + 降级,不让 bootstrap 失败)。

---

## 3.0. Step 0 — PREFLIGHT (collision check, before SCAN)

**强制第一步, 不准跳, 不准延后**。负责回答两个问题:
1. 本项目是否已有 `.claude/` 目录? 若有, 内容是什么? 是否安全继续?
2. 是否被 `--update` 显式触发? 还是 fresh-install 路径?

### 3.0.1 必跑的 collision check

```
collision_paths = list(Glob "<project>/.claude/**/*")
manifest_exists = Read "<project>/.claude/manifest.json"  → JSON 或 NotFound
```

### 3.0.2 决策表(v2.2 — 默认 additive,不再一刀 BLOCK)

> **核心变化**:EXECUTE 现在 no-clobber(`cp -n`,§7.1),plain invoke 在非空项目上**不再具破坏性** → 因此**不再 HARD BLOCK**,改为默认走 additive(只补缺 + 报告 already-exists)。HARD BLOCK 只留给"会真覆盖且未授权"(`--force` 未确认)的窄情形。

| 状态 | 用户调用形式 | 行为 |
|---|---|---|
| `.claude/` 为空 | `/claude-env-bootstrap` | **PASS** → 全量 fresh-install(Step 1 SCAN…)|
| `.claude/` 非空 + 无 manifest | `/claude-env-bootstrap` | **PASS(additive)** → 正常走 SCAN…EXECUTE,但 EXECUTE no-clobber(只补缺、不覆盖);PROPOSE 列出 will-add vs already-exists。可选提示 `--scan-only` 先看 / `--adopt` 纳管 |
| `.claude/` 非空 + 有 manifest | `/claude-env-bootstrap` | **PASS(additive)** → 同上;想全量重新对齐全局则提示 `--update` |
| 任意状态 | `--scan-only` | **PASS(只读)** → §3.0.6,零写 |
| 非空 + 无 manifest | `--adopt` | **PASS** → §8.1 生成描述性 manifest(不覆盖文件)|
| 有 manifest | `--update` | **PASS** → §8 |
| 无 manifest | `--update` | **SOFT REDIRECT** → 提示"无 manifest;建议先 `--adopt` 纳管,或无参数 additive 装",不再 hard-block |
| 任意 + `--force` | `/claude-env-bootstrap --force` | **会覆盖** → 必须在 PROPOSE 显式确认(§3.0.3 narrow BLOCK 兜底);唯一破坏性路径 |

### 3.0.3 BLOCK 输出格式(v2.2 — 仅 narrow 情形)

> v2.2 起 plain invoke 不再 BLOCK(默认 additive)。**只有** `--force`(会覆盖已有文件)且用户未在 PROPOSE 显式确认时,才走下面的 BLOCK。其余情况(非空 / 无 manifest)一律 additive PASS 或软提示,绝不一刀拒绝。

当(narrow)BLOCK 时, 输出给用户:

```
## Preflight BLOCK

检测到 collision (项目 `.claude/` 已存在但状态不一致):

  Existing paths:
    .claude/manifest.json (version: <X.Y.Z>)   ← 或 NotFound
    .claude/CLAUDE.md
    .claude/skills/... (<count> entries)
    .claude/rules/... (<count> entries)
    .claude/agents/... (<count> entries)

  Your command: `/claude-env-bootstrap` (no flag)

  这不安全。两个安全选项:
  1. 备份现有 `.claude/` (例如 `mv .claude .claude.bak-<date>`) 然后重新跑此命令
  2. 跑 `/claude-env-bootstrap --update` 进入 v1→v2 迁移路径 (见 §8)

  绝不静默覆盖。
```

### 3.0.4 为什么 Preflight 必须在 Step 1 SCAN 之前

- SCAN 不区分 "fresh-install" 和 "已有 `.claude/` 但不一致" 的差别 — 它只读项目源码 signal
- COMPOSE 会基于 selector engine 决定要装什么 — 如果不知道现有状态, propose 出来的清单会和实际状态冲突
- EXECUTE 复制文件会覆盖现有内容 — 一旦走到这步就晚了

Preflight 是 hard gate, 不是 advisory。绝不静默 PASS。

### 3.0.5 例外: Skill 自身被 `disable-model-invocation: true` 保护

Preflight 检测的是 **项目状态**, 不影响 skill 本身的 manual-first 边界:
- 此 skill 必须由用户显式 `/claude-env-bootstrap` 触发
- Preflight 跑在用户已显式调用 skill 之后
- Preflight(narrow `--force`)BLOCK 时, 模型不主动进 Step 1; 必须等用户处理后再调一次

### 3.0.6 `--scan-only` 模式(只读评估,零写)

任何项目都能跑(空 / 半配 / 全配),**绝不写任何文件**。流程:PREFLIGHT(只报告 collision 现状)→ Step 1 SCAN → Step 3 COMPOSE → Step 4 PROPOSE → **STOP**(不进 EXECUTE)。输出:

- 项目是什么(signal_vector 摘要 + derived)
- 该装什么(selector 命中的 skill / rules / agents / subsystem)
- **已有什么 vs 缺什么**(逐项对照现有 `.claude/`:already-present / would-add)
- 工具差什么(`provision-tools.js --dry-run`)
- 建议的下一步命令(无参数 additive 装 / `--add X` / `--adopt`)

用途:动手前对已有项目拿一份**非破坏性体检 + 装配建议**。这是 §1.1 表里"零写"那行的展开。

---

## 3. Step 1 — SCAN(signal_vector 生产)

### 3.1 工具

- `Glob` / `Read` / `Grep` / `Bash ls` — 检测文件结构
- 不准只靠用户主观回答 — 那是 Step 2 的事

### 3.2 检测顺序

对每个 raw signal,按 **文件结构 > manifest 内容 > 代码 grep** 顺序检测,先命中先用。完整 25 个 signal + 检测规则见 [`templates/SCAN-VECTOR-SCHEMA.md`](templates/SCAN-VECTOR-SCHEMA.md)。

### 3.3 关键 signal 检测速查

检测顺序：**文件结构 > manifest 内容 > 代码 grep**（先命中先用）。完整速查表（每个 signal 的检测命令）见 [`references/scan-cribs.md`](references/scan-cribs.md)；完整 25 signal 见 [`templates/SCAN-VECTOR-SCHEMA.md`](templates/SCAN-VECTOR-SCHEMA.md)。高频 signal：`lang` / `framework` / `deploy_target` / `risk_surface.{auth,payment,multitenant,file-upload,websocket,llm-agentic}` / `cn_data_signal` / `multitenant_signal` / `payment_signal` / `mobile_native_signal`。

### 3.4 env_baseline_gaps 检测

按 severity 检测（完整检测命令表见 [`references/scan-cribs.md`](references/scan-cribs.md)）：
- **CRITICAL**：`secret-in-dockerfile`（Dockerfile 用 `ARG SECRET_*` / `ENV SECRET_*` 传 secret）
- **HIGH**：`missing-lockfile` / `missing-env-example` / `missing-healthz` / `missing-migration-tool`
- **MED**：`missing-nvmrc` / `missing-validator`
- **LOW**：`missing-gitattributes` / `missing-editorconfig`

### 3.5 Derived signals 推导

raw signals 全部收集完,**在 SCAN 末尾推导 derived signals**。完整推导规则见 SCHEMA §3。要点:

- `_derived.is_saas = payment_signal AND multitenant_signal AND surface.public-web`
- `_derived.needs_release_gate = surface.public-web OR distribution.app-store OR distribution.play-store`
- `_derived.needs_compliance_payment = payment_signal AND risk_surface.financial`
- `_derived.needs_compliance_cn = cn_data_signal AND risk_surface.pii`
- `_derived.is_research_only = notebook_research AND deploy_target.none AND NOT ui_present`

### 3.6 SCAN 输出格式(给用户预览)

```
## SCAN 报告

### Raw signals
- lang: [ts]
- framework: [next]
- runtime: [node, edge-function, browser]
- deploy_target: [vercel]
- surface: [public-web]
- risk_surface: [auth, payment, multitenant, pii, public-api]
- llm_provider: [anthropic]
- ai_pattern: agentic
- ...(完整向量)

### Derived signals
- _derived.is_saas: true
- _derived.needs_release_gate: true
- _derived.needs_compliance_payment: false
- ...

### 状态推断
- 新项目 / 含 LLM agent / 多租户 SaaS / Vercel 部署 / 准备上线
```

---

## 4. Step 2 — ASK(填补 SCAN 推不出的意图)

### 4.1 规则

- 最多 **4 题**,合并成 **1-2 个 `AskUserQuestion`** 调用
- 只问 SCAN 推不出的(意图 / 上线意愿 / 风格倾向 / pentest 意图)
- 不问 SCAN 已能确定的(语言 / 框架 / 部署目标)

### 4.2 必问

**Q1** — 项目一句话描述(填补 surface / content_type)
**Q2** — 交付物形态: `提案型 demo` / `上线生产` / `内部工具` / `研究/论文` / `开源 lib` / `文档/咨询`(填补 surface / distribution)

### 4.3 条件问(根据 SCAN 结果)

| SCAN 结果 | 加问 |
|---|---|
| `ui_present == true` 且 `style_intent == undecided` | Q-style: 风格倾向(`taste/luxury/brutalist/未定`)|
| `surface ⊇ public-web` 且 SCAN 没确定是否 marketing/docs/dashboard | Q-content: 内容类型 |
| `risk_surface` 含 auth/payment/admin | Q-pentest: 本里程碑做 pentest 吗?(默认 否) |
| `mobile_native_signal == true` 或 distribution 含 app-store | Q-aso: 上 App Store / Play Store? |
| 检测到任一代码项目信号 + 部署目标含 k8s/compose/systemd | Q-env: 环境一致性 baseline(secrets 来源 / Devcontainer / OS) |

### 4.4 合并 ASK 调用

正确做法 — 一次 4 题:
```
AskUserQuestion({
  questions: [
    {question: "项目一句话描述?", ...},
    {question: "交付物形态?", options: [...]},
    {question: "风格倾向?", options: [...]},
    {question: "本里程碑做 pentest 吗?", options: [是/否]}
  ]
})
```

错误做法 — 4 次连发 `AskUserQuestion`(用户烦)。

### 4.5 ASK 结果 merge 进 signal_vector

ASK 答案直接写入对应 signal 字段:
- Q-style 答案 → `signal_vector.style_intent`
- Q2 答案 = "研究/论文" → `signal_vector.surface = ["research"]`,`distribution = ["none"]`
- Q-pentest = 是 → 标记 `manual_question_answers.Q-pentest = true`(供 COMPOSE 处理 manual_only_question selector)

---

## 5. Step 3 — COMPOSE(selector engine)

### 5.1 引擎逻辑(伪代码)

```
catalog = Read(catalog.json)
plan = []
for skill_name, meta in catalog.skills:
    # Manual-only check
    if meta.selector.never == true:
        if meta.manual_only_question in manual_question_answers and
           manual_question_answers[meta.manual_only_question] == true:
            plan.add(skill_name, reason="manual:" + meta.manual_only_question)
        continue
    # Standard selector eval
    if evaluate(meta.selector, signal_vector):
        if not blocked_by_excludes_when(meta, signal_vector):
            plan.add(skill_name, reason="selector match: " + matched_predicates)

# Resolve handoff chains (requires)
for skill in plan:
    for dep in catalog.skills[skill].requires:
        if dep not in plan:
            plan.add(dep, reason="auto-pulled by " + skill)

# Resolve mutex groups
for group_name in catalog.mutex_groups:
    candidates = [s for s in plan if catalog.skills[s].mutex_group == group_name]
    if len(candidates) > 1:
        # Prefer default_within_mutex == true; else prefer style_intent match
        winner = pick_one(candidates, signal_vector)
        plan.remove(c) for c in candidates if c != winner
```

### 5.2 Selector 评估规则

支持的 predicate 操作符:

| 操作符 | 含义 |
|---|---|
| `{"all_of": [P1, P2, ...]}` | 全部 P 成立 |
| `{"any_of": [P1, P2, ...]}` | 至少一个 P 成立 |
| `{"not": P}` | P 不成立 |
| `{"signal": "X", "equals": V}` | `signal_vector.X == V` |
| `{"signal": "X", "equals_exact": V}` | 数组完全相等(顺序+值) |
| `{"signal": "X", "contains": V}` | 数组 X 含 V |
| `{"signal": "X", "contains_any": [V1, V2]}` | 数组 X 含 V1 或 V2 |
| `{"signal": "X", "in": [V1, V2]}` | 标量 X 属于列表 |
| `{"signal": "X", "exists": true, "non_empty": true}` | X 字段存在且非空 |
| `{"signal": "_derived.Y", "equals": V}` | derived signal Y |
| `{"never": true}` | 永不自动触发(仅 manual_only_question 触发) |

### 5.3 Handoff resolution

skill 的 `requires` 字段自动 pull 依赖:
- `security-app-multitenant.requires = [appsec-security-orchestrator]` → 装多租户 overlay 自动也装 orchestrator
- `web-aeo.requires = [discoverability-orchestrator]` → 装 web-aeo 自动也装 orchestrator

### 5.4 Mutex 处理

`catalog.mutex_groups` 列出互斥组。多个 skill 同 mutex_group 时:
1. 优先选 `style_intent` 匹配的(用户明确选了某风格 → 对应 L3 skill)
2. 否则选 `default_within_mutex == true` 的
3. L3 style 组若都没明确意向 → 装 `taste-skill`(default)

### 5.5 Rules / Templates / Agents 附加

skill 入选后,其 `rules_addon` / `template_addon` / `agent_addon` 列表也加入复制队列。同名只装一次。

### 5.6 反模式 — selector 引擎绝不允许

- ❌ 在 SKILL.md 里硬编码"凡是 X 就装 Y"(应该写进 catalog.json selector)
- ❌ 在 COMPOSE 阶段补 default skill 列表(应该改 catalog.json selector 触发条件)
- ❌ 全装 catalog 所有 skill(违背"匹配 = 装,不匹配 = 不装"原则)
- ❌ 多个 L3 style 同时入选(必须 mutex resolve)
- ❌ 装 `authorized-pentest-validation` 但跳过 `pentest-scope-and-roe`(`requires` 字段必须遵守)

---

## 6. Step 4 — PROPOSE(dry-run)

### 6.1 输出格式

PROPOSE 是 dry-run 预览（**SEMI-CRIB 骨架**；完整逐字段示例 + selector evidence 写法见 [`references/propose-template.md`](references/propose-template.md)）。必含以下 section（顺序固定）：

1. **SCAN 摘要** — 推断的 derived signals + 可折叠的完整 raw vector
2. **ASK 答案** — Q1/Q2 + 条件问回答
3. **将装的 skills**（按 domain 分组：GSD 核心 / AppSec / Discoverability / UIUX…），每条带 selector evidence
4. **将装的 rules** / **将装的 templates** / **将装的 agents**
5. **将创建的文件**（`.claude/CLAUDE.md` / `manifest.json`(v2,含 selector evidence) / `skills/` / `rules/` / `agents/` / `templates/`）
6. **排除清单**（SCAN 检测到但未入选 + 逐条排除原因）
7. **确认提示**：`确认执行? [Y / 调整清单 / 取消]`

> **工具预览（Step 5c 的 dry-run）**：PROPOSE 还应展示**将装的工具**——跑 `node ~/.claude/scripts/bootstrap/provision-tools.js --project-root . --skills "<plan>" --dry-run`,把 auto(自动装）/ credential(待设凭证）/ ROE-time(攻击工具默认不装）/ manual(手动）分档给用户看。让用户在确认前就知道"装这些 skill 会顺带下哪些工具"。

**铁律**：Step 4 PROPOSE 必须等用户确认才进 Step 5 EXECUTE（§2）。绝不静默覆盖、绝不跳过确认。

### 6.2 调整清单

用户可以:
- 勾掉任何 skill(写入 manifest.user_excluded)
- 添加 catalog 里未入选但用户想装的(写入 manifest.user_added)
- 改 mutex 选择(例: taste-skill → luxury)

---

## 7. Step 5 — EXECUTE

### 7.1 文件操作顺序

```bash
# 1. 创建目录
mkdir -p .claude/{skills,rules,agents,templates}

# v2.2 DEFAULT no-clobber: 已存在的文件一律保留、绝不覆盖,只补缺。--force 才覆盖。
CP="cp -n"; CPR="cp -rn"                                  # 默认 additive / no-clobber
[ "${force:-0}" = "1" ] && { CP="cp"; CPR="cp -r"; }     # --force → overwrite(须 PROPOSE 确认)
# 复制前先记 already-exists,EXECUTE 末尾报告 added vs skipped(见下方 additive 说明)

# 2. 复制每个 skill(整个目录)—— 按 catalog.json 的 `kind` 字段分派来源
for skill in plan.skills:
    case catalog[skill].kind in
      reviewer)   # 实为 agent，住在 ~/.claude/agents/<name>.md，非 skills/ 目录
        $CP ~/.claude/agents/$skill.md .claude/agents/$skill.md ;;
      plugin)     # plugin-sourced(如 claude-api 住在 plugins/marketplaces/...)，不 cp
        echo "[bootstrap] $skill 是 plugin skill，不复制 —— 运行 claude plugin install $skill" ;;
      *)          # 无 kind / 普通 skill：no-clobber 合并入目标(已存在文件保留,只补缺)
        mkdir -p .claude/skills/$skill && $CPR ~/.claude/skills/$skill/. .claude/skills/$skill/ ;;
    esac

# 3. 复制 agents
for agent in plan.agents:
    $CP ~/.claude/agents/$agent.md .claude/agents/$agent.md

# 4. 复制 rules + addons(目录用 src/. 合并形式,避免嵌套)
mkdir -p .claude/rules/common && $CPR ~/.claude/rules/common/. .claude/rules/common/
mkdir -p .claude/rules/{lang} && $CPR ~/.claude/rules/{lang}/. .claude/rules/{lang}/    # 按 signal_vector.lang
$CP ~/.claude/rules/$addon .claude/rules/$addon       # rules_addon(单文件,cp -n 即可)

# 5. 复制 templates(skill 的 template_addon + 全局 templates/)
mkdir -p .claude/templates/planning
$CP ~/.claude/templates/planning/$tpl .claude/templates/planning/

# 6. 装配 subsystem project hooks(见 §7.1a)—— 对每个入选 subsystem 调其 SDK init
#    init 会:建 <sub> config(若缺)→ 复制 project-local hooks → merge .claude/settings.json
for sub in $selected_subsystems:   # appsec / qa / uiux / discoverability
    run "<sub>-sdk init"           # 无 release-tag:只装 config + hooks(幂等)

# 7. 生成 CLAUDE.md(用 templates/CLAUDE-MD-TEMPLATE.md)
# 8. 生成 manifest.json v2(含 selector_evidence)

# 9. seed §0.7 持久账本的固定入口 .goals/LEDGER.md —— 让跨-session 目标从第一天就有固定的家。
#    NEVER clobber:已存在就跳过(项目可能已自带 ledger / 自己的重定向)。内容 = 最小 stub。
mkdir -p .goals
if [ ! -f .goals/LEDGER.md ]; then cat > .goals/LEDGER.md <<'LEDGER_STUB'
# Goals / durable ledgers — FIXED ENTRY (global CLAUDE.md §0.7)

> The single fixed entry point for this repo's cross-session goals — a new session reads THIS first.
> Each active initiative lives here (a section) or redirects to a project-owned ledger; pair each with
> a `project` memory pointer in ~/.claude/projects/<slug>/memory/ so a /clear-resume finds it.

## Active initiatives

_(none yet — the first multi-phase work records its goal + 断点 + next-step here.)_
LEDGER_STUB
fi
```

> **§0.7 seed (step 9):** EXECUTE drops a `.goals/LEDGER.md` stub so every bootstrapped repo has the §0.7
> durable-ledger fixed entry from day one (kills the "现编文件名/位置" ad-hoc). It is **never-clobber** —
> an existing `.goals/LEDGER.md` is left untouched. The `ledger-reminder.js` Stop hook (wire-manifest batch
> C) is the runtime backstop for repos that predate this or that skip it.

> Windows 兼容:用 `cp -rn` / `cp -n` 不用 symlink。
>
> **Additive / no-clobber 默认(v2.2)**:#2–#5 的复制默认 `-n`(no-clobber)——目标已存在的文件**一律保留不覆盖**,只补缺。这是 shell 层的真保证(非靠模型自觉)。EXECUTE 必须报告 `added: [...]` 与 `already-exists, skipped: [...]`。只有 `--force` 才覆盖,且须 PROPOSE 显式确认。#6 subsystem(SDK init)/ #7 CLAUDE.md(§7.4 merge)/ #9 `.goals/`(never-clobber)本就不覆盖。
>
> **目录复制必须用合并形式** `mkdir -p 目标 && cp -rn 源/. 目标/`(注意 `源/.`)——实测 `cp -rn 源 目标` 在目标已存在时会**嵌套**成 `目标/源`(空目录无此问题,但非空就错)。单文件 `cp -n 源 目标文件` 无此坑。

> **`kind` 字段语义(catalog.json,影响 step 2 来源分派)**:
> - `kind: "reviewer"` → 条目实为 agent,住在 `~/.claude/agents/<name>.md`(不是 skills/ 目录),`cp` 单文件到 `.claude/agents/`(如 `typescript-reviewer` / `python-reviewer`)。
> - `kind: "plugin"` → plugin-sourced skill(住在 `plugins/marketplaces/.../skills/`),**不复制**,只在 EXECUTE 输出 `claude plugin install <name>` 提示(如 `claude-api`)。
> - 其余 kind(`core`/`orchestrator`/`narrow`/`overlay`/`l3-style`/`workflow`,或缺省)→ 默认行为:`cp -r ~/.claude/skills/<name>`。

### 7.1a Subsystem hook 装配(Step 6 展开)——v2.1.0 闭合 ORACLE-001

EXECUTE 复制 skill/rules/agents 只是把**上下文**搬进项目;subsystem 的 **enforcement** 靠 hooks 注册进 `<project>/.claude/settings.json` 才生效(§7.5.3)。**关键变化(2026-05-30)**:不再把 hook 注册留给用户手动跑 —— 入选 subsystem 时,EXECUTE **自动**调其 SDK init,init 即 canonical hook-installer。

> ⚠️ **强制不可跳(2026-06-23 真机盲测教训)**:对每个入选 subsystem 跑 SDK init 是**最常被模型跳过**的一步——盲测里 agent 装完文件就收工、跳了它,导致 "context loaded ≠ enforced"(skill 在、enforcement hooks 没装)。它**不是可选**:§7.5b VERIFY **必 HARD BLOCK** 直到 hooks 注册到 `<project>/.claude/settings.json`。**实测这些 init 在 Windows 的 Git Bash 上完全可跑**(qa: 16 copied / 15 registered;appsec: 9;uiux: 4;全 exit 0)——**没有平台借口**。装完文件后**立刻**对每个入选 subsystem 跑下表命令,再进 §7.5b。

**判定哪些 subsystem 入选**:COMPOSE plan 里任一 skill 的 `domain`(见 catalog.json)落在下表 → 该 subsystem 入选(通常是其 orchestrator skill 入选即触发):

| domain / orchestrator skill | init 命令(从 project root 跑) | 装什么 |
|---|---|---|
| `appsec` / `appsec-security-orchestrator` | `bash ~/.claude/scripts/appsec-sdk.sh init` | `.appsec/config.json` + hooks (count: see `manifests/hook-registry.json`) |
| `qa` / `enterprise-qa-testing` | `bash ~/.claude/scripts/qa-sdk.sh init` | `.qa/config.json` + hooks (count: see `manifests/hook-registry.json`) |
| `uiux` / `uiux-product-orchestrator` | `bash ~/.claude/scripts/uiux-sdk.sh init` | `.uiux/config.json` + hooks (count: see `manifests/hook-registry.json`) |
| `discoverability` / `discoverability-orchestrator` | `python ~/.claude/skills/discoverability-orchestrator/scripts/discoverability-sdk.py --project-root . init` | `discoverability.config.yaml` + hooks (count: see `manifests/hook-registry.json`) |
| `i2r` / `idea-to-requirements-orchestrator` | `python ~/.claude/templates/i2r/scripts/i2r.py install --project .` | project-local **4-module toolchain** (`i2r.py`+`i2r_core.py`+`i2r_render.py`+`i2r_validate.py` + schemas + hooks) + hooks 注册进 `<project>/.claude/settings.json` (count: see `manifests/hook-registry.json`)。**I2R 变体**:命令是 `install`(不是 `init`——`init` 只 scaffold run folder);**config 可选**(缺省零配置即跑),hooks 以 `.i2r/` 存在与否 fail-open gate(不像其它 subsystem 用 `<sub>/config.json`)。产物是 `.i2r/runs/.../out/` 下的 Markdown 需求包。 |

> 真相源是 `~/.claude/manifests/hook-registry.json`(每个 subsystem 的 hook 枚举 + `install_command` + `config_gate`)。SDK init 内部读它装 hook,**勿在 SKILL.md / catalog.json 里 hardcode hook 数量**(会再次漂移)。PROPOSE 预览要显示具体数量时,从 `hook-registry.json` 读,不要写死。

**铁律**:
- init **无 release-tag** 跑(`<sub>-sdk init` 裸跑)= 只装 config + hooks,**幂等**,可安全重复跑。release-tag 由后续 orchestrator 在有 tag 时再 `init <tag>` / `set-active <tag>` 补。
- init 缺 `<sub>` config 时**自动从模板建**;已有则保留不覆盖。
- hooks 是 **project-local 自包含**(复制 `.js` 进 `<project>/.claude/hooks/`,settings.json 用 `${CLAUDE_PROJECT_DIR}`)→ 项目 clone / commit 后 hook 跟着走(user lock 2026-05-30)。
- 任一 init 报错(node 缺失 / 模板缺失)→ **不静默**,记进 PROPOSE/VERIFY 输出,让 Step 5b BLOCK 兜底。

### 7.2 manifest.json v2 Schema

每个 skill 记录:
- `name`
- `source_version`(从全局 SKILL.md frontmatter 读)
- `installed_at`
- `user_modified: false`(初始)
- `selector_evidence`(v2 新增): 记录哪个 selector predicate 命中、命中的 signal 值
- `source_path`(供 `--update` 比对)

详见 [`templates/MANIFEST-SCHEMA.md`](templates/MANIFEST-SCHEMA.md)。

> **Additive / adopt 写法(v2.2)**:非空项目 additive 装时,manifest **merge** 新条目、**不丢**已有条目(新加的 skill 追加进 `skills[]`,保留原有)。`--adopt`(§8.1)则**从现状生成** manifest——扫 `.claude/{skills,rules,agents}` 实际存在项,各记 `adopted: true` + `source: observed`(无 selector_evidence),**不覆盖任何文件**,只新建 manifest 本身。

### 7.3 CLAUDE.md 生成

用 `templates/CLAUDE-MD-TEMPLATE.md` 骨架填:
- 项目名(Q1 答案)
- Tech stack(signal_vector 摘要)
- 装的 skill 清单(按 domain 分组)
- 装的 rules 路径
- 业务 / Architecture / Conventions 三块**留空**

### 7.4 已有 CLAUDE.md 合并

检测到根目录已有 `CLAUDE.md`:
- 新建 `.claude/CLAUDE.md`(共存)/ 合并到根目录(末尾追加 "## Bootstrap Manifest")/ 跳过
- 合并模式不覆盖现有内容

---

## 7.5. Step 5b — VERIFY (post-EXECUTE checks, before declaring success)

**强制最后一步**, EXECUTE 完成后必跑。负责回答:
1. 装的文件实际写到磁盘了吗?
2. manifest.json 结构有效吗 (v2 schema)?
3. 被选中的 subsystem (AppSec / QA / UIUX / L12) 的 hooks 实际注册了吗?

### 7.5.1 强制检查项

```
verify_artifacts = {
  files_written: 比对 ManifestDelta.installed_files vs Glob "<project>/.claude/**/*"  → 列出 missing
  manifest_v2_valid: Read "<project>/.claude/manifest.json"  → 验证 version >= 2.0.0 + selector_evidence 段存在
  subsystem_hooks_registered: 对每个 selector 命中的 subsystem (appsec / qa / uiux / discoverability):
    Read "<project>/.claude/settings.json"
    检查 hooks 段是否包含该 subsystem 的 hook entries
    如果 SDK 提供 `--verify` 子命令 (e.g., `appsec-sdk verify`), 跑一次
}
```

### 7.5.2 决策表

| 检查项 | 失败行为 |
|---|---|
| `files_written.missing` 非空 | **BLOCK** — 装错了, 列出 missing 文件, 提示用户检查 EXECUTE 阶段输出 |
| `manifest_v2_valid` 为 false | **BLOCK** — manifest 格式坏了, 提示用户检查 COMPOSE 阶段 selector_evidence 段 |
| `subsystem_hooks_registered` 任一 subsystem 缺 hooks | **HARD BLOCK** — 这是 ORACLE-001 ("context loaded != enforced") 的核心场景, 必须 BLOCK |
| 所有检查通过 | **PASS** — 输出 "Bootstrap complete + Verified" |

### 7.5.3 为什么 Verify 必须存在(对应 ORACLE-001)

Recall oracle 来自 `.feedback/2026-05-26-rules-without-hooks-context-loaded-not-enforced.md`:

> Rules / CLAUDE.md 是 soft constraints (LLM 读到了上下文, 但执行时可能 ignore)
> Hooks 是 hard constraints (PreToolUse 直接 `exit 2` 阻断)
> 如果只装 rules 不装 hooks, 等于 "context loaded but not enforced"

EXECUTE 阶段写了文件不等于"环境就绪"。subsystem (AppSec / QA / UIUX / L12) 的 hooks **必须**注册到 `<project>/.claude/settings.json` 才有 enforcement 效果。Verify 是 hard gate, 强制核实这一点。

### 7.5.4 Verify BLOCK 输出格式

```
## Verify BLOCK

EXECUTE 写完了文件, 但环境未就绪:

  ✓ Files written: 47/47
  ✓ manifest.json: valid v2.1.0
  ✗ AppSec hooks not registered in .claude/settings.json
     - active-scan-guard.js: missing
     - secret-access-guard.js: missing
     - secret-redaction.js: missing
     - finding-schema-prewrite.js: missing
     - finding-schema-postverify.js: missing
     - pentest-authorization.js: missing
     - evidence-required.js: missing
     - governed-gate-workflow-guard.js: missing   ← Governed Gate Mode (CLAUDE.md §3.7, 2026-05-29) — PreToolUse[Workflow]

  原因: Step 6 的 subsystem init 没跑或跑失败 (e.g. node 不在 PATH / 模板缺失)。
  Subsystem 包含 hooks 但 .claude/settings.json 没注册 = context loaded ≠ enforced。

  修复路径 (从 project root 跑对应 init —— 即 Step 6 §7.1a 自动跑的同一命令，幂等):
    bash ~/.claude/scripts/appsec-sdk.sh init                                         # AppSec
    bash ~/.claude/scripts/qa-sdk.sh init                                             # QA
    bash ~/.claude/scripts/uiux-sdk.sh init                                           # UIUX
    python ~/.claude/skills/discoverability-orchestrator/scripts/discoverability-sdk.py --project-root . init   # L12

  每个 init 内部以 manifests/hook-registry.json 枚举为准注册全部该 subsystem hooks
  (含 governed-gate-workflow-guard §3.7；勿 hardcode 数量，否则会再次漂移)。
  跑完后重新调用 `/claude-env-bootstrap --update --verify-only` 重新验证。
```

### 7.5.5 PASS 后才能声明 Bootstrap Complete

未通过 Verify 之前, 绝不输出 "Bootstrap complete" 给用户。

---

## 7.6. Step 5c — PROVISION-TOOLS (per-project external-tool provisioning)

> 加入 2026-06-15。补 "skills 是 markdown,但它们的牙齿是外部 CLI / 包 / 凭证" 的缺口 —— 团队成员 clone 一套 `.claude/` 后,skill 在、工具没装,能力静默降级成 skipped 而没人知道缺了什么。Step 5c 在装完 skill 后,按**本项目实际选中的 skill** 备齐它们要用的工具。**per-project / 按需**:别的项目用不到的工具不装,这个项目选中的才装(user lock 2026-06-15)。

### 7.6.1 怎么跑

EXECUTE + VERIFY 通过后,跑(`--skills` 传 COMPOSE 选中的 skill 列表):

```bash
node ~/.claude/scripts/bootstrap/provision-tools.js --project-root . --skills "<COMPOSE 选中的 skill,逗号分隔>"
```

引擎读 `~/.claude/manifests/tool-requirements.json`(skill → 工具的单一真相源),对选中 skill 的工具求并集,按 tier 处理:

| tier | 行为 |
|---|---|
| `auto` | **自动装**(npm / pip / go / cargo / winget / scoop / brew / apt;project-dev 装进项目)。当前平台没有可自动化路径(需 WSL2 / 需 Docker / 需 admin / 无包管理器)→ **优雅降级成打印命令**,绝不静默 |
| `credential` | 永不装。报告 "设置 env var X(从 Y 获取)";已设则标 ✓ |
| `roe` | 攻击型 recon / authenticated-DAST / exploitation 工具。**bootstrap 默认不装**,报告为 "ROE 时再装"。仅当 `.claude/bootstrap.config.json.provision_offensive_tools === true`(或 `--provision-offensive`)才自动装 |
| `reference` | planning-only skill 仅**引用**、从不执行的工具(`security-pentest-exploitation-planning` 是 Read-only)→ **永不装** |
| `manual` | cluster-side(k8s)/ build-file 插件 / 重型 SDK / 平台锁定 → 报告命令 + 原因,不自动跑 |

### 7.6.2 安全边界(铁律)

- **装二进制 ≠ 放开攻击**:`settings.json` deny-list(sqlmap / hydra / msfconsole / zap-full-scan …)+ pentest ROE 双门仍管 "能不能跑",与是否装好无关。
- offensive(`roe` tier)工具 **bootstrap 默认不装**(`provision_offensive_tools` 缺省 false)。这是用户可在 `.claude/bootstrap.config.json` 翻成 true 的**单一开关**,不是装配工替用户决定。
- `reference`-tier(Metasploit / Sliver / Caldera / Pacu / BloodHound / ScoutSuite)**任何情况都不由 provisioning 装**。

### 7.6.3 报告 + 幂等

- 引擎写 `<project>/.claude/tool-status.json`(结构化)+ 打印分档摘要(已装 / 现装 / 没装成功-给命令 / 待设凭证 / ROE-时再装 / manual / reference)。
- **REPORT-ONLY,绝不阻断 bootstrap**(永远 exit 0)。装不上的工具不让 bootstrap 失败 —— 能力会优雅降级成 skipped(QA / AppSec / L12 引擎已验证这点)。
- **幂等**:已在的工具跳过,可安全重复跑。装完包管理器 / 设完凭证后重跑即可补齐。

---

## 7.7 增量模式 `--add <skill|subsystem>`(给已有项目装一个能力)

不走全量 SCAN/COMPOSE,**只装用户点名的一个 skill 或 subsystem + 其依赖**,additive(no-clobber)。流程:

1. **解析** target:catalog.json 查该 skill 的 `requires`(handoff 链)+ `rules_addon`/`agent_addon`/`template_addon`;subsystem(appsec/qa/uiux/discoverability)则取其 orchestrator skill + 该 domain。
2. **PROPOSE**:列出 will-add(target + 被 pull 的依赖)+ already-exists(跳过)+(subsystem)要跑的 SDK init。等确认。
3. **EXECUTE(additive)**:`cp -n` 复制(§7.1 同款 no-clobber);subsystem 跑 `<sub>-sdk init`(幂等,merge settings.json);manifest **merge** 追加新条目(不丢旧)。
4. **VERIFY + PROVISION**:只对新增项跑 §7.5 / §7.6。

边界:`--add` 永不覆盖已有文件;subsystem 的 enforcement 仍靠其 SDK init 注册 hook(§7.1a)。这条把"想给老项目只加 AppSec"从"全量重跑"降为一条命令。

## 8.1 `--adopt` 模式(纳管已有但无 manifest 的 `.claude/`)

解死循环:已有 `.claude/`(手动攒的 / 早先单跑过某 `<sub>-sdk init` / 老版本留下的)但**没有 v2 manifest** → 既过不了旧 BLOCK、`--update` 又因缺 manifest 不能跑。`--adopt`:

1. **扫描**现有 `.claude/{skills,rules,agents,templates}` + `.claude/settings.json` hooks + 各 `<sub>` config,枚举实际存在项。
2. **生成**描述性 v2 `manifest.json`:每项记 `name` / `source_path`(若能对上全局源)/ `adopted: true` / `source: observed`(无 selector_evidence——它不是 selector 装的)。
3. **绝不覆盖任何已有文件**——只**新建 `manifest.json`**(若已有 manifest 则报告并退出,改走 `--update`)。
4. 完成后该项目即"纳入管理",之后 `--update` 可正常增量同步。

边界:`--adopt` 是**纯登记**,不补缺、不删、不改;要补缺另跑无参数 additive 或 `--add`。

---

## 8. `--update` 模式  →  references/update-workflow.md
> Relocated (SAFE-A appendix — verbatim, not weakened; not needed to execute a run). Read on demand.
> `--update` 在合并新选中的 skill 后,**重跑 Step 5c PROVISION**(§7.6)为新增 skill 备齐工具 —— 这正是用户说的 "update 了就下载新的,需要的时候再下"。

---
## 9. 反模式(常见翻车)

- ❌ **回到 hardcode 时代**:在 SKILL.md 里直接列"装这几个 skill",绕开 catalog.json
- ❌ **塞进所有 catalog skill**:违背 selector engine 的"按需"原则
- ❌ **SCAN 凭主观**:不查文件直接问用户(应该先机器推断,ASK 只补缺)
- ❌ **跳过 PROPOSE**:不让用户确认就执行
- ❌ **多 L3 style 同装**:违反 mutex
- ❌ **symlink 替代 copy**:Windows 不工作
- ❌ **盲 `cp -r` 覆盖已有文件**(v2.2):默认必须 no-clobber(`cp -n`),已存在文件一律保留;只有 `--force` + PROPOSE 确认才覆盖
- ❌ **非空项目一刀 HARD BLOCK**(v2.2 已废):默认 additive PASS;HARD BLOCK 只留 narrow `--force` 未确认
- ❌ **装完文件就收工、跳过 subsystem SDK init**(2026-06-23 盲测教训):= context loaded ≠ enforced;§7.5b VERIFY 必 BLOCK。SDK init 在 Windows Git Bash 实测可跑(qa/appsec/uiux 全 exit 0),无平台借口
- ❌ **`--update` 覆盖 user_modified**:本地改动必须留 merge 机会
- ❌ **CLAUDE.md 内联 N 个 skill 介绍**:CLAUDE.md 应该是规则,不是 catalog 拷贝
- ❌ **混淆 enterprise-qa-testing 与 appsec-security-orchestrator**:QA ≠ AppSec,catalog 里也是两个 domain
- ❌ **`authorized-pentest-validation` 自动入选**:必须靠 Q-pentest manual answer 才入选
- ❌ **`pentest-scope-and-roe` 跳过**:`authorized-pentest-validation.requires` 强制要求
- ❌ **装 skill markdown 但不装它依赖的工具**:团队成员 clone 后能力静默降级成 skipped 而不知缺了什么(Step 5c PROVISION 必须跑,§7.6)
- ❌ **bootstrap 自动装攻击型(offensive)工具**:`roe`-tier 默认不装、`reference`-tier 永不装;只有用户显式 `provision_offensive_tools=true` 才自动装 recon / authenticated-DAST 类(§7.6.2)
- ❌ **provision 失败就让 bootstrap 失败**:Step 5c 是 report-only,装不上 → 报告 + 命令 + 降级,绝不阻断

---

## 10. 与其他 skill 的关系

| Skill | 关系 |
|---|---|
| `gsd-pipeline-orchestrator` | **上游 PM 入口** — 按 CLAUDE.md §2 Step 1,任何 non-trivial 工作先调 PM 总编排器;bootstrap 作为其 Phase-0 环境先决条件,建议在调 `gsd-pipeline-orchestrator` 之前完成 |
| `gsd-new-project` | 协同 — GSD Phase 0 可先跑 bootstrap |
| `/init` | 互补 — `/init` 写 CLAUDE.md 业务部分,bootstrap 写 manifest + skill 装配 |
| `skill-creator` | 不冲突 — 创建新 skill 后,需手动加 catalog.json 条目 |
| `update-config` | 协同 — bootstrap 后用 `update-config` 调 hooks / permissions |
| `appsec-security-orchestrator` v3.0 | 由 catalog selector 触发;orchestrator 自己决定调用哪些 AppSec sub-skill,bootstrap 只负责装齐 |
| `discoverability-orchestrator` | 同上 |
| `enterprise-qa-testing` | 同上 |

---

## 12. 一句话总结

> v2.0.0:bootstrap 不再"挑预设 bundle",而是**SCAN 信号 → catalog.json selector 智能匹配 → 装最贴合的 .claude/**。
> SKILL.md 是引擎,catalog.json 是数据。加 skill 改 catalog,不动 SKILL.md。
