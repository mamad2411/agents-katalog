---
name: unity-physics
description: >
  Unity 6000.3 LTS physics patterns for 3D and 2D. Covers colliders, rigidbodies,
  joints, articulation bodies, character controllers, physics materials, raycasts/queries,
  layer-based collision, trigger vs collision callbacks, compound colliders, physics
  optimization, and Unity 6000-specific features (layer overrides, SimulationMode.Script,
  LowLevelPhysics2D).
  Trigger: When writing physics code in Unity, configuring colliders/rigidbodies,
  implementing joints or articulations, doing raycasts or physics queries,
  optimizing physics performance, or working with 2D physics.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Writing C# code that interacts with Unity's 3D or 2D physics system
- Configuring colliders, rigidbodies, joints, or articulation bodies
- Implementing collision or trigger callbacks
- Performing raycasts, sphere casts, box casts, or overlap queries
- Setting up physics materials (friction, bounciness)
- Building character controllers
- Optimizing physics CPU usage
- Working with 2D physics (Rigidbody2D, Collider2D, effectors, LowLevelPhysics2D)
- Using Unity 6000-specific features (layer overrides, manual simulation mode)

## Critical Rules

### Rigidbody vs Transform — NEVER Mix

```csharp
// ❌ WRONG — Teleports, bypasses physics, breaks collision detection
transform.position = newPos;
transform.rotation = newRot;

// ✅ CORRECT — Use Rigidbody for physics objects
rb.MovePosition(newPos);
rb.MoveRotation(newRot);

// ✅ OK — Teleport only when object is kinematic and you want instant reposition
rb.isKinematic = true;
transform.position = newPos;
```

**Why:** Setting `transform.position` directly on a non-kinematic Rigidbody teleports the object. The physics engine doesn't sweep the movement, so collisions are missed and other bodies react incorrectly.

### FixedUpdate for Physics, Update for Input

```csharp
// ✅ CORRECT — Read input in Update, apply in FixedUpdate
public class PlayerMovement : MonoBehaviour
{
    private Vector2 _input;
    private Rigidbody _rb;

    private void Update()
    {
        _input = new Vector2(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical"));
    }

    private void FixedUpdate()
    {
        _rb.MovePosition(_rb.position + (Vector3)_input * speed * Time.fixedDeltaTime);
    }
}
```

### ForceMode Selection

| Mode | What it does | Use when |
|------|-------------|----------|
| `ForceMode.Force` | Continuous force (mass-dependent, per-second) | Gravity-like, wind, thrust |
| `ForceMode.Impulse` | Instant force (mass-dependent) | Jump, explosion, hit |
| `ForceMode.Acceleration` | Continuous acceleration (mass-independent) | Uniform movement |
| `ForceMode.VelocityChange` | Instant velocity change (mass-independent) | Teleport-like velocity |

```csharp
// Jump — impulse (instant, mass-dependent)
rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);

// Continuous thrust — force (per-second, mass-dependent)
rb.AddForce(transform.forward * thrust, ForceMode.Force);

// Wind — acceleration (mass-independent, same for all objects)
rb.AddForce(windDirection * windStrength, ForceMode.Acceleration);
```

## Collider Types — Performance Hierarchy

**Fastest → Slowest:**

1. **Primitive** (Box, Sphere, Capsule) — Simple math, minimal memory
2. **TerrainCollider** — Heightmap-based, optimized for terrain
3. **MeshCollider** — Full triangle mesh, expensive, use only when necessary

```csharp
// ✅ Use primitive colliders whenever possible
var box = gameObject.AddComponent<BoxCollider>();
box.size = new Vector3(2, 4, 2);

// ❌ Don't use MeshCollider for simple shapes
var mesh = gameObject.AddComponent<MeshCollider>();
mesh.sharedMesh = complexMesh; // Expensive!
```

**MeshCollider rules:**
- Set `convex = true` if the object needs to move or collide with other mesh colliders
- Convex meshes limited to 255 triangles
- Non-convex MeshCollider only collides with other non-convex MeshColliders (static only)
- **CCD does NOT support MeshCollider** — only Box, Sphere, and Capsule

## Collision Detection Modes

