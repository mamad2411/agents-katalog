---
name: tools-unity-gameplay-ability-system
description: Gameplay Ability System patterns for abilities, effects, attributes, and tags including recursion safety and lifecycle management.
---

# Gameplay Ability System (GAS)

## Overview

The Gameplay Ability System provides a framework for abilities, effects, attributes, and gameplay tags. This skill covers safe implementation patterns and common pitfalls.

## When to Use

- Implementing combat abilities
- Managing gameplay effects (buffs, debuffs, damage)
- Attribute-based character stats
- Tag-based gameplay queries
- Status effect systems

## Core Components

### Component Hierarchy

```
AbilitySystemComponent (ASC)
├── Granted Abilities[]
├── Active Effects[]
├── Attribute Sets[]
└── Owned Tags[]
```

### AbilitySystemComponent

```csharp
public class AbilitySystemComponent : MonoBehaviour
{
    private List<GameplayAbilitySpec> _grantedAbilities = new();
    private List<ActiveGameplayEffect> _activeEffects = new();
    private Dictionary<string, AttributeSet> _attributeSets = new();
    private GameplayTagContainer _ownedTags = new();
    
    public IReadOnlyList<GameplayAbilitySpec> GrantedAbilities => _grantedAbilities;
    public IReadOnlyList<ActiveGameplayEffect> ActiveEffects => _activeEffects;
    public GameplayTagContainer OwnedTags => _ownedTags;
}
```

## Abilities

### Ability Specification

```csharp
[CreateAssetMenu(menuName = "GAS/Ability")]
public class GameplayAbilitySO : ScriptableObject
{
    [SerializeField] private string _abilityId;
    [SerializeField] private GameplayTagContainer _abilityTags;
    [SerializeField] private GameplayTagContainer _activationBlockedTags;
    [SerializeField] private GameplayTagContainer _activationRequiredTags;
    [SerializeField] private GameplayTagContainer _cancelAbilitiesWithTags;
    [SerializeField] private float _cooldownDuration;
    [SerializeField] private GameplayEffectSO[] _costEffects;
    [SerializeField] private GameplayEffectSO[] _applyEffects;
    
    public bool CanActivate(AbilitySystemComponent asc)
    {
        // Check cooldown
        if (asc.HasActiveEffectWithTag(_cooldownTag))
            return false;
        
        // Check blocking tags
        if (asc.OwnedTags.HasAny(_activationBlockedTags))
            return false;
        
        // Check required tags
        if (!asc.OwnedTags.HasAll(_activationRequiredTags))
            return false;
        
        // Check cost
        return CanPayCost(asc);
    }
}
```

### Ability Activation Flow

```csharp
public class AbilitySystemComponent
{
    public bool TryActivateAbility(GameplayAbilitySO ability)
    {
        if (!ability.CanActivate(this))
            return false;
        
        // Cancel conflicting abilities
        CancelAbilitiesWithTags(ability.CancelAbilitiesWithTags);
        
        // Pay cost
        ApplyCostEffects(ability);
        
        // Apply cooldown
        ApplyCooldown(ability);
        
        // Execute ability
        var spec = new GameplayAbilitySpec(ability, this);
        _activeAbilities.Add(spec);
        
        spec.Activate();
        
        return true;
    }
    
    public void EndAbility(GameplayAbilitySpec spec)
    {
        spec.End();
        _activeAbilities.Remove(spec);
    }
}
```

## Gameplay Effects

### Effect Definition

```csharp
[CreateAssetMenu(menuName = "GAS/Effect")]
public class GameplayEffectSO : ScriptableObject
{
    [SerializeField] private string _effectId;
    [SerializeField] private GameplayEffectDuration _durationType;
    [SerializeField] private float _duration;
    [SerializeField] private GameplayEffectStacking _stackingPolicy;
    [SerializeField] private int _maxStacks;
    [SerializeField] private AttributeModifier[] _modifiers;
    [SerializeField] private GameplayTagContainer _grantedTags;
    [SerializeField] private GameplayEffectSO[] _conditionalEffects;
    [SerializeField] private GameplayTagContainer _applicationRequiredTags;
    [SerializeField] private GameplayTagContainer _removalTags;
}

public enum GameplayEffectDuration
{
    Instant,
    HasDuration,
    Infinite
}

public enum GameplayEffectStacking
{
    None,
    AggregateBySource,
    AggregateByTarget
}
```

