---
name: unity-uitk-csharp
description: >
  Unity 6000.3 LTS UI Toolkit C# implementation patterns. Covers element querying,
  event handling, runtime vs editor UI, data binding (SerializedObject and runtime),
  custom controls, transitions, ListView, and lifecycle management.
  Trigger: When writing C# code for Unity UI Toolkit, handling UI events,
  implementing data binding, creating editor windows, runtime UI controllers,
  or working with VisualElement lifecycle.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Writing C# code to interact with UI Toolkit elements
- Creating EditorWindow or custom inspector GUIs
- Building runtime UI controllers with UIDocument
- Handling events (click, change, pointer, keyboard, drag)
- Implementing data binding (SerializedObject or runtime)
- Creating custom controls with `[UxmlElement]`
- Working with ListView, transitions, or scheduling

## Critical Rules

### Runtime vs Editor — Different Namespaces, Different Patterns

| Aspect | Runtime UI | Editor UI |
|--------|-----------|-----------|
| **Namespace** | `UnityEngine.UIElements` | `UnityEditor.UIElements` |
| **Entry point** | `UIDocument` + `MonoBehaviour` | `EditorWindow` or `Editor` |
| **Asset loading** | `[SerializeField]` VisualTreeAsset | `AssetDatabase.LoadAssetAtPath<T>()` |
| **Binding source** | Runtime data sources (`[CreateProperty]`) | `SerializedObject` / `SerializedProperty` |
| **Live reload** | ON by default | OFF by default |

**NEVER mix `UnityEditor.UIElements` in runtime code** — it won't compile in builds.

### Lifecycle: OnEnable/OnDisable for Runtime (Live Reload)

Runtime live reload temporarily disables companion MonoBehaviours. Init/teardown MUST be in `OnEnable`/`OnDisable`:

```csharp
// ✅ CORRECT
public class MyUI : MonoBehaviour
{
    private void OnEnable()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;
        var button = root.Q<Button>("my-button");
        button.clicked += OnClicked;
    }

    private void OnDisable()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;
        var button = root.Q<Button>("my-button");
        button.clicked -= OnClicked;
    }

    private void OnClicked() { }
}

// ❌ WRONG — Start() won't re-run after live reload
public class MyUI : MonoBehaviour
{
    void Start()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;
        var button = root.Q<Button>("my-button");
        button.clicked += OnClicked;
    }
}
```

### Element Querying — Use `Q<T>()`

```csharp
// ✅ CORRECT — Type-safe query
var button = root.Q<Button>("my-button");
var label = root.Q<Label>(className: "title-label");

// ✅ Query by class only
var items = root.Query<VisualElement>(className: "list-item").ToList();

// ❌ WRONG — Old pattern, less type-safe
var button = root.Query<Button>().First();
```

## Runtime UI Patterns

### Basic Runtime UI Controller

```csharp
using UnityEngine;
using UnityEngine.UIElements;

public class RuntimeUIController : MonoBehaviour
{
    private UIDocument m_Document;

    private void OnEnable()
    {
        m_Document = GetComponent<UIDocument>();
        var root = m_Document.rootVisualElement;

        var button = root.Q<Button>("start-button");
        button.clicked += OnStartClicked;

        var label = root.Q<Label>("status-label");
        label.text = "Ready";
    }

    private void OnDisable()
    {
        var root = m_Document.rootVisualElement;
        var button = root.Q<Button>("start-button");
        button.clicked -= OnStartClicked;
    }

    private void OnStartClicked()
    {
        Debug.Log("Game started!");
    }
}
```

### Loading UXML/USS at Runtime

```csharp
using UnityEngine;
using UnityEngine.UIElements;

public class RuntimeUILoader : MonoBehaviour
{
    [SerializeField] private VisualTreeAsset m_UxmlAsset;
    [SerializeField] private StyleSheet m_UssAsset;

    private void Start()
    {
        var document = GetComponent<UIDocument>();
        var root = document.rootVisualElement;

        root.Clear();
        m_UxmlAsset.CloneTree(root);
        root.styleSheets.Add(m_UssAsset);
    }
}
```

### Building UI Purely in C#