| Mode | Swept volume? | Performance | Use for |
|------|--------------|-------------|---------|
| Discrete | No | Best | Default, slow/static objects |
| Continuous Speculative | Yes (broad-phase only) | Good | Fast objects that rarely tunnel |
| Continuous | Yes | Moderate | Fast objects, one side of collision |
| Continuous Dynamic | Yes (both sides) | Worst | Fast objects hitting other fast objects |

```csharp
// Bullet — needs continuous detection
bulletRb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
targetRb.collisionDetectionMode = CollisionDetectionMode.Continuous;

// Default — discrete is fine
defaultRb.collisionDetectionMode = CollisionDetectionMode.Discrete;
```

**Speculative CCD:** Unity 6000 default. Uses broad-phase swept volumes. May produce false positives (ghost collisions) but rarely misses real ones.

## Rigidbody Configuration

### Essential Properties

```csharp
var rb = gameObject.AddComponent<Rigidbody>();

// Mass — keep ratios under 10:1 between connected joints
rb.mass = 1.0f;

// Drag — linear resistance (0 = no resistance, infinity = instant stop)
rb.drag = 0.5f;

// Angular drag — rotational resistance
rb.angularDrag = 0.5f;

// Use gravity — affected by Physics.gravity
rb.useGravity = true;

// Is kinematic — not driven by physics, but can push others
rb.isKinematic = false;

// Interpolation — smooths visual position between physics steps
rb.interpolation = RigidbodyInterpolation.Interpolate; // Camera-followed objects
rb.interpolation = RigidbodyInterpolation.Extrapolate; // Network-predicted objects

// Collision detection
rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;

// Constraints — freeze axes to prevent unwanted movement
rb.constraints = RigidbodyConstraints.FreezeRotationX | RigidbodyConstraints.FreezeRotationZ;

// Center of mass — auto-calculated or manual
rb.centerOfMass = new Vector3(0, -0.5f, 0); // Lower COM = more stable

// Inertia tensor — auto-calculated or manual
rb.inertiaTensor = new Vector3(1, 1, 1);
rb.inertiaTensorRotation = Quaternion.identity;
```

### Unity 6000 — Layer Overrides on Rigidbody

```csharp
// Per-body collision filtering (new in Unity 6000)
rb.includeLayers = LayerMask.GetMask("Enemies", "Projectiles");
rb.excludeLayers = LayerMask.GetMask("FriendlyFire");
rb.layerOverridePriority = 1; // Higher priority wins when include/exclude conflict
```

### Unity 6000 — Manual Simulation Mode

```csharp
// Switch to manual physics simulation
Physics.simulationMode = SimulationMode.Script;

// In your game loop:
Physics.Simulate(Time.fixedDeltaTime);
```

## Trigger vs Collision Callbacks

### Collision Callbacks (Both objects have non-trigger colliders, at least one has Rigidbody)

```csharp
public class CollisionHandler : MonoBehaviour
{
    // Called on first frame of contact
    private void OnCollisionEnter(Collision collision)
    {
        foreach (ContactPoint contact in collision.contacts)
        {
            Debug.DrawRay(contact.point, contact.normal, Color.red, 2f);
        }

        if (collision.relativeVelocity.magnitude > 10f)
        {
            // High-impact collision
            PlayImpactSound(collision.relativeVelocity.magnitude);
        }
    }

    // Called every frame while in contact
    private void OnCollisionStay(Collision collision)
    {
        // Continuous contact processing
    }

    // Called when contact ends
    private void OnCollisionExit(Collision collision)
    {
        // Contact ended
    }
}
```

### Trigger Callbacks (At least one collider is a trigger)

```csharp
public class TriggerHandler : MonoBehaviour
{
    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            // Player entered trigger zone
            ActivateTrap();
        }
    }

    private void OnTriggerStay(Collider other)
    {
        // Continuous trigger overlap
    }

    private void OnTriggerExit(Collider other)
    {
        // Left trigger zone
    }
}
```

**Key differences:**
- `OnCollision*` provides `Collision` with contact points, normals, relative velocity
- `OnTrigger*` provides only the `Collider` — no contact data
- Trigger colliders do NOT generate collision responses (they pass through)
- **Both objects need colliders**, at least one needs a Rigidbody for callbacks to fire

## Physics Materials

### Friction

- Default friction: **0.6**
- Default combine mode: **Average**
- Combine priority: **Maximum > Multiply > Minimum > Average**

