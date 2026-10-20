---
name: craft-rpa
description: "录制并实际操作真实浏览器流程，使用 Playwright 上下文采集 Fetch/XHR 完整 headers、文本 body、失败与 frame/Service Worker 上下文，按会话保存 JSONL 并转换成 RPA 改造用 markdown trace。适用于录制浏览器、AI 感知页面并连续 click/fill/type/press/select/check、分析接口与复现请求、session.jsonl 转 trace、Dashboard 控制浏览器、craft rpa、record browser flow；不用于 CI 测试、并行录制、远程多租户或反爬绕过。"
---

# Craft RPA

> 自包含的"感知与操作真实页面 → 录制交互和网络 → 多会话留档 → 机械翻译成 markdown 流程参考"工具，服务于人工或 AI 辅助的 RPA 改造。
> skill 内自带 recorder、Dashboard、统一 browser controller、生命周期脚本和 trace 转换器。

---

## 适用场景

- 录制业务流程作为 RPA / 自动化脚本的**改造素材**(UiPath / Power Automate / Selenium / Playwright)
- 复盘第三方系统的真实交互(尤其严 CSP 站点,如 oracle.com)
- 同一目标多次录制,每次会话独立留档,便于横向对照
- 通过 Dashboard 在另一台机器上观察 + 控制 WSL/Linux 里的录制会话
- 抓 SPA / 复杂前端应用的真实运行轨迹
- 让 AI 在用户授权目标内循环感知页面、执行操作并验证结果
- 保存请求与响应内容，供后续接口分析和复现

## 不适用场景

- 无人值守的 CI 集成测试 → 用 Playwright test runner
- 跨机器并行录制 / 集群压测
- 反爬绕过 / 反检测自动化
- 仅前端 lint / 单测 / spec 验证
- 期望"录完就能跑"的自动重放 —— trace.md 是人/AI 改造素材,不是可执行脚本

---

## 前置条件

- Node ≥ 18(LTS 推荐)
- 系统装 Chrome（默认），或执行 `npx playwright install chromium` 并设置 `CRAFT_RPA_USE_SYSTEM_CHROME=false`
- WSL2 必须有 WSLg(`echo $DISPLAY` 应非空)
- 默认端口 `7777` 未被占用；需要修改时设置 `CRAFT_RPA_PORT=<port>`

---

## 首次安装

skill 推荐装到用户全局,任意仓库自动可用:

```bash
cp -r <source>/.claude/skills/craft-rpa ~/.claude/skills/
# 首次 start 时 run.sh 会自动 npm install,无需手装
```

或每个仓库装一份:

```bash
cp -r <source>/.claude/skills/craft-rpa <repo>/.claude/skills/
```

后文 `$SKILL_DIR` 统一指 `~/.claude/skills/craft-rpa` 或 `<repo>/.claude/skills/craft-rpa`。

---

## 自动模式(AI 代跑)

