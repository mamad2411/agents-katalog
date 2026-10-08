---
name: sango-ui-dev
description: |
  Sango Infinity项目UI开发技能，提供UI资源查询、Prefab结构分析、组件使用规范等支持。
  当用户需要创建、修改UI界面，查询UI组件，查看Prefab结构，或进行UI相关的开发工作时触发此技能。
  项目使用uGUI系统，UI资源位于Assets/Mods/Content/Assets/UI目录。
---

# Sango Infinity UI开发技能

## 技能概述

本技能提供Sango Infinity项目UI开发的完整支持，包括UI资源查询、Prefab结构分析、组件使用规范指导。

## 核心资源

### 1. UI资源文档
详细的UI资源规范文档位于项目的`CodeWiki.md`文件中，包含：
- AtlasTexture精灵分类汇总
- Prefab组件完整清单
- 层级结构规范
- Override处理指南

**查询方法**：读取`references/ui-guide.md`获取快速参考，或直接读取项目根目录的`CodeWiki.md`获取完整文档。

### 2. UI目录结构

```
Assets/Mods/Content/Assets/UI/
├── Animation/      # UI动画资源
├── AtlasTexture/   # 图集纹理(按类别编号组织)
├── Font/          # 字体资源
├── Materials/    # UI材质
├── Prefab/
│   ├── Common/    # 通用组件(116个)
│   ├── Field/     # 字段组件(9个)
│   ├── Editor/    # 编辑器专用UI
│   │   └── EditorTopMenuBar.prefab  # 编辑器顶部菜单栏
│   └── window_*.prefab  # 窗口预设
└── Texture/       # 普通纹理
```

## 编辑器顶部菜单栏

### Prefab位置
`Assets/Mods/Content/Assets/UI/Prefab/Editor/EditorTopMenuBar.prefab`

### Prefab结构
```
EditorTopMenuBar (根对象)
├── LeftMenuArea (HorizontalLayoutGroup)
│   ├── FileMenuBtn + FileMenuLabel (文件)
│   ├── EditMenuBtn + EditMenuLabel (编辑)
│   ├── ViewMenuBtn + ViewMenuLabel (视图)
│   ├── RenderMenuBtn + RenderMenuLabel (渲染)
│   └── HelpMenuBtn + HelpMenuLabel (帮助)
├── LayoutButtonGroup (HorizontalLayoutGroup)
│   ├── LayoutBtn_Default + LayoutBtn_DefaultLabel (默认)
│   ├── LayoutBtn_Wide + LayoutBtn_WideLabel (宽屏)
│   └── LayoutBtn_Vertical + LayoutBtn_VerticalLabel (垂直)
└── RightToolsArea (HorizontalLayoutGroup)
    ├── SearchButton (搜索)
    ├── UserButton (用户)
    └── SettingsButton (设置)
```

### 脚本组件
`Assets/Sango/Scripts/Tools/Editor/EditorTopMenuBar.cs`

### 配置说明
1. 在Unity中实例化Prefa
2. 为根对象添加 `EditorTopMenuBar` 脚本组件
3. 配置 `Menu Categories` 列表定义菜单项
4. 设置 `Layout Buttons` 数组引用布局按钮
5. 配置 `Dropdown Menu Prefab` 下拉菜单模板
6. 绑定事件回调处理菜单点击

## 使用Unity MCP工具

### 查询UI Prefab资源

```csharp
// 搜索Prefabs
manage_asset(action="search", path="Assets/Mods/Content/Assets/UI", filter_type="Prefab", page_size=100)

// 获取Prefab层级结构
manage_prefabs(action="get_hierarchy", prefab_path="Assets/Mods/Content/Assets/UI/Prefab/Common/button_1.prefab")

// 获取Prefab详细信息
manage_prefabs(action="get_info", prefab_path="Assets/Mods/Content/Assets/UI/Prefab/window_dialog.prefab")
```

### 创建编辑器菜单栏Prefa