```csharp
using UnityEngine;
using UnityEngine.UIElements;

public class CSharpUI : MonoBehaviour
{
    public void CreateGUI()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;

        var container = new VisualElement
        {
            style =
            {
                flexDirection = FlexDirection.Column,
                alignItems = Align.Center,
                padding = 20
            }
        };

        var label = new Label("Hello World")
        {
            style = { fontSize = 24, unityFontStyleAndWeight = FontStyle.Bold }
        };
        container.Add(label);

        var button = new Button(OnClicked) { text = "Click Me" };
        container.Add(button);

        root.Add(container);
    }

    private void OnClicked() { }
}
```

## Editor UI Patterns

### Editor Window

```csharp
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;

public class MyEditorWindow : EditorWindow
{
    [SerializeField] VisualTreeAsset m_VisualTreeAsset;

    [MenuItem("Window/UI Toolkit/MyWindow")]
    public static void ShowExample()
    {
        var wnd = GetWindow<MyEditorWindow>();
        wnd.titleContent = new GUIContent("My Window");
    }

    public void CreateGUI()
    {
        VisualElement root = rootVisualElement;
        m_VisualTreeAsset.CloneTree(root);

        var button = root.Q<Button>("my-button");
        button.clicked += OnButtonClicked;
    }

    private void OnButtonClicked()
    {
        Debug.Log("Button clicked!");
    }
}
```

### Custom Inspector

```csharp
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;

[CustomEditor(typeof(MyComponent))]
public class MyComponentEditor : Editor
{
    [SerializeField] VisualTreeAsset visualTreeAsset;

    public override VisualElement CreateInspectorGUI()
    {
        var root = visualTreeAsset.CloneTree();

        // Add custom elements
        var customButton = new Button(OnCustomAction) { text = "Custom Action" };
        root.Add(customButton);

        return root;
    }

    private void OnCustomAction() { }
}
```

### Popup Window

```csharp
using UnityEditor;
using UnityEngine.UIElements;
using PopupWindow = UnityEditor.PopupWindow;

public class PopupExample : EditorWindow
{
    private void CreateGUI()
    {
        var button = rootVisualElement.Q<Button>();
        button.clicked += () => PopupWindow.Show(button.worldBound, new PopupContentExample());
    }
}

public class PopupContentExample : PopupWindowContent
{
    public override VisualElement CreateGUI()
    {
        var asset = AssetDatabase.LoadAssetAtPath<VisualTreeAsset>("Assets/Editor/PopupContent.uxml");
        return asset.CloneTree();
    }

    public override void OnOpen() { }
    public override void OnClose() { }
}
```

## Event Handling

### Click Events

```csharp
// Simple callback
button.clicked += OnClicked;

// With event data (check propagation phase)
btn.RegisterCallback<ClickEvent, VisualElement>(Clicked, root);

private void Clicked(ClickEvent evt, VisualElement root)
{
    // Only act at target phase, not during bubbling
    if (evt.propagationPhase != PropagationPhase.AtTarget) return;
    root.ShowVisualElement(false);
}
```

### Change Events

```csharp
// Generic registration (works on any VisualElement)
rootVisualElement.RegisterCallback<ChangeEvent<bool>>(OnBoolChanged);

// Typed convenience method
toggle.RegisterValueChangedCallback(OnToggleChanged);

private void OnToggleChanged(ChangeEvent<bool> evt)
{
    Debug.Log($"Old: {evt.previousValue}, New: {evt.newValue}");
}
```

### SetValueWithoutNotify (No ChangeEvent)

```csharp
// ❌ Triggers ChangeEvent
m_MyToggle.value = !m_MyToggle.value;

// ✅ Does NOT trigger ChangeEvent — use when updating UI from data
m_MyToggle.SetValueWithoutNotify(!m_MyToggle.value);
```

### Pointer Events

```csharp
element.RegisterCallback<PointerOverEvent>(OnPointerOver);
element.RegisterCallback<PointerOutEvent>(OnPointerOut);
element.RegisterCallback<PointerDownEvent>(OnPointerDown);
element.RegisterCallback<PointerUpEvent>(OnPointerUp);

private void OnPointerOver(PointerOverEvent evt) { }
private void OnPointerOut(PointerOutEvent evt) { }
```

### Keyboard Events

