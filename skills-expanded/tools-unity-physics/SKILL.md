---
name: tools-unity-physics
description: Unity physics patterns including character controllers, collision handling, and tunneling prevention.
---

# Unity Physics

## Overview

Unity physics handles collision detection, rigidbody simulation, and character movement. This skill covers patterns to prevent common issues like floor penetration.

## When to Use

- Character movement and controllers
- Projectile physics
- Collision detection
- Trigger zones
- Ragdoll systems

## Character Controller Safety

### Preventing Floor Penetration

```csharp
public class SafeCharacterController : MonoBehaviour
{
    [SerializeField] private float _moveSpeed = 5f;
    [SerializeField] private float _gravity = -20f;
    [SerializeField] private float _groundCheckDistance = 0.1f;
    [SerializeField] private LayerMask _groundLayer;
    
    private CharacterController _controller;
    private Vector3 _velocity;
    private bool _isGrounded;
    
    private void Awake()
    {
        _controller = GetComponent<CharacterController>();
    }
    
    private void Update()
    {
        // Ground check with spherecast for reliability
        _isGrounded = Physics.SphereCast(
            transform.position + Vector3.up * (_controller.radius + 0.1f),
            _controller.radius * 0.9f,
            Vector3.down,
            out _,
            _groundCheckDistance + 0.1f,
            _groundLayer
        );
        
        if (_isGrounded && _velocity.y < 0)
        {
            // Small negative to keep grounded
            _velocity.y = -2f;
        }
        
        // Movement
        Vector3 move = GetMoveInput() * _moveSpeed;
        _controller.Move(move * Time.deltaTime);
        
        // Gravity
        _velocity.y += _gravity * Time.deltaTime;
        _controller.Move(_velocity * Time.deltaTime);
        
        // CRITICAL: Clamp to ground if penetrating
        ClampToGround();
    }
    
    private void ClampToGround()
    {
        if (Physics.Raycast(transform.position + Vector3.up, Vector3.down, out var hit, 2f, _groundLayer))
        {
            if (transform.position.y < hit.point.y)
            {
                transform.position = new Vector3(
                    transform.position.x,
                    hit.point.y,
                    transform.position.z
                );
            }
        }
    }
    
    private Vector3 GetMoveInput()
    {
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");
        return new Vector3(h, 0, v).normalized;
    }
}
```

### Physics-Based Character Movement

```csharp
public class PhysicsCharacterController : MonoBehaviour
{
    [SerializeField] private float _moveSpeed = 5f;
    [SerializeField] private float _jumpForce = 8f;
    [SerializeField] private float _groundDrag = 6f;
    [SerializeField] private float _airDrag = 1f;
    [SerializeField] private LayerMask _groundLayer;
    
    private Rigidbody _rb;
    private CapsuleCollider _collider;
    private bool _isGrounded;
    
    private void Awake()
    {
        _rb = GetComponent<Rigidbody>();
        _collider = GetComponent<CapsuleCollider>();
        
        // Prevent tunneling
        _rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
        _rb.interpolation = RigidbodyInterpolation.Interpolate;
    }
    
    private void FixedUpdate()
    {
        CheckGrounded();
        ApplyDrag();
        Move();
    }
    
    private void CheckGrounded()
    {
        _isGrounded = Physics.SphereCast(
            transform.position + Vector3.up * (_collider.radius + 0.1f),
            _collider.radius * 0.95f,
            Vector3.down,
            out _,
            0.2f,
            _groundLayer
        );
    }
    
    private void ApplyDrag()
    {
        _rb.linearDamping = _isGrounded ? _groundDrag : _airDrag;
    }
    
    private void Move()
    {
        Vector3 moveDir = GetMoveInput();
        
        if (_isGrounded)
        {
            _rb.AddForce(moveDir * _moveSpeed * 10f, ForceMode.Force);
        }
        else
        {
            _rb.AddForce(moveDir * _moveSpeed * 5f, ForceMode.Force);
        }
        
        // Clamp horizontal velocity
        Vector3 flatVel = new Vector3(_rb.linearVelocity.x, 0, _rb.linearVelocity.z);
        if (flatVel.magnitude > _moveSpeed)
        {
            Vector3 limitedVel = flatVel.normalized * _moveSpeed;
            _rb.linearVelocity = new Vector3(limitedVel.x, _rb.linearVelocity.y, limitedVel.z);
        }
    }
}
```

