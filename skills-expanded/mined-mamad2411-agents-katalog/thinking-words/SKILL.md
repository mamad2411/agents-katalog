---
name: thinking-words
description: |
  切换 Claude Code 的思考词组。当用户说 "/thinking-words"、"切换思考词"、"换个思考词"、"换个spinner词"、"切换spinner" 时触发。
---

# Thinking Words - 切换思考词组

管理 Claude Code 的 spinner verbs 配置，支持预设词组和用户自定义词组。

## 配置文件位置

- **主配置**: `~/.claude/settings.json` - spinnerVerbs 字段
- **预设存储**: `~/.claude/spinner-presets.json` - 用户自定义词组
- **使用统计**: `~/.claude/thinking-words-stats.json` - 预设使用频率统计
- **自动切换**: `~/.claude/thinking-words-auto.json` - 自动切换配置
- **导入导出**: 默认导出到 `~/.claude/thinking-words-export.json`，或指定路径

## 预设心境

### 1. default - 默认英文
使用 Claude Code 内置的 231 个英文思考词（不修改配置即为默认）

### 2. classical - 中文古风
```json
["静思中", "沉吟中", "凝思中", "遐思中", "冥想中", "幽思中", "玄思中", "深思中", "推敲中", "琢磨中", "揣摩中", "参悟中", "领悟中", "体悟中", "感悟中", "禅悟中", "展卷中", "翻阅中", "览阅中", "披阅中", "诵读中", "吟咏中", "吟哦中", "吟诵中", "挥毫中", "泼墨中", "落笔中", "蘸墨中", "题词中", "题字中", "濡墨中", "研墨中", "伫立中", "凝望中", "远眺中", "眺望中", "守候中", "等候中", "期盼中", "翘首中", "徘徊中", "踟蹰中", "踯躅中", "彷徨中", "漫步中", "徜徉中", "游历中", "遨游中", "构思中", "运筹中", "筹划中", "谋划中", "酝酿中", "孕育中", "孵化中", "萌发中", "采撷中", "撷取中", "收集中", "搜罗中", "筛选中", "拣选中", "拾遗中", "探寻中", "编织中", "交织中", "穿针中", "引线中", "经纬中", "纺织中", "织造中", "编结中", "听雨中", "观云中", "赏月中", "望风中", "听风吟", "观潮起", "看云卷", "赏花落", "采菊中", "种豆中", "耕耘中", "播撒中", "浇灌中", "培育中", "养护中", "润泽中", "煮茶中", "烹茶中", "煎茶中", "品茗中", "斟酌中", "酌情中", "斟茶中", "奉茶中", "抚琴中", "弄弦中", "吹箫中", "弹奏中"]
```
示例词组：静思中、煮茶中、抚琴中

### 3. simple - 简洁中文
```json
["思考中", "分析中", "推理中", "计算中", "处理中", "读取中", "写入中", "搜索中", "查询中", "生成中", "创建中", "编辑中", "删除中", "更新中", "连接中", "传输中", "加载中", "解析中", "编译中", "运行中", "测试中", "验证中", "优化中", "重构中", "调试中", "部署中", "发布中", "监控中"]
```
示例词组：思考中、处理中、部署中

### 4. cute - 可爱卖萌
```json
["努力思考中~", "认真分析中~", "绞尽脑汁中~", "使劲想呀~", "大脑运转中~", "冥思苦想中~", "灵光一闪中~", "啊哈时刻~", "嗯嗯思考中~", "好的马上~", "来啦来啦~", "正在努力~", "加油加油~", "冲冲冲~", "好嘞好嘞~", "收到收到~"]
```
示例词组：努力思考中~、来啦来啦~、冲冲冲~

### 5. japanese - 日式风格
```json
["考え中", "検討中", "分析中", "処理中", "作成中", "読込中", "書込中", "接続中", "生成中", "計算中", "探索中", "整理中", "構築中", "最適化中", "確認中", "準備中"]
```
示例词组：考え中、処理中、構築中

