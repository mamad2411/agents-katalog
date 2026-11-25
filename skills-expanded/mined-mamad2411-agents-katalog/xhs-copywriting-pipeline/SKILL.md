---
name: xhs-copywriting-pipeline
description: 小红书图文选题与文案流水线技能。用于按关键词抓取小红书高赞高评论参考内容，结合用户账号/IP人设产出 3-5 个差异化选题，并在用户确认后继续生成最终图文文案。适用于“做一个小红书文案 skill”“小红书流水线”“先抓 10 篇爆文再做选题/写文案”“根据我的 IP 写小红书爆款文案”“做小红书选题策划和正文生成 pipeline”等场景。
---

# 小红书文案流水线（正式版 v1.1，agent-native）

这是一个 **三阶段可续跑流水线 skill**。目标不是一次性胡乱生成，而是像 Jenkins pipeline 一样，把每一轮小红书创作拆成独立 run，支持中断、确认、续跑、落盘。

这个 skill 采用 **agent-native** 设计：
- 确定性步骤（抓取、状态管理、保存文件、长度校验、依赖检查）由脚本负责
- 智能步骤（选题策划、正文生成、SEO 布局）由 OpenClaw agent 自身负责
- 不内置任何模型私钥

## 先读哪些文件

首次触发只读：
- `references/workflow-spec.md`
- `references/user-ip-template.md`
- `references/seo-guidelines.md`

做选题时再读：
- `references/topic-planner-prompt.md`
- `<run-dir>/ref/articles.md`
- `<run-dir>/ref/seo-brief.md`
- `<run-dir>/inputs/user_ip.md`

写正文时再读：
- `references/copywriter-prompt.md`
- `<run-dir>/ref/articles.md`
- `<run-dir>/ref/seo-brief.md`
- `<run-dir>/inputs/user_ip.md`
- `<run-dir>/plan/chosen-topic.json`

## 可移植性规则

不要假设所有用户都使用你的服务器路径。
始终：
- 使用 `scripts/`、`references/` 这种相对 skill 根目录的路径
- 通过脚本自动检查 `xhs` 命令是否存在
- 如果未安装或未登录，明确提示用户先安装 `xiaohongshu-cli` 并完成认证

## 工作目录规范

每次 run 默认放在当前工作目录下的：
`./xhs-copywriting-runs/<timestamp>-<keyword>/`

也可通过环境变量覆盖：
- `XHS_PIPELINE_WORKSPACE`
- `XHS_PIPELINE_RUNS_DIR`
- `XHS_PIPELINE_XHS_BIN`

结构：

```text
<run-dir>/
├── workflow.json
├── inputs/
│   ├── keyword.txt
│   └── user_ip.md
├── ref/
│   ├── articles.json
│   ├── articles.md
│   ├── seo-brief.md
│   ├── note-01-*.json
│   ├── note-01-*.md
│   └── ...
├── plan/
│   ├── topic-options.md
│   ├── chosen-topic.json
│   └── chosen-topic.md
└── drafts/
    └── final.md
```

## 阶段 0：依赖检查（强烈建议先做）

先运行：

```bash
python3 scripts/run_pipeline.py doctor
```

如果失败：
- 提示安装 `xiaohongshu-cli`
- 提示执行 `xhs login` / `xhs status`
- 如 `xhs` 不在 PATH，提示配置 `XHS_PIPELINE_XHS_BIN`

## 阶段 1：抓取参考爆文

如果缺少信息，先向用户要：
- 搜索关键词
- 用户 IP 信息

执行：

```bash
python3 scripts/fetch_refs.py \
  --keyword "<关键词>" \
  --count 10 \
  --pages 2 \
  --user-ip-text "<用户IP信息>"
```

抓取脚本会：
- 调用本机 `xhs`
- 搜索小红书内容
- 按点赞/评论/收藏/分享综合打分筛选前 10 篇
- 逐篇读取详情
- 保存到 `ref/`
- 自动生成 `ref/seo-brief.md`
- 自动更新 `workflow.json`

## 阶段 2：做选题策划

只在 `workflow.stage == refs_fetched` 时进入。

你要做的事：
1. 读取 `ref/articles.md`
2. 读取 `ref/seo-brief.md`
3. 读取 `inputs/user_ip.md`
4. 读取 `references/topic-planner-prompt.md`
5. 由 **agent 自身** 基于这些材料生成 3-5 个差异化选题方案
6. 将完整内容保存到：`plan/topic-options.md`
7. 调用脚本推进阶段到 `topic_options_generated`

更新阶段：

```bash
python3 scripts/run_pipeline.py save-plan --run-dir "<run-dir>" --plan-file "<topic-options.md>"
```

### 选题阶段硬约束
- 每个“核心切入点一句话总结”：**20字以内**
- 每个爆款标题候选：**20字以内**
- 必须具备 SEO 布局意识：标题候选优先覆盖主关键词、次关键词、场景词

### 强制暂停点
阶段 2 完成后，**必须停下来等用户选题**。
不允许跳过确认直接写正文。

## 阶段 3：确认选题并生成正文

当用户选定方案后：
1. 从 `plan/topic-options.md` 读取对应方案
2. 为该方案确定最终标题
3. 将用户确认结果保存到：
   - `plan/chosen-topic.json`
   - `plan/chosen-topic.md`
4. 更新阶段到 `topic_confirmed`
5. 再读取 `references/copywriter-prompt.md`
6. 由 **agent 自身** 基于确认选题、用户 IP、SEO brief、参考爆文生成最终文案
7. 保存到 `drafts/final.md`
8. 更新阶段到 `draft_generated`

更新确认状态：

```bash
python3 scripts/run_pipeline.py choose-topic \
  --run-dir "<run-dir>" \
  --option 2 \
  --title "<最终标题>" \
  --summary "<一句话概述>" \
  --topic-outline "<大纲>"
```

保存最终草稿：

```bash
python3 scripts/run_pipeline.py save-draft --run-dir "<run-dir>" --draft-file "<final.md>"
```

### 正文阶段硬约束
- 最终标题：**20字以内**（含标点、Emoji）
- 最终正文：**1000字以内**
- `save-draft` 会自动校验长度，不通过则必须压缩重写
- 标题、正文、标签都要有 SEO 意识，但不能生硬堆词

## 默认交互策略

### 新建流程
1. 收关键词
2. 收用户 IP 信息
3. doctor / fetch
4. 做选题策划
5. 暂停等待确认

### 继续流程
如果用户回来只说：
- “选第 2 个”
- “把第 3 个改狠一点”
- “继续写正文”

先检查 run 状态：

```bash
python3 scripts/run_pipeline.py status --run-dir "<run-dir>"
```

## 文件写入要求

### `plan/topic-options.md`
必须保留：
- 爆款逻辑拆解
- 3-5 个方案
- 每个方案的 SEO 布局说明
- 每个方案的 3 个标题候选
- 每个方案的简要内容大纲

### `plan/chosen-topic.json`
至少包含：
- `option_index`
- `chosen_title`
- `chosen_topic_outline`
- `chosen_summary`
- `user_note`

### `drafts/final.md`
格式必须是：

```text
【标题】
...

【正文】
...

【标签】
#标签1 #标签2 ...
```

## 故障处理

### 抓取不足 10 篇
如实告诉用户实际抓到多少篇，继续做，但在选题分析里标注样本不足。

### `xhs` 未安装或未登录
不要继续假装抓取成功。先提示安装 / 登录。

### 用户没给够 IP 信息
先用 `references/user-ip-template.md` 追问，不要硬编一个“用户人设”。
