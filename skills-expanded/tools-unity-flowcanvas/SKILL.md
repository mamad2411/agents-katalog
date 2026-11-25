---
name: tools-unity-flowcanvas
description: FlowCanvas visual scripting patterns for abilities, custom nodes, and graph execution.
---

# FlowCanvas (ParadoxNotion)

## Overview

FlowCanvas is a visual scripting solution used in Ungodly for ability graphs. This skill covers patterns for creating custom nodes, handling flow execution, and integrating with the ability system.

## When to Use

- Ability visual scripting
- Designer-friendly logic
- Complex ability sequences
- Event-driven ability flow
- Reusable ability patterns

## Core Concepts

### FlowNode Structure

```csharp
using FlowCanvas;
using ParadoxNotion.Design;

[Category("Abilities")]
[Description("Base ability flow node")]
public abstract class FN_AbilityNode : FlowNode
{
    protected AbilityFlowScriptController Controller => 
        (AbilityFlowScriptController)graph.agent;
    
    protected AbilitySystemComponent AbilitySystem => 
        Controller?.AbilitySystemComponent;
    
    protected GameplayAbilitySpec AbilitySpec => 
        Controller?.CurrentAbilitySpec;
}
```

## Custom Flow Nodes

### Action Node

```csharp
[Category("Abilities/Actions")]
[Name("Apply Damage")]
[Description("Applies damage to targets")]
public class FN_ApplyDamage : FN_AbilityNode
{
    [Input] public FlowInput enter;
    [Output] public FlowOutput exit;
    
    [Input] public ValueInput<List<GameObject>> targets;
    [Input] public ValueInput<float> baseDamage;
    [Input] public ValueInput<DamageType> damageType;
    
    [Output] public ValueOutput<int> hitCount;
    
    private int _hitCount;
    
    protected override void RegisterPorts()
    {
        enter = Input("Enter", Flow);
        exit = Output("Exit");
        
        targets = Input<List<GameObject>>("Targets");
        baseDamage = Input<float>("Base Damage", 10f);
        damageType = Input<DamageType>("Damage Type", DamageType.Physical);
        
        hitCount = Output<int>("Hit Count", () => _hitCount);
    }
    
    private void Flow(Flow f)
    {
        _hitCount = 0;
        
        var targetList = targets.value;
        if (targetList == null || targetList.Count == 0)
        {
            f.Call(exit);
            return;
        }
        
        foreach (var target in targetList)
        {
            if (target == null) continue;
            
            var damageReceiver = target.GetComponent<IDamageReceiver>();
            if (damageReceiver != null)
            {
                var damageInfo = new DamageInfo
                {
                    Damage = baseDamage.value,
                    DamageType = damageType.value,
                    Source = Controller.gameObject
                };
                
                damageReceiver.ApplyDamage(damageInfo);
                _hitCount++;
            }
        }
        
        f.Call(exit);
    }
}
```

### Wait Node (Async)

```csharp
[Category("Abilities/Flow")]
[Name("Wait For Duration")]
[Description("Waits for specified duration")]
public class FN_WaitDuration : FN_AbilityNode
{
    [Input] public FlowInput enter;
    [Output] public FlowOutput exit;
    
    [Input] public ValueInput<float> duration;
    
    private Coroutine _waitCoroutine;
    
    protected override void RegisterPorts()
    {
        enter = Input("Enter", Flow);
        exit = Output("Exit");
        
        duration = Input<float>("Duration", 1f);
    }
    
    private void Flow(Flow f)
    {
        if (_waitCoroutine != null)
        {
            Controller.StopCoroutine(_waitCoroutine);
        }
        
        _waitCoroutine = Controller.StartCoroutine(WaitRoutine(f));
    }
    
    private IEnumerator WaitRoutine(Flow f)
    {
        yield return new WaitForSeconds(duration.value);
        _waitCoroutine = null;
        f.Call(exit);
    }
    
    public override void OnGraphStoped()
    {
        if (_waitCoroutine != null)
        {
            Controller.StopCoroutine(_waitCoroutine);
            _waitCoroutine = null;
        }
    }
}
```

### UniTask Wait Node

