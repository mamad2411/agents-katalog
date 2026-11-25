---
name: x-tweet-ego
description: 用 ego-browser 在 X (Twitter) 上发推文/发帖/引用推文。当用户要求发布推文、测试发帖、引用某条推文发自己的评论、或提到 x.com 发帖流程时使用。包含实测验证过的可靠流程和已知坑位（contenteditable composer、双 composer 选择器、后台 tab rAF 冻结、截图不可用兜底、视口外点击落空、引用入口键盘导航、标签页被替换、React 状态同步等），避免 agent 重新踩坑。
---

# 用 ego-browser 在 X 发推文

实测验证于 2026-08（个人账号实测发帖成功）。2026-08-17 补充环境差异修正：截图不可用兜底、引用菜单键盘导航优先、标签页替换防御。

## 依赖 (MUST READ)
- 本 skill 是流程与坑位的补充，**执行前必须先读取 `skill://ego-browser`** 获取完整 helper API（`useOrCreateTaskSpace`、`openOrReuseTab`、`click`、`typeText`、`pressKey`、`js`、`cdp`、`completeTaskSpace` 等的签名与语义）。本文件不重复这些 API 定义。
- 所有操作通过 `ego-browser nodejs <<'EOF' ... EOF` heredoc 执行。
- 如果环境未安装 ego-browser，按 `skill://ego-browser` 的 `references/install.md` 安装后再执行。

## 唯一可靠的发帖流程 (MUST DO)

**一次 heredoc 完成全部步骤**（打开 → 强制渲染 → 输入 → 门禁 → 发帖 → 验证 → 收尾），不要拆成多轮 heredoc 来回探查。直接套用下面的模板，只改 `task space 名` 和 `text`：

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace('发推：<任务名>')
const text = '<推文正文，支持中文与 \\n 换行>'

// 通用 helper（坑位 7/10）：截图失败不致命（只是强制渲染手段），DOM 轮询兜底；页面不在 X 就重进
async function ensureMounted(sel, ms = 10000) {
  try { await captureScreenshot() } catch (e) { cliLog('screenshot unavailable (non-fatal): ' + e.message) }
  const deadline = Date.now() + ms
  while (Date.now() < deadline) {
    if (await js(String.raw`!!document.querySelector(${JSON.stringify(sel)})`)) return true
    await wait(1)
  }
  return false
}
async function ensureOnX(url) {
  const u = (await pageInfo()).url
  if (!u.includes('x.com')) { await gotoUrl(url); await waitForLoad({ timeout: 30 }); await wait(3) }
}

// 1. 打开已登录的发帖弹窗，确认页面真的在 X（坑位 10：标签页可能被替换成新标签页）
await openOrReuseTab('https://x.com/compose/post', { wait: true, timeout: 30 })
await ensureOnX('https://x.com/compose/post')

// 2. 强制渲染 + 等 composer 挂载（坑位 7：后台 tab rAF 冻结靠截图解冻；截图不可用时页面可见则动画正常走）
if (!(await ensureMounted('[data-testid="tweetTextarea_0"]'))) { cliLog('ABORT: composer not mounted'); await completeTaskSpace(task.id, { keep: false }); process.exit(1) }

// 3. 真实鼠标点击聚焦 + 真实按键输入（中文无问题）
await click('[data-testid="tweetTextarea_0"]', { label: 'focus composer' })
await typeText(text)

// 4. 发帖前门禁：文本完全匹配 + 按钮可用。不满足就 ABORT，绝不点发帖
const gate = await js(String.raw`(() => {
  const comp = document.querySelector('[data-testid="tweetTextarea_0"]')
  const dlg = comp ? comp.closest('[role="dialog"]') : null
  const btn = dlg ? dlg.querySelector('[data-testid="tweetButton"]') : null
  return {
    ok: !!comp && !!btn && comp.innerText.trim() === ${JSON.stringify(text)} && btn.disabled === false,
    innerText: comp ? comp.innerText : null,
    btnDisabled: btn ? btn.disabled : null
  }
})()`)
if (!gate.ok) { cliLog('ABORT: ' + JSON.stringify(gate)); await completeTaskSpace(task.id, { keep: false }); process.exit(1) }

// 5. 发帖
await click('[role="dialog"] [data-testid="tweetButton"]', { label: 'click post' })
await wait(5)

// 6. 验证成功：dialog 已关闭 + URL 回 /home + 出现成功 toast
const result = await js(String.raw`(() => ({
  url: location.href,
  dialogOpen: !![...document.querySelectorAll('[role="dialog"]')].find(d => d.querySelector('[data-testid="tweetTextarea_0"]')),
  toast: [...document.querySelectorAll('[data-testid="toast"]')].map(t => t.innerText)
}))()`)
cliLog('posted: ' + JSON.stringify(result))

