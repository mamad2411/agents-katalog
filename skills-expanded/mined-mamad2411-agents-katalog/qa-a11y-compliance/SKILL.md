---
name: qa-a11y-compliance
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
description: >-
  QA child skill - accessibility compliance: axe scan + WCAG 2.2 A/AA checklist, keyboard-only nav, focus order/trap/visible, accessible name, form label and error association, contrast, reduced motion, ARIA misuse. An axe pass alone is not an a11y pass. Owns parent section 4 Layer 8.
---

# qa-a11y-compliance

## 1. Position

无障碍合规 skill。**自动化工具（axe-core/pa11y/Lighthouse a11y）仅能检出约 57% 的 WCAG 2.2 success criteria（其余约 43% 必须人工 / 半自动验证）**——业界量化口径（Deque/WebAIM 一致：纯自动化覆盖率上限约 30–57%，取乐观上限 57%）。本 skill 区分三档：automated（axe/pa11y/Lighthouse）/ semi-automated（脚本辅助 + 人工）/ manual（必须人工跑，含真实屏幕阅读器）。**axe / pa11y 全绿不能宣布 a11y pass。**

**目标合规级别：WCAG 2.2 Level AA**（commercial-cert 的 hard gate 目标）。WCAG 2.2 共 **87 个 success criteria**（A=32 / AA=24 / AAA=31；A+AA 合计 56 个是 AA 合规必须全过的集合）。

## 2. Triggers

- Parent §6 Step 5（任何 UI 变更 — a11y 是 mandatory layer）
- form / modal / nav / menu / table / dashboard / chart 变更
- public page / marketing site
- keyboard / screen reader 风险
- WCAG compliance 法规要求（公共部门 / 欧盟 EAA / 美国 ADA）

## 3. Responsibilities

- **axe scan**（automated）：axe-core / @axe-core/playwright / vitest-axe
- **WCAG 2.2 A/AA checklist**（semi-automated + manual）
- **Keyboard-only nav**：Tab / Shift+Tab / Enter / Space / Esc / arrows
- **Focus order**：DOM order vs visual order
- **Focus trap**：modal / dialog / dropdown
- **Visible focus**：CSS outline / box-shadow
- **Accessible name**：button / link / icon-only button
- **Form label / error association**：label + input + aria-describedby
- **Color contrast**：4.5:1 normal text，3:1 large text
- **Reduced motion**：`prefers-reduced-motion` 支持
- **ARIA misuse**：role 冗余 / hidden 元素 focusable / 错误的 aria-live

## 3.5 WCAG 2.2 standard detail

### Standard summary

- **Version**: WCAG 2.2（W3C Recommendation, 2023-10-05；2024-12 勘误版为现行）。向后兼容 2.1 / 2.0：满足 2.2 即满足 2.1/2.0。
- **Conformance target**: **Level AA**（A + AA 全过）。AAA 不作为通用 gate（部分准则无法对整页满足）。
- **Totals**: 87 success criteria（A 32 / AA 24 / AAA 31）。

### WCAG 2.2 新增的 9 条 success criteria（相对 2.1，必须显式覆盖）

| SC | Level | 名称 | 验证档 |
|---|---|---|---|
| 2.4.11 | AA | Focus Not Obscured (Minimum) | semi-automated + manual |
| 2.4.12 | AAA | Focus Not Obscured (Enhanced) | manual（仅 AAA 目标时）|
| 2.4.13 | AAA | Focus Appearance | manual（仅 AAA 目标时）|
| 2.5.7 | AA | Dragging Movements（拖拽须有单指替代）| manual |
| 2.5.8 | AA | Target Size (Minimum)（≥24×24 CSS px）| semi-automated（可脚本量测）+ manual |
| 3.2.6 | A | Consistent Help（帮助入口位置一致）| manual |
| 3.3.7 | A | Redundant Entry（避免重复录入）| manual |
| 3.3.8 | AA | Accessible Authentication (Minimum)（不依赖认知谜题）| manual |
| 3.3.9 | AAA | Accessible Authentication (Enhanced) | manual（仅 AAA 目标时）|

> 注：WCAG 2.2 同时**移除**了 4.1.1 Parsing（已废弃，恒视为满足）。AA gate 实际新增需关注的是上表中 6 条 A/AA（2.4.11 / 2.5.7 / 2.5.8 / 3.2.6 / 3.3.7 / 3.3.8）。