### 6. cyberpunk - 赛博朋克
```json
["神经元同步中", "数据注入中", "矩阵计算中", "量子解码中", "神经链接中", "协议握手", "缓存刷新", "进程注入", "内存映射", "端口扫描", "载荷解密", "隧道建立", "协议升级", "节点同步", "数据重构", "逻辑门翻转"]
```
示例词组：神经元同步中、矩阵计算中、端口扫描

### 7. wuxia - 武侠江湖
```json
["悟道中", "修炼中", "破境中", "飞升中", "入定中", "凝气中", "筑基中", "结丹中", "元婴中", "化神中", "渡劫中", "大成中", "圆满中", "运功中", "调息中", "吐纳中", "运转周天", "打通经脉", "冲穴中", "运劲中", "蓄力中", "聚气中", "凝神中", "练剑中", "习武中", "演武中", "切磋中", "对决中", "过招中", "破招中", "出招中", "收招中", "拆招中", "剑气纵横", "剑意凌厉", "剑心通明", "拔剑中", "出鞘中", "御剑中", "祭剑中", "顿悟中", "明悟中", "参透中", "贯通中", "融会贯通", "触类旁通", "行走江湖", "仗剑天涯", "游历四方", "行侠仗义", "闯荡江湖", "踏遍青山", "浪迹天涯", "闭关中", "面壁中", "参禅中", "苦修中", "历练中", "淬炼中", "踏雪无痕", "凌波微步", "飞檐走壁", "身法飘逸", "纵身一跃", "奇门遁甲", "五行八卦", "布阵中", "破阵中", "点穴中", "解穴中", "解毒中", "疗伤中", "炼丹中", "淬毒中", "机关术中", "密室探索", "寻宝中", "夺宝中", "比武中", "论剑中", "擂台中", "江湖救急", "斩妖除魔", "替天行道", "仗义执言", "恩怨分明", "侠骨柔情", "快意恩仇", "剑胆琴心", "笑傲江湖", "问剑中", "求道中", "证道中", "得道中", "化境中", "无我中", "忘我中", "天人合一"]
```
示例词组：悟道中、御剑中、笑傲江湖

### 8. programmer - 程序员梗
```json
["debug中", "stack overflow中", "rubber duck中", "grep中", "commit中", "deploy中", "RTFM中", "它在我机器上能跑", "这不是bug是feature", "压住Enter中", "coffee break中", "写bug中", "改bug中", "又改bug中", "永久修复中", "临时修复中", "猴子补丁中", "面向运气编程", "祈祷中", "烧香中", "祭拜键盘", "玄学调试", "祈祷编译通过", "等待CI中", "等待PR中", "等待review中", "等待merge中", "等待deploy", "等待上线", "等待监控", "等待告警", "等待下班", "等待周五"]
```
示例词组：debug中、它在我机器上能跑、coffee break中

### 9. emoji - 纯 Emoji
```json
["🤔", "🔍", "⚡", "🚀", "💻", "🧠", "🎯", "🔥", "✨", "🐛", "📝", "🎨", "🔧", "💡", "🎪", "🎭"]
```
示例词组：🤔、🚀、🧠

### 10. minimal - 极简
```json
["..."]
```
只有一个词组：...

### 11. time-based - 时间感知（动态预设）
这是一个**特殊预设**，会根据当前时间自动选择合适的词组：
- **早晨 (06:00-12:00)**：晨思中、醒脑中、清醒中、晨练中、早读中
- **下午 (12:00-18:00)**：午思中、下午茶中、小憩中、充能中、继续中
- **傍晚 (18:00-22:00)**：晚思中、收尾中、整理中、总结中、归档中
- **深夜 (22:00-06:00)**：夜思中、沉思中、静夜思、冥想中、入定中

使用 `/thinking-words time-based` 时，会根据当前时间动态生成词组列表。

## 使用方式

