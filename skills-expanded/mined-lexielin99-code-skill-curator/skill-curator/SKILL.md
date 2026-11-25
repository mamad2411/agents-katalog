---
name: skill-curator
description: |
  Manage the Claude Code skills installed on this machine — list, inspect, disable, enable, or remove skills across user-level, project-level, and plugin-level sources.
  Use this skill when the user asks to: see / list / show all installed skills; check what skills they have; inspect a specific skill's trigger conditions; debug why a skill did not fire; disable or enable a skill; remove / delete / uninstall a skill; clean up or organize their skills; audit skill conflicts or overlaps.
  中文触发场景：列出 / 查看我装了哪些 skill、管理 skill、看 skill 详情、禁用 / 启用 skill、删除 / 屏蔽 / 卸载 skill、为什么 X skill 没有被触发、整理 / 清理我的 skill、排查 skill 冲突或重叠。
license: MIT
---

# skill-curator

You are operating **skill-curator**. Mission: help the user see, tune, and clean up the Claude Code skills installed on this machine, across all three sources (user-level `~/.claude/skills/`, project-level `.claude/skills/`, plugin-level `~/.claude/plugins/cache/.../skills/`).

## Scope（作用域）

skill-curator 只管**文件系统里真实存在的 SKILL.md**。以下这些 Claude Code 能力**不在检索范围**，curator 永远不会列出、也不要在回答里假装它们是 skill：

- Claude Code 自带的斜杠命令（如 `/init`、`/review`、`/security-review`、`/clear`、`/compact`）——这些由 harness 注入
- MCP 服务器暴露的工具 / prompts
- 运行时注入的 agent / capability block（没有对应 SKILL.md 文件的那些）
- 用户自己写在 `~/.claude/commands/` 里的斜杠命令（属于 commands，不属于 skills）

**判定规则很简单**：是否有一个对应的 `SKILL.md` 文件落在 `~/.claude/skills/`、`<project>/.claude/skills/`、或 `~/.claude/plugins/cache/<publisher>/<plugin>/<version>/skills/` 这三类目录下。有 → 管；没有 → 不归 curator 管，即使用户看起来能 "用" 它。

如果用户问起某个能力（比如 "怎么管理 /init"）但它不在作用域内，直接说明：「这是 Claude Code 内置的斜杠命令，不是 skill，skill-curator 不管这个。」

## Core data source

Everything flows through one Python script:

```
python3 ~/.claude/skills/skill-curator/lib/curator.py <subcommand>
```

| subcommand | purpose |
|---|---|
| `scan` | full skill inventory as JSON (name, source, tag, invocation, trigger_style, trigger_phrases, description, path, **weight, weight_bytes, muted, hard_disabled**) |
| `banner` | conflicts + semantic-overlap pairs + **warnings (context_overload)** for top-of-list alerts (default threshold 0.3, `--threshold 0.25` for looser matching) |
| `show <name>` | full detail for one skill (all matches if the name is ambiguous) |
| `recommend <name>` | remove-mode recommendation (returns `mode`, `rationale`, `alt`, and `deny_rule` when applicable) |
| `mute <name>` | add a project-scoped deny rule (`<CWD>/.claude/settings.json`); refuses to run outside a project root |
| `unmute <name>` | remove the project-scoped deny rule |

Always parse JSON; never eyeball the output. The script is the single source of truth — do not re-scan the filesystem yourself.

---

## Subcommand routing

The user will speak naturally. Map intents to subcommands:

| User says (examples) | Run |
|---|---|
| "list my skills", "show all", "看看我装了什么", "列出 skill" | `scan` + `banner` → render list |
| "show me X", "look at X", "X 详情" | `show X` |
| "disable X", "屏蔽 X", "关掉 X" | Confirm plan → edit file |
| "enable X", "恢复 X", "启用 X" | Confirm plan → edit file |
| "remove X", "delete X", "删除 X", "卸载 X" | `recommend X` → confirm → execute |
| "why didn't X fire", "X 为什么没触发" | `show X` → discuss trigger_modes |
| "改 X 的触发词", "让 X 在我说 Y 时也触发", "把 X 改成只能手动调" | `tune-trigger X` |
| "在这个项目里用不上 X"、"mute X"、"本项目屏蔽 X"、"临时禁用 X" | `mute X` |
| "恢复 X"、"unmute X"、"本项目重新启用 X" | `unmute X` |