```csharp
element.RegisterCallback<KeyDownEvent>(OnKeyDown);
element.RegisterCallback<KeyUpEvent>(OnKeyUp);

private void OnKeyDown(KeyDownEvent evt)
{
    if (evt.keyCode == KeyCode.Escape)
    {
        evt.PreventDefault();
    }
}
```

### Focus Events

```csharp
element.RegisterCallback<FocusInEvent>(OnFocusIn);
element.RegisterCallback<FocusOutEvent>(OnFocusOut);
```

### Event Propagation Control

```csharp
element.RegisterCallback<ClickEvent>(evt =>
{
    // Stop event from bubbling up
    evt.StopPropagation();

    // Stop event AND prevent other handlers at same level
    evt.StopImmediatePropagation();
});
```

### Capture (Mouse/Pointer)

```csharp
// Pointer capture (preferred — precedes mouse events)
PointerCaptureHelper.CapturePointer(element);
PointerCaptureHelper.ReleasePointer(element);

// Mouse capture
MouseCaptureController.CaptureMouse(element);
MouseCaptureController.ReleaseMouse(element);
```

### Command Events (Editor Only)

```csharp
listView.RegisterCallback<ValidateCommandEvent>(OnValidateCommand);
listView.RegisterCallback<ExecuteCommandEvent>(OnExecuteCommand);

void OnExecuteCommand(ExecuteCommandEvent evt)
{
    if (evt.commandName == "Copy" && listView.selectedIndices.Count() > 0)
    {
        EditorGUIUtility.systemCopyBuffer = items[listView.selectedIndex];
        evt.StopPropagation();
    }
    else if (evt.commandName == "Paste" && !string.IsNullOrEmpty(EditorGUIUtility.systemCopyBuffer))
    {
        items.Add(EditorGUIUtility.systemCopyBuffer);
        listView.RefreshItems();
        evt.StopPropagation();
    }
}

void OnValidateCommand(ValidateCommandEvent evt)
{
    if (evt.commandName == "Copy" && listView.selectedIndices.Count() > 0)
        evt.StopPropagation();
}
```

**Available Commands**: `Copy`, `Cut`, `Paste`, `Delete`, `DeselectAll`, `SoftDelete`, `Duplicate`, `FrameSelected`, `FrameSelectedWithLock`, `SelectAll`, `Find`, `FocusProjectWindow`

### Unregister Callbacks

```csharp
// Always unregister in OnDisable to prevent memory leaks
element.UnregisterCallback<ClickEvent>(OnClick);
element.UnregisterCallback<PointerOverEvent>(OnPointerOver);
```

## Data Binding — SerializedObject (Editor)

### Basic Binding

```csharp
using UnityEditor;
using UnityEditor.UIElements;
using UnityEngine;
using UnityEngine.UIElements;

public class SimpleBindingExample : EditorWindow
{
    TextField m_NameField;

    [MenuItem("Window/Binding Example")]
    public static void ShowExample()
    {
        var wnd = GetWindow<SimpleBindingExample>();
        wnd.titleContent = new GUIContent("Binding Example");
    }

    public void CreateGUI()
    {
        m_NameField = new TextField("Object Name");
        rootVisualElement.Add(m_NameField);
        OnSelectionChange();
    }

    public void OnSelectionChange()
    {
        var selected = Selection.activeObject as GameObject;
        if (selected != null)
        {
            var so = new SerializedObject(selected);
            // Note: "name" property is serialized as "m_Name"
            var property = so.FindProperty("m_Name");
            m_NameField.BindProperty(property);
        }
        else
        {
            m_NameField.Unbind();
        }
    }
}
```

### Binding with UXML

```csharp
public class UxmlBindingExample : EditorWindow
{
    [SerializeField] VisualTreeAsset m_VisualTreeAsset;

    public void CreateGUI()
    {
        m_VisualTreeAsset.CloneTree(rootVisualElement);

        // Bind to selected object
        if (Selection.activeObject != null)
        {
            rootVisualElement.Bind(new SerializedObject(Selection.activeObject));
        }
    }
}
```

### UXML with binding-path

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements" xmlns:uie="UnityEditor.UIElements">
    <ui:Toggle binding-path="enabled"/>
    <ui:TextField binding-path="name" readonly="false" style="flex-grow: 1;"/>
