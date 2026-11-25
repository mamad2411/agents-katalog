---
name: unity-editor
description: >
  Unity 6000.3 LTS editor extension patterns. Covers EditorWindow,
  Custom Inspectors, PropertyDrawers, Gizmos, and IMGUI.
  Trigger: When creating editor tools, custom inspectors,
  or extending the Unity Editor in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Creating EditorWindow-based tools (dockable editor windows)
- Building Custom Inspectors for MonoBehaviours or ScriptableObjects
- Implementing PropertyDrawers for custom attribute-based editing
- Drawing Gizmos in Scene view or Game view overlays
- Using IMGUI for immediate-mode editor UI (legacy but still supported)
- Extending the Unity Editor with menus, handles, and selection tools
- Combining UI Toolkit (UITK) with IMGUI in hybrid editors

## Critical Rules

### UI Toolkit is Preferred in Unity 6000 — IMGUI is Legacy

| Aspect | UI Toolkit (Recommended) | IMGUI (Legacy) |
|--------|-------------------------|----------------|
| **Namespace** | `UnityEditor.UIElements` | `UnityEditor.EditorGUI`, `UnityEditor.GUILayout` |
| **Pattern** | `EditorWindow` + VisualElement tree | `OnGUI()` immediate mode |
| **State** | Retained (event-driven) | Recreated every frame |
| **Live reload** | Supported via `CreateGUI()` | Breaks on domain reload |
| **Best for** | Complex UIs, inspector extensions | Quick tools, gizmos |

**For new tools: Use UI Toolkit.** IMGUI only for Gizmos/Handles and compatibility.

### Editor Scripts Require Assembly Definitions

```csharp
// ✅ CORRECT — Place editor scripts in an Editor assembly
// Assets/Editor/MyTool/MyToolEditor.cs
namespace MyTool.Editor
{
    public class MyToolEditor : EditorWindow { }
}

// ❌ WRONG — Editor code in Runtime assembly causes build errors
// Assets/Scripts/MyTool.cs (from runtime assembly)
namespace MyTool
{
    public class MyTool : EditorWindow { } // Won't compile in builds
}
```

Use one of these structures:
```
Assets/
├── Editor/
│   ├── Editor.asmdef           # Editor-only assembly
│   ├── MyToolEditor.cs
│   └── UI/
│       └── MyToolWindow.uxml
└── Runtime/
    ├── Runtime.asmdef
    └── MyComponent.cs
```

### Use `[InitializeOnLoadMethod]` for Static Constructors

```csharp
// ✅ CORRECT — Static initialization in editor
public static class EditorPrefsHelper
{
    static EditorPrefsHelper()
    {
        // Called on domain reload — safe to access Editor prefs
        if (!EditorPrefs.HasKey("MyKey"))
            EditorPrefs.SetInt("MyKey", 0);
    }
}

// ✅ ALSO CORRECT — Use attribute instead of static constructor
public static class MenuAutomation
{
    [InitializeOnLoadMethod]
    private static void Initialize()
    {
        // Guaranteed to run after domain reload
    }
}
```

### SerializedObject is Thread-Safe — Don't Access GameObjects Directly

```csharp
// ✅ CORRECT — Use SerializedObject for inspector data
[CustomEditor(typeof(MyComponent))]
public class MyComponentEditor : Editor
{
    public override void OnInspectorGUI()
    {
        serializedObject.Update();
        DrawPropertiesExcluding(serializedObject, "m_Script");
        serializedObject.ApplyModifiedProperties();
    }
}

// ❌ WRONG — target.GetComponent() may fail during domain reload
void OnInspectorGUI()
{
    var comp = target as MyComponent;
    var rb = comp.GetComponent<Rigidbody>(); // Risky
}
```

## EditorWindow

### Basic EditorWindow with UI Toolkit

```csharp
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;

public class LevelGeneratorWindow : EditorWindow
{
    [SerializeField] private VisualTreeAsset m_WindowUxml;

    [MenuItem("Tools/Level Generator")]
    public static void ShowWindow()
    {
        var wnd = GetWindow<LevelGeneratorWindow>();
        wnd.titleContent = new GUIContent("Level Generator", EditorGUIUtility.IconContent("d_SceneViewFx").image);
        wnd.minSize = new Vector2(400, 300);
    }

    public void CreateGUI()
    {
        rootVisualElement.Clear();

        // Load and clone UXML
        if (m_WindowUxml != null)
            m_WindowUxml.CloneTree(rootVisualElement);
        else
            CreateDefaultUI();

        // Setup callbacks
        var generateBtn = rootVisualElement.Q<Button>("generate-button");
        generateBtn.clicked += OnGenerateClicked;

        var clearBtn = rootVisualElement.Q<Button>("clear-button");
        clearBtn.clicked += OnClearClicked;
    }

    private void CreateDefaultUI()
    {
        var container = new VisualElement { style = { padding = 10 } };
        container.Add(new Label("Level Generator") { style = { fontSize = 16, unityFontStyleAndWeight = FontStyle.Bold } });

        var buttonRow = new VisualElement { style = { flexDirection = FlexDirection.Row, marginTop = 10 } };
        buttonRow.Add(new Button(OnGenerateClicked) { text = "Generate", name = "generate-button" });
        buttonRow.Add(new Button(OnClearClicked) { text = "Clear", name = "clear-button" });
        container.Add(buttonRow);

        rootVisualElement.Add(container);
    }

    private void OnGenerateClicked()
    {
        Debug.Log("Generating level...");
    }

    private void OnClearClicked()
    {
        Debug.Log("Clearing level...");
    }
}
```

### EditorWindow with UI Toolkit + SerializedObject Binding

