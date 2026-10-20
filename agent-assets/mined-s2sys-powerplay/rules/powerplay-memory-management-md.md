---
name: memory-management
description: Prevent memory leaks, proper disposal, event handler cleanup, GC tuning
globs: ["**/*.cs"]
alwaysApply: false
---

# Memory Management

Prevent memory leaks through proper disposal patterns, event cleanup, and GC awareness. Every resource should be explicitly released.

## Disposal Pattern

**ALWAYS**:
- Implement IDisposable for objects that own unmanaged resources
- Use `using` statement for all IDisposable objects
- Implement IAsyncDisposable for async resource cleanup
- Call base.Dispose() in derived classes
- Set objects to null after disposing (reference cleanup)

**NEVER**:
- Forget to Dispose() resources
- Implement Dispose without IDisposable interface
- Dispose in destructor/finalizer (too late)
- Ignore finalizer cleanup responsibility

### ✅ GOOD Example
```csharp
// Proper IDisposable pattern
public class DatabaseConnection : IDisposable
{
  private bool _disposed;
  private SqlConnection _connection;
  
  public void Connect(string connectionString)
  {
    _connection = new SqlConnection(connectionString);
    _connection.Open();
  }
  
  public void Dispose()
  {
    Dispose(true);
    GC.SuppressFinalize(this);
  }
  
  protected virtual void Dispose(bool disposing)
  {
    if (_disposed) return;
    
    if (disposing)
    {
      _connection?.Dispose();
    }
    
    _disposed = true;
  }
  
  ~DatabaseConnection()
  {
    Dispose(false);
  }
}

// Usage with using statement (automatic Dispose on exit)
using (var db = new DatabaseConnection())
{
  db.Connect("Server=...");
  // Use db
} // Dispose called automatically
```

### ❌ BAD Example
```csharp
// Memory leak: no Dispose, no using
public class DataProcessor
{
  private SqlConnection _connection; // Never disposed!
  
  public void ProcessData()
  {
    _connection = new SqlConnection("Server=...");
    _connection.Open();
    // If exception occurs, connection never closes
  }
}

// Leak in method
public void BadMethod()
{
  var stream = new FileStream("file.txt", FileMode.Open);
  var reader = new StreamReader(stream); // Reader not disposed either
  // If exception occurs, handles leak
}
```

---

## Event Handler Cleanup

**ALWAYS**:
- Unsubscribe from events in Dispose or Destructor
- Use weak event pattern for long-lived publishers
- Store event handler reference if you need to unsubscribe
- Unsubscribe before disposing subscriber

