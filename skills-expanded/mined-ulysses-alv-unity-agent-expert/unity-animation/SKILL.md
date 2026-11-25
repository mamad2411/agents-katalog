---
name: unity-animation
description: >
  Unity 6000.3 LTS animation patterns. Covers Animator, Animator Controller,
  Animation Clip, Timeline, Playables API, and character animation.
  Trigger: When working with character animation, state machines,
  Timeline sequences, or Playables API in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Working with Animator Controller state machines and transitions
- Creating or manipulating Animation Clips at runtime
- Implementing character animation (humanoid or generic)
- Using Timeline for cinematic sequences or cutscenes
- Building custom animation logic with the Playables API
- Handling root motion for character movement
- Setting up animation layers and blend trees
- Controlling animation parameters from scripts
- Implementing inverse kinematics (IK) for characters
- Optimizing animation performance

## Critical Rules

### Never Modify transform Directly When Animating

```csharp
// ❌ WRONG — Fighting the animator, unpredictable behavior
transform.position = new Vector3(1, 2, 3);

// ✅ CORRECT — Let the animator drive, or disable it when needed
animator.applyRootMotion = false; // Then set position manually
rb.MovePosition(newPos); // With physics integration
```

**Why:** The Animator controls the transform hierarchy. Setting transform directly fights the animation system and causes jitter, teleportation, or stability issues.

### Update Mode Must Match Your Use Case

```csharp
// Normal mode (default) — updates with Update()
animator.updateMode = AnimatorUpdateMode.Normal;

// Animate Physics — syncs with FixedUpdate (for physics-interacting characters)
animator.updateMode = AnimatorUpdateMode.AnimatePhysics;

// Unscaled Time — ignores Time.timeScale (for UI animations)
animator.updateMode = AnimatorUpdateMode.UnscaledTime;
```

### Use Trigger Parameters for One-Shot Animations

```csharp
// ❌ WRONG — Using bool that stays true
animator.SetBool("IsJumping", true);

// ✅ CORRECT — Trigger is automatically consumed
animator.SetTrigger("Jump");
```

### Culling Mode for Performance

```csharp
// Always animate (default) — prevents popping but costs CPU
animator.cullingMode = AnimatorCullingMode.AlwaysAnimate;

// Cull Update Transforms — only render when visible
animator.cullingMode = AnimatorCullingMode.CullUpdateTransforms;

// Cull Completely — disable animation when not visible (best performance)
animator.cullingMode = AnimatorCullingMode.CullCompletely;
```

## Animator Controller

### Creating and Configuring via Script

```csharp
// Create Animator Controller at runtime
var controller = new UnityEngine.AnimatorController();
controller.AddLayer("Base Layer");
controller.AddLayer("UpperBody");

// Set up parameters
controller.AddParameter("Speed", AnimatorControllerParameterType.Float);
controller.AddParameter("Jump", AnimatorControllerParameterType.Trigger);
controller.AddParameter("IsGrounded", AnimatorControllerParameterType.Bool);

// Get layer and state machine
var baseLayer = controller.layers[0];
var stateMachine = baseLayer.stateMachine;

// Create states
var idleState = stateMachine.AddState("Idle");
idleState.motion = idleClip;

var walkState = stateMachine.AddState("Walk");
walkState.motion = walkClip;

// Create transitions
var transition = idleState.AddTransition(walkState);
transition.AddCondition(AnimatorConditionMode.Greater, 0.1f, "Speed");
transition.duration = 0.1f;

var walkToIdle = walkState.AddTransition(idleState);
walkToIdle.AddCondition(AnimatorConditionMode.Less, 0.1f, "Speed");
walkToIdle.duration = 0.1f;
```

### State Machine Basics

```csharp
public class CharacterAnimator : MonoBehaviour
{
    private Animator _animator;
    private Rigidbody _rb;
    private static readonly int Speed = Animator.StringToHash("Speed");
    private static readonly int Jump = Animator.StringToHash("Jump");
    private static readonly int IsGrounded = Animator.StringToHash("IsGrounded");

    [SerializeField] private float groundCheckRadius = 0.2f;
    [SerializeField] private LayerMask groundLayer;

    private void Awake()
    {
        _animator = GetComponent<Animator>();
        _rb = GetComponent<Rigidbody>();
    }

    private void Update()
    {
        // Read input and set parameters
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        
        Vector3 velocity = _rb.linearVelocity;
        float speed = new Vector3(velocity.x, 0, velocity.z).magnitude;
        
        _animator.SetFloat(Speed, speed);

        // Jump trigger
        if (Input.GetButtonDown("Jump") && IsGrounded())
        {
            _animator.SetTrigger(Jump);
        }

        _animator.SetBool(IsGrounded, IsGrounded());
    }

    private bool IsGrounded()
    {
        return Physics.CheckSphere(transform.position, groundCheckRadius, groundLayer);
    }
}
```

### Animation Layers

```csharp
// Layer weight — blend between layers
animator.SetLayerWeight(layerIndex, 1.0f); // Full influence
animator.SetLayerWeight(layerIndex, 0.5f); // 50% blend

// Layer blending
// Additive: Layers are combined additively (good for aiming, facial)
// Override: Default — layer replaces lower layers

// Configure via script
var layer = animator.layers[layerIndex];
layer.blendingMode = AnimatorLayerBlendingMode.Additive;
layer.weight = 1.0f;
layer.iKPass = true; // Enable IK on this layer

// Avatar Mask — control which body parts the layer affects
var mask = UnityEngine.AnimatorUtility.AddAvatarMask(
    controller,
    layerIndex,
    "UpperBodyMask" // Name of the mask
);
mask.SetHumanoidBodyPart(AvatarMaskBodyPart.Head, true);
mask.SetHumanoidBodyPart(AvatarMaskBodyPart.LeftArm, false);
// etc.
```