```csharp
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;
using UnityEditor.UIElements;

public class ComponentConfigWindow : EditorWindow
{
    [SerializeField] private VisualTreeAsset m_VisualTree;
    [SerializeField] private ComponentConfig m_Config; // ScriptableObject reference

    [MenuItem("Window/Component Config")]
    public static void Show() => GetWindow<ComponentConfigWindow>();

    public void CreateGUI()
    {
        m_VisualTree.CloneTree(rootVisualElement);

        // Bind to ScriptableObject
        if (m_Config != null)
        {
            rootVisualElement.Bind(new SerializedObject(m_Config));
        }

        // Setup actions
        rootVisualElement.Q<Button>("save-button").clicked += SaveConfig;
        rootVisualElement.Q<Button>("reset-button").clicked += ResetConfig;
    }

    private void SaveConfig()
    {
        EditorUtility.SetDirty(m_Config);
        AssetDatabase.SaveAssetIfDirty(m_Config);
    }

    private void ResetConfig()
    {
        if (EditorUtility.DisplayDialog("Reset Config?", "Reset to defaults?", "Yes", "Cancel"))
        {
            Undo.RecordObject(m_Config, "Reset Config");
            m_Config.Reset();
            serializedObject.Update();
        }
    }
}
```

### EditorWindow with IMGUI (Legacy Pattern)

```csharp
using UnityEditor;
using UnityEngine;

public class LegacyToolWindow : EditorWindow
{
    private bool m_ToggleState;
    private float m_SliderValue = 0.5f;
    private string m_TextFieldValue = "Default";

    [MenuItem("Tools/Legacy Tool")]
    public static void ShowWindow() => GetWindow<LegacyToolWindow>("Legacy Tool");

    private void OnGUI()
    {
        //GUILayout.BeginArea(new Rect(0, 0, position.width, position.height));
        GUILayout.Label("Legacy IMGUI Window", EditorStyles.boldLabel);

        EditorGUILayout.Space();

        m_ToggleState = EditorGUILayout.Toggle("Enable Feature", m_ToggleState);
        m_SliderValue = EditorGUILayout.Slider("Intensity", m_SliderValue, 0f, 1f);
        m_TextFieldValue = EditorGUILayout.TextField("Name", m_TextFieldValue);

        EditorGUILayout.Space();

        EditorGUILayout.BeginHorizontal();
        if (GUILayout.Button("Apply"))
            ApplySettings();
        if (GUILayout.Button("Reset"))
            ResetSettings();
        EditorGUILayout.EndHorizontal();

        //GUILayout.EndArea();
    }

    private void ApplySettings()
    {
        Debug.Log($"Applying: Toggle={m_ToggleState}, Slider={m_SliderValue}, Text={m_TextFieldValue}");
    }

    private void ResetSettings()
    {
        Undo.RecordObject(this, "Reset Tool Settings");
        m_ToggleState = false;
        m_SliderValue = 0.5f;
        m_TextFieldValue = "Default";
        Repaint();
    }
}
```

### Hybrid EditorWindow: UI Toolkit + IMGUI for Handles

```csharp
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;

public class HybridHandlesWindow : EditorWindow
{
    private Vector3 m_Center = Vector3.zero;
    private float m_Radius = 5f;
    private bool m_ShowSphere = true;

    [MenuItem("Tools/Hybrid Handles")]
    public static void Show() => GetWindow<HybridHandlesWindow>();

    private void OnEnable()
    {
        // Subscribe to scene view for gizmo rendering
        SceneView.duringSceneGui += OnSceneGUI;
    }

    private void OnDisable()
    {
        SceneView.duringSceneGui -= OnSceneGUI;
    }

    public void CreateGUI()
    {
        rootVisualElement.Clear();

        var label = new Label("Transform Handles") { style = { fontSize = 14, unityFontStyleAndWeight = FontStyle.Bold } };
        rootVisualElement.Add(label);

        var centerField = new Vector3Field("Center") { value = m_Center };
        centerField.RegisterValueChangedCallback(evt =>
        {
            Undo.RecordObject(this, "Change Center");
            m_Center = evt.newValue;
        });
        rootVisualElement.Add(centerField);

        var radiusSlider = new Slider("Radius") { lowValue = 1f, highValue = 20f, value = m_Radius };
        radiusSlider.RegisterValueChangedCallback(evt =>
        {
            Undo.RecordObject(this, "Change Radius");
            m_Radius = evt.newValue;
        });
        rootVisualElement.Add(radiusSlider);

        var toggle = new Toggle("Show Sphere") { value = m_ShowSphere };
        toggle.RegisterValueChangedCallback(evt =>
        {
            Undo.RecordObject(this, "Toggle Sphere");
            m_ShowSphere = evt.newValue;
            SceneView.RepaintAll();
        });
        rootVisualElement.Add(toggle);
    }

    private void OnSceneGUI(SceneView sceneView)
    {
        if (!m_ShowSphere) return;

        // Draw handle for center position
        EditorGUI.BeginChangeCheck();
        Vector3 newCenter = Handles.PositionHandle(m_Center, Quaternion.identity);
        if (EditorGUI.EndChangeCheck())
        {
            Undo.RecordObject(this, "Move Center");
            m_Center = newCenter;
            rootVisualElement.Q<Vector3Field>("Center")?.SetValueWithoutNotify(m_Center);
        }

        // Draw sphere gizmo
        Handles.color = new Color(0.5f, 0.8f, 1f, 0.3f);
        Handles.SphereHandleCap(0, m_Center, Quaternion.identity, m_Radius * 2, EventType.Repaint);
        Handles.color = new Color(0.5f, 0.8f, 1f, 1f);
        Handles.DrawWireDisc(m_Center, Vector3.up, m_Radius);
        Handles.DrawWireDisc(m_Center, Vector3.right, m_Radius);
        Handles.DrawWireDisc(m_Center, Vector3.forward, m_Radius);
    }
}
```