</ui:UXML>
```

### Nested Binding

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements" xmlns:uie="UnityEditor.UIElements">
    <BindableElement binding-path="health">
        <uie:PropertyField binding-path="armor"/>
        <uie:PropertyField binding-path="life"/>
    </BindableElement>
</ui:UXML>
```

### ListView with SerializedObject Binding

```xml
<ui:ListView
    binding-path="switches"
    item-template="game_switch.uxml"
    show-add-remove-footer="true"
    show-foldout-header="true"
    reorderable="true"
    virtualization-method="DynamicHeight">
</ui:ListView>
```

```csharp
public class ListViewBindingExample : EditorWindow
{
    [SerializeField] private VisualTreeAsset m_VisualTreeAsset;
    [SerializeField] private GameSwitchListAsset gameSwitchList;

    public void CreateGUI()
    {
        m_VisualTreeAsset.CloneTree(rootVisualElement);

        var listView = rootVisualElement.Q<ListView>();
        if (listView != null && gameSwitchList != null)
        {
            listView.itemsSource = gameSwitchList.switches;
            listView.Bind(new SerializedObject(gameSwitchList));
        }
    }
}
```

### Bind Time Rules

| Condition | Automatic Bind Time |
|-----------|-------------------|
| `InspectorElement` constructed in C# | During constructor call |
| Child of `CreateInspectorGUI()` / `CreatePropertyGUI()` return | After method returns |
| Child when `Bind()` / `BindProperty()` called on parent | During the call |
| Other | No automatic binding; must bind manually |

### Best Practices for Editor Binding

- In `CreateInspectorGUI()` / `CreatePropertyGUI()`: set `bindingPath`, DON'T call `Bind()` (automatic)
- For other UI types: call `Bind()` on lowest-level parent encompassing all controls
- NEVER bind the same element more than once (performance impact)
- Don't call `Bind()` from `Editor.CreateInspectorGUI` or `PropertyDrawer.CreatePropertyGUI`

## Data Binding — Runtime (Unity 6000.0+)

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
    public float sum => position.x + position.y + position.z;
}
```

### UXML with Runtime Bindings

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement data-source="MyAsset.asset" style="flex-grow: 1;">
        <ui:Vector3Field label="Position">
            <Bindings>
                <ui:DataBinding property="value" data-source-path="position" binding-mode="ToSource"/>
            </Bindings>
        </ui:Vector3Field>
        <ui:FloatField label="Sum" name="SumField">
            <Bindings>
                <ui:DataBinding property="value" data-source-path="sum" binding-mode="ToTarget"/>
            </Bindings>
        </ui:FloatField>
    </ui:VisualElement>
</ui:UXML>
```

### ListView Runtime Binding

```xml
<ui:ListView
    binding-source-selection-mode="AutoAssign"
    item-template="ListViewItem.uxml"
    data-source="MyListAsset.asset">
    <Bindings>
        <ui:DataBinding property="itemsSource" data-source-path="items"/>
    </Bindings>
</ui:ListView>
```

```csharp
// Set dataSource in C#
var listView = rootVisualElement.Q<ListView>();
listView.dataSource = myListAsset;
```

### Global Type Converters

```csharp
static class RegisterGlobalConverters
{
#if UNITY_EDITOR
    [InitializeOnLoadMethod]
#endif
    [RuntimeInitializeOnLoadMethod]
    public static void Register()
    {
        ConverterGroups.RegisterGlobalConverter((ref TextureHandle handle) => TextureHandle.ResolveTexture(handle));
        ConverterGroups.RegisterGlobalConverter((ref Texture2D texture) => TextureHandle.FromTexture(texture));
    }
}
```

### Per-Binding Converters

```csharp
var binding = new DataBinding();
binding.sourceToUiConverters.AddConverter((ref float radian) => Mathf.RadToDeg * radian);
binding.uiToSourceConverters.AddConverter((ref float degree) => Mathf.DegToRad * degree);
```

### Converter Groups

```csharp
static class RegisterConverterGroup
{
#if UNITY_EDITOR
    [InitializeOnLoadMethod]
#endif
    [RuntimeInitializeOnLoadMethod]
    public static void Register()
    {
        var group = new ConverterGroup("Inverters");
        group.AddConverter((ref int v) => -v);
        group.AddConverter((ref float v) => -v);
        ConverterGroups.RegisterConverterGroup(group);
    }
}

// Apply group to binding
var binding = new DataBinding();
if (ConverterGroups.TryGetConverterGroup("Inverters", out var group))
{
    binding.ApplyConverterGroupToUI(group);
    binding.ApplyConverterGroupToSource(group);
}
```

