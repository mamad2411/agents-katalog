---
name: open-design
description: 制作网页、HTML 演示或社交图文时，查找并复用 OpenDesign 的设计系统、组件示例与模板。
disable-model-invocation: true
license: Apache-2.0
---

# 从成熟的设计资料建立作品

目标是把适合任务的视觉语言、布局和组件用到实际内容中，使作品保持整体一致。已有设计约定先作为背景；需要新方向时，根据内容、受众和媒介挑选资料。

用本 skill 的脚本寻找候选，从项目目录调用脚本的实际路径：

```bash
node /实际技能目录/scripts/查设计系统.mjs "editorial warm"
node /实际技能目录/scripts/查设计系统.mjs "dashboard"
```

结果提供设计说明、颜色与字体等样式变量、组件示例的路径。读选中的 `DESIGN.md` 和 `tokens.css`；需要组件时再看 `components.html`。一次选定一个基础系统，再按任务调整，不必遍读目录。

要复用作品结构，读 [模板使用](references/模板使用.md)，挑网页、HTML 演示或社交图文的模板。把所需文件复制到项目，用实际内容替换示例，并使模板的视觉角色与选定系统相符。

用 `render_page` 和 `read_image` 查看实际画面，判断构图、文字和内容关系是否成立。资料是起点，用户选择与实际效果决定最终设计。打包范围和来源见 [来源](references/来源.md)。
