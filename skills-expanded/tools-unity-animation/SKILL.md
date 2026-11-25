---
name: tools-unity-animation
description: Unity animation patterns including Animancer, state machines, and performance optimization.
---

# Unity Animation

## Overview

Unity animation systems include Mecanim Animator, Animancer (3rd party), and low-level Playables API. This skill covers common patterns and optimizations.

## When to Use

- Character animations
- UI animations
- Procedural animation
- Animation blending
- State-driven animation

## Animancer Patterns

### Basic State Playing

```csharp
using Animancer;

public class CharacterAnimator : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _run;
    [SerializeField] private AnimationClip _attack;
    
    public void PlayIdle()
    {
        _animancer.Play(_idle);
    }
    
    public void PlayRun()
    {
        _animancer.Play(_run, 0.25f); // With fade
    }
    
    public void PlayAttack(Action onComplete)
    {
        var state = _animancer.Play(_attack);
        state.Events.OnEnd = () =>
        {
            PlayIdle();
            onComplete?.Invoke();
        };
    }
}
```

### Animation State Machine

```csharp
public class AnimationStateMachine : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    
    private readonly Dictionary<string, ClipTransition> _states = new();
    private string _currentState;
    
    public void RegisterState(string name, ClipTransition clip)
    {
        _states[name] = clip;
    }
    
    public void Play(string stateName, float fadeDuration = 0.25f)
    {
        if (_currentState == stateName) return;
        
        if (_states.TryGetValue(stateName, out var clip))
        {
            _animancer.Play(clip, fadeDuration);
            _currentState = stateName;
        }
    }
    
    public bool IsPlaying(string stateName) => _currentState == stateName;
}
```

### Blended Movement

```csharp
public class LocomotionAnimator : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private LinearMixerTransition _locomotion;
    
    private LinearMixerState _locomotionState;
    
    private void Awake()
    {
        _locomotionState = (LinearMixerState)_animancer.Play(_locomotion);
    }
    
    public void SetSpeed(float normalizedSpeed)
    {
        // Blend between idle (0), walk (0.5), run (1)
        _locomotionState.Parameter = normalizedSpeed;
    }
}
```

### Layer-Based Animation

```csharp
public class LayeredAnimator : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    
    private const int BaseLayer = 0;
    private const int UpperBodyLayer = 1;
    
    private void Start()
    {
        // Setup layers
        _animancer.Layers.SetCapacity(2);
        
        // Upper body layer only affects specific bones
        _animancer.Layers[UpperBodyLayer].SetMask(CreateUpperBodyMask());
    }
    
    public void PlayUpperBodyAction(AnimationClip clip)
    {
        _animancer.Layers[UpperBodyLayer].Play(clip);
    }
    
    public void StopUpperBodyLayer(float fadeDuration = 0.2f)
    {
        _animancer.Layers[UpperBodyLayer].StartFade(0, fadeDuration);
    }
    
    private AvatarMask CreateUpperBodyMask()
    {
        // Create or load avatar mask for upper body
        var mask = new AvatarMask();
        // Configure mask...
        return mask;
    }
}
```

## Mecanim Patterns

### Safe Parameter Setting

```csharp
public class SafeAnimator : MonoBehaviour
{
    private Animator _animator;
    private readonly Dictionary<string, int> _parameterHashes = new();
    private readonly HashSet<int> _validParameters = new();
    
    private void Awake()
    {
        _animator = GetComponent<Animator>();
        CacheParameters();
    }
    
    private void CacheParameters()
    {
        foreach (var param in _animator.parameters)
        {
            _parameterHashes[param.name] = param.nameHash;
            _validParameters.Add(param.nameHash);
        }
    }
    
    public void SetFloat(string name, float value)
    {
        if (TryGetHash(name, out int hash))
        {
            _animator.SetFloat(hash, value);
        }
    }
    
    public void SetBool(string name, bool value)
    {
        if (TryGetHash(name, out int hash))
        {
            _animator.SetBool(hash, value);
        }
    }
    
    public void SetTrigger(string name)
    {
        if (TryGetHash(name, out int hash))
        {
            _animator.SetTrigger(hash);
        }
    }
    
    private bool TryGetHash(string name, out int hash)
    {
        if (!_parameterHashes.TryGetValue(name, out hash))
        {
            hash = Animator.StringToHash(name);
            _parameterHashes[name] = hash;
        }
        
        return _validParameters.Contains(hash);
    }
}
```

### State Checking

```csharp
public static class AnimatorExtensions
{
    public static bool IsInState(this Animator animator, string stateName, int layer = 0)
    {
        var stateInfo = animator.GetCurrentAnimatorStateInfo(layer);
        return stateInfo.IsName(stateName);
    }
    
    public static bool IsTransitioning(this Animator animator, int layer = 0)
    {
        return animator.IsInTransition(layer);
    }
    
    public static float GetNormalizedTime(this Animator animator, int layer = 0)
    {
        var stateInfo = animator.GetCurrentAnimatorStateInfo(layer);
        return stateInfo.normalizedTime % 1f;
    }
    
    public static bool IsAnimationComplete(this Animator animator, int layer = 0)
    {
        var stateInfo = animator.GetCurrentAnimatorStateInfo(layer);
        return !stateInfo.loop && stateInfo.normalizedTime >= 1f;
    }
}
```

## Animation Events

### Safe Event Handling

