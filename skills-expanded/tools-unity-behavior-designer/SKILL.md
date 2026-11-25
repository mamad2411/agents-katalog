---
name: tools-unity-behavior-designer
description: Behavior Designer patterns for AI behavior trees including task creation, shared variables, conditionals, and debugging.
---

# Behavior Designer

## Overview

Behavior Designer is a behavior tree implementation for Unity AI. This skill covers patterns for creating robust AI behaviors for enemies, NPCs, and game entities.

## When to Use

- Enemy AI behavior
- NPC decision making
- Boss fight patterns
- Companion AI
- Any complex state-based AI

## Core Concepts

### Behavior Tree Structure

```
Selector (OR logic - first success wins)
├── Sequence (AND logic - all must succeed)
│   ├── Conditional (check condition)
│   └── Action (do something)
├── Sequence
│   ├── Conditional
│   └── Action
└── Action (fallback)
```

## Custom Tasks

### Action Task

```csharp
using BehaviorDesigner.Runtime;
using BehaviorDesigner.Runtime.Tasks;

[TaskCategory("Combat")]
[TaskDescription("Attacks the current target")]
public class AttackTarget : Action
{
    [Tooltip("Reference to the ability system")]
    public SharedGameObject abilitySystemOwner;
    
    [Tooltip("The ability to activate")]
    public SharedString abilityTag;
    
    [Tooltip("Target to attack")]
    public SharedGameObject target;
    
    private IAbilitySystem _abilitySystem;
    private bool _abilityStarted;
    
    public override void OnStart()
    {
        _abilityStarted = false;
        
        if (abilitySystemOwner.Value == null)
        {
            Debug.LogError("AttackTarget: No ability system owner");
            return;
        }
        
        _abilitySystem = abilitySystemOwner.Value.GetComponent<IAbilitySystem>();
    }
    
    public override TaskStatus OnUpdate()
    {
        if (_abilitySystem == null || target.Value == null)
        {
            return TaskStatus.Failure;
        }
        
        if (!_abilityStarted)
        {
            if (!_abilitySystem.TryActivateAbilityByTag(abilityTag.Value))
            {
                return TaskStatus.Failure;
            }
            _abilityStarted = true;
        }
        
        // Check if ability is still running
        if (_abilitySystem.IsAbilityActive(abilityTag.Value))
        {
            return TaskStatus.Running;
        }
        
        return TaskStatus.Success;
    }
    
    public override void OnEnd()
    {
        // Cleanup if interrupted
        if (_abilityStarted && _abilitySystem != null)
        {
            _abilitySystem.CancelAbilityByTag(abilityTag.Value);
        }
    }
}
```

### Conditional Task

```csharp
[TaskCategory("Combat")]
[TaskDescription("Checks if target is within attack range")]
public class IsTargetInRange : Conditional
{
    public SharedGameObject target;
    public SharedFloat attackRange;
    public SharedTransform selfTransform;
    
    public override TaskStatus OnUpdate()
    {
        if (target.Value == null || selfTransform.Value == null)
        {
            return TaskStatus.Failure;
        }
        
        float distance = Vector3.Distance(
            selfTransform.Value.position,
            target.Value.transform.position
        );
        
        return distance <= attackRange.Value 
            ? TaskStatus.Success 
            : TaskStatus.Failure;
    }
}
```

### Composite Task (Custom Selector)

```csharp
[TaskCategory("Custom")]
[TaskDescription("Weighted random selection of children")]
public class WeightedSelector : Composite
{
    [Tooltip("Weights for each child (must match child count)")]
    public float[] weights;
    
    private int _currentChildIndex = -1;
    private int _executedChildIndex = -1;
    
    public override void OnStart()
    {
        _currentChildIndex = SelectWeightedChild();
        _executedChildIndex = -1;
    }
    
    public override int CurrentChildIndex()
    {
        return _currentChildIndex;
    }
    
    public override bool CanExecute()
    {
        return _currentChildIndex != _executedChildIndex 
            && _currentChildIndex < children.Count;
    }
    
    public override void OnChildExecuted(TaskStatus childStatus)
    {
        _executedChildIndex = _currentChildIndex;
    }
    
    public override void OnConditionalAbort(int childIndex)
    {
        _currentChildIndex = childIndex;
        _executedChildIndex = childIndex - 1;
    }
    
    private int SelectWeightedChild()
    {
        if (weights == null || weights.Length == 0)
        {
            return Random.Range(0, children.Count);
        }
        
        float totalWeight = 0f;
        for (int i = 0; i < Mathf.Min(weights.Length, children.Count); i++)
        {
            totalWeight += weights[i];
        }
        
        float randomValue = Random.Range(0f, totalWeight);
        float currentWeight = 0f;
        
        for (int i = 0; i < Mathf.Min(weights.Length, children.Count); i++)
        {
            currentWeight += weights[i];
            if (randomValue <= currentWeight)
            {
                return i;
            }
        }
        
        return 0;
    }
}
```