### 随机切换
```
/thinking-words
```
随机选择一组预设词组应用。切换成功后会展示一个随机词组作为反馈。

### 权重随机
```
/thinking-words random --prefer cute
```
随机选择，但指定的预设有更高概率被选中（权重系数为预设的 weight 字段值，默认为 1.0）。

### 指定切换
```
/thinking-words classical
/thinking-words cute
/thinking-words programmer
```

### 切换前预览
```
/thinking-words preview classical
```
展示预设的词组数量、创建时间、以及随机 5 个示例词组，不实际切换。

### 混合多个预设
```
/thinking-words mix classical cute
/thinking-words mix programmer emoji simple
```
将多个预设的词组合并在一起使用，增加多样性。

### 恢复默认
```
/thinking-words default
```
移除自定义配置，使用 Claude Code 默认的英文思考词。

### 查看当前（增强版）
```
/thinking-words show
```
显示：
1. 当前使用的预设名（如果是预设）
2. 词组总数
3. 随机展示 3 个示例词组

### 列出所有预设（增强版）
```
/thinking-words list
```
列出每个预设的：
- 名称
- 词组数量
- 创建时间（自定义预设）
- 随机 3 个示例词组
- 权重值（自定义预设）

### 添加自定义词组（增强校验）
```
/thinking-words add my-style "思考中" "分析中" "生成中" "处理中"
```
添加时会进行校验：
- 词组长度：2-15 字符（emoji 按 1 字符计）
- 去重：自动去除重复词组
- 非法字符：检测明显不合适的输入
- 最少数量：至少需要 3 个词组

添加成功后自动应用，并展示一个示例词组作为反馈。

### 删除自定义词组
```
/thinking-words remove my-style
```

### 导出配置
```
/thinking-words export
/thinking-words export ~/my-mood-backup.json
```
导出所有自定义预设到文件，默认路径 `~/.claude/thinking-words-export.json`。

### 导入配置
```
/thinking-words import ~/my-mood-backup.json
```
从文件导入自定义预设，会合并到现有预设中（同名预设会被覆盖）。

### 查看使用统计
```
/thinking-words stats
```
显示：
- 各预设使用次数排行
- 最常用预设（favorite）
- 总切换次数

### 智能推荐
```
/thinking-words recommend
```
根据使用历史智能推荐预设。推荐逻辑：
- 优先推荐高频使用的预设
- 结合当前时间段（早晨推荐 classical，深夜推荐 minimal 等）

### 自动切换（新功能）

#### 查看自动切换配置
```
/thinking-words auto
```
显示当前自动切换配置和状态（启用/禁用）。

#### 启用自动切换
```
/thinking-words auto on
```
启用自动切换，使用默认配置：
- 早晨 06:00 → classical
- 下午 12:00 → simple
- 傍晚 18:00 → wuxia
- 深夜 22:00 → minimal

会创建 4 个定时任务，每天自动切换。

#### 关闭自动切换
```
/thinking-words auto off
```
关闭自动切换，删除所有相关定时任务。

#### 修改自动切换配置
```
/thinking-words auto set morning cute
/thinking-words auto set afternoon emoji
/thinking-words auto set evening classical
/thinking-words auto set night minimal
```
修改指定时间段的预设。

## 执行步骤

### 1. 解析参数

识别子命令类型：
- 无参数 → 随机切换
- `random [--prefer <预设>]` → 权重随机
- `preview <预设>` → 预览不切换
- `mix <预设1> <预设2>...` → 混合预设
- `<预设名>` → 指定切换
- `show` → 查看当前配置
- `list` → 列出所有预设
- `add <名称> <词组...>` → 添加自定义
- `remove <名称>` → 删除自定义
- `export [路径]` → 导出配置
- `import <路径>` → 导入配置
- `default` → 恢复默认
- `stats` → 查看使用统计
- `recommend` → 智能推荐
- `auto` → 查看自动切换配置
- `auto on` → 启用自动切换
- `auto off` → 关闭自动切换
- `auto set <时间段> <预设>` → 修改自动切换配置