### Dockable EditorWindow with Preset

```csharp
using UnityEditor;
using UnityEngine;

[InitializeOnLoad]
public static class PresetRegistration
{
    static PresetRegistration()
    {
        // Register preset handlers
        Preset.RegisterPresetHandler("CustomTransform", new TransformPresetHandler());
    }
}

public class TransformPresetHandler : PresetHandler
{
    public override void Apply(object target)
    {
        if (target is Transform t)
        {
            Undo.RecordObject(t, "Apply Transform Preset");
            t.localPosition = Vector3.zero;
            t.localRotation = Quaternion.identity;
            t.localScale = Vector3.one;
        }
    }
}
```

## Custom Inspectors

### UI Toolkit Custom Inspector (Unity 6000 Recommended)

```csharp
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;
using UnityEditor.UIElements;

[CustomEditor(typeof(SplineComponent))]
public class SplineComponentEditor : Editor
{
    [SerializeField] private VisualTreeAsset m_InspectorUxml;
    [SerializeField] private VisualTreeAsset m_PointRowUxml;

    private SplineComponent m_Target;
    private VisualElement m_PointsContainer;

    private void OnEnable()
    {
        m_Target = target as SplineComponent;
    }

    public override VisualElement CreateInspectorGUI()
    {
        var container = new VisualElement { style = { padding = 10 } };

        // Header
        var header = new VisualElement { style = { flexDirection = FlexDirection.Row, alignItems = Align.Center } };
        header.Add(new Label("Spline Configuration") { style = { fontSize = 14, unityFontStyleAndWeight = FontStyle.Bold, flexGrow = 1 } });
        var refreshBtn = new Button(() => m_Target.RecalculateLength()) { text = "Refresh" };
        header.Add(refreshBtn);
        container.Add(header);

        EditorGUILayout.Space();

        // Default property fields (auto-bound)
        var enabledField = new PropertyField(serializedObject.FindProperty("m_Enabled"));
        container.Add(enabledField);

        var loopField = new PropertyField(serializedObject.FindProperty("m_IsLooping"));
        container.Add(loopField);

        var resolutionField = new PropertyField(serializedObject.FindProperty("m_Resolution"));
        container.Add(resolutionField);

        // Custom points section
        container.Add(new Label("Control Points") { style = { marginTop = 10, marginBottom = 5 } });

        m_PointsContainer = new VisualElement { name = "points-container", style = { flexDirection = FlexDirection.Column } };
        container.Add(m_PointsContainer);

        var addPointBtn = new Button(AddPoint) { text = "Add Point", style = { marginTop = 5 } };
        container.Add(addPointBtn);

        // Initial population
        RefreshPointsList();

        return container;
    }

    private void RefreshPointsList()
    {
        m_PointsContainer.Clear();

        if (m_Target.ControlPoints == null) return;

        for (int i = 0; i < m_Target.ControlPoints.Count; i++)
        {
            var pointData = m_Target.ControlPoints[i];
            var row = CreatePointRow(i, pointData);
            m_PointsContainer.Add(row);
        }
    }

    private VisualElement CreatePointRow(int index, ControlPoint point)
    {
        var row = new VisualElement { style = { flexDirection = FlexDirection.Row, marginBottom = 5 } };

        var indexLabel = new Label($"Point {index}") { style = { width = 60 } };
        row.Add(indexLabel);

        var posField = new Vector3Field { value = point.Position };
        posField.RegisterValueChangedCallback(evt =>
        {
            Undo.RecordObject(m_Target, "Move Control Point");
            m_Target.ControlPoints[index].Position = evt.newValue;
            EditorUtility.SetDirty(m_Target);
        });
        row.Add(posField);

        var deleteBtn = new Button(() => RemovePoint(index)) { text = "X" };
        deleteBtn.style.width = 30;
        row.Add(deleteBtn);

        return row;
    }

    private void AddPoint()
    {
        Undo.RecordObject(m_Target, "Add Control Point");
        m_Target.ControlPoints.Add(new ControlPoint { Position = Vector3.zero });
        EditorUtility.SetDirty(m_Target);
        RefreshPointsList();
    }

    private void RemovePoint(int index)
    {
        Undo.RecordObject(m_Target, "Remove Control Point");
        m_Target.ControlPoints.RemoveAt(index);
        EditorUtility.SetDirty(m_Target);
        RefreshPointsList();
    }
}
```

### IMGUI Custom Inspector (Legacy)

```csharp
using UnityEditor;
using UnityEngine;

[CustomEditor(typeof(HealthSystem))]
public class HealthSystemEditor : Editor
{
    private bool m_ShowDebugInfo = false;

    public override void OnInspectorGUI()
    {
        var healthSystem = target as HealthSystem;

        // Draw script field (locked)
        GUI.enabled = false;
        EditorGUILayout.ObjectField("Script", MonoScript.FromMonoBehaviour(healthSystem), typeof(MonoBehaviour));
        GUI.enabled = true;

        EditorGUILayout.Space();

        // Standard serialized properties
        serializedObject.Update();
        DrawPropertiesExcluding(serializedObject, "m_Script", "debugInfo");

        // Custom drawing
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("Runtime Info", EditorStyles.boldLabel);

        m_ShowDebugInfo = EditorGUILayout.Foldout(m_ShowDebugInfo, "Debug Information");
        if (m_ShowDebugInfo)
        {
            EditorGUI.indentLevel++;
            EditorGUILayout.LabelField($"Current Health: {healthSystem.CurrentHealth}");
            EditorGUILayout.LabelField($"Max Health: {healthSystem.MaxHealth}");
            EditorGUILayout.LabelField($"Shield: {healthSystem.Shield}");
            EditorGUILayout.LabelField($"Invulnerable: {healthSystem.IsInvulnerable}");

            if (Application.isPlaying)
            {
                EditorGUILayout.LabelField($"Health %: {healthSystem.CurrentHealth / healthSystem.MaxHealth * 100:F1}%");
            }
            EditorGUI.indentLevel--;
        }

        // Apply modifications
        serializedObject.ApplyModifiedProperties();
    }
}
```

