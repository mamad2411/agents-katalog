---
name: log-driven-defect-triage
description: 用户贴来一段日志/报错（含 traceback、行号、或"明明报错了为什么还说一切正常"这类矛盾）时，把日志还原成可复现的证据、定位根因、并顺着"那句总结到底在测哪个轴"挖出被掩盖的故障。也覆盖**没有日志**的情形：用户只说"XX 不成功""指定目录没用""这两个不能一起用了吗"——此时靠一次跑完全部输入组合 + 找两套判据的不一致来定位。还覆盖**只有性能症状**的情形（"这个动作卡我一会""跑得特别慢""日志里连续几条一样的耗时行"）——此时优先数"贵原语被调了几次"，并用 A/B 对照 + 产物 diff 出证据。当用户粘贴日志、贴 traceback、说"跑完提示成功但数据不对/少了"、"这个错以前没有"、"我操作了但没生效"、"卡我一会/太慢了"时使用。也覆盖"报错指着一堆文件、但真凶只有一个"（级联错误）与"命令明明失败却报 EXIT=0"（退出码被管道吃掉）这两类假象。
agent_created: true
task_type: dev.log_driven_defect_triage
---

# 日志驱动排障

用户贴一段日志给你，你要交付的不是"我看到了这个错"，而是**能复现的证据 + 根因 +
为什么监控没拦住它**。四步，每步都要留下可核对的产物。

## 入口分流：有日志 / 没日志

两者方法论不同，先分清：

- **有日志** → 走下面的第 0–4 步（从原文还原证据）。
- **没日志，用户只说"XX 不成功""指定目录没用""这两个不能一起用了吗"** →
  走【入口 B】。要点是：**先别改代码，先把"不成功"变成一条可复现的判定结论。**

## 入口 B：只有一句"XX 不成功"

用户报的"不成功"绝大多数不是"功能不存在"，而是**某个校验逻辑主动拒绝了它**。
定位三步：

**B1. 一次跑完全部输入组合，不要一个一个试。**
写一个探测脚本，把"用户可能选的每一种输入"都过一遍真实的判定函数，
打印每种的 `(中间判据, 最终结论, 报错原文)`。实测价值极大：一次就看出
"选 A 层成功、选 B 层失败"这种规律，而没有脚本时你会来回试五六轮。

```python
# temp/_probe.py —— 入口处必须带 if __name__ == '__main__'，且加 freeze_support()
# ⚠️ 探针要调的函数若内部用 ProcessPoolExecutor，Windows 是 spawn：子进程会
#    **重新导入主模块**，顶层代码会在每个子进程里再跑一遍（递归放大）。
#    症状：几分钟跑不完 + 日志暴涨 + 多个进程各占 1GB，而正确的探针只要十几秒。
for label, path in CANDIDATES:          # 含"正确的那个"和"用户实际用的那个"
    print(label, path)
    print('  exists=', os.path.isdir(path), 'intermediate=', 中间判据函数(path))
    try:
        print('  OK ->', 最终判定函数(path))
    except ValueError as e:
        print('  FAIL:', str(e).splitlines()[0])
```

**B2. 反直觉现象 = 该模块内部有两套判据。**
如果"同一个目标的上一层成功、下一层失败"（或反过来），几乎一定说明代码里
**并排存在两套独立的判定路径**，各自只看局部特征。本例：
`normalize_account_dir` 先看顶层文件名（失败），再 `find_db_storage` 逐层下钻（成功）
—— 两条路结果不一致，才会出现"选深一层死、选浅一层活"。
看到这种不对称，直接去读**两套路径各自的判据**，不要在报错文案上找答案。

**B3. 把判据集合与项目内其它模块的记述对照。**
这是最常见的根因：**同一个事实被两个模块各自维护了一份，且不一致**。
本例 `account_layout._V3_FIXED_NAMES` 把 `Audio2Text.db` 当 v3 独有特征，
而 `versions/recipe.py` 的 `db_layout` 早写明"4.x 的 db_storage 根下也有它"
—— 两处记述冲突 → 该文件同时命中两代特征 → 判定返回 None → 拒绝。
**Grep 那个特征名/常量，看它在全仓库里有几种说法**；不一致处就是 bug。