### Decorator Task

```csharp
[TaskCategory("Decorators")]
[TaskDescription("Repeats child until condition is false")]
public class RepeatWhile : Decorator
{
    public SharedBool condition;
    
    private TaskStatus _childStatus = TaskStatus.Inactive;
    
    public override bool CanExecute()
    {
        return condition.Value && _childStatus != TaskStatus.Running;
    }
    
    public override void OnChildExecuted(TaskStatus childStatus)
    {
        _childStatus = childStatus;
    }
    
    public override TaskStatus Decorate(TaskStatus status)
    {
        if (!condition.Value)
        {
            return TaskStatus.Success;
        }
        
        return TaskStatus.Running;
    }
    
    public override void OnEnd()
    {
        _childStatus = TaskStatus.Inactive;
    }
}
```

## Shared Variables

### Defining Shared Variables

```csharp
// In your behavior tree component or global variables
public class EnemyBehaviorVariables : MonoBehaviour
{
    [Header("References")]
    public SharedGameObject self;
    public SharedTransform selfTransform;
    public SharedGameObject currentTarget;
    
    [Header("Combat")]
    public SharedFloat attackRange = 2f;
    public SharedFloat detectionRange = 10f;
    public SharedFloat health;
    public SharedBool isInCombat;
    
    [Header("Movement")]
    public SharedVector3 homePosition;
    public SharedVector3 targetPosition;
    public SharedFloat moveSpeed = 5f;
}
```

### Custom Shared Variable Type

```csharp
[Serializable]
public class SharedAbilityData : SharedVariable<AbilityData>
{
    public static implicit operator SharedAbilityData(AbilityData value)
    {
        return new SharedAbilityData { Value = value };
    }
}

// Usage in task
public class UseAbility : Action
{
    public SharedAbilityData ability;
    
    public override TaskStatus OnUpdate()
    {
        if (ability.Value == null)
            return TaskStatus.Failure;
            
        // Use ability data
        return TaskStatus.Success;
    }
}
```

### Global Variables

```csharp
public class AIGlobalVariables : MonoBehaviour
{
    public static AIGlobalVariables Instance { get; private set; }
    
    private GlobalVariables _globalVariables;
    
    private void Awake()
    {
        Instance = this;
        _globalVariables = GlobalVariables.Instance;
    }
    
    public void SetPlayerReference(GameObject player)
    {
        _globalVariables.SetVariable("Player", (SharedGameObject)player);
    }
    
    public void SetCombatState(bool inCombat)
    {
        _globalVariables.SetVariable("GlobalCombatActive", (SharedBool)inCombat);
    }
    
    public GameObject GetPlayer()
    {
        var playerVar = _globalVariables.GetVariable("Player") as SharedGameObject;
        return playerVar?.Value;
    }
}
```

## Common Patterns

### Target Selection

```csharp
[TaskCategory("Targeting")]
public class FindClosestEnemy : Action
{
    public SharedGameObject result;
    public SharedFloat searchRadius;
    public SharedLayerMask targetLayers;
    public SharedTransform selfTransform;
    
    private Collider[] _hitColliders = new Collider[20];
    
    public override TaskStatus OnUpdate()
    {
        if (selfTransform.Value == null)
            return TaskStatus.Failure;
        
        int hitCount = Physics.OverlapSphereNonAlloc(
            selfTransform.Value.position,
            searchRadius.Value,
            _hitColliders,
            targetLayers.Value
        );
        
        if (hitCount == 0)
        {
            result.Value = null;
            return TaskStatus.Failure;
        }
        
        float closestDistance = float.MaxValue;
        GameObject closest = null;
        
        for (int i = 0; i < hitCount; i++)
        {
            var col = _hitColliders[i];
            if (col.gameObject == selfTransform.Value.gameObject)
                continue;
            
            float dist = Vector3.Distance(
                selfTransform.Value.position,
                col.transform.position
            );
            
            if (dist < closestDistance)
            {
                closestDistance = dist;
                closest = col.gameObject;
            }
        }
        
        result.Value = closest;
        return closest != null ? TaskStatus.Success : TaskStatus.Failure;
    }
}
```