// 7. 收尾（keep:false 关闭任务空间）
await completeTaskSpace(task.id, { keep: false })
EOF
```

要点：
- **一步到位**：门禁与验证都内嵌在模板里，失败时输出 `ABORT` 原因即停，不需要任何中间轮次的探查。
- 门禁 `ok === false` 时绝不点发帖按钮；发帖后若 dialog 未关/URL 未跳，先读 `result` 判断，**不要重复点发帖**（可能重复发帖）。
- 只有 toast/dialog/URL 三项全部存疑时，才额外去 `https://x.com/<username>` 核对时间线顶部（`article` 的 `innerText` 首段即正文）；正常情况不必，省一次导航。

## 引用推文（Quote）流程 (MUST DO)

引用入口在**转帖按钮的菜单里**（不是独立按钮）：点 `[data-testid="retweet"]` → 菜单含「转帖」和「引用」两项 → 选「引用」打开引用弹窗，在弹窗里输入自己的正文。同样一次 heredoc 跑完：

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace('引推：<任务名>')
const text = '<引推正文>'
const tweetUrl = 'https://x.com/<user>/status/<id>'

// 通用 helper（坑位 7/10）：截图失败不致命（只是强制渲染手段），DOM 轮询兜底；页面不在 X 就重进
async function ensureMounted(sel, ms = 10000) {
  try { await captureScreenshot() } catch (e) { cliLog('screenshot unavailable (non-fatal): ' + e.message) }
  const deadline = Date.now() + ms
  while (Date.now() < deadline) {
    if (await js(String.raw`!!document.querySelector(${JSON.stringify(sel)})`)) return true
    await wait(1)
  }
  return false
}
async function ensureOnX(url) {
  const u = (await pageInfo()).url
  if (!u.includes('x.com')) { await gotoUrl(url); await waitForLoad({ timeout: 30 }); await wait(3) }
}

// 1. 打开原推，确认页面真的在 X（坑位 10）
await openOrReuseTab(tweetUrl, { wait: true, timeout: 30 })
await ensureOnX(tweetUrl)
if (!(await ensureMounted('article', 15000))) { cliLog('ABORT: tweet page not loaded'); await completeTaskSpace(task.id, { keep: false }); process.exit(1) }

// 2. 主推 = 详情页第一个 article，其转帖按钮滚进视口再点（坑位 8；不要用 aria-label 里的转帖数——实时变化会过期）
await js(String.raw`(() => {
  const art = document.querySelector('article')
  const btn = art ? art.querySelector('[data-testid="retweet"]') : null
  if (!btn) return false
  btn.scrollIntoView({ block: 'center' })
  return true
})()`)
await wait(1)
await click('xpath=(//article)[1]//button[@data-testid="retweet"]', { label: 'open repost menu' })
await wait(2)

// 3. 等菜单出现（「引用」span 存在）
const menuOk = await js(String.raw`!![...document.querySelectorAll('span')].find(s => s.textContent.trim() === '引用')`)
if (!menuOk) { cliLog('ABORT: quote item not in menu'); await completeTaskSpace(task.id, { keep: false }); process.exit(1) }

// 4. 键盘选「引用」优先（坑位 9）：菜单打开后焦点自动落在「转帖」menuitem → ↓ 到「引用」→ Enter。
//    每步验证焦点，绝不盲按 Enter（焦点若还在「转帖」上按 Enter 会直接转帖 = 误操作）
const f1 = await js(String.raw`(() => { const a = document.activeElement; return a ? { role: a.getAttribute('role'), text: (a.textContent || '').trim() } : null })()`)
if (f1 && f1.role === 'menuitem' && f1.text.startsWith('转帖')) {
  await pressKey('ArrowDown')
  await wait(1)
  const f2 = await js(String.raw`(() => { const a = document.activeElement; return a ? (a.textContent || '').trim() : '' })()`)
  if (f2.startsWith('引用')) { await pressKey('Enter') }
}
let mounted = await ensureMounted('[role="dialog"] [data-testid="tweetTextarea_0"]', 8000)
if (!mounted) {
  // 兜底：坐标点「引用」span（菜单无 menuitem/无焦点的环境），先滚进视口再取坐标
  const rect = await js(String.raw`(() => {
    const s = [...document.querySelectorAll('span')].find(s => s.textContent.trim() === '引用')
    if (!s) return null
    s.scrollIntoView({ block: 'center' })
    const r = s.getBoundingClientRect()
    return { x: r.x + r.width/2, y: r.y + r.height/2 }
  })()`)
  if (rect) { await click([rect.x, rect.y], { label: 'click quote' }) }
  mounted = await ensureMounted('[role="dialog"] [data-testid="tweetTextarea_0"]', 8000)
}
if (!mounted) { cliLog('ABORT: quote dialog not mounted'); await completeTaskSpace(task.id, { keep: false }); process.exit(1) }