最后判一句：**这个 bug 是偶发还是必然？** 若触发条件由程序自己稳定产生
（本例 v4 读侧每次打开目录都会建那个文件），就是**必然复现**——
那么"用户偶尔遇到"的定性是错的，得按"每个同类目录都中招"来评估影响面。

## 第 0 步：先量日志本身，别急着读

```bash
f="<日志路径>"; wc -l "$f"; ls -la "$f"
awk '{print length"\t"NR}' "$f" | sort -rn | head -20    # 最长行是谁
grep -oP '\[\w+\]' "$f" | sort | uniq -c | sort -rn      # 级别分布
```

**最长行是个信号**。实测：一份 546 行 / 301KB 的日志里有**一条 165591 字符的行**
（某个库把 16 万字符的正文整段写进 `logger.debug`）。这种日志 `grep`、diff、
编辑器全卡死，真正的错误被埋掉。看到这个要先怀疑"日志本身有毛病"，
并把"落盘前截断"列进修复清单。

## 第 1 步：从日志还原 payload，而不是凭猜

日志里的 XML/JSON 通常被缩进过、被 logger 前缀切过。写脚本抽出来：

```python
lines = io.open(LOG, encoding='utf-8').read().split('\n')
start = next(j for j in range(i+1, i+20) if lines[j].strip() == '<msg>')
payload = []
for j in range(start, start+200):
    if lines[j].strip() == '</msg>':
        payload.append(lines[j]); break
    payload.append(lines[j])
raw = '\n'.join(payload)
raw = '\n'.join(l[4:] if l.startswith('    ') else l for l in raw.split('\n'))  # 还原缩进
```

**逐字对齐报错行号**——这是最有力的证据。真机日志报 `line 43, column 12`，
重建出来的 payload 第 43 行正好是 `<content><?xml version="1.0"?>`，
故障就被钉死了。（列号常有几列偏差，以**行号**为准。）

## 第 2 步：拿真机原文过真函数，跑修复前/后对照

不要只 `xmltodict.parse()` 一下就算验证——那绕过了业务分支。直接调被报错的那个函数：

```python
from pkg.module import the_failing_func
print(the_failing_func(payload))     # 修复前： {'text': '发生错误', ...}
```

秒级、无需真机。**修复前的输出要抄进提交信息**（"修复前返回 X，修复后返回 Y"），
这是唯一能证明你真修好了的东西。

## 第 3 步：版本归因不要靠"感觉"

用户说"以前 v3 没问题"时，用证据回答，别顺着说也别硬顶：

```bash
git log -S '<出错的关键字>' --oneline              # 这个逻辑是谁哪版引进的
grep -o 'ExpatError: .*' logs/<更早的日期>-log.log | sort | uniq -c
```

实测结论常常是"**跟版本无关，是老 bug**，只是以前被别的 ERROR 刷屏淹掉了"。
这个结论比"是 v4 的锅"有价值得多，因为它意味着**所有历史数据都受影响**。

## 第 4 步：看到"一切正常"的总结，问它测的是哪个轴

这是最容易漏的一步，也是最值钱的。用户常常问："日志里明明报错了，
为什么最后还打印『未发现未支持的消息格式』？"

做法：去读那句总结的**判据**，然后对着实际故障看它能不能察觉到。

实测套路（三个独立坑叠在一句话里）：
1. **判据太窄**：总结只检查"这个类型有没有注册/有没有工厂"，
   **从不检查工厂内部解析成功了没有**。两个正交的轴被一句话糊在一起。
2. **根本没接上**：那句总结的数据来源只在 A 版本里被填充，B 版本压根没调用，
   于是 `if not 数据: 打印('未发现...')` **无条件**执行。
   验证：`grep -c '未发现' log` vs `grep -c '共发现' log` —— 841 : 0 就露馅了。
3. **缺少单条隔离**：A 版本有 `try/except → '已跳过'`，B 版本没有，
   一条坏数据中断整批，日志里连"跳过"的痕迹都没有
   （`grep -c '已跳过' log` 全天 0 次 = 可疑）。

**修法**：让汇总**任何情况下都报两个数字**（覆盖面 + 内容解析失败条数）。
省掉第二个数字，就等于把那句误导人的话再说一遍。

