---
name: tools-unity-cinemachine
description: Unity Cinemachine camera system patterns including virtual cameras, blending, and state-driven cameras.
---

# Unity Cinemachine

## Overview

Cinemachine is Unity's camera system for dynamic, procedural camera behavior. This skill covers common patterns for gameplay cameras, cutscenes, and camera effects.

## When to Use

- Third-person cameras
- Combat camera behavior
- Cutscene cameras
- Camera shake effects
- Multi-target framing
- State-driven camera transitions

## Basic Setup

### Virtual Camera Configuration

```csharp
using Cinemachine;

public class CameraController : MonoBehaviour
{
    [SerializeField] private CinemachineVirtualCamera _mainCamera;
    [SerializeField] private Transform _followTarget;
    [SerializeField] private Transform _lookAtTarget;
    
    private void Start()
    {
        _mainCamera.Follow = _followTarget;
        _mainCamera.LookAt = _lookAtTarget;
    }
    
    public void SetFollowTarget(Transform target)
    {
        _mainCamera.Follow = target;
    }
    
    public void SetLookAtTarget(Transform target)
    {
        _mainCamera.LookAt = target;
    }
}
```

### Third Person Camera

```csharp
public class ThirdPersonCameraSetup : MonoBehaviour
{
    [SerializeField] private CinemachineVirtualCamera _virtualCamera;
    
    private Cinemachine3rdPersonFollow _bodyComponent;
    private CinemachineComposer _aimComponent;
    
    private void Awake()
    {
        _bodyComponent = _virtualCamera.GetCinemachineComponent<Cinemachine3rdPersonFollow>();
        _aimComponent = _virtualCamera.GetCinemachineComponent<CinemachineComposer>();
    }
    
    public void SetCameraDistance(float distance)
    {
        if (_bodyComponent != null)
        {
            _bodyComponent.CameraDistance = distance;
        }
    }
    
    public void SetShoulderOffset(Vector3 offset)
    {
        if (_bodyComponent != null)
        {
            _bodyComponent.ShoulderOffset = offset;
        }
    }
    
    public void SetDamping(float damping)
    {
        if (_bodyComponent != null)
        {
            _bodyComponent.Damping.x = damping;
            _bodyComponent.Damping.y = damping;
            _bodyComponent.Damping.z = damping;
        }
    }
}
```

## Camera Blending

### Priority-Based Switching

```csharp
public class CameraPriorityManager : MonoBehaviour
{
    [SerializeField] private CinemachineVirtualCamera _explorationCamera;
    [SerializeField] private CinemachineVirtualCamera _combatCamera;
    [SerializeField] private CinemachineVirtualCamera _dialogueCamera;
    
    private const int InactivePriority = 0;
    private const int ActivePriority = 10;
    
    private void Start()
    {
        SetExplorationCamera();
    }
    
    public void SetExplorationCamera()
    {
        _explorationCamera.Priority = ActivePriority;
        _combatCamera.Priority = InactivePriority;
        _dialogueCamera.Priority = InactivePriority;
    }
    
    public void SetCombatCamera()
    {
        _explorationCamera.Priority = InactivePriority;
        _combatCamera.Priority = ActivePriority;
        _dialogueCamera.Priority = InactivePriority;
    }
    
    public void SetDialogueCamera()
    {
        _explorationCamera.Priority = InactivePriority;
        _combatCamera.Priority = InactivePriority;
        _dialogueCamera.Priority = ActivePriority;
    }
}
```

### Custom Blend Settings

```csharp
public class CameraBlendController : MonoBehaviour
{
    [SerializeField] private CinemachineBrain _brain;
    
    public void SetBlendTime(float duration)
    {
        _brain.m_DefaultBlend.m_Time = duration;
    }
    
    public void SetBlendStyle(CinemachineBlendDefinition.Style style)
    {
        _brain.m_DefaultBlend.m_Style = style;
    }
    
    public void SetInstantBlend()
    {
        _brain.m_DefaultBlend.m_Style = CinemachineBlendDefinition.Style.Cut;
    }
    
    public void SetSmoothBlend(float duration = 1f)
    {
        _brain.m_DefaultBlend.m_Style = CinemachineBlendDefinition.Style.EaseInOut;
        _brain.m_DefaultBlend.m_Time = duration;
    }
}
```

## State-Driven Camera

### Animator State Camera

