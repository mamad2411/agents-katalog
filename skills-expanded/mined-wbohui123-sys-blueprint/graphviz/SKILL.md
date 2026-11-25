---
name: graphviz
description: 用 Graphviz 将结构图导出为图片或矢量。
disable-model-invocation: true
---

# graphviz（dot）

用 `dot -V` 确认当前命令可用。

## 用法

```bash
dot -Tpng 图.dot -o 图.png      # 出 png，用 read_image 看
dot -Tsvg 图.dot -o 图.svg      # 出 svg，能嵌进网页
```

## 最小可用模板

```dot
digraph G {
  rankdir=LR;                         // LR 横着排，TB 竖着排（默认）
  node [shape=box, style=rounded];

  需求 -> 原型 [label="定范围"];
  原型 -> 试玩 [label="交给"];
  试玩 -> 原型 [label="改", style=dashed];

  subgraph cluster_0 {
    label="一组";
    原型; 试玩;
  }
}
```

## 坑

- 中文渲染依赖当前可用字体；预览若缺字，为图、节点和边指定支持中文的 `fontname`。
- **查版本是 `dot -V`，而且走 stderr** —— 用 stdout 判断它在不在会判错。
- 节点名里有空格或标点要加引号：`"节点 一" -> "节点 二"`。
- 图大了会摊得很宽，`rankdir=LR` 和 `subgraph cluster_` 是收拾版面的两个主要手段。
