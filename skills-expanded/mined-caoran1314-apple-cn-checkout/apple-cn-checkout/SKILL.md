---
name: apple-cn-checkout
description: 用 bsk_* 浏览器工具在苹果中国官网（apple.com.cn）完成 iPhone 选购与结账。含实测的稳定选择器、5 级门控的一轮批量配方、以及会造成静默失败的坑（networkidle 永不满足 / CSS 猜选择器会打偏 / 点击后立刻读取是旧 DOM）。当用户要求在 Apple 中国官网买手机、加购物袋、或走到微信支付时使用。
---

# Apple 中国官网选购/结账流程（实测固化）

## 0. 铁律（先读，否则会静默做错）

| 事实 | 后果 |
|---|---|
| **点击成功后立刻 observe 会读到旧 DOM** | 徽标/URL 都滞后。**唯一可信的验证 = 重新导航到目标页再读（服务端真相）** |
| **`waitUntil: networkidle` 在 Apple 上永远不满足** | 白等满超时。Apple 页面持续上报，**不要用它做门控** |
| **猜 CSS 选择器会静默打偏** | `clicked at (x,y)` 照样回报成功，实际点错元素。**只用两种来源：observe 给的 `@eN` ref，或从 scoped HTML 读到的确切 `data-autom`** |
| **购物袋是「一行 × 数量 N」** | 不是 N 行。**删一次清空整行**，只有一个移除按钮 |
| **结账必须登录 Apple 账号** | 游客态点结账会跳登录。**登录/验证码必须用 `bsk_assist request-help` 交给用户**，agent 绝不碰账号密码 |
| **微信支付是手机扫码** | 技能文档归类为 phone-only QR scan，**agent 侧设计上阻塞**。走到二维码页即停，交用户扫 |

## 1. 已验证的稳定选择器（国行购买页）

页面：`https://www.apple.com.cn/shop/buy-iphone/iphone-18-pro`

```
机型   input[value="6_3inch"]        iPhone 18 Pro 6.3"
       input[value="6_9inch"]        iPhone 18 Pro Max 6.9"
外观   input[value="burgundy"]       勃艮第酒红色
       input[value="glacier"]        冰川蓝色
       input[value="silver"]         银色
       input[value="black"]          黑色
存储   input[value="256gb"]          256GB  RMB 9999
       input[value="512gb"]          512GB  RMB 11999
       input[value="1tb"]            1TB    RMB 15499
       input[value="2tb"]            2TB    RMB 20499
折抵   input[value="noTradeIn"]      不折抵换购
       input[value="tradeIn"]        添加折抵设备
保障   input[data-autom="noapplecare"]   不加 AppleCare+   ← 两个选项 value 都是 "on"，只能靠 data-autom
提交   button[data-autom="add-to-cart"]  添加到购物袋
```

> `data-autom` 是**从 scoped HTML 读到的**，不是猜的。拿 ref 后读：
> `bsk_inspect({action:"html", ref:"@eN", maxBytes:800})`
> 例：`<input class="form-selector-input rf-applecare-selector" data-autom="noapplecare" type="radio" name="applecare-options">`

## 2. 一轮批量配方（本流程最快的写法）

**依据**：守护进程**按提交顺序串行执行**命令队列，所以「等待 → 点击 → 等待 → 点击」的依赖链可以放在**一次往返**里。

**关键门控**：`state: "attached"` + 选择器带 `:not([disabled])`。
- 默认 `state=visible` 对 Apple 的**隐藏原生 radio** 永远不满足（`visible=false`）→ 每次白等满超时（实测 10004ms）
- 改成 `attached`：未启用就不匹配（`attached=false`）继续轮询，启用瞬间命中（实测 **7–122ms**）

