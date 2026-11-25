---
name: unity-uxml
description: >
  Unity 6000.3 LTS UI Toolkit UXML markup patterns. Covers document structure, namespaces,
  built-in elements, templates, custom controls with [UxmlElement], binding declarativo,
  y sintaxis correcta para archivos .uxml.
  Trigger: When creating or editing .uxml files, defining UI structure in Unity UI Toolkit,
  working with UXML templates, custom UXML elements, or declarative data binding.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Creating or modifying `.uxml` layout files for Unity UI Toolkit
- Defining UI structure with built-in elements (Label, Button, Toggle, ListView, etc.)
- Using templates and template instances
- Creating custom controls with `[UxmlElement]` attribute
- Setting up declarative data binding in UXML
- Working with namespaces (runtime vs editor elements)

## Critical Rules

### Unity 6000 ONLY — Use `[UxmlElement]`, NOT `UxmlFactory`/`UxmlTraits`

**DEPRECATED (pre-Unity 6)**: Manual `UxmlFactory` and `UxmlTraits` boilerplate
**CORRECT (Unity 6000+)**: Attribute-based system on partial classes

```csharp
// ✅ CORRECT — Unity 6000 attribute system
[UxmlElement]
public partial class HealthBar
{
    [UxmlAttribute("current-value")]
    public float CurrentValue { get; set; }

    [UxmlAttribute("max-value")]
    public float MaxValue { get; set; } = 100f;
}
```

```csharp
// ❌ WRONG — Old boilerplate, DO NOT use
public class HealthBar : VisualElement
{
    public new class UxmlFactory : UxmlFactory<HealthBar, UxmlTraits> { }
    public new class UxmlTraits : VisualElement.UxmlTraits { ... }
}
```

### Naming: C# auto-converts to kebab-case

- `HealthBar` → `<health-bar>`
- `CurrentValue` → `current-value`
- `maxValue` → `max-value`

Override with explicit name: `[UxmlElement("my-tag")]`

### Document Structure — Correct UXML Declaration

```xml
<!-- Standard runtime UXML -->
<ui:UXML xmlns:ui="UnityEngine.UIElements" xmlns:uie="UnityEditor.UIElements" editor-extension-mode="False">
    <!-- content -->
</ui:UXML>

<!-- Editor-only controls (enable Editor Extension Authoring in UI Builder) -->
<ui:UXML xmlns:ui="UnityEngine.UIElements" xmlns:uie="UnityEditor.UIElements" editor-extension-mode="True">
    <uie:PropertyField binding-path="myProperty" />
</ui:UXML>
```

### Namespaces

| Prefix | Namespace | Usage |
|--------|-----------|-------|
| `ui` | `UnityEngine.UIElements` | Runtime elements (Label, Button, VisualElement, etc.) |
| `uie` | `UnityEditor.UIElements` | Editor-only elements (PropertyField, InspectorElement, Toolbar, etc.) |
| Custom | Your namespace (e.g., `MyGame.UI`) | Custom `[UxmlElement]` controls |

### CRITICAL: `<Bindings>` tag breaks with default namespaces

When using `<Bindings>` in UXML, you MUST remove `engine=` and `editor=` attributes from `<ui:UXML>`:

```xml
<!-- ✅ CORRECT — No engine/editor attributes when using <Bindings> -->
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:ListView data-source="MyAsset.asset">
        <Bindings>
            <ui:DataBinding property="itemsSource" data-source-path="items"/>
        </Bindings>
    </ui:ListView>
</ui:UXML>

<!-- ❌ WRONG — engine/editor attributes break <Bindings> -->
<ui:UXML xmlns:ui="UnityEngine.UIElements" engine="UnityEngine.UIElements" editor="UnityEditor.UIElements">
    <Bindings>...</Bindings> <!-- BROKEN -->
</ui:UXML>
```

## Built-in Elements Reference

### Layout Elements