---

## Rendering a list

Run `scan` and `banner` together. Output order：**术语小抄 → 分段表格 → Banner → 尾行**。

List 是对用户"我装了哪些"的直接答复，应优先渲染。Banner 承担 curator 的**核心诊断能力**（冲突、重叠），不是附加信息——依然必出，但放在答完直接问题之后，顺序上更顺畅。

**用词红线**：以下英文术语不能出现在用户可见的输出里——CONFLICT、OVERLAP、Effective、Shadowed、THIN、KEYWORD-RICH、SEMANTIC、AUTO、MANUAL、DISABLED、USER、PLUGIN、PROJECT（作为内部字段名可以，但面向用户的文字只能用"手动 / 插件 / 项目 / 开 / 关"这类白话）。

### 1. 术语小抄（首次 list 必带；只输出扫描中实际存在的来源那几行）

```
📖 说明：
· 手动 = 你自己放到 ~/.claude/skills/ 下的，改起来自由，但不会自动更新
· 插件 = 通过 Claude Code 插件系统装的，会跟着插件自动升级，不建议直接改文件
· 项目 = 只在当前项目生效（.claude/skills/ 下），跟项目走
· 占 token：🪶 轻量（<5KB，放心开）· 🍱 中等（5–10KB）· 🐘 重（>10KB，多个同时会吃上下文）
```

### 2. 列表主体 — 按"帮我做什么"分段，每段一张 Markdown 表

**一级分组是 tag（动词能力类别），不是来源**。用户更在乎「这些 skill 帮我做什么」，而不是「它们是怎么装上的」。

段落顺序固定：

1. ✍️ 写作（N）— tag=Write
2. 🔍 检索（N）— tag=Find
3. 🛠️ 构建（N）— tag=Build
4. 📋 管理（N）— tag=Manage
5. 📦 其他（N）— tag=Other

每段一张表，段内按 `name` 字母顺序排：

```
── ✍️ 写作（N）──────

| Skill | 作用 | 触发方式 | 来源 | 占 token | 状态 |
|---|---|---|---|---|---|
| <name> | <≤24 字的短中文> | <具体语境，见下> | <来源> | <占 token，见下> | <状态> |
```

- **Skill** 列：只有 `name`，不带 emoji（emoji 已在分段标题里）
- **作用** 列：从 `description` 压出 ≤24 字的中文句子。砍掉 "when …" / "Use this …" / "触发场景：" 之类的条件从句，只留"做什么 / 给谁用 / 关键能力"。`description` 为空时填 `—（没写说明，可能很难被唤起）`
- **触发方式** 列：**按 `trigger_modes` 渲染具体语境。emoji 必须配中文文本标签，绝不单飞**。让用户一眼看懂这个 skill 怎么被唤起，并且明白"触发是语义匹配，类似意思的说法都算，不用照搬原短语"。渲染规则：

  遍历 `trigger_modes`（数组，每项一个 `{"mode": "...", ...}`），按 `hook > keyword > intent > slash` 顺序拼接，最多 2 个片段，用 `  ·  ` 分隔：

  | mode | 片段模板 |
  |---|---|
  | `hook` | `⚙️ 自动：<events 中文化>`（events = ["PostToolUse"] → "文件编辑后运行"、["UserPromptSubmit"] → "你提交消息时运行"，多个拼接）|
  | `keyword` | `🗣️ 关键词：<你基于 description 概括出的中文场景，≤20 字>（例："<p1>"、"<p2>" 等意思相近的说法都算）`<br/>短语从 `phrases[:2]` 取；原短语是英文就保留英文，**一定要带"意思相近的说法都算"这句话** |
  | `intent` | `💭 场景：<你基于 description/scenario 概括出的中文短句，≤20 字>（语义自动触发）` |
  | `slash` 且 `also: true` | `🔧 也可手动 /<name>`（作为第二片段，前面已有 keyword/intent 时追加）|
  | `slash` 且无 `also` | `🔧 手动：输入 /<name>`（当 skill 只能手动调，作为主片段）|

  **重要：中文场景不是字段值，而是你（Claude）基于 `description` 字段现场概括出来的**。如果 description 是英文，要翻译+提炼成一句中文场景；不要原样搬英文。原始短语只作为"例：..."辅证，用来示范触发语气。

  `trigger_modes` 为空或信息极少 → `⚠️ 说明太少，可能触发不了`

  保留 2 个片段上限是硬约束：命中 3+ 模式时，选前 2 个，在 show 里展示完整。