```
bsk_tabs   {action:"create", url:"…/shop/buy-iphone/iphone-18-pro", active:true}
bsk_page   {action:"wait-for-element", state:"attached", target:'input[value="6_3inch"]:not([disabled])', timeoutMs:25000}
bsk_interact {action:"click", target:'input[value="6_3inch"]'}
bsk_page   {action:"wait-for-element", state:"attached", target:'input[value="burgundy"]:not([disabled])'}
bsk_interact {action:"click", target:'input[value="burgundy"]'}
bsk_page   {action:"wait-for-element", state:"attached", target:'input[value="256gb"]:not([disabled])'}
bsk_interact {action:"click", target:'input[value="256gb"]'}
bsk_page   {action:"wait-for-element", state:"attached", target:'input[value="noTradeIn"]:not([disabled])'}
bsk_interact {action:"click", target:'input[value="noTradeIn"]'}
bsk_page   {action:"wait-for-element", state:"attached", target:'input[data-autom="noapplecare"]:not([disabled])'}
bsk_interact {action:"click", target:'input[data-autom="noapplecare"]'}
bsk_page   {action:"wait-for-element", state:"attached", target:'button[data-autom="add-to-cart"]:not([disabled])'}
bsk_interact {action:"click", target:'button[data-autom="add-to-cart"]'}
bsk_page   {action:"navigate", url:"https://www.apple.com.cn/shop/bag", waitUntil:"load"}
bsk_inspect {action:"observe", maxTokens:700}      ← 唯一的验证：重载后读服务端状态
```

**不要**把 5 个点击裸批量提交（中间无 wait）——React 还没把下一组解锁，点击落在 disabled 控件上被**静默吞掉**，工具照样回报 `clicked at (x,y)`。

**不要**用「点击后立刻 `bsk_tabs list` 看 URL」当验证——SPA 的 URL 更新滞后，会给出假阴性。

## 3. 购物袋

```
读取:  bsk_inspect {action:"observe", maxTokens:1800}
移除:  读到的 `@eN button "移除 …"` 的 ref（ref 可靠；`button[data-autom*="remove"]` 这种猜测会打偏）
验证:  bsk_page {action:"navigate", url:"https://www.apple.com.cn/shop/bag"} + observe → "你的购物袋中没有商品。"
```

## 4. 结账 → 微信支付（需要用户参与）

```
1. 购物袋 → 点「结账」
2. 大概率跳登录 → 立即 bsk_assist {action:"request-help", prompt:"请在这里登录你的 Apple 账号…", completionCriteria:{...}}
   ★ agent 绝不输入账号密码 / 验证码 / 不做人脸
   ★ 只在 continued / completed 之后继续，然后 observe
3. 登录后：配送地址 → 送货或到店取货 → 发票/抬头（如需要）
4. 付款方式选「微信支付」
5. 到达二维码页 → 停。再 request-help 或直接交用户扫码付款
   ★ 微信扫码 = phone-only QR scan，agent 侧设计上阻塞，必须用户完成
```

**边界**：agent 的终点是「微信支付二维码出现」。不替用户点最终付款、不代付。

## 5. 值得记住的国行/美版差异

| | 美国站 apple.com | 中国站 apple.com.cn |
|---|---|---|
| 起价 | $1199 | RMB 9999 |
| 付款方式段 | Buy / Finance / Lease | **无** |
| 运营商段 | Connectivity / carrier | **无** |
| AppleCare 段 | 有 | **有，且是提交前的拦路条件** |
| 其它 | — | 限购 2 部；税费单列（约 RMB 1157） |

---

## 6. 「收藏」（个人收藏）实测结论

**位置与两条入口（实测，2026-10）**：

从根地址 `https://www.apple.com.cn/`（**打开正常、不跳转**）进站后：

| 入口 | 路径 | 是否需要登录 |
|---|---|---|
| ✅ **推荐** | 导航「**打开购物袋**」→ `/shop/bag` 的「**个人收藏**」段 | **不需要**（商店层 cookie 即可见） |
| ❌ | 页脚「账户」→「Apple Store 账户」→ `/shop/signIn/account?ssi=…` | **需要真正登录 secure6** |

⚠️ 更正：早前记的"收藏需登录态"**是错的**。实测在**全新会话、未登录 secure6** 的情况下，
`/shop/bag` 的「个人收藏」段**照样显示**全部收藏项。
但**账户页（`/shop/account/home`）必须登录**才能进 —— 两者不是一回事。

`/shop/saved` 是 **404**，别用。

**竞态（更强了）**：该段**异步加载**，实测**同一页面两次读取，第一次没有、第二次才有**
（连全新会话也一样）。门控写法：


```
bsk_page {action:"wait-for-element", state:"attached", target:'a[href*="iphone-duo"]'}
```

**收藏项上的按钮不是「付款」**：

