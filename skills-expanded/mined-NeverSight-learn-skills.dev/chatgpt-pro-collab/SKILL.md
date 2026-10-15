---
name: chatgpt-pro-collab
description: 当用户明确要求通过 ChatGPT Pro Web 协作处理当前本地仓库，或需要启动、继续、等待、归档、关闭多个相互隔离的 Pro Web 协作任务时使用。宿主 Agent 明确选择 prompt 与附件；本 Skill 只维护浏览器会话、原始回复和逐 turn 审计记录，不理解仓库、不应用回复、不提交代码。
---

# ChatGPT Pro Collab

加载本 Skill 时，以 `SKILL.md` 所在绝对目录替换下列命令中的 `<skill-directory>`。保持宿主项目为当前工作目录，直接执行 `node "<skill-directory>/scripts/collab.ts" <command>`；不要切换到 Skill 目录，也不要调用宿主项目的 package script。把返回的 `taskId`、`turnId`、`responsePath` 和 `artifactPaths` 作为后续宿主流程的显式输入。

## 1. 完成一次设置

首次使用或认证失效时运行：

```sh
node "<skill-directory>/scripts/collab.ts" setup
```

等待用户在打开的浏览器中完成登录。命令成功后设置浏览器会关闭；后续任务复用本机认证源。

## 2. 启动任务

启动前由宿主预生成一个在本轮协作范围内稳定且唯一的 canonical lowercase UUID v4（例如 `uuidgen` 或 `crypto.randomUUID()` 的输出），并保存为 `taskId`：

```sh
node "<skill-directory>/scripts/collab.ts" start <taskId>
```

每个 `start` 都创建独立浏览器进程、context、session 目录和新 conversation；不要因同项目已有任务而复用或拒绝新任务。相同 `taskId` 的重复或并发 `start` 只恢复同一次启动：任务仍在启动中，或已完成启动但尚未绑定 conversation 时，返回同一个 `taskId`；已绑定 conversation、正在关闭、已关闭或失败时返回冲突。closed task 必须按第 5 节执行 `recover` 继续原 conversation，不要用 `start` 或新 task 替代。启动中断后使用同一 `taskId` 重试即可继续同一次启动。

## 3. 准备本轮输入

先把本轮文字输入写入单独的有效 UTF-8 prompt 文件，并确保全文首尾均无空白，包括终止换行，再明确列出本轮所需附件。Collab 不 trim 或改写 prompt；首尾空白会在任何状态持久化或浏览器动作前以 `PROMPT_NOT_VERBATIM_PROVABLE` 拒绝。少量文件直接上传；大量文件由宿主 Agent 先生成一个归档，Collab 不扫描或补充归档内容。

每个新 task 在尚未绑定 conversation 时，为首条 user message 发起的每次 `send` 都必须把以下固定协作合同与宿主选定的当前任务合成同一个 prompt 文件；将当前任务紧接在末尾的“当前任务：”之后，并在同一次 `send` 中携带本轮附件。首次提交前确定失败时，后续显式 `send` 仍须使用完整合同；`unknown-submission` 按第 5 节裁决，不另行发送。不要让 `start` 或额外的 `send` 单独提交启动声明；conversation 绑定后的后续 prompt 依赖已有上下文，不再重复该合同。

```md
你现在处于协作模式，正在与一个能够访问本地仓库和执行环境的宿主 Agent 共同完成任务。

- 宿主 Agent 负责提供任务与附件、执行本地操作和验证，并决定是否集成你的输出。
- 你作为独立协作者，负责完成“当前任务”声明的有界工作。对于宿主环境和仓库事实，只把本消息、附件和后续对话明确提供的内容视为已观察事实。可以使用当前 ChatGPT 会话实际提供的工具，但不要假设能够访问其他本地文件、状态、命令结果或凭证。
- 收到本消息后直接处理当前任务，不要只确认协作模式。交付可供宿主直接验证和使用的具体结果；主动指出错误前提或更简单的路径，区分事实、推断、假设与未验证项，不得声称执行或验证未实际完成的操作。
- 信息不足但仍能推进时，采用合理假设继续，并说明假设错误会改变什么。只有缺失信息会造成实质不同的结果且无法继续时，才提出一个聚焦的阻塞问题。
- 后续消息延续同一协作任务；保留已确认上下文，不重复本声明。

当前任务：
```

