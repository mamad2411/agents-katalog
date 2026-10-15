---
name: classifying-github-stars
description: Use when you need to analyze a GitHub account's starred repositories, propose categories, and optionally write the result back into GitHub Lists.
---

# Classifying GitHub Stars

这个 skill 用来把某个 GitHub 账号的 starred repositories 做成可执行的分类流程：先抓取 stars，再根据仓库元数据生成分类计划，最后在确认后写回 GitHub Lists。

## When To Use

- 你需要整理某个 GitHub 账号的 stars
- 你要把 stars 自动归类到 GitHub Lists
- 你希望先看到分类计划，再决定是否真正写入

## Requirements

- `gh` 已安装
- `jq` 已安装
- `gh auth status -h github.com` 通过
- 如需真正写入 Lists，默认应操作当前已登录账号本人的 stars

## Hard Boundaries

- 默认先 dry-run，再执行写入
- 不硬编码 token、密码、密钥
- List 名称冲突时直接停止，不自动猜测
- 对模糊仓库最多给 1 到 2 个 List，不做过度分类
- 如果目标账号不是当前登录账号，默认只做分析；除非用户明确要求把对方的公开 stars 导入到当前账号的 Lists

## Files

- `skills/classifying-github-stars/scripts/fetch-starred.sh`
- `skills/classifying-github-stars/scripts/apply-lists.sh`
- `skills/classifying-github-stars/references/github-star-classification.md`

## Workflow

### 1. 抓取 starred 数据

先导出目标账号的 stars：

```bash
bash skills/classifying-github-stars/scripts/fetch-starred.sh zhangzqs > /tmp/zhangzqs-stars.json
```

如果省略用户名，则抓取当前登录账号：

```bash
bash skills/classifying-github-stars/scripts/fetch-starred.sh > /tmp/me-stars.json
```

### 2. 读取分类规则

先看 reference，再开始分类：

`skills/classifying-github-stars/references/github-star-classification.md`

分类时优先依据：

1. repository topics
2. language
3. repo name / description
4. 用户当前已经存在的 Lists 命名风格

### 3. 生成分类计划

把分类计划写成 JSON，格式固定如下：

```json
{
  "targetAccount": "zhangzqs",
  "listVisibility": "private",
  "repos": [
    {
      "repo": "openai/openai-python",
      "lists": ["AI", "Python"]
    },
    {
      "repo": "hashicorp/terraform",
      "lists": ["Infra", "DevOps"]
    }
  ]
}
```

要求：

- `repo` 必须是 `owner/name`
- `lists` 至少 1 个
- 优先复用现有 List 名，避免制造很多一次性分类
- 模糊项单独标注，不要硬塞进不合适的 List

### 4. 先做 dry-run

```bash
bash skills/classifying-github-stars/scripts/apply-lists.sh --plan /tmp/plan.json
```

这一步只输出将要创建哪些 Lists、哪些仓库将被追加到哪些 Lists，不真正写入。

### 5. 确认后执行

```bash
bash skills/classifying-github-stars/scripts/apply-lists.sh --plan /tmp/plan.json --execute
```

默认新建 Lists 为私有。若用户明确要求公开 Lists，再加：

```bash
--public-lists
```

## Review Rules

在执行写入前，你必须做这几件事：

1. 说明你准备创建哪些新 Lists
2. 说明每个 repo 会被追加到哪些 Lists
3. 标出模糊或高风险分类
4. 只有在用户确认后才执行 `--execute`

## Failure Modes

- `gh` 未登录：停止并要求重新认证
- stars 为空：停止并报告
- 计划文件缺字段：停止并报具体字段
- 目标 repo 无法解析：跳过该项并在总结中报告
- GraphQL 更新失败：保留失败项，继续其他 repo

## Output Expectations

- dry-run: 输出待创建 Lists 和待更新 repo 摘要
- execute: 输出实际创建结果和每个 repo 的最终 Lists
- 最后给出失败项和需要人工判断的项