### ① 报错指向的不是真凶 —— 去**完整**日志取第一条

编译器 / 引擎 / 框架会把**一个**根错误放大成一串后继错误，而且**后缀错误的信息更具体、
更误导**：它会反复念被牵连者的名字，把你的注意力引到那里，真凶反而没被点名。

**判据**：不要追消息里出现的名字（那是受害者）；按时间顺序取**第一条** error。

实测（Godot 4.7，2026-10-05）：

```
# 第 8 行 —— 真因，唯一提到真实语法问题的一条
SCRIPT ERROR: Parse Error: Signal parameters cannot have a default value.
ERROR: Failed to load script "res://autoload/signals.gd"

# 之后每个引用方的报错 —— 全是噪声，指向"引用者"而不是 signals.gd 本身
SCRIPT ERROR: Parse Error: Could not parse global class "SignalBus" from "res://autoload/signals.gd"
```

四个测试脚本各报一次 `Could not parse global class "SignalBus"`，看上去像四个独立故障；
实际只有一条根因。**若追着这条噪声走，会去改 4 个测试文件**。

⚠️ 连带教训：我最初只看了 `tail -20`，而真错误在第 8 行 —— **首错通常在日志最前面**。
`grep -n -i "error\|Parse" <完整日志>` 永远比 `tail` 可靠。

### ② `echo $?` 之前插了管道 —— 你量的是管道的尾巴

```bash
cmd | tail -8; echo "EXIT=$?"     # ❌ EXIT 是 tail 的，cmd 失败也报 0
cmd > /tmp/out.txt 2>&1; echo "EXIT=$?"   # ✅ 再 grep /tmp/out.txt
```

**判据**：`echo $?` 与被执行命令之间只要隔了任何一个 `|`，这个退出码就与被测命令无关。
本项目测试脚本用 `quit(1)` 表意失败 —— 一旦被管道吃掉，**"有失败"会被读成"全绿"**。

## 第 5 步：症状是"慢 / 重复 / 莫名"，而不是报错 —— 先加分步毫秒日志

有一类问题**不报错、不改行为**，靠读代码几乎找不到（两处调用还隔着两个文件）：
启动慢、某动作被执行了两遍、UI 勾选莫名消失。

做法：**先给启动/主流程每一步打一条日志，且必须带累计毫秒**，再跑一次。

实测（wechatDecode 2026-09-20）：打点后立刻看出 `ctx.load()` 与 `theme.apply()`
各跑了两遍（一处入口、一处主窗口里），主窗口就绪 810ms → 修完 229ms。
危害也不只是慢：

- 重复"加载配置"会**重建对象**，页面上已持有的旧引用静默失效（`is` 比较失败，
  但字段都还在，看不出来）。
- 重复"应用样式/主题"会让 Qt 把所有控件样式重算一遍（含字体重新解析），
  顺带刷出一堆字体噪音日志。

**修法优先做幂等，而不是删掉那处调用**：删调用依赖"只有 A 会构造 B"这类
现在成立、以后未必成立的前提。记下已应用的签名（如 `(主题名, QSS)`），
内容没变就跳过；需要真重读时留 `force=True` 参数。
注意按**内容**判断，A→B→A 回到 A 仍要重新应用。

补一条守卫测试：断言"第二次调用必须真的什么都不做"，而不是"调用不报错"。

## 第 6 步：GUI 噪音日志排查 —— 别用 offscreen 当对照

Qt/PySide6 的 `DirectWrite: CreateFontFaceFromHDC() failed`、
`OpenType support missing for "...", script 20` 这类噪音，
在 `QT_QPA_PLATFORM=offscreen` 下**完全不复现**（不走 DirectWrite，
也不会改控制台代码页）。要定位必须**真实平台**跑一遍。

可复用套路：patch 掉 `QApplication.exec`，让程序自动退出，好无人值守地跑完整启动：

```python
original_exec = QApplication.exec
def auto_quit_exec(*args, **kwargs):
    QTimer.singleShot(600, lambda: QApplication.instance().quit())
    return original_exec()          # ⚠️ 原始槽不收参数，别透传 args
QApplication.exec = auto_quit_exec
```