代码任务默认生成 `.tar.gz`。在 macOS 使用 bsdtar 时必须同时关闭 copyfile 元数据和 xattr：

```sh
COPYFILE_DISABLE=1 tar --no-xattrs -czf <archive.tar.gz> <selected-path>...
tar -tzf <archive.tar.gz>
```

跨平台交付、任务约定或接收方需要 ZIP 时生成 `.zip`：

```sh
zip -X <archive.zip> <selected-path>...
unzip -Z1 <archive.zip>
```

归档只包含明确选择的 regular file 及承载其相对路径所需的目录项。生成后必须列出成员并与本轮选择结果核对；不要添加 manifest、固定顶层目录、哈希或回复协议，除非当前协作任务本身需要。

## 4. 发送并等待一轮

把直接附件或核对后的单个归档作为普通 `attachmentPath` 传给 `send`：

```sh
node "<skill-directory>/scripts/collab.ts" send <taskId> <promptPath> [attachmentPath ...]
node "<skill-directory>/scripts/collab.ts" wait <taskId> <turnId> <observationWindowMs> <captureTimeoutMs>
```

`send` 返回 `turnId` 后即可操作其他任务；不要等待时再次发送同一任务。两个时长都必须是有限正整数毫秒值：观察窗口只约束回复生成，捕获超时约束已完成回复的文字与返回文件落盘。

每个观察窗口只调用一次 `wait`，不要在调用尚未返回时另行轮询浏览器。结果为 `pending` 时，远端生成与本地任务保持活动；需要继续观察时，再由宿主显式发起一个新窗口。结果为 `completed` 时读取原始 `response.md` 和 `artifactPaths`，由宿主决定如何解释、验证或使用；不要让 Collab 自动执行回复内容。捕获超时会返回错误，后续 `wait` 使用新的 `captureTimeoutMs` 继续同一 turn。前一轮完成后，可在同一 `taskId` 再次 send/wait 以保留 conversation 上下文。

`wait` 观察期间，同一 turn 连续 300000ms 仍未捕获时，Collab 会在该次等待内自动 reload 当前 conversation 以重新水合页面，再继续观察与捕获；触发只由时间决定，不检查页面完成信号，reload 不终止远端生成、不改变 turn 状态，观察窗口到期仍正常返回 `pending`。不要把 reload 或 repeated `pending` 当作失败依据；只有用户明确确认失败时才执行下面的裁决。

只有用户明确说明该 Pro response 已失败或终止，或永久无法完成 capturing 且决定放弃时，才裁决原 turn：

```sh
node "<skill-directory>/scripts/collab.ts" resolve-turn <taskId> <turnId> failed
```

不要从 `pending`、超时、reload 或内容稳定自行推断失败。对 `pending`，命令验证原 conversation、目标 user turn 与可继续的 composer；若目标 response 仍显示 `Stop answering`，只在该命令内结束它。对用户明确放弃的 `capturing`，裁决不读取或操作页面，只保留已经冻结的 `response.md`、artifact 记录与错误并把原 turn 标为 `failed`；裁决后只读探测 session 并返回当前安全 `nextAction`。成功后，由宿主准备针对中断点的具体 continuation prompt，再显式执行新的 `send`/`wait`；不要自动发送泛化的“继续”。

## 5. 检查与恢复中断状态

任务异常、进程中断或结果不明时，先运行只读检查：

```sh
node "<skill-directory>/scripts/collab.ts" status <taskId>
```

`status` 返回任务、未完成 turn、未完成 operation、浏览器 session 可用性和唯一安全的 `nextAction`。`nextAction` 只可能是 `setup | start | send | wait | recover | resolve-submission | close | none` 之一，按它继续：

- `wait`：对 browser 可用的 `pending` 或 `capturing` turn 使用原参数合同再次 `wait`。
- `close`：任务正在关闭，只执行 `close`，不要重建浏览器。
- `none`：没有待继续或待解除的持久工作流；它本身不禁止宿主按用户意图、在当前 task 状态允许时显式执行 `send` 或 `close`。
- `recover`：执行恢复命令，由系统按持久阶段和页面证据继续启动、发送准备、browser 缺失重建、closed task 重新激活或归档恢复。closed task 恢复后仍使用原 `taskId` 和 canonical conversation；pending/capturing turn 恢复后再按返回的 `nextAction: wait` 继续：

  ```sh
  node "<skill-directory>/scripts/collab.ts" recover <taskId>
  ```