| 收藏项类型 | 按钮 |
|---|---|
| 配件（如保护壳） | `添加到购物袋` |
| iPhone（配置型） | **`继续`** → 跳到该配置的**专属 SKU 购买页**，配置靠 SKU 保留<br>（实测 `iPhone Duo 512GB 星光白色` → `/shop/buy-iphone/iphone-duo/mk2p4ch/a`） |

**第二个机型复核（iPhone 18 Pro，结论一致）**：

- `iPhone 18 Pro 256GB 勃艮第酒红色` → `/shop/buy-iphone/iphone-18-pro/mjt94ch/a`
- 落点页的机型 radio 显示 `[checked] ="6_3inch"` —— **配置完整保留** ✓
- iPhone 类收藏项**只有「继续」**，既没有「添加到购物袋」，也没有任何「付款」控件
- 配件类收藏项是 `添加到购物袋`（直接进袋，不经配置页）

**结论：从收藏可以「进入购买流程」（直达该配置的购买页），但无法「直达付款」。**

**✅ 全链路已实测走通（iPhone 18 Pro，订单 `#W1873308640`）**——从收藏起步，**一次连续跑完到二维码**：

```
/shop/bag「个人收藏」→ 18 Pro 的「继续」
 → /shop/buy-iphone/iphone-18-pro/mjt94ch/a      （配置已带：256GB 勃艮第酒红色）
 → input[value="noTradeIn"]  → input[data-autom="noapplecare"]
 → button[data-autom="add-to-cart"]              （添加到购物袋）
 → /shop/bag → 结账
 → _s=Fulfillment-init → 「继续填写送货地址」
 → _s=Shipping-init    → button[data-autom="shipping-continue-button"]
 → _s=Billing-init     → input[value="WECHAT"]   （等 :checked 再继续）
 → _s=Review           → button[data-autom="continue-button-review"]
 → button[data-autom="continue-button-placeOrder"]（立即下单）
 → /shop/checkout/thankyou → 微信二维码
```

**入口不影响后续**：从收藏进入购买页后，链路与直连 SKU **完全相同**。
二维码渲染耗时**波动很大**（实测 7s / 30s+ / 34.4s），门控用
`wait-for-element img[alt*="二维码"] --state visible --timeout 40s`，**等它，别刷新**。
完整链路仍是：`收藏 → 继续 → SKU 页 → 折抵/AppleCare → 提交 → 结账 → 配送 → 付款方式 → 订单 → 二维码`

**把商品放进收藏的办法**（实测）：购物袋里每行都有
`@eN button "移入收藏 <商品名>"`；点击后是**异步**的（原位置出现 `image "正在处理"`），
购物袋随即清空。**必须重新加载 `/shop/bag` 才能看到它出现在「个人收藏」**——
立刻 observe 会读到"收藏里还没有"的旧状态。

**结论：从收藏无法直达付款。** 真实路径必然是
`收藏 → 继续 → SKU 页 → 折抵/AppleCare → 提交 → 结账 → 付款方式 → 二维码`

**更快：跳过收藏页，直接开 SKU URL**（一步到位，配置已带）。

## 7. iPhone Duo（预购型商品）实测

- 预购开始 **10 月 16 日晚 8 点**，发售 10 月 23 日；之前页面显示 **`暂未发售`**
- **该页提交控件是「继续」，不是「添加到购物袋」**（与 iPhone 18 Pro 页不同！）

  ```
  <button class="button button-block rc-summary-button-height" type="button"
          disabled="" data-autom="continueButton">继续</button>
  ```

  → 选择器 **`button[data-autom="continueButton"]`**；带 `[disabled]` = 未开卖
- ⚠️ **不要用 `button[data-autom="add-to-cart"]` 探测 Duo 页** —— 该元素根本不存在，会白等满超时（实测 10s + 4s）
- `input[data-autom="noapplecare"]` 两页通用（同一组件）
- Duo 特有：**仅支持 eSIM**，需到运营商线下营业厅核验身份证件激活
- Duo 512GB 星光白色 RMB 17,999，税费另计约 RMB 2,077

## 8. 可复用的「探针」手法

想知道某控件此刻**是否存在 / 是否已启用**，用 `wait-for-element` + `state:"attached"` 当探针（无副作用、毫秒返回）：

```
基选择器        satisfied=false  → 该控件当前不存在
:not([disabled]) 变体 satisfied=true → 已启用
```

比读整页语义树便宜得多，适合「先探再动」。