两个坑：补丁函数必须收 `*args`（`def f(self)` 会被 descriptor 再绑一次 self）；
且**不能**把 args 传给原始 exec，否则
`TypeError: QApplication.exec() takes no arguments (1 given)`。

同类还有 **Windows 控制台中文乱码**：Qt 的 windows 插件把控制台代码页改成
65001(UTF-8)，而 Python 的 `sys.stdout/stderr` 早在解释器启动时按 locale（cp936）
定了编码 → 中文以 GBK 字节写进 UTF-8 控制台。**Qt 自己的报错也会一起乱码**，
用户贴过来的日志里出现这种乱码，就是同一个根因，别当成"编码无关的显示问题"。

## 第 7 步：优化"没生效"——先确认线上走的是哪条分支

症状：代码看对了、测试过了、也推了，但用户那边的现象**一点没变**。
最可能的根因不是优化写错，而是**优化写在了不执行的那条分支上**。

实测（wechatDecode 2026-09-20）：把缓存构建从 95 分钟优化到 4.4 分钟、推了 commit，
用户再跑仍然慢得跑不完。因为入口 `CacheDB.update()` 先判 `is_built()`：

```
is_built() == True  →  _build_incremental()   ← 线上走这条（meta 里有 last_build）
is_built() == False →  _build_full()          ← 优化全写在这里
```

两条分支的耗时结构完全不同（全量按联系人全跑；增量要先逐会话判断有没有新消息），
优化只覆盖一条时，另一条的表现**与优化前一模一样**。

排查动作，按顺序：

1. **找"单一入口 + 多条分支"的地方**，先确定命中的是哪条——读它的判据
   （配置项 / 状态字段 / `meta` 表里的标记），而不是读代码猜。
   本例 `sqlite3` 只读打开缓存库、`SELECT key, value FROM meta` 就一眼看到
   `last_build = 2026-09-05`。
2. **探针必须复刻真实入口**，直接调"我以为会走"的内部函数是**假验证**：
   它跳过了分支选择。本例探针直接调 `_process_contact_full(传 global_stats)`，
   测出 0.24 s/个；真机 8 s/个——**30 倍差距全在"走哪条路"上**。
3. **给入口补一条"走哪条路"的日志**（成本几行）：两条分支耗时结构不同，
   日志里看不出走的哪条时，"为什么慢"只能靠时间账反推。
4. **时间账反推法**：拿日志里已知的段落耗时去减，能证明某段**不可能被执行**。
   本例：`解密完成 → 第一条消息处理` 只隔 8.3 秒，而
   `get_contacts 1.05s + 预扫描 5.58s + 全局聚合 7.24s = 13.9s` 装不下 → 全局聚合没跑。
   这是**不用改代码就能拿到**的强证据，优先找。

修完必须做**变异验证**（否则"测试通过"只证明测试跑得起来）：
把修复逆向注入，测试必须变红。本例两条变异分别红 1 条、红 3 条：

```python
# 变异 1：删掉"没变化就跳过"的 continue       → 1 条测试转红
# 变异 2：把 `if known_count is None` 置为恒真 → 3 条测试转红
```

⚠️ 注入变异时**别用 heredoc 里的 assert 做确认**：命令被重试时会跑第二遍，
第二遍必然 assert 失败（文件已被第一遍改过），报错信息会让人误判成"没改成功"。
改用 Edit 工具做变异与恢复，或先 `cp` 备份再核对内容。

## 第 8 步：同一次操作里"同一份数据被反复拉取"——去数调用次数，别读代码

症状：用户说"这个动作卡我一会"，日志里**连续出现几条一模一样的耗时行**，且
**条数完全相同**：

```
19:26:57 开始获取聊天记录
19:27:05 获取聊天记录耗时：7.84s/206186条消息
19:27:06 开始获取聊天记录          ← 同一个数
19:27:14 获取聊天记录耗时：7.76s/206186条消息
19:27:14 开始获取聊天记录          ← 又一次
19:27:23 获取聊天记录耗时：8.86s/206186条消息
```