### Blend Trees

```csharp
// 1D Blend Tree — single parameter
var blendTree = new BlendTree();
blendTree.AddChild(idleClip, 0f);
blendTree.AddChild(walkClip, 1f);
blendTree.AddChild(runClip, 2f);
blendTree.blendParameter = "Speed";

// 2D Blend Tree — two parameters
var blend2D = new BlendTree();
blend2D.blendType = BlendTreeBlendType._2DFreeformCartesian;
blend2D.AddChild(walkForward, new Vector2(0, 1));
blend2D.AddChild(walkBack, new Vector2(0, -1));
blend2D.AddChild(strafeRight, new Vector2(1, 0));
blend2D.AddChild(strafeLeft, new Vector2(-1, 0));
blend2D.blendParameterX = "Horizontal";
blend2D.blendParameterY = "Vertical";

// Direct Blend Tree — manual control of each child weight
var direct = new BlendTree();
direct.blendType = BlendTreeBlendType.Direct;
direct.AddChild(clip1, 0.8f);
direct.AddChild(clip2, 0.2f);
```

### Sub-State Machines

```csharp
// Create sub-state machine
var subStateMachine = stateMachine.AddStateMachine("Locomotion");
var subEntry = subStateMachine.AddState("Entry");
var subIdle = subStateMachine.AddState("Idle");
var subWalk = subStateMachine.AddState("Walk");

// Connect within sub-state machine
subEntry.AddTransition(subIdle);
subIdle.AddTransition(subWalk).AddCondition(AnimatorConditionMode.Greater, 0.1f, "Speed");

// Add transition from main SM to sub-SM
var toSubSM = stateMachine.AddTransition(subStateMachine);
toSubSM.AddCondition(AnimatorConditionMode.If, 0, "LocomotionMode");

// Add transition from sub-SM back to main SM
var fromSubSM = subStateMachine.AddTransition(anotherState);
fromSubSM.hasExitTime = true;
fromSubSM.exitTime = 0.9f;
```

## Animation Clips

### Creating Animation Clips at Runtime

```csharp
public class RuntimeAnimationClip : MonoBehaviour
{
    [SerializeField] private AnimationCurve positionX;
    [SerializeField] private AnimationCurve positionY;
    [SerializeField] private AnimationCurve rotation;

    public AnimationClip CreateClip()
    {
        var clip = new AnimationClip();
        clip.name = "GeneratedClip";

        // Position keys
        var positionKeys = new ObjectReferenceKeyframe[3];
        positionKeys[0] = new ObjectReferenceKeyframe { time = 0, value = Vector3.zero };
        positionKeys[1] = new ObjectReferenceKeyframe { time = 0.5f, value = Vector3.right * 2 };
        positionKeys[2] = new ObjectReferenceKeyframe { time = 1f, value = Vector3.right * 4 };
        
        var curveBindings = EditorCurveBinding.FloatCurve(
            "myObject",
            typeof(Transform),
            "m_LocalPosition.x"
        );
        AnimationUtility.SetObjectReferenceCurve(clip, curveBindings, positionKeys);

        // Rotation keys
        var rotationKeys = new ObjectReferenceKeyframe[2];
        rotationKeys[0] = new ObjectReferenceKeyframe { time = 0, value = Quaternion.identity };
        rotationKeys[1] = new ObjectReferenceKeyframe { time = 1f, value = Quaternion.Euler(0, 90, 0) };
        
        AnimationUtility.SetObjectReferenceCurve(
            clip,
            EditorCurveBinding.FloatCurve("myObject", typeof(Transform), "m_LocalRotation.x"),
            rotationKeys
        );

        // Or use FloatCurve for float properties
        var floatCurve = new AnimationCurve(
            new Keyframe(0, 0),
            new Keyframe(0.5f, 1f),
            new Keyframe(1, 0)
        );
        AnimationUtility.SetFloatCurve(clip, curveBinding, floatCurve);

        return clip;
    }
}
```

### Animation Events

```csharp
// Define event function in your MonoBehaviour
public void OnFootstep()
{
    AudioSource.PlayClipAtPoint(footstepSound, transform.position);
}

public void OnAttackHit()
{
    // Apply damage at this frame
    damageCollider.Enable();
}

// Add events to clip at runtime (Editor only)
#if UNITY_EDITOR
public void AddEventToClip(AnimationClip clip, float time, string functionName)
{
    var eventMarker = new AnimationEvent
    {
        time = time,
        functionName = functionName,
        intParameter = 0,
        floatParameter = 0f,
        stringParameter = null,
        data = null
    };
    
    var events = AnimationUtility.GetAnimationEvents(clip);
    var newEvents = new AnimationEvent[events.Length + 1];
    Array.Copy(events, newEvents, events.Length);
    newEvents[events.Length] = eventMarker;
    AnimationUtility.SetAnimationEvents(clip, newEvents);
}
#endif
```

### Sampling and Evaluation

```csharp
// Sample an animation clip at a specific time
public void SampleAnimation(GameObject target, AnimationClip clip, float time)
{
    // Create a temporary Animator and controller
    var controller = new AnimatorController();
    var state = controller.AddState("Sample");
    state.motion = clip;
    
    var animator = target.AddComponent<Animator>();
    animator.runtimeAnimatorController = controller;
    
    animator.Update(time);
    
    // Read the sampled transform values
    Vector3 position = target.transform.position;
    Quaternion rotation = target.transform.rotation;
    
    // Clean up
    Destroy(animator);
}
```

### Animation Clip Import Settings

