---
name: tools-unity-navmesh
description: Unity NavMesh pathfinding patterns, safety checks, and performance optimization.
---

# Unity NavMesh Pathfinding

## Overview

NavMesh provides AI pathfinding in Unity. This skill covers safe usage patterns to prevent the 30K+ pathfinding errors seen in production.

## When to Use

- AI movement and navigation
- Enemy patrolling and chasing
- NPC pathfinding
- Dynamic obstacle avoidance
- Multi-agent navigation

## Critical Safety Patterns

### Graph Validation Before Query

```csharp
using Pathfinding;

public class SafePathfinder
{
    private readonly Seeker _seeker;
    
    public bool TryCalculatePath(Vector3 start, Vector3 end, out Path path)
    {
        path = null;
        
        // CRITICAL: Check graph exists
        if (AstarPath.active == null)
        {
            Debug.LogError("No AstarPath instance active");
            return false;
        }
        
        if (AstarPath.active.graphs == null || AstarPath.active.graphs.Length == 0)
        {
            Debug.LogError("No graphs available");
            return false;
        }
        
        // Check if position is on navmesh
        var startNode = AstarPath.active.GetNearest(start).node;
        var endNode = AstarPath.active.GetNearest(end).node;
        
        if (startNode == null || !startNode.Walkable)
        {
            Debug.LogWarning($"Start position {start} not on walkable navmesh");
            return false;
        }
        
        if (endNode == null || !endNode.Walkable)
        {
            Debug.LogWarning($"End position {end} not on walkable navmesh");
            return false;
        }
        
        // Safe to calculate path
        _seeker.StartPath(start, end, OnPathComplete);
        return true;
    }
    
    private void OnPathComplete(Path p)
    {
        if (p.error)
        {
            Debug.LogWarning($"Path failed: {p.errorLog}");
            return;
        }
        
        // Use path
    }
}
```

### Null Graph Guard (Critical Fix for 30K errors)

```csharp
public class PathfindingGuard
{
    public static bool IsPathfindingReady()
    {
        // Check 1: AstarPath singleton exists
        if (AstarPath.active == null)
            return false;
        
        // Check 2: Data is loaded
        if (AstarPath.active.data == null)
            return false;
        
        // Check 3: Graphs exist
        if (AstarPath.active.data.graphs == null)
            return false;
        
        // Check 4: At least one graph is scanned
        foreach (var graph in AstarPath.active.data.graphs)
        {
            if (graph != null && graph.CountNodes() > 0)
                return true;
        }
        
        return false;
    }
}

// Usage in AI
public class EnemyAI : MonoBehaviour
{
    private void RequestPath()
    {
        if (!PathfindingGuard.IsPathfindingReady())
        {
            // Defer pathfinding or use fallback behavior
            StartCoroutine(WaitForPathfinding());
            return;
        }
        
        _seeker.StartPath(transform.position, _target.position);
    }
    
    private IEnumerator WaitForPathfinding()
    {
        while (!PathfindingGuard.IsPathfindingReady())
        {
            yield return new WaitForSeconds(0.5f);
        }
        
        RequestPath();
    }
}
```

### NavMeshAgent Wrapper

```csharp
public class SafeNavMeshAgent : MonoBehaviour
{
    private NavMeshAgent _agent;
    private bool _isNavigating;
    
    private void Awake()
    {
        _agent = GetComponent<NavMeshAgent>();
    }
    
    public bool TrySetDestination(Vector3 destination)
    {
        if (_agent == null || !_agent.isOnNavMesh)
        {
            Debug.LogWarning($"{name} not on NavMesh");
            return false;
        }
        
        // Check if destination is reachable
        NavMeshPath path = new NavMeshPath();
        if (!_agent.CalculatePath(destination, path))
        {
            Debug.LogWarning($"Cannot calculate path to {destination}");
            return false;
        }
        
        if (path.status != NavMeshPathStatus.PathComplete)
        {
            Debug.LogWarning($"Path incomplete: {path.status}");
            return false;
        }
        
        _agent.SetPath(path);
        _isNavigating = true;
        return true;
    }
    
    public void Stop()
    {
        if (_agent != null && _agent.isOnNavMesh)
        {
            _agent.isStopped = true;
            _agent.ResetPath();
        }
        _isNavigating = false;
    }
    
    private void OnDisable()
    {
        Stop();
    }
}
```

## A* Pathfinding Project Patterns

### Seeker Configuration

