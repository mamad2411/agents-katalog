---
name: kanban-worker
description: Pitfalls, examples, and edge cases for Hermes Kanban workers. The lifecycle itself is auto-injected into every worker's system prompt as KANBAN_GUIDANCE (from agent/prompt_builder.py); this skill is what you load when you want deeper detail on specific scenarios.
version: 2.0.0
platforms: [linux, macos, windows]
environments: [kanban]
metadata:
  hermes:
    tags: [kanban, multi-agent, collaboration, workflow, pitfalls]
    related_skills: [kanban-orchestrator]
---

# Kanban Worker — 常见问题与示例

> 您之所以能看到此技能，是因为 Hermes 的 Kanban 调度器通过 `--skills kanban-worker` 参数将您派定为 Worker——该技能会自动加载到每一个被调度的 Worker 中。其**生命周期**（共 6 个阶段：准备 → 执行 → 心跳检测 → 阻塞/完成）也包含在会自动注入系统提示语的 `KANBAN_GUIDANCE` 块中。此技能则提供了更深入的细节：理想的任务交接方式、重试诊断策略以及边缘情况处理方法。

## 工作空间管理

您的工作空间类型决定了您在 `$HERMES_KANBAN_WORKSPACE` 环境下的操作方式：

| 类型 | 含义 | 操作方式 |
|---|---|---|
| `scratch` | 新建的临时目录，仅属于您个人 | 可自由读写；任务归档后该目录会被清理。 |
| `dir:<路径>` | 共享的持久化目录 | 其他运行实例会读取您写入的内容。应将其视为长期存在的状态。路径一定是绝对路径（内核不支持相对路径）。 |
| `worktree` | 位于指定路径下的 Git worktree | 如果该路径下不存在 `.git` 目录，请先在主仓库中执行 `git worktree add <路径> ${HERMES_KANBAN_BRANCH:-wt/$HERMES_KANBAN_TASK}`，之后再切换到该目录并正常工作。请在此处提交代码更改。 |

## 租户隔离

如果设置了 `$HERMES_TENANT`，则任务属于某个租户命名空间。在读写持久化内存时，应在内存条目的前缀加上租户标识，以避免不同租户之间的上下文泄露：

- 正确示例：`business-a: Acme 是我们最大的客户`
- 错误示例（会导致上下文泄露）：`Acme 是我们最大的客户`

## 合理的摘要与元数据格式

下游 Worker 通过 `kanban_complete(summary=..., metadata=...)` 的方式来了解您所完成的工作。以下是有效的格式示例：

**编码任务：**
```python
kanban_complete(
    summary="shipped rate limiter — token bucket, keys on user_id with IP fallback, 14 tests pass",
    metadata={
        "changed_files": ["rate_limiter.py", "tests/test_rate_limiter.py"],
        "tests_run": 14,
        "tests_passed": 14,
        "decisions": ["user_id primary, IP fallback for unauthenticated requests"],
    },
)
```

**需要人工审核的编码任务（需审核）：**

对于大多数涉及代码修改的任务，只有在经过人工审核者检查之后，工作才算真正完成。此时应使用“阻塞”状态而非“完成”状态，并在原因前加上 `review-required: `，这样仪表板就会将该任务标记为需要审核。建议先将结构化元数据（如已修改的文件、测试用例数量、差异对比或 PR 链接等）放入评论中，因为 `kanban_block` 只能存储便于人工阅读的原因说明——而评论才是用于长期记录注释的合适渠道。审核者要么批准任务并执行 `hermes kanban unblock <id>` 命令（这样系统会重新显示该任务及对应的评论线程，以便后续沟通），要么通过另一条评论要求对代码进行修改。

```python
import json

kanban_comment(
    body="review-required handoff:\n" + json.dumps({
        "changed_files": ["rate_limiter.py", "tests/test_rate_limiter.py"],
        "tests_run": 14,
        "tests_passed": 14,
        "diff_path": "/path/to/worktree",  # or PR url if pushed
        "decisions": ["user_id primary, IP fallback for unauthenticated requests"],
    }, indent=2),
)
kanban_block(
    reason="review-required: rate limiter shipped, 14/14 tests pass — needs eyes on the user_id/IP fallback choice before merging",
)
```

仅当任务确实属于最终性工作时，才应使用 `kanban_complete` —— 例如只需修正一行文字的错误、对文档进行不会影响功能的修改，或是研究类任务且其成果本身就是相关报告时。 

**研究类任务：**
```python
kanban_complete(
    summary="3 competing libraries reviewed; vLLM wins on throughput, SGLang on latency, Tensorrt-LLM on memory efficiency",
    metadata={
        "sources_read": 12,
        "recommendation": "vLLM",
        "benchmarks": {"vllm": 1.0, "sglang": 0.87, "trtllm": 0.72},
    },
)
```

