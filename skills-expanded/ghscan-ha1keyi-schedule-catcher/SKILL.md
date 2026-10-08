# 邮件 / 文本 → 日程抽取 Skill

> 「日程捕手」流水线的**机械抽取层**。当输入是**邮件导出文件**或**大段纯文本**时加载本 Skill；
> 单条短文本直接用 `01-日程总结专员.md` 即可，不需要本文件。
>
> 契约版本：**v5**。产出写入 `public/data/schedule.json`。

---

## 何时用

- 用户给了 `.eml` / `.mbox` / 邮件客户端导出的 `.txt` / `.json` / `.csv`
- 用户一次性粘贴了很多封邮件正文 / 一整个学期的公告
- 需要批量、机械地先把「明显是活动/截止」的东西捞出来，再由你（助理）补人话

---

## 一、读取输入

### 路径 A：本地邮件导出文件（最常见，无需任何连接器）

| 格式 | 读法 |
|---|---|
| `.eml` | 纯文本读取；跳过信头，从第一个空行之后开始当正文。需要 `Subject` / `Date` / `From` / `To` 时再从信头取 |
| `.mbox` | 按 `\nFrom ` 分隔成多封，逐封按 `.eml` 处理 |
| 导出的 `.json` | 先看结构：若是数组，通常每封含 `subject / from / date / text / html`；有 `html` 优先用 `text`，`text` 为空再剥 `html` 标签 |
| `.txt` / `.md` | 直接通读；若含多封，按 `Subject:` / `发件人:` / `日期:` 之类的分隔特征切分 |

**去噪**：忽略 `Received:`、`DKIM-Signature`、`X-*`、`Content-Transfer-Encoding`、base64 附件块、退订链接段落。这些里没有日程信息，读它们只会污染上下文。

### 路径 B：邮箱连接器直读（可选，需环境已配置）

若运行环境有 163 邮箱（netease-mail）连接器：

```bash
cd <connector-netease-mail>
node scripts/imap.bundle.js check --recent 30d --limit 50
```

- `--recent 7d|14d|21d|30d`：取最近 N 天；`--limit N`：单批封数；`--unseen`：只取未读。
- 输出 JSON 数组，每封含 `uid, subject, from, date, text, html, attachments`。

> ⚠️ **两个已验证的坑**
> 1. **路径坑**：git-bash 里把重定向目标写成 `/c/...` 会被解析成 `C:\c\...` 而报「文件不存在」。**必须**用 Windows 风格绝对路径 `C:/Users/.../xxx.json`。
> 2. **限流坑**：网易 IMAP 短时间大量连接/大 `limit` 会临时失败。用**递进窗口 + 小 limit** 分批：`7d→14d→21d→30d`，每批 `limit` 从大到小试（80→50→35→20），成功即停；批次间 `sleep 2`。接口**只支持「取最近 N 封」，不支持翻页**。

### 路径 C：Outlook / 学校邮箱

v1 推荐：在 Outlook 网页版把邮件**转发**到可读取的邮箱，再走路径 A/B 读转发副本。
进阶：自接 Microsoft Graph 连接器（成本高，v1 不推荐）。

---

## 二、机械初抽脚本（可选）

`scripts/extract_schedule.py` 做机械初抽，适合**批量邮件 JSON**场景：

```bash
cd <工作目录，内含 batch_*.json / unseen.json>
python3 <repo>/scripts/extract_schedule.py    # 输出 schedule_raw.json
```

脚本职责（**只做机械部分**）：
- **判定 eventish**：subject/正文含 invitation / event / session / webinar / workshop / talk / career day / info session / reception 等强事件词；已排除纯营销/政策/系统欢迎邮件。
- **日期解析**：`yyyy-mm-dd` / `yyyy年m月d日` / `Mon dd, yyyy` / `dd Mon yyyy` / 无年份 `Mon dd`、`dd Mon`（用今年）/ `m月d日`。⚠️ 不要把 `Sep 2026` 当成「日=20」。
- **时间解析**：`5:00 p.m.` 必须保留 am/pm；区间 `1:30 - 3:00pm` → `start=13:30, end=15:00`。
- **配对**：标题含日期 → 以标题日期为准，时间取其后/正文该日期最近出现的时间。
- **去重**：按「标题+日期+时间」。
- 输出契约 v5：`generatedAt`、`source`、`items[]`；抽不到就**整个省略**字段。

> 脚本只给机械字段。**人话部分必须由你补**（见下）。

---

## 三、你必须补的部分（脚本/机械抽取做不到）

- `summary`：**这是什么 + 要我做什么**（例：「Citi 2026 职业洞察线上分享，主题 Banking，需提前在 jobs.citi.com 注册」）。不要极端简洁。
- `notes`：易漏提醒（「参加前需注册，链接见原邮件 / 带简历 / 提前 15 分钟」）。
- `priority`（1–4）/ `project`（如 秋招 / 生活 / BA课程）。
- 补 `end`：机械抽取常只有开始时间，按活动类型补常见时长并在 `notes` 注明是估算。

---

## 四、判定与写法速查

| 情形 | type | 时间写法 |
|---|---|---|
| 限期前要交/完成东西 | `ddl` | `dueAt` |
| 无明确时间的待办 | `todo` | 不写任何时间字段 |
| 单次会议/面试/考试/讲座 | `event` | `times:[{date,start,end}]` |
| 一门课每周固定时段 | `event` | `times:[{wday,start,end,from,until}]` |
| 同一件事固定几次（初筛+终面） | `event` | `times:[多个 date 槽，各带 topic]` |
| 纯参考信息 | `archive` | 一般不写时间 |

---

## 五、硬性规则（契约 v5）

1. 不准编造时间。拿不准 → `type:"todo"` 或 `"archive"`，summary 注明「需确认时间」。
2. 不准漏抽明显 ddl；长邮件里「提交截止 / due date / 考试时间 / 会议时间」必抽。
3. 全部香港本地时间，**不带时区后缀**：`datetime=2026-09-10T23:59`、`date=2026-09-10`、`time=23:59`。
4. **只写有值的字段**：没有就整个省略。禁止 `null`、空字符串 `""`、空数组 `[]`。
5. `event` 必有 `times`（≥1 槽）；`ddl` 必有 `dueAt`；`todo` 不写时间字段。
6. 一门课 = 一条记录（每周多节 → 多个 `wday` 槽）；不同交付物 = 多条记录（作业A、作业B 各自截止 → 两条 ddl）。quiz/小测 = 独立条目，不塞进课程 notes。
7. `summary` 与 `notes` 不混写。
8. 输出中文。
9. **`end` 必须晚于 `start`**——前端导入的硬校验，`end=start` 会让该条整条被拒。

---

## 六、导出前自检（必做）

```bash
node scripts/validate-schedule.mjs public/data/schedule.json
```

输出 `✅ 校验通过` 才能交付。校验器覆盖：信封字段、必填四件套、ddl 的 `dueAt`、event 的 `times`、槽的 `wday/date` 恰好其一、`end > start`、时间格式、残留空值、旧版契约字段（`startAt`/`confirmed`/`recurrence`）。

> 注意：`wday` 周槽本来就没有 `date` 字段，自检时不要把它当缺失报错。