### Multi-object Custom Inspector

```csharp
[CustomEditor(typeof(MaterialQuality), true)] // true = multi-object
public class MaterialQualityEditor : Editor
{
    public override void OnInspectorGUI()
    {
        var materials = targets.Cast<MaterialQuality>().ToArray();

        EditorGUILayout.Space();
        EditorGUILayout.LabelField($"Editing {materials.Length} Material(s)", EditorStyles.boldLabel);
        EditorGUILayout.Space();

        serializedObject.Update();

        // Draw for all selected objects
        foreach (var material in materials)
        {
            EditorGUILayout.LabelField($"Material: {material.name}", EditorStyles.boldLabel);
            EditorGUI.indentLevel++;

            // Per-object settings
            material.qualityLevel = (QualityLevel)EditorGUILayout.EnumPopup("Quality", material.qualityLevel);
            material.lodBias = EditorGUILayout.Slider("LOD Bias", material.lodBias, 0.1f, 2f);

            EditorGUI.indentLevel--;
            EditorGUILayout.Space();
        }

        serializedObject.ApplyModifiedProperties();
    }
}
```

### Editor with Scene Drop Handler

```csharp
[CustomEditor(typeof(ZoneComponent))]
public class ZoneComponentEditor : Editor
{
    private SerializedProperty m_ConnectedZones;
    private SerializedProperty m_ZoneId;

    private void OnEnable()
    {
        m_ConnectedZones = serializedObject.FindProperty("m_ConnectedZones");
        m_ZoneId = serializedObject.FindProperty("m_ZoneId");
    }

    public override void OnInspectorGUI()
    {
        serializedObject.Update();

        EditorGUILayout.PropertyField(m_ZoneId);
        EditorGUILayout.PropertyField(m_ConnectedZones);

        // Custom drag-drop zone
        EditorGUILayout.Space();
        Rect dropRect = EditorGUILayout.GetControlRect(false, 50);
        EditorGUI.LabelField(dropRect, "Drop Prefabs Here", EditorStyles.helpBox);

        if (Event.current.type == EventType.DragPerform && dropRect.Contains(Event.current.mousePosition))
        {
            DragAndDrop.AcceptDrag();
            foreach (var obj in DragAndDrop.objectReferences)
            {
                if (obj is GameObject go)
                {
                    AddConnectedZone(go);
                }
            }
        }

        serializedObject.ApplyModifiedProperties();
    }

    private void AddConnectedZone(GameObject prefab)
    {
        var zone = target as ZoneComponent;
        Undo.RecordObject(zone, "Add Connected Zone");
        zone.ConnectedZones.Add(prefab);
        EditorUtility.SetDirty(zone);
    }
}
```

## PropertyDrawers

### Attribute-Based PropertyDrawer

```csharp
// Custom attribute
[AttributeUsage(AttributeTargets.Field)]
public class MinMaxRangeAttribute : Attribute
{
    public float Min { get; }
    public float Max { get; }

    public MinMaxRangeAttribute(float min, float max)
    {
        Min = min;
        Max = max;
    }
}

// Property drawer
[CustomPropertyDrawer(typeof(MinMaxRangeAttribute))]
public class MinMaxRangeDrawer : PropertyDrawer
{
    public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
    {
        var attr = attribute as MinMaxRangeAttribute;

        // property is a Vector2 holding (min, max)
        EditorGUI.BeginProperty(position, label, property);

        position = EditorGUI.PrefixLabel(position, label);

        float halfWidth = position.width * 0.5f - 4f;
        Rect minRect = new Rect(position.x, position.y, halfWidth, position.height);
        Rect maxRect = new Rect(position.x + halfWidth + 8f, position.y, halfWidth, position.height);

        EditorGUI.BeginChangeCheck();

        float minValue = EditorGUI.FloatField(minRect, property.vector2Value.x);
        float maxValue = EditorGUI.FloatField(maxRect, property.vector2Value.y);

        if (EditorGUI.EndChangeCheck())
        {
            property.vector2Value = new Vector2(
                Mathf.Clamp(minValue, attr.Min, attr.Max),
                Mathf.Clamp(maxValue, minValue, attr.Max)
            );
        }

        EditorGUI.EndProperty();
    }
}

// Usage in MonoBehaviour
public class PlayerStats : MonoBehaviour
{
    [MinMaxRange(0f, 100f)]
    public Vector2 damageRange;

    [MinMaxRange(-50f, 50f)]
    public Vector2 temperatureRange;
}
```

### Custom PropertyDrawer for Complex Types

```csharp
[CustomPropertyDrawer(typeof(AnimationCurve))]
public class CurveDrawer : PropertyDrawer
{
    private AnimationCurve m_CachedCurve;
    private Rect m_CurveRect;

    public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
    {
        EditorGUI.BeginProperty(position, label, property);

        // Draw label
        position = EditorGUI.PrefixLabel(position, label);

        // Draw curve field
        EditorGUI.BeginChangeCheck();
        var curve = EditorGUI.CurveField(position, property.animationCurveValue);
        if (EditorGUI.EndChangeCheck())
        {
            property.animationCurveValue = curve;
        }

        EditorGUI.EndProperty();
    }

    public override float GetPropertyHeight(SerializedProperty property, GUIContent label)
    {
        return EditorGUIUtility.singleLineHeight * 2 + 5;
    }
}
```

### PropertyDrawer for ScriptableObject

