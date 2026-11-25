# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 02-engineering/click-path-state-audit/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当系统化调试已扫过仍有"按钮点了没反应/最终状态不对"的报障、或共享状态 store 大重构后做交互回归时使用；逐个交互触点按调用顺序追踪状态读写与副作用，产出 store 副作用图、触点审计表与互相抵消/竞态的缺陷清单；不适用于纯崩溃/类型/接线类 bug（用 systematic-debugger）或单元接口测试；触发词：点击路径、状态副作用、互相抵消、隐性重置、共享状态冲突、Zustand、