**NEVER**:
- Subscribe in constructor, unsubscribe in Dispose (asymmetry)
- Forget to unsubscribe from static events (memory leak)
- Use anonymous lambdas for events (can't unsubscribe)

### ✅ GOOD Example
```csharp
public class OrderProcessor : IDisposable
{
  private readonly OrderService _service;
  private EventHandler<OrderEventArgs> _onOrderCreated;
  
  public OrderProcessor(OrderService service)
  {
    _service = service;
    
    // Store handler reference for unsubscribe
    _onOrderCreated = OnOrderCreated;
    _service.OrderCreated += _onOrderCreated;
  }
  
  private void OnOrderCreated(object sender, OrderEventArgs e)
  {
    // Handle event
  }
  
  public void Dispose()
  {
    // Explicit unsubscribe
    _service.OrderCreated -= _onOrderCreated;
    _service?.Dispose();
  }
}
```

### ❌ BAD Example
```csharp
public class OrderProcessor : IDisposable
{
  public OrderProcessor(OrderService service)
  {
    // Anonymous lambda - can't unsubscribe!
    service.OrderCreated += (sender, e) => { /* handle */ };
  }
  
  public void Dispose()
  {
    // No way to unsubscribe - memory leak
  }
}

// Static event leak
public static class GlobalService
{
  public static event EventHandler OnProcessing;
}

public class Worker
{
  public Worker()
  {
    GlobalService.OnProcessing += (s, e) => { /* handle */ };
  }
  
  // Even if disposed, handler stays in memory (static event)
}
```

---

## Circular References & Caching

**ALWAYS**:
- Break circular references explicitly
- Use WeakReference for caches of large objects
- Clear caches on disposal
- Parent → Child (strong), Child → Parent (weak)

**NEVER**:
- Parent and Child hold strong references to each other
- Cache objects indefinitely without eviction
- Keep strong references to subscribers after unsubscribe

### ✅ GOOD Example
```csharp
// Weak reference for cache
public class ObjectCache
{
  private Dictionary<string, WeakReference> _cache = new();
  
  public void Add(string key, object value)
  {
    _cache[key] = new WeakReference(value);
  }
  
  public object Get(string key)
  {
    if (_cache.TryGetValue(key, out var weakRef) && weakRef.IsAlive)
    {
      return weakRef.Target;
    }
    _cache.Remove(key);
    return null;
  }
}

// Parent-Child relationship
public class Parent
{
  private Child _child = new(); // Strong reference
  
  public void Dispose()
  {
    _child?.Dispose();
  }
}

public class Child
{
  private WeakReference _parent; // Weak reference to parent
  
  public Child() { }
}
```

### ❌ BAD Example
```csharp
// Circular reference memory leak
public class Parent
{
  private Child _child = new() { Parent = this }; // Circular!
}

public class Child
{
  public Parent Parent { get; set; } // Strong back-reference
}

// Bad cache
public class Cache
{
  private Dictionary<string, object> _cache = new();
  
  public void Add(string key, object value)
  {
    _cache[key] = value; // Cached forever, never collected
  }
}
```

---

## Async Disposal

**ALWAYS**:
- Implement IAsyncDisposable for async cleanup
- Use `await using` for async disposable objects
- In Dispose(), wait for async cleanup to complete synchronously if needed

**NEVER**:
- Call async Dispose from synchronous Dispose without waiting
- Forget DisposeAsync in async cleanup scenarios
- Mix sync and async disposal improperly

### ✅ GOOD Example
```csharp
public class AsyncResource : IAsyncDisposable
{
  private SqlConnection _connection;
  
  public async Task InitializeAsync()
  {
    _connection = new SqlConnection("...");
    await _connection.OpenAsync();
  }
  
  public async ValueTask DisposeAsync()
  {
    if (_connection != null)
    {
      await _connection.CloseAsync(); // Async cleanup
      _connection.Dispose();
    }
  }
}

// Usage with await using
await using var resource = new AsyncResource();
await resource.InitializeAsync();
// DisposeAsync called automatically
```

---

## Large Objects & Allocations

**ALWAYS**:
- Monitor large object heap (LOH) allocations > 85KB
- Rent arrays from ArrayPool instead of allocating
- Return rented arrays when done

**NEVER**:
- Allocate huge arrays in loops
- Ignore Gen 2 collections (expensive)
- Allocate in tight loops without pooling

### ✅ GOOD Example
```csharp
// Use ArrayPool to avoid allocations
public byte[] ProcessData(byte[] input)
{
  var buffer = ArrayPool<byte>.Shared.Rent(input.Length);
  try
  {
    Array.Copy(input, buffer, input.Length);
    // Process buffer
    return buffer.Take(input.Length).ToArray(); // Return clean copy
  }
  finally
  {
    ArrayPool<byte>.Shared.Return(buffer);
  }
}
```

---

## Memory Checklist

- [ ] IDisposable implemented for resources
- [ ] using statements for all IDisposable objects
- [ ] await using for IAsyncDisposable objects
- [ ] Event handlers stored for unsubscribe
- [ ] No circular references (use weak references)
- [ ] No static event handler memory leaks
- [ ] Caches have eviction policy
- [ ] Large objects (> 85KB) carefully managed
- [ ] ArrayPool used instead of allocating buffers
- [ ] GC.Collect() not called except for diagnostics
- [ ] No disposable objects in finalizers