---

## 9. 结账全链路实测（secure6 域）

**核心事实：结账在独立域 `secure6.www.apple.com.cn`，商店层登录态不继承。**
点「结账」会跳到 `/shop/signIn?ssi=…` 登录墙。登录/验证码一律走 `bsk_assist request-help`，**agent 绝不碰密码**。
（实测：用户以为已登录但结账仍要求登录；登录后 URL 变 `?_s=Fulfillment-init`。）

**用 URL 的 `_s=` 参数当门控标记**（比选择器稳）：

| 步骤 | URL 标记 | 页面标题 |
|---|---|---|
| 登录墙 | `/shop/signIn?ssi=…` | 登录 — 安全结账 |
| 订单选项 | `?_s=Fulfillment-init` | 订单选项 — 安全结账 |
| 送货详情 | `?_s=Shipping-init` | 送货详情 — 安全结账 |
| 付款详情 | `?_s=Billing-init` | 付款详情 — 安全结账 |
| 查看订单 | `?_s=Review` | 查看订单 — 安全结账 |
| 下单成功 | `/shop/checkout/thankyou` | 谢谢：订单确认 |

**步骤与控件**（每步点「继续」后是异步推进：按钮变 `[disabled]` + 页面出现 `status "正在处理"`，需等下一屏渲染）：

```
Fulfillment-init
  为我送货(默认 checked) / 我要取货
  送货方式 radio(默认 checked，如 2026/10/23–10/30 免费)
  邮编位置按钮 → 「继续填写送货地址」

Shipping-init
  选择地址：默认地址 radio [checked]（登录后自动带出）/ 「使用新地址」
  联系人手机号码 · 发票类型(默认「电子发票 - 个人」) · 发票抬头(选填)
  → 「继续选择付款方式」

Billing-init                      ★ 微信支付在这里
  常用支付方式：支付宝 ="ALIPAY"   微信支付 ="WECHAT"
  分期付款方案：花呗分期 / 微信分付 / 招商银行 / 中国建设银行 / 工商银行
                （值形如 installments0001243254）
  其他支付方式：信用卡 ="CREDIT"
  → 「检查订单」

Review（只读汇总：地址 / 发票 / 付款方式 / 总计）
  ★ 最终提交： button[data-autom="continue-button-placeOrder"]
              或 #rs-checkout-continue-button-bottom   「立即下单」
```

**微信支付选择器：`input[value="WECHAT"]`**

**边界**：点「立即下单」才会真实创建订单，**之后**才出现微信二维码；QR 属 phone-only scan，必须用户扫。

**异步推进的正确等法**（拿"下一屏才有的元素"当门控）：

| 推进 | 门控 |
|---|---|
| Fulfillment → Shipping | `wait-for-element input[type="text"] state=attached` |
| Billing → Review | `wait-for-element input[value="WECHAT"] state=detached`（实测 3275ms） |

**时区/账号小坑**：登录框会把 11 位中国手机号（如 `136xxxxxxxx`）误格式化成 `+1 (361) xxx-xxxx` 的美国号码样子——**账号没错，别被吓到**。

**下单后的实测（闭环，2026-10 验证）**：

- 点 `button[data-autom="continue-button-placeOrder"]` → **同标签页**跳 `/shop/checkout/thankyou`，标题「谢谢：订单确认」，**不开新标签**
- 该页即出现微信二维码：「请使用你的微信扫描此二维码进行付款。」+「请在 **30 分钟内**完成付款，以免订单被取消。」+「使用微信扫码支付」
- 订单号形如 `#W1827818019`，位于二维码下方
- ⚠️ **二维码 30 分钟时效**；不付款则订单自动取消、无扣款
- ⚠️ **agent 的终点就是这一屏**：扫码属 phone-only scan，必须用户完成。用 `bsk_inspect screenshot` 把二维码截给用户即可
- ⚠️ 该点击会**真实创建订单**，只在用户明确授权时执行

### 9.1 结账各步按钮的稳定选择器（务必用选择器，别用 ref）