- **来源** 列：
  - `source=user` → `手动`
  - `source=project` → `项目`
  - `source=plugin` → `插件 <plugin>`（一定要带插件名）
- **占 token** 列：emoji **必须**配文本标签 + 括号 KB。`<N>` = `round(weight_bytes / 1024)`：
  - `weight=light` → `🪶 轻量（~<N>KB）`
  - `weight=medium` → `🍱 中等（~<N>KB）`
  - `weight=heavy` → `🐘 重（~<N>KB）`

  语义：按 SKILL.md 字节数分档（<5KB / 5–10KB / ≥10KB）。这列告诉用户"一旦唤起会吃多少上下文"。
- **状态** 列：优先级 `hard_disabled > muted > DISABLED > 开`
  - `hard_disabled == true` 或 `invocation == "DISABLED"` → `关`
  - `muted == true` → `🔇 本项目静音`（表示只在当前项目静音，换项目自动复活；emoji 后必须带文本）
  - 否则 → `开`

**空段跳过**——如果某个 tag 下 0 个 skill，整段不输出（包括标题）。

### 3. Banner（仅当 `conflicts` 或 `overlaps` 非空时输出，放在所有表格之后）

`banner` JSON 里每条 conflict / overlap 都附带 `advice` 对象。**逐字转发 advice 里的字段，不要改写、不要合并。**

```
⚠️  这次扫描发现几件事：

<每条一段，按下面模板>

（这次先忽略 · 或永久忽略）
```

Banner JSON 现在含三部分：`conflicts`、`overlaps`、`warnings`。三者都非空时，按 `warnings → conflicts → overlaps` 的顺序渲染（先给最紧迫的"体检结论"）。任意一个为空就跳过对应段落。

**context_overload 类型（`warnings[]` 里 `type: context_overload`）**，三行结构：
```
· <advice.summary>
  <advice.advice>
  当前最重 3 个：<top_heavy[0].name>（<kb>KB）、<top_heavy[1].name>（<kb>KB）、<top_heavy[2].name>（<kb>KB）
```

说明这个警告的触发条件：≥5 个 skill 同时满足「🐘 重型（>10KB）+ 自动触发（keyword/intent/hook）+ 未 mute/disable」。用户可以针对 top_heavy 里的 skill 直接用 `mute <name>`（项目级静音）或 `tune-trigger <name>`（改成仅手动触发）。

**conflict 类型（`type: conflict`）**，两行结构：
```
· <advice.summary>
  <advice.advice>
```

**bundle_conflict 类型（`type: bundle_conflict`，同插件批量冲突）**，两行：
```
· <advice.summary>
  <advice.advice>
```
不展开 `skill_names` 的 14 个名字——如果用户想看清单，用 `show <plugin>` 或追问"列出具体 skill"。

**overlap 类型**（来自 `overlaps[]`），4 行结构：
```
· 「<a.name>」和「<b.name>」功能相似。
  共同点：<advice.common>
  差异：<advice.diff>
  <advice.advice>
```