**任务审核：**
```python
kanban_complete(
    summary="reviewed PR #123; 2 blocking issues found (SQL injection in /search, missing CSRF on /settings)",
    metadata={
        "pr_number": 123,
        "findings": [
            {"severity": "critical", "file": "api/search.py", "line": 42, "issue": "raw SQL concat"},
            {"severity": "high", "file": "api/settings.py", "issue": "missing CSRF middleware"},
        ],
        "approved": False,
    },
)
```

请合理设计`metadata`的结构，以便后续的解析工具（如审核者、数据聚合器、调度程序）无需重新读取您的文本内容即可直接使用这些信息。

## 交付成果（`artifacts=[...]`）

如果您的任务生成了人类实际需要的文件——比如图表、PDF文档、电子表格、生成的图片或压缩包——请将它们的**绝对路径**传递给`kanban_complete(artifacts=[...])`函数。网关通知系统会将这些文件作为原生附件发送给所有关注该任务的用户，这样交付成果就会直接出现在他们的聊天窗口中，与完成消息一同呈现，而无需用户自行去查找路径。

```python
kanban_complete(
    summary="Q3 revenue analysis: 14% QoQ growth, EMEA the laggard. Chart + full PDF attached.",
    artifacts=["/tmp/q3-revenue.png", "/tmp/q3-report.pdf"],
    metadata={"rows_analyzed": 48000, "growth_qoq": 0.14},
)
```

图片和视频可直接内嵌；PDF、docx、csv/xlsx/json/yaml、pptx、zip/tar/gz、音频以及html文件则需以独立文件的形式上传。相关规则如下：

- **仅允许使用绝对路径**，且在你完成操作时该文件必须仍然存在——切勿指向已被删除的临时文件。
- **仅上传真正的交付成果**。请忽略中间日志、临时文件以及用户已拥有的输入内容。
- `artifacts`是通知器读取的**顶层参数**。切勿将交付文件的路径藏在`metadata`中（例如`metadata.codex_lane.artifacts`），并期望它们能被上传——通知器仅会扫描顶层的`artifacts`列表，必要时才会参考你的`summary`/`result`文本作为补充。元数据路径仅用于下游处理程序的记录，而非实际文件传输。
- 空字符串会自动转换为包含一个元素的列表，且会与现有的`metadata.artifacts`合并，同时避免重复项。

即使在非看板环境中，这一机制同样适用：任何智能体只需在响应中写入文件的绝对路径，即可让目标平台直接上传该文件；而Slack、Discord、Telegram等平台则可直接处理这些文件——`artifacts`参数则是结构化看板任务的处理入口。

## 声明由你创建的卡片

如果你的任务执行产生了新的看板任务（通过`kanban_create`功能），请在`kanban_complete`请求中通过`created_cards`参数传递这些任务的ID。系统会验证每个ID确实存在且是由你的账户创建的；任何无效的ID都会导致任务无法完成，并返回错误信息说明问题所在，同时该失败尝试会被永久记录在任务的事件日志中。**请仅列出从成功的`kanban_create`返回值中获取的ID——切勿凭文字描述编造ID，切勿复制之前任务中的ID，也切勿声称是其他用户创建的卡片。**

```python
# GOOD — capture return values, then claim them.
c1 = kanban_create(title="remediate SQL injection", assignee="security-worker")
c2 = kanban_create(title="fix CSRF middleware", assignee="web-worker")

kanban_complete(
    summary="Review done; spawned remediations for both findings.",
    metadata={"pr_number": 123, "approved": False},
    created_cards=[c1["task_id"], c2["task_id"]],
)
```

```python
# BAD — claiming ids you don't have captured return values for.
kanban_complete(
    summary="Created remediation cards t_a1b2c3d4, t_deadbeef",  # hallucinated
    created_cards=["t_a1b2c3d4", "t_deadbeef"],                   # → gate rejects
)
```

如果 `kanban_create` 调用失败（出现异常或工具错误），则表示该卡片并未创建——此时不应为其设置虚拟 ID。可以重新尝试创建，或者直接省略 ID，并在总结中说明此次失败情况。Prose-scan 功能还能检测到自由文本总结中那些无法解析的 `t_<hex>` 引用；这类问题虽不会阻碍任务完成，但会在控制面板的任务项中显示为建议性警告。 

## 能快速得到回复的阻塞原因

错误示例：`"stuck"`——因为相关人员缺乏足够背景信息。 
正确做法：用一句话明确说明所需的具体决策内容，而将更详细的背景信息以注释形式附上。

```python
kanban_comment(
    task_id=os.environ["HERMES_KANBAN_TASK"],
    body="Full context: I have user IPs from Cloudflare headers but some users are behind NATs with thousands of peers. Keying on IP alone causes false positives.",
)
kanban_block(reason="Rate limit key choice: IP (simple, NAT-unsafe) or user_id (requires auth, skips anonymous endpoints)?")
```