```csharp
[Category("Abilities/Flow")]
[Name("Async Wait")]
[Description("Async wait with cancellation support")]
public class FN_AsyncWait : FN_AbilityNode
{
    [Input] public FlowInput enter;
    [Output] public FlowOutput exit;
    [Output] public FlowOutput cancelled;
    
    [Input] public ValueInput<float> duration;
    
    private CancellationTokenSource _cts;
    
    protected override void RegisterPorts()
    {
        enter = Input("Enter", Flow);
        exit = Output("Exit");
        cancelled = Output("Cancelled");
        
        duration = Input<float>("Duration", 1f);
    }
    
    private async void Flow(Flow f)
    {
        _cts?.Cancel();
        _cts = new CancellationTokenSource();
        
        try
        {
            await UniTask.Delay(
                TimeSpan.FromSeconds(duration.value),
                cancellationToken: _cts.Token
            );
            
            f.Call(exit);
        }
        catch (OperationCanceledException)
        {
            f.Call(cancelled);
        }
    }
    
    public override void OnGraphStoped()
    {
        _cts?.Cancel();
        _cts?.Dispose();
        _cts = null;
    }
}
```

### Event Node

```csharp
[Category("Abilities/Events")]
[Name("On Gameplay Event")]
[Description("Triggers on gameplay event")]
public class FN_OnGameplayEvent : FN_AbilityNode, IUpdatable
{
    [Output] public FlowOutput onEvent;
    [Output] public ValueOutput<GameplayEventData> eventData;
    
    [Input] public ValueInput<GameplayTag> eventTag;
    
    private GameplayEventData _lastEventData;
    private bool _eventReceived;
    
    protected override void RegisterPorts()
    {
        onEvent = Output("On Event");
        eventData = Output<GameplayEventData>("Event Data", () => _lastEventData);
        eventTag = Input<GameplayTag>("Event Tag");
    }
    
    public override void OnGraphStarted()
    {
        AbilitySystem.OnGameplayEvent += HandleGameplayEvent;
    }
    
    public override void OnGraphStoped()
    {
        AbilitySystem.OnGameplayEvent -= HandleGameplayEvent;
    }
    
    private void HandleGameplayEvent(GameplayEventData data)
    {
        if (data.EventTag.Matches(eventTag.value))
        {
            _lastEventData = data;
            _eventReceived = true;
        }
    }
    
    public void Update()
    {
        if (_eventReceived)
        {
            _eventReceived = false;
            onEvent.Call(new Flow());
        }
    }
}
```

## Value Nodes

### Getter Node

```csharp
[Category("Abilities/Values")]
[Name("Get Attribute")]
[Description("Gets an attribute value")]
public class FN_GetAttribute : PureFunctionNode<float>
{
    [Input] public ValueInput<AttributeType> attribute;
    [Input] public ValueInput<GameObject> target;
    
    protected override void RegisterPorts()
    {
        attribute = Input<AttributeType>("Attribute");
        target = Input<GameObject>("Target");
    }
    
    public override float Invoke()
    {
        if (target.value == null) return 0f;
        
        var attrSet = target.value.GetComponent<AttributeSet>();
        if (attrSet == null) return 0f;
        
        return attrSet.GetAttributeValue(attribute.value);
    }
}
```

### Math Node

```csharp
[Category("Abilities/Math")]
[Name("Calculate Damage")]
[Description("Calculates final damage with modifiers")]
public class FN_CalculateDamage : PureFunctionNode<float>
{
    [Input] public ValueInput<float> baseDamage;
    [Input] public ValueInput<float> attackPower;
    [Input] public ValueInput<float> damageMultiplier;
    [Input] public ValueInput<float> critMultiplier;
    [Input] public ValueInput<bool> isCrit;
    
    protected override void RegisterPorts()
    {
        baseDamage = Input<float>("Base Damage", 10f);
        attackPower = Input<float>("Attack Power", 100f);
        damageMultiplier = Input<float>("Damage Mult", 1f);
        critMultiplier = Input<float>("Crit Mult", 1.5f);
        isCrit = Input<bool>("Is Crit", false);
    }
    
    public override float Invoke()
    {
        float damage = baseDamage.value * (1 + attackPower.value / 100f);
        damage *= damageMultiplier.value;
        
        if (isCrit.value)
        {
            damage *= critMultiplier.value;
        }
        
        return Mathf.Max(0, damage);
    }
}
```