```csharp
[CustomPropertyDrawer(typeof(ItemData))]
public class ItemDataDrawer : PropertyDrawer
{
    public override VisualElement CreatePropertyGUI(SerializedProperty property)
    {
        var container = new VisualElement { style = { flexDirection = FlexDirection.Column } };

        // Header
        var header = new VisualElement { style = { flexDirection = FlexDirection.Row } };
        header.Add(new Label("Item Data") { style = { flexGrow = 1, fontSize = 12, unityFontStyleAndWeight = FontStyle.Bold } });
        container.Add(header);

        // Properties
        var nameField = new PropertyField(property.FindPropertyRelative("m_ItemName")));
        var iconField = new PropertyField(property.FindPropertyRelative("m_Icon"));
        var rarityField = new PropertyField(property.FindPropertyRelative("m_Rarity"));
        var priceField = new PropertyField(property.FindPropertyRelative("m_Price"));

        container.Add(nameField);
        container.Add(iconField);
        container.Add(rarityField);
        container.Add(priceField);

        return container;
    }
}
```

### Decorator Drawer (Adds UI above a property)

```csharp
public class SectionHeaderAttribute : Attribute
{
    public string Title { get; }
    public float Height { get; }

    public SectionHeaderAttribute(string title, float height = 20f)
    {
        Title = title;
        Height = height;
    }
}

[CustomPropertyDrawer(typeof(SectionHeaderAttribute))]
public class SectionHeaderDrawer : DecoratorDrawer
{
    public override void OnGUI(Rect position)
    {
        var attr = attribute as SectionHeaderAttribute;

        // Draw section header
        var headerRect = new Rect(position.x, position.y, position.width, attr.Height);
        EditorGUI.DropShadowLabel(headerRect, attr.Title, EditorStyles.boldLabel);
    }

    public override float GetHeight()
    {
        return (attribute as SectionHeaderAttribute).Height + 5;
    }
}

// Usage
public class EnemyConfig : MonoBehaviour
{
    [SectionHeader("Movement Settings")]
    public float moveSpeed;

    [SectionHeader("Combat Settings")]
    public int attackDamage;
}
```

## Gizmos and Handles

### Gizmos in MonoBehaviour

```csharp
public class PathGizmo : MonoBehaviour
{
    public Vector3[] waypoints = new Vector3[]
    {
        Vector3.zero,
        new Vector3(5, 0, 0),
        new Vector3(5, 0, 5),
        new Vector3(0, 0, 5)
    };

    private void OnDrawGizmos()
    {
        if (waypoints == null || waypoints.Length < 2) return;

        Gizmos.color = Color.cyan;

        // Draw path lines
        for (int i = 0; i < waypoints.Length - 1; i++)
        {
            Gizmos.DrawLine(waypoints[i], waypoints[i + 1]);
        }

        // Draw waypoint spheres
        Gizmos.color = Color.yellow;
        foreach (var point in waypoints)
        {
            Gizmos.DrawSphere(point, 0.3f);
        }
    }

    private void OnDrawGizmosSelected()
    {
        // Only when selected in hierarchy
        Gizmos.color = Color.green;
        Gizmos.DrawWireSphere(transform.position, 1f);

        // Draw facing direction
        Gizmos.color = Color.red;
        Gizmos.DrawLine(transform.position, transform.position + transform.forward * 2);
    }
}
```

### Handles in EditorWindow (SceneView)

```csharp
public class TransformHandleEditor : EditorWindow
{
    private Vector3 m_Pivot = Vector3.zero;
    private Quaternion m_Rotation = Quaternion.identity;
    private Vector3 m_Scale = Vector3.one;

    [MenuItem("Tools/Transform Handles")]
    public static void Show() => GetWindow<TransformHandleEditor>();

    private void OnEnable()
    {
        SceneView.duringSceneGui += OnSceneGUI;
    }

    private void OnDisable()
    {
        SceneView.duringSceneGui -= OnSceneGui;
    }

    private void OnSceneGUI(SceneView sceneView)
    {
        // Position handle
        EditorGUI.BeginChangeCheck();
        m_Pivot = Handles.PositionHandle(m_Pivot, Quaternion.identity);
        if (EditorGUI.EndChangeCheck())
        {
            Repaint();
        }

        // Rotation handle
        EditorGUI.BeginChangeCheck();
        m_Rotation = Handles.RotationHandle(m_Rotation, m_Pivot);
        if (EditorGUI.EndChangeCheck())
        {
            Repaint();
        }

        // Scale handle
        EditorGUI.BeginChangeCheck();
        m_Scale = Handles.ScaleHandle(m_Scale, m_Pivot, Quaternion.identity, 1f);
        if (EditorGUI.EndChangeCheck())
        {
            Repaint();
        }

        // Custom handles
        DrawBoundingBox();
    }

    private void DrawBoundingBox()
    {
        var size = m_Scale * 2f;
        var center = m_Pivot;

        // Draw box
        Handles.color = new Color(1f, 0.5f, 0f, 0.5f);
        Handles.DrawWireCube(center, size);

        // Draw face handles for resizing
        Vector3[] dirs = { Vector3.right, Vector3.up, Vector3.forward };
        foreach (var dir in dirs)
        {
            for (int sign = -1; sign <= 1; sign += 2)
            {
                var faceCenter = center + dir * sign * size.magnitude * 0.5f;
                var faceSize = new Vector3(size.y, size.z, 0);
                Handles.DrawSolidRectangle(new Rect(faceCenter, faceSize), Color.orange * 0.2f);
            }
        }
    }
}
```

### Custom Handle for Number Input