### Effect Application (Safe Pattern)

```csharp
public class AbilitySystemComponent
{
    private const int MaxRecursionDepth = 16;
    private int _effectApplicationDepth = 0;
    
    public GameplayEffectHandle ApplyEffectToSelf(GameplayEffectSO effect, GameplayEffectContext context)
    {
        return ApplyEffectToTarget(this, effect, context);
    }
    
    public GameplayEffectHandle ApplyEffectToTarget(
        AbilitySystemComponent target,
        GameplayEffectSO effect,
        GameplayEffectContext context)
    {
        // CRITICAL: Recursion guard
        if (_effectApplicationDepth >= MaxRecursionDepth)
        {
            Debug.LogError($"Effect recursion limit reached! Effect: {effect.name}");
            return GameplayEffectHandle.Invalid;
        }
        
        _effectApplicationDepth++;
        
        try
        {
            // Check application requirements
            if (!CanApplyEffect(target, effect))
                return GameplayEffectHandle.Invalid;
            
            // Handle stacking
            var existingEffect = FindExistingEffect(target, effect);
            if (existingEffect != null)
            {
                return HandleStacking(target, existingEffect, effect, context);
            }
            
            // Create new effect instance
            var activeEffect = new ActiveGameplayEffect(effect, context, Time.time);
            target._activeEffects.Add(activeEffect);
            
            // Apply modifiers
            ApplyModifiers(target, activeEffect);
            
            // Grant tags
            target._ownedTags.AddTags(effect.GrantedTags);
            
            // Apply conditional effects (recursive, but guarded)
            ApplyConditionalEffects(target, effect, context);
            
            return activeEffect.Handle;
        }
        finally
        {
            _effectApplicationDepth--;
        }
    }
    
    private void ApplyConditionalEffects(
        AbilitySystemComponent target,
        GameplayEffectSO effect,
        GameplayEffectContext context)
    {
        if (effect.ConditionalEffects == null)
            return;
        
        foreach (var conditionalEffect in effect.ConditionalEffects)
        {
            // Each conditional effect goes through the same guarded path
            ApplyEffectToTarget(target, conditionalEffect, context);
        }
    }
}
```

### Effect Removal

```csharp
public class AbilitySystemComponent
{
    public void RemoveEffect(GameplayEffectHandle handle)
    {
        var effect = _activeEffects.FirstOrDefault(e => e.Handle == handle);
        if (effect == null)
            return;
        
        // Remove modifiers
        RemoveModifiers(effect);
        
        // Remove granted tags
        _ownedTags.RemoveTags(effect.Definition.GrantedTags);
        
        // Remove from list
        _activeEffects.Remove(effect);
        
        // Return to pool if using pooling
        effect.Dispose();
    }
    
    public void RemoveEffectsWithTag(GameplayTag tag)
    {
        // Collect first to avoid modification during iteration
        var toRemove = _activeEffects
            .Where(e => e.Definition.EffectTags.HasTag(tag))
            .Select(e => e.Handle)
            .ToList();
        
        foreach (var handle in toRemove)
        {
            RemoveEffect(handle);
        }
    }
    
    public void RemoveAllEffects()
    {
        // Create copy to avoid modification during iteration
        var handles = _activeEffects.Select(e => e.Handle).ToList();
        
        foreach (var handle in handles)
        {
            RemoveEffect(handle);
        }
    }
}
```

### Effect Lifecycle Update

```csharp
public class AbilitySystemComponent
{
    private void Update()
    {
        UpdateActiveEffects(Time.deltaTime);
    }
    
    private void UpdateActiveEffects(float deltaTime)
    {
        // Use reverse iteration for safe removal
        for (int i = _activeEffects.Count - 1; i >= 0; i--)
        {
            var effect = _activeEffects[i];
            
            // Check duration
            if (effect.Definition.DurationType == GameplayEffectDuration.HasDuration)
            {
                effect.RemainingDuration -= deltaTime;
                
                if (effect.RemainingDuration <= 0)
                {
                    RemoveEffect(effect.Handle);
                    continue;
                }
            }
            
            // Check removal tags
            if (_ownedTags.HasAny(effect.Definition.RemovalTags))
            {
                RemoveEffect(effect.Handle);
                continue;
            }
            
            // Apply periodic effects
            if (effect.Definition.IsPeriodic)
            {
                effect.PeriodTimer -= deltaTime;
                if (effect.PeriodTimer <= 0)
                {
                    ExecutePeriodicEffect(effect);
                    effect.PeriodTimer = effect.Definition.Period;
                }
            }
        }
    }
}
```