块级消息会显示在控制面板/网关通知中，而注释则是人类在查看任务时所能看到的更详细的背景信息。

## 应该发送的心跳信息

优质的心跳信息应能清晰体现进度，例如：“当前处于第12/50轮训练，损失值为0.31”、“已扫描240万行数据中的120万行”、“已上传120个视频中的47个”。

劣质的心跳信息则包括：“仍在处理中”、空注释，或是间隔时间短于几秒的情况。心跳发送频率最多每隔几分钟一次；对于时长不足2分钟的任务，则无需发送心跳信息。

## 重试场景

如果你打开某个任务后，`kanban_show`返回的`runs: [...]`中包含一个或多个已结束的运行记录，那就意味着需要对该任务进行重试。之前各次运行的`outcome`/`summary`/`error`字段会说明哪些环节出现了问题，应避免再次走同样的错误路径。常见的重试原因及诊断方法如下：

- `outcome: "timed_out"` —— 之前的尝试已达到`max_runtime_seconds`设定的时间上限。此时可能需要将任务拆分处理或缩短单次处理时间。
- `outcome: "crashed"` —— 出现内存不足或程序崩溃的情况。应设法减少程序的内存占用。
- `outcome: "spawn_failed"` + `error: "..."` —— 通常是由于配置文件问题导致的（如缺少认证信息、路径设置错误）。此时不应盲目重试，而应通过`kanban_block`向负责人询问问题。
- `outcome: "reclaimed"` + `summary: "task archived..."` —— 是操作员将任务从之前的运行记录中归档了；这种情况下你本就不应该继续执行该任务，需仔细检查任务状态。
- `outcome: "blocked"` —— 之前的尝试已被阻止；此时相关说明评论应该已经出现在讨论线程中了。

## 通知路由配置

你可以通过在`~/.hermes/config.yaml`文件中添加`notification_sources`参数，来配置网关接收跨配置文件的看板任务通知。
- `notification_sources: ['*']`：允许接收所有配置文件发送的通知。
- `notification_sources: ['default', 'zilor-ppt']` 或 `"default,zilor-ppt"`：仅允许接收指定配置文件发送的通知。
- 若不设置该参数，则保持默认的配置文件隔离机制。

## 绝对不要做的事

- 不要使用`delegate_task`来替代`kanban_create`。`delegate_task`适用于在当前运行任务内部处理简单的推理子任务，而`kanban_create`则是用于跨智能体传递任务，这类任务的处理会持续多个API调用周期。
- 不要使用`clarify`来向人类提问。当前系统是以无界面模式运行的，没有实时用户可以回应。此类请求将会超时（默认约120秒），任务会一直处于“运行中”状态，且不会发出需要输入的提示。应改用`kanban_comment`（用于提供背景信息）加上`kanban_block(reason=...)`（表示需要做出决策）的方式——这样任务会在看板上显示为被阻塞状态，操作员能看到后会在评论中给出解答并解除阻塞，随后你便可带着相关讨论线程重新启动任务。
- 除非任务说明中另有要求，否则不要修改 `$HERMES_KANBAN_WORKSPACE` 目录以外的文件。
- 不要为自己创建后续任务，应将其分配给合适的专家处理。
- 不要假装已完成实际上并未完成的任务，应直接将该任务标记为阻塞状态。

## 常见隐患

**任务状态可能在调度与你的程序启动之间发生变化。**从调度器获取任务到你的程序真正启动的这段时间内，任务可能已被阻塞、重新分配或归档。因此务必先调用`kanban_show`查看任务状态。如果显示为“阻塞”或“已归档”，则应立即停止执行，因为你本就不应该继续处理该任务。

**工作空间中可能存在过时的文件。**尤其是`dir:`和`worktree`类型的工作空间，可能会残留之前运行任务产生的文件。请仔细阅读相关评论线程，其中通常会说明为何需要再次运行任务以及当前工作空间的状态。

**当已有相应操作指引时，不要依赖命令行工具。**`kanban_*`系列工具可在所有终端环境中正常使用（包括Docker、Modal、SSH环境）。但从终端工具发出的`hermes kanban <verb>`命令在容器化环境中会失败，因为这些环境中并未安装命令行工具。遇到不确定的情况时，直接使用专用工具更为稳妥。

## 用于脚本编写的命令行替代方案

每款工具都对应有适用于人工操作员和脚本的命令行版本：
- `kanban_show` ↔ `hermes kanban show <id> --json`
- `kanban_complete` ↔ `hermes kanban complete <id> --summary "..." --metadata '{...}'`
- `kanban_block` ↔ `hermes kanban block <id> "reason"`
- `kanban_create` ↔ `hermes kanban create "title" --assignee <profile> [--parent <id>]`
- 以此类推。

这些工具应在智能体内部使用，而命令行工具则是为终端上操作的人工用户设计的。
