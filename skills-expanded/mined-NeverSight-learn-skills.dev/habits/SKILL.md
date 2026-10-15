---
name: habits
description: "管理存储在本地 SQLite 中的每日打卡记录，支持添加打卡、查看记录、统计分析、连续打卡天数、删除和修改。当用户提到打卡、签到、记录运动/阅读/学习/健身/冥想/跑步/骑行等日常习惯，或者想查看自己某个习惯坚持了多少天、本周运动了多少时间、今天打卡了什么，都应主动使用这个 skill。即使用户没有明确说“打卡”，只要涉及日常习惯追踪、活动记录，都适用。英文场景同样适用，如 check in, log my workout, track my reading, how many days in a row, streak, habits。"
argument-hint: "add|list|stats|streak|update|delete|export|import|config [选项]"
metadata:
  version: "1.0.0"
  data_version: "1.0.0"
  author: https://github.com/zsspub
  license: MIT
  updated_at: "2026-04-02"
---

# 每日打卡技能

基于本地 SQLite 数据库记录和管理每日打卡数据。数据文件由脚本通过 `import.meta.dirname` 自动定位，存放在与 skill 目录同级的 `.data/zsspub/habits/` 目录下，无需手动配置路径。时间以 UTC 存入数据库，展示时自动按用户配置的时区进行转换。

## 环境要求

- Node.js >= 22.5.0（使用内置 `node:sqlite`）

## 执行方式

所有命令均通过 `node` 直接运行脚本：

```bash
node <本 SKILL.md 所在目录>/scripts/habits.mjs <命令> [选项]
```

下文中 `habits` 均代表 `node <skill目录>/scripts/habits.mjs`，请替换为实际路径。

## 首次使用：配置时区

脚本将时间以 UTC 存入数据库，展示时按用户配置的时区转换。**首次使用时**，请先判断用户的时区并运行 `config --timezone` 命令：

- 若用户提到城市（如"我在上海"），推断为 `Asia/Shanghai`
- 若无法判断，询问用户所在城市或时区，然后运行：

```bash
habits config --timezone=Asia/Shanghai
```

## 使用流程

### 第一步：理解用户意图，映射到命令

打卡的核心是从用户自然语言中提取结构化信息：

| 用户说的话（示例） | 提取信息 | 应执行的命令 |
|---|---|---|
| "打卡骑行 30 分钟" | 主题=骑行, 标签=运动, 时长=30 | `add`（同时用 `--raw` 存储原话） |
| "今天读了一章《原则》" | 主题=阅读, 标签=学习, 备注=《原则》一章 | `add` |
| "刚跑完步 5 公里 40 分钟" | 主题=跑步, 标签=运动, 时长=40, 备注=5公里 | `add` |
| "冥想打卡" | 主题=冥想, 标签=健康 | `add`（无时长） || "打卡成都美食，吃了火锅和串串香" | 主题=美食, 标签=生活, 备注=成都 火锅 串串香 | `add` |
| "打卡故宫" | 主题=旅行, 标签=生活, 备注=故宫 | `add` || "今天打卡了什么？" | — | `list --period=today` |
| "看看我这个月的打卡记录" | — | `list --period=month` |
| "这周运动了多少时间？" | — | `stats --period=week --tag=运动` |
| "骑行连续打卡多少天了？" | — | `streak --topic=骑行` |
| "把第3条打卡改成45分钟" | — | `update 3 --duration=45` |
| "删掉那条跑步记录" | — | 先 `list` 找到 id，再 `delete <id>` |
| "导出打卡记录" / "备份打卡数据" | — | `export` |
| "导入打卡记录" / "从文件恢复" | — | `import --file=<路径>` |

**原话保存：** 每次 `add` 打卡时，将用户说的原始文字通过 `--raw` 参数原封不动地存储下来，方便日后回溯。

**备注提取规则：** `--note` 用于保存无法归入其他字段的关键信息。例如：
- 地点信息：城市、景点、餐厅名（“打卡故宫” → 备注=故宫）
- 具体内容：书名、课程名、食物名称（“读了《原则》第三章” → 备注=《原则》第三章）
- 量化指标：距离、组数、页数等时长以外的数值（“跑了5公里” → 备注=5公里）

**标签自动推断规则：**

根据主题自动推断标签，用户可以用 `--tags` 覆盖：

