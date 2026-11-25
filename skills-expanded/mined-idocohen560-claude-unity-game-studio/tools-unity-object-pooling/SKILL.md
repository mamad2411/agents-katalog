---
name: tools-unity-object-pooling
description: Object pooling patterns for Unity to reduce GC allocations and improve performance.
---

# Unity Object Pooling

## Overview

Object pooling reuses GameObjects instead of instantiating/destroying them, reducing GC pressure and improving performance.

## When to Use

- Frequently spawned objects (projectiles, particles, enemies)
- UI list items
- Audio sources
- Network messages
- Any high-frequency instantiation

## Basic Object Pool

### Generic Pool Implementation

```csharp
public class ObjectPool<T> where T : class
{
    private readonly Stack<T> _pool = new();
    private readonly Func<T> _createFunc;
    private readonly Action<T> _onGet;
    private readonly Action<T> _onRelease;
    private readonly Action<T> _onDestroy;
    private readonly int _maxSize;
    
    public int CountActive { get; private set; }
    public int CountInactive => _pool.Count;
    public int CountAll => CountActive + CountInactive;
    
    public ObjectPool(
        Func<T> createFunc,
        Action<T> onGet = null,
        Action<T> onRelease = null,
        Action<T> onDestroy = null,
        int defaultCapacity = 10,
        int maxSize = 1000)
    {
        _createFunc = createFunc ?? throw new ArgumentNullException(nameof(createFunc));
        _onGet = onGet;
        _onRelease = onRelease;
        _onDestroy = onDestroy;
        _maxSize = maxSize;
        
        // Pre-warm pool
        for (int i = 0; i < defaultCapacity; i++)
        {
            var obj = _createFunc();
            _onRelease?.Invoke(obj);
            _pool.Push(obj);
        }
    }
    
    public T Get()
    {
        T obj;
        
        if (_pool.Count > 0)
        {
            obj = _pool.Pop();
        }
        else
        {
            obj = _createFunc();
        }
        
        _onGet?.Invoke(obj);
        CountActive++;
        return obj;
    }
    
    public void Release(T obj)
    {
        if (obj == null) return;
        
        _onRelease?.Invoke(obj);
        CountActive--;
        
        if (_pool.Count < _maxSize)
        {
            _pool.Push(obj);
        }
        else
        {
            _onDestroy?.Invoke(obj);
        }
    }
    
    public void Clear()
    {
        while (_pool.Count > 0)
        {
            var obj = _pool.Pop();
            _onDestroy?.Invoke(obj);
        }
        CountActive = 0;
    }
}
```

### Unity Built-in Pool (2021+)

```csharp
using UnityEngine.Pool;

public class ProjectileSpawner : MonoBehaviour
{
    [SerializeField] private Projectile _prefab;
    
    private ObjectPool<Projectile> _pool;
    
    private void Awake()
    {
        _pool = new ObjectPool<Projectile>(
            createFunc: CreateProjectile,
            actionOnGet: OnGetProjectile,
            actionOnRelease: OnReleaseProjectile,
            actionOnDestroy: OnDestroyProjectile,
            collectionCheck: true,
            defaultCapacity: 20,
            maxSize: 100
        );
    }
    
    private Projectile CreateProjectile()
    {
        var proj = Instantiate(_prefab);
        proj.SetPool(_pool);
        return proj;
    }
    
    private void OnGetProjectile(Projectile proj)
    {
        proj.gameObject.SetActive(true);
    }
    
    private void OnReleaseProjectile(Projectile proj)
    {
        proj.gameObject.SetActive(false);
    }
    
    private void OnDestroyProjectile(Projectile proj)
    {
        Destroy(proj.gameObject);
    }
    
    public Projectile Spawn(Vector3 position, Quaternion rotation)
    {
        var proj = _pool.Get();
        proj.transform.SetPositionAndRotation(position, rotation);
        return proj;
    }
}
```

### Pooled Object Base Class

```csharp
public abstract class PooledObject<T> : MonoBehaviour where T : PooledObject<T>
{
    private IObjectPool<T> _pool;
    
    public void SetPool(IObjectPool<T> pool)
    {
        _pool = pool;
    }
    
    public void ReturnToPool()
    {
        if (_pool != null)
        {
            _pool.Release((T)this);
        }
        else
        {
            Destroy(gameObject);
        }
    }
    
    public virtual void OnSpawn() { }
    public virtual void OnDespawn() { }
}

// Usage
public class Projectile : PooledObject<Projectile>
{
    [SerializeField] private float _lifetime = 5f;
    private float _spawnTime;
    
    public override void OnSpawn()
    {
        _spawnTime = Time.time;
    }
    
    public override void OnDespawn()
    {
        // Reset state
    }
    
    private void Update()
    {
        if (Time.time - _spawnTime > _lifetime)
        {
            ReturnToPool();
        }
    }
}
```

## Multi-Prefab Pool

### Pool Manager