想让 AI 替你跑录制 / 停止 / 转换,**不要手 cd 进 recorder/**,改用脚本封装:

```bash
bash "$SKILL_DIR/scripts/run.sh" start [URL]      # 新会话目录 + 后台起;无 URL:TTY 下 prompt,非 TTY 直接 about:blank
bash "$SKILL_DIR/scripts/run.sh" status           # 看是否在跑 + 当前会话 + 历史数 + Dashboard URL
bash "$SKILL_DIR/scripts/run.sh" sessions         # 列所有历史会话(* 标当前)
bash "$SKILL_DIR/scripts/run.sh" logs [N]         # tail 最近 N 行(默认 50)
bash "$SKILL_DIR/scripts/run.sh" control <action> [JSON]
                                                   # AI 感知和操作同一个录制浏览器
bash "$SKILL_DIR/scripts/run.sh" stop             # SIGINT 优雅停止,3s 未退再 SIGTERM
bash "$SKILL_DIR/scripts/run.sh" craft [--session <ts>] [OUT]
                                                   # 转 jsonl → trace.md;--session 默认 = 当前/最新;OUT 默认 ./trace.md
```

运行时状态 / sessions / profile / 依赖全部在 `$(pwd)/.craft-rpa/`(可用 `CRAFT_RPA_HOME` env 覆盖到任意路径)。首次 `start` 自动在 `.craft-rpa/runtime/recorder` 执行 `npm install`(跳浏览器下载,通常 30-60s)。

**AI 行为约定**(看到下列触发就跑对应子命令,不要手敲底层 cd / nohup):

| 用户说 | AI 跑 |
|--------|-------|
| "开始录" / "录浏览器 [URL]" / "start" | `run.sh start [URL]`,把返回的会话 ts + Dashboard URL 贴给用户 |
| "停" / "结束录制" / "stop" | `run.sh stop`,贴出本会话事件数 |
| "转换" / "生成参考" / "craft" | `run.sh craft`(输出 trace.md),贴出输出路径 + 行数 + 会话 ts |
| "转上一次的" / "转 <ts>" | `run.sh craft --session <ts>` |
| "看 log" / "看日志" | `run.sh logs` |
| "在跑吗" / "status" / "看下当前" | `run.sh status` |
| "列会话" / "看历史" | `run.sh sessions` |
| "看看页面" / "感知页面" | `run.sh control observe '{"index":0,"screenshot":true}'` |
| "点击/填写/选择/按键" | 先 observe，再调用对应 `control` action，最后再次 observe 验证 |

**AI 行为边界**:

- 用户授权一个浏览器目标后，按“observe → action → observe/页面断言”连续执行，无需逐次确认每个点击或填写。
- 当目标页面、业务对象或预期结果无法从授权中合理确定，或动作即将超出当前目标时暂停询问。
- 用户要求停止或关闭浏览器时，立即停止后续 action 并执行 `run.sh stop`。
- 不绕过 `run.sh` 直接启动底层进程，避免绕过会话目录和 PID 管理。
- 自己尝试合并语义步骤 / 命名 step / 删事件 —— 这是 AI 精修阶段的事(下一段),`craft` 输出已经包含全部原始信息

---

## 数据位置与多会话约定

录制产物与运行时状态**写入项目根**(与 skill 代码解耦),默认 `<cwd>/.craft-rpa/`,可用环境变量 `CRAFT_RPA_HOME` 覆盖。

```
<repo>/.craft-rpa/              ← 项目根,建议仓库根 .gitignore 豁免整目录
├── sessions/
│   ├── 2026-05-18_10-30-00/   ← 每次 start 创建时间戳目录,不覆盖历史
│   │   ├── session.jsonl
│   │   ├── artifacts/          ← observe 截图和可选 DOM/frame HTML
│   │   └── trace.md            ← 可选,craft 输出可指定到此
│   ├── 2026-05-18_14-22-15/
│   └── legacy-2026-05-17_...   ← 老版本遗留 / 升级时自动归档
├── profile/                    ← Chrome 持久 profile(登录态,项目独立)
├── runtime/recorder/           ← Playwright 运行时依赖,不写入受管 Skill 目录
│   ├── package.json / package-lock.json
│   └── node_modules/
├── .launch.pid / .launch.log   ← 进程管理 + 日志
└── .current-session            ← 最近一次 start 的会话 ts

.claude/skills/craft-rpa/recorder/   ← 仅包含 Plugin 管理的代码资产,不生成运行时软链或 node_modules
```

**为什么这样**:
- 录制 jsonl 是**项目业务数据**,跟着仓库走(每个仓库独立 session 池,不串)
- skill 代码可装 `~/.claude/skills/craft-rpa/` 全局,所有仓库共用同一份代码
- `run.sh` 通过显式环境变量把 profile、session 和 Playwright 依赖路径传给录制器,Plugin 更新不会扫描或覆盖运行时数据

**关键性质**:

- 每次 `run.sh start` 创建新时间戳目录,**不覆盖**历史
- 新版不在 `recorder/` 内创建 `session.jsonl`、`profile` 或 `node_modules`
- 老版本遗留的软链只删除链接本身,不会删除其目标；普通 `recorder/session.jsonl` 在第一次 start 时归档到 `sessions/legacy-<ts>/`,普通 `recorder/profile/` 归档到 `.craft-rpa/profile-legacy-<ts>/`
- 老版本 `recorder/node_modules` 是可重建缓存,第一次 start 时删除并在 `.craft-rpa/runtime/recorder` 重新安装
- `run.sh craft` 默认转最新;`--session <ts>` 可转任意历史
- 删历史:手动 `rm -rf .craft-rpa/sessions/<ts>/`,run.sh 不管删

**`CRAFT_RPA_HOME` env 用法**:

```bash
# 默认:cwd 是 oracle-register 时,数据写在 oracle-register/.craft-rpa/
cd <your-repo> && bash $SKILL_DIR/scripts/run.sh start

# 想统一集中存(比如 home 下中央位置):
export CRAFT_RPA_HOME=~/rpa-recordings
bash $SKILL_DIR/scripts/run.sh start
```

---

## AI 页面感知与连续操作

先观察当前页面，再把 observe 返回的 page/frame/target 原样用于动作：

```bash
bash "$SKILL_DIR/scripts/run.sh" control pages
bash "$SKILL_DIR/scripts/run.sh" control observe '{"index":0,"includeText":true,"includeAria":true,"includeElements":true,"screenshot":true,"dom":false}'
bash "$SKILL_DIR/scripts/run.sh" control click '{"index":0,"frame":{"index":0},"target":{"role":"button","name":"提交","exact":true}}'
bash "$SKILL_DIR/scripts/run.sh" control fill '{"index":0,"target":{"label":"邮箱","exact":true},"value":"user@example.com"}'
bash "$SKILL_DIR/scripts/run.sh" control type '{"index":0,"target":{"selector":"#code"},"value":"123456","delayMs":80}'
bash "$SKILL_DIR/scripts/run.sh" control press '{"index":0,"target":{"selector":"#code"},"key":"Tab"}'
bash "$SKILL_DIR/scripts/run.sh" control select '{"index":0,"target":{"testId":"region"},"value":"sg"}'
bash "$SKILL_DIR/scripts/run.sh" control check '{"index":0,"target":{"label":"同意条款","exact":true}}'
```

target 必须只使用一种主定位策略：`selector`、`role`、`text`、`label`、`placeholder` 或 `testId`。未指定 `nth` 且出现多个可见匹配时，接口返回 `AMBIGUOUS_TARGET` 和候选摘要，不会静默操作第一个元素。跨 frame 时优先回传 observe 给出的 `frame.index`；页面跳转后重新 observe，不沿用过期 index。

observe 默认返回有界可见文本、ARIA snapshot 和最多 500 个交互元素，并受单次请求总超时约束；截图最大 20 MiB，显式请求的 DOM 每个 frame 最大 5 MiB，均保存到当前会话 `artifacts/`，响应只返回本地路径，不内联 base64。

---

## 网络采集与本地数据边界

- Fetch/XHR 由 Playwright BrowserContext 的 `request/requestfinished/requestfailed` 采集，覆盖主页面、跨域 iframe 和 Playwright 可观察到的 Service Worker 请求。
- 每个 HTTP request 只产生一条最终事件；redirect 每一跳独立记录并用 `redirectedFromRequestId` 关联。
- 请求/响应使用完整 headers；文本 body 每个方向最多捕获 **20 MiB**，按 UTF-8 字节边界截断。
- 二进制只保存 Content-Type、大小和跳过原因；multipart 只保存普通字段及文件名、MIME、大小等元数据，不保存文件正文。
- Authorization、Cookie、Set-Cookie、token、密码和正文默认原样保存。`.craft-rpa/` 只在本地使用，不得未经人工检查上传、提交 Git 或发送给第三方。
- trace 默认每个 body 只展示 16 KiB；完整捕获内容通过事件的 `jsonlLine` 回查 `session.jsonl`。
- `/control/*` 不使用 token，本机 CLI 和 Dashboard 可直接调用。logger 继续监听 `0.0.0.0` 供 WSL/Windows 互访，但第三方网页 Origin 的控制请求会被拒绝；不要把端口转发到公网或不可信局域网。

---

## AI 精修阶段做什么(关键)

`jsonl-to-trace.js` 输出是**机械翻译,不删信息**:每个事件平铺一段,字段全保留。这意味着 trace.md 里没有"业务步骤"概念,只有原始事件。

**AI 拿到 trace.md 后应该做的事**(用户没明说时也要主动做):

1. **识别业务步骤**:把多条相邻事件合并成"用户在做一件事"
   例:`input(email)` + `input(password)` + `click(登录)` + `network(POST /api/login → 200)` + `pageload(/dashboard)` = "Step 1 — 用户登录"
2. **给步骤起业务命名**:基于元素 accessibleName / URL / 上下文推断(登录 / 下单 / 创建实例 / 退订),不要叫 "Step 1 — Click button"
3. **标注噪音但不删原文**:对明显无业务意义的事件(高频 mousemove、纯 focus / blur、统计埋点 xhr)在产出里灰显或归类到"噪音观察"段,**但 trace.md 原文不动**

   ⚠ **关键警示**:trace.md 速览表中 `[BUSINESS-IN-NOISE]` 标记的事件**永远不能当噪音过滤**——它们是被埋在 fingerprint frames 噪音段里的业务 click(典型场景:支付 modal 内的 Credit Card / Close 按钮,被前后大量 ThreatMetrix fingerprint frame 包围)。AI 看到此标记必须**反向验证**该 interaction 是否对应一个业务步骤,并在 rpa-draft.md 中显式覆盖。`[NOISE?]` 仅是参考标记不是真值,但 `[BUSINESS-IN-NOISE]` 是"已经发现的反例",优先级最高。
4. **保留选择器全集**:RPA 改造时不同工具偏好不同选择器(UiPath 喜欢 ID,Selenium 偏 XPath,Playwright 喜欢 role+name),不要只挑一个
5. **保留敏感字段原值**:RPA 流程通常需要固定填值,直接呈现,不要替换为占位
6. **输出 RPA 改造草案**:推荐结构

```markdown
# RPA 流程草案 - <场景名>

## 整体流程
<3-5 句业务描述>

## 关键步骤

### Step 1 — <业务命名>
- 触发: <用户什么动作>
- 元素: <accessibleName> (selector: <最稳的两三个>)
- 输入值: <如有>
- 触发请求: <如有>
- 完成判定: <pageload / 元素出现 / network status>

### Step 2 — ...

## 噪音观察(供改造时跳过)
- 事件 #15-#18:鼠标 hover 触发 tooltip,无业务意义
- 事件 #34:百度统计埋点,可忽略

## RPA 工具适配建议
- UiPath:用 attribute 选 testId / id
- Power Automate:用 role+name
- Selenium:用 XPath 兜底
```

7. **保留可追溯性**:每个 Step 标注覆盖的原始事件 # 区间,方便用户回查

### 产物落盘约定

| 项 | 约定 |
|----|------|
| **文件名** | `rpa-draft.md`(固定,不带场景名后缀;场景名写在文档标题里) |
| **位置** | `$CRAFT_RPA_HOME/sessions/<ts>/rpa-draft.md`,与 `trace.md` 同目录,可追溯性最强 |
| **触发关键词** | 用户说"精修" / "RPA 草案" / "改造草案" / "draft" / "进入精修阶段" / "输出草案" 时,AI 主动生成 |
| **不落对话** | 草案体量通常数 KB ~ 数十 KB,写文件后只给用户:**路径 + 关键发现摘要(3-5 点)**,不在对话里贴正文 |
| **重生成** | 重新精修同一会话 → 覆盖 `rpa-draft.md`(不加时间戳后缀,会话隔离已由父目录 `<ts>/` 完成) |
| **跨会话对照** | 不合并 jsonl;由 AI 在精修时读多个 `sessions/<ts>/trace.md`,产出独立的"对照"草案(用户显式要求时) |

---

## RPA 实施模板(撞 → 修循环)

> 本段沉淀自 `oracle-register` 等实战任务的撞坑经验:rpa-draft.md 给出的 selector 表 **绝不是 ground truth**,实施期默认会撞 2-3 次;不内置失败回路就只能盯眼看,几小时排错变成几分钟。

### rpa-draft 不是 ground truth

trace.md 是机械翻译;rpa-draft.md 是 AI 基于 trace 的**推断**——它没看过真实 DOM,只看到了选择器集合 + 文本 + 祖先链。对 react-select / 自定义 radio / 隐藏 checkbox 等第三方深度定制 SPA(典型:oracle.com / cybersource 支付),selector 表只能当 **first guess**:

- 真实跑起来 `getByRole('option')` 找不到、`getByLabel(/X/)` 命中错的元素、提交按钮一直 disabled —— 都是预期内的
- 默认会撞 2-3 次,撞了不是 rpa-draft 写错,是 selector 推断本质上的不确定性
- 撞了**不要硬猜下一个选择器**——dump DOM 看真实结构,再回头改

### 必备四件套

实施 RPA 脚本时必须内置(任一缺失都让排错时长 ×5):

1. **dumpFailure** —— 失败时落:
   - `screenshot.png`(fullPage)
   - `url.txt`(失败时的 URL,SPA 单 URL 时也要)
   - `dom.html`(主 frame `page.content()`)
   - `frame_N_<url>.html`(所有非主 frame 的 `f.content()`)—— iframe 支付 / 跨域 widget 唯一能看到真实 DOM 的方式
   - `error.json`(step / message / stack)
2. **Playwright tracing** —— `ctx.tracing.start({snapshots: true, sources: true})` / `ctx.tracing.stop({path: 'trace.zip'})`,失败后用 `npx playwright show-trace trace.zip` 回放可视化排查
3. **Atomic status machine** —— `pending → running → succeeded / dead`;
   - 退出 hook(SIGINT / SIGTERM / uncaughtException)把 `running` 回写 `pending` 避免账户被悬挂
   - `accounts.json.tmp` + rename 原子写,避免半成品状态
4. **noise / business hint 参考但自验** —— 看到 trace.md 里 `[BUSINESS-IN-NOISE]` 标记的 interaction 当作 **"必须验证是否漏点"的提示**,不直接信任 AI 的噪音过滤结论。被埋在 fingerprint frame 噪音里的支付按钮(Credit Card / Close)是这个标记的典型对象

### 7 类 Playwright stubborn elements 速查

撞 `Timeout` / `intercepts pointer events` / `not visible` / `outside of the viewport` / `getByRole 命中错元素` / Submit 永远 disabled / 等不到 URL 跳转 时,先对照 `<repo>/.trellis/spec/guides/playwright-stubborn-elements-guide.md` 的 7 类速查表 + Click 三层 actionability 跳过参考(.click → force:true → evaluate(el => el.click))。该 guide 含 oracle-register 实战的具体修法和 selector 优先级修订版。

> 注:guide 路径以 `<repo>` 占位,因为 craft-rpa skill 可装到全局 home(`~/.claude/skills/`),而 spec 通常在具体项目仓库。

### 何时升级 timing 应对

实施期撞到下面任一现象,**立刻升级 timing 策略**,不要硬调 selector:

- onBlur validation 不触发(Continue 按钮永远 disabled)→ 字段内 `pressSequentially(value, {delay: 80-150})` + `press('Tab')` 主动 blur,而非一次性 `fill()`
- 后端风控 ban / step 间瞬时切换被检测 → step 间加 500-2000ms `humanPause` 随机停顿
- 字段完全无鼠标移动被 fingerprint(很少需要)→ `page.mouse.move` 加少量随机轨迹

不是所有 input 都要逐字符——**只在校验逻辑挂在 onBlur 或 Continue 一直 disabled 的字段**上加。

### 已知限制(写进 SKILL.md 避免反复踩)

- **Shadow DOM 内 outerHTML 提取**:浏览器 API 限制,跨 shadow root 拿不到,inject.js 的 `target.contextHTML` 字段在 shadow root 元素上会缺失;只能用 selectors / accessibleName 推断
- **跨域 iframe 元素**:同源策略限制,inject.js 在跨域 iframe 内单独运行但无法跨域访问父 frame 上下文;`target.contextHTML` 在跨域 iframe 内取自当前 frame 上下文(不含父 frame)

---

## 工作流

### Step 1: 启动录制

```bash
bash "$SKILL_DIR/scripts/run.sh" start https://target.com
# 或
bash "$SKILL_DIR/scripts/run.sh" start          # 起 about:blank
```

启动成功标志:

- run.sh 返回 `[craft-rpa] started (pid=..., url=...)` + 会话 ts + Dashboard URL
- 浏览器窗口弹出(每个新页面 Console 会打 `[inject] boot at <url>`)
- `<cwd>/.craft-rpa/sessions/<ts>/session.jsonl` 已创建(空文件,等事件)

### Step 2: 用 Dashboard 或 AI 实时感知和操作

打开 `http://localhost:${CRAFT_RPA_PORT:-7777}/dashboard`:

- 顶部 4 计数器(int / net / nav / err)随你的操作上跳
- 没数:`run.sh logs` 看 launch / logger 报错;最常见根因是 `7777` 端口被占

**快捷键**:

| 键 | 动作 |
|----|------|
| `T` | 切主题 |
| `Space` | 暂停 / 恢复事件流 |
| `Ctrl/⌘ + F` | 聚焦搜索 |
| `Esc` | 关闭详情面板 |

**反向控浏览器**(走 `logger.js` 的 `/control/*` 接口):

- Dashboard 顶部 URL 栏输地址回车 → 当前 tab 打开;勾"新标签"则 newTab
- 底部 tabs 区域可点切换 / 关闭 / 刷新 / 前进后退
- AI 使用 `run.sh control observe` 获取真实页面状态，再调用 click/fill/type/press/select/check/uncheck。
- 每次会导致页面状态变化的操作后重新 observe 或检查返回的 `urlAfter`，不要只依据操作请求成功就假设业务完成。

### Step 3: 录完停止

```bash
bash "$SKILL_DIR/scripts/run.sh" stop
# 输出: [craft-rpa] stopped (session=2026-05-18_10-30-00, 187 events)
```

或直接关浏览器窗口(launch.js 自动检测 context.on('close') 关闭 logger,run.sh 的 PID 文件会留着但 status 会发现进程已死自动清掉)。

### Step 4: 生成 RPA 流程参考(trace.md)

```bash
bash "$SKILL_DIR/scripts/run.sh" craft
# 默认 --session=最新 → 写 ./trace.md
```

**trace.md 内容结构**:

1. **头部元数据**:起止时间 / 时长 / 事件总数 / URL 覆盖 / kind.type 分布 / 超长 URL 截断统计
2. **速览表**:每事件一行(`#/jsonl#/t+s/kind.type/简述/最稳selector/value 或 URL`),方便整体把握
3. **事件详情**:每事件一段,字段全保留(target.selectors 全集 / accessibleName / state / boundingBox / 网络字段 / 祖先链 / formFields ...)

**关键性质**:

- 机械翻译,**不过滤任何事件**(信息零损失)
- **不命名业务 step**(js 不知道业务语义,留给 AI 精修)
- **不脱敏**(`recorder/inject.js` 已默认 `REDACT_SENSITIVE=false`,value 全是原值)
- 超长 URL(>800 chars 默认)截断 + 标注 `jsonlLine: <N>` 反查;原文取法 `sed -n '<N>p' session.jsonl | jq .url`
- 网络 headers、body、失败和 frame/Service Worker 上下文会进入详情；body 默认只展示 16 KiB，完整捕获值回查 JSONL。

**AI 拿到 trace.md 后**:走"AI 精修阶段做什么"段的 7 步,输出 RPA 改造草案给用户。

### Step 5: 转给 RPA 工具实施

把 trace.md(原始素材) + AI 精修后的草案(产出) 给到 RPA 工程师,他们对照 selector 全集 + 输入值 + 网络断言 + 业务命名,在 UiPath / Power Automate / 自研 RPA 里搭出可视化流程。

---

## Hard Constraints(违反破坏核心功能)

1. **交互事件以 Playwright binding 为主路径**，不要重新把页面 fetch/XHR hook 或关闭浏览器安全特性作为正常传输方案。
2. **端口只从 `CRAFT_RPA_PORT` / `recorder/config.js` 派生**，不要在 logger、inject、Dashboard 或 client 增加新的硬编码端口。
3. **`recorder/inject.js` 保持单文件 / 无依赖 / 不抛错到业务页面**，启动器读取文件后通过 Playwright `addInitScript({ content })` 注入它。
4. **HTML 注入点必须 `escapeHtml`**，Dashboard 渲染的数据来自任意目标站。
5. **`/log` 与 `/control/*` 的 Origin 策略必须分离**：前者支持任意目标页回退写入，后者拒绝第三方网页 Origin。
6. **敏感字段默认不脱敏**，仅限本地复现；外传或归档前由用户明确检查和处理。
7. **网络正文捕获上限为每方向 20 MiB，trace 展示上限独立为 16 KiB**，不要把展示截断误写成原始捕获截断。

---

## 排错快查

| 症状 | 根因 | 修复 |
|------|------|------|
| 浏览器拉不起 / 找不到 display | WSL2 无 WSLg / Linux 无图形 | 升 Win11 自带 WSLg / 装 X server；只做无界面验证时设置 `CRAFT_RPA_HEADLESS=true` |
| `Executable doesn't exist at .../chrome-linux/chrome` | `CRAFT_RPA_USE_SYSTEM_CHROME=false` 但没装 Chromium | `npx playwright install chromium` 或取消该环境变量 |
| `channel 'chrome' is not installed` | 默认系统 Chrome 不存在 | 安装 Chrome，或下载 Chromium 后设置 `CRAFT_RPA_USE_SYSTEM_CHROME=false` |
| 端口 `7777` 被占 | 其他进程占用 | `export CRAFT_RPA_PORT=8888` 后重新 `run.sh start` |
| Dashboard 一直 0 事件 | inject.js/binding 未安装或 launch 启动失败 | `run.sh logs` 查 `[inject] boot`、`[launch] fatal` 和 binding 错误 |
| action 返回 `AMBIGUOUS_TARGET` | 多个可见元素命中 | 读取候选摘要，改用更稳定 target；确实要选序号时显式传 `target.nth` |
| action 返回 `FRAME_NOT_FOUND` | 页面跳转后 frame index 变化 | 重新 observe，使用最新 frame index/URL |
| trace 没显示完整 body | trace 独立限制为 16 KiB | 按 `jsonlLine` 回查 `session.jsonl` 对应 requestBody/responseBody |
| `run.sh start` 报"already running" 但你没跑 | `.launch.pid` 残留 | `rm .craft-rpa/.launch.pid` 后重试 |
| `craft` 报"no session found" | sessions 目录空 / 没录过 | 先 `run.sh start` 录一段 |
| trace.md 速览表表格错位 | 字段含 `|` 或换行未转义 | js 已转义,如仍有问题报具体 # 事件 |
| 整页跳转后 sessionId 变了对不上 | 这是正常的 —— 每页注入是新会话(jsonl 内的 sessionId,与 run.sh 的会话 ts 是不同概念) | 分析时按 `url` 分组,不依赖 jsonl 内 sessionId 跨页对齐 |
| 历史 sessions 太多占空间 | 手动清理 | `ls .craft-rpa/sessions/` 看,`rm -rf .craft-rpa/sessions/<ts>/` 删 |

---

## 反模式

### 脚本生成 / 解读层面

- 让 `jsonl-to-trace.js` 做语义合并 / step 命名 / 噪音判断 —— 这些需要业务上下文,js 不知道;**留给 AI 精修阶段**
- 在转换器里默认过滤事件 —— 信息丢失不可逆;噪音判断由 AI 在精修阶段标注(但不删原文)
- 用 `xpath` 作为首选 selector —— xpath 是兜底,DOM 一调全断;按 testId → role+name → id → name → ariaLabel → text 顺序找
- 把多次 `run.sh start` 的事件混在一个 trace.md 里 —— 每会话独立,跨会话对照应该是 AI 在精修阶段做,不是合并 jsonl

### 工具使用层面

- 在 `recorder/inject.js` 引入 npm 依赖 —— `addInitScript` 注入约束,只能用浏览器原生 API
- 把端口 / Dashboard 暴露公网 —— logger 监听 `0.0.0.0:7777` 且无鉴权,仅本地开发
- 并行起多个 `launch.js` 共用同一 `.craft-rpa/profile/` —— Chrome 单实例锁,会启动失败或损坏 profile
- 在任一入口重新硬编码 logger URL/port —— 统一通过 `CRAFT_RPA_PORT` 和启动注入配置派生
- 让被录制页面直接调用 `/control/*` —— 页面脚本不是可信控制端，AI 使用 `run.sh control`
- 录制时 `Ctrl+C` 强杀 launch.js —— 优先 `run.sh stop`,让 SIGINT 走完优雅关闭路径,profile 才能正确落盘
- 把 `.craft-rpa/` 提交进 git —— 该目录全是业务数据 + 运行时,装 skill 到新仓库时在仓库根 `.gitignore` 加一行 `.craft-rpa/`

### Skill 使用层面

- 不要为"跑一次 launch.js"创建 trellis task —— 这是工具调用,不是工程任务
- 不要把 `trace.md` 写回 `recorder/` —— recorder 只负责录制,产出应放消费方仓库或 `.craft-rpa/sessions/<ts>/`
- skill 内 `recorder/` 是 skill 自带的独立资产,跟项目根的 oracle-register 代码无关 —— 改 skill 内的代码不会影响项目根,反之亦然(`REDACT_SENSITIVE` 切换属 skill 内本地配置)
