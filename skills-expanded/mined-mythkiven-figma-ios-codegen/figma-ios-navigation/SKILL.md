---
name: figma-ios-navigation
description: >-
  Identify Figma navigation-bar nodes and generate UIKit navigation code using
  .cursor/bindings/host.json (bases, custom nav class, utils). Use when generating
  navigation bar / ViewController base class code from Figma.
---

# Figma → 导航栏 + ViewController 基类

> **宿主配置**：`.cursor/bindings/host.json`（说明见 [PROJECT_BINDING](../figma-ios-PROJECT_BINDING.md)）  
> 颜色 / iconfont：分别查 `color_map.json` / `iconfont_map.json`，不要在 skill 里写死宿主类名。

## ⚡ QUICK_REF

```
识别导航栏      → 节点名含 nav/导航 OR 顶部 y≤60 且 width≥90%屏宽（规则不变）
数据来源        → design.json[node]
VC 基类         → host.json bases.view_controller
导航实现        → host.json navigation.strategy = system | custom
工具表达式      → host.json utils.*
iconfont        → iconfont_map.json
颜色/字体       → color_map.json / font_map.json
```

---

## 一、ViewController 基类（读 host.json）

生成 VC 时：

1. 基类 = `host.bases.view_controller`（Collection/Table 页用对应字段）
2. 类名前缀按 PROJECT_BINDING §0 / `host.class_prefix`
3. 若 `host.vc_required_overrides` 非空 → **每个 VC 都必须输出**其中的方法；`{has_custom_nav}` 替换为 `true`（本页用了自定义导航）或 `false`
4. 若 `host.base_is_objc == true` → 重写基类方法必须加 `@objc`

`vc_required_overrides` 为空（vanilla）→ **不**强制 `isHideNavigationWhenPush` 之类宿主钩子。

---

## 二、导航栏识别规则（优先级从高到低）

### 规则 1：节点命名（最高优先级）

节点 `name` 包含以下关键词之一（大小写不敏感）→ 判定为导航栏：

| 关键词（中文）| 关键词（英文）| 示例 |
|-------------|--------------|------|
| `导航` / `导航栏` / `导航条` | `navigation` / `navbar` / `nav bar` / `nav_bar` | `通用组件/导航栏/左右icon导航栏` |
| `顶栏` / `标题栏` | `titlebar` / `title bar` | `顶栏/深色` |
| 含 `nav` 且非业务词 | `nav-header` / `top-nav` / `navBar` | `nav-container` |

**排除**：节点名含 `导航抽屉` / `侧边导航` / `bottom navigation` → 不是顶部导航栏。

### 规则 2：层级与位置特征（中优先级）

满足以下**全部**条件 → 判定为导航栏：

- 节点类型为 FRAME 或 INSTANCE
- 位于画布顶部：`y ≤ 60`（含状态栏高度）且 `y + height ≤ 100`
- 宽度接近全屏：`width ≥ 屏幕宽度 × 0.9`
- 高度合理：`40 ≤ height ≤ 100`

### 规则 3：子节点特征（辅助判断）

- **返回按钮**：子节点名含 `back` / `返回` / `<` / `arrow_left`
- **标题文本**：TEXT，水平居中，字号 ≥ 14pt
- **右侧按钮**：子节点名含 `more` / `share` / `help` / `?`

### 规则 4：INSTANCE 类型

名称含 `通用组件/导航栏/*` / `NavBar/*` / 或 `host.navigation.custom_nav_class` 类名 → 判定为导航栏。  
`系统控件/Bars_Status/*` → 状态栏占位，跳过（见 to-code-conventions）。

INSTANCE 已由阶段 1 展开：读 `design.json[id].children`，iconfont / TEXT 按 `frame.relative.x` 分左/中/右。

---

## 三、导航栏代码写法

### 数据来源（强制）

1. **标题**：children 中居中 TEXT → `text.value`；颜色走 color_map
2. **背景**：导航节点 `fills[0].color` → color_map
3. **左/右按钮**：`iconfont` 非空节点，按 x 排序；symbol 查 iconfont_map；颜色走 color_map
4. **禁止**再调 Figma REST / MCP

### 按 `navigation.strategy` 生成

#### A. `strategy == "system"`（默认 vanilla）

使用系统 `UINavigationBar` / `navigationItem`，**不要**实例化 `custom_nav_class`。

```swift
class <P>XxxViewController: UIViewController {  // bases.view_controller
    override func viewDidLoad() {
        super.viewDidLoad()
        title = "标题"  // 来自 Figma TEXT
        navigationItem.leftBarButtonItem = UIBarButtonItem(...)  // iconfont_map / 系统图
    }
}
```

#### B. `strategy == "custom"`

使用 `host.navigation.custom_nav_class` / `custom_nav_item_class`，尺寸用 `utils.screen_width` 与 `utils.status_bar_nav_height`（**原样粘贴表达式**）。

示意（类名来自 host，勿写死宿主类名）：

```swift
class <P>XxxViewController: /* bases.view_controller */ {

    private lazy var navigationView: /* custom_nav_class */ = {
        let nav = /* custom_nav_class */(frame: CGRect(
            x: 0, y: 0,
            width: /* utils.screen_width */,
            height: /* utils.status_bar_nav_height */
        ))
        // 标题 / 颜色 / icon：color_map + iconfont_map
        return nav
    }()

    // 若 vc_required_overrides 含 isHideNavigationWhenPush 等，按模板输出
    // {has_custom_nav} = true

    override func viewDidLoad() {
        super.viewDidLoad()
        view.addSubview(navigationView)
        navigationView.snp.makeConstraints { make in
            make.top.leading.trailing.equalToSuperview()
            make.height.equalTo(/* utils.status_bar_nav_height */)
        }
    }
}
```

示例配置（MK）见 `bindings/examples/mk/host.json`（含自定义导航类与 VC overrides）。

### 左右位置

| 位置 | 条件 |
|------|------|
| 左 | `x + width/2 < 父宽/3` |
| 中 | 中间三分之一 → 标题 |
| 右 | `x + width/2 > 父宽×2/3` |

---

## 四、边缘情况

### 仅有状态栏占位

不生成自定义导航；高度用 `utils.status_bar_height`。

### 状态栏 + 导航栏两个 INSTANCE

合并为一个自定义导航（若 strategy=custom），高度用 `status_bar_nav_height`。

### 疑似导航但无标准命名

位置符合规则 2 → 生成并加注释说明节点 id。

### 不应识别

- 底部 TabBar：`y > 屏高×0.8`
- 弹窗内顶栏
- 列表 section header

### 多个右侧按钮

按 Figma 从左到右添加；icon 一律走 iconfont_map。

---

## 相关

- [PROJECT_BINDING](../figma-ios-PROJECT_BINDING.md) / [bindings/README](../bindings/README.md)
- [iconfont-mapping](../figma-ios-iconfont-mapping/SKILL.md)
- [design-token-mapping](../figma-ios-design-token-mapping/SKILL.md)（颜色字体）
- [playbook](../figma-ios-playbook/SKILL.md)