**"耗时相近 + 条数一字不差"就是同一份数据被取了三遍**（不同聊天不可能条数撞上）。
第一时间判据：拿日志里的条数去数据库 `SELECT count(*)` 对一下，能对上就不是"三次不同的查询"。

根因几乎总是这一种：**计算入口与它的取数函数没有缓存**，而入口内部把同一份数据
当参数调了好几处辅助统计。本例 `AnalysisReport.generate()`：

```python
messages  = self.statistics._get_messages(chat_id, time_range)   # 1
time_span = self.statistics.get_time_span(chat_id, time_range)   # 2 —— 内部又 _get_messages
type_dist = self.statistics.get_count_by_type(chat_id, time_range) # 3 —— 又一次
```

`_get_messages()` 本身是**全量拉取 + 解析**（真机 20.6 万条 ≈ 8s），所以白花 16s。
同一模式还有 `get_overview()` 4 次、另一条回退路径 7 次。

排查动作：

1. **先数、不先猜**：把那个贵原语（`get_messages`）包一层计数器再跑一次，
   打印被调了几次、参数是什么。比读调用链快且不会漏。
2. **修法选"记忆化"，不要选"少调几次"**：在数据持有者（这里是 `MessageStatistics`
   实例）上按 `(标识, 时间范围)` 缓存，**返回列表副本**（防调用方就地排序污染）。
   缓存键必须含**时间范围**，否则跨范围会串味 —— 这是本类修复最容易埋的坑，
   要有专门用例钉住"不同范围必须重新取数"。
3. **别把"不同范围"也算进重复**：`get_recent_counts` 的 day/week/month/year 是
   4 个不同查询、SQL 带时间过滤、返回量很小，**不该**被合并。写断言时要按
   "`time_range is None` 的那次只发生一次"来写，而不是"总次数 == 1"，
   否则测试会把正常行为当 bug。

**性能修复的证据形态：A/B 对照 + 产物 diff**（比"变快了"强得多）。
在**同一次会话里**把修复关掉再跑一遍，模拟修复前：

```python
class _NoCache(dict):                 # 让缓存永远 miss
    def get(self, k, d=None): return None
    def __setitem__(self, k, v): pass

report = AnalysisReport(database=db)
stats = report.statistics             # 先触发实例化
if disable_cache:
    stats._messages_cache = _NoCache()
```

实测输出（真机 20.6 万条单群）：

```
修复前  取数次数=3  耗时=31.5s  报告=4134 字节
修复后  取数次数=1  耗时=12.3s  报告=4134 字节
```

然后 `diff <(grep -v 生成时间 A) <(grep -v 生成时间 B)` —— **逐字一致**才说明
这次只省时间、没改行为；顺带还能和用户手上那份产物对撞，确认结论落在同一版本上。

## 可迁移的三条纪律

- **回归指标要测最终产物，不要测前缀字段。** 本项目踩过：指标测的是
  `title`/`desc` 非空，而真正坏的是 `messages` 条数 = 0 —— 指标全绿，
  数据一条没出来。
- **修在一个咽喉，不要补 N 个点。** 把清洗逻辑放进被所有路径共用的那个函数，
  而不是在每个调用点各写一遍 `try/except`。写完加 **AST 守卫测试**，
  禁止那种"省事写法"复活：
  ```python
  for node in ast.walk(ast.parse(src)):
      if isinstance(node, ast.Call) and <是那个坏写法>:
          offenders.append(node.lineno)
  assert not offenders, '请改用 util.common.sanitize_xml'
  ```
- **私人数据不许进 ERROR 日志。** 原文（聊天记录、邮件、身份证）降级到 DEBUG 且
  **截断**，ERROR 只留一行摘要 + 定位字段：
  ```python
  logger.error('X 解析失败（原始 XML 见 DEBUG 日志，最多 %d 字符）', LIMIT)
  logger.debug('原始 XML：%s', _xml_preview(xml))
  ```

## 收尾必做

- 修复前后对照写进 commit message（含真机原文规模、条数、行号）。
- 把"这个坑"写进项目自己的踩坑文档/记忆，而不是只留在对话里。
- 顺手修正**记忆里关于成本的错误档位**：如果这次实测某个"秒级"脚本其实跑了
  2 分 17 秒，就去把那条记忆改掉，否则下次还会误判。