```
配送页「继续填写送货地址」   （无 data-autom，用 ref 或读一次）
配送页「继续选择付款方式」   button[data-autom="shipping-continue-button"]
付款页 微信支付               input[value="WECHAT"]
付款页「检查订单」           button[data-autom="continue-button-review"]
审查页「立即下单」           button[data-autom="continue-button-placeOrder"]
                              （或 #rs-checkout-continue-button-bottom）
二维码渲染完成门控           wait-for-element img[alt*="二维码"] state=visible
                              （实测 7.3 秒 ~ 30 秒以上；等待期间页面只有 "正在处理" 转圈）
```

### 9.2 ⚠️ 布局位移坑（本次真实踩到）

**选中付款方式后，页面会插入一行「你将在检查订单并下单后进行支付。」** → 后面的「检查订单」按钮**位置下移**。
此时若用**位移前读到的 `@eN` ref** 去点，会点到错的位置、**静默不推进**（工具照样回报 `clicked at (x,y)`）。
→ **结账链路上的按钮一律用 `data-autom` 选择器**，它不受布局位移影响。

### 9.3 访客订单 vs 账号订单

- 商店域登录**不**等于结账域登录；但**一旦在 secure6 登录成功，会话会保留**，后续点「结账」可直接进 `?_s=Fulfillment-init`（实测：不再出现登录墙）
- 登录墙上除登录表单外还有 **「以游客身份继续」**；走这条路 → 订单记为**访客订单**
- 判据：访客订单页标题为「访客订单」，URL 为 `/shop/order/guest/<单号>/<token>`，且页面出现 **「使用你的 Apple 账户登录，可更改订单…」+ 「登录」按钮**
- 访客订单**页面没有任何自助取消控件**（实测探测 `a[href*="cancel"]`、`button[data-autom*="cancel"]` 均不存在）；页面只给 `@eN button "登录"` 和 `@eN link "继续使用微信支付"`
- ⚠️ **想立刻取消**：只能在订单页点「登录」后操作（登录属 agent 禁区，走 `request-help`），或致电 400-666-8800
- ✅ **最省事的取消 = 什么都不做**：不付款，等 30 分钟倒计时结束自动取消，不扣款
- ⚠️⚠️ **关键陷阱**：访客结账会留下 **checkout session cookie**，之后点「结账」**可能完全不出现登录墙**——**这不代表账号已登录！**
  实测：第二次结账无登录墙、一路走完，订单**仍然是访客订单**。
  → **判据永远看订单页**：出现「使用你的 Apple 账户登录，可更改订单…」+「登录」按钮 = 访客单。
  商店页显示「个人收藏」只证明**商店域**登录，不证明结账归属。

---

## 10. 预购开闸抢购机制（已实测验证）

**两级探针（缺一不可）**：

```
存在: button[data-autom="continueButton"]                 → 商店在线
启用: button[data-autom="continueButton"]:not([disabled])  → 已开闸（真正要等的信号）
```

实测：未开卖时 `存在=true / 启用=false`；开闸后两者皆 true。**分得干净，不会误判。**

**必须用 bsk CLI 而不是插件工具**（`~/.local/bin/bsk.exe`，配 `BSK_AUTO_START=0`）——
只有 CLI 能做后台循环：`navigate` / `reload --hard` / `wait-for-element --selector --state --timeout --json` /
`wait-ms` / `get-html` / `evaluate` / `debug rule_*`。

**实测结论**（三种故障都真跑过）：

| 场景 | 现象 | 结果 |
|---|---|---|
| 维护「进不去」 | mock 503 +「我们马上回来」 | 按钮不存在 → 抓出标记文字 + 每 ~5s 重试 |
| 限制解除 | 规则 `times:3` 用尽后自动失效 | **自动发现恢复，零人工介入** |
| 开闸 | `evaluate` 去掉 `disabled` | **1 次探测判定开闸，退出码 0**，随即触发购买链 |
| 伪造启用但后端拒单 | 真实后端仍拒绝 | 报 `提交后 URL 未变化` 退出码 3 —— **如实失败，不假装成功** |

**两个硬约束**：

1. **`one command per session`** —— 守护进程对同一会话**同时只允许一条命令**。
   → 监控运行期间**无法再操作该会话**；必须"监控判定开闸 → **退出** → buy.sh 接管"。
   ⚠️ **绝不要同时跑两个 monitor**：会互抢会话、日志交错、行为不可预期。
