---
name: weread2brief
description: 把关注的微信公众号做成「每天早上的一页纸」。走微信读书书架路线读取最近 2 天文章全文（读取当前账号在阅读器内可见的正文），按 URL/标题+日期去重归档为 Markdown，再由 agent 生成分号汇总的每日简报，可选同步到 ima 等知识库。触发词：公众号简报、公众号每日线索、订阅号日报、书架抓取、weread 公众号、每日简报、把公众号读成一页纸。
---

# weread2brief · 公众号每日简报

**一句话**：一次扫码，每天早上把你关注的公众号读成一页纸。

**核心路线**：微信读书书架 → 号内目录 → 最近 2 天 → 内联 iframe 抽全文 → 去重归档 → 生成简报。
不走 mp.weixin.qq.com 直爬（反爬严格、受限内容取不到正文），也不依赖 RSS（源经常挂）。

---

## 一、前置检查（缺一不可，先跑一遍再动手）

| 检查项 | 怎么查 | 不通过怎么办 |
|---|---|---|
| Chrome 已安装 | 常见路径 `/Applications/Google Chrome.app/...`、`C:\Program Files\Google\Chrome\Application\chrome.exe`、`/usr/bin/google-chrome` | 让用户装 Chrome，或设 `CHROME_EXE` |
| `agent-browser` 可用 | 脚本会自动探测；也可用 `AGENT_BROWSER_EXE` 指定 | 报错则当前环境缺这个 CLI，改用 Playwright 版脚本 |
| 持久 profile 存在 | `--profile` 指向的 user-data-dir（默认 `~/.weread2brief/profile`） | 首次运行自动创建，需用户扫码 |
| 登录态有效 | 连 CDP 后 `cookies get` 输出含 **`wr_vid`** | 走「登录续期」流程 |
| 目标账号清单 | `<WORKSPACE>/targets.txt`，一行一个 | 用 `assets/targets.example.txt` 复制 |
| **号已在书架** | 打开「书架」能看到该号，点进去有文章列表 | **硬前提**：让用户先在微信读书搜索该号 → 切「公众号」→「加入书架」。工具只读书架，不代为关注 |
| Python 3.10+ | `python -V` | 用环境自带 managed python |

**跑任何命令前先清代理**（否则 CDP 连 127.0.0.1 会被本机代理撞成 502）：

```bash
export HTTP_PROXY="" HTTPS_PROXY="" ALL_PROXY="" NO_PROXY="127.0.0.1,localhost"
```

Windows PowerShell：

```powershell
$env:HTTP_PROXY=""; $env:HTTPS_PROXY=""; $env:ALL_PROXY=""; $env:NO_PROXY="127.0.0.1,localhost"
```

---

## 二、首次配置（init）

用户第一次使用时，按顺序做这四件事，**每一步都要确认结果再往下**：

**第 0 步（人工，做一次；不通过就别往下走）**：目标公众号必须已经在用户的微信读书书架里。

告诉用户：微信读书搜索框输入号名 → 切「**公众号**」分类 → 进号主页点「**加入书架**」（或「关注」）。
判据不是"用户说加了"，而是**书架里点开该号能看到最近几天的文章标题**。
缺这一步，后面所有环节都会以 `NOT ON SHELF` 结束——那不是 bug，是前置条件没做。

1. **建工作区**

   ```
   <WORKSPACE>/                 # 归档根，例如 ~/weread2brief
   ├── <账号A>/                 # 每号一个目录，md 落这里
   ├── <账号B>/
   ├── targets.txt              # 目标账号清单
   └── config.toml              # 配置
   ```

2. **写 targets.txt**
   一行一个公众号名，**必须与微信读书书架里显示的名称完全一致**（含空格和标点）。
   **前提是这些号已经在书架里**（见第 0 步）；不在书架的号写进来也只会得到 `NOT ON SHELF`。
   首次建议只填 1–2 个号，跑通再加。