### Movement Tasks

```csharp
[TaskCategory("Movement")]
public class MoveToTarget : Action
{
    public SharedGameObject target;
    public SharedFloat stoppingDistance = 1f;
    public SharedFloat moveSpeed = 5f;
    
    private IAstarAI _ai;
    private Transform _transform;
    
    public override void OnStart()
    {
        _ai = GetComponent<IAstarAI>();
        _transform = transform;
    }
    
    public override TaskStatus OnUpdate()
    {
        if (target.Value == null)
            return TaskStatus.Failure;
        
        if (_ai != null)
        {
            _ai.destination = target.Value.transform.position;
            
            if (_ai.reachedEndOfPath)
                return TaskStatus.Success;
                
            return TaskStatus.Running;
        }
        
        // Fallback simple movement
        Vector3 direction = (target.Value.transform.position - _transform.position).normalized;
        _transform.position += direction * moveSpeed.Value * Time.deltaTime;
        
        float distance = Vector3.Distance(
            _transform.position,
            target.Value.transform.position
        );
        
        return distance <= stoppingDistance.Value 
            ? TaskStatus.Success 
            : TaskStatus.Running;
    }
    
    public override void OnEnd()
    {
        if (_ai != null)
        {
            _ai.isStopped = true;
        }
    }
}
```

### Patrol Pattern

```csharp
[TaskCategory("Movement")]
public class Patrol : Action
{
    public SharedTransformList waypoints;
    public SharedInt currentWaypointIndex;
    public SharedFloat waypointReachedDistance = 1f;
    
    private IAstarAI _ai;
    
    public override void OnStart()
    {
        _ai = GetComponent<IAstarAI>();
        
        if (waypoints.Value == null || waypoints.Value.Count == 0)
        {
            return;
        }
        
        SetDestinationToCurrentWaypoint();
    }
    
    public override TaskStatus OnUpdate()
    {
        if (waypoints.Value == null || waypoints.Value.Count == 0)
            return TaskStatus.Failure;
        
        if (_ai == null)
            return TaskStatus.Failure;
        
        // Check if reached waypoint
        float distance = Vector3.Distance(
            transform.position,
            waypoints.Value[currentWaypointIndex.Value].position
        );
        
        if (distance <= waypointReachedDistance.Value)
        {
            // Move to next waypoint
            currentWaypointIndex.Value = 
                (currentWaypointIndex.Value + 1) % waypoints.Value.Count;
            SetDestinationToCurrentWaypoint();
        }
        
        return TaskStatus.Running;
    }
    
    private void SetDestinationToCurrentWaypoint()
    {
        if (_ai != null && waypoints.Value.Count > currentWaypointIndex.Value)
        {
            _ai.destination = waypoints.Value[currentWaypointIndex.Value].position;
            _ai.isStopped = false;
        }
    }
}
```

### Combat State Machine

```csharp
// Tree structure for combat AI
/*
Selector (Root)
├── Sequence [Flee when low health]
│   ├── IsHealthLow
│   └── FleeFromTarget
├── Sequence [Attack when in range]
│   ├── HasTarget
│   ├── IsTargetInRange
│   └── Selector [Choose attack]
│       ├── Sequence [Special attack if ready]
│       │   ├── IsSpecialReady
│       │   └── UseSpecialAttack
│       └── UseBasicAttack
├── Sequence [Chase target]
│   ├── HasTarget
│   └── MoveToTarget
└── Patrol [Default behavior]
*/

[TaskCategory("Combat")]
public class IsHealthLow : Conditional
{
    public SharedFloat currentHealth;
    public SharedFloat maxHealth;
    public SharedFloat lowHealthThreshold = 0.2f;
    
    public override TaskStatus OnUpdate()
    {
        float healthPercent = currentHealth.Value / maxHealth.Value;
        return healthPercent <= lowHealthThreshold.Value 
            ? TaskStatus.Success 
            : TaskStatus.Failure;
    }
}
```

## Conditional Aborts

### Self Abort Pattern