```csharp
public class NumberHandleExample : EditorWindow
{
    private float m_Value = 10f;
    private float m_Sensitivity = 0.1f;

    [MenuItem("Tools/Number Handle")]
    public static void Show() => GetWindow<NumberHandleExample>();

    private void OnEnable()
    {
        SceneView.duringSceneGui += OnSceneGUI;
    }

    private void OnDisable()
    {
        SceneView.duringSceneGui -= OnSceneGUI;
    }

    private void OnSceneGUI(SceneView sceneView)
    {
        var pos = Vector3.zero;

        // Position marker
        Handles.Label(pos, $"Value: {m_Value:F1}");

        // Slider-like drag handle
        EditorGUI.BeginChangeCheck();
        float newValue = Handles.HorizontalSlider(pos, m_Value, 0f, 100f, Handles.CapStyle.Diamond, m_Sensitivity);
        if (EditorGUI.EndChangeCheck())
        {
            Undo.RecordObject(this, "Change Value");
            m_Value = newValue;
            Repaint();
        }

        // Free scalar handle
        EditorGUI.BeginChangeCheck();
        var scale = Handles.ScaleValueHandle(Vector3.one, pos, Quaternion.identity, m_Value, Handles.CubeHandleCap, 0.5f);
        if (EditorGUI.EndChangeCheck())
        {
            Undo.RecordObject(this, "Scale Value");
            m_Value = scale.x;
            Repaint();
        }
    }
}
```

### Button Handle for Interactive Manipulation

```csharp
public class ButtonHandle : EditorWindow
{
    private bool m_IsDragging = false;
    private Vector3 m_DragStart;

    [MenuItem("Tools/Button Handle Demo")]
    public static void Show() => GetWindow<ButtonHandle>();

    private void OnEnable()
    {
        SceneView.duringSceneGui += OnSceneGUI;
    }

    private void OnDisable()
    {
        SceneView.duringSceneGui -= OnSceneGUI;
    }

    private void OnSceneGUI(SceneView sceneView)
    {
        var center = Vector3.zero;

        // Draw button-like handle
        EditorGUI.BeginChangeCheck();
        Vector3 newPos = Handles.Slider(center, Vector3.up, 2f, Handles.CapStyle.Circle, 0.5f);
        bool dragged = EditorGUI.EndChangeCheck();

        if (dragged && !m_IsDragging)
        {
            m_IsDragging = true;
            m_DragStart = newPos;
        }
        else if (!dragged && m_IsDragging)
        {
            m_IsDragging = false;
            Debug.Log($"Dragged from {m_DragStart} to {newPos}, distance: {Vector3.Distance(m_DragStart, newPos)}");
        }

        // Button with color based on state
        Handles.color = m_IsDragging ? Color.green : Color.red;
        if (Handles.Button(center + Vector3.right * 3f, Quaternion.identity, 0.5f, 0.5f, Handles.CubeHandleCap))
        {
            Debug.Log("Button clicked!");
        }

        // Dot handle for selection
        Handles.color = Color.white;
        if (Handles.Button(center + Vector3.left * 3f, Quaternion.identity, 0.2f, 0.2f, Handles.DotHandleCap))
        {
            Debug.Log("Dot selected!");
        }
    }
}
```

## IMGUI Layout

### GUILayout Utilities

```csharp
public class GUILayoutDemo : EditorWindow
{
    [MenuItem("Tools/GUILayout Demo")]
    public static void Show() => GetWindow<GUILayoutDemo>();

    private void OnGUI()
    {
        // BeginVertical/EndVertical for vertical layout
        GUILayout.BeginVertical("Box", GUILayout.Height(200));
        GUILayout.Label("This is a vertical layout");
        GUILayout.Button("Button 1");
        GUILayout.Button("Button 2");
        GUILayout.FlexibleSpace();
        GUILayout.EndVertical();

        // BeginHorizontal/EndHorizontal for horizontal layout
        GUILayout.BeginHorizontal();
        GUILayout.Button("Left");
        GUILayout.Button("Center");
        GUILayout.Button("Right");
        GUILayout.EndHorizontal();

        // Area for explicit positioning
        GUILayout.BeginArea(new Rect(10, 250, 300, 100));
        GUILayout.Label("Area-based layout");
        if (GUILayout.Button("Area Button"))
            Debug.Log("Area button clicked!");
        GUILayout.EndArea();

        // Scroll view
        scrollPos = EditorGUILayout.BeginScrollView(scrollPos, GUILayout.Height(150));
        for (int i = 0; i < 20; i++)
        {
            GUILayout.Label($"Item {i}");
        }
        EditorGUILayout.EndScrollView();
    }

    private Vector2 scrollPos = Vector2.zero;
}
```

### EditorGUILayout vs EditorGUI

| Class | Behavior | Use Case |
|-------|----------|----------|
| `EditorGUI` | Explicit Rect positioning | Complex custom layouts |
| `EditorGUILayout` | Automatic layout | Most cases, simpler code |
| `GUILayout` | Auto-layout, no indentation | Toolbar-style layouts |

```csharp
void OnGUI()
{
    // EditorGUI — manual positioning
    EditorGUI.LabelField(new Rect(0, 0, 100, 20), "Label");
    EditorGUI.IntField(new Rect(100, 0, 100, 20), "Value", myInt);

    // EditorGUILayout — auto-layout
    EditorGUILayout.LabelField("Label");
    myInt = EditorGUILayout.IntField("Value", myInt);

    // GUILayout — no indentation handling
    GUILayout.Label("No indentation");
}
```

### Custom IMGUI Inspector with Foldout Groups

