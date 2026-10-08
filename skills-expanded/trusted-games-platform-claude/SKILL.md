# gomoku-react

P2P 棋类平台。monorepo (pnpm)。

## 结构
- `apps/web/` — React + Vite 前端
- `apps/signaling-cf/` — Cloudflare Workers 信令
- `packages/core/` — 共享逻辑（crypto、hash-chain）

## 开发命令
```bash
pnpm -F web dev
pnpm test
pnpm -F web build
```

## 新增游戏插件
参考 `apps/web/src/plugins/gomoku/`，需要：
- `index.js` — 插件入口
- `engine.js` — 游戏逻辑
- `Board.jsx` — 棋盘组件

着法必须兼容 `packages/core/src/crypto.js` 哈希链。

## 禁止改动
- `packages/core/src/crypto.js`
- 现有 gomoku 插件

---

## 🔁 自循环优化协议（Auto-Optimization Loop）

每轮执行以下流程，结果写入 `.claude/loop-report-{N}.md`：

### STEP 1 — 扫描（Scan）
- 读取所有 `apps/web/src/**` 和 `packages/core/src/**`
- 识别：重复逻辑、未使用导出、过深组件嵌套（>4层）、未处理 Promise、魔法数字

### STEP 2 — 提案（Propose）
对每个问题生成优化提案，格式：
```
[PROPOSAL-{id}]
文件: <path>
问题: <描述>
方案: <具体改法>
风险: LOW | MEDIUM | HIGH
影响范围: <列出受影响文件>
```

### STEP 3 — 剪枝（Prune）
自动标记以下为 ❌ 不合理分支，跳过执行：
- 风险=HIGH 且影响范围>3个文件
- 需要改动 `packages/core/src/crypto.js`
- 重构范围超过单个模块边界（跨 app/package）
- 与现有 gomoku 插件接口不兼容
- 纯风格改动（rename、格式化）无性能/逻辑收益

### STEP 4 — 执行（Execute）
只执行标记为 ✅ 的提案，每个提案：
1. 改动前运行 `pnpm test`，失败则跳过
2. 应用改动
3. 再次运行 `pnpm test`，失败则 git revert

### STEP 5 — 记录（Record）
写入 `.claude/loop-report-{N}.md`：
- 本轮执行的提案列表
- 被剪枝的分支及原因
- 测试结果
- 下一轮建议关注点

### 循环终止条件
满足任一则停止：
- 连续2轮无新提案
- 所有提案均被剪枝
- 测试覆盖率下降

---

## 精简 Prompt 策略（继承自 Claude Code 最佳实践）

> 来源：Anthropic Claude Code 官方工作流 + 社区 prompt 工程实践

1. **最小上下文原则** — 每次只传入当前任务相关文件，不全量读取
2. **结构化输出** — 用固定格式（PROPOSAL块）而非自由文本，便于解析和自动化
3. **显式边界声明** — 在 prompt 开头声明"禁止改动"范围，减少幻觉改动
4. **增量验证** — 每个原子改动后立即测试，不批量提交
5. **自我评审** — 每个提案生成后，先问"这个改动是否真的必要？"再执行
6. **失败快速** — 测试失败立即 revert，不尝试修复测试来掩盖问题