```csharp
public class AIPathfinder : MonoBehaviour
{
    private Seeker _seeker;
    private AIPath _aiPath;
    
    private void Awake()
    {
        _seeker = GetComponent<Seeker>();
        _aiPath = GetComponent<AIPath>();
        
        // Configure seeker
        _seeker.pathCallback += OnPathComplete;
        
        // Set traversable tags
        _seeker.traversableTags = ~0; // All tags
    }
    
    private void OnDestroy()
    {
        if (_seeker != null)
        {
            _seeker.pathCallback -= OnPathComplete;
            _seeker.CancelCurrentPathRequest();
        }
    }
    
    public void MoveTo(Vector3 destination)
    {
        if (!PathfindingGuard.IsPathfindingReady())
        {
            Debug.LogWarning("Pathfinding not ready");
            return;
        }
        
        _aiPath.destination = destination;
        _aiPath.SearchPath();
    }
    
    private void OnPathComplete(Path p)
    {
        if (p.error)
        {
            HandlePathError(p);
            return;
        }
        
        // Path ready
    }
    
    private void HandlePathError(Path p)
    {
        Debug.LogWarning($"Path error: {p.errorLog}");
        
        // Fallback behavior - move directly or stay
    }
}
```

### Path Caching

```csharp
public class PathCache
{
    private readonly Dictionary<(Vector3Int, Vector3Int), Path> _cache = new();
    private readonly float _cacheValidTime = 5f;
    private readonly Dictionary<(Vector3Int, Vector3Int), float> _cacheTimestamps = new();
    
    private const float GridSize = 1f;
    
    public bool TryGetCachedPath(Vector3 start, Vector3 end, out Path path)
    {
        var key = (ToGridPos(start), ToGridPos(end));
        
        if (_cache.TryGetValue(key, out path))
        {
            if (_cacheTimestamps.TryGetValue(key, out var timestamp))
            {
                if (Time.time - timestamp < _cacheValidTime)
                {
                    return true;
                }
            }
            
            // Cache expired
            _cache.Remove(key);
            _cacheTimestamps.Remove(key);
        }
        
        path = null;
        return false;
    }
    
    public void CachePath(Vector3 start, Vector3 end, Path path)
    {
        var key = (ToGridPos(start), ToGridPos(end));
        _cache[key] = path;
        _cacheTimestamps[key] = Time.time;
    }
    
    private Vector3Int ToGridPos(Vector3 pos)
    {
        return new Vector3Int(
            Mathf.RoundToInt(pos.x / GridSize),
            Mathf.RoundToInt(pos.y / GridSize),
            Mathf.RoundToInt(pos.z / GridSize)
        );
    }
}
```

## Performance Optimization

### Batch Path Requests

```csharp
public class PathBatcher
{
    private readonly Queue<PathRequest> _pendingRequests = new();
    private readonly int _maxRequestsPerFrame = 3;
    private bool _isProcessing;
    
    public void RequestPath(Vector3 start, Vector3 end, Action<Path> callback)
    {
        _pendingRequests.Enqueue(new PathRequest(start, end, callback));
        
        if (!_isProcessing)
        {
            ProcessBatch().Forget();
        }
    }
    
    private async UniTaskVoid ProcessBatch()
    {
        _isProcessing = true;
        
        while (_pendingRequests.Count > 0)
        {
            var processedThisFrame = 0;
            
            while (_pendingRequests.Count > 0 && processedThisFrame < _maxRequestsPerFrame)
            {
                var request = _pendingRequests.Dequeue();
                var path = await CalculatePathAsync(request.Start, request.End);
                request.Callback?.Invoke(path);
                processedThisFrame++;
            }
            
            await UniTask.Yield();
        }
        
        _isProcessing = false;
    }
    
    private async UniTask<Path> CalculatePathAsync(Vector3 start, Vector3 end)
    {
        var tcs = new UniTaskCompletionSource<Path>();
        
        var seeker = AstarPath.active.GetComponent<Seeker>();
        seeker.StartPath(start, end, p => tcs.TrySetResult(p));
        
        return await tcs.Task;
    }
    
    private readonly struct PathRequest
    {
        public readonly Vector3 Start;
        public readonly Vector3 End;
        public readonly Action<Path> Callback;
        
        public PathRequest(Vector3 start, Vector3 end, Action<Path> callback)
        {
            Start = start;
            End = end;
            Callback = callback;
        }
    }
}
```

### LOD-Based Pathfinding