```csharp
[CustomEditor(typeof(AdvancedComponent))]
public class AdvancedComponentEditor : Editor
{
    private bool m_ShowGeneral = true;
    private bool m_ShowPhysics = true;
    private bool m_ShowVisuals = false;

    public override void OnInspectorGUI()
    {
        var comp = target as AdvancedComponent;

        // Script field (disabled)
        GUI.enabled = false;
        EditorGUILayout.ObjectField("Script", MonoScript.FromMonoBehaviour(comp), typeof(MonoBehaviour));
        GUI.enabled = true;

        EditorGUILayout.Space();

        // General settings
        m_ShowGeneral = EditorGUILayout.Foldout(m_ShowGeneral, "General Settings", true);
        if (m_ShowGeneral)
        {
            EditorGUI.indentLevel++;
            comp.moveSpeed = EditorGUILayout.FloatField("Move Speed", comp.moveSpeed);
            comp.acceleration = EditorGUILayout.Slider("Acceleration", comp.acceleration, 0f, 1f);
            comp.enabled = EditorGUILayout.Toggle("Enabled", comp.enabled);
            EditorGUI.indentLevel--;
        }

        // Physics settings
        m_ShowPhysics = EditorGUILayout.Foldout(m_ShowPhysics, "Physics Settings", true);
        if (m_ShowPhysics)
        {
            EditorGUI.indentLevel++;
            comp.useGravity = EditorGUILayout.Toggle("Use Gravity", comp.useGravity);
            comp.mass = EditorGUILayout.FloatField("Mass", comp.mass);
            comp.drag = EditorGUILayout.FloatField("Drag", comp.drag);

            EditorGUILayout.Space();
            comp.physicsMaterial = EditorGUILayout.ObjectField("Physics Material", comp.physicsMaterial, typeof(PhysicMaterial));
            EditorGUI.indentLevel--;
        }

        // Visual settings
        m_ShowVisuals = EditorGUILayout.Foldout(m_ShowVisuals, "Visual Settings", true);
        if (m_ShowVisuals)
        {
            EditorGUI.indentLevel++;
            comp.color = EditorGUILayout.ColorField("Color", comp.color);
            comp.visible = EditorGUILayout.Toggle("Visible", comp.visible);
            EditorGUI.indentLevel--;
        }

        // Apply modifications
        if (GUI.changed)
        {
            EditorUtility.SetDirty(comp);
        }
    }
}
```

### IMGUI + Handles Mixed Inspector

```csharp
[CustomEditor(typeof(InteractiveZone))]
public class InteractiveZoneEditor : Editor
{
    private void OnEnable()
    {
        SceneView.duringSceneGui += OnSceneGUI;
    }

    private void OnDisable()
    {
        SceneView.duringSceneGui -= OnSceneGUI;
    }

    public override void OnInspectorGUI()
    {
        serializedObject.Update();

        // Standard properties
        DrawPropertiesExcluding(serializedObject, "m_Script");

        // Custom preview in inspector
        EditorGUILayout.Space();
        var zone = target as InteractiveZone;
        EditorGUILayout.LabelField("Preview", EditorStyles.boldLabel);
        Rect previewRect = GUILayoutUtility.GetRect(0, 100, GUILayout.ExpandWidth(true));
        DrawZonePreview(previewRect, zone);

        serializedObject.ApplyModifiedProperties();
    }

    private void DrawZonePreview(Rect rect, InteractiveZone zone)
    {
        // Simple 2D preview
        GUI.Box(rect, GUIContent.none);

        float centerX = rect.x + rect.width * 0.5f;
        float centerY = rect.y + rect.height * 0.5f;

        var prevColor = GUI.color;
        GUI.color = Color.cyan;
        GUI.DrawRect(new Rect(centerX - 20, centerY - 20, 40, 40), Color.cyan);
        GUI.color = prevColor;

        EditorGUI.DropShadowLabel(new Rect(centerX - 30, centerY + 25, 60, 20), $"{zone.Radius:F0}m");
    }

    private void OnSceneGUI(SceneView sceneView)
    {
        var zone = target as InteractiveZone;

        // Interactive radius handle
        EditorGUI.BeginChangeCheck();
        float newRadius = Handles.RadiusHandle(Quaternion.identity, zone.transform.position, zone.Radius);
        if (EditorGUI.EndChangeCheck())
        {
            Undo.RecordObject(zone, "Change Radius");
            zone.Radius = newRadius;
        }

        // Draw wire sphere
        Handles.color = new Color(0, 1, 1, 0.3f);
        Handles.DrawWireDisc(zone.transform.position, Vector3.up, zone.Radius);

        // Center dot
        Handles.color = Color.white;
        Handles.DrawSolidDisc(zone.transform.position, Vector3.up, 0.2f);
    }
}
```

## Common Mistakes to Prevent

### 1. Not Using SerializedObject in Multi-Edit

```csharp
// ❌ WRONG — Direct target manipulation fails in multi-edit
public override void OnInspectorGUI()
{
    var comp = target as MyComponent; // Only works for single selection
    comp.MyField = EditorGUILayout.Slider("My Field", comp.MyField, 0, 100); // Doesn't sync
}

// ✅ CORRECT — Use SerializedProperty for multi-object support
public override void OnInspectorGUI()
{
    var prop = serializedObject.FindProperty("m_MyField");
    EditorGUILayout.Slider(prop, 0, 100); // Works for multi-edit
}
```

### 2. Forgetting to Call `serializedObject.Update()`/`ApplyModifiedProperties()`

```csharp
// ❌ WRONG — Changes won't persist
public override void OnInspectorGUI()
{
    var prop = serializedObject.FindProperty("m_MyField");
    prop.floatValue = 10f; // Lost
}

// ✅ CORRECT — Proper save cycle
public override void OnInspectorGUI()
{
    serializedObject.Update();
    var prop = serializedObject.FindProperty("m_MyField");
    prop.floatValue = EditorGUILayout.Slider("My Field", prop.floatValue, 0f, 100f);

    if (serializedObject.ApplyModifiedProperties())
    {
        Debug.Log("Saved!");
    }
}

// ✅ ALSO CORRECT — Auto-apply with ApplyModifiedPropertiesWithoutUndo
public override void OnInspectorGUI()
{
    var prop = serializedObject.FindProperty("m_MyField");
    EditorGUILayout.Slider(prop, 0, 100f);
    serializedObject.ApplyModifiedPropertiesWithoutUndo();
}
```

