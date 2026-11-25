---
name: tools-unity-scriptable-objects
description: Unity ScriptableObject patterns for data management, configuration, and runtime systems.
---

# Unity ScriptableObjects

## Overview

ScriptableObjects are data containers that exist outside the scene hierarchy, ideal for configuration, shared data, and decoupling systems.

## When to Use

- Game configuration and settings
- Item/ability/character definitions
- Shared runtime data
- Event systems
- Dependency injection alternatives

## Basic Patterns

### Data Definition

```csharp
[CreateAssetMenu(fileName = "NewItem", menuName = "Game/Item Definition")]
public class ItemDefinition : ScriptableObject
{
    [Header("Basic Info")]
    public string Id;
    public string DisplayName;
    [TextArea] public string Description;
    public Sprite Icon;
    
    [Header("Stats")]
    public ItemRarity Rarity;
    public int MaxStackSize = 99;
    public int BaseValue;
    
    [Header("Gameplay")]
    public bool IsConsumable;
    public bool IsEquippable;
    public EquipmentSlot EquipSlot;
    
    // Runtime lookup optimization
    private static Dictionary<string, ItemDefinition> s_Lookup;
    
    public static ItemDefinition GetById(string id)
    {
        if (s_Lookup == null)
        {
            BuildLookup();
        }
        return s_Lookup.TryGetValue(id, out var item) ? item : null;
    }
    
    private static void BuildLookup()
    {
        s_Lookup = new Dictionary<string, ItemDefinition>();
        var items = Resources.LoadAll<ItemDefinition>("Items");
        foreach (var item in items)
        {
            s_Lookup[item.Id] = item;
        }
    }
}
```

### Database Pattern

```csharp
[CreateAssetMenu(fileName = "ItemDatabase", menuName = "Game/Item Database")]
public class ItemDatabase : ScriptableObject
{
    [SerializeField] private List<ItemDefinition> _items = new();
    
    private Dictionary<string, ItemDefinition> _lookup;
    
    public IReadOnlyList<ItemDefinition> AllItems => _items;
    
    public void Initialize()
    {
        _lookup = new Dictionary<string, ItemDefinition>();
        foreach (var item in _items)
        {
            if (item != null && !string.IsNullOrEmpty(item.Id))
            {
                _lookup[item.Id] = item;
            }
        }
    }
    
    public ItemDefinition GetItem(string id)
    {
        if (_lookup == null) Initialize();
        return _lookup.TryGetValue(id, out var item) ? item : null;
    }
    
    public IEnumerable<ItemDefinition> GetItemsByRarity(ItemRarity rarity)
    {
        return _items.Where(i => i.Rarity == rarity);
    }
    
#if UNITY_EDITOR
    [ContextMenu("Collect All Items")]
    private void CollectItems()
    {
        _items.Clear();
        var guids = UnityEditor.AssetDatabase.FindAssets("t:ItemDefinition");
        
        foreach (var guid in guids)
        {
            var path = UnityEditor.AssetDatabase.GUIDToAssetPath(guid);
            var item = UnityEditor.AssetDatabase.LoadAssetAtPath<ItemDefinition>(path);
            if (item != null && item != this)
            {
                _items.Add(item);
            }
        }
        
        UnityEditor.EditorUtility.SetDirty(this);
    }
#endif
}
```

## Runtime Data

### Shared Runtime Value

```csharp
[CreateAssetMenu(fileName = "RuntimeInt", menuName = "Runtime/Int Value")]
public class RuntimeInt : ScriptableObject
{
    [SerializeField] private int _initialValue;
    
    [NonSerialized] private int _runtimeValue;
    [NonSerialized] private bool _initialized;
    
    public int Value
    {
        get
        {
            EnsureInitialized();
            return _runtimeValue;
        }
        set
        {
            EnsureInitialized();
            if (_runtimeValue != value)
            {
                _runtimeValue = value;
                OnValueChanged?.Invoke(value);
            }
        }
    }
    
    public event Action<int> OnValueChanged;
    
    private void EnsureInitialized()
    {
        if (!_initialized)
        {
            _runtimeValue = _initialValue;
            _initialized = true;
        }
    }
    
    private void OnEnable()
    {
        _initialized = false;
    }
    
    public void Reset()
    {
        _runtimeValue = _initialValue;
        _initialized = true;
        OnValueChanged?.Invoke(_runtimeValue);
    }
}
```