```csharp
// 1. 创建Prefa目录
manage_asset(action="create_folder", path="Assets/Mods/Content/Assets/UI/Prefab/Editor")

// 2. 创建GameObject并保存为Prefa
manage_gameobject(action="create", name="EditorTopMenuBar", position=[0,0,0], 
                  prefab_folder="Assets/Mods/Content/Assets/UI/Prefab/Editor", 
                  primitive_type="Plane", save_as_prefab=true)

// 3. 打开Prefa编辑
manage_prefabs(action="open_prefab_stage", prefab_path="Assets/Mods/Content/Assets/UI/Prefab/Editor/EditorTopMenuBar.prefab")

// 4. 添加UI组件
manage_gameobject(action="modify", target="EditorTopMenuBar", 
                  components_to_add=["UnityEngine.RectTransform", "UnityEngine.CanvasRenderer", "UnityEngine.UI.Image"])

// 5. 创建子对象
manage_prefabs(action="modify_contents", prefab_path="Assets/Mods/Content/Assets/UI/Prefab/Editor/EditorTopMenuBar.prefab", 
               create_child=[{"name": "LeftMenuArea", "parent": "EditorTopMenuBar", 
                             "components_to_add": ["UnityEngine.RectTransform", "UnityEngine.UI.HorizontalLayoutGroup"]}])

// 6. 设置组件属性
manage_components(action="set_property", target="EditorTopMenuBar/LeftMenuArea", 
                  component_type="UnityEngine.UI.HorizontalLayoutGroup", 
                  properties={"childAlignment": 0, "spacing": 5, "padding": {"m_Left": 5, "m_Right": 5}})

// 7. 保存并关闭
manage_prefabs(action="save_prefab_stage", prefab_path="Assets/Mods/Content/Assets/UI/Prefab/Editor/EditorTopMenuBar.prefab")
manage_prefabs(action="close_prefab_stage", prefab_path="Assets/Mods/Content/Assets/UI/Prefab/Editor/EditorTopMenuBar.prefab")
```

### 查询AtlasTexture资源

```csharp
// 搜索纹理
manage_asset(action="search", path="Assets/Mods/Content/Assets/UI/AtlasTexture", filter_type="Texture", page_size=100)

// 获取纹理信息
manage_asset(action="get_info", path="Assets/Mods/Content/Assets/UI/AtlasTexture/4846-2/4846-2_0.png")
```

## 常用UI组件速查

### 按钮组件
| 组件名 | 用途 | 路径 |
|--------|------|------|
| button_1~5 | 普通按钮 | Common/ |
| button_ok | 确定按钮 | Common/ |
| button_cancel | 取消按钮 | Common/ |
| long_btn | 长按钮 | Common/ |

### 面板组件
| 组件名 | 用途 | 路径 |
|--------|------|------|
| bg_panel | 面板背景 | Common/ |
| win_frame | 窗口框架 | Common/ |
| panel_frame | 内容框架 | Common/ |

### 区域装饰
| 组件名 | 用途 | 路径 |
|--------|------|------|
| area_1~6 | 不同边数装饰 | Common/ |
| area_area_area | 复合区域 | Common/ |

### 文本字段
| 组件名 | 用途 | 路径 |
|--------|------|------|
| textField_1~12 | 文本字段 | Common/ |
| doubleTextField | 双列文本 | Common/ |
| numberField | 数字字段 | Common/ |

### 人物相关
| 组件名 | 用途 | 路径 |
|--------|------|------|
| personStatus | 人物状态框 | Common/ |
| personArea | 人物区域 | Common/ |
| person_1 | 人物组件 | Common/ |

### 窗口组件
| 组件名 | 用途 |
|--------|------|
| window_dialog | 对话窗口 |
| window_city_* | 城市相关窗口 |
| window_information_* | 情报窗口 |
| window_technique | 科技窗口 |

## 组件结构规范

