---
name: drawio-diagrams
description: 专业的 DrawIO 图表生成工具，使用 Material Design 配色和圆角矩形风格。支持 (1) 算法/数据结构图 - DP 状态转移、递归树、排序过程、双指针/滑动窗口 (2) 架构图 - 系统架构、微服务、网络拓扑、组件依赖 (3) 流程图/时序图 - 业务流程、决策流程、审批流程 (4) UML/ER 图 - 类图、实体关系、用例图。当用户提到 "drawio"、"draw.io"、需要绘制流程图、架构图、UML 图、ER 图、DP 状态图、算法可视化时使用此技能。
---

# DrawIO 图表生成器

生成专业级 DrawIO 图表，采用统一的 Material Design 配色方案和圆角矩形节点风格。

## 快速开始

1. **确定图表类型**: 根据用户需求判断是算法图、架构图、流程图还是 UML/ER 图
2. **读取样式指南**: 先阅读 `references/style-guide.md` 了解配色和节点样式
3. **读取专项指南**: 根据图表类型读取对应的参考文档
4. **生成 XML**: 创建完整的 mxGraphModel XML 结构
5. **保存文件**: 输出为 `.drawio` 文件

## 图表类型与参考文档

### 算法/数据结构图
适用场景：DP 状态转移、递归树、栈/队列操作、排序过程、双指针/滑动窗口
详见：`references/algorithm-diagrams.md`

**必需元素**：
- 标题区（问题名称 + 状态定义 + 转移公式）
- 输入展示（原始数组/网格）
- 状态转移表（每步的详细计算）
- 易错点提示（红色框标注）
- 最终结果（答案 + 复杂度）

### 架构图
适用场景：系统架构、微服务、网络拓扑、组件依赖、部署架构
详见：`references/architecture-diagrams.md`

**必需元素**：
- 标题（系统名称 + 版本/日期）
- 图例（各节点类型说明）
- 分层标签（清晰标注每层职责）
- 关键说明（重要设计决策标注）

### 流程图/时序图
适用场景：业务流程、算法流程、时序图、决策流程、审批流程
详见：`references/flowchart-diagrams.md`

**必需元素**：
- 开始/结束节点（明确的入口和出口）
- 分支条件（清晰的 Y/N 标注）
- 步骤编号（复杂流程添加）

### UML/ER 图
适用场景：类图、序列图、ER 实体关系、用例图、组件图
详见：`references/uml-diagrams.md`

**类图必需**：类名、属性、方法，以及可见性标记
**ER 图必需**：主键标识、外键标识、多重性标记

## 核心配色方案

| 颜色 | HEX | 用途 |
|------|-----|------|
| 深蓝灰 | `#263238` | 标题、根节点、结束节点 |
| 蓝色 | `#42A5F5` | 初始化、起点、边界条件 |
| 橙色 | `#FFA726` | 处理中、中间步骤、次重要节点 |
| 绿色 | `#66BB6A` | 成功、完成、最优选择 |
| 红色 | `#EF5350` | 关键步骤、警告、终点目标 |
| 紫色 | `#7E57C2` | 循环条件、决策节点、核心概念 |
| 灰色 | `#78909C` | 结束、清理、默认状态 |

完整样式定义见 `references/style-guide.md`。

## XML 结构模板

```xml
<mxfile host="app.diagrams.net">
  <diagram name="图表名称">
    <mxGraphModel dx="1434" dy="796" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1334" pageHeight="850" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 标题 -->
        <mxCell id="title" value="图表标题" style="rounded=1;fillColor=#263238;fontColor=#FFF;fontSize=22;fontStyle=1;arcSize=10;" vertex="1" parent="1">
          <mxGeometry x="100" y="40" width="1114" height="45" as="geometry"/>
        </mxCell>
        <!-- 节点和连接线... -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 常用节点样式

### 基础圆角矩形
```
rounded=1;whiteSpace=wrap;html=1;fillColor=#42A5F5;strokeColor=none;fontColor=#FFF;fontSize=14;fontStyle=1;arcSize=10;
```

### 决策菱形
```
rhombus;whiteSpace=wrap;html=1;fillColor=#FFA726;strokeColor=none;fontColor=#FFF;fontSize=12;fontStyle=1;
```

### 强调箭头
```
html=1;endArrow=block;endFill=1;strokeColor=#42A5F5;strokeWidth=3;
```

### 虚线箭头
```
html=1;endArrow=block;endFill=1;strokeColor=#7E57C2;strokeWidth=2;dashed=1;
```

## 图例与提示框

### 图例样式
```
rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#B0BEC5;strokeWidth=1;fontColor=#37474F;fontSize=11;arcSize=10;align=left;spacingLeft=8;
```

### 警告/易错点
```
rounded=1;whiteSpace=wrap;html=1;fillColor=#FFEBEE;strokeColor=#EF5350;strokeWidth=2;fontColor=#C62828;fontSize=12;fontStyle=1;arcSize=10;align=left;spacingLeft=10;
```

### 注意点
```
rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#66BB6A;strokeWidth=2;fontColor=#2E7D32;fontSize=12;fontStyle=1;arcSize=10;
```

## 布局规范

- **标题区**: 高度 45px，字号 22px，距顶部 40px
- **表头行**: 高度 30px，字号 12-13px，背景 #37474F
- **数据行**: 高度 40-60px，字号 12-14px
- **元素间距**: 10-20px
- **区块间距**: 30-50px