### 2. 执行对应操作

#### preview 命令
1. 检查预设是否存在（内置 + 自定义）
2. 读取预设词组
3. 输出：名称、词组数量、创建时间（如有）、随机 5 个示例词组
4. 提示用户确认是否要切换

#### mix 命令
1. 验证所有预设都存在
2. 合并所有词组（去重）
3. 写入 settings.json，source 字段记录为 "mix:classical,cute"
4. 展示一个随机词组作为反馈

#### random 命令（带 --prefer）
1. 计算权重：prefer 预设权重为 weight 字段值，其他为 1.0
2. 按权重随机选择
3. 应用并展示反馈

#### show 命令（增强版）
1. 读取 settings.json 的 spinnerVerbs
2. 解析 source 字段判断预设来源
3. 输出：来源、词组总数、随机 3 个示例词组
4. 如果 source 为 "mix:xxx,yyy"，列出混合的预设名

#### list 命令（增强版）
1. 遍历所有内置预设和自定义预设
2. 对每个预设输出：名称、词组数量、创建时间（如有）、权重（如有）、随机 3 个示例词组
3. 格式化输出为表格或列表

#### add 命令（增强校验版）
1. 校验词组：
   - 长度检查：每个词组 2-15 字符
   - 去重：去除重复词组
   - 数量检查：至少 3 个有效词组
   - 非法字符检查：不允许纯空格、控制字符等
2. 校验失败时输出具体错误信息
3. 保存到 spinner-presets.json
4. 应用到 settings.json
5. 展示一个示例词组作为反馈

#### time-based 命令
1. 获取当前时间
2. 判断时间段（早晨/下午/傍晚/深夜）
3. 动态生成对应的词组列表
4. 应用并展示反馈

#### stats 命令
1. 读取 `~/.claude/thinking-words-stats.json`
2. 如果文件不存在，初始化空统计
3. 输出：
   - 各预设使用次数排行（按次数降序）
   - 最常用预设（favorite）
   - 总切换次数
4. 如果没有任何历史，提示用户先切换预设

#### recommend 命令
1. 读取 `~/.claude/thinking-words-stats.json`
2. 如果有使用历史：
   - 计算各预设权重 = 使用次数
   - 加入时间段偏好（早晨 classical +1，下午 simple +1，傍晚 wuxia +1，深夜 minimal +1）
   - 按权重随机推荐
3. 如果没有历史，根据当前时间段推荐默认预设

#### auto 命令（查看配置）
1. 读取 `~/.claude/thinking-words-auto.json`
2. 显示：
   - 是否启用
   - 各时间段配置（时间 + 预设）
   - 如果启用，显示定时任务 ID

#### auto on 命令
1. 读取 `~/.claude/thinking-words-auto.json`
2. 设置 `enabled: true`
3. 使用 CronCreate 创建 4 个定时任务：
   - morning: `0 6 * * *` → `/thinking-words <预设>`
   - afternoon: `0 12 * * *` → `/thinking-words <预设>`
   - evening: `0 18 * * *` → `/thinking-words <预设>`
   - night: `0 22 * * *` → `/thinking-words <预设>`
4. 设置 `durable: true` 持久化
5. 保存任务 ID 到配置文件
6. 输出成功信息

#### auto off 命令
1. 读取 `~/.claude/thinking-words-auto.json`
2. 获取所有任务 ID
3. 使用 CronDelete 删除每个任务
4. 设置 `enabled: false`
5. 输出成功信息

#### auto set 命令
1. 读取 `~/.claude/thinking-words-auto.json`
2. 验证时间段（morning/afternoon/evening/night）
3. 验证预设是否存在
4. 更新配置文件
5. 如果已启用，删除旧任务并创建新任务
6. 输出成功信息

### 3. 写入配置