3. **起 Chrome + 扫码**
   用独立 user-data-dir 起 Chrome，带 `--remote-debugging-port=9222`，打开 `https://weread.qq.com/`，
   然后**请用户在本机扫码登录**（自动化无法代做）。
   登录成功判据：cookie 里出现 `wr_vid`。

   > ⚠️ `wr_vid` 是 **session cookie**，不落盘。**不要强杀 Chrome**（`kill -9` / `taskkill /F` /
   > 宿主的"停止任务"），否则要重新扫码。详见 `references/pitfalls.md` 第 15 条。

   **进程会被回收的宿主**（agent 的浏览器活不过本轮对话，扫码还没扫它就没了）：
   不要硬起，直接把续期脚本交给用户手动运行：

   ```bash
   # Windows
   scripts\relogin.cmd  [PROFILE_DIR] [PORT]
   # macOS / Linux
   ./scripts/relogin.sh [PROFILE_DIR] [PORT]
   ```

   两个脚本都已把"别强杀"的告示打进窗口里。用户回来说扫好了，再用 CDP 验证 `wr_vid`。

4. **验证登录并记录**
   成功后写 `<WORKSPACE>/.login_state.json`：

   ```json
   {"last_success": "YYYY-MM-DD"}
   ```

   这个文件用于后续「登录即将过期」预警。

---

## 三、日常运行（run）

**必须后台运行**（耗时 5–13 分钟，前台会被超时掐断）。

```bash
python scripts/scrape_archive.py --workspace "<WORKSPACE>" --profile "<PROFILE_DIR>"
```

常用参数（都给默认值，平时只传 `--workspace`）：

| 参数 | 默认 | 说明 |
|---|---|---|
| `--workspace` | `~/weread2brief` | 归档根目录，md 与 JSON 都落这里 |
| `--profile` | `~/.weread2brief/profile` | Chrome user-data-dir，登录态存这里 |
| `--config` | `<workspace>/config.toml` | 配置文件 |
| `--accounts` | `<workspace>/targets.txt` | 账号清单 |
| `--days` | `2` | 窗口天数，2 = 今天+昨天 |
| `--port` | `9222` | CDP 端口 |

退出码：`0` 正常 · `2` 需要登录 · `3` 环境不满足 · `130` 被中断。

**绝不强杀这个进程**，也别在它跑到一半时"停止任务"——那会连坐它启动的 Chrome，把 `wr_vid` 一起弄丢。

脚本行为：

```
确保 Chrome(CDP 9222) 起来
  → 打开 weread 根域 → 校验 wr_vid
  → 跳 /web/shelf → 扫书架 → 与 targets 匹配（先精确后模糊）
  → 逐号：进目录 → 解析"今天/昨天/3小时前" → 筛最近 2 天
  → 逐篇：点标题 → 从内联 iframe 抽 #js_content + og:url
  → 去重（URL ｜ 标题+日期）→ 落 md
  → 输出 articles_shelf_2d.json + 文章列表 md
```

**跑完必须读日志**，不要只看退出码：

```bash
tail -30 scrape_archive.log
```

判定标准：

| 日志特征 | 含义 | 处理 |
|---|---|---|
| `=== done ===` 且无 `NEED LOGIN` | 正常完成 | 继续生成简报 |
| 出现 `NEED LOGIN` | 登录态失效 | **终止，不生成简报**，走续期流程 |
| 某号 `catalog items: 0` 且重试无效 | 可能是验证码没解掉 | 查 `CAPTCHA` 相关日志 |
| `SHELF-EXTRA(...)` | 书架有号但不在 targets | 提示用户是否补进清单 |
| `NOT ON SHELF: ...` | targets 里的号不在书架 | 提示用户核对名称 |

正常跑完后立刻更新登录状态：

```json
{"last_success": "YYYY-MM-DD"}
```

