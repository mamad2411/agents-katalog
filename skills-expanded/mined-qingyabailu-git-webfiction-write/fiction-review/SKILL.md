---
name: fiction-review
description: |
  质量审查。使用审查模型评估章节质量，生成审查报告并写回审查指标。
  支持单章、批量（1-5）、整卷（--volume N）审查。
  触发方式：/fiction-review {章号或范围}、「审查」「审一下」「检查质量」「review」「帮我看下写得怎么样」。
---
# fiction-review：质量审查

使用审查模型评估章节质量，生成结构化报告和审查指标。

## 执行流程

### Step 1：解析项目根

```bash
# SCRIPTS_DIR 由安装宿主指向本仓库或已安装的 scripts/ 目录。
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${CODEX_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}}" where)"
```

### Step 2：加载审查参考

本 skill 已随仓库提供可读取的参考文件，按需加载：
- 总是加载：`skills/fiction-review/references/review-schema.md`、`quality-rubric.md`
- 涉及爽点/钩子：`cool-points-guide.md`
- 涉及多线交织：`strand-weave-pattern.md`
- 需要处理阻断覆盖时：`blocking-override-guidelines.md`

如果宿主把 skill 安装到全局目录，按当前 skill 目录解析上述相对路径；参考文件不可读时使用
`quality-rubric.md` 中的规则摘要，不得把“参考文件缺失”当成停止审查的理由。

### Step 3：调用 reviewer agent

如果当前宿主提供独立 reviewer agent，优先通过 Agent 工具调用；如果没有可用的 Agent 工具、
部署缺失或调用失败，降级为当前会话的 solo 审查，并在报告中写明具体 fallback。主线不得伪造
“独立 reviewer” JSON。

reviewer 只返回严格结构化 JSON，不评分，不口头总结。主线负责把返回的 JSON 写入 `.novel/tmp/review_results.json`，然后由 review-pipeline 覆盖为标准 review_result artifact。

reviewer 跳过、失败、输出不完整、正文为空 → 记录问题，不等同于已审查。

在调用 reviewer 前先运行确定性完整性检查；它只能发现编码、占位符、控制字符和部分工程词泄漏，不能替代文学审查：

```bash
python -X utf8 "${SCRIPTS_DIR}/check_prose.py" \
  --check "${PROJECT_ROOT}/正文/第{章节号}章-{标题}.md"
```

### Step 4：生成报告并落库

```bash
python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${PROJECT_ROOT}" review-pipeline \
  --chapter {章节号} \
  --review-results "${PROJECT_ROOT}/.novel/tmp/review_results.json" \
  --metrics-out "${PROJECT_ROOT}/.novel/reviews/chapter_{章节号}.metrics.json" \
  --report-file "${PROJECT_ROOT}/审查报告/第{章节号}章审查报告.md" \
  --save-metrics
```

`--review-results` 可以接收内联 JSON，也可以接收已经存在的 JSON 文件路径。文件不存在、损坏、
为空或结构不完整时，报告会保留错误信息，metrics 状态为 `unverified`，不会把路径字符串当成审查结果。

### Step 5：处理阻断

存在 blocking issue 时，用有限选项让用户裁决：
- 立即修复（输出返工清单，最小修改）
- 仅保存报告，稍后处理（保留报告和指标，结束流程）

## 批量审查

```bash
fiction-review 1-5       # 批量审查 1-5 章
fiction-review --volume 1  # 整卷审查
```

批量审查逐章执行 reviewer → 逐章生成报告 → 汇总显示。

## 写回

- 审查报告写入 `审查报告/第{章号}章审查报告.md`
- review metrics 写入 `.novel/reviews/chapter_{N}.metrics.json`（JSON，不是数据库）
- review_results JSON 存入 `.novel/tmp/review_results.json`
- Deep 模式下如项目已有约定，再额外更新 `.story-system/reviews/chapter_{N}.review.json`
- reviewer 缺失/失败/结果不完整时保留报告，但指标状态必须是 `unverified`

## 成功标准

1. 解析真实项目根
2. 通过独立 reviewer 输出结构化 JSON 并落盘；若降级 solo，报告必须标记实际模式
3. 审查报告已生成，metrics 已写入 JSON 文件
4. 存在阻断问题时用户已明确选择处理策略

## 参考

本 skill 已提供：
- `references/review-schema.md`：reviewer 输出结构和未验证规则
- `references/quality-rubric.md`：通用网文审查基准
- `references/cool-points-guide.md`：爽点与钩子检查
- `references/strand-weave-pattern.md`：多线交织检查
- `references/blocking-override-guidelines.md`：阻断项覆盖规则

平台专属 rubric 可以由宿主追加；没有时使用通用基准，不得虚构平台实时数据。
批量审查逐章独立执行，不互相影响结果。
审查报告格式由 review-pipeline 决定，本 skill 不定义。
---

## 致谢

本 skill 的开发参考了以下开源项目的思路与实现：

- [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer)
- [worldwonderer/oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode)

感谢原作者的开源贡献。