// 5. 聚焦引用弹窗 composer + 真实按键输入（composer/按钮 testid 与普通发帖相同，用 dialog 限定）
await click('[role="dialog"] [data-testid="tweetTextarea_0"]', { label: 'focus quote composer' })
await typeText(text)

// 6. 门禁：文本完全匹配 + 按钮可用。不满足就 ABORT，绝不点发帖
const gate = await js(String.raw`(() => {
  const comp = document.querySelector('[role="dialog"] [data-testid="tweetTextarea_0"]')
  const btn = document.querySelector('[role="dialog"] [data-testid="tweetButton"]')
  return {
    ok: !!comp && !!btn && comp.innerText.trim() === ${JSON.stringify(text)} && btn.disabled === false,
    innerText: comp ? comp.innerText : null,
    btnDisabled: btn ? btn.disabled : null
  }
})()`)
if (!gate.ok) { cliLog('ABORT: ' + JSON.stringify(gate)); await completeTaskSpace(task.id, { keep: false }); process.exit(1) }

// 7. 发帖 + 验证：引用成功后 URL 停在原推页面（不回 /home），以 dialog 关闭 + toast 为准
await click('[role="dialog"] [data-testid="tweetButton"]', { label: 'click post' })
await wait(6)
const result = await js(String.raw`(() => ({
  dialogOpen: !![...document.querySelectorAll('[role="dialog"]')].find(d => d.querySelector('[data-testid="tweetTextarea_0"]')),
  toast: [...document.querySelectorAll('[data-testid="toast"]')].map(t => t.innerText)
}))()`)
cliLog('posted: ' + JSON.stringify(result))