## Animation Integration

### Play Animation Node

```csharp
[Category("Abilities/Animation")]
[Name("Play Animation")]
[Description("Plays an Animancer animation")]
public class FN_PlayAnimation : FN_AbilityNode
{
    [Input] public FlowInput enter;
    [Output] public FlowOutput onComplete;
    [Output] public FlowOutput onInterrupt;
    
    [Input] public ValueInput<AnimationClip> clip;
    [Input] public ValueInput<float> fadeTime;
    [Input] public ValueInput<float> speed;
    [Input] public ValueInput<bool> waitForComplete;
    
    private AnimancerState _state;
    
    protected override void RegisterPorts()
    {
        enter = Input("Enter", Flow);
        onComplete = Output("Complete");
        onInterrupt = Output("Interrupted");
        
        clip = Input<AnimationClip>("Clip");
        fadeTime = Input<float>("Fade Time", 0.25f);
        speed = Input<float>("Speed", 1f);
        waitForComplete = Input<bool>("Wait", true);
    }
    
    private void Flow(Flow f)
    {
        var clipValue = clip.value;
        if (clipValue == null)
        {
            f.Call(onInterrupt);
            return;
        }
        
        var animancer = Controller.GetComponent<AnimancerComponent>();
        if (animancer == null)
        {
            f.Call(onInterrupt);
            return;
        }
        
        _state = animancer.Play(clipValue, fadeTime.value);
        _state.Speed = speed.value;
        
        if (waitForComplete.value)
        {
            _state.Events.OnEnd = () =>
            {
                _state = null;
                f.Call(onComplete);
            };
        }
        else
        {
            f.Call(onComplete);
        }
    }
    
    public override void OnGraphStoped()
    {
        if (_state != null && _state.IsPlaying)
        {
            _state.Stop();
            _state = null;
        }
    }
}
```

### Wait For Animation Event

```csharp
[Category("Abilities/Animation")]
[Name("Wait Animation Event")]
[Description("Waits for a specific animation event")]
public class FN_WaitAnimationEvent : FN_AbilityNode
{
    [Input] public FlowInput enter;
    [Output] public FlowOutput onEvent;
    
    [Input] public ValueInput<string> eventName;
    
    private bool _waiting;
    private Flow _currentFlow;
    
    protected override void RegisterPorts()
    {
        enter = Input("Enter", Flow);
        onEvent = Output("On Event");
        eventName = Input<string>("Event Name", "Hit");
    }
    
    private void Flow(Flow f)
    {
        _waiting = true;
        _currentFlow = f;
        
        var eventReceiver = Controller.GetComponent<AnimationEventReceiver>();
        if (eventReceiver != null)
        {
            eventReceiver.OnAnimationEvent += HandleAnimEvent;
        }
    }
    
    private void HandleAnimEvent(string name)
    {
        if (!_waiting || name != eventName.value) return;
        
        _waiting = false;
        
        var eventReceiver = Controller.GetComponent<AnimationEventReceiver>();
        if (eventReceiver != null)
        {
            eventReceiver.OnAnimationEvent -= HandleAnimEvent;
        }
        
        _currentFlow?.Call(onEvent);
    }
    
    public override void OnGraphStoped()
    {
        if (_waiting)
        {
            _waiting = false;
            var eventReceiver = Controller.GetComponent<AnimationEventReceiver>();
            eventReceiver?.OnAnimationEvent -= HandleAnimEvent;
        }
    }
}
```

## Targeting Nodes

### Find Targets Node