2. **调试规则 id 形如 `<run-id>:rN`**（如 `dafc4cff8663f:r2`）；用裸 run id 删除会静默失败 → 规则残留叠加。
   - 规则 `match` 默认 Scope 是 Fetch/XHR；要拦文档必须显式 `"resource_type": "Document"`
   - `times: 0` = 永久；`times: N` = 命中 N 次后自动失效（**可用来自动模拟"限制解除"**）
   - `mock` 支持 `delay_ms`（0..10000）→ 模拟网络延迟；`block` → 模拟完全进不去
   - 规则「**first match wins**」：多条同匹配规则时，先加的赢，后面的永远不命中
3. 加规则前必须先 `debug start`（`network_controls.capture_required: true`）；
   清理用 `debug stop`（自动解除规则）+ `reload` 还原被 `evaluate` 篡改的 DOM。

---

## 11. 耗时预算（CDP 域实测，别用外部轮询）

**结论先行：Apple 结账是「网络受限」，不是「渲染受限」。**
主线程 long task 全程只有 0–2 个、合计 51–126ms（最长 102ms），而文档 DCL 可达 **7.5 秒**。
→ **"点了要转圈" = 在等服务端，不是等浏览器算。** 所以优化方向是"确认服务端回来"而不是"等渲染"。

### 端点级真实耗时（`debug aggregate --slow-ms 200`）

| 端点 | 次数 | 平均 | 最大 | 对应步骤 |
|---|---|---|---|---|
| `/shop/fulfillment-messages` | 10 | 815ms | 960ms | **结账 → 订单选项（实测 8.1s）** |
| `secure6/shop/checkoutx/fulfillment` | 1 | **4161ms** | 4161ms | **继续填写送货地址 → 送货详情（实测 4.2s）** |
| `secure6/shop/bag/status` | 1 | 3205ms | | 购物袋状态 |
| `secure6/shop/checkout` | 1 | 2982ms | | 结账引导 |
| `secure6/shop/checkout/start` | 1 | 1281ms | | 结账启动 |
| `/shop/favoritesx/fetch` | 2 | 803ms | 1263ms | **「个人收藏」异步加载的源头** |
| `/shop/bag` · `recommendedForYou-full` · `sba/d/entry` | 各 1 | 1.2–1.7s | | 页面级 |
| `/shop/updateSummary` | 3 | 163ms | 390ms | 配置变更后摘要刷新 |
| `/shop/updateSEO` · `product-gallery` · `applecare/data` · `engrave` | 3–6 | **37–48ms** | 110ms | **配置点击"秒生效"的原因** |
| `secure6/search-services/.../defaultlinks` | 1 | **6588ms** | | 可疑拖累项 |

### 文档级指标（`debug performance`）

| 页面 | TTFB | DCL | Load | long task 数/总/最大 |
|---|---|---|---|---|
| 购买页（首屏） | 1035ms | 1310ms | 2354ms | 2 / 126ms / 65ms |
| 购买页（SKU 直达） | 6ms | 149ms | 1308ms | 2 / 107ms / 56ms |
| 购物袋 | 1485ms | 1724ms | 2674ms | **0 / 0 / 0** |
| `secure6 _s=Shipping-init` | 2120ms | **7494ms** | **7589ms** | 1 / 51ms / 51ms |

### 等待预算（写脚本按这个设超时）

| 步骤 | 实测 | 建议超时 | 门控条件 |
|---|---|---|---|
| 配置项 5 连击 | **~55ms 就绪** | 8s | 等下一组的 `:not([disabled])` |
| 添加到购物袋 | ~1.3s | 25s | URL 到 `step=attach` |
| 结账 → 订单选项 | **~8.1s** | 30s | URL 到 `Fulfillment-init` |
| 继续填写送货地址 → 送货详情 | **~4.2s** | 20s | URL 到 `Shipping-init` |
| 继续选择付款方式 → 付款详情 | 10–20s | 30s | URL 到 `Billing-init` |
| 选微信支付 | ~51ms | 8s | `:checked` |
| 检查订单 → 查看订单 | 12–20s | 40s | URL 到 `_s=Review` |
| 立即下单 → 二维码 | 7–34s | 45s | `img[alt*="二维码"]` visible |

### 两个必须记住的坑

1. **到达新步骤后要等按钮"启用"再点**：脚本曾在 `Shipping-init` 上立刻点
   `shipping-continue-button` → **点空、后续连锁 TIMEOUT**。到达 Shipping 时页面仍在做
   `checkoutx/fulfillment`(4.2s)、`checkout/start`、`bag/status` 等调用，按钮尚未就绪。
   → 门控用 `...:not([disabled])`，**不要只用"存在"**。