### 3.1 脚本模块

五个 Python 文件职责单一，**改版时先看 `page_selectors.py`**：

| 文件 | 职责 |
|---|---|
| `scripts/scrape_archive.py` | 主流程（书架→目录→正文→归档），CLI 入口 |
| `scripts/captcha_solve.py` | 验证码三后端求解，可单独跑：`--backend human\|agent\|vlm` |
| `scripts/browser.py` | Chrome / agent-browser 定位、CDP 管理、坐标点击 |
| `scripts/config.py` | 配置解析（CLI > 环境变量 > toml > 默认），零第三方依赖 |
| `scripts/page_selectors.py` | 全部 DOM 选择器与 JS 片段 —— **平台改版唯一需要改的文件** |

另有两个**给用户手动运行**的扫码续期脚本（agent 起不了长驻浏览器时用）：
`scripts/relogin.cmd`（Windows，纯 ASCII + CRLF）、`scripts/relogin.sh`（macOS / Linux）。

---

## 四、关键机制（为什么必须这么写）

### 4.1 时间窗口：今天 + 昨天，不含前天

**不要用 `timedelta.days` 做日期比较**（`1.69 天` 会被截断成 `1`，把前天晚间文混进来）。正确写法：

```python
dt.date() >= (now - timedelta(days=1)).date() and dt <= now
```

目录时间是相对标签，必须解析：`刚刚 / N分钟前 / N小时前 / 今天 HH:MM / 昨天 HH:MM / M月D日`。
**解析失败要报警，不要当作"不在窗口"静默丢弃**——这两者混在一起就是静默漏抓的根源。

### 4.2 去重：双键

```
键1 = 来源URL（优先）
键2 = (标准化标题, 日期)
```

只按标题去重会误杀每日同名的固定栏目（如每天一篇《复盘》）。同一篇内容换 URL 转载时，键2 兜底。

### 4.3 验证码（这是本 skill 的核心特色）

weread 在**新起 Chrome 后首次打开公众号阅读页**会弹 TCaptcha 图片点选：

- 弹窗 iframe：`#tcaptcha_iframe_dy`，源自 `captcha.gtimg.com`
- 6 张图其实是**一整张拼图背景**（`.tc-imgarea`），不是 6 个独立元素 → **只能按坐标点选**
- 弹窗约 1–2 分钟不处理会自行消失，但页面**停在死页**，必须重新导航
- 通过后会**链式下发**第 2、3 轮（"选择所有…""包含文字…"），必须循环处理

**三种求解后端**（`config.toml` 的 `[captcha] backend`）：

| 后端 | 依赖 | 适合谁 | 可靠性 |
|---|---|---|---|
| `human` | 无 | 第一次跑、或没有视觉模型 | **最可靠**，人眼永远比模型准 |
| `agent` | 外部 agent 判图 | Claude Code / CodeBuddy / WorkBuddy 等 skill 场景 | 高 |
| `vlm` | 一个 OpenAI 兼容视觉 API Key | 全自动无人值守 | 中（多阶段题面容易翻车） |

**`agent` 后端的闭环（这是 skill 相对纯 CLI 的最大优势）**：

```
1. 检测到弹窗 → 截图到 <WORKSPACE>/.captcha/captcha.png
2. 读 <WORKSPACE>/.captcha/prompt.txt（题干；读不到就直接看图）
3. agent 看图 → 得出点击位置
4. 写 <WORKSPACE>/.captcha/click.json        ← 路径必须准确，写错目录就白等
5. 脚本按坐标点选 → 校验放行
6. 放行判据 = 目录项 > 0（不是"弹窗消失"）
7. 重复 1–6，最多 max_stages(4) 轮
```

**`click.json` 协议**——主协议是**相对 iframe 的比例坐标**，与分辨率、缩放、滚动都无关：

```json
{"points": [[0.50, 0.62], [0.50, 0.88]]}
```