### Custom Binding Type

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

### Runtime vs SerializedObject Binding Comparison

| Aspect | Runtime Binding | SerializedObject Binding |
|--------|----------------|-------------------------|
| UI | Runtime + Editor (no serialized data) | Editor only |
| Data types | Any plain C# `object` | Only `SerializedProperty` types |
| Binding target | Multiple properties per control | Only `value` of `INotifyValueChanged<T>` |
| List syntax | `Path.To.List[2]` | `Path.To.List.Array.data[2]` |
| Extensibility | Custom binding types/attributes | Not extensible |

## Custom Controls

### Unity 6 Attribute-Based Pattern

```csharp
using UnityEngine;
using UnityEngine.UIElements;

[UxmlElement]
partial class MyElement : VisualElement
{
    string _myString = "default_value";
    int _myInt = 2;

    [UxmlAttribute]
    public string myString
    {
        get => _myString;
        set
        {
            _myString = value;
            // React here — update UI, etc.
        }
    }

    [UxmlAttribute]
    public int myInt
    {
        get => _myInt;
        set
        {
            _myInt = value;
            // React here
        }
    }
}
```

### Custom Control with INotifyValueChanged

```csharp
[UxmlElement]
public partial class TexturePreviewElement : BindableElement, INotifyValueChanged<Object>
{
    public static readonly string ussClassName = "texture-preview-element";

    Image m_Preview;
    ObjectField m_ObjectField;
    Texture2D m_Value;

    public TexturePreviewElement()
    {
        AddToClassList(ussClassName);

        m_Preview = new Image();
        Add(m_Preview);

        m_ObjectField = new ObjectField { objectType = typeof(Texture2D) };
        m_ObjectField.RegisterValueChangedCallback(OnObjectFieldValueChanged);
        Add(m_ObjectField);
    }

    void OnObjectFieldValueChanged(ChangeEvent<Object> evt)
    {
        value = evt.newValue;
    }

    public void SetValueWithoutNotify(Object newValue)
    {
        if (newValue == null || newValue is Texture2D)
        {
            m_Value = newValue as Texture2D;
            m_Preview.image = m_Value;
            // CRITICAL: Use SetValueWithoutNotify to avoid recursive ChangeEvent
            m_ObjectField.SetValueWithoutNotify(m_Value);
        }
        else throw new ArgumentException($"Expected {typeof(Texture2D)}");
    }

    public Object value
    {
        get => m_Value;
        set
        {
            if (Equals(value, this.value)) return;
            var previous = this.value;
            SetValueWithoutNotify(value);
            using var evt = ChangeEvent<Object>.GetPooled(previous, value);
            evt.target = this;
            SendEvent(evt);
        }
    }
}
```

### Manual List Binding (Without ListView)

```csharp
[CustomEditor(typeof(TexturePackAsset))]
public class TexturePackEditor : Editor
{
    [SerializeField] VisualTreeAsset m_VisualTreeAsset;

    public override VisualElement CreateInspectorGUI()
    {
        var editor = m_VisualTreeAsset.CloneTree();
        var container = editor.Q(className: "preview-container");
        SetupList(container);

        // Watch array size changes
        var sizeProp = serializedObject.FindProperty(nameof(TexturePackAsset.textures) + ".Array");
        sizeProp.Next(true);
        editor.TrackPropertyValue(sizeProp, prop => SetupList(container));

        editor.Q<Button>("add-button").RegisterCallback<ClickEvent>(OnClick);
        return editor;
    }

    void SetupList(VisualElement container)
    {
        var property = serializedObject.FindProperty(nameof(TexturePackAsset.textures) + ".Array");
        var endProperty = property.GetEndProperty();
        property.NextVisible(true);
        var childIndex = 0;

        do
        {
            if (SerializedProperty.EqualContents(property, endProperty)) break;
            if (property.propertyType == SerializedPropertyType.ArraySize) continue;

            TexturePreviewElement element;
            if (childIndex < container.childCount)
                element = (TexturePreviewElement)container[childIndex];
            else
            {
                element = new TexturePreviewElement();
                container.Add(element);
            }
            element.BindProperty(property);
            ++childIndex;
        }
        while (property.NextVisible(false));

        while (childIndex < container.childCount)
            container.RemoveAt(container.childCount - 1);
    }

    void OnClick(ClickEvent evt)
    {
        var property = serializedObject.FindProperty(nameof(TexturePackAsset.textures));
        property.arraySize += 1;
        serializedObject.ApplyModifiedProperties();
    }
}
```