```csharp
public class StateDrivenCameraController : MonoBehaviour
{
    [SerializeField] private CinemachineStateDrivenCamera _stateDrivenCamera;
    [SerializeField] private Animator _animator;
    
    private void Start()
    {
        // Animator is automatically linked via CinemachineStateDrivenCamera inspector
        // States are mapped to virtual cameras in the component
    }
    
    public void TriggerCameraState(string animatorStateName)
    {
        // Triggering animator state will automatically switch camera
        _animator.CrossFade(animatorStateName, 0.2f);
    }
}
```

### Manual State Switching

```csharp
public class GameStateCameraManager : MonoBehaviour
{
    [SerializeField] private CinemachineVirtualCamera[] _cameras;
    
    private Dictionary<GameState, CinemachineVirtualCamera> _cameraMap;
    
    private void Awake()
    {
        _cameraMap = new Dictionary<GameState, CinemachineVirtualCamera>
        {
            { GameState.Exploration, _cameras[0] },
            { GameState.Combat, _cameras[1] },
            { GameState.Dialogue, _cameras[2] },
            { GameState.Cinematic, _cameras[3] }
        };
    }
    
    public void OnGameStateChanged(GameState newState)
    {
        foreach (var cam in _cameras)
        {
            cam.Priority = 0;
        }
        
        if (_cameraMap.TryGetValue(newState, out var activeCamera))
        {
            activeCamera.Priority = 10;
        }
    }
}
```

## Camera Shake

### Impulse System

```csharp
public class CameraShakeController : MonoBehaviour
{
    [SerializeField] private CinemachineImpulseSource _impulseSource;
    [SerializeField] private CinemachineImpulseDefinition _lightImpulse;
    [SerializeField] private CinemachineImpulseDefinition _heavyImpulse;
    
    public void LightShake()
    {
        _impulseSource.m_ImpulseDefinition = _lightImpulse;
        _impulseSource.GenerateImpulse();
    }
    
    public void HeavyShake()
    {
        _impulseSource.m_ImpulseDefinition = _heavyImpulse;
        _impulseSource.GenerateImpulse();
    }
    
    public void ShakeWithVelocity(Vector3 velocity)
    {
        _impulseSource.GenerateImpulse(velocity);
    }
    
    public void DirectionalShake(Vector3 direction, float force)
    {
        _impulseSource.GenerateImpulse(direction.normalized * force);
    }
}
```

### Noise-Based Shake

```csharp
public class ContinuousShakeController : MonoBehaviour
{
    [SerializeField] private CinemachineVirtualCamera _virtualCamera;
    
    private CinemachineBasicMultiChannelPerlin _noise;
    
    private void Awake()
    {
        _noise = _virtualCamera.GetCinemachineComponent<CinemachineBasicMultiChannelPerlin>();
    }
    
    public void SetShakeIntensity(float amplitude, float frequency)
    {
        if (_noise != null)
        {
            _noise.m_AmplitudeGain = amplitude;
            _noise.m_FrequencyGain = frequency;
        }
    }
    
    public void StartCombatShake()
    {
        SetShakeIntensity(0.5f, 1f);
    }
    
    public void StopShake()
    {
        SetShakeIntensity(0f, 0f);
    }
    
    public async UniTask ShakeForDuration(float amplitude, float frequency, float duration)
    {
        SetShakeIntensity(amplitude, frequency);
        await UniTask.Delay(TimeSpan.FromSeconds(duration));
        StopShake();
    }
}
```

## Target Group

### Multi-Target Framing

```csharp
public class TargetGroupController : MonoBehaviour
{
    [SerializeField] private CinemachineTargetGroup _targetGroup;
    [SerializeField] private CinemachineVirtualCamera _groupCamera;
    
    public void AddTarget(Transform target, float weight = 1f, float radius = 1f)
    {
        _targetGroup.AddMember(target, weight, radius);
    }
    
    public void RemoveTarget(Transform target)
    {
        _targetGroup.RemoveMember(target);
    }
    
    public void SetTargetWeight(Transform target, float weight)
    {
        for (int i = 0; i < _targetGroup.m_Targets.Length; i++)
        {
            if (_targetGroup.m_Targets[i].target == target)
            {
                _targetGroup.m_Targets[i].weight = weight;
                break;
            }
        }
    }
    
    public void ClearAllTargets()
    {
        while (_targetGroup.m_Targets.Length > 0)
        {
            _targetGroup.RemoveMember(_targetGroup.m_Targets[0].target);
        }
    }
}
```