2. **"正在处理"探针只能用 `img[alt*="正在处理"]`**，**不要用 `[role="status"]`**
   —— 后者每个页面都有，会永远误报"在转圈"（实测 `satisfied:true` on idle page）。
3. ⚠️ **限购会"静默拦截"结账（最阴的一种失败）**：购物袋里同一 iPhone 超过 **2 部**时，
   袋页出现 `alert "每名顾客最多可购买 2 个 iPhone 18 Pro。在结帐之前，请调整订单中 iPhone 18 Pro 的总数。"`，
   此时点「结账」**完全无反应**——不报错、不跳转、按钮也不是 `[disabled]`，
   表现得就像"点空了"，会让人误判成门控问题。
   → **结账前必须预检**：`get-html | grep -q '最多可购买'` 命中则先调整数量。
   → 数量控件是 **textbox**（`fill` 后**需 reload 才反映到 DOM**，但服务端即时生效）；
     或直接点该行的 `移除` 清空。

### 工具选择

- **准**：`bsk debug aggregate --slow-ms N`、`bsk debug performance`、
  `bsk debug requests --fields '...,duration_ms'`
- **粗**：外部轮询测墙钟（轮询间隔 120–150ms + 每次命令 ~160ms 开销）→ 只能判"快/慢"，不能定量
- **注意 `bsk tab list` 是表格格式**（TAB/SCOPE/WIN/TITLE/URL），**读 URL 要用 `--json`** 再解析
- 容器里**没有 jq**，但有 `python` 和 `node` 可用于解析 JSON

---

## 12. 购买入口：路径排名与重试策略（实测）

### 三条路（n=5，口径：出发 →「提交按钮已启用」，含必要配置点击 —— 真实口径）

| 路 | 入口 | 最快 | **中位** | 最慢 | 均值 | 排名 |
|---|---|---|---|---|---|---|
| **A** | 深链 SKU `/shop/buy-iphone/<机型>/<sku>` | 976ms | **1025ms** | 1433ms | **1102ms** | 🥇 |
| **C热** | `/shop/bag` **已预热** → 点「继续」 | 1250ms | **1284ms** | 1694ms | **1361ms** | 🥈 |
| **B** | 通用购买页（手配 3 项） | 1446ms | **1488ms** | 2916ms | **1764ms** | 🥉 |
| **C冷** | 现加载 `/shop/bag` → 收藏 → 继续 | 2599ms | **3289ms** | 3651ms | **3131ms** | ❌ |
| D/E | 首页导航菜单 / 商品页 →「购买」 | 步数更多，未实测 | | | | |

（B 的首个样本 2916ms 是冷缓存离群值；其余 4 次 1446–1504ms 很稳。）

⚠️ **更正**：早前记的「A 236ms 🥇 / B 206ms 🥉」只是**页面加载到出现配置控件**的时间，
**不含必要配置与折抵/AppleCare 点击**，口径不对，已作废。

**为什么 A≈B 而 C 慢一倍**：A/B 的耗时主要不在入口，而在
**「折抵 → AppleCare」两级门控等待**（各 ~0.5–1s，背后是 `updateSEO`/`updateSummary` 等 XHR）。
配置点击本身只要 **60–100ms/次**，所以"B 要手配 3 项"几乎不增加成本。
C 多出的 ~1.7s 全在 购物袋页加载 + 收藏异步 `favoritesx/fetch` + 点「继续」。

**策略修正**：**路 B 可作为首选，甚至优于 A** —— 同速，且不依赖深链 URL、不依赖收藏内容
→ 失败模式最少，也是唯一能在"深链 URL 挂掉"时存活的路。
路 A 的独特价值是 **SKU 精确**（不会配错机型/容量）。
路 C（人的正常手点路径）**最慢**，且终点 URL 与 A 相同。

### 预热的影响（n=5 实测）—— 决定性的优化点

| 场景 | 最快 | 中位 | 最慢 | 均值 |
|---|---|---|---|---|
| ① 购物车页加载（含收藏渲染） | 1149ms | **1445ms** | 1621ms | 1412ms |
| ② **C热**：购物车页已开着 → 只算「点继续之后」的增量 | 1250ms | **1284ms** | 1694ms | **1361ms** |
| ③ C冷：现加载购物车页的完整成本 | 2599ms | 3289ms | 3651ms | **3131ms** |
| ④ A 深链直达 | 976ms | **1025ms** | 1433ms | **1102ms** |