### 3. Creating Editor Windows Without MenuItem

```csharp
// ❌ WRONG — Window won't be accessible
public class MyEditorWindow : EditorWindow { }

// ✅ CORRECT — Menu item to open window
public class MyEditorWindow : EditorWindow
{
    [MenuItem("Window/My Window")]
    public static void Show() => GetWindow<MyEditorWindow>();
}
```

### 4. Not Unsubscribing from SceneView Events

```csharp
// ❌ WRONG — Memory leak, exception on domain reload
private void OnEnable()
{
    SceneView.duringSceneGui += OnSceneGUI;
}
// Missing OnDisable!

// ✅ CORRECT — Proper cleanup
private void OnEnable()
{
    SceneView.duringSceneGui += OnSceneGUI;
}

private void OnDisable()
{
    SceneView.duringSceneGui -= OnSceneGUI;
}
```

### 5. Using Runtime Namespaces in Editor Code

```csharp
// ❌ WRONG — Won't compile in builds
using UnityEngine; // Runtime namespace in editor assembly

// ✅ CORRECT — Use UnityEditor for editor-specific code
#if UNITY_EDITOR
using UnityEditor;
#endif
```

### 6. Modifying Scene Objects During Inspector Draw

```csharp
// ❌ WRONG — Can corrupt scene during undo/redo
public override void OnInspectorGUI()
{
    if (GUILayout.Button("Add Component"))
    {
        target.gameObject.AddComponent<Rigidbody>(); // Dangerous
    }
}

// ✅ CORRECT — Wrap in Undo and check for disallowing
public override void OnInspectorGUI()
{
    if (GUILayout.Button("Add Component"))
    {
        Undo.RecordObject(target, "Add Component");
        target.gameObject.AddComponent<Rigidbody>();
        EditorUtility.SetDirty(target);
    }
}
```

### 7. Drawing Gizmos During Normal Play Mode

```csharp
// ❌ WRONG — Gizmos draw even when component not relevant
private void OnDrawGizmos()
{
    Gizmos.DrawSphere(transform.position, 1f); // Always draws
}

// ✅ CORRECT — Check for selected or specific conditions
private void OnDrawGizmos()
{
    if (!Application.isPlaying && enabled) // Only in edit mode when enabled
    {
        Gizmos.DrawSphere(transform.position, 1f);
    }
}

private void OnDrawGizmosSelected()
{
    Gizmos.DrawWireCube(transform.position, Vector3.one); // Only when selected
}
```

### 8. Forgetting `CreateGUI()` Entry Point for UI Toolkit

```csharp
// ❌ WRONG — UI won't appear (CreateGUI not called automatically)
public class MyWindow : EditorWindow
{
    public void Init()
    {
        // Only called if you call it manually
    }
}

// ✅ CORRECT — Use CreateGUI (called automatically) or call in OnEnable
public class MyWindow : EditorWindow
{
    private void OnEnable()
    {
        CreateGUI();
    }

    public void CreateGUI()
    {
        // Build UI
    }
}
```

## Response Format

When creating editor tools, follow this structure:

### C# Code Block Format

```csharp
using UnityEditor;
using UnityEngine;
// Include appropriate namespaces

public class ExampleEditor : EditorWindow
{
    [MenuItem("Tools/Example")]
    public static void ShowWindow()
    {
        var wnd = GetWindow<ExampleEditor>();
        wnd.titleContent = new GUIContent("Example");
    }

    public void CreateGUI()
    {
        // UI Toolkit pattern (preferred)
        rootVisualElement.Add(new Label("Content"));
    }

    private void OnSceneGUI(SceneView view)
    {
        // Handle drawing
    }
}
```

### File Location Structure

```
Assets/
├── Editor/
│   ├── AssemblyInfo.cs
│   ├── Editor.asmdef              # Editor-only assembly definition
│   ├── Windows/
│   │   ├── MyToolWindow.cs
│   │   └── MyToolWindow.uxml
│   ├── Inspectors/
│   │   └── MyComponentEditor.cs
│   ├── PropertyDrawers/
│   │   └── MyAttributeDrawer.cs
│   └── Gizmos/
│       └── MyGizmoHandler.cs
└── Runtime/
    ├── Scripts.asmdef
    └── (your runtime scripts)
```

### Checklist for Editor Script

- [ ] Placed in `Editor/` folder or Editor assembly
- [ ] Has `[MenuItem]` or is invoked by another editor script
- [ ] Cleans up event subscriptions in `OnDisable()`
- [ ] Uses `SerializedObject` for inspector fields
- [ ] Calls `serializedObject.Update()` before drawing
- [ ] Calls `serializedObject.ApplyModifiedProperties()` after drawing
- [ ] Uses `Undo.RecordObject()` before modifying target
- [ ] For UI Toolkit: uses `CreateGUI()` not `Start()`/`OnEnable()`
- [ ] For handles/gizmos: uses `SceneView.duringSceneGui` delegate

### Cross-Reference with UI Toolkit

For UI Toolkit patterns in editor windows, also see:
- `skills/unity-uitk-csharp` — UI Toolkit C# patterns
- `skills/unity-uxml` — UXML markup syntax
- `skills/unity-uss` — USS styling

UI Toolkit editor elements use `UnityEditor.UIElements` namespace:
```csharp
using UnityEditor;
using UnityEditor.UIElements;
using UnityEngine.UIElements;
```

For runtime UI (in builds), use `UnityEngine.UIElements` only.