- `resolve-submission`：消息是否提交无法自动证明时，先检查页面，再由用户提供裁决；两个裁决命令都会先在已登录页面验证，再改变本地状态：

  ```sh
  node "<skill-directory>/scripts/collab.ts" resolve-submission <taskId> <turnId> submitted <conversationUrl>
  node "<skill-directory>/scripts/collab.ts" resolve-submission <taskId> <turnId> not-submitted
  ```

  `submitted` 必须提供无 query、fragment 和凭据的 `https://chatgpt.com/c/<conversationId>` 或 `https://chatgpt.com/g/g-p-<project>/c/<conversationId>` canonical URL；Collab 验证其属于唯一 `chatgpt-pro-collab` Project、与已保存 prompt 及附件名称一致且唯一后，才把原 turn 置为 `pending`。`not-submitted` 只在页面恢复为安全 composer（已绑定 conversation 或唯一目标 Project 的空白 composer）且锚点之后没有匹配提交时，才把原 turn 置为 `failed`，之后由宿主显式重新 `send`。输出丢失后可原样重试相同裁决；不同 verdict 或 submitted URL 会返回冲突，两个分支都不会自动发送消息。

## 6. 管理生命周期

```sh
node "<skill-directory>/scripts/collab.ts" archive <taskId>
node "<skill-directory>/scripts/collab.ts" close <taskId>
```

仅在用户明确要求归档 Web conversation 时运行 `archive`；它不会关闭本地任务。任务暂时不需要浏览器时运行 `close`；它把 task 置为可恢复暂停态，不归档 Web conversation，也不删除 transcript、conversation binding 或共享认证源。用户后续提供 feedback 时，先执行 `status`，按 `nextAction: recover` 恢复同一 conversation，再继续 `send/wait`；不要创建新 task 重建上下文。

## 7. 遵守输入与失败边界

- 只传入宿主明确指定且当前可读的路径；只有宿主 Agent 可以按第 3 节打包已选输入，Collab 运行时不得扫描、打包或自动补充仓库文件。
- 把附件视为不透明文件；不要因 dirty worktree、symlink、仓库外路径或旧任务增加 Collab 安全门。
- 不要求归档使用 manifest、固定目录结构或固定协作协议；Pro 在沙盒中自行解压，Collab 不发送额外解压消息。
- `unknown-submission` 表示无法证明消息是否已提交；不要自动重发，先执行 `status`，按 `resolve-submission` 分支向用户报告并请求裁决。
- `pending` 或 `capturing` 不因超时或页面异常自动变为 `failed`；只有用户明确提供 response 已失败、终止或永久无法完成捕获的事实时，才执行第 4 节的 `resolve-turn`。
- 浏览器、页面 selector、写入或状态不一致时，报告真实错误；不要重启、迁移 conversation、删除 transcript 或伪造成功。

## 8. 结束前检查

- [ ] 本轮 prompt 和每个附件是否都由宿主明确选择？
- [ ] 新 task 的首轮 prompt 是否在同一条消息中包含固定协作合同与当前任务，且后续轮次未重复合同？
- [ ] 使用归档时，是否只包含已选输入，并已核对实际成员？
- [ ] 是否保存了每次成功返回的 `taskId`、`turnId`、`responsePath` 和 `artifactPaths`？
- [ ] 是否在读取原始回复后由宿主独立验证，而未让 Collab 自动执行？
- [ ] 中断或结果不明时，是否先执行 `status` 并按 `nextAction` 继续，而不是盲目重发或重启？
- [ ] 裁决失败 response 时，是否已有用户明确事实，并在成功后另行显式发送具体 continuation？
- [ ] 是否只在用户明确要求时归档 conversation？
- [ ] 暂时不需要浏览器的活动任务是否已显式关闭，并保留 `taskId` 供后续 feedback 恢复？

完成条件：目标协作轮次有独立、可审计的 prompt 与 response；浏览器和 Web conversation 生命周期分别按用户意图处理；中断状态可检查、可恢复、可裁决。
