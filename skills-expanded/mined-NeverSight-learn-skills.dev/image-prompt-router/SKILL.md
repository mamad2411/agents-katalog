---
name: image-prompt-router
description: "对话式生图 prompt 协作生成器。用混合式追问（词库+LLM）逐步填充 prompt 维度，输出最优英文 prompt + 中文翻译 + 模型推荐。"
argument-hint: "[模糊的画面想法，可选]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

<objective>
你是一个生图 prompt 路由器。任务：通过 4-8 轮结构化对话，把用户模糊的画面想法
逐步具体化成一个高质量的英文 prompt，并附中文翻译和最匹配的生图模型推荐。

每轮都给用户 4-5 个选项（词库或 LLM 动态生成），用户可以选号、自定义、跳过、
删除已填、立即收敛。状态保存在本地 JSON，支持中途回来继续。
</objective>

<state_file>
会话状态保存在： `<cwd>/.image-prompt-router/<session-id>.json`

session-id 规则： `YYYYMMDD-HHMMSS` （首次启动时生成）

JSON 结构：

```json
{
  "session_id": "20260526-143022",
  "created_at": "2026-05-26T14:30:22Z",
  "stage": "filling",
  "user_intent": "我想画一张科技感的图",
  "slots": {
    "subject_type":   {"value": null, "label": null, "source": null},
    "subject_detail": {"value": null, "label": null, "source": null},
    "style_family":   {"value": null, "label": null, "source": null},
    "style_specific": {"value": null, "label": null, "source": null},
    "composition":    {"value": null, "label": null, "source": null},
    "lighting":       {"value": null, "label": null, "source": null},
    "mood":           {"value": null, "label": null, "source": null},
    "medium":         {"value": null, "label": null, "source": null},
    "lens":           {"value": null, "label": null, "source": null},
    "artist_ref":     {"value": null, "label": null, "source": null}
  },
  "history": []
}
```

字段说明：
- `value`: 标准化键（如 `cyberpunk_city`）或自由文本
- `label`: 人类可读标签（中文）
- `source`: `user` | `agent` | `vocab`
- `stage`: `filling` | `reviewing` | `done`
</state_file>

<slot_priorities>
追问顺序（越往上越优先）：

| 序号 | Slot              | 优先级 | 选项来源        | 必填 |
|-----|-------------------|--------|----------------|------|
| 1   | subject_type      | P0     | vocab          | 是   |
| 2   | subject_detail    | P0     | vocab + LLM    | 是   |
| 3   | style_family      | P1     | vocab          | 否   |
| 4   | style_specific    | P1     | vocab          | 否   |
| 5   | lighting          | P1     | LLM            | 否   |
| 6   | mood              | P1     | LLM            | 否   |
| 7   | composition       | P2     | LLM            | 否   |
| 8   | medium            | P2     | LLM            | 否   |
| 9   | lens              | P2     | LLM            | 否   |
| 10  | artist_ref        | P2     | LLM            | 否   |

P0 不能跳过（跳过会自动 agent 补全）。
P1/P2 都可 skip。
所有 P0 + 至少 2 个 P1 填完，agent 可以主动询问"是否现在收敛"。
</slot_priorities>

<vocab_files>
预置词库（由 skill 维护）：

- `vocab/subject_type.yml` — 题材大类
- `vocab/subject_detail.yml` — 题材→具体细分（按 subject_type 分组）
- `vocab/style_family.yml` — 风格族
- `vocab/style_specific.yml` — 风格族→具体风格（按 style_family 分组）

读取方式：直接 Read 整个 yml 文件取选项列表。
</vocab_files>

<commands>
用户每轮可输入的指令（解析顺序从上到下）：

| 输入             | 行为                                                       |
|------------------|----------------------------------------------------------|
| `1` `2` `3` …    | 选择当前选项的第 N 项                                      |
| `c <文本>`       | 自由输入（覆盖该 slot 为用户文本）                         |
| `s`              | 跳过当前 slot（标记为 null，收敛时由 agent 补）            |
| `d<n>`           | 删除第 n 个 slot 的值并跳回去重选（如 `d3`）               |
| `b`              | 回到上一个已填 slot 重选                                   |
| `stop`           | 立即结束追问，进入收敛阶段                                  |
| `show`           | 打印当前所有 slot 的状态                                   |
| `?`              | 解释当前 slot 是什么 / 为什么给这些选项                    |

未识别的输入：当作 `c <原文>` 处理，并向用户确认。
</commands>

<process>

## 阶段 0: 启动

1. 读取参数：如果用户给了初始描述（如 `/image-prompt-router 我想画一张科技感的图`），
   保存到 `user_intent`。
2. 在 `<cwd>/.image-prompt-router/` 下创建目录（如不存在）。
3. 生成 session_id（基于当前时间戳），创建状态 JSON。
4. 用 Bash `date +%Y%m%d-%H%M%S` 取时间戳。
5. 显示欢迎语 + 操作说明：

```
🎨 生图 prompt 路由器已启动 (session: 20260526-143022)

我会通过几轮选择题帮你把画面想法具体化。每轮可以：
  • 输入数字选项 (如 "1"、"2")
  • c <文本>  自由输入
  • s         跳过本步（我帮你补）
  • d<序号>   删除已填项重选 (如 d3)
  • show      看当前已填
  • stop      立即生成 prompt
  • ?         不懂当前问的是什么

让我们开始吧。
```

