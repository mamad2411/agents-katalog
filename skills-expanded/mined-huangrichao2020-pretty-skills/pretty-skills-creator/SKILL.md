---
name: pretty-skills-creator
description: |
  创建新 skill 的入口，自动生成 4 件套骨架 + 必填 xxx讲解.pdf 占位说明。
  Use when 用户说"创建 skill / 做个新 skill / 做 skill / 沉淀到 pretty-skills / 提个新 skill"。
  流程: ps create <name> → 填 metadata → 自动生成 4 件套 → 跑 build_case_pdf.py 生成真 PDF → 提 PR。
  v3.20 改造：去 web.html + 去 4 风格 HTML 模板 + 去 --style 参数。
triggers:
  - 创建 skill
  - 做个新 skill
  - 做 skill
  - 沉淀到 pretty-skills
  - 提个新 skill
  - ps create
---

# pretty-skills-creator

> **创** — 让创建新 skill 像"填一个表"一样简单。

## 一句话

**pretty-skills-creator = 创建 skill 的 5 步流水线。**

```
ps create <name>  --title "..." --description "..." --triggers a b c
  → 校验输入（name / title / description / triggers）
  → 生成 4 件套：xxx讲解.pdf.placeholder.md + manifest.yaml + SKILL.md + CHANGELOG.md
  → 装到本地 store（ps create 自动软链 5 agent）
  → 你填细节 + 准备图 → 跑 build_case_pdf.py → ps contribute → 提 PR
```

## v3.20 改造

| 改动 | 原因 |
|---|---|
| ❌ 删 web.html | GitHub 不能预览 + PPT 时代已废 |
| ❌ 删 4 风格 HTML 模板 | 替代方案 = xxx讲解.pdf（GitHub 原生预览）|
| ❌ 删 --style 参数 | PPT 风格 picker 没了，PDF 是统一的 PIL 合并 |
| ✅ 加 xxx讲解.pdf.placeholder.md | 占位说明，告诉用户怎么跑 build_case_pdf.py |

## 必备参数

| 参数 | 校验 | 说明 |
|---|---|---|
| `--title` | ≥ 5 字 | Skill 标题（中文 / 英文都行） |
| `--description` | ≥ 100 字 | 一句话定位 + 详细说明（多行用 `\|` 或 `\n`） |
| `--triggers` | ≥ 3 个 | 触发词（用户自然语言） |

## 可选参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `--contributor` | `@anonymous` | 你的标识 |
| `--tags` | （无） | 标签列表 |
| `--related` | （无） | 关联资源描述 |
| `--out-dir` | （必填） | 输出目录 |
| `--dry-run` | `false` | 只看输出，不写文件 |
| `--created` | `2026-07-10` | 创建日期 YYYY-MM-DD |

## 完整流程

### Step 1 · 写参数

```bash
ps create my-new-skill \
  --title "我的新 skill 标题" \
  --description "$(cat <<EOF
这是一个非常厉害的新 skill，解决了 XXX 问题。
它的核心思路是 YYY，用法是 ZZZ。
适用场景：AAA / BBB / CCC。
EOF
)" \
  --triggers 触发词1 触发词2 触发词3 触发词4 \
  --contributor "huangrichao2020" \
  --tags "tag1" "tag2" \
  --related "knowhub 路径 / 关联 skill" \
  --out-dir "$HOME/.pretty-skills/store"
```

### Step 2 · 校验

脚本会自动校验：
- ✅ name 合法（kebab-case，2-64 字符）
- ✅ title ≥ 5 字
- ✅ description ≥ 100 字
- ✅ triggers ≥ 3 个

### Step 3 · 生成 4 件套

```
~/.pretty-skills/store/my-new-skill/
├── xxx讲解.pdf.placeholder.md   # 怎么跑 build_case_pdf.py 的说明
├── manifest.yaml                # 符合 pretty-skills manifest schema
├── SKILL.md                     # agent 加载入口
└── CHANGELOG.md                 # 变更记录
```

### Step 4 · 准备图 + 跑 build_case_pdf.py

```bash
cd ~/.pretty-skills/store/my-new-skill

# 1. 准备 AI 出图（每页 1 张）
# 用 matrix / DALL-E / 即梦 任意工具
mkdir images
# 把 PNG 放到 images/slide-01.png / slide-02.png / ...

# 2. 跑 PIL 合并 → xxx讲解.pdf
python3 ../../tools/build_case_pdf.py "my-new-skill"
# 工具路径：pretty-skill/tools/build_case_pdf.py · v3.20 极简版（5 行核心）
```

### Step 5 · 软链到 5 agent + 提 PR

```bash
ps add my-new-skill           # 软链到 ~/.claude/ ~/.codex/ ~/.mavis/ ~/.cursor/ ~/.windsurf/

cd ~/.pretty-skills/store/my-new-skill
# 改 SKILL.md / manifest.yaml 补细节
ps contribute my-new-skill
```

`ps contribute` 会：
1. fork 主项目
2. clone fork → 创建分支
3. copy 4 件套 → commit
4. push 分支
5. 提 PR with `auto-deploy-placeholder` + `skill-status:placeholder` 标签
6. 主项目自动 merge + 部署 Git Pages

## 跟 pretty-skills（管）的关系

- **pretty-skills（管）**：管理所有 skill 的增删改查
- **pretty-skills-creator（创）**：创建新 skill 的入口
- 二者是父子：装好 pretty-skills 后，`ps create` 就调 pretty-skills-creator

## 缺能力时体验会差

- ❌ 没 `python3` → `ps create` 整个不能用
- ❌ 没 `gh` / `gh auth` → `ps contribute` 不能用 → 退路：手动用 `bash scripts/push.sh` 或网页提 PR
- ❌ 没 matrix MCP / AI 出图 API → 跑不出真 PDF → 退路：用占位图跑骨架（check-3f 跑通 F3 必填）

跑 `ps doctor` 看完整体检。
