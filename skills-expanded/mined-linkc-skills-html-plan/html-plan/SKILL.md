---
name: html-plan
description: 用户显式要求 html-plan 时，为复杂任务建立本地多 Tab HTML 协作工作面。支持规划、确认表单、PRD、用户故事、用户旅程、待办、日志，以及批注/评论/答案的草稿提交和 inbox 响应。仅在明确调用 /html-plan、用 html plan、开一个 html plan、先做个 plan 文档等情况下触发，普通问答、简单编辑和 ingest 不自动触发。
allowed-tools: Bash Read Write Edit
---

# html-plan

## 使用边界

- 用户显式调用后，为需要多轮沟通的任务创建工作面；不要为普通问答、简单编辑或 ingest 自动创建。
- 保持原任务范围，不为了填满页面增加步骤、问题、Tab 或图。默认只用 `plan` 和 `log`，有待确认问题才加 `confirm`。
- 其他已有 Tab：`prd`、`user-stories`、`user-flow`、`todos`。字段见 `examples/state-sample-product.json`。不使用尚未实现的 Tab。
- 不在状态中保存密码、令牌或秘密；任务数据是本地明文。只绑定 localhost，不修改系统安全或网络设置。

## 先确定两个路径

`SKILL_DIR` 是**本次加载的这个 SKILL.md 的目录**，不要硬编码某个 Agent 的安装路径。`TASK_DIR` 是任务工作区中的 `.html-plan/YYYY-MM-DD-短描述/`。所有路径参数加引号。

```bash
SKILL_DIR="<本次 SKILL.md 所在绝对目录>"
TASK_DIR="<当前任务工作区>/.html-plan/<日期-短描述>"
```

脚本使用 Python 3.8+ 标准库，无需安装依赖。已有任务先读状态并恢复，不能覆盖重建。

## 建立首次工作面

1. 保存用户原始要求到 `raw-input.md`。按 `examples/state-minimal.json` 建立真实任务的 `state.json`；这是结构样例，不要把样例任务当成用户要求。
2. 必须含 `task`、`slug`、ISO 时间 `created_at/updated_at`、`version: 1`、`tabs`、`plan`、`history`、`annotations: []`、`inbox: []`、`draft: []`。步骤用稳定 ID，状态为 `todo/in_progress/done/blocked`。Tab ID 用唯一的字母、数字、`_` 或 `-`，首字符为字母。
3. 启动 sidecar；它选择端口、写入任务地址并生成 `plan.html`。使用当前环境实际支持的持续运行/后台工具，保留输出或日志；不要照抄其他 Agent 的 `run_in_background` 参数，也不要用固定 sleep 判断启动成功。

```bash
python3 "$SKILL_DIR/server.py" --task-dir "$TASK_DIR"
```

4. 确认输出出现 `listening on ...`，检查该 URL 的 `/healthz` 返回本任务路径。打开输出中的 `http://localhost:<port>/plan.html`，不要用 `file://` 打开。受限环境不能监听端口时报告限制，不能把生成文件等同于交互验收。
5. 告诉用户：填写/批注/评论 → **保存草稿** → 顶部 **本轮提交** → **复制提示语** → 回到 AI 助手粘贴。仅保存草稿不会通知 AI。以必要的问题开始，避免要求用户先填完整页。

## 每轮工作循环

每次恢复任务或收到新消息，先检查**已提交** inbox。一次读取当前状态即可，不重复输出整份日志，只展开待处理项及关联字段。`context` 是提交时情境，必要时按 `target` 回查当前数据，不能把快照当成最新状态。

```bash
python3 "$SKILL_DIR/state_store.py" --task-dir "$TASK_DIR"
```

- 按提交顺序理解意见；独立项可一起处理，有依赖或相互冲突的项分别判断。
- 回应每条待处理提交，再推进任务。处理成功或需要用户澄清时写明 `ai_response`，标记 `processed: true`；它表示“已回应”，不代表工作完成。待办评论响应由 inbox 自动同步。
- 撤回/覆盖的提交不重复执行。不能执行的请求说明原因，不假装完成。批注是否 `resolved` 按实际问题是否解决决定。
- 只处理正式提交，不把 `draft` 中的半成品当指令。保持用户原话、稳定 ID 和已有历史，在 `history` 追加本轮实际变化。