```csharp
// Use AbortType.Self to re-evaluate when conditions change
[TaskCategory("Combat")]
public class HasTarget : Conditional
{
    public SharedGameObject target;
    
    // Set abort type in inspector to Self
    // This will re-evaluate the branch when target changes
    
    public override TaskStatus OnUpdate()
    {
        return target.Value != null 
            ? TaskStatus.Success 
            : TaskStatus.Failure;
    }
}
```

### Lower Priority Abort

```csharp
// Use AbortType.LowerPriority to interrupt lower priority branches
[TaskCategory("Combat")]
public class IsUnderAttack : Conditional
{
    public SharedBool underAttack;
    
    // Set abort type to LowerPriority
    // Will interrupt patrol/idle when attacked
    
    public override TaskStatus OnUpdate()
    {
        return underAttack.Value 
            ? TaskStatus.Success 
            : TaskStatus.Failure;
    }
}
```

## Integration with GAS

### Ability Task Integration

```csharp
[TaskCategory("Abilities")]
public class ActivateAbilitiesByTag : Action
{
    public SharedGameObject owner;
    public SharedString abilityTag;
    public SharedBool waitForCompletion = true;
    
    private AbilitySystemComponent _asc;
    private bool _activated;
    
    public override void OnStart()
    {
        _activated = false;
        
        if (owner.Value != null)
        {
            _asc = owner.Value.GetComponent<AbilitySystemComponent>();
        }
    }
    
    public override TaskStatus OnUpdate()
    {
        if (_asc == null)
            return TaskStatus.Failure;
        
        if (!_activated)
        {
            var spec = _asc.TryActivateAbilitiesByTag(
                GameplayTag.FromString(abilityTag.Value)
            );
            
            if (spec == null)
                return TaskStatus.Failure;
            
            _activated = true;
            
            if (!waitForCompletion.Value)
                return TaskStatus.Success;
        }
        
        // Wait for ability to complete
        if (_asc.HasActiveAbilityWithTag(GameplayTag.FromString(abilityTag.Value)))
        {
            return TaskStatus.Running;
        }
        
        return TaskStatus.Success;
    }
}
```

## Debugging

### Behavior Tree Debugging

```csharp
public class BehaviorTreeDebugger : MonoBehaviour
{
    [SerializeField] private BehaviorTree _behaviorTree;
    [SerializeField] private bool _logTaskChanges = true;
    
    private void OnEnable()
    {
        if (_behaviorTree != null)
        {
            _behaviorTree.OnBehaviorStart += OnBehaviorStart;
            _behaviorTree.OnBehaviorRestart += OnBehaviorRestart;
            _behaviorTree.OnBehaviorEnd += OnBehaviorEnd;
        }
    }
    
    private void OnDisable()
    {
        if (_behaviorTree != null)
        {
            _behaviorTree.OnBehaviorStart -= OnBehaviorStart;
            _behaviorTree.OnBehaviorRestart -= OnBehaviorRestart;
            _behaviorTree.OnBehaviorEnd -= OnBehaviorEnd;
        }
    }
    
    private void OnBehaviorStart(Behavior behavior)
    {
        if (_logTaskChanges)
        {
            Debug.Log($"[BT] {name} Started");
        }
    }
    
    private void OnBehaviorRestart(Behavior behavior)
    {
        if (_logTaskChanges)
        {
            Debug.Log($"[BT] {name} Restarted");
        }
    }
    
    private void OnBehaviorEnd(Behavior behavior)
    {
        if (_logTaskChanges)
        {
            Debug.Log($"[BT] {name} Ended");
        }
    }
}
```

## Best Practices

1. **Use shared variables** - For data passing between tasks
2. **Keep tasks simple** - Single responsibility
3. **Use conditional aborts** - For responsive AI
4. **Cache component references** - In OnStart
5. **Handle null gracefully** - Return Failure on null
6. **Use task categories** - Organize custom tasks
7. **Profile behavior trees** - Can be expensive
8. **Use external trees** - For reusable behaviors
9. **Document task descriptions** - Use TaskDescription attribute
10. **Test edge cases** - Target dies, interrupted, etc.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Task never completes | Check for infinite Running state |
| Variables not synced | Verify shared variable binding |
| Abort not working | Check abort type setting |
| Performance issues | Reduce tree complexity, cache refs |
| Null reference | Add null checks in OnUpdate |
| Task not found | Check TaskCategory attribute |