含义：先点验证码框内 (50%, 62%)，再点 (50%, 88%)。**最后一点通常就是「确定」按钮**。
你只需要看图说"在这个框的中间偏下"，不用算像素、不用管设备像素比。

也兼容宫格写法（3 列 × 2 行，0 基）：

```json
{"cells": [[1, 1]]}        // 或 {"row": 1, "col": 1}
```

> 宫格要换算成坐标，依赖 `scripts/page_selectors.py` 里的 `CAPTCHA_IMAGE_AREA_RECT`（经验矩形）。
> **点偏了不用改它**，换 `points` 协议即可——精度完全由看图决定。

> ⚠️ 判图必须"截图 → 立刻看 → 立刻写"闭环。等待窗口建议 ≥300s，180s 太紧（多阶段链式已常态化）。

### 4.4 登录态管理

- 登录由 weread cookie 维持，**一次扫码通常可用数周**，具体有效期不确定
- 以 **21 天**作为安全线预警：超过就在简报和回复里提示"建议近期扫码续期"
- `NEED LOGIN` 时**绝不生成伪简报、绝不拿旧文冒充**——这一点写进产出说明里

### 4.5 幂等闸（防止同日重复触发白跑）

若当天简报已存在、mtime 在 6 小时内、且 `articles_shelf_2d.json` 的 `extracted_at` 是今天
→ 判定为重复触发：**只做只读校验，跳过采集与重写**，必要时补做同步。

---

## 五、简报生成规范

输入**只看** `articles_shelf_2d.json` 里的窗口文章集合，需要正文再定点读对应 md。
**不要**拿历史归档目录重排——旧文会泄漏进当天简报。

### 5.1 结构铁律

```
标题：每日简报 · YYYY-MM-DD
  ↓
速览（≤3 行纯文本）：本期 N 篇 · 新归档 X / 去重跳过 Y · 登录态有效/失效
  ↓
一、逐号线索          ← 正文主体，必须是第一个章节
二、跨号共振
三、待跟踪清单
四、技术状态（本期修了 bug 才写）
五、覆盖说明表        ← 必须排在正文之后
六、采集实况明细      ← 同样后置
结尾声明
```

**严禁在正文之前插入任何表格。** 读者要的是结论，不是你的采集口径。

### 5.2 逐号小节格式

```markdown
### N. 账号名 —《标题》（YYYY-MM-DD）

🔗 [原文](URL)

- 要点1
- 要点2

**可交易映射 / 关键影响**
| 方向 | 标的或板块 | 逻辑 |
```

日期**必须取自归档文件名 `YYYY-MM-DD_` 前缀或 md 内的日期字段**，禁止凭猜测、禁止照抄简报日期。
每节必须有可点击原文链接；拿不到就写"原文链接未获取到"。

### 5.3 可信度标注

| 来源 | 标法 |
|---|---|
| mp.weixin.qq.com 原文直链 + 后台接口 | 最高 |
| mp 原文直链 + weread 内联渲染 | 高（非后台接口，不标最高） |
| 镜像站 / 备份站 | 中，并注明"非微信原文直链" |
| 纯观点文、无硬数据 | 中 |

---

## 六、同步到知识库（可选）

如果用户配置了 sink（ima / Notion / Obsidian），流程是：

```
量文件字节数 → create_media(file_size 必须等于实际字节)
  → 拿上传凭证 → 上传对象存储
  → add_knowledge(带 folder_id)
  → 回查确认解析完成
```

**三个必须做的校验**：

1. `file_size` 必须等于 `wc -c` 的实际值（量完不要再改文件）
2. 上传后 `etag` 必须等于本地 `md5sum`（逐字节一致才叫传成功）
3. 入库后回查标题在列且解析完成（`media_state=2 / progress=100`）；卡在解析中超过 2 分钟就如实报告，**不要死循环轮询**