### Observable Collection

```csharp
[CreateAssetMenu(fileName = "RuntimeList", menuName = "Runtime/List")]
public class RuntimeList<T> : ScriptableObject
{
    [NonSerialized] private List<T> _items = new();
    
    public IReadOnlyList<T> Items => _items;
    public int Count => _items.Count;
    
    public event Action<T> OnItemAdded;
    public event Action<T> OnItemRemoved;
    public event Action OnCleared;
    
    public void Add(T item)
    {
        _items.Add(item);
        OnItemAdded?.Invoke(item);
    }
    
    public bool Remove(T item)
    {
        if (_items.Remove(item))
        {
            OnItemRemoved?.Invoke(item);
            return true;
        }
        return false;
    }
    
    public void Clear()
    {
        _items.Clear();
        OnCleared?.Invoke();
    }
    
    private void OnEnable()
    {
        _items = new List<T>();
    }
}
```

## Event System

### Game Event

```csharp
[CreateAssetMenu(fileName = "GameEvent", menuName = "Events/Game Event")]
public class GameEvent : ScriptableObject
{
    private readonly List<GameEventListener> _listeners = new();
    
    public void Raise()
    {
        // Iterate backwards for safe removal during iteration
        for (int i = _listeners.Count - 1; i >= 0; i--)
        {
            _listeners[i].OnEventRaised();
        }
    }
    
    public void RegisterListener(GameEventListener listener)
    {
        if (!_listeners.Contains(listener))
        {
            _listeners.Add(listener);
        }
    }
    
    public void UnregisterListener(GameEventListener listener)
    {
        _listeners.Remove(listener);
    }
}

public class GameEventListener : MonoBehaviour
{
    [SerializeField] private GameEvent _event;
    [SerializeField] private UnityEvent _response;
    
    private void OnEnable()
    {
        _event?.RegisterListener(this);
    }
    
    private void OnDisable()
    {
        _event?.UnregisterListener(this);
    }
    
    public void OnEventRaised()
    {
        _response?.Invoke();
    }
}
```

### Typed Event

```csharp
public abstract class GameEvent<T> : ScriptableObject
{
    private readonly List<IGameEventListener<T>> _listeners = new();
    
    public void Raise(T value)
    {
        for (int i = _listeners.Count - 1; i >= 0; i--)
        {
            _listeners[i].OnEventRaised(value);
        }
    }
    
    public void RegisterListener(IGameEventListener<T> listener)
    {
        if (!_listeners.Contains(listener))
            _listeners.Add(listener);
    }
    
    public void UnregisterListener(IGameEventListener<T> listener)
    {
        _listeners.Remove(listener);
    }
}

public interface IGameEventListener<T>
{
    void OnEventRaised(T value);
}

[CreateAssetMenu(fileName = "IntEvent", menuName = "Events/Int Event")]
public class IntEvent : GameEvent<int> { }

[CreateAssetMenu(fileName = "StringEvent", menuName = "Events/String Event")]
public class StringEvent : GameEvent<string> { }
```

## Configuration

### Game Settings

```csharp
[CreateAssetMenu(fileName = "GameSettings", menuName = "Config/Game Settings")]
public class GameSettings : ScriptableObject
{
    [Header("Gameplay")]
    public float PlayerMoveSpeed = 5f;
    public float JumpForce = 10f;
    public int MaxHealth = 100;
    
    [Header("Audio")]
    [Range(0, 1)] public float MasterVolume = 1f;
    [Range(0, 1)] public float MusicVolume = 0.8f;
    [Range(0, 1)] public float SfxVolume = 1f;
    
    [Header("Graphics")]
    public QualityPreset DefaultQuality = QualityPreset.Medium;
    public bool VSyncEnabled = true;
    public int TargetFrameRate = 60;
    
    // Singleton access
    private static GameSettings _instance;
    public static GameSettings Instance
    {
        get
        {
            if (_instance == null)
            {
                _instance = Resources.Load<GameSettings>("GameSettings");
            }
            return _instance;
        }
    }
}
```

### Platform-Specific Config