### 按钮标准结构
```
button_X
├── Image (按钮背景)
└── lab   (Text子节点)
```

### 窗口标准结构
```
window_xxx (根Canvas + UIXXX脚本)
├── mask (可选遮罩)
└── root (UIKeepInScreen + DragController)
    ├── win_frame
    │   ├── bg, l/r/t/b (框架装饰)
    │   ├── titleframe, title (标题)
    │   └── button_ok/cancel (按钮)
    └── content (主要内容)
```

### personStatus完整结构
```
personStatus
├── bg
├── area_6 (嵌套装饰)
├── person_1 (UIPersonItem)
│   ├── icon (RawImage)
│   ├── namebg/name
│   └── featurebg/feature
└── status_little (UIStatusItem)
    ├── hex (状态背景)
    └── textField_* (状态值)
```

## AtlasTexture分类速查

| 前缀 | 数量 | 用途 |
|------|------|------|
| 4846-2 | 38张 | 人物立绘/头像 |
| 4846-3 | 24张 | 人物表情 |
| 4846-4 | 128张| 场景/建筑 |
| 4846-5 | 19张 | UI边框 |
| 4846-6 | 87张 | 按钮/图标 |
| 4846-7 | 120张| 地图/地形 |
| 4846-8 | 25张 | 特效 |
| 4846-9 | 60张 | 兵种 |
| 4854-* | 110张| 装备/科技 |

## Sango UI自定义组件

项目中使用的自定义组件(`Sango.UI`命名空间)：

| 组件类 | 用途 |
|--------|------|
| UIPersonItem | 人物显示 |
| UIStatusItem | 状态显示 |
| UITextField | 文本字段 |
| UIDoubleTextField | 双列文本 |
| UIDialog | 对话框 |
| UICityInfoPanel | 城市面板 |
| UICityRecruit | 城市招募 |
| UIKeepInScreen | 屏幕边界 |
| DragController | 拖拽控制 |

## 编辑器工具组件

编辑器专用组件(`SangoTools.Editor`命名空间)：

| 组件类 | 用途 |
|--------|------|
| EditorTopMenuBar | 顶部菜单栏控制器 |
| EditorTopMenuConfig | 菜单配置ScriptableObject |
| EditorTopMenuBarIntegration | 菜单栏集成示例 |

## 开发工作流

### 1. 创建编辑器UI
1. 在 `Editor/` 目录下创建Prefa
2. 使用Unity MCP工具构建UI结构
3. 添加必要的组件和属性
4. 保存并测试

### 2. 创建新UI窗口
1. 基于现有窗口Prefab复制
2. 修改根节点名称和Handler类
3. 配置Canvas和GraphicRaycaster
4. 添加必要的Sango.UI组件

### 3. 使用Common组件
1. 从Common拖拽组件到目标Prefab
2. 设置Anchor和Pivot
3. Override需要修改的属性
4. 添加事件绑定

### 4. 更新UI显示
- 使用`UITextField.SetInfo()`更新文本
- 使用`UIStatusItem`管理武将状态
- 通过Controller脚本处理业务逻辑

## 代码加载示例

```csharp
// 加载Common组件
Resources.Load<GameObject>("UI/Prefab/Common/button_1");

// 加载编辑器菜单栏
Resources.Load<GameObject>("UI/Prefab/Editor/EditorTopMenuBar");

// 加载窗口
Resources.Load<GameObject>("UI/Prefab/window_dialog");

// 加载图集
Resources.Load<Texture2D>("UI/AtlasTexture/4846-2/4846-2_0");
```

## 相关文档

- `CodeWiki.md` - UI资源完整文档
- `references/ui-guide.md` - UI快速参考指南
- `Assets/Sango/Scripts/Tools/Editor/README_TopMenuBar.md` - 顶部菜单栏使用说明
- `Assets/Sango/Scripts/Tools/Editor/EDITOR_TOP_MENU_UI_GUIDE.md` - UI配置指南