```csharp
// Note: These are typically set in the Inspector or via asset database
// Runtime access is limited, editor-only for most settings

// Animation compression options (import setting)
enum AnimationCompression
{
    Off,
    KeyframeReduction,
    Optimal
}

// Read clip settings
var clip = UnityEngine.AnimationClip;
clip.wrapMode = WrapMode.Loop;
clip.localRotation = Quaternion.identity; // For root transform

// Note: Most import settings are in ModelImporter, not AnimationClip itself
```

## Timeline

### Timeline Setup and Basics

```csharp
using UnityEngine;
using UnityEngine.Playables;
using UnityEngine.Timeline;

public class TimelineSetup : MonoBehaviour
{
    [SerializeField] private GameObject directorObject;

    private PlayableDirector _director;

    private void Awake()
    {
        _director = directorObject.GetComponent<PlayableDirector>();
        if (_director == null)
        {
            _director = directorObject.AddComponent<PlayableDirector>();
        }
    }

    public void CreateTimeline()
    {
        var timeline = ScriptableObject.CreateInstance<TimelineAsset>();
        timeline.name = "MyTimeline";
        
        // Set duration mode
        timeline.durationMode = TimelineDurationMode.FixedLength;
        timeline.fixedDuration = 10.0; // 10 seconds

        // Create track
        var animationTrack = timeline.CreateTrack<AnimationTrack>(null, "CharacterTrack");
        
        // Create clip
        var clip = animationTrack.CreateClip<AnimationPlayableAsset>();
        clip.start = 0;
        clip.duration = 5;
        clip.asset.clip.animationClip = walkCycleClip;

        // Assign to director
        _director.playableAsset = timeline;
    }

    public void Play() => _director.Play();
    public void Pause() => _director.Pause();
    public void Stop() => _director.Stop();

    public void SetTime(float t) => _director.time = t;
    public float GetTime() => _director.time;
    public float GetDuration() => _director.duration;
}
```

### Timeline with Multiple Tracks

```csharp
public void CreateMultiTrackTimeline()
{
    var timeline = ScriptableObject.CreateInstance<TimelineAsset>();
    
    // Animation Track (for character)
    var animTrack = timeline.CreateTrack<AnimationTrack>(null, "Character");
    var animClip = animTrack.CreateClip<AnimationPlayableAsset>();
    animClip.start = 0;
    animClip.duration = 10;
    animClip.asset.clip = characterAnimationClip;

    // Activation Track (show/hide objects)
    var activationTrack = timeline.CreateTrack<ActivationTrack>(null, "Visibility");
    var activationClip = activationTrack.CreateClip<ActivationPlayableAsset>();
    activationClip.start = 3;
    activationClip.duration = 4;
    activationClip.asset.active = true; // Show during this interval

    // Signal Track (emit events)
    var signalTrack = timeline.CreateTrack<SignalTrack>(null, "Events");
    var signalEmitter = signalTrack.CreateSignal<SignalEmitter>();
    signalEmitter.time = 5.0;
    signalEmitter.asset.once = true;

    // Audio Track
    var audioTrack = timeline.CreateTrack<AudioTrack>(null, "Music");
    var audioClip = audioTrack.CreateClip<AudioPlayableAsset>();
    audioClip.start = 0;
    audioClip.asset.audioClip = musicClip;

    // Control Track (particle systems, etc.)
    var controlTrack = timeline.CreateTrack<ControlTrack>(null, "Effects");
    var controlClip = controlTrack.CreateClip<ControlPlayableAsset>();
    controlClip.start = 2;
    controlClip.duration = 3;
    controlClip.asset.prefabGameObject = particleEffectPrefab;
}
```

### Timeline Binding

```csharp
public void BindTracks(TimelineAsset timeline, GameObject character, GameObject camera)
{
    // Get tracks
    var animTrack = timeline.GetOutputTrack(0); // First animation track
    var activationTrack = timeline.GetOutputTrack(1);
    
    // Bind GameObjects to tracks
    _director.SetGenericBinding(animTrack, character);
    _director.SetGenericBinding(activationTrack, cameraObject);
    
    // Or by track name
    var tracks = timeline.GetOutputTracks();
    foreach (var track in tracks)
    {
        if (track.name == "Character")
            _director.SetGenericBinding(track, character);
    }
}
```

### Timeline Callbacks and Control

```csharp
public class TimelineController : MonoBehaviour, ITimeControl
{
    private PlayableDirector _director;

    private void Awake()
    {
        _director = GetComponent<PlayableDirector>();
        _director.played += OnTimelinePlayed;
        _director.paused += OnTimelinePaused;
        _director.stopped += OnTimelineStopped;
        _director.timeUpdated += OnTimeUpdated;
    }

    private void OnTimelinePlayed(PlayableDirector director)
    {
        Debug.Log("Timeline started playing");
    }

    private void OnTimelinePaused(PlayableDirector director)
    {
        Debug.Log("Timeline paused");
    }

    private void OnTimelineStopped(PlayableDirector director)
    {
        Debug.Log("Timeline stopped");
    }

    private void OnTimeUpdated(PlayableDirector director)
    {
        // Called every frame with current time
    }

    // ITimeControl implementation (for tracks that need per-frame updates)
    public void SetTime(float time)
    {
        // Called by timeline system
    }

    public void OnStop(PlayableDirector director)
    {
        // Called when timeline stops
    }

    public void ProcessFrame(PlayableDirector director, FrameData info, 
        object playerData)
    {
        // Called each frame
    }
}
```

### Mixing Timeline and Script

