---
name: unity-cinemachine
description: >
  Unity 6000.3 LTS camera and Timeline patterns. Covers Cinemachine 3,
  virtual cameras, Timeline editor, and cinematic sequencing.
  Trigger: When working with cameras, cinematics, Timeline,
  or virtual camera systems in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Creating cinematic camera movements
- Setting up virtual cameras for gameplay
- Timeline-based sequences and cutscenes
- Camera blending and transitions
- Dolly tracks and mechanical camera rigs
- Integration with 2D Pixel Perfect camera

## Critical Rules

### Unity 6000 Uses Cinemachine 3
```csharp
// Cinemachine 3 (Unity 6000) - new API
using Unity.Cinemachine;

// Virtual Camera
CinemachineCamera vcam = gameObject.AddComponent<CinemachineCamera>();
vcam.Target.TrackingTarget = playerTransform;
vcam.Lens.FieldOfView = 60f;
vcam.Priority = 10;
```

### Upgrade from Cinemachine 2.X
Cinemachine 3 is newer but upgrading from 2.X requires effort. Refer to official upgrade guide.

### Timeline Requires PlayableDirector
```csharp
using Unity.Timeline;
using UnityEngine.Playables;

PlayableDirector director = GetComponent<PlayableDirector>();
director.playableAsset = timelineAsset;
director.Play();
```

## Cinemachine Components

### CinemachineCamera (CM3)
```csharp
// Basic virtual camera setup
CinemachineCamera vcam = targetGameObject.AddComponent<CinemachineCamera>();

// Aim (look at target)
CinemachineRotationComposer composer = vcam.GetOrAddComponent<CinemachineRotationComposer>();
composer.Target = playerTransform;

// Body (follow target)
CinemachineFollow follow = vcam.GetOrAddComponent<CinemachineFollow>();
follow.Target = playerTransform;
follow.Damping = Vector3.one * 0.3f;
```

### CinemachineBrain
```csharp
// Camera brain - handles blending
CinemachineBrain brain = Camera.main.GetComponent<CinemachineBrain>();
brain.DefaultBlend.m_Time = 0.5f;  // 0.5 second blend
brain.DefaultBlend.m_Style = CinemachineBlendDefinition.Style.EaseInOut;
```

### Framing Transposer (2D)
```csharp
CinemachineFramingTransposer transposer = vcam.GetCinemachineComponent<CinemachineFramingTransposer>();
transposer.Frame枕 = new Vector2(0.5f, 0.5f); // Center frame
transposer.Damping = new Vector2(0.5f, 0.5f);
transposer.adjustAspect = false;
```

## Virtual Camera Types

### Free Look Camera
```csharp
CinemachineFreeLook localVcam = gameObject.AddComponent<CinemachineFreeLook>();
localVcam.Target = playerTransform;
localVcam.Privacy = 10;

// Configure orbits
localVcam.UseDamper = true;
localVcam.Damping = new Vector3(0.5f, 0.5f, 0.5f);
```

### Stateful Camera
```csharp
// CM 3 introduces stateful cameras for better transitions
CinemachineStateDrivenCamera stateCam = gameObject.AddComponent<CinemachineStateDrivenCamera>();
stateCam.DefaultLayer = LayerMask.GetMask("Default");
```

## Timeline Integration

### Creating Timeline
```csharp
// Create timeline asset
TimelineAsset timeline = ScriptableObject.CreateInstance<TimelineAsset>();

// Create output track
var outputTrack = timeline.CreateOutputTrack("Camera Switcher", null);

// Add activation clip
var clip = outputTrack.CreateClip<ActivationPlayable>();
clip.start = 0;
clip.duration = 2;
```

### Timeline Signals
```csharp
// Emit signal from timeline
public class MySignalEmitter : MonoBehaviour
{
    [SerializeField] private SignalAsset signalAsset;

    public void RaiseSignal()
    {
        // Used in Timeline to trigger events
    }
}

// In Timeline: Add Signal Track → Add Marker → SignalEmitter
```

### Controlling Timeline from Code
```csharp
PlayableDirector director = GetComponent<PlayableDirector>();

// Play
director.Play();

// Pause
director.Pause();

// Stop and reset
director.Stop();

// Seek to time
director.time = 3.5f;
director.Evaluate();

// Control playback speed
director.playableGraph.GetRootPlayable(0).SetSpeed(0.5); // 0.5x speed
```

## Timeline Tracks

### Activation Track
```csharp
// Mute/unmute GameObjects at specific times
ActivationMixerPlayable mixer = outputTrack.CreateOutput<ActivationMixerPlayable>("Activation");
```

### Animation Track
```csharp
// Animate GameObject transforms
AnimationTrack animTrack = timeline.CreateTrack<AnimationTrack>("Animation");
var clip = animTrack.CreateClip<AnimationPlayable>();
clip.duration = 2.0;
```

### Signal Track
```csharp
// Trigger events at timeline points
SignalTrack signalTrack = timeline.CreateTrack<SignalTrack>("Signals");
```

### Playable Track
```csharp
// Custom Playable assets
public class MyPlayable : PlayableBehaviour
{
    public override void ProcessFrame(Playable playable, FrameData info, object playerData)
    {
        // Custom timeline logic
    }
}
```

## Camera Transitions

### Blend Handlers
```csharp
// Custom blend curves
CinemachineBlendDefinition blend = new CinemachineBlendDefinition();
blend.m_Style = CinemachineBlendDefinition.Style.Custom;
blend.m_CustomCurve = animationCurve; // AnimationCurve for custom blend
brain.DefaultBlend = blend;
```

### Hard Cut
```csharp
// Immediate camera switch
vcam.Priority = 100;  // Higher priority
brain.m_DefaultBlend.m_Time = 0f;  // Zero blend time
```

## 2D Specific

### Cinemachine Pixel Perfect
```csharp
// URP 2D Pixel Perfect + Cinemachine integration
// Add Cinemachine Pixel Perfect extension to virtual cameras
CinemachinePixelPerfect pixelPerfect = vcam.AddExtension<CinemachinePixelPerfect>();
pixelPerfect.CropFill = new Vector2(0.1f, 0.1f);
```

## Common Mistakes

| Mistake | Correct |
|---------|---------|
| Priority not set high enough | vcam.Priority = 10+ to activate |
| No target for follow | Set vcam.Target.TrackingTarget |
| Timeline not playing | Check PlayableDirector is enabled |
| Camera jitter | Increase damping values |
| Blend too slow | Set brain.DefaultBlend.m_Time < 0.3 |
| Forgetting to build Addressables before Player build | Pre-build Addressables content |

## Response Format

When asked about cameras, Timeline, or cinematics:

1. **Identify type**: Virtual camera, Timeline sequence, camera transition
2. **Provide Unity 6000 Cinemachine 3 patterns** (not legacy CM2)
3. **Include C# code** with correct API
4. **Reference**: `skill/reference/com.unity.cinemachine.md`, `com.unity.timeline.md`

Example response:
```
[Cinemachine] Virtual camera with follow
[C#] Using CinemachineCamera + CinemachineFollow
[Timeline] Integration with PlayableDirector
```