修改 `~/.claude/settings.json` 中的 `spinnerVerbs` 字段，格式：

```json
{
  "spinnerVerbs": {
    "mode": "replace",
    "verbs": ["思考中", "分析中", ...],
    "source": "classical"
  }
}
```

source 字段记录来源：
- 单一预设：`"classical"`
- 混合预设：`"mix:classical,cute"`
- 自定义预设：`"my-style"`
- time-based：`"time-based:morning"`（带时间段）

### 4. 写入统计

每次切换预设后，更新 `~/.claude/thinking-words-stats.json`：

1. 读取现有统计数据
2. 在 `history` 数组添加记录（保留最近 100 条）
3. 更新 `counts` 中对应预设的计数
4. 更新 `favorite` 为使用最多的预设
5. 写回文件

### 4. 提示生效

告知用户需要重启 Claude Code 才能生效，并展示一个随机词组让用户立刻感受新风格。

## 配置格式

### settings.json
```json
{
  "spinnerVerbs": {
    "mode": "replace",
    "verbs": ["思考中", "分析中", ...],
    "source": "classical"
  }
}
```

### spinner-presets.json
```json
{
  "presets": {
    "my-style": {
      "verbs": ["思考中", "分析中", ...],
      "created_at": "2026-03-26",
      "weight": 1.0,
      "example": ["思考中", "分析中", "生成中"]
    }
  }
}
```

### mood-export.json（导出格式）
```json
{
  "exported_at": "2026-03-28",
  "version": "2.0",
  "presets": {
    "my-style": {
      "verbs": [...],
      "created_at": "2026-03-26",
      "weight": 1.0
    }
  }
}
```

### mood-stats.json（使用统计）
```json
{
  "history": [
    { "preset": "wuxia", "time": "2026-03-28T10:30:00Z" },
    { "preset": "emoji", "time": "2026-03-28T11:00:00Z" }
  ],
  "counts": {
    "wuxia": 5,
    "emoji": 3,
    "classical": 2
  },
  "favorite": "wuxia"
}
```

### mood-auto.json（自动切换配置）
```json
{
  "enabled": true,
  "schedule": {
    "morning": { "time": "06:00", "preset": "classical", "job_id": "mood-morning" },
    "afternoon": { "time": "12:00", "preset": "simple", "job_id": "mood-afternoon" },
    "evening": { "time": "18:00", "preset": "wuxia", "job_id": "mood-evening" },
    "night": { "time": "22:00", "preset": "minimal", "job_id": "mood-night" }
  }
}
```

## 错误处理

| 错误情况 | 提示信息 |
|----------|----------|
| JSON 解析失败 | 配置文件损坏，请检查 ~/.claude/spinner-presets.json |
| 预设不存在 | 预设 'xxx' 不存在，可用预设：default, classical, ... |
| 词组长度不合规 | 词组 'xxx' 长度为 20，超出限制（2-15字符） |
| 词组数量不足 | 至少需要 3 个有效词组，当前只有 2 个 |
| 词组重复 | 去重后剩余 5 个词组（原 8 个中有 3 个重复） |
| 导入文件不存在 | 导入文件 ~/xxx.json 不存在 |
| 导入格式错误 | 导入文件格式错误，缺少 presets 字段 |

## 注意事项

- 切换后需要**重启 Claude Code** 才能生效
- `default` 预设会移除 spinnerVerbs 配置，恢复 Claude Code 默认行为
- 用户自定义词组保存在 `~/.claude/spinner-presets.json`，升级不会丢失
- `time-based` 预设每次切换时会根据当前时间动态生成词组
- 混合预设的去重是基于词组文本完全匹配
- 权重随机时，weight 值越大被选中概率越高，默认为 1.0
- **使用统计**：history 数组最多保留 100 条记录，超出时删除最早的
- **自动切换**：需要 Claude Code 运行中才能触发定时任务，关闭后任务暂停
- **自动切换**：定时任务 durable 模式会在重启后自动恢复