```csharp
public class MixedTimelineControl : MonoBehaviour
{
    [SerializeField] private PlayableDirector timelineDirector;
    [SerializeField] private AnimationClip overrideClip;

    private Animator _animator;
    private float _manualBlendWeight = 0f;

    private void Awake()
    {
        _animator = GetComponent<Animator>();
    }

    private void Update()
    {
        // Check timeline progress
        if (timelineDirector.state == PlayState.Playing)
        {
            float progress = (float)(timelineDirector.time / timelineDirector.duration);
            
            // Override certain animations based on progress
            if (progress > 0.5f && progress < 0.7f)
            {
                _animator.SetLayerWeight(1, 1f);
            }
        }
    }

    // Blend from timeline to manual control
    public void BlendToManual(float duration)
    {
        StartCoroutine(BlendCoroutine(duration));
    }

    private System.Collections.IEnumerator BlendCoroutine(float duration)
    {
        float elapsed = 0f;
        while (elapsed < duration)
        {
            elapsed += Time.deltaTime;
            float t = elapsed / duration;
            _animator.SetLayerWeight(1, 1f - t);
            yield return null;
        }
        
        // After blend, disable timeline track
        timelineDirector.stopped += DisableTimelineTrack;
        timelineDirector.Stop();
    }
}
```

## Playables API

### PlayableGraph Basics

```csharp
using UnityEngine.Animations;
using UnityEngine.Playables;

public class PlayableGraphExample : MonoBehaviour
{
    private PlayableGraph _graph;
    private AnimationLayerMixerPlayable _mixer;
    private AnimationClipPlayable _clip1;
    private AnimationClipPlayable _clip2;

    public AnimationClip clip1;
    public AnimationClip clip2;

    private void Start()
    {
        // Create the graph
        _graph = PlayableGraph.Create();
        _graph.SetTimeUpdateMode(DirectorUpdateMode.GameTime);

        // Create output (connects to Animator)
        var output = AnimationPlayableOutput.Create(_graph, "Animation", GetComponent<Animator>());

        // Create mixers and clips
        _mixer = AnimationLayerMixerPlayable.Create(_graph, 2);
        _clip1 = AnimationClipPlayable.Create(_graph, clip1);
        _clip2 = AnimationClipPlayable.Create(_graph, clip2);

        // Connect to mixer
        _graph.Connect(_clip1, 0, _mixer, 0);
        _graph.Connect(_clip2, 0, _mixer, 1);

        // Set initial weights
        _mixer.SetInputWeight(0, 1f);
        _mixer.SetInputWeight(1, 0f);

        // Connect mixer to output
        output.SetSourcePlayable(_mixer);

        // Play
        _graph.Play();
    }

    private void OnDestroy()
    {
        // Clean up
        if (_graph.IsValid())
            _graph.Destroy();
    }

    // Blend between clips
    public void SetBlend(float t)
    {
        if (!_graph.IsValid()) return;
        
        _mixer.SetInputWeight(0, 1f - t);
        _mixer.SetInputWeight(1, t);
    }
}
```

### Custom Animation Playable

```csharp
public class CustomAnimationPlayable : PlayableBehaviour
{
    private Vector3 _startPosition;
    private Quaternion _startRotation;
    private float _duration;
    private bool _initialized;

    public static Playable Create(PlayableGraph graph, Vector3 startPos, 
        Quaternion startRot, float duration)
    {
        var playable = ScriptPlayable<CustomAnimationPlayable>.Create(graph, 1);
        var behaviour = playable.GetBehaviour();
        behaviour._duration = duration;
        behaviour._startPosition = startPos;
        behaviour._startRotation = startRot;
        return playable;
    }

    public override void ProcessFrame(Playable playable, FrameData info, 
        object playerData)
    {
        if (!_initialized)
        {
            _startPosition = (Vector3)playerData;
            _initialized = true;
        }

        float t = (float)(playable.GetTime() / playable.GetDuration());
        Vector3 currentPos = Vector3.Lerp(_startPosition, _startPosition + Vector3.forward, t);
        
        // Apply to transform
        var go = playerData as GameObject;
        if (go != null)
        {
            go.transform.position = currentPos;
            go.transform.rotation = Quaternion.Slerp(_startRotation, 
                _startRotation * Quaternion.Euler(0, 90, 0), t);
        }
    }
}

// Usage
var customPlayable = CustomAnimationPlayable.Create(graph, transform.position, 
    transform.rotation, 2.0f);
graph.Connect(customPlayable, 0, mixer, 2);
```

### Playable Scheduling

```csharp
public class PlayableScheduling : MonoBehaviour
{
    private PlayableGraph _graph;
    private AnimationClipPlayable _idleClip;
    private AnimationClipPlayable _walkClip;
    private AnimationClipPlayable _runClip;

    private void Start()
    {
        _graph = PlayableGraph.Create();

        // Create clips
        _idleClip = AnimationClipPlayable.Create(_graph, idleAnimation);
        _walkClip = AnimationClipPlayable.Create(_graph, walkAnimation);
        _runClip = AnimationClipPlayable.Create(_graph, runAnimation);

        // Create mixer
        var mixer = AnimationMixerPlayable.Create(_graph, 3);
        _graph.Connect(_idleClip, 0, mixer, 0);
        _graph.Connect(_walkClip, 0, mixer, 1);
        _graph.Connect(_runClip, 0, mixer, 2);

        var output = AnimationPlayableOutput.Create(_graph, "Animation", GetComponent<Animator>());
        output.SetSourcePlayable(mixer);

        // Schedule sequences
        _idleClip.SetDuration(2.0);
        _walkClip.SetDuration(3.0);
        _runClip.SetDuration(1.0);

        // Chain: idle -> walk -> run
        _idleClip.AddNotification();
        _idleClip.Play();
        
        // When idle finishes, play walk
        _idleClip.RegisterAnimationStartedCallback(OnIdleStarted);
        _walkClip.RegisterAnimationStartedCallback(OnWalkStarted);
        _runClip.RegisterAnimationStartedCallback(OnRunStarted);

        _graph.Play();
    }

    private void OnIdleStarted(Playable playable)
    {
        _walkClip.Play();
    }

    private void OnWalkStarted(Playable playable)
    {
        _runClip.Play();
    }

    private void OnRunStarted(Playable playable)
    {
        // Loop back to idle
        _idleClip.SetTime(0);
        _idleClip.Play();
    }
}
```