### 工具枚举（automated 档）

| 工具 | 引擎 | 适用 | 备注 |
|---|---|---|---|
| `axe-core` | axe | 通用 DOM 规则引擎 | 业界基准；零误报导向 |
| `@axe-core/playwright` | axe | E2E 集成（Playwright）| QA 主路径 |
| `@axe-core/react` / `vitest-axe` / `jest-axe` | axe | 组件/单测级 | 组件库回归 |
| `pa11y` / `pa11y-ci` | HTML_CodeSniffer 或 axe（可切）| CLI 批量 URL 扫描 + CI gate | 支持 `--standard WCAG2AA`、阈值 `--threshold` |
| `Lighthouse` a11y category | axe（子集）| 单页快速评分 | 仅子集，不可替代 axe/pa11y 全量 |

> 任一自动化工具的 violations 都按 impact 归一到 `critical / serious / moderate / minor`（见 §6 / schema）。

## 3.6 Toolchain landing（concrete CLI — CLI-first, free + OSS, Q6）

> 加入 2026-06-15（Q6 — a11y 工具链落地，纯能力，**零新 gate**）。§3.5 枚举了"有哪些工具"，本节落地"**具体怎么装、怎么跑、怎么进 CI**"。全部 free + OSS，CLI-first（不依赖任何付费 SaaS / MCP）。runner（`qa-a11y-runner`）只跑**项目已安装**的工具，缺失即 `decision_hint: WARN`（tool absence 是项目缺口，不是 regression）——所以本节是"建议项目装这套"，不是 runner 私自 `npm install`。

### 3.6.1 四个工具的安装命令（按需选，不必全装）

| 工具 | 安装命令 | 引擎 | 最适合 |
|---|---|---|---|
| `@axe-core/playwright` | `npm i -D @axe-core/playwright @playwright/test` | axe-core | **QA 主路径** — E2E 集成、跑真实渲染后的页面 / 交互态 |
| `@lhci/cli`（Lighthouse CI） | `npm i -D @lhci/cli` | axe-core 子集 | 单页快速评分 + CI assertion（a11y category score gate） |
| `pa11y-ci` | `npm i -D pa11y-ci` | HTML_CodeSniffer 或 axe（可切） | CLI 批量多 URL 扫描 + threshold gate |
| `vitest-axe` / `jest-axe` | `npm i -D vitest-axe`（或 `jest-axe`） | axe-core | 组件 / 单测级回归（设计系统组件库） |

> 选型建议：**有 Playwright E2E → 首选 `@axe-core/playwright`**（跑交互后真实 DOM，覆盖最全）；**只有静态页 / 想要分数门 → `@lhci/cli` 或 `pa11y-ci`**；**组件库 → 加 `vitest-axe` 做单测级回归**。三档可叠加。

### 3.6.2 各工具的 runner 调用命令（runner 自动发现并执行）

`qa-a11y-runner` 按 `devDependencies` 自动发现已装工具，跑对应命令，输出机器可读 JSON 作 evidence：

```bash
# A. @axe-core/playwright（QA 主路径）— 在 Playwright test 里 import + analyze，跑带 @a11y tag 的 spec
npx playwright test --grep @a11y --reporter=json

# B. Lighthouse CI（a11y category）— 单页评分，JSON 输出
npx lhci autorun --collect.settings.onlyCategories=accessibility
#   或单次：npx lighthouse <url> --only-categories=accessibility --output=json --quiet --output-path=a11y-lh.json

# C. pa11y-ci（批量 URL + WCAG2AA 标准）— .pa11yci 配置 urls + threshold
npx pa11y-ci --json > a11y-pa11y.json
#   或单 URL：npx pa11y --standard WCAG2AA --reporter json <url>

# D. vitest-axe（组件级）— 在 component test 里 expect(await axe(container)).toHaveNoViolations()
npx vitest run --reporter=json a11y
```

**axe Playwright 用法骨架**（项目侧 spec，runner 跑它、不写它）：

```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('checkout page @a11y', async ({ page }) => {
  await page.goto('/checkout');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])  // §3.6.4 标签映射
    .analyze();
  expect(results.violations).toEqual([]);  // gate：critical/serious 见 §6.5 floor
});
```