```csharp
public class AnimationEventReceiver : MonoBehaviour
{
    public event Action<string> OnAnimationEvent;
    
    private readonly Dictionary<string, Action> _eventHandlers = new();
    
    public void RegisterHandler(string eventName, Action handler)
    {
        _eventHandlers[eventName] = handler;
    }
    
    public void UnregisterHandler(string eventName)
    {
        _eventHandlers.Remove(eventName);
    }
    
    // Called by animation events
    public void OnAnimEvent(string eventName)
    {
        if (_eventHandlers.TryGetValue(eventName, out var handler))
        {
            handler?.Invoke();
        }
        
        OnAnimationEvent?.Invoke(eventName);
    }
    
    // Common events
    public void FootstepLeft() => OnAnimEvent("FootstepLeft");
    public void FootstepRight() => OnAnimEvent("FootstepRight");
    public void AttackHit() => OnAnimEvent("AttackHit");
    public void AttackEnd() => OnAnimEvent("AttackEnd");
}
```

### Async Animation Waiting

```csharp
public static class AnimationAsyncExtensions
{
    public static async UniTask WaitForStateComplete(
        this Animator animator, 
        string stateName, 
        int layer = 0,
        CancellationToken ct = default)
    {
        // Wait for state to start
        while (!animator.IsInState(stateName, layer) && !ct.IsCancellationRequested)
        {
            await UniTask.Yield(ct);
        }
        
        // Wait for state to complete
        while (!animator.IsAnimationComplete(layer) && !ct.IsCancellationRequested)
        {
            await UniTask.Yield(ct);
        }
    }
    
    public static async UniTask PlayAndWait(
        this AnimancerComponent animancer,
        AnimationClip clip,
        CancellationToken ct = default)
    {
        var state = animancer.Play(clip);
        
        await UniTask.WaitUntil(
            () => state.NormalizedTime >= 1f || !state.IsPlaying,
            cancellationToken: ct
        );
    }
}
```

## Root Motion

### Controlled Root Motion

```csharp
public class RootMotionController : MonoBehaviour
{
    private Animator _animator;
    private CharacterController _controller;
    
    [SerializeField] private bool _useRootPosition = true;
    [SerializeField] private bool _useRootRotation = true;
    [SerializeField] private float _rootMotionScale = 1f;
    
    private void Awake()
    {
        _animator = GetComponent<Animator>();
        _controller = GetComponent<CharacterController>();
    }
    
    private void OnAnimatorMove()
    {
        if (_useRootPosition)
        {
            Vector3 deltaPosition = _animator.deltaPosition * _rootMotionScale;
            _controller.Move(deltaPosition);
        }
        
        if (_useRootRotation)
        {
            transform.rotation *= _animator.deltaRotation;
        }
    }
    
    public void SetRootMotionEnabled(bool position, bool rotation)
    {
        _useRootPosition = position;
        _useRootRotation = rotation;
    }
}
```

## Performance Optimization

### Animator Culling

```csharp
public class AnimatorOptimizer : MonoBehaviour
{
    private Animator _animator;
    
    private void Awake()
    {
        _animator = GetComponent<Animator>();
        
        // Configure culling based on use case
        if (IsMainCharacter())
        {
            _animator.cullingMode = AnimatorCullingMode.AlwaysAnimate;
        }
        else
        {
            _animator.cullingMode = AnimatorCullingMode.CullUpdateTransforms;
        }
    }
    
    private bool IsMainCharacter()
    {
        return CompareTag("Player");
    }
}
```

### LOD Animation

```csharp
public class AnimationLOD : MonoBehaviour
{
    private Animator _animator;
    private float _lastUpdateTime;
    
    [SerializeField] private float _nearDistance = 10f;
    [SerializeField] private float _farDistance = 30f;
    
    private Camera _mainCamera;
    
    private void Start()
    {
        _animator = GetComponent<Animator>();
        _mainCamera = Camera.main;
    }
    
    private void LateUpdate()
    {
        float distance = Vector3.Distance(transform.position, _mainCamera.transform.position);
        
        if (distance > _farDistance)
        {
            // Very far - minimal updates
            _animator.updateMode = AnimatorUpdateMode.Normal;
            _animator.speed = 0.5f; // Slow motion illusion from distance
        }
        else if (distance > _nearDistance)
        {
            // Medium distance
            _animator.updateMode = AnimatorUpdateMode.Normal;
            _animator.speed = 1f;
        }
        else
        {
            // Close - full quality
            _animator.updateMode = AnimatorUpdateMode.AnimatePhysics;
            _animator.speed = 1f;
        }
    }
}
```

### Disable When Offscreen

```csharp
public class AnimatorVisibilityOptimizer : MonoBehaviour
{
    private Animator _animator;
    private Renderer _renderer;
    
    private void Awake()
    {
        _animator = GetComponent<Animator>();
        _renderer = GetComponentInChildren<Renderer>();
    }
    
    private void OnBecameInvisible()
    {
        if (_animator != null)
        {
            _animator.enabled = false;
        }
    }
    
    private void OnBecameVisible()
    {
        if (_animator != null)
        {
            _animator.enabled = true;
        }
    }
}
```

## Best Practices

1. **Use Animancer** for flexibility over Mecanim
2. **Cache parameter hashes** - Avoid string lookups
3. **Set culling modes** appropriately
4. **Use animation events** sparingly
5. **Pool animated objects** - Avoid Instantiate
6. **Reduce bone count** for mobile
7. **Use LOD** for distant characters
8. **Disable when invisible** - Save CPU
9. **Bake animations** when possible
10. **Profile animation cost** - Major performance factor

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Animation not playing | Check Animator enabled, state exists |
| Jerky transitions | Adjust fade duration |
| Root motion drift | Verify Apply Root Motion setting |
| Parameter not found | Cache and validate parameters |
| Performance issues | Enable culling, reduce bones |
| Stuck in state | Check exit conditions, transitions |