```csharp
[CreateAssetMenu(fileName = "PlatformConfig", menuName = "Config/Platform Config")]
public class PlatformConfig : ScriptableObject
{
    [SerializeField] private PlatformSettings _ios;
    [SerializeField] private PlatformSettings _android;
    [SerializeField] private PlatformSettings _desktop;
    
    public PlatformSettings Current
    {
        get
        {
#if UNITY_IOS
            return _ios;
#elif UNITY_ANDROID
            return _android;
#else
            return _desktop;
#endif
        }
    }
}

[Serializable]
public class PlatformSettings
{
    public int MaxEnemies = 20;
    public int MaxParticles = 100;
    public int TextureQuality = 2;
    public bool EnableShadows = true;
    public float LodBias = 1f;
}
```

## Validation

### Editor Validation

```csharp
public abstract class ValidatedScriptableObject : ScriptableObject
{
#if UNITY_EDITOR
    private void OnValidate()
    {
        Validate();
    }
    
    protected virtual void Validate()
    {
        var errors = GetValidationErrors();
        foreach (var error in errors)
        {
            Debug.LogError($"[{name}] {error}", this);
        }
    }
    
    protected virtual IEnumerable<string> GetValidationErrors()
    {
        yield break;
    }
#endif
}

[CreateAssetMenu(fileName = "NewWeapon", menuName = "Game/Weapon")]
public class WeaponDefinition : ValidatedScriptableObject
{
    public string Id;
    public string DisplayName;
    public int Damage;
    public float AttackSpeed;
    public Sprite Icon;
    
#if UNITY_EDITOR
    protected override IEnumerable<string> GetValidationErrors()
    {
        if (string.IsNullOrEmpty(Id))
            yield return "Id is required";
            
        if (string.IsNullOrEmpty(DisplayName))
            yield return "DisplayName is required";
            
        if (Damage <= 0)
            yield return "Damage must be positive";
            
        if (AttackSpeed <= 0)
            yield return "AttackSpeed must be positive";
            
        if (Icon == null)
            yield return "Icon is required";
    }
#endif
}
```

### ID Uniqueness Check

```csharp
#if UNITY_EDITOR
public static class ScriptableObjectValidator
{
    [UnityEditor.Callbacks.DidReloadScripts]
    private static void ValidateAllItems()
    {
        ValidateUniqueIds<ItemDefinition>("Items");
        ValidateUniqueIds<WeaponDefinition>("Weapons");
    }
    
    private static void ValidateUniqueIds<T>(string folder) where T : ScriptableObject
    {
        var guids = UnityEditor.AssetDatabase.FindAssets($"t:{typeof(T).Name}");
        var idToAsset = new Dictionary<string, string>();
        
        foreach (var guid in guids)
        {
            var path = UnityEditor.AssetDatabase.GUIDToAssetPath(guid);
            var asset = UnityEditor.AssetDatabase.LoadAssetAtPath<T>(path);
            
            var idProperty = typeof(T).GetField("Id");
            if (idProperty == null) continue;
            
            var id = (string)idProperty.GetValue(asset);
            if (string.IsNullOrEmpty(id)) continue;
            
            if (idToAsset.TryGetValue(id, out var existingPath))
            {
                Debug.LogError($"Duplicate ID '{id}' found in:\n{existingPath}\n{path}");
            }
            else
            {
                idToAsset[id] = path;
            }
        }
    }
}
#endif
```

## Best Practices

1. **Use CreateAssetMenu** for easy creation
2. **Initialize runtime state in OnEnable**
3. **Clear runtime state** - SO persists in editor
4. **Use databases** for collections
5. **Validate in editor** with OnValidate
6. **Keep IDs unique** - Validate automatically
7. **Use SerializeField** for private fields
8. **Avoid scene references** in SO
9. **Reset state between plays** in editor
10. **Use Resources.Load sparingly** - Prefer Addressables

## Troubleshooting

| Issue | Solution |
|-------|----------|
| State persists between plays | Reset in OnEnable |
| Null reference to SO | Check asset assignment |
| Duplicate IDs | Add validation check |
| SO not saving changes | Call EditorUtility.SetDirty |
| Large SO slows editor | Split into smaller assets |
| Events not firing | Check listener registration |