```xml
<!-- Basic container (flexbox by default) -->
<ui:VisualElement name="container" class="flex-column">
    <ui:VisualElement name="child-1" />
    <ui:VisualElement name="child-2" />
</ui:VisualElement>

<!-- ScrollView -->
<ui:ScrollView name="content-scroll" mode="Vertical" horizontal-scroller-visibility="Auto">
    <!-- scrollable content -->
</ui:ScrollView>

<!-- Box (styled container) -->
<ui:Box name="content-box" style="flex-direction: row;">
    <ui:Toggle binding-path="enabled"/>
    <ui:TextField binding-path="name" style="flex-grow: 1;"/>
</ui:Box>
```

### Controls

```xml
<!-- Text -->
<ui:Label text="Hello World" name="title-label" />
<ui:TextElement name="dynamic-text" />

<!-- Buttons -->
<ui:Button name="submit-button" text="Submit" />
<ui:Button name="icon-button" icon="path/to/icon" />
<ui:RepeatButton name="hold-button" text="Hold Me" delay="500" interval="100" />

<!-- Input Fields -->
<ui:TextField name="username" label="Username" max-length="32" />
<ui:TextField name="password" label="Password" is-password-field="true" />
<ui:IntegerField name="age" label="Age" value="0" />
<ui:FloatField name="weight" label="Weight" value="0" />
<ui:DoubleField name="precision" label="Precision" value="0" />
<ui:LongField name="big-number" label="Big Number" value="0" />

<!-- Boolean -->
<ui:Toggle name="enabled-toggle" label="Enabled" value="true" />

<!-- Sliders -->
<ui:Slider name="volume" label="Volume" low-value="0" high-value="100" value="50" />
<ui:SliderInt name="quality" label="Quality" low-value="0" high-value="3" value="2" />
<ui:MinMaxSlider name="range" label="Range" low-limit="0" high-limit="100" min-value="20" max-value="80" />

<!-- Dropdowns -->
<ui:PopupField name="resolution" label="Resolution" choices="1920x1080;1280x720" value="1920x1080" />
<ui:DropdownField name="options" label="Options" />
<ui:EnumField name="mode" label="Mode" value="Horizontal" />

<!-- Vector Fields -->
<ui:Vector2Field name="position" label="Position" />
<ui:Vector3Field name="scale" label="Scale" />
<ui:Vector4Field name="color-vec" label="Color" />
<ui:Vector2IntField name="grid-size" label="Grid Size" />
<ui:Vector3IntField name="tile-coords" label="Tile" />

<!-- Rect Fields -->
<ui:RectField name="rect" label="Rect" />
<ui:RectIntField name="rect-int" label="Rect Int" />

<!-- Bounds Fields -->
<ui:BoundsField name="bounds" label="Bounds" />
<ui:BoundsIntField name="bounds-int" label="Bounds Int" />

<!-- Progress -->
<ui:ProgressBar name="loading-bar" value="0.5" show-text="true" />

<!-- Grouping -->
<ui:GroupBox name="settings-group" text="Settings">
    <!-- grouped controls -->
</ui:GroupBox>
<ui:Foldout name="advanced-foldout" text="Advanced" value="true">
    <!-- collapsible content -->
</ui:Foldout>

<!-- Radio Buttons -->
<ui:RadioButton name="option-a" label="Option A" group-name="choices" value="0" />
<ui:RadioButton name="option-b" label="Option B" group-name="choices" value="1" />
<ui:RadioButtonGroup name="choices" value="0">
    <ui:RadioButton label="Option A" />
    <ui:RadioButton label="Option B" />
</ui:RadioButtonGroup>

<!-- Image -->
<ui:Image name="logo" src="path/to/image.png" />
```

### Editor-Only Elements (`uie:` prefix)

```xml
<uie:PropertyField binding-path="myProperty" />
<uie:InspectorElement name="inspector" />
<uie:Toolbar name="main-toolbar">
    <ui:Button name="toolbar-button" text="Action" />
    <uie:ToolbarToggle name="toolbar-toggle" label="Toggle" />
    <uie:ToolbarMenu name="toolbar-menu" text="Menu" />
    <uie:ToolbarSpacer />
    <uie:ToolbarBreadcrumbs />
</uie:Toolbar>
<uie:EnumFlagsField name="flags" label="Flags" binding-path="myFlags" />
<uie:ColorField name="color" label="Color" binding-path="myColor" />
<uie:CurveField name="curve" label="Curve" binding-path="myCurve" />
<uie:GradientField name="gradient" label="Gradient" binding-path="myGradient" />
<uie:LayerField name="layer" label="Layer" binding-path="myLayer" />
<uie:LayerMaskField name="layer-mask" label="Layer Mask" binding-path="myLayerMask" />
<uie:MaskField name="mask" label="Mask" binding-path="myMask" />
<uie:TagField name="tag" label="Tag" binding-path="myTag" />
<uie:ObjectField name="object-ref" label="Object" binding-path="myObject" />
<uie:MinMaxSlider name="range" label="Range" low-limit="0" high-limit="100" min-value="20" max-value="80" />
```