## 安全更新与渲染

**运行中不要用 Write/Edit 直接覆盖 `state.json`。**AI 与 sidecar 共用 `state_store.py` 的文件锁和版本检查。读取版本，准备局部更新文件，使用 JSON Pointer 路径写入改动。数组可作为一个字段整体更新，但必须基于刚读到的状态保留其他条目。

例：当前版本为 4，第一条 inbox 已回应，同时更新步骤：

```json
{
  "expected_version": 4,
  "changes": {
    "/plan/steps/0/status": "in_progress",
    "/plan/steps/0/notes": "已按用户反馈调整，正在验证。",
    "/inbox/0/processed": true,
    "/inbox/0/ai_response": "已调整这一项，验证结果会补充在步骤中。"
  }
}
```

实际补丁还需追加 history：使用 `"/history": [...保留的旧条目, 新条目]` 的真实数组，不能写入占位文本。

```bash
python3 "$SKILL_DIR/state_store.py" --task-dir "$TASK_DIR" --patch "$TASK_DIR/update.json"
python3 "$SKILL_DIR/render.py" --task-dir "$TASK_DIR"
```

版本冲突返回退出码 2，原状态不变。重新读取、核对新增用户提交、重新生成补丁；不能只改版本号盲目重试。`server`、`draft`、版本和时间由脚本管理。

更新后核对改变的字段、inbox 响应与渲染结果。页面在没有未保存输入或待提交草稿时同步更新；有输入时保留输入，必要时提示用户提交后刷新。不要以命令成功替代目标功能验收。

## 数据约定

- `plan/log` 必备；`confirm` 数据为 `open_questions`，题型为 `radio/text/multiline/checkbox/select`。选项是字符串数组，checkbox 答案是选项数组，其他答案是字符串。`required` 问题需要非空答案。
- 步骤 `s1/s2/...`，问题 `q1/q2/...`，待办 `td1/td2/...`；sidecar 分配批注、评论、草稿和 inbox ID。
- `annotations.target` 含 `scope/ref_id/field/anchor_text/start_offset/end_offset`；关键点引用为 `kp-<index>`。
- inbox 含 `id/at/type/target/body/context/processed/ai_response/ai_responded_at`。`type` 为 `annotation/todo_comment/form_answer`。
- 草稿提交可能部分成功：页面显示已生效数量与剩余错误。依据最新状态处理已提交内容，修正失败目标后再试，不重复创建成功项。
- 图示可选，`flow:/state:/sequence:` 或原生 Mermaid；语法见 `examples/dsl-samples.md`。无图任务不加载 Mermaid，有图保持自包含。图要实际验证。

## 结束与恢复

只有所有必要问题有有效答案、步骤都已完成、正式 inbox 已回应，才报告任务完成。`blocked` 表示暂停/阻塞，需要报告原因和下一步，不能当作完成。

```bash
python3 "$SKILL_DIR/server.py" --task-dir "$TASK_DIR" --stop
```

该命令只停止经 `/healthz` 确认为本目录的 sidecar，不凭旧 PID 杀进程。保留任务目录，后续可用同一启动命令恢复。

- JSON 损坏且备份有效：共享保存模块恢复备份，保留 `state.corrupt-*.json` 并输出说明。告知恢复可能丢失最后一轮，核对后继续。备份也损坏则停止，不重新生成覆盖。
- 批注无法定位：保留原话与锚点，检查“无法定位”列表，不静默丢弃。
- 启动失败：读取实际错误/日志，报告 Python、文件或端口原因。不要安装额外依赖或改变系统设置掩盖错误。

维护时运行 `python3 -m unittest discover -s tests -v` 和 `node tests/test_ui.js`；允许 localhost 监听时再运行 `python3 tests/http_integration.py`。然后用当前可用浏览器验收有图/无图、改答、草稿提交、窄屏与键盘操作；没有做的检查必须注明。
