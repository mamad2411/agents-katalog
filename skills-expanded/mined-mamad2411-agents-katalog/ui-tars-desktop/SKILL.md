---
name: ui-tars-desktop
description: Route for ByteDance UI-TARS Desktop / Agent TARS. Use when the task mentions UI-TARS, Agent TARS, GUI agent, desktop automation, computer operator, browser operator, multimodal agent stack, remote computer operator, or Chinese triggers: 桌面智能体、电脑操作、GUI智能体、视觉操作、浏览器操作、远程电脑、远程浏览器、UI-TARS安装、Agent TARS。
tags: [ui-tars, agent-tars, gui-agent, desktop-automation, browser-operator]
version: 1
---

# UI-TARS Desktop / Agent TARS

Purpose
- Route UI-TARS Desktop and Agent TARS tasks to the local reviewed source clone.
- Prefer passive source inspection before running package scripts or desktop automation.

Local source
- ~/.hermes/external-repos/UI-TARS-desktop
- Upstream: https://github.com/bytedance/UI-TARS-desktop

Safe workflow
1. Read README/docs/package manifests first.
2. For CLI/package use, inspect `package.json` scripts and lockfile before `pnpm install`, `npm install`, or `npx`.
3. For desktop/browser/computer control, confirm target scope and credentials before launching operators.
4. Keep sandbox artifacts outside unrelated user directories.

Chinese route triggers
- UI-TARS, Agent TARS, 桌面智能体, GUI智能体, 电脑操作, 视觉操作, 多模态智能体, 浏览器操作, 远程电脑, 远程浏览器, UI-TARS 安装, Agent TARS CLI
