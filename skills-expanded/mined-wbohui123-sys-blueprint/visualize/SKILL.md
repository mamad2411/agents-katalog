---
name: visualize
description: 制作项目内的交互图表与模拟，让用户调整参数、比较关系和变化。
disable-model-invocation: true
---

# 可交互的说明

把当前需要理解的关系变成可操作的 HTML：让用户调整关键参数、查看变化，并能读懂每个数值的意义。仅需说明一个事实时，用文字即可；静态结构图沿用 Graphviz。

本技能有不依赖网络的 SVG 图表起点。脚本位置相对本 skill，产物路径相对命令当前工作目录；调用时使用脚本绝对路径：

```bash
node "<本技能目录>/scripts/创建可视化.mjs" "关系探索.html"
```

示例用于传递交互与解释的分寸，不是当前问题的答案。按任务替换数据、关系、单位与控件；让图中变化和用户操作直接对应，区分真实数据、估计和示意。范围、公式和来源随作品说明，不用任意曲线暗示实际规律。

通过内置 `render_page` 检查画面，按状态代码核对参数、数值和图形的关系；交互手感由实际操作判断。当前截图工具不点击控件。通过 `present_artifact` 交回可打开的 HTML。此实现参考 [dsh-visualize](https://github.com/Nagi-ovo/dsh-visualize/tree/db54992331d98af68390796d0de4b57bc76453ca) 的独立交互内容方式，保留当前 studio 的预览入口。