## Transitions

### Triggering Transitions via Class Toggle

```csharp
private void OnClick(ClickEvent evt)
{
    colorChanger.ToggleInClassList("color-transition");
}
```

### Pointer-Based Transitions

```csharp
public class TransitionExample : EditorWindow
{
    VisualElement cSharpLabel;
    Rotate defaultRotate;
    Scale defaultScale;

    public void CreateGUI()
    {
        cSharpLabel = new Label("Hello World! From C#");
        rootVisualElement.Add(cSharpLabel);

        cSharpLabel.style.transitionDuration = new List<TimeValue> { new TimeValue(3) };
        defaultRotate = cSharpLabel.resolvedStyle.rotate;
        defaultScale = cSharpLabel.resolvedStyle.scale;

        cSharpLabel.RegisterCallback<PointerOverEvent>(OnPointerOver);
        cSharpLabel.RegisterCallback<PointerOutEvent>(OnPointerOut);
    }

    void OnPointerOver(PointerOverEvent evt) => SetHover(evt.currentTarget as VisualElement, true);
    void OnPointerOut(PointerOutEvent evt) => SetHover(evt.currentTarget as VisualElement, false);

    void SetHover(VisualElement label, bool hover)
    {
        label.style.rotate = hover ? new(Angle.Degrees(10)) : defaultRotate;
        label.style.scale = hover ? new Vector2(1.1f, 1) : defaultScale;
    }

    void OnDisable()
    {
        cSharpLabel.UnregisterCallback<PointerOverEvent>(OnPointerOver);
        cSharpLabel.UnregisterCallback<PointerOutEvent>(OnPointerOut);
    }
}
```

### Transition Events

```csharp
colorChanger.RegisterCallback<TransitionRunEvent>(OnTransitionRun);
colorChanger.RegisterCallback<TransitionStartEvent>(OnTransitionStart);
colorChanger.RegisterCallback<TransitionEndEvent>(OnTransitionEnd);
colorChanger.RegisterCallback<TransitionCancelEvent>(OnTransitionCancel);
```

### Looping Yo-Yo (A→B→A with transition both ways)

```csharp
private void SetupYoyo(VisualElement root)
{
    _yoyoLabel = root.Q<Label>(name: "yoyo-label");
    _yoyoLabel.RegisterCallback<TransitionEndEvent>(evt =>
        _yoyoLabel.ToggleInClassList("enlarge-scale-yoyo"));
    root.schedule.Execute(() => _yoyoLabel.ToggleInClassList("enlarge-scale-yoyo")).StartingIn(100);
}
```

### Looping A-to-B (A→B with transition, B→A instant)

```csharp
private void SetupA2B(VisualElement root)
{
    _a2bLabel = root.Q<Label>(name: "a2b-label");
    _a2bLabel.RegisterCallback<TransitionEndEvent>(evt =>
    {
        _a2bLabel.RemoveFromClassList("enlarge-scale-a2b");
        _a2bLabel.schedule.Execute(() => _a2bLabel.AddToClassList("enlarge-scale-a2b")).StartingIn(10);
    });
    _a2bLabel.schedule.Execute(() => _a2bLabel.AddToClassList("enlarge-scale-a2b")).StartingIn(100);
}
```

## Scheduling

```csharp
// Execute once after delay
root.schedule.Execute(() => DoSomething()).StartingIn(100);

// Execute every N ms
element.schedule.Execute(() => DoSomething()).Every(1000);

// Debounced input
private ScheduledItem m_Debounce;

textField.RegisterCallback<ChangeEvent<string>>(evt =>
{
    m_Debounce?.ExecuteLater(300);
    m_Debounce = textField.schedule.Execute(() =>
    {
        OnInputConfirmed(evt.newValue);
    });
});
```