## Collision Detection

### Safe Collision Handling

```csharp
public class CollisionHandler : MonoBehaviour
{
    public event Action<Collision> OnCollisionEnterSafe;
    public event Action<Collider> OnTriggerEnterSafe;
    
    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject == null) return;
        if (collision.contactCount == 0) return;
        
        OnCollisionEnterSafe?.Invoke(collision);
    }
    
    private void OnTriggerEnter(Collider other)
    {
        if (other == null) return;
        if (!other.gameObject.activeInHierarchy) return;
        
        OnTriggerEnterSafe?.Invoke(other);
    }
}
```

### Layer-Based Collision

```csharp
public class CollisionLayerManager
{
    // Define layers
    public const int PlayerLayer = 8;
    public const int EnemyLayer = 9;
    public const int ProjectileLayer = 10;
    public const int EnvironmentLayer = 11;
    
    public static void Initialize()
    {
        // Player ignores other players
        Physics.IgnoreLayerCollision(PlayerLayer, PlayerLayer, true);
        
        // Projectiles pass through each other
        Physics.IgnoreLayerCollision(ProjectileLayer, ProjectileLayer, true);
        
        // Enemy projectiles don't hit enemies
        // (Configure in project settings)
    }
    
    public static LayerMask GetPlayerHitLayers()
    {
        return (1 << EnemyLayer) | (1 << EnvironmentLayer);
    }
    
    public static LayerMask GetEnemyHitLayers()
    {
        return (1 << PlayerLayer) | (1 << EnvironmentLayer);
    }
}
```

## Preventing Tunneling

### Continuous Collision Detection

```csharp
public class ProjectilePhysics : MonoBehaviour
{
    [SerializeField] private float _speed = 50f;
    [SerializeField] private LayerMask _hitLayers;
    
    private Rigidbody _rb;
    private Vector3 _lastPosition;
    
    private void Awake()
    {
        _rb = GetComponent<Rigidbody>();
        
        // Use continuous for fast objects
        _rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
        _rb.interpolation = RigidbodyInterpolation.Interpolate;
    }
    
    private void Start()
    {
        _rb.linearVelocity = transform.forward * _speed;
        _lastPosition = transform.position;
    }
    
    private void FixedUpdate()
    {
        // Manual raycast for very fast projectiles
        var direction = transform.position - _lastPosition;
        var distance = direction.magnitude;
        
        if (distance > 0.01f)
        {
            if (Physics.Raycast(_lastPosition, direction.normalized, out var hit, distance, _hitLayers))
            {
                OnHit(hit);
            }
        }
        
        _lastPosition = transform.position;
    }
    
    private void OnHit(RaycastHit hit)
    {
        // Handle impact
        Destroy(gameObject);
    }
}
```

### SubStepping for Fast Movement

```csharp
public class HighSpeedMovement : MonoBehaviour
{
    [SerializeField] private float _speed = 100f;
    [SerializeField] private LayerMask _collisionLayers;
    
    private const float MaxStepDistance = 0.5f;
    
    public void MoveTowards(Vector3 target)
    {
        Vector3 direction = (target - transform.position).normalized;
        float totalDistance = Vector3.Distance(transform.position, target);
        float distanceMoved = 0f;
        
        while (distanceMoved < totalDistance)
        {
            float stepDistance = Mathf.Min(MaxStepDistance, totalDistance - distanceMoved);
            Vector3 nextPosition = transform.position + direction * stepDistance;
            
            // Check for collision in this step
            if (Physics.Raycast(transform.position, direction, out var hit, stepDistance, _collisionLayers))
            {
                transform.position = hit.point - direction * 0.01f;
                OnCollision(hit);
                return;
            }
            
            transform.position = nextPosition;
            distanceMoved += stepDistance;
        }
    }
    
    private void OnCollision(RaycastHit hit)
    {
        // Handle collision
    }
}
```

## Physics Queries

### SphereCast for Ground Detection