```csharp
public class PoolManager : MonoBehaviour
{
    public static PoolManager Instance { get; private set; }
    
    private readonly Dictionary<GameObject, ObjectPool<GameObject>> _pools = new();
    
    private void Awake()
    {
        Instance = this;
    }
    
    public GameObject Spawn(GameObject prefab, Vector3 position, Quaternion rotation)
    {
        if (!_pools.TryGetValue(prefab, out var pool))
        {
            pool = CreatePool(prefab);
            _pools[prefab] = pool;
        }
        
        var obj = pool.Get();
        obj.transform.SetPositionAndRotation(position, rotation);
        return obj;
    }
    
    public void Despawn(GameObject obj, GameObject prefab)
    {
        if (_pools.TryGetValue(prefab, out var pool))
        {
            pool.Release(obj);
        }
        else
        {
            Destroy(obj);
        }
    }
    
    public void PrewarmPool(GameObject prefab, int count)
    {
        if (!_pools.ContainsKey(prefab))
        {
            var pool = CreatePool(prefab, count);
            _pools[prefab] = pool;
        }
    }
    
    private ObjectPool<GameObject> CreatePool(GameObject prefab, int initialSize = 10)
    {
        Transform poolParent = new GameObject($"Pool_{prefab.name}").transform;
        poolParent.SetParent(transform);
        
        return new ObjectPool<GameObject>(
            createFunc: () =>
            {
                var obj = Instantiate(prefab, poolParent);
                obj.SetActive(false);
                return obj;
            },
            actionOnGet: obj => obj.SetActive(true),
            actionOnRelease: obj => obj.SetActive(false),
            actionOnDestroy: obj => Destroy(obj),
            defaultCapacity: initialSize,
            maxSize: 200
        );
    }
}
```

### Pooled Spawn Extension

```csharp
public static class PoolExtensions
{
    public static GameObject SpawnPooled(
        this GameObject prefab, 
        Vector3 position, 
        Quaternion rotation)
    {
        return PoolManager.Instance.Spawn(prefab, position, rotation);
    }
    
    public static void DespawnPooled(this GameObject obj, GameObject prefab)
    {
        PoolManager.Instance.Despawn(obj, prefab);
    }
}

// Usage
var enemy = _enemyPrefab.SpawnPooled(spawnPoint, Quaternion.identity);
// Later...
enemy.DespawnPooled(_enemyPrefab);
```

## Component Pool

### Component-Specific Pool

```csharp
public class ComponentPool<T> where T : Component
{
    private readonly ObjectPool<T> _pool;
    private readonly Transform _parent;
    
    public ComponentPool(T prefab, Transform parent, int initialSize = 10)
    {
        _parent = parent;
        
        _pool = new ObjectPool<T>(
            createFunc: () =>
            {
                var obj = UnityEngine.Object.Instantiate(prefab, parent);
                obj.gameObject.SetActive(false);
                return obj;
            },
            actionOnGet: c => c.gameObject.SetActive(true),
            actionOnRelease: c =>
            {
                c.gameObject.SetActive(false);
                c.transform.SetParent(_parent);
            },
            actionOnDestroy: c => UnityEngine.Object.Destroy(c.gameObject),
            defaultCapacity: initialSize
        );
    }
    
    public T Get() => _pool.Get();
    public void Release(T component) => _pool.Release(component);
}

// Usage for UI
public class DamageNumberPool : MonoBehaviour
{
    [SerializeField] private DamageNumber _prefab;
    
    private ComponentPool<DamageNumber> _pool;
    
    private void Awake()
    {
        _pool = new ComponentPool<DamageNumber>(_prefab, transform, 20);
    }
    
    public DamageNumber Show(Vector3 worldPos, int damage)
    {
        var number = _pool.Get();
        number.Initialize(worldPos, damage, () => _pool.Release(number));
        return number;
    }
}
```

## List/Collection Pooling

### List Pool

```csharp
public static class ListPool<T>
{
    private static readonly ObjectPool<List<T>> s_Pool = new(
        createFunc: () => new List<T>(),
        actionOnRelease: list => list.Clear(),
        defaultCapacity: 10,
        maxSize: 100
    );
    
    public static List<T> Get() => s_Pool.Get();
    
    public static void Release(List<T> list)
    {
        if (list != null)
            s_Pool.Release(list);
    }
    
    // Disposable wrapper
    public static PooledList<T> GetDisposable()
    {
        return new PooledList<T>(s_Pool.Get());
    }
}

public struct PooledList<T> : IDisposable
{
    public List<T> List { get; }
    
    public PooledList(List<T> list)
    {
        List = list;
    }
    
    public void Dispose()
    {
        ListPool<T>.Release(List);
    }
}

// Usage
using (var pooledList = ListPool<Enemy>.GetDisposable())
{
    GetEnemiesInRange(pooledList.List);
    foreach (var enemy in pooledList.List)
    {
        // Process
    }
} // Automatically returned to pool
```

