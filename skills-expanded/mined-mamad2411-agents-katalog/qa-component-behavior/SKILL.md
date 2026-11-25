---
name: qa-component-behavior
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
description: >-
  QA child skill - component layer: React/Vue/Svelte/Angular component tests via Testing Library + jsdom or Storybook play, over the state matrix (default/loading/error/empty/success/disabled/permission-denied) plus keyboard and a11y smoke. No implementation-detail tests. Owns parent section 4 Layer 3.
---

# qa-component-behavior

## 1. Position

Component-layer 测试 skill。针对**同步 Client Components / 交互组件 / 表单 / shared UI library**。在 jsdom 或浏览器中渲染单个组件并验证用户可观察行为。

## 2. Triggers

- Parent §6 Step 5（默认 dispatch，当 §3 Layer Selection 选了 Component）
- React / Vue / Svelte / Angular 组件变更
- 表单校验、loading、empty、error、disabled、permission state 变更
- Storybook story / design system / shared component 变更
- UI 逻辑复杂但还没到 E2E

## 3. Responsibilities

- **Testing Library query priority**：`getByRole` > `getByLabel` > `getByText` > `getByPlaceholder` > `getByTestId`（fallback only）
- **`afterEach(cleanup)` 必配（高频假阳根因）**：多个 `render()` 而不 unmount 会让 DOM 在同一文件内**累积**，下一个 `getByRole`/`getByText` 撞到上一个 test 的残留节点 → 报 **"Found multiple elements with…"** 假失败（不是组件 bug，是测试卫生）。RTL 在 vitest globals / jest 环境下**通常自动 cleanup**，但**非 globals 模式（如 vitest `globals:false`）必须显式 `import { cleanup } from '@testing-library/react'; afterEach(cleanup);`**。命中"multiple elements"先查 cleanup，再考虑用 `getByRole(role, { name })` exact-match 收窄，而不是改断言去迁就脏 DOM。E2E 实测：首版组件测试因缺 cleanup 触发此假失败，补 cleanup 后即转绿。
- **Storybook `play` function**：在 story 上跑交互断言
- **State matrix**（必填）：
  - default
  - loading
  - error
  - empty
  - success
  - disabled
  - permission_denied
- **User interactions**：click / type / keyboard / focus
- **Component-level MSW**：mock 网络边界，不 mock 内部 hook
- **Basic a11y smoke**：role / accessible name / focus order

## 4. Non-responsibilities

- 不跑完整浏览器业务流（→ `qa-e2e-coverage-gate`）
- 不替代 unit tests（→ `qa-test-design-tdd-bridge`）
- 不替代完整 a11y（→ `qa-a11y-compliance`）
- 不写 implementation-detail tests
- 不 mock 被测组件内部的 hook 来"测自己"

## 5. Workflow

1. Pull components in scope from parent Step 3
2. List state matrix per component
3. Choose query priority for each interaction
4. Mock network with MSW（不 mock 组件内部）
5. Run `vitest run` or `storybook test`
6. Output `component_behavior` YAML

## 6. Output Contract

```yaml
component_behavior:
  components_under_test:
    - path: src/components/CheckoutForm.tsx
      state_matrix_covered: [default, loading, error, success, disabled]
      missing_states: [permission_denied]
  user_interactions:
    - { component: ..., action: click, locator: getByRole_button }
  accessibility_smoke:
    role_used_count: 12
    aria_label_used_count: 5
    testid_used_count: 1  # fallback only
  commands_run:
    - command: npx vitest run __tests__/components --reporter=verbose
      exit_code: 0
      stdout_excerpt: ...
  evidence:
    test_files: [paths]
    story_files: [paths]
    stdout: ...
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

## 7. Parent Integration

- Triggered by: parent §6 Step 5
- Returns: `component_behavior` YAML
- Consumed by: `qa-evidence-bundle` → `child_skill_results.component`

## 8. Forbidden patterns

- 用 CSS path locator（`.container > div:nth-child(2)`）
- mock 组件内部 hook 后断言自己
- snapshot-only assertion 不配合行为
- `data-testid` 作为首选 query（仅 fallback）
- 跳过 negative state（permission_denied / error / empty）

## 9. References

- [Testing Library — query priority](https://testing-library.com/docs/queries/about#priority)
- [Testing Library — guiding principles](https://testing-library.com/docs/guiding-principles/)
- [Storybook — interaction tests](https://storybook.js.org/docs/writing-tests/interaction-testing)
- [Vitest — browser mode (optional)](https://vitest.dev/guide/browser/)