### Script Playable Examples

```csharp
// Blended animation with procedural override
public class ProceduralBlender : PlayableBehaviour
{
    public float BlendedSpeed { get; set; }
    public Vector3 Direction { get; set; }

    private Vector3 _blendedPosition;

    public override void PrepareData(Playable playable, FrameData info, object playerData)
    {
        // Called before ProcessFrame
        // Good for expensive computations
    }

    public override void ProcessFrame(Playable playable, FrameData info, object playerData)
    {
        if (playerData == null) return;

        // Blend between procedural and baked animation
        var animator = playerData as Animator;
        if (animator == null) return;

        // Get bone transforms for procedural adjustment
        animator.SetBoneLocalRotation(HumanBodyBones.Spine, 
            Quaternion.Euler(Direction.x * 10, 0, Direction.z * 10));
    }
}

public class ProceduralBlenderPlayable
{
    public static ScriptPlayable<ProceduralBlender> Create(
        PlayableGraph graph, 
        float blendSpeed,
        Vector3 direction)
    {
        var playable = ScriptPlayable<ProceduralBlender>.Create(graph, 1);
        var behaviour = playable.GetBehaviour();
        behaviour.BlendedSpeed = blendSpeed;
        behaviour.Direction = direction;
        return playable;
    }
}
```

## Common Patterns

### Character Locomotion

```csharp
public class CharacterLocomotion : MonoBehaviour
{
    [SerializeField] private Animator animator;
    [SerializeField] private Rigidbody rb;
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float rotationSpeed = 10f;

    private static readonly int SpeedHash = Animator.StringToHash("Speed");
    private static readonly int JumpHash = Animator.StringToHash("Jump");
    private static readonly int GroundedHash = Animator.StringToHash("Grounded");
    private static readonly int FallHash = Animator.StringToHash("Fall");

    private bool _isGrounded;
    private Vector3 _inputDirection;

    private void Update()
    {
        // Read input
        float horizontal = Input.GetAxisRaw("Horizontal");
        float vertical = Input.GetAxisRaw("Vertical");
        _inputDirection = new Vector3(horizontal, 0, vertical).normalized;

        // Update animator
        float speed = _inputDirection.magnitude * moveSpeed;
        animator.SetFloat(SpeedHash, speed, 0.1f, Time.deltaTime);

        // Jump
        if (Input.GetButtonDown("Jump") && _isGrounded)
        {
            animator.SetTrigger(JumpHash);
        }

        // Fall detection
        if (!_isGrounded && rb.linearVelocity.y < -2f)
        {
            animator.SetBool(FallHash, true);
        }
    }

    private void FixedUpdate()
    {
        // Apply root motion or manual movement
        if (animator.applyRootMotion)
        {
            // Let animator drive
        }
        else
        {
            // Manual movement
            Vector3 targetVelocity = _inputDirection * moveSpeed;
            targetVelocity.y = rb.linearVelocity.y;
            rb.linearVelocity = Vector3.Lerp(rb.linearVelocity, targetVelocity, 0.1f);
        }

        // Rotation
        if (_inputDirection != Vector3.zero)
        {
            Quaternion targetRotation = Quaternion.LookRotation(_inputDirection);
            transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, 
                rotationSpeed * Time.fixedDeltaTime);
        }
    }

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.CompareTag("Ground"))
        {
            _isGrounded = true;
            animator.SetBool(GroundedHash, true);
            animator.SetBool(FallHash, false);
        }
    }

    private void OnCollisionExit(Collision collision)
    {
        if (collision.gameObject.CompareTag("Ground"))
        {
            _isGrounded = false;
            animator.SetBool(GroundedHash, false);
        }
    }
}
```

### IK (Inverse Kinematics)

```csharp
public class CharacterIK : MonoBehaviour
{
    private Animator _animator;

    [SerializeField] private Transform leftHandTarget;
    [SerializeField] private Transform rightHandTarget;
    [SerializeField] private Transform lookTarget;
    [SerializeField] private float leftHandWeight = 1f;
    [SerializeField] private float rightHandWeight = 1f;

    private void Awake()
    {
        _animator = GetComponent<Animator>();
    }

    private void OnAnimatorIK(int layerIndex)
    {
        if (_animator == null) return;

        // Look at target
        if (lookTarget != null)
        {
            _animator.SetLookAtWeight(1f);
            _animator.SetLookAtPosition(lookTarget.position);
        }

        // Left hand IK
        if (leftHandTarget != null)
        {
            _animator.SetIKPositionWeight(AvatarIKGoal.LeftHand, leftHandWeight);
            _animator.SetIKRotationWeight(AvatarIKGoal.LeftHand, leftHandWeight);
            _animator.SetIKPosition(AvatarIKGoal.LeftHand, leftHandTarget.position);
            _animator.SetIKRotation(AvatarIKGoal.LeftHand, leftHandTarget.rotation);
        }

        // Right hand IK
        if (rightHandTarget != null)
        {
            _animator.SetIKPositionWeight(AvatarIKGoal.RightHand, rightHandWeight);
            _animator.SetIKRotationWeight(AvatarIKGoal.RightHand, rightHandWeight);
            _animator.SetIKPosition(AvatarIKGoal.RightHand, rightHandTarget.position);
            _animator.SetIKRotation(AvatarIKGoal.RightHand, rightHandTarget.rotation);
        }
    }

    // Procedural IK during specific animations
    private void ProceduralFootIK()
    {
        // Get animator
        var animator = _animator;

        // Foot IK
        float leftFootWeight = animator.GetFloat("LeftFootWeight");
        float rightFootWeight = animator.GetFloat("RightFootWeight");

        if (leftFootWeight > 0)
        {
            animator.SetIKPositionWeight(AvatarIKGoal.LeftFoot, leftFootWeight);
            animator.SetIKRotationWeight(AvatarIKGoal.LeftFoot, leftFootWeight);
            // Calculate foot position on ground...
        }
    }
}
```