```csharp
public class GroundChecker
{
    private readonly float _radius;
    private readonly float _distance;
    private readonly LayerMask _groundMask;
    
    public GroundChecker(float radius, float distance, LayerMask groundMask)
    {
        _radius = radius;
        _distance = distance;
        _groundMask = groundMask;
    }
    
    public bool IsGrounded(Vector3 position, out RaycastHit hitInfo)
    {
        Vector3 origin = position + Vector3.up * (_radius + 0.05f);
        
        return Physics.SphereCast(
            origin,
            _radius * 0.9f,
            Vector3.down,
            out hitInfo,
            _distance + 0.1f,
            _groundMask,
            QueryTriggerInteraction.Ignore
        );
    }
    
    public float GetGroundAngle(RaycastHit hit)
    {
        return Vector3.Angle(hit.normal, Vector3.up);
    }
}
```

### OverlapSphere with Filtering

```csharp
public class AreaDetector
{
    private readonly Collider[] _results = new Collider[32];
    
    public int DetectInRadius<T>(
        Vector3 center, 
        float radius, 
        LayerMask layers, 
        List<T> output) where T : Component
    {
        output.Clear();
        
        int count = Physics.OverlapSphereNonAlloc(
            center, 
            radius, 
            _results, 
            layers, 
            QueryTriggerInteraction.Ignore
        );
        
        for (int i = 0; i < count; i++)
        {
            if (_results[i].TryGetComponent<T>(out var component))
            {
                output.Add(component);
            }
        }
        
        return output.Count;
    }
}
```

## Physics Performance

### Optimized Physics Settings

```csharp
public class PhysicsOptimizer
{
    public static void ApplyMobileSettings()
    {
        // Reduce solver iterations for mobile
        Physics.defaultSolverIterations = 4;
        Physics.defaultSolverVelocityIterations = 1;
        
        // Increase sleep threshold
        Physics.sleepThreshold = 0.05f;
        
        // Reduce bounce threshold
        Physics.bounceThreshold = 2f;
        
        // Lower fixed timestep for mobile (45 Hz instead of 50)
        Time.fixedDeltaTime = 1f / 45f;
    }
    
    public static void ApplyDesktopSettings()
    {
        Physics.defaultSolverIterations = 6;
        Physics.defaultSolverVelocityIterations = 1;
        Physics.sleepThreshold = 0.01f;
        Time.fixedDeltaTime = 1f / 60f;
    }
}
```

### Physics Job System

```csharp
using Unity.Jobs;
using Unity.Collections;
using Unity.Burst;

[BurstCompile]
public struct RaycastJob : IJobParallelFor
{
    [ReadOnly] public NativeArray<RaycastCommand> Commands;
    public NativeArray<RaycastHit> Results;
    
    public void Execute(int index)
    {
        // Results are written by Unity's job system
    }
}

public class BatchRaycaster
{
    public void PerformBatchRaycasts(
        Vector3[] origins, 
        Vector3[] directions, 
        float[] distances,
        LayerMask layerMask,
        RaycastHit[] results)
    {
        int count = origins.Length;
        
        var commands = new NativeArray<RaycastCommand>(count, Allocator.TempJob);
        var hits = new NativeArray<RaycastHit>(count, Allocator.TempJob);
        
        for (int i = 0; i < count; i++)
        {
            commands[i] = new RaycastCommand(
                origins[i],
                directions[i],
                QueryParameters.Default,
                distances[i]
            );
        }
        
        var handle = RaycastCommand.ScheduleBatch(commands, hits, 1);
        handle.Complete();
        
        hits.CopyTo(results);
        
        commands.Dispose();
        hits.Dispose();
    }
}
```

## Best Practices

1. **Use ContinuousDynamic** for fast-moving objects
2. **SphereCast for ground** - More reliable than raycast
3. **Clamp positions** after physics update
4. **Use NonAlloc methods** for queries (OverlapSphereNonAlloc)
5. **Configure layer matrix** - Avoid unnecessary collisions
6. **Sleep inactive rigidbodies** - Set appropriate thresholds
7. **Profile FixedUpdate** - Physics runs at fixed rate
8. **Use compound colliders** sparingly
9. **Batch physics queries** with job system
10. **Test at low framerates** - Tunneling is worse

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Objects fall through floor | Use ContinuousDynamic, clamp position |
| Jittery movement | Enable Interpolation |
| Collision missed | Increase solver iterations |
| Physics too slow | Reduce collider complexity |
| Character stuck | Check collider radius vs step offset |
| Floating point drift | Reset position periodically |