### ListView

```xml
<!-- ListView with runtime binding (Unity 6000.0+) -->
<ui:ListView
    binding-source-selection-mode="AutoAssign"
    item-template="ListViewItem.uxml"
    data-source="MyListAsset.asset"
    show-foldout-header="true"
    virtualization-method="DynamicHeight"
    show-border="false"
    reorderable="true"
    horizontal-scrolling="false"
    selection-type="Single"
    reorder-mode="Animated"
    show-add-remove-footer="true">
    <Bindings>
        <ui:DataBinding property="itemsSource" data-source-path="items"/>
    </Bindings>
</ui:ListView>

<!-- ListView with SerializedObject binding (Editor) -->
<ui:ListView
    binding-path="switches"
    item-template="game_switch.uxml"
    show-add-remove-footer="true"
    show-foldout-header="true"
    reorderable="true"
    virtualization-method="DynamicHeight">
</ui:ListView>
```

## Templates

### Define and Use Templates

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <!-- Define template -->
    <ui:Template name="switch" src="game_switch.uxml"/>

    <!-- Use template instances -->
    <ui:Instance template="switch" binding-path="useLocalServer"/>
    <ui:Instance template="switch" binding-path="showDebugMenu"/>
    <ui:Instance template="switch" binding-path="showFPSCounter"/>
</ui:UXML>
```

### Template with Attribute Overrides

```xml
<ui:Instance template="item-slot-template">
    <ui:AttributeOverrides selector=".item-name" text="Sword of Destiny" />
</ui:Instance>
```

## Custom Controls in UXML

### Basic Custom Control

```csharp
[UxmlElement]
public partial class InventorySlot
{
    [UxmlAttribute("item-id")]
    public string ItemId { get; set; }

    [UxmlAttribute("quantity")]
    public int Quantity { get; set; } = 1;
}
```

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements" xmlns:local="MyGame.UI">
    <local:inventory-slot item-id="sword_001" quantity="1" />
</ui:UXML>
```

### Complex Data with `[UxmlObject]`

```csharp
[UxmlElement]
public partial class InventorySlot
{
    [UxmlObject]
    [UxmlObjectReference("item-data")]
    public ItemData Item { get; set; }
}

[UxmlElement]
public partial class ItemData
{
    [UxmlAttribute("id")]
    public string Id { get; set; }

    [UxmlAttribute("quantity")]
    public int Quantity { get; set; }
}
```

```xml
<inventory-slot>
    <item-data id="sword_001" quantity="1" />
</inventory-slot>
```

### Custom Type Converters

For types not natively supported as attributes:

```csharp
public class Vector2Converter : UxmlAttributeConverter<Vector2>
{
    public override Vector2 FromString(string value)
    {
        var parts = value.Split(',');
        return new Vector2(float.Parse(parts[0]), float.Parse(parts[1]));
    }

    public override string ToString(Vector2 value) => $"{value.x},{value.y}";
}

[UxmlElement]
public partial class CustomElement
{
    static CustomElement()
    {
        UxmlAttributeConverter.Register(new Vector2Converter());
    }

    [UxmlAttribute("position")]
    public Vector2 Position { get; set; }
}
```

### Custom Binding Types

```csharp
[UxmlObject]
public partial class AddMenuUssClass : CustomBinding
{
    protected override BindingResult Update(in BindingContext context)
    {
        var element = context.targetElement;
        var index = element.parent.IndexOf(element);
        element.EnableInClassList("menu-button--first", index == 0);
        element.EnableInClassList("menu-button--last", index == element.parent.childCount - 1);
        return new BindingResult(BindingStatus.Success);
    }
}
```