### Root Motion Handling

```csharp
public class RootMotionController : MonoBehaviour
{
    private Animator _animator;
    private Rigidbody _rb;
    private Vector3 _rootMotion;

    private void Awake()
    {
        _animator = GetComponent<Animator>();
        _rb = GetComponent<Rigidbody>();
    }

    private void OnAnimatorMove()
    {
        // Called when animator moves
        // Use root motion delta
        Vector3 deltaPosition = _animator.deltaPosition;
        Quaternion deltaRotation = _animator.deltaRotation;

        // Option 1: Apply root motion to physics
        _rb.MovePosition(_rb.position + deltaPosition);
        _rb.MoveRotation(_rb.rotation * deltaRotation);

        // Option 2: Accumulate and apply manually
        _rootMotion += deltaPosition;

        // Option 3: Scale or modify root motion
        Vector3 scaledMotion = deltaPosition * movementScale;
        _rb.MovePosition(_rb.position + scaledMotion);
    }

    // Manual root motion extraction
    public Vector3 GetRootMotionDelta()
    {
        return _animator.deltaPosition;
    }

    public Quaternion GetRootRotationDelta()
    {
        return _animator.deltaRotation;
    }
}
```

### Animation State Callbacks

```csharp
public class AnimationStateCallbacks : StateMachineBehaviour
{
    // Called when entering a state
    public override void OnStateEnter(Animator animator, AnimatorStateInfo stateInfo, 
        int layerIndex)
    {
        if (stateInfo.IsName("Jump"))
        {
            // Enable jump physics or effects
        }
    }

    // Called every frame in a state
    public override void OnStateUpdate(Animator animator, AnimatorStateInfo stateInfo, 
        int layerIndex)
    {
        if (stateInfo.normalizedTime > 0.5f && stateInfo.IsName("Jump"))
        {
            // Peak of jump
        }
    }

    // Called when exiting a state
    public override void OnStateExit(Animator animator, AnimatorStateInfo stateInfo, 
        int layerIndex)
    {
        if (stateInfo.IsName("Jump"))
        {
            // Land
        }
    }

    // Called on every state machine transition
    public override void OnStateMachineEnter(Animator animator, int stateMachinePathHash)
    {
        // Entering state machine
    }

    public override void OnStateMachineExit(Animator animator, int stateMachinePathHash)
    {
        // Exiting state machine
    }

    // IK callbacks
    public override void OnStateIK(Animator animator, AnimatorStateInfo stateInfo, 
        int layerIndex)
    {
        // IK is active for this state
    }
}

// Usage: Attach to Animation Clips in the Inspector
// Or add via code:
public void AddStateMachineBehaviour(AnimatorState state)
{
    state.AddStateMachineBehaviour<AnimationStateCallbacks>();
}
```

### Blend Between Animation and Physics (Ragdoll Transition)

```csharp
public class RagdollTransition : MonoBehaviour
{
    private Animator _animator;
    private Rigidbody[] _ragdollBodies;
    private Collider[] _ragdollColliders;
    private bool _isRagdoll;
    private float _blendProgress;

    [SerializeField] private float blendSpeed = 2f;

    private void Awake()
    {
        _animator = GetComponent<Animator>();
        
        // Get all ragdoll components
        _ragdollBodies = GetComponentsInChildren<Rigidbody>();
        _ragdollColliders = GetComponentsInChildren<Collider>();
        
        // Disable ragdoll initially
        SetRagdoll(false);
    }

    public void EnableRagdoll(Vector3 hitForce)
    {
        _isRagdoll = true;
        _animator.enabled = false;
        SetRagdoll(true);

        // Apply hit force
        foreach (var rb in _ragdollBodies)
        {
            rb.linearVelocity = Vector3.zero;
            rb.AddForce(hitForce, ForceMode.Impulse);
        }
    }

    public void DisableRagdoll()
    {
        _isRagdoll = false;
        StartCoroutine(BlendBackCoroutine());
    }

    private System.Collections.IEnumerator BlendBackCoroutine()
    {
        SetRagdoll(false);
        _animator.enabled = true;

        float elapsed = 0f;
        while (elapsed < 1f / blendSpeed)
        {
            elapsed += Time.deltaTime * blendSpeed;
            float t = Mathf.Clamp01(elapsed);

            // Gradually reduce ragdoll influence
            foreach (var rb in _ragdollBodies)
            {
                rb.mass *= (1f - t);
            }

            yield return null;
        }
    }

    private void SetRagdoll(bool enabled)
    {
        foreach (var rb in _ragdollBodies)
        {
            rb.isKinematic = !enabled;
        }
        foreach (var col in _ragdollColliders)
        {
            col.enabled = enabled;
        }
    }
}
```

### Animation Layer Masking for Partial Body Animation