**结论**：
- **C热（1.28s）≈ A（1.03s）** —— 只要购物车页**已经开着**，「购物车 → 收藏 → 继续」
  和深链直达**基本一样快**（差 0.25s，可忽略）
- **C冷（3.29s）** 多出的 ~2s **全部来自"现加载购物车页"**（≈1.4s 页面 + 收藏异步）
- 数值自洽：`C冷 3.13s ≈ 购物车加载 1.41s + C热 1.36s`
- → **关键不是选路，而是预热**。19:55 就把购物车页开着，20:00 到了直接点「继续」即可。

**预热购物车页优于预热购买页**：点「继续」会落到**新的**购买页（自动是开卖状态）；
而预先停在购买页会保持"暂未发售"的旧状态，20:00 仍需一次 reload（≈1s）。

路 C 两次采样明细：

```
购物袋页就绪      1512 / 1535 ms
收藏区出现        1673 / 1699 ms      ← 用 --wait-until load 加载，收藏区基本同时就绪，通常无需重载
点「继续」→购买页  2018 / 1025 ms
合计             3691 / 2724 ms      配置已带 ✓
```

### ⚠️ 决定性的结构事实：A 与 C 汇聚到同一个 URL

`收藏 → 继续` 的落点**就是**路 A 的深链 URL。→ **那条 URL 一挂，A 和 C 一起挂。**
此时唯一真正不同的路是 **B**；若 B 也挂，说明是**维护态，只能等**（换路解决不了）。

### 重试策略：最快的那条必须先重试，不能一次失败就降级

```
路A  连试 3 次，间隔 2s / 3s / 5s（递增退避）
     ├─ 出现「我们马上回来」/503  → 判定【维护】：启动 monitor 轮询，而不是死磕换路
     └─ 连续 3 次拿不到购买页控件 → 降级
路C  连试 2 次（每次允许最多 3 次 reload 等收藏区）
     └─ 失败 → 降级
路B  连试 2 次；成功则手动配 机型 / 外观 / 存储 三项
     └─ 失败 → 判定不可达，回到 monitor 轮询
```

**为什么必须重试而不是立刻换路**：预购开闸瞬间极易出现**瞬时 5xx / 半开状态**，
第一次失败常常是"门刚开一条缝"，几秒后同一条路就通了；此时换路反而绕远
（C 要 ~3s，B 还要手动配 3 项）。

**故障演练已验证（n=5，用 `debug` 规则阻断深链文档）**：5/5 行为完全一致 ——

```
路A 试 3 次（2s / 4s 递增退避）→ 路C 试 2 次 → 路B 试 1 次成功
每轮 80–83 秒；零抖动
```

同时**证实了那条结构推断**：**路C 同样失败**（它落在与 A 相同的 URL 上）
→ **A 与 C 同生共死，B 是唯一能兜底的路**。
→ 因此实战排序建议：**首选 A（快+准），A 挂则 B（唯一活路）；不要指望 C。**

### 两个反直觉的实测结论

1. **首页的购物袋图标不是链接，是 flyout**：
   ```html
   <li id="globalnav-bag" data-topnav-flyout-label="打开购物袋"
       class="globalnav-item globalnav-bag"
       data-globalnav-iconflyout-enabled="true">
   ```
   - 点它**打开浮层**，URL 不变；**首页上没有任何指向 `/shop/bag` 的链接**（grep 零命中）
   - ⚠️ 浮层里**不显示「个人收藏」**（两次实测，14.4s 内未出现收藏链接）
   → 从首页到收藏必须先"开浮层 → 查看购物袋 → 等整页加载"，**比直接导航 `/shop/bag` 还多一步**。
   → 脚本要进购物袋页：**直接导航 `/shop/bag`**。
   → 没有 `aria-label` 含"购物袋"的元素，入口标签在 `data-topnav-flyout-label` 上，别用 aria-label 选它。
2. **配置是否已带必须探测，不能假设**：深链 A/C 会带配置，
   通用页 B 不带。用 `input[value="6_3inch"]:checked` 判断，据此决定是否要配 3 项。