### Combat Target Group

```csharp
public class CombatCameraController : MonoBehaviour
{
    [SerializeField] private CinemachineTargetGroup _combatGroup;
    [SerializeField] private Transform _player;
    
    private readonly List<Transform> _enemies = new();
    
    public void StartCombat()
    {
        _combatGroup.AddMember(_player, 2f, 2f); // Higher weight for player
    }
    
    public void AddEnemy(Transform enemy)
    {
        _enemies.Add(enemy);
        _combatGroup.AddMember(enemy, 1f, 1f);
    }
    
    public void RemoveEnemy(Transform enemy)
    {
        _enemies.Remove(enemy);
        _combatGroup.RemoveMember(enemy);
    }
    
    public void EndCombat()
    {
        foreach (var enemy in _enemies)
        {
            _combatGroup.RemoveMember(enemy);
        }
        _enemies.Clear();
        _combatGroup.RemoveMember(_player);
    }
}
```

## Field of View

### Dynamic FOV

```csharp
public class DynamicFOVController : MonoBehaviour
{
    [SerializeField] private CinemachineVirtualCamera _virtualCamera;
    
    [SerializeField] private float _defaultFOV = 60f;
    [SerializeField] private float _sprintFOV = 70f;
    [SerializeField] private float _aimFOV = 45f;
    [SerializeField] private float _fovTransitionSpeed = 5f;
    
    private float _targetFOV;
    
    private void Start()
    {
        _targetFOV = _defaultFOV;
    }
    
    private void Update()
    {
        _virtualCamera.m_Lens.FieldOfView = Mathf.Lerp(
            _virtualCamera.m_Lens.FieldOfView,
            _targetFOV,
            Time.deltaTime * _fovTransitionSpeed
        );
    }
    
    public void SetSprintFOV()
    {
        _targetFOV = _sprintFOV;
    }
    
    public void SetAimFOV()
    {
        _targetFOV = _aimFOV;
    }
    
    public void ResetFOV()
    {
        _targetFOV = _defaultFOV;
    }
}
```

## Dolly Track

### Dolly Camera Movement

```csharp
public class DollyCameraController : MonoBehaviour
{
    [SerializeField] private CinemachineVirtualCamera _dollyCamera;
    [SerializeField] private CinemachineDollyCart _dollyCart;
    [SerializeField] private CinemachineSmoothPath _dollyPath;
    
    public void StartDollyShot(float duration)
    {
        StartCoroutine(PlayDollyShot(duration));
    }
    
    private IEnumerator PlayDollyShot(float duration)
    {
        _dollyCart.m_Position = 0f;
        _dollyCamera.Priority = 20;
        
        float elapsed = 0f;
        float pathLength = _dollyPath.PathLength;
        
        while (elapsed < duration)
        {
            elapsed += Time.deltaTime;
            float t = elapsed / duration;
            _dollyCart.m_Position = t * pathLength;
            yield return null;
        }
        
        _dollyCamera.Priority = 0;
    }
    
    public void SetDollyPosition(float normalizedPosition)
    {
        _dollyCart.m_Position = normalizedPosition * _dollyPath.PathLength;
    }
}
```

## Confiner

### Camera Bounds

```csharp
public class CameraConfinerController : MonoBehaviour
{
    [SerializeField] private CinemachineConfiner2D _confiner;
    
    public void SetBounds(Collider2D boundsCollider)
    {
        _confiner.m_BoundingShape2D = boundsCollider;
        _confiner.InvalidateCache();
    }
    
    public void ClearBounds()
    {
        _confiner.m_BoundingShape2D = null;
    }
    
    public void SetDamping(float damping)
    {
        _confiner.m_Damping = damping;
    }
}
```

## Best Practices

1. **Use virtual cameras** - Don't move main camera directly
2. **Set priorities** for camera switching
3. **Use impulse** for one-shot shakes
4. **Use noise** for continuous shake
5. **Tune damping** for smooth following
6. **Use target groups** for multi-subject framing
7. **Cache component references** on Awake
8. **Test blend times** for feel
9. **Use confiners** for bounded areas
10. **Profile camera updates** - Can be expensive

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Camera not switching | Check priorities |
| Jerky movement | Adjust damping values |
| Shake too intense | Lower amplitude gain |
| Wrong blend | Check custom blends in brain |
| Target lost | Verify Follow/LookAt assigned |
| Confiner issues | Call InvalidateCache() |
