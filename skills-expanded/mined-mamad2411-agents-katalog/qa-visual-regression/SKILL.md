---
name: qa-visual-regression
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
description: >-
  QA child skill - visual regression: Playwright `toHaveScreenshot()` / Storybook + Chromatic, with baseline lifecycle, ADR for first-time approval, viewport and theme matrix, deterministic settings (font/timezone/animation/locale), diff threshold lock and owner approval. Owns parent section 4 Layer 7.
---

# qa-visual-regression

## 1. Position

视觉回归测试 skill。CSS / layout / typography / spacing / theme / responsive 改动的最后一道防线。**首次 baseline 必须在 CI Docker 中 one-time approval（按 parent §2.2 + ADR 记录）**，本地 dev 机不允许生成正式 baseline。

## 2. Triggers

- Parent §6 Step 5（UI 变更 + risk 选了 Visual layer）
- CSS / layout / typography / spacing / theme 变更
- Design system component 变更
- Marketing / landing / dashboard 高可见页变更
- Pixel-sensitive UI（dashboard chart / brand homepage）

## 3. Responsibilities

- **Tool**：Playwright `toHaveScreenshot()`（主推）/ Storybook + Chromatic（如已集成）
- **Baseline lifecycle**：首次生成必须 CI Docker + one-time approval + ADR 记录
- **Viewport matrix**：mobile 320 / tablet 768 / desktop 1440（最小三档；按 product 加）
- **Theme matrix**：dark / light（同时存在则必测）
- **Deterministic settings**：lock font、timezone、animation（`prefers-reduced-motion`）、system locale
- **Diff threshold**：默认 0.2%，不允许为 pass 随意放宽
- **Owner approval**：每次 baseline 更新必须有 owner 签名

## 4. Non-responsibilities

- 不测交互（→ `qa-component-behavior` / `qa-e2e-coverage-gate`）
- 不替代 a11y（→ `qa-a11y-compliance`）
- 不本地随便 `--update-snapshots`（违反 parent §2.2）

## 5. Workflow

1. 识别 visual targets（route / component / story）
2. 选 viewport matrix + theme matrix
3. Lock 不确定性源（font / timezone / animation / locale）
4. 首次 baseline → CI Docker + ADR
5. PR diff check → 若 diff > threshold → 报告 + owner approval
6. Output `visual_regression` YAML

## 6. Output Contract

```yaml
visual_regression:
  tool: playwright_screenshot | chromatic | percy | mixed
  targets:
    - route_or_component: /dashboard
      viewports: [320, 768, 1440]
      themes: [light, dark]
  baselines:
    new_created: <N>
    updated: <N>
    approved_by: <github handle>
    adr_path: <docs/adr/visual-baseline-NNN.md>
    ci_image_hash: <hash>
  deterministic_settings:
    font_locked: true
    timezone_locked: UTC
    animation_disabled: true
    locale_locked: en-US
  diff_results:
    diff_threshold: 0.002
    max_diff_observed: <ratio>
    over_threshold_diffs: []  # if any, list each
  threshold_changed: false
  artifacts:
    screenshots_path: <playwright-report/...>
    diffs_path: <test-results/...>
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

## 7. Parent Integration

- Triggered by: parent §6 Step 5
- Returns: `visual_regression` YAML
- Consumed by: `qa-evidence-bundle` → `child_skill_results.visual`

## 8. Forbidden patterns

- 本地生成正式 baseline（必须 CI Docker）
- silent `--update-snapshots`（违反 parent Hard Rule §2.2）
- 调高 diff threshold 让 PR pass
- 跳过 dark theme 测试当项目同时支持 dark/light
- 不 lock font / timezone / animation 引起像素漂移

## 9. References

- [Playwright — visual comparisons](https://playwright.dev/docs/test-snapshots)
- [Storybook — visual tests](https://storybook.js.org/docs/writing-tests/visual-testing)
- [Chromatic](https://www.chromatic.com/docs/)
- Parent §2.2 first-baseline approval clause