同步失败**不要中止任务**：本地简报照常交付，如实说明"同步未完成 + 原因"。

---

## 七、失败处理（最重要的一节）

### 绝对禁止

- ❌ 拿昨天的文章冒充今天的
- ❌ 登录失效还生成一份"看起来正常"的简报
- ❌ 编造 URL 或数据
- ❌ 某个号抓不到就静默跳过（必须写进"未获取到新文"名单）

### 必须如实标注

| 情况 | 标注文案 |
|---|---|
| 某号近 2 天没发文 | 「近 2 天零更新」 |
| 某号不在书架 | 「书架未关注」 |
| 目录渲染失败 | 「目录渲染失败（疑似验证码/改版）」 |
| 登录失效 | 「登录态已失效（距上次成功 N 天），需扫码续期」 |
| 正文只有"回复关键词" | 「后台回复型存根，正文不在阅读器内」 |

---

## 八、交付前自检（每次都要跑）

```bash
# 1. 字节数与修改时间
ls -la --time-style=+%H:%M:%S "<BRIEF>"

# 2. 章节顺序（应为一/二/三/四 → 五 → 六）
grep -n '^## ' "<BRIEF>"

# 3. 每个小节标题是否都带日期
grep -n '^### ' "<BRIEF>"
```

再用脚本（**不要用 grep**）校验转义污染：

```python
t = open(BRIEF, encoding="utf-8").read()
print("backslash-amp:", t.count(chr(92) + "&"))
print("backslash-pipe:", t.count(chr(92) + "|"))
```

> 写完重要文件后**隔 20–30 秒复查一次**字节数与 mtime。
> 如果字节数变大且出现「表格列宽被自动对齐」「`&` 变成 `\&`」——那是本机编辑器旧缓冲整份回写，重写文件并提醒用户关闭那个窗口。

---

## 九、故障速查

| 现象 | 最可能原因 | 处置 |
|---|---|---|
| 整号 `catalog items: 0`，无报错 | 验证码残留帧（`-9999`）被误判为"弹窗还在" | 可见性判据加 `left > -1000 && top > -1000` |
| 目录恒 0，重试三次无效 | 验证码链式未解完 | 循环处理最多 4 个 stage |
| 解完验证码仍 0 | 通过后页面停在死壳，未重新导航 | 求解后 `location.href` 重载 |
| 归档只有几十字 | iframe 渲染竞态，正文没铺完 | 脚本已做「字数下限 + 重试取最长」，仍不足会标 `extract_incomplete` |
| 报 `NEED LOGIN` 但浏览器是登录的 | 工具路径解析失败被当成未登录 | 检查 `except` 是否吞掉了 `FileNotFoundError` |
| 日志停在 `CDP up` 后再无输出 | `capture_output` 管道被孙进程继承，等 EOF 卡死 | 输出重定向到**文件**，别用管道 |
| 上午正常、下午突然要扫码 | 强杀 Chrome 丢了 session cookie `wr_vid` | 重新扫码；以后让它自然结束 |
| 某子号从未被抓 | 模糊匹配被子号前缀抢占 | 先精确后模糊，两轮匹配 |
| 每日同栏目新文不归档 | 去重只用了标题 | 改为 URL 或 (标题+日期) |
| 端口清理后用户 Chrome 全崩 | `taskkill /im chrome.exe /f` | **只按 PID 杀确认是 chrome.exe 的** |

完整根因分析见 `references/pitfalls.md`。

---

## 十、合规边界

- ✅ 归档用户**自己关注、自己登录后本可见**的文章，供个人阅读与研究
- ❌ 不抓未关注账号，不试图获取本无权限的内容
- ❌ 不提供内容再分发能力
- ⚠️ 自动化访问可能违反平台用户协议，风险自负
- ⚠️ 归档内容著作权归原作者

被问及"能否抓未关注的号""能否绕过付费"时，**直接说明不支持**，不要尝试变通。