```csharp
public class PartialBodyAnimation : MonoBehaviour
{
    private Animator _animator;

    [SerializeField] private AvatarMask upperBodyMask;
    [SerializeField] private float blendSpeed = 5f;

    private int _baseLayerIndex;
    private int _upperBodyLayerIndex;

    private void Awake()
    {
        _animator = GetComponent<Animator>();
        
        // Find or create layers
        _baseLayerIndex = 0; // Base layer
        _upperBodyLayerIndex = 1; // Upper body layer with mask
    }

    public void BlendUpperBody(float targetWeight)
    {
        StartCoroutine(BlendLayerWeight(_upperBodyLayerIndex, targetWeight));
    }

    private System.Collections.IEnumerator BlendLayerWeight(int layer, float targetWeight)
    {
        float startWeight = _animator.GetLayerWeight(layer);
        float elapsed = 0f;

        while (Mathf.Abs(_animator.GetLayerWeight(layer) - targetWeight) > 0.01f)
        {
            elapsed += Time.deltaTime * blendSpeed;
            float t = Mathf.Clamp01(elapsed);
            float newWeight = Mathf.Lerp(startWeight, targetWeight, t);
            _animator.SetLayerWeight(layer, newWeight);
            yield return null;
        }
    }

    // Example: Shooting animation overrides upper body
    public void PlayShoot()
    {
        // Set shoot animation on upper body layer
        var state = _animator.GetCurrentAnimatorStateInfo(_upperBodyLayerIndex);
        if (!state.IsName("Shoot"))
        {
            _animator.SetTrigger("Shoot");
        }
    }
}
```

## Common Mistakes to Prevent

### Mistake 1: Forgetting to Reset Triggers

```csharp
// ❌ WRONG — Trigger stays forever
void Update()
{
    if (Input.GetButtonDown("Fire"))
        animator.SetTrigger("Fire"); // Stays true!
}

// ✅ CORRECT — Use ResetTrigger to clear, or rely on auto-reset
void Update()
{
    if (Input.GetButtonDown("Fire"))
    {
        animator.SetTrigger("Fire");
    }
    // OR
    animator.ResetTrigger("Fire"); // Manual reset
}
```

**Why:** Triggers are bools under the hood. They persist until consumed or reset.

### Mistake 2: Mismatched Update Modes

```csharp
// ❌ WRONG — Physics in Normal mode causes desync
animator.updateMode = AnimatorUpdateMode.Normal;

// ✅ CORRECT — Use AnimatePhysics for physics-coupled animation
animator.updateMode = AnimatorUpdateMode.AnimatePhysics;
```

### Mistake 3: Hardcoded Parameter Names

```csharp
// ❌ WRONG — String allocation every frame, typo-prone
animator.SetFloat("Speed", value);

// ✅ CORRECT — Cache hash
private static readonly int SpeedHash = Animator.StringToHash("Speed");
animator.SetFloat(SpeedHash, value);
```

### Mistake 4: Not Handling Missing Avatar

```csharp
// ❌ WRONG — Assumes humanoid
animator.GetBoneTransform(HumanBodyBones.LeftHand);

// ✅ CORRECT — Check for avatar
if (animator.avatar != null)
{
    var bone = animator.GetBoneTransform(HumanBodyBones.LeftHand);
}
```

### Mistake 5: Circular Dependencies in State Machine

```csharp
// ❌ WRONG — A -> B -> A with no exit time
// Causes instant oscillation

// ✅ CORRECT — Always have exit conditions or exit time
var transition = stateA.AddTransition(stateB);
transition.hasExitTime = true;
transition.exitTime = 0.8f; // Wait until 80% through animation
// OR
transition.AddCondition(AnimatorConditionMode.If, 0, "CanExit");
```

### Mistake 6: Playing Timeline Without Binding

```csharp
// ❌ WRONG — Track has no target
director.Play();

// ✅ CORRECT — Ensure bindings
var track = timeline.GetOutputTrack(0);
director.SetGenericBinding(track, targetObject);
director.Play();
```

### Mistake 7: Forgetting Playable Cleanup

```csharp
// ❌ WRONG — Memory leak
void Start()
{
    graph = PlayableGraph.Create();
    // ... use graph
} // graph never destroyed!

// ✅ CORRECT — Always clean up
void OnDestroy()
{
    if (graph.IsValid())
        graph.Destroy();
}

// Or use "using" pattern with IDisposable
```

### Mistake 8: Ignoring Animation Curves Memory

```csharp
// ❌ WRONG — Many float curves on many objects
// Each curve consumes memory

// ✅ CORRECT — Share clip data, use integer/enum for states
```

## Performance Tips

### Key Numbers

| Operation | Cost | Notes |
|-----------|------|-------|
| Animator Update (idle) | ~0.1ms | No bones, no curves |
| Animator Update (complex) | ~2-5ms | Many bones, many curves |
| AnimationClip (memory) | ~1KB-100KB | Depends on curves, keys |
| PlayableGraph (overhead) | ~0.02ms | Lightweight |
| State Transition | ~0.05ms | No I/O, pure calculation |

### Optimization Strategies

```csharp
// 1. Enable Culling for off-screen characters
animator.cullingMode = AnimatorCullingMode.CullCompletely;

// 2. Use GPU skinning for many characters (Project Settings)
// Edit > Player > Other > GPU Skinning

// 3. Optimize keyframes
// In import settings: Animation > Compression = Optimal

// 4. Reduce animation layers
// Only enable layers you're using

// 5. Use Direct blend trees instead of 1D/2D when possible
// Less computation

// 6. Disable write access when reading animations
animator.writeDefaultValuesOnDisable = false;

// 7. Use Humanoid retargeting (shares clips between characters)
// One clip, many skeletons

// 8. Avoid Animator for simple object animations
// Use LeanTween, DOTween, or simple coroutines instead
```

### LOD for Animation

```csharp
public class AnimationLOD : MonoBehaviour
{
    [SerializeField] private LODGroup lodGroup;
    private Animator _animator;

    private void Start()
    {
        _animator = GetComponent<Animator>();
        lodGroup.onLODChanged += OnLODChanged;
    }

    private void OnLODChanged(LODGroup group)
    {
        int currentLOD = GetCurrentLOD();
        
        // Simplify animation at distance
        if (currentLOD >= 2) // Far LOD
        {
            _animator.cullingMode = AnimatorCullingMode.CullCompletely;
        }
        else
        {
            _animator.cullingMode = AnimatorCullingMode.AlwaysAnimate;
        }
    }
}
```