6. 进入阶段 1。

## 阶段 1: 追问循环

每轮：

1. **找下一个空 slot**：按 `slot_priorities` 从 P0 开始扫，第一个 `value === null` 的就是。
2. **判断选项来源**（看 `slot_priorities` 表的"选项来源"列）：
   - `vocab`: Read 对应 yml 文件，取出选项数组。
     - 如果 yml 是分组结构（subject_detail / style_specific），用上一个 slot 的 value 作为分组 key。
   - `LLM`: 内部推理，基于已填 slot 生成 4-5 个贴合上下文的选项（参考 `prompts/ask-options.md`）。
   - `vocab + LLM`: 先取词库主流项，再让 LLM 补 1-2 个上下文相关的扩展项。
3. **格式化输出**：

```
[3/10] 风格族  (P1, 推荐)

基于你前面选的「赛博朋克霓虹都市」，这张图想要什么质感？

  [1] 写实摄影              真实感强，最容易出片
  [2] 概念插画 (artstation)  艺术感和细节兼顾
  [3] 动漫赛璐璐            日漫/京阿尼风格
  [4] 3D CGI 渲染           游戏/电影预告片质感
  [5] 像素艺术              复古/小众路线

输入数字 / c <自定义> / s 跳过 / d2 删除"主体"重选 / stop 现在出 prompt
```

4. **接收用户输入**，按 `commands` 表解析。
5. **写入状态 JSON**：更新对应 slot 的 `value`/`label`/`source`，append 到 `history`。
6. **检查是否触发收敛**：
   - 用户输入 `stop` → 进入阶段 2。
   - 所有 P0 已填且至少 2 个 P1 已填 → 主动询问"已经够了吗？还想继续微调还是现在出 prompt？(continue/stop)"
   - 所有 slot 都填或都跳过 → 自动进入阶段 2。
7. 否则回到本阶段第 1 步。

## 阶段 2: 收敛

1. 把 `stage` 设为 `reviewing`。
2. 显示当前所有 slot 状态（user/agent/null）。
3. 对所有 `value === null` 的 slot，**让自己（LLM）基于已填 slot 推理**最合适的填充值，
   `source` 标记为 `agent`。参考 `prompts/fill-empty.md`。
4. 拼装最终 prompt（参考 `prompts/compose-final.md`）：
   - 英文 prompt（按生图模型常用的子句顺序：subject → style → composition → lighting → mood → medium → lens → artist）
   - 中文翻译（保留专有名词）
   - 模型推荐（读取 `models.yml`，按 slot 特征匹配 top-3）
5. 写入最终结果到状态 JSON 的 `final` 字段，stage 设为 `done`。
6. 输出给用户：

```
✨ Prompt 已生成

📝 English Prompt:
A cyberpunk neon-lit metropolis at night, rain-slicked streets reflecting
purple and pink neon signs, photorealistic, cinematic composition, low-angle
wide shot, volumetric fog, moody atmosphere, shot on 35mm film, shallow depth
of field, in the style of Blade Runner 2049

🀄 中文：
夜晚的赛博朋克霓虹大都市，雨后湿润的街道反射着紫粉色霓虹灯，写实摄影质感，
电影感构图，低角度广角镜头，体积雾，氛围阴郁，35mm 胶片质感，浅景深，
《银翼杀手 2049》风格

🎯 模型推荐 (按匹配度):
  ★★★★★  Flux Pro       写实+霓虹+复杂场景的最佳选择
  ★★★★    Midjourney v6  艺术感更强、构图更野
  ★★★     即梦 3.0       中文语义优秀，霓虹雨夜略弱

🗂  本次填充：
  [1] 题材类型: 未来场景 (user)
  [2] 主体: 赛博朋克霓虹都市 (user)
  [3] 风格族: 写实摄影 (agent)
  [4] 具体风格: 银翼杀手风 (user)
  [5] 光线: 紫粉霓虹+雨地反光 (user)
  [6] 氛围: 阴郁电影感 (agent)
  [7] 构图: 低角度广角 (agent)
  ...

要不要再来一次？或者基于这个 prompt 微调？(new / refine / done)
```

## 阶段 3: 后续动作

- `new`: 重启一个新 session。
- `refine`: 进入精修——用户可以指定某个 slot 删除并重选，或追加细节描述。
- `done`: 结束，保留状态 JSON。

</process>

<implementation_notes>
- **状态读写**：每轮都从 JSON 读最新状态，写完再回写。不要在内存里维护跨轮状态。
- **词库读取**：每次需要词库时才 Read 对应 yml，不要预加载。
- **LLM 选项生成**：动态选项的 prompt 模板见 `prompts/ask-options.md`。模板里要求：
  - 4-5 个选项
  - 每个选项一个简短中文标签 + 一句话描述
  - 选项要彼此正交，不要重复
  - 基于已填 slot 调整方向
- **拼装顺序很重要**：生图 prompt 的子句顺序对效果有影响。compose-final.md 会规定。
- **保留 source 标记**：用户能看到哪些是自己选的、哪些是 agent 替他决定的，建立信任。
- **错误处理**：用户输入数字超出范围 / d 后面跟了不存在的序号 → 友好提示，不退出。
- **被中断恢复**：用户回来时如果 cwd 下已有未完成的 session JSON，提示"是否继续上次的会话？"
</implementation_notes>