### StringBuilder Pool

```csharp
public static class StringBuilderPool
{
    private static readonly ObjectPool<StringBuilder> s_Pool = new(
        createFunc: () => new StringBuilder(256),
        actionOnRelease: sb => sb.Clear(),
        defaultCapacity: 5,
        maxSize: 50
    );
    
    public static StringBuilder Get() => s_Pool.Get();
    public static void Release(StringBuilder sb) => s_Pool.Release(sb);
    
    public static string GetStringAndRelease(StringBuilder sb)
    {
        string result = sb.ToString();
        Release(sb);
        return result;
    }
}

// Usage
var sb = StringBuilderPool.Get();
sb.Append("Player: ");
sb.Append(playerName);
sb.Append(" Score: ");
sb.Append(score);
string message = StringBuilderPool.GetStringAndRelease(sb);
```

## Audio Pool

### Pooled Audio Source

```csharp
public class AudioPool : MonoBehaviour
{
    [SerializeField] private AudioSource _prefab;
    [SerializeField] private int _poolSize = 20;
    
    private ObjectPool<AudioSource> _pool;
    
    private void Awake()
    {
        _pool = new ObjectPool<AudioSource>(
            createFunc: () =>
            {
                var source = Instantiate(_prefab, transform);
                source.gameObject.SetActive(false);
                return source;
            },
            actionOnGet: source => source.gameObject.SetActive(true),
            actionOnRelease: source =>
            {
                source.Stop();
                source.clip = null;
                source.gameObject.SetActive(false);
            },
            defaultCapacity: _poolSize,
            maxSize: _poolSize * 2
        );
    }
    
    public void PlayOneShot(AudioClip clip, Vector3 position, float volume = 1f)
    {
        var source = _pool.Get();
        source.transform.position = position;
        source.clip = clip;
        source.volume = volume;
        source.Play();
        
        // Return after clip finishes
        StartCoroutine(ReturnAfterPlay(source, clip.length));
    }
    
    private IEnumerator ReturnAfterPlay(AudioSource source, float delay)
    {
        yield return new WaitForSeconds(delay + 0.1f);
        _pool.Release(source);
    }
}
```

## Performance Considerations

### Warm-up Strategy

```csharp
public class PoolWarmer : MonoBehaviour
{
    [SerializeField] private PoolWarmupConfig[] _configs;
    
    private async UniTaskVoid Start()
    {
        await WarmPools();
    }
    
    private async UniTask WarmPools()
    {
        foreach (var config in _configs)
        {
            PoolManager.Instance.PrewarmPool(config.Prefab, config.InitialCount);
            
            // Spread over frames
            if (config.InitialCount > 10)
            {
                await UniTask.Yield();
            }
        }
    }
}

[Serializable]
public class PoolWarmupConfig
{
    public GameObject Prefab;
    public int InitialCount = 10;
}
```

### Pool Statistics

```csharp
public class PoolStats
{
    private readonly Dictionary<string, PoolMetrics> _metrics = new();
    
    public void RecordGet(string poolName)
    {
        GetOrCreate(poolName).Gets++;
    }
    
    public void RecordRelease(string poolName)
    {
        GetOrCreate(poolName).Releases++;
    }
    
    public void RecordCreate(string poolName)
    {
        GetOrCreate(poolName).Creates++;
    }
    
    public void LogStats()
    {
        foreach (var (name, metrics) in _metrics)
        {
            float hitRate = metrics.Gets > 0 
                ? (float)(metrics.Gets - metrics.Creates) / metrics.Gets 
                : 0;
            
            Debug.Log($"Pool {name}: Gets={metrics.Gets}, Creates={metrics.Creates}, HitRate={hitRate:P1}");
        }
    }
    
    private PoolMetrics GetOrCreate(string name)
    {
        if (!_metrics.TryGetValue(name, out var metrics))
        {
            metrics = new PoolMetrics();
            _metrics[name] = metrics;
        }
        return metrics;
    }
    
    private class PoolMetrics
    {
        public int Gets;
        public int Releases;
        public int Creates;
    }
}
```

## Best Practices

1. **Pre-warm pools** during loading screens
2. **Set appropriate max sizes** - Don't pool forever
3. **Reset state** on release, not on get
4. **Use composition** - PooledObject base class
5. **Track pool hit rates** - Optimize sizes
6. **Release in OnDisable** - Handle scene changes
7. **Parent inactive objects** - Organize hierarchy
8. **Use built-in pools** when available (2021+)
9. **Pool expensive components** - Particle systems, audio
10. **Profile allocation reduction** - Verify GC improvement

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Objects not resetting | Implement OnDespawn/Reset |
| Pool growing indefinitely | Set maxSize limit |
| Objects active when spawned | SetActive in create, not get |
| Memory not decreasing | Clear pools on scene change |
| Wrong pool used | Track prefab->pool mapping |