## Attributes

### Attribute Definition

```csharp
public class AttributeSet
{
    private Dictionary<string, GameplayAttribute> _attributes = new();
    
    public float GetValue(string attributeName)
    {
        if (_attributes.TryGetValue(attributeName, out var attr))
            return attr.CurrentValue;
        return 0f;
    }
    
    public void SetBaseValue(string attributeName, float value)
    {
        if (_attributes.TryGetValue(attributeName, out var attr))
            attr.BaseValue = value;
    }
}

public class GameplayAttribute
{
    public string Name { get; }
    public float BaseValue { get; set; }
    public float CurrentValue => CalculateCurrentValue();
    
    private List<AttributeModifier> _modifiers = new();
    
    private float CalculateCurrentValue()
    {
        float value = BaseValue;
        
        // Apply additive modifiers
        foreach (var mod in _modifiers.Where(m => m.Operation == ModifierOperation.Add))
            value += mod.Value;
        
        // Apply multiplicative modifiers
        foreach (var mod in _modifiers.Where(m => m.Operation == ModifierOperation.Multiply))
            value *= mod.Value;
        
        // Apply override (last one wins)
        var overrides = _modifiers.Where(m => m.Operation == ModifierOperation.Override).ToList();
        if (overrides.Any())
            value = overrides.Last().Value;
        
        return value;
    }
}
```

### Attribute Modification

```csharp
public class AttributeModifier
{
    public string AttributeName { get; }
    public ModifierOperation Operation { get; }
    public float Value { get; }
    public GameplayEffectHandle SourceEffect { get; }
}

public enum ModifierOperation
{
    Add,
    Multiply,
    Override
}

// Applying modifiers from an effect
private void ApplyModifiers(AbilitySystemComponent target, ActiveGameplayEffect effect)
{
    foreach (var modDef in effect.Definition.Modifiers)
    {
        var modifier = new AttributeModifier
        {
            AttributeName = modDef.AttributeName,
            Operation = modDef.Operation,
            Value = CalculateModifierValue(modDef, effect.Context),
            SourceEffect = effect.Handle
        };
        
        target.AttributeSet.AddModifier(modifier);
    }
}
```

## Gameplay Tags

### Tag Container

```csharp
public class GameplayTagContainer
{
    private HashSet<GameplayTag> _tags = new();
    
    public bool HasTag(GameplayTag tag)
    {
        return _tags.Contains(tag) || HasParentTag(tag);
    }
    
    public bool HasAny(GameplayTagContainer other)
    {
        foreach (var tag in other._tags)
        {
            if (HasTag(tag))
                return true;
        }
        return false;
    }
    
    public bool HasAll(GameplayTagContainer other)
    {
        foreach (var tag in other._tags)
        {
            if (!HasTag(tag))
                return false;
        }
        return true;
    }
    
    public void AddTag(GameplayTag tag)
    {
        _tags.Add(tag);
    }
    
    public void RemoveTag(GameplayTag tag)
    {
        _tags.Remove(tag);
    }
    
    private bool HasParentTag(GameplayTag tag)
    {
        // Check hierarchical tags (e.g., "Status.Debuff.Stun" matches "Status.Debuff")
        var parent = tag.GetParent();
        while (parent != null)
        {
            if (_tags.Contains(parent))
                return true;
            parent = parent.GetParent();
        }
        return false;
    }
}
```

### Common Tag Patterns

```csharp
// Tag hierarchy example
"Ability.Type.Attack"
"Ability.Type.Attack.Melee"
"Ability.Type.Attack.Ranged"
"Ability.Type.Defense"
"Ability.Type.Defense.Dodge"
"Ability.Type.Defense.Block"

"Status.Buff"
"Status.Buff.Speed"
"Status.Debuff"
"Status.Debuff.Stun"
"Status.Debuff.Slow"

"State.Combat"
"State.Combat.Attacking"
"State.Combat.Blocking"
"State.Movement.Running"
"State.Movement.Jumping"
```

## Common Pitfalls & Solutions