```csharp
[Category("Abilities/Targeting")]
[Name("Find Targets In Area")]
[Description("Finds targets in a spherical area")]
public class FN_FindTargetsInArea : FN_AbilityNode
{
    [Input] public FlowInput enter;
    [Output] public FlowOutput exit;
    [Output] public FlowOutput noTargets;
    
    [Input] public ValueInput<Vector3> center;
    [Input] public ValueInput<float> radius;
    [Input] public ValueInput<LayerMask> targetLayers;
    [Input] public ValueInput<int> maxTargets;
    
    [Output] public ValueOutput<List<GameObject>> targets;
    
    private List<GameObject> _targets = new();
    private Collider[] _hitColliders = new Collider[32];
    
    protected override void RegisterPorts()
    {
        enter = Input("Enter", Flow);
        exit = Output("Exit");
        noTargets = Output("No Targets");
        
        center = Input<Vector3>("Center");
        radius = Input<float>("Radius", 5f);
        targetLayers = Input<LayerMask>("Layers");
        maxTargets = Input<int>("Max Targets", 10);
        
        targets = Output<List<GameObject>>("Targets", () => _targets);
    }
    
    private void Flow(Flow f)
    {
        _targets.Clear();
        
        int hitCount = Physics.OverlapSphereNonAlloc(
            center.value,
            radius.value,
            _hitColliders,
            targetLayers.value
        );
        
        for (int i = 0; i < hitCount && _targets.Count < maxTargets.value; i++)
        {
            var col = _hitColliders[i];
            
            // Filter self
            if (col.gameObject == Controller.gameObject)
                continue;
            
            // Validate target
            if (col.TryGetComponent<IDamageReceiver>(out _))
            {
                _targets.Add(col.gameObject);
            }
        }
        
        if (_targets.Count > 0)
        {
            f.Call(exit);
        }
        else
        {
            f.Call(noTargets);
        }
    }
}
```

## Effect Application

### Apply Gameplay Effect Node

```csharp
[Category("Abilities/Effects")]
[Name("Apply Effect")]
[Description("Applies a gameplay effect to targets")]
public class FN_ApplyEffect : FN_AbilityNode
{
    [Input] public FlowInput enter;
    [Output] public FlowOutput exit;
    [Output] public FlowOutput failed;
    
    [Input] public ValueInput<GameplayEffectSO> effectDef;
    [Input] public ValueInput<List<GameObject>> targets;
    [Input] public ValueInput<float> level;
    
    [Output] public ValueOutput<int> appliedCount;
    
    private int _appliedCount;
    
    protected override void RegisterPorts()
    {
        enter = Input("Enter", Flow);
        exit = Output("Exit");
        failed = Output("Failed");
        
        effectDef = Input<GameplayEffectSO>("Effect");
        targets = Input<List<GameObject>>("Targets");
        level = Input<float>("Level", 1f);
        
        appliedCount = Output<int>("Applied Count", () => _appliedCount);
    }
    
    private void Flow(Flow f)
    {
        _appliedCount = 0;
        
        var effect = effectDef.value;
        var targetList = targets.value;
        
        if (effect == null || targetList == null || targetList.Count == 0)
        {
            f.Call(failed);
            return;
        }
        
        foreach (var target in targetList)
        {
            if (target == null) continue;
            
            var targetASC = target.GetComponent<AbilitySystemComponent>();
            if (targetASC == null) continue;
            
            var spec = AbilitySystem.MakeOutgoingSpec(effect, level.value);
            if (targetASC.ApplyGameplayEffect(spec))
            {
                _appliedCount++;
            }
        }
        
        if (_appliedCount > 0)
        {
            f.Call(exit);
        }
        else
        {
            f.Call(failed);
        }
    }
}
```

## MemoryPack Serialization

### Custom Formatter for FlowCanvas

```csharp
using MemoryPack;

[MemoryPackable]
public partial class SerializableFlowData
{
    public string GraphJson;
    public Dictionary<string, object> Variables;
    
    [MemoryPackConstructor]
    public SerializableFlowData(string graphJson, Dictionary<string, object> variables)
    {
        GraphJson = graphJson;
        Variables = variables;
    }
}
```

## Best Practices

1. **Inherit from FN_AbilityNode** for ability-specific nodes
2. **Handle cancellation** in OnGraphStoped
3. **Use ValueInput defaults** for optional parameters
4. **Validate inputs** before execution
5. **Clean up coroutines** and subscriptions
6. **Use async nodes** for long operations
7. **Cache component references** when possible
8. **Provide clear node names** and descriptions
9. **Use categories** for organization
10. **Test node interruption** scenarios

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Node not appearing | Check Category attribute, rebuild |
| Flow not continuing | Verify f.Call(exit) is called |
| Null reference | Add null checks for inputs |
| Memory leak | Clean up in OnGraphStoped |
| Animation stuck | Handle interruption properly |
| Variables not updating | Check port registration |