`pa11y-ci` 配置骨架（`.pa11yci`，`WCAG2AA` 标准 + threshold）：

```json
{
  "defaults": { "standard": "WCAG2AA", "threshold": 0, "timeout": 30000 },
  "urls": ["https://staging.example.com/", "https://staging.example.com/checkout"]
}
```

### 3.6.3 CI wiring（GitHub Actions — a11y job 进 release gate）

> a11y 进 CI 是 §4 Layer 8（含 HTML 输出的 surface 必跑）+ commercial-cert 的 hard gate（§6.5 floor）。下面是最小可用 job 骨架（注入 staging URL，evidence 上传给 `qa-evidence-bundle` 引用）：

```yaml
# .github/workflows/qa-a11y.yml （或并入既有 qa job）
a11y:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with: { node-version: 20, cache: npm }
    - run: npm ci
    - run: npx playwright install --with-deps chromium   # 仅 @axe-core/playwright 路径需要
    # 主路径：axe + Playwright（真实渲染）
    - run: npx playwright test --grep @a11y --reporter=json > a11y-axe.json
      continue-on-error: true     # 由 deterministic A11yGate / qa-evidence-bundle 裁决，不靠 step exit
    # 可选：Lighthouse a11y 分数门
    - run: npx lhci autorun --collect.settings.onlyCategories=accessibility || true
    # 可选：pa11y-ci 批量
    - run: npx pa11y-ci --json > a11y-pa11y.json || true
    - uses: actions/upload-artifact@v4
      with: { name: a11y-evidence, path: "a11y-*.json" }
```

> **裁决归 gate，不靠 CI step exit**：CI step 用 `continue-on-error`/`|| true` 收集证据即可；PASS/WARN/BLOCK 由 §6.5 `a11y_gate_policy`（workflow 模式）或 `qa-evidence-bundle`（prompt-only）按 floor 裁决。**绝不**为了 step 变绿而放宽阈值（违反父级 Hard Rule §2.7 + §8 Forbidden）。

### 3.6.4 WCAG 2.2 AA ↔ axe tag 映射（自动化覆盖哪些、漏哪些）

axe-core 用 `withTags()` 选规则集。覆盖 WCAG 2.2 AA 需挂全下列标签；但**自动化仅约 57% SC 可机检**（§1），剩余须 §3.5 manual 档补：

| axe tag | 覆盖 | 机检性 |
|---|---|---|
| `wcag2a` / `wcag2aa` | WCAG 2.0 A/AA | 自动 |
| `wcag21a` / `wcag21aa` | WCAG 2.1 新增 A/AA | 自动 |
| `wcag22aa` | WCAG 2.2 新增 AA（部分，如 2.4.11 Focus Not Obscured 的可机检子集） | 部分自动 |
| `best-practice` | axe 最佳实践（非 WCAG 强制） | 自动（advisory） |

**axe 标签覆盖不到、必须 manual / semi-automated 的 WCAG 2.2 新增 A/AA**（与 §3.5 表一致）：`2.5.7` Dragging Movements（manual）· `2.5.8` Target Size（semi-automated 可脚本量测 ≥24×24px）· `3.2.6` Consistent Help（manual）· `3.3.7` Redundant Entry（manual）· `3.3.8` Accessible Authentication（manual）。→ 这 5 条是 §3.5 "axe 全绿 ≠ AA pass" 的具体落点。

## 4. Non-responsibilities

- 不替代真正屏幕阅读器人工测试（NVDA / JAWS / VoiceOver 测试需 owner 安排）
- 不做完整 manual audit（小范围 spot check）
- 不实施访问控制 / 不做安全（a11y ≠ security）

## 5. Workflow

1. 识别 a11y targets（route / component）
2. Run `axe` automated scan
3. 跑 keyboard-only nav 脚本检查
4. Manual spot-check：focus order / focus trap / accessible name / contrast
5. WCAG 2.2 checklist sign-off
6. Output `a11y_compliance` YAML

## 6. Output Contract