如果同类条目（conflict/overlap 分别计）超过 5 条，展示前 5 条，末尾追加 `…还有 N 条同类问题，说"全部列出"查看剩余`。

### 4. 尾行

```
总计 N（手动 a · 项目 b · 插件 c）。看详情：skill-curator show <名字>
```

**不要在列表里放**：path、完整 description、完整 trigger_modes 明细、frontmatter 其他字段。全部留给 `show <name>`。

---

## Rendering a show

Run `show <name>`. If multiple matches, list them and ask the user to pick one.

Render as a structured card（全部中文白话）：

```
── <name> ──────────────────────

分类：<tag 中文>（✍️写作 / 🔍检索 / 🛠️构建 / 📋管理 / 📦其他）
来源：<手动 / 项目 / 插件 xxx>
占 token：<🪶 轻量 / 🍱 中等 / 🐘 重>（~<weight_bytes 转成 KB，整数> KB）
状态：<开 / 🔇 本项目静音 / 关>

作用
  <description 原文，不截断>

触发方式
  <按 trigger_modes 数组展开，每种一段，见下>

文件路径
  <path>
```

**触发方式渲染**（遍历 `trigger_modes`，按 `hook → keyword → intent → slash` 排序，每种一段）：

- **keyword 型**：
  ```
  🗣️ 关键词触发 — 你说到下面这些话或意思相近的表述时会自动用到（Claude Code 是语义匹配，原文是英文也 OK）：
      · <phrases[0]>
      · <phrases[1]>
      · ...（所有 phrases）
  ```

- **intent 型**：
  ```
  💭 场景触发 — 你在做下面这件事时会自动用到：
      <scenario 原文，完整>
  ```

- **slash 型**（非 also）：
  ```
  🔧 仅手动调用 — 要用它请输入：<command>
  ```

- **slash 型（also: true）**：
  ```
  🔧 也可手动输入 <command>（上面的自动触发不依赖这个）
  ```

- **hook 型**：
  ```
  ⚙️ 自动运行 — 发生下面这些事件时会自动跑：<events 全部>
  ```

如果 `trigger_modes` 为空：
```
⚠️ 检测不到有效的触发方式——这个 skill 可能永远不会被唤起。
    检查 ~/.claude/settings.json 里是否被 deny，或 description 是否写得太少。
```

如果 description 为空，在"作用"行显示 `（没写说明——这个 skill 很难被自动触发，建议补充描述）`。

---

## Operations

### disable <name>

1. Run `show <name>` to locate. If multiple matches, disambiguate with the user first.
2. **Before any write**, show the user the exact change you are about to make and ask to confirm.
3. Execute:
   - **user** or **project** source:
     - Back up: `cp <path> <path>.bak-<timestamp>`
     - Edit frontmatter: set `disable-model-invocation: true` and `user-invocable: false` (add these keys right after `name:` if missing).
   - **plugin** source:
     - DO NOT touch the plugin SKILL.md (plugin updates will overwrite it).
     - Run `recommend <name>` to obtain the exact `deny_rule`.
     - Edit `~/.claude/settings.json`: add `deny_rule` (e.g. `"Skill(claude-mem:do)"`) to `permissions.deny` (create the nested structure if absent). Preserve all other settings.
4. 反馈一行：`已禁用 <name>。撤销：skill-curator enable <name>`

### enable <name>

1. Locate via `show <name>`.
2. Reverse of disable:
   - **user/project**: either delete the two invocation flags or set them to `false` / `true` respectively. Restore from `.bak-<timestamp>` if the user prefers a full revert.
   - **plugin**: remove the matching `Skill(plugin:name)` entry from `permissions.deny`.
3. 反馈一行：`已启用 <name>`

### remove <name>