## Cross-Reference: Unity-Physics Integration

### Animation-Physics Sync

When using physics with animation (e.g., character collision with objects):

```csharp
// Rigidbody connected to animated bone
public class ConnectedBonePhysics : MonoBehaviour
{
    [SerializeField] private ConfigurableJoint joint;
    [SerializeField] private Rigidbody connectedBody;
    [SerializeField] private Transform boneTarget;

    private void LateUpdate()
    {
        // Update joint target position to match animated bone
        joint.targetPosition = boneTarget.localPosition;
        joint.targetRotation = boneTarget.localRotation;
    }
}
```

### Ragdoll with Animation Blending

See `skills/unity-physics/` for ragdoll setup. Key integration points:

1. **Mass ratios** — Animated bones typically have mass 1. Match ragdoll parts
2. **Joint constraints** — Use spherical joints for shoulders/hips
3. **Transition timing** — Blend over 0.1-0.3s to avoid pop
4. **Collision layers** — Ragdoll should use different layer than character controller

```csharp
// Integration pattern
public class AnimatedRagdoll : MonoBehaviour
{
    [SerializeField] private Animator animator;
    [SerializeField] private Rigidbody ragdollRoot;
    [SerializeField] private float blendTime = 0.2f;

    private bool _isRagdoll;
    private float _blendTimer;

    public void EnableRagdoll(Vector3 force)
    {
        _isRagdoll = true;
        animator.enabled = false;
        
        // Enable ragdoll colliders
        SetRagdollColliders(true);
        
        // Apply force
        ragdollRoot.AddForce(force, ForceMode.Impulse);
        
        // Start blend timer
        _blendTimer = 0;
    }

    public void DisableRagdoll()
    {
        _isRagdoll = false;
        _blendTimer = 0;
        
        // Blend physics to animation
        StartCoroutine(BlendToAnimation());
    }

    private System.Collections.IEnumerator BlendToAnimation()
    {
        // Gradually reduce ragdoll influence
        while (_blendTimer < blendTime)
        {
            _blendTimer += Time.deltaTime;
            float t = _blendTimer / blendTime;

            // Ease in
            float weight = Mathf.SmoothStep(0, 1, t);
            
            // Set animator position to ragdoll position
            transform.position = ragdollRoot.position;
            transform.rotation = ragdollRoot.rotation;
            
            yield return null;
        }

        // Finalize
        SetRagdollColliders(false);
        animator.enabled = true;
    }
}
```

### Force Receiver Pattern

```csharp
// Apply external forces to animated character
public class AnimationForceReceiver : MonoBehaviour
{
    private Animator _animator;
    private Rigidbody _rb;
    private Vector3 _externalForce;
    private Vector3 _externalTorque;

    [SerializeField] private float drag = 5f;

    private void Awake()
    {
        _animator = GetComponent<Animator>();
        _rb = GetComponent<Rigidbody>();
    }

    public void AddForce(Vector3 force, ForceMode mode = ForceMode.Force)
    {
        _externalForce += force;
    }

    public void AddTorque(Vector3 torque, ForceMode mode = ForceMode.Force)
    {
        _externalTorque += torque;
    }

    private void FixedUpdate()
    {
        // Apply accumulated forces
        if (_externalForce.sqrMagnitude > 0.01f)
        {
            _rb.AddForce(_externalForce, ForceMode.Force);
            _externalForce = Vector3.zero;
        }

        if (_externalTorque.sqrMagnitude > 0.01f)
        {
            _rb.AddTorque(_externalTorque, ForceMode.Force);
            _externalTorque = Vector3.zero;
        }

        // Apply drag to angular velocity for smoother stops
        _rb.angularDrag = drag;
    }
}
```

## Response Format

When answering Unity animation questions:

1. **Always show compilable C# code** — Complete class patterns, not snippets
2. **Use Unity 6000.3 LTS API** — Verify API exists in this version
3. **Include performance considerations** — Memory, CPU, GPU implications
4. **Show the WHY** — Explain why this approach over alternatives
5. **Reference related systems** — Physics, Timeline, Playables integration
6. **Include error handling** — Null checks, validation, edge cases
7. **Provide complete patterns** — Full implementation, not just the interesting part

### Example Response Structure

```
## Solution

### Quick Answer
[2-3 sentences]

### Code Example
[Full compilable class]

### How It Works
[Explanation]

### Performance Notes
[Timing, memory considerations]

### Common Variations
[Alternative approaches]

### Integration Points
[How this connects to physics/Timeline/etc.]
```

## Quick Reference

### Parameter Setup
```csharp
Animator.StringToHash("Name")           // Cache these
Animator.SetFloat("Name", value)        // Continuous values
Animator.SetBool("Name", value)         // Toggle states
Animator.SetTrigger("Name")             // One-shot events
Animator.ResetTrigger("Name")           // Clear triggers
```

### State Info
```csharp
AnimatorStateInfo stateInfo = animator.GetCurrentAnimatorStateInfo(layer);
bool isName = stateInfo.IsName("Jump");
float normalizedTime = stateInfo.normalizedTime;
float progress = stateInfo.normalizedTime % 1; // Looped progress
```

### Transitions
```csharp
var transition = animator.CrossFade("StateName", 0.3f); // Smooth blend
animator.Play("StateName", layer, normalizedTime); // Direct jump
```

### Playables
```csharp
PlayableGraph.Create()
AnimationPlayableOutput.Create()
ScriptPlayable<T>.Create()
AnimationClipPlayable.Create()
AnimationMixerPlayable.Create()
graph.Play(); graph.Stop(); graph.Destroy()
```