### Pitfall 1: Effect Recursion

```csharp
// BAD: Infinite recursion
public class DamageReflectEffect : GameplayEffectSO
{
    // On damage taken, apply damage to attacker
    // Attacker has same effect, applies damage back
    // INFINITE LOOP!
}

// GOOD: Use recursion guard + source tracking
public GameplayEffectHandle ApplyEffect(...)
{
    if (_effectApplicationDepth >= MaxRecursionDepth)
    {
        Debug.LogError("Recursion limit!");
        return GameplayEffectHandle.Invalid;
    }
    
    // Also track source to prevent A→B→A chains
    if (context.SourceASC == this && effect.CanReflect)
    {
        return GameplayEffectHandle.Invalid;
    }
}
```

### Pitfall 2: Null Target References

```csharp
// BAD: Target may be destroyed
public class ProjectileAbility
{
    private AbilitySystemComponent _target;
    
    public void OnHit()
    {
        _target.ApplyEffect(damageEffect); // CRASH if target destroyed
    }
}

// GOOD: Null check or weak reference
public void OnHit()
{
    if (_target == null || _target.gameObject == null)
        return;
    
    _target.ApplyEffect(damageEffect);
}

// BETTER: Use targeting system with validity checks
public void OnHit()
{
    if (!_targetHandle.IsValid)
        return;
    
    var target = _targetHandle.GetTarget();
    target?.ApplyEffect(damageEffect);
}
```

### Pitfall 3: Modifying Collection During Iteration

```csharp
// BAD: ConcurrentModificationException
foreach (var effect in _activeEffects)
{
    if (ShouldRemove(effect))
        _activeEffects.Remove(effect); // CRASH
}

// GOOD: Reverse iteration or collect first
for (int i = _activeEffects.Count - 1; i >= 0; i--)
{
    if (ShouldRemove(_activeEffects[i]))
        RemoveEffectAt(i);
}

// OR
var toRemove = _activeEffects.Where(ShouldRemove).ToList();
foreach (var effect in toRemove)
    RemoveEffect(effect);
```

### Pitfall 4: Stack Overflow in Attribute Calculation

```csharp
// BAD: Attribute A depends on B, B depends on A
public float CalculateAttack()
{
    return BaseAttack * GetDefenseMultiplier(); // Calls CalculateDefense
}

public float CalculateDefense()
{
    return BaseDefense * GetAttackMultiplier(); // Calls CalculateAttack - LOOP!
}

// GOOD: Use dependency order or caching
private bool _isCalculating;

public float CalculateValue()
{
    if (_isCalculating)
    {
        Debug.LogWarning("Circular attribute dependency!");
        return BaseValue;
    }
    
    _isCalculating = true;
    try
    {
        return DoCalculation();
    }
    finally
    {
        _isCalculating = false;
    }
}
```

## Cleanup Patterns

### Effect Cleanup on Death/Respawn

```csharp
public void OnCharacterDeath()
{
    // Remove all effects
    RemoveAllEffects();
    
    // Clear tags
    _ownedTags.Clear();
    
    // Cancel active abilities
    foreach (var ability in _activeAbilities.ToList())
    {
        EndAbility(ability);
    }
}

public void OnCharacterRespawn()
{
    // Reset attributes to base values
    foreach (var attr in _attributeSet.Attributes)
    {
        attr.ClearModifiers();
    }
    
    // Apply default effects
    foreach (var defaultEffect in _characterDef.DefaultEffects)
    {
        ApplyEffectToSelf(defaultEffect, new GameplayEffectContext(this));
    }
}
```

### Scene/Zone Transition Cleanup

```csharp
public void OnZoneExit()
{
    // Remove zone-specific effects
    RemoveEffectsWithTag(GameplayTags.Effect_ZoneSpecific);
    
    // Keep persistent effects
    // (e.g., equipment, permanent buffs)
}
```

## Best Practices

1. **Always guard against recursion** in effect application
2. **Use handles** instead of direct references for targets
3. **Iterate safely** when modifying collections
4. **Pool effect instances** for frequently applied effects
5. **Use tags extensively** for queries instead of type checks
6. **Clear effects properly** during state transitions
7. **Log effect chains** for debugging
8. **Set reasonable stack limits** to prevent infinite stacking
9. **Test edge cases** like self-targeting, simultaneous effects