## Reading Resolved Styles

```csharp
// Use resolvedStyle for final computed values
float height = element.resolvedStyle.height;

// Track geometry changes
element.RegisterCallback<GeometryChangedEvent>(OnGeometryChanged);

public void OnGeometryChanged(GeometryChangedEvent evt)
{
    var el = evt.target as VisualElement;
    float height = el.resolvedStyle.height;
    Debug.Log($"Resolved height: {height}");
}

// Periodic style check
element.schedule.Execute(() =>
{
    Debug.Log(element.resolvedStyle.height);
}).Every(100);
```

## Coordinate System

```csharp
// Panel space to element local space
Vector2 local = element.WorldToLocal(panelPoint);

// Element local space to Panel space
Vector2 panel = element.LocalToWorld(localPoint);

// Between two elements' local spaces
Vector2 target = sourceElement.ChangeCoordinatesTo(targetElement, sourcePoint);

// Element's final computed position
Rect layout = element.layout;

// Window space coordinates (includes window header height)
Rect worldBound = element.worldBound;
```

## Read-Only Children (Shadow Tree)

Some built-in controls have internal hierarchies (shadow trees) that are read-only:

```csharp
// Access read-only children of ScrollView inside ListView
var scrollView = listView.Q<ScrollView>();
scrollView.mouseWheelScrollSize = 55;
```

## Pseudo-State Timing Gotcha

Properties like `hasFocusPseudoState` may reflect PRE-EVENT states during callbacks:

```csharp
// ❌ WRONG — May still show false during FocusInEvent
element.RegisterCallback<FocusInEvent>(evt =>
{
    bool hasFocus = element.hasFocusPseudoState;
});

// ✅ CORRECT — Check on next frame
element.RegisterCallback<FocusInEvent>(evt =>
{
    element.schedule.Execute(() =>
    {
        bool hasFocus = element.hasFocusPseudoState;
        Debug.Log($"Has focus: {hasFocus}");
    }).ExecuteLater(1);
});
```

## State Management

```csharp
// Enable/disable
myToggle.SetEnabled(false);

// USS pseudo-class for disabled state
// .unity-button:disabled { background-color: #000000; }

// Class list manipulation
element.AddToClassList("active");
element.RemoveFromClassList("active");
element.ToggleInClassList("active");
element.EnableInClassList("first-class", index == 0);
```

## Dynamic Atlas Management

```csharp
// Reset dynamic atlas to defragment
rootVisualElement.panel.ResetDynamicAtlas();

// Custom atlas filter
class MyCustomFilter : MonoBehaviour
{
    public PanelSettings panelSettings;
    public Texture2D largeTexture;

    void OnEnable() { panelSettings.dynamicAtlasSettings.customFilter = Filter; }
    void OnDisable() { panelSettings.dynamicAtlasSettings.customFilter = null; }

    bool Filter(Texture2D texture, ref DynamicAtlasFilters filtersToApply)
    {
        if (texture == largeTexture)
        {
            filtersToApply &= ~DynamicAtlasFilters.Size;
        }
        return true;
    }
}
```

## 2D Visual Content Generation

### Painter2D API (Vector/Canvas-like)

```csharp
class QuadVectorElement : VisualElement
{
    public Color color = Color.red;

    public QuadVectorElement()
    {
        generateVisualContent += OnGenerateVisualContent;
    }

    void OnGenerateVisualContent(MeshGenerationContext mgc)
    {
        var painter2D = mgc.painter2D;
        painter2D.fillColor = color;

        painter2D.BeginPath();
        painter2D.MoveTo(Vector2.zero);
        painter2D.LineTo(new Vector2(layout.width, 0));
        painter2D.LineTo(new Vector2(layout.width, layout.height));
        painter2D.LineTo(new Vector2(0, layout.height));
        painter2D.ClosePath();
        painter2D.Fill();
    }
}
```

### Painter2D — Lines

```csharp
painter2D.lineWidth = 10.0f;
painter2D.strokeColor = Color.white;
painter2D.lineJoin = LineJoin.Round;
painter2D.lineCap = LineCap.Round;

painter2D.BeginPath();
painter2D.MoveTo(new Vector2(100, 100));
painter2D.LineTo(new Vector2(120, 120));
painter2D.Stroke();
```

