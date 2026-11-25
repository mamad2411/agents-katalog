# 这个仓库的协作约定

zeup330.github.io，纯静态站，push `main` 即自动部署。

## 两个 agent 同时在这里干活

这个仓库被多个 agent 会话共用过，出现过连续三次「A 的提交裹走了 B 正在写的文件」——
`git add -A` 会把对方未提交的工作一起提交，commit 信息和内容就对不上了。

因此：

- **各自用独立 worktree**。主目录 `~/github/ZEUP330.github.io` 走 `main`；
  第二个 agent 用 `~/github/site-b`，分支 `agent-b`：

  ```bash
  git worktree list                 # 看现有的
  cd ~/github/site-b && git status  # 第二个 agent 在这里干活
  ```

  两边是同一个 `.git`，但工作树和分支互相独立，谁也 `add` 不到对方的文件。
  完成后从 `agent-b` 合回 `main`。

- **永远不要 `git add -A` / `git add .`**，只 `git add` 明确路径。即使有了 worktree，
  这条仍然要守：worktree 防的是跨会话，路径显式防的是自己手滑。

- 提交信息只描述这次实际改的东西。裹进无关文件时，宁可拆成两条提交。

## 结构

```
index.html          主页
mortgage/           房贷年限 × 月供
housing/            全国房价走势地图      housing/data/  ← housing.yml 写入
options/            美股期权 wheel 筛选器  options/data/  ← options.yml 写入
macro/              美国经济数据 × 纳指     macro/data/    ← macro.yml 写入
changsha/           长沙行程
assets/theme.*      全站共享的样式底座（配色/字号/控件/动效）+ 三个行为，每页两行 include
assets/statusbar.*  全站共享状态栏（更新时间 + 抽签），每页两行 include
scripts/            两个采集脚本，在 Actions runner 里跑
```

## 几个踩过的坑

- **状态栏的 cron 表是硬编码的**。`assets/statusbar.js` 里的 `SETS[].cron` 必须和
  `.github/workflows/*.yml` 手工保持一致，页面读不到 workflow 文件，改了那边不改这边
  会静默偏差。
- **更新时间走 sidecar**。`*/data/status.json` 只有几十字节，专门给状态栏读；
  数据本体 158KB / 291KB，不要为了一个时间戳让每个页面都下载。
- **数据提交用 amend 压缩**。两个 workflow 都只在 HEAD 是自己的快照提交时才 amend，
  否则每次运行留一个 JSON blob，仓库很快就废了。手写的提交永远不会被改写。
- **图表用 CSS 变量上色时注意 canvas 读不到**。Chart.js / echarts-gl 里要写死 hex，
  inline SVG 才能用 `var(--ink)`。
- **`assets/theme.css` 必须排在页面自己的 `<style>` 之前**。顺序反了页面就再也覆盖不了它。
  它只管 token 和基础元素（body / h1-h3 / p / a / table / button / range / .card 一类），
  页面各自的 `main { max-width }` 和额外 token（`--warn`、`--call`…）仍留在页内。
- **theme.css 里的选择器不能用通名**。踩过三次，都是同一个原因：
  `button[aria-pressed="true"]` 会盖住 options/drawdown/changsha 自己的 chip 选中样式的
  文字色、留下它们的背景色，变成蓝底蓝字；`.warn` 同时是块级提示框和修饰词，
  于是 `<b class="hl warn">` 继承了提示框的 padding/border，变成一个压在下一行文字上的方块。
  修饰类一律带前缀（`.key--cost`、`.hl--warn`），填充选中态用 `.btn.on`。
  第三次是同一个 `.warn`：它还命中了状态栏的 `.zb-dot.warn`，把 8px 的圆点撑成带 padding
  和边框的提示框 —— **每一页都有**，而且是从提交那天起就一直在。已经把 `.warn` 从
  theme.css 的选择器里彻底去掉（提示框现在是 `.note`/`.alert-note`/`.callout`）。
  规则很简单：**共享样式表里不要占用任何一个会被当作状态词的通名**。
- **入场动画不能靠 IntersectionObserver 判可见**。观察器只报「跨过阈值」，用户一次跳到
  页尾时中间那几个元素从未相交，会永久停在 opacity 0。theme.js 改成按 rect 位置扫，
  并且 `.rise` 由 JS 加上 —— 关掉 JS 时内容必须是直接可见的。
- **本机连不上 Deribit**（公司网），但 Cboe 可以。采集脚本能不能本地跑要先测。
- **长沙页的实景底图必须免 key**。天地图授权更合适，但要申请浏览器端 key 并维护域名白名单，
  没人维护的 key 就是一张会静默失效的地图。现在用 Esri World Imagery（卫星）
  和 CARTO Positron/Dark Matter（矢量，跟随深浅色），两个都不用注册，attribution 挂在右下角。
  两个坑：坐标是 WGS84，**不要拿高德/百度的 GCJ-02 坐标**，会偏几百米；
  分节是 JS 包成 `<details>` 的，地图在收起状态下量不到尺寸，重新展开要 `invalidateSize()`。

## 数据与口径

页面上的金融与政策数字都要能追到官方来源，并标注核对日期。所有涉及钱的页面写明
「不构成投资建议」，年化、IV 这类数字要同时给出风险侧（Delta、缓冲、价差、杠杆标记），
不要只展示收益。