```csharp
public class LODPathfinder
{
    private readonly float _preciseRadius = 20f;
    private readonly float _mediumRadius = 50f;
    
    public void RequestPath(Vector3 agent, Vector3 target)
    {
        var distance = Vector3.Distance(agent, target);
        
        if (distance <= _preciseRadius)
        {
            // Use full detail graph
            RequestPrecisePath(agent, target);
        }
        else if (distance <= _mediumRadius)
        {
            // Use simplified graph
            RequestMediumPath(agent, target);
        }
        else
        {
            // Use waypoint system
            RequestWaypointPath(agent, target);
        }
    }
}
```

## Dynamic Obstacles

### NavMesh Obstacle Handling

```csharp
public class DynamicObstacle : MonoBehaviour
{
    private NavMeshObstacle _obstacle;
    private Coroutine _carveDelayCoroutine;
    
    private void Awake()
    {
        _obstacle = GetComponent<NavMeshObstacle>();
        _obstacle.carving = true;
        _obstacle.carveOnlyStationary = true;
    }
    
    public void EnableCarving()
    {
        if (_carveDelayCoroutine != null)
        {
            StopCoroutine(_carveDelayCoroutine);
        }
        
        // Delay carving to prevent rapid updates
        _carveDelayCoroutine = StartCoroutine(DelayedCarveEnable());
    }
    
    private IEnumerator DelayedCarveEnable()
    {
        yield return new WaitForSeconds(0.5f);
        _obstacle.carving = true;
    }
    
    public void DisableCarving()
    {
        if (_carveDelayCoroutine != null)
        {
            StopCoroutine(_carveDelayCoroutine);
        }
        _obstacle.carving = false;
    }
}
```

### Graph Updates

```csharp
public class NavMeshUpdater
{
    public void UpdateArea(Bounds bounds)
    {
        if (AstarPath.active == null) return;
        
        var graphUpdateObject = new GraphUpdateObject(bounds)
        {
            updatePhysics = true,
            modifyWalkability = true
        };
        
        AstarPath.active.UpdateGraphs(graphUpdateObject);
    }
    
    public void UpdateAreaAsync(Bounds bounds, Action onComplete)
    {
        if (AstarPath.active == null)
        {
            onComplete?.Invoke();
            return;
        }
        
        var graphUpdateObject = new GraphUpdateObject(bounds)
        {
            updatePhysics = true
        };
        
        AstarPath.active.UpdateGraphs(graphUpdateObject, onComplete);
    }
}
```

## Error Recovery

### Stuck Detection

```csharp
public class StuckDetector : MonoBehaviour
{
    private Vector3 _lastPosition;
    private float _stuckTime;
    private const float StuckThreshold = 0.1f;
    private const float StuckTimeout = 3f;
    
    public event Action OnStuck;
    
    private void Update()
    {
        var moved = Vector3.Distance(transform.position, _lastPosition);
        
        if (moved < StuckThreshold)
        {
            _stuckTime += Time.deltaTime;
            
            if (_stuckTime >= StuckTimeout)
            {
                OnStuck?.Invoke();
                _stuckTime = 0f;
            }
        }
        else
        {
            _stuckTime = 0f;
        }
        
        _lastPosition = transform.position;
    }
}
```

### Position Recovery

```csharp
public class NavMeshRecovery
{
    public bool TryRecoverPosition(Transform agent, float searchRadius = 10f)
    {
        // Sample nearest valid position
        if (NavMesh.SamplePosition(agent.position, out var hit, searchRadius, NavMesh.AllAreas))
        {
            agent.position = hit.position;
            return true;
        }
        
        // Try expanding search
        for (float radius = searchRadius; radius <= 50f; radius += 10f)
        {
            if (NavMesh.SamplePosition(agent.position, out hit, radius, NavMesh.AllAreas))
            {
                agent.position = hit.position;
                return true;
            }
        }
        
        return false;
    }
}
```

## Best Practices

1. **Always check graph validity** before pathfinding
2. **Use path callbacks** - Don't block on path calculation
3. **Batch path requests** - Limit per-frame calculations
4. **Cache paths** for repeated queries
5. **Handle path failures** gracefully
6. **Use NavMesh.SamplePosition** for validation
7. **Update graphs async** for dynamic obstacles
8. **Implement stuck detection** with recovery
9. **Cancel paths on disable/destroy**
10. **Profile pathfinding cost** on target devices

## Troubleshooting

| Issue | Solution |
|-------|----------|
| NullReferenceException in pathfinding | Add graph null checks |
| Agent not moving | Check isOnNavMesh |
| Path incomplete | Verify destination reachable |
| Slow pathfinding | Batch requests, cache paths |
| Agent stuck | Implement stuck detection + recovery |
| Dynamic obstacles ignored | Enable carving, update graphs |