```xml
<ui:Button text="Menu Item">
    <Bindings>
        <AddMenuUssClass property="add-menu-button-class" />
    </Bindings>
</ui:Button>
```

## Declarative Data Binding (Runtime)

### Single Property Binding

```xml
<ui:FloatField label="Value">
    <Bindings>
        <ui:DataBinding property="value" data-source-path="myValue" binding-mode="TwoWay"/>
    </Bindings>
</ui:FloatField>
```

### Binding Modes

| Mode | Direction | Use Case |
|------|-----------|----------|
| `TwoWay` | UI ↔ Source | Editable fields |
| `ToTarget` | Source → UI | Display-only fields |
| `ToSource` | UI → Source | Input-only fields |

### Per-Binding Converters

```xml
<ui:DataBinding
    source-to-ui-converters="Inverters"
    ui-to-source-converters="Inverters" />
```

### Data Source with `[CreateProperty]`

```csharp
using Unity.Properties;
using UnityEngine;

[CreateAssetMenu]
public class MyDataSource : ScriptableObject
{
    [CreateProperty]
    public Vector3 position;

    [CreateProperty]
    public float health;
}
```

## Common UXML Patterns

### Dialog / Modal

```xml
<ui:VisualElement name="modal-overlay" class="modal-overlay">
    <ui:VisualElement name="modal-dialog" class="modal-dialog">
        <ui:Label name="modal-title" text="Confirm Action" class="modal-title" />
        <ui:Label name="modal-message" text="Are you sure?" />
        <ui:VisualElement name="modal-buttons" class="modal-buttons">
            <ui:Button name="confirm-button" text="Confirm" />
            <ui:Button name="cancel-button" text="Cancel" />
        </ui:VisualElement>
    </ui:VisualElement>
</ui:VisualElement>
```

### Tab Control

```xml
<ui:VisualElement name="tab-container" class="tab-container">
    <ui:VisualElement name="tab-headers" class="tab-headers">
        <ui:Button name="tab-1-header" text="Tab 1" class="tab-header active" />
        <ui:Button name="tab-2-header" text="Tab 2" class="tab-header" />
    </ui:VisualElement>
    <ui:VisualElement name="tab-content" class="tab-content">
        <ui:VisualElement name="tab-1-content" class="tab-panel active" />
        <ui:VisualElement name="tab-2-content" class="tab-panel" />
    </ui:VisualElement>
</ui:VisualElement>
```

### List Item Template

```xml
<ui:VisualElement name="list-item" class="list-item" style="flex-direction: row;">
    <ui:Image name="item-icon" class="item-icon" />
    <ui:Label name="item-name" class="item-name" />
    <ui:Label name="item-description" class="item-description" />
    <ui:Button name="item-action" class="item-action" text="Use" />
</ui:VisualElement>
```

## Best Practices

1. **UXML = structure only** — No logic, no inline styles (use USS)
2. **Use classes for styling** — `class="primary-button"` not inline `style="..."`
3. **Meaningful names** — `submit-button` not `button1`
4. **Templates for repetition** — Don't duplicate complex structures
5. **Namespace custom controls** — Avoid naming conflicts (`xmlns:local="MyGame.UI"`)
6. **Remove engine/editor attrs when using `<Bindings>`** — Critical gotcha
7. **Use `binding-path` for SerializedObject binding** — Editor inspectors
8. **Use `<Bindings>` + `data-source` for runtime binding** — Unity 6000.0+

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `<Bindings>` doesn't work | `engine=`/`editor=` attrs on `<ui:UXML>` | Remove those attributes |
| Custom control not in UI Builder | Missing `[UxmlElement]` or not `partial` | Add both |
| Editor controls not showing | `editor-extension-mode="False"` | Set to `"True"` or enable in UI Builder settings |
| Binding not updating | Wrong `binding-path` syntax | Use `Path.To.List[2]` for runtime, `Path.To.List.Array.data[2]` for SerializedObject |
| Property not in UXML | Not using `[UxmlAttribute]` | Add attribute to property |