### Painter2D — Arcs

```csharp
painter2D.BeginPath();
painter2D.MoveTo(new Vector2(100, 100));
painter2D.Arc(new Vector2(100, 100), 50.0f, 10.0f, 95.0f);
painter2D.ClosePath();
painter2D.Fill();
painter2D.Stroke();
```

### Painter2D — Bezier Curves

```csharp
painter2D.BeginPath();
painter2D.MoveTo(new Vector2(100, 100));
painter2D.BezierCurveTo(new Vector2(150, 150), new Vector2(200, 50), new Vector2(250, 100));
painter2D.Stroke();
```

### Painter2D — Holes with FillRule

```csharp
painter2D.BeginPath();
// Outer rectangle
painter2D.MoveTo(new Vector2(10, 10));
painter2D.LineTo(new Vector2(300, 10));
painter2D.LineTo(new Vector2(300, 150));
painter2D.LineTo(new Vector2(10, 150));
painter2D.ClosePath();

// Inner diamond (hole)
painter2D.MoveTo(new Vector2(150, 50));
painter2D.LineTo(new Vector2(175, 75));
painter2D.LineTo(new Vector2(150, 100));
painter2D.LineTo(new Vector2(125, 75));
painter2D.ClosePath();

painter2D.Fill(FillRule.OddEven);
```

## Background Images in C#

```csharp
// From AssetDatabase (Editor)
myElement.style.backgroundImage = AssetDatabase.LoadAssetAtPath<Texture2D>("path/to/image.png");
myElement.style.backgroundImage = new StyleBackground(AssetDatabase.LoadAssetAtPath<Sprite>("path/to/sprite.png"));

// From Resources (Runtime)
myElement.style.backgroundImage = Resources.Load<Texture2D>("imageFile");

// Editor built-in icons
myElement.style.backgroundImage = EditorGUIUtility.FindTexture("CloudConnect");
myElement.style.backgroundImage = Background.FromTexture2D(EditorGUIUtility.IconContent("FolderOpened Icon").image as Texture2D);
```

### Background Scale Mode in C# (Unity 6000)

```csharp
myElement.style.backgroundPositionX = BackgroundPropertyHelper.ConvertScaleModeToBackgroundPosition(ScaleMode.ScaleAndCrop);
myElement.style.backgroundPositionY = BackgroundPropertyHelper.ConvertScaleModeToBackgroundPosition(ScaleMode.ScaleAndCrop);
myElement.style.backgroundRepeat = BackgroundPropertyHelper.ConvertScaleModeToBackgroundRepeat(ScaleMode.ScaleAndCrop);
myElement.style.backgroundSize = BackgroundPropertyHelper.ConvertScaleModeToBackgroundSize(ScaleMode.ScaleAndCrop);
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Namespace errors | Mixing `UnityEditor.UIElements` in runtime | Use `UnityEngine.UIElements` for runtime |
| MonoBehaviours disabled | Runtime live reload | Move init to `OnEnable`/`OnDisable` |
| Event handlers duplicated | Not unregistering | Always unregister in `OnDisable` |
| Binding not updating | Wrong path syntax | Runtime: `List[2]`, SerializedObject: `List.Array.data[2]` |
| `<Bindings>` broken | `engine=`/`editor=` attrs on UXML root | Remove those attributes |
| Recursive ChangeEvent | Setting `.value` inside callback | Use `SetValueWithoutNotify()` |
| Pseudo-state wrong timing | Checking during event callback | Check on next frame via scheduler |
| Type converter fails | Source/dest types don't match exactly | No implicit `int`↔`float` unless `UnityEngine.Object` |

## Best Practices

1. **OnEnable/OnDisable for runtime** — Critical for live reload compatibility
2. **Separate Editor and Runtime code** — Different namespaces, different patterns
3. **Load assets via serialization** — `[SerializeField]` for runtime, `AssetDatabase` for editor
4. **Clean up event handlers** — Prevent memory leaks and duplicate registrations
5. **Use `Q<T>()` for querying** — Type-safe, concise
6. **`SetValueWithoutNotify` when updating from data** — Avoid recursive events
7. **Bind at lowest common parent** — Don't bind individual elements if a parent covers all
8. **Never bind same element twice** — Performance impact