```yaml
a11y_compliance:
  standard: WCAG_2_2_AA
  scope:
    routes: [...]
    components: [...]
  automated_scan:
    tool: axe-core | @axe-core/playwright | vitest-axe
    violations:
      critical: 0
      serious: 0
      moderate: <N>
      minor: <N>
    artifact: <a11y-report.json or junit>
  semi_automated:
    keyboard_navigation_passed: true | false
    focus_order_passed: true | false
    focus_trap_passed: true | false  # for modal / dialog
    visible_focus_passed: true | false
  manual_checks:
    accessible_name_audit:
      buttons_checked: <N>
      icon_only_buttons_with_label: <N> / <total>
    label_association_audit:
      forms_checked: <N>
      label_input_pairs_correct: <N> / <total>
    color_contrast_audit:
      normal_text_min_ratio: 4.5
      large_text_min_ratio: 3.0
      failures: []
    reduced_motion_audit:
      prefers_reduced_motion_supported: true | false
    aria_misuse_audit:
      issues: []
  exceptions:
    - rule: <WCAG ID>
      reason: <approved exception>
      owner: <github handle>
      expiry: <date>
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

## 6.5 Hard threshold (DOUBLE-WRITE — workflow mode 才会拦)

> 在 prompt-only 模式下本 skill 给 advisory decision；在 **workflow-spec 模式（commercial-cert）** 下，拦截由 deterministic `a11y_gate_policy` op 完成。要让它真的拦，目标级别 + violations 阈值必须**双写**：同步进 `A11Y_AUDIT_SCHEMA` 与 `a11y_gate_policy` 的 floor。否则 gate 拿不到阈值，workflow 模式不拦。

**Canonical a11y floor（已双写，2026-06-05）**：

| 项 | 值 | gate 读取字段 |
|---|---|---|
| 目标级别 | WCAG 2.2 **AA** | `_target`（文档）|
| critical violations | **max 0** → 超出即 **BLOCK** | `ctx.policy.a11y_floor.max_critical` |
| serious violations | **max 0** → 超出即 **WARN** | `ctx.policy.a11y_floor.max_serious` |
| moderate / minor | advisory（报告，不自动拦）| — |

**双写位置（三处必须一致，字段名与 `qa-orchestrator.js` `a11y_gate_policy` 读取处逐字对齐）**：
1. Schema：`~/.claude/orchestrator-runtime/qa/schemas/A11Y_AUDIT_SCHEMA.v1.json` → `_canonical_threshold_policy`
2. Gate policy（baked default）：`~/.claude/orchestrator-runtime/qa/presets/commercial-cert.json` → `context.policy.a11y_floor`
3. Runtime：parent `enterprise-qa-testing` §18.5 step 13 把 `policy` 透传进 `Workflow` 的 `input.context.policy`（engine 在 `qa-orchestrator.js` 第 47 行读的是 runtime `input.context.policy`，**不是** preset 静态块——所以 Skill 必须把 preset 的 baked floor 复制/合并进 launch context）。

> decision 语义：`critical_count > max_critical => BLOCK`；`serious_count > max_serious => WARN`；否则 `PASS`。axe/pa11y 全绿仍只覆盖约 57% SC，AA gate 必须叠加 §3.5 manual 档。

## 7. Parent Integration

- Triggered by: parent §6 Step 5
- Returns: `a11y_compliance` YAML
- Consumed by: `qa-evidence-bundle` → `child_skill_results.a11y`

## 8. Forbidden patterns

- axe / pa11y 全绿就宣布 a11y pass（自动化仅约 57% SC 覆盖，其余须人工/半自动）
- 把 WCAG 目标级别 / violations 阈值只写进 schema 不写进 `a11y_gate_policy`（或反之）→ workflow 模式不拦（见 §6.5 双写）
- 漏跑 WCAG 2.2 新增的 6 条 A/AA（2.4.11 / 2.5.7 / 2.5.8 / 3.2.6 / 3.3.7 / 3.3.8）
- 接受 `aria-hidden="true"` 配合 focusable element
- 接受 icon-only button 无 accessible name
- 接受 color contrast < 4.5:1（normal text）
- 跳过 keyboard-only navigation
- 不验证 reduced motion 支持

## 9. References

- [WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/)
- [What's New in WCAG 2.2 (W3C)](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- [How to Meet WCAG 2.2 (quick ref)](https://www.w3.org/WAI/WCAG22/quickref/)
- [axe-core](https://www.deque.com/axe/)
- [@axe-core/playwright](https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright)
- [pa11y / pa11y-ci](https://github.com/pa11y/pa11y)
- [WebAIM — keyboard accessibility](https://webaim.org/techniques/keyboard/)
