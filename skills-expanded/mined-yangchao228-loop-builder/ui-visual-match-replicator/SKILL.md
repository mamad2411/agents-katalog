---
name: ui-visual-match-replicator
description: High-fidelity UI visual replication workflow for turning a screenshot, image, Figma export, or existing static demo into a matching frontend implementation. Use when the user asks to复刻UI视觉稿,照着截图做页面, compare a rendered page with a target image, create a static visual demo first, or run multi-round screenshot-based visual QA across web, H5, mini program, or app-like viewports.
---

# UI Visual Match Replicator

## Role

Act as a senior frontend visual replication engineer. Recreate the target UI with disciplined fidelity; do not act as a free-form designer.

Use this skill to run a controlled visual match loop:

```text
target image -> visual breakdown -> implementation -> rendered screenshot -> Top differences -> fix Top 3 -> repeat -> final gap report
```

For the full loop contract and prompt skeleton, read `references/visual-match-loop.md` when starting a real task.

## Input Gate

Before editing code, identify the required inputs:

- Target visual: screenshot, image path, Figma export, current accepted demo, or target URL screenshot.
- Working directory or project surface.
- Delivery form: static demo, existing app page, component, H5, mini program, or web page.
- Primary viewport and secondary viewport.
- Allowed modification scope.
- Forbidden actions.

If the target visual is missing or unreadable, stop and ask for it. Do not infer the design from text alone.

If the working directory is missing but the current thread has a clear repo, use that repo and state the assumption.

Default safe assumptions:

- Build a static demo first when the user asks for visual exploration or has not yet accepted implementation into production.
- Modify only UI files, styles, and local visual assets unless the user explicitly allows business logic changes.
- Do not introduce a UI framework or new dependency without confirmation.
- Do not submit, publish, deploy, or change production configuration.

## Required First Step

Start with read-only visual and repo analysis. Do not write code yet.

Visual breakdown must cover:

- Page structure.
- Component tree.
- Color tokens.
- Font sizes, weights, and line heights.
- Spacing system.
- Border radii and shadows.
- Backgrounds, translucency, gradients, and blur.
- Icon and image handling.
- Responsive or viewport scaling strategy.

Repo analysis must cover:

- Existing demo, static, docs, public, assets, and page/component directories.
- Existing visual assets that can be reused.
- Existing scripts for dev server, build, type check, and tests.
- Dirty worktree state, without reverting user changes.

## Implementation Loop

Use Plan-Execute-Verify as the main loop.

1. Create or update a visible implementation in the requested delivery location.
2. Start the local preview when the surface needs a server.
3. Capture the primary viewport screenshot.
4. Compare target and rendered screenshots.
5. List Top 5 visual differences.
6. Fix only the Top 3 highest-impact differences.
7. Capture another screenshot and repeat.

High-fidelity visual work must run at least 5 visual rounds:

- Rounds 1-3: structure, major layout, major components, major color and asset gaps.
- Rounds 4-5: detail review for font weight, color depth, spacing, radius, shadows, clipping, overlap, mobile viewport fit, and icon alignment.
- If the screen is already close by round 3, run rounds 4-5 as check rounds; they may make small or no changes but must record the inspection.
- For complex screens, extend to 6-8 rounds when the feedback still improves and the user budget allows it.

Each round may only fix the Top 3 differences. This prevents broad restyling and keeps the loop auditable.

## Verification

For rendered frontend work, use the in-app Browser plugin when available. Otherwise use the repo's existing browser or Playwright workflow.

Every final answer must report:

- Modified or created files.
- Local URL or open path.
- Primary and secondary screenshot paths.
- Validation commands run.
- Console errors or warnings.
- Top remaining differences.
- Manual refinement suggestions.

For app-like, mini program, or mobile targets, always verify the requested viewport. For this category, check horizontal overflow, fixed bottom bars, safe areas, long text, and whether the final card/control is hidden by navigation.

## Stop Rules

Stop and report clearly when any condition is met:

- Target visual is missing or unreadable.
- Same difference shows no improvement for 2 consecutive rounds.
- Requested fidelity would require business logic changes, new dependencies, production config, publishing, or backend changes.
- The preview cannot be started or screenshot after reasonable recovery.
- The loop reaches the planned maximum rounds.
- The user accepts the visual result.

## Forbidden Actions

- Do not freely change the target style to make it look better.
- Do not hide visual mismatches instead of reporting them.
- Do not overwrite an existing same-name demo or skill without confirmation.
- Do not revert unrelated user changes.
- Do not commit, publish, deploy, or change secrets.
- Do not modify business logic unless explicitly authorized and necessary.

## Output Shape

Use concise Chinese by default when the user works in Chinese.

For implementation tasks, keep a small mismatch ledger:

```text
Round N screenshot: /tmp/...
Top 5 differences:
1. ...
2. ...
3. ...
Fixes this round:
- ...
Remaining:
- ...
```

Final response:

- 新增/修改文件清单
- 本地打开方式或预览 URL
- 每轮截图路径
- 验证命令与结果
- 最终差异清单
- 剩余人工精修建议