| 主题关键词 | 推断标签 |
|---|---|
| 骑行、跑步、游泳、健身、瑜伽、拉伸、健走、跳绳、打球、登山、滑雪、滑冰 | 运动 |
| 阅读、读书、看书、听书 | 学习 |
| 冒想、早睡、早起、喝水、护肤 | 健康 |
| 背单词、刷题、练琴、画画、写作、练字、学英语 | 学习 |
| 做饭、家务、整理、美食、在家练习 | 生活 |
| 旅行、参观、游览、打卡景点 | 生活 |
| 看电影、追剧、听音乐、玩游戏 | 娱乐 |

如果主题不在上述列表中，请根据语义合理推断。打卡总应当有标签，方便后续统计筛选。

**时长推断规则：**
- "X 分钟" → `--duration=X`
- "X 小时" → `--duration=X*60`
- "X 小时 Y 分钟" → `--duration=X*60+Y`
- "半小时" → `--duration=30`
- "X个半小时" / "X小时半" → `--duration=X*90`
- "一个半小时" → `--duration=90`
- "一刻钟" / "15分钟" → `--duration=15`
- 没有提到时长则不传 `--duration`

### 第二步：执行命令并呈现结果

将命令输出直接展示给用户。打卡成功后，可以给一句简短的鼓励。

## 命令说明

### 添加打卡
```
habits add "主题" --raw="用户原话" [--tags=标签1,标签2] [--duration=分钟数] [--note="备注"] [--at="YYYY-MM-DD HH:mm:ss"]
```
- `--raw`：**必填**，用户说的原话，原封不动存储
- `--tags`：逗号分隔的标签列表，例如 `运动,户外`
- `--duration`：时长（分钟），正整数
- `--note`：备注文本
- `--at`：打卡时间（用户本地时区），默认当前时间。用于补打卡场景

### 查看打卡记录
```
habits list [--topic=主题] [--tag=标签] [--date=YYYY-MM-DD] [--period=today|week|month|year] [--from="YYYY-MM-DD HH:mm:ss"] [--to="YYYY-MM-DD HH:mm:ss"] [--search=关键字] [--limit=数量]
```
- `--period`：快捷时间范围（today/week/month/year）
- `--date`：查看某天的所有打卡
- `--from` / `--to`：时间范围筛选
- `--search`：按主题和备注模糊搜索
- `--limit`：限制返回条数
- 默认按时间倒序

### 修改打卡
```
habits update <id> [--topic=...] [--tags=...] [--duration=...] [--note=...] [--at="YYYY-MM-DD HH:mm:ss"]
```
- 清除时长：`--duration=null`

别名：`edit`

### 删除打卡
```
habits delete <id>
```
别名：`del`、`rm`

### 统计分析
```
habits stats [--topic=主题] [--tag=标签] [--period=today|week|month|year] [--from="YYYY-MM-DD HH:mm:ss"] [--to="YYYY-MM-DD HH:mm:ss"]
```
- `--period`：快捷时间范围（today/week/month/year）
- 输出：总打卡次数、总时长、按主题统计、按标签统计

### 连续打卡
```
habits streak [--topic=主题] [--tag=标签]
```
- 输出：当前连续天数、最长连续天数、累计打卡天数

### 查看/更新配置
```
habits config [--timezone=<IANA时区>]
```

### 导出打卡记录
```
habits export [--file=<路径>] [--topic=主题] [--tag=标签]
```
- 导出为 CSV 格式
- `--file`：指定输出文件路径，不指定则自动生成到数据目录
- `--topic` / `--tag`：可选筛选条件

### 导入打卡记录
```
habits import --file=<路径>
```
- 从 CSV 文件导入，CSV 必须包含 `topic` 列
- 导入前会校验数据格式，校验失败则取消导入

## 示例

```bash
# 打卡骑行 30 分钟
habits add "骑行" --tags=运动 --duration=30 --raw="打卡骑行 30 分钟"

# 打卡阅读，带备注
habits add "阅读" --tags=学习 --note="《原则》第三章"

# 补打卡（昨天的跑步）
habits add "跑步" --tags=运动 --duration=40 --note="5公里" --at="2026-04-01 19:30:00"

# 查看今天的打卡
habits list --date=2026-04-02

# 查看所有骑行记录
habits list --topic=骑行

# 本周运动统计
habits stats --period=week --tag=运动

# 查看骑行连续打卡天数
habits streak --topic=骑行

# 修改第 2 条打卡的时长
habits update 2 --duration=45

# 删除第 5 条打卡
habits delete 5
```