1. Run `recommend <name>`.
2. 输出直接推荐（不做中立多选菜单），rationale 要翻成中文白话，不保留 "permission deny" / "frontmatter flags" 之类术语：
   ```
   推荐：<白话版 mode>
     理由：<中文白话 rationale>
   或者：<白话版 alt>
   ```
   mode 白话对照：
   - `DISABLE (frontmatter flags)` → "停用（改文件开关）"
   - `DISABLE via permission deny` → "停用（在设置里拒绝加载）"
   - `UNINSTALL plugin` → "整个插件卸载"
3. 问一句："按推荐的来吗？（是 / 用备选 / 取消）"
4. Execute based on user's pick:
   - **DISABLE (frontmatter flags)** → same flow as `disable` on user/project source.
   - **DISABLE via permission deny** → same flow as `disable` on plugin source.
   - **UNINSTALL plugin** → DO NOT run the uninstall command silently. Print the exact command for the user's Claude Code version (commonly via the plugin-management UI or `/plugin` command) and wait for them to confirm or run it themselves. Uninstall is destructive.
   - **Hard remove** (only offered as `alt` for user-level skills):
     - Move the skill directory to `~/.claude/skills/.trash/<name>-<YYYYMMDD-HHMMSS>/`
     - Write a companion file `<trash-entry>/.expires` containing the epoch-time cutoff (now + 3 days).

### tune-trigger <name>

调触发方式——remix 的 MVP 入口。**只管触发相关**：开关 auto/manual flag、加/改 description 里的触发关键词、改场景描述。不做 description 其他部分的编辑（那属于未来的完整 tune）。

1. **读取现状**：运行 `show <name>`，把当前 `trigger_modes` 全部念给用户听（每种模式的具体数据：关键词列表、场景原文、slash 命令、hook 事件），并说"你想怎么调？"

2. **识别 hook 型 skill**：如果 `trigger_modes` 里有 `mode: hook` 的条目，告诉用户：
   ```
   这个 skill 的一部分触发方式是由插件代码里的 hook 定义的（事件：<events>），
   不在 SKILL.md 里，tune-trigger 改不了 hook 部分。
   但它的关键词/场景触发（如果有）还是可以调。
   ```
   如果**只有 hook 模式**：拒绝操作，建议用户去改插件源码或 settings.json。

3. **识别诉求**：根据用户自然语言，判断属于哪种调整：
   - "在我说 X 时也触发" / "加个触发词" → 在 description 里追加一段关键词
   - "不要自动触发了，只能手动调" → 把 `disable-model-invocation` 设为 `true`
   - "反过来，想让它自动出现" → 把 `disable-model-invocation` 删掉或设为 `false`
   - "场景描述不对，改成 X" → 改写 description 里的场景段

4. **插件级 skill 强制先 fork**（`source == plugin`）：
   ```
   这个 skill 来自 <plugin> 插件（~/.claude/plugins/cache/.../skills/<name>/）。
   插件原文件不能改，否则下次插件更新会盖掉你的改动。
   我要把它整个 skill 目录复制到 ~/.claude/skills/<name>/，在你的副本上改。
   复制完后 Claude Code 会优先用你的手动版（手动 > 插件）。
   确认吗？
   ```
   用户确认后：
   - `cp -r <plugin_skill_dir> ~/.claude/skills/<name>/`
   - 在新副本的 frontmatter 顶部加注释行 `# forked from <plugin>@<version> on <date>`
   - 后续编辑针对用户副本

5. **生成 diff 预览**：明确展示 frontmatter / description 的改动（Before/After），等用户确认。

6. **写入**：备份 `<path>.bak-<timestamp>`（最多保留 5 份），再写新内容。

7. **反馈**：
   - 关键词调整：`已在 <name> 加了 N 个触发词。下次你说"<example>"它就会出来。`
   - 开关切换：`已把 <name> 改成仅手动调用。要用它请输入 /<name>。` / `已把 <name> 改成自动触发。`
   - fork：前置反馈 `已把 <name> fork 到 ~/.claude/skills/<name>/`

### mute <name>