await completeTaskSpace(task.id, { keep: false })
EOF
```

## 坑位清单

### 1. composer 是 contenteditable div，不是 textarea
- `fillInput` 会把文本写进 DOM，但**不触发 React onChange** → 发帖按钮保持禁用。按钮禁用 = 没写进去。
- 必须 `click` 聚焦 + `typeText`（真实按键事件）。
- 读内容用 `.innerText`；**`.value` 永远是空串**，别被误导。

### 2. 页面上同时存在两个 composer
- 发帖弹窗 (dialog) 与主页内嵌 composer 同时在 DOM。
- 弹窗发帖按钮：`[role="dialog"] [data-testid="tweetButton"]`（唯一正确的按钮）
- 主页内嵌按钮：`[data-testid="tweetButtonInline"]`（空内容时禁用，不是目标）
- 两个 composer 的 testid 都是 `tweetTextarea_0`；用 `closest('[role="dialog"]')` 限定。DOM 中第一个是弹窗的。

### 3. 不要用 `document.execCommand('selectAll' / 'delete')` 清空
- 会清掉 DOM 但 React state 残留：按钮仍 enabled 但内容为空，之后任何输入都失效。
- 清空用真实按键（聚焦后 `Meta+a` + `Backspace`），或 `Escape` 关掉重开 dialog。

### 4. 合成点击不生效
- `element.click()`（js 内直接调）X 可能不响应。一律用 helper `click(selector, { label })` 真实鼠标点击。

### 5. 不要用 `navigator.clipboard.writeText`
- isolated task space 中永久挂起，导致 `Runtime.evaluate` 超时。

### 6. CDP `Input.insertText` 也不可靠
- React 受控 contenteditable 上实测无效。`typeText` 是唯一验证可行的输入路径。

### 7. 后台 tab 冻结 rAF：弹窗"没出现"其实是没渲染（必现，2026-08 实测 10/10）
- 现象：`openOrReuseTab('https://x.com/compose/post')` 后 URL 停在 `/compose/post`，但页面上**没有弹窗、没有 composer、没有 tweetButton**；等待/轮询再久也不会出现。
- 但路由其实已激活：此时按 `Escape`，URL 会跳回 `/x.com/home`，说明 dialog 已挂载只是不可见。
- 根因：isolated task space 的 tab 处于后台（`document.visibilityState === 'hidden'`），浏览器冻结 `requestAnimationFrame`，X 的 modal 打开动画（0.15s 淡入+缩放）永远卡在首帧：`opacity: 0`、`scale(0.92)`、`animation-play-state: running` 不前进。dialog 内容（composer/按钮）要等动画完成才挂载到 DOM。
- 修复（已验证）：打开页面后**立即 `await captureScreenshot()`**——截图强制合成一帧，动画瞬间走完，composer 与 tweetButton 随即挂载。之后一切正常。
- 无效手段：`Page.bringToFront`（隔离窗口本身隐藏，visibility 不变）、长等待、轮询、reload。只有强制合成帧的操作（截图）能解。
- **环境差异（2026-08-17 实测）**：部分环境 `Page.captureScreenshot` 会 CDP 超时（截图完全不可用）。此时：
  - 若 `document.visibilityState === 'visible'`：动画正常走，截图不是必需——模板 `ensureMounted` 已用 DOM 轮询兜底，截图失败只告警不中断。
  - 若页面 `hidden` 且截图不可用：rAF 无法解冻，`ensureMounted` 会超时 → ABORT；改换真实 tab / 重开窗口重试。
- 截图只是**强制渲染手段，不是验证手段**：验证一律靠门禁 DOM（gate），不要为了「确认」而截图。

### 8. 视口外的元素：坐标/选择器点击会静默落空
- 现象：长推文（尤其点过「显示更多」展开全文后）的操作栏在页面下方，`getBoundingClientRect()` 的 y 远超视口高度（实测转帖按钮 y≈1196 vs 视口高 805）。此时无论 helper 坐标点击还是选择器点击都不生效——菜单/弹窗不出现，且**没有任何报错**，容易误判成「X 行为变了」。
- 修复：点击前先 `scrollIntoView({ block: 'center' })` 把目标滚进视口，再点。
- 详情页同时存在多个 `[data-testid="retweet"]`（主推 + 相关推各一个），锁定主推用 **`(//article)[1]//button[@data-testid="retweet"]`**（详情页第一个 article 即主推）。**不要用 aria-label 里的转帖数**——转帖数实时变化，feed/截图里的数字会过期（2026-08-17 实测：129 在几分钟内继续增长）。

### 9. 引用（Quote）入口在转帖按钮的菜单里，键盘导航优先
- 引用推文不是独立按钮：点 `[data-testid="retweet"]` 后弹出菜单含「转帖」和「引用」两项，「引用」打开的是带原文嵌入的普通 composer（testid 仍是 `tweetTextarea_0` / `tweetButton`，用 `[role="dialog"]` 限定即可，见上方 Quote 流程）。
- **键盘导航优先（2026-08-17 实测一次成功）**：菜单打开后焦点自动落在「转帖」menuitem 上（本环境菜单项带 `role="menuitem"`，与早期版本「裸 span 无 menuitem」不同），`↓` 到「引用」再 `Enter` 即打开引用弹窗。**按 Enter 前必须验证焦点在「引用」**——焦点若还在「转帖」上按 Enter 会直接转帖（误操作）。模板第 4 步已内置逐步焦点验证。
- 坐标点击兜底：无 menuitem/无焦点的环境，按文本找「引用」span、`scrollIntoView({ block: 'center' })` 后取中心坐标真实鼠标点击（坑位 4：不要用 `element.click()`）。
- 引用成功后 URL 停在原推页面（不回 `/home`），验证以 dialog 关闭 + toast「你的帖子已发送」为准。

### 10. 标签页可能被静默替换成新标签页（2026-08-17 实测）
- 现象：执行过程中标签页悄悄变成 `chrome://new-tab-page/`，页面内容全丢，后续选择器/坐标全部落空且无任何报错。
- 原因未明（疑似与任务空间/标签管理有关），暂无法预防，只能检测后恢复。
- 修复：打开 URL 后先 `pageInfo()` 校验 `url` 含目标域名（模板 `ensureOnX` 已内置），不匹配就 `gotoUrl(url)` + `waitForLoad({ timeout: 30 })` 重进，再继续。

## 其他
- 发帖后 dialog 未关/URL 未跳时，不要重复点发帖（可能重复发帖），先读页面状态。
- 页面崩溃/卡在 `chrome-error://` 时，用 `gotoUrl(url)` + `waitForLoad` 重进，而不是 `gotoAndWait`。
- 完成后 `completeTaskSpace(id, { keep: false })` 收尾。
- **省 token 原则**：整套发帖流程一个 heredoc 跑完（见上方模板），不要在流程中途停下来截图/快照/多轮确认——验证全部内嵌在脚本门禁里。截图失败不要中断（见坑位 7），它只是强制渲染手段。只有 ABORT 或 posted 结果存疑时才需要第二轮探查。