```csharp
var material = new PhysicMaterial();
material.dynamicFriction = 0.3f;  // Moving friction
material.staticFriction = 0.6f;   // Stationary friction
material.frictionCombine = PhysicMaterialCombine.Minimum; // Ice-like
```

**Gotcha:** PhysX multiplies friction forces for surface-area contacts (not point contacts). For large contact areas, **halve your friction values**.

### Bounciness

- Default bounciness: **0** (no bounce)
- Bounce threshold: **2** (default — relative velocity below this won't bounce)

```csharp
var bouncy = new PhysicMaterial();
bouncy.bounciness = 0.8f;
bouncy.bounceCombine = PhysicMaterialCombine.Maximum; // Super bouncy
```

### Applying Materials

```csharp
// To a collider
boxCollider.material = iceMaterial;

// To all colliders on children (compound)
foreach (var col in GetComponentsInChildren<Collider>())
{
    col.sharedMaterial = iceMaterial;
}
```

## Joints

### Joint Stability Rules

1. **Mass ratios > 10:1** between connected bodies cause jitter
2. **Spring values** that are too high cause instability
3. **Limits** should have some margin, not exact
4. Use **ConfigurableJoint** for complex constraints, simpler joints for basic needs

### HingeJoint

```csharp
var hinge = gameObject.AddComponent<HingeJoint>();
hinge.connectedBody = targetRb;

// Axis of rotation
hinge.axis = Vector3.up;

// Anchor point (local space)
hinge.anchor = Vector3.zero;

// Limits
var limits = new JointLimits
{
    min = -45f,
    max = 45f,
    bounciness = 0.2f,
    bounceMinVelocity = 0.5f
};
hinge.limits = limits;

// Motor
var motor = new JointMotor
{
    targetVelocity = 100f,
    force = 100f,
    freeSpin = false
};
hinge.motor = motor;
hinge.useMotor = true;
```

### ConfigurableJoint (most flexible)

```csharp
var config = gameObject.AddComponent<ConfigurableJoint>();
config.connectedBody = targetRb;

// Linear motion
config.xMotion = ConfigurableJointMotion.Limited;
config.yMotion = ConfigurableJointMotion.Locked;
config.zMotion = ConfigurableJointMotion.Free;

// Angular motion
config.angularXMotion = ConfigurableJointMotion.Limited;
config.angularYMotion = ConfigurableJointMotion.Locked;
config.angularZMotion = ConfigurableJointMotion.Locked;

// Linear limit
var limit = new SoftJointLimit { limit = 2f, spring = 100f, damper = 50f };
config.linearLimit = limit;

// Angular limit
var angularLimit = new SoftJointLimitLimitSpring2
{
    limit = 45f,
    spring = 100f,
    damper = 50f
};
config.angularXLimit = angularLimit;

// Target rotation/position (for driving)
config.targetRotation = Quaternion.identity;
config.targetPosition = Vector3.zero;
```

## Character Controllers

```csharp
var controller = gameObject.AddComponent<CharacterController>();
controller.height = 2f;
controller.radius = 0.5f;
controller.slopeLimit = 45f;
controller.stepOffset = 0.3f;
controller.skinWidth = 0.02f; // Small gap to prevent jitter
controller.minMoveDistance = 0.001f;

// Movement
Vector3 move = new Vector3(inputX, 0, inputZ);
move = transform.TransformDirection(move);
move *= speed;

// Apply gravity manually
velocity.y += gravity * Time.deltaTime;

controller.Move((move + velocity) * Time.deltaTime);

// Check if grounded
bool isGrounded = controller.isGrounded;

// Collision flags
var flags = controller.Move(move);
if ((flags & CollisionFlags.Below) != 0) isGrounded = true;
if ((flags & CollisionFlags.Above) != 0) HitCeiling();
if ((flags & CollisionFlags.Sides) != 0) HitWall();
```

**CharacterController vs Rigidbody:**
- CharacterController: No physics simulation, manual gravity, no mass/inertia
- Rigidbody: Full physics, automatic collision response, mass-based interactions
- Use CharacterController for player characters (predictable, no jitter)
- Use Rigidbody for physics-driven NPCs or objects

## Articulation Bodies

### Joint Types

| Joint Type | Degrees of Freedom | Use for |
|-----------|-------------------|---------|
| Fixed | 0 | Welded connections |
| Prismatic | 1 (linear) | Sliding mechanisms |
| Revolute | 1 (angular) | Hinges, wheels |
| Spherical | 3 (angular) | Ball joints |

### Drive Formula

```
force = spring × (targetPosition - currentPosition) + damping × (targetVelocity - currentVelocity)
```

```csharp
var articulation = gameObject.AddComponent<ArticulationBody>();

// Joint type
articulation.jointType = ArticulationJointType.RevoluteJoint;

// Anchor and axis
articulation.anchorPosition = Vector3.zero;
articulation.anchorRotation = Quaternion.identity;
articulation.swingAxis = Vector3.up;

// Linear limits (for prismatic)
var linearLimit = new ArticulationLinearLimit
{
    lower = -1f,
    upper = 1f
};
articulation.linearLimit = linearLimit;

// Twist limits (for revolute/spherical)
var twistLimit = new ArticulationTwistLimit
{
    lower = -90f,
    upper = 90f
};
articulation.twistLimit = twistLimit;

// Drive
var drive = new ArticulationDrive
{
    lowerLimit = -90f,
    upperLimit = 90f,
    stiffness = 1000f,
    damping = 100f,
    forceLimit = 1000f,
    target = 0f,
    targetVelocity = 0f
};
articulation.xDrive = drive;
```

### Articulation Rules

- Max hierarchy depth: **64 GameObjects**
- Each body can have only **one** ArticulationBody component
- Parent body is implicitly the connected body (no explicit connection needed)
- Uses **reduced coordinate space** — constraints are unbreakable (unlike regular joints)

## Compound Colliders

```csharp
// Create compound collider from multiple primitive colliders
void SetupCompoundCollider()
{
    // Head
    var head = new GameObject("HeadCollider");
    head.transform.SetParent(transform);
    head.transform.localPosition = new Vector3(0, 0.8f, 0);
    var headSphere = head.AddComponent<SphereCollider>();
    headSphere.radius = 0.3f;

    // Torso
    var torso = new GameObject("TorsoCollider");
    torso.transform.SetParent(transform);
    torso.transform.localPosition = new Vector3(0, 0.2f, 0);
    var torsoBox = torso.AddComponent<BoxCollider>();
    torsoBox.size = new Vector3(0.6f, 0.8f, 0.4f);

    // All colliders on the same Rigidbody form a compound collider
}
```

## Layer-Based Collision

### Editor: Physics Settings Collision Matrix

Edit > Project Settings > Physics > Layer Collision Matrix

### Runtime: Layer Mask Queries

```csharp
// Layer mask for raycast
int enemyLayer = LayerMask.NameToLayer("Enemy");
int groundLayer = LayerMask.NameToLayer("Ground");
int layerMask = (1 << enemyLayer) | (1 << groundLayer);

// Raycast only against specific layers
if (Physics.Raycast(transform.position, transform.forward, out var hit, 100f, layerMask))
{
    Debug.Log($"Hit: {hit.collider.name}");
}

// Inverse mask — raycast against everything EXCEPT these layers
int ignoreLayer = LayerMask.NameToLayer("Player");
int ignoreMask = ~(1 << ignoreLayer);

// Unity 6000 — Per-body layer overrides
rb.includeLayers = LayerMask.GetMask("Enemies", "Projectiles");
rb.excludeLayers = LayerMask.GetMask("FriendlyFire");
```

## Raycasts and Queries

### Basic Raycast

```csharp
if (Physics.Raycast(transform.position, transform.forward, out RaycastHit hit, 100f))
{
    Debug.Log($"Hit: {hit.collider.name} at distance {hit.distance}");
    Debug.Log($"Normal: {hit.normal}");
    Debug.Log($"Point: {hit.point}");
}
```

### SphereCast / BoxCast

```csharp
// SphereCast — swept sphere (good for character ground check)
if (Physics.SphereCast(transform.position, 0.5f, transform.forward, out var hit, 10f))
{
    // Hit something
}

// BoxCast — swept box (good for wide obstacles)
Vector3 boxSize = new Vector3(0.5f, 1f, 0.5f);
if (Physics.BoxCast(transform.position, boxSize, transform.forward, out var hit, transform.rotation, 10f))
{
    // Hit something
}
```

### Non-Allocating Queries (Performance Critical)

```csharp
// Pre-allocate arrays once
private RaycastHit[] _hits = new RaycastHit[16];

void Update()
{
    int count = Physics.RaycastNonAlloc(transform.position, transform.forward, _hits, 100f);
    for (int i = 0; i < count; i++)
    {
        ProcessHit(_hits[i]);
    }
}
```

### Overlap Queries

```csharp
// Sphere overlap — find all colliders in radius
Collider[] colliders = Physics.OverlapSphere(position, radius, layerMask);
foreach (var col in colliders)
{
    ApplyDamage(col.gameObject);
}

// Non-allocating overlap
private Collider[] _results = new Collider[32];

void CheckArea()
{
    int count = Physics.OverlapSphereNonAlloc(position, radius, _results, layerMask);
    for (int i = 0; i < count; i++)
    {
        ProcessCollider(_results[i]);
    }
}
```

### Batch Queries (Unity 6000)

```csharp
// Batch multiple raycasts in a single call
Ray[] rays = new Ray[10];
RaycastHit[] hits = new RaycastHit[10];

for (int i = 0; i < rays.Length; i++)
{
    rays[i] = new Ray(transform.position, transform.forward * i);
}

int count = Physics.RaycastBatch(rays, hits, 100f);
```

## 2D Physics

### Rigidbody2D Body Types

| Type | Driven by | Use for |
|------|-----------|---------|
| Dynamic | Forces, collisions | Player, enemies, physics objects |
| Kinematic | Script (MovePosition) | Platforms, moving obstacles |
| Static | Nothing | Ground, walls, level geometry |

```csharp
var rb2d = gameObject.AddComponent<Rigidbody2D>();
rb2d.bodyType = RigidbodyType2D.Dynamic;
rb2d.mass = 1f;
rb2d.gravityScale = 1f; // 0 = no gravity
rb2d.collisionDetectionMode = CollisionDetectionMode2D.Continuous;

// Movement
rb2d.MovePosition(rb2d.position + velocity * Time.fixedDeltaTime);
rb2d.AddForce(Vector2.up * jumpForce, ForceMode2D.Impulse);
```

### Collider2D Types

- **BoxCollider2D** — Rectangle
- **CircleCollider2D** — Circle
- **CapsuleCollider2D** — Capsule (vertical/horizontal)
- **EdgeCollider2D** — Line/edge (terrain, platforms)
- **PolygonCollider2D** — Arbitrary polygon (expensive)
- **TilemapCollider2D** — Auto-generated from Tilemap
- **CompositeCollider2D** — Merged colliders for performance
- **CustomCollider2D** — User-defined geometry

### 2D Effectors

```csharp
// Platform Effector — one-way platform
var platform = gameObject.AddComponent<PlatformEffector2D>();
platform.useOneWay = true;
platform.rotationalOffset = 0f; // Angle of the "top"

// Point Effector — radial force field
var point = gameObject.AddComponent<PointEffector2D>();
point.forceMagnitude = 100f;
point.forceMode = PointEffectorMode2D.Force;
point.drag = 0.5f;

// Area Effector — directional force in an area
var area = gameObject.AddComponent<AreaEffector2D>();
area.forceAngle = 90f; // Upward
area.forceMagnitude = 50f;
area.useColliderMask = true;
area.colliderMask = LayerMask.GetMask("Player");

// Surface Effector — tangential force along collider surface
var surface = gameObject.AddComponent<SurfaceEffector2D>();
surface.speed = 5f;
surface.speedVariation = 2f;
```

### 2D Joints

- **HingeJoint2D** — Rotational joint
- **SliderJoint2D** — Linear sliding joint
- **SpringJoint2D** — Spring connection
- **DistanceJoint2D** — Fixed distance
- **FixedJoint2D** — Welded connection
- **FrictionJoint2D** — Friction-based connection
- **TargetJoint2D** — Move towards target point
- **WheelJoint2D** — Wheel with suspension
- **RelativeJoint2D** — Relative position/rotation
- **CableJoint2D** — Cable-like connection

### Unity 6000 — LowLevelPhysics2D API

```csharp
// NEW: Separate 2D physics API that does NOT interact with built-in components
using UnityEngine.LowLevelPhysics2D;

// Create physics world
var world = new PhysicsWorld2D();

// Manual simulation
world.Simulate(Time.fixedDeltaTime);

// This API is completely separate from Rigidbody2D/Collider2D
// Use for custom physics simulations
```

## Physics Optimization

### CPU Optimization

```csharp
// 1. Reduce fixed timestep frequency (default 0.02 = 50Hz)
// Edit > Project Settings > Time > Fixed Timestep
// Try 0.033 (30Hz) or 0.04 (25Hz) if physics load is high

// 2. Use static colliders for non-moving objects
// Don't add Rigidbody to objects that never move

// 3. Use primitive colliders over MeshCollider
// Box/Sphere/Capsule >> MeshCollider

// 4. Reduce solver iterations only if precision isn't critical
Physics.defaultSolverIterations = 6; // Default: 6
Physics.defaultSolverVelocityIterations = 1; // Default: 1

// 5. Use sleeping — rigidbodies stop simulating when at rest
rb.sleepThreshold = 0.005f; // Default

// 6. Disable collision between layers that don't need to interact
Physics.IgnoreLayerCollision(layer1, layer2, true);

// 7. Use interpolation only on camera-followed objects
rb.interpolation = RigidbodyInterpolation.None; // Default
```

### Key Performance Numbers

| Setting | Default | Impact |
|---------|---------|--------|
| Fixed timestep | 0.02 (50Hz) | Higher = more CPU |
| Solver iterations | 6 | Higher = more stable, more CPU |
| Solver velocity iterations | 1 | Higher = more accurate, more CPU |
| Sleep threshold | 0.005 | Lower = less sleeping, more CPU |
| Bounce threshold | 2 | Lower = more bounce calculations |
| Max angular velocity | 7 | Limits rotational speed |
| Default contact offset | 0.01 | Lower = more precise, more CPU |

### Memory Optimization

```csharp
// Use shared materials instead of instance materials
collider.sharedMaterial = myPhysicMaterial; // ✅
collider.material = myPhysicMaterial; // ❌ Creates instance

// Reduce contact pairs by ignoring unnecessary layer collisions
Physics.IgnoreLayerCollision(LayerMask.NameToLayer("UI"), LayerMask.NameToLayer("Environment"));
```

## Common Patterns

### Ground Check

```csharp
public class GroundCheck : MonoBehaviour
{
    [SerializeField] private Transform _groundCheck;
    [SerializeField] private float _checkRadius = 0.2f;
    [SerializeField] private LayerMask _groundLayer;
    private bool _isGrounded;

    private void FixedUpdate()
    {
        _isGrounded = Physics2D.OverlapCircle(_groundCheck.position, _checkRadius, _groundLayer);
    }

    // 3D version
    private void FixedUpdate3D()
    {
        _isGrounded = Physics.CheckSphere(_groundCheck.position, _checkRadius, _groundLayer);
    }
}
```

### Object Pooling with Physics

```csharp
public class ProjectilePool : MonoBehaviour
{
    [SerializeField] private GameObject _prefab;
    [SerializeField] private int _poolSize = 20;
    private Queue<Rigidbody> _pool = new();

    private void Start()
    {
        for (int i = 0; i < _poolSize; i++)
        {
            var obj = Instantiate(_prefab);
            obj.SetActive(false);
            _pool.Enqueue(obj.GetComponent<Rigidbody>());
        }
    }

    public Rigidbody Get(Vector3 position, Quaternion rotation)
    {
        if (_pool.Count == 0) return null;

        var rb = _pool.Dequeue();
        rb.transform.position = position;
        rb.transform.rotation = rotation;
        rb.gameObject.SetActive(true);
        rb.velocity = Vector3.zero;
        rb.angularVelocity = Vector3.zero;
        return rb;
    }

    public void Return(Rigidbody rb)
    {
        rb.gameObject.SetActive(false);
        _pool.Enqueue(rb);
    }
}
```

### Ragdoll Stability

```csharp
// 1. Keep mass ratios under 10:1
// 2. Use appropriate joint limits
// 3. Start with small solver iterations, increase if needed
// 4. Use ConfigurableJoint for complex constraints
// 5. Test with forces gradually increasing

public class RagdollSetup : MonoBehaviour
{
    void SetupRagdoll()
    {
        // Set consistent masses
        foreach (var rb in GetComponentsInChildren<Rigidbody>())
        {
            rb.mass = Mathf.Clamp(rb.mass, 0.5f, 5f);
        }

        // Increase solver iterations for stability
        // (per-rigidbody via Physics.defaultSolverIterations)
    }
}
```

## Unity 6000-Specific Features

### Layer Overrides on Rigidbody (NEW)

```csharp
// Per-body collision filtering — overrides global layer collision matrix
Rigidbody rb = GetComponent<Rigidbody>();

// Only collide with these layers
rb.includeLayers = LayerMask.GetMask("Enemies", "Projectiles", "Ground");

// Never collide with these layers
rb.excludeLayers = LayerMask.GetMask("FriendlyFire", "Triggers");

// When include and exclude conflict, priority determines winner
rb.layerOverridePriority = 1; // Higher priority wins
```

### SimulationMode.Script (NEW)

```csharp
// Take manual control of physics simulation
Physics.simulationMode = SimulationMode.Script;

// In your game loop:
void Update()
{
    // Custom logic before simulation
    ApplyCustomForces();

    // Step physics manually
    Physics.Simulate(Time.fixedDeltaTime);

    // Custom logic after simulation
    ProcessPostSimulation();
}
```

### Physics Debug Window

`Window > Analysis > Physics Debug`

- Visualize colliders, contacts, broad-phase
- See sleep states, trigger zones
- Debug collision detection issues

### Automatic Center Of Mass / Tensor (NEW)

```csharp
// Toggle auto vs manual calculation on Rigidbody
// In inspector: "Auto Center Of Mass" and "Auto Tensor" toggles
// When disabled, you must set centerOfMass and inertiaTensor manually

rb.centerOfMass = new Vector3(0, -0.5f, 0);
rb.inertiaTensor = new Vector3(1, 2, 1);
rb.inertiaTensorRotation = Quaternion.identity;
```

### LowLevelPhysics2D (NEW)

```csharp
// Completely separate 2D physics API
// Does NOT interact with Rigidbody2D/Collider2D components
// Use for custom physics simulations, deterministic physics, etc.
using UnityEngine.LowLevelPhysics2D;
```

## Common Issues / Gotchas

| Issue | Cause | Solution |
|-------|-------|----------|
| Objects pass through each other | Fast movement + Discrete mode | Use Continuous or Continuous Speculative |
| Joint jitter | Mass ratio > 10:1 between connected bodies | Equalize masses or reduce ratio |
| Rigidbody won't move | isKinematic = true or frozen constraints | Check constraints and kinematic state |
| Collision callbacks not firing | Missing Rigidbody on both objects | At least one needs Rigidbody |
| Trigger not detecting | Both colliders are non-trigger | Set `isTrigger = true` on at least one |
| MeshCollider not colliding | Non-convex vs non-convex | Set `convex = true` for dynamic objects |
| Physics feels "floaty" | Wrong gravity scale or drag | Adjust `gravityScale`, `drag`, `angularDrag` |
| Friction not working | Using instance material instead of shared | Use `sharedMaterial` |
| CCD not working on mesh | CCD only supports Box, Sphere, Capsule | Use primitive collider for CCD objects |
| Physics stutter | Fixed timestep too high or interpolation off | Lower fixed timestep, enable interpolation |

## Best Practices

1. **Use Rigidbody for movement, NOT Transform** — `MovePosition()` / `MoveRotation()`
2. **Read input in Update, apply physics in FixedUpdate** — Consistent timing
3. **Prefer primitive colliders** — Box/Sphere/Capsule >> MeshCollider
4. **Keep mass ratios under 10:1** — Prevents joint jitter
5. **Use shared materials** — Avoid runtime material instantiation
6. **Enable interpolation only on camera-followed objects** — Performance
7. **Use non-allocating queries in hot paths** — `RaycastNonAlloc`, `OverlapSphereNonAlloc`
8. **Disable unnecessary layer collisions** — Reduces collision pairs
9. **Use static colliders for level geometry** — No Rigidbody needed
10. **Test with realistic forces** — Start small, ramp up gradually
11. **Use CharacterController for players** — Predictable, no physics jitter
12. **Profile physics CPU usage** — Use Physics Debug window to identify bottlenecks