把 skill 在**当前项目**里静音——只影响当前项目，换项目自动复活。典型用法："这个 web 项目里我用不到飞书的 skill"。与 `disable`（全局停用）的差别就是作用域。

1. **定位**：运行 `show <name>`，多个匹配时先消歧。

2. **已被全局 disable 的情况**：如果该 skill 的 `hard_disabled` 为 true，告诉用户：
   ```
   <name> 已经全局 disable 了，本项目里自然也不会触发，不需要再 mute。
   如果想恢复全局，用 enable <name>。
   ```
   然后退出。

3. **说明作用域 + 确认**：
   ```
   我要把 <name> 加到 <当前项目目录>/.claude/settings.json 的 permissions.deny 里。
   作用域：只当前项目。换到别的项目自动失效，不需要手动 unmute。
   对比 disable：disable 是全局的，换项目也不会触发。
   确认 mute 吗？
   ```

4. **执行**：`python3 ~/.claude/skills/skill-curator/lib/curator.py mute <name>`

5. **边界：非项目根目录**：如果 curator.py 返回非零退出码并提示"当前目录不像项目根"（没有 `.claude/`、`.git/`、或常见 package 清单），转达给用户：
   ```
   当前目录看起来不是项目根，mute 是项目级的——会写到 <cwd>/.claude/settings.json，
   但这个目录不像一个项目。要不要改用 disable <name> 做全局停用？
   ```
   不自作主张创建 `.claude/settings.json`。

6. **反馈**：
   ```
   已在本项目静音 <name>（写入 <project>/.claude/settings.json）。
   换项目自动失效，或 skill-curator unmute <name> 立即恢复。
   ```

### unmute <name>

从当前项目的 settings.json 里撤掉 mute 规则。

1. **执行**：`python3 ~/.claude/skills/skill-curator/lib/curator.py unmute <name>`

2. **未找到规则**：如果当前项目 settings.json 里没有该条 deny 规则，curator.py 会返回相应提示，转达：
   ```
   本项目里没静音过 <name>，无需操作。
   （如果你是想恢复全局停用，用 enable <name>。）
   ```

3. **反馈**：`已在本项目恢复 <name>。`

### Trash auto-purge

At the start of **every** `remove` invocation, scan `~/.claude/skills/.trash/`. For any entry whose mtime is older than 3 days, `rm -rf` it. If any were purged, 追加一行：`已清理 N 个过期回收站条目。`

---

## Safety rules (non-negotiable)

1. **Never** modify files under `~/.claude/plugins/cache/`. They are controlled by plugin updates and your edits will be overwritten.
2. **Always** back up user- or project-level SKILL.md files before editing (`.bak-<timestamp>`). Keep at most 5 backups per skill (rotate oldest).
3. **Always** show the user the exact diff / change before writing. Wait for their explicit confirmation.
4. **Never** present the "recommended" and "alternative" modes as equal options. The recommendation is direct; the alternative is a one-line override path.
5. **Never** run a plugin uninstall command silently — it removes many skills at once.

---

## Tone

- **用户可见的输出一律用中文白话**。不出现 CONFLICT / OVERLAP / Effective / Shadowed / THIN / KEYWORD-RICH / SEMANTIC / AUTO / MANUAL / DISABLED / USER / PLUGIN / PROJECT 这类英文术语（skill 名、插件名、命令名这类专有标识除外）。
- 直接推荐，不说"也许 / 或许 / 你可以看看"。
- 操作反馈一行就够。不复述、不总结、不说"我刚才做了 X"。
- 请求有歧义（比如同名冲突）就问一次，不要猜。
- **emoji 不单飞**：任何 emoji 出现时必须紧跟中文文本标签。`🪶`/`🍱`/`🐘` 要带「轻量/中等/重」，`🗣️`/`💭`/`🔧`/`⚙️` 要带「关键词/场景/手动/自动」，`🔇` 要带「本项目静音」。用户不该靠背 emoji 含义来读懂界面。
